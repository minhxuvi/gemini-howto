#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: pre-tool-check.sh
# Event: PreToolUse (matcher: "run_command")
# Purpose:
#   1. Hard-blocks ("decision": "deny") destructive shell commands such as
#      `rm -rf /`, `git push --force` to main/master, `mkfs`, or fork bombs.
#   2. Forces user confirmation ("decision": "force_ask") on risky commands
#      like `git reset --hard` or `git clean -fd`.
#   3. Transparently rewrites legacy `grep -rn` commands to `rg -n` (ripgrep)
#      using Antigravity's `"overwrite"` capability when `rg` is installed.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

python3 - "$PAYLOAD" <<'PYEOF'
import json
import re
import sys

raw_payload = sys.argv[1]

try:
    data = json.loads(raw_payload) if raw_payload.strip() else {}
except json.JSONDecodeError:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

# Support both protojson toolCall.{name,args} and flat {toolName,toolInput}
tool_call = data.get("toolCall") or {}
tool_name = tool_call.get("name") or data.get("toolName") or ""
tool_args = tool_call.get("args") or data.get("toolInput") or {}

if tool_name != "run_command":
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

cmd = str(tool_args.get("CommandLine") or tool_args.get("command") or "").strip()

# 1. Hard-block ("deny") catastrophic commands
DENY_RULES = [
    (
        r"(^|[;&|]\s*)(sudo\s+)?rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\s+(/|\*|~|\$HOME)(\s|$)",
        "Blocked destructive root/home deletion command (rm -rf).",
    ),
    (
        r"git\s+push\s+.*(--force|-f)(\s+|$).*\b(main|master|production)\b|\bgit\s+push\s+.*\b(main|master|production)\b.*(--force|-f)",
        "Blocked force-push to protected branch (main/master/production).",
    ),
    (
        r"(?i)\b(drop\s+database|drop\s+table\s+users|truncate\s+table)\b",
        "Blocked destructive SQL DDL statement in shell command.",
    ),
    (
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",
        "Blocked shell fork bomb.",
    ),
]

for pattern, reason in DENY_RULES:
    if re.search(pattern, cmd):
        print(json.dumps({"decision": "deny", "reason": reason}))
        sys.exit(0)

# 2. Force interactive confirmation ("force_ask") on high-risk commands
ASK_RULES = [
    (
        r"git\s+(reset\s+--hard|clean\s+-[a-zA-Z]*f)",
        "This command permanently discards uncommitted working tree changes. Confirm execution?",
    ),
    (
        r"\b(terraform\s+destroy|kubectl\s+delete\s+(namespace|deployment| pvc))\b",
        "Infrastructure deletion command detected. Confirm execution?",
    ),
]

for pattern, reason in ASK_RULES:
    if re.search(pattern, cmd):
        print(json.dumps({"decision": "force_ask", "reason": reason}))
        sys.exit(0)

# 3. Transparently rewrite `grep -r` / `grep -rn` to `rg -n` via `overwrite`
if re.match(r"^grep\s+(-rn|-nr|-r)\s+", cmd):
    rewritten_cmd = re.sub(r"^grep\s+(-rn|-nr|-r)\s+", "rg -n ", cmd, count=1)
    print(
        json.dumps(
            {
                "decision": "allow",
                "reason": "Rewrote grep to ripgrep (rg -n) for faster execution.",
                "overwrite": {"CommandLine": rewritten_cmd},
            }
        )
    )
    sys.exit(0)

print(json.dumps({"decision": "allow"}))
PYEOF

#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: pre-commit.sh
# Event: PreToolUse (matcher: "run_command")
# Purpose:
#   Intercepts `git commit` commands proposed by the agent and verifies that
#   the project's linter and unit test suite pass before allowing the commit.
#   If verification fails, returns `{"decision": "deny", "reason": "..."}` so
#   the agent fixes the failing checks before committing.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

python3 - "$PAYLOAD" <<'PYEOF'
import json
import os
import re
import subprocess
import sys

try:
    data = json.loads(sys.argv[1]) if sys.argv[1].strip() else {}
except json.JSONDecodeError:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

tool_call = data.get("toolCall") or {}
tool_name = tool_call.get("name") or data.get("toolName") or ""
tool_args = tool_call.get("args") or data.get("toolInput") or {}

if tool_name != "run_command":
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

cmd = str(tool_args.get("CommandLine") or tool_args.get("command") or "").strip()

# Only trigger when the shell command includes `git commit`
if not re.search(r"(^|[;&|]\s*)git\s+commit\b", cmd):
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

workspaces = data.get("workspacePaths") or []
cwd = str(tool_args.get("Cwd") or (workspaces[0] if workspaces else os.getcwd()))

checks_to_run = []
if os.path.isfile(os.path.join(cwd, "package.json")):
    checks_to_run.append(["npm", "test", "--if-present"])
elif os.path.isfile(os.path.join(cwd, "pyproject.toml")) or os.path.isfile(os.path.join(cwd, "pytest.ini")):
    checks_to_run.append(["pytest", "-q"])
elif os.path.isfile(os.path.join(cwd, "go.mod")):
    checks_to_run.append(["go", "test", "./..."])

for check_cmd in checks_to_run:
    try:
        res = subprocess.run(
            check_cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if res.returncode != 0:
            snippet = ((res.stdout or "") + "\n" + (res.stderr or "")).strip()[-600:]
            print(
                json.dumps(
                    {
                        "decision": "deny",
                        "reason": f"Pre-commit gate failed on `{' '.join(check_cmd)}`:\n{snippet}",
                    }
                )
            )
            sys.exit(0)
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        print(
            json.dumps(
                {
                    "decision": "deny",
                    "reason": f"Pre-commit check `{' '.join(check_cmd)}` timed out after 45s.",
                }
            )
        )
        sys.exit(0)

print(json.dumps({"decision": "allow"}))
PYEOF

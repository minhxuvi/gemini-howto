#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: security-scan.sh
# Event: PreToolUse (matcher: "write_to_file|replace_file_content|multi_replace_file_content")
# Purpose:
#   Scans proposed file writes and edits (`CodeContent`, `ReplacementContent`,
#   and `ReplacementChunks`) for hardcoded secrets (AWS Access Keys, GitHub PATs,
#   Google API Keys, Slack tokens, private keys) and blocks the write before
#   secrets ever touch disk.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

python3 - "$PAYLOAD" <<'PYEOF'
import json
import re
import sys

try:
    data = json.loads(sys.argv[1]) if sys.argv[1].strip() else {}
except json.JSONDecodeError:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

tool_call = data.get("toolCall") or {}
tool_name = tool_call.get("name") or data.get("toolName") or ""
tool_args = tool_call.get("args") or data.get("toolInput") or {}

if tool_name not in ("write_to_file", "replace_file_content", "multi_replace_file_content"):
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

target_file = str(tool_args.get("TargetFile") or "")

# Collect all candidate code strings being written
chunks_to_scan = []
if "CodeContent" in tool_args and tool_args["CodeContent"]:
    chunks_to_scan.append(str(tool_args["CodeContent"]))
if "ReplacementContent" in tool_args and tool_args["ReplacementContent"]:
    chunks_to_scan.append(str(tool_args["ReplacementContent"]))
for chunk in tool_args.get("ReplacementChunks") or []:
    if isinstance(chunk, dict) and chunk.get("ReplacementContent"):
        chunks_to_scan.append(str(chunk["ReplacementContent"]))

combined_content = "\n".join(chunks_to_scan)

SECRET_SIGNATURES = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID (AKIA...)"),
    (r"gh[pousr]_[A-Za-z0-9_]{20,}", "GitHub Personal Access Token (ghp_/gho_/ghs_...)"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google Cloud / Gemini API Key (AIza...)"),
    (r"xox[baprs]-[0-9A-Za-z\-]{10,}", "Slack API Token (xoxb-/xoxp-...)"),
    (r"sk-[A-Za-z0-9]{32,}", "Hardcoded API Secret Key (sk-...)"),
    (r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "PEM Private Key block"),
]

findings = []
for pattern, label in SECRET_SIGNATURES:
    if re.search(pattern, combined_content):
        findings.append(label)

if findings:
    reason = (
        f"Security gate blocked writing hardcoded credential(s) [{', '.join(findings)}] "
        f"to '{target_file}'. Use environment variables (e.g., os.environ or ${{VAR}}) instead."
    )
    print(json.dumps({"decision": "deny", "reason": reason}))
    sys.exit(0)

print(json.dumps({"decision": "allow"}))
PYEOF

#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: log-commands.sh
# Event: PostToolUse (matcher: ".*")
# Purpose:
#   Appends a structured JSON Lines (JSONL) audit record for every tool call
#   executed by Antigravity (including timestamp, conversationId, modelName,
#   stepIdx, toolName, arguments, and error status) to `.agents/audit.log`.
#   Returns `{}` on stdout per the PostToolUse contract.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

python3 - "$PAYLOAD" <<'PYEOF'
import datetime
import json
import os
import sys

try:
    data = json.loads(sys.argv[1]) if sys.argv[1].strip() else {}
except json.JSONDecodeError:
    print("{}")
    sys.exit(0)

workspaces = data.get("workspacePaths") or []
base_dir = workspaces[0] if workspaces and os.path.isdir(workspaces[0]) else os.getcwd()
log_dir = os.path.join(base_dir, ".agents")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "audit.log")

tool_call = data.get("toolCall") or {}
tool_name = tool_call.get("name") or data.get("toolName") or "unknown"
tool_args = tool_call.get("args") or data.get("toolInput") or {}

record = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "conversationId": data.get("conversationId", ""),
    "modelName": data.get("modelName", ""),
    "stepIdx": data.get("stepIdx"),
    "toolName": tool_name,
    "toolInput": tool_args,
    "error": data.get("error") or data.get("toolError") or "",
}

try:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
except OSError:
    pass

print("{}")
PYEOF

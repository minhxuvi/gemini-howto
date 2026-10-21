#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: goal-gate.sh
# Event: Stop (Flat handler array)
# Purpose:
#   Executes when the agent loop is about to go idle (`Stop`).
#   1. Checks `fullyIdle` and `terminationReason` so it never blocks when
#      background tasks/subagents are still running or when the user canceled.
#   2. Runs fast build/test verification if a test suite is present.
#   3. Returns `{"decision": "continue", "reason": "..."}` to re-enter the
#      agent loop if verification fails, or `{"decision": "allow"}` when clean.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

python3 - "$PAYLOAD" <<'PYEOF'
import json
import os
import subprocess
import sys

try:
    data = json.loads(sys.argv[1]) if sys.argv[1].strip() else {}
except json.JSONDecodeError:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

# 1. Never block stop if background tasks are still running or on user/error termination
fully_idle = data.get("fullyIdle", True)
termination_reason = str(data.get("terminationReason") or "")
execution_num = int(data.get("executionNum") or 0)

SAFE_EXIT_REASONS = {
    "USER_CANCELED",
    "ERROR",
    "MAX_INVOCATIONS",
    "MAX_FORCED_INVOCATIONS",
    "MAX_TOKEN_BUDGET_EXCEEDED",
}

if not fully_idle or termination_reason in SAFE_EXIT_REASONS or execution_num >= 3:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

workspaces = data.get("workspacePaths") or []
cwd = workspaces[0] if workspaces and os.path.isdir(workspaces[0]) else os.getcwd()

# 2. Detect and run project verification command
verify_cmd = None
if os.path.isfile(os.path.join(cwd, "package.json")):
    verify_cmd = ["npm", "test", "--if-present"]
elif os.path.isfile(os.path.join(cwd, "pyproject.toml")) or os.path.isfile(os.path.join(cwd, "pytest.ini")):
    verify_cmd = ["pytest", "-q"]
elif os.path.isfile(os.path.join(cwd, "go.mod")):
    verify_cmd = ["go", "test", "./..."]

if verify_cmd:
    try:
        res = subprocess.run(
            verify_cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if res.returncode != 0:
            tail = ((res.stdout or "") + "\n" + (res.stderr or "")).strip()[-500:]
            print(
                json.dumps(
                    {
                        "decision": "continue",
                        "reason": f"Goal gate verification (`{' '.join(verify_cmd)}`) failed. Fix the failing tests before stopping:\n{tail}",
                    }
                )
            )
            sys.exit(0)
    except Exception:
        pass

print(json.dumps({"decision": "allow"}))
PYEOF

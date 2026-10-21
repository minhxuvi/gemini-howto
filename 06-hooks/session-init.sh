#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: session-init.sh
# Event: SessionStart (Flat handler array)
# Purpose:
#   Runs once when a new Antigravity conversation starts. Inspects the active
#   workspace's Git branch, uncommitted file count, recent commit title, and
#   local Node/Python versions, injecting a persistent startup `systemMessage`
#   via `injectSteps`.
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
    data = {}

workspaces = data.get("workspacePaths") or []
workspace = workspaces[0] if workspaces and os.path.isdir(workspaces[0]) else os.getcwd()

def run_quiet(cmd):
    try:
        res = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, timeout=3)
        return res.stdout.strip() if res.returncode == 0 else ""
    except Exception:
        return ""

branch = run_quiet(["git", "rev-parse", "--abbrev-ref", "HEAD"])
status_lines = [line for line in run_quiet(["git", "status", "--porcelain"]).splitlines() if line.strip()]
last_commit = run_quiet(["git", "log", "-1", "--oneline"])
node_ver = run_quiet(["node", "--version"])
py_ver = run_quiet(["python3", "--version"])

summary_parts = [f"Workspace initialized: {workspace}"]
if branch:
    summary_parts.append(f"Git branch: {branch} ({len(status_lines)} uncommitted file(s))")
if last_commit:
    summary_parts.append(f"HEAD: {last_commit}")
runtimes = [v for v in (node_ver and f"Node {node_ver}", py_ver) if v]
if runtimes:
    summary_parts.append("Runtimes: " + ", ".join(runtimes))

system_note = " | ".join(summary_parts)

output = {
    "injectSteps": [
        {
            "systemMessage": {
                "systemMessage": system_note
            }
        }
    ]
}

print(json.dumps(output))
PYEOF

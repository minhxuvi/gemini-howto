#!/usr/bin/env bash
# ==============================================================================
# Antigravity Hook: format-code.sh
# Event: PostToolUse (matcher: "write_to_file|replace_file_content|multi_replace_file_content")
# Purpose:
#   Automatically formats modified source files using the appropriate language
#   formatter (prettier, ruff/black, gofmt, rustfmt, shfmt) immediately after
#   Antigravity writes or edits a file. Always returns `{}` on stdout per the
#   PostToolUse contract.
# ==============================================================================
set -euo pipefail

PAYLOAD="$(cat)"

TARGET_FILE="$(python3 - "$PAYLOAD" <<'PYEOF'
import json
import sys

try:
    data = json.loads(sys.argv[1]) if sys.argv[1].strip() else {}
except json.JSONDecodeError:
    sys.exit(0)

# Skip formatting if the tool execution itself failed
if data.get("error") or data.get("toolError"):
    sys.exit(0)

tool_call = data.get("toolCall") or {}
tool_args = tool_call.get("args") or data.get("toolInput") or {}
target = tool_args.get("TargetFile") or tool_args.get("file_path") or ""
print(target)
PYEOF
)"

if [[ -n "$TARGET_FILE" && -f "$TARGET_FILE" ]]; then
  case "$TARGET_FILE" in
    *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.json|*.css|*.scss|*.md|*.yaml|*.yml)
      if command -v prettier >/dev/null 2>&1; then
        prettier --write "$TARGET_FILE" >/dev/null 2>&1 || true
      fi
      ;;
    *.py)
      if command -v ruff >/dev/null 2>&1; then
        ruff format "$TARGET_FILE" >/dev/null 2>&1 || true
      elif command -v black >/dev/null 2>&1; then
        black --quiet "$TARGET_FILE" >/dev/null 2>&1 || true
      fi
      ;;
    *.go)
      if command -v gofmt >/dev/null 2>&1; then
        gofmt -w "$TARGET_FILE" >/dev/null 2>&1 || true
      fi
      ;;
    *.rs)
      if command -v rustfmt >/dev/null 2>&1; then
        rustfmt "$TARGET_FILE" >/dev/null 2>&1 || true
      fi
      ;;
  esac
fi

# PostToolUse contract requires returning an empty JSON object on stdout
printf '{}\n'

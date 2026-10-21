#!/usr/bin/env bash
# Quantitative Code Metrics Analyzer for code-review-specialist skill
# Usage: ./scripts/check-metrics.sh <file-or-directory>

set -euo pipefail

TARGET="${1:-.}"

if [ ! -e "$TARGET" ]; then
  echo "Error: Target '$TARGET' does not exist." >&2
  exit 1
fi

echo "================================================================"
echo "  Code Review Metrics Report: $TARGET"
echo "================================================================"
printf "%-42s | %7s | %6s | %6s | %5s\n" "File" "Lines" "Funcs" ">100ch" "TODOs"
echo "----------------------------------------------------------------"

analyze_file() {
  local file="$1"
  local lines funcs long_lines todos

  lines=$(wc -l < "$file" | tr -d ' ')
  # Count common function declarations across TS/JS, Python, Go, Rust
  funcs=$(grep -E -c '(^\s*(export\s+)?(async\s+)?function\s+|=>\s*\{|^\s*def\s+|^\s*async\s+def\s+|^\s*func\s+|^\s*(pub\s+)?(async\s+)?fn\s+)' "$file" 2>/dev/null || true)
  long_lines=$(awk 'length > 100 { count++ } END { print count+0 }' "$file")
  todos=$(grep -E -c '(TODO|FIXME|HACK|XXX)' "$file" 2>/dev/null || true)

  printf "%-42.42s | %7s | %6s | %6s | %5s\n" "$file" "$lines" "$funcs" "$long_lines" "$todos"
}

if [ -f "$TARGET" ]; then
  analyze_file "$TARGET"
else
  while IFS= read -r -d '' file; do
    analyze_file "$file"
  done < <(find "$TARGET" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -print0 | sort -z)
fi

echo "================================================================"

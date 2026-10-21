# Documentation & Architecture Sync — Formatting Rules

While the `documentation` plugin is enabled, apply these technical writing and formatting standards to all Markdown files and artifacts:

## 1. GitHub Flavored Markdown & Alerts
- Use GitHub-style callout alerts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) to highlight critical context. Never place two alerts consecutively or nest them.
- Preserve existing docstrings and inline code comments when updating source files.

## 2. Mermaid Diagram Rules
- Only use supported Mermaid diagram types: `flowchart TD` / `flowchart LR`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram`, and `xychart-beta`.
- Always quote node labels containing parentheses, brackets, colons, or slashes: `A["Service (v2)"]` instead of `A[Service (v2)]`.

## 3. Clickable Symbol & File Links
- Reference files and symbols using `file://` links with basenames as link text: `[server.ts](file:///abs/path/to/server.ts#L15-L42)`.

## 4. LaTeX & Dollar Sign Escaping
- Because `$` opens inline KaTeX math, always escape literal dollar signs in prose as `\$` (e.g., `\$100/month`) or wrap shell variables in backticks (`` `$HOME` ``).

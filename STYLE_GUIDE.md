# Style Guide — gemini-howto

This guide defines the writing, formatting, and diagram standards for all tutorials and templates in **gemini-howto**.

---

## 1. Writing Principles

1. **Practical & Action-Oriented**: Start every module with *what problem it solves*, *how long it takes*, and a *copy-pasteable quick start* that works immediately in Google Antigravity.
2. **Show, Don't Just Tell**: Pair every architectural explanation with a concrete configuration file, CLI command, or Mermaid diagram.
3. **Version Accuracy**: Target the current Google Antigravity ecosystem:
   - **Antigravity App**: v2.24.0+
   - **Antigravity CLI (`agy`)**: v1.4.0+
   - **Antigravity Python SDK (`google-antigravity`)**: v0.1.22+
   - **Models**: Gemini 4 Argon (`gemini-4-argon`), Gemini 3.8 Flash (`gemini-3.8-flash`), Gemini 3.1 Pro (`gemini-3.1-pro`), Nano Banana 2

---

## 2. Module `README.md` Structure

Every numbered module (`01-` through `10-`) follows a consistent structure:

1. **Header Block**:
   - Module title (`# Module XX: Title`)
   - Metadata badges/summary: **Difficulty**, **Time to Complete**, **Prerequisites**, **Key Deliverables**
2. **Overview & Mental Model**:
   - Why this feature exists and when to use it over alternatives
   - High-level Mermaid architecture diagram
3. **Core Concepts & Configuration**:
   - File locations (`.agents/...` vs `~/.gemini/config/...`)
   - Exact schema / YAML frontmatter / JSON contract tables
4. **Hands-On Walkthroughs**:
   - Step-by-step practical scenarios referencing the copy-paste templates in that folder
5. **Best Practices & Anti-Patterns**:
   - Side-by-side **Do** vs **Don't** comparisons
6. **Troubleshooting**:
   - Common pitfalls and how to diagnose them (`/context`, `/hooks`, `/mcp`, `/agents`, `agy plugin validate`)
7. **Navigation Footer**:
   - Links to the previous module, `README.md`, `QUICK_REFERENCE.md`, and the next module, plus a prompt to run `/lesson-quiz XX`.

---

## 3. Mermaid Diagram Guidelines

Antigravity renders Mermaid diagrams natively in Markdown previews and Artifacts. Follow these rules to prevent syntax errors:

- **Supported Diagram Types**:
  - `flowchart TD` / `flowchart LR` (or `graph TD` / `graph LR`)
  - `sequenceDiagram`
  - `stateDiagram-v2`
  - `classDiagram`
  - `erDiagram`
  - `xychart-beta`
- **Quote Labels with Special Characters**:
  - Always wrap node labels containing parentheses `()`, brackets `[]`, slashes `/`, or colons `:` in double quotes:
    ```mermaid
    flowchart LR
      A["User Prompt (/boost)"] --> B["Strategic Orchestrator (Phase 1)"]
      B --> C["DeepCoder (Git Worktree)"]
    ```
- **Avoid HTML Tags Inside Nodes**: Use newline escapes or succinct labels instead of `<br/>` or `<b>`.

---

## 4. GitHub Flavored Markdown Alerts

Use GitHub-style callouts strategically (do not place two alerts back-to-back without intervening text):

```markdown
> [!NOTE]
> Background context or how Antigravity resolves paths under the hood.

> [!TIP]
> Pro-tips, keyboard shortcuts (`Ctrl+J`, `Alt+M`), or token-saving patterns.

> [!IMPORTANT]
> Required YAML frontmatter fields or mandatory JSON keys.

> [!WARNING]
> Common pitfalls, budget limits (24 KB / 20k tokens), or breaking changes.

> [!CAUTION]
> Security boundaries, unsandboxed execution, or destructive operations.
```

---

## 5. Bilingual Synchronization (`./` and `./vi/`)

- Keep all code blocks, file paths, JSON keys, CLI flags, and slash commands identical in English across both the root English docs and the `vi/` Vietnamese docs.
- Translate prose, diagram node descriptions (where helpful for comprehension), and explanations into clear, natural Vietnamese for developers.

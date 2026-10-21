# Documentation & Architecture Sync (`documentation`)

An Antigravity plugin that keeps project READMEs, API reference tables, and Mermaid architecture diagrams synchronized with codebase changes.

## Bundled Components

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Manifest** | `plugin.json` | Declares `documentation` v1.0.0 and starter prompts |
| **Rules** | `rules/AGENTS.md` | Enforces GitHub Flavored Markdown, valid Mermaid syntax, KaTeX escaping (`\$`), and clickable `file://` symbol links |
| **Hooks** | `hooks.json` | `PostToolUse` validator that checks edited `.md` files for unquoted Mermaid labels or broken formatting |
| **Skill: `/docs-update`** | `skills/docs-update/SKILL.md` | Diffs recent code changes and updates READMEs, diagrams, and API tables |
| **Agent: `api-documenter`** | `agents/api-documenter.md` | Extracts public classes, functions, CLI flags, and REST endpoints into reference docs |

## Installation & Validation

```bash
agy plugin validate ./07-plugins/documentation --strict
agy plugin install ./07-plugins/documentation
```

# Context Optimization & Rule Splitting Patterns (`references/context-patterns.md`)

When auditing or refactoring a bloated `GEMINI.md` or `AGENTS.md`, use these patterns to maximize instruction adherence while minimizing `always_on` token consumption.

---

## 1. Decomposing a Bloated Root `GEMINI.md`

A common anti-pattern is placing every database rule, frontend style guide, protobuf convention, and deployment runbook into a single 1,500-line root `GEMINI.md`. Because `GEMINI.md` is `always_on`, it consumes thousands of tokens from the **20,000-token `defaultRulesBudget`** on every turn—even when the user is just fixing a typo.

### The Decomposition Matrix

| Content Found in Bloated `GEMINI.md` | Target Destination | Why |
| :--- | :--- | :--- |
| Repo-wide build/test/lint commands & core architectural boundaries | Keep in root `./GEMINI.md` or `./AGENTS.md` (<200 lines) | Needed in nearly every coding session. |
| Package-specific architecture (e.g., `packages/billing/` rules) | Move to `packages/billing/AGENTS.md` | Loaded dynamically via directory walk-up **only** when the agent reads/edits files in `packages/billing/**`. |
| File-extension rules (`.proto`, `.sql`, `.test.ts`, `.tsx`) | Move to `.agents/rules/<name>.md` with `trigger: glob` | Activated **only** when matching files are touched. |
| Specialized domain guidelines (migrations, caching, a11y, i18n) | Move to `.agents/rules/<name>.md` with `trigger: model_decision` | Progressive disclosure: only `description` (~30 tokens) is loaded upfront; body loads on demand. |
| Release checklists, security audit rubrics, incident templates | Move to `.agents/rules/<name>.md` with `trigger: manual` | Zero token cost until explicitly invoked via `@rule-name`. |
| Multi-step procedures, code generators, or slash workflows | Move to `.agents/skills/<name>/SKILL.md` | Registered as `/<name>` slash command + 3-stage progressive disclosure. |

---

## 2. Choosing Between `@[label](path)` and `@path`

Antigravity provides two file reference mechanisms inside rule files:

### Pattern A: `@path` (Canonical Path Pointer — Recommended Default)
```markdown
Before modifying authentication flows, read @docs/auth-state-machine.md and @src/auth/session.ts.
```
- **How Antigravity processes it**: Rewrites `@docs/auth-state-machine.md` to its canonical workspace path (`@/workspace/docs/auth-state-machine.md`).
- **Token impact**: Costs ~10 tokens upfront. The agent calls `view_file` on the target path only when working on authentication.

### Pattern B: `@[label](path)` (Inline Splicing — Use Sparingly)
```markdown
@[Mandatory Cryptography Policy](docs/security/crypto-policy.md)
```
- **How Antigravity processes it**: Reads `docs/security/crypto-policy.md`, strips any YAML frontmatter from it, and splices its full Markdown content directly into the rule before checking the **24,000-byte per-file cap**.
- **Token impact**: Full file content counts immediately toward the 24 KB file limit and 20,000-token rules budget. Use only for short (<2 KB), non-negotiable shared policies.

---

## 3. Auditing `.agents/rules/` Frontmatter Validity

Run this mental checklist on every `.agents/rules/*.md` file:

```yaml
---
# 1. Must be exact snake_case: always_on | model_decision | glob | manual
trigger: glob
# 2. Required for model_decision; strongly recommended for all rules (used if demoted over budget)
description: "Enforce React 19 Server Component boundaries and client directive rules."
# 3. Always quote glob strings containing * so YAML does not parse * as an alias!
globs: "**/*.tsx, packages/web/src/**/*.ts"
---
```

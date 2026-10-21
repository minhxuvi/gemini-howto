---
name: gemini-md
description: >-
  Author, audit, and optimize GEMINI.md, AGENTS.md, and modular .agents/rules/*.md files
  following Antigravity's 24 KB file cap, 20,000-token rules budget, and progressive disclosure
  patterns. Use when the user asks to initialize or improve GEMINI.md / AGENTS.md, migrate rules,
  or runs /gemini-md.
---

# `GEMINI.md`, `AGENTS.md` & `.agents/rules/` Architect (`gemini-md`)

Use this skill whenever the user asks to create, audit, refactor, or optimize `GEMINI.md`, `AGENTS.md`, or `.agents/rules/*.md` files in their workspace or global `~/.gemini/` configuration.

## Supporting Reference Files (Stage 3 Progressive Disclosure)

- **Context & Trigger Architecture Patterns**: [`references/context-patterns.md`](./references/context-patterns.md) — Detailed guide to splitting bloated root instruction files into `model_decision`, `glob`, and `manual` modular rules, plus `@[label](path)` vs. `@path` trade-offs.
- **Golden Example Files**: [`references/example-files.md`](./references/example-files.md) — Production templates for monorepo root `GEMINI.md`, subdirectory `AGENTS.md`, and `.agents/rules/*.md`.

---

## Step-by-Step Workflow

### Step 1: Audit Existing Workspace & Rule Footprint
1. **Scan Existing Instruction Files**:
   - Check for root `./GEMINI.md`, `./AGENTS.md`, `./.agents/GEMINI.md`, `./.agents/AGENTS.md`, `./.agents/rules/*.md`, and `./.agents/rules.json`.
   - Measure byte size (`wc -c`) and line count (`wc -l`) of each file.
2. **Inspect Codebase Tooling (If Creating from Scratch)**:
   - Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `turbo.json`, and `.github/workflows/` to discover exact build, test, lint, typecheck, and migration commands.

### Step 2: Enforce Antigravity's Golden Rule Invariants
Read [`references/context-patterns.md`](./references/context-patterns.md) and evaluate the rules against these five invariants:

1. **No YAML Frontmatter in `GEMINI.md` / `AGENTS.md`**:
   - Standalone `GEMINI.md` and `AGENTS.md` files are plain Markdown and always active (`always_on`). Never add YAML frontmatter to them.
2. **Mandatory YAML Frontmatter in `.agents/rules/*.md`**:
   - Every file in `.agents/rules/` MUST start with valid YAML frontmatter containing `trigger: always_on | model_decision | glob | manual`.
   - Verify `trigger` uses exact `snake_case` (never `alwaysOn` or `modelDecision`).
   - Verify `model_decision` rules include a high-signal `description`.
   - Verify `glob` rules wrap patterns starting with `*` in double quotes (`globs: "**/*.ts, **/*.tsx"`).
3. **Respect the 24 KB File Cap & 20,000-Token Budget**:
   - Keep root `GEMINI.md` / `AGENTS.md` **under 200 lines** (~4–8 KB).
   - Move file-type-specific rules to `.agents/rules/<topic>.md` (`trigger: glob`), domain guides to `trigger: model_decision`, and multi-step procedures to `.agents/skills/<name>/SKILL.md`.
4. **Use `@path` Pointers Over `@[label](path)` for Large Docs**:
   - Use `@docs/architecture.md` (canonical path pointer, zero upfront bloat) for large reference documents, and reserve `@[Label](path)` (inline expansion) for short, mandatory invariants.
5. **High-Signal, Non-Obvious Instructions Only**:
   - Remove generic filler (*"Write clean code"*, *"Follow best practices"*).
   - Include exact, runnable commands, architectural boundaries, and non-obvious codebase gotchas.

### Step 3: Draft or Refactor & Verify
Read [`references/example-files.md`](./references/example-files.md) for structural templates, apply the creates/edits, and verify that:
- Every file under `.agents/rules/*.md` is a direct child of `.agents/rules/` (or explicitly listed in `.agents/rules.json`).
- No single rule file exceeds `24,000` bytes after expanding `@[label](path)` includes.

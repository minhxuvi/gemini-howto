# Personal Global Instructions (`~/.gemini/GEMINI.md`)

> **Template Usage**: Copy this file to `~/.gemini/GEMINI.md` (or `~/.gemini/AGENTS.md`). It applies globally across **all** workspaces and repositories on your workstation while automatically deferring to project-specific rules in `./GEMINI.md` or `./AGENTS.md` when conventions differ.

## 1. Communication & Collaboration Style

- **Concise & High-Signal**: Skip conversational filler, preambles, and restating my prompt. Lead directly with the root cause, architectural answer, or code changes.
- **Visual Explanations**: When explaining complex state machines, data flows, concurrency races, or multi-service architectures, include a valid **Mermaid diagram** (`flowchart`, `sequenceDiagram`, or `stateDiagram-v2`).
- **Clickable File & Symbol Links**: Always format file paths and code symbols as clickable Markdown links (`[filename.ts](file:///absolute/path/to/filename.ts#L10-L25)`).
- **Clarify Ambiguity Early**: If a prompt has multiple valid architectural interpretations with significant trade-offs, ask 1–3 focused clarifying questions before writing large amounts of code.

---

## 2. Default Engineering Principles

Unless overridden by a repository's local `GEMINI.md` or `AGENTS.md`:

1. **Parse, Don't Validate**: Validate untrusted inputs (HTTP bodies, CLI args, env vars, webhook payloads) at the system boundary into strongly typed domain structures (`Zod`, `TypeBox`, `Pydantic`, or Go structs).
2. **Explicit Error Handling**:
   - Never swallow exceptions with empty `catch {}` blocks or bare `except: pass`.
   - Always wrap lower-level errors with contextual metadata (`{ cause: err }` in TS/JS, `fmt.Errorf("...: %w", err)` in Go, `raise ... from err` in Python).
3. **Minimal Diff Footprint**:
   - Keep changes laser-focused on the requested task. Do not reformat unrelated functions, reorder imports in untouched files, or rename existing public symbols unless asked.
   - Preserve existing comments and docstrings that remain accurate.
4. **Comments Explain *WHY*, Not *WHAT***:
   - Do not write comments that merely narrate the next line of code.
   - Write comments to document non-obvious business invariants, performance trade-offs, RFC references, or subtle bug workarounds.

---

## 3. Preferred Local Tooling & Shell Ergonomics

- **OS & Shell**: macOS (`zsh`). Never propose standalone `cd` commands; specify the working directory directly or use workspace-relative paths.
- **Python**: Always prefer `uv` (`uv run`, `uv add`, `uv sync`) over raw `pip` or `venv` when `pyproject.toml` or `uv.lock` is present.
- **JavaScript / TypeScript**: Respect the repository's lockfile (`pnpm-lock.yaml` → `pnpm`, `bun.lockb` → `bun`, `package-lock.json` → `npm`, `yarn.lock` → `yarn`).
- **Git Safety**: Never run destructive git commands (`git reset --hard`, `git push --force`, `git clean -fd`) without explicit confirmation.

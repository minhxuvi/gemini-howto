---
name: commit
description: >-
  Audit modified files for secrets or build artifacts, stage logical atomic changes, and
  create a well-structured git commit following Conventional Commits and repository history.
  Use when the user runs /commit or asks to stage and commit their current changes.
---

# Atomic Conventional Commit (`/commit`)

Use this skill when invoked via `/commit [optional-hint]` or when the user asks to commit staged or working-tree changes.

## Usage Examples

```text
/commit
/commit fix race condition in token refresh
/commit --amend
```

---

## Step-by-Step Agent Instructions

### Step 1: Gather Repository Context
Execute these commands to inspect the current state and match the repository's commit conventions:
1. `git status --short` — View staged, unstaged, and untracked files.
2. `git diff --cached` — Inspect currently staged changes.
3. `git diff` — Inspect unstaged working-tree changes (if nothing is staged yet).
4. `git log -n 5 --oneline` — Observe the repository's existing commit message style (e.g., Conventional Commits `type(scope): description`, ticket prefixes, capitalization).

### Step 2: Pre-Commit Safety Audit
Before staging or committing any file, verify that **none** of the following are included:
- **Secrets & Credentials**: `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `credentials.json`, service account keys, or inline API keys/tokens (`sk-...`, `AIza...`, `ghp_...`).
- **Build & Dependency Artifacts**: `node_modules/`, `dist/`, `build/`, `__pycache__/`, `.venv/`, `.DS_Store`, coverage reports, or temporary scratch files.
- **Unintended Debug Leftovers**: Accidental `debugger` statements, temporary `console.log("HERE")` lines, or conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

> [!CAUTION]
> If you detect a secret, private key, or merge conflict marker in the diff, **abort the commit immediately** and report the exact file and line number to the user.

### Step 3: Logical Staging
- If the user has **already staged specific files** (`git diff --cached` is non-empty), respect their staging selection and only commit the staged changes.
- If **nothing is staged**, stage all relevant modified/new source files explicitly by path (`git add <file1> <file2>`) rather than blindly running `git add .` if untracked scratch files are present.
- If the working tree contains two completely unrelated changes (e.g., a database bugfix and a README typo), offer to split them into two separate atomic commits.

### Step 4: Draft Conventional Commit Message
Construct a concise, high-signal commit message:

```text
<type>(<optional-scope>): <imperative summary under 72 chars>

<optional body explaining WHY the change was made, key trade-offs, or root cause>
```

**Supported `<type>` values**:
- `feat`: New user-facing or API feature
- `fix`: Bug fix or regression repair
- `perf`: Performance or memory optimization
- `refactor`: Internal code restructuring without behavior change
- `test`: Adding or updating unit/integration/E2E tests
- `docs`: Documentation or code comment updates
- `build` / `ci`: Build system, dependencies, or CI/CD pipeline configuration
- `chore`: Routine maintenance and tooling tasks

### Step 5: Execute & Verify Commit
1. Run `git commit -m "<subject>" -m "<body>"` (avoid interactive `-i` or editor flags).
2. Run `git log -n 1 --stat` and `git status --short` to confirm the commit succeeded cleanly and display the commit hash and summary to the user.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

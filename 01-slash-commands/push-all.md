---
name: push-all
description: >-
  Run pre-push quality gates (linter, typecheck, tests), scan for secrets and oversized files,
  stage and commit changes with a Conventional Commit message, push to the remote branch, and
  verify remote status. Use when the user runs /push-all or asks to validate, commit, and push
  all work in one workflow.
---

# End-to-End Validate, Commit & Push (`/push-all`)

Use this skill when invoked via `/push-all [commit-message-hint]` to safely validate, stage, commit, and push changes to the remote repository.

## Usage Examples

```text
/push-all
/push-all feat(billing): add Stripe webhook signature verification
```

---

## Step-by-Step Agent Instructions

### Step 1: Branch & Protected-Branch Safety Check
1. Check current branch and remote tracking status:
   ```bash
   git status -sb
   git branch --show-current
   ```
2. **Protected Branch Guard**: If the current branch is `main`, `master`, or `production`, **pause and ask the user for explicit confirmation** before pushing directly, or offer to create a feature branch (`git checkout -b <type>/<short-name>`) first.

### Step 2: Secret, Artifact & Large File Scan
Inspect all modified and untracked files (`git status --porcelain`):
1. **Secrets & Keys**: Verify no `.env` files, private keys (`*.pem`, `*.key`), credentials (`credentials.json`), or high-entropy API tokens appear in `git diff HEAD` or untracked files.
2. **Large Binary Files**: Check that no file being staged exceeds `10 MB` unless tracked by Git LFS (`.gitattributes`).
3. **Ignored Artifacts**: Ensure build outputs (`dist/`, `build/`, `.next/`, `target/`, `node_modules/`, `__pycache__/`) are properly listed in `.gitignore`.

### Step 3: Run Local Quality Gates
Detect the project's toolchain (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`) and run the fast verification suite on modified packages:
1. **Format / Lint check**: e.g., `npm run lint`, `ruff check .`, `golangci-lint run`, `cargo clippy`.
2. **Typecheck**: e.g., `npm run typecheck` / `tsc --noEmit`, `mypy .`, `pyright`.
3. **Unit Tests**: e.g., `npm test -- --watchAll=false`, `pytest`, `go test ./...`, `cargo test`.

> [!IMPORTANT]
> If any lint, typecheck, or test command fails, **do not commit or push**. Fix the reported issue first (or report the failure clearly) and re-run the check until green.

### Step 4: Stage & Create Conventional Commit
1. Stage all intended files (`git add <files>` or `git add -A` once untracked files are verified clean).
2. If there are staged changes, create a Conventional Commit (`<type>(<scope>): <summary>`) incorporating the user's hint (if provided) and the `WHY` behind the diff.

### Step 5: Sync & Push to Remote
1. Fetch remote state to check for upstream divergence:
   ```bash
   git fetch origin
   ```
2. Push the branch to origin (setting upstream tracking if needed):
   ```bash
   git push -u origin HEAD
   ```
   *(Never run `git push --force` or `--force-with-lease` unless explicitly instructed by the user.)*
3. **Verification**: Run `git status -sb` and `git log -n 1 --oneline` (and `gh run list -L 1` if GitHub CLI is configured) to confirm the remote branch is up to date.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

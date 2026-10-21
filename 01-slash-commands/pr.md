---
name: pr
description: >-
  Prepare a pull request by running pre-flight quality checks, analyzing branch diffs against
  the base branch, detecting breaking changes, and generating a structured Pull Request title
  and description. Use when the user runs /pr or asks to prepare, summarize, or open a PR.
---

# Pull Request Preparation & Description Generator (`/pr`)

Use this skill when invoked via `/pr [base-branch]` or when the user asks to prepare a pull request, summarize branch changes, or open a PR via `gh pr create`.

## Usage Examples

```text
/pr
/pr main
/pr --create "feat(auth): add OIDC JWKS token verifier"
```

---

## Step-by-Step Agent Instructions

### Step 1: Inspect Repository & Branch State
Run the following read-only git commands to gather full branch context:
1. **Current & Base Branch**:
   - Check current branch: `git branch --show-current`
   - Determine base branch (use user argument if provided; otherwise detect `origin/main` or `origin/master`).
2. **Working Tree & Commit History**:
   - Check uncommitted changes: `git status --short`
   - List commits unique to this branch: `git log --oneline <base>..HEAD`
   - Inspect diff stat and full changes: `git diff --stat <base>...HEAD` and `git diff <base>...HEAD`

> [!WARNING]
> If there are unstaged or uncommitted changes in the working tree, alert the user and ask whether they want to stage and commit them (or invoke `/commit`) before finalizing the PR.

### Step 2: Pre-Flight Quality Checklist
Verify that the branch is clean and ready for review:
- [ ] **No stray debug code or secrets**: Scan the diff for accidental `console.log`, `print()`, `debugger`, `TODO: remove`, or hardcoded credentials/tokens.
- [ ] **Tests & Typecheck**: Run the project's fast verification commands (e.g., `npm test`, `pytest`, `cargo test`, `go test ./...`, and linter/typechecker) on changed packages.
- [ ] **Breaking Change Detection**: Check if any public API signatures, database migrations, environment variables (`.env.example`), or protobuf/OpenAPI schemas were altered in a backward-incompatible way.

### Step 3: Generate Structured PR Title & Body
Draft a Conventional Commits PR title (`<type>(<scope>): <summary>`) and a comprehensive Markdown description using the following template:

```markdown
## Summary
<!-- 2-3 sentence executive summary of what problem this PR solves and why -->

## Key Changes
- **[Component/Module]**: Concise explanation of architectural or implementation changes (`path/to/file.ts`)
- **[Component/Module]**: Explanation of secondary changes

## Breaking Changes & Migration Notes
<!-- Omit or write "None" if 100% backward-compatible. Otherwise list required env vars, DB migrations, or API changes. -->

## Verification & Testing Performed
- [x] Unit / integration tests executed (`<command run>`)
- [x] Typecheck & linter verified (`<command run>`)
- [ ] Manual / E2E verification steps:
  1. Step one
  2. Step two

## Risk & Rollback Plan
- **Blast Radius**: Low / Medium / High — [explain affected services]
- **Rollback**: Safe to revert commit / Requires feature flag toggle / Requires migration rollback
```

### Step 4: Optional PR Creation (`gh` CLI)
- If the user passed `--create` or explicitly asked to open the PR on GitHub:
  1. Ensure the current branch is pushed to origin (`git push -u origin HEAD`).
  2. Run `gh pr create --base <base> --title "<title>" --body "<generated-body>"` and return the resulting PR URL.
- Otherwise, present the generated PR title and Markdown block so the user can review or copy it with `/copy`.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

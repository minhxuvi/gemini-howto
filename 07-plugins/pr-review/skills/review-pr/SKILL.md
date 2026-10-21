---
name: review-pr
description: "Run a comprehensive multi-agent pull request review covering correctness, security vulnerabilities, performance bottlenecks, and test coverage."
---

# Comprehensive Pull Request Review (`/review-pr`)

Execute a structured, multi-agent code review of the current branch or staged diff.

## Step 1: Gather Diff & Scope

1. Determine the diff target:
   - If the user passed a ref or branch range (e.g., `main..HEAD`), run `git diff <range> --stat` and `git diff <range>`.
   - Otherwise, inspect both staged and unstaged changes via `git status --short` and `git diff HEAD`.
2. Identify all modified, added, and deleted files.

## Step 2: Parallel Specialist Delegation

Use `invoke_subagent` to launch both specialist reviewers concurrently in read-only mode:
- **`security-reviewer`**: Audit all changed files for injection flaws, broken access control, secrets exposure, unsafe deserialization, and SSRF.
- **`performance-reviewer`**: Audit all changed files for algorithmic complexity regressions, N+1 queries, blocking I/O in async paths, and unnecessary allocations.

## Step 3: Main Agent Correctness & Test Audit

While the specialist subagents analyze the diff, inspect the changed files directly for:
1. Logic errors, off-by-one boundaries, and null/undefined edge cases.
2. Backward compatibility of public interfaces, database schemas, and API payloads.
3. Presence and quality of unit/integration tests covering the new code paths.

## Step 4: Synthesize the Review Report

Combine findings from `security-reviewer`, `performance-reviewer`, and your own analysis into a clean Markdown report:

```markdown
# Pull Request Review Report

## Executive Summary
- **Files Changed**: <count>
- **Merge Readiness**: ✅ Approved | ⚠️ Approved with Comments | ❌ Request Changes
- **Findings Breakdown**: <N> Critical, <N> High, <N> Medium, <N> Low

## 🔴 Critical & 🟠 High Priority Findings
1. **[SEVERITY] Title** — [file.ts:L10-L25](file:///abs/path/file.ts#L10-L25)
   - **Impact**: ...
   - **Recommended Fix**:
     ```ts
     // drop-in replacement
     ```

## 🟡 Medium & 🔵 Low Priority Findings
...

## Test Coverage & Verification Assessment
...
```

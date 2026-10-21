---
name: code-review-specialist
description: >-
  Perform comprehensive security, performance, algorithmic complexity, and maintainability
  code reviews backed by quantitative metrics and structured audit checklists. Use when the
  user asks to review code, audit a pull request or git diff, check for security vulnerabilities,
  or invokes /code-review-specialist.
---

# Code Review Specialist (`code-review-specialist`)

Use this skill to conduct rigorous, evidence-backed code reviews across individual files, directories, or branch diffs.

## Supporting Files in This Skill Bundle (Stage 3 Progressive Disclosure)

- ** Quantitative Metrics Helper**: [`scripts/check-metrics.sh`](./scripts/check-metrics.sh) — Shell script that computes line counts, function density, long-line outliers, and `TODO`/`FIXME` markers. **Always run this script first** on target files.
- **Audit Checklist**: [`resources/checklist.md`](./resources/checklist.md) — Exhaustive security (OWASP), performance, concurrency, and testing rubric. Read this file during Step 2.
- **Sample Output**: [`examples/sample-review.md`](./examples/sample-review.md) — Reference example demonstrating the exact severity grading and before/after patch format expected by this skill.

---

## Step-by-Step Review Workflow

### Step 1: Gather Context & Quantitative Metrics
1. **Determine Target Files**:
   - If the user provided specific file paths or directories, target those files.
   - If no files were specified, run `git diff --name-only HEAD` (or `git diff --name-only origin/main...HEAD`) to review all modified files on the current branch.
2. **Execute the Metrics Script**:
   Run the bundled [`check-metrics.sh`](./scripts/check-metrics.sh) script against the target file(s) from the skill directory:
   ```bash
   bash .agents/skills/code-review-specialist/scripts/check-metrics.sh <target-file-or-dir>
   ```
   *(If running directly from the `03-skills` tutorial folder, use `bash 03-skills/code-review-specialist/scripts/check-metrics.sh <target>`.)*

### Step 2: Systematic Audit Against `resources/checklist.md`
Read [`resources/checklist.md`](./resources/checklist.md) and evaluate the target code across four pillars:
1. **Security & Trust Boundaries**: Injection vectors (SQLi, command injection, XSS), broken object-level authorization (BOLA/IDOR), hardcoded secrets, timing-unsafe token comparisons, and missing input validation.
2. **Performance & Scalability**: $O(n^2)$ nested loops, N+1 database queries inside loops, unindexed query predicates, sequential `await` waterfalls, and memory leaks (unclosed streams/listeners).
3. **Correctness & Edge Cases**: Unhandled null/undefined values, race conditions on shared state, integer overflow/floating-point precision in financial math, and silent error swallowing.
4. **Maintainability & Testing**: Functions exceeding 50 lines, high cyclomatic complexity, leaky abstractions, and missing unit tests for failure paths.

### Step 3: Format the Review Report
Read [`examples/sample-review.md`](./examples/sample-review.md) to match the required reporting format:
1. **Executive Summary & Scorecard**: Overall readiness (`APPROVE`, `APPROVE WITH NITS`, `REQUEST CHANGES`), quantitative metrics table from Step 1, and category scores (`1–5`).
2. **Prioritized Findings (`Critical`, `High`, `Medium`, `Low / Nit`)**:
   - Exact file and 1-indexed line range link
   - Root cause and concrete failure/exploit scenario
   - Minimal, drop-in **Before / After** code fix
3. **Positive Highlights**: Acknowledge well-designed patterns, clean abstractions, or thorough test coverage in the reviewed code.

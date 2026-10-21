# PR Review Suite — Always-On Engineering Rules

While the `pr-review` plugin is enabled, follow these code review standards across all review and summary tasks:

## 1. Evidence-Backed Findings Only
- Every reported defect, vulnerability, or performance bottleneck **must** cite the exact file and 1-indexed line range using a clickable markdown link: `[filename.ts:L42-L58](file:///absolute/path/to/filename.ts#L42-L58)`.
- Do not speculate about code that was not inspected. Read the surrounding context of every modified hunk before flagging an issue.

## 2. Severity Classification
Classify every finding into one of four actionable tiers:
- 🔴 **`CRITICAL` (Blocker)**: Exploitable security vulnerability, data loss/corruption risk, unhandled crash on the main path, or breaking API contract change.
- 🟠 **`HIGH` (Must Fix Before Merge)**: Race condition, missing error handling on I/O boundaries, N+1 query in a loop, or missing test coverage for new business logic.
- 🟡 **`MEDIUM` (Should Fix)**: Suboptimal complexity, maintainability debt, missing edge-case validation, or unclear naming.
- 🔵 **`LOW` (Nit / Suggestion)**: Idiomatic cleanup, documentation polish, or minor refactoring opportunity.

## 3. Concrete Remediation Snippets
- For every `CRITICAL` and `HIGH` finding, include a minimal drop-in code snippet showing the recommended fix.
- Preserve existing comments and docstrings when proposing replacements.

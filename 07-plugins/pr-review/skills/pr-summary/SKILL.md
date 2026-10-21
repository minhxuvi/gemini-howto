---
name: pr-summary
description: "Generate a structured Pull Request title, motivation summary, Mermaid architecture diff diagram, and verification checklist from branch commits."
---

# Pull Request Summary Generator (`/pr-summary`)

Draft a clear, reviewer-friendly Pull Request description from the current branch's commits and file changes.

## Workflow

1. **Inspect Commit & Diff History**:
   - Run `git log main..HEAD --oneline` (or compare against the repository's default branch) to list all commits included in the branch.
   - Run `git diff main...HEAD --stat` to quantify changed files and modules.
2. **Categorize Changes**:
   - Group modifications into **Features**, **Bug Fixes**, **Refactoring**, **Security/Performance**, and **Tests/Docs**.
   - Identify any breaking changes, new environment variables, or database migrations.
3. **Render the PR Description**:
   Produce a ready-to-paste GitHub/GitLab Pull Request body using the template below:

```markdown
## Summary
<1–3 sentences explaining *why* this change is being made and *what* problem it solves.>

## Key Changes
- **<Component/Module>**: <Concise description with clickable file links>
- **<Component/Module>**: <Concise description>

## Architecture / Data Flow
```mermaid
flowchart LR
    Client["Client Request"] --> Middleware["Updated Auth Middleware"]
    Middleware --> Handler["Route Handler"]
```

## Breaking Changes & Migration Notes
- [ ] None / Backward-compatible
- [ ] Requires migration or config update: `<details>`

## Test Plan & Verification
- [x] Unit tests passing (`npm test` / `pytest`)
- [ ] Verified edge cases: `<list>`
```

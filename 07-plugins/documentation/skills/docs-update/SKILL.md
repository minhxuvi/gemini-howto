---
name: docs-update
description: "Inspect recent code changes and synchronize READMEs, API reference tables, and Mermaid architecture diagrams."
---

# Documentation Synchronizer (`/docs-update`)

Keep project documentation accurate and up-to-date with recent code modifications.

## Workflow

1. **Detect Codebase Changes**:
   - Run `git diff HEAD~1..HEAD --stat` (or `git status --short` if working on uncommitted changes) to identify modified source files, CLI flags, configuration schemas, or public exports.
2. **Delegate API Extraction**:
   - Invoke `api-documenter` on modified source modules to extract updated signatures, parameter types, return values, and usage examples.
3. **Update Documentation & Diagrams**:
   - Update affected `README.md` sections, configuration tables, and `mermaid` architecture diagrams so they reflect the current implementation.
   - Verify all `file://` links and relative navigation links resolve cleanly.

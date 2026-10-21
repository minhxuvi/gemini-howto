---
name: doc-refactor
description: >-
  Audit and reorganize project documentation, fix broken relative links, eliminate stale
  instructions that have drifted from the codebase, and add valid Mermaid architecture
  and sequence diagrams. Use when the user runs /doc-refactor or asks to clean up READMEs
  and technical docs.
---

# Documentation Restructuring & Diagram Enrichment (`/doc-refactor`)

Use this skill when invoked via `/doc-refactor [target-dir-or-file]` or when the user asks to modernize, reorganize, or audit repository documentation.

## Usage Examples

```text
/doc-refactor README.md
/doc-refactor docs/
/doc-refactor Verify all CLI flags and architecture diagrams in docs/ match src/
```

---

## Step-by-Step Agent Instructions

### Step 1: Inventory & Codebase Drift Audit
1. **Discover Documentation Files**:
   - Locate all `.md` files in the target scope (`README.md`, `CONTRIBUTING.md`, `docs/**/*.md`).
2. **Detect Code-to-Doc Drift**:
   - Cross-check every shell command, npm script (`package.json`), environment variable (`.env.example` / config loader), and file path mentioned in the docs against the live repository.
   - Flag any referenced files that no longer exist or CLI flags that were renamed.
3. **Audit Relative Links**:
   - Verify that every internal Markdown link (`[label](./path/to/file.md#anchor)`) resolves to an existing file and heading anchor.

### Step 2: Structural Reorganization (Diátaxis Framework)
Reorganize sprawling or unstructured Markdown files into clear, scannable sections:
1. **Quick Start (Under 5 Minutes)**: Prerequisites, copy-pasteable install/run commands, and expected output.
2. **Architecture & Visual Overview**: High-level component topology and request flows using **Mermaid diagrams**.
3. **Task-Oriented How-To Guides**: Step-by-step instructions for common developer workflows (testing, migrations, debugging, deployment).
4. **Configuration & Reference Tables**: Exhaustive tables of environment variables, CLI flags, and scripts with types and defaults.

### Step 3: Enrich with Valid Mermaid Diagrams
Replace dense walls of architectural prose with clean Mermaid diagrams. Follow these strict syntax rules:
- Use only supported diagram types: `flowchart TD`, `flowchart LR`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, or `erDiagram`.
- **Always wrap node labels containing parentheses, brackets, colons, or slashes in double quotes**:
  - ✅ `API["API Gateway (v2)"] --> Auth["Auth Service [JWT]"]`
  - ❌ `API[API Gateway (v2)] --> Auth[Auth Service]` (causes Mermaid syntax error)
- Never use raw HTML tags (`<br/>`, `<b>`) inside node labels.

### Step 4: Formatting & Verification
1. **Apply GitHub Flavored Markdown (GFM) Alerts**:
   - Use `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, and `> [!CAUTION]` for key callouts (never place two alerts consecutively without text in between).
2. **Verify All Links & Commands**:
   - Check that every file path referenced in links exists on disk.
   - Present a summary table of fixed broken links, updated commands, and newly added Mermaid diagrams.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

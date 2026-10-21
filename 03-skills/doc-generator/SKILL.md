---
name: doc-generator
description: >-
  Generate accurate API reference documentation and OpenAPI 3.1 specifications by extracting
  public function, class, and route signatures directly from source files. Use when the user
  asks to generate API docs, document a module or SDK, or invokes /doc-generator.
---

# API & SDK Documentation Generator (`doc-generator`)

Use this skill to generate developer-ready Markdown API reference documentation and OpenAPI 3.1 schemas that are 100% grounded in the actual source code signatures.

## Supporting Files in This Skill Bundle (Stage 3 Progressive Disclosure)

- **Signature Extractor Script**: [`scripts/extract-signatures.py`](./scripts/extract-signatures.py) — Python script using `ast` (for Python) and regex pattern matching (for TypeScript/Go) to extract exported functions, classes, decorators, and route definitions with exact line numbers.
- **Documentation Template**: [`templates/api-template.md`](./templates/api-template.md) — Standardized Markdown template for modules, endpoints, parameters, error codes, and runnable code examples.
- **Reference Output**: [`examples/sample-docs.md`](./examples/sample-docs.md) — Complete sample documentation generated using this skill.

---

## Step-by-Step Documentation Workflow

### Step 1: Extract Signatures Deterministically
Never guess function parameters or route paths from memory. Run the bundled [`extract-signatures.py`](./scripts/extract-signatures.py) helper script against the target file or directory:

```bash
python3 .agents/skills/doc-generator/scripts/extract-signatures.py <target-path>
```
*(If running directly from the `03-skills` directory, run `python3 03-skills/doc-generator/scripts/extract-signatures.py <target-path>`.)*

Review the JSON/table output of extracted symbols, parameters, return annotations, and line numbers, then read the source files around those lines to inspect validation schemas (`Zod`, `TypeBox`, `Pydantic`) and thrown error types.

### Step 2: Format Using `templates/api-template.md`
Read [`templates/api-template.md`](./templates/api-template.md) and [`examples/sample-docs.md`](./examples/sample-docs.md), then generate documentation that includes:
1. **Module / Service Overview & Architecture**: A concise summary and a valid **Mermaid sequence or flowchart diagram** showing how callers interact with the module or endpoint.
2. **Signature & Parameter Reference Table**: Every parameter, its exact type, required/optional status, default value, and validation constraints.
3. **Return Value & Error Catalogue**: Exact response payload schemas and a table of every error code or exception that can be raised.
4. **Copy-Pasteable Runnable Examples**: Realistic usage snippets (including authentication headers, error handling, and expected output).

### Step 3: Verification Against Source Truth
Before finishing, verify that:
- Every documented symbol, parameter name, and default value matches the output of `extract-signatures.py`.
- All internal file links and Mermaid diagrams use valid syntax.

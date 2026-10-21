# Clean Code & Agentic Engineering Rules

Reusable engineering principles that can be referenced from your `GEMINI.md`, `AGENTS.md`, or `.agents/rules/*.md` via `@[Clean Code Rules](clean-code-rules.md)`.

---

## 1. Surgical, Verifiable Changes

- **Minimal Diff Surface**: Touch only the lines and files directly required by the task. Do not bundle opportunistic formatting or unrelated refactors into functional changes.
- **Preserve Existing Intent**: Never delete existing comments, docstrings, or public exports unless explicitly instructed or superseded by the requested change.
- **Verify Before Declaring Done**: Every code change must be paired with an executable verification step (unit test, typecheck, linter, or reproduction script).

## 2. Clarity Over Cleverness

- **Explicit Control Flow**: Prefer early returns (guard clauses) over deeply nested `if/else` pyramids.
- **Self-Describing Identifiers**: Name variables after *what they hold* (`unverifiedUserIds`, `retryDelayMs`) and functions after *what they do* (`parseWebhookSignature`, `revokeExpiredTokens`).
- **Single Level of Abstraction**: Keep functions focused on one responsibility. If a function mixes high-level orchestration with low-level byte/string parsing, extract the low-level helper.

## 3. Type Safety & Boundary Validation

- **Validate at System Boundaries**: Parse and validate untrusted inputs (HTTP payloads, CLI flags, environment variables, webhook bodies, MCP responses) at the ingress boundary using strict schemas (Zod, Pydantic, JSON Schema, Protobuf).
- **Avoid Stringly-Typed Internal State**: Use enums, discriminated unions, or typed dataclasses internally rather than passing raw unvalidated dicts or `any`.
- **Explicit Error Handling**: Never swallow exceptions silently (`except Exception: pass` or empty `catch {}`). Wrap errors with actionable context (`what failed`, `which identifier`, `why`) while redacting secrets and PII.

## 4. Test Engineering Principles

- **Behavior Over Implementation**: Test observable inputs, outputs, and side effects rather than mocking internal private methods.
- **Deterministic Execution**: Avoid real `sleep()` calls, unseeded randomness, or live external network requests in unit tests.
- **Edge-Case First**: Always cover empty collections, boundary values (`0`, `-1`, `MAX_INT`), malformed UTF-8/JSON, and concurrent race conditions.

## 5. Security & Secrets Hygiene

- **Zero Hardcoded Credentials**: Never commit API keys, bearer tokens, private keys, or connection strings. Use environment variables (`.env.example`) or secret managers.
- **Least-Privilege Agent Execution**: Scope subagent tools and `mcp(server/tool)` permissions to the minimum required set. Keep the OS Terminal Sandbox enabled for untrusted or third-party scripts.
- **Parameterized Queries Only**: Never interpolate user input directly into SQL queries, shell commands, or HTML templates.

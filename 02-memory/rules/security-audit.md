---
trigger: manual
description: "Comprehensive OWASP API & application security audit rubric invoked explicitly via @security-audit."
---

# On-Demand Security Audit Rubric (`@security-audit`)

> **Activation Mode**: `trigger: manual`. This rule is never loaded automatically into context. It is injected only when the user explicitly mentions `@security-audit` in a chat prompt (e.g., *"Review `src/auth/` using `@security-audit`"*).

When `@security-audit` is referenced, perform a systematic line-by-line security audit of the target files or diff against the following six threat categories:

## 1. Authentication, Session & Token Security
- [ ] **JWT Verification**: Ensure `jwt.verify()` explicitly restricts allowed `algorithms` (e.g., `["RS256"]` or `["ES256"]`) to prevent `alg: "none"` or HMAC/RSA key-confusion attacks, and validates `iss`, `aud`, and `exp`.
- [ ] **Timing-Safe Comparisons**: Verify all webhook HMAC signatures, API keys, and CSRF tokens are compared using `crypto.timingSafeEqual` rather than `===` or `==`.
- [ ] **Cookie Flags**: Confirm session cookies set `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict`), and a bounded `Max-Age`.

## 2. Broken Object Level Authorization (BOLA / IDOR)
- [ ] **Tenant & Owner Scoping**: Verify that every `SELECT`, `UPDATE`, and `DELETE` query operating on a user-supplied resource ID (`:id`) also filters by the authenticated principal's `organization_id` or `user_id` in the `WHERE` clause.
- [ ] **Mass Assignment**: Ensure incoming JSON payloads are filtered through an explicit allowlist schema before passing to ORM `.update()` or `.insert()` calls (preventing users from overwriting `role`, `isAdmin`, or `organizationId`).

## 3. Injection & Unsafe Execution
- [ ] **SQL Injection**: Flag any string interpolation or template literals inside raw SQL (`sql.raw(\`... \${input}\`)`, `query("SELECT ... " + id)`). Enforce parameterized queries.
- [ ] **Command Injection**: Flag any `child_process.exec` or `execSync` calls using untrusted input; require `execFile` or `spawn` with an argument array and `shell: false`.
- [ ] **Path Traversal**: Verify file operations resolve paths via `path.resolve(baseDir, userPath)` and assert that the resolved path starts with `baseDir + path.sep`.

## 4. Server-Side Request Forgery (SSRF) & XXE
- [ ] **Outbound URL Fetching**: If user-supplied URLs (webhooks, avatar URLs, imports) are fetched server-side, verify DNS resolution and IP blocklisting against loopback (`127.0.0.0/8`), link-local/cloud metadata (`169.254.169.254`), and RFC 1918 private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).

## 5. Secrets, Cryptography & Data Exposure
- [ ] **Cryptographic Primitives**: Flag weak algorithms (`MD5`, `SHA1` for passwords, `Math.random()` for tokens/IDs). Require `Argon2id` / `scrypt` for passwords and `crypto.randomBytes` / `crypto.randomUUID` for tokens.
- [ ] **Log & Error Leakage**: Ensure stack traces, database error details, and PII/tokens are stripped from external HTTP error responses and redacted in structured logs.

## 6. Output Format for `@security-audit`
Present findings in a severity-ranked table (`Critical`, `High`, `Medium`, `Low`, `Informational`) including CWE identifiers, exact file/line links, a concrete exploit scenario, and a drop-in remediation patch.

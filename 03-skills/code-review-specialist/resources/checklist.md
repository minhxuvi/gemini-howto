# Code Review Specialist Checklist (`resources/checklist.md`)

Use this checklist during **Step 2** of the `code-review-specialist` workflow to ensure every high-risk category is systematically evaluated.

---

## 1. Security & Trust Boundaries (OWASP Top 10)

- [ ] **Injection Prevention**: Are all SQL queries parameterized? Are shell invocations using argument arrays (`execFile`/`spawn` with `shell: false`) instead of string concatenation?
- [ ] **Authorization & Tenant Isolation (BOLA/IDOR)**: Does every data-access query filter by the authenticated user's `organization_id` or `user_id` rather than trusting a resource ID from `req.params` or `req.body` alone?
- [ ] **Input Schema Validation**: Are request bodies, query parameters, and headers validated against a strict schema (`Zod`, `TypeBox`, `Pydantic`) with unknown keys stripped or rejected?
- [ ] **Secrets & PII Hygiene**: Are API keys, JWT secrets, and passwords loaded exclusively from secret managers/environment variables and redacted from logs and error responses?
- [ ] **Cryptographic Safety**: Are webhook HMAC signatures and tokens compared with `crypto.timingSafeEqual`? Is `crypto.randomBytes`/`randomUUID` used instead of `Math.random()`?

---

## 2. Performance, Database & Resource Management

- [ ] **No N+1 Queries**: Are database queries or outbound HTTP calls ever executed inside a `for`/`forEach`/`.map()` loop? Replace with batched `WHERE id IN (...)` queries or joins.
- [ ] **Algorithmic Complexity**: Are there nested array scans (`.find()`, `.includes()`, `.filter()`) inside loops yielding $O(N \times M)$ complexity? Convert the inner collection to a `Map` or `Set` for $O(1)$ lookup.
- [ ] **Async Concurrency**: Are independent `await` calls executed sequentially when they could run concurrently via `Promise.all()` / `asyncio.gather()`? Conversely, are large fan-outs bounded by a concurrency limit?
- [ ] **Resource Cleanup**: Are file handles, database transactions, streams, timers, and `AbortController` signals properly cleaned up in `finally` blocks or `using` / `defer` statements?
- [ ] **Pagination & Bounds**: Does every list endpoint or bulk query enforce a maximum `LIMIT` to prevent out-of-memory crashes on large tenants?

---

## 3. Correctness, Concurrency & Error Handling

- [ ] **Explicit Error Propagation**: Are `catch` blocks preserving root causes (`{ cause: err }`, `from err`, `%w`) and avoiding silent swallowing?
- [ ] **Idempotency & Race Conditions**: If a request or background job is retried or executed concurrently, could it double-charge a customer or corrupt state? (Check for `SELECT ... FOR UPDATE`, optimistic locking, or idempotency keys.)
- [ ] **Boundary & Null Safety**: Are empty arrays `[]`, `0`, empty strings `""`, `null`/`undefined`, and timezone/leap-year boundaries handled safely?
- [ ] **Financial & Floating-Point Precision**: Are currency calculations performed using integer minor units (cents) or arbitrary-precision `Decimal` rather than IEEE 754 `float`/`number`?

---

## 4. Maintainability, Architecture & Testing

- [ ] **Single Responsibility & Size**: Are functions under ~50 lines with a single clear level of abstraction?
- [ ] **Type Safety**: Are `any`, `@ts-ignore`, or unchecked type casts (`as unknown as T`) avoided in favor of discriminated unions and type guards?
- [ ] **Test Coverage Parity**: Do unit/integration tests cover both the happy path and the new error/edge branches introduced in this change?

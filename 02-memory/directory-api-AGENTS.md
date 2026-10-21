# API Package Instructions (`packages/api/AGENTS.md`)

> **Template Usage**: Copy this file to a subdirectory such as `packages/api/AGENTS.md` (or `packages/api/GEMINI.md`). Antigravity loads this file **on demand via hierarchical directory walk-up** whenever the agent reads or edits any file inside `packages/api/**`, supplementing the root `./GEMINI.md`.

## 1. Scope & Responsibility

This package (`@acme/api`) owns the external HTTP/REST API gateway, webhook ingestion endpoints, OpenAPI schema generation, and authentication middleware.
- **It MUST NOT** contain raw SQL strings or direct Drizzle table definitions (import repository methods from `@acme/db`).
- **It MUST NOT** execute synchronous CPU-bound workloads >10ms on the Fastify event loop.

---

## 2. Route Handler & Schema Conventions

1. **Contract-First Route Registration**:
   - Every route in `packages/api/src/routes/**` must declare `schema: { params, querystring, body, response }` using `TypeBox` (`@sinclair/typebox`) so Fastify compiles fast JSON serializers and auto-generates OpenAPI 3.1 specs.
2. **Authentication & Tenant Isolation**:
   - Every route under `/v1/*` (except `/v1/health` and `/v1/webhooks/*`) must attach the `requireAuth` preHandler hook.
   - **Tenant Guard**: Always scope database queries by `req.auth.organizationId` extracted from the verified JWT—never trust an `organizationId` passed in the query string or request body without verifying membership.
3. **Standard Response Envelope**:
   - Collection endpoints (`GET /v1/<resource>`) must use cursor-based pagination (`cursor`, `limit` max `100`) and return:
     ```json
     {
       "data": [],
       "pagination": {
         "nextCursor": "cur_01J9...",
         "hasMore": true
       },
       "requestId": "req_98a7b6c5"
     }
     ```
   - Error responses must be thrown via `AppError` subclasses (`NotFoundError`, `ConflictError`, `ValidationError`) so the central Fastify error handler formats RFC 9457 Problem Details (`application/problem+json`).

---

## 3. Webhook Ingestion Rules (`src/routes/webhooks/`)

- **Raw Body Signature Verification**: Always verify HMAC signatures (`stripe-signature`, `x-hub-signature-256`) against `req.rawBody` using `crypto.timingSafeEqual` **before** parsing or acting on the JSON payload.
- **Idempotent Fast Ack**: Persist the incoming `eventId` in Redis/Postgres (`INSERT ... ON CONFLICT DO NOTHING`), enqueue background processing, and return `202 Accepted` within `250ms`.

---

## 4. Verification Commands for `packages/api`

When modifying files in `packages/api/`, run these scoped checks before completing your task:

```bash
pnpm --filter @acme/api typecheck
pnpm --filter @acme/api test
pnpm --filter @acme/api openapi:validate
```

# Project Instructions (`GEMINI.md`)

> **Template Usage**: Copy this file to `./GEMINI.md` (or `./AGENTS.md`) at the root of your repository. Standalone `GEMINI.md` and `AGENTS.md` files do **not** use YAML frontmatter and are always active for their directory scope.

## 1. System Overview & Tech Stack

- **Service**: `acme-commerce-platform` (Multi-tenant B2B Order & Billing Platform)
- **Runtime & Language**: Node.js 22 LTS, TypeScript 5.8 (`strict: true`, `noUncheckedIndexedAccess: true`)
- **Backend Framework**: Fastify v5 + TypeBox schema validation (`packages/api/`)
- **Frontend Framework**: Next.js 15 App Router + React 19 + Tailwind CSS v4 (`packages/web/`)
- **Data Layer**: PostgreSQL 17 (Drizzle ORM), Redis 7.4 (idempotency & rate limiting), Kafka (async domain events)
- **Package Manager**: `pnpm` v9 workspaces (monorepo managed via Turborepo)

---

## 2. Essential Development Commands

Always use `pnpm` (never `npm` or `yarn`). Run commands from the repository root or scoped via `--filter`:

| Action | Command | Notes |
| :--- | :--- | :--- |
| **Install dependencies** | `pnpm install --frozen-lockfile` | Never modify lockfile without explicit dependency change |
| **Build all packages** | `pnpm build` | Runs `turbo run build` across dependency graph |
| **Typecheck** | `pnpm typecheck` | Runs `tsc --noEmit` across all workspaces |
| **Lint & Format Check** | `pnpm lint` | Biome linter + formatter check (`pnpm format` to auto-fix) |
| **Unit Tests (Fast)** | `pnpm test:unit` | Vitest unit suite (no Docker required, `<5s`) |
| **Integration Tests** | `pnpm test:integration` | Requires local PostgreSQL & Redis via `docker compose up -d` |
| **Single Test File** | `pnpm --filter @acme/api test src/orders/create.test.ts` | Always run targeted tests first before full suite |
| **Generate DB Migration** | `pnpm --filter @acme/db db:generate` | Generates SQL migration from Drizzle schema changes |

---

## 3. Architecture & File Reference Pointers

We use Antigravity's `@path` pointers for on-demand reference (zero upfront token cost) and `@[label](path)` for mandatory inline invariants:

- **System Architecture & Service Boundaries**: Read @docs/architecture-overview.md when designing cross-package features.
- **Database Schema Source of Truth**: Inspect @packages/db/src/schema/index.ts before writing queries or migrations.
- **Shared Error Catalogue**: Use error classes from @packages/shared/src/errors/domain-errors.ts.

<!-- Optional inline inclusion example (uncomment if docs/security-invariants.md exists in your repo):
@[Core Security Invariants](docs/security-invariants.md)
-->

---

## 4. Non-Negotiable Coding & Architectural Invariants

1. **Strict Module Boundaries**:
   - Never import from another package's `src/` or `internal/` directory (`@acme/db/src/...` is forbidden). Always import via the package's public barrel export (`@acme/db`).
2. **Financial & Currency Arithmetic**:
   - All monetary amounts in the database and API payloads are represented as **integer minor units** (`amountCents: bigint | number`) alongside an explicit ISO 4217 `currency` code.
   - Never use IEEE 754 floating-point math (`number` division/multiplication) for tax or discount calculations; use `Decimal` from `decimal.js` with `ROUND_HALF_EVEN` (banker's rounding).
3. **Database Access & Transactions**:
   - Every multi-table write MUST execute inside `db.transaction(async (tx) => { ... })`.
   - Always pass an explicit `{ signal: AbortSignal.timeout(5000) }` or statement timeout on user-facing queries.
4. **Structured Logging & PII Redaction**:
   - Use the request-scoped Pino logger (`req.log.info({ orderId }, "Order created")`). Never use `console.log` in production packages.
   - Never log raw `Authorization` headers, API keys, payment card details, or customer email addresses.
5. **Deterministic Testing**:
   - Never hit live third-party APIs (Stripe, SendGrid, OIDC providers) in unit or integration tests. Use the typed mock harnesses in `packages/test-utils/`.

---

## 5. Known Gotchas & Environment Quirks

- **BigInt Serialization**: Fastify's default `JSON.stringify` throws on native JS `BigInt`. Always run monetary `bigint` columns through `serializeMoney(amount, currency)` in `@acme/shared` before returning HTTP responses.
- **Local Test Database Port**: `docker-compose.yml` maps PostgreSQL to host port **`5433`** (not `5432`) so it does not collide with local Postgres installations.

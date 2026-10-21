# Golden Example Files (`references/example-files.md`)

Use these concise, production-tested examples as models when authoring or refactoring `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md` files.

---

## Example 1: Concise Monorepo Root `GEMINI.md` (~60 Lines)

```markdown
# Project Instructions (`GEMINI.md`)

## Stack & Workspace Layout
- **Runtime**: Go 1.24 (`services/*`) + TypeScript 5.8 / Next.js 15 (`apps/console`)
- **Data**: Cloud Spanner (`services/ledger`), Redis 7.4, Pub/Sub

## Commands
- **Build all**: `make build`
- **Go unit tests (fast)**: `go test -race ./services/...`
- **Single Go package test**: `go test -v ./services/ledger/internal/posting`
- **Frontend typecheck & test**: `pnpm --filter console typecheck && pnpm --filter console test`
- **Lint**: `golangci-lint run && pnpm lint`

## Architecture Pointers
- Ledger double-entry invariants: @docs/ledger-invariants.md
- Spanner schema DDL: @services/ledger/schema/spanner.sql
- Protobuf definitions: @proto/acme/ledger/v1/ledger.proto

## Critical Invariants
1. **Double-Entry Balance**: Every `LedgerTransaction` write in `services/ledger` MUST verify `sum(debits) == sum(credits)` per currency before committing the Spanner read-write transaction.
2. **Spanner Commit Timestamps**: Always use `spanner.CommitTimestamp` for `created_at` and `posted_at` columns—never use application-server `time.Now()`.
3. **Context Propagation**: Pass `ctx context.Context` as the first argument to every I/O function; never use `context.Background()` inside request handlers.
```

---

## Example 2: Modular `model_decision` Rule (`.agents/rules/spanner-queries.md`)

```markdown
---
trigger: model_decision
description: "Apply these Cloud Spanner SQL optimization, index hint, and read-write transaction lock rules whenever writing or reviewing Spanner queries or repositories."
---

# Cloud Spanner Query & Transaction Rules

1. **Prefer `ReadOnlyTransaction` for Queries**: Never use `ReadWriteTransaction` for read-only workloads, as it acquires shared locks and increases abort contention.
2. **Parameterized SQL Only**: Always use `@paramName` syntax in `spanner.Statement{SQL: ..., Params: map[string]any{...}}`.
3. **Interleaved Table Joins**: Join parent and interleaved child tables on the full composite primary key prefix to ensure co-located local joins.
```

---

## Example 3: Modular `glob` Rule (`.agents/rules/frontend-components.md`)

```markdown
---
trigger: glob
globs: "apps/console/**/*.tsx, packages/ui/**/*.tsx"
description: "React 19 Server Components, accessibility, and Tailwind v4 conventions for UI files."
---

# Frontend Component Conventions

1. **Server Components by Default**: Do not add `"use client"` unless the component uses browser APIs, event handlers (`onClick`, `onChange`), or stateful React hooks (`useState`, `useEffect`).
2. **Accessible Interactive Elements**: Never attach `onClick` to a non-interactive `<div>` or `<span>`; always use semantic `<button type="button">` or `<a>` elements with visible `:focus-visible` rings.
```

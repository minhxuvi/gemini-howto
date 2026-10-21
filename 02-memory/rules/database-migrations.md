---
trigger: model_decision
description: "Apply these zero-downtime PostgreSQL migration and schema evolution rules whenever writing, reviewing, or modifying SQL migrations, Drizzle/Prisma schemas, or database indexes."
---

# Zero-Downtime Database Migration Rules

> **Activation Mode**: `trigger: model_decision` (Progressive Disclosure). Antigravity loads only the `description` above into the prompt index and reads this full file on demand when the task involves database schemas or migrations.

When authoring or reviewing database schema changes and SQL migrations, strictly enforce these zero-downtime PostgreSQL invariants:

## 1. Expand-and-Contract Pattern (No Breaking Drops/Renames)

Never drop, rename, or change the type of an active column or table in a single deployment while existing application pods are still running against the database:
1. **Release 1 (Expand)**: Add the new nullable column (`ALTER TABLE ... ADD COLUMN new_col ...`) and deploy dual-write application logic.
2. **Release 2 (Backfill & Switch Reads)**: Backfill historical rows in small batched transactions (`LIMIT 5000` with `FOR UPDATE SKIP LOCKED`), then switch application reads to `new_col`.
3. **Release 3 (Contract)**: Remove references to `old_col` in application code, deploy, and only then execute `ALTER TABLE ... DROP COLUMN old_col` in a subsequent migration.

## 2. Non-Blocking Index Creation & Removal

- Standard `CREATE INDEX` acquires a `SHARE` lock that blocks all `INSERT`, `UPDATE`, and `DELETE` operations on the table for the duration of the build.
- **Rule**: Every index added to an existing table MUST use `CONCURRENTLY` outside a transaction block:
  ```sql
  -- migrate: no-transaction
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_org_created_at
    ON orders (organization_id, created_at DESC);
  ```
- Similarly, always drop indexes with `DROP INDEX CONCURRENTLY IF EXISTS ...`.

## 3. Safe `NOT NULL` and Foreign Key Constraints

- **Never run `ALTER TABLE ... ADD COLUMN col TEXT NOT NULL` without a volatile-free default** on large existing tables, and never run `ALTER TABLE ... SET NOT NULL` directly without a pre-validated check constraint (which otherwise triggers a full-table scan under an `ACCESS EXCLUSIVE` lock).
- **Safe 3-Step Pattern for `NOT NULL` / Foreign Keys**:
  ```sql
  -- Step 1: Add constraint as NOT VALID (acquires brief lock, skips existing rows, enforces on new writes)
  ALTER TABLE invoices
    ADD CONSTRAINT chk_invoices_amount_not_null
    CHECK (amount_cents IS NOT NULL) NOT VALID;

  -- Step 2: Backfill any NULL rows in batches

  -- Step 3: Validate constraint (acquires SHARE UPDATE EXCLUSIVE lock; does NOT block reads/writes)
  ALTER TABLE invoices
    VALIDATE CONSTRAINT chk_invoices_amount_not_null;
  ```

## 4. Lock & Statement Timeouts

Every migration script running in production must start with explicit safety timeouts so a blocked lock acquisition fails fast rather than queueing all application traffic behind an `ACCESS EXCLUSIVE` waiter:

```sql
SET lock_timeout = '3s';
SET statement_timeout = '30s';
```

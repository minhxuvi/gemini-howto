# Sample Code Review Output (`examples/sample-review.md`)

> This example illustrates the structure, tone, quantitative scorecard, and actionable Before/After code patches expected from the `code-review-specialist` skill.

---

## Code Review Report: `src/services/payout-processor.ts`

- **Verdict**: 🔴 **REQUEST CHANGES** (1 Critical, 1 High, 1 Medium, 1 Low)
- **Reviewed Scope**: `src/services/payout-processor.ts` (142 lines)

### Quantitative Metrics (`scripts/check-metrics.sh`)

| File | Lines | Functions | Lines > 100 chars | `TODO` / `FIXME` |
| :--- | :---: | :---: | :---: | :---: |
| `src/services/payout-processor.ts` | 142 | 4 | 3 | 1 |

### Category Scorecard

| Category | Score (1–5) | Summary |
| :--- | :---: | :--- |
| **Security** | `2 / 5` | Missing tenant isolation check in `cancelPayout()` allows cross-tenant IDOR. |
| **Performance** | `2 / 5` | N+1 database query inside `settleBatchPayouts()` loop ($O(N)$ round-trips). |
| **Correctness** | `3 / 5` | Floating-point fee multiplication causes rounding drift on fractional cents. |
| **Maintainability** | `4 / 5` | Clean module structure and clear naming; needs unit test for partial batch failure. |

---

## Findings

### 1. [CRITICAL] Cross-Tenant Broken Object Level Authorization (BOLA / IDOR)
- **Location**: `src/services/payout-processor.ts:48-55`
- **Category**: Security (OWASP API1:2023)
- **Impact**: `cancelPayout(payoutId, actorOrgId)` looks up and updates the payout solely by `payoutId` without verifying that `payout.organizationId === actorOrgId`. Any authenticated user who guesses or enumerates a UUID can cancel another organization's pending payout.

**Before:**
```typescript
export async function cancelPayout(payoutId: string, actorOrgId: string) {
  const [updated] = await db
    .update(payouts)
    .set({ status: "cancelled", updatedAt: new Date() })
    .where(and(eq(payouts.id, payoutId), eq(payouts.status, "pending")))
    .returning();
  return updated;
}
```

**After (Drop-in Fix):**
```typescript
export async function cancelPayout(payoutId: string, actorOrgId: string) {
  const [updated] = await db
    .update(payouts)
    .set({ status: "cancelled", updatedAt: new Date() })
    .where(
      and(
        eq(payouts.id, payoutId),
        eq(payouts.organizationId, actorOrgId),
        eq(payouts.status, "pending")
      )
    )
    .returning();

  if (!updated) {
    throw new NotFoundError(`Pending payout ${payoutId} not found`);
  }
  return updated;
}
```

---

### 2. [HIGH] N+1 Database Query in `settleBatchPayouts()`
- **Location**: `src/services/payout-processor.ts:89-104`
- **Category**: Performance
- **Impact**: For a batch of 500 payouts, `db.query.merchantAccounts.findFirst()` is awaited inside the `for...of` loop, executing 500 sequential SQL round-trips (~2.5 seconds) instead of 1 batched `inArray` query (~8ms).

**Before:**
```typescript
for (const item of batchItems) {
  const account = await db.query.merchantAccounts.findFirst({
    where: eq(merchantAccounts.id, item.merchantId),
  });
  if (!account?.stripeAccountId) continue;
  await dispatchTransfer(item, account.stripeAccountId);
}
```

**After (Drop-in Fix):**
```typescript
const merchantIds = [...new Set(batchItems.map((i) => i.merchantId))];
const accounts = await db.query.merchantAccounts.findMany({
  where: inArray(merchantAccounts.id, merchantIds),
});
const accountByMerchantId = new Map(accounts.map((a) => [a.id, a]));

for (const item of batchItems) {
  const account = accountByMerchantId.get(item.merchantId);
  if (!account?.stripeAccountId) continue;
  await dispatchTransfer(item, account.stripeAccountId);
}
```

---

### 3. [MEDIUM] IEEE 754 Floating-Point Fee Calculation
- **Location**: `src/services/payout-processor.ts:118`
- **Category**: Correctness (Financial Math)
- **Impact**: `amountCents * 0.0145` produces non-integer floats (e.g., `1999 * 0.0145 = 28.985500000000003`) which causes Stripe integer parameter rejections. Use integer basis points (`145n` bps / `10_000n`) or `Decimal`.

---

## Positive Highlights
- Good use of idempotency keys (`idempotencyKey: \`payout_\${item.id}\``) when calling the downstream Stripe Transfers API on line 127.

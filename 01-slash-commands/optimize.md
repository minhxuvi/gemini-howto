---
name: optimize
description: >-
  Analyze code for performance bottlenecks, algorithmic complexity, N+1 database queries,
  memory leaks, and frontend bundle size regressions, then implement and benchmark verified
  optimizations. Use when the user runs /optimize or asks to profile, speed up, or reduce
  the memory or bundle footprint of a file, endpoint, or module.
---

# Performance & Resource Optimization (`/optimize`)

Use this skill when invoked via `/optimize [target]` or when the user asks to diagnose and fix performance, latency, memory, database query, or bundle size bottlenecks.

## Usage Examples

```text
/optimize src/services/order-processor.ts
/optimize Why is GET /api/v2/analytics taking >1.5s on large accounts?
/optimize --focus=memory src/workers/stream-ingestor.py
```

---

## Step-by-Step Agent Instructions

### Step 1: Scope & Baseline Measurement
1. **Identify Target**:
   - If the user passed a file path, symbol, endpoint, or directory after `/optimize`, focus on that target and its direct callees.
   - If no target was specified, run `git diff --name-only HEAD` to inspect recently modified code, or ask the user which hot path to analyze.
2. **Establish a Baseline**:
   - Look for existing benchmarks, load tests, or unit tests covering the target (`*bench*`, `*perf*`, `*test*`).
   - Run the relevant test or benchmark command to capture baseline execution time, query count, or bundle size before making edits.

### Step 2: Multi-Dimensional Bottleneck Audit
Audit the target code systematically across these five dimensions:

1. **Algorithmic & CPU Complexity**:
   - Identify $O(n^2)$ or worse nested loops, repeated array scans (`.find()` / `.includes()` inside `.map()` or `.filter()`), and redundant serialization/deserialization.
   - Replace linear lookups in hot loops with `Map` / `Set` hash indexes ($O(1)$ lookup).
   - Check for synchronous blocking I/O or heavy regex compilation inside per-request handlers.
2. **Database & I/O Efficiency (N+1 Queries)**:
   - Detect queries or network calls executed inside loops (`for`, `forEach`, `Promise.all(items.map(...))` hitting the DB per item).
   - Check for missing composite indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
   - Identify over-fetching (`SELECT *` or loading large relations when only IDs/counts are needed) and unbounded queries lacking pagination or `LIMIT`.
3. **Memory Footprint & Leaks**:
   - Spot unclosed event listeners, timers (`setInterval`), streams, or database cursors.
   - Identify unbounded in-memory caches (maps/arrays that grow without TTL or LRU eviction).
   - Look for unnecessary deep clones or large intermediate array allocations that can be streamed or iterated lazily.
4. **Concurrency & Async Waterfalls**:
   - Find sequential `await` statements for independent I/O operations that can be parallelized with `Promise.all()` / `asyncio.gather()` / `errgroup`.
   - Ensure bounded concurrency (worker pools / semaphores) when fanning out across large collections so downstream services aren't overwhelmed.
5. **Frontend Rendering & Bundle Size (if applicable)**:
   - Identify heavy third-party imports that block tree-shaking or should be dynamically imported (`lazy()` / `import()`).
   - Detect unnecessary component re-renders caused by unstable object/function references or overly broad state subscriptions.

### Step 3: Prioritized Optimization Report
Before applying invasive structural changes, present a concise findings table ordered by impact:

| Priority | Category | Location | Root Cause | Complexity / Cost Change |
| :--- | :--- | :--- | :--- | :--- |
| **Critical** | N+1 Query | `order.ts:142` | `getUser()` called inside loop of $N$ orders | $N+1$ queries $\rightarrow$ $1$ batched `WHERE id IN (...)` query |
| **High** | Algorithmic | `matcher.ts:88` | `items.find()` inside `records.map()` | $O(N \times M) \rightarrow O(N + M)$ using `Map` |
| **Medium** | Async Waterfall | `report.ts:54` | 3 independent `await` fetches run serially | $\text{Latency} = t_1 + t_2 + t_3 \rightarrow \max(t_1, t_2, t_3)$ |

### Step 4: Implementation & Verification
1. **Apply Optimizations**: Implement the high-impact fixes while strictly preserving external API contracts, return types, and error handling behavior.
2. **Run Verification Suite**:
   - Execute the existing unit/integration test suite to confirm zero regressions.
   - Re-run the baseline benchmark or timing script from Step 1 and report the measured before/after improvement.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

---
name: unit-test-expand
description: >-
  Analyze line and branch coverage gaps in target modules and write deterministic unit tests
  covering happy paths, boundary conditions, malformed inputs, concurrency races, and error
  handling. Use when the user runs /unit-test-expand or asks to increase test coverage.
---

# Unit Test Coverage Expansion (`/unit-test-expand`)

Use this skill when invoked via `/unit-test-expand [target-file-or-dir]` or when the user asks to close test coverage gaps and test edge cases.

## Usage Examples

```text
/unit-test-expand src/billing/invoice-calculator.ts
/unit-test-expand services/auth/
/unit-test-expand --target-coverage=90 src/utils/parser.py
```

---

## Step-by-Step Agent Instructions

### Step 1: Discover Test Runner & Baseline Coverage
1. **Identify Framework & Conventions**:
   - Inspect existing test files (`*.test.ts`, `*.spec.ts`, `test_*.py`, `*_test.go`, `*_test.rs`) to match the project's test runner (`Vitest`, `Jest`, `pytest`, `go test`, `cargo test`), assertion style, and directory layout (co-located vs. `tests/` folder).
2. **Run Baseline Coverage**:
   - Execute the coverage command for the target module (e.g., `npx vitest run --coverage <target>`, `pytest --cov=<target> --cov-report=term-missing`, `go test -coverprofile=coverage.out ./...`).
   - Identify exact uncovered lines, untested conditional branches (`if/else`, `switch`, ternary, nullish coalescing), and unexercised `catch` blocks.

### Step 2: Map Untested Branches & Edge-Case Matrix
Before writing test code, build a coverage matrix across these five categories for every public function/method in the target:

| Category | Scenarios to Cover |
| :--- | :--- |
| **1. Happy Path** | Standard valid inputs, expected state transitions, and return value invariants. |
| **2. Boundary & Empty Values** | `0`, `-1`, `MAX_SAFE_INTEGER`, `NaN`, empty string `""`, whitespace-only `"   "`, empty array `[]`, single-element array `[x]`, `null` / `undefined` / `None`. |
| **3. Error & Rejection Paths** | Invalid argument types, network/DB timeouts, malformed JSON, unauthorized access, and custom domain exceptions. |
| **4. State & Idempotency** | Repeated calls with identical inputs, out-of-order execution, and partial failure rollback. |
| **5. Time & Concurrency** | Leap years, timezone boundaries (`UTC` vs. local), expired TTLs (using fake timers), and concurrent `Promise.all` calls. |

### Step 3: Write Deterministic, High-Signal Tests
Follow these strict testing principles when authoring the new test cases:
1. **Arrange-Act-Assert (AAA)**: Structure every test clearly into setup (`Arrange`), execution (`Act`), and verification (`Assert`).
2. **Zero Flakiness (Deterministic Isolation)**:
   - Never rely on wall-clock `setTimeout` delays, live external HTTP endpoints, or shared mutable global state between tests.
   - Use fake timers (`vi.useFakeTimers()`, `jest.useFakeTimers()`, `freezegun`) and mock only external I/O boundaries (database, network, filesystem)—never mock the unit under test itself.
3. **Table-Driven / Parameterized Tests**: Use `it.each(...)` (Vitest/Jest), `@pytest.mark.parametrize` (Python), or table structs (Go) to test boundary permutations cleanly without copy-paste boilerplate.
4. **Assert Behavior, Not Implementation**: Assert on public return values, thrown error types/codes, and observable side effects rather than private internal helper calls.

### Step 4: Execute & Verify Coverage Delta
1. Run the test suite to verify 100% of newly added tests pass.
2. Re-run the coverage command from Step 1 and report a before/after summary table:

| File | Before (Line / Branch %) | After (Line / Branch %) | New Test Cases Added |
| :--- | :---: | :---: | :--- |
| `src/billing/invoice-calculator.ts` | `62.4% / 48.0%` | `96.8% / 92.5%` | +14 tests (rounding, negative discounts, tax-exempt) |

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |

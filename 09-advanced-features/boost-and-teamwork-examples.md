# Playbook: `/boost`, `/teamwork-preview`, `/goal`, and `/grill-me`

Real-world engineering prompts and operational patterns for Antigravity's specialized multi-agent reasoning commands.

---

## 1. `/boost` Playbooks (3-Phase Multi-Agent Deep Reasoning)

Use `/boost` when a problem requires hypothesis testing, trace correlation, or competing implementations in isolated Git worktrees (`Seconds to Hours`).

### Playbook 1A: Hunting an Intermittent Concurrency Bug
```text
/boost Our Go gRPC worker pool in internal/pool/ occasionally deadlocks when a downstream stream cancels mid-batch under >500 RPS. Formulate hypotheses, write a deterministic reproduction test with -race enabled, and implement a deadlock-free fix.
```
**What happens behind the scenes**:
1. **Phase 1 (Strategic Orchestrator)**: Inspects `internal/pool/`, maps channel lifecycles and mutex acquisition order, and defines a `go test -race -count=50` verification harness.
2. **Phase 2 (Parallel Execution)**:
   - `DeepInvestigator` traces context cancellation propagation across goroutines without modifying files.
   - `DeepCoder` builds the reproduction test and tests candidate lock-ordering fixes in an isolated worktree.
3. **Phase 3 (Synthesis)**: Runs the full `-race` suite across 50 iterations and merges the verified fix back into your workspace.

### Playbook 1B: Algorithmic Optimization with Benchmarks
```text
/boost Optimize the JSONL trajectory parser in src/parser/stream.ts to cut heap allocations by at least 50% on 100MB logs while keeping all existing edge-case tests green. Include a before/after benchmark.
```

---

## 2. `/teamwork-preview` Playbooks (2-Phase Autonomous Agent Teams)

Use `/teamwork-preview` for large multi-file migrations, greenfield subsystem builds, or formal mathematical proofs (`Hours to Days`).

### Playbook 2A: Framework Migration (`development` Integrity Mode)
```text
/teamwork-preview Migrate our Express v4 backend (38 route handlers and 6 middleware layers) to Fastify v5 with full TypeScript schema validation, OpenAPI 3.1 generation, and zero regression across our integration test suite.
```
**How to answer the Phase 1 Scoping Interview**:
- **Objective & Audience**: Production migration for our core API service.
- **Shortcuts / Integrity Mode**: Select **`development`** (allows standard Fastify plugins like `@fastify/swagger` and `@fastify/jwt`).
- **Verification Rubric**: `npm run typecheck && npm run test:integration` plus a latency comparison script.
- **Approval**: Review the generated **Prompt Artifact** (`~/teamwork_projects/fastify-migration`) and click **Proceed**.
- **Phase 2 Execution**: **Sentinel** spawns the **Project Orchestrator**, which assigns non-overlapping route files to **Workers** and subjects every milestone to the **Critic → Challenger → Auditor → Success Auditor** pipeline.

### Playbook 2B: From-Scratch Systems / Benchmark Build (`benchmark` Integrity Mode)
```text
/teamwork-preview Implement a cycle-accurate RISC-V RV32IMC instruction-set simulator in Rust with a 5-stage pipeline, hazard detection unit, and lockstep verification harness against golden trace vectors.
```
- During the Phase 1 interview, rule out external emulator crates and test-peeking to lock the run into **`benchmark` integrity mode**, where the **Auditor** verifies 100% standard-library implementation and authentic test output.

---

## 3. `/goal` Playbooks (Unattended Autonomous Loops)

Use `/goal <objective>` when the task is well-defined but tedious—requiring dozens of edit-compile-test cycles until every file passes:

```text
/goal Enable strictNullChecks in tsconfig.json and resolve every resulting TypeScript compiler error across all 94 files in src/ without using 'any' or non-null assertions (!), ensuring the full test suite passes.
```

---

## 4. `/grill-me` & `/btw` Playbooks

### Stress-Testing a Design Before Coding (`/grill-me`)
```text
/grill-me I want to add multi-tenant row-level security (RLS) to our PostgreSQL billing tables. Interview me to uncover any edge cases around background cron jobs, admin impersonation, and connection pooling before we write the migration.
```

### Asking a Non-Interrupting Side Question (`/btw`)
While the main agent is in the middle of a 10-minute refactoring turn:
```text
/btw Which environment variable controls the Redis connection timeout in src/config/env.ts?
```
Then copy the answer to your clipboard without scrolling:
```text
/copy btw
```

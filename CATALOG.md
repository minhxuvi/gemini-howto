# Template Catalog: Copy-Paste Configurations for Google Antigravity & Gemini

**English** | [Tiếng Việt](vi/CATALOG.md)

Every template in **gemini-howto** is production-ready and designed to be copied directly into your workspace (`.agents/`) or global configuration (`~/.gemini/config/`).

---

## 1. Custom Slash-Command Skills (`01-slash-commands/`)

In Antigravity, any skill placed at `.agents/skills/<name>/SKILL.md` becomes both a `/<name>` slash command and a semantically auto-discovered capability.

| Template | Slash Command | Description | One-Line Install Command |
| :--- | :--- | :--- | :--- |
| [`optimize.md`](01-slash-commands/optimize.md) | `/optimize` | Profile hot paths, N+1 queries, memory allocations, and bundle size | `mkdir -p .agents/skills/optimize && cp 01-slash-commands/optimize.md .agents/skills/optimize/SKILL.md` |
| [`pr.md`](01-slash-commands/pr.md) | `/pr` | Run pre-PR checks, summarize branch diffs, and open/update a GitHub PR | `mkdir -p .agents/skills/pr && cp 01-slash-commands/pr.md .agents/skills/pr/SKILL.md` |
| [`commit.md`](01-slash-commands/commit.md) | `/commit` | Scan staged changes for secrets, verify lints, and craft a Conventional Commit | `mkdir -p .agents/skills/commit && cp 01-slash-commands/commit.md .agents/skills/commit/SKILL.md` |
| [`push-all.md`](01-slash-commands/push-all.md) | `/push-all` | Run full test suite, commit cleanly, push to remote, and verify CI status | `mkdir -p .agents/skills/push-all && cp 01-slash-commands/push-all.md .agents/skills/push-all/SKILL.md` |
| [`generate-api-docs.md`](01-slash-commands/generate-api-docs.md) | `/generate-api-docs` | Extract route handlers and generate OpenAPI 3.1 + Markdown reference docs | `mkdir -p .agents/skills/generate-api-docs && cp 01-slash-commands/generate-api-docs.md .agents/skills/generate-api-docs/SKILL.md` |
| [`doc-refactor.md`](01-slash-commands/doc-refactor.md) | `/doc-refactor` | Restructure docs, fix broken links, and add Mermaid architecture diagrams | `mkdir -p .agents/skills/doc-refactor && cp 01-slash-commands/doc-refactor.md .agents/skills/doc-refactor/SKILL.md` |
| [`setup-ci-cd.md`](01-slash-commands/setup-ci-cd.md) | `/setup-ci-cd` | Scaffold GitHub Actions or Cloud Build pipelines with caching and security gates | `mkdir -p .agents/skills/setup-ci-cd && cp 01-slash-commands/setup-ci-cd.md .agents/skills/setup-ci-cd/SKILL.md` |
| [`unit-test-expand.md`](01-slash-commands/unit-test-expand.md) | `/unit-test-expand` | Identify untested edge cases and generate deterministic unit tests | `mkdir -p .agents/skills/unit-test-expand && cp 01-slash-commands/unit-test-expand.md .agents/skills/unit-test-expand/SKILL.md` |

---

## 2. Rules & Persistent Memory (`02-memory/`)

| Template | Trigger / Type | Target Location | Purpose |
| :--- | :--- | :--- | :--- |
| [`project-GEMINI.md`](02-memory/project-GEMINI.md) | Always active (`GEMINI.md`) | `./GEMINI.md` | Workspace-wide tech stack, commands, architecture, and `@[label](path)` includes |
| [`personal-GEMINI.md`](02-memory/personal-GEMINI.md) | Global always active | `~/.gemini/GEMINI.md` | Personal coding preferences, tone, git workflow, and verification habits |
| [`directory-api-AGENTS.md`](02-memory/directory-api-AGENTS.md) | Hierarchical subdirectory | `packages/api/AGENTS.md` | Subtree-specific rules loaded only when touching files under `packages/api/` |
| [`rules/database-migrations.md`](02-memory/rules/database-migrations.md) | `trigger: model_decision` | `.agents/rules/database-migrations.md` | Progressive-disclosure zero-downtime SQL migration rules |
| [`rules/protobuf-conventions.md`](02-memory/rules/protobuf-conventions.md) | `trigger: glob` (`**/*.proto`) | `.agents/rules/protobuf-conventions.md` | File-pattern-scoped Protobuf & gRPC backward-compatibility rules |
| [`rules/security-audit.md`](02-memory/rules/security-audit.md) | `trigger: manual` (`@security-audit`) | `.agents/rules/security-audit.md` | On-demand OWASP & threat-modeling checklist loaded via `@security-audit` |
| [`rules.json`](02-memory/rules.json) | Rule inheritance manifest | `.agents/rules.json` | Cross-repository rule inheritance (`inherits`, `entries`, `include_only`, `exclude`) |
| [`clean-code-rules.md`](clean-code-rules.md) | Reusable `@[...](...)` include | `./clean-code-rules.md` | Modular clean-code principles for surgical diffs, type safety, and testing |

---

## 3. Multi-File Agent Skills (`03-skills/`)

| Skill Package | Bundled Assets | Target Location | Purpose |
| :--- | :--- | :--- | :--- |
| [`code-review-specialist/`](03-skills/code-review-specialist/SKILL.md) | `SKILL.md`, `scripts/check-metrics.sh`, `resources/checklist.md`, `examples/sample-review.md` | `.agents/skills/code-review-specialist/` | Automated diff complexity analysis and severity-graded code reviews |
| [`doc-generator/`](03-skills/doc-generator/SKILL.md) | `SKILL.md`, `scripts/extract-signatures.py`, `templates/api-template.md`, `examples/sample-docs.md` | `.agents/skills/doc-generator/` | AST-based Python/TS signature extraction and standardized documentation generation |
| [`refactor/`](03-skills/refactor/SKILL.md) | `SKILL.md` | `.agents/skills/refactor/` | Behavior-preserving incremental refactoring with test-first verification |
| [`gemini-md/`](03-skills/gemini-md/SKILL.md) | `SKILL.md`, `references/context-patterns.md`, `references/example-files.md` | `.agents/skills/gemini-md/` | Author, audit, and optimize `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md` within the 20k budget |
| [`blog-draft/`](03-skills/blog-draft/SKILL.md) | `SKILL.md`, `examples/good-post.md`, `examples/bad-post.md` | `.agents/skills/blog-draft/` | Technical engineering blog writer with anti-fluff style comparisons |
| [`brand-voice/`](03-skills/brand-voice/SKILL.md) | `SKILL.md` | `.agents/skills/brand-voice/` | Enforce developer-focused tone, terminology, and formatting across docs and UI copy |
| [`skills.json`](03-skills/skills.json) | Skill registry manifest | `.agents/skills.json` | Register external or shared monorepo skill directories |
| [`.agents/skills/self-assessment/`](.agents/skills/self-assessment/SKILL.md) | `SKILL.md`, `README.md`, `references/*.md` | `.agents/skills/self-assessment/` | Interactive 10-question Antigravity & Gemini proficiency diagnostic |
| [`.agents/skills/lesson-quiz/`](.agents/skills/lesson-quiz/SKILL.md) | `SKILL.md`, `README.md`, `references/question-bank.md` | `.agents/skills/lesson-quiz/` | Interactive 5-question quiz per module (`01`–`10`) using `ask_question` |

---

## 4. Specialized Subagents (`04-subagents/`)

Install any subagent into `.agents/agents/<name>.md` (workspace) or `~/.gemini/config/agents/<name>.md` (global):

| Subagent Template | Mode / Tools | Best Invoked With | Purpose |
| :--- | :--- | :--- | :--- |
| [`code-reviewer.md`](04-subagents/code-reviewer.md) | Read-only + `run_command` (sandbox) | `Workspace: "inherit"` | Holistic code quality, architecture, and maintainability review |
| [`secure-reviewer.md`](04-subagents/secure-reviewer.md) | Read-only + security scanners | `Workspace: "inherit"` | Deep security audit for injection flaws, auth bypasses, and secrets |
| [`debugger.md`](04-subagents/debugger.md) | Full read/write/command | `Workspace: "branch"` | Root-cause analysis, minimal reproduction test creation, and surgical fix |
| [`test-engineer.md`](04-subagents/test-engineer.md) | Full read/write/command | `Workspace: "branch"` | Unit, integration, and property-based test authoring with coverage verification |
| [`performance-optimizer.md`](04-subagents/performance-optimizer.md) | Full read/write/command | `Workspace: "branch"` | Benchmark-driven latency, memory, and SQL query optimization |
| [`documentation-writer.md`](04-subagents/documentation-writer.md) | Read/write + Mermaid | `Workspace: "inherit"` | Keep READMEs, ADRs, OpenAPI specs, and changelogs synchronized with code |
| [`clean-code-reviewer.md`](04-subagents/clean-code-reviewer.md) | Read-only | `Workspace: "inherit"` | Audit complexity, naming, dead code, and SOLID adherence |
| [`implementation-agent.md`](04-subagents/implementation-agent.md) | Full read/write/command | `Workspace: "branch"` or `"share"` | Parallel feature worker for executing discrete tasks from an Implementation Plan |
| [`data-scientist.md`](04-subagents/data-scientist.md) | Read/write/command (`uv`/`python3`) | `Workspace: "inherit"` | Exploratory data analysis, statistical validation, and data pipeline profiling |

---

## 5. MCP Server Configurations (`05-mcp/`)

Merge into `~/.gemini/config/mcp_config.json` or `<plugin-root>/mcp_config.json`:

| Template | Transport Types | Servers Configured |
| :--- | :--- | :--- |
| [`github-mcp.json`](05-mcp/github-mcp.json) | Streamable HTTP (`${GITHUB_PERSONAL_ACCESS_TOKEN}`) + Stdio fallback | GitHub Issues, PRs, Actions, Code Search |
| [`database-mcp.json`](05-mcp/database-mcp.json) | Stdio | PostgreSQL (`@modelcontextprotocol/server-postgres`) & SQLite |
| [`filesystem-mcp.json`](05-mcp/filesystem-mcp.json) | Stdio | Scoped local filesystem & Git repository MCP servers |
| [`multi-mcp.json`](05-mcp/multi-mcp.json) | Streamable HTTP + Stdio | Full-stack bundle: GitHub, Postgres, Sentry, Slack, and Context7 docs |

---

## 6. Lifecycle Hooks (`06-hooks/`)

| File | Lifecycle Event | Matcher | Purpose |
| :--- | :--- | :--- | :--- |
| [`hooks.json`](06-hooks/hooks.json) | All 6 events | Complete config | Drop-in `.agents/hooks.json` wiring up all 8 scripts below |
| [`pre-tool-check.sh`](06-hooks/pre-tool-check.sh) | `PreToolUse` | `run_command` | Blocks destructive commands (`rm -rf /`, force push) and rewrites `grep` via `overwrite` |
| [`security-scan.sh`](06-hooks/security-scan.sh) | `PreToolUse` | `write_to_file\|replace_file_content\|multi_replace_file_content` | Scans file edits for hardcoded AWS/GCP/API keys and returns `"decision": "deny"` |
| [`pre-commit.sh`](06-hooks/pre-commit.sh) | `PreToolUse` | `run_command` (`git commit`) | Runs linter and fast unit tests before allowing `git commit` to execute |
| [`format-code.sh`](06-hooks/format-code.sh) | `PostToolUse` | `write_to_file\|replace_file_content\|multi_replace_file_content` | Auto-formats modified files using `prettier`, `ruff`, or `gofmt` |
| [`log-commands.sh`](06-hooks/log-commands.sh) | `PostToolUse` | `.*` | Appends structured JSON audit trail to `.agents/audit.log` |
| [`session-init.sh`](06-hooks/session-init.sh) | `SessionStart` | — | Injects current git branch, dirty file count, and runtime versions via `injectSteps` |
| [`context-tracker.py`](06-hooks/context-tracker.py) | `PreInvocation` | — | Monitors transcript size and injects an `ephemeralMessage` reminder when context grows large |
| [`goal-gate.sh`](06-hooks/goal-gate.sh) | `Stop` | — | Checks `fullyIdle` and blocks stopping (`"decision": "continue"`) if test suite is failing |

---

## 7. Native Antigravity Plugin Bundles (`07-plugins/`)

Install locally with `agy plugin install ./07-plugins/<name>` and validate with `agy plugin validate ./07-plugins/<name> --strict`:

| Plugin Bundle | Components Included | Purpose |
| :--- | :--- | :--- |
| [`pr-review/`](07-plugins/pr-review/README.md) | `plugin.json`, `rules/AGENTS.md`, `hooks.json`, `skills/review-pr`, `skills/pr-summary`, `agents/security-reviewer.md`, `agents/performance-reviewer.md` | End-to-end pull request review, security scanning, and summary generation |
| [`devops-automation/`](07-plugins/devops-automation/README.md) | `plugin.json`, `rules/AGENTS.md`, `hooks.json`, `mcp_config.json`, `skills/deploy`, `skills/rollback`, `agents/incident-responder.md` | Safe deployment orchestration, rollback runbooks, and incident triage |
| [`documentation/`](07-plugins/documentation/README.md) | `plugin.json`, `rules/AGENTS.md`, `hooks.json`, `skills/docs-update`, `agents/api-documenter.md` | Automated documentation synchronization and OpenAPI/Mermaid generation |

---

## 8. Checkpoints, Artifacts, Generative UI & Sidecars (`08-checkpoints/`)

| Template | Type | Purpose |
| :--- | :--- | :--- |
| [`checkpoint-and-worktree-examples.md`](08-checkpoints/checkpoint-and-worktree-examples.md) | Playbook | Workflows for `/rewind` (conversation-only vs code+chat), `/fork`, and Git Worktrees |
| [`implementation-plan-template.md`](08-checkpoints/implementation-plan-template.md) | Artifact Template | Structured Antigravity **Implementation Plan** with inline-review sections & verification plan |
| [`generative-ui-widget.html`](08-checkpoints/generative-ui-widget.html) | Generative UI (`<agent-embed>`) | Interactive Model Latency & Token Cost Simulator using `tailwindcss.min.js` and `var(--card)` CSS tokens |
| [`sidecar-schedule-example.json`](08-checkpoints/sidecar-schedule-example.json) | Scheduled Automation (`sidecar.json`) | Daily 9:00 AM (`CRON_TZ`) PR & CI triage automation with scoped `access_grants` |
| [`sidecar-worker-example.json`](08-checkpoints/sidecar-worker-example.json) | Daemon Sidecar (`sidecar.json`) | Persistent background worker & `sidecar://` interactive panel configuration |

---

## 9. Advanced Features, Permissions & Python SDK (`09-advanced-features/` & `10-cli/`)

| Template | Module | Purpose |
| :--- | :--- | :--- |
| [`settings-examples.json`](09-advanced-features/settings-examples.json) | `09-advanced-features/` | Annotated `~/.gemini/antigravity-cli/settings.json` profiles (`defaultRulesBudget`, `editorMode`, `altScreen`) |
| [`permissions-examples.json`](09-advanced-features/permissions-examples.json) | `09-advanced-features/` | `Deny > Ask > Allow` profiles (Strict Enterprise, Full-Stack Web, Autonomous CI) with `regex:` |
| [`boost-and-teamwork-examples.md`](09-advanced-features/boost-and-teamwork-examples.md) | `09-advanced-features/` | Prompt templates and playbooks for `/boost`, `/teamwork-preview`, `/goal`, and `/grill-me` |
| [`planning-mode-examples.md`](09-advanced-features/planning-mode-examples.md) | `09-advanced-features/` | Structured architecture planning and inline plan review recipes |
| [`sdk-examples/hello_agent.py`](10-cli/sdk-examples/hello_agent.py) | `10-cli/` | Basic `google-antigravity` `Agent`, `GeminiModelOptions`, and streaming `thoughts`/`tool_calls` |
| [`sdk-examples/custom_tools_and_mcp.py`](10-cli/sdk-examples/custom_tools_and_mcp.py) | `10-cli/` | Custom Python tools, `InlineSkill`, `SubagentConfig`, and declarative `allow`/`deny` policies |
| [`sdk-examples/dynamic_workflow.py`](10-cli/sdk-examples/dynamic_workflow.py) | `10-cli/` | Multi-step `@beta.workflows.define` orchestration with `phase`, `parallel`, and `pipeline` |
| [`sdk-examples/local_litert_agent.py`](10-cli/sdk-examples/local_litert_agent.py) | `10-cli/` | Offline on-device agent using `LiteRTAgentConfig` (Gemma 4 26B) and `LocalOpenAIAgentConfig` (Ollama) |

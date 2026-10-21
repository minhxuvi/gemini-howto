# Self-Assessment Question Bank (Modules 01–10)

This question bank contains **22 multiple-choice questions** (at least 2 per module across Modules 01 through 10). When running `/self-assessment`, select **1 question per module** (10 questions total), shuffle the 4 options before calling `ask_question`, and never reveal the answer before the user responds.

---

## Module 01: Slash Commands (`01-slash-commands`)

### M01-Q1 (Variant A)
- **Question**: You want the agent to interview you with clarifying questions and challenge edge cases in your design before writing any code. Which built-in Antigravity slash command should you run?
- **Options**:
  - A) `/grill-me`
  - B) `/btw`
  - C) `/learn`
  - D) `/goal`
- **Correct**: A
- **Explanation**: `/grill-me` launches an interactive design alignment interview where the agent probes ambiguities, edge cases, and trade-offs before implementation. `/btw` asks a side question without polluting main task flow, `/learn` persists newly discovered repo conventions into a skill/rule, and `/goal` runs a thorough autonomous loop until the goal is achieved.

### M01-Q2 (Variant B)
- **Question**: How are custom `/<name>` slash commands created and exposed in Google Antigravity?
- **Options**:
  - A) By defining a skill at `.agents/skills/<name>/SKILL.md` (which automatically registers `/<name>` in the slash menu)
  - B) By adding shell aliases to `~/.zshrc` with the `agy_` prefix
  - C) By registering custom routes inside `~/.gemini/config/mcp_config.json`
  - D) Only built-in commands (`/` commands shipped with the binary) can be invoked with a slash
- **Correct**: A
- **Explanation**: In Google Antigravity, skills located in `.agents/skills/<name>/SKILL.md` (or `~/.gemini/skills/<name>/SKILL.md`) automatically register as user-invocable `/<name>` slash commands in addition to supporting contextual auto-discovery.

---

## Module 02: Memory & Rules (`02-memory`)

### M02-Q1 (Variant A)
- **Question**: You have a rule file in `.agents/rules/database-migrations.md` that should only be loaded when the agent's semantic router determines the task involves schema changes or SQL migrations. Which YAML frontmatter `trigger` value should you use?
- **Options**:
  - A) `trigger: model_decision` (with a clear `description` field)
  - B) `trigger: always_on`
  - C) `trigger: glob`
  - D) `trigger: manual`
- **Correct**: A
- **Explanation**: `trigger: model_decision` uses the `description` frontmatter field so Antigravity semantically evaluates whether the rule is relevant to the current prompt before loading its body. `always_on` loads on every turn, `glob` matches active file paths, and `manual` only activates when explicitly referenced via `@rule-name`.

### M02-Q2 (Variant B)
- **Question**: What is the context budget for `always_on` rules (`GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md`), and how do you reference external project files inside a rule?
- **Options**:
  - A) ~24 KB (~20,000 tokens) combined budget for `always_on` rules, using `@[label](path/to/file)` links for modular references
  - B) 500 KB per file with `#include <path>` C-style macros
  - C) 1,000 tokens total across the entire repository, using `{{import:path}}` syntax
  - D) Unlimited token budget; all Markdown files in the repo are concatenated automatically on startup
- **Correct**: A
- **Explanation**: Antigravity enforces an approximate 24 KB (~20,000-token) budget for `always_on` instruction files (`GEMINI.md`, `AGENTS.md`, and `always_on` rules) to prevent context bloat, and supports `@[label](path)` links plus `.agents/rules.json` toggles to keep core instructions lean.

---

## Module 03: Skills (`03-skills`)

### M03-Q1 (Variant A)
- **Question**: How does Antigravity's 3-stage progressive disclosure work for skills in `.agents/skills/<name>/SKILL.md`?
- **Options**:
  - A) Stage 1 loads only YAML frontmatter (`name` + `description`); Stage 2 reads `SKILL.md` when triggered; Stage 3 reads `scripts/`, `references/`, or `resources/` on demand
  - B) Stage 1 runs all scripts in `scripts/`; Stage 2 reads `SKILL.md`; Stage 3 writes output to `.agents/skills.json`
  - C) All `SKILL.md` files and `references/` are loaded into the system prompt at session startup
  - D) Skills are compiled into binary `.wasm` modules before the conversation starts
- **Correct**: A
- **Explanation**: Progressive disclosure preserves the context window: at startup only the compact `name` and `description` metadata are visible (Stage 1). When a skill is matched or invoked, the agent reads `SKILL.md` (Stage 2) and only loads helper files in `references/`, `scripts/`, or `examples/` when needed (Stage 3).

### M03-Q2 (Variant B)
- **Question**: Which file lets a team selectively enable or disable specific skills in a workspace without deleting their `.agents/skills/<name>/` directories?
- **Options**:
  - A) `.agents/skills.json`
  - B) `~/.gemini/config/mcp_config.json`
  - C) `.agents/hooks.json`
  - D) `package.json`
- **Correct**: A
- **Explanation**: `.agents/skills.json` acts as the workspace registry/control file for enabling, disabling, or configuring installed skills without removing their directories from version control.

---

## Module 04: Subagents (`04-subagents`)

### M04-Q1 (Variant A)
- **Question**: When spawning multiple subagents via `invoke_subagent` to implement competing approaches in parallel without dirtying your main working tree or duplicating the entire `.git` object store, which `Workspace` mode is ideal?
- **Options**:
  - A) `Workspace: "share"` (or `"branch"` for full isolated clone/branch)
  - B) `Workspace: "inherit"`
  - C) `Workspace: "readonly"`
  - D) `Workspace: "tmpfs"`
- **Correct**: A
- **Explanation**: `invoke_subagent` supports three workspace modes: `inherit` (shares the parent's live working tree), `branch` (creates an isolated branched/cloned workspace), and `share` (creates an isolated working directory sharing the underlying repository storage, similar to a git worktree/`hg share`).

### M04-Q2 (Variant B)
- **Question**: How should a parent agent wait for a background subagent (e.g., `research`, `browser`, `self`, or a custom `.agents/agents/<name>.md` subagent) to finish its task?
- **Options**:
  - A) Stop calling tools (or continue independent work) and rely on reactive wakeup when the subagent calls `send_message` back to the parent
  - B) Run a `while true; do sleep 5; done` bash loop to poll the subagent transcript file
  - C) Call `manage_subagents(Action="list")` in a tight loop every 2 seconds until state is `"idle"`
  - D) Subagents automatically overwrite the parent agent's terminal buffer without `send_message`
- **Correct**: A
- **Explanation**: Antigravity uses a reactive wakeup architecture: subagents run asynchronously and must call `send_message` with the caller's conversation ID to report findings. The parent agent never polls in a loop; it simply ends its turn (or does other work) and is automatically woken up when the message arrives.

---

## Module 05: MCP — Model Context Protocol (`05-mcp`)

### M05-Q1 (Variant A)
- **Question**: Where are MCP servers configured in Google Antigravity, and how are remote Streamable HTTP servers authenticated safely?
- **Options**:
  - A) In `~/.gemini/config/mcp_config.json` (or workspace `.agents/mcp_config.json`) using `"url"` and `"headers"` with `${ENV_VAR}` interpolation
  - B) In `.env.mcp` using plaintext API keys committed to git
  - C) Inside `GEMINI.md` using `@mcp(http://...)` markdown tags
  - D) Only local Stdio servers (`command` + `args`) are supported; remote HTTP servers are blocked
- **Correct**: A
- **Explanation**: Antigravity configures MCP servers in `mcp_config.json`, supporting both local Stdio (`command`, `args`, `env`) and remote Streamable HTTP (`url`, `headers`) with `${VAR}` environment variable interpolation so secrets stay out of config files.

### M05-Q2 (Variant B)
- **Question**: How do you grant fine-grained permission for a specific MCP tool and troubleshoot a failing MCP server connection in the Antigravity UI?
- **Options**:
  - A) Use `mcp(server_name/tool_name)` in permission rules, and click **Fix with Agent** in the MCP status panel when a server fails to initialize
  - B) Use `Bash(mcp:*)` permissions and restart the operating system
  - C) Set `allow_all_mcp: true` in `SKILL.md`
  - D) Recompile the MCP server into a Python wheel
- **Correct**: A
- **Explanation**: Antigravity permissions address MCP tools via `mcp(server)` (all tools on that server) or `mcp(server/tool)` (a single tool), and the IDE includes a one-click **Fix with Agent** diagnostic action when an MCP server errors on startup.

---

## Module 06: Hooks (`06-hooks`)

### M06-Q1 (Variant A)
- **Question**: In `.agents/hooks.json`, a `PreToolUse` hook script wants to block a dangerous shell command or rewrite its arguments before execution. Which camelCase JSON fields does Antigravity's hook stdout contract expect?
- **Options**:
  - A) `decision` (`"allow"` or `"block"`), optional `reason`, and `overwrite` (to replace tool arguments)
  - B) `exit_status: 2` and `new_input_args`
  - C) `status: "rejected"` and `patch_input`
  - D) `allowTool: false` and `mutatedParams`
- **Correct**: A
- **Explanation**: Antigravity hooks communicate via a structured camelCase JSON contract on stdout: `decision` (`"allow"` | `"block"`), `reason` (explanation shown to the agent/user), and `overwrite` (modified tool parameters for `PreToolUse`).

### M06-Q2 (Variant B)
- **Question**: Which hook lifecycle event fires when the agent finishes its turn, and what fields let a hook inject follow-up verification steps only when the agent and all background tasks are completely idle?
- **Options**:
  - A) The `Stop` event, checking `fullyIdle` in the input payload and returning `injectSteps` in the JSON output
  - B) The `SessionStart` event, returning `autoContinue: true`
  - C) The `PostToolUse` event, returning `rerunLastTool: true`
  - D) The `PreInvocation` event, returning `loopForever: true`
- **Correct**: A
- **Explanation**: Antigravity supports 6 core hook events (`SessionStart`, `PreInvocation`, `PreToolUse`, `PostToolUse`, `PostInvocation`, `Stop`). In a `Stop` hook, inspecting `fullyIdle: true` ensures no subagents or background tasks are still running, and returning `injectSteps` queues automated verification prompts.

---

## Module 07: Plugins (`07-plugins`)

### M07-Q1 (Variant A)
- **Question**: Where must `hooks.json` and `mcp_config.json` be placed inside an Antigravity plugin bundle so they register automatically when the plugin is enabled?
- **Options**:
  - A) At the plugin's root directory alongside `plugin.json` (plus subdirectories `skills/`, `agents/`, and `rules/`)
  - B) Hidden inside `.claude-plugin/nested/config/`
  - C) Inside `node_modules/@gemini/plugin-runtime/`
  - D) Embedded as base64 strings inside `GEMINI.md`
- **Correct**: A
- **Explanation**: An Antigravity plugin directory contains `plugin.json` (manifest), optional root-level `hooks.json` and `mcp_config.json`, and component directories (`skills/`, `agents/`, `rules/`).

### M07-Q2 (Variant B)
- **Question**: When a plugin named `sec-ops` provides a skill named `audit`, how is that skill namespaced and how do you validate the plugin structure from the CLI?
- **Options**:
  - A) It is namespaced as `sec-ops:audit`, and validated using `agy plugin validate <path>`
  - B) It overwrites all global skills named `audit` without a namespace, and is validated with `npm test`
  - C) It is invoked as `/plugin_sec_ops_audit`, and cannot be validated from the CLI
  - D) It requires manual copying into `.agents/rules/` before use
- **Correct**: A
- **Explanation**: Antigravity namespaces plugin customizations as `<plugin-name>:<component-name>` (e.g., `sec-ops:audit`) so enabling or disabling a plugin via `/plugin` or `agy plugin` is atomic and collision-free. `agy plugin validate` verifies the manifest and directory layout.

---

## Module 08: Checkpoints, Generative UI & Sidecars (`08-checkpoints`)

### M08-Q1 (Variant A)
- **Question**: You want to explore an alternative refactoring approach from an earlier turn without losing your current conversation state or code changes. Which command should you use vs. rolling back destructively?
- **Options**:
  - A) Use `/fork` (or `/branch`) to spin off an independent branch from that turn, whereas `/rewind` (or `/undo`) rolls the current session back to an earlier checkpoint
  - B) Use `/clear` to save a branch, and `/exit` to undo file edits
  - C) Use `git reset --hard HEAD~5` inside a `PostToolUse` hook
  - D) Antigravity only supports conversation rewind; file changes cannot be checkpointed
- **Correct**: A
- **Explanation**: `/rewind` (alias `/undo`) restores conversation and/or workspace files to a prior checkpoint, while `/fork` (alias `/branch`) clones the session state so you can test an alternative direction safely in parallel. Users can also leave inline comments directly on an Implementation Plan artifact before clicking **Proceed**.

### M08-Q2 (Variant B)
- **Question**: How do Generative UI widgets (`<agent-embed>`) and interactive Sidecar viewers (`sidecar.json`) differ in Google Antigravity?
- **Options**:
  - A) `<agent-embed>` renders self-contained HTML/JS widgets inline in chat (using `tailwindcss.min.js` and theme CSS tokens), while Sidecars (`sidecar.json`) run persistent interactive panels opened via `sidecar://` pill links
  - B) `<agent-embed>` is only for terminal ASCII art, while `sidecar.json` is used for cron scheduling
  - C) Both require deploying an external Next.js server to Cloud Run before rendering
  - D) Sidecars can only display static PNG screenshots
- **Correct**: A
- **Explanation**: Generative UI embeds rich, interactive HTML/SVG/Canvas widgets directly in the chat stream or artifacts using `<agent-embed>` and local `tailwindcss.min.js`, whereas Sidecars (`sidecar.json`) provide dedicated, persistent companion panels (such as the 3D Biomolecular Structure Viewer) linked via `sidecar://` pills.

### M08-Q3 (Variant C — Scheduling)
- **Question**: When scheduling a recurring background check with `/schedule` (or the `schedule` tool), how do you specify a timezone-aware cron schedule and ensure a standing daily report keeps running after your current task finishes?
- **Options**:
  - A) Prefix the 5-field cron expression with `CRON_TZ=<Timezone>` (if supported by the schedule config) and set `IsDaemon: true` for standing jobs that outlive the current task
  - B) Run `nohup sleep 86400 &` via `run_command`
  - C) Add a `PreToolUse` hook with `sleep(3600)`
  - D) Set `TimerCondition: "any"` on a 10-second one-shot timer
- **Correct**: A
- **Explanation**: The native `schedule` tool and `/schedule` command manage one-shot timers (`DurationSeconds` + `TimerCondition`) and 5-field recurring cron jobs (`CronExpression`, `MaxIterations`, `IsDaemon`). Never use background `sleep` commands for timers.

---

## Module 09: Advanced Features (`/boost`, `/teamwork-preview`, Models & Security) (`09-advanced-features`)

### M09-Q1 (Variant A)
- **Question**: What is the architectural difference between `/boost` and `/teamwork-preview` in Google Antigravity?
- **Options**:
  - A) `/boost` runs a structured 3-phase deep-reasoning pipeline (Decompose/Plan → Parallel DeepCoder/DeepInvestigator Execution → Rigorous Verification), while `/teamwork-preview` orchestrates a 2-phase multi-agent team with specialized adversarial roles (Sentinel, Critic, Challenger, Auditor)
  - B) `/boost` simply increases token output speed, while `/teamwork-preview` shares your screen on Google Meet
  - C) `/boost` only works on Gemini 3.8 Flash, while `/teamwork-preview` disables all subagents
  - D) They are identical aliases for `/compact`
- **Correct**: A
- **Explanation**: `/boost` activates multi-perspective strategic planning and verification (using specialist flows like DeepCoder and DeepInvestigator), whereas `/teamwork-preview` coordinates a collaborative/adversarial agent team (including Sentinel, Critic, Challenger, and Auditor roles) across two structured phases.

### M09-Q2 (Variant B)
- **Question**: In what precedence order does Antigravity evaluate tool permission rules, and what OS-level sandboxing mechanisms protect command execution?
- **Options**:
  - A) `Deny > Ask > Allow` precedence, backed by macOS Seatbelt (`sandbox-exec`) and Linux `nsjail` OS-level sandboxing
  - B) `Allow > Ask > Deny` precedence, backed only by regex filtering in JavaScript
  - C) Most-recently-added rule wins, with no OS-level process isolation
  - D) `Ask > Allow > Deny` precedence, requiring Docker Desktop for every command
- **Correct**: A
- **Explanation**: Security rules always evaluate in strict `Deny > Ask > Allow` order so an explicit `Deny` rule can never be overridden by a broad `Allow`. Command execution is further isolated at the OS kernel level using Seatbelt on macOS and `nsjail` on Linux.

### M09-Q3 (Variant C — Models & Remote Control)
- **Question**: When choosing between **Gemini 4 Argon** and **Gemini 3.8 Flash**, and continuing your local session from another device, which pairing is best?
- **Options**:
  - A) Use **Gemini 4 Argon** for deep architectural reasoning and complex multi-file refactors, **Gemini 3.8 Flash** for high-speed lookups/subagents, and `agy remote-control` to securely bridge your local session
  - B) Use **Gemini 3.8 Flash** exclusively for `/boost` architectural planning, and copy `.git` over FTP for remote access
  - C) Both models have identical latency and reasoning depth; `agy remote-control` only edits `mcp_config.json`
  - D) Models can only be switched by reinstalling the `agy` CLI binary
- **Correct**: A
- **Explanation**: Gemini 4 Argon is optimized for deep multi-step reasoning, architecture, and complex coding, while Gemini 3.8 Flash excels at low-latency exploration and lightweight subagent tasks. `agy remote-control` exposes a secure remote bridge to your running local session.

---

## Module 10: CLI & Python SDK (`10-cli`)

### M10-Q1 (Variant A)
- **Question**: You want to run Antigravity non-interactively in a GitHub Actions CI pipeline to audit a diff and return structured JSON without hanging on interactive prompts. Which CLI invocation should you use?
- **Options**:
  - A) `git diff | agy -p "Audit this diff for security issues" --mode auto --output-format json`
  - B) `agy --interactive --gui "Audit this diff"`
  - C) `agy plugin install ci-mode`
  - D) `python3 -m webbrowser https://antigravity.google.com`
- **Correct**: A
- **Explanation**: `agy -p` (print/headless mode) combined with `--mode auto` (or non-interactive permissions) and `--output-format json` lets you pipe stdin directly into Antigravity inside CI/CD scripts and parse the resulting JSON output. In interactive TUI/IDE sessions, shortcuts like `alt+m` (cycle mode) and `Ctrl+J`/`Ctrl+K` speed up navigation.

### M10-Q2 (Variant B)
- **Question**: In the `google-antigravity` Python SDK, which primitives are used to define multi-step orchestrated workflows and configure hybrid on-device/edge execution?
- **Options**:
  - A) `Agent`, `@beta.workflows.define` for declarative multi-agent workflows, and `LiteRTAgentConfig` for on-device LiteRT execution
  - B) `FlaskApp`, `@app.route`, and `SQLiteConfig`
  - C) `SubprocessRunner` and `RawSocketClient`
  - D) The Python SDK only supports generating static Markdown files and cannot invoke tools or workflows
- **Correct**: A
- **Explanation**: The `google-antigravity` Python SDK provides programmatic `Agent` instantiation, the `@beta.workflows.define` decorator for repeatable multi-step agentic workflows, and `LiteRTAgentConfig` for low-latency on-device/hybrid execution with Google LiteRT.

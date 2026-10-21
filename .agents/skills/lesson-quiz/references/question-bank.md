# Lesson Quiz — 50-Question Scenario Bank (Modules 01–10)

Contains **50 scenario-based multiple-choice questions** (5 per module across Modules `01` through `10`). Always randomize the order of options A–D before presenting each question via `ask_question`, and present the detailed explanations after the user finishes all 5 questions.

---

## Module 01: Slash Commands (`01-slash-commands`)

### Q1.1 — Interactive Design Alignment Before Coding
- **Question**: You have a rough product spec for a multi-tenant billing webhook, and you want the agent to interview you about edge cases, idempotency keys, and failure retries *before* it generates an implementation plan or writes code. Which built-in slash command is purpose-built for this?
- **Options**:
  - A) `/grill-me`
  - B) `/goal`
  - C) `/btw`
  - D) `/compact`
- **Correct**: A
- **Explanation**: `/grill-me` puts the agent into an interactive alignment interview mode where it systematically questions underspecified requirements and architectural trade-offs before execution. `/goal` is for autonomous multi-step completion, `/btw` asks a quick side question without polluting main task context, and `/compact` summarizes conversation history to free up tokens.

### Q1.2 — Persistent Long-Running Goal Execution
- **Question**: You are kicking off a comprehensive test-coverage migration across 40 modules and want the agent to keep iterating, fixing test failures, and verifying results without stopping prematurely after the first pass. Which slash command activates this behavior?
- **Options**:
  - A) `/goal`
  - B) `/btw`
  - C) `/learn`
  - D) `/theme`
- **Correct**: A
- **Explanation**: `/goal` instructs Antigravity to operate in an extra-thorough, goal-driven autonomous loop that persists through multi-step implementation and verification until the stated objective is genuinely satisfied.

### Q1.3 — Capturing Institutional Knowledge After a Debugging Session
- **Question**: After 20 minutes of debugging, you and the agent discover that your repository's legacy GraphQL client requires custom headers whenever `X-Tenant-ID` is present. You want the agent to codify this lesson into a reusable customization for future sessions. Which slash command should you use?
- **Options**:
  - A) `/learn`
  - B) `/rewind`
  - C) `/clear`
  - D) `/status`
- **Correct**: A
- **Explanation**: `/learn` distills a newly solved setup, debugging insight, or user correction from the current conversation into a persistent rule or skill so future sessions automatically follow the pattern.

### Q1.4 — Asking a Side Question Without Derailing the Active Plan
- **Question**: While the agent is mid-way through refactoring your authentication middleware, you want to ask a quick question about a PostgreSQL index syntax without derailing or bloating the active refactoring context. Which command should you run?
- **Options**:
  - A) `/btw <question>`
  - B) `/clear`
  - C) `/reset`
  - D) `/fork --destroy`
- **Correct**: A
- **Explanation**: `/btw` ("by the way") answers an ephemeral side question in a lightweight overlay without injecting the tangent into your primary conversation history or disrupting the ongoing task.

### Q1.5 — Authoring a Custom Team Slash Command
- **Question**: Your team wants a custom `/release-notes` slash command that anyone cloning the repository can invoke from the `/` menu, backed by a helper Python script and a Markdown template. Where should you define it in Google Antigravity?
- **Options**:
  - A) `.agents/skills/release-notes/SKILL.md` (with `name: release-notes` in YAML frontmatter, plus `scripts/` and `resources/`)
  - B) `.agents/hooks.json` under the `SlashCommand` key
  - C) `~/.gemini/config/mcp_config.json` under `customCommands`
  - D) `GEMINI.md` inside an HTML `<command name="release-notes">` tag
- **Correct**: A
- **Explanation**: In Google Antigravity, custom slash commands and skills are unified: any skill defined at `.agents/skills/<name>/SKILL.md` (workspace) or `~/.gemini/skills/<name>/SKILL.md` (global) is automatically exposed as `/<name>` in the slash menu while also supporting supporting files (`scripts/`, `references/`, `resources/`).

---

## Module 02: Memory & Rules (`02-memory`)

### Q2.1 — Cross-Agent Compatibility (`GEMINI.md` and `AGENTS.md`)
- **Question**: Your engineering organization uses Google Antigravity alongside other AI coding agents and wants shared repository conventions alongside Antigravity-specific modular rules. How does Antigravity handle `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md`?
- **Options**:
  - A) Antigravity natively loads both `GEMINI.md` and `AGENTS.md` as always-on workspace memory, alongside modular rules in `.agents/rules/*.md`
  - B) `AGENTS.md` causes a fatal startup error if `GEMINI.md` is also present
  - C) Only `~/.bashrc` is read for memory; Markdown files in the repo are ignored
  - D) `.agents/rules/*.md` completely deletes the contents of `GEMINI.md`
- **Correct**: A
- **Explanation**: Antigravity supports both `GEMINI.md` and the cross-tool `AGENTS.md` standard at the workspace root, combining them with global memory (`~/.gemini/GEMINI.md`) and modular `.agents/rules/*.md` files.

### Q2.2 — Choosing the Right Rule Trigger Mode
- **Question**: You are writing a rule file `.agents/rules/graphql-resolvers.md` that enforces strict dataloader batching, but it is only relevant when the agent is reading or editing files inside `src/graphql/**/*.ts`. Which YAML frontmatter configuration is most token-efficient?
- **Options**:
  - A) `trigger: glob` with `globs: ["src/graphql/**/*.ts"]`
  - B) `trigger: always_on`
  - C) `trigger: manual` with `alwaysLoad: true`
  - D) No frontmatter (which defaults to loading on every bash command)
- **Correct**: A
- **Explanation**: Antigravity rules support four trigger modes: `always_on` (loaded every turn), `model_decision` (loaded when the semantic router matches `description`), `glob` (loaded automatically when active files match `globs`), and `manual` (loaded only when explicitly mentioned via `@rule-name`). Using `trigger: glob` keeps GraphQL rules out of context when working on unrelated frontend or infra files.

### Q2.3 — Semantic Rule Activation (`model_decision`)
- **Question**: You create `.agents/rules/incident-postmortem.md` containing instructions for writing blameless root-cause analyses. Since postmortems can live in many folders and file formats, you want Antigravity to load this rule only when the user's request is semantically about incidents or postmortems. How should you configure its frontmatter?
- **Options**:
  - A) Set `trigger: model_decision` and provide a specific `description` explaining when the rule applies
  - B) Set `trigger: glob` with `globs: ["*"]`
  - C) Set `trigger: always_on` and paste 50 pages of past postmortems directly into `GEMINI.md`
  - D) Rename the file to `incident-postmortem.exe`
- **Correct**: A
- **Explanation**: With `trigger: model_decision`, Antigravity evaluates the rule's `description` against the task context and only injects the full rule body when relevant, saving valuable tokens on normal coding turns.

### Q2.4 — Respecting the 24 KB / 20,000-Token Budget & `@[label](path)` Links
- **Question**: Your team's `GEMINI.md` has grown to 85 KB because engineers pasted full API schemas and architecture runbooks directly into it, exceeding Antigravity's ~24 KB (~20,000-token) `always_on` budget. What is the recommended way to refactor this?
- **Options**:
  - A) Keep `GEMINI.md` concise (<24 KB) with core invariants, move specialized guides into `.agents/rules/*.md` (`model_decision` or `glob`), and link reference docs using `@[API Schema](docs/api-schema.md)`
  - B) Compress `GEMINI.md` into `GEMINI.md.gz` so the model reads raw binary gzip bytes
  - C) Duplicate the 85 KB file into every subdirectory
  - D) Split the file into 10 `trigger: always_on` files so all 85 KB still load on every turn
- **Correct**: A
- **Explanation**: The ~24 KB (~20,000-token) budget applies to `always_on` instructions so that the model retains ample context for code, tool outputs, and reasoning. Offloading domain-specific guidelines to `model_decision`/`glob` rules and using `@[label](path)` links keeps startup context lean.

### Q2.5 — Toggling Workspace Rules with `.agents/rules.json`
- **Question**: A team repository contains 12 rule files in `.agents/rules/`, and you want a declarative registry file to enable, disable, or set priority/state for those rules without deleting the Markdown files. Which file controls this?
- **Options**:
  - A) `.agents/rules.json`
  - B) `.agents/hooks.json`
  - C) `tsconfig.json`
  - D) `~/.gemini/credentials.json`
- **Correct**: A
- **Explanation**: `.agents/rules.json` provides workspace-level state and configuration management for rules in `.agents/rules/`, allowing rules to be toggled cleanly without removing files from git.

---

## Module 03: Skills (`03-skills`)

### Q3.1 — Three-Stage Progressive Disclosure Architecture
- **Question**: You install 25 specialized skills in `.agents/skills/`. Why doesn't having 25 installed skills exhaust your context window before you even ask your first question?
- **Options**:
  - A) Because Stage 1 only loads each skill's compact YAML frontmatter (`name` and `description`); Stage 2 reads `SKILL.md` only when a skill is activated; Stage 3 reads `references/`, `scripts/`, or `resources/` on demand
  - B) Because Antigravity deletes 24 of the 25 skills at random on startup
  - C) Because skills are stored on an external FTP server and cannot be read locally
  - D) Because `SKILL.md` files are limited to 10 characters total
- **Correct**: A
- **Explanation**: Antigravity's 3-stage progressive disclosure architecture ensures that installing dozens of skills has near-zero idle token overhead: Stage 1 exposes only `name` + `description` in the skill index, Stage 2 loads the full `SKILL.md` instructions when relevant, and Stage 3 loads deep reference documents or executes scripts only as needed.

### Q3.2 — Writing High-Signal Skill Descriptions
- **Question**: Your custom `.agents/skills/db-migration-auditor/SKILL.md` never activates automatically when developers ask *"Check if this Alembic migration will lock the `users` table in production"*, even though it works when invoked manually via `/db-migration-auditor`. What is the most likely cause?
- **Options**:
  - A) The YAML frontmatter `description` is too vague (e.g., `"Database helper"`) instead of stating both what the skill does and explicit trigger phrases/scenarios (Alembic, SQL migrations, table locks, schema changes)
  - B) The skill folder is missing a `Makefile`
  - C) Skills in `.agents/skills/` can never be triggered automatically by the model
  - D) The file extension must be `.skill` instead of `SKILL.md`
- **Correct**: A
- **Explanation**: During Stage 1 discovery, the agent only sees `name` and `description`. A well-crafted `description` must clearly state *what* the skill does and *when* to activate it (including domain keywords like "Alembic", "SQL migration", "table lock", and "When NOT to use").

### Q3.3 — Organizing Bundled Scripts and Reference Material
- **Question**: You are building a `openapi-validator` skill that needs a 1,200-line OAS 3.1 style guide, a deterministic Python linter (`validate_spec.py`), and a starter YAML template. How should you structure `.agents/skills/openapi-validator/`?
- **Options**:
  - A) Keep `SKILL.md` focused on the workflow steps, put `validate_spec.py` in `scripts/`, the 1,200-line guide in `references/`, and the starter template in `resources/` (or `examples/`)
  - B) Paste all 1,200 lines of the style guide and the entire Python script inside the YAML frontmatter `description` field
  - C) Put `validate_spec.py` in `/usr/bin` and hardcode `/Users/alice/Desktop` paths in `SKILL.md`
  - D) Create 15 separate `SKILL.md` files inside the same folder
- **Correct**: A
- **Explanation**: Separating workflow orchestration (`SKILL.md`) from heavy documentation (`references/`), executable helpers (`scripts/`), and templates (`resources/` or `examples/`) takes full advantage of Stage 3 progressive disclosure.

### Q3.4 — Managing Installed Skills via `.agents/skills.json`
- **Question**: Your monorepo contains skills for iOS, Android, and Web teams under `.agents/skills/`. How are workspace skill states and metadata tracked and toggled declaratively?
- **Options**:
  - A) Via `.agents/skills.json`
  - B) Via `.gitmodules`
  - C) Via `~/.ssh/config`
  - D) Via `GEMINI.lock`
- **Correct**: A
- **Explanation**: `.agents/skills.json` tracks skill enablement and configuration at the workspace level so teams can manage active skills cleanly.

### Q3.5 — Skill Precedence Across Discovery Roots
- **Question**: If both a personal global skill (`~/.gemini/skills/pr-check/SKILL.md`) and a workspace skill (`.agents/skills/pr-check/SKILL.md`) exist with the name `pr-check`, how does Antigravity resolve them?
- **Options**:
  - A) Workspace customizations (`.agents/skills/`) take priority over user-global (`~/.gemini/skills/`) customizations for that repository so team standards are respected
  - B) Both skills are deleted automatically due to a collision
  - C) Global skills always overwrite workspace skills and delete `.agents/`
  - D) Neither skill can be used unless renamed with a random UUID
- **Correct**: A
- **Explanation**: Antigravity's customization hierarchy prioritizes workspace-level definitions (`.agents/skills/`) over user-global definitions (`~/.gemini/skills/`), ensuring project-specific workflows override personal defaults when working inside a team repo.

---

## Module 04: Subagents (`04-subagents`)

### Q4.1 — Built-In Subagents (`research`, `browser`, `self`)
- **Question**: You need to investigate how 15 different microservices in your monorepo handle JWT token revocation without filling your main agent's context window with 60 file reads. Which built-in subagent should you invoke via `invoke_subagent`?
- **Options**:
  - A) `research` (read-only exploration subagent with isolated context)
  - B) `firestore-rules-author`
  - C) `image-generator`
  - D) No subagent; read all 60 files sequentially in the main conversation
- **Correct**: A
- **Explanation**: The built-in `research` subagent is equipped with read-only codebase and web research tools in its own isolated context window, returning a concise synthesis back to the parent agent. (`self` inherits full parent capabilities including write tools, and `browser` handles interactive browser tasks.)

### Q4.2 — Choosing `Workspace: inherit | branch | share`
- **Question**: You want to launch two `self` subagents concurrently to prototype two different database caching layers (Redis vs. in-memory LRU) and run their test suites without the two subagents overwriting each other's files or duplicating a 4 GB `.git` folder. Which `Workspace` parameter on `invoke_subagent` should you choose?
- **Options**:
  - A) `Workspace: "share"` (creates an isolated working tree that shares the underlying repository storage, similar to a git worktree)
  - B) `Workspace: "inherit"` (both subagents edit the exact same files simultaneously in the parent workspace)
  - C) `Workspace: "none"`
  - D) `Workspace: "production"`
- **Correct**: A
- **Explanation**: `Workspace: "inherit"` shares the parent's working directory directly (great for read-only tasks or disjoint file edits), `Workspace: "branch"` creates a full isolated clone/branch, and `Workspace: "share"` creates a separate workspace directory sharing the parent's underlying repository storage so parallel subagents can edit and test independently without storage bloat.

### Q4.3 — Reactive Wakeup & Subagent Communication (`send_message`)
- **Question**: You are authoring a custom subagent in `.agents/agents/security-auditor.md` (or defining one dynamically with `define_subagent`). How must the subagent deliver its final audit report back to the parent agent, and how does the parent wait for it?
- **Options**:
  - A) The subagent MUST call `send_message(Recipient="<parent-conversation-id>", Message="...")`; the parent agent stops calling tools (or does other work) and is automatically woken up when the message arrives
  - B) The subagent just prints plain text and exits; the parent runs `sleep 60` in a loop to poll the subagent
  - C) The subagent writes its report to `/dev/null`
  - D) The parent must call `manage_subagents(Action="list")` 100 times per second until the subagent finishes
- **Correct**: A
- **Explanation**: In Antigravity, text generated by a subagent outside of `send_message` is not automatically relayed to the caller. Subagents must call `send_message` with the parent's conversation ID, and the parent relies on Antigravity's reactive wakeup system rather than polling.

### Q4.4 — Custom Subagent Definition in `.agents/agents/<name>.md`
- **Question**: When defining a reusable workspace subagent in `.agents/agents/migration-specialist.md` (or via `define_subagent`), which capability flags control whether the subagent can modify files, call MCP servers, or spawn its own child subagents?
- **Options**:
  - A) `enable_write_tools`, `enable_mcp_tools`, and `enable_subagent_tools` (alongside `name`, `description`, and the system prompt)
  - B) `sudo: true`, `network: host`, and `privileged: true`
  - C) `chmod: 777` in `package.json`
  - D) Subagents can never use write tools or MCP tools under any configuration
- **Correct**: A
- **Explanation**: Subagents have read-only codebase tools and `send_message` by default. Enabling `enable_write_tools`, `enable_mcp_tools`, or `enable_subagent_tools` grants file editing/command execution, MCP tool access, or hierarchical subagent spawning respectively.

### Q4.5 — Reusing an Existing Subagent vs. Spawning a New One
- **Question**: A `research` subagent (`conversationId: "8f3a..."`) just sent you a summary of the authentication module, and you now have a follow-up question about a specific function it inspected. What is the best practice?
- **Options**:
  - A) Call `send_message(Recipient="8f3a...", Message="...")` to continue with the existing subagent that already has those files in its context window
  - B) Call `manage_subagents(Action="kill_all")` and spawn 5 new subagents from scratch
  - C) Re-read all the authentication files in the parent agent's context
  - D) Restart the Antigravity IDE
- **Correct**: A
- **Explanation**: Sending a follow-up message via `send_message` to an idle subagent reuses its warm context window and avoids redundant file reads and token cost.

---

## Module 05: MCP — Model Context Protocol (`05-mcp`)

### Q5.1 — Configuring Stdio vs. Streamable HTTP MCP Servers
- **Question**: You are configuring two MCP servers in `~/.gemini/config/mcp_config.json`: a local PostgreSQL server launched via `npx` and a remote Sentry MCP server hosted over HTTPS. Which configuration structure is valid?
- **Options**:
  - A) Use `"command"` + `"args"` + `"env"` for the local Stdio server, and `"url"` + `"headers"` (with `"Authorization": "Bearer ${SENTRY_TOKEN}"`) for the remote Streamable HTTP server inside `"mcpServers"`
  - B) Use `"socketPath"` for both and hardcode plaintext tokens in `GEMINI.md`
  - C) Put both servers inside `.agents/hooks.json` under `"PreToolUse"`
  - D) Antigravity only supports XML-RPC over port 21
- **Correct**: A
- **Explanation**: `mcp_config.json` defines servers under `"mcpServers"`. Local Stdio servers specify `"command"`, `"args"`, and `"env"`, while remote Streamable HTTP servers specify `"url"` and `"headers"` with `${ENV_VAR}` environment variable expansion.

### Q5.2 — Granular MCP Permissions (`mcp(server/tool)`)
- **Question**: Your team connected a GitHub MCP server named `github` that exposes both read tools (`get_pull_request`, `list_issues`) and destructive write tools (`merge_pull_request`, `delete_branch`). How do you allow read tools automatically while requiring confirmation before merging a PR?
- **Options**:
  - A) Add `mcp(github/get_pull_request)` and `mcp(github/list_issues)` to the `Allow` list, and `mcp(github/merge_pull_request)` to the `Ask` list (or `mcp(github/delete_branch)` to `Deny`)
  - B) Set `mcp(*)` to `Allow` and hope the model never calls `delete_branch`
  - C) Disconnect the network cable whenever a PR is open
  - D) Rename `mcp_config.json` to `mcp_readonly.txt`
- **Correct**: A
- **Explanation**: Antigravity's permission syntax supports both server-wide rules (`mcp(github)`) and per-tool rules (`mcp(github/merge_pull_request)`), evaluated under strict `Deny > Ask > Allow` precedence.

### Q5.3 — Diagnosing Broken MCP Servers with **Fix with Agent**
- **Question**: You add a new local Python MCP server to `~/.gemini/config/mcp_config.json`, but it fails to start because `uvx` is missing a required flag or environment variable. What is the fastest way to diagnose and repair it in the Antigravity IDE?
- **Options**:
  - A) Click the **Fix with Agent** button next to the errored server in the MCP panel so the agent inspects the stderr logs and proposes the config fix
  - B) Reformat your hard drive and reinstall macOS
  - C) Write a 500-line C++ wrapper around `stdio`
  - D) Disable all skills in `.agents/skills.json`
- **Correct**: A
- **Explanation**: When an MCP server fails initialization or handshake, Antigravity surfaces the error log and a **Fix with Agent** button that hands the diagnostic context directly to the agent to fix `mcp_config.json` or missing dependencies.

### Q5.4 — Securing Credentials for MCP Servers
- **Question**: A teammate submits a PR that adds `.agents/mcp_config.json` containing `"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_RealSecretToken123"`. How should this be remediated?
- **Options**:
  - A) Revoke the leaked token immediately, replace the literal value in `mcp_config.json` with `"${GITHUB_PERSONAL_ACCESS_TOKEN}"`, and store the secret in the local environment or OS keychain via the `credentials` workflow
  - B) Base64-encode the token inside `mcp_config.json` and merge the PR
  - C) Move the plaintext token into `GEMINI.md` instead
  - D) Add a comment asking coworkers not to look at line 12
- **Correct**: A
- **Explanation**: Never commit literal secrets to `mcp_config.json` or markdown files. Use `${VAR}` interpolation in `mcp_config.json` and manage sensitive keys in local environment variables or untracked credential stores.

### Q5.5 — Combining MCP with Subagents
- **Question**: You want a custom `db-analyst` subagent in `.agents/agents/db-analyst.md` to query your read-only BigQuery MCP server. What must be enabled in the subagent's configuration?
- **Options**:
  - A) `enable_mcp_tools: true` in the subagent's definition (and appropriate `mcp(bigquery/*)` permissions)
  - B) `enable_subagent_tools: true` only
  - C) `trigger: glob`
  - D) Nothing; subagents can never call MCP tools
- **Correct**: A
- **Explanation**: By default, custom subagents only have local read-only codebase tools and `send_message`. Setting `enable_mcp_tools: true` equips the subagent to call configured MCP servers.

---

## Module 06: Hooks (`06-hooks`)

### Q6.1 — The 6 Hook Lifecycle Events
- **Question**: Which set of 6 lifecycle events is supported in Antigravity's `.agents/hooks.json`?
- **Options**:
  - A) `SessionStart`, `PreInvocation`, `PreToolUse`, `PostToolUse`, `PostInvocation`, and `Stop`
  - B) `onMount`, `onUpdate`, `onUnmount`, `onError`, `onClick`, and `onSubmit`
  - C) `gitPreCommit`, `gitPostCommit`, `gitPush`, `dockerBuild`, `npmInstall`, and `exit`
  - D) `BeforePrompt`, `AfterPrompt`, `BeforeModel`, `AfterModel` only
- **Correct**: A
- **Explanation**: Antigravity's hook engine in `.agents/hooks.json` (and `~/.gemini/config/hooks.json` or plugin `hooks.json`) provides 6 deterministic lifecycle hooks spanning session startup (`SessionStart`), model/turn boundaries (`PreInvocation`, `PostInvocation`, `Stop`), and individual tool executions (`PreToolUse`, `PostToolUse`).

### Q6.2 — Blocking or Rewriting Tool Calls in `PreToolUse`
- **Question**: You write a `PreToolUse` hook matching `run_command` to ensure every `pytest` invocation automatically runs with `-q --tb=short` and that any command containing `rm -rf /` is rejected. What JSON payload should your script output to `stdout` in each case?
- **Options**:
  - A) Return `{"decision": "block", "reason": "Destructive rm -rf / blocked"}` to block, or `{"decision": "allow", "overwrite": {"CommandLine": "pytest -q --tb=short"}}` to rewrite the tool arguments
  - B) Return `{"status": 403}` or `{"status": 200, "args": "..."}`
  - C) Print `BLOCK` to `stderr` and delete `.agents/hooks.json`
  - D) Modify the parent process memory using `gdb`
- **Correct**: A
- **Explanation**: Antigravity uses a clean camelCase JSON stdout contract for `PreToolUse` hooks: `"decision": "block"` (with `"reason"`) halts execution and informs the agent, while `"decision": "allow"` with `"overwrite"` transparently replaces the tool input parameters before the tool runs.

### Q6.3 — Automated Verification with `Stop`, `fullyIdle`, and `injectSteps`
- **Question**: You want a `Stop` hook to automatically ask the agent to run `npm test` before finishing, **but only** when all background tasks and subagents have finished running (so it doesn't interrupt an async wakeup wait). How should your `Stop` hook script behave?
- **Options**:
  - A) Check that the stdin JSON payload has `"fullyIdle": true` (and that tests haven't already passed), then output `{"injectSteps": ["Run npm test and fix any failures before completing."]}`
  - B) Always output `{"injectSteps": ["Run npm test"]}` unconditionally on every `PreToolUse` event, causing an infinite loop
  - C) Spawn a background `sleep 300` process inside `SessionStart`
  - D) Use `"overwrite": {"Stop": false}`
- **Correct**: A
- **Explanation**: When the agent stops calling tools because it is waiting for a background command or subagent, `fullyIdle` is `false`. Checking `fullyIdle: true` in the `Stop` hook payload ensures your hook only injects follow-up verification prompts via `injectSteps` when all async work has settled.

### Q6.4 — Post-Edit Auto-Formatting with `PostToolUse`
- **Question**: You want `ruff format` and `ruff check --fix` to run automatically every time the agent modifies a `.py` file via `replace_file_content` or `write_to_file`. Which hook event and matcher should you configure in `.agents/hooks.json`?
- **Options**:
  - A) Event `PostToolUse` with a matcher targeting `replace_file_content|write_to_file`, inspecting `toolInput.TargetFile` in the stdin JSON and formatting if it ends in `.py`
  - B) Event `SessionStart` with matcher `*`
  - C) Event `PreInvocation` before any file has been edited
  - D) Event `Stop` with `decision: "block"`
- **Correct**: A
- **Explanation**: `PostToolUse` runs immediately after a matched tool completes and receives both `toolInput` (including `TargetFile`) and `toolOutput` on `stdin`, making it ideal for deterministic auto-formatting, linting, or audit logging.

### Q6.5 — Preventing Infinite Loops in `Stop` Hooks
- **Question**: If a `Stop` hook returns `{"injectSteps": ["Verify all lint checks pass"]}` every time `Stop` fires without checking whether verification was already injected in this session/turn cycle, what will happen?
- **Options**:
  - A) The agent will enter an infinite verification loop because each injected step ends with another `Stop` event
  - B) `injectSteps` is ignored after the first character
  - C) Antigravity automatically deletes `.agents/hooks.json`
  - D) The `Stop` event only fires once per calendar year
- **Correct**: A
- **Explanation**: Because `injectSteps` resumes the agent for another turn (which eventually triggers `Stop` again), a well-written `Stop` hook must check state (such as a session marker, clean git/test status, or invocation counter) and return `{}` once the verification condition is satisfied.

---

## Module 07: Plugins (`07-plugins`)

### Q7.1 — Anatomy of an Antigravity Plugin Bundle
- **Question**: You are packaging your team's security skills, custom subagents, rules, pre-tool hooks, and an internal vulnerability MCP server into a single distributable plugin named `corp-sec`. What is the standard directory layout?
- **Options**:
  - A) A root `plugin.json` manifest alongside optional root-level `hooks.json` and `mcp_config.json`, plus `skills/`, `agents/`, and `rules/` subdirectories
  - B) A single monolithic `.zip.exe` binary with no JSON files
  - C) Placing everything inside `.git/hooks/plugin/`
  - D) Putting `plugin.json` inside `~/.bashrc`
- **Correct**: A
- **Explanation**: Antigravity plugins follow a clean, self-contained layout: `plugin.json` at the plugin root defines metadata (`name`, `version`, `description`), `hooks.json` and `mcp_config.json` live at the plugin root, and customizations live in `skills/`, `agents/`, and `rules/`.

### Q7.2 — Namespacing & Collision Prevention
- **Question**: Your workspace defines `.agents/skills/deploy/SKILL.md`, and you also install a plugin named `cloud-run` that includes `skills/deploy/SKILL.md`. How does Antigravity prevent a naming conflict?
- **Options**:
  - A) The plugin's skill is namespaced as `cloud-run:deploy` (invocable as `/cloud-run:deploy`), while your workspace skill remains `deploy` (`/deploy`)
  - B) Installing the plugin deletes `.agents/skills/deploy/SKILL.md`
  - C) Antigravity refuses to start until you uninstall one of them
  - D) Both skills merge into a single corrupted Markdown file
- **Correct**: A
- **Explanation**: All components inside a plugin are automatically namespaced with `<plugin-name>:<item-name>` (e.g., `cloud-run:deploy`), preventing collisions with workspace or personal skills and allowing atomic enable/disable.

### Q7.3 — Validating and Installing Plugins via `agy plugin` and `/plugin`
- **Question**: Before publishing your `corp-sec` plugin to your organization's git repository, how should you validate its manifest and component structure from the command line, and how can teammates manage it interactively?
- **Options**:
  - A) Run `agy plugin validate ./corp-sec` (and `agy plugin install <source>`), or use `/plugin` interactively in the chat UI
  - B) Run `gcc -Wall plugin.json`
  - C) Run `agy --destroy-cache`
  - D) Plugins cannot be validated or installed without recompiling the IDE
- **Correct**: A
- **Explanation**: The `agy plugin validate <path>` CLI command checks `plugin.json`, `hooks.json`, `mcp_config.json`, and all skill/agent/rule frontmatter for schema errors, while `agy plugin install` and `/plugin` handle installation and toggling.

### Q7.4 — When to Package as a Plugin vs. Standalone `.agents/` Files
- **Question**: Which scenario is the strongest candidate for creating a **Plugin** (`07-plugins`) rather than loose files in `.agents/`?
- **Options**:
  - A) You want to distribute a cohesive bundle of skills, subagents, hooks, and MCP servers across 30 microservice repositories and toggle the entire suite on or off as a single unit
  - B) You want to document the build command (`npm run build`) for a single personal side project
  - C) You want to rewind a single mistaken file edit in the current chat
  - D) You want to ask a one-off question with `/btw`
- **Correct**: A
- **Explanation**: Repo-specific build commands belong in `GEMINI.md` or `.agents/rules/`, whereas multi-component toolkits shared across repositories or teams belong in a versioned plugin bundle.

### Q7.5 — Referencing Files Within a Plugin
- **Question**: Inside a plugin skill (`skills/audit/SKILL.md`) or `hooks.json`, how should scripts and reference files be referenced so the plugin works on any developer's machine?
- **Options**:
  - A) Use paths relative to the skill or plugin root (never hardcode `/Users/<username>/...` absolute paths in committed plugin files)
  - B) Hardcode `/Users/admin/Desktop/my-plugin/scripts/run.sh`
  - C) Host all shell scripts on Pastebin and `curl | bash` them on every turn
  - D) Store scripts in `/tmp` and expect them to persist across reboots
- **Correct**: A
- **Explanation**: Portable plugins always reference bundled scripts, templates, and references relative to the plugin/skill root so they work across macOS, Linux, and CI containers.

---

## Module 08: Checkpoints, Generative UI & Sidecars (`08-checkpoints`)

### Q8.1 — Rewinding (`/rewind`) vs. Forking (`/fork`) a Session
- **Question**: The agent just finished implementing a GraphQL subscription layer at Turn 12. You want to keep this working GraphQL implementation intact in its own session while spinning off a parallel conversation from Turn 8 to test a WebSocket/gRPC alternative. Which command should you run?
- **Options**:
  - A) `/fork` (or `/branch`) from Turn 8 to create an independent branch while preserving the original trajectory
  - B) `/rewind` (or `/undo`) to Turn 8 and choose "Restore code and conversation", which rolls back the current session
  - C) `/clear`
  - D) `/exit`
- **Correct**: A
- **Explanation**: `/rewind` (alias `/undo`) rolls the current session back to an earlier checkpoint, whereas `/fork` (alias `/branch`) clones the conversation at the selected point so you can explore an alternative path without discarding your current work.

### Q8.2 — Inline Comments on Implementation Plan Artifacts
- **Question**: The agent presents an `implementation_plan.md` artifact in the Antigravity viewer with a **Proceed** button, proposing changes across 6 files. You agree with 5 of the files, but want the agent to use `zod` instead of `joi` in `src/validators/user.ts`. What is the most ergonomic workflow?
- **Options**:
  - A) Highlight the `src/validators/user.ts` section directly in the Implementation Plan artifact, add an inline review comment (*"Use zod instead of joi here"*), and submit feedback so the agent revises the plan before execution
  - B) Reject the entire session with `/clear` and retype your prompt from scratch
  - C) Manually edit the agent's internal `.jsonl` transcript file
  - D) Unplug your network connection before clicking Proceed
- **Correct**: A
- **Explanation**: Antigravity's artifact viewer supports Google Docs-style inline comments on `implementation_plan.md` artifacts (`RequestFeedback: true`), letting you critique specific lines or sections before approving execution.

### Q8.3 — Authoring Self-Contained Generative UI Widgets (`<agent-embed>`)
- **Question**: You want to render an interactive latency comparison chart and filterable table inline in the chat using Antigravity's Generative UI skill. Which technical practices are required for `<agent-embed>` widgets?
- **Options**:
  - A) Emit a self-contained `<agent-embed>` block loading local `/tailwind/tailwindcss.min.js`, using semantic theme CSS variables (so dark/light mode works automatically), and avoiding external CDN dependencies that could fail offline
  - B) Emit a bare `<script src="http://untrusted-cdn.example.com/chart.js">` tag outside of `<agent-embed>`
  - C) Write a Java Applets `.class` file
  - D) Hardcode `#000000` text on `#000000` backgrounds without CSS variables
- **Correct**: A
- **Explanation**: Antigravity's `<agent-embed>` Generative UI runtime provides local `/tailwind/tailwindcss.min.js` and theme-adaptive CSS custom properties, enabling rich, interactive HTML/SVG/Canvas widgets directly in chat.

### Q8.4 — Interactive Science & Custom Sidecars (`sidecar.json` & `sidecar://` Links)
- **Question**: You load a 3D protein structure (`1tup.cif`) into the Biomolecular Structure Viewer sidecar via its MCP tools. According to Antigravity's sidecar rules, what **must** you include in your chat response to the user?
- **Options**:
  - A) Always surface the viewer's exact `sidecar://` pill link in the chat response so the user can open or toggle the interactive sidecar panel with one click
  - B) Only describe the protein in ASCII text and never mention the sidecar
  - C) Dump the entire raw 50,000-line `.cif` coordinate file into the chat response
  - D) Tell the user to install PyMOL manually instead of using the interactive sidecar
- **Correct**: A
- **Explanation**: Sidecars (`sidecar.json`) provide rich, interactive companion panels (like the Mol* 3D Biomolecular Structure Viewer). Whenever an agent loads or updates a visualization in a sidecar, it must include the exact `sidecar://` pill link in the chat response for one-click user access.

### Q8.5 — Scheduling Timers and Cron Jobs (`/schedule` & `schedule` Tool)
- **Question**: You spawned 4 long-running research subagents and want to set a 5-minute safety check-in timer that automatically cancels itself as soon as *any* of the subagents sends you a message. How should you call the `schedule` tool?
- **Options**:
  - A) `schedule(DurationSeconds=300, Prompt="Check in on subagents", TimerCondition="any")`
  - B) `run_command(CommandLine="sleep 300 && echo wakeup")`
  - C) `schedule(CronExpression="* * * * *", IsDaemon=true)`
  - D) `schedule(DurationSeconds=300, TimerCondition="never")`
- **Correct**: A
- **Explanation**: Setting `DurationSeconds=300` with `TimerCondition="any"` creates a liveness timer that automatically cancels early if any message arrives from a subagent or background task before 300 seconds elapse. Never use `sleep` in `run_command` for timers.

---

## Module 09: Advanced Features (`09-advanced-features`)

### Q9.1 — `/boost` 3-Phase Deep Reasoning Architecture
- **Question**: You invoke `/boost` to solve a complex distributed race condition across your payment service and message queue. What happens inside Antigravity's `/boost` execution pipeline?
- **Options**:
  - A) It executes a structured 3-phase workflow: (1) Strategic Decomposition & Multi-Perspective Planning, (2) Parallel Specialist Execution (DeepCoder / DeepInvestigator subagents in isolated workspaces), and (3) Rigorous Verification & Synthesis
  - B) It simply sets `temperature: 2.0` on a single prompt with no subagents or verification
  - C) It skips all tests and commits directly to `main`
  - D) It switches your model to a 1-billion-parameter offline model
- **Correct**: A
- **Explanation**: `/boost` is designed for high-complexity coding and research tasks, combining deep strategic decomposition, parallel specialist subagents (DeepCoder, DeepInvestigator), and strict end-to-end verification before presenting the final solution.

### Q9.2 — `/teamwork-preview` Multi-Agent Adversarial Roles
- **Question**: How does `/teamwork-preview` structure its multi-agent collaboration differently from a single-agent turn?
- **Options**:
  - A) It runs a 2-phase collaborative/adversarial protocol where specialized agents — **Sentinel** (security/invariants), **Critic** (code quality/design flaws), **Challenger** (edge cases/failure modes), and **Auditor** (verification/compliance) — review and stress-test the implementation
  - B) It creates 4 identical copies of the same prompt and picks the shortest response
  - C) It emails your coworkers on Gmail and waits 3 days for a human reply
  - D) It only runs on markdown files in `vi/`
- **Correct**: A
- **Explanation**: `/teamwork-preview` orchestrates an autonomous team of distinct specialist personas (Sentinel, Critic, Challenger, Auditor) across 2 phases to uncover architectural blind spots, security bugs, and edge cases before finalizing code changes.

### Q9.3 — Model Selection: Gemini 4 Argon vs. Gemini 3.8 Flash
- **Question**: You are configuring a multi-agent workflow where the lead architect agent designs a cross-service database sharding plan while 6 helper agents scan 200 log files for error patterns. How should you pair **Gemini 4 Argon** and **Gemini 3.8 Flash**?
- **Options**:
  - A) Use **Gemini 4 Argon** for the lead architect agent (deep multi-step reasoning and complex synthesis) and **Gemini 3.8 Flash** for the high-throughput log-scanning subagents
  - B) Use **Gemini 3.8 Flash** only for deep architectural planning and **Gemini 4 Argon** only for trivial regex lookups
  - C) Never use both models in the same project
  - D) Disable thinking effort on the architect agent
- **Correct**: A
- **Explanation**: **Gemini 4 Argon** delivers frontier reasoning depth for complex architecture, debugging, and `/boost` workflows, while **Gemini 3.8 Flash** provides ultra-fast, cost-efficient execution ideal for parallel lookups, triage, and high-fanout subagent tasks.

### Q9.4 — Permission Precedence (`Deny > Ask > Allow`)
- **Question**: A workspace security configuration has the following three rules:
  1. `Allow`: `Bash(git *)`
  2. `Ask`: `Bash(git push *)`
  3. `Deny`: `Bash(git push --force*)`
  What happens when the agent attempts to run `git push --force origin main`?
- **Options**:
  - A) The command is **blocked immediately** because Antigravity evaluates permissions in strict `Deny > Ask > Allow` order
  - B) The command runs without prompting because `Allow: Bash(git *)` is listed first
  - C) The user is prompted because `Ask` is in the middle
  - D) All three rules cancel out and reset to factory defaults
- **Correct**: A
- **Explanation**: Regardless of rule order in the config file, Antigravity evaluates `Deny` rules first, then `Ask`, and finally `Allow`. Because `git push --force origin main` matches the `Deny` rule, it is unconditionally rejected.

### Q9.5 — OS-Level Sandboxing (Seatbelt & `nsjail`) and `agy remote-control`
- **Question**: How does Antigravity isolate shell commands at the operating-system level on macOS and Linux, and how can you securely monitor or steer a long-running local session from a mobile browser or secondary laptop?
- **Options**:
  - A) It enforces kernel-level filesystem and network boundaries using **Seatbelt** (`sandbox-exec`) on macOS and **`nsjail`** on Linux, and provides `agy remote-control` for encrypted remote session control
  - B) It relies purely on prompt instructions asking the model "please do not read `/etc/shadow`"
  - C) It opens port 23 (Telnet) to the public internet with no password
  - D) It requires running Windows XP inside VirtualBox
- **Correct**: A
- **Explanation**: Antigravity pairs declarative `Deny > Ask > Allow` tool permissions with OS-enforced sandboxing (macOS Seatbelt profiles and Linux `nsjail` namespaces/seccomp filters) and offers `agy remote-control` for authenticated remote session bridging.

---

## Module 10: CLI (`agy`) & Python SDK (`10-cli`)

### Q10.1 — Non-Interactive Headless Execution (`agy -p` & `--mode auto`)
- **Question**: You are building a GitHub Actions workflow that pipes the output of `pytest --tb=short` into Antigravity to generate a root-cause JSON report whenever CI fails. Which command line is correct?
- **Options**:
  - A) `pytest --tb=short | agy -p "Analyze these test failures and output root causes" --mode auto --output-format json`
  - B) `agy --gui --wait-for-mouse-click "Analyze failures"`
  - C) `agy plugin validate pytest`
  - D) `agy -i --mode manual`
- **Correct**: A
- **Explanation**: `agy -p` runs Antigravity in non-interactive print/headless mode, reading piped `stdin` and combining with `--mode auto` and `--output-format json` for deterministic CI/CD automation.

### Q10.2 — Interactive TUI/IDE Keyboard Shortcuts (`alt+m`, `Ctrl+J` / `Ctrl+K`)
- **Question**: During an interactive `agy` CLI or IDE session, which keyboard shortcuts let you quickly cycle execution/permission modes (`manual`, `auto`, `plan`) and navigate between items/panels?
- **Options**:
  - A) `alt+m` to cycle execution/permission modes, and `Ctrl+J` / `Ctrl+K` for fast vertical navigation
  - B) `Ctrl+Alt+Delete` to switch modes, and `F13` to scroll
  - C) `CapsLock+Q` to toggle `mcp_config.json`
  - D) Keyboard shortcuts are disabled in `agy`
- **Correct**: A
- **Explanation**: `alt+m` cycles through operating modes (`manual`, `auto`, `plan`) on the fly without leaving the prompt, while `Ctrl+J` and `Ctrl+K` provide ergonomic keyboard navigation across lists, history, and UI panels.

### Q10.3 — Programmatic Agents with the `google-antigravity` Python SDK
- **Question**: You want to instantiate an Antigravity agent inside a Python microservice using the official `google-antigravity` SDK, equipping it with workspace skills and a custom model. Which code pattern is accurate?
- **Options**:
  - A) Import `Agent` from `google_antigravity`, configure `Agent(model="gemini-4-argon", workspace="/path/to/repo", skills=["code-review-specialist"])`, and call `await agent.run(prompt)`
  - B) Use `urllib.request.urlopen("ftp://localhost:21/agent")`
  - C) Import `antigravity` from Python's Easter egg module (`import antigravity`) which opens an xkcd webcomic
  - D) The SDK only supports PHP 5
- **Correct**: A
- **Explanation**: The `google-antigravity` Python SDK (`google_antigravity` package) exposes the `Agent` class to programmatically configure models, workspaces, tools, skills, and permissions and run turns asynchronously or synchronously.

### Q10.4 — Declarative Multi-Step Pipelines with `@beta.workflows.define`
- **Question**: In the `google-antigravity` Python SDK, what is the purpose of the `@beta.workflows.define` decorator?
- **Options**:
  - A) It defines a reusable, type-checked multi-agent workflow pipeline with state handoffs, retries, and observability across multiple `Agent` steps
  - B) It compiles Python functions into CSS stylesheets
  - C) It disables all hooks in `.agents/hooks.json`
  - D) It is used only to uninstall the `agy` CLI
- **Correct**: A
- **Explanation**: `@beta.workflows.define` allows platform engineers to compose deterministic Python control flow with multi-agent turns, structured Pydantic outputs, and checkpointed step transitions.

### Q10.5 — Hybrid & On-Device Execution with `LiteRTAgentConfig`
- **Question**: You are building a latency-sensitive local developer tool that needs to classify file intents and run lightweight local transformations offline or on-device using Google's LiteRT runtime before escalating complex tasks to Gemini 4 Argon. Which SDK configuration class enables this?
- **Options**:
  - A) `LiteRTAgentConfig` passed to `Agent(...)` in the `google-antigravity` SDK
  - B) `MainframeCobolConfig`
  - C) `WebGLShaderConfig`
  - D) `DisableAllModelsConfig`
- **Correct**: A
- **Explanation**: `LiteRTAgentConfig` configures hardware-accelerated on-device/edge inference via Google LiteRT with seamless fallback or routing to cloud Gemini models when deeper reasoning is required.

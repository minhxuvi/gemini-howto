# Topic & Scenario Index — gemini-howto

**English** | [Tiếng Việt](vi/INDEX.md)

Find the exact module and template you need—organized both by **Problem / Use Case** ("How do I...?") and **Alphabetical Concept Index (A–Z)**.

---

## Part 1: Problem-Oriented Index ("How Do I...?")

### Project Setup & Memory
- **How do I teach Gemini my project's build commands and architecture?** → [Module 02: Rules & Memory](02-memory/README.md) & [`project-GEMINI.md`](02-memory/project-GEMINI.md)
- **How do I write rules that only load when editing specific file types (e.g., `.proto` or `.sql`)?** → [Module 02: `trigger: glob` & `trigger: model_decision`](02-memory/README.md) & [`protobuf-conventions.md`](02-memory/rules/protobuf-conventions.md)
- **How do I share coding rules across multiple repositories in an organization?** → [Module 02: `.agents/rules.json`](02-memory/README.md) & [`02-memory/rules.json`](02-memory/rules.json)
- **How do I automatically turn my corrections in chat into permanent project rules?** → Run `/learn` ([Module 01](01-slash-commands/README.md) & [Module 02](02-memory/README.md))
- **How do I check how many tokens my rules, skills, and MCP tools are consuming?** → Run `/context` ([Module 01](01-slash-commands/README.md) & [Module 02](02-memory/README.md))

### Workflow Automation & Custom Commands
- **How do I create a custom `/commit` or `/optimize` slash command?** → Create `.agents/skills/<name>/SKILL.md` ([Module 01](01-slash-commands/README.md) & [Module 03](03-skills/README.md))
- **How do I migrate legacy `.agents/workflows/*.md` files to modern skills?** → Use `/migrate-workflows` ([Module 01](01-slash-commands/README.md))
- **How do I bundle helper Python/Bash scripts inside a skill so they don't bloat the prompt?** → [Module 03: 3-Stage Progressive Disclosure](03-skills/README.md) & [`doc-generator/`](03-skills/doc-generator/SKILL.md)
- **How do I schedule a recurring daily report or CI check at 9:00 AM?** → Use `/schedule` or `sidecar.json` with `CRON_TZ` ([Module 08](08-checkpoints/README.md) & [`sidecar-schedule-example.json`](08-checkpoints/sidecar-schedule-example.json))

### Multi-Agent & Parallel Execution
- **How do I keep noisy file searches out of my main conversation window?** → Delegate to the built-in `research` subagent ([Module 04](04-subagents/README.md))
- **How do I run multiple subagents in parallel without them overwriting each other's files?** → Use `invoke_subagent` with `Workspace: "branch"` or `"share"` ([Module 04](04-subagents/README.md))
- **How do I solve a deeply complex algorithmic bug or performance bottleneck using competing hypotheses?** → Run `/boost <task>` ([Module 09](09-advanced-features/README.md) & [`boost-and-teamwork-examples.md`](09-advanced-features/boost-and-teamwork-examples.md))
- **How do I build a large multi-component system with autonomous workers and adversarial QA gates?** → Run `/teamwork-preview <task>` ([Module 09](09-advanced-features/README.md))
- **How do I let the agent run autonomously until all tests pass?** → Run `/goal <objective>` ([Module 09](09-advanced-features/README.md))

### Security, Hooks & Sandboxing
- **How do I deterministically block the agent from writing hardcoded API keys or running `rm -rf`?** → Configure a `PreToolUse` hook in `.agents/hooks.json` ([Module 06](06-hooks/README.md), [`security-scan.sh`](06-hooks/security-scan.sh), [`pre-tool-check.sh`](06-hooks/pre-tool-check.sh))
- **How do I automatically run `prettier` or `ruff` after every file edit?** → Configure a `PostToolUse` hook ([Module 06](06-hooks/README.md) & [`format-code.sh`](06-hooks/format-code.sh))
- **How do I prevent the agent from stopping before unit tests pass?** → Configure a `Stop` hook returning `{"decision": "continue"}` ([Module 06](06-hooks/README.md) & [`goal-gate.sh`](06-hooks/goal-gate.sh))
- **How do I restrict which files and network domains terminal commands can access at the OS kernel level?** → Configure `Deny > Ask > Allow` permissions + OS Terminal Sandbox ([Module 09](09-advanced-features/README.md) & [`permissions-examples.json`](09-advanced-features/permissions-examples.json))

### Visual UI, Artifacts & Remote Control
- **How do I leave line-by-line review comments on an agent's plan before it writes code?** → Use `/plan` and inline comments on the **Implementation Plan** artifact ([Module 08](08-checkpoints/README.md))
- **How do I undo the last turn's chat message WITHOUT deleting the code edits on disk?** → Use Confirm Undo (conversation-only revert) or `/rewind` ([Module 08](08-checkpoints/README.md))
- **How do I render an interactive HTML/Tailwind chart or simulator inline in the chat?** → Build a **Generative UI** `<agent-embed>` widget ([Module 08](08-checkpoints/README.md) & [`generative-ui-widget.html`](08-checkpoints/generative-ui-widget.html))
- **How do I monitor and steer my local CLI session from my phone or browser?** → Run `agy --remote-control` or `agy remote-control start` ([Module 09](09-advanced-features/README.md) & [Module 10](10-cli/README.md))

---

## Part 2: Alphabetical Concept Index (A–Z)

- **`@[label](path)` (File Inlining Syntax)** — [Module 02](02-memory/README.md)
- **`AGENTS.md` (Open Standard Instructions)** — [`AGENTS.md`](AGENTS.md), [Module 02](02-memory/README.md)
- **`<agent-embed>` (Generative UI Inline Tag)** — [Module 08](08-checkpoints/README.md), [`generative-ui-widget.html`](08-checkpoints/generative-ui-widget.html)
- **`agy` (Antigravity CLI v1.4.0)** — [Module 10](10-cli/README.md), [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
- **Artifacts (`<appDataDir>/brain/<conversation-id>/`)** — [Module 08](08-checkpoints/README.md)
- **Auto Mode (`--mode auto` & Egress Classifier)** — [Module 09](09-advanced-features/README.md), [Module 10](10-cli/README.md)
- **`/boost` (3-Phase Deep Reasoning Mode)** — [Module 01](01-slash-commands/README.md), [Module 09](09-advanced-features/README.md), [`boost-and-teamwork-examples.md`](09-advanced-features/boost-and-teamwork-examples.md)
- **`/browser` (Browser Subagent)** — [Module 01](01-slash-commands/README.md), [Module 04](04-subagents/README.md)
- **`/btw` (Ephemeral Side Question)** — [Module 01](01-slash-commands/README.md)
- **Checkpoints (`/rewind`, `/undo`, Confirm Undo)** — [Module 08](08-checkpoints/README.md), [`checkpoint-and-worktree-examples.md`](08-checkpoints/checkpoint-and-worktree-examples.md)
- **`commandExecutionPolicy` (`sandbox | auto | eager | off`)** — [Module 04](04-subagents/README.md)
- **`/compact` & `/context`** — [Module 01](01-slash-commands/README.md), [Module 02](02-memory/README.md)
- **`defaultRulesBudget` (20,000-Token Budget & 24 KB Limit)** — [Module 02](02-memory/README.md), [`gemini_concepts_guide.md`](gemini_concepts_guide.md)
- **`define_subagent` & `invoke_subagent`** — [Module 04](04-subagents/README.md)
- **`/fork` (`/branch` Session Cloning)** — [Module 01](01-slash-commands/README.md), [Module 08](08-checkpoints/README.md)
- **Gemini 4 Argon, Gemini 3.8 Flash, Gemini 3.1 Pro, Nano Banana 2** — [Module 09](09-advanced-features/README.md), [Module 10](10-cli/README.md)
- **Gemma 4 (`LiteRTAgentConfig` On-Device Local Model)** — [Module 10](10-cli/README.md), [`local_litert_agent.py`](10-cli/sdk-examples/local_litert_agent.py)
- **`GEMINI.md`** — [`GEMINI.md`](GEMINI.md), [Module 02](02-memory/README.md), [`03-skills/gemini-md/`](03-skills/gemini-md/SKILL.md)
- **Generative UI (`tailwindcss.min.js` & CSS Theme Variables)** — [Module 08](08-checkpoints/README.md), [`generative-ui-widget.html`](08-checkpoints/generative-ui-widget.html)
- **`/goal` (Autonomous Goal Loop)** — [Module 01](01-slash-commands/README.md), [Module 09](09-advanced-features/README.md)
- **`google-antigravity` (Python SDK v0.1.22)** — [Module 10](10-cli/README.md), [`10-cli/sdk-examples/`](10-cli/sdk-examples/)
- **`/grill-me` (Interactive Design Interview)** — [Module 01](01-slash-commands/README.md), [Module 09](09-advanced-features/README.md)
- **Hooks (`hooks.json`: `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`)** — [Module 06](06-hooks/README.md), [`06-hooks/hooks.json`](06-hooks/hooks.json)
- **Implementation Plan Artifact & Inline Comments** — [Module 08](08-checkpoints/README.md), [`implementation-plan-template.md`](08-checkpoints/implementation-plan-template.md)
- **`/learn` (`learning_proposal.md` Memory Distillation)** — [Module 01](01-slash-commands/README.md), [Module 02](02-memory/README.md)
- **MCP (`mcp_config.json`, Stdio, Streamable HTTP, `${VAR}` headers, Fix with Agent)** — [Module 05](05-mcp/README.md)
- **OS Kernel Sandbox (Apple Seatbelt `sandbox-exec`, Linux `nsjail`, Windows `AppContainer`)** — [Module 09](09-advanced-features/README.md)
- **Permissions (`Deny > Ask > Allow`, `action(target)`, `regex:`)** — [Module 09](09-advanced-features/README.md), [`permissions-examples.json`](09-advanced-features/permissions-examples.json)
- **Plugins (`plugin.json`, `agy plugin install/validate`, `/plugin`)** — [Module 07](07-plugins/README.md)
- **Remote Control (`agy remote-control`, `/remote-control`)** — [Module 09](09-advanced-features/README.md), [Module 10](10-cli/README.md)
- **Rules (`.agents/rules/*.md`, `.agents/rules.json`, `always_on | model_decision | glob | manual`)** — [Module 02](02-memory/README.md)
- **Sidecars & Automations (`sidecar.json`, `/schedule`, `CRON_TZ`, `sidecar://`)** — [Module 08](08-checkpoints/README.md)
- **Skills (`.agents/skills/<name>/SKILL.md`, `.agents/skills.json`)** — [Module 01](01-slash-commands/README.md), [Module 03](03-skills/README.md)
- **Subagents (`.agents/agents/*.md`, `Workspace: inherit | branch | share`)** — [Module 04](04-subagents/README.md)
- **`/teamwork-preview` (2-Phase Multi-Agent Teams: `Sentinel`, `Critic`, `Challenger`, `Auditor`)** — [Module 09](09-advanced-features/README.md), [`boost-and-teamwork-examples.md`](09-advanced-features/boost-and-teamwork-examples.md)
- **Workflows SDK (`@beta.workflows.define`, `phase`, `parallel`, `pipeline`)** — [Module 10](10-cli/README.md), [`dynamic_workflow.py`](10-cli/sdk-examples/dynamic_workflow.py)

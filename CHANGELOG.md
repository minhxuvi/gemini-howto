# Changelog

All notable changes to the **gemini-howto** curriculum and its alignment with **Google Antigravity** and **Gemini** releases are documented in this file.

---

## [1.0.0] — 2026-10-21

### Aligned Ecosystem Versions
- **Antigravity Desktop & Web App**: `v2.24.0` (October 2026)
- **Antigravity CLI (`agy`)**: `v1.4.0` (October 2026)
- **Antigravity Python SDK (`google-antigravity`)**: `v0.1.22` (October 2026)
- **Antigravity IDE**: `v2.5.5` & VS Code Extension `v1.7.0`
- **Frontier Models**: Gemini 4 Argon (`gemini-4-argon`), Gemini 3.8 Flash (`gemini-3.8-flash`), Gemini 3.1 Pro (`gemini-3.1-pro`), Nano Banana 2, Gemma 4 26B (local LiteRT-LM)

### Added
- **Complete 10-Module Curriculum (`01-` to `10-`)**:
  - `01-slash-commands/`: Full coverage of 35+ built-in commands (`/boost`, `/teamwork-preview`, `/goal`, `/plan`, `/grill-me`, `/learn`, `/btw`, `/rewind`, `/fork`, `/schedule`, `/browser`) + 8 ready-to-use skill-based slash command templates.
  - `02-memory/`: Deep dive into `GEMINI.md`, `AGENTS.md`, modular `.agents/rules/*.md` (`always_on`, `model_decision`, `glob`, `manual`), `@[label](path)` file inlining, the 24 KB / 20,000-token `defaultRulesBudget`, `.agents/rules.json` cross-project inheritance, and `/learn`.
  - `03-skills/`: Open Agent Skills (`agentskills.io`) 3-stage progressive disclosure guide + 6 multi-file skill packages (`code-review-specialist`, `doc-generator`, `refactor`, `gemini-md`, `blog-draft`, `brand-voice`) and `skills.json`.
  - `04-subagents/`: Built-in subagents (`research`, `browser`, `self`), custom `.agents/agents/*.md` specs, `Workspace: inherit | branch | share` isolation, reactive wakeup via `send_message`, CLI `/agents` (`Ctrl+J`/`Ctrl+K`), and 9 specialized subagent templates.
  - `05-mcp/`: `~/.gemini/config/mcp_config.json`, Stdio & Streamable HTTP transports with `${VAR}` header interpolation (CLI v1.4.0), `mcp(server/tool)` permissions, **Fix with Agent**, and 4 production JSON configs.
  - `06-hooks/`: All 6 lifecycle events (`SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`), camelCase JSON stdin/stdout contracts, `overwrite` & `injectSteps`, and 8 executable hook scripts.
  - `07-plugins/`: Native Antigravity plugins (`plugin.json`, root-level `hooks.json` & `mcp_config.json`), `agy plugin install/validate` workflows, and 3 complete plugin bundles (`pr-review`, `devops-automation`, `documentation`).
  - `08-checkpoints/`: Checkpoints (`/rewind`, `/fork`, Confirm Undo conversation-only revert, Git Worktrees), Implementation Plan inline commenting, Generative UI (`<agent-embed>` with `tailwindcss.min.js` & CSS theme variables), and Sidecars/Automations (`sidecar.json` + `/schedule` with `CRON_TZ`).
  - `09-advanced-features/`: `/boost` (3-phase DeepCoder/DeepInvestigator), `/teamwork-preview` (2-phase with Sentinel, Critic, Challenger, Auditor), `/goal`, Gemini 4 Argon effort tuning, Fine-Grained Permissions (`Deny > Ask > Allow`), OS Terminal Sandbox (Seatbelt/`nsjail`/`AppContainer`), and `agy remote-control`.
  - `10-cli/`: Complete reference for `agy` CLI v1.4.0 (TUI, `-p` print mode, `--mode auto`, `alt+m` queue mode, OSC 7501) and `google-antigravity` Python SDK v0.1.22 (`Agent`, `@beta.workflows.define`, `LiteRTAgentConfig`, `LocalOpenAIAgentConfig`).
- **Interactive Learning Skills (`.agents/skills/`)**:
  - `/self-assessment`: 10-question adaptive diagnostic using `ask_question`.
  - `/lesson-quiz`: 5-question module quiz across a 50-question bank.
- **Complete Vietnamese Edition (`vi/`)**:
  - Full Vietnamese translation of all root guides and all 10 module tutorials (`vi/01-slash-commands/` through `vi/10-cli/`).

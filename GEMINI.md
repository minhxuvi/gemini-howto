# GEMINI.md — Repository Instructions for Google Antigravity & Gemini

This file provides persistent workspace context and authoring conventions for agents working in the **gemini-howto** repository.

## Project Overview

**gemini-howto** is a comprehensive, visual, example-driven guide to mastering **Google Antigravity** (App v2.24+, CLI `agy` v1.4+, Python SDK `google-antigravity` v0.1.22+, and IDE extensions) powered by **Gemini** frontier models (Gemini 4 Argon, Gemini 3.8 Flash, Gemini 3.1 Pro, Nano Banana 2).

The repository is organized as a progressive 10-module curriculum (`01-` through `10-`), accompanied by production-ready copy-pasteable templates, interactive self-assessment skills (`.agents/skills/`), and a complete Vietnamese edition (`vi/`).

## Repository Structure

```text
gemini-howto/
├── README.md                    # Main landing page, feature matrix, and quick start
├── GEMINI.md                    # Workspace instructions for Gemini / Antigravity
├── AGENTS.md                    # Cross-agent open standard instructions (includes GEMINI.md)
├── LEARNING-ROADMAP.md          # Structured learning tracks from Beginner to Architect
├── QUICK_REFERENCE.md           # Single-page cheat sheet for all commands & configs
├── CATALOG.md                   # Complete inventory of copy-pasteable templates
├── INDEX.md                     # Topic & scenario-based lookup index
├── gemini_concepts_guide.md     # Deep architectural guide & mental models
├── STYLE_GUIDE.md               # Documentation & Mermaid diagram authoring standards
├── clean-code-rules.md          # Modular clean-code engineering rules reference
├── CHANGELOG.md                 # Curriculum & Antigravity version alignment history
├── .agents/skills/              # Interactive learning skills (/self-assessment, /lesson-quiz)
├── 01-slash-commands/           # Built-in slash commands & skill-backed custom commands
├── 02-memory/                   # GEMINI.md, AGENTS.md, .agents/rules/*.md & /learn
├── 03-skills/                   # Agent Skills (.agents/skills/<name>/SKILL.md)
├── 04-subagents/                # Subagents (.agents/agents/*.md, branch/share worktrees)
├── 05-mcp/                      # Model Context Protocol (mcp_config.json, Stdio & HTTP)
├── 06-hooks/                    # Lifecycle Hooks (hooks.json, 6 events, JSON contract)
├── 07-plugins/                  # Native Antigravity Plugins (plugin.json, agy plugin CLI)
├── 08-checkpoints/              # Checkpoints, Artifacts, Generative UI & Sidecars
├── 09-advanced-features/        # /boost, /teamwork-preview, Permissions, Sandbox, Remote Control
├── 10-cli/                      # Antigravity CLI (agy) & Python SDK (google-antigravity)
└── vi/                          # Complete Vietnamese translation of the curriculum
```

## Authoritative Technical Conventions

When adding or updating tutorials, templates, or quiz questions in this repository, enforce the following authoritative Antigravity specifications:

1. **Customization Paths**:
   - Workspace customizations live in `.agents/` (`.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/plugins/`, `.agents/hooks.json`).
   - Global user customizations live in `~/.gemini/config/` (`rules/`, `skills/`, `agents/`, `plugins/`, `sidecars/`, `mcp_config.json`, `hooks.json`) and `~/.gemini/antigravity-cli/settings.json`.
   - Never use `.claude/` paths in Antigravity examples.

2. **Rules & Memory (`02-memory/`)**:
   - Standalone `GEMINI.md` and `AGENTS.md` files use plain Markdown (no YAML frontmatter required) and are loaded hierarchically from workspace root down to target subdirectories.
   - Modular rule files in `.agents/rules/*.md` **require** YAML frontmatter with `trigger: always_on | model_decision | glob | manual`.
   - Use `@[label](relative/path.md)` to inline referenced files (stripping frontmatter) or `@relative/path.md` for path-pointer references.
   - Respect the **24 KB** per-file limit and the **20,000-token** aggregate `defaultRulesBudget`.

3. **Skills & Custom Slash Commands (`01-slash-commands/` & `03-skills/`)**:
   - Legacy `.agents/workflows/*.md` are deprecated (migrated via `/migrate-workflows`).
   - Every skill in `.agents/skills/<name>/SKILL.md` is both semantically auto-discovered AND directly invokable as `/<name>`.

4. **Hooks Contract (`06-hooks/`)**:
   - Hooks are configured in `.agents/hooks.json`, `~/.gemini/config/hooks.json`, or `<plugin-root>/hooks.json`.
   - Supported events: `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`.
   - Always use **camelCase** JSON keys (`conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`, `toolName`, `toolInput`, `injectSteps`, `permissionOverrides`, `fullyIdle`, `terminationReason`).

5. **Plugins (`07-plugins/`)**:
   - Manifest is `<plugin-root>/plugin.json`.
   - `hooks.json` and `mcp_config.json` must sit at the **plugin root**, never inside a `hooks/` subdirectory.

6. **Documentation & Diagram Standards**:
   - Follow @[Style Guide](STYLE_GUIDE.md) for Markdown structure, Mermaid diagram syntax (always quote node labels containing parentheses or special characters), and module navigation footers.
   - Keep English (`./`) and Vietnamese (`./vi/`) documentation synchronized when updating core concepts.

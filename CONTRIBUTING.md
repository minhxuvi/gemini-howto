# Contributing to gemini-howto

Thank you for your interest in contributing to **gemini-howto**! Our goal is to maintain the most practical, accurate, and copy-paste-ready guide to **Google Antigravity** and **Gemini**.

---

## Ways to Contribute

1. **New Copy-Paste Templates**:
   - Practical Skills (`.agents/skills/<name>/SKILL.md`) in `01-slash-commands/` or `03-skills/`
   - Scoped Rules (`.agents/rules/*.md`) in `02-memory/rules/`
   - Specialized Subagents (`.agents/agents/*.md`) in `04-subagents/`
   - MCP Server configs (`mcp_config.json`) in `05-mcp/`
   - Lifecycle Hook scripts (`hooks.json` + shell/Python handlers) in `06-hooks/`
   - Native Antigravity Plugins (`plugin.json` bundles) in `07-plugins/`
   - Generative UI widgets, Implementation Plan templates, or `sidecar.json` automations in `08-checkpoints/`
   - Python SDK (`google-antigravity`) examples in `10-cli/sdk-examples/`
2. **Version Updates**: Keeping documentation aligned with new releases of Antigravity App, `agy` CLI, IDE extensions, and the `google-antigravity` Python SDK.
3. **Translations**: Keeping the Vietnamese (`vi/`) tutorials synchronized with root English tutorials.

---

## Quality Checklist Before Submitting a PR

- [ ] Read and follow [`GEMINI.md`](GEMINI.md) and [`STYLE_GUIDE.md`](STYLE_GUIDE.md).
- [ ] Verify that all customization file paths use `.agents/` (workspace) or `~/.gemini/config/` (global).
- [ ] Ensure any modular rule in `02-memory/rules/` includes valid YAML frontmatter (`trigger: always_on | model_decision | glob | manual`) and stays under 24 KB.
- [ ] Ensure any hook example in `06-hooks/` uses the exact camelCase JSON stdin/stdout schema (`conversationId`, `workspacePaths`, `toolName`, `toolInput`, `injectSteps`, `fullyIdle`).
- [ ] Validate any plugin changes in `07-plugins/` using `agy plugin validate ./07-plugins/<plugin-name> --strict`.
- [ ] Check that Mermaid node labels with parentheses or special characters are enclosed in double quotes (`["Label (Detail)"]`).
- [ ] Update [`CATALOG.md`](CATALOG.md) and [`INDEX.md`](INDEX.md) if you added a new template file.

# Google Antigravity & Gemini: Quick Reference Cheat Sheet

**English** | [Tiếng Việt](vi/QUICK_REFERENCE.md)

A single-page cheat sheet covering every slash command, file path, YAML frontmatter schema, JSON hook contract, permission syntax, CLI flag, and Python SDK snippet in **Google Antigravity** (App v2.24+, CLI `agy` v1.4+, Python SDK `google-antigravity` v0.1.22+).

---

## 1. File Locations & Discovery Hierarchy

| Customization | Workspace Path (Project-Scoped) | Global Path (User-Scoped) | Multi-Project Registry |
| :--- | :--- | :--- | :--- |
| **Always-On Instructions** | `./GEMINI.md`, `./AGENTS.md` (and any subdirectory) | `~/.gemini/GEMINI.md`, `~/.gemini/AGENTS.md`, `~/.gemini/config/GEMINI.md` | Via `@[label](path)` includes |
| **Modular Scoped Rules** | `.agents/rules/*.md` | `~/.gemini/config/rules/*.md` | `.agents/rules.json` |
| **Skills & `/commands`** | `.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills/<name>/SKILL.md` | `.agents/skills.json` |
| **Subagents** | `.agents/agents/<name>.md` | `~/.gemini/config/agents/<name>.md` | Bundled via Plugins |
| **MCP Servers** | `<plugin-root>/mcp_config.json` | `~/.gemini/config/mcp_config.json` | Bundled via Plugins |
| **Lifecycle Hooks** | `.agents/hooks.json` | `~/.gemini/config/hooks.json` | `<plugin-root>/hooks.json` |
| **Native Plugins** | `.agents/plugins/<name>/plugin.json` | `~/.gemini/config/plugins/<name>/plugin.json` | `.agents/plugins.json` |
| **Sidecars & Automations** | `<plugin-root>/sidecars/<id>/sidecar.json` | `~/.gemini/config/sidecars/<id>/sidecar.json` | Managed via `/schedule` |
| **CLI Settings & Keys** | `.agents/settings.json` | `~/.gemini/antigravity-cli/settings.json`, `keybindings.json` | — |

---

## 2. Built-in Slash Commands (`01-slash-commands/`)

### Autonomous & Multi-Agent Modes
| Command | Purpose |
| :--- | :--- |
| `/boost <task>` | Launch 3-phase deep reasoning (`Orchestrator` → parallel `DeepCoder`/`DeepInvestigator` worktrees → multi-round verification) |
| `/teamwork-preview <task>` | Launch 2-phase multi-agent team (`Scoping Interview` → autonomous `Sentinel`, `Explorers`, `Workers`, `Critic`, `Challenger`, `Auditor`) |
| `/goal <objective>` | Run continuously until the goal and all verification checks are complete |
| `/plan [task]` | Enter Planning mode and generate a reviewable **Implementation Plan** artifact |
| `/grill-me` | Conduct an interactive architectural interview to resolve ambiguities before coding |
| `/browser <task>` | Delegate web navigation, UI testing, or scraping to the sandboxed browser subagent |
| `/schedule <when> <task>` | Create a recurring cron job or one-shot background automation (`sidecar.json`) |

### Session, Context & Checkpoints
| Command | Aliases | Purpose |
| :--- | :--- | :--- |
| `/rewind` | `/undo` | Revert conversation and/or workspace files to a previous turn checkpoint |
| `/fork` | `/branch` | Clone the current conversation at this point into an independent parallel session |
| `/btw <question>` | — | Ask a quick side question in an ephemeral overlay without polluting main conversation history |
| `/compact` | — | Summarize conversation history to free up context window tokens |
| `/context` | — | Inspect live context token usage across rules, skills, MCP tools, and conversation history |
| `/diff` | — | View uncommitted git changes and current-turn file diffs |
| `/resume` | `/switch`, `/conversation` | Switch to or resume a previous conversation thread |
| `/clear` | `/new` | Start a fresh conversation session |
| `/copy [n\|btw]` | — | Copy the latest agent response, the *n*-th response, or the latest `/btw` answer |

### Customizations, Models & Configuration
| Command | Aliases | Purpose |
| :--- | :--- | :--- |
| `/learn [instruction]` | — | Distill session corrections into a persistent rule or skill via `learning_proposal.md` |
| `/skills` | — | List and inspect all discovered workspace, global, and plugin skills |
| `/agents` | — | Open the live Subagents manager (inspect status, jump to approvals, terminate) |
| `/mcp` | — | Inspect MCP servers, view exposed tools, **Restart**, or run **Fix with Agent** |
| `/hooks` | — | View registered lifecycle hooks across workspace, global, and plugin scopes |
| `/plugin` | `/plugins` | Open interactive plugin manager (install, enable, disable, uninstall) |
| `/model` | — | Switch active model (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.1-pro`, etc.) |
| `/effort [level]` | — | Set reasoning effort (`low`, `medium`, `high`, `max`) |
| `/fast` | — | Toggle fast execution mode (`gemini-3.8-flash`) |
| `/permissions` | — | View and edit `Allow`, `Ask`, and `Deny` permission rules |
| `/remote-control [on\|off]` | — | Enable/disable remote web control at `https://antigravity.google.com` |
| `/config` | `/settings` | Open interactive settings editor |

---

## 3. Rules & Memory Cheat Sheet (`02-memory/`)

### Modular Rule Frontmatter (`.agents/rules/*.md`)
```yaml
---
trigger: model_decision          # always_on | model_decision | glob | manual
description: Apply when writing or reviewing PostgreSQL migrations or SQL queries.
globs: "**/*.sql, db/migrations/**"  # Required only when trigger: glob
---
```

### File Inclusions & Limits
- **Inline file content** (strips target YAML frontmatter): `@[API Standards](docs/api-standards.md)`
- **Path pointer reference** (zero upfront token cost): `@docs/api-standards.md`
- **Hard Limits**: **24 KB** (`24,000` bytes) per rule file; **20,000 tokens** aggregate `defaultRulesBudget` for `always_on`/global rules (excess rules are gracefully demoted to path pointers).

---

## 4. Skills Cheat Sheet (`03-skills/`)

Every `.agents/skills/<name>/SKILL.md` is both a `/<name>` slash command and semantically auto-discovered:

```yaml
---
name: code-review-specialist
description: Perform a structured security, performance, and maintainability code review. Use when reviewing PRs, staged diffs, or when the user invokes /code-review-specialist.
---

# Instructions
1. Run `bash scripts/check-metrics.sh` to gather diff complexity metrics.
2. Consult `resources/checklist.md` and format findings using `examples/sample-review.md`.
```

---

## 5. Subagents Cheat Sheet (`04-subagents/`)

### Custom Subagent (`.agents/agents/secure-reviewer.md`)
```yaml
---
name: secure-reviewer
description: Read-only application security auditor for OWASP Top 10 and secret exposure.
tools:
  - view_file
  - grep_search
  - find_by_name
  - list_dir
  - run_command
subagent: true
mainAgent: false
model: inherit                   # inherit | flash_lite | flash | pro
commandExecutionPolicy: sandbox  # sandbox | auto | eager | off
---
```

### Workspace Isolation Modes (`invoke_subagent`)
- `Workspace: "inherit"` — Shares parent workspace directory (best for read-only or non-overlapping edits).
- `Workspace: "branch"` — Clones an isolated workspace branch (best for parallel competing implementations).
- `Workspace: "share"` — Git-worktree-style shared storage with independent branch state.

---

## 6. MCP Configuration Cheat Sheet (`05-mcp/`)

File: `~/.gemini/config/mcp_config.json` (or `<plugin-root>/mcp_config.json`)

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

---

## 7. Lifecycle Hooks Cheat Sheet (`06-hooks/`)

File: `.agents/hooks.json` | `~/.gemini/config/hooks.json` | `<plugin-root>/hooks.json`

| Event | Config Structure | Can Block / Modify? | Key Output JSON Fields (stdout) |
| :--- | :--- | :---: | :--- |
| `SessionStart` | Flat handler array | Injects context | `{"injectSteps": [{"systemMessage": {"systemMessage": "..."}}]}` |
| `PreToolUse` | Matcher array (`matcher` + `hooks`) | **Yes** (`deny`, `ask`, `allow`, `overwrite`) | `{"decision": "deny", "reason": "...", "overwrite": {...}, "permissionOverrides": [...]}` |
| `PostToolUse` | Matcher array (`matcher` + `hooks`) | Side-effects / logs | `{}` |
| `PreInvocation` | Flat handler array | Injects context | `{"injectSteps": [{"ephemeralMessage": "..."}]}` |
| `PostInvocation` | Flat handler array | Force continue / stop | `{"injectSteps": [...], "terminationBehavior": "force_continue"}` |
| `Stop` | Flat handler array | **Yes** (`continue` vs `allow`) | `{"decision": "continue", "reason": "Unit tests failed"}` |

**Common Stdin Payload (camelCase)**: `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName` (+ `toolName`, `toolInput` on tool hooks; `fullyIdle`, `terminationReason` on `Stop`).

---

## 8. Permissions & OS Sandbox Cheat Sheet (`09-advanced-features/`)

Precedence: **`Deny` > `Ask` > `Allow`**

| Rule Syntax | Meaning |
| :--- | :--- |
| `read_file(.env*)` | Match reading `.env` files (typically placed in `Deny`) |
| `write_file(src/**)` | Match writing files under `src/` |
| `command(npm test*)` | Match running `npm test` commands inside the OS Sandbox |
| `command(regex:^git (status\|diff\|log))` | Regex match for safe read-only Git commands |
| `unsandboxed(docker *)` | Allow running `docker` outside the OS Seatbelt/`nsjail` sandbox |
| `read_url(docs.python.org)` | Allow outbound network/HTTP access to `docs.python.org` inside the sandbox |
| `mcp(github/*)` | Match all tools exposed by the `github` MCP server |
| `mcp(postgres/query)` | Match only the `query` tool on the `postgres` MCP server |

---

## 9. Antigravity CLI (`agy`) & Python SDK (`10-cli/`)

### Common `agy` CLI Commands
```bash
agy                                           # Start interactive TUI
agy -p "Summarize staged changes"             # Headless print mode
git diff | agy -p "Review for security bugs"  # Pipe stdin to headless agent
agy --model gemini-4-argon --effort max       # Launch with frontier model & max reasoning
agy --mode auto --sandbox -p "Fix lints"      # Autonomous mode inside OS Sandbox
agy --resume                                  # Resume recent session (-c / --continue for latest)
agy plugin install pr-review@antigravity-plugins-official
agy plugin validate ./my-plugin --strict
agy remote-control start --name "workstation" # Start headless remote-control daemon
```

### TUI Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| `Alt+M` | Toggle message queueing mode (`Queue` vs `Immediate Interrupt`) |
| `Ctrl+J` / `Alt+J` | Jump directly to a background subagent waiting for permission approval |
| `Ctrl+K` | Fast-path approve a pending subagent tool request |
| `Shift+Tab` | Cycle execution/planning mode |
| `Esc` / `Ctrl+C` | Interrupt current generation or tool execution |

### Python SDK (`google-antigravity` v0.1.22+) Minimal Example
```python
from google.antigravity import Agent, GeminiModelOptions, LocalAgentConfig

agent = Agent(
    model="gemini-4-argon",
    config=LocalAgentConfig(workspace_dir="."),
    model_options=GeminiModelOptions(max_output_tokens=16384),
)

for chunk in agent.stream("Audit the authentication module and run pytest"):
    if chunk.thoughts:
        print(f"[Thinking] {chunk.thoughts}")
    if chunk.text:
        print(chunk.text, end="", flush=True)
```

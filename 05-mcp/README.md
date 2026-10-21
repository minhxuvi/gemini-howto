<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/gemini-howto-logo-dark.svg">
  <img alt="Gemini & Antigravity How To" src="../resources/logos/gemini-howto-logo.svg">
</picture>

# Module 05: Model Context Protocol (MCP) — Complete Reference Guide

The **Model Context Protocol (MCP)** is an open standard that connects Google Antigravity to external tools, databases, issue trackers, cloud APIs, and live data sources. By configuring MCP servers in `mcp_config.json`, you extend the agent's built-in toolset with custom, strongly-typed capabilities governed by Antigravity's fine-grained permission engine.

## Table of Contents

1. [Overview](#overview)
2. [MCP Architecture in Antigravity](#mcp-architecture-in-antigravity)
3. [Discovery Locations & Scoping (`mcp_config.json`)](#discovery-locations--scoping-mcp_configjson)
4. [Supported Transports: Stdio, Streamable HTTP & Legacy SSE Bridge](#supported-transports-stdio-streamable-http--legacy-sse-bridge)
5. [Environment Variable Interpolation (`${VAR}`) & Secrets Management](#environment-variable-interpolation-var--secrets-management)
6. [Fine-Grained MCP Permissions (`mcp(server/tool)`)](#fine-grained-mcp-permissions-mcpservertool)
7. [Subagent-Scoped MCP Servers](#subagent-scoped-mcp-servers)
8. [Python SDK MCP Integration (`McpStdioServer` & `McpStreamableHttpServer`)](#python-sdk-mcp-integration-mcpstdioserver--mcpstreamablehttpserver)
9. [Managing & Troubleshooting MCP Servers (`/mcp` & Fix with Agent)](#managing--troubleshooting-mcp-servers-mcp--fix-with-agent)
10. [Security Best Practices](#security-best-practices)
11. [Ready-to-Use `mcp_config.json` Templates in This Folder](#ready-to-use-mcp_configjson-templates-in-this-folder)
12. [Installation Instructions](#installation-instructions)
13. [Related Concepts](#related-concepts)

---

## Overview

While Rules (`GEMINI.md`) and Skills (`SKILL.md`) provide instructions and procedural knowledge, **MCP Servers** give Antigravity live, two-way execution access to external systems:

- **Live External Context**: Query PostgreSQL/SQLite schemas, inspect GitHub PR review comments, fetch Sentry stack traces, or search internal documentation in real time.
- **Standardized Tool Binding**: Discovered MCP tools are automatically converted into native agent tools (`mcp_<server>_<tool>`) and injected into the agent's tool registry.
- **Zero-Trust Permission Controls**: Every MCP tool call passes through Antigravity's permission engine (`Allow`, `Ask`, `Deny`) using `mcp(server-name/tool-name)` rules and `PreToolUse` hooks.
- **Self-Healing Diagnostics**: Built-in **Restart** and **Fix with Agent** actions in the MCP panel automatically diagnose broken server configurations, missing `npx`/`uvx` binaries, or expired tokens.

---

## MCP Architecture in Antigravity

When Antigravity starts a session or loads a plugin, the Language Server / Runtime connects to configured MCP servers, discovers their tool schemas, and routes tool executions over either **Stdio** (local child process) or **Streamable HTTP** (remote service).

```mermaid
flowchart TB
    subgraph AGY["Google Antigravity Runtime"]
        Planner["Gemini Planner / Agent"]
        PermEngine["Permission Engine & PreToolUse Hooks<br/>mcp(server/tool) -> Allow | Ask | Deny"]
        MCPHost["Antigravity MCP Host Client"]
        
        Planner -->|"1. Emits mcp_github_get_pr"| PermEngine
        PermEngine -->|"2. Approved"| MCPHost
    end

    subgraph Transports["MCP Transport Layer"]
        Stdio["Stdio Transport<br/>(Local Child Process: npx / uvx / binary)"]
        HTTP["Streamable HTTP Transport<br/>(HTTPS POST /mcp + Bearer ${TOKEN})"]
        Bridge["mcp-remote Bridge<br/>(Stdio -> Legacy HTTP+SSE /sse)"]
    end

    subgraph External["External Data & Services"]
        LocalDB[("PostgreSQL / SQLite<br/>Local Filesystem")]
        CloudAPI["GitHub / Sentry / Linear<br/>Remote Cloud APIs"]
        LegacySSE["Legacy SSE MCP Endpoints<br/>(MCP Spec 2024-11-05)"]
    end

    MCPHost -->|"stdin / stdout JSON-RPC"| Stdio
    MCPHost -->|"Streamable HTTP (2025-03-26)"| HTTP
    MCPHost -->|"stdin / stdout"| Bridge

    Stdio --> LocalDB
    HTTP --> CloudAPI
    Bridge --> LegacySSE

    style AGY fill:#e1f5fe,stroke:#0277bd,color:#000
    style PermEngine fill:#fff3e0,stroke:#e65100,color:#000
    style Transports fill:#f3e5f5,stroke:#6a1b9a,color:#000
    style External fill:#e8f5e9,stroke:#2e7d32,color:#000
```

---

## Discovery Locations & Scoping (`mcp_config.json`)

Antigravity discovers MCP server definitions from `mcp_config.json` files in two primary locations, plus optional subagent frontmatter:

| Scope | Configuration Path | Lifecycle & Visibility |
| :--- | :--- | :--- |
| **Global User Configuration** | `~/.gemini/config/mcp_config.json` | Active across all projects and workspaces on your machine |
| **Plugin Configuration** | `<plugin-root>/mcp_config.json` *(e.g., `~/.gemini/config/plugins/<name>/mcp_config.json` or `.agents/plugins/<name>/mcp_config.json`)* | Active whenever the parent plugin is enabled; tools are automatically namespaced to prevent collisions |
| **Subagent Frontmatter** | `.agents/agents/<name>.md` (`mcpServers:` field) | Scoped exclusively to that custom subagent when invoked |

### Basic `mcp_config.json` Structure

The file contains a top-level `"mcpServers"` object mapping each unique server name to its transport configuration:

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "postgres-local": {
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"],
      "env": {
        "PGCONNECT_TIMEOUT": "10"
      }
    }
  }
}
```

---

## Supported Transports: Stdio, Streamable HTTP & Legacy SSE Bridge

Antigravity natively supports **Stdio** and **Streamable HTTP** transports, and supports legacy HTTP+SSE servers via the `mcp-remote` bridge.

```mermaid
sequenceDiagram
    participant Agent as Antigravity Agent
    participant Host as MCP Host
    participant Stdio as Local Stdio Server (npx/uvx)
    participant HTTP as Remote Streamable HTTP (/mcp)

    Note over Host,Stdio: 1. Stdio Transport (Local Process)
    Host->>Stdio: Spawn process with args & env
    Host->>Stdio: JSON-RPC initialize & tools/list (stdin)
    Stdio-->>Host: Tool definitions (stdout)
    Agent->>Host: Call mcp_postgres_execute_sql
    Host->>Stdio: tools/call (stdin)
    Stdio-->>Host: Query result JSON (stdout)

    Note over Host,HTTP: 2. Streamable HTTP Transport (Remote)
    Host->>HTTP: HTTPS POST /mcp (Headers: Authorization: Bearer ${VAR})
    HTTP-->>Host: Tool definitions & session state
    Agent->>Host: Call mcp_github_list_pull_requests
    Host->>HTTP: HTTPS POST /mcp (tools/call)
    HTTP-->>Host: Streamed JSON-RPC response
```

### 1. Stdio Transport (Local Process)

Used to launch local command-line MCP servers (Node.js `npx`, Python `uvx`, Docker containers, or compiled binaries). Antigravity spawns the process and communicates over `stdin` and `stdout`.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `command` | `string` | **Yes** | Executable to run (e.g., `"npx"`, `"uvx"`, `"node"`, `"python3"`, `"docker"`). |
| `args` | `string[]` | No | Array of command-line arguments passed to `command`. |
| `env` | `object` | No | Key-value map of environment variables injected into the spawned process. |

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Projects/my-app"
      ]
    }
  }
}
```

### 2. Streamable HTTP Transport (Remote Server)

Used to connect to remote cloud MCP servers implementing the modern [MCP Streamable HTTP specification (2025-03-26)](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `url` | `string` | **Yes** | The HTTP(S) URL of the remote Streamable HTTP MCP endpoint (typically ending in `/mcp`). The legacy alias `serverUrl` is also accepted. |
| `headers` | `object` | No | Custom HTTP headers sent with every request. Supports `${VAR}` environment variable interpolation (Antigravity v1.4.0+). |

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 3. Legacy HTTP+SSE Bridge (`mcp-remote`)

> [!IMPORTANT]
> The deprecated HTTP+SSE transport (`MCP spec 2024-11-05`, typically ending in `/sse`) is not directly supported via `url`. Always point `url` to the server's Streamable HTTP endpoint (`/mcp`). If a third-party server only exposes a legacy `/sse` endpoint, bridge it over Stdio using `npx -y mcp-remote`:

```json
{
  "mcpServers": {
    "legacy-sse-service": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.legacy-provider.com/sse",
        "--header",
        "Authorization: Bearer ${LEGACY_API_TOKEN}"
      ],
      "env": {
        "LEGACY_API_TOKEN": "${LEGACY_API_TOKEN}"
      }
    }
  }
}
```

---

## Environment Variable Interpolation (`${VAR}`) & Secrets Management

Never hardcode API keys, Personal Access Tokens (PATs), or database passwords directly in `mcp_config.json`.

### `${VAR}` Header & Config Interpolation (v1.4.0+)

Starting in **Antigravity v1.4.0+**, `mcp_config.json` supports `${VAR}` environment variable interpolation in HTTP `headers`, `url`, `args`, and `env` values:

```json
{
  "mcpServers": {
    "sentry": {
      "url": "https://mcp.sentry.dev/mcp",
      "headers": {
        "Authorization": "Bearer ${SENTRY_AUTH_TOKEN}",
        "X-Sentry-Org": "${SENTRY_ORG_SLUG}"
      }
    }
  }
}
```

### Storing Secrets Safely in `~/.gemini/.env`

To make credentials available to Antigravity across both the desktop App, IDE, and CLI without polluting your global shell profile or risking accidental Git commits:

1. Store your secrets in `~/.gemini/.env` with strict file permissions (`chmod 600 ~/.gemini/.env`):

```bash
# Create a private environment file for Antigravity
touch ~/.gemini/.env
chmod 600 ~/.gemini/.env

cat >> ~/.gemini/.env << 'EOF'
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
DATABASE_URL=postgresql://readonly_user:pass@localhost:5432/app_db
SENTRY_AUTH_TOKEN=sntrys_your_token_here
SLACK_BOT_TOKEN=xoxb-your-token-here
EOF
```

2. Reference `${GITHUB_PERSONAL_ACCESS_TOKEN}` or `${DATABASE_URL}` inside `~/.gemini/config/mcp_config.json`.

> [!CAUTION]
> Never read or print the contents of `~/.gemini/.env` inside an agent conversation, as doing so exposes plaintext secrets in the conversation transcript (`transcript.jsonl`). To verify whether a key exists without exposing its value, check keys only: `cut -d= -f1 ~/.gemini/.env`.

---

## Fine-Grained MCP Permissions (`mcp(server/tool)`)

Connecting an MCP server does not mean the agent should have unrestricted execution access to destructive tools (like `delete_repository`, `merge_pull_request`, or `drop_table`). Antigravity's **Permission Grants** system lets you control MCP tools at three levels of granularity across **Allow**, **Ask**, and **Deny** rules:

| Permission Pattern | Scope | Example |
| :--- | :--- | :--- |
| `mcp(server-name/tool-name)` | **Specific Tool** on a specific MCP server | `mcp(github/merge_pull_request)` |
| `mcp(server-name/*)` | **All Tools** on a specific MCP server | `mcp(postgres-readonly/*)` |
| `mcp(*)` | **All MCP Tools** across all connected servers | `mcp(*)` |

### Permission Evaluation Flow

```mermaid
flowchart TD
    Call["Agent calls MCP tool:<br/>github / merge_pull_request"] --> CheckSpecDeny{"Matches Specific Deny?<br/>mcp(github/merge_pull_request)"}
    CheckSpecDeny -->|Yes| Denied["❌ Hard Blocked (Deny)"]
    CheckSpecDeny -->|No| CheckSpecAsk{"Matches Specific Ask?<br/>mcp(github/merge_pull_request)"}
    CheckSpecAsk -->|Yes| Prompt["⚠️ Prompt User for Confirmation (Ask)"]
    CheckSpecAsk -->|No| CheckSpecAllow{"Matches Specific Allow?<br/>mcp(github/get_pull_request)"}
    CheckSpecAllow -->|Yes| Allowed["✅ Auto-Executed (Allow)"]
    CheckSpecAllow -->|No| CheckServer["Evaluate Server Wildcard<br/>mcp(github/*)"]
    CheckServer --> CheckGlobal["Evaluate Global Wildcard<br/>mcp(*)"]
    CheckGlobal --> DefaultPolicy["Fallback to Default Tool Execution Policy"]

    style Call fill:#e1f5fe,stroke:#0277bd,color:#000
    style Denied fill:#ffebee,stroke:#c62828,color:#000
    style Prompt fill:#fff3e0,stroke:#e65100,color:#000
    style Allowed fill:#e8f5e9,stroke:#2e7d32,color:#000
```

### Recommended Production Permission Strategy

Configure your Global or Project Permission Grants (**Settings > Agent Settings > Permission Grants** or `settings.json`) to auto-allow read operations, prompt on writes, and hard-deny destructive operations:

| Rule Tier | Permission Grants | Rationale |
| :--- | :--- | :--- |
| **Allow (Auto-Run)** | `mcp(context7/*)`<br/>`mcp(github/get_*)`<br/>`mcp(github/list_*)`<br/>`mcp(github/search_*)`<br/>`mcp(postgres-readonly/execute_sql)` | Read-only documentation, issue/PR lookups, and `SELECT`-only database queries are safe to run autonomously. |
| **Ask (Require Review)** | `mcp(github/create_pull_request)`<br/>`mcp(github/create_issue)`<br/>`mcp(slack/post_message)` | External mutations visible to teammates should be reviewed before execution. |
| **Deny (Hard Block)** | `mcp(github/delete_*)`<br/>`mcp(github/merge_pull_request)`<br/>`mcp(filesystem/delete_file)` | Destructive or irreversible external actions remain strictly human-only. |

> [!TIP]
> **Using `@` Mentions with MCP**: In the Antigravity Chat Canvas or CLI, type `@` to open the mention menu and select **MCP Servers / Tools** to attach specific MCP resources or explicitly direct the agent to use a connected server for your prompt.

---

## Subagent-Scoped MCP Servers

You can grant a custom subagent access to specific MCP servers via the `mcpServers` property in its `.agents/agents/<name>.md` frontmatter. This keeps specialized tool schemas out of the main agent's context window and isolates credentials to the specialist subagent that needs them:

```yaml
---
name: release-manager
description: Drafts release notes, inspects GitHub PRs, and posts release summaries to Slack.
tools:
  - view_file
  - grep_search
  - run_command
  - send_message
subagent: true
mainAgent: false
model: inherit
commandExecutionPolicy: sandbox
mcpServers:
  - github
  - slack
---

# System Prompt
You are the Release Manager subagent. Use the `github` MCP server to query merged PRs since the last tag, compile categorized release notes, and use `slack` MCP tools to post the draft to #releases.
```

---

## Python SDK MCP Integration (`McpStdioServer` & `McpStreamableHttpServer`)

When building autonomous agents with the **Google Antigravity Python SDK** (`google-antigravity`), you can attach both Stdio and Streamable HTTP MCP servers directly on `LocalAgentConfig`, filter exposed tools with `enabled_tools` / `disabled_tools`, and enforce overloaded safety policies via `google.antigravity.hooks.policy`:

```python
import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

# 1. Configure a local Stdio MCP server with tool allowlisting (saves context tokens!)
db_server = types.McpStdioServer(
    name="postgres_analytics",
    command="npx",
    args=["-y", "@bytebase/dbhub", "--dsn", os.environ["DATABASE_URL"]],
    enabled_tools=["execute_sql", "list_tables"],  # Mutually exclusive with disabled_tools
)

# 2. Configure a remote Streamable HTTP MCP server with custom headers
github_server = types.McpStreamableHttpServer(
    name="github",
    url="https://api.githubcopilot.com/mcp/",
    headers={"Authorization": f"Bearer {os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']}"},
    disabled_tools=["delete_branch", "merge_pull_request"],
)

async def confirm_write_tool(tool_call: types.ToolCall) -> bool:
    print(f"[Security Gate] Approve {tool_call.name}({tool_call.args})? [y/N]: ", end="")
    return input().strip().lower() == "y"

async def main():
    # 3. Combine deny-by-default policies with overloaded MCP server policy helpers
    config = LocalAgentConfig(
        mcp_servers=[db_server, github_server],
        policies=[
            policy.deny_all(),
            policy.allow("view_file"),
            policy.allow(db_server),  # Allows all enabled tools on db_server
            policy.allow(github_server, ["get_pull_request", "list_pull_requests"]),
            policy.ask_user(github_server, ["create_issue"], handler=confirm_write_tool),
        ],
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "Check open PRs on GitHub and cross-reference active user counts in postgres_analytics."
        )
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Managing & Troubleshooting MCP Servers (`/mcp` & Fix with Agent)

Antigravity includes built-in interactive tools to inspect, restart, and repair MCP connections without manual log-diving.

```mermaid
flowchart LR
    Error["MCP Server Connection Error<br/>(Red Status Indicator)"] --> Panel["Open /mcp or<br/>Additional Options (...) > MCP Servers"]
    Panel --> Action1["Click 'Restart'<br/>(Reloads process & re-reads env vars)"]
    Panel --> Action2["Click 'Fix with Agent'<br/>(Launches automated diagnostic repair)"]
    Action2 --> Diag["Agent inspects stderr logs,<br/>mcp_config.json syntax & PATH"]
    Diag --> Fix["Fixes missing npx/uvx args, legacy /sse URL,<br/>or prompts for missing ~/.gemini/.env key"]
    Fix --> Healthy["🟢 Connected & Tools Registered"]

    style Error fill:#ffebee,stroke:#c62828,color:#000
    style Panel fill:#e1f5fe,stroke:#0277bd,color:#000
    style Action2 fill:#f3e5f5,stroke:#6a1b9a,color:#000
    style Healthy fill:#e8f5e9,stroke:#2e7d32,color:#000
```

### 1. The `/mcp` Command & MCP Servers Panel

- **In Antigravity CLI (`agy`) or Chat**: Type `/mcp` to view all configured MCP servers, their connection state (`Connected`, `Disconnected`, `Error`), and the exact list of discovered tools per server.
- **In Antigravity App & IDE**: Navigate to **Additional Options (`...`) > MCP Servers** (or **Skills & Customizations > MCP Servers** in the left sidebar).

### 2. One-Click **Restart** & **Fix with Agent**

When an MCP server fails to start or loses connection:
- **Restart**: Terminates the hung child process or closes the stale HTTP session, re-interpolates `${VAR}` environment variables, and re-runs `initialize` / `tools/list`.
- **Fix with Agent**: One-click button in the MCP panel that hands the server's configuration block and `stderr` crash trace directly to Antigravity. The agent automatically diagnoses common issues:
  - Converting an unsupported legacy `/sse` URL to `/mcp` or wrapping it with `npx -y mcp-remote`.
  - Adding `-y` to `npx` commands so the process doesn't hang waiting for interactive install confirmation on `stdin`.
  - Resolving `command not found: npx` when Node.js is installed under `nvm`/`fnm`/`volta` by resolving the binary path or environment.
  - Identifying unset `${VAR}` tokens in `~/.gemini/.env`.

### Common Troubleshooting Reference

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| Server hangs indefinitely on startup | `npx` is waiting for interactive `[y/n]` package installation prompt | Always pass `"-y"` as the first argument in `"args": ["-y", "@scope/pkg"]` |
| `401 Unauthorized` or `403 Forbidden` | Unset `${VAR}` or trailing newline in token | Verify variable name in `~/.gemini/.env` matches `${VAR}` in `mcp_config.json` and click **Restart** |
| `404 Not Found` or `Unsupported SSE transport` | URL points to legacy `/sse` endpoint | Change endpoint to `/mcp` (Streamable HTTP) or wrap with `npx -y mcp-remote <url>` |
| Server connects but shows `0 tools` | Missing required CLI flag (e.g., `--dsn` or allowed directory path) | Click **Fix with Agent** in the MCP panel to inspect the server's startup stderr output |

---

## Security Best Practices

### Do's ✅
- **Use `${VAR}` Interpolation Everywhere**: Keep `~/.gemini/config/mcp_config.json` and plugin `mcp_config.json` files 100% free of literal credentials so configs can be shared safely.
- **Use Read-Only Database Roles**: When connecting PostgreSQL or MySQL via `@bytebase/dbhub`, connect with a database role granted `SELECT` only, and pair it with `readonly = true` in `dbhub.toml`.
- **Scope Filesystem Paths**: Never mount `/` or `~` into `@modelcontextprotocol/server-filesystem`; pass only the specific directories required.
- **Combine Permissions with `PreToolUse` Hooks**: As shown in [Module 06: Hooks](../06-hooks/README.md), you can intercept `mcp_<server>_<tool>` calls in `.agents/hooks.json` for custom payload validation and audit logging.

### Don'ts ❌
- **Don't Hardcode Secrets in `mcp_config.json`**: Even in `~/.gemini/config/mcp_config.json`, prefer `${VAR}` backed by `~/.gemini/.env` (`0600` permissions).
- **Don't Auto-Approve Destructive MCP Tools**: Never grant `Allow` on `mcp(*)` when connected to production databases or repository administration servers.

---

## Ready-to-Use `mcp_config.json` Templates in This Folder

This directory contains **4 copy-pasteable `mcp_config.json` templates** ready for `~/.gemini/config/mcp_config.json` or plugin bundles:

| File | Servers Included | Transport Types Demonstrated | Purpose |
| :--- | :--- | :--- | :--- |
| [`github-mcp.json`](./github-mcp.json) | `github`, `github-stdio` | Streamable HTTP (`url` + `headers` with `${VAR}`) & Stdio (`npx`) | PR reviews, issue triage, code search, and commit inspection |
| [`database-mcp.json`](./database-mcp.json) | `postgres-readonly`, `postgres-dev`, `sqlite-local` | Stdio (`@bytebase/dbhub` & `uvx mcp-server-sqlite`) | Safe read-only production analytics + local dev/SQLite database inspection |
| [`filesystem-mcp.json`](./filesystem-mcp.json) | `filesystem-scoped`, `git-repo` | Stdio (`@modelcontextprotocol/server-filesystem` & `uvx mcp-server-git`) | Sandboxed multi-directory file access and structured Git repository operations |
| [`multi-mcp.json`](./multi-mcp.json) | `github`, `postgres`, `sentry`, `slack`, `context7` | Hybrid Streamable HTTP + Stdio + `mcp-remote` | Complete full-stack engineering setup combining code, DB, error telemetry, chat, and live library docs |

---

## Installation Instructions

### Step 1: Copy a Template to `~/.gemini/config/mcp_config.json`

```bash
# Ensure global config directory exists
mkdir -p ~/.gemini/config

# Copy the full-stack multi-server template (or merge into your existing mcp_config.json)
cp /path/to/gemini-howto/05-mcp/multi-mcp.json ~/.gemini/config/mcp_config.json
```

### Step 2: Configure Secrets in `~/.gemini/.env`

```bash
touch ~/.gemini/.env
chmod 600 ~/.gemini/.env

# Add your tokens (replace placeholders with real values)
cat >> ~/.gemini/.env << 'EOF'
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://readonly:password@localhost:5432/mydb
SENTRY_AUTH_TOKEN=sntrys_xxxxxxxxxxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx
SLACK_TEAM_ID=T0123456789
EOF
```

### Step 3: Verify & Manage in Antigravity

Open Antigravity or `agy` CLI and run:

```text
/mcp
```

Verify all configured servers show a green **Connected** badge and non-zero tool counts. If any server needs adjustment, click **Fix with Agent** in the MCP panel.

---

## Related Concepts

- **[Module 03: Skills](../03-skills/README.md)** — Pair MCP servers with a `SKILL.md` that teaches the agent *how* and *when* to query your custom MCP tools
- **[Module 04: Subagents](../04-subagents/README.md)** — Scope MCP servers to specialized background subagents via `mcpServers:` frontmatter
- **[Module 06: Hooks](../06-hooks/README.md)** — Audit, gate, or rewrite `mcp_<server>_<tool>` calls using `PreToolUse` and `PostToolUse` hooks
- **[Module 07: Plugins](../07-plugins/README.md)** — Bundle `mcp_config.json` alongside skills, agents, and rules in a single installable plugin

---

<p align="center">
  <a href="../04-subagents/README.md">← Previous: Module 04 - Subagents</a> | <a href="../README.md">Home</a> | <a href="../06-hooks/README.md">Next: Module 06 - Hooks →</a>
</p>

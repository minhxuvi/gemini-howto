<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/gemini-howto-logo-dark.svg">
  <img alt="Gemini & Antigravity How To" src="../resources/logos/gemini-howto-logo.svg">
</picture>

# Module 06: Lifecycle Hooks (`hooks.json`) — Complete Reference Guide

Lifecycle hooks allow you to execute deterministic shell scripts or Python programs at **6 key points** during Google Antigravity's execution loop. Unlike rules or prompts (which rely on the model choosing to follow instructions), hooks enforce **hard programmatic guarantees**: blocking destructive commands, scanning file edits for leaked secrets, auto-formatting generated code, injecting live Git context at session startup, and preventing the agent from stopping until tests pass.

## Table of Contents

1. [Overview](#overview)
2. [The 6 Lifecycle Events & Agent Loop Architecture](#the-6-lifecycle-events--agent-loop-architecture)
3. [Discovery Locations & Multi-Level Merging](#discovery-locations--multi-level-merging)
4. [`hooks.json` Configuration Schema](#hooksjson-configuration-schema)
5. [Supported Tool Names for Matchers](#supported-tool-names-for-matchers)
6. [JSON Stdin / Stdout Contract (camelCase)](#json-stdin--stdout-contract-camelcase)
7. [`PreToolUse` Decision Precedence Pyramid & Argument Rewriting (`overwrite`)](#pretooluse-decision-precedence-pyramid--argument-rewriting-overwrite)
8. [`Stop` Gate Verification Loop (`fullyIdle`)](#stop-gate-verification-loop-fullyidle)
9. [Python SDK Declarative Policies & Lifecycle Hooks](#python-sdk-declarative-policies--lifecycle-hooks)
10. [Ready-to-Use Hook Scripts in This Folder](#ready-to-use-hook-scripts-in-this-folder)
11. [Managing, Testing & Debugging Hooks (`/hooks`)](#managing-testing--debugging-hooks-hooks)
12. [Security Best Practices](#security-best-practices)
13. [Installation Instructions](#installation-instructions)
14. [Related Concepts](#related-concepts)

---

## Overview

Hooks bridge Antigravity's reasoning loop with your local engineering toolchain:

- **Deterministic Guardrails (`PreToolUse`)**: Inspect every proposed tool call before it executes. Allow, prompt (`ask` / `force_ask`), hard-deny (`deny`), or transparently rewrite tool arguments on the fly via `"overwrite"`.
- **Automated Post-Processing (`PostToolUse`)**: Automatically run `prettier`, `ruff`, or `gofmt` whenever `write_to_file`, `replace_file_content`, or `multi_replace_file_content` modifies a file, and record tamper-evident audit logs.
- **Dynamic Trajectory Injection (`SessionStart`, `PreInvocation`, `PostInvocation`)**: Inject persistent `systemMessage` or transient `ephemeralMessage` steps into the conversation without cluttering static `GEMINI.md` files.
- **Autonomous Completion Gates (`Stop`)**: Verify that tests compile and pass when `fullyIdle` is `true` — returning `{"decision": "continue", "reason": "..."}` to force the agent back into the loop until quality gates succeed.

---

## The 6 Lifecycle Events & Agent Loop Architecture

Antigravity fires 6 distinct lifecycle events across the session, model invocation, and tool execution loops:

```mermaid
flowchart TB
    Start(["New Conversation Starts"]) --> SS["1. SessionStart Hook<br/>(Flat handler array — runs once)<br/>Can inject startup systemMessage"]
    SS --> PreInv["2. PreInvocation Hook<br/>(Flat handler array — before model call)<br/>Can inject ephemeralMessage / systemMessage"]
    PreInv --> Model["Gemini Model Invocation<br/>(Generates thoughts, text, or tool calls)"]
    Model --> PostInv["3. PostInvocation Hook<br/>(Flat handler array — after model call)<br/>Can inject steps or set terminationBehavior"]

    PostInv --> HasTools{"Did model emit<br/>tool calls?"}
    HasTools -->|"Yes (for each tool call)"| PreTool["4. PreToolUse Hook<br/>(Grouped by 'matcher' regex)<br/>Returns decision: allow | deny | ask | force_ask<br/>Optional: overwrite args & permissionOverrides"]
    
    PreTool -->|"decision == 'deny'"| Blocked["Tool Blocked<br/>Reason returned to Agent"]
    PreTool -->|"decision == 'allow' / approved"| ExecTool["Execute Tool<br/>(With overwritten args if specified)"]
    ExecTool --> PostTool["5. PostToolUse Hook<br/>(Grouped by 'matcher' regex)<br/>Auto-format, lint, or audit log"]
    
    Blocked --> PreInv
    PostTool --> PreInv

    HasTools -->|"No tool calls (or loop ending)"| StopHook["6. Stop Hook<br/>(Flat handler array — checks fullyIdle)<br/>Returns decision: allow | continue"]
    StopHook -->|"decision == 'continue'<br/>(Injects reason as systemMessage)"| PreInv
    StopHook -->|"decision == 'allow'"| Idle(["Agent Turn Complete (Idle)"])

    style SS fill:#e1f5fe,stroke:#0277bd,color:#000
    style PreInv fill:#e1f5fe,stroke:#0277bd,color:#000
    style PostInv fill:#e1f5fe,stroke:#0277bd,color:#000
    style PreTool fill:#fff3e0,stroke:#e65100,color:#000
    style PostTool fill:#f3e5f5,stroke:#6a1b9a,color:#000
    style StopHook fill:#e8f5e9,stroke:#2e7d32,color:#000
    style Blocked fill:#ffebee,stroke:#c62828,color:#000
```

### Event Summary Table

| Event | When It Fires | Structure in `hooks.json` | Matcher Target | Primary Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **`SessionStart`** | Once when a new conversation session starts, before the first model call | **Flat** (array of handler objects directly under `SessionStart`) | N/A *(ignored)* | Inject initial workspace/Git status via `injectSteps` |
| **`PreInvocation`** | Before Antigravity calls the Gemini model on each turn | **Flat** (array of handler objects) | N/A *(ignored)* | Track context growth, inject transient `ephemeralMessage` reminders |
| **`PreToolUse`** | Immediately before a tool step executes | **Grouped** (`matcher` regex + `hooks` array) | Tool name *(e.g., `run_command`)* | Gate execution (`allow`, `deny`, `ask`, `force_ask`), rewrite inputs (`overwrite`) |
| **`PostToolUse`** | Immediately after a tool step completes (or errors) | **Grouped** (`matcher` regex + `hooks` array) | Tool name *(e.g., `write_to_file`)* | Run code formatters (`prettier`, `ruff`), write audit logs |
| **`PostInvocation`** | Immediately after each model invocation finishes | **Flat** (array of handler objects) | N/A *(ignored)* | Inspect trajectory, inject steps, or set `terminationBehavior` (`force_continue` / `terminate`) |
| **`Stop`** | When the agent execution loop is about to terminate / go idle | **Flat** (array of handler objects) | N/A *(ignored)* | Run build/test verification gates; return `"decision": "continue"` to block stopping |

---

## Discovery Locations & Multi-Level Merging

Antigravity discovers `hooks.json` files across three scopes:

| Scope | File Location | UI Management Surface |
| :--- | :--- | :--- |
| **1. Workspace** | `.agents/hooks.json` *(at project root)* | Shared with team via Git |
| **2. Global User** | `~/.gemini/config/hooks.json` *(or inside `~/.gemini/antigravity-cli/settings.json` for CLI)* | **App**: `Settings > Customizations > Hooks`<br/>**IDE**: `... > Customizations > Hooks`<br/>**CLI**: `/hooks` |
| **3. Plugin** | `<plugin-root>/hooks.json` | Active whenever the plugin is enabled |

### Merging & Precedence Behavior

- **All Matching Hooks Execute**: Unlike skills (where workspace overrides global by name), **all** enabled hooks across Workspace, Global, and Plugin `hooks.json` files that match an event are merged and executed sequentially.
- **Most Restrictive Decision Wins (`PreToolUse`)**: When multiple `PreToolUse` hooks evaluate the same tool call, the most restrictive decision takes precedence (`"deny"` overrides `"ask"`, which overrides `"allow"`).
- **Working Directory**: Hook commands execute via `sh -c` on macOS/Linux (`cmd /c` on Windows) with the working directory set to the directory containing the `hooks.json` file (or workspace root), and `~` is automatically expanded.

---

## `hooks.json` Configuration Schema

The `hooks.json` file is a top-level JSON object where each key is a descriptive **hook group name** mapping to its lifecycle event handlers and an optional `"enabled"` boolean:

```json
{
  "command-safety-guard": {
    "enabled": true,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/pre-tool-check.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "auto-formatter": {
    "enabled": true,
    "PostToolUse": [
      {
        "matcher": "write_to_file|replace_file_content|multi_replace_file_content",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/format-code.sh",
            "timeout": 15
          }
        ]
      }
    ]
  },
  "workspace-session-init": {
    "enabled": true,
    "SessionStart": [
      {
        "type": "command",
        "command": "./.agents/hooks/session-init.sh",
        "timeout": 10
      }
    ]
  }
}
```

### Structural Difference: Grouped vs. Flat Events

> [!IMPORTANT]
> Notice the structural difference between tool events and invocation/session events:
> - **`PreToolUse` and `PostToolUse` (Grouped)**: Each array item is a matcher group containing `"matcher": "<regex>"` and `"hooks": [ { "type": "command", "command": "...", "timeout": 30 } ]`.
> - **`SessionStart`, `PreInvocation`, `PostInvocation`, and `Stop` (Flat)**: Each array item is a handler object directly (`{ "type": "command", "command": "...", "timeout": 30 }`) without a `matcher` wrapper.

---

## Supported Tool Names for Matchers

In `PreToolUse` and `PostToolUse`, the `"matcher"` field is evaluated as a regular expression against the Antigravity tool name:

| Category | Tool Name | Key Arguments in `toolCall.args` / `toolInput` |
| :--- | :--- | :--- |
| **Command Execution** | `run_command` | `CommandLine`, `Cwd`, `WaitMsBeforeAsync`, `RunPersistent`, `RequestedTerminalID` |
| **File Creation & Edits** | `write_to_file` | `TargetFile`, `Overwrite`, `CodeContent`, `Description`, `ArtifactMetadata` |
| | `replace_file_content` | `TargetFile`, `StartLine`, `EndLine`, `TargetContent`, `ReplacementContent`, `AllowMultiple` |
| | `multi_replace_file_content` | `TargetFile`, `ReplacementChunks` (array of `{StartLine, EndLine, TargetContent, ReplacementContent}`) |
| **File Reading & Search** | `view_file` | `AbsolutePath`, `StartLine`, `EndLine` |
| | `grep_search` | `SearchPath`, `Query`, `IsRegex`, `CaseInsensitive`, `Includes` |
| | `find_by_name` | `SearchDirectory`, `Pattern`, `Type`, `Extensions`, `Excludes` |
| | `list_dir` | `DirectoryPath` |
| **Web & Research** | `read_url_content` | `Url` |
| | `search_web` | `query`, `domain` |
| **Subagents & Tasks** | `invoke_subagent` | `Subagents` (array of `{TypeName, Role, Prompt, Model, Workspace}`) |
| | `define_subagent` | `name`, `description`, `system_prompt`, `enable_write_tools`, `enable_mcp_tools` |
| | `send_message` | `Recipient`, `Message` |
| | `manage_subagents` | `Action` (`list`, `kill`, `kill_all`), `ConversationIds` |
| | `manage_task` | `Action` (`list`, `kill`, `status`, `send_input`), `TaskId` |
| | `schedule` | `DurationSeconds`, `CronExpression`, `Prompt`, `TimerCondition` |
| **MCP Tools** | `mcp_<server>_<tool>` | Server-specific tool arguments (match all tools on a server via `"mcp_github_.*"`) |
| **Match All Tools** | `".*"` or `"*"` or `""` | Matches every tool execution |

---

## JSON Stdin / Stdout Contract (camelCase)

All hook scripts communicate with Antigravity by reading a JSON object from **`stdin`** and printing a single valid JSON object to **`stdout`**.

> [!IMPORTANT]
> **All JSON keys use `camelCase`** (protojson encoding), such as `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, and `modelName`.

### Common Stdin Fields (Present on ALL 6 Events)

```json
{
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/Users/yourname/Projects/my-app"],
  "transcriptPath": "/Users/yourname/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "/Users/yourname/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-pro"
}
```

> [!NOTE]
> The `<app_data_dir>` base directory in `transcriptPath` and `artifactDirectoryPath` reflects the active Antigravity surface:
> - **Antigravity 2.0 App**: `~/.gemini/antigravity`
> - **Antigravity CLI (`agy`)**: `~/.gemini/antigravity-cli`
> - **Antigravity IDE**: `~/.gemini/antigravity-ide`

---

### 1. `SessionStart` Stdin & Stdout

- **Stdin**: Common fields (`conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`).
- **Stdout**: Optional `injectSteps` array to inject startup context before the first model turn.

```json
{
  "injectSteps": [
    {
      "systemMessage": {
        "systemMessage": "Active Git branch: feat/oauth-pkce (2 uncommitted files). Node v22.14.0."
      }
    }
  ]
}
```

---

### 2. `PreInvocation` Stdin & Stdout

- **Stdin**: Common fields + `invocationNum` (0-based integer) + `initialNumSteps` (number of steps currently in trajectory).
- **Stdout**: Optional `injectSteps` array. Supported step objects inside `injectSteps`:
  - `{"systemMessage": {"systemMessage": "...", "metadata": {...}}}` — Persists in the conversation trajectory across turns (note the nested `systemMessage` object!).
  - `{"ephemeralMessage": "..."}` — Transient hint injected for the current turn only and dropped afterward so it never bloats the transcript.
  - `{"userMessage": "..."}` — Injected user message string.

```json
{
  "injectSteps": [
    {
      "ephemeralMessage": "Context window is at 78% capacity (~140 steps). Consider summarizing findings into an artifact or recommending /compact."
    }
  ]
}
```

---

### 3. `PreToolUse` Stdin & Stdout

- **Stdin**: Common fields + `stepIdx` (integer) + tool call details (`toolCall.name` & `toolCall.args`, or `toolName` & `toolInput`):

```json
{
  "toolCall": {
    "name": "run_command",
    "args": {
      "CommandLine": "grep -rn 'TODO' src/",
      "Cwd": "/Users/yourname/Projects/my-app",
      "WaitMsBeforeAsync": 5000
    }
  },
  "toolName": "run_command",
  "toolInput": {
    "CommandLine": "grep -rn 'TODO' src/",
    "Cwd": "/Users/yourname/Projects/my-app",
    "WaitMsBeforeAsync": 5000
  },
  "stepIdx": 12,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/Users/yourname/Projects/my-app"],
  "transcriptPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-pro"
}
```

- **Stdout**:

```json
{
  "decision": "allow",
  "reason": "Rewrote grep to ripgrep (rg) for faster workspace search.",
  "overwrite": {
    "CommandLine": "rg -n 'TODO' src/"
  },
  "permissionOverrides": ["command(rg -n 'TODO' src/)"]
}
```

---

### 4. `PostToolUse` Stdin & Stdout

- **Stdin**: Common fields + `stepIdx` + `toolCall` (`name`, `args`) / `toolName` / `toolInput` + `toolOutput` (string) + `error` / `toolError` (string, non-empty if the tool failed).
- **Stdout**: Must return an empty JSON object `{}`.

---

### 5. `PostInvocation` Stdin & Stdout

- **Stdin**: Common fields + `invocationNum` + `initialNumSteps`.
- **Stdout**:

```json
{
  "injectSteps": [],
  "terminationBehavior": ""
}
```

Valid `terminationBehavior` values:
- `"force_continue"`: Forces the agent loop to continue for another invocation.
- `"terminate"`: Forces the execution loop to stop immediately.
- `""` *(or omitted)*: Default agent loop behavior.

---

### 6. `Stop` Stdin & Stdout

- **Stdin**: Common fields + `executionNum` (integer) + `terminationReason` (string, e.g., `"NO_TOOL_CALL"` / `"model_stop"`, `"MAX_INVOCATIONS"`, `"ERROR"`, `"USER_CANCELED"`) + `error` (string) + `fullyIdle` (boolean — `true` only when all background tasks and subagents have finished).
- **Stdout**:
  - To **block stopping** and force the agent to fix an issue:
    ```json
    {
      "decision": "continue",
      "reason": "Verification failed: 2 unit tests in tests/auth.test.ts are failing. Fix them before finishing."
    }
    ```
  - To **allow stopping**:
    ```json
    {
      "decision": "allow"
    }
    ```

---

## `PreToolUse` Decision Precedence Pyramid & Argument Rewriting (`overwrite`)

### Decision Precedence Order

When `PreToolUse` hooks return a `"decision"`, Antigravity supports 6 decision levels ordered from **most restrictive** to **least restrictive**. When multiple hooks match the same tool call, the highest-priority (most restrictive) decision wins:

```mermaid
flowchart TB
    D1["1. 'deny' (Highest Priority)<br/>Hard blocks tool execution immediately; returns 'reason' to the agent"]
    D2["2. 'force_ask'<br/>Always prompts the user for interactive confirmation, ignoring cached 'Always Allow' grants"]
    D3["3. 'ask'<br/>Prompts the user for confirmation, respecting cached 'Always Allow' grants"]
    D4["4. 'deny_unless_prior_grant'<br/>Denies execution unless the resource was already approved in a prior session grant"]
    D5["5. 'allow'<br/>Approves the tool call in this hook, delegating to the next hook or default policy"]
    D6["6. 'auto_approve' (Lowest Priority)<br/>Automatically approves when the default policy would otherwise prompt, while honoring explicit user deny rules"]

    D1 --> D2 --> D3 --> D4 --> D5 --> D6

    style D1 fill:#ffebee,stroke:#c62828,color:#000
    style D2 fill:#fbe9e7,stroke:#d84315,color:#000
    style D3 fill:#fff3e0,stroke:#e65100,color:#000
    style D4 fill:#fff8e1,stroke:#f57f17,color:#000
    style D5 fill:#e8f5e9,stroke:#2e7d32,color:#000
    style D6 fill:#e1f5fe,stroke:#0277bd,color:#000
```

### Transparent Argument Rewriting (`overwrite`)

The `"overwrite"` field in a `PreToolUse` stdout payload performs a **shallow, top-level merge** into the tool call's arguments before execution:
- Each key in `"overwrite"` replaces the corresponding top-level argument key (e.g., `"CommandLine"` on `run_command` or `"TargetFile"` on `write_to_file`).
- The modified tool call is what actually executes on disk/shell.
- Antigravity automatically prepends a notice to the tool output informing the agent which argument keys were rewritten by the hook so the model stays in sync.

---

## `Stop` Gate Verification Loop (`fullyIdle`)

A `Stop` hook acts as an automated quality gate at the end of an agent turn. Because Antigravity supports asynchronous background commands and subagents, always inspect `"fullyIdle"` before running heavy verification checks:

```mermaid
sequenceDiagram
    participant Agent as Antigravity Agent
    participant Runtime as Execution Loop
    participant StopHook as goal-gate.sh (Stop Hook)
    participant TestSuite as Build & Test Runner

    Agent->>Runtime: Finishes response (NO_TOOL_CALL)
    Runtime->>StopHook: stdin: { fullyIdle: true, terminationReason: "NO_TOOL_CALL", ... }
    StopHook->>StopHook: Check fullyIdle == true & terminationReason != "USER_CANCELED"
    StopHook->>TestSuite: Run npm test / pytest / go test
    alt Tests Fail (Exit != 0)
        TestSuite-->>StopHook: 1 failing test in auth.spec.ts
        StopHook-->>Runtime: stdout: { "decision": "continue", "reason": "Tests failed: ..." }
        Runtime->>Agent: Injects reason as systemMessage & resumes loop!
        Agent->>Agent: Fixes bug in auth.ts & re-runs test
    else Tests Pass (Exit == 0)
        TestSuite-->>StopHook: All tests pass!
        StopHook-->>Runtime: stdout: { "decision": "allow" }
        Runtime->>Agent: Enters Idle state
    end
```

> [!TIP]
> **Prevent Infinite Continuation Loops**: Always allow stopping if `terminationReason` is `"USER_CANCELED"`, `"ERROR"`, `"MAX_INVOCATIONS"`, or `"MAX_FORCED_INVOCATIONS"`, or if `fullyIdle` is `false` (meaning the agent is legitimately waiting on a background task or subagent wakeup).

---

## Python SDK Declarative Policies & Lifecycle Hooks

When using the **Google Antigravity Python SDK** (`google-antigravity`), you can combine declarative policies (`from google.antigravity.hooks.policy import allow, deny, ask_user`) with async decorator hooks (`@hooks.pre_tool_call_decide`, `@hooks.stop`, etc.):

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig, types
from google.antigravity.hooks import hooks, policy
from google.antigravity.hooks.policy import allow, deny

# 1. Declarative Policy Rules (9-tier precedence: Specific Deny > Specific Ask > Specific Allow > Wildcards)
security_policies = [
    deny(
        "run_command",
        when=lambda args: "rm -rf" in args.get("CommandLine", "")
        or "git push --force" in args.get("CommandLine", ""),
        name="block_destructive_shell",
    ),
    allow("view_file"),
    allow("grep_search"),
    allow("run_command"),
]

# 2. Programmatic Lifecycle Hook Decorators
@hooks.pre_tool_call_decide
async def audit_tool_call(call: types.ToolCall) -> types.HookResult:
    print(f"[Audit] Tool={call.name} Args={call.args}")
    return types.HookResult(allow=True)

@hooks.stop
async def enforce_summary_on_stop(data: types.StopArgs) -> types.StopHookResult:
    # Require a verification summary on the first stop attempt
    if data.continuation_count == 0 and "verified" not in data.response_text.lower():
        return types.StopHookResult(
            decision=types.StopDecision.CONTINUE,
            reason="Before finishing, run the test suite and include a 'Verified' section in your response.",
        )
    return types.StopHookResult(decision=types.StopDecision.ALLOW_STOP)

async def main():
    config = LocalAgentConfig(
        capabilities=CapabilitiesConfig(),
        policies=security_policies,
        hooks=[audit_tool_call, enforce_summary_on_stop],
    )
    async with Agent(config) as agent:
        response = await agent.chat("Refactor utils.py and verify all tests pass.")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Ready-to-Use Hook Scripts in This Folder

This directory contains a complete [`hooks.json`](./hooks.json) configuration file and **8 executable hook scripts** (`chmod +x`) covering all 6 lifecycle events:

| Script | Lifecycle Event | Matcher | What It Does |
| :--- | :--- | :--- | :--- |
| [`pre-tool-check.sh`](./pre-tool-check.sh) | `PreToolUse` | `run_command` | Blocks destructive commands (`rm -rf /`, `git push --force` to `main`/`master`, `DROP TABLE`), prompts (`force_ask`) on `git reset --hard`, and rewrites `grep` to `rg` via `"overwrite"` |
| [`security-scan.sh`](./security-scan.sh) | `PreToolUse` | `write_to_file\|replace_file_content\|multi_replace_file_content` | Scans `CodeContent`, `ReplacementContent`, and `ReplacementChunks` for hardcoded AWS keys (`AKIA...`), GitHub PATs (`ghp_...`), Google API keys (`AIza...`), and private keys before they touch disk |
| [`pre-commit.sh`](./pre-commit.sh) | `PreToolUse` | `run_command` | Intercepts `git commit` commands and runs project linters/tests first; returns `"decision": "deny"` with compiler output if checks fail |
| [`format-code.sh`](./format-code.sh) | `PostToolUse` | `write_to_file\|replace_file_content\|multi_replace_file_content` | Automatically runs `prettier`, `ruff`/`black`, `gofmt`, or `rustfmt` on `TargetFile` immediately after any file edit |
| [`log-commands.sh`](./log-commands.sh) | `PostToolUse` | `.*` | Appends structured JSON Lines audit records (`timestamp`, `conversationId`, `modelName`, `toolName`, `stepIdx`, `error`) to `.agents/audit.log` |
| [`session-init.sh`](./session-init.sh) | `SessionStart` | *(Flat)* | Inspects current Git branch, dirty file count, recent commits, and Node/Python runtime versions, injecting a startup `systemMessage` |
| [`context-tracker.py`](./context-tracker.py) | `PreInvocation` | *(Flat)* | Inspects `transcriptPath` file size and `initialNumSteps`; injects a transient `ephemeralMessage` advising `/compact` or artifact checkpointing when context grows large |
| [`goal-gate.sh`](./goal-gate.sh) | `Stop` | *(Flat)* | Checks `fullyIdle == true` and runs test/build verification; returns `{"decision": "continue", "reason": "..."}` if tests are failing |

---

## Managing, Testing & Debugging Hooks (`/hooks`)

### 1. Inspecting Active Hooks

- **Antigravity CLI (`agy`)**: Run `/hooks` inside the TUI to list all loaded hooks across Workspace, Global, and Plugin scopes, their `enabled` status, and event bindings.
- **Antigravity App**: Open **Settings > Customizations > Hooks** to view and toggle individual hook groups on or off.
- **Antigravity IDE**: Open **`...` > Customizations > Hooks** in the agent side panel.

### 2. Testing Hooks Standalone in Your Terminal

Because hooks are standard executables that read JSON from `stdin` and write JSON to `stdout`, you can test every script in this folder directly from your terminal before enabling it:

```bash
# 1. Test blocking a destructive rm -rf command (expects "decision": "deny")
echo '{
  "toolCall": {
    "name": "run_command",
    "args": { "CommandLine": "rm -rf /" }
  },
  "conversationId": "test-123",
  "workspacePaths": ["/tmp"]
}' | ./06-hooks/pre-tool-check.sh

# 2. Test rewriting grep to rg via overwrite (expects "decision": "allow" + "overwrite")
echo '{
  "toolCall": {
    "name": "run_command",
    "args": { "CommandLine": "grep -rn TODO src/" }
  }
}' | ./06-hooks/pre-tool-check.sh

# 3. Test scanning a file edit for leaked AWS keys (expects "decision": "deny")
echo '{
  "toolCall": {
    "name": "write_to_file",
    "args": {
      "TargetFile": "/tmp/config.py",
      "CodeContent": "AWS_SECRET = \"AKIAIOSFODNN7EXAMPLE\""
    }
  }
}' | ./06-hooks/security-scan.sh

# 4. Test SessionStart environment injection
echo '{
  "conversationId": "test-123",
  "workspacePaths": ["'"$PWD"'"],
  "modelName": "gemini-3.6-pro"
}' | ./06-hooks/session-init.sh
```

---

## Security Best Practices

| Do ✅ | Don't ❌ |
| :--- | :--- |
| Parse `stdin` with a real JSON parser (`python3 -c "import sys, json..."` or `jq`) | Use fragile `sed`/`awk` regexes on raw JSON strings |
| Always output valid JSON on `stdout` (even `{}` on `PostToolUse`) | Print unstructured debug messages to `stdout` (send debug logs to `stderr` or a log file instead!) |
| Set a reasonable `"timeout"` (e.g., `10`–`30` seconds) on every hook | Run unbounded long-running builds inside synchronous `PreToolUse` hooks |
| Check `fullyIdle == true` in `Stop` hooks before running verification | Block `Stop` when `terminationReason == "USER_CANCELED"` |

---

## Installation Instructions

### Install to Your Project Workspace (`.agents/hooks.json`)

```bash
# 1. Create the workspace .agents/hooks directory
mkdir -p .agents/hooks

# 2. Copy all executable hook scripts and ensure +x permissions
cp /path/to/gemini-howto/06-hooks/*.sh /path/to/gemini-howto/06-hooks/*.py .agents/hooks/
chmod +x .agents/hooks/*.sh .agents/hooks/*.py

# 3. Copy the hooks.json configuration to .agents/hooks.json
cp /path/to/gemini-howto/06-hooks/hooks.json .agents/hooks.json
```

---

## Related Concepts

- **[Module 01: Slash Commands](../01-slash-commands/README.md)** — Use `/hooks` to inspect loaded hooks and `/compact` when `context-tracker.py` alerts you
- **[Module 02: Rules & Memory](../02-memory-and-rules/README.md)** — Pair soft guidance in `GEMINI.md` with hard enforcement in `hooks.json`
- **[Module 04: Subagents](../04-subagents/README.md)** — Gate or log `invoke_subagent` calls with `PreToolUse` and `PostToolUse`
- **[Module 05: MCP](../05-mcp/README.md)** — Match `mcp_<server>_<tool>` calls in `PreToolUse` for custom MCP payload auditing
- **[Module 07: Plugins](../07-plugins/README.md)** — Package `hooks.json` inside reusable plugins

---

<p align="center">
  <a href="../05-mcp/README.md">← Previous: Module 05 - MCP</a> | <a href="../README.md">Home</a> | <a href="../07-plugins/README.md">Next: Module 07 - Plugins →</a>
</p>

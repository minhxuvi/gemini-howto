# Checkpoints, Session Forking, `/diff` & Git Worktree Playbooks

Practical workflows for time-traveling across conversation states, branching experiments with `/fork`, inspecting code changes with `/diff`, and isolating parallel work in Git worktrees.

---

## Playbook 1: Conversation-Only Undo vs. Full Code Rewind

### Scenario A: Keep the Code Edits, Rewind the Conversation Context
You asked the agent to implement a new database migration AND write 15 verbose debugging scripts. The migration file on disk is perfect, but the 15 debugging turns polluted the context window.

1. **In the Antigravity App**:
   - Hover over the turn right after the migration was written and click **Undo / Revert**.
   - In the **Confirm Undo** dialog (`v2.19.1+`), check **Revert only the conversation**.
   - Click **Confirm**. Your migration file stays on disk untouched, while the noisy debugging turns are removed from the conversation history!
2. **Alternative — On-Demand Compaction (`/compact`)**:
   - If you want to keep a concise summary of those turns instead of rewinding them, run `/compact` (`v2.24.0+` / CLI `v1.3.5+`) to summarize the history in place and free up context tokens.

### Scenario B: Revert Both Files and Conversation (`/rewind`)
You asked the agent to refactor an authentication module, and the test suite now fails across 12 files.

```text
# Inside Antigravity CLI (agy)
> /rewind
```
1. The interactive **Rewind Timeline** opens, showing each user prompt with its relative timestamp (`2m ago`, `14m ago`) and modified file count.
2. Press `↑` / `↓` to select the prompt before the refactor began and press `Enter`.
3. Both the workspace files on disk and the conversation history are restored to that exact snapshot.

---

## Playbook 2: Parallel Architecture Exploration with `/fork`

Suppose you have an active session where the agent has already mapped out your API bottlenecks. You want to benchmark **Approach A (Redis Streams)** against **Approach B (In-Process Ring Buffer)** without losing the shared investigation context.

```text
# Session 1 (Original Thread)
> Analyze our ingestion pipeline in src/ingest/ and identify the top 3 latency bottlenecks.
[Agent completes analysis at Step 8]

# Clone the session at Step 8 into a new independent thread
> /fork
Forked conversation created (ID: 9b4e1c20-...). Switched to forked session.

# In the Forked Session: implement Approach B
> Implement the lock-free in-process ring buffer approach and run the benchmark suite.

# Switch back to the Original Session anytime via /resume
> /resume
```

---

## Playbook 3: Mastering the Interactive `/diff` Viewer

Run `/diff` at any time in `agy` to review uncommitted work, turn-by-turn agent edits, or the last 100 repository commits (`v1.4.0+`):

| Keybinding | View | Action |
| :--- | :--- | :--- |
| `Tab` / `Shift+Tab` | All Views | Cycle between **Uncommitted Changes**, **Turns**, and **Commit Tree** (100 commits) |
| `j` / `k` or `↑` / `↓` | File Diff | Move cursor line-by-line (`v1.3.0+`) |
| `←` / `→` | File Diff | Open previous / next changed file at its first modified hunk (`v1.3.1+`) |
| `n` / `N` | File Diff | Jump to next / previous change hunk across all changed files (`v1.3.1+`) |
| `Ctrl+O` | File Diff | Expand or collapse folded unchanged lines nearest the cursor (`v1.3.5+`) |
| `f` | File Diff | Toggle between **Changes Only** and **Whole File** view (`v1.3.5+`) |
| `Enter` | Commit Tree | Open the highlighted commit's full diff (`v1.4.0+`) |

---

## Playbook 4: Git Worktree Isolation (App & Subagents)

### 1. Starting a Worktree Thread in the Antigravity App
When starting a new conversation inside a Git-backed Project:
1. In the prompt composer bar, switch the target toggle from **`Local`** to **`Worktree`**.
2. Send your prompt (e.g., `"Upgrade React Router v6 to v7 across all routes"`).
3. Antigravity creates a fresh Git worktree branch automatically so your main working directory remains clean while the agent edits and runs tests in isolation.

### 2. Spawning Subagents in Isolated Worktrees
When the main agent delegates competing implementations to subagents, it can isolate their filesystem changes using `Workspace: "branch"` or `Workspace: "share"`:

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Fastify Migration Worker",
      "Workspace": "branch",
      "Prompt": "Migrate src/server.ts from Express to Fastify and run npm test in your isolated worktree."
    }
  ]
}
```
Each subagent worktree is stored cleanly under `<appDataDir>/worktrees/` (`v1.2.10+`) and never pollutes your main checkout or artifact list.

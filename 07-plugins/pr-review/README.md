# PR Review Suite (`pr-review`)

An Antigravity plugin that bundles automated code review workflows, specialized security and performance subagents, git safety hooks, and review formatting rules into a single toggleable package.

## Bundled Components

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Manifest** | `plugin.json` | Declares plugin identity, version `1.2.0`, and starter prompts |
| **Rules** | `rules/AGENTS.md` | Enforces severity classification (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and clickable `file://` line citations |
| **Hooks** | `hooks.json` | Blocks accidental `git push --force` during review sessions and logs review artifact writes |
| **Skill: `/review-pr`** | `skills/review-pr/SKILL.md` | Orchestrates parallel security and performance subagents across the branch diff |
| **Skill: `/pr-summary`** | `skills/pr-summary/SKILL.md` | Generates structured Pull Request descriptions with architectural diagrams and test checklists |
| **Agent: `security-reviewer`** | `agents/security-reviewer.md` | Read-only security auditor focused on injection, auth bypass, SSRF, and leaked secrets |
| **Agent: `performance-reviewer`** | `agents/performance-reviewer.md` | Read-only performance specialist focused on N+1 queries, memory leaks, and hot-path latency |

## Installation & Validation

```bash
# Validate the plugin structure
agy plugin validate ./07-plugins/pr-review --strict

# Install into your local Antigravity profile
agy plugin install ./07-plugins/pr-review

# Verify installation
agy plugin list
```

## Usage

Once installed and enabled, invoke the bundled skills in the Antigravity App or CLI:

```text
/review-pr
/pr-review:review-pr main..HEAD
/pr-summary
```

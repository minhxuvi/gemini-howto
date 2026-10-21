# DevOps & SRE Automation Suite (`devops-automation`)

A production-grade Antigravity plugin that packages deployment and rollback skills, an incident-response subagent, destructive-command safety hooks, and a lifecycle-bound observability MCP server.

## Bundled Components

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Manifest** | `plugin.json` | Declares `devops-automation` v1.1.0 and SRE starter prompts |
| **Rules** | `rules/AGENTS.md` | Enforces pre-deploy verification, canary health gates, and blast-radius controls |
| **Hooks** | `hooks.json` | Blocks destructive cluster/infrastructure commands (`kubectl delete namespace`, `terraform destroy`) |
| **MCP Config** | `mcp_config.json` | Registers the `devops-automation_k8s-telemetry` MCP server while the plugin is enabled |
| **Skill: `/deploy`** | `skills/deploy/SKILL.md` | Pre-flight test/lint gate, canary rollout, and post-deploy smoke verification |
| **Skill: `/rollback`** | `skills/rollback/SKILL.md` | Fast service reversion, health verification, and post-incident summary artifact |
| **Agent: `incident-responder`** | `agents/incident-responder.md` | High-reasoning (`model: pro`) root-cause triage specialist with MCP access |

## Installation & Validation

```bash
agy plugin validate ./07-plugins/devops-automation --strict
agy plugin install ./07-plugins/devops-automation
```

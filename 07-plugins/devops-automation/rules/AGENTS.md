# DevOps & SRE Automation — Operational Safety Rules

When the `devops-automation` plugin is enabled, strictly adhere to these operational guardrails:

## 1. Pre-Flight Verification Before Any Rollout
- Never initiate a deployment if the working tree has uncommitted modifications (`git status --porcelain` must be clean) or if the test suite is failing.
- Always record the current live revision/digest before applying a new release so an immediate rollback target is known.

## 2. Blast-Radius & Environment Isolation
- Treat `production` / `prod` namespaces and clusters as strictly protected. Always verify the active context (`kubectl config current-context` or target environment variable) before running state-mutating commands.
- Never run un-targeted destructive operations (`terraform destroy`, `kubectl delete --all`, or `DROP TABLE`).

## 3. Incident Response Discipline
- During an active incident or `/rollback`, prioritize **mitigation and service restoration** over root-cause code fixes. Restore last-known-good state first, then delegate deep log correlation to `incident-responder`.

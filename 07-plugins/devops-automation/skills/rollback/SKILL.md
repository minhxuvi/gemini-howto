---
name: rollback
description: "Immediately revert a service deployment to the previous last-known-good revision, verify service recovery, and draft an incident timeline."
---

# Emergency Rollback (`/rollback`)

Restore service health by reverting to the last known good release and capturing post-incident diagnostics.

## Workflow

1. **Identify Target Revision**:
   - Use the user-supplied revision SHA/tag, or read the previous deployment revision from rollout history (`kubectl rollout history` / git tags).
2. **Execute Rollback**:
   - Revert the service to the target revision (`kubectl rollout undo` or target deployment command).
   - Wait for rollout status to reach `complete` and verify `/healthz` responds with `200 OK`.
3. **Delegate Root-Cause Triage**:
   - Invoke `incident-responder` in the background to correlate the failed release's logs and commit diff while service restoration is confirmed.
4. **Produce Incident Summary**:
   - Report time of detection, time of rollback completion, restored revision ID, and initial root-cause findings from `incident-responder`.

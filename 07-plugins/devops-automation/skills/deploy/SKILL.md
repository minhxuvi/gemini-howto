---
name: deploy
description: "Execute a verified staged deployment with pre-flight git/test checks, canary health monitoring, and post-deploy smoke verification."
---

# Staged Canary Deployment (`/deploy`)

Run a controlled deployment workflow with pre-flight safety gates and automated health verification.

## Step 1: Pre-Flight Readiness Gate

1. Verify target environment (`staging` by default unless `production` is explicitly specified).
2. Confirm clean git working state via `git status --porcelain` and capture the current commit SHA (`git rev-parse --short HEAD`).
3. Run the unit and integration test suite to verify build integrity before rollout.

## Step 2: Record Rollback Baseline

1. Query the currently deployed revision or image tag so a deterministic rollback target is recorded before any mutation occurs.
2. Save the baseline state to `$PLUGIN_DATA/last_known_good.json` if `PLUGIN_DATA` is available.

## Step 3: Canary Rollout & Health Check

1. Apply the deployment to the canary slice or target environment.
2. Monitor pod readiness, HTTP health check endpoints (`/healthz`), and error rate metrics for regressions.
3. If error rate or p99 latency exceeds threshold, immediately trigger `/rollback`.

## Step 4: Deployment Summary

Output a structured deployment card containing:
- **Environment**: `<target>`
- **Previous Revision**: `<prev-sha>`
- **Deployed Revision**: `<new-sha>`
- **Health Check Status**: `✅ Healthy`
- **Quick Rollback Command**: `/rollback <prev-sha>`

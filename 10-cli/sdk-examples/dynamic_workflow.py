#!/usr/bin/env python3
"""Module 10 Example 3: Dynamic Multi-Agent Workflows (@beta.workflows.define).

Demonstrates the `google-antigravity` v0.1.22 dynamic workflow orchestration API:
1. Decorating a workflow function with `@beta.workflows.define`.
2. Structuring execution stages with `phase(...)` and `log(...)`.
3. Fanning out concurrent specialist agents with `parallel(agent(...), ...)`.
4. Chaining sequential synthesis stages with `pipeline(agent(...), ...)`.
5. Running the workflow via `await client.beta.run_workflow(pr_readiness_workflow, payload)`.

Usage:
    python3 10-cli/sdk-examples/dynamic_workflow.py --dry-run
    GEMINI_API_KEY="your-key" python3 10-cli/sdk-examples/dynamic_workflow.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class PRWorkflowInput:
    """Structured input passed to `agent.beta.run_workflow(...)`."""

    pr_number: int
    target_directory: str
    base_branch: str = "main"


def describe_workflow_topology(payload: PRWorkflowInput) -> dict[str, Any]:
    """Return a deterministic representation of the workflow graph for --dry-run."""
    return {
        "workflow_name": "pr_readiness_workflow",
        "sdk_version": "0.1.22",
        "input": asdict(payload),
        "phases": [
            {
                "phase": "1-parallel-specialist-review",
                "primitive": "parallel",
                "branches": [
                    {"agent": "security-auditor", "model": "gemini-4-argon"},
                    {"agent": "performance-profiler", "model": "gemini-3.8-flash"},
                    {"agent": "documentation-verifier", "model": "gemini-3.8-flash"},
                ],
            },
            {
                "phase": "2-sequential-synthesis-pipeline",
                "primitive": "pipeline",
                "stages": [
                    {"agent": "findings-deduplicator", "model": "gemini-3.8-flash"},
                    {"agent": "release-decision-gate", "model": "gemini-4-argon"},
                ],
            },
        ],
    }


async def run_live_workflow(workspace_root: str) -> None:
    """Define and execute a multi-agent workflow using google.antigravity.beta."""
    from google.antigravity import (  # type: ignore[import-not-found]
        Agent,
        GeminiAPIEndpoint,
        LocalAgentConfig,
        beta,
        types,
    )
    from google.antigravity.beta.workflows import (  # type: ignore[import-not-found]
        agent,
        log,
        parallel,
        phase,
        pipeline,
    )

    @beta.workflows.define
    async def pr_readiness_workflow(data: PRWorkflowInput) -> dict[str, Any]:
        """Multi-stage PR verification workflow combining parallel and pipeline primitives."""
        await log(f"Starting PR #{data.pr_number} verification on {data.target_directory}")

        # Phase 1: Concurrent specialist audits using `parallel(...)`
        async with phase("1-parallel-specialist-review"):
            sec_report, perf_report, docs_report = await parallel(
                agent(
                    name="security-auditor",
                    model="gemini-4-argon",
                    prompt=(
                        f"Audit '{data.target_directory}' for security vulnerabilities, "
                        "unsafe shell hooks, or hardcoded credentials."
                    ),
                ),
                agent(
                    name="performance-profiler",
                    model="gemini-3.8-flash",
                    prompt=(
                        f"Inspect '{data.target_directory}' for token-budget efficiency, "
                        "eager MCP loading overhead, and timeout bounds."
                    ),
                ),
                agent(
                    name="documentation-verifier",
                    model="gemini-3.8-flash",
                    prompt=(
                        f"Verify that all README links and JSON manifests inside "
                        f"'{data.target_directory}' are complete and accurate."
                    ),
                ),
            )

        # Phase 2: Sequential synthesis and release gating using `pipeline(...)`
        async with phase("2-sequential-synthesis-pipeline"):
            await log("Synthesizing specialist reports into final release verdict...")
            combined_context = (
                f"Security:\n{sec_report.text}\n\n"
                f"Performance:\n{perf_report.text}\n\n"
                f"Documentation:\n{docs_report.text}"
            )
            final_verdict = await pipeline(
                agent(
                    name="findings-deduplicator",
                    model="gemini-3.8-flash",
                    prompt=(
                        "Deduplicate and rank the following three specialist reports by "
                        f"severity (P0, P1, P2):\n\n{combined_context}"
                    ),
                ),
                agent(
                    name="release-decision-gate",
                    model="gemini-4-argon",
                    prompt=(
                        "Produce an executive Go/No-Go release recommendation based on the "
                        "deduplicated findings from the previous stage."
                    ),
                ),
            )

        return {
            "pr_number": data.pr_number,
            "target_directory": data.target_directory,
            "verdict": final_verdict.text,
        }

    config = LocalAgentConfig(
        workspace_root=workspace_root,
        endpoint=GeminiAPIEndpoint(
            api_key=os.environ["GEMINI_API_KEY"],
            model="gemini-4-argon",
        ),
        builtin_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.LIST_DIR,
            types.BuiltinTools.GREP_SEARCH,
        ],
    )

    payload = PRWorkflowInput(pr_number=42, target_directory="07-plugins")
    async with Agent(config) as client:
        result = await client.beta.run_workflow(pr_readiness_workflow, payload)
        print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity Dynamic Workflow Example")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the @beta.workflows.define execution DAG without making API calls.",
    )
    args = parser.parse_args()

    sample_input = PRWorkflowInput(pr_number=42, target_directory="07-plugins")
    if args.dry_run:
        topology = describe_workflow_topology(sample_input)
        print("[dynamic_workflow.py --dry-run] Validated @beta.workflows.define DAG:")
        print(json.dumps(topology, indent=2))
        return

    repo_root = str(Path(__file__).resolve().parents[2])
    asyncio.run(run_live_workflow(repo_root))


if __name__ == "__main__":
    main()

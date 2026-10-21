#!/usr/bin/env python3
"""Module 10 Example 2: Custom Python Tools, MCP Servers, Inline Skills & Policies.

Demonstrates:
1. Defining custom Python tools (`tools=[...]`) with type annotations, docstrings,
   and stateful `types.ToolContext` access (`ctx.get_state` / `ctx.set_state`).
2. Connecting an external MCP server via `types.McpStreamableHttpServer` with
   `force_all_tools_eager=True` and `mcp_max_output_bytes=65536`.
3. Injecting an in-memory `InlineSkill` alongside filesystem `skills_paths`.
4. Registering a specialist subagent via `types.SubagentConfig` and governing
   tool invocations with declarative security policies (`google.antigravity.hooks.policy`).

Usage:
    python3 10-cli/sdk-examples/custom_tools_and_mcp.py --dry-run
    GEMINI_API_KEY="your-key" python3 10-cli/sdk-examples/custom_tools_and_mcp.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# 1. Custom Python Tools (automatically converted to JSON Schema by the SDK)
# ---------------------------------------------------------------------------

def check_slo_budget(service_name: str, window_days: int = 30) -> dict[str, Any]:
    """Fetch the remaining error budget and burn rate for a production service.

    Args:
        service_name: Canonical service identifier (e.g., 'checkout-api', 'auth-gateway').
        window_days: Rolling SLO evaluation window in days (default: 30).
    """
    sample_budgets = {
        "checkout-api": {"slo_target": 99.95, "remaining_budget_pct": 68.4, "burn_rate_1h": 0.8},
        "auth-gateway": {"slo_target": 99.99, "remaining_budget_pct": 14.2, "burn_rate_1h": 3.4},
    }
    metrics = sample_budgets.get(
        service_name,
        {"slo_target": 99.9, "remaining_budget_pct": 95.0, "burn_rate_1h": 0.2},
    )
    return {
        "service": service_name,
        "window_days": window_days,
        **metrics,
        "release_allowed": metrics["remaining_budget_pct"] >= 20.0 and metrics["burn_rate_1h"] < 2.0,
    }


def record_release_audit_note(service_name: str, verdict: str, note: str, ctx: Any = None) -> str:
    """Persist a structured release-readiness audit note in session state.

    Args:
        service_name: Target service name.
        verdict: Either 'APPROVED' or 'BLOCKED'.
        note: Short rationale for the release decision.
        ctx: Optional Antigravity ToolContext injected automatically at runtime.
    """
    entry = {"service": service_name, "verdict": verdict.upper(), "note": note}
    if ctx is not None and hasattr(ctx, "get_state") and hasattr(ctx, "set_state"):
        history = list(ctx.get_state("release_audit_log", []))
        history.append(entry)
        ctx.set_state("release_audit_log", history)
    return f"Recorded {entry['verdict']} decision for {service_name}: {note}"


# ---------------------------------------------------------------------------
# 2. Inline Skill & Declarative Configuration Builder
# ---------------------------------------------------------------------------

SRE_GATEKEEPER_SKILL_MD = """\
# SRE Release Gatekeeper Playbook

1. Always call `check_slo_budget` before approving any production deployment.
2. If `remaining_budget_pct < 20.0` or `burn_rate_1h >= 2.0`, mark the release as `BLOCKED`
   and call `record_release_audit_note` with the exact remediation steps.
3. Never run destructive shell commands (`rm -rf`, `kubectl delete namespace`).
"""


async def run_live_agent(workspace_root: str) -> None:
    """Configure and run an Agent with custom tools, MCP, InlineSkill, and policies."""
    from google.antigravity import (  # type: ignore[import-not-found]
        Agent,
        GeminiAPIEndpoint,
        InlineSkill,
        LocalAgentConfig,
        types,
    )
    from google.antigravity.hooks.policy import (  # type: ignore[import-not-found]
        allow,
        ask_user,
        confirm_run_command,
        deny,
        workspace_only,
    )

    config = LocalAgentConfig(
        workspace_root=workspace_root,
        endpoint=GeminiAPIEndpoint(
            api_key=os.environ["GEMINI_API_KEY"],
            model="gemini-4-argon",
        ),
        builtin_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.GREP_SEARCH,
            types.BuiltinTools.RUN_COMMAND,
            types.BuiltinTools.INVOKE_SUBAGENT,
        ],
        # Custom Python tools
        tools=[check_slo_budget, record_release_audit_note],
        # Streamable HTTP MCP server configuration
        mcp_servers=[
            types.McpStreamableHttpServer(
                name="github-enterprise",
                url=os.environ.get("GITHUB_MCP_URL", "https://api.githubcopilot.com/mcp/"),
                headers={"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}"},
            )
        ],
        force_all_tools_eager=True,
        mcp_max_output_bytes=65536,
        # In-memory skill + filesystem skills discovery
        inline_skills=[
            InlineSkill(
                name="sre-release-gatekeeper",
                description="Enforces SLO error budget checks before production releases.",
                content=SRE_GATEKEEPER_SKILL_MD,
            )
        ],
        skills_paths=[os.path.join(workspace_root, ".gemini", "skills")],
        # Specialist subagent registration
        subagents=[
            types.SubagentConfig(
                name="rollback-planner",
                description="Drafts step-by-step rollback runbooks when an SLO gate fails.",
                system_prompt="You are a site reliability rollback specialist.",
                model="gemini-3.8-flash",
                capabilities=types.SubagentCapabilities(
                    enable_write_tools=False,
                    enable_mcp_tools=True,
                ),
            )
        ],
        max_subagent_depth=2,
        # OS-level command sandbox + declarative 9-level policy rules
        run_command_config=types.RunCommandConfig(enable_sandbox=True),
        policies=[
            workspace_only(),
            deny(
                types.BuiltinTools.RUN_COMMAND,
                when=lambda args: "rm -rf" in args.get("CommandLine", ""),
                reason="Destructive rm -rf commands are blocked by SRE policy.",
            ),
            ask_user(
                types.BuiltinTools.RUN_COMMAND,
                when=lambda args: "kubectl apply" in args.get("CommandLine", ""),
            ),
            allow("check_slo_budget"),
            allow("record_release_audit_note"),
            confirm_run_command(),
        ],
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "Evaluate whether 'checkout-api' and 'auth-gateway' can be deployed today, "
            "and record an audit note for each service."
        )
        async for thought in response.thoughts:
            print(f"\033[2m[Thought] {thought}\033[0m", end="", flush=True)
        async for token in response:
            print(token, end="", flush=True)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Custom Tools, MCP & Policy SDK Example")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the custom tools locally and print the validated configuration.",
    )
    args = parser.parse_args()

    if args.dry_run:
        checkout = check_slo_budget("checkout-api")
        auth = check_slo_budget("auth-gateway")
        note = record_release_audit_note(
            "auth-gateway",
            "BLOCKED",
            "1h burn rate (3.4x) exceeds 2.0x threshold and remaining budget is 14.2%.",
        )
        print("[custom_tools_and_mcp.py --dry-run] Custom Tool Verification:")
        print(json.dumps({"checkout_slo": checkout, "auth_slo": auth, "audit_note": note}, indent=2))
        return

    repo_root = str(Path(__file__).resolve().parents[2])
    asyncio.run(run_live_agent(repo_root))


if __name__ == "__main__":
    main()

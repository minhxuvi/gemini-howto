#!/usr/bin/env python3
"""Module 10 Example 1: Basic Agent Queries, Streaming Thoughts & Tool Calls.

Demonstrates:
1. Configuring `LocalAgentConfig` with `GeminiAPIEndpoint` (or `VertexEndpoint`).
2. Setting `types.GeminiModelOptions` (`thinking_level="high"`, `max_output_tokens`,
   and `service_tier=types.ServiceTier.PRIORITY`).
3. Running single-turn queries with `await agent.query(...)`.
4. Streaming real-time thoughts (`chunk.thoughts`), tool calls (`chunk.tool_calls`),
   and response text (`chunk.text`) with `async for chunk in agent.stream(...)`,
   as well as low-level `await agent.chat(...)` token/thought iterators.

Usage:
    python3 10-cli/sdk-examples/hello_agent.py --dry-run
    GEMINI_API_KEY="your-key" python3 10-cli/sdk-examples/hello_agent.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any


def build_agent_config_dict(workspace_root: str, use_vertex: bool = False) -> dict[str, Any]:
    """Return a serializable preview of the LocalAgentConfig for --dry-run inspection."""
    endpoint_cfg = (
        {
            "type": "VertexEndpoint",
            "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project"),
            "location": os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
            "model": "gemini-4-argon",
        }
        if use_vertex
        else {
            "type": "GeminiAPIEndpoint",
            "model": "gemini-4-argon",
            "api_key_env": "GEMINI_API_KEY",
        }
    )
    return {
        "workspace_root": workspace_root,
        "endpoint": endpoint_cfg,
        "model_options": {
            "thinking_level": "high",
            "max_output_tokens": 16384,
            "service_tier": "PRIORITY",
        },
        "builtin_tools": [
            "VIEW_FILE",
            "LIST_DIR",
            "GREP_SEARCH",
            "FIND_BY_NAME",
        ],
    }


async def run_live_agent(workspace_root: str, use_vertex: bool = False) -> None:
    """Execute a live query and streaming turn using the google-antigravity SDK."""
    from google.antigravity import (  # type: ignore[import-not-found]
        Agent,
        GeminiAPIEndpoint,
        LocalAgentConfig,
        VertexEndpoint,
        types,
    )

    model_options = types.GeminiModelOptions(
        thinking_level="high",
        max_output_tokens=16384,
        service_tier=types.ServiceTier.PRIORITY,
    )

    if use_vertex:
        endpoint = VertexEndpoint(
            project=os.environ["GOOGLE_CLOUD_PROJECT"],
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
            model="gemini-4-argon",
            model_options=model_options,
        )
    else:
        endpoint = GeminiAPIEndpoint(
            api_key=os.environ["GEMINI_API_KEY"],
            model="gemini-4-argon",
            model_options=model_options,
        )

    config = LocalAgentConfig(
        workspace_root=workspace_root,
        endpoint=endpoint,
        builtin_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.LIST_DIR,
            types.BuiltinTools.GREP_SEARCH,
            types.BuiltinTools.FIND_BY_NAME,
        ],
    )

    async with Agent(config) as agent:
        print("=== 1. Single-Turn Query (agent.query) ===")
        summary = await agent.query(
            "List the 10 learning modules in this repository in one concise bullet per module."
        )
        print(summary.text)

        print("\n=== 2. Real-Time Streaming (agent.stream) ===")
        prompt = (
            "Inspect 07-plugins/ and report the name and version of each plugin "
            "defined in its plugin.json manifest."
        )
        async for chunk in agent.stream(prompt):
            if chunk.thoughts:
                print(f"\033[2m[Thought] {chunk.thoughts}\033[0m", end="", flush=True)
            for tool_call in chunk.tool_calls:
                print(f"\n\033[36m[Tool Call] {tool_call.name}({tool_call.args})\033[0m")
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity SDK Hello Agent Example")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the agent configuration without making network calls.",
    )
    parser.add_argument(
        "--vertex",
        action="store_true",
        help="Configure VertexEndpoint instead of GeminiAPIEndpoint.",
    )
    args = parser.parse_args()

    repo_root = str(Path(__file__).resolve().parents[2])
    if args.dry_run:
        preview = build_agent_config_dict(repo_root, use_vertex=args.vertex)
        print("[hello_agent.py --dry-run] Validated LocalAgentConfig:")
        print(json.dumps(preview, indent=2))
        return

    asyncio.run(run_live_agent(repo_root, use_vertex=args.vertex))


if __name__ == "__main__":
    main()

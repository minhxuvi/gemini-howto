#!/usr/bin/env python3
"""Module 10 Example 4: On-Device Execution with LiteRT-LM (Gemma 4 26B) & Local OpenAI.

Demonstrates offline and local-server execution introduced in `google-antigravity` v0.1.22:
1. `LiteRTAgentConfig` running a local quantized `Gemma 4 26B` model imported via
   `litert-lm import google/gemma-4-26b-it --quantization int4`.
2. Automatic `.lightweight()` optimizations applied by `LiteRTAgentConfig` (compact system
   prompt, minimal tool schemas, and a `40,960`-token context compaction threshold).
3. `LocalOpenAIAgentConfig(model="gemma4:26b", base_url="http://localhost:11434/v1").lightweight()`
   for local Ollama, vLLM, LM Studio, or llama.cpp endpoints.

Usage:
    python3 10-cli/sdk-examples/local_litert_agent.py --dry-run
    python3 10-cli/sdk-examples/local_litert_agent.py --backend litert
    python3 10-cli/sdk-examples/local_litert_agent.py --backend ollama
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_LITERT_MODEL_PATH = os.path.expanduser(
    "~/.litert-lm/models/gemma4-26b/model.litertlm"
)
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"


def build_local_config_preview(workspace_root: str, backend: str) -> dict[str, Any]:
    """Return a serializable preview of LiteRTAgentConfig or LocalOpenAIAgentConfig."""
    if backend == "litert":
        return {
            "config_class": "LiteRTAgentConfig",
            "model_path": DEFAULT_LITERT_MODEL_PATH,
            "workspace_root": workspace_root,
            "auto_applied_preset": "lightweight()",
            "compaction_threshold_tokens": 40960,
            "import_command": (
                "litert-lm import google/gemma-4-26b-it "
                "--quantization int4 "
                f"--output {DEFAULT_LITERT_MODEL_PATH}"
            ),
        }
    return {
        "config_class": "LocalOpenAIAgentConfig.lightweight()",
        "model": "gemma4:26b",
        "base_url": DEFAULT_OLLAMA_BASE_URL,
        "workspace_root": workspace_root,
        "auto_applied_preset": "lightweight()",
        "compaction_threshold_tokens": 40960,
    }


async def run_local_agent(workspace_root: str, backend: str) -> None:
    """Run an offline agent using either LiteRTAgentConfig or LocalOpenAIAgentConfig."""
    from google.antigravity import (  # type: ignore[import-not-found]
        Agent,
        LiteRTAgentConfig,
        LocalOpenAIAgentConfig,
        types,
    )

    if backend == "litert":
        config = LiteRTAgentConfig(
            model_path=os.environ.get("LITERT_MODEL_PATH", DEFAULT_LITERT_MODEL_PATH),
            workspace_root=workspace_root,
            builtin_tools=[
                types.BuiltinTools.VIEW_FILE,
                types.BuiltinTools.LIST_DIR,
                types.BuiltinTools.GREP_SEARCH,
            ],
        )
    else:
        config = LocalOpenAIAgentConfig(
            model=os.environ.get("LOCAL_OPENAI_MODEL", "gemma4:26b"),
            base_url=os.environ.get("LOCAL_OPENAI_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
            workspace_root=workspace_root,
            builtin_tools=[
                types.BuiltinTools.VIEW_FILE,
                types.BuiltinTools.LIST_DIR,
                types.BuiltinTools.GREP_SEARCH,
            ],
        ).lightweight()

    async with Agent(config) as agent:
        async for chunk in agent.stream(
            "Read 08-checkpoints/README.md and summarize how checkpoints differ from git worktrees."
        ):
            for tool_call in chunk.tool_calls:
                print(f"\n[Local Tool Call] {tool_call.name}({tool_call.args})")
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="On-Device LiteRT & Local OpenAI SDK Example")
    parser.add_argument(
        "--backend",
        choices=["litert", "ollama"],
        default="litert",
        help="Select 'litert' (LiteRTAgentConfig) or 'ollama' (LocalOpenAIAgentConfig).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the local agent configuration without loading model weights.",
    )
    args = parser.parse_args()

    repo_root = str(Path(__file__).resolve().parents[2])
    if args.dry_run:
        preview = build_local_config_preview(repo_root, args.backend)
        print(f"[local_litert_agent.py --dry-run] Validated {args.backend} configuration:")
        print(json.dumps(preview, indent=2))
        return

    asyncio.run(run_local_agent(repo_root, args.backend))


if __name__ == "__main__":
    main()

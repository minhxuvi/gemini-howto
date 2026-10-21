#!/usr/bin/env python3
"""
Antigravity Hook: context-tracker.py
Event: PreInvocation (Flat handler array)
Purpose:
  Inspects `transcriptPath` size and `initialNumSteps` before each model
  invocation. When the conversation trajectory grows large, injects a transient
  `ephemeralMessage` via `injectSteps` reminding the agent to persist key state
  into artifacts or recommend `/compact` to the user.
"""

import json
import os
import sys

STEP_WARNING_THRESHOLD = 80
BYTE_WARNING_THRESHOLD = 400_000  # ~100k estimated tokens


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print(json.dumps({"injectSteps": []}))
        return

    initial_steps = int(data.get("initialNumSteps") or 0)
    transcript_path = os.path.expanduser(str(data.get("transcriptPath") or ""))

    transcript_bytes = 0
    if transcript_path and os.path.isfile(transcript_path):
        try:
            transcript_bytes = os.path.getsize(transcript_path)
        except OSError:
            transcript_bytes = 0

    est_tokens = transcript_bytes // 4

    if initial_steps >= STEP_WARNING_THRESHOLD or transcript_bytes >= BYTE_WARNING_THRESHOLD:
        hint = (
            f"[Context Monitor] Trajectory has reached {initial_steps} steps "
            f"(~{est_tokens:,} estimated tokens). Keep responses concise, offload "
            f"exploratory searches to the `research` subagent, and consider updating "
            f"your task artifact or recommending `/compact` to the user."
        )
        print(
            json.dumps(
                {
                    "injectSteps": [
                        {
                            "ephemeralMessage": hint,
                        }
                    ]
                }
            )
        )
        return

    print(json.dumps({"injectSteps": []}))


if __name__ == "__main__":
    main()

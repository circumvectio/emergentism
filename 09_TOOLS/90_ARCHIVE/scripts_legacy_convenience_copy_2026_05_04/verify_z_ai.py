#!/usr/bin/env python3
"""
verify_z_ai.py — confirm z.ai connectivity for the organism.

Loads .env from project root. Pings z.ai's OpenAI-compatible endpoint with
a 10-token test prompt. Tries the configured ZAI_MODEL first; falls back
through glm-5.1 -> glm-5 -> glm-4.6 -> glm-4-plus -> glm-4-air if needed.

Prints OK + (model, latency_ms, tokens). Never prints the key.

Run: python3 EMERGENTISM_ORG/09_TOOLS/verify_z_ai.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Fallback ladder if the configured model name does not resolve at z.ai.
MODEL_FALLBACK_LADDER = ["glm-5.1", "glm-5", "glm-4.6", "glm-4-plus", "glm-4-air"]


def main() -> int:
    if not ENV_PATH.exists():
        print(f"FAIL: .env not found at {ENV_PATH}")
        return 2
    load_dotenv(ENV_PATH)

    api_key = os.environ.get("ZAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("ZAI_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    configured_model = os.environ.get("ZAI_MODEL") or os.environ.get("OPENAI_MODEL")

    if not api_key:
        print("FAIL: ZAI_API_KEY (or OPENAI_API_KEY) missing in .env")
        return 2
    if not base_url:
        print("FAIL: ZAI_BASE_URL (or OPENAI_BASE_URL) missing in .env")
        return 2

    print(f"base_url: {base_url}")
    print(f"key: present (length redacted)")
    print(f"configured_model: {configured_model}")

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Try the configured model first, then the fallback ladder
    candidates: list[str] = []
    if configured_model:
        candidates.append(configured_model)
    for m in MODEL_FALLBACK_LADDER:
        if m not in candidates:
            candidates.append(m)

    last_error: str | None = None
    for model in candidates:
        print(f"trying: {model}")
        t0 = time.perf_counter()
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Say only: organism heartbeat ready"}
                ],
                max_tokens=10,
                temperature=0.0,
            )
        except Exception as exc:
            err = repr(exc)
            # Redact any accidental key echo
            if api_key in err:
                err = err.replace(api_key, "<redacted>")
            print(f"  ERR ({model}): {err[:200]}")
            last_error = err
            continue
        latency_ms = round((time.perf_counter() - t0) * 1000, 1)

        content = resp.choices[0].message.content if resp.choices else ""
        usage = resp.usage
        usage_str = (
            f"prompt={usage.prompt_tokens} completion={usage.completion_tokens} "
            f"total={usage.total_tokens}"
            if usage
            else "n/a"
        )

        print(
            f"  OK ({model}): {content!r} latency_ms={latency_ms} tokens={usage_str}"
        )

        if model != configured_model:
            print(
                f"NOTE: fallback used. Pin model in .env -> ZAI_MODEL={model}"
            )

        return 0

    print(f"FAIL: no candidate model resolved at z.ai. last_error: {last_error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

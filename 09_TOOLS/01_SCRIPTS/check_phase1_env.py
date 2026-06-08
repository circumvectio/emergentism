#!/usr/bin/env python3
"""
Stage 0 preflight checker for Phase 1.

Validates that:
1. `.env.phase1` exists and contains all required keys.
2. Placeholder values have been replaced.
3. `.env.phase1` is gitignored.
4. A Stage 0 decision log exists.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_KEYS = [
    "HEDERA_ACCOUNT_ID",
    "HEDERA_PRIVATE_KEY",
    "HEDERA_NETWORK",
    "HEDERA_MIRROR_URL",
    "ARWEAVE_KEYFILE_PATH",
    "ARWEAVE_ADDRESS",
    "ARWEAVE_NETWORK",
    "NOSTR_RELAYS",
    "NPM_TOKEN",
    "PYPI_API_TOKEN",
    "CIRCLE_DOMAIN",
    "VERCEL_PROJECT_ID",
    "VERCEL_TEAM_ID",
    "BACKEND_HOST",
    "RF_FIRST_MARKET_QUESTION",
    "CAPITAL_POSTURE",
    "ARWEAVE_ANCHORING_MODE",
]


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[2]
    default_env = repo_root / "SKYZAI_ORG/02_ORGANS/Skyzai/execution/.env.phase1"
    default_glob = "SKYZAI_ORG/04_PROJECT_MANAGEMENT/PHASE_1_STAGE_0_DECISION_LOG_*.md"

    parser = argparse.ArgumentParser(
        description="Validate Phase 1 Stage 0 environment and decision-log readiness."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root,
        help="Repository root. Defaults to the parent of EMERGENTISM_ORG/09_TOOLS/.",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=default_env,
        help="Path to the filled `.env.phase1` file.",
    )
    parser.add_argument(
        "--decision-log-glob",
        default=default_glob,
        help="Glob, relative to repo root, for the Stage 0 decision log.",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def is_placeholder(value: str) -> bool:
    placeholder_patterns = [
        r"^<.*>$",
        r"X{3,}",
        r"0\.0\.X+",
        r"^npm_[Xx]+$",
        r"^pypi-[Xx]+$",
        r"^/secure/path/",
        r"^\s*$",
    ]
    return any(re.search(pattern, value) for pattern in placeholder_patterns)


def git_check_ignore(repo_root: Path, target: Path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", str(target)],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    env_file = args.env_file.resolve()

    failures = 0

    print("Phase 1 Stage 0 Preflight")
    print("=" * 44)

    if not env_file.exists():
        print(f"FAIL env file missing: {env_file}")
        failures += 1
        env = {}
    else:
        print(f"OK env file present: {env_file}")
        env = load_env_file(env_file)

    for key in REQUIRED_KEYS:
        value = env.get(key)
        if value is None:
            print(f"MISSING {key}")
            failures += 1
            continue
        if is_placeholder(value):
            print(f"PLACEHOLDER {key}={value}")
            failures += 1
            continue
        print(f"OK {key}")

    rel_env_file = env_file.relative_to(repo_root)
    if git_check_ignore(repo_root, rel_env_file):
        print(f"OK ignored {rel_env_file}")
    else:
        print(f"FAIL not ignored {rel_env_file}")
        failures += 1

    decision_logs = sorted(repo_root.glob(args.decision_log_glob))
    if decision_logs:
        print(f"OK decision log {decision_logs[-1].relative_to(repo_root)}")
    else:
        print(f"MISSING decision log ({args.decision_log_glob})")
        failures += 1

    if failures:
        print("-" * 44)
        print(f"Stage 0 NOT ready: {failures} issue(s) found.")
        return 1

    print("-" * 44)
    print("Stage 0 ready: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

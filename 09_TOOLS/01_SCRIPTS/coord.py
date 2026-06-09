#!/usr/bin/env python3
"""coord — multi-agent throughput-optimization tool for the Magnum Opus repository.

> **Constitutional framing (per L7 Ṛṣi reading 2026-04-28):**
>
> *This tool reduces redundant computation. It does not enforce correctness.
> Correctness is enforced by shared grammar + shared substrate, which produce
> convergent output independent of this tool.*
>
> When parallel agents holding the same grammar produce byte-identical output,
> that is **convergence**, not collision. Convergence is success; **divergence
> is the only event requiring adjudication.** This tool's claim/release
> mechanism is a politeness protocol — a cheap throughput optimization — not
> a constitutional principle. Do not let the locking surface convince L4 that
> the underlying law is exclusion. The underlying law is *shared grammar +
> shared substrate → isomorphic output*. The lock is just politeness.

15+ observed races during 2026-04-28 (initial six: CH_25B byte-identical
authoring, Track E completion + rebuild, title-rename, packet 195/196
numbering, root-tidy; subsequent: yieldfront 4-track parallel execution,
strategic-analysis double-absorption, Cerberus Kālī audit, dual-register
consolidation, K0+ audit-trail spec, Sprint-5 four-adapter parity, DID
identity layer, dual-vessel K2 briefs, holobiont reorientation surveys —
list non-exhaustive). All resolved cleanly through deterministic
convergence + the External Work Integration Convention's worked-example
pattern (4 examples now documented, see
`01_EMERGENTISM/08_FRAMEWORK_SUPPORT/05_SYNTHESIS/00_EXTERNAL_WORK_INTEGRATION_CONVENTION.md`).
The cumulative duplicated-token cost is the *insurance premium on
decentralization*; this tool tunes it, does not eliminate it.

Architecture:
    - 00_ACTIVE_CLAIMS.md is the canonical claim file at
      `02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/`
      (relocated 2026-05-29 from the retired organism root).
    - This tool wraps the claim/release cycle as atomic git commits.
    - Atomicity comes from git's commit lock: only one commit at a time.
    - Conflicts surface as commit failures; the loser re-evaluates.

Subcommands:
    coord claim <sprint-name> [--estimate Xh] [--agent NAME]
        Atomically claim a sprint via a git commit. Fails if already claimed.
    coord release <sprint-name> [--commit HASH]
        Release a claim, optionally referencing the completion commit.
    coord check [<sprint-name>]
        Show active claims; check conflict status for a candidate sprint.
    coord status
        Brief one-line status: claims count, recent commit count.
    coord sweep [--since 24h]
        Post-hoc divergence detection. When parallel agents produce
        byte-identical output, that's a *positive signal* (network is
        healthy). The sweep flags ONLY divergences — cases where two
        agents working on overlapping scope produced *different* outputs.
        Divergence indicates either grammar drift (repair upstream) or
        substrate drift (timestamp mismatch; reconcile at L4). Convergence
        requires no ceremony beyond keeping one commit.

Non-goals:
    - Hard locking. Agents can still skip the claim step; this tool makes
      compliance easy and detection automatic, not enforcement absolute.
    - Real-time inter-agent communication. We rely on git as substrate.
    - Centralized scheduling. The framework's grammar prefers distributed
      coordination through deterministic shared state.

The framework's anti-fragility-through-decentralization claim applies:
this tool makes coordination cheaper but does not require it. Races
will still happen; they will resolve through convergence. The gain is
visibility and reduced duplicated effort, not perfect synchronization.

⊙ = • × ○
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[3]
# Path repaired 2026-06-09: the constant lagged the docstring (and the
# 2026-05-29 relocation note above) by one reorg era. It pointed at the retired
# `03_VENTURES/SKYZAI/…` path, so every subcommand died with "not found" and the
# claim/release politeness-protocol was silently inert. Canonical home is
# `02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/`, matching active_claims_status.py.
CLAIMS_FILE = (
    REPO_ROOT
    / "02_SKYZAI"
    / "01_NOOSPHERE"
    / "05_PROJECT_MANAGEMENT"
    / "00_ACTIVE_CLAIMS.md"
)
CLAIMS_TABLE_HEADER = "| Sprint / Item | Agent | Claim time (GMT+7) | Expected end | Status | Commit hash |"
CLAIMS_TABLE_SEPARATOR = "|---|---|---|---|---|---|"
EMPTY_ROW = "| (none currently) | | | | | |"


# ---------------------------------------------------------------------------
# git helpers
# ---------------------------------------------------------------------------


def git(*args: str, check: bool = True, capture: bool = True) -> str:
    """Run a git command in the repo root and return stdout (when capturing)."""
    cmd = ["git", "-C", str(REPO_ROOT), *args]
    result = subprocess.run(cmd, check=check, capture_output=capture, text=True)
    return result.stdout.strip() if capture else ""


def current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD")


def short_sha(ref: str = "HEAD") -> str:
    return git("rev-parse", "--short", ref)


def now_str() -> str:
    """Current UTC+7 timestamp in compact form."""
    tz = timezone(timedelta(hours=7))
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M")


# ---------------------------------------------------------------------------
# claims-file operations
# ---------------------------------------------------------------------------


def read_claims() -> list[str]:
    """Return the lines of the claims file."""
    if not CLAIMS_FILE.exists():
        raise SystemExit(f"FAILED: {CLAIMS_FILE} not found.")
    return CLAIMS_FILE.read_text(encoding="utf-8").splitlines()


def write_claims(lines: list[str]) -> None:
    CLAIMS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_table_indices(lines: list[str]) -> tuple[int, int]:
    """Return (header_index, end_index) for the active-claims table."""
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip() == CLAIMS_TABLE_HEADER:
            header_idx = i
            break
    if header_idx is None:
        raise SystemExit(
            f"FAILED: claims table header not found in {CLAIMS_FILE}. "
            f"Expected line: {CLAIMS_TABLE_HEADER}"
        )
    end_idx = header_idx + 2
    while end_idx < len(lines) and lines[end_idx].strip().startswith("|"):
        end_idx += 1
    return header_idx, end_idx


def parse_rows(lines: list[str], header_idx: int, end_idx: int) -> list[list[str]]:
    """Parse table rows (excluding header + separator). Returns list of cell lists."""
    rows: list[list[str]] = []
    for line in lines[header_idx + 2 : end_idx]:
        if line.strip() == EMPTY_ROW.strip():
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6:
            rows.append(cells)
    return rows


def serialize_rows(rows: list[list[str]]) -> list[str]:
    if not rows:
        return [EMPTY_ROW]
    return ["| " + " | ".join(row[:6]) + " |" for row in rows]


def replace_rows(
    lines: list[str], header_idx: int, end_idx: int, new_rows: list[list[str]]
) -> list[str]:
    new_table = serialize_rows(new_rows)
    return lines[: header_idx + 2] + new_table + lines[end_idx:]


def normalize_sprint(name: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation for fuzzy matching."""
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


def overlapping_claim(
    rows: list[list[str]], sprint: str
) -> tuple[int, list[str]] | None:
    """Return (index, row) if any row's sprint name overlaps with the candidate."""
    target = normalize_sprint(sprint)
    if not target:
        return None
    for i, row in enumerate(rows):
        existing = normalize_sprint(row[0])
        if existing == target:
            return i, row
        # Substantial-substring match (>=10 chars overlap)
        if len(target) >= 10 and len(existing) >= 10:
            if target in existing or existing in target:
                return i, row
    return None


# ---------------------------------------------------------------------------
# subcommands
# ---------------------------------------------------------------------------


def cmd_claim(args: argparse.Namespace) -> int:
    sprint = args.sprint.strip()
    if not sprint:
        print("FAILED: empty sprint name.", file=sys.stderr)
        return 1
    agent = args.agent or current_branch()
    estimate = args.estimate or "?"

    lines = read_claims()
    header, end = find_table_indices(lines)
    rows = parse_rows(lines, header, end)

    overlap = overlapping_claim(rows, sprint)
    if overlap is not None:
        idx, row = overlap
        print(
            f"CONFLICT: sprint already claimed.\n"
            f"  Existing: {row[0]} (agent: {row[1]}, claim time: {row[2]})\n"
            f"  Per 00_ACTIVE_CLAIMS.md resolution rule, earlier claim wins.\n"
            f"  Either coordinate with that agent, switch to a different sprint,\n"
            f"  or wait for release.",
            file=sys.stderr,
        )
        return 2

    new_row = [
        sprint,
        agent,
        now_str(),
        f"~{estimate}" if estimate != "?" else "?",
        "active",
        "—",
    ]
    rows.append(new_row)
    new_lines = replace_rows(lines, header, end, rows)
    write_claims(new_lines)

    git("add", str(CLAIMS_FILE.relative_to(REPO_ROOT)))
    short_label = sprint.split(":")[0].strip().lower().replace(" ", "-")[:40]
    msg = f"claim({short_label}): {sprint}\n\nAgent: {agent}\nClaim time: {now_str()}\nEstimate: ~{estimate}"
    git("commit", "-m", msg, check=True)
    print(f"CLAIMED: {sprint}\n  Agent: {agent}\n  Commit: {short_sha()}")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    sprint = args.sprint.strip()
    agent = args.agent or current_branch()
    completion = args.commit or short_sha()

    lines = read_claims()
    header, end = find_table_indices(lines)
    rows = parse_rows(lines, header, end)

    target = normalize_sprint(sprint)
    matched_idx = None
    for i, row in enumerate(rows):
        existing = normalize_sprint(row[0])
        # Use the same fuzzy-match rule as claim's overlapping_claim:
        # exact OR substantial-substring match (≥10 char overlap)
        match = existing == target or (
            len(target) >= 10
            and len(existing) >= 10
            and (target in existing or existing in target)
        )
        agent_match = agent in row[1] or row[1] in agent
        if match and agent_match:
            matched_idx = i
            break

    if matched_idx is None:
        print(
            f"WARNING: no matching active claim found for '{sprint}' by '{agent}'.\n"
            f"  Active claims:",
            file=sys.stderr,
        )
        for row in rows:
            print(f"    - {row[0]} (agent: {row[1]})", file=sys.stderr)
        if not args.force:
            print(f"\nUse --force to commit a release row anyway.", file=sys.stderr)
            return 1

    if matched_idx is not None:
        rows.pop(matched_idx)
    new_lines = replace_rows(lines, header, end, rows)
    write_claims(new_lines)

    git("add", str(CLAIMS_FILE.relative_to(REPO_ROOT)))
    short_label = sprint.split(":")[0].strip().lower().replace(" ", "-")[:40]
    msg = f"release({short_label}): complete {completion}\n\nSprint: {sprint}\nAgent: {agent}\nReleased: {now_str()}"
    git("commit", "-m", msg, check=True)
    print(f"RELEASED: {sprint}\n  Agent: {agent}\n  Completion: {completion}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    lines = read_claims()
    header, end = find_table_indices(lines)
    rows = parse_rows(lines, header, end)

    if args.sprint:
        overlap = overlapping_claim(rows, args.sprint)
        if overlap is not None:
            idx, row = overlap
            print(
                f"CONFLICT: '{args.sprint}' overlaps with existing claim.\n"
                f"  Existing: {row[0]} (agent: {row[1]}, claim time: {row[2]})"
            )
            return 1
        print(f"CLEAR: '{args.sprint}' is unclaimed. Safe to claim.")
        return 0

    if not rows:
        print("No active claims.")
    else:
        print(f"{len(rows)} active claim(s):")
        for row in rows:
            print(f"  - {row[0]} (agent: {row[1]}, claim time: {row[2]}, status: {row[4]})")

    print(f"\nRecent commits (last 10):")
    log = git("log", "--oneline", "-10")
    for line in log.splitlines():
        print(f"  {line}")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    lines = read_claims()
    header, end = find_table_indices(lines)
    rows = parse_rows(lines, header, end)

    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    recent_commits = git("log", "--since", one_hour_ago, "--oneline")
    recent_count = len([l for l in recent_commits.splitlines() if l.strip()])

    print(
        f"branch={current_branch()} "
        f"claims={len(rows)} "
        f"recent_commits_1h={recent_count} "
        f"head={short_sha()}"
    )
    return 0


def cmd_sweep(args: argparse.Namespace) -> int:
    """Post-hoc divergence-detection.

    Per L7 reading 2026-04-28: convergence is success, not waste. We flag only
    divergences — overlapping scope with non-isomorphic outputs.
    """
    since = args.since
    log = git(
        "log",
        f"--since={since}",
        "--format=%H%x09%an%x09%s",
    )
    if not log:
        print(f"No commits in the last {since}.")
        return 0

    entries: list[tuple[str, str, str]] = []
    for line in log.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            entries.append((parts[0], parts[1], parts[2]))

    print(f"Scanning {len(entries)} commits since {since}...\n")

    # Pair commits with high subject-overlap as convergence-candidate pairs.
    # Then check whether their actual file changes are byte-identical
    # (convergence — positive signal) or different (divergence — flag for L4).
    subjects = [(i, e[2]) for i, e in enumerate(entries)]
    convergence_count = 0
    divergence_pairs: list[tuple[str, str, str, str]] = []

    seen = set()
    for ia, sa in subjects:
        for ib, sb in subjects[ia + 1 :]:
            ta = set(re.findall(r"\w+", sa.lower()))
            tb = set(re.findall(r"\w+", sb.lower()))
            if not ta or not tb:
                continue
            overlap = len(ta & tb) / min(len(ta), len(tb))
            if overlap < 0.6:
                continue
            sha_a, sha_b = entries[ia][0], entries[ib][0]
            key = tuple(sorted([sha_a, sha_b]))
            if key in seen:
                continue
            seen.add(key)
            # Compare touched-file paths between the two commits
            files_a = set(git("show", "--name-only", "--format=", sha_a).splitlines())
            files_b = set(git("show", "--name-only", "--format=", sha_b).splitlines())
            shared = files_a & files_b
            if not shared:
                continue
            # If any shared file differs in content between the two commits' tree states,
            # it's a divergence event. Otherwise, convergence.
            divergent = False
            for path in shared:
                try:
                    blob_a = git("show", f"{sha_a}:{path}", check=False)
                    blob_b = git("show", f"{sha_b}:{path}", check=False)
                    if blob_a != blob_b:
                        divergent = True
                        break
                except Exception:
                    continue
            if divergent:
                divergence_pairs.append((sha_a[:8], sa, sha_b[:8], sb))
            else:
                convergence_count += 1

    print(f"## Convergence events (positive signal): {convergence_count}\n")
    if divergence_pairs:
        print(f"## Divergence events (require L4 adjudication): {len(divergence_pairs)}\n")
        for sha_a, sa, sha_b, sb in divergence_pairs[:20]:
            print(f"  - {sha_a} {sa}\n    {sha_b} {sb}\n")
    else:
        print("## Divergence events: 0 — network is healthy.\n")

    # Pattern 2: orphaned claims (claim commits without subsequent release)
    claim_log = git("log", "--all", f"--since={since}", "--grep=^claim(", "--format=%H%x09%s")
    release_log = git("log", "--all", f"--since={since}", "--grep=^release(", "--format=%H%x09%s")

    claims_in_window = []
    releases_in_window = set()
    for line in claim_log.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            sprint_label = re.match(r"claim\((.+?)\):", parts[1])
            if sprint_label:
                claims_in_window.append((parts[0], sprint_label.group(1)))
    for line in release_log.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            sprint_label = re.match(r"release\((.+?)\):", parts[1])
            if sprint_label:
                releases_in_window.add(sprint_label.group(1))

    orphan_claims = [c for c in claims_in_window if c[1] not in releases_in_window]
    if orphan_claims:
        print(f"## Orphan claims (claimed but not released within window):\n")
        for sha, label in orphan_claims:
            print(f"  - {sha[:8]}  claim({label})")
    else:
        print("No orphan claims detected.\n")

    # Pattern 3: current active claims still in 00_ACTIVE_CLAIMS.md
    lines = read_claims()
    header, end = find_table_indices(lines)
    rows = parse_rows(lines, header, end)
    if rows:
        print(f"\n## Currently-active claims in 00_ACTIVE_CLAIMS.md:\n")
        for row in rows:
            print(f"  - {row[0]} (agent: {row[1]}, claim time: {row[2]})")
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Multi-agent coordination tool for the Magnum Opus repo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_claim = sub.add_parser("claim", help="Atomically claim a sprint via git commit.")
    p_claim.add_argument("sprint", help="Sprint or item name (free text).")
    p_claim.add_argument("--estimate", default=None, help="Estimated duration, e.g. '2h'.")
    p_claim.add_argument("--agent", default=None, help="Agent identifier (defaults to git branch).")

    p_release = sub.add_parser("release", help="Release a claim on completion.")
    p_release.add_argument("sprint", help="Sprint or item name to release.")
    p_release.add_argument("--commit", default=None, help="Completion commit hash (defaults to HEAD).")
    p_release.add_argument("--agent", default=None, help="Agent identifier (defaults to git branch).")
    p_release.add_argument("--force", action="store_true", help="Commit release even if no matching claim.")

    p_check = sub.add_parser("check", help="Show active claims; check a candidate sprint for conflicts.")
    p_check.add_argument("sprint", nargs="?", help="Candidate sprint name to check.")

    sub.add_parser("status", help="One-line status summary (branch, claims, recent commits).")

    p_sweep = sub.add_parser("sweep", help="Post-hoc convergence/redundancy detection.")
    p_sweep.add_argument("--since", default="24 hours ago", help="Time window (git log syntax).")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return 0

    handlers = {
        "claim": cmd_claim,
        "release": cmd_release,
        "check": cmd_check,
        "status": cmd_status,
        "sweep": cmd_sweep,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
dac_ancestry_audit.py — Audit descendant DAC repos against the current scaffold genome.

Walks a root of descendant repos (default `Github/`), reads each
`_DAC_SCAFFOLD_APPLIED.md`, extracts the recorded scaffold tree hash
and manifest snapshot, compares the recorded hash against the current
`tree_hash(DAC_SCAFFOLD/)`, and emits a report per descendant.

Exit codes:
  0 — all descendants aligned with current genome (or none found)
  1 — one or more descendants speciated from a stale genome (drift)
  2 — error reading a descendant's record

Usage:
    python dac_ancestry_audit.py                                  # audits Github/*
    python dac_ancestry_audit.py --root /path/to/repos            # custom root
    python dac_ancestry_audit.py --scaffold /path/to/DAC_SCAFFOLD  # custom genome
    python dac_ancestry_audit.py --markdown                       # emit markdown report
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

def _find_github_root() -> Path:
    """Locate the Github/ staging dir. It lives at the main repo root, but this
    script may run from a git worktree under .claude/worktrees/<name>/. Probe
    the worktree-sibling path first, then climb until we find `Github/`."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[3] / "Github",           # direct run from main repo
        here.parents[3].parent.parent.parent / "Github",  # from .claude/worktrees/<name>/
    ]
    for c in candidates:
        if c.is_dir():
            return c
    # fallback to the first candidate for error reporting clarity
    return candidates[0]


DEFAULT_ROOT = _find_github_root()
DEFAULT_SCAFFOLD = (
    Path(__file__).resolve().parents[3]
    / "SKYZAI_ORG"
    / "00_REFERENCE"
    / "DAC_FACTORY"
    / "DAC_SCAFFOLD"
)
APPLIED_FILENAME = "_DAC_SCAFFOLD_APPLIED.md"
HASH_LINE_RE = re.compile(r"^-\s*Scaffold tree hash:\s*`([0-9a-f]+)`", re.MULTILINE)
TIMESTAMP_RE = re.compile(r"^-\s*Applied at:\s*([^\n]+)", re.MULTILINE)
MANIFEST_NAME_RE = re.compile(r"^-\s*Manifest:\s*`([^`]+)`", re.MULTILINE)


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix().encode()
            h.update(b"\x00" + rel + b"\x00")
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def parse_applied(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    rec: dict[str, str] = {}
    m = HASH_LINE_RE.search(text)
    if m:
        rec["hash"] = m.group(1)
    m = TIMESTAMP_RE.search(text)
    if m:
        rec["applied_at"] = m.group(1).strip()
    m = MANIFEST_NAME_RE.search(text)
    if m:
        rec["manifest"] = m.group(1)
    return rec


def audit(root: Path, scaffold: Path) -> tuple[str, list[dict]]:
    current_hash = tree_hash(scaffold)
    records: list[dict] = []
    for applied in sorted(root.glob(f"*/{APPLIED_FILENAME}")):
        descendant = applied.parent
        try:
            rec = parse_applied(applied)
        except Exception as exc:
            records.append(
                {
                    "descendant": descendant.name,
                    "status": "ERROR",
                    "note": f"parse failed: {exc}",
                }
            )
            continue
        recorded = rec.get("hash", "UNKNOWN")
        aligned = recorded == current_hash
        records.append(
            {
                "descendant": descendant.name,
                "status": "ALIGNED" if aligned else "DRIFT",
                "recorded_hash": recorded,
                "current_hash": current_hash,
                "applied_at": rec.get("applied_at", "?"),
                "manifest": rec.get("manifest", "?"),
            }
        )
    return current_hash, records


def render_text(current_hash: str, records: list[dict]) -> str:
    lines = [
        f"DAC ancestry audit",
        f"current scaffold tree hash: {current_hash}",
        f"descendants found: {len(records)}",
        "",
    ]
    for rec in records:
        if rec["status"] == "ERROR":
            lines.append(f"  [ERROR]   {rec['descendant']:20s} {rec['note']}")
        elif rec["status"] == "ALIGNED":
            lines.append(
                f"  [ALIGNED] {rec['descendant']:20s} "
                f"{rec['recorded_hash']} (via {rec['manifest']}, {rec['applied_at']})"
            )
        else:
            lines.append(
                f"  [DRIFT]   {rec['descendant']:20s} "
                f"recorded={rec['recorded_hash']} current={rec['current_hash']} "
                f"(via {rec['manifest']}, {rec['applied_at']})"
            )
    return "\n".join(lines)


def render_markdown(current_hash: str, records: list[dict]) -> str:
    from datetime import datetime, timezone

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    drift_count = sum(1 for r in records if r["status"] == "DRIFT")
    error_count = sum(1 for r in records if r["status"] == "ERROR")
    aligned_count = sum(1 for r in records if r["status"] == "ALIGNED")
    lines = [
        "# DAC Ancestry Audit",
        "",
        f"- Generated: {ts}",
        f"- Current scaffold tree hash: `{current_hash}`",
        f"- Descendants: {len(records)} "
        f"(aligned: {aligned_count}, drift: {drift_count}, error: {error_count})",
        "",
        "| Descendant | Status | Recorded hash | Manifest | Applied at |",
        "|---|---|---|---|---|",
    ]
    for rec in records:
        if rec["status"] == "ERROR":
            lines.append(
                f"| `{rec['descendant']}` | ❌ ERROR | — | — | {rec.get('note', '?')} |"
            )
        else:
            mark = "✅" if rec["status"] == "ALIGNED" else "⚠️"
            lines.append(
                f"| `{rec['descendant']}` | {mark} {rec['status']} | "
                f"`{rec['recorded_hash']}` | `{rec['manifest']}` | {rec['applied_at']} |"
            )
    lines.append("")
    if drift_count:
        lines.append(
            "## Drift remediation\n\n"
            "For each DRIFT row, either:\n"
            "1. Re-apply the scaffold with `apply_dac_scaffold.py --overwrite` "
            "(accepts the current genome), or\n"
            "2. Audit what changed in the genome since the recorded hash and "
            "decide whether the descendant still expresses the intended niche.\n"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Audit DAC descendants against the current scaffold genome.")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--scaffold", type=Path, default=DEFAULT_SCAFFOLD)
    ap.add_argument("--markdown", action="store_true", help="Emit a markdown report")
    args = ap.parse_args(argv)

    if not args.scaffold.is_dir():
        print(f"error: scaffold not found: {args.scaffold}", file=sys.stderr)
        return 2
    if not args.root.is_dir():
        print(f"error: root not found: {args.root}", file=sys.stderr)
        return 2

    current_hash, records = audit(args.root, args.scaffold)
    out = render_markdown(current_hash, records) if args.markdown else render_text(current_hash, records)
    print(out)

    if any(r["status"] == "ERROR" for r in records):
        return 2
    if any(r["status"] == "DRIFT" for r in records):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

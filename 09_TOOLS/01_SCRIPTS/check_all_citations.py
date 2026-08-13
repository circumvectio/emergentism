#!/usr/bin/env python3
"""Resolve EVERY citation channel in the corpus, not just inline markdown links.

Why this exists: the 2026-08-13 census found check_links.py checks inline links
only, and that 238 of 382 unresolved paths live in the frontmatter channel
(parents / sources / depends / supersedes) — gated by nothing at all. A folder
restructure rewrites exactly those paths, so without this the damage a move does
would be invisible to the corpus's own gates.

It also distinguishes RESOLVES-TO-STUB from RESOLVES: a path that lands on a
forwarding stub is technically alive and semantically dead. Corollary C4's
authority currently resolves to a 1,290-byte stub this way.

Exit 0 only when the broken count is at or below --max-broken (default 0).
Use --baseline to record the current number, then gate a migration on it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules", ".vercel", "__pycache__"}

INLINE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
FM_KEYS = ("parents", "sources", "depends", "depends_on", "supersedes",
           "supersedes_ref", "owner_ref", "source_path", "parent")
STUB_MARKERS = ("forwarding stub", "no current semantic authority",
                "content lives in the archive", "this address was archived")
STUB_MAX_BYTES = 4096


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def fm_paths(fm: str):
    out, key = [], None
    for raw in fm.splitlines():
        line = raw.rstrip()
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"\'')
            if key in FM_KEYS and val and not val.startswith("#"):
                out.append((key, val))
            continue
        m = re.match(r"^\s+-\s+(.*)$", line)
        if m and key in FM_KEYS:
            val = m.group(1).strip().strip('"\'')
            val = val.split("#")[0].strip()
            if val:
                out.append((key, val))
    return out


def is_stub(p: Path) -> bool:
    try:
        if p.stat().st_size > STUB_MAX_BYTES:
            return False
        low = p.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return False
    return any(m in low for m in STUB_MARKERS)


def scan():
    broken, stubs, total = [], [], 0
    for md in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in md.parts):
            continue
        rel = md.relative_to(ROOT).as_posix()
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        refs = [("inline", h) for h in INLINE.findall(text)]
        refs += fm_paths(frontmatter(text))

        for channel, href in refs:
            if re.match(r"^(https?:|mailto:|#|data:)", href):
                continue
            total += 1
            cand = (md.parent / href) if not href.startswith("/") else (ROOT / href.lstrip("/"))
            try:
                cand = cand.resolve()
            except OSError:
                broken.append((rel, channel, href)); continue
            if cand.exists():
                if cand.is_file() and cand.suffix == ".md" and is_stub(cand):
                    stubs.append((rel, channel, href))
                continue
            alt = (ROOT / href).resolve()
            if alt.exists():
                continue
            broken.append((rel, channel, href))
    return total, broken, stubs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-broken", type=int, default=0)
    ap.add_argument("--baseline", type=Path)
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    total, broken, stubs = scan()
    by_channel: dict[str, int] = {}
    for _, ch, _ in broken:
        by_channel[ch] = by_channel.get(ch, 0) + 1

    print(f"citations resolved : {total - len(broken)}/{total}")
    print(f"BROKEN             : {len(broken)}")
    for ch, n in sorted(by_channel.items(), key=lambda x: -x[1]):
        print(f"    {ch:12} {n}")
    print(f"resolve to a STUB  : {len(stubs)}  (alive, semantically dead)")

    if args.json:
        args.json.write_text(json.dumps(
            {"total": total, "broken": broken, "stubs": stubs}, indent=1), encoding="utf-8")

    limit = args.max_broken
    if args.baseline and args.baseline.exists():
        limit = json.loads(args.baseline.read_text(encoding="utf-8"))["broken"]
        print(f"baseline           : {limit}")
    if args.write_baseline and args.baseline:
        args.baseline.write_text(json.dumps({"broken": len(broken), "total": total}), encoding="utf-8")
        print(f"baseline written   : {len(broken)}")
        return 0

    if len(broken) > limit:
        print(f"\nFAIL — {len(broken)} broken exceeds {limit}.")
        for r, ch, h in broken[:25]:
            print(f"   {r}  [{ch}]  ->  {h}")
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

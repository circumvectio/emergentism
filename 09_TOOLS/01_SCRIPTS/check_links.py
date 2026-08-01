#!/usr/bin/env python3
"""Fail when a Markdown link in the active corpus points at a file that is not there.

WHAT THIS REPLACED, AND WHY IT MATTERED.

The previous version was the worst kind of check: it reported safety it had never tested. It
walked `04_PWAs` — a directory that does not exist in this repository — resolved from
`os.getcwd()`, so its result also depended on where you happened to run it from. It swallowed
every exception, it had no failure path at all, and it finished by printing "Link check
complete." and exiting 0. It could not fail. Anyone reading its output would conclude the
corpus's links had been checked. Nothing had been checked.

That is the pattern this repository has written down as forbidden — never build a gate that
can pass a property it does not test — so the script now tests the property.

WHAT IT CHECKS
  · every Markdown inline link `[text](target)` in the active corpus
  · relative targets resolved against the linking file's own directory
  · absolute-looking `/path` targets resolved from the repository root
  · an `#anchor` on a local Markdown target must exist as a heading or id in that file

WHAT IT DOES NOT CHECK
  · http(s) URLs — no network by design; a link checker that reaches the network fails
    differently on every machine and blocks CI when someone else's site is down
  · 90_ARCHIVE, 91_COMPATIBILITY, 11_UPLINK, 00_HANDOFF — provenance, not authority; a dated
    receipt records where a file WAS and must not be rewritten to keep a link green
  · 12_PUBLIC_SITE — predeploy_check.py owns HTML routes and understands them; this does not
  · reference-style links, and links inside fenced code blocks are still counted (a known
    over-report; it costs false failures, never false passes)

THE BASELINE IS ZERO, AND IT IS REAL. The active corpus currently has no broken local
Markdown link. It got there by repair, not by tolerance: 14 route files linked
00_SETTLED_CANON_REGISTRY.md and 00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md as if they
were siblings when both live in 00_META/, and those were fixed. The remaining 64 misses were
all inside 11_UPLINK and 00_HANDOFF, which are excluded for the reason given at SKIP_DIRS.
Never raise BASELINE to make a commit pass; fix the link.

Usage: python3 check_links.py            (gate mode — no arguments, as gate.sh invokes it)
       python3 check_links.py --list     (print every broken link, for repair work)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SKIP_DIRS = {
    # Same scope rule check_emergentism_purity.py already applies, and for the same stated
    # reason: "Archives, compatibility stubs, public projection, session packets, handoffs,
    # and dated receipts are provenance rather than authority." A receipt written on a date
    # records where a file WAS; it is not wrong when the file later moves, and rewriting a
    # dated receipt to keep a link green would falsify the record.
    #
    # This exclusion is what lets BASELINE be a real zero. Scanning receipts produced 64
    # historical misses, and a gate carrying a 64-item baseline hides the 65th — which is
    # the one that matters.
    "90_ARCHIVE", "91_COMPATIBILITY", "12_PUBLIC_SITE",
    "11_UPLINK", "00_HANDOFF",
    ".git", ".lake", "node_modules", "__pycache__", ".vercel", ".pytest_cache",
}

# Raised only by repairing links, never to make a commit pass.
BASELINE = 0

LINK = re.compile(r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def slug(heading: str) -> str:
    s = heading.strip().lower()
    s = re.sub(r"[`*_~\[\]()]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")


def anchors_of(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    out = {slug(m.group(1)) for m in HEADING.finditer(text)}
    out |= set(re.findall(r'<a\s+[^>]*name="([^"]+)"', text))
    out |= set(re.findall(r'\bid="([^"]+)"', text))
    return out


def active_markdown() -> list[Path]:
    files = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        files.append(p)
    return sorted(files)


def resolve(src: Path, target: str) -> Path | None:
    """Resolved path, or None when the target is out of this checker's scope."""
    if target.startswith(("http://", "https://", "mailto:", "tel:", "#", "<")):
        return None
    clean = target.split("#", 1)[0]
    if not clean:
        return None
    if clean.startswith("/"):
        return (ROOT / clean.lstrip("/")).resolve()
    return (src.parent / clean).resolve()


def collect() -> tuple[list[str], int]:
    broken: list[str] = []
    checked = 0
    for src in active_markdown():
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            broken.append(f"{src.relative_to(ROOT)}: unreadable ({exc})")
            continue
        rel_src = src.relative_to(ROOT)
        for m in LINK.finditer(text):
            target = m.group("target")
            dest = resolve(src, target)
            if dest is None:
                continue
            checked += 1
            line = text[: m.start()].count("\n") + 1
            if not dest.exists():
                broken.append(f"{rel_src}:{line}: missing target -> {target}")
                continue
            frag = target.split("#", 1)[1] if "#" in target else ""
            if frag and dest.is_file() and dest.suffix == ".md":
                if slug(frag) not in anchors_of(dest):
                    broken.append(f"{rel_src}:{line}: no such anchor '#{frag}' in {target}")
    return broken, checked


def main(argv: list[str]) -> int:
    broken, checked = collect()

    if "--list" in argv:
        for b in broken:
            print(b)
        print(f"\n{len(broken)} broken of {checked} local links")
        return 0

    if len(broken) > BASELINE:
        print("LINKS: FAIL")
        print(f"- {len(broken)} broken local links; baseline is {BASELINE}. A link broke.")
        for b in broken[:15]:
            print(f"  {b}")
        if len(broken) > 15:
            print(f"  ... and {len(broken) - 15} more — run: python3 check_links.py --list")
        return 1

    print(
        f"LINKS: PASS ({checked} local Markdown links resolved; {len(broken)} broken, "
        f"baseline {BASELINE})"
    )
    print(
        "  scope: local Markdown links only. NOT http(s) URLs (no network by design), NOT "
        "90_ARCHIVE / 91_COMPATIBILITY / 11_UPLINK / 00_HANDOFF (provenance — a dated "
        "receipt records where a file WAS), NOT 12_PUBLIC_SITE (predeploy_check.py owns "
        "HTML routes)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

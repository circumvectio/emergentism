#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_contradiction_census.py — instrument the retired Titan infix census.

The retired Titan infix ``⊙ = • × ○`` is a type error: the realm mark presented
as a product of boundary marks. The K2 disposition (WO-D1, 2026-07-19) withdrew
it. This script is the *instrumented* count — not a one-off grep in a wave
receipt — so the next reader can recompute and audit the headline metric for
the rungs.

CATEGORIES
----------
- **Total** — every pattern hit across the 01_EMERGENTISM tree.
- **Live** — pattern hits, excluding any path whose segments contain
  ``90_ARCHIVE`` or ``91_COMPATIBILITY`` (K3 archive-first applies at any depth).
- **Public site** — pattern hits under ``12_PUBLIC_SITE/``, live.
- **HTML pages in public site** — ``*.html`` pattern hits under
  ``12_PUBLIC_SITE/``, live.
- **HTML as live doctrinal use** — HTML hits that are NOT meta-references.
  Meta-references cite the pattern as withdrawn/retired/swept/replaced, or
  live in corrections/, archive/, _plans/, or rung paths.

TARGETS (2026-08-06)
--------------------
- 0 live
- 0 public site
- 0 HTML-as-doctrinal-use

EXIT CODES
----------
- 0  all live counts at-or-below target (PASS)
- 1  any count exceeds target (FAIL)
- 2  the script itself errored

USAGE
-----
    python3 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
    python3 09_TOOLS/01_SCRIPTS/check_contradiction_census.py /path/to/01_EMERGENTISM
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# The retired Titan infix. Per the K2 disposition (WO-D1, 2026-07-19) this is
# a type error: the realm mark presented as a product of boundary marks. The
# pattern allows both Unicode × and ASCII * between the boundary marks, since
# both have appeared in historical surfaces.
RETIRED_TITAN_INFIX = re.compile(r"⊙\s*=\s*•\s*(?:×|\*)\s*○")

# K3 archive-first exclusions. Archive is provenance, not doctrine, at any
# depth — including archives nested under 12_PUBLIC_SITE/ (the public site
# carries its own 90_ARCHIVE/ sub-tree for tool noise).
ARCHIVE_PARTS = ("90_ARCHIVE", "91_COMPATIBILITY")

# The registered public-site root, per the VMOSK-A per Project directive.
PUBLIC_SITE_ROOT = "12_PUBLIC_SITE"

# Corpus scan extensions. Same set used by check_foundation.py and
# demand_census.py: markdown + HTML for doctrinal surfaces, Python + JSON/YAML
# for tooling that names the pattern.
SCAN_EXTENSIONS = (".md", ".html", ".py", ".json", ".yaml", ".yml")

# Meta-reference classification. A file is a meta-reference (not a live
# doctrinal use) if EITHER its path carries a corrections/archive/plans/rung
# subdir OR its body carries an explicit retirement marker within ±300
# characters of any pattern match. The two heuristics are independent and
# each is sufficient to mark a file as meta.
META_PATH_MARKERS = (
    "corrections",
    "archive",
    "_plans",
    "rung",
)
META_BODY_MARKERS = (
    "withdrawn",
    "retired",
    "deprecated",
    "killed",
    "swept",
    "needs repair",
    "previous form",
    "old form",
    "replaced with",
    "ill-typed",
    "type error",
    "no surviving candidate",
    "disposition",
    "wdo-d1",
)

# Top-N cap for the scannable file list. Full lists are reproducible from the
# script + a re-run; the report keeps to the 10 most useful for the eye.
TOP_N = 10


def _ict_now() -> datetime:
    """Return the current wall-clock in ICT (UTC+7, no DST)."""
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+

        return datetime.now(ZoneInfo("Asia/Bangkok"))
    except ImportError:  # pragma: no cover — pre-3.9 fallback
        return datetime.now(timezone(timedelta(hours=7)))


def now_ict() -> str:
    """Format the current time in ICT as ``YYYY-MM-DD HH:MM:SS ICT``."""
    return _ict_now().strftime("%Y-%m-%d %H:%M:%S ICT")


def script_root() -> Path:
    """Resolve the 01_EMERGENTISM root, defaulting to the script's grandparent."""
    if len(sys.argv) > 1 and sys.argv[1]:
        return Path(sys.argv[1]).resolve()
    return Path(__file__).resolve().parents[2]


def is_archived(rel: Path) -> bool:
    """K3 archive-first: any path segment in ARCHIVE_PARTS disqualifies a file."""
    return any(part in rel.parts for part in ARCHIVE_PARTS)


def is_public(rel: Path) -> bool:
    """A file is in the public site iff its first path segment is the public root."""
    return bool(rel.parts) and rel.parts[0] == PUBLIC_SITE_ROOT


def is_html(rel: Path) -> bool:
    """A file is HTML iff its extension is .html (case-insensitive)."""
    return rel.suffix.lower() == ".html"


def is_meta_reference(rel: Path, body: str) -> bool:
    """A meta-reference presents the pattern as withdrawn/retired/swept.

    Either the path or the body's local neighbourhood near a match is enough.
    """
    lowered_path = rel.as_posix().lower()
    if any(marker in lowered_path for marker in META_PATH_MARKERS):
        return True
    lowered_body = body.lower()
    for match in RETIRED_TITAN_INFIX.finditer(body):
        window_start = max(0, match.start() - 300)
        window_end = min(len(body), match.end() + 300)
        window = lowered_body[window_start:window_end]
        if any(marker in window for marker in META_BODY_MARKERS):
            return True
    return False


def scan(root: Path) -> dict[str, list[Path]]:
    """Walk the root tree and return categorised pattern hits.

    Returns a dict with sorted, root-relative paths for each category:

    - ``total`` — every pattern hit
    - ``live`` — pattern hits, K3 archive-first applied at any depth
    - ``public`` — pattern hits under 12_PUBLIC_SITE/, live
    - ``public_html`` — ``*.html`` in 12_PUBLIC_SITE/, live
    - ``public_html_doctrinal`` — HTML that is NOT a meta-reference
    """
    total: list[Path] = []
    live: list[Path] = []
    public: list[Path] = []
    public_html: list[Path] = []
    public_html_doctrinal: list[Path] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not RETIRED_TITAN_INFIX.search(body):
            continue
        rel = path.relative_to(root)
        total.append(rel)
        if is_archived(rel):
            continue  # K3: archive-first at any depth
        live.append(rel)
        if not is_public(rel):
            continue
        public.append(rel)
        if not is_html(rel):
            continue
        public_html.append(rel)
        if not is_meta_reference(rel, body):
            public_html_doctrinal.append(rel)

    return {
        "total": total,
        "live": live,
        "public": public,
        "public_html": public_html,
        "public_html_doctrinal": public_html_doctrinal,
    }


def read_body(root: Path, rel: Path) -> str:
    """Re-read a file for inline classification (small files, audit-only)."""
    try:
        return (root / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def render_report(root: Path, counts: dict[str, list[Path]], timestamp: str) -> tuple[str, int]:
    """Render the scannable report and return ``(text, exit_code)``."""
    targets = {"live": 0, "public": 0, "html_doctrinal": 0}
    actual = {
        "live": len(counts["live"]),
        "public": len(counts["public"]),
        "html_doctrinal": len(counts["public_html_doctrinal"]),
    }
    exceeds = {k: v for k, v in actual.items() if v > targets[k]}
    status = "PASS" if not exceeds else "FAIL"
    exit_code = 0 if not exceeds else 1

    lines: list[str] = []
    lines.append(f"CONTRADICTION CENSUS — {timestamp}")
    lines.append("")
    lines.append(f"Root: {root}")
    lines.append(f"Pattern: ⊙\\s*=\\s*•\\s*(?:×|\\*)\\s*○  (retired Titan infix)")
    lines.append("")
    lines.append(f"Total files in 01_EMERGENTISM (pattern hits): {len(counts['total'])}")
    lines.append(f"Live files (exclude 90_ARCHIVE, 91_COMPATIBILITY): {len(counts['live'])}")
    lines.append(f"Public site (12_PUBLIC_SITE/): {len(counts['public'])}")
    lines.append(f"HTML pages in public site: {len(counts['public_html'])}")
    lines.append(f"HTML pages as live doctrinal use: {len(counts['public_html_doctrinal'])}")
    lines.append("")
    lines.append(
        f"Targets: {targets['live']} live / "
        f"{targets['public']} public site / "
        f"{targets['html_doctrinal']} HTML-as-doctrinal-use"
    )
    lines.append(
        f"Status: {status}  "
        f"(live={actual['live']}, public={actual['public']}, "
        f"html-doctrinal={actual['html_doctrinal']})"
    )
    lines.append("")

    if counts["public_html"]:
        lines.append("HTML files in public site matching the pattern:")
        for rel in counts["public_html"]:
            meta = is_meta_reference(rel, read_body(root, rel))
            tag = "META" if meta else "DOCTRINAL"
            lines.append(f"  [{tag}] {rel.as_posix()}")
        lines.append("")

    top = counts["total"][:TOP_N]
    if top:
        lines.append(f"Top files (top {TOP_N} by path):")
        for rel in top:
            lines.append(f"  {rel.as_posix()}")
        if len(counts["total"]) > TOP_N:
            lines.append(
                f"  ... and {len(counts['total']) - TOP_N} more "
                f"(re-run this script to enumerate the full set)"
            )
        lines.append("")

    lines.append(f"CENSUS: {status}  (exit {exit_code})")
    return "\n".join(lines), exit_code


def main() -> int:
    try:
        root = script_root()
        if not root.is_dir():
            print(f"ERROR: root not a directory: {root}", file=sys.stderr)
            return 2
        counts = scan(root)
    except Exception as exc:  # noqa: BLE001 — gate must fail loudly, not silently
        print(f"ERROR: contradiction census failed: {exc}", file=sys.stderr)
        return 2

    report, exit_code = render_report(root, counts, now_ict())
    print(report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Mark frozen generated-library pages as historical projections, deterministically."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SITE = Path(__file__).resolve().parent
MANIFEST = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))
MARKER = "data-frozen-library-boundary=\"2026-07-22\""
BANNER = (
    '<aside data-frozen-library-boundary="2026-07-22" role="note" '
    'style="padding:.75rem 1rem;border-bottom:1px solid rgba(255,235,59,.35);'
    'background:#17150a;color:#d8d2bd;font:600 .76rem/1.5 ui-monospace,monospace">'
    '[D] Frozen library projection — preserved for provenance, noindex, and excluded from current retrieval. '
    'Where it conflicts with the <a href="/dimensions/" style="color:#ffeb3b">dimension-first spine</a> '
    'or a named source owner, the current owner governs.</aside>'
)


def paths() -> list[Path]:
    out: list[Path] = []
    for root in MANIFEST["frozenLibraryRoots"]:
        base = SITE / root
        if base.is_dir():
            out.extend(sorted(base.rglob("*.html")))
    return out


def desired(text: str) -> str:
    if MARKER in text:
        return text
    return re.sub(r"(<body\b[^>]*>)", r"\1\n" + BANNER, text, count=1, flags=re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift: list[str] = []
    for path in paths():
        current = path.read_text(encoding="utf-8", errors="replace")
        target = desired(current)
        if current == target:
            continue
        if args.check:
            drift.append(str(path.relative_to(SITE)))
        else:
            path.write_text(target, encoding="utf-8")
    if drift:
        print("frozen-library boundary drift:")
        print("\n".join(drift))
        return 1
    print(f"frozen-library boundary: {'clean' if args.check else 'applied'} ({len(paths())} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

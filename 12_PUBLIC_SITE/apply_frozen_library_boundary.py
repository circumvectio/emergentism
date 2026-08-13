#!/usr/bin/env python3
"""Mark frozen generated-library pages as historical projections, deterministically."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SITE = Path(__file__).resolve().parent
MANIFEST = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))
WITHHELD = json.loads((SITE / "withheld-routes.json").read_text(encoding="utf-8"))
MARKER = "data-frozen-library-boundary=\"2026-07-22\""
ROBOTS = '<meta name="robots" content="noindex, follow">'
BANNER = (
    '<aside data-frozen-library-boundary="2026-07-22" role="note" '
    'style="padding:.75rem 1rem;border-bottom:1px solid rgba(255,235,59,.35);'
    'background:#17150a;color:#d8d2bd;font:600 .76rem/1.5 ui-monospace,monospace">'
    '[D] Frozen library projection — provenance only, noindex, not current retrieval. '
    'It does not warrant its claims. Current nectar sits at '
    '<a href="/amrita/" style="color:#ffeb3b">/amrita/</a> and '
    '<a href="/spark/" style="color:#ffeb3b">/spark/</a>. '
    'Where this attic conflicts with the <a href="/dimensions/" style="color:#ffeb3b">dimension-first spine</a> '
    'or a named source owner, the current owner governs.</aside>'
)


def paths() -> list[Path]:
    out: set[Path] = set()
    withheld = {row["artifact"] for row in WITHHELD["artifacts"]}
    provisional = {rel for rel in MANIFEST.get("declaredProvisional", {}).get("routes", [])}
    for root in MANIFEST["frozenLibraryRoots"]:
        base = SITE / root
        if base.is_dir():
            out.update(base.rglob("*.html"))
    out.update(SITE / rel for rel in MANIFEST.get("frozenLegacySurfaces", []))
    return sorted(
        path for path in out
        if path.is_file()
        and path.relative_to(SITE).as_posix() not in withheld
        and path.relative_to(SITE).as_posix() not in provisional
    )


def desired(text: str) -> str:
    target = text
    robots = re.compile(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>', re.IGNORECASE)
    if robots.search(target):
        target = robots.sub(ROBOTS, target, count=1)
    else:
        target = re.sub(r"(<head\b[^>]*>)", r"\1\n" + ROBOTS, target, count=1, flags=re.IGNORECASE)
    if MARKER in target:
        target = re.sub(
            r"<aside\b[^>]*data-frozen-library-boundary=\"2026-07-22\"[^>]*>.*?</aside>",
            BANNER,
            target,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    else:
        target = re.sub(r"(<body\b[^>]*>)", r"\1\n" + BANNER, target, count=1, flags=re.IGNORECASE)
    return target


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

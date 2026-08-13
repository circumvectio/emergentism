#!/usr/bin/env python3
"""Apply the frozen-library and exact public-link boundaries deterministically."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

from predeploy_check import is_vercel_ignored, load_vercelignore_patterns


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
FROZEN_BANNER = re.compile(
    r'<aside\b[^>]*\bdata-frozen-library-boundary=["\'][^"\']+["\'][^>]*>.*?</aside>\s*',
    re.IGNORECASE | re.DOTALL,
)
META_TAG = re.compile(r"<meta\b[^>]*>", re.IGNORECASE)
WITHHELD_ROUTE_KEYS = {
    route.rstrip("/")
    for row in WITHHELD["artifacts"]
    for route in row.get("publicRoutes", [])
}
ANCHOR_HREF = re.compile(r"(<a\b[^>]*\bhref=)([\"'])([^\"']*)(\2)", re.IGNORECASE)
DECLARED_CURRENT_OR_PROVISIONAL = {
    *MANIFEST.get("currentSurfaces", []),
    *MANIFEST.get("declaredProvisional", {}).get("routes", []),
}


def frozen_paths() -> set[Path]:
    out: set[Path] = set()
    withheld = {row["artifact"] for row in WITHHELD["artifacts"]}
    provisional = {rel for rel in MANIFEST.get("declaredProvisional", {}).get("routes", [])}
    for root in MANIFEST["frozenLibraryRoots"]:
        base = SITE / root
        if base.is_dir():
            out.update(base.rglob("*.html"))
    out.update(SITE / rel for rel in MANIFEST.get("frozenLegacySurfaces", []))
    return {
        path for path in out
        if path.is_file()
        and path.relative_to(SITE).as_posix() not in withheld
        and path.relative_to(SITE).as_posix() not in provisional
    }


def paths() -> list[Path]:
    """Every deployable HTML page whose anchors can affect the public journey."""

    withheld = {row["artifact"] for row in WITHHELD["artifacts"]}
    excluded = {".git", ".vercel", "node_modules", "book-pwa", "partials", "_archive", "90_ARCHIVE"}
    patterns = load_vercelignore_patterns() or []
    out: set[Path] = set()
    for path in SITE.rglob("*"):
        if path.suffix.lower() not in {".html", ".htm"}:
            continue
        rel = path.relative_to(SITE).as_posix()
        if any(part in excluded for part in path.relative_to(SITE).parts):
            continue
        if (
            rel in withheld
            or rel == "historical-boundary/index.html"
            or is_vercel_ignored(rel, patterns)
        ):
            continue
        out.add(path)
    return sorted(out)


def _targets_withheld_artifact(page: Path, href: str) -> bool:
    """Whether an in-site anchor points at an exact withheld public route."""

    parsed = urlsplit(href)
    if parsed.netloc and parsed.hostname not in {"emergentism.org", "www.emergentism.org"}:
        return False
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return False
    if not parsed.path:
        return False
    if parsed.path.startswith("/"):
        route = posixpath.normpath(parsed.path)
    else:
        route = posixpath.normpath(
            posixpath.join(page.relative_to(SITE).parent.as_posix(), parsed.path)
        )
    route = "/" + route.lstrip("/")
    if route.endswith("/index.html"):
        route = route[: -len("index.html")]
    return route.rstrip("/") in WITHHELD_ROUTE_KEYS


def desired(text: str, page: Path, *, frozen: bool) -> str:
    target = text
    relative = page.relative_to(SITE).as_posix()
    if frozen:
        robots = re.compile(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>', re.IGNORECASE)
        if robots.search(target):
            target = robots.sub(ROBOTS, target, count=1)
        else:
            target = re.sub(r"(<head\b[^>]*>)", r"\1\n" + ROBOTS, target, count=1, flags=re.IGNORECASE)
        if MARKER in target:
            target = FROZEN_BANNER.sub(BANNER, target, count=1)
        else:
            target = re.sub(r"(<body\b[^>]*>)", r"\1\n" + BANNER, target, count=1, flags=re.IGNORECASE)
    elif relative in DECLARED_CURRENT_OR_PROVISIONAL:
        # A page declared current or provisional has affirmative indexability.
        # Old frozen banners/robots tags cannot persist beside that declaration;
        # retain an explicit index/follow tag if the page already supplies one.
        target = FROZEN_BANNER.sub("", target)

        def remove_hidden_robots(match: re.Match[str]) -> str:
            tag = match.group(0)
            if not re.search(r'\bname=["\']robots["\']', tag, re.IGNORECASE):
                return tag
            if re.search(r'\bcontent=["\'][^"\']*\b(?:noindex|none)\b', tag, re.IGNORECASE):
                return ""
            return tag

        target = META_TAG.sub(remove_hidden_robots, target)

    # Frozen pages remain viewable as provenance, but no deployed page may use
    # its old navigation to revive a route withheld by the semantic firewall.
    # The exact public boundary preserves the explanation and the original
    # bytes remain in repository custody; this only corrects live link targets.
    def replace_anchor(match: re.Match[str]) -> str:
        prefix, quote, href, _ = match.groups()
        if not _targets_withheld_artifact(page, href):
            return match.group(0)
        return f'{prefix}{quote}/historical-boundary/{quote}'

    target = ANCHOR_HREF.sub(replace_anchor, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift: list[str] = []
    frozen = frozen_paths()
    for path in paths():
        current = path.read_text(encoding="utf-8", errors="replace")
        target = desired(current, path, frozen=path in frozen)
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
    print(
        "public link boundary: "
        f"{'clean' if args.check else 'applied'} "
        f"({len(paths())} public pages; {len(frozen)} frozen-library projections)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

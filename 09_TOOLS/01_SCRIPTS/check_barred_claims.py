#!/usr/bin/env python3
"""Check claim cards, active book sources, and every deployable public page."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from claim_policy import violations


ROOT = Path(__file__).resolve().parents[2]
CARD_DIR = ROOT / "00_META/claim_cards"
BOOK_MANIFEST = ROOT / "13_BOOKS/book-manifest.json"
PUBLIC_DIR = ROOT / "12_PUBLIC_SITE"
PUBLIC_MANIFEST = PUBLIC_DIR / "public_semantic_parity.json"
if str(PUBLIC_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLIC_DIR))
from predeploy_check import is_vercel_ignored, load_vercelignore_patterns


def _card_and_book_paths() -> list[Path]:
    paths = sorted(CARD_DIR.glob("*.yaml"))
    manifest = json.loads(BOOK_MANIFEST.read_text(encoding="utf-8"))
    for work in manifest["works"]:
        if work["release_state"] != "source_active_projection_review_open":
            continue
        for source_record in work["historical_sources"]:
            paths.append((BOOK_MANIFEST.parent / source_record["path"]).resolve())
    paths.extend(sorted((ROOT / "13_BOOKS").rglob("*.md")))
    return sorted(set(paths))


def _declared_public_paths() -> list[Path]:
    manifest = json.loads(PUBLIC_MANIFEST.read_text(encoding="utf-8"))
    current = manifest.get("currentSurfaces", [])
    provisional = manifest.get("declaredProvisional", {}).get("routes", [])
    if not isinstance(current, list) or not isinstance(provisional, list):
        raise ValueError("public lifecycle manifests must contain path lists")
    return [PUBLIC_DIR / rel for rel in current + provisional]


def _deployable_public_html_paths() -> list[Path]:
    """Use the release gate's exact ignore semantics, never a weaker glob."""

    patterns = load_vercelignore_patterns()
    if patterns is None:
        raise ValueError(".vercelignore is required to determine public claim scope")
    return sorted(
        path
        for path in PUBLIC_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".html", ".htm"}
        and not is_vercel_ignored(path.relative_to(PUBLIC_DIR).as_posix(), patterns)
    )


def _public_paths() -> list[Path]:
    """Declared non-HTML surfaces plus every HTML artifact Vercel can receive."""

    return sorted(set(_declared_public_paths()) | set(_deployable_public_html_paths()))


def check(scope: str) -> list[str]:
    paths: list[Path] = []
    if scope in {"cards", "all"}:
        paths.extend(_card_and_book_paths())
    if scope in {"public", "all"}:
        paths.extend(_public_paths())
    errors: list[str] = []
    for path in sorted(set(paths)):
        if not path.is_file():
            errors.append(f"{path.relative_to(ROOT)}:0:missing-current-surface:missing file")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for rule, line, snippet in violations(text):
            errors.append(f"{path.relative_to(ROOT)}:{line}:{rule}:{snippet}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("cards", "public", "all"), default="all")
    args = parser.parse_args(argv)
    errors = check(args.scope)
    if errors:
        print("BARRED CLAIMS: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"BARRED CLAIMS: PASS ({args.scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

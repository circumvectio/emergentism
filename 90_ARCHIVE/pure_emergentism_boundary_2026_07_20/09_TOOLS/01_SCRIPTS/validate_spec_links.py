#!/usr/bin/env python3
"""
validate_spec_links.py — Check internal markdown links in the spec corpus.

Usage:
    python validate_spec_links.py [path...]

Defaults to checking:
    - 03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/
    - SKYZAI_COM/
    - EMERGENTISM_ORG/11_UPLINK/

Exit codes:
    0 = all links valid
    1 = broken links found
"""

import re
import sys
from pathlib import Path

# Default paths to scan
DEFAULT_PATHS = [
    Path("03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON"),
    Path("SKYZAI_COM"),
    Path("EMERGENTISM_ORG/11_UPLINK"),
]

# Regex for markdown links: [text](path)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Regex for markdown image links: ![alt](path)
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def resolve_link(link_target: str, source_file: Path) -> Path | None:
    """Resolve a markdown link target relative to the source file."""
    if link_target.startswith("http://") or link_target.startswith("https://"):
        return None  # External link, skip
    if link_target.startswith("#"):
        return None  # Anchor-only link, skip
    if link_target.startswith("/"):
        # Absolute from repo root
        return Path(link_target.lstrip("/"))
    # Relative to source file
    return (source_file.parent / link_target).resolve()


def check_file(filepath: Path) -> list[tuple[str, Path, str]]:
    """Check all links in a single markdown file."""
    broken = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        broken.append((str(filepath), filepath, f"read error: {e}"))
        return broken

    for match in LINK_RE.finditer(content):
        text, target = match.groups()
        resolved = resolve_link(target, filepath)
        if resolved is None:
            continue
        # Strip anchor
        resolved_path = Path(str(resolved).split("#")[0])
        if not resolved_path.exists():
            broken.append((text, resolved_path, "missing file"))

    for match in IMG_RE.finditer(content):
        alt, target = match.groups()
        resolved = resolve_link(target, filepath)
        if resolved is None:
            continue
        if not resolved.exists():
            broken.append((alt or "image", resolved, "missing image"))

    return broken


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_PATHS

    all_broken = []
    files_checked = 0
    links_checked = 0

    for base in paths:
        if not base.exists():
            print(f"Warning: path does not exist: {base}")
            continue
        for filepath in base.rglob("*.md"):
            files_checked += 1
            broken = check_file(filepath)
            links_checked += len(broken)
            for text, resolved, reason in broken:
                all_broken.append((filepath, text, resolved, reason))

    if all_broken:
        print(f"\n{len(all_broken)} broken link(s) found across {files_checked} files:\n")
        for filepath, text, resolved, reason in all_broken:
            print(f"  {filepath}")
            print(f"    [{text}] -> {resolved} ({reason})")
        return 1
    else:
        print(f"✅ All links valid across {files_checked} markdown files.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

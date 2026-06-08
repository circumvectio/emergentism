#!/usr/bin/env python3
"""
neuter_broken_archive_links.py — Remove hyperlink syntax from broken archive links.

Strategy:
- For each broken internal link in archive files, replace `[text](path)` with `text [↯]`
- For each broken image link, replace `![alt](path)` with `![alt — missing]`
- This preserves the textual reference while removing the dangling pointer.
- External links and anchor-only links are preserved.
"""

import re
import sys
from pathlib import Path

ARCHIVE_PATHS = [
    Path("08_ARCHIVE"),
    Path("EMERGENTISM_ORG/11_UPLINK/90_ARCHIVE"),
]

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def resolve_link(link_target: str, source_file: Path) -> Path | None:
    if link_target.startswith("http://") or link_target.startswith("https://"):
        return None
    if link_target.startswith("#"):
        return None
    if link_target.startswith("/"):
        return Path(link_target)
    return (source_file.parent / link_target).resolve()


def neuter_file(filepath: Path) -> dict:
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e), "links_neutered": 0, "images_neutered": 0}

    original = content
    links_neutered = 0
    images_neutered = 0
    changes = []

    def link_replacer(match):
        nonlocal links_neutered
        text = match.group(1)
        target = match.group(2)
        resolved = resolve_link(target, filepath)
        if resolved is None:
            return match.group(0)
        resolved_path = Path(str(resolved).split("#")[0])
        if resolved_path.exists():
            return match.group(0)
        links_neutered += 1
        changes.append(f"  [{text}] -> {target}")
        return f"{text} [↯]"

    def img_replacer(match):
        nonlocal images_neutered
        alt = match.group(1)
        target = match.group(2)
        resolved = resolve_link(target, filepath)
        if resolved is None:
            return match.group(0)
        if resolved.exists():
            return match.group(0)
        images_neutered += 1
        changes.append(f"  ![{alt}] -> {target}")
        return f"![{alt} — missing]"

    content = LINK_RE.sub(link_replacer, content)
    content = IMG_RE.sub(img_replacer, content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return {
        "links_neutered": links_neutered,
        "images_neutered": images_neutered,
        "changes": changes,
        "error": None,
    }


def main() -> int:
    total_links = 0
    total_images = 0
    files_modified = 0
    files_checked = 0

    for base in ARCHIVE_PATHS:
        if not base.exists():
            continue
        for filepath in base.rglob("*.md"):
            files_checked += 1
            report = neuter_file(filepath)
            if report.get("error"):
                print(f"ERROR reading {filepath}: {report['error']}")
                continue
            if report["links_neutered"] > 0 or report["images_neutered"] > 0:
                files_modified += 1
                total_links += report["links_neutered"]
                total_images += report["images_neutered"]
                print(f"NEUTERED {filepath} ({report['links_neutered']} links, {report['images_neutered']} images)")
                for change in report["changes"]:
                    print(change)

    print(f"\n{'='*60}")
    print(f"Archive link neutering complete.")
    print(f"  Files checked:      {files_checked}")
    print(f"  Files modified:     {files_modified}")
    print(f"  Links neutered:     {total_links}")
    print(f"  Images neutered:    {total_images}")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

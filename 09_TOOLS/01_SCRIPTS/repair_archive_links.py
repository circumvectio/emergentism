#!/usr/bin/env python3
"""
repair_archive_links.py — Systematic link repair for archived/legacy files.

Strategy:
1. Scan archive directories for markdown files with broken internal links.
2. For each broken link, attempt path resolution via known reorganization patterns.
3. Replace stale relative references with corrected paths where target exists.
4. Report: fixed, unfixable (target truly gone), and manual-review required.

Patterns handled:
- /Users/Yves/Documents/01_FRAMEWORK/... → 08_ARCHIVE/01_FRAMEWORK/...
- /Users/Yves/Documents/02_ORGANISM/... → 08_ARCHIVE/organism_legacy/...
- /Users/Yves/Documents/Emergence_22_04/01_FRAMEWORK/... → 08_ARCHIVE/01_FRAMEWORK/...
- ../../01_FRAMEWORK/... from intake_legacy → ../../../01_FRAMEWORK/... or 08_ARCHIVE/...
"""

import re
import sys
from pathlib import Path

ARCHIVE_ROOT = Path("08_ARCHIVE")
REPO_ROOT = Path("/Users/Yves/Documents/Emergence_22_04")

# Known reorganization mappings: old_prefix -> new_prefix (relative to repo root)
REORG_MAP = {
    "01_FRAMEWORK/": "08_ARCHIVE/01_FRAMEWORK/",
    "02_ORGANISM/P-SCORES.md": "08_ARCHIVE/organism_legacy/P-SCORES.md",
    "02_ORGANISM/ORGANISM_RUNTIME_TRUTH.md": "08_ARCHIVE/organism_legacy/ORGANISM_RUNTIME_TRUTH.md",
    "02_ORGANISM/01_ENTITIES/AATC_KSA/": "08_ARCHIVE/02_ORGANISM/01_ENTITIES/AATC_KSA/",
    "02_ORGANISM/02_ORGANS/Skyzai/": "08_ARCHIVE/organism_legacy/02_ORGANS/Skyzai/",
    "02_ORGANISM/04_PROJECT_MANAGEMENT/00_CANON/": "08_ARCHIVE/organism_legacy/04_PROJECT_MANAGEMENT/00_CANON/",
    "03_UPLINK/": "03_UPLINK/",  # Some uplink files still live here
    "00_INTAKE/PROCESSED/": "08_ARCHIVE/intake_processed/",
}

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def resolve_link(link_target: str, source_file: Path) -> Path | None:
    if link_target.startswith("http://") or link_target.startswith("https://"):
        return None
    if link_target.startswith("#"):
        return None
    if link_target.startswith("/"):
        # Absolute path — could be from repo root or system root
        if link_target.startswith("/Users/"):
            # macOS absolute path from repo root
            return Path(link_target)
        return (REPO_ROOT / link_target.lstrip("/")).resolve()
    return (source_file.parent / link_target).resolve()


def attempt_fix(resolved: Path, source_file: Path) -> str | None:
    """Try to find an alternative path for a broken link. Returns new target string or None."""
    resolved_str = str(resolved)

    # Determine suffix relative to repo root
    suffix = None
    if resolved_str.startswith("/Users/Yves/Documents/Emergence_22_04/"):
        suffix = resolved_str.removeprefix("/Users/Yves/Documents/Emergence_22_04/")
    elif resolved_str.startswith("/Users/Yves/Documents/01_") or resolved_str.startswith("/Users/Yves/Documents/02_") or resolved_str.startswith("/Users/Yves/Documents/03_"):
        # Old absolute paths that didn't include repo name
        suffix = resolved_str.removeprefix("/Users/Yves/Documents/")
    else:
        try:
            suffix = str(resolved.relative_to(REPO_ROOT))
        except ValueError:
            pass

    if not suffix:
        return None

    # Try reorganization mappings
    for old_prefix, new_prefix in REORG_MAP.items():
        if suffix.startswith(old_prefix):
            candidate = REPO_ROOT / new_prefix / suffix.removeprefix(old_prefix)
            if candidate.exists():
                # Compute relative path from source to candidate
                try:
                    source_rel = source_file.parent.relative_to(REPO_ROOT)
                    target_rel = Path(new_prefix) / suffix.removeprefix(old_prefix)
                    up = "../" * len(source_rel.parts)
                    return up + str(target_rel)
                except ValueError:
                    return str(candidate.relative_to(REPO_ROOT))

    # Check if the file exists at original path in archive
    archive_candidate = REPO_ROOT / "08_ARCHIVE" / suffix
    if archive_candidate.exists():
        try:
            source_rel = source_file.parent.relative_to(REPO_ROOT)
            target_rel = Path("08_ARCHIVE") / suffix
            up = "../" * len(source_rel.parts)
            return up + str(target_rel)
        except ValueError:
            return str(archive_candidate.relative_to(REPO_ROOT))

    return None


def repair_file(filepath: Path) -> dict:
    """Repair links in a single file. Returns report dict."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e), "fixed": 0, "unfixable": 0}

    original = content
    fixed_count = 0
    unfixable_count = 0
    changes = []

    def replacer(match, kind="link"):
        nonlocal fixed_count, unfixable_count
        text_or_alt = match.group(1)
        target = match.group(2)
        resolved = resolve_link(target, filepath)
        if resolved is None:
            return match.group(0)
        resolved_path = Path(str(resolved).split("#")[0])
        if resolved_path.exists():
            return match.group(0)

        fix = attempt_fix(resolved, filepath)
        if fix:
            fixed_count += 1
            changes.append(f"  [{text_or_alt}] {target} -> {fix}")
            return f"{match.group(0)[0]}[{text_or_alt}]({fix})"
        else:
            unfixable_count += 1
            return match.group(0)

    content = LINK_RE.sub(lambda m: replacer(m, "link"), content)
    content = IMG_RE.sub(lambda m: replacer(m, "img"), content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return {
        "fixed": fixed_count,
        "unfixable": unfixable_count,
        "changes": changes,
        "error": None,
    }


def main() -> int:
    archive_paths = [
        Path("08_ARCHIVE"),
        Path("EMERGENTISM_ORG/11_UPLINK/90_ARCHIVE"),
    ]

    total_fixed = 0
    total_unfixable = 0
    files_modified = 0
    files_checked = 0

    for base in archive_paths:
        if not base.exists():
            continue
        for filepath in base.rglob("*.md"):
            files_checked += 1
            report = repair_file(filepath)
            if report.get("error"):
                print(f"ERROR reading {filepath}: {report['error']}")
                continue
            if report["fixed"] > 0:
                files_modified += 1
                total_fixed += report["fixed"]
                print(f"FIXED {filepath} ({report['fixed']} links)")
                for change in report["changes"]:
                    print(change)
            total_unfixable += report["unfixable"]

    print(f"\n{'='*60}")
    print(f"Archive link repair complete.")
    print(f"  Files checked:    {files_checked}")
    print(f"  Files modified:   {files_modified}")
    print(f"  Links fixed:      {total_fixed}")
    print(f"  Links unfixable:  {total_unfixable}")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

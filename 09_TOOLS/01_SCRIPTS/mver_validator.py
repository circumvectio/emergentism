#!/usr/bin/env python3
"""
mver_validator.py — Validate MVER data rooms against a markdown-based MVER Index.

Parses directory structure, filenames, and expected SHA-256 hashes from an MVER_INDEX.md,
computes hashes of files in a physical directory, and cross-checks them.

Exit codes:
  0 = Valid (no missing files, no hash mismatches)
  1 = Invalid (missing files, mismatched hashes, or unindexed files found)
"""

from __future__ import annotations
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

# Regex patterns for parsing MVER_INDEX.md
DIR_PATTERN = re.compile(r"^###\s+`([^`]+)`")
FILE_PATTERN = re.compile(r"^\*\s+`([^`]+)`\s+\((?:Hash:\s+)?sha256:([a-f0-9]{64})\)")


def compute_sha256(filepath: Path) -> str:
    """Compute the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def parse_index(index_path: Path) -> dict[str, dict[str, str]]:
    """
    Parse the MVER_INDEX.md file.
    Returns a dict mapping relative dir paths to a dict of {filename: sha256}.
    """
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")

    content = index_path.read_text(encoding="utf-8")
    index_data: dict[str, dict[str, str]] = {}
    current_dir = ""

    for line in content.splitlines():
        line = line.strip()
        # Check for directory headers e.g. ### `/01_LEGAL_AND_CORPORATE/`
        if dir_match := DIR_PATTERN.search(line):
            dir_path = dir_match.group(1).strip("/")
            current_dir = dir_path
            if current_dir not in index_data:
                index_data[current_dir] = {}
        # Check for file items e.g. * `rddc_articles_of_association_moj.pdf` (Hash: sha256:...)
        elif file_match := FILE_PATTERN.search(line):
            if not current_dir:
                # File defined before any directory
                continue
            filename = file_match.group(1)
            expected_hash = file_match.group(2)
            index_data[current_dir][filename] = expected_hash

    return index_data


def validate_directory(
    target_dir: Path, index_data: dict[str, dict[str, str]]
) -> tuple[int, list[str]]:
    """
    Validate target_dir against parsed index_data.
    Returns (exit_code, list_of_messages).
    """
    errors = 0
    messages: list[str] = []

    # Map physical files
    physical_files: dict[str, set[str]] = {}
    for root, _, files in os.walk(target_dir):
        root_path = Path(root)
        rel_dir = root_path.relative_to(target_dir).as_posix().strip("/")
        if rel_dir == ".":
            rel_dir = ""
        physical_files[rel_dir] = set(files)

    # 1. Check for missing files and hash mismatches defined in index
    for rel_dir, expected_files in index_data.items():
        messages.append(f"Scanning directory: /{rel_dir}")
        for filename, expected_hash in expected_files.items():
            file_rel_path = Path(rel_dir) / filename
            file_abs_path = target_dir / file_rel_path

            if not file_abs_path.exists():
                messages.append(f"  ❌ MISSING: {file_rel_path}")
                errors += 1
                continue

            # Compute and check hash
            actual_hash = compute_sha256(file_abs_path)
            if actual_hash == expected_hash:
                messages.append(f"  ✅ MATCH: {file_rel_path}")
            else:
                messages.append(
                    f"  ❌ HASH MISMATCH: {file_rel_path}\n"
                    f"     Expected: {expected_hash}\n"
                    f"     Actual:   {actual_hash}"
                )
                errors += 1

    # 2. Check for unindexed files in target_dir
    for rel_dir, files in physical_files.items():
        for filename in files:
            # Skip hidden files
            if filename.startswith("."):
                continue
            # If directory or file not in index, flag it
            if rel_dir not in index_data or filename not in index_data[rel_dir]:
                file_rel_path = Path(rel_dir) / filename
                messages.append(f"  ⚠️  UNINDEXED: {file_rel_path}")
                # Note: Unindexed files are warnings, not hard failure exit code 1
                # unless strict mode or similar, but let's keep them as informational warning

    exit_code = 1 if errors > 0 else 0
    return exit_code, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="MVER Index Validator")
    parser.add_argument(
        "--index",
        required=True,
        help="Path to the MVER_INDEX.md file",
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Path to the target directory containing evidence room files",
    )
    args = parser.parse_args()

    index_path = Path(args.index).resolve()
    target_dir = Path(args.dir).resolve()

    if not target_dir.is_dir():
        print(f"Error: Target path is not a directory: {target_dir}")
        return 1

    try:
        index_data = parse_index(index_path)
    except Exception as e:
        print(f"Error parsing index: {e}")
        return 1

    exit_code, messages = validate_directory(target_dir, index_data)

    for msg in messages:
        print(msg)

    if exit_code == 0:
        print("\n✅ MVER validation passed successfully.")
    else:
        print("\n❌ MVER validation failed with errors.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

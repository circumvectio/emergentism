#!/usr/bin/env python3
"""
manifest_check.py — validator for the root `manifest.yaml`.

Runs three integrity checks:

  1. **Path existence**: every `path:` in manifest resolves on disk.
  2. **Orphan detection**: every candidate organ/entity/product
     directory under SKYZAI_ORG/ appears in the manifest
     (catches drift where a new organ is created but not indexed).
  3. **Shared-lib reverse-dep consistency**: for each declared
     `consumers:` list, at least one import line actually exists
     in that consumer's tree.

Exit 0 = manifest is consistent with reality.
Exit 1 = drift detected; the report lists each drift row.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("manifest_check: PyYAML not installed — cannot parse manifest.yaml", file=sys.stderr)
    print("install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def _repo_root() -> Path:
    """Find the repository root from this script's moved canonical home."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "manifest.yaml").exists() and (parent / ".git").exists():
            return parent
    # Fallback for partial checkouts that keep manifest.yaml but omit .git.
    for parent in here.parents:
        if (parent / "manifest.yaml").exists():
            return parent
    return here.parent.parent.parent


REPO_ROOT = _repo_root()
MANIFEST = REPO_ROOT / "manifest.yaml"


def _load_manifest() -> dict:
    if not MANIFEST.exists():
        print(f"manifest_check: {MANIFEST} not found", file=sys.stderr)
        sys.exit(2)
    with MANIFEST.open() as f:
        return yaml.safe_load(f)


def _entries_with_paths(manifest: dict) -> list[tuple[str, str, str]]:
    """Yield (section, name, path) for every entry declaring a path."""
    out = []
    for section in (
        "organs",
        "infrastructure",
        "organism_scaffolds",
        "entities",
        "portfolio_orgs",
        "substrates",
        "products",
        "child_dacs",
        "deployed_products",
        "shared_libraries",
    ):
        for entry in manifest.get(section, []) or []:
            if "path" in entry:
                out.append((section, entry.get("name", "?"), entry["path"]))
    for section in ("doctrine", "archive", "intake", "tools", "attachments"):
        for entry in manifest.get(section, []) or []:
            if "path" in entry:
                out.append((section, entry.get("role", "?")[:40], entry["path"]))
    return out


def check_path_existence(manifest: dict) -> list[str]:
    errors: list[str] = []
    for section, name, path in _entries_with_paths(manifest):
        # `.local_github_mirrors/` holds intentionally-local, gitignored source
        # mirrors (see deployed_products notes in manifest.yaml). They are expected
        # to be absent in clean checkouts, worktrees, and CI, so a missing local
        # mirror is not manifest drift.
        if path.startswith(".local_github_mirrors/"):
            continue
        full = REPO_ROOT / path
        if not full.exists():
            errors.append(f"[{section}] {name}: path does not exist — {path}")
    return errors


def check_orphans(manifest: dict) -> list[str]:
    """Directories under 02_SKYZAI/01_NOOSPHERE/02_ORGANS, 03_VENTURES,
    02_SKYZAI/01_NOOSPHERE/03_PRODUCTS that are NOT in the manifest."""
    indexed_paths = {path for _, _, path in _entries_with_paths(manifest)}
    errors: list[str] = []
    for parent_rel in ("02_SKYZAI/01_NOOSPHERE/02_ORGANS", "03_VENTURES", "02_SKYZAI/01_NOOSPHERE/03_PRODUCTS"):
        parent = REPO_ROOT / parent_rel
        if not parent.exists():
            continue
        for child in sorted(parent.iterdir()):
            if not child.is_dir():
                continue
            rel = f"{parent_rel}/{child.name}"
            if rel not in indexed_paths:
                errors.append(f"[orphan] {rel}: directory exists on disk but is not in manifest.yaml")
    return errors


def check_shared_lib_consumers(manifest: dict) -> list[str]:
    """For each shared-lib's consumers list, verify at least one import
    of `from <pkg> import ...` exists in the consumer's tree."""
    errors: list[str] = []
    name_to_path = {o["name"]: o["path"] for o in manifest.get("organs", []) or []}
    for lib in manifest.get("shared_libraries", []) or []:
        lib_name = lib.get("name", "?")
        # The Python module name we expect to see imported
        # e.g. "emergentism-core" → "emergentism_core"
        mod_name = lib_name.replace("-", "_")
        for consumer in lib.get("consumers", []) or []:
            consumer_path = name_to_path.get(consumer)
            if not consumer_path:
                errors.append(f"[consumer] {lib_name}: consumer '{consumer}' not in organs list")
                continue
            consumer_tree = REPO_ROOT / consumer_path
            if not consumer_tree.exists():
                errors.append(f"[consumer] {lib_name}: consumer path {consumer_path} does not exist")
                continue
            # Fast grep
            found = False
            for py_file in consumer_tree.rglob("*.py"):
                try:
                    text = py_file.read_text(errors="ignore")
                except OSError:
                    continue
                if f"from {mod_name}" in text or f"import {mod_name}" in text:
                    found = True
                    break
            if not found:
                errors.append(
                    f"[consumer] {lib_name}: declared consumer '{consumer}' "
                    f"has no imports of '{mod_name}' in its tree"
                )
    return errors


def main() -> int:
    manifest = _load_manifest()
    all_errors: list[str] = []

    print(f"manifest_check: {MANIFEST}")
    print(f"  organism_version: {manifest.get('organism_version', '?')}")
    print(f"  schema_version:   {manifest.get('schema_version', '?')}")

    for check_name, check_fn in [
        ("path_existence", check_path_existence),
        ("orphans", check_orphans),
        ("shared_lib_consumers", check_shared_lib_consumers),
    ]:
        errors = check_fn(manifest)
        if errors:
            print(f"\n❌ {check_name}: {len(errors)} issues")
            for e in errors:
                print(f"  {e}")
            all_errors.extend(errors)
        else:
            print(f"✅ {check_name}")

    if all_errors:
        print(f"\ndrift detected: {len(all_errors)} total issues")
        return 1
    print("\nmanifest consistent with reality")
    return 0


if __name__ == "__main__":
    sys.exit(main())

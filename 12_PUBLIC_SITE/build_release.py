#!/usr/bin/env python3
"""Build the deterministic, deny-by-default Emergentism static release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "release-manifest.json"
OUT = ROOT / ".release"
BLOCKED_PARTS = {"90_ARCHIVE", "_archive", "__pycache__", "node_modules", ".git", ".vercel"}


def load_manifest() -> dict:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 1 or data.get("status") != "pure-emergentism-release":
        raise SystemExit("release-manifest.json has an unsupported contract")
    return data


def safe_source(rel: str) -> Path:
    source = (ROOT / rel).resolve()
    try:
        source.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit(f"release path escapes site root: {rel}") from exc
    if any(part in BLOCKED_PARTS for part in source.relative_to(ROOT).parts):
        raise SystemExit(f"release path enters a blocked tree: {rel}")
    if not source.is_file():
        raise SystemExit(f"release source missing: {rel}")
    return source


def copy_file(rel: str, out: Path) -> None:
    source = safe_source(rel)
    target = out / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def tree_hash(out: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        rel = path.relative_to(out).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the manifest-allowlisted Emergentism static release."
    )
    return parser.parse_args(argv)


def publish(staging: Path) -> None:
    """Replace OUT only after staging is complete; restore the prior tree on error."""
    backup: Path | None = None
    if OUT.exists() or OUT.is_symlink():
        backup = Path(tempfile.mkdtemp(prefix=".release.previous-", dir=ROOT))
        backup.rmdir()
        os.replace(OUT, backup)
    try:
        os.replace(staging, OUT)
    except BaseException:
        if backup is not None and backup.exists() and not OUT.exists():
            os.replace(backup, OUT)
        raise
    if backup is not None:
        shutil.rmtree(backup)


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    manifest = load_manifest()
    staging = Path(tempfile.mkdtemp(prefix=".release.next-", dir=ROOT))

    try:
        requested: set[str] = set()
        requested.update(row["file"] for row in manifest["routes"])
        requested.update(manifest["rootFiles"])
        requested.update(manifest["assetFiles"])
        for rel in sorted(requested):
            copy_file(rel, staging)

        digest = tree_hash(staging)
        (staging / "RELEASE_SHA256").write_text(digest + "\n", encoding="ascii")
        publish(staging)
    finally:
        if staging.exists():
            shutil.rmtree(staging)

    print(f"release files={sum(1 for p in OUT.rglob('*') if p.is_file())} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

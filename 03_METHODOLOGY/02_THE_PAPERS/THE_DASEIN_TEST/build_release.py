#!/usr/bin/env python3
"""Build or verify the uncompiled arXiv source and deterministic release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
WORKTREE = HERE.parents[2]
MANUSCRIPT = HERE / "THE_DASEIN_TEST.md"
METADATA = HERE / "metadata.yaml"
BIBLIOGRAPHY = HERE / "references.bib"
ARXIV_TEX = HERE / "arxiv" / "main.tex"
MANIFEST = HERE / "RELEASE_MANIFEST.json"
SOURCE_BINDINGS = (
    WORKTREE / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "06_THE_DASEIN_TEST_EUB1_v1.0.md",
    WORKTREE / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "eub_v1" / "FREEZE_MANIFEST.json",
    WORKTREE / "00_HANDOFF" / "EUB1_V1_DASEIN_TEST_OWNER_DIRECTION_2026_08_21.md",
    WORKTREE / "00_META" / "ADJUDICATION_W10_SPARK_EUB1_V1_2026_08_21.md",
    WORKTREE / "12_PUBLIC_SITE" / "record" / "eub-1" / "index.html",
    WORKTREE / "12_PUBLIC_SITE" / "public_semantic_parity.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_tex(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "pandoc", str(MANUSCRIPT), "--standalone", "--citeproc",
        "--metadata-file", str(METADATA), "--bibliography", str(BIBLIOGRAPHY),
        "--output", str(destination),
    ]
    subprocess.run(command, cwd=HERE, check=True, text=True, capture_output=True)


def package_files() -> list[Path]:
    result = []
    for path in HERE.rglob("*"):
        if not path.is_file() or path == MANIFEST or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        result.append(path)
    return sorted(result, key=lambda path: path.relative_to(HERE).as_posix())


def build_manifest() -> dict[str, object]:
    missing = [str(path) for path in SOURCE_BINDINGS if not path.exists()]
    if missing:
        raise FileNotFoundError("missing source binding(s): " + ", ".join(missing))
    return {
        "schema_id": "DaseinTestReleaseManifest.v1",
        "title": "The Dasein Test: Benchmarking Whether an AI Can Unfold How Being and Itself Emerged",
        "author": "Yves R. Burri",
        "version": "1.0.0",
        "status": "OFFLINE-READY · [D] · UNSUBMITTED · UNDEPLOYED · ARXIV_SOURCE_UNCOMPILED",
        "self_excluded": True,
        "publication_targets": {
            "doi_archive": "PREPARED_NOT_DEPOSITED",
            "arxiv": "SOURCE_CANDIDATE_NOT_SUBMITTED_NOT_COMPILED",
            "public_site": "LOCAL_SOURCE_NOT_DEPLOYED"
        },
        "files": [
            {"path": path.relative_to(HERE).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in package_files()
        ],
        "source_bindings": [
            {"path": path.relative_to(WORKTREE).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in SOURCE_BINDINGS
        ],
        "external_actions": {
            "model_evaluation": False,
            "doi_deposit": False,
            "arxiv_submission": False,
            "site_deployment": False,
            "priority_established": False
        }
    }


def encoded(value: object) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"


def check() -> list[str]:
    errors: list[str] = []
    if not ARXIV_TEX.exists():
        errors.append("arxiv/main.tex is missing")
    else:
        with tempfile.TemporaryDirectory() as temp:
            rendered = Path(temp) / "main.tex"
            render_tex(rendered)
            if rendered.read_bytes() != ARXIV_TEX.read_bytes():
                errors.append("arxiv/main.tex drift")
    if not MANIFEST.exists():
        errors.append("RELEASE_MANIFEST.json is missing")
    else:
        try:
            if MANIFEST.read_bytes() != encoded(build_manifest()):
                errors.append("RELEASE_MANIFEST.json drift")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"release manifest unreadable: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--acknowledge-review", action="store_true")
    args = parser.parse_args()
    if args.write:
        if not args.acknowledge_review:
            parser.error("--write requires --acknowledge-review")
        render_tex(ARXIV_TEX)
        MANIFEST.write_bytes(encoded(build_manifest()))
        print("DASEIN RELEASE: WROTE REVIEW CANDIDATE (arXiv source remains uncompiled)")
        return 0
    if not args.check:
        parser.error("choose --check or --write --acknowledge-review")
    errors = check()
    if errors:
        print("DASEIN RELEASE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 2
    print("DASEIN RELEASE: PASS (source candidate uncompiled; no external action)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

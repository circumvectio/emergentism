#!/usr/bin/env python3
"""Validate the active Emergentism folder and authority contract."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TOP_LEVELS = (
    "00_CONTROL",
    "00_HANDOFF",
    "00_META",
    "01_TELEOLOGY",
    "02_EPISTEMOLOGY",
    "03_METHODOLOGY",
    "04_AXIOLOGY",
    "05_COSMOLOGY",
    "06_ONTOLOGY",
    "07_THEOLOGY",
    "08_FRAMEWORK_SUPPORT",
    "09_TOOLS",
    "10_SEED",
    "11_UPLINK",
    "12_PUBLIC_SITE",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
)

ROUTE_TRIPLETS = (
    "00_CONTROL",
    "00_HANDOFF",
    "00_META",
    "01_TELEOLOGY",
    "02_EPISTEMOLOGY",
    "03_METHODOLOGY",
    "04_AXIOLOGY",
    "05_COSMOLOGY",
    "06_ONTOLOGY",
    "07_THEOLOGY",
    "08_FRAMEWORK_SUPPORT",
    "09_TOOLS",
    "10_SEED",
    "11_UPLINK",
    "12_PUBLIC_SITE",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
)

DOOR_LANES = (
    "00_HANDOFF",
    "01_TELEOLOGY",
    "02_EPISTEMOLOGY",
    "03_METHODOLOGY",
    "04_AXIOLOGY",
    "05_COSMOLOGY",
    "06_ONTOLOGY",
    "07_THEOLOGY",
    "08_FRAMEWORK_SUPPORT",
    "09_TOOLS",
    "10_SEED",
    "11_UPLINK",
    "12_PUBLIC_SITE",
)

ROOT_BODY_ALLOWLIST = {
    "AGENT_README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "ROSETTA.md",
    "00_THE_KERNEL_INDEX.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
}

TARGET_PATTERN = re.compile(
    r"^(?:canonical_target|historical_target):\s*[\"']?([^\"'\n]+)", re.MULTILINE
)


def resolve_target(source: Path, raw: str) -> Path:
    raw = raw.strip()
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    root_candidate = ROOT / candidate
    if root_candidate.exists():
        return root_candidate
    return source.parent / candidate


def main() -> int:
    errors: list[str] = []

    for name in REQUIRED_TOP_LEVELS:
        if not (ROOT / name).is_dir():
            errors.append(f"missing top-level lane: {name}")

    for lane in ROUTE_TRIPLETS:
        for filename in ("README.md", "AGENTS.md", "CLAUDE.md"):
            if not (ROOT / lane / filename).is_file():
                errors.append(f"missing route surface: {lane}/{filename}")

    for lane in DOOR_LANES:
        if not any((ROOT / lane).glob("00_THE_*.md")):
            errors.append(f"missing Door: {lane}/00_THE_*.md")

    for lane in REQUIRED_TOP_LEVELS:
        if lane in {"00_META", "90_ARCHIVE", "91_COMPATIBILITY"}:
            continue
        nested_meta = ROOT / lane / "00_META"
        if nested_meta.exists():
            errors.append(f"forbidden per-lane governance folder: {nested_meta.relative_to(ROOT)}")

    for root_doc in sorted(ROOT.glob("*.md")):
        if root_doc.name in ROOT_BODY_ALLOWLIST:
            continue
        text = root_doc.read_text(encoding="utf-8")
        if "stub" not in text.lower() and "routing" not in text.lower():
            errors.append(f"root document is neither owner nor forwarding stub: {root_doc.name}")
            continue
        matches = TARGET_PATTERN.findall(text)
        if not matches:
            errors.append(f"forwarding stub has no declared target: {root_doc.name}")
            continue
        if not any(resolve_target(root_doc, raw).exists() for raw in matches):
            errors.append(f"forwarding stub targets do not exist: {root_doc.name}")

    required_local_doors = (
        "08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/README.md",
        "08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/00_MAGNUM_OPUS/README.md",
        "08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/02_ANALYSIS_DOCUMENTS/README.md",
        "08_FRAMEWORK_SUPPORT/91_COMPATIBILITY/README.md",
    )
    for rel in required_local_doors:
        if not (ROOT / rel).is_file():
            errors.append(f"missing local route surface: {rel}")

    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    for raw in tracked:
        if not raw:
            continue
        path = Path(raw)
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts:
            errors.append(f"tracked filesystem noise present: {path}")

    if errors:
        print("TREE CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("TREE CONTRACT: PASS")
    print(f"top-level lanes: {len(REQUIRED_TOP_LEVELS)}")
    print(f"route triplets: {len(ROUTE_TRIPLETS)}")
    print(f"Door lanes: {len(DOOR_LANES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

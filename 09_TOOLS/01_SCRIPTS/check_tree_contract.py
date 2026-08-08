#!/usr/bin/env python3
"""Validate the active Emergentism folder and authority contract."""

from __future__ import annotations

import hashlib
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
    "00_THE_CLOSED_READING_LOOP_K2_SIGN_RECEIPT_2026_08_01.md",
    "00_THE_FOUNDATION.md",
    "00_THE_KERNEL_INDEX.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
    "00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md",
    "VMOSK_A.md",
    "VMOSK_A_v2_2026_07_31.md",
}

# These three files are grandfathered compatibility tombstones inside a
# categorically forbidden per-pillar 00_META. They are a held violation, not a
# conforming lane. Adding a file, changing a body, or substituting a symlink
# fails; exact custody remains visible as debt until D-OWNER-02 is selected.
HELD_SUPPORT_META_TOMBSTONE_SHA256 = {
    "CLAUDE.md": "0802649fc2b1a581ba59ed85fbb6d0867b37b61bfe9990d39991a2f4697a64da",
    "00_MAGNUM_OPUS/CLAUDE.md": (
        "9ee14e3de1a691a50409ab7adea269c5b11f2cac6f0ccfc18c4fa9808aa9c2f7"
    ),
    "02_ANALYSIS_DOCUMENTS/CLAUDE.md": (
        "1784d975a03340530a0e00344e84f64b662e68c1557ca20fefcb9c08f73f91cc"
    ),
}
HELD_SUPPORT_META_DIRECTORIES = {
    "00_MAGNUM_OPUS",
    "02_ANALYSIS_DOCUMENTS",
}
HELD_SUPPORT_META_ENTRIES = (
    set(HELD_SUPPORT_META_TOMBSTONE_SHA256) | HELD_SUPPORT_META_DIRECTORIES
)

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


def has_symlink_component(path: Path) -> bool:
    """Reject a held path if it or any component below ROOT is a symlink."""

    relative = path.relative_to(ROOT)
    candidate = ROOT
    for component in relative.parts:
        candidate /= component
        if candidate.is_symlink():
            return True
    return False


def main() -> int:
    errors: list[str] = []
    held_debts: list[str] = []

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
        # Lexical presence matters: Path.exists() is false for a broken
        # symlink, but a broken or non-directory `00_META` entry is still a
        # topology violation and must not disappear from the gate.
        if nested_meta.exists() or nested_meta.is_symlink():
            if lane == "08_FRAMEWORK_SUPPORT":
                entries = {
                    str(path.relative_to(nested_meta))
                    for path in nested_meta.rglob("*")
                }
                bodies_are_exact = entries == HELD_SUPPORT_META_ENTRIES
                if bodies_are_exact:
                    expected_paths = [
                        nested_meta,
                        *(nested_meta / rel for rel in HELD_SUPPORT_META_ENTRIES),
                    ]
                    bodies_are_exact = not any(
                        has_symlink_component(path) for path in expected_paths
                    )
                if bodies_are_exact:
                    bodies_are_exact = all(
                        (nested_meta / rel).is_dir()
                        for rel in HELD_SUPPORT_META_DIRECTORIES
                    )
                if bodies_are_exact:
                    for rel, expected_sha256 in HELD_SUPPORT_META_TOMBSTONE_SHA256.items():
                        tombstone = nested_meta / rel
                        if not tombstone.is_file() or (
                            hashlib.sha256(tombstone.read_bytes()).hexdigest()
                            != expected_sha256
                        ):
                            bodies_are_exact = False
                            break
                if bodies_are_exact:
                    held_debts.append(
                        "08_FRAMEWORK_SUPPORT/00_META remains a hash-bound, "
                        "grandfathered violation while D-OWNER-02 is UNSET"
                    )
                    continue
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

    if held_debts:
        print("TREE CONTRACT: PASS-WITH-DEBT")
        for debt in held_debts:
            print(f"- {debt}")
    else:
        print("TREE CONTRACT: PASS")
    print(f"top-level lanes: {len(REQUIRED_TOP_LEVELS)}")
    print(f"route triplets: {len(ROUTE_TRIPLETS)}")
    print(f"Door lanes: {len(DOOR_LANES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

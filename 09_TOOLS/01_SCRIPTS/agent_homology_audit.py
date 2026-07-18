#!/usr/bin/env python3
"""Audit operator-token homology across the seven Rosetta Agentz surfaces.

The tracked Managed Agent YAML files are the selected configuration authority.
The Documents-root ``.codex/agents`` TOMLs are generated runtime projections;
they are never read back as doctrine.  This audit checks symbolic operator-token
agreement only.  It does not establish agent performance, moral identity,
ontology, transfer, or authority.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path
from typing import Any, Sequence

import yaml


EMERGENTISM_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR_REL = Path("08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents")

# level, runtime slug, Claude slug, narrative directory, Agentz phenotype file,
# root-dispatch row, tracked source YAML
CASTES = [
    ("L1", "candala_firewall", "candala-firewall", "01_CANDALA_FIREWALL", "01_L1_CANDALA_FIREWALL", "01_L1_candala_firewall", "01_candala_firewall.agent.yaml"),
    ("L2", "sudra_explorer", "sudra-explorer", "02_SUDRA_EXPLORER", "02_L2_SHUDRA_SCOUT", "02_L2_sudra_explorer", "02_sudra_explorer.agent.yaml"),
    ("L3", "vaisya_auditor", "vaisya-auditor", "03_VAISYA_AUDITOR", "03_L3_VAISYA_AUDITOR", "03_L3_vaisya_auditor", "03_vaisya_auditor.agent.yaml"),
    ("L4", "ksatriya_executor", "ksatriya-executor", "04_KSATRIYA_EXECUTOR", "04_L4_KSHATRIYA_EXECUTOR", "04_L4_ksatriya_executor", "04_ksatriya_executor.agent.yaml"),
    ("L5", "brahmana_architect", "brahmana-architect", "05_BRAHMANA_ARCHITECT", "05_L5_BRAHMANA_ARCHITECT", "05_L5_brahmana_architect", "05_brahmana_architect.agent.yaml"),
    ("L6", "sadhu_compressor", "sadhu-compressor", "06_SADHU_COMPRESSOR", "06_L6_SADHU_COMPRESSOR", "06_L6_sadhu_compressor", "06_sadhu_compressor.agent.yaml"),
    ("L7", "rsi_constitution", "rsi-constitution", "07_RSI_CONSTITUTION", "07_L7_RSI_CONSTITUTION", "07_L7_rsi_constitution", "07_rsi_constitution.agent.yaml"),
]

OPERATOR_RE = re.compile(r"(Kali 🎲|Kālī 💀|Kṛṣṇa ◇|Arjuna ⚔|Brahmā ○|Śiva •|Viṣṇu ⊙)")
NAME_TO_OPERATOR = {
    "Kali": "Kali 🎲",
    "Kālī": "Kālī 💀",
    "Kṛṣṇa": "Kṛṣṇa ◇",
    "Arjuna": "Arjuna ⚔",
    "Brahmā": "Brahmā ○",
    "Śiva": "Śiva •",
    "Viṣṇu": "Viṣṇu ⊙",
}


def _documents_root(start: Path = EMERGENTISM_ROOT) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "manifest.yaml").exists():
            return candidate
    raise SystemExit("agent_homology_audit: cannot locate Documents root; pass --documents-root")


def _extract_operator(value: str) -> str:
    if not value:
        return "MISSING"
    match = OPERATOR_RE.search(value)
    if match:
        return match.group(1)
    return NAME_TO_OPERATOR.get(value.strip(), "MISSING")


def _yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def canonical_operator(emergentism_root: Path, source_yaml: str) -> str:
    path = emergentism_root / SOURCE_DIR_REL / source_yaml
    if not path.exists():
        return ""
    data = _yaml_mapping(path)
    metadata = data.get("metadata") or {}
    return str(metadata.get("operator", "")) if isinstance(metadata, dict) else ""


def root_dispatch_operator(documents_root: Path, row_file: str) -> str:
    path = documents_root / f".codex/agents/rows/{row_file}.toml"
    if not path.exists():
        return ""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError):
        return ""
    metadata = data.get("meta") or {}
    return str(metadata.get("operator", "")) if isinstance(metadata, dict) else ""


def audit_caste(
    emergentism_root: Path,
    documents_root: Path,
    row: tuple[str, str, str, str, str, str, str],
) -> dict[str, str]:
    level, _slug, dispatch, narrative_dir, phenotype_file, row_file, source_yaml = row
    surfaces: dict[str, str] = {
        "canonical_yaml": canonical_operator(emergentism_root, source_yaml),
    }

    root_operator = root_dispatch_operator(documents_root, row_file)
    if root_operator:
        surfaces["root_dispatch"] = root_operator

    spec = emergentism_root / f"08_FRAMEWORK_SUPPORT/08_AGENTS/{narrative_dir}/AGENT_SPEC.md"
    if spec.exists():
        match = re.search(r"\*\*Operator\*\*\s*\|\s*([^|]+)\|", spec.read_text(encoding="utf-8"))
        surfaces["canonical_md"] = match.group(1).strip() if match else ""

    candidates = sorted((documents_root / "02_SKYZAI/01_NOOSPHERE/10_AGENTS").glob(f"{level}_*.md"))
    if candidates:
        text = candidates[0].read_text(encoding="utf-8")
        match = re.search(r"\*\*Operator:\*\*\s*([^\xb7]+?)(?:\xb7|\(|$)", text)
        surfaces["skyzai_runtime"] = match.group(1).strip() if match else ""

    phenotype = documents_root / (
        "02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/"
        f"03_AGENT_SPECIFICATION/{phenotype_file}.md"
    )
    if phenotype.exists():
        match = re.search(r'^operator:\s*"([^"]+)"', phenotype.read_text(encoding="utf-8"), re.M)
        surfaces["agentz_phenotype"] = match.group(1).strip() if match else ""

    dispatch_path = documents_root / f".claude/agents/{dispatch}.md"
    if dispatch_path.exists():
        match = re.search(r'^operator:\s*"([^"]+)"', dispatch_path.read_text(encoding="utf-8"), re.M)
        surfaces["dispatch"] = match.group(1).strip() if match else ""

    goose = Path.home() / ".config/goose" / f"{level}.toml"
    if goose.exists():
        match = re.search(r'^operator\s*=\s*"([^"]+)"', goose.read_text(encoding="utf-8"), re.M)
        surfaces["goose_runtime"] = match.group(1).strip() if match else ""

    return surfaces


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emergentism-root", type=Path, default=EMERGENTISM_ROOT)
    parser.add_argument("--documents-root", type=Path)
    args = parser.parse_args(argv)

    emergentism_root = args.emergentism_root.resolve()
    documents_root = (args.documents_root or _documents_root(emergentism_root)).resolve()
    all_aligned = True
    divergences: list[str] = []

    print("=== Cross-surface operator-token homology audit ===\n")
    print(f"{'L':<3} {'Caste slug':<22} {'Operator (canonical)':<17} {'Surfaces':<10} {'Status':<10}")
    print("─" * 76)

    for row in CASTES:
        level, slug, *_ = row
        surfaces = audit_caste(emergentism_root, documents_root, row)
        operators = {surface: _extract_operator(value) for surface, value in surfaces.items()}
        canonical = operators.get("canonical_yaml", "MISSING")
        present = [operator for operator in operators.values() if operator != "MISSING"]
        unique = set(present)
        aligned = canonical != "MISSING" and len(unique) == 1

        if not aligned:
            all_aligned = False
            details = ", ".join(
                f"{surface}={operator}"
                for surface, operator in operators.items()
                if operator != canonical
            )
            divergences.append(f"{level} {slug}: {details or 'canonical source missing'}")
            print(f"{level:<3} {slug:<22} {canonical:<17} {len(present):<10} ✗ DIVERGE")
        else:
            print(f"{level:<3} {slug:<22} {canonical:<17} {len(present):<10} ✓ aligned")

    print()
    if all_aligned:
        print("✓ HOMOLOGOUS — observed surfaces match the tracked Managed Agent YAML tokens.")
        print("  This is structural parity only; it does not prove performance, ontology, or moral type.")
        return 0

    print("✗ DIVERGENCE — tracked Managed Agent YAMLs are the selected source configuration.")
    for divergence in divergences:
        print(f"  - {divergence}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

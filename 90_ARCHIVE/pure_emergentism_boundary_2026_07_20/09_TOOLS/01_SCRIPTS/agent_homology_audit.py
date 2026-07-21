#!/usr/bin/env python3
"""
agent_homology_audit.py — verify the seven Rosetta agents are homologous across
all surfaces.

The polygenetic skill tree doctrine says: one genotype, many phenotypes. The
canonical TOML at .codex/agents/rosetta_agent_rows.toml is the genotype trunk.
Every other surface (generated TOMLs, canonical markdown, Skyzai runtime,
Agentz phenotype, dispatch) must read the same operator-deity for each
L-level.

This script extracts the deity glyph from each surface and reports any
divergence.

Seven surfaces audited:
  1. canonical_toml    — .codex/agents/rosetta_agent_rows.toml (constitutional source)
  2. generated_toml    — .codex/agents/{caste}.toml (sync_agents.py output)
  3. canonical_md      — 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/0X_*/AGENT_SPEC.md
  4. skyzai_runtime    — 02_SKYZAI/01_NOOSPHERE/10_AGENTS/L*_*.md (organism-runtime applied)
  5. agentz_phenotype  — 02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/0X_LX_*.md
  6. dispatch          — .claude/agents/<caste>.md (Claude SDK invocation surface)
  7. goose_runtime     — ~/.config/goose/L<N>.toml (Goose applied-framework runtime,
                          derived from VMOSK CONFIG via agent_goose_sync.py).
                          Skipped if Goose is not installed.

Exit 0 = all 7 castes × audited surfaces converge on the same deity glyph.
Exit 1 = at least one divergence detected; report lists the mismatches.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CASTES = [
    ("L1", "candala_firewall",  "candala-firewall",  "01_CANDALA_FIREWALL",  "01_L1_CANDALA_FIREWALL",  "01_L1_candala_firewall"),
    ("L2", "sudra_explorer",    "sudra-explorer",    "02_SUDRA_EXPLORER",    "02_L2_SHUDRA_SCOUT",      "02_L2_sudra_explorer"),
    ("L3", "vaisya_auditor",    "vaisya-auditor",    "03_VAISYA_AUDITOR",    "03_L3_VAISYA_AUDITOR",    "03_L3_vaisya_auditor"),
    ("L4", "ksatriya_executor", "ksatriya-executor", "04_KSATRIYA_EXECUTOR", "04_L4_KSHATRIYA_EXECUTOR","04_L4_ksatriya_executor"),
    ("L5", "brahmana_architect","brahmana-architect","05_BRAHMANA_ARCHITECT","05_L5_BRAHMANA_ARCHITECT","05_L5_brahmana_architect"),
    ("L6", "sadhu_compressor",  "sadhu-compressor",  "06_SADHU_COMPRESSOR",  "06_L6_SADHU_COMPRESSOR",  "06_L6_sadhu_compressor"),
    ("L7", "rsi_constitution",  "rsi-constitution",  "07_RSI_CONSTITUTION",  "07_L7_RSI_CONSTITUTION",  "07_L7_rsi_constitution"),
]

DEITY_RE = re.compile(r"(Kali 🎲|Kālī 💀|Kṛṣṇa ◇|Arjuna ⚔|Brahmā ○|Śiva •|Viṣṇu ⊙)")

# Goose runtime TOML stores `operator = "Kali"` (sanskrit name only) +
# `glyph = "dice"` separately. Map bare names to their canonical glyph form
# so the homology check accepts the Goose surface as equivalent.
SANSKRIT_TO_CANONICAL = {
    "Kali": "Kali 🎲",
    "Kālī": "Kālī 💀",
    "Kṛṣṇa": "Kṛṣṇa ◇",
    "Arjuna": "Arjuna ⚔",
    "Brahmā": "Brahmā ○",
    "Śiva": "Śiva •",
    "Viṣṇu": "Viṣṇu ⊙",
}


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "manifest.yaml").exists():
            return parent
    raise SystemExit("agent_homology_audit: cannot locate repo root")


def _section(text: str, key: str) -> str:
    m = re.search(rf"\[agents\.{key}\.profile\](.*?)(?=\n\[|$)", text, re.S)
    return m.group(1) if m else ""


def _field(text: str, key: str) -> str:
    m = re.search(rf"^{key}\s*=\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def _extract_deity(s: str) -> str:
    if not s:
        return "MISSING"
    m = DEITY_RE.search(s)
    if m:
        return m.group(1)
    # Try bare sanskrit name (Goose runtime TOML form)
    stripped = s.strip()
    if stripped in SANSKRIT_TO_CANONICAL:
        return SANSKRIT_TO_CANONICAL[stripped]
    return "MISSING"


def audit_caste(root: Path, L: str, caste: str, dispatch: str, sk_dir: str, agentz_file: str, row_file: str) -> dict:
    surfaces: dict[str, str] = {}

    # 1. canonical TOML — per-agent source under rows/
    row = root / f".codex/agents/rows/{row_file}.toml"
    if row.exists():
        sec = _section(row.read_text(), caste)
        surfaces["canonical_toml"] = _field(sec, "display_operator")

    # 2. generated parent TOML
    gen = root / f".codex/agents/{caste}.toml"
    if gen.exists():
        m = re.search(r"^- operator:\s*(.+)$", gen.read_text(), re.M)
        surfaces["generated_toml"] = m.group(1).strip() if m else ""

    # 3. canonical markdown AGENT_SPEC
    spec = root / f"01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/{sk_dir}/AGENT_SPEC.md"
    if spec.exists():
        m = re.search(r"\*\*Operator\*\*\s*\|\s*([^|]+)\|", spec.read_text())
        surfaces["canonical_md"] = m.group(1).strip() if m else ""

    # 4. Skyzai runtime applied spec
    candidates = list((root / "02_SKYZAI/01_NOOSPHERE/10_AGENTS").glob(f"{L}_*.md"))
    if candidates:
        text = candidates[0].read_text()
        m = re.search(r"\*\*Operator:\*\*\s*([^·]+?)(?:·|\(|$)", text)
        surfaces["skyzai_runtime"] = m.group(1).strip() if m else ""

    # 5. Agentz phenotype spec
    agentz = root / f"02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/{agentz_file}.md"
    if agentz.exists():
        m = re.search(r"^operator:\s*\"([^\"]+)\"", agentz.read_text(), re.M)
        surfaces["agentz_phenotype"] = m.group(1).strip() if m else ""

    # 6. Claude dispatch
    disp = root / f".claude/agents/{dispatch}.md"
    if disp.exists():
        m = re.search(r"^operator:\s*\"([^\"]+)\"", disp.read_text(), re.M)
        surfaces["dispatch"] = m.group(1).strip() if m else ""

    # 7. Goose runtime layer (~/.config/goose/L<N>.toml). Skipped if Goose isn't installed.
    goose = Path.home() / ".config" / "goose" / f"{L}.toml"
    if goose.exists():
        m = re.search(r"^operator\s*=\s*\"([^\"]+)\"", goose.read_text(), re.M)
        surfaces["goose_runtime"] = m.group(1).strip() if m else ""

    return surfaces


def main() -> int:
    root = _repo_root()
    all_aligned = True
    divergences: list[str] = []

    print("=== Cross-surface operator homology audit ===\n")
    print(f"{'L':<3} {'Caste':<22} {'Deity (canonical)':<14} {'Surfaces':<10} {'Status':<10}")
    print("─" * 70)

    for L, caste, dispatch, sk_dir, agentz_file, row_file in CASTES:
        surfaces = audit_caste(root, L, caste, dispatch, sk_dir, agentz_file, row_file)
        deities = {s: _extract_deity(v) for s, v in surfaces.items()}
        present = [d for d in deities.values() if d != "MISSING"]
        unique = set(present)

        canon_deity = deities.get("canonical_toml", "MISSING")
        n_surfaces = len(present)
        aligned = len(unique) == 1 and canon_deity != "MISSING"

        if not aligned:
            all_aligned = False
            div_detail = ", ".join(f"{s}={d}" for s, d in deities.items() if d != canon_deity)
            divergences.append(f"{L} {caste}: {div_detail}")
            print(f"{L:<3} {caste:<22} {canon_deity:<14} {n_surfaces:<10} ✗ DIVERGE")
        else:
            print(f"{L:<3} {caste:<22} {canon_deity:<14} {n_surfaces:<10} ✓ aligned")

    print()
    if all_aligned:
        print("✓ HOMOLOGOUS — all surfaces converge on the canonical operator deities.")
        print("  Polygenetic skill tree doctrine empirically satisfied.")
        return 0
    else:
        print("✗ DIVERGENCE detected. Source of truth is rosetta_agent_rows.toml.")
        for d in divergences:
            print(f"  - {d}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

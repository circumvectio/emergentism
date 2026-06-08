---
rosetta:
  primary_level: L6
  primary_column: Tools Legacy Archive Front Door
  secondary:
    - level: L3
      column: Stale-Tool Evidence Audit
      role: "separate archived scripts and dependency snapshots from current tooling"
    - level: L4
      column: Migration Operations
      role: "route porting, tombstoning, successor selection, and archive repair"
    - level: L7
      column: Provenance Witness
      role: "preserve historical context without granting current authority"
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[I/B]"
  canonical_phrase: "90_ARCHIVE — L6 Tools Legacy Archive"
title: "90_ARCHIVE — L6 Tools Legacy Archive"
status: "FRONT DOOR — tools legacy archive"
evidence_tier: "[I] for archive provenance; [B] only for dated migration, replacement, or source-owner receipts."
---

# 90_ARCHIVE — L6 Tools Legacy Archive

> Archived legacy scripts that are no longer in active use. Preserved for provenance; not current runtime.

**Rosetta boundary:** [I] This front door is historical/provenance context. It
does not [B] authorize archived scripts as current tooling; use current
successors or port with a dated migration receipt.

## Contents

### `bridge_scripts_2026_04_17/`

**Source location (archived from)**: `05_TOOLS/90_ARCHIVE/bridge_scripts/`

**What**: 15 Python scripts used in earlier uplink-rebuild / organism-compression / verification passes (examples: `rebuild.py`, `compress_organism.py`, `verify_uplinks.py`, `align_organism.py`, etc.).

**Reason archived**: the Rosetta L6 audit (2026-04-22) flagged these as stale — referenced by audit docs as "previous passes" but no longer invoked by current tooling. They sat at the top of `_legacy/` without explicit archival framing.

**Canonical current tools** (use these, not the archive):
- [`../01_SCRIPTS/compile_uplink.py`](../01_SCRIPTS/compile_uplink.py) — uplink staleness check + recompile
- [`../01_SCRIPTS/compile_state.py`](../01_SCRIPTS/compile_state.py) — state compilation
- [`../01_SCRIPTS/check_links.py`](../01_SCRIPTS/check_links.py) — link integrity
- Historical organism lint paths are not current in this tree; resolve a live lint owner before using that legacy reference.

## Archive discipline

- [I] These scripts may depend on paths or assumptions that no longer hold. Do not run them directly against the current corpus without review.
- [I] Do not treat archived scripts as authority for the operations they once performed. If an equivalent operation is needed now, use the canonical current tool (above) or write a scoped successor.
- If a script in here turns out to be still useful, port it out with a dated note.

---

*⊙ = • × ○*

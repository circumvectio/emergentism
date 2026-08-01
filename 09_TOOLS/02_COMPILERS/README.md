---
rosetta:
  primary_level: L5
  primary_column: Compiler Front Door
  secondary:
    - level: L3
      column: Reproducibility Audit
      role: "state which compiler outputs are source-backed and which are dormant"
    - level: L4
      column: Compiler Execution
      role: "keep compiler commands explicit and diff-reviewed before generated output is accepted"
    - level: L6
      column: Source Boundary
      role: "make compiler output downstream from source-owned doctrine and route cards"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "02_COMPILERS"
title: "02_COMPILERS"
status: "ACTIVE — compiler front door"
evidence_tier: "[B] for local compiler inventory and source-input status; [S] for downstream-output rule; [I] for folder-boundary guidance."
---

# 02_COMPILERS

Focused compiler utilities for building derived maps and compressed working
surfaces from source-owned material.

## What Belongs Here

- narrow compilers that emit indexes, maps, or other derived views
- helper builders that support source-first navigation

## What Does Not

- source doctrine
- hand-authored authority files that should live in the owning row
- deployment scripts

## Authority Rule

Compiler output is downstream. If a compiled artifact disagrees with the owning
source lane, repair the source and recompile.

## Current Compiler Inventory

| Compiler | Output | Status |
|---|---|---|
| `compile_claim_cards.py` | `00_META/registers/CLAIM_CARD_REGISTER.json`, `CLAIM_GRAPH.json`, `CLAIM_LIFECYCLE_INVENTORY.json` | [B/S] Active deterministic claim/owner/dependency compiler. |
| `build_corpus_map.py` | compatibility front door for `compile_claim_cards.py` | [B] Active; the absent-source holographic compiler was replaced in W0. |
| `render_burri_rules.py` | deterministic Burri plate renders from `05_COSMOLOGY/00_THE_BURRI_RULES.md` | [B/S] Active; covered by `test_render_burri_rules.py`. |

## Claim-card commands

```sh
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --write
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
python3 09_TOOLS/02_COMPILERS/test_corpus_claim_graph.py
```

The `*.yaml` inputs use the JSON subset of YAML 1.2 so compilation remains
stdlib-only and deterministic. Generated graphs are routing views, not owners
or evidence.

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- current corpus gate: `../01_SCRIPTS/gate.sh`
- Uplink route map: `../../11_UPLINK/README.md`

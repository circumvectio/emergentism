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
| `build_corpus_map.py` | `00_CORPUS.md` folder-perspective maps | [B] Dormant in this checkout: requires `../_corpus_source.yaml`, which is not present. |

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- UPLINK compile entry point: `../01_SCRIPTS/compile_uplink.py`
- full routing layer: `../../11_UPLINK/00_CORE/00_INDEX.md`

## Kintsugi audit foundation

The A0 baseline validator freezes the known repository test state without treating existing failures as new truth:

```bash
set -euo pipefail
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

`kintsugi_baseline_failures.json` records 19 baseline node IDs and five exact failure signatures at `main@26e616e651e2a87e8c85bf37db515d7fcd007b7b`. A previously failing node may turn green; a removed node, new failure, exception drift, or signature drift fails. The validator itself introduces no direct writes and disables pytest cache and Python bytecode writes; arbitrary repository test bodies are not sandboxed. The baseline gate has no K2 approval gate.

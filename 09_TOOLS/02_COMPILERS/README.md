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
| `render_burri_rules.py` | `05_COSMOLOGY/00_BURRI_RULES_PLATE.svg` and `05_COSMOLOGY/00_BURRI_RULES_EMBLEM.svg` | [B] Deterministic generated views of the `[D]` Burri Rules topology; the L5 Markdown rulebook remains semantic authority. |

## Burri Rules Renderer

Ownership is split deliberately:

- `05_COSMOLOGY/00_THE_BURRI_RULES.md` owns semantics and claim boundaries.
- `05_COSMOLOGY/00_BURRI_RULES_TOPOLOGY.json` is a non-authoritative semantic
  mirror plus geometry and source data. It may not introduce claims; all mirrored
  semantics must remain at parity with the Markdown authority.
- `render_burri_rules.py` validates that contract and derives both SVG views.

Write both outputs atomically after topology review:

```bash
python3 -B 09_TOOLS/02_COMPILERS/render_burri_rules.py --write
```

Check tracked bytes for missing or drifted generated output without writing:

```bash
python3 -B 09_TOOLS/02_COMPILERS/render_burri_rules.py --check
```

Exactly one mode is required. Output contains no timestamp or
environment-dependent value; both views carry the renderer version and the
same topology SHA-256.

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- UPLINK compile entry point: `../01_SCRIPTS/compile_uplink.py`
- full routing layer: `../../11_UPLINK/00_CORE/00_INDEX.md`

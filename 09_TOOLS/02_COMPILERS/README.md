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
| `render_burri_rules.py` | `05_COSMOLOGY/00_BURRI_RULES_PLATE.svg` and `05_COSMOLOGY/00_BURRI_RULES_EMBLEM.svg`, rendered from `05_COSMOLOGY/00_BURRI_RULES_TOPOLOGY.json` | [B] Present and runnable in this checkout: the topology input exists, and `test_render_burri_rules.py` is its local test surface. Output is downstream — repair the Markdown owners, then re-render. |
| `build_corpus_map.py` | `00_CORPUS.md` folder-perspective maps | [B] Dormant in this checkout: requires `../_corpus_source.yaml`, which is not present. |

**Corrected 2026-07-22.** This table previously held only the dormant
`build_corpus_map.py` row, so it read as though the lane had no working
compiler — while omitting the deterministic Burri plate renderer that the parent
lane README names as this folder's headline active surface. Counted by listing
`*.py` here: 7 files, of which 5 are `test_*.py`, leaving 2 compilers; both are
now in the table. The dormancy claim for `build_corpus_map.py` was rechecked and
holds (line 19 sets `SOURCE` to `_corpus_source.yaml` under `09_TOOLS/`, which is
absent). Runnability receipt for the renderer, 2026-07-22:
`python3 09_TOOLS/02_COMPILERS/render_burri_rules.py --check` exited 0 with
`BURRI-OK topology valid; generated SVG bytes are current`.

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- UPLINK compile entry point: **none — archived 2026-07-20.**
  `compile_uplink.py` left `../01_SCRIPTS/` and is preserved at
  [`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/01_SCRIPTS/compile_uplink.py`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/01_SCRIPTS/compile_uplink.py).
  No live compiler in this lane builds UPLINK.
- full routing layer: **archived provenance, not live routing authority** —
  `00_INDEX.md` left `11_UPLINK/00_CORE/` on 2026-07-20 and is preserved at
  [`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/00_INDEX.md`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/00_INDEX.md);
  the live address is now the forwarding stub
  [`../../11_UPLINK/00_CORE/README.md`](../../11_UPLINK/00_CORE/README.md).

> **Corrected 2026-07-22.** Both bullets above previously named live targets.
> Counted by path test: 0 of 2 present. They were bare backticked paths, so the
> mechanical dead-citation and forwarding-stub gates did not see them.

---
rosetta:
  primary_level: L4
  primary_column: Script Operations
  secondary:
    - level: L3
      column: Validation Receipts
      role: "own manifest, link, Rosetta, and path repair helpers as audit-support tools"
    - level: L5
      column: Tooling Architecture
      role: "route reusable libraries and scenario harnesses to their owner folders"
    - level: L6
      column: Authority Boundary
      role: "prevent active scripts from overriding upstream source owners"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "01_SCRIPTS — Script Front Door"
title: "01_SCRIPTS"
status: "ACTIVE — script front door"
evidence_tier: "[B] for local script inventory; [I] for folder-boundary guidance."
---

# 01_SCRIPTS

## What This Folder Is

General-purpose repository scripts.

## What It Owns

- Manifest validation. **Archived 2026-07-20** — `manifest_check.py` moved to the
  [pure-boundary archive](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/01_SCRIPTS/);
  no manifest validator remains in this lane (corrected 2026-07-22).
- Uplink/state compilation. **Archived 2026-07-20** — `compile_uplink.py` and
  `compile_state.py` moved to the same archive; this lane no longer compiles
  UPLINK or state (corrected 2026-07-22).
- Corpus gates: dead citations, forwarding stubs, tree contract, purity, and
  rule-token linting.
- Rosetta annotation helpers.
- Path and link repair utilities.
- `check_tree_contract.py` — enforce top-level lanes, route triplets, Doors,
  forwarding targets, the single root governance spine, and a noise-free tree.
- One-file support scripts that are not large enough to become packages.

## What It Must Not Own

- Long-lived shared libraries. Route those to `../06_PACKAGES/`.
- Scenario-based simulations. Route those to `../03_SIMULATIONS/`.
- Historical one-off scripts. Route those to `../90_ARCHIVE/`.

## Read First

The gates this lane actually runs:

- `check_tree_contract.py`
- `check_dead_citations.py`
- `check_forwarding_stubs.py`
- `check_emergentism_purity.py`

**Corrected 2026-07-22.** This block previously listed `manifest_check.py`,
`compile_uplink.py`, `compile_state.py`, `validate_spec_links.py`, and
`path_rewrite_sweep.py` as the lane's entry points. Counted by testing each of
those five names against this folder: 0 present, 5 absent. All five were moved on
2026-07-20 and are preserved byte-intact in the
[pure-boundary archive](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/01_SCRIPTS/).
An agent following the old block reached nothing.

## Status

Active support folder. Scripts can compile, validate, and repair routing, but source owners remain upstream.

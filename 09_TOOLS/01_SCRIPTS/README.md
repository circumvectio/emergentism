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

- Manifest validation.
- Uplink/state compilation.
- Rosetta annotation helpers.
- Path and link repair utilities.
- One-file support scripts that are not large enough to become packages.

## What It Must Not Own

- Long-lived shared libraries. Route those to `../06_PACKAGES/`.
- Scenario-based simulations. Route those to `../03_SIMULATIONS/`.
- Historical one-off scripts. Route those to `../90_ARCHIVE/`.

## Read First

- `manifest_check.py`
- `compile_uplink.py`
- `compile_state.py`
- `validate_spec_links.py`
- `path_rewrite_sweep.py`

## Status

Active support folder. Scripts can compile, validate, and repair routing, but source owners remain upstream.

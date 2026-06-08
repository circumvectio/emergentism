---
rosetta:
  primary_level: L5
  primary_column: Package Front Door
  secondary:
    - level: L3
      column: Package Inventory Audit
      role: "state which package surfaces exist and which are still queued"
    - level: L4
      column: Build/Test Operations
      role: "keep install, test, and release claims tied to explicit commands"
    - level: L6
      column: Owner Boundary
      role: "keep reusable libraries downstream from source-owned doctrine and one-off scripts"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/D/I]"
  canonical_phrase: "06_PACKAGES"
title: "06_PACKAGES"
status: "ACTIVE — package front door"
evidence_tier: "[B] for package metadata and tested/released APIs; [D] for planned extraction; [I] for architectural routing."
---

# 06_PACKAGES

## What This Folder Is

Workspace package root for shared libraries used by tools and organism-facing scripts.

## What It Owns

- Reusable code packages.
- Package metadata and tests.

## What It Must Not Own

- One-off scripts. Route those to `../01_SCRIPTS/`.
- Simulations. Route those to `../03_SIMULATIONS/`.
- Doctrine. Route doctrine to the owning Foundation root.

## Current Packages

| Package | Status |
|---|---|
| `emergentism-core/` | [B] Package metadata exists (`pyproject.toml`, version `0.1.0`) with source under `src/emergentism_core/`; API/test/release status must be verified in the nested package pass. |

## Status

Active support folder.

## Rosetta Queue Note

The package root is only the folder-level authority surface. The nested
`emergentism-core/`, `src/`, `src/emergentism_core/`, and
`src/emergentism_core/polygenic/` route cards remain queued as separate
subfolder/package-boundary passes.

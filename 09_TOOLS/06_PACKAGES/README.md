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

None. This folder currently holds no package. `emergentism-core/` was moved out
of the pure-Emergentism boundary on 2026-07-20 and is preserved under
[`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/06_PACKAGES/emergentism-core/`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/06_PACKAGES/emergentism-core/).

## Status

Empty package root, retained as the declared destination for a future shared
library.

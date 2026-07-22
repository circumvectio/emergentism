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
| `emergentism-core/` | RETIRED from this lane on 2026-07-20. The whole package tree — `pyproject.toml` (version `0.1.0`) and `src/emergentism_core/` — was moved to the [pure-boundary archive](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/06_PACKAGES/emergentism-core/) and is preserved byte-intact there. No API, test, or release claim is carried forward. |

**This folder currently holds no package.** Counted 2026-07-22 by listing the
folder: 3 files (`AGENTS.md`, `CLAUDE.md`, `README.md`), 0 package directories;
`emergentism-core` resolves only under the pure-boundary archive. The row above
previously asserted in the present tense, at tier [B], that the package and its
`src/emergentism_core/` tree were here.

## Status

Active as a folder-level authority surface only — an empty package root. The
parent lane README does not list `06_PACKAGES/` among its active surfaces, and
records that application packages "were preserved intact under the pure-boundary
archive".

## Rosetta Queue Note

The package root is only the folder-level authority surface. The nested
`emergentism-core/`, `src/`, `src/emergentism_core/`, and
`src/emergentism_core/polygenic/` route-card passes are **withdrawn from the
queue as of 2026-07-22**: none of those paths exists in this lane. They are
archived provenance; should a package be reinstated here, queue fresh passes
against the reinstated paths rather than these.

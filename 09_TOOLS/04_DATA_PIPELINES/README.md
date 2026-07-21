---
rosetta:
  primary_level: L2
  primary_column: Data Pipeline Front Door
  secondary:
    - level: L3
      column: Evidence Audit
      role: "index local GFS outputs as receipts, not doctrine"
    - level: L4
      column: Pipeline Execution
      role: "identify active fetch and analysis scripts plus rerun boundaries"
    - level: L5
      column: Model Architecture
      role: "route interpretation into evidence and governance lanes"
  operator: "Kālī 💀"
  tier: "God"
  regime: "Śūdra"
  register: "[B/I/C]"
  canonical_phrase: "04_DATA_PIPELINES"
title: "04_DATA_PIPELINES"
status: "ACTIVE — data-pipeline front door"
evidence_tier: "[B] for local script/result inventory and source-backed outputs; [I] for interpretation; [C] for unreplicated statistical claims."
---

# 04_DATA_PIPELINES

Data ingestion, transformation, and analysis scripts plus their local output
artifacts.

## What Belongs Here

- fetchers and loaders for external datasets
- transformation and analysis scripts
- reproducible local outputs that are clearly tied to a pipeline run

## Current Focus

No GFS study surface remains active. The complete retired lane is preserved
under `90_ARCHIVE/2026_07_13_gfs_retraction/`.

## Current Pipeline Inventory

| Surface | Status |
|---|---|
| GFS fetcher, three analysis scripts, and dated result artifacts | **RETIRED.** Byte-preserved under `90_ARCHIVE/2026_07_13_gfs_retraction/`; no active copy remains. |
| `ra_files.txt` | [I] Legacy absolute-path inventory; do not treat as live route authority. |

## Authority Rule

Pipeline output is evidentiary or analytical support, not doctrine by default.
If a result changes an upstream claim, update the owning evidence or management
surface explicitly rather than letting a CSV or text artifact speak for the repo
on its own.

## Route Upstream

- tool inventory: `../README.md` and `../CLAUDE.md`
- evidence/governance interpretation: `../../08_FRAMEWORK_SUPPORT/03_EVIDENCE/`

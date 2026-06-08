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

This folder currently holds the GFS-oriented analysis lane and its supporting
artifacts.

## Current Pipeline Inventory

| Surface | Status |
|---|---|
| `download_gfs.py` | [B] OSF file-list fetcher for the GFS node; network-dependent, no local data write by default. |
| `gfs_22_country_analysis_v2_fixed.py` | [B] Preferred GFS Codebook v2 analysis script in this checkout. |
| `gfs_22_country_analysis.py` | [I] Earlier/provenance script; superseded for codebook-v2 runs by the v2-fixed variant. |
| `gfs_22_country_analysis_wave2.py` | [I] Wave-2/provenance variant; use only with matching source data and column-mapping review. |
| `gfs_results_20260409.csv` / `gfs_meta_analysis_20260409.txt` | [B] Local dated outputs from the GFS analysis lane; evidence artifacts, not doctrine. |
| `ra_files.txt` | [I] Legacy absolute-path inventory; do not treat as live route authority. |

## Authority Rule

Pipeline output is evidentiary or analytical support, not doctrine by default.
If a result changes an upstream claim, update the owning evidence or management
surface explicitly rather than letting a CSV or text artifact speak for the repo
on its own.

## Route Upstream

- tool inventory: `../README.md` and `../CLAUDE.md`
- evidence/governance interpretation: `../../08_FRAMEWORK_SUPPORT/03_EVIDENCE/`

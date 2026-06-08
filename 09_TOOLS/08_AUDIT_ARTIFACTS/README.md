---
rosetta:
  primary_level: L3
  primary_column: Audit Artifact Front Door
  secondary:
    - level: L4
      column: Audit Operations
      role: "name rerun and remediation boundaries before touching source-owner files"
    - level: L5
      column: Audit Topology
      role: "map dependency graph, link verification, and tooling health artifacts"
    - level: L6
      column: Generated Evidence Boundary
      role: "separate dated evidence from live doctrine and long-term archive material"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[B/I/D]"
  canonical_phrase: "08_AUDIT_ARTIFACTS"
title: "08_AUDIT_ARTIFACTS"
status: "ACTIVE — audit-artifact front door"
evidence_tier: "[B] for dated audit artifacts and runnable helper outputs; [I] for summaries; [D] for plans."
---

# 08_AUDIT_ARTIFACTS

## What This Folder Is

This folder stores outputs and helper scripts for tooling audits.

## What It Owns

- Generated audit reports.
- Audit helper scripts that inspect the corpus or dependency graph.
- Cross-folder link verification artifacts that need triage before source-owner repair.

## Current Inventory

| Surface | Tier | Use |
|---|---|---|
| `audit_dependency_graph.py` | [D/B] | Read-only dependency graph audit script; output is only current when rerun against the live tree. |
| `audit_output.md` | [B] | Generated dependency graph report from its recorded run; use as triage evidence, not live truth. |
| `CROSS_FOLDER_LINK_VERIFICATION_REPORT_2026_04_25.md` | [B] | Dated cross-folder link scan; some path recommendations are stale and must be rechecked before repair. |
| `TOOLS_AUDIT_REPORT.md` | [B/I] | Dated 09_TOOLS health audit; treat findings as queue input, not automatic edit authority. |

## What It Must Not Own

- Active doctrine.
- Source-owner corrections.
- Long-term archive material that belongs in `../90_ARCHIVE/`.

## Status

Support folder. Treat generated outputs as evidence surfaces, not authority surfaces.

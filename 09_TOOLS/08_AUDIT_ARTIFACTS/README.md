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
| `2026_08_01_FIRST_60_ADJUDICATION.jsonl` | [B] | Immutable adjudication evidence for actionable findings 1–60: one metadata record plus 60 finding records. The metadata fixes the source-journal hash and explains that asynchronous result order is not the finding identity. |
| `2026_08_01_REMAINING_169_ADJUDICATION.jsonl` | [B] | Immutable adjudication evidence for actionable findings 61–229: one metadata record plus 169 finding records. The metadata fixes the raw-findings, workflow-journal, and source-session hashes and declares `global_actionable_id = 60 + remaining_ordinal`. |
| `2026_08_01_REMAINING_169_INDEPENDENT_REVIEW_SUPPLEMENT.jsonl` | [B] | Additive independent-review custody: preserves the source ledger byte-for-byte while recording two disposition corrections, seven confirmed closures, one preserved owner gate, and the KSC-02 downstream-drift docket. |

The three dated reports formerly listed here were moved out of the
pure-Emergentism boundary on 2026-07-20 and are preserved under
[`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/08_AUDIT_ARTIFACTS/`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/08_AUDIT_ARTIFACTS/).
The two JSONL ledgers above are bounded run evidence, not doctrine or authority;
their rows must not be rewritten to make a later audit look cleaner.

## What It Must Not Own

- Active doctrine.
- Source-owner corrections.
- Long-term archive material that belongs in `../90_ARCHIVE/`.

## Status

Support folder. Treat generated outputs as evidence surfaces, not authority surfaces.

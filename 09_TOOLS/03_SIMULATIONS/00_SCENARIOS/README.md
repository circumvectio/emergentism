---
rosetta:
  primary_level: L5
  primary_column: Scenario Fixture Front Door
  secondary:
    - level: L4
      column: Harness Execution
      role: "index active scenario fixtures that can be run through ../harness.py"
    - level: L3
      column: Assertion Audit
      role: "distinguish YAML inputs, transcripts, and assertion receipts"
    - level: L6
      column: Dormant Boundary
      role: "mark future scenario families as placeholders rather than active fixtures"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/D/I]"
  canonical_phrase: "00_SCENARIOS"
title: "00_SCENARIOS"
status: "ACTIVE — scenario fixture front door"
evidence_tier: "[B] for local fixture inventory and harness path; [D] for placeholder families; [I] for folder-boundary guidance."
---

# 00_SCENARIOS

## What This Folder Is

Scenario fixtures for the actor simulation harness.

## What It Owns

- YAML scenario inputs.
- Expected transcript/assertion fixtures where present.

## What It Must Not Own

- The harness implementation. Route current Packet 164 work to `../harness.py`.
- Older standalone simulations. Route those to `../`.

## Current Scenario Families

| Family | Status |
|---|---|
| `00_happy/` | [B] Active fixture family with YAML input, transcript, and assertion receipt. |
| `01_byzantine/` | [B] Active fixture family with YAML input, transcript, and assertion receipt. |
| `02_withholding/` | [B] Active fixture family with YAML input, transcript, and assertion receipt. |
| `03_partition/` | [B] Active fixture family with YAML input, transcript, and assertion receipt. |
| `04_combined/` | [D] Placeholder; no active scenario fixture files in this checkout. |
| `05_cluster/` | [D] Placeholder; no active scenario fixture files in this checkout. |
| `06_cross/` | [D] Placeholder; no active scenario fixture files in this checkout. |

## Status

Active support fixtures.

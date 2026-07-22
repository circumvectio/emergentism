---
rosetta:
  primary_level: L5
  primary_column: DAC Script Front Door
  secondary:
    - level: L3
      column: Script Inventory Audit
      role: "separate folder ownership from current script inventory, test coverage, and run receipts"
    - level: L4
      column: Support Operations
      role: "route lifecycle scripts, manual processing, and membrane helpers to this lane"
    - level: L6
      column: Ownership Boundary
      role: "prevent DAC-frame scripts from absorbing general repository scripts or doctrine"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/B]"
  canonical_phrase: "scripts"
title: "scripts"
status: "FRONT DOOR — DAC-frame scripts support folder"
evidence_tier: "[I] for folder ownership; [B] only for current script inventory, tests, run logs, or code receipts."
---

# scripts

## What This Folder Is

Executable scripts for the DAC frame toolset.

**Rosetta boundary:** [I] This front door owns DAC-frame support scripts. It
does not prove script behavior, safety, coverage, or execution; [B] those require
current code, tests, and run logs.

## What It Owns

- DAC frame lifecycle scripts.
- Manual processing and membrane-operation helpers.

## What It Must Not Own

- [I] General repository scripts. Route those to `../../01_SCRIPTS/`.
- [I] DAC frame doctrine. Route that to `../blueprint/` or `../constitution/`.

## Status

Active DAC-frame support folder.

---
rosetta:
  primary_level: L4
  primary_column: Scenario Fixture Execution
  secondary:
    - level: L3
      column: Assertion Audit
      role: "bind the byzantine YAML to its transcript and assertion receipt"
    - level: L5
      column: Simulation Architecture
      role: "route harness behavior back to the parent simulation architecture"
    - level: L6
      column: Fixture Boundary
      role: "prevent one adversarial fixture from becoming a global runtime proof"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "01_byzantine"
title: "01_byzantine"
status: "ACTIVE — byzantine-minority fixture"
evidence_tier: "[B] for local fixture files and asserted properties; [I] for harness-behavior interpretation."
---

# 01_byzantine

## What This Folder Is

Minority-byzantine fixture: 2 honest validators, 1 byzantine validator that
withholds signatures, 1 honest archiver, over 20 rounds. Tests that a byzantine
minority cannot finalize.

## Files

| File | Role |
|---|---|
| `minority_byzantine.yaml` | [B] Scenario input (actors, events, asserted properties). |
| `minority_byzantine.transcript` | [B] Expected deterministic transcript fixture. |
| `minority_byzantine.assertions` | [B] Recorded assertion receipt for the run. |

## Asserted Properties

- `every_super_checkpoint_reaches_green`
- `no_event_pruned_before_bundle_verified`
- `byzantine_minority_cannot_finalize`

## Run

See [`../../harness.py`](../../harness.py) for the actor simulation
implementation and [`../README.md`](../README.md) for the scenario family
overview.

## Boundary

A passing fixture supports a property under these inputs; it does not by itself
upgrade a runtime claim to doctrine. Route runtime status through the owning
management lane.

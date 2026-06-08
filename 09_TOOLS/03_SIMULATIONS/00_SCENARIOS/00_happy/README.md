---
rosetta:
  primary_level: L4
  primary_column: Scenario Fixture Execution
  secondary:
    - level: L3
      column: Assertion Audit
      role: "bind the happy-path YAML to its transcript and assertion receipt"
    - level: L5
      column: Simulation Architecture
      role: "route harness behavior back to the parent simulation architecture"
    - level: L6
      column: Fixture Boundary
      role: "prevent one happy-path fixture from becoming a global runtime proof"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "00_happy"
title: "00_happy"
status: "ACTIVE — happy-path fixture"
evidence_tier: "[B] for local fixture files and asserted properties; [I] for harness-behavior interpretation."
---

# 00_happy

## What This Folder Is

The honest-path baseline fixture for the actor simulation harness: 3 honest
validators, 1 honest archiver, 10 events across 20 rounds, 2 super-checkpoints.

## Files

| File | Role |
|---|---|
| `honest_path.yaml` | [B] Scenario input (actors, events, asserted properties). |
| `honest_path.transcript` | [B] Expected deterministic transcript fixture. |
| `honest_path.assertions` | [B] Recorded assertion receipt for the run. |

## Asserted Properties

- `every_super_checkpoint_reaches_green`
- `no_event_pruned_before_bundle_verified`
- `deterministic_transcript_hash`

## Run

See [`../../harness.py`](../../harness.py) for the actor simulation
implementation and [`../README.md`](../README.md) for the scenario family
overview.

## Boundary

A passing fixture supports a property under these inputs; it does not by itself
upgrade a runtime claim to doctrine. Route runtime status through the owning
management lane.

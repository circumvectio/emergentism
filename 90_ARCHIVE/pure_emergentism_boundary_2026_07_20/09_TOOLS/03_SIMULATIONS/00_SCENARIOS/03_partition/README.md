---
rosetta:
  primary_level: L4
  primary_column: Scenario Fixture Execution
  secondary:
    - level: L3
      column: Assertion Audit
      role: "bind the partition YAML to its transcript and assertion receipt"
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
  canonical_phrase: "03_partition"
title: "03_partition"
status: "ACTIVE — network-partition fixture"
evidence_tier: "[B] for local fixture files and asserted properties; [I] for harness-behavior interpretation."
---

# 03_partition

## What This Folder Is

Network-partition fixture: 4 honest validators split into two islands of 2 for
5 rounds, 1 archiver, over 30 rounds. Tests that a checkpoint created after the
partition heals still reaches green.

## Files

| File | Role |
|---|---|
| `network_partition.yaml` | [B] Scenario input (actors, events, asserted properties). |
| `network_partition.transcript` | [B] Expected deterministic transcript fixture. |
| `network_partition.assertions` | [B] Recorded assertion receipt for the run. |

## Asserted Properties

- `every_super_checkpoint_reaches_green`
- `no_event_pruned_before_bundle_verified`

## Run

See [`../../harness.py`](../../harness.py) for the actor simulation
implementation and [`../README.md`](../README.md) for the scenario family
overview.

## Boundary

A passing fixture supports a property under these inputs; it does not by itself
upgrade a runtime claim to doctrine. Route runtime status through the owning
management lane.

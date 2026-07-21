---
rosetta:
  primary_level: L4
  primary_column: Scenario Fixture Execution
  secondary:
    - level: L3
      column: Assertion Audit
      role: "bind the withholding YAML to its transcript and assertion receipt"
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
  canonical_phrase: "02_withholding"
title: "02_withholding"
status: "ACTIVE — archiver-withholding fixture"
evidence_tier: "[B] for local fixture files and asserted properties; [I] for harness-behavior interpretation."
---

# 02_withholding

## What This Folder Is

Archiver-withholding fixture: 3 honest validators, 1 dishonest archiver that
withholds bundles, over 20 rounds. Tests that a checkpoint still reaches green
via validator quorum despite the withholding archiver.

## Files

| File | Role |
|---|---|
| `archiver_withhold.yaml` | [B] Scenario input (actors, events, asserted properties). |
| `archiver_withhold.transcript` | [B] Expected deterministic transcript fixture. |
| `archiver_withhold.assertions` | [B] Recorded assertion receipt for the run. |

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

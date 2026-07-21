---
rosetta:
  primary_level: L4
  primary_column: DAC Harness Execution
  secondary:
    - level: L3
      column: Assertion Receipts
      role: "treat transcripts and assertion JSON as local evidence artifacts"
    - level: L5
      column: Simulation Architecture
      role: "keep Packet 164 harness structure tied to the simulation lane"
    - level: L6
      column: Runtime Boundary
      role: "prevent harness behavior from becoming current runtime truth without upstream receipts"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "DAC Simulation Harness"
title: "DAC Simulation Harness"
status: "ACTIVE — harness execution guide"
evidence_tier: "[B] for local harness path and runnable scenario commands; [I] for Packet-era implementation notes."
---

# DAC Simulation Harness

**Evidence tier:** [I] — implementation artifact per Packet 164
**Status:** Track A week 2 deliverable; Track B week 3 entry point
**Kill criteria:** ≤ 1 engineer-week; simplicity beats completeness

---

## Current Route

This is the numbered tool lane for the Packet 164 DAC simulation harness.
Scenario fixtures live in `00_SCENARIOS/`.

Old Packet 164-era references to `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/` should
route here.

## Quick start

```bash
# Run a single scenario
python3 harness.py run --scenario 00_SCENARIOS/00_happy/honest_path.yaml

# Run all scenarios in a directory
python3 harness.py run --dir 00_SCENARIOS/00_happy/

# Verify determinism (same seed → identical transcript)
python3 harness.py verify --scenario 00_SCENARIOS/00_happy/honest_path.yaml --runs 5
```

## Scenario classes

| Directory | Class | Description |
|---|---|---|
| `00_SCENARIOS/00_happy/` | Happy path | All honest actors |
| `00_SCENARIOS/01_byzantine/` | Byzantine validators | Dishonest validators withhold signatures |
| `00_SCENARIOS/02_withholding/` | Archiver withholding | Dishonest archiver refuses bundles |
| `00_SCENARIOS/03_partition/` | Network partition | Validator set split temporarily |
| `00_SCENARIOS/04_combined/` | Combined attack | Multiple attacks simultaneously (week 7+) |
| `00_SCENARIOS/05_cluster/` | Organ layer | Cluster formation/dissolution (Track B week 3) |
| `00_SCENARIOS/06_cross/` | Cross-layer | Substrate + organ interaction (week 7+) |

## Actor types

### Substrate (Track A)

| Actor | Key transitions |
|---|---|
| `Validator` | `sign_checkpoint(cp_height)` |
| `Archiver` | `store_bundle(cp_height)`, `withhold_bundle(cp_height)` |
| `Event` | Passive — produced by validators |
| `SuperCheckpoint` | `transition_to_green(quorum_sigs)` |

### Organ (Track B)

| Actor | Key transitions |
|---|---|
| `Cluster` | `merge_members()`, `split_member()` |

## Output files

Each run produces:
- `.transcript` — JSON-per-line action log
- `.assertions` — assertion check results

## Determinism Target

[B] The harness uses seeded randomness. Same YAML + same seed should produce a byte-identical transcript; verify with `python3 harness.py verify ...` before treating a transcript as a receipt.

## Extending the harness

- **Add actors:** Subclass `Actor`, implement `act(round, global_state)`
- **Add scenarios:** Write YAML in `00_SCENARIOS/XX_class/name.yaml`
- **Add assertions:** Extend `Harness._check_assertions()`

## References

- Packet 164 — Simulation Harness Shared Spec (Track A ↔ Track B)
- Packet 154 §2.7 — Track A/B coordination
- Packet 162 §3.4 — Track A Week 2 D4 gate

`Zero-Sum Resolution Equation`

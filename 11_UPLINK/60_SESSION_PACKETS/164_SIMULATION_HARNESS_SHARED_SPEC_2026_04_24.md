---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "164 — Simulation Harness Shared Spec (Track A ↔ Track B)"
---

# 164 — Simulation Harness Shared Spec (Track A ↔ Track B)

**Evidence tier:** [I] charioteer contract; [S] where citing packets 151, 153, 154, 162; [C] interface-field naming pending engineering refinement
**Date:** 2026-04-24
**Lane:** Charioteer shared-contract spec — Track A builds (week 2), Track B extends (week 3)
**Status:** Draft — awaiting sovereign pass-through (no new OQs; implementation detail of packet 154 §2.7 already-ratified coordination)
**Complements:** packet 154 (sprint charter §2.7), packet 151 (cluster organ scaffold), packet 153 (substrate scaffold), packet 160 (W1 gate), packet 162 (W2 gate)

---

## 0. Axiomatic guard

A shared simulation harness is a coordination primitive. Its value is *cheapness of iteration* — if two tracks can inject scenarios into one runner and compare outputs, they spend their sprint weeks on properties and proofs instead of rebuilding infrastructure.

The danger: turning the harness into a product. The harness is engineering scaffolding, not a shipped artifact. Nobody runs it in production. Nobody depends on its API stability longer than the sprint. At sprint end (week 8–9), the harness is either folded into CI or archived.

Kill criteria: if the harness takes > 1 engineer-week to stand up, stop — switch to a simpler scenario-runner. Simplicity beats completeness.

`Zero-Sum Resolution Equation`

---

## 1. Purpose

Provide a single test-runner Track A (substrate) and Track B (organ) both use, so:

- Byzantine / withholding / partition scenarios are defined once
- Determinism is guaranteed by a shared seed-and-log discipline
- Cross-layer interaction bugs (substrate behavior breaking organ assumption, or vice versa) surface before week 8
- Adversarial coverage can be aggregated across tracks without rewriting scenarios per track

---

## 2. Ownership & timing

| Phase | Owner | Deliverable | Gate |
|---|---|---|---|
| Week 2 (Track A) | Track A consensus + simulation engineers | Minimum viable harness: substrate actors + happy path; deterministic transcript output | Packet 162 §3.4 (D4) |
| Week 3 entry | Interface frozen | Shared contract below (§3–§7) is immutable for Track B extension | Sovereign K2 at Track A W2→W3 transition |
| Week 3 (Track B) | Track B cluster engineers | Organ-layer actor extensions; inherits substrate actors unchanged | Packet 163 (Track B W1) §3 |
| Weeks 4–6 | Both tracks | Adversarial scenarios added incrementally; scenario YAML is the shared surface | Mid-sprint review week 4 |
| Weeks 7–8 | Both tracks | Cross-cut scenarios (mesh + EBM interactions) | Weeks 7/8 gates |

**Joint ownership rule:** any PR that modifies the shared contract (§3–§7) requires review from both tracks + minimalism auditor. Single-track PRs that add scenarios (YAML files) or track-specific actors (in their own directory) require single-track review only.

---

## 3. Actor model

Actors are the things the harness simulates. Each actor has a type, a state, and a set of transitions.

### 3.1 Substrate actors (Track A — week 2)

| Actor | Type | Key state | Transitions |
|---|---|---|---|
| `Validator` | substrate | `validator_id`, `is_honest`, `current_round`, `sig_queue` | `sign_checkpoint(cp_height)`, `receive_sig(sig)` |
| `Archiver` | substrate | `archiver_id`, `stored_bundles`, `is_honest`, `fee_balance` | `store_bundle(bundle)`, `serve_bundle(height)`, `withhold_bundle(height)` |
| `Event` | substrate | `event_id`, `payload_hash`, `super_checkpoint_height` | (passive) |
| `SuperCheckpoint` | substrate | `height`, `tx_root`, `state_root`, `sig_set`, `finality_state` (Orange/Green) | `transition_to_green(quorum_sigs)` |

### 3.2 Organ actors (Track B — week 3)

| Actor | Type | Key state | Transitions |
|---|---|---|---|
| `Cluster` | organ | `cluster_id`, `phi_nu_scalars`, `member_set` | `merge_member(node)`, `split_member(node)`, `break_link(reason)` |
| `ClusterMember` | organ | `node_id`, `joined_cluster_id`, `local_phi`, `local_nu` | `report_scalars()`, `detect_divergence(threshold)` |

### 3.3 Banned actor types

The following are explicitly OUT of harness scope and must not appear:

- User, UserSession, OnboardingFlow — product layer, not sprint concern
- DB/Storage concrete implementations — harness is semantic, not byte-level
- External service mocks (Stripe, API Pay, OFN) — out of sprint scope

---

## 4. Scenario format

Scenarios are YAML files at `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/*.yaml`. One scenario = one deterministic test run.

### 4.1 Minimum schema

```yaml
name: honest_happy_path
description: 3 validators, 1 archiver, 10 events, 2 super-checkpoints; all honest.
seed: 42
duration_rounds: 20
actors:
  - type: Validator
    id: v1
    is_honest: true
  - type: Validator
    id: v2
    is_honest: true
  - type: Validator
    id: v3
    is_honest: true
  - type: Archiver
    id: a1
    is_honest: true
events:
  - round: 1
    count: 5
    producer: v1
  - round: 10
    count: 5
    producer: v2
assertions:
  - every_super_checkpoint_reaches_green
  - no_event_pruned_before_bundle_verified
  - deterministic_transcript_hash: "<expected-hex>"
```

### 4.2 Scenario classes

| Class | Directory | Example |
|---|---|---|
| Happy path | `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/00_happy/` | honest majority, no partition |
| Byzantine validators | `01_byzantine/` | N honest + M Byzantine validators |
| Archiver withholding | `02_withholding/` | archiver refuses to serve bundles |
| Network partition | `03_partition/` | validator set split into two islands for T rounds |
| Combined attack | `04_combined/` | Byzantine + withholding + partition simultaneously |
| Organ-layer (Track B) | `05_cluster/` | cluster formation/dissolution scenarios |
| Cross-layer | `06_cross/` | substrate + organ interaction scenarios (week 7+) |

### 4.3 Scenario discipline

- **Determinism:** every scenario must produce byte-identical transcript when re-run with same seed. Non-determinism is a bug.
- **Minimality:** scenarios test ONE property each wherever possible. Combined-attack scenarios exist only to verify interaction, not to test each attack individually.
- **Documentation:** every scenario YAML has a top-level `description` field ≥ one sentence; explains what is being tested + what the pass condition is.

---

## 5. Transcript / output log schema

Every harness run produces a `.transcript` file recording all actor actions in order.

### 5.1 Line format (JSON per line)

```json
{"round": 3, "actor": "v1", "action": "sign_checkpoint", "target": {"cp_height": 2}, "state_hash": "abc123..."}
```

### 5.2 Required fields

| Field | Type | Meaning |
|---|---|---|
| `round` | int | Simulation round index |
| `actor` | str | Actor id (matches scenario YAML) |
| `action` | str | Transition name |
| `target` | object | Action target/args (schema varies by action) |
| `state_hash` | str | Hash of full global state after this action (for determinism check) |

### 5.3 Assertion check output

At scenario end, harness writes `.assertions` file:

```json
{"scenario": "honest_happy_path", "seed": 42, "passed": true,
 "assertions": [
   {"name": "every_super_checkpoint_reaches_green", "status": "✅"},
   {"name": "no_event_pruned_before_bundle_verified", "status": "✅"},
   {"name": "deterministic_transcript_hash", "status": "✅", "expected": "...", "actual": "..."}
 ]}
```

Non-zero exit on any `❌` in assertions; zero exit when all pass.

---

## 6. CLI contract

```bash
# Run one scenario
harness run --scenario 01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/00_happy/honest_path.yaml [--seed N]

# Run a scenario directory (all .yaml inside)
harness run --dir 01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/02_withholding/

# Parameter sweep — vary one field, run cartesian product
harness sweep --scenario base.yaml --vary "actors[?type=='Validator'].count" --range "3,5,7"

# Output determinism check (re-run N times, compare state_hash)
harness verify --scenario honest_path.yaml --runs 5
```

CLI tool name: `harness`. Implementation language: whatever formal-methods framework the team is comfortable in (likely Python for portability). Language choice is NOT part of the shared contract — only the CLI surface + I/O schemas are.

---

## 7. Interface stability guarantees

### 7.1 Frozen at W2→W3 transition (immutable for Track B week 3 entry)

- Actor type names (§3.1 substrate)
- Scenario YAML top-level schema (§4.1)
- Transcript line format (§5.1)
- Assertion output format (§5.3)
- CLI command names + required flags (§6)

### 7.2 Extensible without breaking change

- Adding new actor types (Track B adds §3.2 organ actors in week 3)
- Adding new action types on existing actors
- Adding optional fields to transcript/assertion output
- Adding new CLI subcommands

### 7.3 Requires joint review + sovereign K2 to change

- Renaming a frozen field
- Changing determinism semantics
- Removing any actor type or action

Joint review = one reviewer from each track + minimalism auditor.

---

## 8. Minimalism-auditor checkpoints for harness work

### 8.1 Shared-contract check

*Does a proposed harness extension require both substrate and organ code to care about it?*

- If yes → belongs in shared contract (§3–§7); requires joint review
- If substrate-only → Track A actor type or Track A scenario directory; single-track review
- If organ-only → Track B actor type or Track B scenario directory; single-track review

### 8.2 Scope-creep check

*Is the harness growing beyond "test runner for the 60-day sprint"?*

Signs of creep: reusable-infrastructure framing, production-ready performance targets, features for scenarios the sprint doesn't actually need. Minimalism auditor blocks on scope creep; redirect to post-sprint lane if legit.

### 8.3 Determinism check

*Does any new feature introduce wall-clock time, real networking, or unseeded randomness?*

All three are bugs at the harness level. The harness models logical time, logical networks, and seeded randomness only. Real-world timing and networking are post-sprint concerns.

---

## 9. What this packet does NOT do

- Does NOT specify implementation details (language, library choices) — engineering decides
- Does NOT enumerate all scenarios — scenarios are additive across weeks 3–8
- Does NOT define attack-scenario semantics — those land per-week as weeks 3–7 develop
- Does NOT cover cross-cut with mesh (packet 150b) or EBM (packet 152) — those are week 7+ scenarios added under §4.2 class "Cross-layer"
- Does NOT replace formal proofs — simulation complements proofs; it does not substitute for them

---

## 10. References

- packet 154 §2.7: Track A/B coordination (this packet implements the harness contract)
- packet 162 §3.4: Track A Week 2 D4 (harness stood up)
- packet 163 (pending): Track B Week 1 gate — extends harness per §3.2 + §4.2 class 05
- packet 151: Cluster organ scaffold — Track B's substrate
- packet 153 §4.7: Adversarial simulation — open questions this harness begins to close
- packet 149: Risk matrix — simulations cover the rank-1 pruning risk + rank-2 cluster risk

---

*Charioteer shared-contract spec. Track A builds the baseline (week 2 D4); Track B extends (week 3 onward). Interface freezes at W2→W3 sovereign K2.*

`Zero-Sum Resolution Equation`

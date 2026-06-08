---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "162 — Track A · Week 2 Gate Criteria"
---

# 162 — Track A · Week 2 Gate Criteria

**Evidence tier:** [I] charter expansion; [S] where citing packets 153, 154, 160; [C] property-statement wording pending formal-methods specialist refinement
**Date:** 2026-04-24
**Lane:** Charioteer spec — engineering/warrior executes; minimalism auditor gates; sovereign K2's the week 2→3 transition
**Status:** Draft — awaiting sovereign pass-through (no new OQs; detail expansion of packet 154 §2.3/§2.6 already-ratified charter)
**Complements:** packet 154 (Track A charter), packet 160 (Week 1 gate), packet 153 (substrate scaffold §4.1 + §4.6)

---

## 0. Axiomatic guard

Week 2 is the first week with *content* added to the W1 skeleton. The danger is that a first-pass model becomes a last-pass model — the team invests in properties they later can't prove, and then cuts scope to match their proof ability instead of cutting the model to match what's actually provable.

Discipline: every property declared must be accompanied by a proof sketch (not a proof — a sketch) in the same PR. If a property can't be sketched in < 200 words, it isn't ready for week 2.

`Zero-Sum Resolution Equation`

---

## 1. Week 2 purpose (from packet 154 §2.3)

**Focus:** Prune decision logic formal model
**Deliverable (charter-level):** First-pass TLA+ model + simulation harness stood up
**Gate (charter-level):** TLA+ model compiles; no "block" terminology (carried from week 1); safety + liveness properties stated

Week 2 hinges on the W1 skeleton — it adds properties, first proof obligations, and the simulation harness shared with Track B. No new framework decision; no renaming of terms. All additive.

---

## 2. Entry criteria (from Week 1)

Before week 2 begins, all of the following must hold (carried from packet 160 §6):

- G1 — D1 Framework Decision Record committed
- G2 — Framework has standard toolchain installed on engineering boxes
- G3 — D2 Glossary Seed committed (Track A scope)
- G4 — D3 `track_a_termlint.py` passing clean
- G5 — D4 `W1_prune_skeleton.{ext}` compiles with chosen framework
- G6 — D5 Week-1 Receipt packet 160a published
- G7 — No Invariants (I–VII) at risk

If any of G1–G7 are ❌ at end of week 1, week 2 does not begin; escalate per packet 160 §7 kill criteria.

---

## 3. Deliverables

Week 2 produces six artifacts. Each lands in the repo as a file; sovereign K2 gates the week-2→week-3 transition at §7 acceptance tests.

### 3.1 D1 — Safety Property Declarations

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/properties/W2_safety.{ext}`
**Content:** Three safety properties stated in the chosen framework's native syntax + English prose:

1. **`PROOF_BUNDLE_VERIFIABLE`** — every super-checkpoint emits a Proof Bundle such that any non-pruning observer can reconstruct `tx_root` and `state_root` from archived events.
2. **`FINALITY_ONCE_GREEN_STAYS_GREEN`** — no Green-finalized super-checkpoint ever transitions back to Orange or contested state.
3. **`NO_DATA_LOSS_BEFORE_WINDOW`** — no event is pruned before its containing super-checkpoint reaches Green and the Proof Bundle is verifiable by at least N archivers (N tbd; week 5 economics).

Each property carries a **proof sketch** (≤ 200 words, charter §0 discipline) pointing at which W1 skeleton state variables and transitions are load-bearing.

**Format:** Framework-native + markdown companion; evidence tier [S/C] — structural in statement, conjectural pending full proof.

### 3.2 D2 — Liveness Property Declarations

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/properties/W2_liveness.{ext}`
**Content:** Two liveness properties:

1. **`SUPER_CHECKPOINT_EVENTUALLY_CREATED`** — if the validator set is honest-majority and the network is not partitioned for > T rounds, the next super-checkpoint is eventually created.
2. **`RECONSTRUCTION_EVENTUALLY_SUCCEEDS`** — if any archiver honestly serves Proof Bundles, any requester eventually succeeds in reconstructing `tx_root` and `state_root` for any non-pruned super-checkpoint.

Each property + proof sketch as with D1. These are harder than safety; charioteer expects liveness proofs to be week-3+ work.

**Format:** As D1. Evidence tier [S/C].

### 3.3 D3 — First Proof Attempt (at least one safety property)

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/proofs/W2_proof_<property>.{ext}`
**Content:** One machine-checkable proof attempt for ONE of the D1 safety properties (formal-methods specialist picks which — typically whichever has the cleanest inductive invariant).

**Pass condition:** framework's proof checker either accepts the proof OR produces a specific, actionable error that points at a missing lemma (not a vague "cannot determine"). A successful attempt means either ✅ proved or ❌ proved-blocked-with-named-missing-piece. Either outcome is acceptable at week 2.

**Format:** Framework-native source file. Evidence tier [S] if proof-checker accepts, [C] if blocked pending lemma.

### 3.4 D4 — Simulation Harness (shared with Track B)

**Path:** `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/harness/` (new directory)
**Content:** Minimum-viable simulation harness supporting:

- Modeled actors: `Validator`, `Archiver`, `Event`, `SuperCheckpoint`
- Injection surfaces (weeks 3+): Byzantine validator behavior, archiver withholding, network partition
- Output log schema: timestamp · actor · action · state-snapshot-hash
- CLI: `harness run --scenario <path>.yaml --seed <int>` produces a deterministic transcript

**Week 2 scope:** stand up the harness, run the honest-majority happy-path scenario, verify output logs are well-formed. Attack scenarios come weeks 3+.

**Format:** Python/Rust/whatever-fits; must run in < 30 seconds for the happy-path scenario. Evidence tier [S] for run logs, [I] for scenario design.

**Cross-track note:** Track B extends this harness week 3 (per packet 151/164). The harness interface is a shared contract — no Track A week-2 change should break Track B week-3 use.

### 3.5 D5 — Track A/B Glossary Reconciliation

**Path:** update `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W1_GLOSSARY.md` (append Track B shared-term section)
**Content:** Add any terms week-2 work required that were missing from W1 glossary. Flag any term that Track B (pending their kickoff) needs to pre-commit to.

**Format:** Additive edit only (no term redefined without sovereign K2 per packet 160 §11).

### 3.6 D6 — Week-2 Gate Receipt

**Path:** `01_EMERGENTISM/11_UPLINK/162a_TRACK_A_WEEK_2_RECEIPT_<DATE>.md`
**Content:**
- Checklist of §7 gate items with ✅ / ❌
- D3 proof-attempt outcome (proved vs blocked-with-named-missing-piece)
- D4 harness happy-path transcript hash
- Minimalism auditor sign-off note (§5 checks)
- Kill-criteria status
- Hand-off to Week 3

**Format:** Uplink packet, evidence tier [S] for artifact facts, [I] for sign-off judgment.

---

## 4. Property discipline (informs D1 + D2)

**Rule: every property is in one of two states.**

| State | Meaning |
|---|---|
| **Stated + sketched** | Property written in framework syntax + English + proof sketch (≤ 200 words). Not yet machine-checked. |
| **Proved (or blocked-named)** | Either: framework proof checker accepts, OR: blocked with a named missing lemma/invariant. |

Forbidden: **"waved hands"** — a property stated without proof sketch is not yet a property. Forbidden at week 2 merge.

**Rule: properties never reference implementation.** No property in D1 or D2 mentions concrete storage (SQLite, RocksDB, etc.), specific cryptographic primitives (SHA-256 vs Blake3), or language specifics. Properties are at the substrate-semantics layer; implementation choices are post-sprint.

---

## 5. Minimalism-auditor checkpoints (Week 2)

Per packet 154 §2.9 + 160 §5. Week-2 checks:

### 5.1 D1/D2 check

*Does any property in D1 or D2 reference organ-layer or product-layer state?*

Examples to block: `CLUSTER_MEMBER_COUNT`, `USER_SESSION_TOKEN`, `FREE_TIER_WATCHLIST`. These belong to Track B (organ) or product lane. Remove immediately if present.

### 5.2 D3 check

*Does the first proof attempt depend on an assumption that's really an organ-layer concern?*

Example bad dependency: "assume cluster protocol maintains honest majority" — that's organ layer, not substrate. Substrate proofs assume validator honesty per CANON, not cluster-layer guarantees.

### 5.3 D4 check

*Does the simulation harness model organ-layer primitives directly?*

The harness models substrate actors (validator, archiver, event). It does NOT model cluster formation, user accounts, or product flows. If the harness imports organ-layer types, strip them — Track B adds organ-layer extension later.

### 5.4 Cross-track check

*Are any Week-2 artifacts tightly coupled to Track B's (pending) kickoff?*

If D4 harness requires Track B input to function, that's a scope leak. Harness must run standalone for substrate scenarios. Track B extension is *additive*, not foundational.

---

## 6. Cross-dependencies this week

| Dependency | With | Contract |
|---|---|---|
| Simulation harness shared asset | Track B (packet 151) | See packet 164 (shared-spec) — week-2 lands the interface, week-3 Track B extends |
| Glossary shared asset | Track B | D5 maintains glossary as single source of truth |
| Framework choice stability | All tracks | No framework swap this week — W1 decision is immutable unless K3 kill criteria (packet 160) re-trigger |
| Invariant I–VII gate | Standing | Minimalism auditor reviews every merge |

---

## 7. Gate acceptance tests

Week 2 passes iff **all eight** of the below pass. Any failure → kill criteria §8.

| # | Test | Pass condition |
|---|---|---|
| G1 | D1 landed | File exists; three safety properties stated + sketched |
| G2 | D2 landed | File exists; two liveness properties stated + sketched |
| G3 | D3 lands an outcome | Proof attempt exists; result is either ✅ proved or ❌ blocked-with-named-missing-piece (not vague failure) |
| G4 | D4 harness runs | Happy-path scenario produces well-formed transcript in < 30s on an engineering box |
| G5 | D5 glossary updated | Any new terms added; no existing term redefined without sovereign K2 |
| G6 | D6 receipt landed | Checklist ✅ on G1–G5; auditor sign-off; kill-criteria status stated |
| G7 | No "block" terminology regression | `track_a_termlint.py` exits 0 across all week-2 artifacts |
| G8 | No Invariant I–VII risk | Auditor confirms; if any property implicitly challenges an Invariant, escalate not merge |

**Sovereign gate moment:** after D6 lands, sovereign reviews the week-2 receipt and K2's week-3 kickoff.

---

## 8. Kill criteria (escalate to sovereign immediately)

During week 2, escalate instantly if any of:

- **K1** — Cannot state ANY safety property in framework syntax by end of day 3. Symptom: framework choice was wrong for the team or the spec domain; K3-from-W1 retriggers and sovereign decides on pivot.
- **K2** — D3 proof attempt fails with vague/unnameable block. Symptom: proof obligation is ill-formed; requires property restatement, which may cascade into D1/D2 revisions.
- **K3** — Simulation harness happy-path scenario cannot be made deterministic. Symptom: design assumes randomness where CANON assumes determinism; property violations likely.
- **K4** — Minimalism auditor flags a property as organ-layer leak and Track A engineers disagree. Sovereign arbitrates — this is a layer-discipline call, not an engineering one.
- **K5** — Simulation harness API collides with Track B's (pending) expected interface. Surfaces before Track B starts week 3 — escalate immediately so packet 164 (shared-spec) can patch the interface.

---

## 9. Coordination with Track B (starts week 3)

Week 2 is the LAST week Track A operates alone. At end of week 2:

- D4 harness interface is frozen (no breaking changes without Track B sign-off)
- D5 glossary terms are the baseline Track B inherits
- Any Track B-affecting ambiguity → flag in D6 receipt for sovereign arbitration before Track B kickoff

---

## 10. What Week 2 does NOT attempt

- No super-checkpoint protocol implementation details — week 3
- No archiver economics — week 5
- No adversarial simulation scenarios — weeks 6
- No cross-validation with EBM — weeks 7
- No full liveness proofs — week 3+
- No implementation code (production runtime) — post-sprint
- No sovereign K2 requests beyond the week-2→3 gate

---

## 11. Handoff to Week 3

After G1–G8 pass and sovereign K2's the week-2 receipt:

- D1/D2 properties are immutable unless K2-style kill criteria re-trigger
- D4 simulation harness interface is frozen for Track B extension
- Week 3 begins super-checkpoint protocol draft (packet 154 §2.3 week-3 focus)
- Track B formally kicks off week 3 (per packet 163 — to be written)

Week 3's first task: draft super-checkpoint generation + signature protocol. Week 3 deliverable at end of week 3.

---

## 12. References

- packet 154 §2.3 + §2.6: Week 2 focus + gate criteria (charter)
- packet 154 §2.7: Track A/B coordination
- packet 160: Week 1 gate pattern (this packet inherits structure)
- packet 153 §3: Converged MVD — substrate design the properties encode
- packet 153 §4.1 + §4.6: Pruning decision logic + formal-methods verification (open questions this week begins to close)
- packet 149: Risk matrix + invariants
- packet 164 (pending): Simulation harness shared-spec (companion to D4 interface freeze)

---

*Charioteer week-2 gate packet. Engineering executes; minimalism auditor gates; sovereign K2's the week-2→3 transition at §7 acceptance tests.*

`Zero-Sum Resolution Equation`

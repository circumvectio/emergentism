---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "168 — Track A · Week 3 Gate Criteria"
---

# 168 — Track A · Week 3 Gate Criteria

**Evidence tier:** [I] charter expansion; [S] where citing packets 153, 154, 160, 162; [C] protocol-shape recommendations pending engineering iteration
**Date:** 2026-04-24
**Lane:** Charioteer spec — engineering/warrior executes; minimalism auditor gates; sovereign K2's the week-3→4 transition
**Status:** Draft — awaiting sovereign pass-through (no new OQs; detail expansion of packet 154 §2.3/§2.6 already-ratified charter)
**Complements:** packet 154 (Track A charter), packet 160 (W1 gate), packet 162 (W2 gate), packet 163 (Track B W1 — runs in parallel starting this week), packet 153 (§4.2 super-checkpoint protocol + §4.3 proof-of-reconstruction)

---

## 0. Axiomatic guard

Week 3 is where the sprint leaves solo-lane. Track A continues its work AND Track B starts. The coordination surface becomes real for the first time. Every deliverable this week must pass the minimalism-auditor layer-separation check — substrate changes cannot assume organ-layer behavior, and vice versa.

The protocol draft landing this week is *draft*, not *final*. The full super-checkpoint protocol spec lands week 8 (packet 153d). Week 3 produces the first readable protocol document + starts proving its properties.

`Zero-Sum Resolution Equation`

---

## 1. Week 3 purpose (from packet 154 §2.3)

**Focus:** Super-checkpoint protocol draft; validator coordination model
**Deliverable (charter-level):** Generation + signature + distribution spec; proof-of-reconstruction algorithm formal
**Gate (charter-level):** Super-checkpoint protocol draft; proof-of-reconstruction algorithm formal

Week 3 takes the W2 properties (safety + liveness) and drafts the *protocol* that instantiates them. Protocol is the how; properties are the what.

---

## 2. Entry criteria (from Week 2)

Before Week 3 begins, all packet 162 §7 gates must have landed:

- G1–G2: D1 + D2 safety/liveness properties stated and sketched
- G3: D3 first proof attempt landed (✅ proved or ❌ blocked-with-named-missing-piece)
- G4: D4 simulation harness runs deterministic happy-path
- G5: D5 glossary updated with shared-term section
- G6: D6 receipt packet 162a committed
- G7: No "block" terminology regression
- G8: No Invariant I–VII risk

Plus Track B entry per packet 163 §2 (their own W1 begins this same calendar week).

If any Track A W2 gate ❌, Track A W3 does not begin; Track B W1 also does not begin (cross-track lockstep).

---

## 3. Deliverables

Week 3 produces seven artifacts. Each lands as a file in the repo; sovereign K2 gates the W3→W4 transition at §7 acceptance tests.

### 3.1 D1 — Super-Checkpoint Generation Protocol

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W3_SUPER_CHECKPOINT_PROTOCOL.md`
**Content:**
- When is a super-checkpoint generated? (round-boundary, event-count threshold, or both — engineering decides, must justify)
- Who initiates generation? (leader election, round-robin, emergent — must be deterministic for given validator set)
- What does the super-checkpoint header contain? (minimum: `height`, `prev_hash`, `tx_root`, `state_root`, `sig_set`, `proof_bundle_commitment`)
- Distribution protocol (gossip, direct-to-archiver, both)

**Format:** Markdown protocol spec with pseudocode. Evidence tier [I/S] — interpretive where engineering-shape; structural where CANON-tied (Paper 12 §IV).

### 3.2 D2 — Signature Aggregation Spec

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W3_SIGNATURE_AGGREGATION.md`
**Content:**
- Signature scheme choice (BLS, Schnorr+MuSig, or independent signatures — protocol-level decision)
- Threshold model: simple majority vs. 2/3 Byzantine-tolerant (CANON-directed: 2/3 for Green finality per Paper 12 §IV.2)
- Aggregation protocol: who gathers, who broadcasts, how quorum is detected
- Failure modes: what happens when quorum is not reached within T rounds

**Format:** Markdown protocol spec. Evidence tier [S/I].

### 3.3 D3 — Validator Coordination Model (formal)

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/models/W3_validator_coord.{ext}`
**Content:**
- Framework-native model of validator coordination
- State variables: `ValidatorSet`, `CurrentRound`, `SigThresholdMet`, `FinalityState` (Orange/Green)
- Transitions encode D1 + D2 protocol semantics
- Must compile + type-check
- Must enable proof attempt on at least ONE liveness property from packet 162 D2 (typically `SUPER_CHECKPOINT_EVENTUALLY_CREATED`)

**Format:** Framework-native source file. Evidence tier [S] if compiles + proof-attempt lands; [C] if proof blocked.

### 3.4 D4 — Proof-of-Reconstruction Algorithm (formal)

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/models/W3_reconstruction_algo.{ext}`
**Content:**
- Formal statement of reconstruction algorithm — given a super-checkpoint header + Proof Bundle, reconstruct `tx_root` and `state_root`
- Spot-check logic (when a requester challenges an archiver, exact query protocol)
- Halt-on-failure logic (what a requester does when reconstruction fails)
- Proof sketch for `RECONSTRUCTION_EVENTUALLY_SUCCEEDS` liveness property (packet 162 D2.2)

**Format:** Framework-native + markdown. Evidence tier [S].

### 3.5 D5 — First Byzantine Scenario (simulation)

**Path:** `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/01_byzantine/W3_one_byzantine_validator.yaml`
**Content:**
- Scenario: 4 validators, 1 Byzantine (signs conflicting super-checkpoints at same height)
- Assertions:
  - `every_super_checkpoint_reaches_green` — may fail (acceptable — this is testing)
  - `honest_quorum_finalizes_correct_checkpoint`
  - `no_data_loss_before_window`
- Transcript determinism verified per packet 164 §4.3

**Format:** YAML scenario file. Evidence tier [S] when harness runs it.

**Discipline:** this is the *first* adversarial scenario. Packet 153 §4.7 enumerates the full adversarial coverage (week 6). Week 3 proves the harness can ingest one Byzantine scenario; week 6 exhausts the space.

### 3.6 D6 — Track A/B Coordination Touchpoint

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W3_COORD_TRACK_B.md`
**Content:**
- Log of any Track B questions/asks surfaced during Track B W1 that affect Track A
- Explicit "no changes to shared contract (packet 164 §7.1)" confirmation OR list of proposed changes for joint review
- Sync meeting notes (weekly sync per packet 154 §2.7)

**Format:** Markdown log. Evidence tier [I].

### 3.7 D7 — Week-3 Gate Receipt

**Path:** `01_EMERGENTISM/11_UPLINK/168a_TRACK_A_WEEK_3_RECEIPT_<DATE>.md`
**Content:**
- Checklist of §7 gate items with ✅ / ❌
- Protocol-draft summary (2-paragraph description of what D1 + D2 establish)
- Proof-attempt outcome for liveness property (D3)
- Byzantine scenario transcript hash (D5)
- Track B touchpoint outcome (D6)
- Minimalism auditor sign-off
- Kill-criteria status
- Hand-off to Week 4 (mid-sprint review per packet 154 §2.3)

**Format:** Uplink packet, evidence tier [S]/[I] per section.

---

## 4. Protocol discipline (informs D1 + D2 + D3 + D4)

**Rule: protocol drafts never reference implementation.** No D1–D4 content mentions concrete libraries (libp2p, Tokio, etc.), specific cryptographic primitives by implementation (`Blake3`, `SHA3-256`), language or byte-level layout. Protocol is at substrate-semantics layer.

**Rule: every protocol claim is proof-sketchable.** If a protocol property can't be sketched against the framework model in ≤ 200 words, the property is malformed. Block at merge.

**Rule: no substrate↔organ coupling.** Super-checkpoint protocol does NOT consult cluster-layer state. Cluster protocol (Track B) may consume substrate finality events, but not vice versa. Minimalism auditor enforces.

---

## 5. Minimalism-auditor checkpoints (Week 3)

### 5.1 D1/D2 check — protocol substrate scope

*Does the super-checkpoint protocol or signature aggregation reference any organ-layer or product-layer primitive?*

Examples to block: "cluster members vote on checkpoint" (organ leak); "user-initiated checkpoint" (product leak). Remove immediately if present.

### 5.2 D3 check — validator coordination model

*Does the validator coordination model import or reference cluster state?*

Validators are substrate actors. Their behavior is governed by consensus protocol, not by cluster-layer trust scores. Clusters observe validators; they do not coordinate validators.

### 5.3 D4 check — reconstruction algorithm

*Does the reconstruction algorithm assume archiver cooperation beyond what Paper 14 §IV.1 "Memory as Market" specifies?*

The algorithm must work against an adversarial archiver set (some cooperative, some withholding). If the algorithm silently assumes all archivers are honest, that's a gap — flag.

### 5.4 D5 check — Byzantine scenario

*Does the Byzantine validator in the scenario affect organ-layer state or product-layer state?*

Byzantine = substrate-layer adversary. Its action surface is limited to substrate transitions (signing, broadcasting). If the scenario allows it to manipulate cluster formation, the scenario is malformed.

### 5.5 D6 check — Track B coordination

*Are any Track B asks this week implicit layer violations?*

If Track B asks Track A to expose substrate-internal state for cluster consumption, that's a layer leak and Track A blocks the ask. Cluster layer consumes finality events (Orange/Green transitions); not raw validator state.

---

## 6. Cross-dependencies this week

| Dependency | With | Contract |
|---|---|---|
| Shared harness interface | Track B (packet 163 + 164) | Frozen per packet 164 §7.1; Track B extends only |
| Glossary shared asset | Track B | Any Track A glossary addition must not collide with Track B's expected organ-layer terms |
| Shared scenarios dir | Track B | `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/01_byzantine/` (Track A) + `05_cluster/` (Track B) — disjoint directories |
| Framework version | All tracks | No framework-toolchain upgrade this week (W1 D1 immutable) |
| Invariant I–VII | Standing | Minimalism auditor enforces |

Weekly sync at sprint-week boundary between tracks. Conflicts escalate to sovereign within 48h per packet 154 §2.7.

---

## 7. Gate acceptance tests

Week 3 passes iff **all nine** below pass. Any failure → kill criteria §8.

| # | Test | Pass condition |
|---|---|---|
| G1 | D1 landed | Protocol generation + distribution spec exists; addresses when/who/what/how |
| G2 | D2 landed | Signature aggregation spec exists; scheme chosen; threshold explicit (2/3 Byzantine) |
| G3 | D3 compiles + proof-attempted | Validator coord model compiles; ≥ 1 liveness property proof attempted; result ✅ or ❌-with-named-block |
| G4 | D4 formal | Reconstruction algorithm machine-checkable; `RECONSTRUCTION_EVENTUALLY_SUCCEEDS` proof sketch passes sketch review |
| G5 | D5 harness runs | Byzantine scenario produces deterministic transcript; assertions evaluated (pass/fail both acceptable at W3) |
| G6 | D6 coordination log | Track B asks logged; no unilateral changes to shared contract |
| G7 | D7 receipt landed | Checklist ✅ on G1–G6; auditor sign-off; kill-criteria status stated |
| G8 | No "block" regression | `track_a_termlint.py` exits 0 across all W3 artifacts |
| G9 | No Invariant I–VII risk | Auditor confirms |

**Sovereign gate moment:** after D7 lands, sovereign reviews week-3 receipt and K2's week-4 kickoff (which is the mid-sprint review per packet 154 §2.3).

---

## 8. Kill criteria (escalate to sovereign immediately)

- **K1** — Cannot converge on super-checkpoint generation trigger (round-based vs event-count vs hybrid) by end of day 4. Requires sovereign arbitration or scope-reduction decision.
- **K2** — Signature aggregation scheme choice blocks on security-assumption ambiguity. Sovereign arbitrates via K2-revisable default (BLS if uncertain).
- **K3** — D3/D4 model compiles but no proof attempt succeeds or names a missing lemma. Symptom of over-ambitious property or malformed spec.
- **K4** — D5 Byzantine scenario cannot run deterministically. Non-determinism is a bug at harness level; escalate per packet 164 §8.3.
- **K5** — Track B W1 asks reveal a hidden assumption in Track A that Track A engineers disagree on. Sovereign arbitrates layer-discipline question.
- **K6** — Mid-sprint review (week 4) cannot begin because week 3 deliverables materially short of spec. Not a W3 kill criterion per se but surfaces in the W4 gate.

---

## 9. Coordination with Track B (starts this week)

Week 3 is the first week of Track A/B parallel operation. Entry conditions:

- Track A completed packet 162 W2 gates G1–G8
- Track B completed packet 163 W1 gates G1–G7
- Shared contract (packet 164) is frozen
- Weekly sync scheduled (day 1 of the sprint week)

Track A W3 + Track B W1 run in parallel. Handoff events this week:

- Track A D5 Byzantine scenario lives in `01_byzantine/`; Track B cluster-formation scenarios live in `05_cluster/`. Disjoint.
- Track A D6 coordination log explicit about any Track B asks.
- If Track B W1 fails any gate (packet 163 §8 kill criteria), Track B pauses; Track A continues unless the failure leaks into the shared contract.

---

## 10. What Week 3 does NOT attempt

- No archiver economics — week 5 (packet 153c)
- No exhaustive adversarial simulation — week 6 (packet 153 §4.7)
- No EBM interaction — week 7
- No full spec — week 8 (packet 153d)
- No implementation code — post-sprint
- No K2 requests beyond the W3→W4 gate

---

## 11. Handoff to Week 4 (mid-sprint review)

After G1–G9 pass and sovereign K2's the W3 receipt:

- Protocol draft (D1 + D2) is the W4 starting point
- Validator coord model (D3) stable for W4 property refinement
- Reconstruction algorithm (D4) ready for W4 formalization push
- Byzantine scenarios (D5) baseline set; W4 adds partition + withholding
- Mid-sprint review surfaces: timeline, scope, team load, Track A/B coordination friction

Week 4 is explicitly a **review week** per packet 154 §2.3. If the protocol shape needs pivot, week 4 is the gate — not week 5+. Sovereign holds the pivot call.

---

## 12. References

- packet 154 §2.3: Week 3 focus (charter)
- packet 154 §2.6: Week-3 gate (charter)
- packet 154 §2.7: Track A/B coordination
- packet 160, 162: Predecessor gate packets (same pattern)
- packet 163: Track B W1 gate (runs in parallel this week)
- packet 164: Shared harness contract
- packet 153 §4.2 + §4.3: Super-checkpoint protocol + proof-of-reconstruction (open questions W3 begins to close)
- packet 149: Risk matrix + invariants
- Paper 12 §IV.1–IV.2: CANON source for commitment-without-burden + Orange/Green finality
- Paper 14 §IV.1: CANON source for archiver market

---

*Charioteer week-3 gate packet. Engineering executes; minimalism auditor gates (now across both tracks); sovereign K2's the W3→W4 transition at §7 acceptance tests.*

`Zero-Sum Resolution Equation`

---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "163 — Track B · Week 1 Gate Criteria"
---

# 163 — Track B · Week 1 Gate Criteria

**Evidence tier:** [I] charter expansion + Track A pattern adaptation; [S] where citing packets 151, 154, 164; [C] attestation-scheme choice pending engineering evaluation
**Date:** 2026-04-24
**Lane:** Charioteer spec — engineering/warrior executes; minimalism auditor gates; sovereign K2's the week-1 receipt
**Status:** Draft — awaiting sovereign pass-through (no new OQs; detail expansion of packet 154 §2.7 + packet 151 already-scaffolded work)
**Complements:** packet 151 (cluster organ scaffold), packet 154 (sprint charter §2.3 + §2.7), packet 160 (Track A W1 pattern), packet 164 (simulation harness shared-spec)
**Timing:** Track B week 1 begins at Track A sprint week 3 (sprint calendar week 3, not absolute week 1)

---

## 0. Axiomatic guard

Track B extends existing scaffolding. It does NOT restart from scratch. The formal-methods framework chosen by Track A (packet 160 D1) is inherited; the glossary (packet 160 D2) is inherited; the simulation harness (packet 162 D4 + packet 164 contract) is inherited.

If Track B feels the need to redesign any of these, halt and escalate. Redesign is out of Track B scope — the purpose of starting Track B week 3 is to land additive organ-layer work on top of an already-stable substrate.

`Zero-Sum Resolution Equation`

---

## 1. Week 1 purpose

**Focus:** Organ-layer primitive definition + attestation scheme shortlist + harness extension for cluster actors
**Deliverable (charter-level):** First-pass cluster model in chosen framework; attestation scheme shortlisted; simulation harness extended with organ actors
**Gate:** Cluster model compiles; no substrate-layer leak in cluster definitions; no product-layer leak either; no "blockchain" / "cluster-as-chain" framings

Track B's week 1 mirrors Track A's week 1 in structure. The key discipline is **layer-separation**: cluster logic never reads or writes substrate state; cluster logic never references product/user state.

---

## 2. Entry criteria (inherited from Track A W2)

Before Track B week 1 begins, these must hold (from Track A packet 162 §7 gates G1–G8):

- Track A W2 D4 simulation harness stood up and runs deterministic happy-path
- Track A W2 D5 glossary published with Track-B-shared term section
- Simulation harness interface frozen per packet 164 §7.1
- Sovereign has K2'd Track A week-2→3 transition

If any of the above are ❌ at Track A end-of-week-2, Track B does not start; Track A continues alone until unblock.

---

## 3. Deliverables

Week 1 (Track B) produces six artifacts. Each lands as a file; sovereign K2 gates Track B week-1→week-2 transition at §7 acceptance tests.

### 3.1 D1 — Cluster Primitive Definition

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_b/W1_CLUSTER_PRIMITIVE.md`
**Content:**
- Formal definition of `Cluster` and `ClusterMember` per packet 151 §2 MVD
- Three cluster scalars explicitly named: `surprise_score`, `resistance_trend`, `voltage`
- State transitions: `form`, `strengthen`, `degrade`, `break`, `re-form`
- Explicit non-goals: no weights shared, no embeddings, no full latents, no permanent cluster identity
- Evidence-tier annotations per claim

**Format:** Markdown spec with framework-native type declarations in fenced code blocks. Evidence tier [I/S].

### 3.2 D2 — Attestation Scheme Shortlist

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_b/W1_ATTESTATION_SHORTLIST.md`
**Content:**
- Comparison matrix: TPM 2.0 · Apple Secure Enclave · Android StrongBox · Linux IMA · software TEE (as baseline rejection)
- Criteria: cross-platform availability · revocation support · known attack surface · auditor-verifiability · cost of integration
- Shortlisted schemes (minimum 2, maximum 4)
- Pre-committed abandon criteria (what conditions force dropping a shortlisted scheme)
- Signed by CTO or delegated security lead

Note: this is NOT a final choice; that comes week 3–4. Week 1 just narrows the space.

**Format:** Markdown ADR-style. Evidence tier [I/S].

### 3.3 D3 — Track B Glossary Append

**Path:** append to `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W1_GLOSSARY.md` (shared glossary from Track A)
**Content:** Add organ-layer terms:
- `Cluster`, `ClusterMember`, `cluster scalar (surprise_score, resistance_trend, voltage)`, `attestation`, `divergence threshold`, `break-link`, `attack-mode`, `cluster lifecycle`
- Each term: definition ≤ 60 words · CANON citation (packet 151 as primary source) · aliases-banned list
- **Aliases-banned must include:** "cluster as chain", "super-cluster", "cluster-state-machine" (these connote substrate behavior Track B must NOT adopt)

**Format:** Markdown table append. No existing Track A term is redefined (per packet 160 §11 immutability rule).

### 3.4 D4 — Cluster Actor Harness Extension

**Path:** `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/harness/actors/organ/` (new subdirectory under the harness built in Track A W2)
**Content:**
- `Cluster` actor implementation per packet 164 §3.2
- `ClusterMember` actor implementation per packet 164 §3.2
- Three new transitions: `form_cluster(members)`, `report_scalars()`, `break_link(reason)`
- Minimum one scenario YAML under `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/scenarios/05_cluster/` — a "two-node happy-path cluster formation" test

**Format:** Framework-native (whatever Track A chose) + YAML scenario. Evidence tier [S] for runnable, [I] for scenario design.

**Discipline:** extensions are ADDITIVE only. No change to substrate actors or shared schema per packet 164 §7.2 (extensible without breaking) vs §7.3 (requires joint review to change).

### 3.5 D5 — Minimalism Auditor Charter for Track B

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_b/W1_MINIMALISM_CHARTER.md`
**Content:**
- Track-B-specific questions the minimalism auditor asks per merge (beyond the Track A substrate check):
  - *Does this cluster-layer change require any substrate-layer code to care?* If yes → layer violation; redirect.
  - *Does this cluster-layer change require any product-layer primitive?* If yes → the change belongs in product or DAC layer, not organ.
  - *Does this primitive propose sharing any state beyond the three cluster scalars?* If yes → kill (Invariant VI + packet 151 §2 MVD).
- Standing reviewer role: one engineer per Track B merge acts as minimalism auditor

**Format:** Markdown charter. Evidence tier [I].

### 3.6 D6 — Week-1 Gate Receipt (Track B)

**Path:** `01_EMERGENTISM/11_UPLINK/163a_TRACK_B_WEEK_1_RECEIPT_<DATE>.md`
**Content:**
- Checklist of §7 gate items with ✅ / ❌
- Attestation shortlist summary (which 2–4 schemes survived)
- Harness-extension smoke-test outcome (cluster-formation scenario transcript hash)
- Minimalism-auditor sign-off
- Kill-criteria status
- Hand-off to Track B week 2

**Format:** Uplink packet, evidence tier [S]/[I] per section.

---

## 4. Terminology lock (informs D3)

**Rule:** Track B inherits every Track A banned term (packet 160 §4) PLUS adds its own:

| Banned (Track B additions) | Use instead | Reason |
|---|---|---|
| super-cluster | (no synonym — concept is banned) | Substrate-laden framing; clusters don't compose into super-clusters in this protocol |
| cluster-state-machine | cluster lifecycle | "State machine" connotes substrate finite-state formalism; organ-layer lifecycle is simpler |
| cluster as chain | cluster | Chain connotes sequential append; clusters form/break, not append |
| mega-cluster | — | Size-class framings are Invariant-VI-violating; OQ-I1 says no hard cap |
| cluster hub | — | Centralization framing; protocol is peer-to-peer |

Inherited from Track A: `block`, `blockchain`, `mining`, `miner`, `tx`, `genesis` (without qualifier).

The extended lint script (`track_a_termlint.py` from packet 160 D3) should accept a Track B–specific banned-list file and enforce both sets at Track B merges.

---

## 5. Minimalism-auditor checkpoints (Track B Week 1)

### 5.1 D1 check — cluster primitive

*Does the cluster primitive definition mention any substrate state variable (validator set, checkpoint height, tx_root, state_root)?*

If yes → substrate leak; redirect. Cluster primitive is purely organ-layer; substrate consumes cluster signals (via E_trust), not the other way around.

### 5.2 D2 check — attestation

*Does the attestation shortlist prefer a scheme that would require substrate-layer changes?*

If yes → wrong layer. Attestation is purely organ-layer onboarding discipline; substrate has its own validator attestation (different lane).

### 5.3 D3 check — glossary

*Does any added Track B term conflict with an existing Track A term (same name, different meaning)?*

If yes → name collision; escalate to sovereign. Glossary unification is the point of sharing it.

### 5.4 D4 check — harness extension

*Does the organ actor extension modify any substrate actor, scenario schema, or transcript format?*

If yes → breaks packet 164 §7.1 frozen interface; requires joint review per §7.3. Single-track merges cannot change the shared contract.

### 5.5 D5 check — charter

*Does the Track B minimalism charter soften any Track A minimalism discipline, or does it strictly add to it?*

Charter ADDITIONS only. Softening existing discipline requires sovereign K2.

---

## 6. Cross-track coordination this week

| Dependency | With | Contract |
|---|---|---|
| Harness interface | Track A (via packet 164) | Frozen at Track A W2→W3; Track B strictly extends |
| Glossary | Track A | Track B appends terms, never redefines |
| Framework choice | Track A W1 D1 | Inherited; no re-evaluation |
| Minimalism auditor role | Standing (packet 154 §2.9 + 160 §5) | Track B adds the §5 layer-specific checks above |
| Invariant gate I–VII | Standing | Auditor confirms at every merge |

Weekly sync at sprint-week boundary between tracks. Any conflict escalates to sovereign within 48h (per packet 154 §2.7).

---

## 7. Gate acceptance tests

Track B Week 1 passes iff **all seven** pass. Any failure → kill criteria §8.

| # | Test | Pass condition |
|---|---|---|
| G1 | D1 landed | File exists; three cluster scalars named; state transitions listed; non-goals explicit |
| G2 | D2 landed | Shortlist 2–4 schemes; comparison matrix present; abandon criteria stated; signed |
| G3 | D3 glossary appended | New organ-layer terms added; no existing term redefined; lint-banned aliases recorded |
| G4 | D4 harness extension compiles + runs | Cluster-formation scenario produces deterministic transcript in harness |
| G5 | D5 charter landed | Track-B-specific minimalism questions explicit; standing reviewer role defined |
| G6 | D6 receipt landed | Checklist ✅ on G1–G5; auditor sign-off; kill-criteria status stated |
| G7 | No harness contract violation | Frozen interface (packet 164 §7.1) is unchanged; lint passes |

**Sovereign gate moment:** after D6 lands, sovereign reviews the Track B week-1 receipt and K2's Track B week-2 kickoff.

---

## 8. Kill criteria (escalate to sovereign immediately)

During Track B week 1, escalate instantly if any of:

- **K1** — No engineer familiar with attestation schemes available on-team. Track B cannot proceed without at least one person who can meaningfully compare TPM / Secure Enclave / StrongBox.
- **K2** — D2 shortlist cannot converge to ≤ 4 schemes. Symptom of no-viable-option or analysis-paralysis; sovereign arbitrates.
- **K3** — D4 harness extension requires breaking change to shared contract (packet 164 §7.1). Escalate for joint review; do NOT merge unilaterally.
- **K4** — Minimalism auditor flags a layer violation that Track B engineers disagree with. Sovereign arbitrates — layer discipline is constitutional, not engineering-management.
- **K5** — Three cluster scalars (packet 151 §2 MVD) deemed insufficient. This is an Invariant-VI attack — adding any fourth scalar or any non-scalar shared state requires sovereign K2 AND re-affirmation that MVD minimalism still holds.

---

## 9. What Track B Week 1 does NOT attempt

- No attestation scheme final choice — week 3–4
- No full formal-methods proof of cluster protocol — weeks 4–6
- No adversarial simulation scenarios beyond happy-path — weeks 4–6
- No economic modeling of cluster formation incentives — post-sprint
- No UX for cluster onboarding — product layer, not sprint
- No new sovereign K2 requests — this packet is detail expansion

---

## 10. Handoff to Track B Week 2

After G1–G7 pass and sovereign K2's the Track B W1 receipt:

- D1 primitive definition is immutable unless K5-style trigger
- D2 attestation shortlist narrowed; week 2 begins tiebreaker analysis
- D4 harness extension interface stable; week 2 adds state-sharing protocol scenarios
- Week 2's first task: draft divergence-detection formal metric + begin attack-mode cascade model

---

## 11. References

- packet 151: Cluster organ scaffold (primary source for MVD)
- packet 154 §2.7: Track A/B coordination
- packet 160: Track A Week 1 gate pattern (Track B inherits structure)
- packet 162: Track A Week 2 gate (Track B's direct predecessor in sprint timeline)
- packet 164: Simulation harness shared-spec (interface Track B extends)
- packet 149: Risk matrix — cluster protocol is rank-2 engineering risk
- packet 147: Layer discipline (organ ≠ substrate ≠ product)

---

*Charioteer Track B week-1 gate packet. Track B engineering executes; minimalism auditor gates (with layer-specific checks); sovereign K2's the week-1→week-2 transition at §7 acceptance tests.*

`Zero-Sum Resolution Equation`

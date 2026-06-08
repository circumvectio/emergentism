---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "153 — Prune & Proof (Substrate Layer) — Spec Scaffold"
---

# 153 — Prune & Proof (Substrate Layer) — Spec Scaffold

**Evidence tier:** [I] scaffold; [S] CANON citations per line; [C] parameter values pending simulation + formal methods
**Date:** 2026-04-24
**Lane:** Charioteer scaffold — full spec requires Track A engineering + formal-methods verification
**Status:** Scaffold / enumeration of what the full spec must cover
**Layer:** Substrate (Kernel-Invariant-bound; Lane B to modify shape, Lane A for parameters)
**Rank in risk matrix (packet 149):** **#1 — Critical × High likelihood.** One bug here = retroactive finality break or permanent history loss.
**Prerequisite packets:** 146, 147, 149, 150, 150a
**Symmetric to:** 151 (cluster organ scaffold) + 152 (EBM gradient scaffold). Completes the three-scaffold set for 60-day engineering sprint.

---

## 0. Axiomatic guard

This is a scaffold, not a spec. Pruning is the single most dangerous operation in the substrate. Writing a full spec without formal methods + adversarial simulation would encode premature commitments in the one place where a single bug cascades catastrophically. The scaffold names what the spec must answer; the answers come from Track A's 60-day engineering sprint.

**Discipline:** every decision in this scaffold is checked against "what breaks if we're wrong?" If the failure mode is catastrophic, the decision requires belt-and-suspenders safeguards, not best-effort heuristics.

`Zero-Sum Resolution Equation`

---

## 1. Scope

**Is:**
- Enumeration of the substrate pruning-and-checkpoint primitive
- Minimum-viable design converged in packets 146–150
- Open engineering questions that block full spec
- Assignment of full-spec ownership to Track A

**Is not:**
- A full protocol with parameter values locked
- A production-ready specification
- A commitment to specific cryptographic libraries or runtimes

---

## 2. What CANON already fixes

[S] Paper 12 §IV.1 "Commitment Without Burden":
> *"Validators do not store history. They commit to it. Each round, the consensus layer produces a signed checkpoint header containing two roots: one for the transactions that occurred (tx_root), one for the state that resulted (state_root)."*

[S] Paper 12 §IV.2 Orange/Green: finality states are two (OQ-D1-refined charioteer recommendation).

[S] Paper 14 §IV.1: "Memory as Market — Archivers are a competitive market. They sell Proof Bundles."

[S] Kernel Invariant II (Substrate Primacy): "L1 anchoring required for state finality."

**Fixed by CANON:** Merkle-tree commitment architecture, archiver market, Proof Bundle verification, validator signing.

**NOT fixed by CANON — left to this spec:** when pruning actually happens, what triggers super-checkpoints, what the safety buffer is, how reconstruction is verified.

---

## 3. Minimum viable design (converged)

From packet 149 row 1 + Grok's executive recommendation + charioteer additions:

- **Event-level pruning (not block-level).** Hashgraph uses "events," not "blocks." Terminology matters for spec clarity.
- **Pruning gate:** an event may be pruned only after it has been referenced by **N consecutive Green finality rounds** (N is a Lane A parameter; Grok proposed N=3; baseline is 3, subject to simulation-informed refinement).
- **Super-checkpoint cadence:** every 1,000 consensus rounds, the protocol generates a **cryptographic super-checkpoint** — a Merkle root of the entire current DAG state at that moment. Super-checkpoints are **never pruned**.
- **Fast bootstrap:** a new node joins the network with only the last super-checkpoint + the DAG since that checkpoint. No need to replay all history.
- **Proof-of-reconstruction at each super-checkpoint:** the protocol spot-checks random pre-prune events by requesting Proof Bundles from archivers and verifying Merkle paths. If verification fails, pruning halts network-wide pending investigation.
- **Terminology:** use "event" not "block"; use "super-checkpoint" for the 1,000-round Merkle anchor vs "checkpoint" for per-round validator commitments.

---

## 4. What the full spec must answer (open engineering questions)

Each question needs formal-methods verification or adversarial simulation data:

### 4.1 Pruning decision logic

- Exact algorithm: what structure tracks "referenced by N consecutive Green rounds"?
- Is pruning atomic across validators, or can validators prune independently?
- What happens if one validator prunes and another doesn't (divergence detection)?
- Can an event "un-prune" if a fork reorg re-introduces it? (Per Green finality, no — but formal verification needed.)

### 4.2 Super-checkpoint protocol

- Who generates the super-checkpoint? All validators? A rotating subset? Threshold signature?
- What's the minimum number of validator signatures required? (Must align with Byzantine-tolerance threshold.)
- How does the network reach consensus on the super-checkpoint content before signing?
- What happens if a super-checkpoint is contested (different validators sign different Merkle roots)?
- Super-checkpoint size: the entire DAG state is potentially large; is there a size budget?
- Compression strategy for super-checkpoint distribution?

### 4.3 Proof-of-reconstruction

- How many pre-prune events are spot-checked per super-checkpoint? Sample size, probabilistic vs deterministic coverage.
- What archivers are queried? Random selection, weighted by reputation, cross-validation?
- What's the verification deadline? If an archiver doesn't respond, does that count as failure?
- What's the response protocol if reconstruction fails? Halt pruning globally? Halt locally? Triage mode?
- How does the network resume after a halt?

### 4.4 Archiver economics

- Per packet 149 + Paper 14 §IV.1: archivers are paid. How?
- Fee type — is "archival" a fifth fee category alongside ROUTING / TRUTH / BROADCAST / STREAMING / APPLICATION?
- Settlement: Orange at request time, Green at proof-verification?
- Spam defense: how is an archiver protected from endless low-fee queries that occupy storage bandwidth?
- Incentive to store old state: why would an archiver keep 5-year-old event bodies?

### 4.5 Finality interaction

- OQ-D: two-state Orange/Green confirmed. How do we verify an event passed Green in N rounds? What's the formal predicate?
- What if Green is reached, then a super-checkpoint containing that event is contested — does the event stay Green or degrade?
- Light-node verification: how does a mobile client verify Green finality without trusting full validators?

### 4.6 Formal-methods verification

This is load-bearing. The pruning logic must be formally verified — not just property-tested.

- Which formal-methods framework? (Coq, Isabelle, TLA+, K framework.)
- What properties must be proved?
  - Liveness: pruning doesn't halt the network under normal operation
  - Safety: an event once pruned cannot be recovered to contradict the super-checkpoint
  - Determinism: same inputs → same pruning decisions across validators
  - No-data-loss: Proof Bundles for any pruned event remain verifiable against their super-checkpoint
- Budget for verification effort: multi-month engineering work.

### 4.7 Adversarial simulation

- What attack scenarios must the sim cover?
  - Byzantine validator signs contradictory super-checkpoints
  - Archiver withholds specific event bodies then demands ransom
  - Attacker generates N malicious events then triggers rapid pruning before N consecutive Greens
  - Network partition during super-checkpoint generation
  - Light-node attempts to spoof a Green proof from a pruned-and-archived event
- Simulation harness requirements: adversarial node distributions, network partition models, delay injection.

### 4.8 Interaction with mesh transport (per 150b)

- Can a mesh-only node verify a super-checkpoint without internet access?
- What's the minimum mesh-bandwidth to verify Proof Bundles?
- If a mesh-partition lasts longer than one super-checkpoint cycle, how does the node reconcile on reconnect?
- Does an event reach Green inside a mesh partition, or does Green require internet-scale consensus?

### 4.9 Interaction with EBM routing (per 152 scaffold)

- Super-checkpoint generation is compute-intensive. Does the SmallEBM node participate, or is super-checkpoint generation a separate validator role?
- How does super-checkpoint activity impact routing-fee revenue for validators?

### 4.10 Upgrade path

- How does the protocol upgrade pruning parameters (N consecutive Greens, super-checkpoint cadence) under Lane A governance without breaking already-pruned history?
- What's the rollback path if a pruning parameter change proves unsafe in production?

---

## 5. Ownership and timing

**Owner:** Track A of the 60-day engineering sprint per packet 149 §5 — CTO + consensus engineering + formal-methods specialists.

**Prerequisites for full spec:**
1. Formal-methods framework selected (Lane A decision — engineering preference)
2. OQ-D ratification (two-state Orange/Green confirmed per charioteer-recommended D1)
3. Adversarial simulation harness operational (byproduct of Track B's cluster work — shared asset)
4. Archiver economic model drafted (feeds §4.4)
5. Field-test data from testnet operating at genesis-scale (Egg phase per Paper 12 §VI)

**Estimated timeline:** sprint weeks 1–8 (per packet 149 §5), longest track due to formal-methods burden.

**Deliverables (before spec finalization):**
- `01_EMERGENTISM/11_UPLINK/153a_PRUNE_FORMAL_SPEC.md` — TLA+ or Coq formal specification + proved properties
- `01_EMERGENTISM/11_UPLINK/153b_PRUNE_SIMULATION_RESULTS.md` — adversarial simulation coverage
- `01_EMERGENTISM/11_UPLINK/153c_ARCHIVER_ECONOMICS.md` — fee model, spam defense, storage incentives
- `01_EMERGENTISM/11_UPLINK/153d_PRUNE_FULL_SPEC.md` — closes all §4 questions

---

## 6. What is assumed vs open

**Assumed by this scaffold (pending sovereign K2 on OQ-D):**
- Two-state Orange/Green finality (no Red state promoted to substrate)
- Event-level, not block-level, pruning (hashgraph-native terminology)
- Super-checkpoint at every 1,000 rounds as a starting cadence
- N=3 consecutive Green rounds as starting safety buffer
- Proof-of-reconstruction spot-check at each super-checkpoint as mandatory safety net

**Open (requires engineering):**
- All of §4
- Specific parameter values (N, super-checkpoint cadence, sample sizes)
- Formal-methods framework selection
- Archiver economic parameters

---

## 7. Why this is a scaffold rather than a full spec

Writing a full pruning protocol spec in charioteer lane without formal-methods verification would:
- Encode parameter values before adversarial simulation validates them
- Commit to a generation protocol before Byzantine-tolerance analysis completes
- Define proof-of-reconstruction thresholds that may miss attack vectors
- Risk a catastrophic rank-1 risk manifesting in production

Per Foundation Minimalism: specify only what the substrate must know; let Track A's engineering sprint + formal-methods lane close the open questions.

**Additional discipline for pruning specifically:** the failure mode is asymmetric. A conservative spec that over-protects is annoying; a loose spec that misses an attack vector is catastrophic + unrecoverable. Bias the scaffold toward conservatism.

---

## 8. Cross-dependencies with other scaffolds

| Scaffold | What pruning depends on | What depends on pruning |
|---|---|---|
| 151 (cluster organ) | Cluster detection of Byzantine validator behavior may feed into super-checkpoint contestation | Cluster trust computations may use Green finality age as an input |
| 152 (EBM gradient) | EBM training may use pruned history if available via archivers | Archiver reputation in EBM trust model |
| 150b (mesh) | Mesh partitions interact with super-checkpoint reachability | Mesh-only finality verification needs Proof Bundles |

Coordination across scaffolds requires a shared glossary of terms (event, super-checkpoint, Proof Bundle, Green, Orange, Normal Mode, Fallback Mode). Track A should publish this as an early deliverable.

---

## 9. References

**CANON:**
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md` §IV — Prune & Proof architecture
- `.../V3_CANONICAL/14_WHY_SKYZAI_MONEY_FOR_THE_ENERGY_AGE.md` §IV.1 — Memory as Market
- `.../V3_CANONICAL/11_SKYZAI_CANON.md` Doc 03 — Invariant II Substrate Primacy

**Session packets:**
- 146 audit · 147 layer discipline · 148 formula repair · 149 risk matrix (§1.1 OQ-D, §2 row 1) · 150 integrated blueprint · 150a Constitutional Economics · 150b mesh integration · 151 cluster scaffold · 152 EBM gradient scaffold

**Historical packets:**
- 112 HIERO_FOR_L1_BODY_NOT_SPECTRE_BRAIN (hashgraph terminology)

---

*Scaffold. Full spec earned through formal methods + adversarial simulation, not prescribed in advance. Rank-1 risk; conservatism beats cleverness here.*

`Zero-Sum Resolution Equation`

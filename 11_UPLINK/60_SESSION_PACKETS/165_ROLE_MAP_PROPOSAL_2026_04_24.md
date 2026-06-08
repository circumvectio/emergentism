---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "165 — Role-Map Proposal (Track A + Track B Sprint)"
---

# 165 — Role-Map Proposal (Track A + Track B Sprint)

**Evidence tier:** [I] charioteer proposal; [S] where citing packets 149, 154; [C] throughout — NO names assigned, NO authority delegated
**Date:** 2026-04-24
**Lane:** Charioteer draft → **SOVEREIGN K2 REQUIRED** before any warrior picks up named assignments
**Status:** Draft proposal — role definitions only; name-filling is sovereign-exclusive
**Complements:** packet 149 §4 (role proposals), packet 154 §2.5 (Grok-suggested owners), packet 160 §7/§8 (escalation paths)

---

## 0. Axiomatic guard

This packet defines **roles**, not people. A role is a scope of authority + a set of gates + a rotation discipline. A person holds a role by sovereign K2 signature, not by charioteer proposal. No paragraph in this packet assigns authority to any named individual, and no section should be read as implying one.

If any reader (warrior, engineer, charioteer) picks up work on the assumption that a role is "already filled," they are in violation of the Sovereign Non-Delegation Law (packet 99 §4.2). Halt. Wait for sovereign K2.

The role-map exists so that when the sovereign does sign, everyone understands what was signed.

`Zero-Sum Resolution Equation`

---

## 1. Why a role-map packet

Without this packet, the sprint charter (packet 154 §2.5) leaves six roles named but unfilled. Engineers picking up Track A week 1 work have been implicitly treating the roles as "whoever is doing the task at the moment." That works for small sprints, but this sprint has:

- Non-delegable gates (minimalism auditor, formal-methods specialist)
- Constitutional-level kill criteria (packets 160, 162, 163)
- Cross-track coordination (packets 154, 164)
- A sovereign-K2 gate at every weekly transition

Those conditions require named authority. This packet enumerates what "named authority" means for each role, so sovereign K2 lands on a known surface.

---

## 2. Role catalog

Six roles. Each has: scope · authority · gates-owned · escalation-to · skills-required · time-commitment · Grace Exit (K4).

### 2.1 CTO / Track Accountability

**Scope:** Overall Track A + Track B accountability. The person through whom all sprint-level decisions flow.

**Authority:**
- Mid-sprint review decisions (scope, timeline)
- Resource allocation across tracks
- Escalation to sovereign when kill criteria trigger
- Final sign-off on week-N receipt packets (160a, 162a, 163a, etc.)

**Gates owned:**
- Framework decision record (packet 160 D1) — co-signer
- Weekly receipts (packet 160 D5, 162 D6, 163 D6) — signer
- Cross-track escalations within 48h SLA (packet 154 §2.7)

**Escalation to:** Sovereign (for kill criteria K1–K5 at any week)

**Skills required:** Distributed systems depth; previous experience leading sprint-scale formal-methods work OR previous experience leading substrate redesigns

**Time commitment:** 20–40% of engineering time over 60 days

**Grace Exit (K4):** If CTO needs to step out, sovereign appoints successor within 72h. Prior CTO's receipt-signing authority does not transfer automatically — sovereign K2 required for the new name.

**K2 slot:** _[name]_ — sovereign fills

---

### 2.2 Consensus Engineering Lead (Track A)

**Scope:** Track A substrate protocol — pruning decision logic, super-checkpoint protocol, event-level semantics.

**Authority:**
- Technical direction on Track A architecture
- Merge approval on Track A-only PRs (substrate actors, substrate scenarios)
- Packet 153 §4 open-question closure (weeks 2–8)

**Gates owned:**
- Weekly D1–D4 landings (packets 160, 162)
- Proof-obligation declarations (packet 162 §3.1, §3.2)
- Super-checkpoint protocol draft (week 3 deliverable)

**Escalation to:** CTO (for scope or timeline issues); Sovereign (for invariant-risk items)

**Skills required:** Consensus protocols (Paxos, Raft, or BFT family); prior experience with formal-methods specification

**Time commitment:** 60–80% of engineering time over 60 days

**Grace Exit (K4):** Sprint continues; interim lead elevated by CTO; sovereign K2 on named successor within 1 week.

**K2 slot:** _[name]_ — sovereign fills

---

### 2.3 Formal-Methods Specialist

**Scope:** TLA+/Coq/K/Isabelle/Lean4 model authorship and proof discipline across both tracks.

**Authority:**
- Framework choice (packet 160 D1) — primary decider
- Proof-attempt architecture (packet 162 D3, weeks 3–8 proofs)
- Block on any proof-obligation that cannot be sketched (charter §0 discipline)

**Gates owned:**
- D1 Framework Decision Record (co-signer with CTO)
- D3 First Proof Attempt (week 2)
- All subsequent proof landings

**Escalation to:** CTO (for tooling/infrastructure); Sovereign (for framework pivot decisions per K3 kill criteria)

**Skills required:** Machine-checked proof of at least one published distributed-systems protocol, OR equivalent demonstrated proficiency in the chosen framework

**Time commitment:** 70–100% of engineering time over 60 days (role is extraordinarily load-bearing)

**Grace Exit (K4):** If specialist leaves mid-sprint, the sprint itself may need to pause; escalate to sovereign for framework-pivot or scope-reduction decision. Do not attempt to continue proofs without a specialist signed in by sovereign.

**K2 slot:** _[name]_ — sovereign fills

---

### 2.4 Simulation Engineer (shared across tracks)

**Scope:** Simulation harness (packet 162 D4 + packet 164 shared-spec + packet 163 D4 organ extension), scenario authoring, determinism maintenance.

**Authority:**
- Harness implementation choices (Python vs Rust vs ...)
- Scenario YAML authorship and merge approval
- Determinism-violation triage

**Gates owned:**
- Harness stand-up (packet 162 §3.4)
- Shared-contract interface freeze at Track A W2→W3 (packet 164 §7.1)
- Cross-track scenario coverage over weeks 3–7

**Escalation to:** CTO (for infrastructure/resource blocks); Consensus Lead (for protocol-semantic questions); Cluster Lead (for organ-layer questions)

**Skills required:** Simulation-framework experience (ideally deterministic runners for distributed protocols); Python + one systems language

**Time commitment:** 50–70% of engineering time over 60 days

**Grace Exit (K4):** Harness continues; CTO appoints interim; sovereign K2 on successor within 2 weeks.

**K2 slot:** _[name]_ — sovereign fills

---

### 2.5 Economic Modeler

**Scope:** Archiver economics (packet 153 §4.4 + §4.5); fee-type assignment; spam defense modeling; settlement flows.

**Authority:**
- Economic model drafting (week 5 deliverable — packet 153c)
- Parameter proposals for simulation sweeps (week 6)
- Escalation of economic-Invariant-risk items (Invariant I ZAI Cap, Invariant II Substrate Primacy)

**Gates owned:**
- Packet 153c archiver economics (week 5)
- Cross-check with 150a Constitutional Economics sheet

**Escalation to:** CTO (for scope/timing); Sovereign (for Invariant-risk or token-economic changes — token economics are constitutionally protected)

**Skills required:** Tokenomics experience OR formal mechanism-design background OR prior work on blockchain archiver/storage economics

**Time commitment:** 30–50% of engineering time over weeks 4–6 primarily

**Grace Exit (K4):** Sprint continues with deferred economics packet; sovereign decides whether to delay 153c or reshuffle scope.

**K2 slot:** _[name]_ — sovereign fills

---

### 2.6 Minimalism Auditor (standing, rotating)

**Scope:** Every substrate and organ merge across both tracks. Asks the packet 154 §2.9 question: *"Could this change live at organ or product layer without the substrate caring?"*

**Authority:**
- Block any merge on layer-violation grounds
- Flag Invariant-risk items to sovereign
- Veto on unapproved scope leak

**Gates owned:**
- Every merge (standing gate)
- Weekly receipt sign-off (packets 160a, 162a, 163a, and onward)
- Standing Invariant I–VII check

**Escalation to:** Sovereign directly (layer discipline is constitutional, not engineering-management)

**Skills required:** Distributed-systems layering experience; Foundation Minimalism principle internalized; emotional fortitude to block merges from senior engineers

**Time commitment:** Rotating role — 1 engineer per merge week; approximately 10% engineering time if rotation is weekly across 4-person pool

**Grace Exit (K4):** Role rotates weekly anyway; individual auditors can step out between weeks without disruption.

**K2 slot (rotation pool):** _[name1, name2, name3, name4]_ — sovereign fills

---

## 3. Role-interaction rules

### 3.1 Veto-chain

| Role | Can veto |
|---|---|
| Minimalism auditor | Any merge across both tracks |
| Formal-methods specialist | Any proof-obligation that violates charter §0 discipline |
| CTO | Any weekly receipt until satisfied |
| Sovereign | Any of the above (and any decision by any role, by definition) |

### 3.2 Authority-gradient

From packet 99 §4.2 (Sovereign Non-Delegation Law), the following powers remain sovereign-exclusive regardless of role assignment:

- K2 signature (no role signs on sovereign's behalf)
- Refusal of engineering proposals (sovereign only)
- Receipt inspection (sovereign only; CTO sign-off is receipt *completion*, not inspection)
- Three-Stage Process separation decisions (sovereign only)
- Legal asymmetry decisions (sovereign only)

No role in §2 has any of these five powers. The role-map authorizes operational execution, not constitutional authority.

### 3.3 Rotation and Grace Exit (K4)

Every role in §2 carries a K4 Grace Exit — the person can leave the role without leaving the organism, and the organism keeps nothing from the handoff. Practical implication:

- No role documents are "owned" by the role-holder
- Handoff documentation is maintained weekly by the role-holder as receipt-packet appendices
- The next role-holder inherits the documentation pointer, not the person's head-knowledge

---

## 4. Sovereign K2 slot

**This packet becomes operational only when sovereign fills the six K2 slots below and signs:**

| Role | K2 name slot |
|---|---|
| CTO | ________________ |
| Consensus Engineering Lead | ________________ |
| Formal-Methods Specialist | ________________ |
| Simulation Engineer | ________________ |
| Economic Modeler | ________________ |
| Minimalism Auditor Pool | ____________, ____________, ____________, ____________ |

**Sovereign signature:** ______________________ · **Date:** __________

Without sovereign K2, the role-map is proposal only. No warrior or engineer should treat §2 as implying any assignment.

---

## 5. What this packet does NOT do

- Does NOT fill any role (sovereign-exclusive)
- Does NOT grant any authority (sovereign K2 required)
- Does NOT override existing lane discipline (packet 99 §4.2 stands)
- Does NOT create new roles beyond the six in packet 154 §2.5 (charioteer cannot expand role inventory without sovereign K2)
- Does NOT prescribe hiring — existing team members filling these roles is the primary expectation

---

## 6. What charioteer recommends (advisory only)

Without assigning names, charioteer offers these observations on the role-map shape:

1. **Consensus Engineering Lead and Formal-Methods Specialist are distinct roles.** Even if one person can fill both, treating them as distinct makes the Grace Exit cleaner if one needs to leave.

2. **Minimalism Auditor as rotating role is deliberately load-spread.** Vesting it in one person risks that person becoming a bottleneck OR a rubber-stamp. Rotation (with sovereign K2 on the pool) is healthier.

3. **Economic Modeler is part-time by design.** The role is hot weeks 4–6; pulling someone full-time for 60 days wastes their capacity.

4. **CTO's role here is sprint-scoped, not organ-organ spanning.** If the organism's global CTO also fills this role, flag time-allocation tension up to sovereign.

5. **If fewer than six people are available**, recommend sovereign collapses:
   - Economic Modeler into CTO
   - Simulation Engineer into either Consensus Lead or Formal-Methods Specialist (with time-allocation note)
   - Minimalism Auditor pool reduced to 2 rotating members

   Do NOT collapse Formal-Methods Specialist and Consensus Engineering Lead — that pairing carries too much risk-concentration.

---

## 7. References

- packet 99 §4.2: Sovereign Non-Delegation Law (constitutional frame)
- packet 149 §4: Risk-to-role mapping (origin of this role inventory)
- packet 154 §2.5: Sprint charter role proposals (direct predecessor)
- packet 154 §2.9: Minimalism Auditor standing definition
- packet 160, 162, 163: Weekly gate packets (the gates these roles own)
- packet 164: Shared-spec (simulation-engineer-owned interface)

---

*Charioteer role-map proposal. Sovereign K2 fills the slots. Without K2, no role is filled, and no warrior or engineer should act otherwise.*

`Zero-Sum Resolution Equation`

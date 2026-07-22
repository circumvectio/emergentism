---
rosetta:
  primary_level: L5
  primary_column: Engagement Architecture
  secondary:
    - level: L3
      column: Audit Method
      role: "rank expert inputs against constitutional fit and receipts"
    - level: L4
      column: Governance
      role: "preserve WHISPER/FLOW/K2 engagement binding path"
    - level: L6
      column: Core State
      role: "bound availability and expert claims to engagement-specific contracts"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I/C]"
  canonical_phrase: "Consulting Expert Engagement Protocol"
title: "Consulting Expert Engagement Protocol"
status: "ACTIVE — C-Suite expert-engagement protocol"
evidence_tier: "[I] for engagement workflow; [S] for WHISPER + API PAY rail; [C] for specific expert availability claims."
---

# Consulting Expert Engagement Protocol

**Date:** 2026-04-29
**Status:** ACTIVE — Phase 0 implementation per packet 224
**Lane:** C-Suite buildout — second artifact (b) per the four-step sequence
**Evidence tier:** [I] for the engagement workflow | [S] for WHISPER + API PAY rail | [C] for specific expert availability claims (each engagement is its own contract)
**Depends on:** packet 224 (C-Suite + experts), packet 215 (WHISPER), packet 216 (API PAY rail), packet 214 (Five-Ws)

> **Phase 0:** experts as bibliographic packages + on-demand LLM consultation. Phase 1 (after S1): real human contracts via WHISPER. Phase 2 (after S4): niche-graph integrated. This doc specs the workflow that survives across all three phases.

---

## 1. The Six-Step Engagement Workflow

```
1. C-SUITE GAP DETECTION
       │
       ▼ (a C-role names "this exceeds my standing competence")
2. AGENTZ PROACTIVITY SURFACES THE PROPOSAL
       │
       ▼ (Five-Ws filled per packet 214 + Q11 smallest-gap)
3. WHISPER TRANSMITS THE ENGAGEMENT
       │
       ▼ (intent → AI drafts → K2 accepts → NIP-17 wrap → expert)
4. EXPERT RESPONDS
       │
       ▼ (WHISPER reply / RELAY broadcast / FLOW signed deliverable)
5. C-SUITE INTEGRATES
       │
       ▼ (CAO ranks input against constitution; CEO decides)
6. K2 BINDS + FLOW RECEIPT PERSISTS
```

Every step emits a receipt; the engagement is fully auditable.

### Step 1: C-Suite Gap Detection

A standing C-role (typically CAO at L3, since ranking depends on domain expertise) detects that a proposed answer is *underconfident* — the constitutional-tags audit returns *uncertain* on at least one dimension, and the local LeWorldModel cannot resolve. The C-role emits a `gap_finding`:

```yaml
gap_finding:
  detected_by: CAO  # the C-role that surfaced it
  question: <the specific question that needs expert input>
  domain: <one of the 12 expert domains>
  urgency: immediate | soon | scheduled
  constitutional_dimension: <which invariant is at risk>
  blocking: <the Objective(s) that wait on this answer>
```

### Step 2: Agentz Proactivity Surfaces the Proposal

The Agentz question-loop (packet 214) takes the gap_finding and constructs an engagement Objective with full Five-Ws:

```yaml
engagement_objective:
  what: "Engage E2 (DeFi expert) for novel-yield-strategy ranking"
  when: "2026.05.03 - 14:00 UTC"  # proposed time window
  where: "remote / async via WHISPER"
  who: "E2 expert (Vaibhav Singh, npub_E2_xxxx)"
  why: "Mission — YieldFront Opportunity Ranking (S1 substrate spine)"
  five_ws_complete: true
  smallest_gap_score: <branching_factor / answer_effort>
```

If any Five-Ws field is empty, Agentz asks the user (or the CAO) to fill before proceeding.

### Step 3: WHISPER Transmits the Engagement

Per packet 215 + Q7 symmetric persistence:

```
Yves's intent:    "@E2 rank these 5 yield strategies; constitutional-fit only"
Yves's AI drafts:  structured engagement proposal with Five-Ws
Yves K2-accepts:   single tap on the AI's translation
Transmit:          NIP-17 gift-wrap → E2's npub
E2's AI receives:  decrypts, presents actionable card
E2 K2-accepts:     single tap to accept the engagement
Both workflows update: Yves's "engagement-proposed" → "confirmed";
                       E2's workflow gets a "delegated-to-me" Objective
```

### Step 4: Expert Responds

The expert returns their deliverable through the appropriate substrate:

| Deliverable type | Substrate |
|---|---|
| Yes/no answer | WHISPER reply (ephemeral; receipt of the answer persists on FLOW) |
| Ranked list | WHISPER reply with structured payload |
| Public position / paper | RELAY broadcast (durable, signed) |
| Code / spec / artifact | FLOW signed deliverable + storage reference |
| Multi-session consultation | Repeated WHISPERs + a final FLOW deliverable |

### Step 5: C-Suite Integrates

The CAO receives the expert's deliverable, ranks it against the existing constitutional audit, and produces an updated decision-ready list. The CEO then takes the ranked list to K2.

```yaml
csuite_integration:
  expert_input: <the deliverable>
  cao_ranking: <updated composite score with expert dimension added>
  ceo_decision: commit | refuse | further-consultation
  k2_acceptance_card: <the single-tap proposal>
```

### Step 6: K2 Binds + FLOW Receipt Persists

K2 single-tap. FLOW receipt records:
- The original gap_finding (Step 1)
- The engagement Objective with Five-Ws (Step 2)
- The WHISPER engagement event (Step 3)
- The expert's deliverable (Step 4) — content-addressed
- The C-Suite integration + decision (Step 5)
- The K2 signature event (Step 6)

The whole engagement is one auditable trail.

---

## 2. Per-Expert Engagement Templates

Each of the twelve experts has a templated engagement spec. Use these as the starting point for the WHISPER intent.

### E1 — Quantum Foundations

```
DOMAIN: Quantum mechanics, Bell tests, Bloch sphere, JEPA / EBM
INVOKE WHEN:
  - Framework claims touch quantum physics (per packet 212)
  - A new physics paper challenges or supports the D4/D5 reading
  - Bloch sphere mapping needs verification

DEFAULT INTENT TEMPLATE:
"@E1 [topic]: I'm proposing the framework reads [X] as evidence for [Y].
Verify or falsify against established quantum-foundations literature.
Specifically check: (1) [reference paper], (2) Bell-inequality
implications, (3) whether the framework's interpretation oversteps
[S] tier.

Cite your sources. If my reading is [I] tier, confirm. If it's [C]
tier or worse, explain why."

ACCEPTABLE OUTPUTS: Verification with citations / falsification with
counterexample / suggested re-tiering.

K2 GATE: Bind only if expert confirms [S]+[I] interpretation; downgrade
to [C] if expert flags overreach.

PHASE 0 IMPLEMENTATION: Bibliographic package = QUANTUM_PHYSICS_CONFIRMATIONS.md
+ PD_25 + arXiv search corpus. LLM consultation with cite-checking.
```

### E2 — DeFi / Yield Strategy

```
DOMAIN: DeFi protocols, yield strategies, AMM mechanics, lending markets,
LST / LRT, basis trades, real-world-asset yield, structured products

INVOKE WHEN:
  - YieldFront's Opportunity Ranking encounters a novel protocol
  - A yield candidate's risk/return profile needs domain validation
  - A protocol's smart-contract trust assumptions are unclear

DEFAULT INTENT TEMPLATE:
"@E2 [protocol]: I'm considering [specific strategy] on [protocol].
Rank against my universe of [N] alternatives. Specifically assess:
(1) smart-contract risk, (2) liquidity profile, (3) admin-key
inventory (η-check), (4) historical APY distribution, (5) failure
modes observed in similar protocols.

Tag with constitutional fit per packet 219: η-near-zero, K2-eligible,
K4-Grace-Exit-applicable."

PHASE 0 IMPLEMENTATION: Bibliographic package = DeFiLlama corpus +
audit reports + protocol docs. LLM consultation with cross-check.
```

### E3 — Smart-Contract Security

```
DOMAIN: Smart-contract audits, on-chain vulnerabilities, formal
verification, MEV, prompt-injection-equivalent in DeFi

INVOKE WHEN:
  - Any new on-chain integration before deployment
  - Post-incident root-cause analysis
  - Vault.sol or any L2 credit primitive change

DEFAULT INTENT TEMPLATE:
"@E3 [contract address or code]: Pre-deployment review. Specifically:
(1) reentrancy exposure, (2) admin-key surface, (3) oracle dependency,
(4) upgrade path (or its absence), (5) match against known exploit
patterns. Output a go/no-go with explicit risk score.

Refuse to advise if you cannot verify the source matches the deployed
bytecode."

PHASE 0 IMPLEMENTATION: Bibliographic = OpenZeppelin + Trail of Bits +
Code4rena corpus. Phase 1: real auditor contract.
```

### E4 — LLM / JEPA / World Models

```
DOMAIN: Large language models, JEPA, energy-based models, world models,
fine-tuning, model evaluation, LeCun lineage

INVOKE WHEN:
  - LeWorldModel architecture choices (per Q4 base-model selection)
  - Substrate evolution from Phase 0 → Phase 1 → Phase 2
  - Performance regression in any LeWorldModel deployment

DEFAULT INTENT TEMPLATE:
"@E4 [decision]: Assessing [option A] vs [option B] for our
LeWorldModel substrate. Constraints: (1) sovereign deployment,
(2) API-PAY-payable compute, (3) JEPA-aligned architecture,
(4) [parameter budget].

Recommend with rationale. Flag any architectural choice that conflicts
with packet 216 sovereignty discipline."

PHASE 0 IMPLEMENTATION: Bibliographic = arXiv + LeCun paper corpus +
JEPA implementations. Phase 1: contracted ML architect.
```

### E5 — Regulatory / Compliance

```
DOMAIN: Jurisdictional regulation (Switzerland, UK FCA, US SEC, EU MiCA),
DAC legal status, K2 boundary per packet 207, securities law,
tax implications

INVOKE WHEN:
  - New jurisdiction operations
  - Charter amendment touching legal structure
  - SCC operator admission across borders (per Q10)
  - QNTM (the institutional MPC/ZK-Identity rail) / banking line questions

DEFAULT INTENT TEMPLATE:
"@E5 [jurisdiction + question]: Considering [action] in [jurisdiction].
Specifically: (1) regulatory classification of the act, (2) K2 boundary
implications per packet 207, (3) tax / reporting implications,
(4) precedent / comparable cases.

Output a green/yellow/red light with required mitigations."

PHASE 0 IMPLEMENTATION: Bibliographic = FCA + SEC + MiCA + Swiss
FINMA + tax-treaty corpus. Phase 1: contracted attorney per jurisdiction.
```

### E6 — UX / UI Design

```
DOMAIN: Information architecture, workflowy UX, question-queue patterns,
mobile-first design, accessibility, K2 acceptance UX

INVOKE WHEN:
  - nexus-web shell design decisions
  - Question-queue panel layout (S3)
  - WHISPER recipient card design (S2)
  - K2 acceptance UX latency concerns

DEFAULT INTENT TEMPLATE:
"@E6 [feature]: Designing [specific UI surface]. Constraints:
(1) one-tap K2 discipline, (2) Agentz asks one question at a time,
(3) ephemeral WHISPER auto-fades, (4) Five-Ws schema.

Surface design proposals with tradeoff analysis."

PHASE 0 IMPLEMENTATION: Bibliographic = Nielsen Norman + Apple HIG +
Material Design + research papers. Phase 1: contracted UX designer.
```

### E7 — Security / Adversarial Robustness

```
DOMAIN: Spam mitigation, prompt injection, adversarial ML, canary tests,
threat modeling, social engineering

INVOKE WHEN:
  - PAM-forbidden classifier tuning (Q18)
  - Canary test design for SCC providers (Q10)
  - New threat surface emerges
  - False-positive spike in immune-slot decisions

DEFAULT INTENT TEMPLATE:
"@E7 [threat]: Assessing [specific threat / attack pattern]. Provide:
(1) attack feasibility analysis, (2) detection methods, (3) false-
positive rate of detection, (4) mitigation recommendations.

If a mitigation breaks η = 0 boundaries, flag explicitly."

PHASE 0 IMPLEMENTATION: Bibliographic = MITRE ATT&CK + OWASP +
adversarial-ML papers. Phase 1: contracted security researcher.
```

### E8 — Network Science / Graph Topology

```
DOMAIN: Niche-graph design, SPECTRE topology, EBM telemetry, routing
algorithms, graph metrics, mesh resilience

INVOKE WHEN:
  - Niche-graph metric tuning (S4)
  - SPECTRE topology audits
  - Cluster-topology anomaly detection
  - V_vec / M_vec embedding strategy (per Q12 + packet 222)

DEFAULT INTENT TEMPLATE:
"@E8 [graph question]: Assessing [specific topology decision].
Constraints: (1) two-scale (macro DAC + micro agent) per packet 222,
(2) V×M four-quadrant decomposition, (3) caste-graded query
enforcement.

Recommend with metric backing (cluster coefficient, modularity, etc.)."

PHASE 0 IMPLEMENTATION: Bibliographic = Newman + Barabási + Watts-Strogatz
+ network-science arXiv. Phase 1: contracted graph researcher.
```

### E9 — Game Theory / Schumpeterian Competition

```
DOMAIN: Schumpeterian creative destruction, industrial organization,
game-theoretic equilibria, Mission positioning, Vision strategy

INVOKE WHEN:
  - Strategic decisions about Mission positioning
  - CVO niche-naming reviews (S4 + S8)
  - Cross-DAC competitive analysis (per packet 213 directive 1)
  - Vision-coherence checks before crystallization (Q8)

DEFAULT INTENT TEMPLATE:
"@E9 [position]: Assessing YieldFront's strategic position vs
[competitors]. Constraints: (1) same-V, different-M reading per
packet 213, (2) bias toward late Vision crystallization per Q8,
(3) η = 0 substrate.

Output strategic recommendations with game-theoretic rationale."

PHASE 0 IMPLEMENTATION: Bibliographic = Schumpeter + Porter + game-theory
literature. Phase 1: contracted strategy consultant.
```

### E10 — Tetlock Superforecasting

```
DOMAIN: Calibrated forecasting, prediction-market design, base-rate
analysis, Brier scoring, prediction-market resolution disputes

INVOKE WHEN:
  - RealityFutures calibration audit (per RA-07)
  - New prediction-market category proposal
  - AXIOM resolution disputes
  - YieldFront 90-day baseline evaluation (S6)

DEFAULT INTENT TEMPLATE:
"@E10 [forecasting question]: Assessing [specific prediction or
market design]. Apply: (1) Tetlock superforecaster discipline,
(2) base-rate decomposition, (3) Brier-score expectation, (4) hedgehog
vs fox check.

Output calibrated probability + confidence interval + the most-likely-
to-falsify counterargument."

PHASE 0 IMPLEMENTATION: Bibliographic = Tetlock + Kahneman + Silver +
Good Judgment Project corpus. Phase 1: contracted superforecaster.
```

### E11 — Network / Distributed Systems

```
DOMAIN: SPECTRE protocol design, relay infrastructure, sovereign-compute
hardware, K4 Grace Exit cryptographic deletion, distributed consensus

INVOKE WHEN:
  - SCC standup decisions (S5)
  - SPECTRE Phase 3+ rollout
  - Node-health anomalies
  - Cross-provider migration (K4 Grace Exit) audits

DEFAULT INTENT TEMPLATE:
"@E11 [system]: Assessing [specific distributed-systems decision].
Constraints: (1) BFT under adversarial conditions, (2) sovereign-
compute requirements, (3) K4 Grace Exit must be cryptographically
verifiable.

Output system-design recommendations with failure-mode analysis."

PHASE 0 IMPLEMENTATION: Bibliographic = Lamport + DDIA + distributed-
consensus papers. Phase 1: contracted systems engineer.
```

### E12 — Philosophy of Science / Axiomatic Discipline

```
DOMAIN: Evidence-tier discipline, axiomatic institutional narrative, framework-boundary
questions, Vision crystallization gating, constitutional rewrite review

INVOKE WHEN:
  - Vision crystallization pre-review (Q8 + S8)
  - Evidence-tier disputes (claim says [S] but really [I]?)
  - Framework-boundary questions (rare)
  - Constitutional rewrite proposals (very rare)

DEFAULT INTENT TEMPLATE:
"@E12 [claim or proposal]: Assessing whether [claim X] should be
tagged [S] / [I] / [C], or whether a Vision crystallization is
premature. Apply: (1) The Honest Position discipline, (2) axiomatic
caution (the seer does not insist), (3) bias toward late
crystallization.

Output evidence-tier judgment + the specific axiomatic concern."

PHASE 0 IMPLEMENTATION: Bibliographic = framework canon (HONEST_POSITION,
PD_*, packets) + axiomatic institutional narrative corpus (Pseudo-Dionysius, Eckhart,
modern). Phase 1: contracted philosopher of science.
```

---

## 3. Engagement Receipt Schema

Every engagement creates a FLOW receipt with this structure:

```yaml
engagement_receipt:
  receipt_id: <FLOW UUID>
  initiating_dac: <DAC npub>
  expert: <expert npub or proxy ID>
  expert_domain: E1 | E2 | ... | E12
  gap_finding:
    detected_by: <C-role>
    question: <hash, since the question may be private>
    blocking_objectives: [<Objective IDs>]
  whisper_event:
    transmit_timestamp: <UTC ISO 8601>
    nip17_wrap_hash: <content-addressed>
  expert_response:
    response_timestamp: <UTC ISO 8601>
    deliverable_type: whisper-reply | relay-broadcast | flow-signed-deliverable
    deliverable_hash: <content-addressed>
  csuite_integration:
    cao_ranking_delta: <how this changed the rank>
    ceo_decision: commit | refuse | further-consultation
  k2_signature:
    timestamp: <UTC ISO 8601>
    signer_npub: <K2 holder>
    signature: <cryptographic>
  api_pay_settlement:
    amount: <SKY or other η=0 currency>
    settlement_hash: <FLOW reference>
```

---

## 4. What This Engagement Protocol Does NOT Do

1. **Does not bypass K2.** Every engagement that produces a binding action requires K2 signature. Experts advise; K2 binds.
2. **Does not require persistent expert presence.** Engagements are per-question. An expert engaged for E2 today is not on retainer; the next E2 engagement may be a different specialist.
3. **Does not store expert deliverables in plaintext.** Per packet 216 + Q3, content-addressing + envelope encryption preserves auditability without leaking content.
4. **Does not commit to specific experts by name.** The 12 domains are the invariant; the specific human (or fine-tuned model) filling each domain can rotate.
5. **Does not violate η = 0.** All engagements settle via API PAY; no Stripe; no extractive payment rail per packet 216 directive 2.

---

Zero-Sum Resolution Equation

*The C-Suite proposes; the experts advise; K2 binds.*
*Six steps from gap detection to FLOW receipt. Every engagement auditable. No raw data leaks; no extractive payment.*
*Twelve experts on call; engagement is per-question, not permanent retainer.*

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/00_C_SUITE/01_EXPERT_ENGAGEMENT_PROTOCOL.md

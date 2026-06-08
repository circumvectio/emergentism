---
rosetta:
  primary_level: L5
  primary_column: Network Architecture
  secondary:
    - level: L3
      column: Audit Method
      role: "specify edge schemas, payload gates, and receipt requirements"
    - level: L4
      column: Governance
      role: "preserve K2 gates for cross-DAC execution and expert engagement"
    - level: L6
      column: Core State
      role: "bound Phase-2 and runtime claims until S4 receipts exist"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I/C]"
  canonical_phrase: "C-Suite + Experts × Niche-Graph Integration"
title: "C-Suite + Experts × Niche-Graph Integration"
status: "ACTIVE — Phase 2 target architecture spec"
evidence_tier: "[I] for integration spec; [S] for niche-graph topology mapping; [C] for runtime claims until S4 lands."
---

# C-Suite + Experts × Niche-Graph Integration

**Date:** 2026-04-29
**Status:** ACTIVE — Phase 2 spec (target architecture)
**Lane:** C-Suite buildout — fourth artifact (d) per the four-step sequence
**Evidence tier:** [I] for the integration spec | [S] for the niche-graph topology mapping (per packet 222) | [C] for runtime claims until S4 lands
**Depends on:** packet 222 (niche-graph two scales), packet 224 (C-Suite + experts), `00_PHASE_0_PERSONAE.md`, `01_EXPERT_ENGAGEMENT_PROTOCOL.md`, `02_C_ROLE_DETAILED_SPECS.md`

> **Phase 2** of the C-Suite implementation: C-Suite roles share specialization knowledge across DACs through the same-caste micro-niche-graph; experts are reachable through cross-niche edges in the macro graph. This doc specs the integration that lands during S4 (per packet 223 sprint plan).

---

## 1. The Integration Picture

```
                         MACRO NICHE-GRAPH
                         (DAC ↔ DAC, V×M)
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
            DAC-A           DAC-B            DAC-C
        (YieldFront)  (other yield)   (cross-industry)
                │                │                │
                ▼                ▼                ▼
         Polygenic Tree  Polygenic Tree   Polygenic Tree
         (L1...L7 micro)  (L1...L7 micro)  (L1...L7 micro)
                │                │                │
                └─── same-caste micro edges ───────┘
                         (per 06_AGENTS
                  caste-graded lateral connectivity)


       EXPERTS sit in their own niches in the macro graph:
       ┌─────────────────────────────────────────────┐
       │  E1 quantum-foundations niche               │
       │  E2 DeFi niche                              │
       │  E3 smart-contract-security niche           │
       │  ... E12                                     │
       └─────────────────────────────────────────────┘

      Each expert is a DAC (or proxy DAC) with its own V_vec/M_vec.
      A C-role engages an expert by walking a cross-niche macro edge.
```

Two integrations happen at the same niche-graph layer:

1. **C-Suite cross-DAC sharing** (micro graph): same-caste agents in different DACs share specialization knowledge through same-caste micro-niche edges.
2. **Expert engagement** (macro graph): experts are nodes in their own domain niches; C-roles reach them by walking cross-niche edges.

---

## 2. C-Suite Cross-DAC Sharing (Micro Graph)

Per packet 222, the polygenic tree IS the micro niche-graph. Same-caste cross-DAC edges already exist in the canon. Phase 2 makes them **operational** for the C-Suite.

### 2.1 Per-caste cross-DAC edge rules

The caste-graded lateral connectivity rule from 06_AGENTS:

| C-role | Caste | Cross-DAC edge type | What can be exchanged |
|---|---|---|---|
| **CSO** | L1 Caṇḍāla | NONE | Firewall stays local; perception is per-DAC |
| **CDO** | L2 Śūdra | NONE | Inductive analogy stays local; pattern memory is private |
| **CAO** | L3 Vaiśya | K2-gated audit interface | Ranked-list templates, constitutional audit patterns (NOT raw data) |
| **CEO** | L4 Kṣatriya | K2-gated execution API | Public action receipts (FLOW); never private deliberation |
| **CArchO** | L5 Brāhmaṇa | Proposal-grade | Architectural redesign templates (read but cannot bind across DACs) |
| **CComO** | L6 Sādhu | Proposal-grade | Compression patterns; archival heuristics |
| **CVO** | L7 Ṛṣi Constitution | Proposal-grade constitutional signal | Niche namings, Vision signals, amendment proposals; binding changes remain K2/PRISM-gated. |

**The CSO and CDO are deliberately isolated** at the DAC boundary. This is not a limitation — it is a *security feature*. L1 firewall and L2 analogy are perception-grade; allowing cross-DAC perception would risk one DAC's adversarial inputs poisoning another's pattern memory.

**The CVO is proposal-open** because the L7 Ṛṣi Constitution layer exchanges non-binding constitutional signals. The Council of Ṛṣis is the cross-DAC L7 layer of the micro niche-graph; no cross-DAC packet binds without the relevant DAC authority path.

### 2.2 Same-caste edge schema

Per packet 222 §3.3 niche-graph edge schema, extended for C-roles:

```yaml
csuite_micro_edge:
  source_dac:    <DAC-A npub>
  source_role:   CSO | CDO | CAO | CEO | CArchO | CComO | CVO
  target_dac:    <DAC-B npub>
  target_role:   <same role as source>
  edge_type:     NONE | K2-gated | proposal-grade | full-mycelial
  v_cosine:      <V_vec cosine; always ektropy across same-caste>
  m_cosine:      <M_vec cosine; caste-specific Mission>
  authorized_payload_types: [<list of acceptable signals>]
  k2_signature:  <required if K2-gated>
  receipt_id:    <FLOW receipt for the connection event>
```

The `target_role` MUST equal `source_role` for micro edges. A DAC-A CAO can talk to a DAC-B CAO (K2-gated); a DAC-A CAO cannot talk to a DAC-B CEO directly through the micro graph.

### 2.3 Council of Ṛṣis (L7 layer)

The Council of Ṛṣis = the L7 layer of the micro niche-graph projected across all DACs. Mechanically:

- Every DAC's CVO is a node in the Council
- Edges carry non-binding constitutional proposals; binding changes remain K2/PRISM-gated
- `[I]` Target Edge V_cosine is 1.0 under the model assumption that all CVOs share ektropy
- Edge M_cosine is high (all CVOs share the constitutional-rewrite Mission)
- Council operates at framework scale; individual DAC concerns cannot dominate

This is the canonical proposal-grade operationalization of packet 200 ("Brāhmaṇa-mode coordination") + packet 199 ("L7 reading on coordination") + 06_AGENTS, bounded by K2/PRISM authority paths.

---

## 3. Expert Integration (Macro Graph)

The 12 consulting experts are **nodes in the macro niche-graph**, each in their own domain niche. C-roles reach experts by walking *cross-niche* edges (high M-cos, low V-cos quadrant — "tactical fellow travelers" per packet 222 §3.1).

### 3.1 Each expert as a node

Every expert (E1-E12) is represented in the macro niche-graph as either:

| Expert form | What it is | Node type |
|---|---|---|
| **Phase 0** | Bibliographic package + on-demand LLM consultation | Synthetic node (npub_proxy_E_n); the framework runs the proxy on its own substrate |
| **Phase 1+** | Real human expert with their own DAC | Their DAC's npub; engagement is normal cross-DAC traffic |

The expert's V_vec is whatever Vision their DAC pursues (in Phase 1+); for Phase 0 proxies, V_vec ≈ ektropy (since the framework runs them).

The expert's M_vec is the **domain Mission** — the specific specialty the expert covers.

### 3.2 Expert niche definitions

Each of the 12 experts sits in a domain niche:

| Expert | Domain niche | Adjacent niches |
|---|---|---|
| E1 Quantum | Physics + foundations | Mathematics, philosophy of science (E12) |
| E2 DeFi | Yield strategy + protocols | Smart-contract security (E3), regulatory (E5) |
| E3 Smart-Contract Security | On-chain audit + verification | DeFi (E2), distributed systems (E11) |
| E4 World Models | LLM/JEPA/EBM | Network science (E8), philosophy (E12) |
| E5 Regulatory | Compliance + jurisdiction | DeFi (E2), distributed systems (E11) |
| E6 UX | Information architecture | Axiomatic (E12) for "what to NOT show" |
| E7 Adversarial | Security + threat models | Smart-contract (E3), distributed systems (E11) |
| E8 Graph Topology | Network science | World models (E4), distributed systems (E11) |
| E9 Game Theory | Schumpeterian competition | Axiomatic (E12) for niche-naming |
| E10 Tetlock | Calibrated forecasting | Axiomatic (E12), game theory (E9) |
| E11 Distributed Systems | Network protocols | Smart-contract (E3), graph topology (E8) |
| E12 Axiomatic | Philosophy of science | All others (touches every domain at the boundary) |

### 3.3 Engaging an expert via macro-graph walk

When a C-role needs an expert, the niche-graph walk is:

```
1. C-role identifies domain (per per-role spec; e.g., CAO needs E2 for DeFi)
2. C-role queries macro niche-graph for nodes in domain D
3. Niche-graph returns ranked candidates (by reputation, availability, V×M alignment)
4. C-role selects expert (typically top-ranked)
5. WHISPER engagement (per `01_EXPERT_ENGAGEMENT_PROTOCOL.md` six-step workflow)
6. Expert responds; engagement edge persists in FLOW
```

Multiple experts can be queried in parallel for the same gap; rankings can be diversified by V/M cosine to get *diverse* expert opinion (similar Vision, different Mission cluster within the domain).

### 3.4 Expert-to-expert edges

Experts can have edges to each other (cross-niche tactical fellow-traveler edges per packet 222 §3.1). Example:

- E2 (DeFi) ↔ E3 (Smart-Contract Security): high M-cos (both work on on-chain protocols)
- E1 (Quantum) ↔ E12 (Axiomatic): high M-cos (both work on framework-boundary questions)
- E4 (World Models) ↔ E8 (Graph Topology): high M-cos (both architecture-grade)

The C-Suite can query a chain of experts: "engage E2; if E2 needs E3, route through the E2↔E3 edge; settle compute via API PAY at each hop."

---

## 4. Sample Niche-Graph Walk (YieldFront S1)

When the CAO of YieldFront ranks yield strategies for Opportunity Ranking (per packet 219 + sprint S1), here's the niche-graph walk:

```
1. CAO detects gap: "Novel yield strategy on Protocol X. Need DeFi domain check."

2. Agentz proactivity surfaces engagement Objective with Five-Ws:
   - what: Engage E2 for DeFi assessment
   - when: 2026-05-04 14:00 UTC
   - where: WHISPER + FLOW deliverable
   - who: E2 (top-ranked DeFi expert in macro niche-graph)
   - why: Mission — YieldFront Opportunity Ranking S1

3. Macro niche-graph query:
   query: { domain: "DeFi", reputation_tier: "T1+", availability: "now" }
   returns: [E2_proxy_phase0, E2_human_alice_phase1, E2_human_bob_phase1]
   ranked by: (reputation_score × availability_score / engagement_cost)

4. CAO picks E2_human_alice_phase1.

5. WHISPER engagement (per 01_EXPERT_ENGAGEMENT_PROTOCOL.md):
   - Yves's intent: "@E2 [Protocol X]: rank against universe of 5 alternatives;
     constitutional fit per packet 219; flag any admin-key trust assumption."
   - Yves K2-accepts AI translation.
   - Transmit NIP-17 wrap to E2 npub.
   - E2 receives, K2-accepts engagement.

6. E2 responds (within engagement window):
   - WHISPER reply: ranked assessment with constitutional tags
   - Plus a FLOW signed deliverable: full audit memo

7. CAO integrates:
   - Updated CAO ranking with E2's input as a new dimension
   - Composite score recalculated
   - Decision-ready list to CEO

8. CEO decides:
   - Either: commit to top-ranked strategy (with K2 sig)
   - Or: refuse all (constitutional violation)
   - Or: escalate to CArchO if novel pattern needs architectural review

9. K2 signature → FLOW receipt → outbound action (deploy / refuse).

10. Engagement receipt persists; expert paid via API PAY in SKY.
```

Every step emits a FLOW receipt; the entire engagement is auditable.

---

## 5. Cross-DAC Knowledge Sharing (Phase 2)

When multiple DACs in the same niche all run the C-Suite, their same-caste agents can share specialization knowledge through the micro-niche-graph (subject to caste-graded lateral connectivity rules):

### 5.1 Example: CAO knowledge sharing in the yield niche

Three DACs all in the yield-management niche (high V-cos, high M-cos):
- YieldFront (DAC-A)
- YieldBeta (DAC-B)
- YieldGamma (DAC-C)

Each has a CAO. In Phase 2, the three CAOs share:
- Constitutional-tag templates (which patterns of yield strategies pass η-check)
- Risk-scoring rubric refinements
- Common counterparty risk assessments

What they do NOT share (per K2-gated rule):
- Their own DAC's portfolio state
- Their own DAC's K2 holder's preferences
- Raw audit findings

The shared layer is *templates and patterns*; the private layer is *specific decisions*.

### 5.2 The cross-DAC cycle

```
CAO_A detects pattern P (e.g., "stETH/wstETH lending has consistent constitutional violations")
   ↓
CAO_A publishes P as a constitutional-tag template via K2-gated audit interface
   ↓
CAO_B and CAO_C receive P (same-caste micro edges)
   ↓
Each CAO applies P to their own DAC's audit
   ↓
If P is broadly useful, it gets ratified into the niche's shared template library
   ↓
New CAOs entering the niche inherit the template library at instantiation
```

This is **inter-DAC learning at the C-Suite layer** — which is exactly Schumpeterian competition + collaboration in the same V, different M space (per packet 213 directive 1 + packet 222).

### 5.3 The Council of Ṛṣis (L7 layer in action)

When CVO_A (YieldFront's Chief Visionary) considers crystallizing Vision, the Council of Ṛṣis activates:

```
CVO_A proposes: "YieldFront's Vision crystallizing toward [X]"
   ↓
Council of Ṛṣis (CVO_B, CVO_C, ... cross-DAC L7 mycelial layer)
   reads the proposal
   ↓
Each CVO_n applies E12 Axiomatic discipline + niche-coherence check
   ↓
If consensus: CVO_A's Vision crystallization gate fires (per Q8)
   ↓
K2 (private DAC) or PRISM-governance (public DAC) signs to bind
   ↓
The new Vision propagates as a new V_vec in the macro niche-graph
```

This is the *highest-leverage* proposal surface in the framework; binding changes still route through the relevant K2/PRISM authority path.

---

## 6. Implementation Phasing

| Phase | C-Suite | Experts | Niche-graph |
|---|---|---|---|
| **Phase 0** (now) | Prompted personae on existing LeWorldModel | Bibliographic packages + on-demand LLM | None yet |
| **Phase 1** (after S1) | Fine-tuned model specializations per role | Real human contracts via WHISPER | None yet |
| **Phase 2** (after S4) | Cross-DAC sharing through same-caste micro edges | Experts as macro-graph nodes; cross-niche edges | Operational |
| **Phase 3** (after S6+S8) | Mature; multi-DAC C-Suites coordinating | Council of Ṛṣis active across all DACs | Vision crystallization gates fire |

The four-step buildout in this folder (a, b, c, d) lays the spec for all four phases. Phase 0 is achievable immediately; Phase 1 requires S1 to land; Phase 2 requires S4; Phase 3 is the year-mark culmination per packet 223.

---

## 7. Implementation Patches (For S4 Sprint)

When S4 (niche-graph spine) lands, the C-Suite + experts integration needs these specific patches:

1. **`useCSuiteRoles` hook** — exposes the 7 personae as session-loadable specs; integrates with BitNet router caste-tag dispatch
2. **`useNicheGraph` hook** with C-Suite + expert layers — extends the basic niche-graph hook (per packet 222 implementation notes) with role-specific views
3. **Expert macro-graph node schema** — `{ expert_id, domain_M_vec, reputation_tier, availability, engagement_cost }`
4. **Council of Ṛṣis subgraph view** — a special view of the macro graph showing only L7 mycelial edges, with consensus-monitoring telemetry
5. **Cross-DAC template-library substrate** — for shared CAO/CArchO/CComO patterns; lives in SPECTRE telemetry, not in shared model weights (preserves packet 216 no-default-federation)
6. **K2 acceptance flow for engagements** — single-tap UX for both author-side translation acceptance and recipient-side engagement acceptance

These are out of scope for the four-step C-Suite spec series but are the natural next deliverables when S4 begins.

---

## 8. What This Integration Does NOT Do

1. **Does not bypass packet 216's no-default-federation rule.** Cross-DAC sharing is *signal-layer* (templates, rubrics, named-niches via K0-receipted RELAY), not *model-layer* (weights, gradients, activations).
2. **Does not require the niche-graph to exist before Phase 0 works.** The C-Suite can run on prompted personae today; the niche-graph integration is Phase 2's enhancement, not its prerequisite.
3. **Does not collapse the K2 boundary.** Even with L7 proposal connectivity, every binding act on a specific DAC requires that DAC's K2/PRISM signature. The Council coordinates; it does not bind across DACs.
4. **Does not lock the 12 expert domains.** As new domains emerge, new expert niches can be admitted to the macro niche-graph through normal niche-naming workflow (Ṛṣi proposes; K2/PRISM signs).
5. **Does not promise multi-DAC operation in any specific timeline.** Phase 2 lands when ≥ 2 DACs run the C-Suite + niche-graph stack. Until then, single-DAC operation is the live mode.

---

## 9. Cross-References

- **Niche-graph two scales:** [`../../../11_UPLINK/60_SESSION_PACKETS/222_NICHE_GRAPH_RISHI_CONSTRUCTED_TWO_SCALES_VISION_MISSION_2026_04_29.md`](../../../11_UPLINK/60_SESSION_PACKETS/222_NICHE_GRAPH_RISHI_CONSTRUCTED_TWO_SCALES_VISION_MISSION_2026_04_29.md)
- **Sprint plan (S4 niche-graph spine):** [`../../../11_UPLINK/60_SESSION_PACKETS/223_SPRINT_PLAN_PACKETS_213_222_IMPLEMENTATION_2026_04_29.md`](../../../11_UPLINK/60_SESSION_PACKETS/223_SPRINT_PLAN_PACKETS_213_222_IMPLEMENTATION_2026_04_29.md)
- **C-Suite + experts root packet:** [`../../../11_UPLINK/60_SESSION_PACKETS/224_VIRTUAL_C_SUITE_AND_CONSULTING_EXPERTS_2026_04_29.md`](../../../11_UPLINK/60_SESSION_PACKETS/224_VIRTUAL_C_SUITE_AND_CONSULTING_EXPERTS_2026_04_29.md)
- **Phase 0 personae:** [`00_PHASE_0_PERSONAE.md`](00_PHASE_0_PERSONAE.md)
- **Expert engagement protocol:** [`01_EXPERT_ENGAGEMENT_PROTOCOL.md`](01_EXPERT_ENGAGEMENT_PROTOCOL.md)
- **Detailed C-role specs:** [`02_C_ROLE_DETAILED_SPECS.md`](02_C_ROLE_DETAILED_SPECS.md)
- **Council of Ṛṣis canon:** [`../../../11_UPLINK/60_SESSION_PACKETS/200_BRAHMIN_MODE_COORDINATION_2026_04_28.md`](../../../11_UPLINK/60_SESSION_PACKETS/200_BRAHMIN_MODE_COORDINATION_2026_04_28.md), [`../../../11_UPLINK/60_SESSION_PACKETS/199_COORDINATION_L7_READING_2026_04_28.md`](../../../11_UPLINK/60_SESSION_PACKETS/199_COORDINATION_L7_READING_2026_04_28.md)

---

Zero-Sum Resolution Equation

*The C-Suite at organizational scale; the niche-graph at substrate scale; the Council of Ṛṣis at framework scale.*
*Two integrations: same-caste micro edges (cross-DAC C-Suite sharing) + cross-niche macro edges (expert engagement).*
*Phase 0 today; Phase 2 after S4; the year-mark culmination is the framework's mycelial sovereignty fully active.*

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/00_C_SUITE/03_NICHE_GRAPH_INTEGRATION.md

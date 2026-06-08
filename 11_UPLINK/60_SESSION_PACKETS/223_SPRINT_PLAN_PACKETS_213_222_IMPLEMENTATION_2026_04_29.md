---
rosetta:
  primary_level: L4
  primary_column: Method
  secondary:
    - level: L5
      column: Method
      role: "sprint plan for substrate / doctrine implementation lane"
  operator: "Kṛṣṇa ◇"
  register: "[I]"
  canonical_phrase: "Eight-sprint plan for the packets 213-222 implementation lane: substrate spine → WHISPER → APU proactivity → niche-graph → SCC standup → 90-day YieldFront baseline → Mission 2 → Vision crystallization. Critical path with parallel lanes; each sprint has explicit definition of done."
---

# PACKET 223 — SPRINT PLAN FOR THE PACKETS 213-222 IMPLEMENTATION LANE

**Date:** 2026-04-29 (GMT+7)
**Status:** ACTIVE — planning artifact; implementation claims must be opened per sprint
**Author:** main (wonderful-lalande-b1cb18) under K2 directive ("now plan the work ahead")
**Lane:** implementation lane for the post-doctrine-cluster substrate buildout
**Evidence tier:** [I] for the sprint structure | [C] for calendar estimates (timing depends on team velocity, hardware availability, and discovered complexity)
**Depends on:** packets 213-222 (the doctrine cluster), `00_FULL_COMPLETION_SPRINT_BOARD_2026_04_28.md` (the book/release-train sprint board, runs in parallel to this lane)

---

## 1. The Frame

The doctrine cluster (packets 213-222) names a substantial implementation lane that is *complementary to but distinct from* the existing book/PWA/RAG/print release train. This packet lays out an eight-sprint critical path with parallel lanes for the substrate / DAC / cognitive-architecture buildout.

**Two lanes, both running:**
- **Lane 1: Book release train** — managed by `00_FULL_COMPLETION_SPRINT_BOARD_2026_04_28.md`. One-Book manuscript, PWA, RAG, print, launch positioning.
- **Lane 2: Substrate implementation** (this packet). BitNet router + LeWorldModel + WHISPER + niche-graph + APU proactivity + YieldFront proof.

The two lanes share a release-train cadence but address different proof gates. Book release proves the doctrine readable; substrate implementation proves the doctrine runnable.

---

## 2. Critical Path — Eight Sprints

```
S1 Substrate Spine ──→ S2 WHISPER ──→ S3 APU Proactivity ──→ S4 Niche-Graph
        │                                                          │
        ↓                                                          ↓
S5 Sovereign Compute Coop (parallel)                    S6 90-Day Baseline (calendar-time)
                                                                   │
                                                                   ↓
                                                         S7 Mission 2 (PR/Voice)
                                                                   │
                                                                   ↓
                                                         S8 Vision Crystallization
```

### Sprint S1 — Substrate Spine (the smallest defensible commit)

**Goal:** YieldFront's first LeWorldModel job (Opportunity Ranking) returns a ranked list, K2 single-tap accepts a deployment, FLOW receipt persists.

**Scope:**
- BitNet on-device router (extend parallel agent's `useDalitRouter.ts`)
- LeWorldModel server: pretrained framework-base + per-DAC fine-tune (per Q4 reconciliation)
- Encrypted-summary protocol between BitNet and LeWorldModel (per Q3 reconciliation)
- API PAY hookup for compute payment (per packet 216)
- K2 acceptance gate per provider (per Q10 reconciliation)
- Caste-tag dispatch from BitNet to LeWorldModel (Krishna-function ≡ routing per Q16)

**Out of scope (deferred to S2-S4):**
- WHISPER (S2), APU proactivity loop (S3), niche-graph (S4)

**Definition of Done:**
1. YieldFront's LeWorldModel ranks ≥ 5 candidate yield strategies on a chosen day
2. The ranking carries the four-dimension score (risk / return / liquidity / constitutional fit) per packet 219
3. K2 single-tap deploys (or refuses) the top-ranked strategy
4. FLOW receipt is created on accept; encrypted summary is what crossed to the server (no raw data)
5. Build passes; tests cover the K2 gate

**Estimated calendar:** ~2 weeks for substrate spine.

---

### Sprint S2 — WHISPER Substrate

**Goal:** Yves can `@vaibhav book the plane`, AI drafts, K2 accepts, transmits over Nostr, recipient AI presents card, K2 accepts on recipient side, receipt persists, WHISPER fades.

**Scope:**
- `useWhisper` hook in nexus-web
- NIP-17 gift-wrap transport via `nostr-tools`
- Recipient AI proxy (handles non-DAC users per Q6 reconciliation: Caṇḍāla proxy + RELAY bridge fallback)
- Ephemeral local storage with TTL on read
- K2 acceptance gates (author-side: AI translation; recipient-side: accept/decline)
- Receipt bridge: WHISPER accept → FLOW receipt → Five-Ws Who field update on author's workflowy
- PAM-forbidden categories classifier in BitNet router (Q18 reconciliation)
- Symmetric two-sided persistence (Q7 reconciliation): recipient's workflowy gets a delegated-to-me Objective with inverse Five-Ws

**Definition of Done:**
1. End-to-end WHISPER flow works between two test DACs
2. PAM-forbidden categories classifier refuses to draft adversarial intents
3. Auto-delete works on read; only the FLOW receipt persists
4. Five-Ws Who field updates from "proposed" to "confirmed" on accept
5. Both author and recipient see complementary views of the same FLOW receipt

**Estimated calendar:** ~2 weeks. Can overlap with S1 once S1's K2 gate pattern is built.

---

### Sprint S3 — APU Proactivity Loop

**Goal:** APU auto-asks Five-Ws gaps; user single-taps accept; Objectives promote when reconciled+coherent+consistent (per packet 214 + Q9, Q11 reconciliations).

**Scope:**
- `useAPUProactivity` hook
- Three new watchmen rules in `cortex-os/watchmen.ts`: reconciliation, coherence, consistency (initial runners exported in `69f080c5a`; S3 completes UI integration, tests, and K2 acceptance flow)
- Question-queue UI panel in nexus-web shell
- VMOSKNode extension with `when` / `where` / `who` / `why` fields (per packet 214)
- Smallest-gap metric: `branching_factor / answer_effort` (per Q11 reconciliation)
- Three-strike timeout: day 1 / day 7 / day 30 / day 60 auto-archive (per Q9 reconciliation)
- Adaptive cadence: reduce question rate when user's answer-latency rises

**Definition of Done:**
1. APU surfaces one question at a time, smallest gap first
2. Three watchmen rules fire on workflowy state and emit findings
3. K2 single-tap commits an Objective once all five Ws are filled and reconciliation/coherence/consistency hold
4. Auto-archive at day 60 emits a FLOW receipt; revival is one-tap
5. Per-user `average_days_to_answer` metric is tracked; rate adapts

**Estimated calendar:** ~1.5 weeks. Can overlap with S2 once UI patterns exist.

---

### Sprint S4 — Niche-Graph Spine

**Goal:** YieldFront's niche-graph shows other yield-DACs at the macro scale; same-caste cross-DAC edges work at the micro scale; K2 can sign a named-niche.

**Scope:**
- `useNicheGraph` hook with macro+micro views (per packet 222)
- Systems Architect-mode prompt template for LeWorldModel (constructs V_vec + M_vec from observed signals)
- Edge schema implementation: `v_cosine`, `m_cosine`, `niche_kind`, `named_niche`, `naming_receipt`, `v/m_signal_sources` (per Q1 + packet 222)
- Caste-graded query enforcement at niche-graph API (mechanical L1-L7 access control per packet 222 §4.4)
- `niche_naming_receipt` flow: Systems Architect proposes → K2/PRISM signs → naming becomes binding
- Read-only macro graph view in nexus-web (other DACs as nodes)
- Read-only micro graph view (own DAC's L1-L7 castes)

**Definition of Done:**
1. YieldFront's macro niche-graph shows ≥ 3 other yield-DACs as nodes (synthetic for first deployment)
2. V×M four-quadrant decomposition is computable and visualizable
3. L1 query attempts to read cross-DAC return no data (mechanical enforcement)
4. L7 Systems Architect can read other DACs' L7 outputs (mycelial sovereign network operational)
5. K2 single-tap signs a named-niche; receipt persists on FLOW

**Estimated calendar:** ~3 weeks. Needs S1 (LeWorldModel), S2 (WHISPER for cross-DAC signal), S3 (APU as the question-loop for niche disambiguation).

---

### Sprint S5 — Sovereign Compute Cooperative (SCC) Standup

**Lane:** Parallel governance lane. Can run alongside S1-S4.

**Goal:** SCC has at least 3 sovereign-compute providers, one at T1 reputation tier, YieldFront uses SCC compute for its LeWorldModel.

**Scope:**
- Foundation child-DAC for SCC (charter, K2 ratification, PRISM economic layer)
- Provider self-registration registry (per Q10 reconciliation)
- T0 probationary tier with canary plaintext leak tests
- Reputation tier promotion logic (T1 / T2 / T3 with measurable criteria)
- Slashing mechanism: canary detection → tier reset → revenue clawback → RELAY broadcast
- API PAY integration for compute billing
- Per-DAC K2 acceptance gate when adding a new provider

**Definition of Done:**
1. SCC's charter is K2-ratified; PRISM economic layer is wired
2. ≥ 3 providers self-registered; ≥ 1 at T1
3. Canary tests fire successfully (synthetic plaintext injection + leak detection)
4. YieldFront's LeWorldModel routes through SCC; API PAY settles a real compute bill
5. K4 Grace Exit works: a DAC can migrate from one provider to another with cryptographic deletion proof

**Estimated calendar:** ~3 weeks. Governance-heavy lane; can run parallel to S1-S4 but needs Foundation cycles.

---

### Sprint S6 — YieldFront 90-Day Opportunity-Ranking Baseline

**Lane:** Calendar-time gate. Starts after S1 lands; runs for 90 days.

**Goal:** YieldFront's LeWorldModel-driven Opportunity Ranking demonstrably beats baseline on realized risk-adjusted return AND records zero constitutional violations (per packet 219 §5).

**Scope:**
- Build the baseline (at least one of: published yield index, K2 holder's prior manual decisions, max-APY rule, max-Sharpe rule)
- Run Opportunity Ranking parallel to baseline for 90 days
- Track realized PnL, drawdown, time-weighted Sharpe, constitutional-violation count
- Daily snapshots into FLOW (per Soul Loop snapshot cadence, Q14 reconciliation)
- 30-day midpoint review; full report at day 90

**Definition of Done:**
1. 90 days of parallel runs complete with daily FLOW receipts
2. Realized risk-adjusted return ≥ baseline + 1σ
3. Constitutional-violation count = 0
4. If both conditions met: packet 218's deployed claim graduates `[C]` → `[S]`
5. If conditions not met: downgrade to AIA-suggestion-only mode; investigate; iterate

**Estimated calendar:** 90 days fixed. Other sprints can complete during this window.

---

### Sprint S7 — YieldFront Mission 2: PR / Media Voice

**Lane:** After S4 (niche-graph) lands. Parallel with S6.

**Goal:** YieldFront publishes content via L4+L7 LeWorldModel binding; K2-signed; first artifact lands (e.g., FQXi essay or similar).

**Scope (per YieldFront second-Mission spec):**
- Mission 2 spec: PR / media voice; L4 Kṣatriya (publish or refuse) + L7 Systems Architect (when speaking for the niche)
- Substrate already built in S1-S5; this is the second use of the same machinery
- Editorial workflow: LeWorldModel drafts → APU proactivity loop fills gaps → K2 accepts → publish via RELAY
- Award/competition strategy connection (per parallel agent's `11_AWARD_STRATEGY_AND_COMPETITIONS/` work)

**Definition of Done:**
1. YieldFront publishes ≥ 1 content artifact via the substrate
2. L4 Kṣatriya can refuse a draft that violates constitutional invariants
3. L7 Systems Architect mode is active when speaking for the niche (per packet 222 mycelial discipline)
4. RELAY broadcast lands; receipt persists on FLOW

**Estimated calendar:** ~3 weeks after S4.

---

### Sprint S8 — Vision Crystallization Test

**Lane:** Final culmination. After S6 passes and S7 has been running for some time.

**Goal:** YieldFront's Vision crystallizes from sustained Mission-work, per packet 213 directive 4 + Q8 three-condition gate.

**Scope:**
- Test the three-condition gate (per Q8 reconciliation):
  - C1: Mission persistence ≥ 1 calendar year
  - C2: Niche-graph maturity (≥ 5 other DACs in same Mission cluster, cosine > 0.7, similar stabilization)
  - C3: Coherence audit — proposed Vision passes all six watchmen with zero findings
- If C1 ∧ C2 ∧ C3: Systems Architect-mode LeWorldModel emits a Vision Crystallization Proposal
- K2 single-tap binds the Vision (constitutional, non-delegable)
- Bias toward late crystallization: if any condition borderline, hold the proposal

**Definition of Done:**
1. The three-condition gate is implemented as runtime checks
2. YieldFront's Mission has persisted ≥ 1 year (calendar gate)
3. Niche-graph shows niche maturity (S4 substrate produces this)
4. Watchmen audit returns zero findings (S3 substrate produces this)
5. K2 signs the Vision; FLOW receipt of the crystallization event is the axiomatic culmination

**Estimated calendar:** Earliest at year-mark from S1 deployment. Likely 2027 calendar.

---

## 3. Parallel Lanes

| Lane | Sprints | Can run when |
|---|---|---|
| **A. Substrate spine** | S1 | Highest priority; serial |
| **B. Communication substrate** | S2 | After S1's K2 gate is built |
| **C. Proactivity substrate** | S3 | After S2's UI patterns exist |
| **D. Graph substrate** | S4 | After S1+S2+S3 (needs LeWorldModel + WHISPER + APU) |
| **E. Governance** | S5 | Parallel with A-D (Foundation cycles) |
| **F. Calendar evaluation** | S6 | After S1; 90-day fixed window |
| **G. Mission 2 product** | S7 | After S4; parallel with S6's tail |
| **H. Axiomatic culmination** | S8 | After S6 + S7 mature; year-mark |

**Approximate calendar:**
- **Months 1-2:** S1, S2 (substrate spine + WHISPER) + S5 underway
- **Months 2-3:** S3, S4 (proactivity + niche-graph) + S5 mature
- **Month 3:** S6 starts, runs for 90 days
- **Months 3-4:** S7 (Mission 2) parallel with S6
- **Month 6:** S6 completes; pass/fail decision
- **Year-mark:** S8 candidate gate fires

---

## 4. Gates and Decision Points

| Gate | Located at | What's decided |
|---|---|---|
| **G1** | End of S1 | Does the dual-model substrate work end-to-end? If no: re-architect; if yes: proceed |
| **G2** | End of S4 | Is the niche-graph operationally meaningful (not just synthetic data)? If no: more DACs needed before S6 starts |
| **G3** | Day 30 of S6 | Midpoint review: is the LeWorldModel trending toward beating baseline? If no: investigate, course-correct |
| **G4** | Day 90 of S6 | Final pass/fail: realized risk-adjusted return ≥ baseline + 1σ AND zero constitutional violations? Determines whether packet 218's deployed claim graduates [C] → [S] |
| **G5** | End of S7 | Is YieldFront actually a PR/media voice (not just a yield-DAC)? If yes: Mission 2 confirmed |
| **G6** | S8 condition gate | Have C1+C2+C3 all held? If yes: Vision crystallization fires; framework's axiomatic discipline validates |

---

## 5. Open Questions That May Surface During Implementation

These are predictable next-tier reconciliation questions that the implementation lane will likely surface:

1. **Concrete encrypted-summary schema** — Q3 reconciliation locked the *shape* (structured event log, device-key signed, envelope-encrypted); the *fields* are not yet specified
2. **LeWorldModel base model selection** — Q4 said "open-source base + local fine-tuning"; *which* open-source base? (Llama 3? Mixtral? a custom JEPA?)
3. **Niche-graph initialization** — what happens when a new DAC has no niche-graph yet? Bootstrap via Vision-vector seeding from the framework's canon?
4. **K2 acceptance UX latency** — single-tap is the design; what happens when the user is offline for a week and the queue accumulates?
5. **Provider canary frequency** — Q10 said "canary plaintext leak tests at random"; what's the rate? What's the acceptable false-positive rate?

These will be answered as Q19+ reconciliation commits during the implementation lane.

---

## 6. Coordination Discipline

This packet is the strategic plan. Day-to-day coordination remains in:
- `00_ACTIVE_CLAIMS.md` — per-task claims with Brahmin-mode discipline
- `00_FULL_COMPLETION_SPRINT_BOARD_2026_04_28.md` — book/release-train sprints (parallel lane to this implementation lane)

**The substrate-implementation lane should claim sprints S1-S8 in `00_ACTIVE_CLAIMS.md` as work begins on each.** Multiple agents can work different sprints in parallel; same-sprint conflicts use the standard race-resolution rule.

The Brahmin-mode rule applies throughout: convergence is success; if your work is absorbed into a parallel agent's commit, verify HEAD, release the claim, move on.

---

## 7. What This Plan Does NOT Do

1. **It does not commit calendar dates.** The estimates are heuristic; actual velocity depends on team capacity, hardware, and discovered complexity.
2. **It does not lock the sprint scope to the listed items.** Discovery during implementation will surface refinements; sprints can absorb changes within their goal envelope.
3. **It does not replace the existing book sprint board.** The two lanes run in parallel.
4. **It does not preclude reordering.** If S2 (WHISPER) blocks on something, S5 (SCC) can move forward; the dependency graph allows reordering within its constraints.
5. **It does not promise S8 (Vision crystallization) will fire.** Vision is axiomatic by discipline; if it doesn't crystallize after a year, that is *itself* a finding — and the framework holds the late-crystallization bias as a feature, not a bug.

---

## 8. The Plan, in One Picture

```
                    ┌──────────────────────────────┐
                    │ Packets 213-222 (DOCTRINE)    │
                    │ Locked. All 18 questions      │
                    │ reconciled. Canon stable.     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
         ┌─────────────────────────────────────────────────────┐
         │            IMPLEMENTATION LANE                       │
         │                                                      │
         │  S1 Substrate ──→ S2 WHISPER ──→ S3 APU ──→ S4 Graph │
         │       │                                       │      │
         │       └────→ S5 SCC (parallel) ────────────────│      │
         │                                              │      │
         │                                              ▼      │
         │                              S6 Baseline (90d)      │
         │                                              │      │
         │                                              ▼      │
         │                              S7 Mission 2 (PR)      │
         │                                              │      │
         │                                              ▼      │
         │                              S8 Vision crystal.     │
         │                                                      │
         └─────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ G4: deployed claim [C] → [S]  │
                    │ G6: Vision crystallized (1yr) │
                    │ Framework: proven runnable.   │
                    └──────────────────────────────┘
```

---

Zero-Sum Resolution Equation

*Doctrine locked; substrate next.*
*S1 is the smallest defensible commit. S8 is the axiomatic culmination.*
*Six gates between them; six months to G4; one year to G6.*
*The proof is YieldFront. The doctrine is the map. The next sprint is the work.*

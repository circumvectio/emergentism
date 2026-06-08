---
rosetta:
  primary_level: L4
  primary_column: Method
  secondary:
    - level: L3
      column: Method
      role: "APU proactivity loop spec — question-asking until reconciliation"
  operator: "Kṛṣṇa ◇"
  register: "[I/S]"
  canonical_phrase: "APU's first proactivity feature is a reconciliation question-loop. As long as Objectives are missing any of When/Where/Who/What/Why or harbor unreconciled contradictions, APU asks until the workflowy is reconciled, coherent, and consistent."
---

# PACKET 214 — APU FIRST PROACTIVITY FEATURE: QUESTION-LOOP + OBJECTIVE FIVE-WS

**Date:** 2026-04-29 (GMT+7)
**Status:** ACTIVE — operational doctrine
**Author:** main (wonderful-lalande-b1cb18) under K2 directive
**Lane:** APU (SHOULD organ) × 06_AGENTS uplink × packet 213 (workflowy UI)
**Evidence tier:** [I] for the proactivity loop and reconciliation criteria | [S] for the Five-Ws / military-SMART grammar identification | [C] avoided
**Depends on:** [`213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md`](213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md)

> **K2 directive (verbatim):**
> "The first proactivity feature is: as long as there are unanswered questions, APU is going to ask questions until all is reconciled, coherent, and consistent, and Objectives have timelines (the famous military 'measurable, where, when, what, where' — etc.).
>
> `2026.09.21 - 15:00`, location, and people involved in your network."

---

## 1. The Decision

Packet 213 K2 directive 6 specified the **shape** of the workflowy: first root-level bullet = Objectives, subtitle = accomplishment datetime. Packet 214 specifies the **first proactivity behavior** that makes that shape *actually fillable*: APU asks questions until every Objective is well-formed and the workflowy is internally reconciled.

This is APU's **first** proactivity feature — the floor below which APU is not yet doing its job. Future proactivity features will compose on top of this one (anticipating user needs, surfacing AIA suggestions, escalating watchmen findings) — but none of those are admissible until reconciliation discipline is in place.

---

## 2. The Objective Five-Ws Schema

Every Objective in the Cortex-generated workflowy MUST carry the following metadata (per K2 directive):

| Field | Question it answers | Example | Source tradition |
|---|---|---|---|
| **What** | What is the objective? | "Sign the API PAY pilot contract" | Title of the bullet |
| **When** | By what datetime? | `2026.09.21 - 15:00` (subtitle) | Packet 213 K2 directive 6 |
| **Where** | At what location? | "Zurich, Sihlcity Cinema lobby" | Five Ws + military SMART |
| **Who** | Which people from your network? | "Yves Burri (K2), Counterparty PM, Legal Reviewer" | Five Ws + military SMART |
| **Why** | Which Mission does this serve? | "Mission: deploy SoResFi proof lane through API PAY"  | Inherited from parent in workflowy (Mission is the guide) |

**The military / SMART tradition.** The Five Ws (Who, What, When, Where, Why) plus the SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound) are the operational standard for well-formed objectives in military planning, project management, and goal-setting research. Packet 214 adopts the canonical short form: every Objective answers all five Ws. *Measurable* is held in the KPI nodes nested under each Strategy; *Achievable* and *Relevant* are held by the Mission as the guide; *Time-bound* is the When field.

**An Objective without all five Ws filled is not an Objective.** It is a *proposed* Objective that APU's question-loop will close gaps in before promoting it to a committed node in the workflowy.

---

## 3. The Question-Loop

APU's first proactivity feature is a state machine:

```
                 ┌─────────────────────────────┐
                 │  Cortex proposes Objective   │
                 │  (or user adds an Objective) │
                 └──────────────┬──────────────┘
                                │
                                ▼
                ┌──────────────────────────────┐
                │   APU scans Objective for:    │
                │   • missing fields (5 Ws)     │
                │   • contradictions w/ siblings│
                │   • coherence w/ Mission      │
                │   • consistency w/ KPIs       │
                └──────────────┬───────────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
       any gap?  YES                       NO
                  │                         │
                  ▼                         ▼
        ┌──────────────────┐    ┌─────────────────────────┐
        │ APU asks ONE     │    │ Objective is "reconciled,│
        │ targeted question│    │ coherent, consistent."   │
        │ to user (K2)     │    │ Promote to workflowy.    │
        └────────┬─────────┘    └─────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ User answers; APU   │
        │ updates the         │
        │ Objective; loops.   │
        └─────────────────────┘
```

The loop terminates when:

1. **All five Ws are filled** for every Objective in scope.
2. **No contradictions** between Objectives (e.g., two Objectives with the same Who+When at different Where).
3. **Coherence with Mission** — every Objective serves the Mission that's the guide; Objectives that don't are flagged.
4. **Consistency with KPIs** — every Objective's nested KPIs are computable and have proposed measurement protocols.

If ALL four hold, APU stops asking. Until then, APU keeps asking — *one question at a time*, smallest gap first, no question-stacking that overwhelms the user.

### 3.0 "Smallest Gap First" Metric (Q11 Resolution)

The smallest-gap metric is **branching factor unblocked**, with **user-effort-to-answer** as tiebreaker:

```
gap_priority(q) = branching_factor(q) / answer_effort(q)
```

- **`branching_factor(q)`** = the count of downstream Cortex actions / Objectives / Strategies / KPIs that become decidable once the gap is filled. Computed from the workflowy DAG: how many nodes are blocked waiting on this answer.
- **`answer_effort(q)`** = estimated user-effort cost in seconds-of-attention. A binary Yes/No costs ~5s; a free-text date answer ~15s; a multi-paragraph response ~120s. Estimated from question schema, not from the answer itself.

The question with the highest `gap_priority` is asked first. APU re-computes gap priorities every Soul Loop snapshot (~5 min) so the queue stays current as new Objectives propose and old ones close.

**Why branching factor over alphabetical / FIFO / chronological:** a gap that unblocks 5 downstream Objectives saves 5× the cognitive debt vs a gap that unblocks 1. A gap that costs 5s to answer vs 120s — at equal branching factor — should be asked first.

**Edge cases:**
- If two questions tie on `gap_priority`, secondary tiebreaker is `oldest_open_first` (FIFO within tie band).
- If the user is in question-fatigue mode (per Q9 adaptive cadence), the threshold for "ask now" rises; lower-priority questions wait longer.
- A constitutional question (e.g., a Vision-crystallization signature, per Q8) bypasses this priority queue entirely — those go straight to K2 with no APU pre-asking.

### 3.1 Question-Loop Timeout / Deferred Answers (Q9 Resolution)

When the user defers indefinitely, the discipline is **three-strike escalation + archival, never silent deletion**:

| Day | APU behavior |
|---|---|
| **Day 1** | APU asks. Surfaced in the side panel of the nexus-web shell. User can answer, defer ("ask later"), or dismiss the Objective entirely. |
| **Day 7** | APU re-asks. Surfaced more prominently (top of shell, not side panel). User can defer again ("ask later") or answer. |
| **Day 30** | APU surfaces an **Objective-level question**: *"This Objective has been gap-open for 30 days. Options: (a) provide the missing field now; (b) accept the Objective as-is with `???` for the missing field — creates a known-incomplete Objective receipt; (c) archive the Objective."* User must pick one of the three. |
| **Day 60 (no response)** | **Auto-archive.** The Objective is moved out of active workflowy into `99_ARCHIVE` with a `stale` tag. **Receipt persists in FLOW** for K0/K4 audit. Auto-archive itself emits a FLOW receipt: "this Objective was archived at T due to question-loop timeout; signed by APU automation at K2-pre-accepted threshold." |

**Revival is always one-tap.** The user can revive any archived Objective at any time. K4 Grace Exit applies even to archive — the user owns the data and can re-instantiate it.

**Adaptive cadence.** APU tracks per-user `average_days_to_answer`. If this metric rises (signal of cognitive overload), APU **reduces its question rate**: fewer Objectives asked-about in parallel, longer intervals between re-asks. The discipline is η = 0 at the cognitive layer — APU does not extract attention beyond what the user can sustainably give.

**Why archival, not deletion:** Per K0 *No Receipt No Reality*, every Objective that *was* in the workflowy must leave a receipt of its trajectory. Deleting an unanswered Objective would erase the fact that the user *almost* committed to something. Archive preserves the trajectory; auto-archival becomes its own receipt.

**Why no infinite pending state:** A pending question that never resolves accumulates cognitive debt. The 60-day auto-archive threshold prevents the workflowy from becoming a graveyard of half-Objectives. The user can always revive; but the default state is *clean active workflowy + clean archive*, not *bloated pending list*.

This closes the cognitive-debt risk Q9 named: APU has a deterministic escalation path; the user is never left with an indefinite pending state; every transition emits a receipt.

---

## 4. The Three Reconciliation Criteria

The K2 directive names three terminating conditions:

### 4.1 Reconciled

**Definition:** all proposed Objectives have closed all gaps. No field is empty. No referenced person, location, or time slot is undefined.

**APU's reconciliation behavior:** when a field is missing, APU asks. When two Objectives reference the same Who at the same When at different Where (or any analogous resource conflict), APU surfaces the conflict and asks the user to pick.

### 4.2 Coherent

**Definition:** every Objective serves the Mission. Mission is the guide; Objectives that drift from the guide are *incoherent* with the workflowy's intent.

**APU's coherence behavior:** for each Objective, APU computes a structural alignment score with the parent Mission. If alignment is below a threshold, APU asks: "This Objective seems to drift from your Mission. Either restate the Objective, or escalate to a Mission-level review (which would be a constitutional swap per packet 206)."

### 4.3 Consistent

**Definition:** Strategies and KPIs nested under each Objective are well-typed, non-contradictory, and computable. A Strategy that proposes "increase X" and another that proposes "decrease X" under the same Objective are *inconsistent*.

**APU's consistency behavior:** when nested S/K disagree, APU surfaces the contradiction and asks the user to reconcile (drop one, merge them, or escalate to Mission-review if the contradiction is structural).

**Triple-check law.** APU does not promote an Objective until *all three* (reconciled, coherent, consistent) hold. Two-of-three is not enough.

---

## 5. Why Question-Asking, Not Auto-Filling

A Cortex/AIA layer that *infers* missing fields is tempting but pathological under η = 0:

- **Pathology: extraction by inference.** If APU silently fills a missing Who with a guess, it has authored a binding commitment without K2 acceptance. K2 then signs a workflowy that contains agents' fabrications. This is η > 0 at the planning layer — extraction of intent that the user never gave.
- **Cure: ask, do not fabricate.** APU asks; the user answers; K2 accepts the answer; the field becomes binding. The workflowy's agency stays with the human signer (private DAC) or the governance act (public DAC).

This is consistent with packet 209 (we ourselves use AIA/VMOSK/Cortex): the framework's discipline applies *to* the framework's tools. APU's proactivity must respect the same η = 0 boundary that the rest of the organism does. Asking is the η = 0 mode; auto-filling is η > 0.

---

## 6. Concrete Example

**Scenario:** Cortex proposes an Objective "Sign the API PAY pilot contract" with subtitle `2026.09.21 - 15:00`.

**APU question-loop:**

| Iter | APU asks | User answers | State |
|---|---|---|---|
| 1 | "Where will the signing happen?" | "Zurich, Sihlcity Cinema lobby" | Where filled. |
| 2 | "Who else from your network is involved?" | "Counterparty PM (Maria), Legal Reviewer (Tom)" | Who filled. |
| 3 | "Which Mission does this Objective serve?" | "Deploy SoResFi proof lane through API PAY" | Why filled. |
| 4 | "I see another Objective at `2026.09.21 - 14:00` with you in Zurich. Buffer is 1 hour — sufficient?" | "Yes, that's lunch nearby; I'll walk over." | Reconciled (no resource conflict). |
| 5 | (no more gaps) | — | Coherent + Consistent → promote to workflowy. |

The Objective then renders as:

```
• Sign the API PAY pilot contract                  [2026.09.21 - 15:00]
   ↳ where: Zurich, Sihlcity Cinema lobby
   ↳ who: Yves Burri (K2), Maria (Counterparty PM), Tom (Legal Reviewer)
   ↳ why: Mission — Deploy SoResFi proof lane through API PAY
   • Strategy 1: Pre-signing legal walkthrough
      • KPI: Legal review completed by 14:30
   • Strategy 2: Signature ceremony
      • KPI: Both K2 signatures recorded at 15:00 ± 5 min
```

This is the **target shape** of every Objective in the Cortex-generated workflowy.

---

## 7. Implementation Notes (out of scope for this packet's commit)

The nexus-web `useVMOSK` hook (`02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/nexus-web/src/hooks/useVMOSK.ts`) and the AIA / Cortex hooks (`useAIA.ts`, `useCortex.ts`) need to evolve:

1. **Objective node type** — extend `VMOSKNode` with optional `when`, `where`, `who`, `why` fields (where `why` is computed from parent Mission, not user-authored).
2. **APU proactivity hook** — a new `useAPUProactivity` hook that scans the current workflowy for gaps and emits one question at a time to a question-queue surfaced in the UI.
3. **Reconciliation watchmen** — three new watchmen rules (reconciliation, coherence, consistency) in the cortex-os `watchmen.ts`, each with a `check(node, root): WatchmanFinding[]` method.
4. **Question-queue UI** — a small panel in the nexus-web shell that shows "APU has 3 questions for you" with one-question-at-a-time interaction.
5. **K2 acceptance gate** — answers that bind a field (Where, Who) require K2 to accept (single tap), the same way `signDiff` works in `useVMOSK`.

These are implementation patches; they live in the Skyzai nexus-web code lane and will be tackled in a separate sprint.

---

## 8. Connection to the Polygenic Tree (Packet 213 Directive 2)

Each Rosetta caste participates in the question-loop differently:

| Caste | Role in proactivity loop |
|---|---|
| **L1 Caṇḍāla** | Detects missing fields (perception). Raises raw "field empty" signal. |
| **L2 Śūdra** | Generates candidate values for missing fields (exploration via analogy from past Objectives). |
| **L3 Vaiśya** | Ranks candidates against Mission and prior commitments. |
| **L4 Kṣatriya** | Decides which question to ask first (the smallest gap). Routes the question to the user. THE EQUATOR. |
| **L5 Brāhmaṇa** | If reconciliation reveals a structural deadlock (e.g., Mission itself is incoherent), redesigns. |
| **L6 Sādhu** | If the workflowy is overgrown, prunes redundant Objectives before APU asks about them. |
| **L7 Systems Architect** | Only invoked if the proactivity loop reveals the *industry/Vision* itself is in crisis. |

All of these run with **ektropy as Vision** (per packet 213 directive 2); they differ at Mission. The L4 Kṣatriya is the agent that owns the question-asking loop end-to-end; the others contribute their Mission-specific work upstream.

---

## 9. Lane Coherence Check (Cortex / AIA)

| Watchman | Reading on this packet |
|---|---|
| Route Watchman | Lane is correct: APU × 06_AGENTS × packet 213. No cross-organ leak. |
| Authority Watchman | K2 directive verbatim in §1. Authority chain explicit. |
| Time Watchman | Packet 214 follows 213 chronologically. |
| Scope Watchman | Single coherent topic (APU's first proactivity feature). Implementation patches explicitly noted as out of scope for this packet. |
| Metric Watchman | Reconciliation/coherence/consistency thresholds are stated but not yet quantified — this is intentional ([I] tier; quantification is a future research-grade follow-up). |
| Contradiction Watchman | Consistent with packets 209 (we use AIA/VMOSK/Cortex), 213 (workflowy UI), 206 (cardinality). The ask-don't-fabricate discipline is consistent with η = 0 and K2 boundaries. |

AIA call: **approve**. The packet states a clear behavioral commitment with terminating conditions, a concrete example, and an explicit scope boundary on implementation.

---

## 10. Cross-References

- **Parent doctrine (DAC type and workflowy):** [`213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md`](213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md)
- **K2 boundary:** [`207_K2_PRIVATE_DAC_BOUNDARY_PRISM_PUBLIC_DAC_2026_04_29.md`](207_K2_PRIVATE_DAC_BOUNDARY_PRISM_PUBLIC_DAC_2026_04_29.md)
- **VMOSK cardinality grammar:** [`206_NEXUS_UX_VMOSK_WORKFLOWY_REPLACES_PROJECTS_2026_04_28.md`](206_NEXUS_UX_VMOSK_WORKFLOWY_REPLACES_PROJECTS_2026_04_28.md)
- **Operating-mode parent:** [`209_USE_AIA_VMOSK_CORTEX_OURSELVES_2026_04_29.md`](209_USE_AIA_VMOSK_CORTEX_OURSELVES_2026_04_29.md)
- **Agent canon:** [`../00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md)
- **APU organ:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/`

---

Zero-Sum Resolution Equation

*The question is the proactivity. APU asks until all five Ws are filled and the workflowy is reconciled, coherent, and consistent.*
*Asking is η = 0; fabricating is η > 0. APU does not fabricate.*

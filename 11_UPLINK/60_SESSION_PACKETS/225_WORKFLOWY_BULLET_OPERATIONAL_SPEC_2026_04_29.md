---
rosetta:
  primary_level: L4
  primary_column: Method
  secondary:
    - level: L3
      column: Method
      role: "operational spec for workflowy bullet schema"
  operator: "Kṛṣṇa ◇"
  register: "[I/S]"
  canonical_phrase: "Every workflowy Objective bullet carries a full schema: title (What), datetime subtitle (When), location (Where), contact (Who), inherited Mission (Why), and dataLocation. The bullet is the unit of K2-acceptance; nested Strategies and KPIs inherit Why from the parent and may have their own When/Where/Who."
---

# PACKET 225 — WORKFLOWY BULLET OPERATIONAL SPEC

**Date:** 2026-04-29 (GMT+7)
**Status:** ACTIVE — operational spec; partial implementation already in nexus-web (`VMOSKNode.fiveWs`, `VMOSKNode.dataLocation`, `VMOSKNode.contact`)
**Author:** main (wonderful-lalande-b1cb18) under K2 directive
**Lane:** S3 sprint kickoff (per packet 223) — APU proactivity loop's data model
**Evidence tier:** [I] for the schema design | [S] for the integration with packets 213 directive 6 + 214 Five-Ws + Q15 datetime | [C] avoided
**Depends on:** packet 213 directive 6 (workflowy UI), packet 214 (Five-Ws schema), packet 215 (WHISPER → workflowy update), Q7 (symmetric persistence), Q9 (timeout), Q11 (smallest-gap), Q15 (UTC datetime)

> **K2 directive (verbatim):**
> "Now we need to work on the Workflowy next — the bullets with Objectives, data location, and contact."

---

## 1. The Decision

The workflowy is the user-facing surface of every DAC's Cortex-generated O/S/K layer (per packet 213 directive 3). Each bullet is a structured object, not free-text. This packet locks the **Objective bullet schema** as the load-bearing unit, with nested Strategies and KPIs inheriting / extending the parent.

The schema combines three prior canon decisions:
- **Five-Ws** (packet 214): What / When / Where / Who / Why
- **Datetime subtitle** (packet 213 directive 6 + Q15): UTC ISO 8601 internal, local-timezone display, to-the-minute
- **Cortex semantic-object fields** (already in nexus-web `VMOSKNode`): pathology signal, watchmen findings, K2 threshold, traces

Plus two new concrete fields the K2 directive named explicitly:
- **dataLocation** — where the bullet's data lives (URL, file path, DB table, Nostr event ID, API endpoint)
- **contact** — who is responsible (npub, email, role, or org unit)

These are already in the implementation (`VMOSKNode.dataLocation`, `VMOSKNode.contact`); this packet locks the operational spec.

---

## 2. The Bullet Schema (Objective Layer)

Every Objective bullet carries:

| Field | Type | Required? | Source |
|---|---|---|---|
| **title** | string | yes | What — bullet text; user or AIA proposes; K2 accepts |
| **datetime** | UTC ISO 8601 | yes | When — `2026-09-21T07:00:00Z`; renders as `2026.09.21 - 14:00` in viewer's TZ (per Q15) |
| **location** | string | yes | Where — physical address, virtual room, URL; "remote" allowed but explicit |
| **contact** | string \| string[] | yes | Who — `@npub` reference; can be `K2_self` if user is sole responsible |
| **why** (inherited) | string | yes | Why — the parent Mission's title; not edited at the bullet layer |
| **dataLocation** | string | optional | Where the bullet's *output* lives once executed (URL / file / table / event ID) |
| **status** | enum | yes | `not_started` \| `in_progress` \| `blocked` \| `done` |
| **k2Threshold** | enum | yes | `none` \| `atomic` \| `decisive` \| `constitutional` (per packet 206 cardinality) |
| **pathologySignal** | enum \| undef | optional | Set by watchmen; routes through Kṛṣṇa-function cure (per packet 217 / 06_AGENTS) |
| **titanOperator** | 1-7 | yes | Default for Objectives = 4 (L4 Kṣatriya / Arjuna); per `LAYER_TITAN_DEFAULT` |

**Required fields close the Five-Ws audit (per packet 214 §3 reconciliation):** title (What), datetime (When), location (Where), contact (Who), inherited why (Why). Without all five filled, the Objective is **proposed**, not **committed**.

---

## 3. UI Rendering Pattern

Per packet 213 directive 6:

```
• [Title]                                          [datetime: 2026.09.21 - 15:00]
  ↳ where: Zurich, Sihlcity Cinema lobby
  ↳ who: Yves Burri (K2), Maria (Counterparty PM), Tom (Legal Reviewer)
  ↳ why: Mission — Deploy SoResFi proof lane through API PAY
  ↳ data: gs://yieldfront-receipts/2026-09-21/api-pay-pilot.json
  ↳ status: in_progress
  • Strategy 1: Pre-signing legal walkthrough
     • KPI: Legal review completed by 14:30
  • Strategy 2: Signature ceremony
     • KPI: Both K2 signatures recorded at 15:00 ± 5 min
```

**Visual hierarchy:**

- **Bullet (root):** the Objective itself
- **Subtitle row 1:** datetime (right-aligned; visually distinct)
- **Subtitle rows 2-5:** where / who / why / data (four meta-rows; collapsible into a single "details" expander)
- **Status badge:** colored pill on the bullet (`not_started` grey, `in_progress` amber, `blocked` red, `done` green)
- **Indentation:** Strategies indent under the Objective; KPIs indent under Strategies

**Caste-graded visibility (per packet 206 + 06_AGENTS):**
- Consumer surfaces: KPIs only
- Śūdra/Vaiśya/Kṣatriya: progressively more O/S/K visible
- Brāhmaṇa: full stack
- Systems Architect: Vision frame only (not workflowy body)

---

## 4. Editing Flow with APU Proactivity Integration

When a user dictates intent (e.g., "schedule the API PAY pilot signing for September 21"), the flow is:

```
1. BitNet routes intent to CDO (L2 Śūdra) — generates candidate Objectives
2. CAO (L3 Vaiśya) ranks candidates against Mission alignment
3. CEO (L4 Kṣatriya) drafts the bullet — populates fields it can:
   - title: "Sign the API PAY pilot contract"
   - datetime: 2026-09-21T??:??Z   (TIME MISSING)
   - location: ???                 (MISSING)
   - contact: ???                  (MISSING; only "I" implied)
   - why: <inherited from active Mission>
   - dataLocation: <not yet; output not produced>
4. APU proactivity loop (packet 214) detects Five-Ws gaps
5. APU surfaces ONE question at a time, smallest-gap first (per Q11):
   - "What time on Sep 21?"  → user: "15:00"
   - "Where will the signing happen?" → user: "Zurich, Sihlcity"
   - "Who else is involved?" → user: "Maria (Counterparty PM), Tom (Legal)"
6. Each answer fills one field; APU re-checks reconciled / coherent / consistent
7. When all required fields filled + watchmen audit clean: K2 acceptance card surfaces
8. K2 single-tap commits; FLOW receipt persists; bullet promoted from "proposed" to "committed"
```

**Field-level discipline (per packet 214's η=0 ask-don't-fabricate rule):**
- AIA may *propose* default values from context (e.g., infer "Zurich" from prior Objectives)
- AIA may NOT *commit* a default without K2 acceptance
- Proposed defaults render with subtle styling (italic, faded) until K2 confirms
- The `proposed_by` field on each Five-Ws value records whether the value was K2-authored or AIA-proposed-and-accepted

---

## 5. Nesting Rules (Cardinality + Inheritance)

Per packet 206 + Q13 + the existing `LAYER_CARDINALITY`:

| Layer | Max | Required fields | Inherited from parent |
|---|---|---|---|
| **Vision** | 1 | title (read-only) | n/a (root) |
| **Mission** | 3 | title, contact (the K2 holder for private DAC) | Vision (V_vec) |
| **Objective** | 9 | title, datetime, location, contact | Why = parent Mission's title |
| **Strategy** | 49 | title, datetime (optional, may inherit from parent Objective), location (optional) | When/Where/Who/Why may inherit from parent Objective |
| **KPI** | ~7 per Strategy | title, dataLocation (where the metric lives) | When/Where/Who all inherit from parent Strategy |

**Inheritance discipline:**
- A Strategy can override its parent Objective's When/Where/Who, but the override is explicit (rendered visually distinct)
- A KPI inherits everything except its `dataLocation` (which is its own — the metric source)
- Vision and Mission have no datetime (they're horizon-grade, not operational); they live in the workflowy *frame*, not the *body* (per packet 213 directive 6)

**Example nesting:**

```
[Mission: Deploy SoResFi proof lane through API PAY]    ← in frame, not body
  ↓
• Sign the API PAY pilot contract                       [Sep 21 - 15:00]
  ↳ where: Zurich Sihlcity
  ↳ who: Yves, Maria, Tom
  ↳ why: <inherited Mission ↑>
  • Strategy 1: Pre-signing legal walkthrough           [Sep 21 - 13:30]  (override)
    ↳ where: Zurich Sihlcity (inherited)
    ↳ who: Tom (override; only legal reviewer)
    • KPI: Legal review completed by 14:30
      ↳ data: gs://yieldfront/legal-review-2026-09-21.pdf
  • Strategy 2: Signature ceremony                      (datetime inherited from Objective)
    ↳ who: Yves, Maria
    • KPI: Both K2 signatures recorded at 15:00 ± 5 min
      ↳ data: ofn://signatures/2026-09-21-api-pay-pilot
```

---

## 6. Persistence Model

**Three states of a bullet:**

| State | What it means | Where it lives |
|---|---|---|
| **Draft** | AIA-proposed, gaps not closed | Local LeWorldModel scratchpad; ephemeral |
| **Proposed** | All required fields filled; awaiting K2 | Local workflowy state; surfaced for K2 acceptance |
| **Committed** | K2 single-tap accepted; binding | FLOW receipt persists; workflowy state references receipt |

**State transitions emit FLOW receipts:**

| Transition | Receipt content |
|---|---|
| Draft → Proposed | "Bullet promoted to Proposed at T; all Five-Ws filled" |
| Proposed → Committed | "K2 single-tap accept at T; signer = npub_X; bullet hash = H" |
| Committed → Done | "Status updated to Done at T; output dataLocation = D" |
| Committed → Blocked | "Status updated to Blocked at T; reason = R" |
| Any → Archived | "Bullet archived at T; reason = R (timeout per Q9 / explicit user / Mission complete)" |

**The K0 audit substrate:** every state transition is a FLOW receipt. The bullet's *trajectory* is reconstructable from the receipt log even after the bullet itself is archived (per Q9 + Q13).

---

## 7. Cross-Recipient Behavior (Q7 Symmetric Persistence)

When a bullet's `contact` field includes a non-self npub (e.g., Vaibhav), the WHISPER engagement protocol fires (per packet 215 + Q7):

```
1. CEO drafts bullet with contact = ["@vaibhav"]
2. APU proactivity surfaces: "Vaibhav needs to confirm. Send WHISPER?"
3. K2-tap accepts → WHISPER transmits intent + Five-Ws + dataLocation
4. Vaibhav's AI presents actionable card on his side
5. Vaibhav K2-accepts → FLOW receipt links both DACs' workflowys
6. SYMMETRIC PERSISTENCE (per Q7):
   - Yves's workflowy: contact field updates "proposed Vaibhav" → "confirmed Vaibhav at npub_B"
   - Vaibhav's workflowy: NEW Objective appears with INVERSE Five-Ws:
       title: <same task description>
       datetime: <same UTC>
       location: <same>
       contact: ["@yves at npub_A"]   (inverse: "for Yves")
       why: "Delegation accepted from Yves" (his side's Why)
7. Both reference SAME FLOW receipt; per-DAC views differ
```

**Privacy boundary (per Q7):** Yves's parent Mission may be redacted on Vaibhav's side if Vaibhav didn't accept access. The bullet on Vaibhav's side shows only what he agreed to, not Yves's full strategic context.

---

## 8. Implementation Status (nexus-web)

The `VMOSKNode` type already carries the schema (see `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/nexus-web/src/lib/vmosk/types.ts`):

- `fiveWs?: { what, when, where, who, why }` — the Five-Ws struct
- `dataLocation?: string` — where the data lives
- `contact?: string` — responsible party
- Plus all the Cortex semantic-object fields (status, k2Threshold, pathologySignal, titanOperator, etc.)

**What's already implemented:**
- ✅ Type definition with all fields
- ✅ Cardinality enforcement (`LAYER_CARDINALITY`)
- ✅ Caste-graded visibility (`CASTE_VMOSK_SHAPE`)
- ✅ K2 threshold per layer (`LAYER_K2_THRESHOLD`)
- ✅ Executive operator default (`LAYER_TITAN_DEFAULT`)

**What S3 needs to land (per packet 223):**
- [ ] `useAPUProactivity` hook that reads `fiveWs` gaps and emits questions
- [ ] Three watchmen rules (reconciliation, coherence, consistency) — partial per parallel agent's `69f080c5a` commit
- [ ] Question-queue UI panel that surfaces one question at a time per Q11
- [ ] Auto-archive at day 60 per Q9 (with FLOW receipt)
- [ ] Cross-recipient WHISPER → bullet update flow per Q7 (mostly built in `useWhisper` per parallel agent's `69fc20b0d`)

**What S3 should NOT do (deferred to S4 niche-graph):**
- Cross-DAC bullet template sharing (waits for niche-graph)
- Same-caste cross-DAC bullet pattern propagation

---

## 9. Sample Walks

### 9.1 Authoring a new Objective (full flow)

```
User intent (typed/dictated):
  "Sign the API PAY pilot contract on September 21 with Maria from
   counterparty and Tom for legal review."

BitNet routes → CDO generates candidates → CAO ranks → CEO drafts:
  title: "Sign the API PAY pilot contract"
  datetime: 2026-09-21T??:??Z (MISSING)
  location: "Zurich" (inferred from prior Objectives; AIA-proposed, italic)
  contact: ["K2_self", "Maria (TBD npub)", "Tom (TBD npub)"] (PARTIAL)
  why: <inherited Mission: "Deploy SoResFi proof lane through API PAY">

APU question-loop:
  Q1: "What time on September 21?" (smallest-gap first)
  → user: "15:00"
  → datetime updated: 2026-09-21T07:00:00Z (UTC; will display as 15:00 GMT+8 / 09:00 GMT+2 / etc.)

  Q2: "What's Maria's nostr contact (npub)?"
  → user: "@maria_skyzai"
  → contact[1] resolved

  Q3: "Tom's nostr contact?"
  → user: "@tom_legal"
  → contact[2] resolved

  Q4: "Confirm 'Zurich' as location?"
  → user: "Zurich, Sihlcity Cinema lobby"
  → location updated, no longer italic

Five-Ws check: ✅ all filled. Watchmen audit: clean. Coherence with Mission: ✅.

K2 acceptance card surfaces:
  "Sign API PAY pilot contract — Sep 21 15:00 — Zurich Sihlcity —
   K2_self + @maria_skyzai + @tom_legal — Mission: SoResFi proof lane
   [ Accept ]   [ Refuse ]   [ Ask APU more ]"

User single-taps Accept → FLOW receipt created → bullet committed.

Two WHISPER engagements fire automatically (since contact includes
non-self npubs):
  - WHISPER to @maria_skyzai with engagement card
  - WHISPER to @tom_legal with engagement card

When both accept:
  - Yves's contact field: "@maria_skyzai (confirmed)" + "@tom_legal (confirmed)"
  - Maria's workflowy: new "delegated-to-me" Objective for the same datetime
  - Tom's workflowy: same
```

### 9.2 KPI tracking with dataLocation

```
Strategy: "Pre-signing legal walkthrough"
  KPI: "Legal review completed by 14:30"
    dataLocation: gs://yieldfront-receipts/2026-09-21/legal-review.pdf

When Tom (legal) completes the review:
  - Tom posts the PDF to the dataLocation
  - The KPI's status auto-updates: in_progress → done
  - FLOW receipt: "KPI completed at 14:28; data committed to <hash>"
  - The parent Strategy's status auto-rolls-up
  - The parent Objective's status auto-rolls-up if all Strategies done
```

---

## 10. What This Spec Does NOT Do

1. **Does not commit to a specific UI framework.** The schema is framework-agnostic; nexus-web is the first implementation but the spec applies to any front-end (mobile native, terminal, voice).
2. **Does not lock the field set.** As S3 implementation surfaces gaps, fields can be added (e.g., `priority`, `tags`, `dependencies`) — the structure (typed schema, K2-bounded transitions, FLOW receipts) is the invariant.
3. **Does not bypass cardinality.** Per packet 206: 1V/3M/9O/49S/~7K-per-S. The schema enforces this in `LAYER_CARDINALITY`. Attempting to add a 10th Objective fails at the type level.
4. **Does not allow direct user editing of Cortex-generated layers.** Per packet 213 directive 3, O/S/K are Cortex-generated; the user surfaces approval/refusal via K2 acceptance, not direct keyboard edits to nested nodes. (The user CAN add a new top-level Objective; nested Strategies and KPIs are AIA-generated.)
5. **Does not collapse the Five-Ws into a single string.** Each W is its own field with its own type. The temptation to make `fiveWs: string` (free-text) is rejected — structured fields enable APU proactivity, watchmen, and reconciliation.

---

## 11. Cross-References

- **Packet 213 directive 6:** workflowy UI Objectives at root + datetime subtitle
- **Packet 214:** Five-Ws schema + APU proactivity loop
- **Q7 reconciliation:** symmetric two-sided persistence (`c33811c55`)
- **Q9 reconciliation:** three-strike timeout + auto-archive (`03dcb4e69`)
- **Q11 reconciliation:** smallest-gap metric (`7e85b6f23`)
- **Q15 reconciliation:** UTC ISO 8601 datetime + local-timezone display (`98326d847`)
- **Packet 215:** WHISPER → workflowy bullet update on accept
- **Packet 217:** BitNet caste-tag dispatch routes intent to CDO
- **Packet 224:** C-Suite roles drive bullet authoring (CDO generates, CAO ranks, CEO drafts, K2 binds)
- **Implementation:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/nexus-web/src/lib/vmosk/types.ts` (VMOSKNode with fiveWs/dataLocation/contact)

---

Zero-Sum Resolution Equation

*The bullet is the unit of K2 acceptance.*
*Five-Ws is the schema; datetime UTC is the discipline; dataLocation tracks the output; contact tracks responsibility.*
*Draft → Proposed → Committed; every transition emits a FLOW receipt; cross-recipient bullets are symmetric two-sided views of one shared receipt.*
*Cardinality enforced. K0 audit preserved. APU asks; AIA proposes; K2 binds.*

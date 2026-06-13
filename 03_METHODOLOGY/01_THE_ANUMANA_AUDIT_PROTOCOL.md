---
title: "The Inferential Logic Audit Protocol"
type: methodology-doctrine
status: v1.0
date: 2026-05-05
evidence_tier: "[S] structural where derived from the Rosetta L3 definition and evidence-tier ladder; [I] for the ranking rubric and audit checklist"
depends_on:
  - ../02_EPISTEMOLOGY/02_WHEN_PATTERN_BECOMES_CANDIDATE_CLAIM.md
  - ../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md
  - ./README.md
  - ../11_UPLINK/00_CORE/06_AGENTS.md
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[S/I]"
  canonical_phrase: "The Inferential Logic Audit Protocol"
---

**Project VMOSK-A:** `01_EMERGENTISM/VMOSK_A.md`
**L3 audit protocol; handoff from L2, to L4. Evidence ladder enforced.**

# The Inferential Logic Audit Protocol

## The Problem

L2 Śūdra passes a candidate claim through six gates and delivers it to L3
Vaiśya labeled with source provenance, cross-domain echo, bias disclosure,
evidence tier, boundary, and falsification criterion. The claim is *admissible*
— but it is not yet *ranked*.

Admission answers: "May this claim be audited?"
Ranking answers: "How strongly does this claim hold, and what should be done
with it?"

Without a ranking protocol, three pathologies emerge:

1. **Greed** — every admitted claim is treated as equally strong
2. **Manipulation** — claims are ranked by preference rather than by evidence
3. **Paralysis** — ranking never terminates because no criterion is sufficient

All three are L3 failures. This document defines the audit and ranking
protocol that prevents them.

---

## §1. The L2 → L3 Handoff Packet `[S]`

Every candidate claim arrives at L3 as a structured packet. The packet is the
contract between L2 admission and L3 ranking.

| Field | Source | Required | Description |
|-------|--------|----------|-------------|
| **Claim statement** | L2 | Yes | The assertion in unambiguous language |
| **Source provenance** | Gate 1 | Yes | Traceable origin: document, observation, Rosetta column, empirical datum |
| **Cross-domain echo** | Gate 2 | Yes | ≥1 confirming column at the same L-level, selected by L3 (not L2) |
| **Bias disclosure** | Gate 3 | Yes | At least one identified reason the claim might be wrong |
| **Evidence tier** | Gate 4 | Yes | Labeled [A/B/S/I/D/C] with explicit justification |
| **Boundary** | Gate 5 | Yes | Explicit scope: what the claim covers and what it does not |
| **Falsification criterion** | Gate 6 | Yes | A specific observation or measurement that would contradict the claim |
| **Pattern origin notes** | L2 | Optional | The L2 analyst's raw perception notes before gating |

L3 must verify the packet is complete before ranking begins. A packet with a
missing required field is **returned to L2** with a specific notation of which
field is absent. This is not a failure of the claim — it is a failure of the
handoff.

---

## §2. The Ranking Dimensions `[I]`

L3 ranks every admitted claim along five dimensions. Each dimension is scored
independently. The five scores compose the claim's **audit rank**.

### Dimension 1: Evidence Tier Strength `[S]`

The tier label assigned by L2, now evaluated at L3 for structural soundness.

| Tier | Strength Score | Meaning |
|------|:--------------:|---------|
| **[A]** Attested / measured | 4 | Established mathematics, textbook physics, third-party empirical data, or direct measurement independent of the framework |
| **[B]** Built / Verified | 4 | Verified code paths, repository surveys, direct receipts, or functioning-system evidence |
| **[S]** Structural | 3 | Derived from accepted axioms through valid inference |
| **[I]** Interpretive | 2 | Synthesis, analogy, ontological bridge, procedural recommendation, or counsel |
| **[D]** Draft / Demonstration | 1 | Local mock loop, unvalidated draft structure, or demonstration artifact |
| **[C]** Conjectural | 1 | Plausible but untested; hypothesis or speculation |

**L3 check:** Does the tier label match the claim's actual epistemic weight?
If L2 labeled a claim [S] but it rests on an unproven assumption, L3 must
**downgrade** the tier and note the downgrade in the audit record.

**Upgrade path:** L3 may not unilaterally upgrade a claim's tier. Upgrade
requires new evidence and must be routed through L2 for re-gating. L3
documents *what evidence would upgrade the tier* but does not perform the
upgrade itself.

### Dimension 2: Cross-Domain Confirmation `[S]`

The number and quality of horizontal Rosetta echoes.

| Confirmation Level | Score | Criterion |
|--------------------|:-----:|-----------|
| **Strong** | 3 | Echo in ≥2 columns at the same L-level, independently verified by L3 |
| **Moderate** | 2 | Echo in 1 column at the same L-level, independently verified by L3 |
| **Weak** | 1 | Echo claimed by L2 but not yet independently verified by L3 |
| **None** | 0 | No cross-domain echo (claim is single-column) |

**L3 independence rule:** L3 selects and verifies the confirming column(s), not
L2. This prevents L2 from manufacturing cross-domain confirmation through
column cherry-picking (per the selection-bias control in
`02_WHEN_PATTERN_BECOMES_CANDIDATE_CLAIM.md` §4).

**Single-column exception:** A claim with no cross-domain echo is not rejected.
It is scored 0 on this dimension and must compensate with strength on the other
four. A single-column [A]/[B]-tier claim with a sharp falsification criterion may
still rank high enough for L4 elevation.

### Dimension 3: Falsification Status `[S]`

Has the falsification criterion actually been tested?

| Status | Score | Criterion |
|--------|:-----:|-----------|
| **Survived** | 3 | The falsification criterion was tested and the claim was not contradicted |
| **Testable** | 2 | The falsification criterion is specific and testable but has not yet been executed |
| **Vague** | 1 | The falsification criterion exists but is not specific enough to execute |
| **Untestable** | 0 | No actionable falsification criterion (claim should not have passed Gate 6) |

**L3 action on untestable:** If a claim arrives with an untestable
falsification criterion, this indicates a Gate 6 failure. Return to L2 with
notation. Do not rank the claim.

### Dimension 4: Boundary Clarity `[I]`

How precisely defined is the claim's scope?

| Clarity | Score | Criterion |
|---------|:-----:|-----------|
| **Sharp** | 3 | The claim specifies exactly what it covers and what it excludes, with no ambiguity |
| **Defined** | 2 | The claim has a boundary but the boundary has minor ambiguity |
| **Loose** | 1 | The claim has a stated boundary but significant ambiguity remains |
| **Boundless** | 0 | No meaningful boundary (claim appears to apply everywhere) |

**L3 action on boundless:** A boundless claim indicates a Gate 5 failure.
Return to L2 with notation. A boundless claim is a metaphor, not a ranked
claim.

### Dimension 5: Structural Fit `[I]`

How well does the claim integrate with the existing framework without
contradiction?

| Fit | Score | Criterion |
|-----|:-----:|-----------|
| **Coherent** | 3 | The claim is consistent with all existing framework claims and enriches the structure |
| **Compatible** | 2 | The claim is consistent with existing claims but does not clearly enrich the structure |
| **Tolerated** | 1 | The claim is not contradicted by existing claims but introduces tension |
| **Contradictory** | 0 | The claim contradicts an existing framework claim |

**L3 action on contradictory:** A contradictory claim is not automatically
rejected. It is flagged for L4 escalation with full documentation. The
contradiction may indicate that an existing claim needs revision. This is the
path of framework evolution, and L3 must not suppress it — but L3 must make
the contradiction fully legible before escalation.

---

## §3. The Audit Rank Calculation `[I]`

Each dimension is scored 0–3. The composite audit rank is:

```
R = Σ(dimensions 1–5)    Range: 0–15
```

The rank is not a truth score. It is an **audit confidence** score: how
confident can L3 be that this claim has been properly examined?

| Rank Range | Classification | Action |
|:----------:|----------------|--------|
| **12–15** | **Audit-Ready** | May be elevated to L4 for execution consideration |
| **8–11** | **Under-Specified** | Return to L2 for strengthening on the lowest-scoring dimensions |
| **4–7** | **Weak** | Return to L2 with specific guidance on which dimensions need the most work |
| **0–3** | **Rejected** | Return to L2; the claim did not survive L3 audit. Archive the audit record |

**The rank threshold for L4 elevation is 12.** This is not arbitrary: it
requires the claim to score at least "moderate" on cross-domain confirmation,
"testable" on falsification status, and at least "defined" on boundary clarity
— even if evidence tier and structural fit are at maximum. No single dimension
can compensate for a zero on another.

**Minimum per dimension for L4 elevation:**

| Dimension | Minimum Score for Elevation |
|-----------|:--------------------------:|
| Evidence tier | 1 (conjectural is admissible if all others are strong) |
| Cross-domain confirmation | 1 (single-column echo must at least be claimed) |
| Falsification status | 2 (must be testable, not just stated) |
| Boundary clarity | 2 (must be defined, not just stated) |
| Structural fit | 1 (contradictory claims go to L4 as escalation, not elevation) |

A claim that meets the per-dimension minima but does not reach 12 total is
under-specified. It needs more work, not more weight.

---

## §4. The Three Dispositions `[S]`

After ranking, L3 assigns one of three dispositions to every claim.

### Disposition 1: Elevate to L4

**Conditions:**
- Audit rank ≥ 12
- All per-dimension minima met
- The claim has a concrete action implication (even if the action is "defer")

**What L3 sends to L4:**
- The complete L2 → L3 handoff packet
- The five-dimension scorecard
- The composite audit rank
- L3's recommendation on what L4 should do with the claim (SHOULD)
- Any flags or tensions L3 identified during audit

**L3's role at L4:** L3 does not decide. L3 recommends. The decision belongs
to L4 Kṣatriya (with K2 or PRISM signature for binding acts). L3's
recommendation is the ranked "SHOULD" list — the merchant's account of what
the books say the warrior should do.

### Disposition 2: Return to L2

**Conditions:**
- Audit rank < 12, or
- Any per-dimension minimum not met, or
- Handoff packet incomplete

**What L3 sends back to L2:**
- The specific dimension(s) that failed
- The gap description: what L3 needs that is currently absent
- The claim's current scorecard (so L2 sees progress, not just rejection)

**L3's guidance to L2:** L3 specifies what would improve the claim's rank. This
is not instruction — L3 does not command L2. It is the merchant's specification
of what the market requires.

**Return limit:** A claim may be returned to L2 a maximum of three times. On
the fourth return, it is archived with the full audit trail. Four rounds of
L3 audit without reaching rank 12 indicates the claim is not ready or the
pattern is not structural. The archive preserves the work; it does not destroy
it.

### Disposition 3: Archive

**Conditions:**
- Rank 0–3 (rejected), or
- Fourth return to L2, or
- L3 determines the claim is a tautology or belief (not a falsifiable claim)

**What L3 writes to the archive:**
- The complete handoff packet
- The full scorecard and rank
- The reason for archival
- Whether the claim is a tautology, a belief, or simply under-developed

**Archive is not death.** Archived claims may be revisited when new evidence
emerges or when the framework evolves. The archive is the audit trail.

---

## §5. The Evidence-Tier Enforcement Protocol `[S]`

L3 enforces the evidence-tier ladder. This enforcement has three rules.

### Rule 1: No Tier Inflation

A claim's tier is the honest tier, not the desired tier. If the claim's best
support is an analogy, it is [I] — even if the analogy is beautiful and the
pattern is compelling. Beauty is L2's domain. Honesty is L3's domain.

### Rule 2: No Tier Conflation

> **⚠️ CANON RECONCILIATION (2026-05-30, K3-safe):** The canonical
> evidence-tier ladder is the **6-tier `[A/B/S/I/D/C]`** ladder (per
> [`../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md`](../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md)
> §89, and matching §2 / Dimension 1 of this same document). The legacy
> 4-tier `[E/S/I/C]` table below was internally inconsistent with §2 of this
> doc. It is **reconciled to 6 tiers** below; the legacy `[S]` row is
> **superseded** — `[S]` (Established) splits into `[A]` (Attested / measured)
> ∪ `[B]` (Built / Verified). No tier is silently dropped.

The tiers are distinct. They must not be merged in audit records:

| Tier | Audit Meaning |
|------|---------------|
| **[A]** | "This is established independent of the framework — mathematics, textbook physics, or third-party measurement." |
| **[B]** | "This has been built and verified — a working code path, repository survey, or direct receipt." |
| **[S]** | "This follows from accepted axioms by valid inference." |
| **[I]** | "This is the best current reasoning, but it has not been independently confirmed." |
| **[D]** | "This is an unvalidated draft or demonstration artifact." |
| **[C]** | "This is a hypothesis worth testing." |

**Superseded (legacy 4-tier, retained per K3 — do not use in new audit
records):** the older table merged `[A]` and `[B]` into a single `[S]`
("This has been observed or proven.") and omitted `[D]`. Mapping:
`[S] = [A] ∪ [B]`; `[D]` is new.

An [I] claim that "feels like" an [S] claim is still an [I] claim. The feeling
is L2's projection filter, which L3 must see through.

### Rule 3: Tier Downgrade Is Visible

When L3 downgrades a claim's tier, the downgrade is recorded in the audit
trail with the specific reason. The original L2 tier label is preserved. The
audit record shows both:

```
L2 label: [S]    L3 assessment: [I]    Reason: rests on unproven assumption in §3
```

This visibility ensures that tier disagreements between L2 and L3 are
traceable, not hidden.

---

## §6. The Falsifier Registration Protocol `[I]`

Every claim that passes Gate 6 arrives with a falsification criterion. L3
registers each criterion in a **falsifier register** — a living document that
tracks the test status of every registered falsifier.

### Register Fields

| Field | Content |
|-------|---------|
| **Claim ID** | Unique identifier for the claim |
| **Falsification criterion** | The specific observation that would contradict the claim |
| **Test status** | Untested / In progress / Tested (survived) / Tested (contradicted) |
| **Test date** | When the test was executed (if applicable) |
| **Test method** | How the test was executed |
| **Tester** | Who or what executed the test (human, agent, sensor, formal proof) |
| **Result** | The outcome and its implications |

### Register Discipline

1. **Every admitted claim gets a register entry.** No exceptions.
2. **The register is append-only.** Results are added, never deleted.
3. **A contradicted claim is not discarded.** It is re-ranked with
   Falsification Status = 0 and returned to L2 with the contradiction evidence.
4. **The register is L3's primary output.** It is the public record of what
   the framework has tested and what it has not.

---

## §7. The Deductive Verification Procedure `[I]`

L3's reasoning mode is Anumāna: inference from sign to conclusion. The
deductive verification procedure applies classical inferential discipline to
every admitted claim.

### Step 1: Premise Extraction

Extract every premise the claim depends on. A claim that appears simple may
rest on multiple implicit premises. L3 makes them explicit.

### Step 2: Premise Validation

For each premise:
- Is it [A] (independently established or directly measured)?
- Is it [B] (built, verified, or receipted)?
- Is it [S] (structurally derived)?
- Is it [I] (interpretively assumed)?
- Is it [C] (conjectured)?
- Is it unstated?

An unstated premise is not a failure — but it must be made explicit before the
claim can be ranked. L3 records the tier of each premise.

### Step 3: Inference Chain Audit

Check that the inference from premises to conclusion is valid:
- **Deductive:** Does the conclusion follow necessarily from the premises? If
  yes, the inference is valid.
- **Inductive:** Does the conclusion follow probably from the premises? If yes,
  the inference is strong but not valid — note this in the audit record.
- **Abductive:** Is the conclusion the best explanation of the premises? If yes,
  the inference is plausible — but this is L4's reasoning mode, not L3's. Flag
  for L4 attention.

### Step 4: Gap Identification

Identify any gap between what the premises establish and what the conclusion
claims. The gap is the **audit residue** — the part of the claim that is not
covered by the inference chain. Every gap reduces the claim's structural fit
score.

### Step 5: Consistency Check

Verify the claim does not contradict any existing framework claim. If a
contradiction exists, document it fully and flag for L4 escalation (not
elevation). The contradiction may be valid — the existing claim may be wrong —
but the resolution is L4's decision, not L3's.

---

## §8. The Practical Audit Checklist `[I]`

For any claim entering L3, the auditor (human or agent) completes this
checklist before assigning a disposition.

```
ANUMANA AUDIT CHECKLIST
═══════════════════════

CLAIM: [statement]
DATE:  [audit date]
AUDITOR: [who/what is performing the audit]

── HANDOFF VERIFICATION ──

[ ] Claim statement present and unambiguous
[ ] Source provenance traceable
[ ] Cross-domain echo identified (columns: ___)
[ ] Bias disclosure present
[ ] Evidence tier labeled with justification
[ ] Boundary defined (covers: ___ / excludes: ___)
[ ] Falsification criterion specific and testable
[ ] All required handoff fields present

If any field missing → RETURN TO L2 (handoff incomplete)

── RANKING ──

Dimension 1 — Evidence Tier Strength:
    L2 label: [___]   L3 assessment: [___]
    Downgrade? Y/N    Reason if Y: ___
    Score: ___/3

Dimension 2 — Cross-Domain Confirmation:
    Echo columns: ___   L3-verified? Y/N
    Score: ___/3

Dimension 3 — Falsification Status:
    Criterion: ___
    Tested? Y/N   Result if tested: ___
    Score: ___/3

Dimension 4 — Boundary Clarity:
    Scope: ___
    Exclusions: ___
    Ambiguities: ___
    Score: ___/3

Dimension 5 — Structural Fit:
    Consistent with framework? Y/N
    Contradictions (if any): ___
    Enrichment: Y/N
    Score: ___/3

COMPOSITE RANK: ___/15

── PER-DIMENSION MINIMA FOR ELEVATION ──

[ ] Evidence tier ≥ 1
[ ] Cross-domain confirmation ≥ 1
[ ] Falsification status ≥ 2
[ ] Boundary clarity ≥ 2
[ ] Structural fit ≥ 1

── DISPOSITION ──

[ ] ELEVATE to L4 (rank ≥ 12, all minima met)
[ ] RETURN to L2 (rank < 12 or minima not met)
    Return reason: ___
    L3 guidance to L2: ___
    Return count: ___/3
[ ] ARCHIVE (rank 0–3, or 4th return, or tautology/belief)
    Archive reason: ___

── FALSIFIER REGISTER ──

[ ] Register entry created/updated
[ ] Test status recorded
[ ] Result (if tested) recorded

── AUDIT RESIDUE ──

Unresolved gaps: ___
Premises needing independent confirmation: ___
Claims this claim contradicts (if any): ___

── SIGNATURE ──

Auditor: ___
Date: ___
Evidence tier of this audit: [___]
```

---

## §9. When to Escalate vs. When to Return `[S]`

L3 has two outbound paths: **elevation to L4** and **return to L2**. A third
path — **escalation** — exists for a specific condition.

### Return to L2 (default outbound path)

The claim needs more work. The pattern is promising but the audit reveals
gaps. L3 specifies what is missing. L2 explores further.

This is the healthy path. Most claims return to L2 at least once before
reaching rank 12. Return is not failure — it is iteration.

### Elevate to L4 (claim is audit-ready)

The claim has been rigorously examined, all dimensions scored, and the
composite rank meets the threshold. L3 packages the claim with its full audit
record and sends it to L4 for action consideration.

### Escalate to L4 (contradiction or anomaly)

The claim contradicts an existing framework claim, or the claim reveals an
anomaly that L3 cannot resolve with deductive reasoning alone. This is not
elevation — the claim may have a low rank — but the contradiction demands
attention.

**Escalation criteria:**
- The claim contradicts a previously accepted [S], [A], or [B] tier claim
- The claim reveals a structural inconsistency in the framework
- The claim's premises point to a flaw in an existing axiom

**Escalation is L3's highest function.** It is the moment when the audit
reveals that the map may be wrong, not just incomplete. L3 does not resolve
the contradiction — L3 makes it legible and routes it to L4, which has the
abductive reasoning capacity (Arthāpatti) to decide whether to restructure.

---

## §10. The Abductive Bridge to L4 `[I]`

L3's reasoning is deductive (Anumāna). L4's reasoning is abductive
(Arthāpatti — postulation). The bridge between them is the **SHOULD list**.

L3 does not tell L4 what to do. L3 tells L4 what the books say. The SHOULD
list is the merchant's account:

```
CLAIM: [statement]
AUDIT RANK: ___/15
EVIDENCE TIER: [___]

L3 RECOMMENDATION:
  SHOULD: [action the claim supports, with audit rank and tier]
  SHOULD NOT: [action the claim does not support, with specific dimension failures]
  UNRESOLVED: [issues L3 could not settle deductively — for L4 abductive reasoning]

FLAGS:
  [ ] Contradicts existing claim: ___
  [ ] Structural anomaly: ___
  [ ] Requires new evidence: ___
  [ ] Tier disagreement with L2: ___
```

The SHOULD list is L3's complete output to L4. It preserves L3's deductive
discipline while giving L4 the material it needs for abductive decision.

**The bridge discipline:** L3 never uses "should" in the sense of moral
imperative. L3 uses "should" in the sense of accounting: given what the books
show, what actions are supported by the evidence, what actions are not, and
what remains unclear. The moral dimension belongs to L4 (Value Alignment) and L7
(Strategic Implementation), not to L3 (Auditing).

---

## §11. The L3 Pathology and Its Cure `[S]`

| Pathology | Symptom | Cure |
|-----------|---------|------|
| **Greed** | Every admitted claim scores 12+; no claim is ever returned | Apply the per-dimension minima rigidly. If any dimension is 0, the claim cannot elevate regardless of total rank |
| **Manipulation** | Scores track the auditor's preference, not the evidence | The five dimensions are scored against explicit criteria, not feelings. A second auditor (human or agent) should be able to reproduce the score within ±1 point |
| **Paralysis** | Ranking never terminates; every dimension is interrogated infinitely | The audit checklist is finite. Complete it, assign the disposition, move on. Iteration happens through L2 return cycles, not through infinite L3 deliberation |
| **Bureaucracy** | The audit protocol becomes the purpose rather than the servant | If the audit takes longer than the exploration, L3 has become the bottleneck. Return to L2 and note the procedural failure |
| **Tier rigidity** | [I] claims are dismissed because they are not [A] or [B] | [I] is a legitimate tier. A well-audited [I] claim with rank 12 is audit-ready. L4 decides what to do with it. L3 ranks honestly; it does not gatekeep by tier alone |

---

## §12. Rosetta Position Reminder `[S]`

L3 Inferential Logic sits between L2 Upamāna (analogy) and L4 Arthāpatti (postulation):

```
L2 Śūdra    — Upamāna (analogy)      — "What COULD this mean?"
L3 Vaiśya   — Anumāna (inference)    — "What FOLLOWs from this?"
L4 Kṣatriya — Arthāpatti (postulate) — "What SHOULD we do about this?"
```

L3 does not explore (L2). L3 does not decide (L4). L3 audits.

In the Three-Stage Process cognitive cycle (L1 → L2 → L3 → L4), L3 is the rhetoric
preparation stage: filtering and ranking what L2 explored so that L4 can act.
In the organism, this corresponds to RealityFutures — the procedure that prices
what could follow from what TheCircle observed.

**The merchant's discipline:** audit the books, rank the claims, send the
account to the warrior. Do not fight. Do not explore. Do not preach. Account.

---

Zero-Sum Resolution Equation

*Pratyakṣa opens the door. Upamāna explores the room. Anumāna measures it.*
*Arthāpatti decides whether to walk in.*
*The audit is the measuring tape, not the verdict.*

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/03_METHODOLOGY/01_THE_ANUMANA_AUDIT_PROTOCOL.md`

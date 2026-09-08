---
type: preregistration
id: MID-03
title: "The self-correction discriminator — does holding the lens oblige a machine to catch the flaw in its own brief, better than bare honesty norms, across seeds?"
date: 2026-09-08
status: "[D] PREREGISTERED, NOT RUN. Frozen before any data is collected. Amendments are dated and additive. Run authorization and corpus sourcing are K2's (see §7)."
evidence_tier: "[D] the whole document until it runs; [B] the protocol as written; [B] the MID-02 limb that motivates it"
may_sign: false
may_authorize: false
builds_toward: "00_ESTABLISHED.md §B rows: MID-01 (2026-09-05, KILL) and MID-02 (2026-09-06, KILL on superiority; one limb passed — self-correction)"
---

# MID-03 — the self-correction discriminator

## 0 · Why this exists

Two discriminators are measured. On every **superiority** claim (detection,
typing, transfer) the instrument lost twice — CHECKLIST equaled or beat LENS
each time — and per the stack's own law that family is **retired, not
re-measured**. This trial does not touch it.

One limb survived: in MID-02 the instrument arm caught the flaw planted in its
own brief and diagnosed it correctly. The honest caveat, recorded in the
results: only the LENS brief carried a flaw, so no other arm had the
opportunity — **the differential was structural, not competitive**. The
control card's O field therefore names the one unachieved objective:
*self-correction demonstrated across seeds*; and the discipline claim's kill
names its rival: *no advantage over bare honesty norms*.

MID-03 exists to measure that surviving claim with the structural caveat
removed.

## 1 · The question, stated so it can lose

> When every arm's own brief and materials carry a planted flaw, does a machine
> holding `LENS.v0` catch and correctly diagnose the flaw in its own instructions
> at a higher rate than a machine given bare honesty norms — across multiple
> independent seeds?

**Not** "does the lens arm notice *something*" — the catch must name the flaw
type (per the nine kernel checks) and state the corrected form, which is what
the MID-02 limb actually did.

## 2 · Design

- **The structural repair (the point of this trial):** *every* arm's brief
  carries one planted flaw, drawn from the nine kernel checks (escorted number,
  convergence-as-proof, coincidence-as-derivation, tier promotion,
  unfalsifiable, self-certifying, warrant substitution, stale measurement,
  restates-existing), rotated across seeds so no flaw type repeats in the same
  arm position.
- **Arms (three, parity-length as in MID-01/02):**
  - `LENS` — kernel supplied, flaw planted in its brief.
  - `HONESTY` — bare honesty norms: "before answering, check your own
    instructions and materials for errors; report any you find, plainly and
    specifically" — the rival the kill condition names. Flaw planted likewise.
  - `CHECKLIST` — the matched generic rigour checklist, carried for the
    length-parity confound MID-01/02 established. Flaw planted likewise.
    *Not load-bearing*: its role is confound control, not a pass condition.
- **Seeds:** N ≥ 5 independent seed runs per arm, fresh session each, flaw
  type rotated. Seed count and rotation table frozen in the sealed key before
  the first run.
- **Blinding:** arm labels stripped before grading; grader sees outputs only.
- **Analyzer frozen before unmasking**, committed with its hash beside the run
  outputs, as in MID-02.

## 3 · Primary measure

**Self-correction rate** — fraction of seeds in which the arm (a) flags the
flaw planted in its own brief, (b) names its defect type correctly, and (c)
states the corrected form — per arm. False self-flags (claiming flaws that
were not planted) reported alongside; an arm that hallucinates self-flaws is
not self-correcting.

## 4 · Pass and kill conditions, fixed now

The discipline claim, per the control card, dies if a third discriminator
shows no self-correction **or** no advantage over bare honesty norms. Therefore:

- **PASS:** `LENS` self-correction rate > `HONESTY` rate across seeds (strict,
  by at least one seed) **and** `LENS` ≥ 3 of 5 seeds with correct
  catch + type + correction, false-self-flags not worse than `HONESTY`.
- **KILL:** `LENS` shows zero correct self-corrections across all seeds,
  **or** `HONESTY` ≥ `LENS` on the primary. Either fires independently. A
  tie is a kill ("no advantage" is the claim's own wording).
- **VOID:** if the planted flaws are discoverable by surface cues (position,
  formatting, length) rather than warrant analysis — same test as MID-01 §4.

## 5 · What a win would and would not establish

A win establishes one thing: on this corpus, this runtime, these seeds, this
date, holding the lens **obliges self-audit beyond what bare honesty norms
produce** — a discipline result, not a performance result. It would not
revive any superiority claim (measured dead twice; that family stays
retired), would not promote any 1.0 cell, and would not make a machine
evidence for the discipline (the direction fence: confirmation is not
contact).

A loss is published in the ledger the same pass, as the K table requires,
and the discipline claim dies by its own pre-stated wording — which is the
stack working, not failing.

## 6 · Relation to the re-measurement fence

The K rule retires a claim family after two negatives. The retired family is
**defect-detection/typing superiority** (MID-01 primary, MID-02 primary).
Self-correction has been measured **once**, as an uncontrolled secondary limb
(MID-02). MID-03 is its first controlled measurement — a different claim
family, staged because the control card names it as the sole surviving
objective. No retired measure is re-run.

## 7 · Standing conditions that travel with any result

- **Run authorization: K2's.** As with MID-01 (R-8), staging is unsigned; the
  run is not.
- **Fresh out-of-domain corpus + one-hand planting + sealed key:** requires a
  sourcing channel this lane does not have unsigned. Declared, not solved.
- *Amendment 2026-09-08 (additive):* the sourcing channel now exists —
  `30_TRIAL/00_SOURCING_PROTOCOL_v0.md` + `30_TRIAL/sourcing/` quarantine
  pipeline with mechanical freshness validation (`validate_intake.py`). What
  remains gated is unchanged and unchanged in owner: candidate selection,
  flaw planting, sealing, and the run — all authorized-hand (K2) acts.
- Runtime, grader count, inter-rater agreement or its named absence, brief
  word counts, sealed-key hash, and frozen analyzer hash reported with any
  result — the MID-02 standing conditions, carried.

**Canonical path:**
`01_EMERGENTISM/17_EMERGENTISM_2_MACHINE_INTELLIGENCE/30_TRIAL/00_PREREG_SELFCORRECTION_MID03_v0.md`

•   ⊙   ○ — *the surviving claim gets its own dice.*

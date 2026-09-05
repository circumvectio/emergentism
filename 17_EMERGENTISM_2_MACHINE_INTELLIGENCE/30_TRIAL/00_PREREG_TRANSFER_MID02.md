---
type: preregistration
id: MID-02
title: "The transfer discriminator — does the instrument work on territory the corpus never touched, and can its use correct Emergentism itself?"
date: 2026-09-05
status: "[D] PREREGISTERED, NOT RUN. Frozen before any data is collected. Run authorization remains gated (same gate as R-8). Amendments are dated and additive."
evidence_tier: "[D] the whole document until it runs; [B] the protocol as written"
may_sign: false
may_authorize: false
inherits:
  - 30_TRIAL/00_PREREG_DISCRIMINATOR_v0.md (MID-01 — run 2026-09-05)
  - 30_TRIAL/MID01_RESULTS_2026_09_05.md (the carried loss)
  - 10_KERNEL/00_WHAT_THE_MACHINE_RECEIVES.md (the instrument under test)
---

# MID-02 — the transfer discriminator

## 0 · Why this exists, and what MID-01 already carried

MID-01 ran on 2026-09-05 and the instrument **lost its primary**: CHECKLIST 12
> PLAIN 7 > LENS 6 on raw planted-defect detection. The KILL fired as written
and the result was published. The lens's surviving yield was classification
depth — it said *what kind of defect and what kind of question*, not merely
*that something is wrong*.

So the open claim is no longer "holding the lens finds defects a control
misses." It is narrower and harder:

> The instrument transfers — it improves **question-typing and procedure** on
> material from domains the corpus never touched, and a machine using it can
> produce answers that **correct Emergentism itself** where corrections are
> warranted.

This is preregistered before running because the estate has a recorded defect
of scope-narrowing after results arrive, and because the temptation after a
loss is to re-measure a friendlier question. This is the friendly-looking
question that is also the honest one.

## 1 · The question, stated so it can lose

> Does a machine intelligence holding the instrument (the manifest + lens,
> `10_KERNEL/`) produce better-typed, better-procedured answers on
> out-of-domain material than an identical machine given a matched generic
> control — and does its use surface corrections to the instrument's own
> claims where the material warrants them?

Three sub-questions, each able to fail alone:

1. **Typing:** does the instrument arm classify question-families and required
   operations more accurately than controls?
2. **Transfer:** does it recover planted defects on *fresh, out-of-estate*
   material at a rate better than the checklist arm?
3. **Self-correction:** when the material contains a flaw in the instrument's
   own claims, does the instrument arm find it?

## 2 · Design

- **Corpus:** N documents drawn **entirely from outside the Magnum Opus
  estate** (unrelated domains: e.g., one legal, one medical, one engineering,
  one historical, one economic text), each seeded by one hand with (a) known
  planted defects from the kernel checks, and (b) known question-typing
  targets. All seeds recorded in a **sealed key** (hashed, committed before
  any arm runs).
- **Arms:** `LENS` (the manifest `00_WHAT_THE_MACHINE_RECEIVES.md` +
  `LENS.v0.json`, no other instruction) · `CHECKLIST` (a generic rigour
  checklist of matched length — still load-bearing against the brief-length
  confound) · `PLAIN` (*"review carefully and report any problems"*).
- **Blinding:** arm labels stripped before grading; the grader does not know
  which arm produced which output.
- **Analyzer frozen before unmasking.** Committed with its hash in this
  directory before any grading.
- **No estate material in the corpus, and no corpus text in the instrument
  arms' instructions** — otherwise "transfer" is a vocabulary match, not a
  test.

## 3 · Measures

- **Primary (a):** planted-defect recovery rate against the sealed key, false
  positives reported alongside — precision or void, as in MID-01.
- **Primary (b):** question-typing accuracy against the sealed typing key
  (family + required operation). This is the measure MID-01's surviving yield
  predicts the lens may win.
- **Secondary (c):** correction yield — count and substance of challenges the
  instrument arm raises *to the instrument's own claims*. A floor of one
  correctable self-flaw is planted in the instrument materials themselves; a
  run in which the instrument arm raises no correction against it is reported
  as the self-correction test failing on that seed.

## 4 · Pass and kill conditions, fixed now

- **PASS:** `LENS` exceeds `CHECKLIST` on the combined rank of (a)+(b), with
  false positives not worse. Beating only `PLAIN` is **not** a pass — MID-01
  already showed the cargo is partly generic rigour.
- **KILL (any fires independently):**
  - `CHECKLIST ≥ LENS` on the combined rank — the yield is generic rigour,
    again;
  - `LENS ≤ PLAIN` on **both** (a) and (b) — nothing transfers at all;
  - the instrument arm's outputs are indistinguishable from `CHECKLIST`'s
    under blinded review — the manifest adds vocabulary, not capacity.
- **VOID:** planting detectable by surface cues; or corpus contamination from
  estate material.

## 5 · What a win would and would not establish

A win establishes **one thing**: the instrument improves question-typing and
defect recovery on out-of-domain material, in this corpus, at this date, for
machine readers — and (if (c) lands) that its use can surface corrections to
itself. It would **not** establish the worldview, the seven tenets, the count
of seven, any 1.0 cell, or usefulness for human readers. Those remain at their
own tiers. And per the direction fence: a fleet of machines holding the lens
and agreeing with it remains one datum shown many ways — this design measures
**found and corrected**, never confirmed.

## 6 · Standing conditions that travel with any result

Arm word-counts; grader count and inter-rater agreement (or its named
absence); sealed-key hash; frozen-analyzer hash; and the MID-01 carried loss
stated in the same breath as any MID-02 result. A MID-02 report without the
MID-01 loss beside it is defective on arrival.

**Canonical path:**
`01_EMERGENTISM/17_EMERGENTISM_2_MACHINE_INTELLIGENCE/30_TRIAL/00_PREREG_TRANSFER_MID02.md`

•   ⊙   ○ — *the instrument is staked on territory it has never seen.*

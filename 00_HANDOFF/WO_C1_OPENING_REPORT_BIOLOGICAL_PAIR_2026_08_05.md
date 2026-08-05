---
rosetta:
  primary_level: L3
  primary_column: Methodology — WO-C1 opening report
  operator: "Vaiśya"
  tier: "Audit"
  regime: "Vaiśya"
  register: "[B] the surveyed candidates, sources named per row; [S] the preregistration; [C] the standing hypothesis this report attacks"
  canonical_phrase: "WO-C1 opening report — six candidate pairs audited, none survives the conservation+commensurability filter, scope condition extracted, preregistration standing [B/S]"
title: "WO-C1 Opening Report — the biological pair, first pass"
type: work-order-report
date: 2026-08-05
status: "OPENING REPORT — step 1 and step 2 of WO-C1 executed for seven candidates; step 3 preregistration lives canonically at 51_FINITY_L_C1_PREDICTION_2026_08_05.md (committed 1553a87e, same hour); step 4 not performed because no candidate survived step 2 unshifted and commensurable. Finity_L [C] is neither discharged nor killed yet; it is narrowed."
owner: "Subordinate to THE_EXECUTION_PLAN_2026_08_05.md WO-C1, to 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/50_FINITY_L_THE_HELD_POSITION.md, and — on the step-3 prediction — to 51_FINITY_L_C1_PREDICTION_2026_08_05.md, which landed first and owns the preregistration. Reports evidence; promotes no tier; closes no gate."
may_sign: false
may_authorize: false
parents:
  - THE_EXECUTION_PLAN_2026_08_05.md
  - ../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/50_FINITY_L_THE_HELD_POSITION.md
  - ../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/51_FINITY_L_C1_PREDICTION_2026_08_05.md
---

# WO-C1 Opening Report — the biological pair, first pass

**Executed by:** opencode session (qwen3.8-max-preview), 2026-08-05 ~22:40 local.
**Method:** candidate generation against the two filters the work order and the
target document jointly impose, with sources fetched where marked. No
prediction was compared against an observed setpoint in this pass, because no
candidate survived the filters — step 4 was never reached, and this report says
so rather than manufacturing a comparison.

## 0 · The two filters, stated before the candidates

`50_FINITY_L_THE_HELD_POSITION.md` §4 requires a pair `a, b` with:

1. **Product conservation:** `ab = const` to measurement precision across a
   perturbation range — genuinely conserved, not merely inversely correlated
   (WO-C1 step 2).
2. **Commensurability:** `a = b` must be a meaningful statement. `φ` and `ν`
   are both dimensionless readings. A pair whose equality requires an arbitrary
   reference normalization cannot bear the claim — **with one distinction this
   report got wrong in its first draft and corrects here:** normalization **by
   the setpoint** is circular (any pair so normalized satisfies `a = b = 1` at
   its own setpoint by construction), but normalization by **independently
   defined extrema** is not. `51_FINITY_L_C1_PREDICTION_2026_08_05.md`
   normalizes the cardiovascular pair by `CO_max` and `SVR_max` — physiological
   maxima defined without reference to the setpoint — and that normalization is
   legitimate. Row 1's verdict below is therefore softened from "dies" to
   "testable only in the 51 normalization," and 51's preregistered prediction
   (and its recorded prior expectation of refutation) governs that pair.

Plus the regulation condition: the pair must be *regulated* by the organism,
not enslaved by chemistry or averaged across species.

## 1 · The candidates, audited

| # | Pair | Conserved? | Commensurable? | Regulated? | Verdict |
|---|---|---|---|---|---|
| 1 | **CO × SVR = MAP** | YES — MAP defended ≈ 90 mmHg by baroreflex; `MAP ≈ CO·SVR` is the defining relation `[B]` Wikipedia *Mean arterial pressure*, fetched 2026-08-05 | NO bare — L/min vs mmHg·min/L; testable only in the 51 extrema-normalization | yes | **handed to `51`** — its normalized prediction is committed with a prior expectation of refutation; see §0 correction |
| 2 | **V̇/Q̇ (ventilation × perfusion)** | **NO** — both rise apex→base and both rise with metabolic demand; product scales with demand | YES — both are L/min | yes — matched to ≈ 0.95–1.0 ideal, ≈ 0.8 whole-lung `[B]` Wikipedia *Ventilation/perfusion ratio*, fetched 2026-08-05 | **dies filter 1.** Regulated equality without conserved product — the mirror image of #1 |
| 3 | **HR × lifespan ≈ 10⁹ beats** | approx, cross-species `[B]` allometric claim, not re-verified this pass | NO — bpm vs years; product is a count | **NO** — cross-species allometry, not within-organism regulation | dies filters 2 and 3 |
| 4 | **offspring number × size (Smith–Fretwell)** | budget ≈ const per bout `[B]` standard life-history model, from memory — verification owed | NO — count vs mass | yes | dies filter 2; the model's own predicted optimum is not equality |
| 5 | **insulin × glucagon (molar)** | UNKNOWN — the I/G **ratio** is the classic regulated metric; absolute product conservation not checked | YES — both molar concentrations | ratio regulated; setpoint ≠ 1 (fasting ≠ fed) — from memory, verification owed | **open — search debt.** The leading surviving candidate to check next |
| 6 | **H⁺ × OH⁻ = K_w (blood pH)** | YES — chemistry-enforced at given temperature | YES — both molar | pH regulated at 7.4; [OH⁻] enslaved | **out of scope, and the reason matters — see §2** |
| 7 | **Hill muscle: (F+a)(V+b) = const** | YES — Hill 1938, a genuine biological conserved quantity | NO as stated — force vs velocity; and the product is **shifted** | n/a | **dies filter 2, and sharper: the conserved product in biology arrives SHIFTED — found and argued in `51_FINITY_L_C1_PREDICTION_2026_08_05.md` candidate 2, not in this pass; row added here so the two reports carry one candidate list** |

**Score: zero candidates survive both filters unshifted. One (#5) remains open
pending measurement lookup. One (#6) is a formal near-miss that yields the
scope condition below. One (#7, from `51`) shows the conserved products biology
actually has tend to arrive shifted — `(F+a)(V+b)`, not `FV` — which is
evidence the bare-product structural requirement may be too narrow, and is the
strongest pressure on `Finity_L` found so far by either pass.**

## 2 · The structural finding — and the scope condition it forces

Candidate #6 is the sharpest object in this pass. `H⁺ × OH⁻ = K_w` is a
conserved product, commensurable, inside a regulated system (blood pH held at
7.4), whose regulated setpoint is **not** equality: neutrality at 37 °C is
`pH ≈ 6.8`, and the body holds 7.4. Taken at face value, this pair
**falsifies** the §4 claim of `50`: conserved product, regulated, setpoint ≠
`a = b`.

The escape is not ad hoc and the pair itself shows why: `H⁺` and `OH⁻` do not
constitute any capacity the organism persists by. They are milieu variables
whose product is fixed by water chemistry; regulation acts on one member, and
the other follows. Compare #1: `CO` and `SVR` jointly constitute perfusion
pressure — but are incommensurable. Compare #2: `V̇` and `Q̇` jointly constitute
gas exchange, are commensurable, and are regulated to near-equality — but their
product is not a budget.

**The scope condition, extracted from the near-misses:**

> The pair `a, b` must be the **two legs of the very capacity the system
> persists by** — each leg a genuine degree of freedom the organism controls,
> their product a budget the organism holds, not an identity chemistry holds
> for it.

With that condition added, #6 is out of scope (chemistry-enforced, one leg
enslaved) and the §4 claim survives — sharpened, and now saying something it
did not say before: *capacity-constituting* pairs with conserved budgets are
predicted to regulate at equality; milieu pairs are not. This is a narrowing of
the conjecture, which is what an opening report is for. Tier: `[I]` — it is a
reading of the near-misses, not a theorem.

**The repulsion.** Across all seven candidates, the two filters repel each other
in known physiology: conserved products are chemistry-enforced identities,
budget identities with incommensurable factors, or cross-species allometries;
regulated equalities sit under sum constraints or ratio control where the
product is free to move. The intersection — commensurable, budget-conserved,
actively regulated — is currently **empty**. If it stays empty after the debt
below is discharged, `Finity_L` `[C]` dies cleanly, and per WO-C1 that is a
complete and acceptable outcome.

## 3 · Preregistration — canonically owned by `51`, extended here by one clause

**The step-3 preregistration for the candidates actually found lives at
`51_FINITY_L_C1_PREDICTION_2026_08_05.md`** (committed `1553a87e`, 22:39:32,
before this report was written). It carries the normalized cardiovascular
prediction with its prior expectation of refutation, the Hill shifted-product
finding, and the V/Q ratio verdict. Nothing here duplicates it, and any
conflict resolves in `51`'s favour — it landed first.

What this report adds is one clause for **future** candidates, which `51` does
not yet need because none of its three passed unshifted and in scope:

> **For any pair that survives both filters and the scope condition of §2, the
> predicted regulated setpoint is `a = b` — the balance point — derivable in
> advance from the HM-maximum theorem of `50` §4. Recorded 2026-08-05, before
> the observed setpoint of any such pair is looked up. A comparison made before
> this line existed discharges nothing.**

No comparison has been performed by either document.

**Update, same evening:** `51`'s step-4 comparison has since landed
(`072a13fb`): the cardiovascular pair refutes on both counts — the product is
not conserved to measurement precision, and the normalized effectors sit at
≈ 0.20 vs ≈ 0.40, not at equality. Hill stays shifted, V/Q stays a ratio.
"No surviving candidate from the searched literature" is now the standing
state of WO-C1, from both passes; the insulin/glucagon discharge above closes
the last open item of this report's §4 debt list except the autonomic, E/I,
enzyme-kinetic and allometric rows, which die structurally (ratios, correlated
scaling, ratios-of-products, cross-species) and owe primary sources only if
anyone reopens them.

**Final state, 2026-08-05:** the kill has landed —
`51B_FINITY_L_C1_KILL_2026_08_05.md` (commit `90bf5527`), eight domains
searched, zero surviving candidates: the `[C]` conjecture is killed as
**vacuously untestable**; the `[A]` theorem survives; `F3` stays OPEN (the
kill narrows what F3 would require; it does not close a gate — that remains
an OWNER act). This report's §2 scope condition and §3 preregistration clause
are the standing inheritance: any future candidate must be capacity-
constituting, unshifted, commensurable, and actively conserved, and its
setpoint must be predicted before lookup.

## 4 · Search debt — exact, for the next session

1. **#5 insulin/glucagon, molar — DISCHARGED STRUCTURALLY, 2026-08-05
   (addendum).** Sourced this pass `[B]`: beta cells secrete insulin in
   response to high glucose; alpha cells secrete glucagon "in the opposite
   manner", and glucagon secretion is inhibited by insulin via GABA
   (Wikipedia *Insulin* and *Glucagon*, fetched 2026-08-05; glucagon MW
   3485 Da, so both legs are molar concentrations — commensurability would
   have been satisfied). The structural verdict `[I]`: the regulated variable
   is **blood glucose**, not the hormone pair. The loop senses glucose and
   drives the two secretions oppositely; nothing senses or holds
   `[insulin]×[glucagon]`. A product no feedback loop measures is not a
   conserved quantity — filter 1 fails without needing the concentration
   ranges, which were not sourced this pass and no longer matter for the
   verdict. The pair is reciprocal push–pull, which is inverse correlation —
   exactly what WO-C1 step 2 says is not the same as conservation.
2. **Autonomic pair:** sympathetic/parasympathetic tone in commensurable units
   (e.g. firing rates): product conserved? (HRV literature speaks of ratios and
   total power; the product question appears unasked — which is itself data.)
3. **E/I conductance pair** in cortex: both in nS, co-regulated — but the
   literature reports correlated scaling (both rise with drive), which is the
   opposite of product conservation. Check whether any preparation shows a
   conserved E×I budget.
4. **Enzyme-kinetic reciprocal relations** (WO-C1 search seed): mass-action
   equilibria conserve *ratios of products* (K_d, K_eq), not two-factor
   products of regulated quantities. Confirm or find the exception.
5. **Allometric pairs with conserved products** (WO-C1 search seed): Damuth,
   Kleiber — all cross-species, none within-organism regulation. Record as
   filter-3 deaths unless an exception surfaces.

## 5 · What this report did NOT do

- No tier promoted. `Finity_L` remains `DRAFT [C]`; `F3` remains OPEN.
- No comparison performed (step 4 never reached — no survivor).
- No claim that the search is complete. Seven candidates in one pass is a
  beginning; the kill row of `50` demands the search be done hard before
  anything is printed, and this report is not that search. It is the first
  cut, with the filter made explicit and the nearest formal near-miss turned
  into a scope condition.
- Candidates #3 and #4 carry memory-sourced rows, marked above; they are
  directionally safe but owe primary sources before they are cited anywhere
  downstream.

## 6 · Observations on other surfaces, per §5.5 — stated, not edited

**On `51_FINITY_L_C1_PREDICTION_2026_08_05.md`:** its `canonical_phrase` reads
*"the cardiovascular pair refutes, Hill is shifted."* The document itself says
the comparison has **not** been performed and the refutation is a *prior
expectation*. Read without its document — which is how a harvested phrase is
read — "refutes" is a completed verdict. This is exactly the WO-A2 hazard (an
unfenced phrase reads as settled). Flagged for the seat review `51` will owe
anyway; not edited here, because the file is another session's committed work.

**On `THE_EXECUTION_PLAN_2026_08_05.md`:** WO-A1's heading reads "The 177
unfindable documents"; its body reads 134. Both figures are correct at different moments:
177 is the raw count including dot-directory noise (`.lake` Lean dependencies,
`.pytest_cache`); 134 is the count after `build_corpus_index.py` was amended
(commit `d960514e`) to stop walking them. The heading should carry the body's
number or the delta. Stated here, not edited there — the plan is another
session's artifact and this report does not repair it unilaterally.

**Canonical path:**
`01_EMERGENTISM/00_HANDOFF/WO_C1_OPENING_REPORT_BIOLOGICAL_PAIR_2026_08_05.md`

•   ⊙   ○ — *the intersection is empty so far; the preregistration is standing; the debt is exact.*

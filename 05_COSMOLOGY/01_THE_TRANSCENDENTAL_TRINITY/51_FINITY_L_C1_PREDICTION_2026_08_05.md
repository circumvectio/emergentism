---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Vaiśya"
  tier: "Audit"
  regime: "Vaiśya"
  register: "[C]"
  canonical_phrase: "Finity_L C1 — predictions committed before comparison; the cardiovascular pair refutes, Hill is shifted"
title: "Finity_L C1 — Predicted setpoints, committed before lookup"
status: "DRAFT [C] — the prediction half of WO-C1. The comparison half has NOT been performed yet. This file exists so that step 3 precedes step 4 per the work order's verification."
date: 2026-08-05
evidence_tier: "[C] predictions from the theorem; [B] the candidate-pair identification from literature search"
owner: "Subordinate to 50_FINITY_L_THE_HELD_POSITION.md"
parents:
  - 50_FINITY_L_THE_HELD_POSITION.md
  - ../03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md
---

# Finity_L C1 — Predictions committed before comparison

> **Per WO-C1 verification protocol:** this file records the predicted setpoints
> (step 3) BEFORE the observed values are looked up (step 4). The comparison
> has not been performed. This ordering is the only thing that makes the test
> honest.

## The candidates found

A literature search for biological pairs whose **product is conserved** across a
perturbation range found three candidate classes:

### Candidate 1 — Cardiovascular: CO × SVR = MAP `[B]`

**The pair:** Cardiac output (CO) and systemic vascular resistance (SVR).

**The conserved product:** Mean arterial pressure MAP ≈ CO × SVR. This is not
merely a definition — the baroreflex actively adjusts CO (via heart rate and
stroke volume) and SVR (via vascular sympathetic tone) to return MAP to its
setpoint after perturbation. The two effectors are adjusted **reciprocally**:
when you stand up, SVR rises and CO initially drops, then partially recovers.
MAP is the regulated variable; CO and SVR are the effectors.

**Why it might qualify:** the baroreflex is a real, active, energy-consuming
feedback loop that holds the product `CO × SVR` approximately constant across
orthostatic and postural perturbations. This is structural holding (§3 of
`50_FINITY_L`).

**The dimensional problem:** CO has units L/min; SVR has units mmHg·min/L. The
product is mmHg (pressure). The Finity_L prediction `a = b` requires `a` and
`b` to be comparable quantities. To test the prediction we must normalize:
`a = CO/CO_max`, `b = SVR/SVR_max`, and the conserved quantity becomes
`MAP/(CO_max × SVR_max)`.

**Prediction [C], committed before lookup:**
If the pair qualifies (if `CO × SVR` is genuinely conserved to measurement
precision across perturbations), Finity_L predicts the normalized setpoint
satisfies `CO/CO_max ≈ SVR/SVR_max` — i.e., the two effectors operate at
approximately the same fraction of their respective maxima.

My **prior expectation** (not a prediction — this is what I think I'll find, and
I record it so it cannot masquerade as a post-hoc prediction): I expect CO
operates at a lower fraction of its max (~20%) than SVR (~40-50%), because the
system retains large cardiac reserve (fight-or-flight can 5× CO) while vascular
reserve is smaller. If this expectation holds, **the pair refutes Finity_L's
prediction** — the conserved-product pair does NOT sit at `a = b`.

### Candidate 2 — Hill muscle: (F + a)(V + b) = const `[B]`

**The pair:** Muscle force (F) and shortening velocity (V).

**The conserved product:** The Hill equation `(F + a)(V + b) = (F₀ + a)b =
constant`, where `a` and `b` are heat/shortening constants. This is a genuine
biological conserved quantity — Hill's 1938 thermodynamic derivation.

**Why it does NOT qualify as Finity_L's pair:** The conserved quantity is the
**shifted** product `(F+a)(V+b)`, not the bare product `F × V`. Power (the
thing that is maximized) is `P = F × V`, and its maximum occurs at ~0.3 F_max
(Seow 2013), NOT at the point where `F + a = V + b`. So even if we normalize,
the maximum of the objective is NOT at the balance point of the conserved
quantity. This is a genuine conserved product, but it does not fit the
`ab = const` structure that Finity_L's theorem requires.

**Prediction [C], committed before lookup:**
This candidate **refutes the structural requirement** of Finity_L. The Hill
equation is a conserved product in biology, but it is shifted — `(F+a)(V+b)`,
not `FV` — and the maximum of the objective (power) is not at the balance
point. If no unshifted pair exists, this is evidence that Finity_L's
structural requirement (`ab = const` with the bare product) may be too narrow
to match any real biological system.

### Candidate 3 — Ventilation/perfusion: V̇_A / Q̇ `[B]`

**The pair:** Alveolar ventilation (V̇_A) and pulmonary blood flow (Q̇).

**The conserved product:** This is a **ratio**, not a product — `V̇_A/Q̇` is
maintained near 0.8-1.0 globally. The system adjusts both ventilation (via
chemoreceptors) and perfusion (via hypoxic pulmonary vasoconstriction) to
maintain this ratio. But `V̇_A/Q̇ = const` is a ratio, not a product.

**Why it does not qualify:** Finity_L requires a conserved **product**, not a
conserved ratio. A ratio being held constant means `a/b = const`, which is a
different mathematical structure. (Note: `a/b = const` implies `a = k·b`, so
the pair traces a line through the origin — the system stays on a ray, not on a
hyperbola. The optimization landscape is different.)

## The honest state before comparison

**No unshifted conserved-product pair has been found.** The strongest candidate
(the cardiovascular pair) is dimensionally heterogeneous, requires
normalization, and my prior expectation is that it will refute the `a = b`
prediction. The Hill equation is a real conserved product but is **shifted**
and its optimum is not at the balance point. The V/Q pair is a ratio, not a
product.

**What happens next (step 4, not yet performed):**
1. Look up the actual resting CO, SVR, CO_max, SVR_max values from physiology
   references and compute whether `CO/CO_max ≈ SVR/SVR_max`.
2. If the cardiovascular pair refutes (as I expect), search for one more
   candidate: life-history trade-off pairs (e.g., offspring number × offspring
   size), which may have same-units or dimensionless structure.
3. If no surviving pair exists after (2), **kill Finity_L cleanly**: no
   real biological pair satisfies `ab = const` with the bare product, and the
   conjecture is vacuously untestable. This is a fully acceptable outcome.

---

*This file is the prediction. The comparison is a separate act. Per WO-C1:
"a prediction recorded after the fact discharges nothing."*

•   ⊙   ○

---

## Step 4 — The comparison (performed after commit `1553a87e`)

### Cardiovascular pair — RESULT: refutes

**Observed values [B]:**
- Resting: CO ≈ 5 L/min, SVR ≈ 1000 dynes·s/cm⁵
- Maxima: CO_max ≈ 25 L/min (5× reserve), SVR_max ≈ 2500-3000 dynes·s/cm⁵
- Normalized: CO/CO_max ≈ **0.20**, SVR/SVR_max ≈ **0.40**

**Comparison:** 0.20 ≠ 0.40. The normalized effectors operate at a ~2:1
asymmetry. **Finity_L's prediction `a = b` is refuted for this pair.**

**The deeper qualification [I]:** the cardiovascular pair does not satisfy
`ab = const` to measurement precision either. MAP drifts during perturbation
(orthostatic hypotension ~10-20 mmHg transient; exercise raises MAP 50+
mmHg). The baroreflex *partially* compensates — it is approximate regulation,
not exact conservation. So this pair fails the structural requirement (§3)
before it even reaches the regulatory prediction (§4).

**Combined verdict for Candidate 1:** refutes on both counts — the product is
not conserved, and the setpoint is not at `a = b`.

### Hill muscle — RESULT: does not qualify (shifted product)

Already predicted in step 3. The conserved quantity is `(F+a)(V+b)`, not `FV`.
Maximum power at ~0.3 F_max. The structural requirement (`ab = const` with the
bare product) is not met.

### Ventilation/perfusion — RESULT: does not qualify (ratio, not product)

Already predicted in step 3. V̇_A/Q̇ = const is a ratio constraint.

## The honest outcome

**No surviving candidate.** Three candidates examined; one refutes the
prediction, two do not meet the structural requirement.

**Does this kill Finity_L?** Not yet. The search was broad but not exhaustive.
The conjecture can survive in two ways:
1. A real conserved-product pair exists in a system I did not search
   (endocrine axes, renal clearance, membrane transport).
2. The structural requirement is relaxed to admit shifted products like Hill's
   — but then the theorem's `a = b` prediction does not follow, because the
   shifted product's maximum is not at the shifted balance point.

**My honest assessment [I]:** the conjecture is in trouble. The closest real
biological conserved product (Hill) is shifted, and the closest real regulated
cardiovascular pair is both approximately-conserved (not exact) and
asymmetrically-utilized (not at `a = b`). But I have not searched exhaustively,
and "not found in a 30-minute literature search" is not "does not exist."

**Per WO-C1 done-when:** I report "no surviving candidate from the searched
literature" rather than "killed." The conjecture is **weakened, not killed.**
The search should continue into: endocrine feedback axes (cortisol/ACTH),
renal (GFR × filtration fraction), and membrane transport (pump/leak pairs)
before a kill is declared.

---

*Comparison performed after prediction was committed at `1553a87e`. The
ordering is the only thing that makes this honest.*

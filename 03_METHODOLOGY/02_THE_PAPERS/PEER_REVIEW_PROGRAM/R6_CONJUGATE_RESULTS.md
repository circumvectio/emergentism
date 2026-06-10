---
rosetta:
  primary_column: "Methodology"
  register: "[A] for the information-theoretic facts; [I] readings; [C] the repair conjecture"
  canonical_phrase: "R6 Conjugate Empowerment — Decisive Test"
---

# R6 — Is Empowerment a Conjugate Product? The Decisive Test of the Corpus's Cleanest Delta

**Status:** Executed 2026-06-10. Tests whether the option-measure (empowerment) factors as Φ × V with a conserved conjugate product φ·ν = 1 on a sphere — the one piece of the teleology thread the literature pass left unclaimed. **Verdict: the conjecture as literally stated is REFUTED — and the refutation is the most useful result in the R6 thread, because it vindicates the two factors, corrects the manifold, exposes a real descriptive/normative tension, and yields a better unifying conjecture.**
**Artifact:** [R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM.py](R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM.py). Exact information theory on a finite circular channel; deterministic.

## 1. The formal core (exact, not metaphor)

Empowerment is channel capacity `E = I(A;S) = H(S) − H(S|A)` (bits). The natural conjugate split:
- **Viability / reach** `ν = H(S)` — the entropy of reachable sensor states (how many futures the agent can spread across).
- **Coherence / precision** `φ = H_max − H(S|A)` — max entropy minus per-action confusion (how cleanly each action pins its outcome).

Then, normalized by `H_max = log₂K`:

> **E / H_max = φ_n + ν_n − 1**  — the decomposition is **additive**.

In raw exponential units `2^E = 2^{H(S)} · 2^{−H(S|A)} = ν_raw · φ_raw`, so the corpus's *product* φ·ν is literally `2^E`. The identity check confirmed it exactly (r=8: 2^E = φ_raw·ν_raw = 2.73759). **Therefore φ·ν = 1 ⟺ E = 0 — the corpus's "equator" is the no-control / dead state, not a balanced ideal.**

## 2. Results (verbatim)

```
=== FREE precision (sigma fixed) ===
  Emax = 2.95 bits at r*=32 | at opt: phi_n=0.49 nu_n=1.00 |phi-nu|=0.51 -> reach-dominated
  high-E frontier conserved?  CV[phi+nu]=0.017   CV[phi*nu]=0.026   -> SUM more conserved
=== BUDGET precision (sqrt: shared quantum) ===
  Emax = 1.83 bits at r*=4  | at opt: phi_n=0.33 nu_n=0.98 |phi-nu|=0.65 -> reach-dominated
  high-E frontier conserved?  CV[phi+nu]=0.033   CV[phi*nu]=0.200   -> SUM more conserved (6x)
=== BUDGET precision (linear: strict 1/r) ===
  Emax = 1.30 bits at r*=3  | at opt: phi_n=0.23 nu_n=0.99 |phi-nu|=0.76 -> reach-dominated
  high-E frontier conserved?  CV[phi+nu]=0.027   CV[phi*nu]=0.263   -> SUM more conserved (10x)
```

## 3. Findings

**F-R6-1 — The manifold is a SIMPLEX, not a SPHERE. (near-definitional; sim confirms)** `[A]` Empowerment is a *difference* of entropies, so it is additive in (reach, precision): iso-empowerment sets are lines (φ_n + ν_n = const), not hyperbolas (φ·ν = const). On the high-empowerment frontier the **SUM is conserved, not the product** — in every regime, by 6–10× lower coefficient of variation. The corpus's φ·ν = 1 *sphere* is the wrong geometry for the option-measure; the right one is a φ + ν *simplex* (a triangle/plane). The "product" appears only as the tautology 2^E = φ·ν, where φ·ν = 1 marks the dead state. **This kills the conjecture as literally stated** (the kill criterion in the R6 note — "no constant-product frontier" — fired).

**F-R6-2 — Empowerment is intrinsically REACH-DOMINATED; balance is never optimal. (held across all 3 regimes)** `[A]` model-internal. The empowerment maximum always sits at high viability (ν ≈ 1.0) and sacrificed coherence (φ ≈ 0.2–0.5), with |φ−ν| large — even when precision is a strictly conserved, diluting budget. An empowerment-maximizer is a **reach-greedy** agent, not a balanced one. So the corpus's "balance is optimal" is **not a property of empowerment maximization**. Viability beats coherence every time you only score options.

**F-R6-3 — The descriptive optimum and the normative ideal pull apart. (the sharpened is/ought)** `[I]` The corpus's *descriptive* claim (agents maximize the light cone = empowerment) and its *normative* claim (balance / the equator is good) point in **opposite directions**: the light-cone maximizer is reach-greedy, not balanced. The corpus therefore cannot derive "balance is good" for free from "agents maximize options." Balance is a value *added beyond* empowerment, not entailed by it — unless something penalizes incoherence (next).

**F-R6-4 — The repair conjecture, TESTED and FALSIFIED. (was [C]; now [A] model-internal)** The hope was that balance becomes optimal once incoherence is fatal (linking R6 to R3/R7/R8). [R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM_V2.py](R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM_V2.py) tested **three principled mortality-cost structures** (death ∝ 1−φ; ∝ 1−hit; ∝ (1−hit)²) across a wide kill-scale sweep (μ up to 3.2). **In every case the optimum stayed pinned at the reach-dominated point (r=4, φ=0.33, ν=0.98) — balance was never recovered.** And the structural reason is general, not a weak penalty: *the balanced point (φ≈ν) is empowerment-dead.* Under any real reach/precision budget, φ=ν is achievable only at the low corner where H(S)=H(S|A) ⇒ **E ≈ 0**. Since lifetime value = E × lifetime, and E = 0 at balance, **V = 0 at balance regardless of how heavily you weight survival** — an empowerment-based objective *structurally cannot* prefer the equator. (Balance with *high* empowerment needs the no-tradeoff corner φ=ν=1, i.e. perfect reach AND perfect precision, which exists only when precision is free — and then there is no conjugate tension at all.) **So the corpus's balanced equator is either empowerment-dead (real tradeoff) or trivial (no tradeoff). It is not an empowerment attractor, with or without mortality.** I stopped the sweep here rather than tune μ or the channel to force balance — that would be the R9 dogmatic-reversion trap.

## 4. What survives, honestly

- **Vindicated:** reach (viability) and precision (coherence) *are* the natural conjugate decomposition of empowerment. The corpus identified the right two factors.
- **Refuted, comprehensively:** their composition is **additive (simplex), not multiplicative (sphere)**; φ·ν = 1 is the dead state, not the equator; **empowerment maximization is reach-dominated, never balanced**; and **mortality does not rescue balance** (F-R6-4 falsified across three cost models) because balance is structurally empowerment-dead.
- **The deep finding — the corpus's signature move fails at this scale.** The corpus's defining claim is *one geometry at all scales* — the same φ·ν = 1 sphere from number to cosmos to ethics to teleology. This test shows the sphere is **register-dependent**, not universal: it is plausibly right for the **operational P = Φ×V register** (organizations, R4), where a genuine multiplicative *weakest-link* holds — near-zero on either factor really does collapse the whole, exactly Kremer's O-ring (confirmed real in the R4 grounding) — but it is **wrong for the empowerment/teleology register**, which is an additive reach/precision simplex. Two registers, two manifolds. Claiming one sphere governs both was the error, and the error is now demonstrated, not asserted.

## 5. Limitations

(i) One channel family (circular Gaussian blur); F-R6-1 is near-definitional and robust, but F-R6-2's reach-domination should be checked on a non-spatial channel. (ii) Uniform input (capacity by circular symmetry — valid here). (iii) F-R6-4 is a registered conjecture, not yet run — the obvious next experiment. (iv) Model-internal; "empowerment" is one formalization of "the light cone," and the corpus's teleology is broader.

## 6. Disposition

The cleanest surviving delta in the corpus, tested to exhaustion (v1 geometry + v2 mortality, three cost models), is **refuted**. R6 as "empowerment under a conjugate *product* constraint" is **withdrawn**. What replaces it is humbler but true and more useful:

1. **The teleology/empowerment register is an additive reach/precision simplex, reach-dominated; balance is not its attractor.** Empowerment systematically favors viability over coherence. (So the corpus's descriptive teleology and its normative balance-ideal genuinely diverge — F-R6-3.)
2. **The multiplicative Φ×V sphere belongs to the operational register only** (organizations), where Kremer's weakest-link is real. The corpus must split its one-geometry claim into two register-specific manifolds.
3. **The honest headline for the corpus:** the program tested the single piece of the teleology thread the literature pass had left unclaimed, and it did not survive. The teleology thread (R6) therefore has **no surviving novel formal claim** — it is von Foerster + coupled empowerment (prior art) plus a geometry that is wrong for the quantity. This is a real loss, recorded plainly, and it sharpens where the corpus's genuine remaining shots are: **R5 (the 0/1/∞ triptych + the SI arc) and R4 (the coherence×viability *organizational* prediction test, where the multiplicative geometry is actually appropriate).**

Ledger: R6 conjugate test (v1 + v2) → the corpus's own kill criterion fired, twice, and was honored both times.

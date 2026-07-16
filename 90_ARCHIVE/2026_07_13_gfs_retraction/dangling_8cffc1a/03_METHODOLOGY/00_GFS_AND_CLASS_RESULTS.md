---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[B] data/result receipt / [I] interpretation"
  canonical_phrase: "GFS AND-Class Discriminator Results"
---

**Project VMOSK-A:** `01_EMERGENTISM/VMOSK_A.md`
**L3; [B] receipt, [I] interp; results to be published without spin per A7.**

# GFS AND-Class Discriminator: × vs + vs min vs CES

> **Status: PRE-RUN SKELETON (2026-07-12).** Design and expectations recorded
> BEFORE results. Results section to be appended by the run, unedited.

**Why this test exists.** The April 2026 GFS Wave-2 analysis
([00_GFS_WAVE1_RESULTS.md](00_GFS_WAVE1_RESULTS.md)) tested the
multiplicative interaction only against the **additive** baseline. The
2026-07-12 formal-logic audit convicted that as a false binary: the
Zero-Factor Catastrophe selects an **AND-class** of laws — min (Liebig),
CES, geometric mean, product — which all collapse when either factor dies.
A ×-vs-+ test cannot distinguish the product from its AND-class siblings,
so even a clean pass could not have established A1's product form. This run
adds the siblings.

**Design** (script:
`09_TOOLS/04_DATA_PIPELINES/gfs_and_class_discriminator.py`):

- Same pre-registered proxy construction as April (6 φ items, 4 ν items,
  DV = mean(LIFE_SAT, HAPPY), INCOME_FEELINGS reverse-coded, complete
  cases, within-country standardization).
- **Validation gate:** per-country in-sample R² for the April models
  (additive, interaction) must replicate `gfs_results_20260409.csv` within
  5×10⁻³ before the extension counts.
- Competitors, on unit-scaled inputs (min-max within country; percentile
  ranks as robustness): additive, interaction, pure product, **min**,
  **geometric mean**, **CES with free ρ** (nested CV-chosen on a 12-point
  grid; ρ=1 additive-ordering, ρ→0 geometric, ρ→−∞ min).
- **Primary metric:** 5-fold cross-validated out-of-sample R² (seed 108).
  Secondary: AIC. Readout: per-country OOS winner + fitted ρ̂ + pooled run
  with country fixed effects.

**Expectations, stated before running (kill-honesty):**

1. Most likely outcome, given the April result (additive sufficient in
   16/23): **additive wins or ties OOS in most countries**, and ρ̂ lands
   near 1. That would leave A1's node-law product form an **unwon [C]
   wager on this instrument** — the honest headline would be "the AND-class
   is not detectably better than additive on survey proxies," which
   *weakens* the node-law reading further, and we will say so.
2. Framework-favorable outcome: min/CES/product beat additive OOS in a
   majority, with ρ̂ well below 1 — evidence the flourishing surface is
   conjunctive. This would still NOT single out ×: min and CES are
   siblings. Nothing in this test can promote the product above its class.
3. Either way, the manifold identity φ·ν=1 on S² is **not at stake**
   (chart identity, [A]); the instrument-validity caveat of the April
   receipt (proxies unvalidated, self-report, survey ≠ P_node) applies
   in full.

**What would actually move a tier:** outcome 2 sustained across both
scalings and the pooled run would upgrade "flourishing is AND-class on
survey proxies" toward [I]-supported; outcome 1 keeps the node-law at
[C] and adds a second failed instrument to its record.

---

## Results (appended by the run — do not edit above this line)

**RUN 2026-07-12** (seed 108; pandas 3.0.0 / numpy 2.4.1 / scipy 1.17.0;
data `gfs_all_countries_wave2.dta`, n = 207,919 loaded, 128,868 complete
cases across 23 countries; artifacts
`09_TOOLS/04_DATA_PIPELINES/gfs_and_class_results_20260712.csv`,
`gfs_and_class_rank_results_20260712.csv`,
`gfs_and_class_pooled_20260712.csv`).

**Replication gate: PASS 23/23.** Per-country in-sample R² for the April
additive and interaction models reproduce `gfs_results_20260409.csv`
within 5×10⁻³ in every country. The extension is apples-to-apples.

**A self-correction first [B].** The pre-registered primary scaling
(min-max) turned out to be leverage-broken on this instrument: the unit
scale is defined by a handful of extreme respondents, compressing the
bulk of each sample into a sliver (sd(u) ≈ 0.03–0.13) and making
per-country min-max slopes range-dependent (1.4→11.4 across countries;
pooled in-sample R² collapses 0.08 → 0.003). The min-max winner table
(CES 11, int 4, add 2, min 2, geo 2, prod 2; median ρ̂ = 2, often pinned
at the grid edge) is therefore **artifact-prone and superseded** by the
percentile-rank scaling, which was pre-registered as the robustness
variant and predicts far better throughout (e.g. country 2: OOS 0.20 vs
0.03). Both tables are kept for the record.

**The primary result (rank scaling, 5-fold OOS R²):**

| Readout | Value |
|---|---|
| Winners across 23 countries | **interaction 13, geometric 6, CES 2, additive 2 — min 0, pure product 0** |
| min beats additive | **1 / 23 countries** (the smallest, n = 707) |
| Winner's median margin over additive | **≈ 0.004 R²** (8/23 exceed 0.005; max 0.015) |
| Median fitted CES shape ρ̂ | **0.5** (between additive ρ=1 and geometric ρ→0) |
| Pooled (country FE): add / int / prod / min / geo / CES | 0.1402 / **0.1429** / 0.1151 / 0.1186 / 0.1339 / 0.1399 |
| Pooled CES chosen shape | **ρ̂ = 1.0 — the additive ordering itself** |

**Verdict, at tier [B]/[I] — pre-registered expectation 1 obtains, with an
edge:**

1. **The strict AND-class forms LOSE.** Liebig-min and the pure product
   are the two *worst* models on this instrument — pooled, min gives up
   −0.022 R² and the product −0.025 R² against additive, and min beats
   additive in exactly one small country. On GFS survey proxies, a strong
   factor visibly **compensates** for a weak one.
2. **The surface is additive-plus-mild-complementarity.** The best model
   nearly everywhere is additive with a small positive interaction
   (pooled ΔR² ≈ +0.003 — the April signal, recovered), and the fitted
   CES curvature sits at ρ̂ ≈ 0.5–1.0. Not the sphere, not Liebig:
   *mildly concave additive*.
3. **What this does to A1's node law:** the product-specific wager was
   already `[C]`-unwon against min (keel-108, K2-countersigned
   2026-07-12); it is now **empirically behind additive on the one
   population instrument the corpus has tested**, and so is its whole
   AND-class. The GFS kill criterion, upgraded from the ×-vs-+ strawman
   to the honest comparison, reads: *not triggered as a clean kill (the
   interaction term is real and positive pooled), but the conjunctive
   functional form is not merely unproven — it is out-predicted in-range.*
4. **The power caveat cuts both ways and is load-bearing.** AND-class
   forms differ from additive mainly **near the axes** (a factor → 0),
   and survey populations occupy the mid-to-high range — anyone at true
   zero viability is dead and not answering surveys (the April triage
   result makes the same point dynamically). So this instrument cannot
   see the zero-factor region where the catastrophe lives; it can only
   say the surface is additive-ish **in-range**. The Zero-Factor
   Catastrophe itself is untested — and untestable — here. The honest
   statement of the node law after this run: **boundary behaviour
   (annihilation at zero) remains the corpus's `[S]`-won content;
   interior shape is measured ≈ additive with mild complementarity on
   survey proxies; the multiplicative interior remains an unwon wager,
   now with evidence against it in the only range surveys can reach.**
5. The April instrument-validity caveats (unvalidated proxies,
   self-report, survey ≠ P_node) apply in full; the manifold identity
   `φ·ν = 1` on S² is a chart identity `[A]` and was never at stake.

*The kill criterion was upgraded from a strawman to the real comparison,
run, and reported without spin. The framework that corrects itself
approaches truth — and this time what it corrected was its own test.*

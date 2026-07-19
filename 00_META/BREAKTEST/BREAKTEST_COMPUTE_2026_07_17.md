---
rosetta:
  primary_level: L1
  primary_column: Meta
  operator: "Kali 🎲"
  tier: "Workforce"
  regime: "Caṇḍāla"
  register: "[D] STAGED audit — K2 aware, not K2-signed"
  canonical_phrase: "Breaktest Compute — the doctrine's geometry, attacked numerically where the algebra hides the float"
title: "BREAKTEST_COMPUTE — numerical red-team battery against the Titan arithmetic core"
status: "[D] STAGED audit — K2 aware, not K2-signed"
evidence_tier: "[A] the float arithmetic (numpy float64, managed python3); [S] the doctrinal readings attached to it. Nothing here upgrades or downgrades any claim; it maps where the computational embodiment holds."
date: 2026-07-17
battery_script: /Users/Yves/Documents/BREAKTEST_COMPUTE_battery.py
---

# BREAKTEST_COMPUTE — numerical red team vs. the arithmetic core

**Dispatch:** RedTeam_Compute (L1 firewall, Kali 🎲). Everything attacked here is
proven algebraically in the corpus; this battery asks the orthogonal question —
**does the float64 embodiment break in a regime the doctrine's simulations
actually visit?** Each test: SETUP → RESULT (max deviation, degradation regime)
→ VERDICT (ROBUST / DEGRADES-AT ⟨regime⟩ / FAILS).

**Battery script:** `/Users/Yves/Documents/BREAKTEST_COMPUTE_battery.py`
(run: `python3 BREAKTEST_COMPUTE_battery.py`; ~1 s; numpy only; rng seeded
20260717; eps = 2.220446049250313e-16 throughout; deviations reported in eps
units).

**Doctrinal sources attacked:** `TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md`
§2 (T-A1, T-A2, T-A5, T-A6, T-A13); `40_THE_TITAN_COMPOSITION_LAW.md` §§2–3
(receipt 104); `FALSWEEP_C_CROSSFILE_2026_07_17.md` (F6, P5).

---

## TEST 1 — Pole conditioning of φ·ν = 1 (T-A2)

**SETUP.** θ = π·d and π·(1−d), d log-spaced [1e-3, 0.5] → 10⁶ pole-dense points
in θ/π ∈ [1e-3, 1−1e-3]. Form A (naive doctrine form): `cot(θ/2)·tan(θ/2)` with
cot evaluated independently as `cos/sin`. Form B: `ν·(1/ν)`, ν = `tan(θ/2)`.
Extended probe pushes d down to 1e-320 on both sides.

**RESULT.**

- Primary sweep: Form A max dev **2.000 eps** (at θ/π ≈ 0.99876); Form B max dev
  **0.500 eps**. **Zero** deviations beyond 10×eps anywhere in the swept regime.
  Answer to the dispatch question: *nowhere in the swept regime does the product
  leave ±2 eps of 1.*
- Extended probe, θ→0 side: **breakdown wall at d = θ/π ≲ 3.541e-309** — φ =
  cos/sin overflows when sin(x) < 5.563e-309 (x = θ/2), giving inf·ν = inf;
  Form B hits the same wall via 1/ν overflow. Float breakdown appears **~309
  orders of magnitude before** the θ = 0 domain boundary, in log terms — the
  float sphere's south polar cap is cut off far above the pole.
- Extended probe, θ→π side: **no breakdown** — finite everywhere, max dev 2.000
  eps. θ rounds to fl(π) for d ≤ 5.544e-17 (383,273 probe pts collapse onto one
  shell); `tan(fl(π/2)) = 1.633123935319537e16`. fl(π) undershoots true π, so
  the domain edge is never crossed. The ν-pole is unreachable: the θ-chart caps
  ν at 1.63e16.
- Chart conditioning: cond(θ→ν) = θ(1+ν²)/2ν **crosses 10 at θ/π ≈ 0.9079**
  (ν ≈ 636.6) and reaches **999 at θ/π = 0.999**. The product identity is
  self-cancelling (both factors evaluated at the same float x); the *coordinate*
  is not — a simulation reading ν as state near a pole inherits up to ~10³ eps
  of pure representation noise while P∞ = φ·ν stays within 2 eps.

**VERDICT: ROBUST** (the identity, in the swept regime and everywhere θ is
representable). **DEGRADES-AT** θ/π ≲ 3.5e-309 (overflow wall, inf/NaN) and
DEGRADES-AT θ/π ≳ 0.91 for the ν-coordinate as a state variable (chart
ill-conditioning > 10 eps; the identity itself never moves). The doctrine's
claim is a *chart tautology* (receipt 104 B.2) — numerically it behaves exactly
like one: unbreakable, because it says nothing the float can refute.

---

## TEST 2 — Velocity-dictionary chain (P5) full range

**SETUP.** cos θ vs `(1−ν²)/(1+ν²)` vs `−u(ν²)` (u = (x−1)/(x+1), T-A6) vs
`−tanh(log ν)`, ν = tan(θ/2), over the full 10⁶-point θ-sweep plus the extended
probe. Then a ν-*direct* sweep (2×10⁶ pts, ν log-spaced 1e-320…1e308) to test
the forms where the θ-chart cannot reach.

**RESULT.**

- θ-chart residuals vs cos θ: `(1−ν²)/(1+ν²)`: **3.955e-16 (1.78 eps)** at
  θ/π ≈ 0.516 (equatorial cancellation — absolute, benign); `−u(ν²)`: identical
  3.955e-16; `−tanh(log ν)`: **3.678e-16 (1.66 eps)**. **Zero sign mismatches,
  zero NaN.** No branch surprise near θ→π: log ν → +∞ cleanly; tanh saturates
  to exactly −1 for |log ν| > 18.7 with max abs gap 1.11e-16 (cos is below
  float resolution there too — both fail *together*).
- ν-direct sweep — **the hidden asymmetry the algebra conceals**: the rational
  forms `(1−ν²)/(1+ν²)` and `−u(ν²)` go **NaN for ν > 1.341e154** (ν² overflow;
  490,041 pts), while `−tanh(log ν)` records **0 NaN across the entire float64
  range**. Where both are finite they agree to 2.22e-16. Three algebraically
  identical forms; three different float domains.
- θ-chart reachability: ν ∈ **[6.123e-17, 1.633e16]** — only ~33 of float64's
  ~616 orders of magnitude are reachable through the θ chart. The float
  embodiment of the sphere through this chart is a thin equatorial shell in
  ν-space; the doctrine's poles are further from simulation than the algebra
  suggests.

**VERDICT: ROBUST** within the θ-chart (chain exact to ≤ 1.78 eps, no branch or
sign event). The ν²-forms **FAIL** for ν > 1.34e154 (NaN, not degradation);
`−tanh(log ν)` is ROBUST over all of float64 ν-space. Any simulation working in
the manifold coordinate ν directly (the doctrine's own native register for
φ·ν = 1) must use the tanh form or cap ν — the Weierstrass rational form is
silently mortal above 1e154.

---

## TEST 3 — F6 repair check (tat-tvam-asi Step-1 defect)

**SETUP.** (a) The defective public-site assignment cos θ = ν, sin θ = φ forces
φ·ν = sin θ cos θ. 4×10⁶-point grid over (0, π). (b) The staged repair
ν = tan(θ/2), φ = cot(θ/2) on the 10⁶-point pole-dense sweep, plus the repair's
projection identities sin θ = 2ν/(1+ν²), cos θ = (1−ν²)/(1+ν²).

**RESULT.**

- (a) max(sin θ · cos θ) = **0.49999999999996148 ≈ 0.5**, argmax within 1.96e-7
  of **θ = π/4** (grid resolution). Value at θ = π/2: 6.123e-17 ≈ 0.
  **Correction to the dispatch brief:** the maximum sits at π/4, not π/2 — the
  brief's parenthetical was numerically refuted; the defect bound φ·ν ≤ 0.5
  itself (FALSWEEP F6) is confirmed exact.
- (b) Repair: φ·ν − 1 max **2.000 eps** (φ = cos/sin), **0.500 eps**
  (φ = 1/ν). sin θ vs 2ν/(1+ν²): 1.50 eps. cos θ vs (1−ν²)/(1+ν²): 1.78 eps.

**VERDICT:** defect **CONFIRMED** (bound exact; location π/4). Repair **ROBUST**
— the Weierstrass assignment restores φ·ν = 1 to ≤ 2 eps over the full sweep,
and both projection identities hold at the same tolerance. The staged F6 banner
extension is numerically safe to apply.

---

## TEST 4 — B = sech(√E), E = (log x)²

**SETUP.** x log-spaced 1e-12…1e12 (10⁶ pts), extended 1e-320…1e308 (10⁶ pts).
B computed directly as sech(log x) and via the E-route sech(√E); √E checked
against |log x|; inversion symmetry B(1/x) = B(x) spot-checked.

**RESULT.**

- max |B − sech(√E)| = **0.000e+00** — **bit-identical on 100.00% of all 2×10⁶
  points**, including the extremes. √E = |log x| to **0.00 eps** (the rounded
  square roots back exactly). sech is even, so the |·| branch is absorbed
  exactly — **no branch issue, confirmed bit-for-bit, not just to tolerance.**
- Underflow regime: sech flushes to denormal for |log x| ≳ 708.4 and to exactly
  0 beyond the cosh overflow at |log x| ≈ 709.7 — **both forms flush together**,
  still bit-identical. The well's depth simply drops below float sea level at
  x ≈ e^{±709}; nothing disagrees on the way down.
- B(1/x) − B(x): max 2.22e-16 (1 eps).

**VERDICT: ROBUST** — the cleanest object in the battery. The one identity in
the cluster whose float embodiment is *exact*, not merely accurate.

---

## TEST 5 — Composition law (receipt 104: Viṣṇu = Śiva∘Brahmā iff |σκ| = 1)

**SETUP.** Canonical definition taken from
`40_THE_TITAN_COMPOSITION_LAW.md` §§2–3 (grep-confirmed): σ, κ are **multipliers
of axis-fixing dilations** M_λ(z) = λz on the shared titan axis {0, ∞} —
Brahmā |κ| > 1, Śiva |σ| < 1 — *not* generic Möbius maps. In SL(2,ℂ):
M_λ = diag(√λ, 1/√λ), tr² = λ + 2 + λ⁻¹. 10⁴ random axis pairs (log-magnitudes
to e^{±690}, uniform phases), then 10⁴ general random SL(2,ℂ) compositions for
the scope fence, plus a dedicated balanced-locus shell scan (δ = |λ|−1 log-spaced
1e-17…1e-6).

**RESULT.**

- **Correspondence is exact:** 10⁴ random axis pairs → **0 classification
  disagreements** between "tr² ∈ [0,4)" and "|λ| = 1" away from the float
  shell; **0/10⁴ random hits** on the locus (measure-zero, confirmed
  numerically). On the locus λ = e^{iθ}: tr² = 4cos²(θ/2) to max dev 8.95e-16,
  all values in [0,4). The algebra: Im(tr²) = (r−r⁻¹)sinθ vanishes ⟺ r = 1
  (elliptic) or θ = 0 (hyperbolic, tr² > 4). Doctrine's [A] survives the float.
- **Float fuzz on the exact boundary:** fl(|λ|) == 1.0 for δ < 1.3e-16;
  Im(tr²) emerges above 10-eps noise only for δ ≳ 8.6e-15. The balance locus
  |σκ| = 1 is **unresolvable inside |δ| ≲ 1e-15 relative** — a simulation can
  never *verify* perfect balance, only bound it. (The boundary is a discipline,
  not a measurable state — that reading is [S]; the 1e-15 shell is [A].)
- **The dispatch cross-check "|tr|² < 4 ⟺ elliptic" is FALSE as stated** for
  complex traces: 36/10⁴ mismatches on-axis; on 10⁴ general random SL(2,ℂ)
  compositions it tags **6,534/10,000 = 65.3%** as elliptic while the true
  elliptic count is **0/10,000**. Correct criterion: **tr² ∈ [0,4)** (real,
  non-negative, sub-parabolic). Example of the failure mode: tr = 1.9i has
  |tr|² = 3.61 < 4 and is loxodromic.
- **Scope fence T-S12 numerically confirmed:** generic (different-axis)
  compositions are loxodromic — 0/10⁴ elliptic; the eigenvalue-ratio
  |multiplier| = 1 cross-check agrees with the trace criterion on 10,000/10,000.
  Off-axis there *is* no canonical σκ; the law's condition is defined exactly
  where the doctrine says it lives.
- Implementation caveat found: numpy complex `sqrt` overflows **internally** for
  |λ| ≳ 1e154; the direct form λ + 2 + λ⁻¹ survives to ~1.8e308.
  Branch-consistency where safe: max **1.73e-16 relative** (sub-eps; no
  principal-branch surprise).

**VERDICT:** the doctrine's conditional law is **ROBUST** — the correspondence
|σκ| = 1 ⟺ elliptic is exact outside a ~1e-15-relative float shell that no
computation can shrink. The naive |tr|² < 4 formulation **FAILS** (65.3% false
positives on generic input); any simulator or audit script must test
tr² ∈ [0,4), never |tr|² < 4.

---

## TEST 6 — Free hunt: T-A6, the Cayley involution u(1/x) = −u(x)

**SETUP.** From the ledger §2: T-A6, u = (x−1)/(x+1), inversion ↦ −u. x
log-spaced 1e-12…1e12 (10⁶ pts), extended 1e-320…1e308 (10⁶ pts); residual
r = |u(x) + u(1/x)|. T-A1 spot-check: min(φ + ν) under φ·ν = 1 on the
10⁶-point sweep.

**RESULT.**

- Core range: max r = **2.22e-16 (1.00 eps)** at x = 4.885e-04. Full
  reciprocal-closed range: max r = **3.33e-16 (1.50 eps)**. No degradation near
  x = 1 (Sterbenz exactness: x−1 and (1/x)−1 are exact there — the involution's
  fixed region is float-safe).
- **Wall:** 1/x overflows for x < 2.2e-308 → u(inf) = inf/inf = **NaN**;
  breakdown for x ≲ 5.557e-309 (18,703 NaN probe pts). float64's
  reciprocal-closed interval is [2.2e-308, 4.5e308]: **inversion symmetry is not
  embodied over float's own full range**, even though x·(1/x) itself stays
  ≤ 0.5 eps (correctly rounded division is innocent; the *range* is the
  culprit).
- T-A1 spot: min(φ + ν) = **2.00000000000000000 exactly** at θ/π = 0.5; zero
  samples below 2 − 4.5e-16 across 10⁶ points. The AM-GM floor holds to the ulp.

**VERDICT: ROBUST** inside the reciprocal-closed range (≤ 1.5 eps, no
cancellation pathology). **DEGRADES-AT** x ≲ 5.6e-309 (NaN wall — the float
sphere's inversion map is partial at the extreme caps). T-A1 **ROBUST**.

---

## Summary table

| # | Target | Max deviation | Degradation regime | Verdict |
|---|---|---|---|---|
| 1 | φ·ν = 1 (T-A2) | 2.000 eps (cot·tan) / 0.500 eps (ν·(1/ν)); zero >10 eps | overflow wall θ/π ≲ 3.5e-309; chart cond > 10 beyond θ/π ≈ 0.91 | **ROBUST** (identity); DEGRADES-AT wall / ill-conditioned coordinate |
| 2 | P5 cosine chain | 3.955e-16 (1.78 eps); 0 sign/branch events | ν²-forms NaN for ν > 1.341e154; tanh form clean to 1e308 | **ROBUST** in θ-chart; ν²-forms **FAIL** beyond 1.34e154 |
| 3 | F6 defect + repair | defect max 0.5 exact (at **π/4**, not π/2); repair ≤ 2.000 eps | none found in (0,π) | defect **CONFIRMED**; repair **ROBUST** |
| 4 | B = sech(√E) | **0.000e+00 — bit-identical on 2×10⁶ pts** | underflow below |log x| ≳ 708.4, both forms together | **ROBUST** (exact) |
| 5 | \|σκ\| = 1 ⟺ elliptic | 0/10⁴ disagreements; locus hits 0/10⁴; on-locus tr² dev 8.95e-16 | boundary unresolvable \|δ\| ≲ 1e-15; **\|tr\|²<4 criterion: 65.3% false positives** | doctrine **ROBUST**; naive \|tr\|²<4 **FAILS** |
| 6 | u(1/x) = −u(x) (T-A6) | 2.22e-16 (1.00 eps) core; 3.33e-16 (1.50 eps) full | NaN wall x ≲ 5.6e-309 (1/x overflow) | **ROBUST**; DEGRADES-AT wall. T-A1 min exact 2.0 |

## The three numbers K2 should see

1. **65.3%** — the false-positive rate of the naive `|tr|² < 4` ellipticity
   test on generic SL(2,ℂ) (6,534/10,000 tagged elliptic; true count 0). The
   doctrine's own |σκ| = 1 criterion is exact; this common paraphrase of the
   trace criterion is not. Any audit/simulation code must use `tr² ∈ [0,4)`.
2. **1.341e154** — the cliff where the Weierstrass rational forms
   (1−ν²)/(1+ν²) and −u(ν²) NaN out (ν² overflow), while −tanh(log ν) survives
   the entire float64 range. Algebraically identical, computationally mortal.
   Same family of hazard as the complex-sqrt internal overflow at |λ| > 1e154.
3. **3.541e-309** — the φ-overflow wall: the product φ·ν = 1 breaks (inf/NaN)
   ~309 orders of magnitude before θ = 0, while the θ→π side never breaks at
   all (it collapses onto the fl(π) shell at d ≤ 5.5e-17 with ν capped at
   1.63e16). The float sphere is grossly asymmetric around the equator the
   doctrine calls symmetric.

**Aggregate finding:** every [A] claim attacked survived numerically *as a
claim about the identity*; what breaks is the **coordinate embodiment** —
charts cap, forms overflow at unequal walls, and exact boundaries (|σκ| = 1)
sit inside a ~1e-15 float-fuzzy shell. The doctrine's own register discipline
("chart tautology," "equator-ethic as discipline, not state") is the correct
computational posture, arrived at independently from below.

---

*Battery script: `/Users/Yves/Documents/BREAKTEST_COMPUTE_battery.py` ·
numpy float64, managed python3, rng seed 20260717, runtime ~1 s. [D] STAGED
audit — K2 aware, not K2-signed. Prepared under Kali 🎲 L1 firewall dispatch;
caste: L1 intake/contradiction-isolation. All raw numbers reproducible by
re-running the script.*

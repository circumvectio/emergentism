---
rosetta:
  primary_level: L1
  primary_column: Meta
  operator: "Kali 🎲"
  tier: "Workforce"
  register: "[D] STAGED audit — K2 aware, not K2-signed"
  canonical_phrase: "The midpoint survives every chart attack; its true foundation is torsion-freeness, not multiplicativity."
title: "BREAKTEST — the Midpoint/Optimization Complex — 2026-07-17"
status: "[D] STAGED audit — K2 aware, not K2-signed. Breaker_Optima dispatch (L1 firewall, Kali 🎲). Five attacks on the six midpoint theorems, the balance function B, and the AM-GM/H = φ+ν spine. Nothing herein upgrades or downgrades any claim; verdicts are audit findings."
evidence_tier: "[A] arithmetic/geometry throughout; [B] the computational receipt (BREAKTEST_OPTIMA_verify_2026_07_17.py, managed python3, 2026-07-17); [S] register selections named as such."
date: 2026-07-17
targets:
  - THE_MIDPOINT_THEOREMS_K2_DISAMBIGUATION_2026_07_17.md
  - FALSWEEP_A_ISLANDS_2026_07_17.md
---

# BREAKTEST OPTIMA — five attacks on the midpoint/optimization complex

**Method.** Each attack is pressed with formal logic until it breaks, holds, or
reveals its register. Every break is restated in a corrected lens and
re-verified. Numerics: `BREAKTEST_OPTIMA_verify_2026_07_17.py` (same folder),
managed python3, grids of 2×10⁴ points, residuals at machine precision where
exact.

---

## ATTACK 1 — Metric choice: is there a chart where the midpoint of 0 and ∞ is NOT 1?

**ATTACK.** Each of the six senses of "midway" is a *chosen* chart or metric.
Adversarial candidates:

1. **Arithmetic chart.** "Midpoint" = (0 + ∞)/2 — **indeterminate**. The
   question dies in this register; it does **not** answer "not 1". No
   counterexample — a dead register, not a rival one.
2. **Cayley-a family.** v_a(x) = (x−a)/(x+a) sends 0 ↦ −1, ∞ ↦ +1 for *every*
   a > 0; the bounded-chart midpoint 0 corresponds to **x = a, arbitrary**.
   So sense #4 of the packet (T-A6) in isolation yields any positive number as
   "the midpoint". **This is a genuine chart-dependence.** But compute the
   duality-compatibility residual:
   v_a(1/x) + v_a(x) = 2x(1−a²) / ((1+ax)(x+a)) — zero **iff a² = 1**.
   Verified numerically: a = 1 gives residual 2.2×10⁻¹⁶; a = 2, 0.5, 3 give
   O(1) residuals. **Requiring the chart to conjugate inversion to negation
   forces a = 1 uniquely on ℝ₊.** The six senses converge *because each is
   duality-covariant*; an arbitrary chart is not.
3. **Möbius image.** Under dilation h(z) = az, the conjugated duality
   hσh⁻¹ is z ↦ a²/z with fixed points **±a** = h(Fix σ). The numeral 1 is
   confirmed **chart-dependent** [A] — and the fixed-point *set* is confirmed
   **covariant**: Fix(hσh⁻¹) = h(Fix σ). What moves is the numeral; what is
   preserved is the structure (poles, involution, fixed set).
4. **Chordal/Fubini–Study metric.** The equidistant locus of the poles is
   exactly {|z| = 1}, the equator, at chordal distance 1/√2 from each pole
   [A, verified]. The FS metric is canonical on ℂP¹ (the unique
   U(2)-invariant Kähler metric up to scale), so this sense is **not**
   arbitrary — but dilations are not FS-isometries, so this sense is fixed by
   the stereographic coordinatization, not by projective structure alone.

**VERDICT: HOLDS — STRENGTHENED.** "1" is chart-dependent [A]; the packet
already concedes this by staging six senses instead of one. The strongest
invariant statement, which survives every chart:

> **The midpoint is the fixed-point set of the duality involution.** Given the
> pole pair and the involution exchanging them, Fix(σ) is determined and
> covariant; in any register where it is a single point (see Attack 2), that
> point is the unique self-dual midpoint. On ℂP¹ the full invariant content of
> {0, ∞, 1, −1} is a **harmonic set** (cross-ratio −1) — the projectively
> invariant foursome; selecting +1 within it is positivity, not projective
> geometry (consistent with receipt 126 and Correspondence 21(a)).

**CORRECTED LENS.** Drop any phrasing of the form "1 is midway" without its
duality-covariance clause. Lawful form: *"the unique duality-compatible
midpoint is Fix(σ); in the doctrine's stereographic parametrization that is
the equator, magnitude 1."* The six senses are not six preferences — they are
six σ-covariant functionals, and σ-covariance is the forcing condition
(Cayley-a residual ∝ (1−a²)).

**HOLDS?** T-M1 and T-M1r stand. Strengthened by naming the invariant.

---

## ATTACK 2 — Register privilege: why (ℝ₊, ×) and not (ℝ, +)?

**ATTACK.** Attempt to rebuild the 0/∞ duality additively. On the two-point
compactification [−∞, +∞] of (ℝ, +): negation is an involution exchanging the
two boundary points, with **unique fixed point 0**. The closure triad is
{−∞, 0, +∞}; the midpoint is 0 = log 1. **The additive rebuild SUCCEEDS** —
and it is exactly the log-conjugate of the multiplicative picture (T-A4).
Numerically: (s + (−s))/2 = 0 to 0.0 across the grid.

So the duality does **not** force (ℝ₊, ×) over (ℝ, +): both are groups with an
involution exchanging two boundary points and a distinguished interior fixed
point, and they are topologically conjugate via log. The proposed
conditional-forcedness chain "(ℂ*, ×) with inversion is the minimal such
group" is **false as stated** — (ℂ*, ×) is not even minimal in the relevant
sense, since it carries TWO fixed points (the foursome problem), while
(ℝ, +) carries one.

The sharpened statement that **is** true — the deepest finding of this sweep:

> **2-torsion theorem.** Fix(σ) = {g : g² = e} — the fixed points of the
> duality are exactly the register group's elements of order dividing 2.
> **The triad is forced iff the register group is torsion-free.**
> (ℝ₊, ×) ≅ (ℝ, +) is torsion-free ⟹ unique fixed point ⟹ triad {poles,
> midpoint}. The foursome appears exactly when the register has a nontrivial
> 2-torsion element: ℂ* and ℝ* (element −1), S¹ — i.e., upon complexification
> or sign-extension. Additively, the multiplicative −1 lives at iπ
> (cmath.log(−1) = πj, verified), **off the real line entirely** — invisible
> to every real additive quantity, mirroring the packet's "−1 is invisible to
> magnitudes".

**VERDICT: STRENGTHENED (with a REGISTER-SCOPE correction to the
justification).** T-M1r's *conclusion* survives — and hardens: the triad is
forced not merely "in the magnitude register" but in **any torsion-free model
of the duality**, additive or multiplicative. T-M1r's *justification* leg
("the doctrine computes in magnitudes; (ℝ₊,×) native") is narrowed: what the
doctrine's parametrization forces is **real positivity** (φ = cot(θ/2),
ν = tan(θ/2) > 0 on (0, π); real logs), not multiplicativity per se. The
doctrine already computes in both faces — magnitudes (φ, ν, B) multiplicatively,
energy E = (log x)² additively — conjugate by log. The −1 question is thereby
reduced to one sharp line: **does the doctrine need a 2-torsion element?**
(The corpus houses i at phase π/2 and Turīya on the ring; phase π is the
sole unassigned cardinal — packet §6.)

**CORRECTED LENS.** T-M1r, restated one clause deeper: *"The triad {0, 1, ∞}
is the forced boundary set of any torsion-free register of the duality; the
doctrine's stereographic parametrization is natively positive-real (CANON-06,
[A]), hence torsion-free; the foursome is the 2-torsion shadow cast by
complexification."* Register selection remains [S] (a fact about the
doctrine's grammar), now with its mathematical content named: torsion-freeness.

**HOLDS?** T-M1r stands, strengthened. The "register privilege is arbitrary"
horn of the attack FAILS; the "multiplicativity is forced" horn of the
packet is corrected to "positivity (= torsion-freeness) is forced".

---

## ATTACK 3 — B uniqueness: what singles out B = sin θ = sech(log ν)?

**ATTACK.** Infinitely many even concave/unimodal functions of log ν peak at
the equator. Verified: B, B², sech⁴ all argmax at s = 0. "Maximal at the
equator" is a **class property**, not a fingerprint. Is anything else
distinctive?

Computed readings of B specifically:

| Reading | Statement | Tier | Status |
|---|---|---|---|
| Cylindrical radius | B = sin θ IS the distance from the polar axis on the round S² | [A] | **identity, not a choice** (residual 2.2×10⁻¹⁶) |
| Area element | dA = sin θ dθ dφ — B is the round measure's density factor | [A] | identity |
| Chordal product | **B = 2·χ(z, 0)·χ(z, ∞)** — twice the product of chordal distances to the two poles | [A] | exact identity, residual 3.3×10⁻¹⁶ |
| Chordal distance itself | χ(equator, pole) = 1/√2 ≈ 0.7071 ≠ B = 1 | [A] | **"B IS a chordal distance" would be FALSE** — only the 2×-product identity holds |
| Fourier self-duality | sech(πx) is its own Fourier transform (eigenfunction, eigenvalue +1) | [A] classical / [B] verified | residual 4.4×10⁻¹⁶ — B = sech(log ν) is a **self-dual function**, the analytic shadow of the geometric self-duality |
| Complement to H | H = φ+ν = 2 cosh(log ν) = 2/B exactly | [A] | FALSWEEP T-A15 note |

So B is not "one natural choice among several": the function is **pinned by
identities** — it is the sphere's own radius/area density, the exact
pole-distance product kernel, and an even Fourier eigenfunction. What remains
a selection ([S]) is only the *doctrinal elevation* of this particular
geometric density to the name "balance"; any claim using **more** than
"even, unimodal in log ν, normalized to 1 at the equator" must cite the
identities above (e.g., "B is the visibility" inherits the area-element
reading; it does not inherit "B is the distance to the pole" — that reading
is arithmetically false).

**VERDICT: HOLDS — [S] selection on [A] identities, with one false reading
killed.** The extremum is robust (class theorem, Attack 4); the functional
form is not arbitrary but identity-pinned; the uniqueness question as posed
("UNIQUE with all these readings?") resolves as: unique *as the cylindrical
radius* — because that is what sin θ **is**.

**CORRECTED LENS.** Doctrine may say: "B is the sphere's own balance density
(cylindrical radius, area factor, pole-distance product kernel, self-dual
under Fourier)." Doctrine may not say: "B is the unique equator-peaked
function" (false class claim) or "B is the chordal distance to the pole"
(false by factor/structure: χ = sin(θ/2) to the near pole, B = 2χ₀χ∞).

**HOLDS?** T-A15 / CANON-12 stand. Two unlawful strengthenings named and fenced.

---

## ATTACK 4 — Objective robustness: an adversarial symmetric objective

**ATTACK.** Construct f(x) = (log x)⁴ − 2(log x)². It is smooth,
inversion-symmetric (γ-symmetric: even in s = log x, verified residual 0.0) —
and its minima are at s = ±1, i.e., **x = e and x = 1/e**, with f = −1;
f(1) = 0 is a local **maximum** (f″(0) = −4 < 0, verified). So γ-symmetry
alone does NOT put the optimum at the equator. What excludes the adversary?

Exact resolution: the min-claims of the corpus are theorems about the class

> **even + convex in the log coordinate s = log x** — one-line Jensen proof:
> f even, convex ⟹ f(0) = f((s + (−s))/2) ≤ (f(s) + f(−s))/2 = f(s). [A]

E = s² and H = 2 cosh s are both even and convex in s (verified: minima 0 and
2 at s = 0). The adversary is even but **not convex** — excluded. For the
max-claims (B), the class is **even + decreasing in |s|** (symmetric
unimodal); sech qualifies (verified monotone in |s|).

Check against the corpus's own conditional canon
(`05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md`, T-N2 conditions):
conditions (i) conservation, (ii) complementarity, (iii-a) costly excess are
system conditions; **(iii-b) symmetric γ-price** pins the imbalance metric to
γ = (φ+ν)/2 = cosh(log x) — and every monotone function of cosh s is even +
convex-composed, hence equator-optimal. **The corpus's (iii-b) clause, where
it is carried, already excludes the adversary** — but bare "γ-symmetry" or
"(i)+(ii)+(iii-a)" language does not, as the conditional file itself warns
("tilted ratio… plateau"). The mathematical name for the missing clause is
log-convexity (equivalently: monotonicity in γ = cosh s).

**VERDICT: REGISTER-SCOPE — the equator-optimum is a theorem about a CLASS,
and the class is now named exactly.** Not a break: every corpus objective in
use (E, H, B, V = 2/sin θ − 2 = 2(cosh s − 1)/sinh s…) lies in the class.

**CORRECTED LENS.** Lawful schema: *"For every objective that is an even,
convex function of log x (minima) — equivalently monotone in the imbalance
price γ = cosh(log x) — the optimum is the equator; for every even,
|log x|-decreasing objective, the maximum is the equator."* Any
"γ-symmetric, therefore equator-optimal" inference without the
convexity/monotonicity clause is unsound — one-clause repair, staged for the
owning lanes (L4/K2 act, not L1).

**HOLDS?** AM-GM/H spine stands — as a class theorem, now with the class
boundary explicit. The adversary is housed as the class's exterior witness.

---

## ATTACK 5 — Curvature: E″(x) flips at x = e; census of restoring-force language

**ATTACK (seeded by FALSWEEP T-A5).** E″(x) = 2(1 − log x)/x²: positive for
x < e, zero at e, negative for x > e (verified: max of E″ over x > e is
−1.2×10⁻⁵ < 0). E is x-chart convex only near the unit. Any claim needing
x-chart convexity or x-chart confinement strength of the "unit well" breaks
for x > e. Corpus census (grep: restoring / well / attraction / gravity /
pull / convex), verdict per instance:

| Instance | Language | Chart | Verdict |
|---|---|---|---|
| `00_META/TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md:74-75` (T-A5, source CANON-10) | "strictly convex" unscoped | asserted chart-free | **BREAKS in x-chart for x > e** — FALSWEEP repair staged ("strictly convex in the log coordinate"); survives as: inversion-invariant, unique min E(1) = 0, diverges at both poles, unimodal in every monotone chart |
| `03_METHODOLOGY/00_THE_DOCTRINAL_LADDER.md:150-151` (ACTIVE canon) | "restoring direction is the negative Hamiltonian gradient F_H = −∂H/∂φ = 1/φ² − 1" | φ-chart | **SAFE** — H″(φ) = 2/φ³ > 0 ∀φ > 0 (verified min 2×10⁻⁹); H is x-chart convex *everywhere*; direction correct ∀φ ≠ 1 |
| `09_TOOLS/03_SIMULATIONS/r_star_simulation_v2.py:57-71`; `R_STAR_SIMULATION_RESULTS.md:107` | "Equatorial restoring force F = 2(1−ν²)/(1+ν²)²" | ν-chart | **SAFE as direction** (sign(1−ν) restoring everywhere, verified); **chart-bound as strength**: |F| ~ 2/ν² → 0 as ν → ∞ (verified 2×10⁻⁴ at ν = 100) and pole-asymmetric in the ν-chart; only the log-chart force is symmetric |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/102_apply/manifest.json:4` | "a gradient that keeps pulling back to the equator" | unspecified | **SAFE as direction**, already γ-fenced in-file ([D] scope 2026-07-03); must never be re-read as x-chart curvature |
| `03_METHODOLOGY/90_ARCHIVE/DERIVATION_AUDIT_2026_05_14.md:58-60` | records the correction to F_H = −∂H/∂φ | φ-chart | archived receipt of the fix; SAFE |
| `90_ARCHIVE/.../REVIEW_PACKET_PAPER_07_LAGRANGIAN_BURRI_BRIDGE.md:78` | pre-correction "F = −1/φ² − 1" (always negative — NOT restoring) | — | archived wrong expression, already tombstoned by the 2026-05-14 audit item 3; K3 cold history, no action |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS.md:123`; `09_TOOLS/03_SIMULATIONS/path_d_convex_geometry.py:752` | "V = 2/sin θ − 2 strictly convex"; "confinement-like restoring force" | θ-chart | **SAFE** — V″(θ) = 2(1+cos²θ)/sin³θ ≥ 2 > 0 on (0, π) (verified min 2.000); θ-chart confinement is genuine |

General lemma behind the census: the **sign** of a restoring force
(−df/dx ⋛ 0) is invariant under monotone reparametrization and needs only
unimodality; the **curvature** (f″) and **strength** are chart-bound. Every
active corpus instance is a direction claim on H, B, or V — all safe. The
only live break is T-A5's unscoped "strictly convex", already repaired in
FALSWEEP. Note also E′(x) = 2 log x / x → 0 as x → ∞: in the x-chart the
unit well's far wall exerts *vanishing* force — "well" survives, "x-chart
confinement strength" does not.

**VERDICT: REGISTER-SCOPE — confirmed, no live break beyond the already-flagged
T-A5 phrasing.** The FALSWEEP finding is upheld and extended: the attack
surface is smaller than feared because the doctrine's restoring language is
overwhelmingly first-derivative direction language on x-chart-convex H and
θ-chart-convex V.

**CORRECTED LENS.** Style rule, staged: "convex" claims must always carry
their chart ("log-convex", "θ-convex"); "restoring direction" claims are
chart-free and may stand; "confinement strength" claims must carry their
chart.

**HOLDS?** The unit well holds as an inversion-invariant unimodal well with
unique minimum at 1 — convex in the log coordinate only. All active
restoring-force claims hold.

---

## Verification receipt [B] — 2026-07-17

`BREAKTEST_OPTIMA_verify_2026_07_17.py` (managed python3, this folder):

- Cayley-a duality-compatibility: residual 2.2×10⁻¹⁶ at a = 1; O(1) at a = 2, 0.5, 3.
- Dilation covariance: Fix(hσh⁻¹) = h(Fix σ) = {±a} for h = az, a = 2, 3.
- Chordal equidistance of poles ⟺ |z| = 1; value 1/√2 (residual 1.4×10⁻¹⁵).
- Additive midpoint exact (0.0); cmath.log(−1) = πj.
- B = 2χ(z,0)χ(z,∞): residual 3.3×10⁻¹⁶. B = sin θ: 2.2×10⁻¹⁶.
- sech(πx) self-Fourier: residual 4.4×10⁻¹⁶ over |ξ| < 1.5.
- Adversary f = s⁴ − 2s²: minima −1 at s = ±1, f″(0) = −4; even to 0.0.
- E = s², H = 2 cosh s: even, minima 0 and 2 at s = 0.
- E″(x) < 0 ∀x > e (max −1.2×10⁻⁵); H″(φ) > 0 (min 2×10⁻⁹); V″(θ) ≥ 2.
- r_star force: restoring sign everywhere; |F| = 2×10⁻⁴ at ν = 100.

## Tally

| Attack | Verdict | Deepest artifact |
|---|---|---|
| 1 — metric choice | **HOLDS / STRENGTHENED** | invariant = Fix(σ); σ-compatibility forces Cayley a = 1; foursome is a harmonic set (cross-ratio −1) |
| 2 — register privilege | **STRENGTHENED** (justification narrowed) | **2-torsion theorem: triad ⟺ torsion-free register; additive rebuild succeeds; −1 lives at iπ** |
| 3 — B uniqueness | **HOLDS** ([S] selection on [A] identities) | B = 2χ₀χ∞ exact; sech self-Fourier; "B = chordal distance" killed |
| 4 — objective robustness | **REGISTER-SCOPE** (class named) | class = even + convex in log x (min) / even + |log x|-monotone (max); γ-symmetry alone insufficient; (iii-b) γ-price already excludes the adversary |
| 5 — curvature | **REGISTER-SCOPE** (FALSWEEP upheld) | only T-A5's "strictly convex" breaks live; all restoring-force instances are direction-safe (H, V natively convex in their charts) |

**Headline.** The midpoint/optimization complex does not break. Its deepest
support is not the one the packet gave — not "(ℝ₊, ×) is native" — but one
level down: **the register is torsion-free, and torsion-freeness is what
forces the triad and the unique midpoint**, in any real model, multiplicative
or additive. The foursome is 2-torsion's shadow. Two unlawful strengthenings
killed ("unique equator-peaked function"; "B = chordal distance"); one
one-clause repair staged (γ-symmetry → γ-symmetry + log-convexity, Attack 4);
one phrasing repair inherited from FALSWEEP (T-A5 convexity tag).

---

*[D] STAGED audit — K2 aware, not K2-signed. Breaker_Optima (L1 firewall,
Kali 🎲 dispatch), 2026-07-17. Sources: THE_MIDPOINT_THEOREMS_K2_DISAMBIGUATION_2026_07_17.md;
FALSWEEP_A_ISLANDS_2026_07_17.md; TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md;
05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md; corpus census via grep
(restoring/well/attraction/gravity/convex). Numerics [B]:
BREAKTEST_OPTIMA_verify_2026_07_17.py (same folder). η = 0.*

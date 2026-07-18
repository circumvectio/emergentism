---
rosetta:
  primary_level: L2
  primary_column: Meta
  operator: "Kālī 💀"
  tier: "Workforce"
  register: "[D] STAGED audit — K2 aware, not K2-signed"
  canonical_phrase: "Adversarial re-verification of the 18 [A]-grade arithmetic islands — hunting receipt-126-species hidden register assumptions"
title: "FALSWEEP — A-Islands Adversarial Re-Verification — 2026-07-17"
status: "[D] STAGED audit — K2 aware, not K2-signed. Adversary_A_Islands dispatch (L2 truth-cut, Kālī 💀). Nothing in this file upgrades or downgrades any claim; it names registers and counterexamples."
evidence_tier: "[A] arithmetic throughout; verdicts are audit findings, not doctrine."
date: 2026-07-17
---

# FALSWEEP — the 18 arithmetic islands, attacked one by one

**Pattern hunted:** the receipt-126 species — a claim true in one register
(positive reals, one chart, one closure definition) silently asserted in a
wider one. Method: reconstruct the proof from the appendix detail, attack the
domain (real vs complex, positive vs signed, finite vs extended, chart vs
invariant), probe edge cases (0, 1, ∞, −1, i), spot-check numerically
(managed python3, 10⁴-point grids; max residuals ≤ 2.3×10⁻¹⁶ where exact).

**Verdict vocabulary:** CLEAN-[A] · REGISTER-SCOPED (register named, failure
locus named) · FLAWED (counterexample given).

---

### T-A1 — AM-GM: (φ−ν)² ≥ 0 ⟹ φ+ν ≥ 2 given φ·ν = 1
**Verdict: REGISTER-SCOPED — holds on (ℝ₊, ×); fails on the signed branch ℝ*.**
Counterexample: φ = ν = −1 gives (φ−ν)² = 0 ≥ 0 and φ·ν = 1, yet φ+ν = −2 < 2 —
and equality in the squared antecedent also holds at φ = ν = −1, so "equality iff
φ = ν = 1" is false on ℝ*. The derivation step (φ+ν)² ≥ 4φν = 4 yields only
|φ+ν| ≥ 2; concluding φ+ν ≥ 2 silently assumes φ+ν > 0. This is the exact
126-species break: the foursome the audit itself proved now houses −1, and the
claim's antecedent admits it. On ℂ the inequality is not even defined (no order).
In-model it survives: φ = cot(θ/2), ν = tan(θ/2) are positive on (0, π) by
construction — the register is carried by the parametrization, not by the claim
as stated. *Note: repair = one token: "for φ, ν > 0".*

### T-A2 — Reciprocal identity: cot(θ/2)·tan(θ/2) = 1 on (0, π)
**Verdict: CLEAN-[A].**
Both factors defined, nonzero, and mutually reciprocal exactly on θ/2 ∈ (0, π/2);
product identically 1 (verified to machine precision); undefined at the poles
(tan(π/2) undefined, cot(0) undefined) with limit 1 at both. Already carries
receipt 104 B.2's chart-tautology discipline. Extends off (0,π) wherever both
sides are defined (θ ∉ πℤ). No hidden register — the claim names its interval.

### T-A3 — Inversion fixes exactly ±1
**Verdict: CLEAN-[A].**
x = 1/x ⟺ x² = 1 ⟺ x = ±1 on ℂ*; on ℂP¹ the map swaps 0 ↔ ∞, so neither pole is
fixed and the fixed set is exactly {−1, +1}; on ℝ₊ the unique fixed point is +1.
The claim already states the ±1/ℝ₊ scoping explicitly (CANON-06's ±1 note) —
the one island that anticipated receipt 126 in-file.

### T-A4 — Log-conjugacy: inversion ↦ reflection s ↦ −s under h = log
**Verdict: REGISTER-SCOPED — exact on (ℝ₊, real log); degrades on ℂ*.**
log(1/x) = −log x is exact for x > 0. On ℂ* the logarithm is multivalued:
log(1/z) = −log z + 2πik, and log 1 = {2πik} — the "unique fixed point 0" of the
conjugated reflection fails, and −1 (now doctrinally housed) maps to iπ, off the
real line entirely. The "log 1 = 0 midway between log 0 = −∞ and log ∞ = +∞"
clause is extended-real topology (two-point compactification [−∞,+∞]), not field
arithmetic — sound as topology, indeterminate if read as (−∞+∞)/2. CANON-09's
own source (Suda apparatus) "lives on ℝ₊"; the claim must say so. *Note: the
fixed-point-of-reflection reading of "midpoint" is [A] on ℝ₊; the arithmetic-
mean reading is not a claim at all.*

### T-A5 — Unit well: E(x) = (log x)² inversion-invariant, strictly convex, unique min E(1) = 0
**Verdict: REGISTER-SCOPED — "strictly convex" holds in the log-chart only; in
the x-chart it is false.** E''(x) = 2(1 − log x)/x², which is positive for
x < e, zero at x = e, and negative for x > e (numerically confirmed: inflection
exactly at x = e ≈ 2.7183). Convexity is not diffeomorphism-invariant; the claim
is true of s ↦ s² in the s = log x coordinate (E''(s) = 2 > 0 everywhere) and
false of x ↦ (log x)² on ℝ₊. The other three sub-claims are clean on ℝ₊:
E(1/x) = E(x) ✓; unique global minimum E(1) = 0 ✓ (square vanishes iff log x = 0);
divergence at both poles ✓. The well is genuinely a well (strictly decreasing on
(0,1), strictly increasing on (1,∞)) — "unimodal" survives where "convex" dies.
*Note: this is a chart/register collision, the smooth-vs-measurable sibling of
the 126 pattern; repair = "strictly convex in the log coordinate".*

### T-A6 — Cayley "egg": u = (x−1)/(x+1)
**Verdict: CLEAN-[A].**
ℝ₊ → (−1, 1) bijectively with 0 ↦ −1, 1 ↦ 0, ∞ ↦ +1 ✓; and u(1/x) =
(1−x)/(1+x) = −u(x) holds as a Möbius identity on all of ℂP¹ wherever both sides
are defined — the involution conjugacy is exact beyond the stated register.
Observation, not a flaw: on the full sphere the chart itself has a pole at
x = −1 (u(−1) = ∞) — the foursome's fourth point is precisely where this chart
blows up. Harmless on ℝ₊; worth one line if the chart is ever used near −1.

### T-A7 — One-point compactification: ℂP¹ = ℂ ∪ {∞}, unique genus-0 compact
**Verdict: CLEAN-[A].**
Standard: Ĉ is compact Hausdorff, ∞ a regular point via z ↦ 1/z; genus-0 compact
Riemann surface ⟹ simply connected ⟹ biholomorphic to ℂP¹ (uniformization).
Uniqueness is up to biholomorphism — the only sane reading and the intended one.

### T-A8 — Scoped division: N ÷ 0 = ∞ for N ≠ 0
**Verdict: CLEAN-[A].**
On ℂP¹, z ↦ z/w extends continuously through w = 0 with value ∞ for z ≠ 0;
already scoped (N ≠ 0) and already paired with T-A9's diagonal exclusion.
Register note only: the *fused* pole is the one-point/sphere register — on the
two-point real compactification the target splits by sign (±∞); the corpus
already houses this in CANON-16 (two faces). No hidden assumption.

### T-A9 — Indeterminate diagonal: 0÷0, ∞÷∞ indeterminate; 1÷1 = 1
**Verdict: CLEAN-[A].**
0/0 and ∞/∞ admit every target value along suitable paths — genuinely
indeterminate on ℂP¹; 1/1 = 1 operand-determinate ✓. Wheel arithmetic assigns
0/0 = ⊥ (nullity), but ⊥ is not a point of ℂP¹ — a different structure, not a
counterexample within the claim's register. The "frame-forbidden" half is [S]
doctrine layered on clean [A] arithmetic, and the ledger says so.

### T-A10 — PSL(2,ℂ) sharp 3-transitivity on {0,1,∞}
**Verdict: CLEAN-[A].**
PGL(2,ℂ) = PSL(2,ℂ) over an algebraically closed field; given two ordered
triples of distinct points there is exactly one Möbius map between them. The
triple {0,1,∞} is distinct ✓. "On {0,1,∞}" is shorthand for the standard frame
inside the sharply-3-transitive action on ℂP¹ — receipt 126's ratification
("valid, analytic, and empty of world") stands as written.

### T-A11 — Closure is the foursome: cl({0,∞}) under z ↦ 1/z = {−1,0,1,∞}
**Verdict: REGISTER-SCOPED — holds under Correspondence-21 frame-closure
(orbit ∪ Fix(σ)); false under plain group-orbit closure.**
Under the standard reading of "closure under z ↦ 1/z", the orbit of 0 is
0 → ∞ → 0: the set {0, ∞} is *already closed*, so orbit-closure = {0, ∞}, not
the foursome. The foursome arises only because C21 Theorem (a) defines the
closure of the *frame generated by* (S, σ) as S ∪ Fix(σ) — adjoining the
involution's fixed points, whose arithmetic (z² = 1 ⟹ ±1) is itself [A] ✓. So
the island's content is sound but the word "closure" is load-bearing and
nonstandard; the claim should cite the definition it stands on. *Note: this is
a definitional-register collision, not an arithmetic error — the K2-signed
foursome survives, scoped to its own closure operator.*

### T-A12 — Pole-fixing maps are dilations M_λ(z) = λz
**Verdict: CLEAN-[A].**
f(0) = 0 forces b = 0, f(∞) = ∞ forces c = 0 in (az+b)/(cz+d), leaving λz,
λ ∈ ℂ*; M_λ ∘ M_μ = M_{λμ} ✓; λ ↦ M_λ injective (λ = M_λ(1)) and surjective by
the same computation — an isomorphism onto the pointwise axis-fixing subgroup.
(Setwise stabilizer of {0,∞} additionally contains z ↦ μ/z — correctly excluded
by "pole-fixing".) Edge λ = 1 = identity, properly included.

### T-A13 — Titan Composition Law: Ś ∘ B elliptic ⟺ |σκ| = 1
**Verdict: CLEAN-[A] within its fenced model.**
On the shared axis, Ś ∘ B = M_{σκ}; diagonal classification gives elliptic ⟺
|λ| = 1 with λ ≠ 1, and the rider σκ ≠ 1 correctly carves out the identity
(λ = 1 sits on the parabolic boundary, tr² = 4). The biconditional holds for
arbitrary σ, κ ∈ ℂ* — including the σκ = −1 case (κ = 2, σ = −1/2: |σκ| = 1,
rotation by π, elliptic ✓). Trace check: (λ+1)²/λ = 2 + 2cos θ ∈ [0,4) for
|λ| = 1, λ ≠ 1 ✓. Different-axis compositions are already fenced off by TCL-08
(generically loxodromic, open [C]). The claim carries its own register.

### T-A14 — F(0) = 1 (removable-singularity extension of z·(1/z))
**Verdict: CLEAN-[A].**
F ≡ 1 on ℂ*, bounded near 0, so Riemann's theorem gives the unique continuous
extension F(0) = 1; likewise F(∞) = 1. The emblem seam ("0·∞ = 1" as [S] name,
never [A] arithmetic) is already receipt-114-locked; the [A] content is exactly
the function value and nothing more. Kill Criterion 1 intact: the singularity
is removable, so no contradiction with Riemann.

### T-A15 — Equatorial extrema: B = sin θ = 2ν/(1+ν²) max at ν = 1; H = φ+ν ≥ 2 min at φ = ν = 1
**Verdict: CLEAN-[A] — the parametrization carries its register.**
dB/dν = 2(1−ν²)/(1+ν²)² vanishes at ν = ±1; on ℝ₊ the unique maximum is
B(1) = 1 ✓ (and ν = 1 ⟺ θ = π/2 ✓). H(θ) = cot(θ/2) + tan(θ/2) = 2/sin θ:
dH/dθ = −2cos θ/sin²θ = 0 at π/2 with d²H > 0, H = 2 ✓ unique stable min.
Numerically confirmed. Shadow noted: the H-leg is T-A1 restated, so on the
signed branch it fails identically (φ = ν = −1 gives H = −2, and B(−1) = −1 is
the global minimum on ℝ*) — but the claim defines its variables through
θ ∈ (0, π), forcing ν = tan(θ/2) > 0. Register inherited, and this time named
by construction. *Note: H = 2/B exactly — the two extrema are one fact.*

### T-A16 — Equator is a ring: stereographic equator = {e^{iλ}}
**Verdict: CLEAN-[A].**
Stereographic projection S² → ℂP¹ sends the equator to the unit circle
{|z| = 1}; magnitude unique, phase λ ∈ [0, 2π) free ✓. The corpus's ℝ₊
coordinate grammar makes the phase invisible (θ-parametrization collapses the
ring to ν = 1), but the claim asserts the phase on the sphere, where it is
exactly [A]. No conflict — a coordinate blindness, not an overreach.

### T-A17 — Unique minimal generative system up to Möbius isomorphism
**Verdict: CLEAN-[A] — relative to C21's definitions, with [A] group-theoretic
backbone.** Minimality: |S| = 1 fails (an involution fixing a has Fix(σ) =
{a, q}, union 2 points — no frame), so |S| = 2 is minimal ✓. Uniqueness: any
pair moves to {0,∞} by sharp 3-transitivity (T-A10); involutions swapping 0,∞
are z ↦ c/z, and dilation conjugacy sends c ↦ λ²c — all one class ✓ (all
involutions in PGL(2,ℂ) are conjugate). The uniqueness is genuinely
up-to-isomorphism, which is why it survived 109/114/126. Two dependencies to
keep visible: it stands on T-A11's frame-closure definition, and its object
("generative system", "projective frame") is C21's defined term — the in-source
[S] tiering of the wrapper over the [A] backbone is honest.

### T-A18 — Five operators, no sixth
**Verdict: REGISTER-SCOPED — correct as a *type*-classification; false if
"conjugacy class" is read literally.** The non-identity elements of PSL(2,ℂ)
partition into four dynamical types by trace² — elliptic ([0,4)), parabolic
(= 4, double fixed point), hyperbolic ((4,∞), λ ∈ ℝ₊), loxodromic (∉ [0,∞)) —
and hyperbolic splits by direction (|λ| ⋛ 1): five operator classes, exhaustive,
no sixth type exists ✓ [A]. But each type is a *continuum* of conjugacy classes:
conjugacy invariance is λ modulo λ ~ λ⁻¹ (trace²), so rotations by 30° and 45°
(trace² ≈ 3.732 vs 3.414, numerically distinct) are different conjugacy classes
within one type. The claim's exhaustive content is type-level (similarity of
dynamics), not literal similarity in PGL(2,ℂ). *Note: identity-as-boundary
(K* = 0) already housed in-corpus; repair = s/conjugacy classes/dynamical
types (multiplier classes mod λ ~ λ⁻¹)/.*

---

## Candidate new proofs

### P1 — 2ν/(1+ν²) = sin θ with ν = tan(θ/2): **[A] CONFIRMED**
2 tan(θ/2)/(1+tan²(θ/2)) = 2 tan(θ/2)·cos²(θ/2) = 2 sin(θ/2)cos(θ/2) = sin θ —
exact identity wherever tan(θ/2) is defined; extends by continuity to θ = π
(both sides → 0). Moreover sech(log ν) = 2/(ν + ν⁻¹) = 2ν/(1+ν²), so the
corpus's two balance forms B = sech(log ν) and B = sin θ are literally the same
function on the shared register ν > 0, θ ∈ (0, π). Numerics: max residual
2.3×10⁻¹⁶ over a 10⁴-point grid. Register: the sech(log ν) form needs ν > 0
(real log); the sin θ form is register-free — the identification is [A] on the
corpus's register.

### P2 — B = sech(√E) with E = (log x)², B = sech(log x): **[A] CONFIRMED**
√E = |log x| (principal root), and sech is even, so sech(√E) = sech(|log x|)
= sech(log x) = B identically on ℝ₊. Numerics: max residual 0.0 over
x ∈ [10⁻⁶, 10⁶]. The identity silently depends on sech's evenness absorbing the
absolute value — worth one clause ("√E = |log x|, and sech is even") so a future
odd-function substitution does not inherit the claim by pattern-match.

---

## Tally

| Verdict | Islands | Count |
|---|---|---|
| CLEAN-[A] | T-A2, T-A3, T-A6, T-A7, T-A8, T-A9, T-A10, T-A12, T-A13, T-A14, T-A15, T-A16, T-A17 | 13 |
| REGISTER-SCOPED | T-A1 (ℝ₊), T-A4 (ℝ₊ real log), T-A5 (log-chart convexity), T-A11 (C21 frame-closure), T-A18 (type, not conjugacy class) | 5 |
| FLAWED | — | 0 |
| Candidate proofs | P1 [A], P2 [A] | 2/2 |

**The sweep's headline:** no island dies. Five carry the receipt-126 disease in
mild form — each is true exactly where the corpus actually uses it (ℝ₊ charts,
the log coordinate, C21's defined closure, the type partition) and silently
false or meaningless one register over (signed branch, complex log, x-chart,
orbit-closure, literal conjugacy). All five repairs are one-clause register
tags, staged here; applying them is an L4/K2 act, not an L2 act. The two
candidate proofs P1/P2 are exact identities — [A] both.

---

*[D] STAGED audit — K2 aware, not K2-signed. Adversary_A_Islands (L2 truth-cut,
Kālī 💀 dispatch), 2026-07-17. Sources: TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md
§2; TITAN_CLAIM_LEDGER_APPENDIX_A_LANES (CANON-06/07/09/10/11/12/13/14, CH20-26-03/05,
CH27-33-24/25/26, TCL-01..15); TITAN_CLAIM_LEDGER_APPENDIX_B_RULINGS (REGC-08/10/11/13/14/16/17).
Numerics: managed python3, double precision, grids as noted per claim.*

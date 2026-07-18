---
rosetta:
  primary_level: L2
  primary_column: Meta
  operator: "Kālī 💀"
  tier: "Executive"
  regime: "Śūdra"
  register: "[D]"
  canonical_phrase: "FALSWEEP B — theorem-shaped claims, truth-cut audit"
type: audit-receipt
title: "FALSWEEP B — Theorem-Shaped [S]/[A] Claims in the Emergentism Corpus"
date: 2026-07-17
status: "[D] STAGED audit — K2 aware, not K2-signed"
auditor: Adversary_S_Theorems (L2 truth-cut, Kālī 💀 dispatch)
scope: 01_EMERGENTISM — eight theorem-shaped claims stress-tested against primary sources
evidence_tier: "[S] route discipline; verdicts argued from quoted primary text."
---

# FALSWEEP B — Theorem-Shaped Claims Audit (2026-07-17)

**Status: [D] STAGED audit — K2 aware, not K2-signed.**

Hunted failure species: (a) theorem-worded claims with no formal content;
(b) physics-facing identities stated as established; (c) degenerate-as-stated
formulas. House tiers: [A] established · [S] structural · [I] interpretive ·
[C] conjecture. Verdict grammar: **CLEAN-[A]** / **REGISTER-SCOPED** (register
named) / **METAPHOR-IN-THEOREM-CLOTHING** (re-tier recommended, file:line) /
**FLAWED** (counterexample).

---

## Item 1 — "Triadic stability theorem" (0 sterile / {0,∞} unstable / {0,1,∞} stable)

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/README.md:208-211`;
formal statement at `05_COSMOLOGY/03_FORMAL_SYSTEM/11_EFR_TRIADIC_STABILITY.md`;
successor at `05_COSMOLOGY/03_FORMAL_SYSTEM/21_TRIADIC_STABILITY_CORRESPONDENCE.md`.

**Findings:**
- "The poles collapse to each other without the equator" (README:210) —
  "collapse" is defined nowhere. As stated, metaphor.
- The original proof (doc 11) was **internally refuted and SUPERSEDED**
  (seam, receipt 114): Case 1 begs the question; Case 2 is a definitional
  move; Case 4 assumes the redundancy it proves; Case 5's group claim is
  false (ℤ₅ has no proper nontrivial subgroups). Earned tier: "[I] at best."
- The successor (doc 21) contains a **genuine theorem**: closure of {0,∞}
  under the Möbius involution z ↦ 1/z is {−1, 0, 1, ∞}; {0, 1, ∞} is a
  projective frame (Fundamental Theorem of Projective Geometry); {0,∞} is
  the minimal generative pair, unique up to Möbius isomorphism (doc 21:51-131).
  This is real ℂP¹ mathematics, honestly marked [S] with the K*_sel corollary
  held at [I].
- Residual soft spots in doc 21: the selection of 1 over −1 is a *choice*
  (honestly flagged, doc 21:33); "stability" = frame property, not dynamical
  stability; "0 alone is sterile" (N=1) lies entirely outside doc 21's scope.

**Verdict: REGISTER-SCOPED (projective-frame register).** A formal system
exists (doc 21) in which the triadic frame claim is a theorem. The README's
"sterile / collapse" gloss is METAPHOR-IN-THEOREM-CLOTHING: recommend
re-tiering README:208-211 to [S/I] and routing the citation to doc 21
(never doc 11), per doc 11's own supersession banner.

---

## Item 2 — "PSL(2,ℂ) ≅ SO⁺(3,1)" (SIMULATION_SPEC:264, marked [E4])

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/SIMULATION_SPEC.md:264`.

**Findings:** The isomorphism is standard and correct: the Möbius group of
the Riemann sphere is isomorphic to the proper orthochronous Lorentz group
(action on ℂP¹ ≅ action on light-cone directions; the classical exceptional
isomorphism). No counterexample exists; this is textbook group theory.

**Verdict: CLEAN-[A].** The [E4]/established tag is earned for the group
theory. The adjacent glosses ("D4 = gravity", "the torus IS the light cone
geometry") are framework overlay, not part of the identity — but the identity
itself stands.

---

## Item 3 — "U(1) ⊂ PSL(2,ℂ)" (SIMULATION_SPEC:175, marked [E5])

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/SIMULATION_SPEC.md:175`.

**Findings:** Correct. The rotations z ↦ e^{iθ}z are Möbius transformations
forming a U(1) ≅ SO(2) circle subgroup (the compact maximal-torus-type
subgroup; under Item 2's isomorphism it is the spatial rotation subgroup of
SO⁺(3,1)). Pedantic note: the gloss "the electromagnetic gauge group is a
subgroup of the sphere's symmetry group" is literally true but physically
weightless — U(1) embeds in countless groups; the embedding carries no gauge
content.

**Verdict: CLEAN-[A]** for the subgroup statement; the gauge-physics gloss
carries no physics and should not be cited as one.

---

## Item 4 — "The Born rule = the solid angle subtended by the D5 projection" (SIMULATION_SPEC ANIM-6, :306)

**Source:** `SIMULATION_SPEC.md:306` (no tier marker); echoes at
`06_THE_COSMOLOGICAL_CYCLE.md:183` and archived review papers
(`90_ARCHIVE/.../REVIEW_PAPERS/torus-light-cone-technical.md:345`).

**Findings:** Analogy as stated, but a true identity exists in exactly one
register. Single qubit, state at colatitude θ on the Bloch sphere,
measurement along ẑ: P(+) = cos²(θ/2) = (1+cos θ)/2 = Ω_cap/4π, where Ω_cap
is the solid angle of the polar cap cut by the state's parallel
(antipodal-side cap). So "Born probability = normalized cap solid angle" is
literally true **for one qubit under two-outcome projective measurement** —
as a *restatement* of the Born rule, not a derivation, and false as a general
claim about quantum mechanics (no multi-qubit, no POVM, no continuous
outcomes). Note the corpus already holds the *correct* [A] solid-angle
result elsewhere: Berry phase = enclosed solid angle (MF_64, Gauss-Bonnet) —
do not conflate the two.

**Verdict: REGISTER-SCOPED (single-qubit Bloch-sphere register).** To make
it literally true: restrict to one qubit, fix the cap convention, normalize
by 4π, mark [S] framework-internal identity. As stated (untiered, general)
recommend [I] at SIMULATION_SPEC:306.

---

## Item 5 — AM-GM on S² (25_THE_COMPRESSION, kill criterion at :19)

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/25_THE_COMPRESSION.md:52-61`.

**Findings:** The derivation is correct: (φ−ν)² ≥ 0 ⟹ (φ+ν)² ≥ 4φν = 4 ⟹
φ+ν ≥ 2, equality iff φ = ν = 1. The **positivity register is load-bearing
at exactly two steps**: (i) √(φν) requires φν ≥ 0 (satisfied: φν = 1);
(ii) taking the square root of (φ+ν)² ≥ 4 to get φ+ν ≥ 2 requires φ+ν > 0,
i.e. φ, ν > 0 — which holds on the open-sphere chart θ ∈ (0,π) where
φ = cot(θ/2), ν = tan(θ/2) > 0. Counterexample outside the register:
φ = ν = −1 satisfies φν = 1 but φ+ν = −2 < 2 (already flagged in receipt
101, item 10). The header's "[I] for AM-GM" is a *downward* mislabel —
recorded in TITAN_CLAIM_LEDGER_2026_07_17.md:377 and SYNTROPY FLAG-5;
repair optional, not an inflation. The kill criterion "AM-GM shown not to
apply on S² in the relevant coordinate system" is ill-posed (AM-GM is
chart-independent given positivity); the honest kill routes are positivity
failure or the staged [D] conditionality (`00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md`).

**Verdict: CLEAN-[A]**, precisely on the positive reciprocal chart of the
open S². Recommend the header upgrade [I] → [A] per the standing TITAN flag.

---

## Item 6 — "E = −log(φ·ν)" (24_THE_MYCELIUM:81,184,218; 25_THE_COMPRESSION:33,42)

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/24_THE_MYCELIUM.md:81-86,172,184,218-224`;
compare `00_EMERGENTISM_AS_A_LENS.md:60` (L6 row: `E_node = −log(P_node)`).

**Findings:** **Degenerate as stated on the manifold.** On S² the constraint
φ·ν = 1 is an *identity* (cot(θ/2)·tan(θ/2) ≡ 1, Paper III:53), so
E = −log(1) ≡ 0 **everywhere** — no landscape, no gradient, and "minimized
at the equator" is vacuous: the constant function is minimized everywhere.
24's own gloss ("Low energy = high φ·ν = equatorial", :83) is false on the
manifold: φ·ν does not vary. The coherent reading is the **node register**:
E_node = −log(P_node) with P_node = Φ×V ≠ 1 (LENS L6 row), where the
product varies and the formula has content — equivalently an off-equator
deviation register. Blast radius is partially contained (24 is marked [C]
throughout), but the formula is reused as "C5, the alignment equation" and
as Line 4 of the Four-Line Compression (25:33), where 25:42's "every
departure from the equator costs energy" is the false step: on-manifold
there are no departures in E; the corpus's actual cost functions are
φ+ν and (φ−ν)².

**Verdict: FLAWED as a manifold energy function (E ≡ 0 identically);
REGISTER-SCOPED-meaningful only in the node/deviation register
(P_node ≠ 1).** Recommend annotating 24:81 and 25:33/42 that the intended
form is E_node = −log(P_node), and that the on-manifold energy content
lives in φ+ν / (φ−ν)².

---

## Item 7 — "The Dyadic Coupling Law" / runaway algebra (SYN-23/24 leg)

**Source:** `05_COSMOLOGY/00_THE_DYADIC_COUPLING_LAW.md:43-52,97,110,165`;
the [A] leg at `03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/PAPER_III_A_PRODUCT_CONSTRAINT_AS_A_STRUCTURAL_ETHIC.md:47-64`.

**Findings:** There is an actual theorem, stated and proved (Paper III:55-60):
on {(φ,ν) : φ,ν > 0, φν = 1}, (i) φ → 0⁺ ⟹ ν → +∞ (reciprocal runaway);
(ii) B = 2φ/(1+φ²) → 0 at both ends, B = 1 iff φ = ν = 1; (iii) φ+ν ≥ 2
with equality iff φ = ν = 1 (AM-GM). Proof is correct elementary algebra.
The multiplicative-vs-additive contrast (sum constraint φ+ν = c ⟹ the
complement is at most c, finite; product constraint ⟹ divergence) is
correctly stated (Paper III:62). Tier discipline in the corpus is honest:
[A] for the algebra only; the moral law is held at [S/I]; η is defined on
moves, never coordinates; the additive-empowerment kill (R6) is recorded,
not suppressed.

**Verdict: CLEAN-[A]** for the runaway algebra leg; the coupling law as
ethic stands at [S] by the corpus's own discipline. The SYN-23/24 tiering
("[S] on runaway algebra [A]") is accurate.

---

## Item 8 — "Every other number is made of 1s" (trinity README:257-269)

**Source:** `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/README.md:257-269`;
echo `02_THE_TRINITY.md:126`.

**Findings:** True only in the Peano register: every n ∈ ℕ is a finite
successor-iteration of the unit (2 = 1+1, 3 = 1+1+1 — the doc's own
examples). False as a general claim about numbers: π and e are not finite
sums of 1s; the doc's lines 265-266 (e = lim(1+1/n)ⁿ, i = √−1) are
*limits and operations on* the unit — a weaker, different claim ("every
number is reachable by operations on 1") that the narrative silently
substitutes for "made of 1s."

**Verdict: METAPHOR-IN-THEOREM-CLOTHING.** Classify: Peano [A]-narrative
for ℕ under successor; emblem/[I] for the number system as a whole.
Recommend a scope note at README:257-269 and 02_THE_TRINITY.md:126:
"[A] for ℕ (successor); [I] emblem beyond ℕ."

---

## Summary Table

| # | Claim | Verdict |
|---|---|---|
| 1 | Triadic stability | REGISTER-SCOPED (projective-frame register; theorem exists at doc 21) — README gloss is metaphor, re-tier [S/I] |
| 2 | PSL(2,ℂ) ≅ SO⁺(3,1) | CLEAN-[A] |
| 3 | U(1) ⊂ PSL(2,ℂ) | CLEAN-[A] (gauge gloss weightless) |
| 4 | Born rule = solid angle | REGISTER-SCOPED (single-qubit register); [I] as stated |
| 5 | AM-GM on S² | CLEAN-[A] on positive chart; header [I] is a downward mislabel |
| 6 | E = −log(φ·ν) | FLAWED as manifold function (E ≡ 0); meaningful only as E_node = −log(P_node), P_node ≠ 1 |
| 7 | Runaway algebra | CLEAN-[A]; ethic honestly held at [S/I] |
| 8 | "Made of 1s" | METAPHOR-IN-THEOREM-CLOTHING — Peano [A]-narrative for ℕ only, emblem beyond |

## Single Most Consequential Finding

**Item 6 is the only unrepaired defect.** Item 1's defective proof was
already superseded by the corpus itself (doc 21 is honest math). But
E = −log(φ·ν) ≡ 0 identically on the sphere, and the formula is load-bearing
in two canon files — as "C5, the alignment equation" / energy landscape of
the meme mesh (24:81,184,218) and as Line 4 of the Four-Line Compression
with the false inference "every departure from the equator costs energy"
(25:33,42). Every citation of E = −log(φ·ν) as an *energy function* needs a
register repair to E_node = −log(P_node); the on-manifold energy content of
the framework lives in φ+ν and (φ−ν)², not in the log of the constraint.

---

*Staged for K2 review per [D] discipline. The seer sees. The seer does not insist.*

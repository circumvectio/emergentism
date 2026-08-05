---
title: "What Is Proved — [A] only"
status: "PROJECTION — rules nothing"
date: 2026-08-05
semantic_ownership: "Source documents retain semantic ownership. This file reports; it rules nothing, ratifies nothing, creates no second owner, and promotes no tier. Where this file and a source disagree, the source governs and this file is the defect."
evidence_tier: "[A] only — analytic, inside stated definitions and premises, or machine-checked at one remove. No entry is carried above the tier its source assigns it. Every unratified source carries its status on the same line as the claim."
supersession: "This projection is part of a dated successor edition to 07_THEOLOGY/00_THE_AMRITA.md (DISTILLATION, 2026-07-03, recovery-integrated 2026-07-19). That file already implements this structure — 72 nectar / 48 halāhala across 12 lanes — and predates every ruling cited here. Until the supersession line is written INTO it, two distillations stand and give two answers. That is unfinished, and it is stated here rather than left to the reader."
---

# What is proved

**No entry in this file is owned by this corpus.** Every [A] result below belongs to Euclid, Dedekind, Cantor, Russell, Zermelo, von Neumann, Hardy & Wright, Möbius, Klein, Lagrange, Hermite, Lindemann, Napier, Euler, Cauchy, Mac Lane, Peano, Galois, Presburger, Tarski, Steenrod, Laplace, Legendre, Cartan, Killing, Witten, Atiyah, Hirzebruch, Lotka, Volterra, Glashow–Weinberg–Salam, or to ordinary universal algebra, ring theory and field theory. What the corpus contributed is the checking, the fences, and — in several entries — the refutation of something it had itself published.

After the 2026-08-05 prior-art sweep the corpus's own delta is one sentence, and its own receipt states it, verbatim, at `05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md:155-158`:

> "the observation that the two syntactic exclusions (`ιι = id`, `ι(1) = 1`) are *the same constraint* as the classical `a_n ≥ 2` normalisation — an expository identification, `[I]`, of real pedagogical value and no theorem content."

That is `[I]`. Being `[I]`, it does not enter this file. **This file therefore contains zero results owned by this corpus.**

---

### The bound, declared before the entries were written

The corpus's own rule B2 — declare the shape, not the number, so a reader can recompute whether it was honoured (owner: Lan–DeMets; O'Brien–Fleming; ICH E9) — applied to this projection.

- **Admission function:** stated tier; stated kill (or `[A]` with prior art named); kill not fired; one adversarial pass survived (or `[A]` with prior art); real owner named in the same line as the claim. This file additionally admits **`[A]` only**.
- **Deduplication rule:** one finding, one entry, wherever it appeared across the assembling sweeps. This is the corpus's rule S3 — "agreement between two framings is one claim twice" — applied to the pipeline that produced this file, which multiply-counted several findings before this gate ran.
- **Expected admissions:** 12–20. **Actual: 19.** Folded, re-filed or rejected rather than admitted: 20+, listed at the foot with reasons.

### Non-ratification

Inclusion here confers no tier and ratifies nothing. `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md` and `49_THE_THREE_MODES_OF_COUNTING.md` are **STAGED PROPOSAL — unratified**; `THE_BOUNDARY_RULES_STANDALONE.md` is **DRAFT 1**, tier `[D]`, `not_a_gate`; `55` is ACTIVE but its verdict has not propagated. None of the twelve files added on 2026-08-05 appears in `FILE_REGISTER.json`, and a grep of `00_META/` and the record ledger for them returns zero hits each. This projection is downstream of a register that has not yet recorded its sources.

### What "machine-checked" means here — at one remove, every time

The Lean file was **not** recompiled in this pass: a `lake build` was started, began pulling ~224 MB of mathlib into an iCloud-synced tree, and was killed; the working tree was left clean. The recorded successful build is `11_UPLINK/50_AUDITS_AND_EXECUTIONS/182_C_HAT_IS_NOT_A_RING_MACHINE_CHECKED_2026_07_29.md` ("8661 jobs, 20 theorems, no sorry", four axiom-free traces). The file's last commit (`31fa4533`, 2026-08-01) **postdates** that build; the diff is a two-line docstring change touching no theorem statement and no proof term.

Re-verified directly in this pass at `09_TOOLS/05_FORMAL_VERIFICATION/`: `grep -c '^theorem' EmergentismCheck.lean` = **20**; `lean-toolchain` = `leanprover/lean4:v4.33.0-rc1`; `lake-manifest.json` pins mathlib at `932a58b04d34`. On stubs: `grep -nE 'sorry|admit'` returns **three** hits, all prose — line 7 ("There is no `sorry` in this file"), line 150 ("proved is"), line 207 ("admits"). No proof term is stubbed. The earlier sweep line "no `sorry` in the file (verified by grep)" is restated here with the actual pattern, count and disposition, because a provenance line that rounds is the defect this projection is downstream of.

---

## I. [A] results that refute claims this corpus published

**1 · Existence of a multiplicative identity is NOT forced — the published F2 was false.** Uniqueness is the theorem (`at_most_one_identity`; owner: standard algebra, textbook folklore — e·e′ = e′ and = e). Existence is not: the constant operation on Bool has no two-sided identity, and of the sixteen binary operations on a two-element set, twelve admit none (`existence_not_forced`, machine-checked at one remove). Owner of the mathematics: elementary universal algebra. Owner of the error: the corpus.
· src `09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean:105,116`; `00_META/00_SETTLED_CANON_REGISTRY.md:78` (KSC-28)
· kill: exhibit a structure with two distinct two-sided identities. Not fired.

**2 · The corpus's own falsifier is stronger than the corpus knew — its premise is already impossible.** 0·w = 0 in any ring, so 0·w = 1 forces 1 = 0; no associativity is needed (`falsifier_premise_impossible`, machine-checked at one remove, strictly subsuming `associativity_falsifier`). Owner: standard ring theory.
· src `EmergentismCheck.lean:186` (subsuming `:174`)
· kill: exhibit a nontrivial ring with 0·w = 1. Not fired.

**3 · Ĉ is not a ring, and the REASON is what is proved.** No nontrivial ring admits an additively absorbing element — w + 1 = w forces 1 = 0 — and the point at infinity must absorb; instantiated at ℂ. Owner: standard ring theory (additive cancellation). Scope, from the file's own §7 and travelling with it: ℂP¹ is never constructed in the file and mathlib's `Projectivization` is never used, so nothing here is a statement about that library.
· src `EmergentismCheck.lean:193,202,209`
· kill: exhibit a nontrivial ring with w + 1 = w. Not fired.

**4 · Fixing both boundary points fixes no third point.** The stabiliser of {0, ∞} in PGL₂(ℂ) is {z ↦ λz} ∪ {z ↦ λ/z}, λ ≠ 0, and that group acts **transitively** on ℂ* — for any w ≠ 0 take λ = 1/w. Owner: standard PGL(2,ℂ) theory (Möbius, Klein); the application against the corpus is the corpus's. This refuted, on the day it was written, the proposed mathematical home for the three retired Titan equations (forms not reproduced — retired 2026-08-01 as ill-typed, refuted 2026-08-05 in content). Sharp 3-transitivity does not rescue it: it applies to any three distinct points and so privileges none. The source forbids a weakened rewrite — "There is no salvage sentence."
· src `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md:147-186` — **STAGED PROPOSAL, unratified**; ratified only in the weaker KSC-04 form at `00_META/00_SETTLED_CANON_REGISTRY.md:54`
· kill: exhibit a stabiliser of {0,∞} that is not transitive on the complement. Not fired.
· **Counted once.** This is the projection's single entry for this result; elsewhere it is cited, not restated.

**5 · Reciprocation fixes ±1, so a three-mark picture has a fourth mark it is not drawing.** ι(x) = 1/x fixes exactly ±1 (`inversion_fixed_iff`, machine-checked at one remove — solve x² = 1); (−x)⁻¹ = −(x⁻¹) (`involutions_commute`); and {id, neg, ι, neg∘ι} is a Klein four-group — **Felix Klein**, stated at 48 §4.1 and *not* in the Lean file. Consequence recorded by the corpus against itself: the orbit of {0,∞} under reciprocation is just {0,∞}, so a distinguished unit is **adjoined by naming, not forced by closure**.
· src `EmergentismCheck.lean:35,137`; `48:177-181` (**STAGED PROPOSAL, unratified**); `00_META/00_THE_CLAIM_STATUS_REGISTER.md` DF-09
· kill: exhibit a third fixed point of z ↦ 1/z. Not fired.

**6 · Line 4 was published at [S] Established and is false.** Under the constraint that makes it a register, −log(φ·ν) is identically zero at *every* latitude, so it has no minimum and locates nothing; four published consequences fall with it, including "every displacement from the equator costs energy". Repaired, not deleted: E = φ + 1/φ − 2 = (√φ − 1/√φ)² = 4 sinh²(s/2) ≥ 0, zero exactly at the equator. Owner: elementary; AM–GM is **Cauchy (1821)** and the hyperbolic form is classical.
· src `11_UPLINK/50_AUDITS_AND_EXECUTIONS/191_LINE_4_REFUTED_AND_THE_CITATION_DEFECT_2026_07_30.md` §1
· kill: exhibit a latitude where −log(φ·ν) ≠ 0 while the constraint holds. Not possible.
· **live defect, not a death:** the refuted expression is still standing in a live register — `08_FRAMEWORK_SUPPORT/00_KNOWN_UNKNOWNS.md` KU-7 reads "The Lagrangian already exists: E = -log(phi*nu)."

**7 · Four load-bearing lemmas, each killed by one counterexample.** (i) "Any group with N ≥ 4 elements has proper subgroups" is false — ℤ₅, or any prime-order group, has none, by **Lagrange**; the N ≥ 5 branch of "N = 3 is the unique stable count" was discharged solely by it, so N = 3 is *selected*, not derived. (ii) The Lotka–Volterra "basin of attraction" does not exist: classical LV is conservative (**Lotka 1925, Volterra 1926**), its interior equilibrium a neutrally-stable centre; only the *time-average* equals 1. (iii) "All paths on S² are helical" is refuted by a meridian — a great-circle geodesic with dφ = 0 (elementary differential geometry). (iv) "Algebraic closure implies simple-connectedness" is refuted by the torus — a smooth projective curve over ℂ with π₁ = ℤ² (classical Riemann-surface theory). What did **not** fall is recorded in the same audit: η = 0 survives, because canon carries it as a conditional gate rather than as a consequence of the count.
· src `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS.md` §2.1–2.4 (K2-countersigned 2026-07-12)
· kill: each is an exhibited counterexample; none can be un-exhibited.

**8 · Gödel's incompleteness does not lift universally.** Presburger arithmetic (**Presburger, 1929**) and the theory of real-closed fields (**Tarski, 1948–51**) are both complete and decidable — two standard counterexamples inside the claim's own declared system. Successor, narrow and honest: Gödel survives as apparatus, never as law.
· src `00_META/00_THE_CLAIM_STATUS_REGISTER.md` DF-12
· kill: none — the decidability results are theorems.

**9 · A limiting claim that flattered the corpus was retracted, because the limit was argued wrongly.** "An SU(3) gauge theory cannot be defined over S²" is **false**: a gauge group's dimension is an internal-fibre fact and need not equal the base dimension, and principal SU(3) bundles over S² are classified by π₁(SU(3)), which is trivial — so the bundle exists and carries nonzero connections and curvature. Owner: standard fibre-bundle theory (clutching construction; **Steenrod, 1951**). What survives is narrower and true: sphere topology and the reciprocal chart alone underdetermine a physical gauge theory, and the scalar-Laplacian degeneracy claim stands — see 10.
· src `03_METHODOLOGY/02_THE_PAPERS/PAPER_P_SU3_OBSTRUCTION_BARE_S2.md` (retraction 2026-07-20)
· kill: none outstanding — the bundle exists.

**10 · All four declared routes from S² to the Standard Model are blocked, and the strongest block is one line.** **Path C (parity):** the multiplicities of the S² Laplacian are 2l+1 = 1, 3, 5, 7, … — always **odd**; dim SU(3) = 8 is **even**; so SU(3) can never appear as a spectral multiplicity, at any l, at any resolution. Owner: classical spectral theory of the Laplacian on S² (**Laplace, Legendre**; representation theory of SO(3)), with **Cartan/Killing** for the Lie-algebra dimensions. Four embedding checks also fail (8 > dim SO(3) = 3, > dim SU(2) = 3, > dim PSL(2,ℂ) = 6, > dim SO(4) = 6). **Path A** passes the gauge-group dimension count (**Witten, 1981** — 7 is the minimum dimension for a compact manifold whose isometry group contains SU(3)×SU(2)×U(1)) and then dies to the **Atiyah–Hirzebruch chirality no-go (1984)**: pure Kaluza–Klein on any smooth compact M⁷ gives vector-like spectra, never chiral. **Path B** dies three ways (Liouville's continuous spectrum cannot give discrete root systems; Virasoro ≠ Yang–Mills; the closed bosonic string at D = 26 gives a graviton and no spin-1 gauge bosons). **Path D** returns a negative from convex geometry: the AM–GM half-plane has 1 facet and 0 extreme rays, the quadrant-restricted wedge 2 direction rays — 0, 1 or 2, never 4. Separately, the force bijection is refuted from outside the framework: electroweak unification (**Glashow–Weinberg–Salam**) makes two of the four "lines" one interaction above ~246 GeV. **What survives, named in the same table:** gravity via PSL(2,ℂ) ≅ SO⁺(3,1); U(1) from l = 0; SU(2) from l = 1 (2l+1 = 3 = dim SU(2)).
· src `11_UPLINK/50_AUDITS_AND_EXECUTIONS/119_LAGRANGIAN_QUESTION_CLOSED_ALL_FOUR_PATHS_RUN_PENDING_K2.md:25,72-76,99-106` (K2-countersigned 2026-08-04); `118_COMPUTATIONAL_RESULTS_FOUR_EXPERIMENTS.md`; `117_PATH_D_NEGATIVE_RESULT.md`; `00_META/00_THE_CLAIM_STATUS_REGISTER.md` DF-01, DF-10
· kill: exhibit an even multiplicity of the S² Laplacian, or a smooth compact M⁷ Kaluza–Klein construction with a chiral spectrum. Neither exists.
· **not admitted from the same document:** the "c = 25 as AM–GM saturation" chain to 26. It is a numeric coincidence read as a derivation with no exhibited map — the class the corpus's own DF-20 types CATEGORY-ERROR.
· **register gap, stated rather than hidden:** grepping `00_THE_CLAIM_STATUS_REGISTER.md`, `00_SETTLED_CANON_REGISTRY.md` and `00_ESTABLISHED/README.md` for this closure returns only DF-10, which covers the force bijection via receipt 117 alone. The largest signed negative result in the corpus is in no register three weeks after countersignature, and `00_KNOWN_UNKNOWNS.md` KU-6 still reads "SU(3) problem — Reopened".

## II. [A] results that stand, all inherited

**11 · a/0 is *no such element*, and the reason is algebraic, not a matter of limits.** For a ≠ 0 in any field there is no y with 0·y = a (`no_quotient_by_zero`, machine-checked at one remove; owner: the field axioms — 0·y = 0 follows from distributivity). The same undefinedness holds in GF(7), a field with no topology, no sequences and no approach at all (finite-field witness: **Galois**) — which retires "division by zero is undefined because the limit is never reached". *Footnote, not a second finding:* mathlib **defines** a/0 = 0 as a junk value (`div_zero`), a convention of that library, recorded so that no proof assistant is ever cited as agreeing that a/0 has a solution.
· src `EmergentismCheck.lean:23,30`; `49_THE_THREE_MODES_OF_COUNTING.md:181,239` (**STAGED PROPOSAL, unratified**); `53_THE_NUMBER_CHART.md:123-126`
· kill: exhibit a field with 0·y = 1. Directly refuted in the same file.

**12 · G1 — reachability from 1 under S(x) = x+1 and ι(x) = 1/x is exactly ℚ⁺.** Owner: **Euclid** — the descent is the Euclidean algorithm; the presentation is **Stern (1858) / Brocot / Calkin–Wilf (2000)**, and the source states this itself. With the asymmetry (G6/G7): ι alone generates {1}; S alone generates ℕ⁺ and never falls below 1; only together do they give ℚ⁺, so the descent toward zero exists only as the reciprocal image of the ascent. G4 is **not** admitted separately — it is the (⊆) half of this restated, and its declared kill cannot fire, the evaluator's codomain being ℚ⁺.
· src `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md:130-140,223-246`; `09_TOOLS/01_SCRIPTS/check_generative_base.py` re-run 2026-08-05, exit 0
· kill: exhibit q ∈ ℚ⁺ reachable by no finite word, or a word whose value is irrational. Not fired.

**13 · G3/G5 — zero and unboundedness are approached and never reached, and the reason is the finiteness of words.** No finite word attains 0, and not merely by omission: ι(x) = 0 has no solution at all. Both limits are approached in the declared real embedding — val(Sⁿ) = n+1 → ∞ and val(Sⁿι) = 1/(n+1) → 0. Owner: elementary positivity induction; classical. The typed endpoint names are declared extended-real names and explicitly not Titan terms (52 §3.1); that firewall is what keeps this `[A]`.
· src `52:190-214`
· kill: exhibit a word with value 0, or a neighbourhood of 0 or ∞ containing no reachable value. Not fired.

**14 · The log coordinate sees exactly one point of the generative base.** Under s = log x, ι becomes s ↦ −s — true, but it carries completion to ℝ as a premise, because log q is **transcendental** for every rational q ≠ 1 (**Hermite 1873, Lindemann 1882**). Every reachable value except the centre leaves ℚ. The finding is the demotion: on 2026-07-29 the corpus used a classical theorem to move its own claim off a flat `[A]`.
· src `52:253-272`
· kill: would require refuting Hermite–Lindemann. Not fired.

**15 · As Möbius maps every word has determinant ±1 — so the coordinate the corpus borrowed is not generated by its own base.** S = [[1,1],[0,1]] (det +1) and ι = [[0,1],[1,0]] (det −1), so every word has det ±1; owner: **Möbius**, standard PGL(2,ℚ) theory. The imported hinge u = (x−1)/(x+1) is [[1,−1],[1,1]], det 2, and 2λ² = ±1 has no rational solution. And the same session's claim that the determinant *is* the fork was retracted in place: determinant and sign are independent obstructions, witness n∘ι : x ↦ −1/x, which has det +1, passes the determinant test, and is still not a word, because every word's value lies in ℚ⁺.
· src `52:275-340`
· kill: an error in the determinant argument, or a collapse of the four-quadrant table. Not fired.

**16 · The unit, three inherited facts.** (N1) 1 is the unique additive irreducible of (ℕ⁺,+) — n ≥ 2 splits as 1 + (n−1), 1 does not — and therefore (N2) {1} lies in every additive generating set; owner: elementary semigroup theory, **Peano/Dedekind** lineage. N2 follows immediately from N1, so the source's phrase "FIVE independent theorems" is an overcount: five statements, not five independent theorems. (N3, structural half only) (ℕ⁺,+) is the free semigroup on one generator and (ℕ,+) the free monoid whose identity is 0 — standard universal algebra; the naming question is `[S]` and does not enter this file. (N4) ℤ is **initial in Ring**: exactly one ring homomorphism ℤ → R, n ↦ n·1_R; owner: standard algebra and category theory, **Mac Lane**. Read N4's kill, never its prose gloss — "nothing else in any ring does that" is false as worded, since −1 also additively generates (ℤ,+).
· src `53_THE_NUMBER_CHART.md:53-57,74,77,83`
· kill: exhibit a generating set of (ℕ⁺,+) not containing 1; or a unital ring with a second ring homomorphism from ℤ. Not fired.

**17 · "0 is not a number" is false, and the phrasing is banned by signed ruling.** 0 **is** a real number; what is true is 0 ∉ ℝˣ — 0 is the unique element of a field with no multiplicative inverse. Say ℝˣ, never ℝ. The partner clause is a theorem, unqualified: ∞ ∉ ℝ, entering only by declared compactification — and ℝP¹ (one unsigned point) and [−∞,+∞] (two ordered endpoints) are **different constructions, not variants**. Owner: standard field theory and standard analysis. The correction and its cost are the corpus's: the owner's most quotable sentence can never again be published bare.
· src `53:78,80`; `00_ESTABLISHED/README.md:121`; `11_UPLINK/50_AUDITS_AND_EXECUTIONS/193_FIVE_RULINGS_SIGNED_2026_07_31.md` §5.1 (signed, natural person)
· kill: exhibit a field in which 0 has a multiplicative inverse. Not fired.

**18 · Absorption is the property that discriminates: V ∪ {x} = V, literally, as classes.** For finite S, |S ∪ {x}| = |S| + 1 ≠ |S|; at the totality, adjoining an element changes nothing. Owner: **Richard Dedekind, *Was sind und was sollen die Zahlen?* (1888)** — a set is infinite exactly when equinumerous with a proper subset of itself; named in the source. Cantor's absolute is company, not evidence, and the source refuses to upgrade it.
· src `49:61-84,234` — **STAGED PROPOSAL, unratified**
· kill: exhibit a finite set unchanged by adjoining a new element. Not fired.

**19 · Non-self-membership discriminates nothing, and Russell's set is not available.** Under Foundation no well-founded set is a member of itself (**Zermelo; von Neumann**), so "ℝ ∉ ℝ" is true of ℕ, ℝ, ∅ and every set — it cannot identify anything, and must not be led with. And {x : x ∉ x} is **Russell's (1901)** set: it provably does not exist as a set, and under Foundation the qualifier is vacuous. The barber does not loop; the barber does not exist, and the argument is a proof by contradiction, not a description of an oscillating thing. This one fact killed three separate seat proposals in a week, each named on the record.
· src `49:76-80,178-180,235-238` — **STAGED PROPOSAL, unratified**
· kill: exhibit a well-founded set that is a member of itself; exhibit Russell's set. Not fired.

---

## What is not here, and the list is the point

**φ·ν = 1, in every form** — the "keel", the complementary-angle identity tan A · tan(π/2 − A) = 1 (classical trigonometry, Euclid/Thales lineage), and the curve-bound reciprocal chart. It is **one identity**, and it is filed **once, on the halāhala side**, not here: `00_META/00_THE_CLAIM_STATUS_REGISTER.md` DF-05 types it CATEGORY-ERROR with **no successor owner** — one of only two rows so classified — and `07_THEOLOGY/00_THE_AMRITA.md:68` already carries it there. The fence travels with it in the same breath: it holds only because ν is *defined* as 1/φ; let the two vary independently, φ = n and ν = k/n, and φν = k exactly, for any k, and the two-variable limit at the corner does not exist. And in the empowerment register the composition is **additive** — E = H(S) − H(S|A) is a difference of entropies, φ·ν is the tautology 2^E, and φν = 1 marks the **dead state**, not the balanced ideal (`03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/R6_CONJUGATE_RESULTS.md`; owners Shannon; Klyubin/Polani/Nehaniv).

**G2** — proved 2026-08-05 and, in the same act, found to be prior art: the uniqueness of the finite simple continued fraction with last partial quotient ≥ 2, owner **Hardy & Wright, *An Introduction to the Theory of Numbers*, Ch. X** (also Khinchin §I.2, Perron), with **Euclid**'s algorithm underneath. Its home is the necrology, not a proved-findings column, because the proof extinguished the novelty; `55` §7 and `42`'s F1 note both forbid citing it as passing F1. **Publication block, both paths cited so this file asserts no register state the register denies:** `00_ESTABLISHED/README.md:100` still lists G2 as an "open general claim" and `:114` still reads "G2 remains open until a complete proof or formalization lands," against `55_G2_PRIOR_ART_ADJUDICATION.md`. Carried against the corpus's interest: `55:107-109` records that the Hardy & Wright theorem *number* was never checked against a physical copy.

**(log x)² ≥ 0 with equality at x = 1** — "log x = 0 iff x = 1 wearing a square" (**Napier/Euler**). Excluded as a restatement, together with `negation_fixes_zero`, `negation_swaps_units`, `projection_at_45`, `inversion_fixed_units` and `orbit_product`. All remain true and remain in the file; none is a finding.

**`unique_positive_fixed_point` over ℝ⁺** — not a second theorem. It deletes one root from entry 5; and the ℚ⁺ restriction is one line of ordinary reasoning that is **not** in the Lean file (`52:86-92`), so "machine-checked" may not be said flatly of the ℚ⁺ version.

**AM–GM under a declared budget** (**Cauchy, 1821**) — trivial and inherited; the source itself tiers the domain-general Saturation-Contrast claim `[C]` and "unearned". The discipline around it is method, not a proved finding. **A locally pure-gauge potential has zero local field strength** (**Poincaré/Cartan**, d² = 0) — standard gauge theory, load-bearing on nothing here.

**The Lorentz–Möbius correspondence**, compressed to its one owned clause: SL(2,ℂ) double-covers SO⁺(3,1) and PSL(2,ℂ) ≅ the Möbius group (**Möbius, Klein**); circle-preservation on the sky is **Terrell** and **Penrose**, both 1959; β = tanh(rapidity) is **Einstein/Minkowski/Whittaker**. It is entirely other people's physics, and the only corpus-owned content is the refusal to call it a derivation.

**The category error read three-fold** — the type facts are `[A]`, but the middle limb (a *collection* offered where a *member* is required) is true only if the middle mark denotes the realm, and that referent is contested on disk, resting on a same-day owner act whose recorded warrant is the generic completion instruction that the same day's audit named as the day's clearest instance of the corpus's named failure mode. Not admissible to an `[A]`-only file while the sort of its subject is contested. `48:354-395`, `49:144-169`.

**F0** is marked **NOT PASSED** — its required negative tests are three `assertIn` substring assertions on prose; nothing type-checks. **F1** is **OPEN**, its first and only adjudicated candidate having failed. **The three Titan equations** are dead twice (ill-typed 2026-08-01; false in content 2026-08-05) and × and / between the boundary marks are banned; the standing agent memory "restored by proof on ℂP¹" is **stale and contradicted by disk**. **The potential reading** — realm as finite potential, ground with none, horizon with all and none — is **not on disk**: grep across all live files returns nothing, so it has no source path, no tier, no kill and no adversarial pass, and admitting it from a brief would have made this projection a second owner in its first act.

## What this file may not be cited for

F0 as a gate cleared — it is NOT PASSED. F1 as passed — it is OPEN, first candidate adjudicated prior art. F2, F3, F4 — not started. Any aggregator as established: KSC-02 adopts min as a working score and retires the product as a ranking. P = Φ×V — an AND-class law, not a proved product, and explicitly not established. η = 0 — a conditional gate, not a consequence of any count. The efficacy of the honesty protocol — `[C]`, never run as a controlled trial. The four-status teachability test — designed, never run. The Rosetta, the D-ladder and the μ-contract (μ₂ and μ₃ adjudicated **FAILED**), the Titan ontological reading, the Justice formulae, the 5+1 Constitution, the paradox dissolutions, and the Samudra Manthan itself — none of them can pass this gate, and the last of those is the metaphor this projection is named for. The vessel is not one of the drops.

None of that is thereby false. It is unchecked, or selected, or interpretive, and those are different things from false. This file exists so that the difference cannot be blurred by fluency.

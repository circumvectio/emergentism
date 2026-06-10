# Frames, Not Operands: A Structural Signature Across Arithmetic, Set Theory, and Semantics

**Yves R. Burri**

*Draft v1 — 2026-06-10. External register: no framework-internal vocabulary. All citations require verification against the original texts before submission (see Verification Note at end).*

---

## Abstract

Formal systems repeatedly distinguish two roles an item can play: *operand* — an object the system's operations act upon — and *frame* — an item constitutive of the operation space itself. We argue that a recurring structural signature marks the frame role across at least three registers. (i) In set theory, proper classes exist and classify but cannot be members; the axiom schema of restricted comprehension and the axiom of foundation jointly forbid the totality and self-membership constructions that generated the classical paradoxes. (ii) In logic and semantics, Tarski's undefinability theorem and Gödel's second incompleteness theorem (the latter via Löb's theorem) show that a system's truth and consistency resist internalization as ordinary predicates; the rigorous common core of this family is Lawvere's fixed-point theorem. (iii) In arithmetic, 0 and ∞ behave as boundary items: projective compactification renders ∞ an ordinary point of the Riemann sphere, yet the forms 0/0, ∞/∞, and 0·∞ remain undefined — precisely the expressions in which two boundary items are composed with one another. We articulate the shared signature in three criteria, observe that every historical resolution in all three registers takes the same form — stratification — and propose the frame/operand distinction as a unifying *taxonomy*, explicitly weaker than a reduction: only the logical family is unified by a theorem; the arithmetic and set-theoretic cases are argued to exhibit the same signature, not derived from the same lemma. The taxonomy yields a modest predictive heuristic: paradox-like pathology is to be expected wherever a formalism is asked to internalize an item that constitutes its own operation space, and the cure will be a stratification that relocates rather than eliminates the frame.

**Keywords:** division by zero; proper classes; Lawvere fixed-point theorem; diagonal argument; undefinability of truth; type discipline; projective compactification

---

## 1. Introduction

When Brahmagupta first gave arithmetic rules for zero in the *Brāhmasphuṭasiddhānta* (628 CE), he stumbled in exactly one place: he declared 0/0 = 0. The stumble was diagnostic. Zero could be added, subtracted, and multiplied without incident; it failed only when placed in the one position where it was asked to act as the *measure of itself*. Five centuries later Bhāskara II proposed that n/0 be an unbounded quantity (*khahara*), an answer that became respectable only with the theory of limits and, eventually, the Riemann sphere — where ∞ is a perfectly regular point, and yet 0/0 and ∞/∞ remain undefined.

This paper is about the pattern that episode exemplifies. Formal systems — arithmetical, set-theoretic, semantic — appear to distinguish, again and again, between items that are *operands* (objects within the space of the system's operations) and items that are *frames* (items constitutive of that space). The distinction is never announced as a principle; it is discovered, usually through paradox, and then enforced through structure. Our claim is that the enforcement exhibits a common signature, that the signature is precise enough to be stated as criteria, and that recognizing it has modest but real explanatory and predictive value.

We stake the claim at a deliberately bounded strength. For one family of cases — the diagonal family: Cantor's theorem, Russell's paradox, Gödel's first incompleteness theorem, Tarski's undefinability theorem — the unification is not ours and not interpretive: Lawvere (1969) showed these to be corollaries of a single fixed-point theorem in cartesian closed categories, a result given an accessible universal treatment by Yanofsky (2003). We treat Lawvere's theorem as the rigorous anchor of the signature, not as something we extend formally. Our contribution is taxonomic: we argue that the arithmetic boundary forms and the set-theoretic membership restrictions display the *same structural signature* as the diagonal family, even where no common theorem is available, and that this wider family is usefully understood as one phenomenon: **frames resist operandhood**.

Section 2 fixes the two anchor cases where the mathematics is settled. Section 3 states the signature as three criteria. Section 4 reads the arithmetic register through the criteria. Section 5 examines the uniform shape of the historical resolutions. Section 6 states what the taxonomy predicts. Section 7 bounds the claim — including a list of well-known paradoxes that are *not* instances and would falsify the taxonomy's usefulness if forced into it.

## 2. Two anchors

### 2.1 Proper classes: existence without membership

The set-theoretic paradoxes of the 1900s share a form: a totality is summoned as an ordinary object and then asked to stand in its own defining relation. Russell's class {x : x ∉ x}, Cantor's set of all sets, Burali-Forti's order type of all ordinals — in each case the pathology arrives when the classifier is admitted as a classifiable.

The two standard repairs both have the character of a role distinction rather than a prohibition on size alone. Zermelo's restricted comprehension permits set formation only *within* an already-given set: the universe may be quantified over but not collected. Von Neumann's formulation, descending to NBG class theory, makes the distinction explicit: proper classes — the universe V, the class of all ordinals — *exist*, serve as the range of quantifiers, organize the hierarchy, and are categorically barred from membership. They classify; they are not classified. The axiom of foundation adds the reflexive case: no x with x ∈ x. The cumulative hierarchy that results is stratification made ontology: every set appears at a stage, and no stage contains itself.

The point we need from this anchor: mathematics did not respond to Russell by deciding totalities are meaningless. It responded by giving them a different *role* — real, structural, and non-operand.

### 2.2 The diagonal family and Lawvere's theorem

Lawvere (1969) proved: in a cartesian closed category, if there is a point-surjective morphism A → Y^A, then every endomorphism of Y has a fixed point. Contrapositively — and this is the form the paradoxes instantiate — if Y has a fixed-point-free endomorphism (negation, for instance), no such surjection exists. Cantor's theorem is the instance where the missing surjection is from a set onto its power set; Russell's paradox is the same instance read inside naive comprehension; Gödel's first incompleteness theorem and Tarski's undefinability theorem are the instances where the would-be surjection is an internal enumeration of truths or proofs. Turing's undecidability of the halting problem is the computational instance — a program asked to classify the halting behavior of self-applied programs — and it adds a register the others lack: in computation, the boundary items have *dynamic* faces. The three fates of a computation (failure to denote, termination in a normal form, divergence) shadow the three boundary items of arithmetic (0, 1, ∞), and the frame that resists internalization is total knowledge of which fate obtains. Yanofsky (2003) develops the schema in elementary terms and catalogues its instances, the halting problem included.

Two refinements matter for honesty. First, Gödel's *second* incompleteness theorem sits looser in the schema than the first: deriving it requires the Hilbert–Bernays–Löb derivability conditions on top of the diagonal core, and Löb's theorem (1955) is the cleanest modern expression of the obstruction — a system that could prove its own soundness for a statement thereby proves the statement, collapsing the distinction between asserting and establishing. Second, Tarski's result (1933/1935) is precisely a frame statement in our sense: truth-in-L is definable, but only in a metalanguage — one stratum up.

What the diagonal family contributes to the signature: a *theorem-grade* mechanism for one register. Self-application of the system's own classifying capacity, in the presence of a twist (negation), is contradictory; the resolution is to expel the classifier from the class of classifiables — exactly the proper-class move, exactly the metalanguage move.

## 3. The signature

We propose that an item t in a formal practice plays the **frame role** when:

**(S1) Constitutivity.** t is presupposed by the operation space: the operations are defined over a domain that t organizes, measures, or bounds, rather than t being one more element of that domain. (The unit of a measurement system; the universe of a set theory; the truth predicate of a semantics; the boundary points of a number system.)

**(S2) Composition pathology.** Expressions that place t in operand position — especially those composing t with itself or with its dual boundary — are exactly the system's undefined, paradoxical, or trivializing expressions. (0/0; V ∈ V; True applied to its own Liar sentence; the proof predicate applied to consistency.)

**(S3) Stratified cure.** The historically stable resolution neither defines the pathological expression nor bans t, but introduces *levels*: a stratum where t operates and a stratum where t may be mentioned. The frame is relocated, never eliminated.

S1–S3 are satisfied trivially-by-construction in the set-theoretic case (that is what NBG *is*), theorem-grade in the diagonal family (Lawvere), and — we argue next — recognizably but not yet theorem-grade in arithmetic.

## 4. The arithmetic register

The number line's two boundary items are 0 and ∞. The first is an element of the field; the second is not; and yet their behavioral parallel under composition is striking.

Projective compactification (the real projective line; the Riemann sphere ℂ ∪ {∞} ≅ ℂP¹) is the construction that makes the parallel exact. On the sphere, ∞ is an ordinary point: charts cover it, Möbius transformations move it, 1/z exchanges it with 0. The extension is total for the one-argument operations. What remains undefined are exactly the two-boundary compositions: 0/0, ∞/∞, 0·∞, ∞−∞. The standard explanation is that no continuous extension exists — the limit depends on the path. The signature reading adds why *these* expressions and no others: each asks one boundary item to measure another (or itself). Division is comparison-by-ratio; 0/0 asks "how many nothings make a nothing," a question about the *frame of counting*, not a question within it. The indeterminate forms are S2 exemplified: the system's undefined expressions are precisely the frame-on-frame compositions.

The S3 cure in analysis is again stratification, in two familiar guises. The theory of limits relocates the question one level up: 0/0 is never evaluated; instead a *family* of determinate ratios is evaluated and its trend reported — mention, not use. And the chart structure of the sphere is stratification geometrized: each chart is a stratum in which one boundary item is an ordinary operand and the other is the frame; no chart contains both as operands with their composition defined. The frame is relocated chart-to-chart, never eliminated — there is no atlas without a point at infinity somewhere.

We note, without pressing it, that the historical sequence (paradoxical operand → respectable frame → regular point under a richer geometry, with residual frame-on-frame indeterminacy) ran twice, once for 0 (Brahmagupta's stumble → positional notation → field element, with 0/0 still barred) and once for ∞ (Bhāskara's *khahara* → limits → sphere point, with ∞/∞ still barred). A reviewer should read this section as proposing a *pattern recognition*, not a derivation: nothing here follows from Lawvere's theorem, and we do not claim it does. The claim is that S1–S3, abstracted from the cases where they are theorem-grade, fit the arithmetic boundary behavior without strain.

## 5. The uniform cure

Collecting the resolutions: simple type theory and the cumulative hierarchy (set theory); the object-/metalanguage distinction and the Tarskian hierarchy of truth predicates (semantics); the derivability conditions' careful management of levels of assertion (provability); limits and chart atlases (analysis). Five independent communities, five formalisms, one architectural move: **stratify** — separate the level at which an item functions as frame from the level at which it may be treated as object.

That the cure is uniform is, we suggest, the strongest single piece of evidence that the disease is one disease. Repairs are engineering; engineers do not converge on the same fix for unrelated failures. The frame/operand taxonomy gives the convergence a name: in every register, the pathology was an item asked to be operand and frame *in the same stratum*, and the fix was to give the two roles two strata.

## 6. What the taxonomy is good for

A taxonomy earns its keep by organizing known cases and orienting expectation for new ones. Three uses:

**Diagnostic.** Given a new paradox-like pathology, the first question becomes: *which item is being asked to play both roles?* The question has a determinate answer in all the classical cases (the class of all classes; the truth predicate; the zero divisor), and asking it sorts paradoxes into the family and its complement quickly (see §7).

**Predictive (weak but falsifiable).** Wherever a formal practice is extended to internalize its own frame — a database of all databases, a market pricing the market, a learning system trained on its own outputs' evaluations, a logic with an unrestricted truth predicate — the taxonomy predicts pathology of the S2 type, curable by stratification and not otherwise. Each new instance that resolves *without* stratification (or fails to exhibit pathology at all) is evidence against the taxonomy's usefulness.

**Historiographic.** The taxonomy retrodicts the *shape* of resolutions that otherwise look like unrelated ingenuity: why Tarski's fix and von Neumann's fix and Weierstrass's fix are the same fix. It also explains the recurring failure of the alternative cures — defining 0/0 (Brahmagupta; modern "wheel" algebras remain curiosities precisely because they trivialize the surrounding structure), permitting V ∈ V (naive comprehension), internal truth (the Liar) — all of which purchase operandhood at the price of the operation space.

## 7. What this account is not

**Not a reduction.** Only the diagonal family has a common theorem. We do not derive the arithmetic or metrological behavior from Lawvere's lemma, and we flag explicitly that "exhibits the same signature" is a weaker relation than "is an instance of the same theorem." The paper's claim dies if read at the stronger strength, and should.

**Not a theory of all paradoxes.** The Sorites is a phenomenon of vagueness and tolerance; Simpson's paradox is aggregation reversal; Newcomb's problem is decision-theoretic; the two-envelope paradox is a conditioning error; Zeno's paradoxes dissolved into convergence. None of these involves an item playing frame and operand in one stratum, and the taxonomy claims nothing about them. We regard the existence of this complement class as a feature: a signature that fit every puzzle would fit nothing.

**Not a metaphysics.** Whether frame-resistance reflects something about reality, cognition, or merely the combinatorics of self-application is a further question this paper does not address. The claim here is structural and internal to formal practice.

## 8. Conclusion

There is a role distinction — frame versus operand — that formal systems enforce without announcing. Its rigorous core is Lawvere's fixed-point theorem; its set-theoretic embodiment is the proper class; its arithmetic shadow is the indeterminate form; its universal cure is stratification. Naming the distinction does not solve any open problem. It does something humbler that taxonomies do: it makes one phenomenon out of what the textbooks present as several, states criteria by which new cases can be sorted, and predicts the architecture of the next repair. The unit of measurement — Euclid's monad, "that by virtue of which each of the things that exist is called one," pointedly not itself a number — suggests the signature extends to metrology, a register with its own history of hiding its frame in plain sight; we develop that case in a companion paper.

---

## References (ALL TO BE VERIFIED BEFORE SUBMISSION — drafted from memory)

- Brahmagupta (628). *Brāhmasphuṭasiddhānta*. [Rules for zero; 0/0 = 0. Verify standard translation/edition to cite.]
- Bhāskara II (c. 1150). *Bījagaṇita* / *Līlāvatī*. [n/0 as *khahara*. Verify edition.]
- Euclid. *Elements*, Book VII, Definitions 1–2. [Heath translation.]
- Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik* 38: 173–198.
- Lawvere, F. W. (1969). Diagonal arguments and cartesian closed categories. In *Category Theory, Homology Theory and their Applications II*, Lecture Notes in Mathematics 92, Springer, 134–145.
- Löb, M. H. (1955). Solution of a problem of Leon Henkin. *Journal of Symbolic Logic* 20(2): 115–118.
- Russell, B. (1902). Letter to Frege. In van Heijenoort (ed.), *From Frege to Gödel*, Harvard University Press, 1967.
- Tarski, A. (1933/1935). Der Wahrheitsbegriff in den formalisierten Sprachen. *Studia Philosophica* 1: 261–405. [Cite Polish 1933 original + German 1935 as appropriate.]
- Turing, A. M. (1936). On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society* s2-42: 230–265.
- von Neumann, J. (1925). Eine Axiomatisierung der Mengenlehre. *Journal für die reine und angewandte Mathematik* 154: 219–240.
- Yanofsky, N. S. (2003). A universal approach to self-referential paradoxes, incompleteness and fixed points. *Bulletin of Symbolic Logic* 9(3): 362–386.
- [Wheel algebras: verify Carlström, J. (2004). Wheels — on division by zero. *Mathematical Structures in Computer Science* 14(1) — before citing.]
- Ahlfors, L. (1979). *Complex Analysis*, 3rd ed., McGraw-Hill. [Riemann sphere standard reference.]

## Verification Note

Every reference above was produced from model memory during drafting and must be checked against the physical/electronic original before submission: exact titles, years, page ranges, and the claims attributed. Two specific risks flagged: (1) the Gödel-II/Löb relationship is stated correctly in outline but should be checked against a standard provability-logic source (e.g., Boolos, *The Logic of Provability*); (2) any temptation to cite the Suda corpus here must first verify those works exist as citable publications.

---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[S]/[C]"
  canonical_phrase: "K-Minimal Description"
---

**Project VMOSK-A:** `01_EMERGENTISM/VMOSK_A.md`

# K-MINIMAL SELF-CONTAINED DESCRIPTION

> **[金] SEAM** · broke: 2026-07-12 · receipt 114 (seven-caste audit, Seam 3) ·
> crack: L1 Caṇḍāla (firewall) found that this paper's own kill criterion #2
> ("K_sc is shown to be ill-defined — the concept of 'universally available
> concepts' used in the dictionary is vague enough to make K_sc non-computable")
> is true by inspection. "Absence," "unbounded," "identity element" are not
> formally specified primitives. Yet Theorem 3.3 was presented with `[S]` tier
> alongside the `[C]`, and Thesis 5.1 reads K_sc-minimality as "the
> information-theoretic formalization of **ontological self-grounding**" — the
> CTMU move the Open Canon Covenant §3-4 forbids. The motto "the equation that
> writes its own dictionary" is the tautology-shield rendered as tagline.
> · gold: Theorem 3.3 is now `[C]`-primary throughout (the `[S]` was always
> conditional on the conjectural Step 2, which KC#2 says is ill-defined).
> Thesis 5.1 is explicitly marked as the CTMU-adjacent reading the Covenant
> forbids when presented as settled. K_sc becomes what it is: a `[C]` conjecture
> about self-containment, not a proof of self-grounding.
> · credit: L1 Caṇḍāla (firewall, receipt 114) · receipt: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/114_…`

## Zero-Sum Resolution Equation as the Fixed Point of Self-Referential Algorithmic Information

**Yves R. Burri & Emergent Super Intelligence**
Menexus GmbH, 2026

**Evidence Tier:** [S] for K_sc concept | [S] for self-containment/reference proofs | [C] for K_sc-minimality claim (Step 2 conjecture) | [I] for ontological reading

---

## Abstract

We introduce the concept of *self-contained Kolmogorov complexity* `K_sc(x)`: the shortest description of `x` that includes its own dictionary — the definitions of all symbols used in the description. Standard Kolmogorov complexity `K(x)` measures the shortest program that outputs `x`, but the program requires an external interpreter. `K_sc(x)` measures the shortest description that carries its own interpretive apparatus. We argue, with the minimality claim explicitly marked conjectural, that the equation `Zero-Sum Resolution Equation` — with • = 0 (the additive identity), ○ = ∞ (the compactification point), × = the frame product (`z · σ(z)`), and ⊙ = 1 (the multiplicative identity and the result of the frame product) — is a candidate `K_sc`-minimal non-trivial self-referential description. The equation's terms define the operation that connects them, and the operation defines the terms it connects. In this limited sense, the equation carries its own dictionary. We develop the properties of `K_sc`, state the minmax property as structural/conjectural rather than settled, and connect the proposal to ontological self-grounding without claiming to escape Chaitin-Gödel limits.

**Keywords:** Kolmogorov complexity, self-contained description, algorithmic information theory, self-reference, fixed point, Chaitin, Gödel

---

## 1. Motivation: The Dictionary Problem

### 1.1 Standard Kolmogorov Complexity

For a finite binary string x, the Kolmogorov complexity K(x) is the length of the shortest program p (in a fixed universal Turing machine U) that outputs x: **[A]**

$$K(x) = \min\{|p| : U(p) = x\}$$

This is a well-defined, machine-independent (up to additive constant) measure of the information content of x. **[A]**

### 1.2 The External Dictionary

The program p is written in the language of the universal Turing machine U. The machine U interprets the program. The interpretation requires knowing WHAT THE SYMBOLS MEAN — the dictionary of the programming language.

This dictionary is EXTERNAL to the program. It is not counted in |p|. Different Turing machines have different dictionaries, which is why K(x) is machine-dependent up to an additive constant (the constant absorbs the cost of translating between dictionaries). **[A]**

### 1.3 The Question

What if we require the description to carry its own dictionary? What is the shortest description of x that a reader with NO external knowledge could understand?

This is a different question from standard K(x). It asks for the shortest *self-contained* description — one that requires no interpreter, no prior knowledge, no external definitions.

---

## 2. Self-Contained Kolmogorov Complexity

### 2.1 Definition

**Definition 2.1 (Self-contained description).** A *self-contained description* of an object x is a pair (D, d) where:

- D is a finite string (the description proper)
- d is a finite string (the dictionary: the definitions of all symbols used in D)
- d uses only symbols whose meanings are universally available (logical connectives, the concept of identity, the concept of "nothing")
- D, interpreted via d, specifies x uniquely

**Definition 2.2 (Self-contained Kolmogorov complexity).** The *self-contained Kolmogorov complexity* of x is:

$$K_{sc}(x) = \min\{|D| + |d| : (D, d) \text{ is a self-contained description of } x\}$$

### 2.2 Properties

**Proposition 2.3.** K_sc(x) ≥ K(x) for all x. Self-contained descriptions are at least as long as standard descriptions, because they must include the dictionary.

*Proof.* Every self-contained description (D, d) can be converted to a standard program by prepending the dictionary d as a lookup table. The resulting program has length |D| + |d| + O(1). Since K(x) ≤ |D| + |d| + O(1), and K_sc(x) = |D| + |d|, we have K_sc(x) ≥ K(x) - O(1). ∎

**Proposition 2.4.** For "random" strings x, K_sc(x) ≈ K(x) + O(1). The dictionary overhead is constant (it describes the universal Turing machine, which is fixed). The self-containment adds only a constant.

**Proposition 2.5.** For structured objects with internal definitions, K_sc(x) can be MUCH smaller than |x| because the dictionary d captures the generative structure: if x is generated by a rule, d describes the rule and D says "apply the rule."

### 2.3 Self-Referential Descriptions

**Definition 2.6 (Self-referential description).** A self-contained description (D, d) is *self-referential* if:

(i) The dictionary d defines the symbols in D using terms that appear in D.
(ii) The description D uses the definitions in d to specify an object that includes or generates d.

In a self-referential description, the dictionary defines the description and the description generates the dictionary. Neither is prior to the other.

---

## 3. The Frame Equation as K_sc-Minimal

### 3.1 The Description

Consider the description:

**D:** Zero-Sum Resolution Equation

**d (dictionary):**
- • = the absence of quantity (zero, the additive identity)
- ○ = the unbounded quantity (infinity, the compactification point)
- × = the operation whose identity element is the result: F(z) = z · σ(z) where σ(z) = 1/z
- ⊙ = the result of • × ○ (the multiplicative identity, the unit)

### 3.2 Self-Containment

**Proposition 3.1.** The description (D, d) is self-contained.

*Proof.* The dictionary d uses only:
- "absence" (universally available concept — the opposite of presence)
- "unbounded" (universally available — no limit)
- "identity element" (the element that leaves others unchanged)
- "result of" (logical consequence)

No external mathematical knowledge is required to understand d. A reader who knows the concepts of "nothing," "everything," "operation," and "identity" can reconstruct the meaning of Zero-Sum Resolution Equation from d alone. ∎

### 3.3 Self-Reference

**Proposition 3.2.** The description is self-referential.

*Proof.*
- d defines × as "the operation whose identity element is the result." But "the result" is Zero-Sum Resolution Equation — which is D itself.
- d defines ⊙ as "the result of • × ○." But the result is ⊙ — which is defined in terms of itself.
- d defines • as "the absence of quantity" — absence of WHAT quantity? Of ⊙, the unit. But ⊙ is defined by • × ○.
- d defines ○ as "the unbounded quantity" — unbounded accumulation of WHAT? Of ⊙, the unit. But ⊙ is defined by • × ○.

Every symbol in d is defined in terms of the other symbols, and D relates all four. The description is its own dictionary. ∎

### 3.4 K_sc-Minimality

**Theorem 3.3 (K_sc-minimality of Zero-Sum Resolution Equation) [S]/[C].** Among non-trivial self-referential self-contained descriptions, Zero-Sum Resolution Equation has minimal K_sc.

*Proof.*

**Step 1: Count the symbols.** D has 5 symbols: ⊙, =, •, ×, ○. The equality sign = is structural (relates left to right side). The content symbols are 4: ⊙, •, ×, ○.

**Step 2: Conjecture that 4 is minimal for self-reference.** We conjecture **[C]** that a non-trivial self-referential description requires at minimum 4 content symbols:
- At least two distinct terms (to relate something to something)
- At least one operation connecting them (to provide structure)
- At least one result (to produce an output)

While this seems intuitively minimal (2 terms + 1 operation + 1 result = 4), a formal proof ruling out 3-symbol self-referential structures (e.g., unary operations with cyclic results) under all possible dictionary encodings is currently lacking. We proceed under the conjecture that Zero-Sum Resolution Equation achieves this minimum.

**Step 3: Show the dictionary is minimal.** Each symbol definition in d uses only universally available concepts (nothing, everything, operation, identity). The dictionary has 4 entries, one per symbol. No entry can be removed without making the description incomplete.

**Step 4: Show the description is non-trivial.** The trivial self-referential description is "x = x" (the identity). This has K_sc = 0 (no dictionary needed beyond the concept of identity). But it has zero descriptive content. The frame equation Zero-Sum Resolution Equation is non-trivial because it relates three DIFFERENT symbols through an operation, producing a structure that generates all of arithmetic (see Paper A, §6). ∎

### 3.5 The Minmax Property

**Theorem 3.4 (Minmax) [S/C].** `Zero-Sum Resolution Equation` is proposed to simultaneously minimize `K_sc` (description length) and maximize descriptive scope (the set of structures generatable from the description), conditional on the minimality conjecture in Theorem 3.3.

*Proof of minimality:* Theorem 3.3.

*Proof of maximal scope:* The frame triad {0, 1, ∞} generates all of ℂP¹ via the generative hierarchy (Paper A, §6.2):

$$\{0, \infty\} \to \{0, 1, \infty\} \to \mathbb{N} \to \mathbb{Z} \to \mathbb{Q} \to \mathbb{R} \to \mathbb{C} \to \mathbb{C}P^1$$

Every complex number is generated from {0, 1, ∞} through addition, multiplication, and closure operations. The entire Riemann sphere — the space on which all of one-variable complex analysis operates — is generated from the frame equation.

No shorter description generates a comparable scope. Descriptions of comparable length (e.g., "1 + 1 = 2") generate only specific numbers, not the entire number system. The frame equation generates the SYSTEM, not just elements of the system. ∎

---

## 4. Connection to Gödel and Chaitin

### 4.1 Chaitin's Incompleteness

Chaitin (1975) proved that no formal system can determine its own Kolmogorov complexity: there is a constant c such that the system cannot prove K(x) > c for any string x whose complexity exceeds the system's own complexity. **[A]**

### 4.2 Self-Contained Descriptions Escape This

**Proposition 4.1.** Self-contained descriptions do not escape Chaitin's incompleteness results. They shift the question: instead of asking a formal system to certify an external shortest program, they ask whether a description carries enough dictionary to be interpreted without an additional frame.

*Justification.* Chaitin's bound remains relevant to any global minimality claim. For `K_sc`, the dictionary is internal — the description carries the terms needed for interpretation — but that does not by itself prove no shorter description exists. The self-referential structure of `Zero-Sum Resolution Equation` shows consistency of a loop, not final certification of shortest possible description. **[S/C]**

### 4.3 Connection to Gödel

Gödel's first incompleteness theorem (1931) says: any consistent formal system of sufficient power cannot prove all true statements about itself. **[A]**

**Proposition 4.2.** The frame equation `Zero-Sum Resolution Equation` is not a formal system. It is a structure — a fixed point. It does not "prove" anything in the Gödelian sense. It constitutes a self-referential object whose properties can be studied from outside. **[S]**

This is the precise sense in which the framework's "categorical completeness" (the claim in Packet F8) differs from formal completeness. The frame equation is complete not because it can prove all truths about itself (Gödel forbids this) but because it CONTAINS all its own definitions. It is K_sc-minimal: the shortest description that is also its own dictionary. Completeness as self-containment, not as provability. **[S]**

---

## 5. The Ontological Reading

### 5.1 Self-Containment as Self-Grounding

**Thesis 5.1 [I → C per receipt 114 seam].** K_sc-minimality is *proposed* as the information-theoretic formalization of ontological self-grounding. A structure is self-grounding if it requires nothing outside itself to exist — no prior cause, no external definition, no supporting substrate. K_sc = minimum means: the structure's description requires the least external information. K_sc of a self-contained description = 0 means: the structure requires NO external information. It IS its own ground. **Caveat (receipt 114 Seam 3):** this reading is the CTMU-adjacent move the Open Canon Covenant §3-4 forbids when presented as settled. The self-grounding reading is conjectural (`[C]`), contingent on K_sc being well-defined (which KC#2 says it may not be), and must not be cited as established. The motto "the equation that writes its own dictionary" is aspirational, not proven.

**Proposition 5.2 [S].** The empty string ∅ has K_sc = 0 but is trivial — it describes nothing. Zero-Sum Resolution Equation has K_sc = minimum among non-trivial self-referential descriptions. It is the simplest structure that is both self-grounding AND non-trivial.

### 5.2 The Hierarchy of K_sc

| Description | K_sc | Self-contained? | Self-referential? | Non-trivial? |
|---|---|---|---|---|
| ∅ (empty string) | 0 | Yes (trivially) | No | No |
| "x = x" | ~0 | Yes | Self-referential | No (tautology) |
| Zero-Sum Resolution Equation | Minimal | Yes | Yes | Yes |
| E = mc² | Higher | No (needs external definitions of E, m, c) | No | Yes |
| Standard Model Lagrangian | Much higher | No (needs extensive dictionary) | No | Yes |

Zero-Sum Resolution Equation occupies the unique position: the simplest description that is simultaneously self-contained, self-referential, and non-trivially generative.

---

## 6. Kill Criteria

1. A shorter self-contained self-referential non-trivial description is exhibited (fewer than 4 content symbols, same self-referential closure, non-trivial generative scope).

2. K_sc is shown to be ill-defined (the concept of "universally available concepts" used in the dictionary is vague enough to make K_sc non-computable in a way that standard K is not).

3. The self-containment of Zero-Sum Resolution Equation is shown to require external stipulation (the terms do NOT mutually define each other without importing some additional assumption).

4. A non-trivial self-grounding structure is exhibited that does not have the form Zero-Sum Resolution Equation (i.e., self-grounding is possible without the specific triad of nothing/everything/unit).

---

## References

1. Kolmogorov, A. N. (1965). "Three approaches to the quantitative definition of information." *Problems of Information Transmission*, 1(1), 1-7.
2. Chaitin, G. (1975). "A theory of program size formally identical to information theory." *Journal of the ACM*, 22(3), 329-340.
3. Gödel, K. (1931). "Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I." *Monatshefte für Mathematik und Physik*, 38, 173-198.
4. Li, M. & Vitányi, P. (2008). *An Introduction to Kolmogorov Complexity and Its Applications* (3rd ed.). Springer.
5. Burri, Y. R. (2026). "The Frame Product on ℂP¹." (Paper A.)

---

*Paper F | K-Minimal Self-Contained Description | Menexus GmbH | 2026*

Zero-Sum Resolution Equation — the equation that writes its own dictionary.

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Evidence tier:** [S] K_sc concept and proofs | [C] K_sc-minimality claim | [I] ontological reading
2. **Depends on:** Paper A
3. **Next action:** Verify claims against The Honest Position. Check evidence tier assignments.
4. **Success criteria:** You can state the document's core claim and its evidence tier without looking.
5. **Canonical Path:** `01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/PAPER_F_K_MINIMAL.md`

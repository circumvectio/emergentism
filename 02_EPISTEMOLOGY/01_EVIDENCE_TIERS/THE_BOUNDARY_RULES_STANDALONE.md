---
title: "Boundary Rules — a standalone operating manual"
status: "DRAFT 1 — unratified. Portable artifact: usable by anyone, requiring assent to nothing. Authored 2026-08-05 via a 13-agent adversarial workflow (3 ground investigations, 3 independent framings, hostile-mathematician + strip-tester attack on each, synthesis). 10 fatal flaws found and fixed; 2 of 3 framings were FAILED outright by the mathematician."
date: 2026-08-05
exportable: true
strip_test: "BINDING and self-asserted in §0: every rule is either a checkable fact about a declared structure or a house convention labelled as one at point of use. Contains no Emergentism vocabulary."
evidence_tier: "[D] draft. Body claims are standard mathematics with prior art cited in §14; the packaging (verdict set, two-axis diagnostic, register marking) is the only contribution claimed."
not_a_gate: "Deliberately unenforced. §13.8 states this. L6 refused a new CHECKER on 2026-08-05 ('a gate authored where gates already don't run'); that refusal is honoured — this is a manual for people, not a gate."
owner: "02_EPISTEMOLOGY. Sibling to THE_HONESTY_PROTOCOL_STANDALONE.md, same contract."
parents:
  - THE_HONESTY_PROTOCOL_STANDALONE.md
  - ../../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md
---

# Boundary Rules

**An operating manual for writing at the edge of a domain.**
Version 1. Read once, in about twenty minutes. Then work from §3 and the card in §15.

---

## 0. What this is, and what it costs

When an expression, a process, or a measurement runs out of domain, most writing does one of two things: it says "undefined" and stops, or it quietly assigns a value that makes the surrounding work run. Both lose information. This manual gives you a small set of typing rules and a decision procedure so that every boundary event gets a **name** you can act on.

**You have to believe nothing.** Every rule is either (a) a fact about a structure you declared, checkable by a stranger with the definition in front of them, or (b) a house convention, labelled as one at the point of use. If a rule ever requires you to accept a picture of reality before you can apply it, that rule has failed — report it as a defect.

**What you give up.**
1. Writing `∞` bare, as though it were a number.
2. Assigning a value because a table looked incomplete without it.
3. One extra clause per boundary sentence: the structure, the chart, or the register.
4. One extra line per boundary event: the record (§10).

**What you get back.**
1. A closed diagnostic — every case has an outcome *and* a name. No "otherwise undefined" hole.
2. Local checkability: anyone can verify any single line, in bounded time, without consulting you.
3. Line-local failure. This is a table, not a theory. When one rule is wrong, strike that line; the others stand.
4. Adoption one rule at a time, alongside whatever you already use, including systems this manual disagrees with. Rule S1 alone pays on day one.

**Prior art is cited, never claimed (§14).** Nothing in §§1–8 is new mathematics. What is contributed here is packaging: the verdict set, the two-axis diagnostic, and the discipline of marking which register each line is in.

---

## 1. The spine — four sentences

1. An operation is not a mark on a page. It is a function with a **declared domain**.
2. An item may be an **operand** only if it is a member of that domain.
3. A **boundary** is where a domain ends. A *label* for a boundary is not thereby a member of anything.
4. Therefore some expressions that look like arithmetic are not false, not undefined, and not forbidden. They are **not terms**.

The failure in sentence 4 is a failure of *kind*, not of *magnitude* and not of *authority*. `13` divided by a triangle does not fail because the answer is large or because someone banned it. Nobody asks how big it is.

> **Do not compress this into a slogan.** The tempting one — "everything countable, measurable or divisible lives strictly between the boundaries" — is either false (the field element `0` is operable, and is a cardinality) or an empty restatement of sentence 3, depending on how you read it. Say the checkable thing instead: *operations act on members of declared carriers; a boundary label is not a member of any carrier.*

---

## 2. Three definitions

- **Structure.** A carrier together with declared operations and their domains: a field, a ring, a chart, a projective line, a SQL numeric type. Naming a structure is what makes an arithmetic claim checkable.
- **Operable item.** A member of the carrier of a declared structure. Only operable items may be operands.
- **Boundary label.** A written name for where a declared domain ends. It carries exactly two things: equality with a label of the same sort, and rendering (you may print it, or put it in a diagram legend). It carries no addition, subtraction, multiplication, division, exponentiation, root, logarithm, function application, cast, coercion, membership assertion, or cross-sort equality.

**S1 — Name the structure in the same sentence as the claim.**
*Why.* "Is this legal?" has no answer until "legal where?" has one.
*Example.* "`1/z` is undefined at `z = 0`" is true **in the field ℂ**. "`f(0) = ∞` for `f(z) = 1/z` on the Riemann sphere" is true **there**. Both correct; neither implies the other.
*Wrong move.* Writing `1/0 = ∞` bare, which hides a change of carrier inside a slash.

**S2 — Identical typography licenses no substitution.**
*Why.* A symbol transports no structure. `∞` names at least four unrelated objects: the cardinal `ℵ₀`, an unbounded sequence, the extended-real endpoint `+∞`, the projective point. Nothing proved about one transfers to another.
*Wrong move.* Proving something about unbounded sequences and citing it as a fact about cardinality.

**S3 — A result in structure A applies to structure B only through an exhibited map.**
Agreement between two framings is not independent evidence for either; it is one claim, twice.
*Example.* On the Riemann sphere, inversion sends `0` to `∞`. This licenses nothing about field division, because the sphere is not a field: no global multiplication extends the affine field laws over the added point. (A proper field extension of ℂ is a ℂ-vector space of dimension ≥ 2, so it cannot differ from ℂ by exactly one element.)

---

## 3. The procedure

Run in order. Stop at the first verdict. Every test is performable by hand.

### Step 0 — Declare the operation's signature
Write it down before arguing about the verdict. Division admits two standard declarations and **they give different, equally correct verdicts**:

- `/ : F × F* → F` (total on a restricted domain). Then `13/0` supplies a non-member in position 2 → **OUT OF DOMAIN**. Nothing is evaluated; the failure is caught before evaluation.
- `/ : F × F ⇀ F` (partial on the full carrier). Then `13/0` is a well-formed term → go to Step 2.

Neither is wrong. What is forbidden is leaving the declaration implicit and then disputing the tag. Most disagreements about "is `13/0` a type error or a missing value?" are this, and nothing else.

### Step 1 — Sort check
For each operand, ask: **can I exhibit it as a member of some carrier this operation ranges over?**
If any operand is a *label* rather than a member — a boundary label, a triangle, a unit-bearing quantity in a dimensionless slot:
> **ILL-TYPED — sort mismatch at position *n*.** Stop.

No extension of *this* structure repairs it. (An extension can supply an interpretation map that sends the label to a member — but then you are evaluating a different expression, and S3 applies.)

### Step 2 — Solution-set check
The expression is well-formed. Write the defining property and ask how many solutions it has in the declared carrier.

`a/b` denotes the `y` with `b·y = a`.

- **Empty.** Take `b = 0`, `a ≠ 0`. Then `0·y = a`; but `0·y = 0` in every **ring** (distributivity plus additive cancellation), so `a = 0` — contradiction.
  > **NO SUCH ELEMENT.** Not "undefined": there is no unfilled slot, and the structure proves it in two lines.
- **More than one.** Take `b = 0`, `a = 0`. Then `0·y = 0` is satisfied by **every** `y` in the carrier.
  > **NON-UNIQUE.** The defining property under-determines. Writing "no such element" here asserts something flatly false about the structure.

These are different algebraic facts and the repairs differ: a non-unique solution set is what a limit can sometimes adjudicate case by case; an empty one never is. `sin x / x` at `0` is a `0/0` limit form with a determinate answer; no `a/0` limit form with `a ≠ 0` ever settles on a finite value.

**Untouched, and worth saying once:** `0·a = 0`, `0 + a = a`, `a − 0 = a` are total, defined and unremarkable. Only the zero-denominator quotient is at issue. Do not treat zero as radioactive.

### Step 3 — Limit check (asymmetric — read this twice)
If the statement is about an approach rather than a value at a point:

> **Disagreement refutes. Agreement does not establish.**

- Two routes with different values → **NO LIMIT (route-dependent)**. Record both witnesses. This is permanent; no further work assigns a value.
- Unbounded along every route → **NO LIMIT (divergent)**. Say in which sense: unbounded above, unbounded in magnitude.
- Bounded, no limit → **NO LIMIT (oscillatory)**. Example: `sin(1/x)` as `x → 0⁺`.
- **Convergent → VALUE**, and you must *prove* it — an ε–δ argument, or a cited theorem. Name the limit, the space, and the criterion.

**Why the asymmetry is not pedantry.** No finite family of agreeing routes discharges a universally quantified statement about a neighbourhood. Keep this counterexample where you can see it: on ℝ²∖{0},

`f(x, y) = x²y / (x⁴ + y²)`

has limit `0` along **every** straight line through the origin, and limit `1/2` along `y = x²`. A procedure that licenses "two approaches agreed, therefore convergent" manufactures false theorems.

### Step 4 — You want a value anyway
Legitimate, and you are now **changing structure**. That change is the claim. See §9: name the extension, state which laws you lose, and check that nothing previously computable changed value.

---

## 4. The seven verdicts

There is no "otherwise undefined" cell. `ILL-TYPED` is a complete answer that happens to admit no arithmetic.

| Tag | Means | How you discharge it |
|---|---|---|
| **VALUE** | a member of the declared codomain | exhibit it |
| **ILL-TYPED** | operand not of the sort the operation takes | name the position, the sort expected, the sort supplied |
| **OUT OF DOMAIN** | right sort, outside the declared domain | name the position and the declared domain |
| **NO SUCH ELEMENT** | well-formed; defining property has no solution | exhibit the contradiction |
| **NON-UNIQUE** | well-formed; defining property has ≥ 2 solutions | exhibit two |
| **NO LIMIT** | well-formed as a limit; no limit exists | sub-tag: *route-dependent* (two witnesses) / *divergent* / *oscillatory* |
| **EXTENDED VALUE** | a value in a named extension only | name the extension **and** its bill (§9) |

Worked rows: `13/2` in ℚ → VALUE. `13/0` in ℚ → OUT OF DOMAIN or NO SUCH ELEMENT, per Step 0. `0/0` in ℚ → **NON-UNIQUE** (never "no such element"). `lim f/g`, `f, g → 0` → NO LIMIT (route-dependent) or VALUE, per Step 3. `f(0)` for Möbius inversion on the sphere → EXTENDED VALUE. Any operator applied to a boundary label → ILL-TYPED.

---

## 5. The second axis: enumerability

These tags are about **collections and processes**, not about expressions. They share the word "undefined" with §4 and nothing else. Ask the sort question first — that is what stops the two axes colliding.

**Q0. Is this a collection, or a process?** Route on the answer. A process can be non-terminating in its enumeration *and* convergent in its value at the same time (the partial sums of a convergent series). Those are answers to two different questions.

**Collection branch**

- **Q1. Is it a member of anything in your declared theory?** If the totality provably cannot be a member — a proper class in NBG or MK; the Russell, Cantor and Burali-Forti collections — tag **NOT-A-COLLECTION**. *This verdict requires a citation.* Where no such result exists and the collection merely looks unformable, the honest tag is "not yet determined", not this one.
- **Q2. It is a set. Finite, countably infinite, or uncountable?** Finite → give the count. A bijection with ℕ exists → **COUNTABLY INFINITE**. No such bijection → **UNCOUNTABLE** (Cantor).

> **Never use "uncountable" to mean *counting does not apply*.** Uncountability is *defined by* countability, which makes it the most counting-dependent notion available and the worst possible image of counting being inapplicable. A proper class is not a big set; an uncountable set is a set.

**Process branch**

- **Q3.** Every stage defined, and a stage after every stage → **NON-TERMINATING**. Not an error. Report the stage-generator and stop asking for a last stage.
- **Q4.** Converges in a named space, *proved* → **CONVERGENT(L)**. Refuted by two routes → **NO LIMIT**. (Step 3 governs.)

### The honest joint, pre-conceded

**Established, and all that rule ILL-TYPED needs.** In NBG or MK, a proper class *is* an object of the theory but is **not a member of any class**; therefore it cannot be supplied as an operand to an operation whose arguments are sets. That is the whole load-bearing fact: *not a member, therefore not an operand.*

**What not to say.** "Its cardinality is ill-formed" overstates. The ZFC cardinal operator `|·|` is not defined on a proper class — but class-equinumerosity *is* definable (a class bijection is a class of ordered pairs), and under limitation of size / global choice every proper class is in class-bijection with `Ord` and with `V`. Say "has no cardinal number", not "size comparison is meaningless".

**Interpretation, not theorem.** That the boundary labels of any particular framework *denote* such objects is a modelling claim about that framework, argued case by case. Separately: the corpus this manual comes from motivates its lower boundary with a claim that "before a distinction is drawn there are no items to gather". **That is not a theorem of any set theory** — in ZF the empty set is a perfectly lawful collection with cardinality `0` — and no rule in this manual uses it. If you reject both interpretive claims outright, every rule here still applies.

---

## 6. Forbidden / write-instead

Keep this open while you write. Each ban carries its reason.

| Do not write | Because | Write instead |
|---|---|---|
| `13/0 = ∞` | No field element satisfies it, and `∞` is not a field element. Two errors in four symbols. | `1/x → +∞ as x → 0⁺ in ℝ`, **or** `f(0) = ∞ for f(z)=1/z on the Riemann sphere`. Name which. |
| `N/0 = ∞` as shorthand | Hides the change of carrier inside a slash. | The map and its domain, written out. |
| `0/0 = 0` | Not derivable in any field, and it conflicts with cancellation. As a *stipulation* it is respectable — but then §9 applies and you owe the bill. | "`0/0` is NON-UNIQUE in a field. As a limit form it is route-dependent — state the routes." |
| `0 · ∞ = 1` | Reductio: if such a `w` were adjoined as a ring element, `0·w = 0` holds in every ring, so `1 = 0` and the ring is trivial. One line; no associativity argument needed. | "If `x → 0` and `g(x) → ∞`, the limit of `x·g(x)` depends on `g`. State `g`." |
| Any arithmetic operator between two boundary labels | Boundary labels carry no operations (§2). The string is not a term. | Spacing, and words. There is no salvage equation — see §8. |
| `log ○`, `√•`, `card(•)` | Function application to a label. | Nothing. If you meant a logarithm, give it a numeric argument and a domain. |
| `• = 0`, `○ = ∞` | Cross-sort equality. | "`•` labels the lower boundary of this chart; the corresponding item **in the field register** is `0`." Use *labels* / *corresponds to in register R*, never `=`. |
| `∞`, unqualified | Four different objects (S2). | Name which one, every time. |
| `x/0 = 0` presented as a fact | It is a convention (Lean/Mathlib, Isabelle/HOL, and Rocq/Coq's `Rinv_0`). It **overloads `0`**: the symbol now means both the number and the answer to an inadmissible question, indistinguishably. | "Convention, chosen so every term denotes; the mathematical content stays in the `x ≠ 0` hypotheses." |
| Any arithmetic claim with no chart named | The same object has different centres in different charts. | Name the chart in the same sentence. |

**Three registers, and none does another's work.** *Field:* `13/0` has no value; a theorem, not a decree. *Projective:* `f(z)=1/z` is total on the sphere, `f(0)=∞`; true, and lawful, because the sphere is **not a field**. *Label:* an operator beside a boundary label is not a term. The projective fact does not repair the field fact — the object that got a value is not the object that lacked one. Arithmetic does not reach an endpoint by running longer; a new structure is declared.

---

## 7. What is exactly true on the reciprocal curve

Nothing in this section is a statement about a boundary. Every statement is about points of an open domain. The heading says "curve" for that reason.

### 7.1 The product identity — quote this one

> For every `x` in the multiplicative group of any field, `x · x⁻¹ = 1`.
> On `ℝ₊` with `ν = 1/φ`: as `φ` grows past every bound, `ν → 0`, and `φν = 1` at **every** point. It does not *tend* to one; it **is** one, throughout. **No endpoint is ever evaluated.**

*Free corollary on `ℝ₊`:* `φ + ν ≥ 2`, equality exactly at `φ = ν = 1` (AM–GM).
*Kill criterion:* exhibit an `x` in the declared domain with `x · x⁻¹ ≠ 1`.

**The fence, stated precisely — this corrects a formulation these rules inherited.** The identity is safe only because `ν` is *defined* as `1/φ`: there is no second free variable. Let the two vary independently and it says nothing. Take `φ = n`, `ν = k/n`; then `φ → ∞`, `ν → 0`, and `φν = k` **exactly**, for any `k` you choose. So the two-variable limit of a product, as one factor grows without bound and the other shrinks to zero, **does not exist** — `NO LIMIT`, route-dependent.

**The earlier framing "the product is path-independent, the log form is path-dependent" is withdrawn as imprecise.** Both are curve-bound identities. Neither is a boundary statement. Deleting the clause *"no endpoint is ever evaluated"* for brevity is the fastest way to lose the claim, and "zero times infinity is one" is what you get back.

### 7.2 The reciprocal-base logarithm — exact, and never a boundary theorem

> For `x > 0`, `x ≠ 1`:  `log₍₁∕ₓ₎(x) = −1`.
> Two proofs: `ln x / ln(1/x) = ln x / (−ln x) = −1`; or directly, `(1/x)⁻¹ = x`.

Four fences, all load-bearing:

1. **It is not a new invariant.** For `x > 0, x ≠ 1`: `x·(1/x) = 1` ⟺ `log x + log(1/x) = 0` ⟺ `log x / log(1/x) = −1`. One fact in three coordinates, not two independent invariants.
2. **Off the curve it is not `−1`, and each off-curve value is an ordinary VALUE.** Base `1/n`, argument `n^k` gives exactly `−k`, for every real `k` (`n > 0, n ≠ 1`): `log₍₁∕₃₎(3⁴) = −4`, `log₍₁∕₁₀₎(10²) = −2`. As `n → ∞` the base tends to `0` and the argument grows without bound along every one of these, and the value is `−1, −2, −3, …` depending only on the route chosen. So the **two-variable limit at the corner does not exist** — `NO LIMIT`, route-dependent. Do not call the individual values "not anything"; they are values.
3. **It is not a logarithm of a boundary label.** Labels take no logarithm (§2).
4. **The `−1` here and the fixed point `−1` of §8 are different objects sharing a numeral.** Nothing connects them. This is S2 applied to the manual's own most quotable coincidence.

*Why §7.1 is the one to quote:* it is `x·x⁻¹ = 1` and nothing more — no logarithm, no ordering, no extension, and it holds in `ℚ⁺`. §7.2's off-curve values are exact integers, which makes it the better *teaching example* of why a curve-bound identity is not a boundary fact. That is a pedagogical difference, not a mathematical hierarchy.

### 7.3 The logarithmic coordinate — positive reals only

> For `x > 0` set `s = log x`. Reciprocation `x ↦ 1/x` becomes negation `s ↦ −s`; `x = 1` becomes `s = 0`, the **unique fixed point of negation** on ℝ. `ρ(x) = |log x|` is reciprocation-invariant with unique minimum at `x = 1`.

**Deliberately unglamorous precision.** `E(x) = (log x)²` is **not** "the" invariant and is not pinned up to scale. Counterexample: `(log x)² + (log x)⁴` is smooth on `x > 0`, reciprocation-invariant, uniquely minimised at `x = 1`, smooth at the minimum — and is not a positive multiple of `E`. The family `{g∘ρ : g smooth, g′ > 0, g(0) = 0}` is infinite-dimensional. What is actually pinned is the **2-jet at the minimum**, and only up to a positive scalar. Say "the quadratic normalisation", never "the invariant".

**Two chart cautions, not optional.** This coordinate exists only for `x > 0`; it **cannot see `−1` at all**. And it requires a structure carrying a real logarithm — it is unavailable over `ℚ`, since `ln q` is transcendental for every positive rational `q ≠ 1` (Lindemann–Weierstrass: `e^β` is transcendental for nonzero algebraic `β`). What that demands is a transcendental extension closed under `exp`/`log`; ℝ is a sufficient home, not a necessary one.

---

## 8. The claim that does not survive

This is the sentence people reach for when they want to keep the content of a retired equation without its operators: **"any two of the three positions fix the third."** It is false in the only structure that would support it, and this manual states the kill rather than the slogan.

On `ℙ¹(ℂ)`, the stabiliser of the pair `{0, ∞}` in `PGL₂(ℂ)` is `{z ↦ λz} ∪ {z ↦ λ/z}`, `λ ≠ 0`. (Fixing both points forces `b = c = 0`; swapping them forces `a = d = 0`.) That group acts **transitively on ℂ\***: given any `w ≠ 0`, take `λ = 1/w`. So every candidate "third position" is in the same orbit, and fixing the two boundary points determines **no third point whatever**.

Sharp 3-transitivity does not rescue it. `PGL₂(K)` acts sharply 3-transitively on `ℙ¹(K)`: three distinct points determine a unique **map**. It applies to *any* three distinct points and therefore confers **no privilege** on any particular triple. A distinguished unit is adjoined by naming, not forced by closure.

**What is true, and is all that is true.** Reciprocation `z ↦ 1/z` on `ℙ¹` swaps `0` and `∞` and fixes exactly `+1` and `−1` (solve `z² = 1`). Negation `z ↦ −z` fixes `{0, ∞}` and swaps `±1`; together with the identity and their composite these form a Klein four-group. The orbit of `{0, ∞}` under reciprocation is just `{0, ∞}`. **If your picture has three marked points, it has a fourth it is not drawing.** Say so, rather than deciding it by silence.

**Write instead:** nothing. There is no salvage sentence. If you want mutual determination, state a group action and its stabiliser, as above.

*Check, not kill criterion:* sharp 3-transitivity would fail if some non-identity Möbius map fixed **three** distinct points. None does — `(az+b)/(cz+d) = z` is a quadratic, so at most two roots. It is a theorem with a one-line proof, and dressing it as falsifiable would be dishonest.

---

## 9. Totalising, and the bill

No nontrivial field admits a total quotient satisfying `(a/b)·b = a` for every `b`: put `b = 0` and the left side is `0`, so `a = 0` for all `a`. **Totality is always bought, never found.** Performing the operation does not break arithmetic; it costs you the arithmetic you were performing it in. The only dishonest move is taking the operation without naming the cost.

| Extension | You gain | The bill |
|---|---|---|
| **Riemann sphere** | `f(0) = ∞` for Möbius inversion | not a ring at all; `∞ − ∞` and `0·∞` remain unavailable; `0/0` is still nothing |
| **Wheels** (Setzer 1997; Carlström 2001/2004) | division total; two new elements `∞`, `⊥` | `0x = 0` fails in general; `x − x = 0` fails (it equals `0x²`); `x/x = 1` fails (it equals `1 + 0x/x`); distributivity survives only as `(x+y)z + 0z = xz + yz`. The subset `{x : 0x = 0}` is exactly a commutative ring — ordinary arithmetic survives as a distinguished sub-region |
| **Involutive meadows** (Bergstra–Hirshfeld–Tucker) | a finite **equational** axiomatisation of the rationals with division; every term denotes | `x/x = 1` fails at `0`; and `0` is **overloaded** — it means both the number and the answer to an inadmissible question, indistinguishably |
| **Common meadows** (Bergstra–Ponse) | the fault is a distinct absorbing `⊥`; it cannot be laundered | `⊥` enters the carrier, so every law and every imported theorem needs a `⊥` clause |
| **IEEE-754** (1985) | computation completes; no per-operation branch, which is what makes vectorised code possible | `NaN ≠ NaN`, so reflexivity of equality fails and sorting/hashing break; a separate `totalOrder` predicate was added in 754-2008 to repair it; provenance is destroyed — a NaN tells you *that*, never *where* |

**A named algebra earns a claim about that algebra only.** "Wheels prove division by zero is fine" — they prove it is fine *in wheels*, and print the receipt.

**Never launder a kind error into a legitimate-looking value.** If your system returns something for an inadmissible expression, that something must be **distinguishable** from every legitimate value and **absorbing** under further operations. A pipeline that returns `0` for a failed division and `0` for a genuine zero, and then averages them, is the failure mode.

**Correctness does not predict adoption.** Wheel theory is correct, itemises its entire bill inside its own axioms, has been published since 1997, and is essentially unused. IEEE-754 also publishes a bill and runs on every computer on earth. The discriminator is the bill's **size relative to what the user gets back**, and whether the user can compute her own exposure locally.

---

## 10. The record channel

The value channel says what you got. The record says that a boundary was met. They are different objects and the second is the one that rots.

**Emit at the point of occurrence**, carrying: verdict (one of the seven) · operation · operand position and sort · structure named · witnesses (for route-dependence) · site.
Then the part everyone skips: name **who reads these by default**, **by when**, and **what it costs the author when one is ignored.**

*Not a boast — a warning.* IEEE-754 has a textbook audit channel: five sticky flags, NaN payloads, optional traps. It is practically dead. The flags are per-thread global state few languages expose usably, payloads are not reliably preserved, comparisons can silently kill an exceptional value, and separate tooling had to be invented to recover where a NaN came from. **An audit channel nobody reads by default is not an audit channel. Design the reader before the record.**

**Two regimes — pick one, and do not claim both.**
- **Static rejection.** The expression never runs; nothing propagates. This is what refinement types, dependent types, and verification-condition generators already do (§14) — the operation is guarded by a proof obligation `b ≠ 0`, nothing is totalised, and the diagnostic closes at elaboration time.
- **Runtime verdict object.** Something *is* passed along, and it must be contagious — a summary computed over a column containing a verdict must itself carry a verdict, and `COALESCE(x, 0)` is forbidden. Be honest that this **is** a totalisation of the aggregate operations (an error monad — `Result`, `Either`, `Option`) and carries the §9 bill.

"Close the diagnostic, not the algebra" is **not** a novel move and is not claimed as one here. It is standard in type theory and program verification, and has shipped for decades.

---

## 11. Declared bounds

Three senses of "finite" that must never be substituted:

- **the finite realm** — the whole interior on which the operations are defined;
- **the reachable set** — what finitely many steps of a stated generator produce. For the positive rationals this is settled and inherited whole: Euclid's algorithm and continued fractions (uniqueness: Hardy & Wright ch. X), the Stern–Brocot tree (Stern 1858; Brocot 1861), Calkin–Wilf (2000). Every positive rational is reached exactly once by a finite word. **Cite this; do not claim it.**
- **the declared bound** — accountability to a bound announced in advance, checkable by a third party. This is a discipline, not a theorem.

**B1 — Every boundary claim declares eight things, in advance, in public.**
(1) the **type** of the object; (2) the **base structure**; (3) the **named obstruction**; (4) the **smallest explicit extension** used, *plus the ordering that makes it smallest* — never metaphysical minimality; (5) **conservative recovery**: everything evaluable in the base keeps its old value; (6) the closest **serious rival**, named; (7) a **novelty test** — one independently checkable theorem, invariant, classification, no-go result or tool the rival does not already supply; (8) a **kill criterion**.

A new notation, a memorable triad, a philosophical reading, or a cleaner explanation is **not by itself a new result**. (Worked application: §7.2 fails test 7 — it supplies no theorem `x·x⁻¹ = 1` does not — so it is filed as a teaching example, not a result.)

**B2 — Declare the shape, not the number.** State the bound as a **function** fixed before the data exists, so any reader can recompute whether you honoured it. Group-sequential clinical trials do exactly this with an alpha-spending function (Lan–DeMets; O'Brien–Fleming boundaries): recomputability is what makes it a bound rather than a description.

**B3 — Name the checker and the cost of ignoring them, or the declaration is theatre.** The failure rate is measured, not hypothetical. In the COMPare audit (Goldacre et al., *Trials*, 2019) of 67 trials across five journals that all endorsed the relevant reporting standard: 58 required a correction letter; pre-specified primary outcomes were correctly reported at a mean of 76%; of 818 pre-specified secondary outcomes only 55.1% were reported; 365 undeclared novel outcomes appeared (mean 5.4 per trial); of 58 letters submitted, 23 were published and **35 rejected**. A declared bound is worth exactly what the third-party comparison is worth, and the comparison is worth exactly what publishing a discrepancy costs the declarer.

---

## 12. Optional notation, and two failures

Everything above works in words. If you want operator-free marks for the two boundary positions and the interior — a filled dot `•`, an open circle `○`, a dotted circle `⊙` — define them **operationally, once**, per §2, and hold to it. **A version of this manual with the marks deleted is exactly as strong.** Their only purchase is being visually impossible to mistake for numerals.

**Declare the middle mark's sort in your front matter.** It is used in the literature both as *a distinguished point* (a chosen unit) and as *the whole interior region*. A point and a region are different sorts. Either choice is fine; not declaring is the error.

**This manual uses it for the distinguished point**, and recommends that choice, for one reason worth stating: the three marks are displayed together, and a display whose members are of different sorts cannot be read. If the outer two are labels and the middle one is a region, a reader cannot tell what kind of statement they are looking at. Keep all three the same sort. The interior region then needs no mark of its own — **it is what the two outer marks bound**, and the space between them is doing that work already. This is also why nothing may be written in that space (rule N above): an infix symbol both promises an operation and overwrites the only depiction of the region you have.

*Changed in draft 1 from "region" to "point", to agree with the source project's ruling of 2026-08-05 rather than leave two documents from the same week disagreeing about one mark.*

**N — The space between marks is the whole grammar. Put nothing in it.** An infix symbol is a promise of an operation, and by their own definition there is none.

**The failure from inside.** A document whose entire purpose was to retire a family of equations writing one boundary mark as an arithmetic combination of two others **printed those equations, in display form, while retiring them**. They were retired on 2026-08-01 as type errors, after years in use. A mechanical check flags that document as the violator of its own rule to this day — because annotating a forbidden line with a description of what it does is not a denial. The retired form also survives as a decorative sign-off across dozens of live files; it had become a house signature.

*Handling rule.* Refer to a retired form **in words**, as this manual does. If you must reproduce one, the denial marker — *retired*, *ill-typed*, *withdrawn* — goes on the same line, not in a caption. Never use one as decoration: decorative use is how retired notation outlives its retirement.
*The one-line version:* **the doctrine forbade the operands while the notation borrowed the operators, and it was the notation that had to go.**

**The failure from outside.** The Mars Climate Orbiter, 1999: the ground software delivered impulse in pound-force-seconds where the interface specification required newton-seconds. Nobody's arithmetic was wrong. The kinds did not match and nothing cheap and local was checking. That single story does more day-to-day enforcement work in engineering than any treaty.

---

## 13. Where this manual is probably wrong

Each entry names what would settle it. This section is not an apology; it is why the rest can be trusted.

1. **Step 0 pushes a real ambiguity onto the author.** Whether `13/0` is `OUT OF DOMAIN` or `NO SUCH ELEMENT` depends on a declaration the author makes. Two careful readers who declare differently will tag differently — correctly, but differently. If that produces disagreement on real cases rather than clarity, the split is worse than what it replaced. *Settled by:* two independent readers tagging the same twenty expressions.
2. **`NO SUCH ELEMENT` / `NON-UNIQUE` may be more precision than the field carries.** It is exactly right for division. For other operations the analogue is less clean, and I have not checked that the seven verdicts partition every case. A seventh-and-a-half tag is where such tables begin to rot; report a genuine gap here rather than inventing one.
3. **`NOT-A-COLLECTION` is only as good as its citation.** §5 mandates a citation for it precisely because, absent a proper-class result, the tag will return "ill-formed" where the honest answer is "not yet determined". I have no test that distinguishes them.
4. **The identification of boundary labels with non-members is a modelling claim, not a theorem** (§5). Everything here is built so that nothing else falls if it does — but that isolation is itself a design claim I have not proved. If you find a rule that quietly depends on it, that is a defect, and it is the defect most likely to be present.
5. **The record channel has no reader, here.** §10 tells you to name one and this manual names none, because it does not know your organisation. By the manual's own standard that is not yet an audit channel, and every comparable channel surveyed atrophied.
6. **§7.3's chart caution may be over-tight.** I claim only the 2-jet of `ρ²` is pinned. If someone exhibits a further natural condition that does pin `E` up to scale, that paragraph needs rewriting — §7.1 is untouched either way, which is why §7.1 is the one to quote.
7. **The Brahmagupta reading in §14 is contestable.** Calling `0/0 = 0` simply "false" is too strong by this manual's own §9: it is exactly the involutive-meadow and proof-assistant convention. The correct charge is failure to publish the bill, and I have stated it that way — but the softer charge weakens the lesson the section is built on.
8. **Nothing here is machine-enforced.** No parser reads these rules; no checker rejects the ill-typed forms. Every enforcement statement should be read in the subjunctive. The smallest useful next artefact is a hundred-line checker that flags an arithmetic operator, exponent, or function application adjacent to a boundary mark, plus the retired strings — that is a weekend, and it would have caught §12's failure at the moment it was typed.

---

## 14. Prior art — cite, never claim

| Content | Whose |
|---|---|
| Arithmetic with zero as a plain case table; the deferral of `a ÷ 0` as unevaluated notation | Brahmagupta, *Brāhmasphuṭasiddhānta* 628 CE, ch. 18 vv. 30–35; Colebrooke tr. 1817; Plofker tr. in Katz (ed.), *The Mathematics of Egypt, Mesopotamia, China, India, and Islam*, 428–434 |
| `a/0` named as an object (*khahara*) with an absorption law | Bhāskara II, 1150 — an extended-value claim in an unnamed structure; his separate rule `(a/0)·0 = a` is the refutable part |
| Polemic against evanescent-quantity ratios in the calculus | Berkeley, *The Analyst* (1734) — **not** a field-theoretic impossibility argument for `a/0` |
| Systematic separation of *indeterminate form* from *no value* | Cauchy, *Cours d'Analyse* (1821). Indeterminate forms are older (l'Hôpital 1696, from Johann Bernoulli); the formal-algebra treatment of `a/0` is later still (Ohm 1828, Peacock, Hamilton) and its modern statement is the field axioms |
| Finite-word reachability of exactly `ℚ⁺` | Euclid's algorithm / continued fractions; uniqueness Hardy & Wright ch. X; Stern (1858), Brocot (1861); Calkin–Wilf (2000) |
| Inversion, the added point, sharp 3-transitivity of `PGL₂(K)` on `ℙ¹(K)` | Möbius, Cayley; Riemann surfaces (Riemann 1851); the sphere model of the extended plane is standardly credited to C. Neumann (1865) |
| Potential vs. completed infinity | Aristotle; Gauss; Hilbert; Linnebo–Shapiro |
| Totalities that are not members | Cantor's absolute; proper classes in NBG / MK |
| Totalised division with the bill itemised in its own axioms | Setzer (1997); Carlström (Stockholm 2001; MSCS 2004) — wheels. Bergstra–Hirshfeld–Tucker — involutive meadows. Bergstra–Ponse — common meadows |
| Closed case table + separate sticky audit channel | IEEE-754 (1985), Kahan et al.; `totalOrder` added 2008 |
| Kind discipline that travels because the check is local | SI; dimensional homogeneity; the BIPM SI Brochure |
| Preconditions on operations, discharged mechanically; diagnostics closed without totalising | refinement types (Liquid Haskell, F*), dependent types (Agda, Rocq/Coq, Lean), verification conditions (Dafny, SPARK), Hoare-logic preconditions, Ada constrained subtypes |
| Bounds declared in advance and recomputable by any reader | ICH E9; Lan–DeMets alpha spending; O'Brien–Fleming; CONSORT/SPIRIT; the COMPare audit |

**The one empirical result in this manual.** One author, one table, two boundary cases. Brahmagupta **closed** `0/0`, asserting the value `0` — the single line in the set that did not travel, and nobody rescued it in twelve hundred years. (By §9's standard the charge is precise: not that stipulating a value is impossible — Lean does it — but that he stipulated inside a table presented as arithmetic, with no bill.) He **deferred** `a/0`, writing only that the expression stands with zero underneath, naming no value. That line was never falsified. It was only ever *replaced* by successors' guesses — `a/0 = a` (c. 830), `a/0 = ∞` (1150), `1/0 = ∞` (1831) — each of which failed in turn while the deferral stood. Note the failure mode exactly: the first reviser did not fix the wrong line; he filled the *deferred* one, and added a second error.

> **Close what you can compute. Defer, in writing, what you cannot. Never close a case to look complete.**

And ship a numbered table, not a theory. Those clauses survived because they were independently checkable with no derivational dependencies: nothing was derived *from* the false one, so nothing fell when it fell. **A theory fails whole; a table fails line by line.** If a rule in your table has many dependents, it is a theory in disguise.

*Two ancestry claims not made here.* Brahmagupta had no type theory and no set/non-set distinction; he deferred because he had no value to give, not because he held it the wrong *kind* of question. The **shape** of the deferral matches §2; doctrinal ancestry is not claimed. And the story that medieval Europe banned these numerals as satanic is a modern myth — the 1299 Florentine text is a money-changers' guild rule about legible ledger entries (Nothaft). Adoption was by coexistence: Adam Ries's 1522 bestseller teaches reckoning on the lines **and** with the pen, and ran to 100-plus editions. Nothing here displaces anything.

---

## 15. The card

Keep this visible. The rest is commentary.

1. **Name the structure** — in the same sentence as the claim. Adopt this alone and it pays today.
2. **Declare the signature** before arguing about the verdict.
3. **Sort check.** Operand not a member of any carrier → **ILL-TYPED, position *n***. Stop.
4. **Domain check.** Right sort, outside the declared domain → **OUT OF DOMAIN**. Stop.
5. **Solution set.** Empty → **NO SUCH ELEMENT** (not "undefined"). More than one → **NON-UNIQUE** (this is `0/0`; never call it "no such element").
6. **Limits: disagreement refutes, agreement does not establish.** Two routes differ → **NO LIMIT, route-dependent**, record both. Unbounded → **NO LIMIT, divergent**. Bounded, no limit → **NO LIMIT, oscillatory**. Convergent → **VALUE**, and prove it.
7. **Collections vs processes** — ask which before tagging. Not a member of anything, with a citation → **NOT-A-COLLECTION**. Otherwise finite / countably infinite / uncountable. Processes: **NON-TERMINATING** is not an error.
8. **Want a value anyway?** Name the extension and the laws you lose, same paragraph → **EXTENDED VALUE**.
9. **Write the verdict.** Never a blank, never a dash, never a zero. Name the reader and the deadline.
10. **Boundary labels carry equality and rendering. Nothing goes between them — and there is no salvage sentence** (§8).

**Three you may always say.** On the open positive reals `x·x⁻¹ = 1` at every point, no endpoint evaluated. In a field, for `a ≠ 0`, `a/0` has no value and the field proves it, while `0·a = 0` is untouched. Extending is allowed; publish the bill.

**Three you may never say.** Any arithmetic sentence with a boundary label as an operand. "Any two of the three positions fix the third." That a convention is a theorem, or a theorem a convention.

**The test for any rule you add.** Can a hostile stranger, holding only this document and disagreeing with everything you believe, reach the same verdict in bounded time? If not, weaken the rule until they can.

---

*This is a table, not a theory. When one line is shown wrong, strike it and keep the others — that is what the format is for.*
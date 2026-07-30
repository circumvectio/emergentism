---
rosetta:
  primary_level: L6
  primary_column: Ontology
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[A] the formal results; [I] the dialectical reading; [S] the repair"
title: "The Admissibility of Nothing — dialectical and formal treatment of the null state"
status: "ACTIVE — treats the admissibility question; does NOT touch the permanently-open why-anything question"
date: 2026-07-29
evidence_tier: "[A] §3, §4, §5A.1–2, §5A.4, §6A.1–2, §6A.5; [I] §2, §6, §6A.6; [S] §5, §5A.3, §5A.5, §6A.3–4"
parents:
  - 45_THE_TITAN_INVERSION_STRUCTURE.md
  - 00_THE_TRANSCENDENTAL_TRINITY_CANON.md
  - ../../06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md
  - ../../00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md
---

# The Admissibility of Nothing

> **Scope fence, first.** Two questions are constantly confused and must not be.
>
> - *"Why is there something rather than nothing?"* — listed in four owners as
>   **permanently open**, unanswerable from inside the corpus. **This document
>   does not touch it.**
> - *"Is 'nothing' logically admissible?"* — a formal question about logics,
>   with a definite and interesting answer. **This is the one treated here.**
>
> The owner's claim is the second. It is answerable. The answer is not the one
> the claim expects.

## 1 · The claim

Owner, 2026-07-29:

> *"In theory, logically nothing could be the state… things don't have to exist,
> this I believe is the foundational axiom of all axioms… before Dasein there is
> Nicht-sein."*

Formally, two separable assertions. No modal operator is used until a modal
semantics is named:

```text
(N)  Sat_L(¬∃x (x = x))             an empty-domain sentence is satisfiable in L
(F)  (N) is the foundational axiom of all axioms
```

`(N)` is treated in §2–§3. `(F)` is treated in §4, and fails.

## 2 · The dialectical treatment `[I]`

The ancients fought this exact fight, and the framework should know it lost the
first round.

**Parmenides — the strongest objection, and it comes first.** The Eleatic
position is that what-is-not can neither be known nor spoken: thought and being
are the same, and there is no path of inquiry toward non-being. On this view
`(N)` is not false but *unthinkable* — the sentence fails to have content, since
its subject cannot be given. Any Emergentist appeal to `•` must answer
Parmenides before it appeals to anyone else. He is not a foil; he is the reason
the question is hard.

**Plato — the parricide, and the move Emergentism actually needs.** In the
*Sophist*, the Eleatic Stranger commits what he calls parricide against father
Parmenides, and rescues non-being. But note **how** he rescues it: `τὸ μὴ ὄν`
is reinterpreted not as absolute absence but as **the different** (`τὸ
ἕτερον`) — not-being-F is being-other-than-F. Plato could not make absolute
nothing coherent either. He converted it into **difference**.

This is the load-bearing observation. Plato's repair of non-being *is*
distinction — which is precisely `D1`, the first positive freedom, and precisely
what `μ₀` opens. The oldest surviving treatment of nothing arrives at the
corpus's own D1 by a different road. `[I]`, and offered as a lens only.

**Hegel — the indistinguishability, and the honest cost.** The *Science of
Logic* opens with pure `Sein`: being with no determination whatever. Having no
determination, it has nothing to distinguish it from `Nichts`. The two pass into
one another, and their truth is `Werden` — becoming.

Mapped to the seats, this is exact in structure and must be marked as
correspondence, not proof:

```text
•   Nichts                 absence, no determination
○   pure indeterminate Sein   unboundedness, equally without determination
⊙   das Bestimmte          the determinate, the bounded — what appears
```

The cost Hegel pays is the one Emergentism must also pay: if `•` and `○` are
*both* wholly indeterminate, they are not two. The distinctness of the two poles
has to come from somewhere. In doc 45 it comes from a **selected representation**
whose two endpoint images are swapped by inversion — a relational model, not an
intrinsic difference in the opaque seats. That is the honest account: `•` and
`○` are distinguished in this reading by the relation between their images, not
by mathematical content carried by the glyphs themselves.

**Heidegger — the correct location of the insight.** The question of why there
is anything at all rather than nothing, and the priority of `Nicht-sein` to
`Dasein`, is not a proof that nothing is possible. It is the observation that
**Dasein is contingent** — that being-there carries no warrant for itself. That
observation survives everything below, and it is the part of the owner's claim
that stands unharmed.

## 3 · The formal treatment `[A]`

Here is the actual result, and it is sharper than either yes or no.

**In standard first-order semantics, `(N)` is unsatisfiable — by stipulation.** Classical
FOL is presented with the **non-empty domain convention**: every model has
`D ≠ ∅`. Consequently

```text
⊨_FOL  ∃x (x = x)
```

is a **validity**. "Something exists" is a theorem of standard logic. Not
because logic discovered that something must exist, but because the semantics
was defined to exclude the empty structure — largely to keep familiar
quantifier laws clean.

**In inclusive (universally free) semantics, `(N)` is satisfiable — and the empty model is
a model.** Inclusive logic drops that convention and admits `D = ∅`. In the
empty structure:

```text
∀x φ    is vacuously TRUE   for every φ
∃x φ    is FALSE            for every φ
hence   ¬∃x (x = x)         is satisfiable
```

So the empty world is a perfectly well-behaved model. Nothing incoherent
happens. The price is that `∃x(x=x)` stops being valid and some classical
inference patterns require restatement.

### The result

```text
Whether "nothing" is logically possible is NOT settled by logic.
It is settled by WHICH LOGIC IS ADOPTED — and that adoption is a selection.
```

`(N)` is therefore not a discovered necessity. It is **a consequence of choosing
inclusive over classical semantics.** That choice is principled and defensible —
if you intend to reason about the null state you must not adopt a logic that
excludes it by fiat — but it is a choice, and the framework must declare it
rather than inherit it silently.

**This is the fourth instance in one session of the same structure**: something
*selected* presenting itself as something *found*. See doc 45 §7A and the
2026-07-29 corrections on chart-centre and graph-emergence.

## 4 · Why `(N)` cannot be a language-independent axiom of all axioms `[A/S]`

The stronger claim `(F)` fails, and the argument is short.

```text
1. (N) is a satisfiability claim about the sentence ¬∃x(x=x).
2. A sentence has truth-conditions only relative to a language L
   and a consequence relation ⊨_L.
3. Evaluating (N) therefore presupposes L and ⊨_L.
4. Hence L and ⊨_L are prior to (N).
5. A language-independent "axiom of all axioms" would have to be prior to
   L and ⊨_L.
6. From 4 and 5: (N) is not such a language-independent axiom. ∎
```

Sharper still: §3 showed that `(N)`'s truth **varies with the choice of `L`**. A
proposition whose truth-value is decided by a prior selection cannot be the
ground of that selection.

The dependence is not peculiar to this framework. It blocks the specific demand
for a proposition prior to every language; it does not show that ordinary
language-relative axioms cannot be foundational inside a declared theory.
Asserting a ground uses an apparatus of expression and interpretation. The
corpus's own D0 rule therefore keeps the Titans in the metalanguage, articulated
from the D1/D4 descriptive side, never as object-level states inside D0.

## 5 · The repair — the foundational **refusal** `[S]`

The intent survives, and it survives better in the form the framework already
uses for its deepest commitments. Convert the assertion into a refusal:

> **R0 — No necessary being.**
> Emergentism refuses to treat existence as self-warranting. It demands no
> reason for the null state and grants existence no logical entitlement. Where a
> logic is needed to reason about the boundary, the framework adopts an
> **inclusive** semantics and says so.

Why this is a better-typed constitutional form:

- it does not purport to be a theorem prior to language; as a written refusal it
  still requires linguistic and normative interpretation;
- it is honest about the selection in §3 rather than hiding it;
- it binds the holder rather than the world, which is what the 5+1 Constitution
  is for — a refusal binds one's own hand;
- it preserves the whole of the Heideggerian content: **Dasein is contingent**,
  and nothing in the framework may quietly re-derive necessity for it;
- it is killable: if a sound argument establishes a necessary being, `R0` fails
  as a refusal and must be withdrawn openly.

**ADOPTED 2026-07-29 by owner ruling (receipt 176).** `R0` was proposed here as
a candidate sixth refusal or a scholium to Refusal 5; the owner ruling seated it
as neither. It is now the **foundational refusal in K-5**, *prior* to the five
and different in type: the five are practice constraints on how the framework
acts, `R0` is an ontological constraint on what it may assume before acting. It
does not rename the 5+1 architecture. Owner:
[`00_THE_FIVE_PLUS_ONE_CONSTITUTION.md`](../../00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md);
routing: `KSC-28`.

## 5A · The canvas, and why the poles are correlative `[A]`

Owner, same sitting:

> *"An empty canvas gives the potential for things to be painted upon it, while
> a painted canvas implies it being possible to be empty… neither zero and
> infinity can exist independently, one gives rise to the other."*

There is a theorem here, a modal fallacy beside it, and a resolution that doc 45
already proved. Separating the three is the whole work.

### 5A.1 What is false — emptiness does not entail plenitude `[A]`

The tempting step is `◇(nothing) ⟹ everything is possible`. It is invalid.

**Counterexample.** Let the modal space contain exactly two worlds,
`w₁ = ∅` and `w₂ = {a}`. Then `◇(nothing)` is true, `◇(a exists)` is true, and
`◇(b exists)` is **false** — `b` exists at no world. Emptiness of one world
constrains the richness of the space not at all.

This matters because one further step lands on buried ground. "Nothing implies
all potential things" → "all potential things are admitted" is precisely the
**retired plenitude inflation** (DoF ontology §2.3: *everything
coherent-consistent-emergent actually exists, dense in the interior* — retired,
because it smuggles in both an actuality bridge and an unstated measure). The
canvas intuition is one inference from a grave.

### 5A.2 What is true — the empty state excludes least `[A]`

Let `Compat(w)` be the things addable to a state `w` without conflict. Under
monotone consistency, for every state `w`:

```text
Compat(∅) ⊇ Compat(w)
```

Worked instance: with `things = {a, ¬a, b}` and `a` conflicting with `¬a`,

```text
Compat(∅)   = {a, ¬a, b}
Compat({a}) = {b}
```

Every actual content *excludes*. The empty state, having no content, excludes
nothing. That is the canvas insight in its exact form — and note what it says:

> **The empty canvas does not GIVE potential. It WITHHOLDS constraint.**

The two look identical from the inside and run in opposite logical directions.
One is the *absence of an exclusion*; the other would be the *presence of a
production*. Only the first is licensed. `•` is maximally **permissive**, never
generative — the Trinity canon already forbids the Titans being "a generator of
the D-ladder," and `D6` already forbids converting a remainder into a positive
object.

### 5A.3 The converse needs `R0` `[S]`

"A painted canvas implies it could be empty" is
`∃x(x exists) ⟹ ◇¬∃x(x=x)`. This **fails** if anything exists necessarily: the
world would be occupied while emptiness remained impossible.

So the reciprocity the owner wants is not free in either direction. Painting
needs extendability; emptiness needs **no necessary being** — which is exactly
`R0` from §5. The canvas symmetry is not a discovery; it is **what `R0` buys.**

### 5A.4 The resolution — correlativity in the selected model, not paradox `[A/I]`

*"Neither zero nor infinity can exist independently; one gives rise to the
other."* A precise survivor is available in doc 45. It is not a theorem about
Titan seats and it licenses no generation; it is a **correlativity under a
declared representation**.

On the declared projective carrier, the endpoint points form a **2-cycle** of
`ι`:

```text
ι(0) = ∞_P        ι(∞_P) = 0        ι∘ι = id
```

Doc 45 separately selects an interpretive map `r_T` from opaque Titan seats to
tagged sphere features. The induced feature map `ι_*` swaps `r_T(•)` and
`r_T(○)`; neither `ι` nor arithmetic acts on `TitanFrame` itself.

A 2-cycle cannot have one member. On `[0,∞)` the reciprocal `ι(x)=1/x` is
**partial**, because its value at `0` is absent from that carrier. On the
declared projective extension containing both endpoint points it is **total**.

```text
ι is total on the declared endpoint-closed carrier
⟺ its domain contains both members of the endpoint orbit {0,∞_P}
```

That is the theorem available to the owner's sentence. Under the selected
interpretation, the endpoint images are **co-instituted as an orbit**: neither
is generated by the other. Doc 46 §2 reached the corresponding Hegelian reading
— two wholly indeterminate seats can be distinguished only relationally — and
doc 45 supplies one model of that relation.

**Internal precedent, one register down.** `KSC-21` states that D1 opens with
the *oriented pair* `SignedUnit_N = {+1_N, −1_N}` — co-opened, not one then the
other. The Titan poles may be read as the same pattern at the boundary. This is
an `[I]` comparison, not an identity between D1 objects and Titan seats.

### 5A.5 The fence `[S]`

**Correlativity is not generation.** "One gives rise to the other" is licensed
only as *co-definition*, never as production, causation, or temporal priority.
`•` does not make `○`; their represented images are two faces of one
involution.

The owner's own tradition supplies the sharpest guardrail here. In Madhyamaka,
`śūnyatā` is itself empty — `śūnyatā-śūnyatā` — and Nāgārjuna's explicit warning
is against those who convert emptiness into a view or a ground. That is the same
fence as `D6`, arrived at independently and stated more forcefully. Reifying `•`
as a productive ground is the error the tradition names, not a discovery
Emergentism gets to make.

## 6 · The transcendentals `[I]`

The owner reads the Titans as the transcendental aspects of the Good were
thought of. One precision and one genuine correspondence.

**Precision.** The scholastic transcendentals — `ens, unum, verum, bonum` — are
**convertible with being** (*ens et unum convertuntur*). They are coextensive
with being, not above it. So the Titans are not scholastic transcendentals; a
seat that is *beyond* being is a different structure.

**The correspondence that does hold.** Plato places the Good `ἐπέκεινα τῆς
οὐσίας` — beyond being in dignity and power (*Republic* 509b). The Good is not a
being among beings; it is the condition under which beings are and are known.

That is structurally the position `•` occupies, and — importantly — it is the
position the corpus **already** assigns it: `Carrier(D0)={ground_0}` with
`PositiveFreedom = ∅`, and `TitanFrame : Type_Meta`, never an object-level
state. The Titans are not things; they are the framing under which things become
sayable.

So the honest reading is **Neoplatonic rather than scholastic**: the One/Good
beyond being, not a transcendental convertible with it. `[I]`, a lens, and by
`KSC-12` it transfers no proof. Nor may its agreement with §2 or with doc 45 be
counted as confirmation — `DF-15`, one datum.

## 6A · The foundation, stated precisely `[A]`

Owner, same sitting:

> *"No matter what we do we can either take the position that no thing could be,
> or that all things and their relationships even if self-referential could
> exist — and thus both of those are foundational Titans."*

This is the strongest form of the foundational claim reached so far, and it is
**nearly** right. One word fails, and repairing it makes the foundation better.

### 6A.1 The dilemma is not exhaustive `[A]`

"No matter what we do" asserts that every position takes one horn or the other.
It does not. The space is a **2×2**, not a fork, because two independent
questions are in play:

```text
Q1  may the domain be EMPTY?
Q2  may it contain a TOTALITY of itself?
```

| Framework | `Q1` | `Q2` | |
|---|---|---|---|
| classical FOL + ZF | no | no | mainstream mathematics — **takes neither horn** |
| inclusive logic + ZF | yes | no | free logic |
| classical FOL + NBG/MK | no | yes | class theory; `V` as a proper class |
| **inclusive + NBG/MK** | **yes** | **yes** | **Emergentism's corner** |

The top row is live, dominant, and coherent, and it refuses both Titans:
classical FOL makes `∃x(x=x)` valid by convention, and ZF forbids the universal
set by Russell/Cantor. So the disjunction is not forced, and the two horns are
not jointly exhaustive.

### 6A.2 The selected diagnostic — useful, not unavoidable `[S]`

Emergentism chooses to ask two boundary questions:

> Does the declared semantics admit an empty domain? Does the declared ontology
> admit a totality object of the relevant kind?

These questions discriminate familiar frameworks, but the taxonomy is ours.
Silence can leave a specification incomplete rather than constitute an answer,
and another framework may reject the vocabulary or split the questions further.

```text
The DIAGNOSTIC is selected.   Answers inside a declared formalism are checkable.
```

`•` and `○` are therefore **not two propositions the framework proves**. They
index two boundary questions Emergentism elects to track, and Emergentism
currently answers *yes* to both under separately declared formalisms. That is the standing the
corpus already gives them — `TitanFrame : Type_Meta`, framing vocabulary, never
object-level states inside D0. The Titans are the questions the frame must
settle, not entities within it.

This is non-trivial in the right way: not because the diagnostic is forced, but
because **most frameworks occupy a different corner**, and naming which one you
stand in is a real commitment with real consequences.

### 6A.3 The self-reference fork, which is a further choice `[A]`

"Even if self-referential" is ambiguous between two distinct mathematics, and
the corpus must pick:

| Reading | Home | Object |
|---|---|---|
| the totality that is **not** self-membered | NBG / MK | `V`; under Foundation `R={x:x∉x}=V` |
| genuine circularity, `x ∈ x` | **non-well-founded set theory** (Aczel's AFA) | e.g. `Ω = {Ω}` |

Doc 45 §8.2 seated `○` on the **first** reading. "Even if self-referential"
points at the **second**, which is a strictly stronger commitment: AFA replaces
Foundation, and identity of hypersets is given by bisimulation rather than
extensional descent. It is rigorous and available — but it is another declared
selection, not a consequence of the first. **Routed to the K-1/K-2 owners as an
open fork; not decided here.**

### 6A.4 The fence — admitting a totality is not asserting plenitude `[S]`

The sharpest risk in this section. Two claims must never fuse:

```text
FORMAL:        the framework admits a totality-object     (NBG admits V)
METAPHYSICAL:  all things and relations actually exist    (W0-CROWN, E4)
```

NBG admits `V` while asserting nothing whatever about what exists. `E4`'s
plenitude is `[C]` with a **named unpaid debt** (`REACHABLE`, see `RQ-09`), and
the inflation *everything coherent actually exists* is **retired** (DoF §2.3).

So `○` as a foundational Titan means only: *this framework does not forbid the
totality as an object.* It does **not** mean the plenum obtains. Reading `Q2 =
yes` as support for `W0` or `E4` would smuggle a `[C]` wager in through the
foundation — the seam-is-not-the-score error (`DF-21`) at the deepest possible
layer, where it would be hardest to see.

### 6A.5 The proposed reciprocity — the attempted proof fails `[A/S]`

Owner: *"One person could argue that all things coherent and consistent can
exist. Another that no things could exist. But one implies the other as a
possibility."*

The proposed proof does not establish either implication. Its genuine theorem is
narrower and remains useful.

**First, a distinction the argument turns on.** Two objects are routinely fused:

```text
empty THEORY   no sentences asserted   trivially consistent in any consistent logic
empty MODEL    domain D = ∅            EXCLUDED by classical FOL convention
```

Downward closure of consistency yields the **first** and not the second.
Position B is about the empty *model*. So B does not follow from the cheap fact
that the empty theory is consistent — that is the near-miss to avoid.

**What Lindenbaum and Henkin actually establish.**

```text
1. if the background proof system is consistent, the empty THEORY is consistent
2. LINDENBAUM: under its premises, it extends to a maximal consistent theory Δ
3. MODEL EXISTENCE (Henkin): under its premises, Δ has a model
∴ a language-relative maximal theory can have a model
```

The empty-*model* premise `B` appears nowhere in that derivation. Moreover, a
maximal consistent theory in `L` is not a totality of all objects or all coherent
possibilities. Therefore `B ⟹ ◇A` does not follow.

**The reverse direction is also unproved.** A formalism that admits a totality
object need not admit an empty domain; the NBG/MK row in §6A.1 is a counterexample
under standard non-empty first-order semantics. Choosing inclusive semantics can
make the two answers co-admissible, but co-admissibility is not implication.

**A surviving comparison, not an implication.** The constructions just named
have different formal costs, but they must not be relabelled as the Titan
extremes:

```text
empty theory                   cheap relative to a consistent proof system
maximal consistent theory     requires an extension theorem under stated premises
model of that theory          requires the applicable model-existence theorem
universal class V             comes from the separately selected NBG/MK axioms
```

The exact choice strength of a Lindenbaum argument depends on the theorem and
metatheory used, so no blanket "costs the axiom of choice" claim is made here.
None of the first three objects is the universal class or a totality of all
objects; their cost supplies no comparison between `•` and `○`.

**The fence, and it is the whole point.** Every line above establishes
**admissibility**, never **existence**:

```text
consistent  ⟹  admissible-in-the-formalism
consistent  ⟹̸  obtains
```

Lindenbaum hands you a maximal consistent *set of sentences* and Henkin hands
you a *model of those sentences*. Neither hands you a world. Reading this proof
as showing that all coherent things **exist** is exactly the retired plenitude
inflation (DoF §2.3) and exactly `E4`'s unpaid `REACHABLE` debt (`RQ-09`).

So the owner's reciprocity is **unproved even in its formal admissibility
reading**. The survivor is that empty theories, empty models, maximal theories,
totality objects, and obtaining worlds are five different types.

### 6A.6 The pattern, now unmistakable `[I]`

This is the **seventh** instance in one session of a single structure: something
*selected* arriving dressed as something *found*. The Titan equation, the
arithmetic criterion, the chart centre, the graph-emergence claim, the choice of
logic, the foundational dilemma, and the corner-relative reciprocity of §6A.5.

That recurrence is itself the finding. The framework's characteristic move is
**principled selection at a boundary** — which is a legitimate and honest
epistemic act under `E1` and `KSC-04`, and becomes an error only in the last
step, when the selection forgets itself and is cited back as discovery. The
corpus already owns the cure and writes it apologetically: *selected, not
forced.* It should be written as a **standard**, not a confession.

## 7 · Claims and kills

| Claim | Tier | Kill |
|---|---|---|
| standard FOL stipulates non-empty domains, making `∃x(x=x)` valid | `[A]` | exhibit a standard presentation admitting `D=∅` |
| inclusive logic admits the empty model; `¬∃x(x=x)` is satisfiable there | `[A]` | derive a contradiction in the empty structure |
| the admissibility of nothing is logic-relative, hence selected | `[A]` | show one logic is forced independently of any selection |
| `(N)` cannot be a language-independent axiom prior to every semantics | `[A/S]` | supply a coherent semantics-independent meaning of that proposed role |
| Plato's repair of non-being is difference, i.e. D1 | `[I]` | textual reading of the *Sophist* that avoids `τὸ ἕτερον` |
| `•`/`○` are distinguished relationally under the selected representation, not by mathematical content in the glyphs | `[S/I]` | supply an intrinsic differentia for the opaque seats or withdraw the representation |
| `•` sits as the Good sits — beyond being, not a being | `[I]` | none; lens only, transfers no proof |
| Dasein is contingent | `[I]` | a sound argument for a necessary being — which also kills `R0` |
| `◇(nothing)` does **not** entail that all things are possible | `[A]` | the two-world counterexample in §5A.1 fails |
| `Compat(∅) ⊇ Compat(w)` — the empty state excludes least | `[A]` | exhibit a state admitting an addition the empty state forbids |
| `{0,∞_P}` is an endpoint orbit and `ι` is total on the declared endpoint-closed carrier | `[A]` | show the extended reciprocal fails to swap those projective points or is not total there |
| correlativity, never generation: `•` does not produce `○` | `[S]` | any owner deriving content from `•` alone |
| the `•`/`○` dilemma is **not** exhaustive — FOL+ZF takes neither horn | `[A]` | show classical FOL admits `D=∅` or ZF admits a universal set |
| `Q1`/`Q2` are Emergentism's selected boundary diagnostic | `[S]` | a clearer diagnostic displaces it |
| Emergentism's corner is `Q1=yes, Q2=yes` (inclusive + NBG/MK) | `[S]` declared | the corpus is shown to rely on a theorem unavailable in that corner |
| admitting a totality-object ≠ asserting plenitude | `[S]` | any owner citing `Q2=yes` as support for `W0-CROWN` or `E4` |
| Lindenbaum/Henkin concern theories and models, not a Titan implication | `[A]` | a valid derivation that uses the empty-model premise and reaches a totality object |
| admitting an empty domain and admitting a totality object are independent selections | `[A/S]` | derive either answer from the other without an added premise |
| exact metatheoretic cost depends on the chosen extension theorem | `[S]` | name and prove the required choice strength for the declared theorem |
| the proposed reciprocity remains unproved | `[S]` | a type-correct proof of both directions |

**What this document does not do.** It does not answer why anything is
instantiated; that remains permanently open and is not touched. It does not
prove nothing is possible — it shows the question is decided by a declared
choice of logic. It does not derive `•` from the Good. It adds no ontology.

•   ⊙   ○ — *the null state is admissible because we chose a logic that admits it; saying so is the difference between a ground and a wish.*

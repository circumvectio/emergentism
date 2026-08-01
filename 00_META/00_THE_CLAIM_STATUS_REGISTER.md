---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Kṛṣṇa ◇"
  tier: "Executive"
  regime: "Vaiśya"
  register: "[S] status-routing discipline; every claim retains the tier named by its owner"
  canonical_phrase: "Validation status is a second axis — a tier says how strong, a status says how it stands"
title: "The Claim Status Register"
status: "ACTIVE — validation-status routing surface; creates no doctrine and promotes no claim"
date: 2026-07-29
owner: "00_META routing only; K-1…K-7 remain semantic owners"
evidence_tier: "[B] corpus custody of the rows; [S] the status ladder and its one-way rule; [I] the adjudication of each grave"
parents:
  - 00_SETTLED_CANON_REGISTRY.md
  - 00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md
  - ADEQUACY_DOCKETS.yaml
  - ../06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md
  - ../06_ONTOLOGY/04_THE_CONJECTURES.md
  - ../11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md
---

# The Claim Status Register

> A tier says **how strong** a claim's warrant is. A status says **how it
> currently stands**. The corpus had the first axis and not the second, so one
> word — *dead* — was carrying eight different epistemic states at once. This
> register separates them, and in doing so reopens every grave that can honestly
> be reopened.

This surface routes. It creates no doctrine, owns no claim, and promotes
nothing. Where it disagrees with a semantic owner, the owner wins and this file
is the lagging document to repair.

---

## 1 · Two axes, not one

| Axis | Vocabulary | Answers |
|---|---|---|
| **Evidence tier** (existing) | `[A] [B] [S] [I] [C] [D]` | how strong is the warrant? |
| **Validation status** (this register) | the ladder below | where does the claim stand right now? |

They are orthogonal. `[A]`-tier claims can be `FORMALLY-REFUTED` (a proof was
attempted and a counterexample landed). `[C]`-tier claims can be perfectly
healthy (`OPEN-EMPIRICAL`, discriminator named, test unrun). Confusing the axes
is how "we buried it" came to mean both *we proved it false* and *we found it
was only ever a wager*.

The maturity ladder in [`ADEQUACY_DOCKETS.yaml`](ADEQUACY_DOCKETS.yaml) is a
third, separate thing: it tracks how far a research packet has been prosecuted,
explicitly "not truth labels." This register does not replace it.

---

## 2 · The validation status ladder

### Live statuses

| Status | Meaning | Admits |
|---|---|---|
| `FORMALLY-VALID` | proved inside a named formal system, with its hypotheses stated | citation at `[A]`/`[S]` inside those hypotheses only |
| `RECEIPTED` | custodied observation, measurement, build, or dated corpus fact | citation at `[B]` within declared scope and custody |
| `OPEN-FORMAL` | well-posed formal question; neither proved nor refuted | work, at `[C]` |
| `OPEN-EMPIRICAL` | well-posed empirical claim; discriminator and kill named; test unrun | preregistration, at `[C]` |
| `COMPONENT-SUPPORTED` | neighbouring evidence exists for a *component*; the integrated claim does not inherit it | careful citation that names the gap |
| `NARROWED` | the strong form failed; a named weaker form survives and is live under its own owner | citation of the weaker form only |
| `OWNER-REOPENED` | a terminal row restored to **active investigation** by owner ruling, with its counterexample intact | work on the *question*; **never** citation of the refuted form as true |

### Terminal statuses

| Status | Meaning | One-way? |
|---|---|---|
| `FORMALLY-REFUTED` | a counterexample exists **inside the claim's own declared system** | **yes** — as stated, permanently |
| `EMPIRICALLY-REFUTED` | contradicted by sourced observation **within its declared scope** | **yes for that instance**; a new instance may be searched |
| `CATEGORY-ERROR` | the claim mixes types (frame/operand, seam/score, is/ought, analytic/empirical) | **yes** — no evidence repairs a type error; only retyping does |
| `NOT-WELL-POSED` | no truth-conditions yet: ostensive, circular, or unfalsifiable as written | no — but it can be neither validated nor refuted until re-posed |
| `DECORATIVE` | well-posed and unrefuted, but does no work anywhere | no — it returns if it earns a use |
| `PROCESS-DEFECT` | not a claim at all; a failure of the record machinery | n/a — routed to E9 enforcement |

### The one-way rule `[S]`

> A row at `FORMALLY-REFUTED`, `EMPIRICALLY-REFUTED`, or `CATEGORY-ERROR` may
> **never** return to a live status *as the claim it was*. Its counterexample
> stays attached, permanently and visibly.

**Exactly three moves are lawful**, and no fourth exists:

| Move | Requires | Restores |
|---|---|---|
| `NARROWED` | a **named weaker form**, live under its own owner | citation of the weaker form only |
| a new `RQ` row | new ID · the weakening or retyping stated against the parent · the parent's counterexample carried · a discriminator · a kill · a survivor | a *different* question |
| `OWNER-REOPENED` | **all four**: an owner **ruling receipt on disk** · the **counterexample intact** · the **`status_before_reopening`** recorded · a declared **`repair_path`** | **active investigation only** — never the truth of the refuted form |

The four preconditions on `OWNER-REOPENED` are not ceremony. They are the entire
defence against silent thawing, and the validator enforces every one of them.
**A ruling can reopen a question; it cannot delete a counterexample.**

This is not conservatism. It is the whole content of E9 and Refusal 5. Without
it, "work in progress" becomes the mechanism by which a fired kill is quietly
logged as a pass — dead form **DF-22**, the exact move A7 exists to forbid.

### The reopening protocol `[S]`

A **new `RQ` row** — the second of the three lawful moves in §2 — requires all five
of the following. (This is the protocol for *opening a new question*; it is not the
route by which an existing terminal row changes status, which is `OWNER-REOPENED`.)

1. a **new ID** (the old row is not edited);
2. the **weakening or retyping** stated explicitly against the refuted form;
3. the **counterexample that killed the parent**, and why it does not reach the successor;
4. a **discriminator** — what observation or proof would distinguish it from its strongest rival;
5. a **kill criterion** and the **survivor** if it fires.

Anything less is not a reopening. It is the parent claim wearing a new coat.

---

## 3 · `FORMALLY-VALID` — what is actually proved

These hold inside their stated hypotheses and nowhere else. None of them
licenses an ontology, an ethic, a conservation law, or a node-power result.

| ID | Result | System / hypotheses | Tier |
|---|---|---|---|
| `FV-01` | `φ=cot(θ/2)`, `ν=tan(θ/2)` ⟹ `φν=1` | open chart `θ∈(0,π)` | `[A]` |
| `FV-02` | `(φ−ν)²≥0` ⟹ `φ+ν≥2` | same chart, positive coordinates | `[A]` |
| `FV-03` | `B=2/(φ+ν)=sinθ ≤ 1` | same chart | `[A]` |
| `FV-04` | `φ=ν=1` uniquely maximizes `B` and minimizes `φ+ν` | AM-GM, equality at `θ=π/2` | `[A]` |
| `FV-05` | log form: `log φ + log ν = 0`; `B=sech(s)`; `H=2cosh(s)≥2` | `s=log ν` | `[A]` |
| `FV-06` | `1` is the self-dual positive point under inversion on `ℝ₊` | — | `[A]` |
| `FV-07` | on `ℂP¹` inversion fixes `±1` and swaps the orbit `{0,∞}` | — | `[A]` |
| `FV-08` | `ℤ_•=ℤ\{0}` is not additively closed, since `(+1)+(−1)=0` | — | `[A]` |
| `FV-09` | `ℝP¹=ℝ∪{∞_P}` has real dimension one | adjoining one projective point | `[A]` |
| `FV-10` | no map `X→℘(X)` is surjective (Cantor) | ZF-style | `[A]` |
| `FV-11` | the unrestricted Russell class is not a set | ZF-style comprehension | `[A]` |
| `FV-12` | the normalized AND-class `C(0,V)=C(Φ,0)=0`, `C(1,1)=1`, monotone **does not select a unique member** | `[0,1]²→[0,1]` | `[A]` |
| `FV-13` | `A=dλ` locally ⟹ `F=dA=0` | Abelian gauge theory | `[A]` |
| `FV-14` | Fourier duality and noncommuting observables give the uncertainty principle | inherited QM | `[A]` |
| `FV-15` | `G7=M4⊎F3` has exactly seven symbols | **by construction of the declared vocabulary** | `[S]` |
| `FV-16` | under closure + `E−R≥ε>0` + strictly increasing `Q=f(S)`: `S(t₁)≤S(t₀)−ε(t₁−t₀)`, and substrate-supported extractor power falls | declared interval, all three premises | `[S]` |
| `FV-17` | `support(K_X^C) ⊆ support(K_X)` — higher constraints reweight, never manufacture, admissible trajectories | declared constraint model | `[S]` |
| `FV-18` | under budget `Φ̂₄+V₄≤1`: `Φ̂₄=1 ⟹ V₄=0 ⟹ P_node=0` | **only** with the budget premise declared | `[S]` |

**`FV-12` is load-bearing and easy to misread.** It is a proof of
*non-uniqueness*. It is the counterexample that killed `DF-04`, not support for
the product.

---

## 4 · `OPEN` — unvalidated and live

The wager ledger [`W0–W12`](../06_ONTOLOGY/04_THE_CONJECTURES.md) is the owner.
Status here; tiers and kills there.

| ID | Wager (compressed) | Status | Docket |
|---|---|---|---|
| `W0-CROWN` | necessary algebra may be instantiated as *das All* | `OPEN-FORMAL` (metaphysical; may never resolve) | A2 |
| `W1` | `REACHABLE` definable existence-independently | `NOT-WELL-POSED` → see **§6, RQ-09** | A1 |
| `W2` | quantum record / history-space emergence | `COMPONENT-SUPPORTED` (decoherence is real; the integrated reading is not) | A6 |
| `W3` | product beats AND-class rivals in ≥1 preregistered domain | `OPEN-EMPIRICAL` | A6 |
| `W4` | candidate two-factor `Φ×V` out-predicts one general factor under separately defended cardinal proxies | `OPEN-EMPIRICAL` | A6 |
| `W5` | the equator transfers to premise-satisfying real systems | `OPEN-EMPIRICAL` — see **RQ-01** | A6 |
| `W6` | the vow is load-bearing in a frozen domain set | `OPEN-EMPIRICAL` | A4 |
| `W7a–W7e` | five modular force role-affinities | `OPEN-EMPIRICAL`, five legs, independently killable | A6 |
| `W8` | model-mediated future influence | `COMPONENT-SUPPORTED` (future-cue analogues exist) | A5 |
| `W9` | the Egregoreotype five-marker criterion | `COMPONENT-SUPPORTED` (stigmergic trace evidence) | A7 |
| `W10` | the mirror grammar travels within scoped lineages | `OPEN-EMPIRICAL` | A7 |
| `W11` | the `−1` dark twin does functional work | `OPEN-FORMAL` — at risk of `DECORATIVE` | A1 |
| `W12` | the apophatic boundary relation lives in practice | `OPEN-EMPIRICAL` (practice discrimination) | A5 |

The axioms `E1–E10` are not on this table: `E1–E7` are ontology and structure at
their own tiers, and `E8–E10` are *posited conduct*, which no test validates or
refutes. A vow is kept or abandoned, never proved.

---

## 5 · The graves, adjudicated — `DF-01…DF-22`

> **Owner ruling, 2026-07-29 (`174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md`), corrected by `177_WP1_DEFECTIVE_VALIDATOR_HARDENED_2026_07_29.md`: 21 of the 22
> rows are `OWNER-REOPENED`.** `DF-14` was already `NARROWED` — a live status — so
> it was not reopened; `174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md`'s "all 22" was over-broad by exactly one row.
> The status column below records what each was reopened *from*, preserved per
> row as `status_before_reopening`. Every counterexample stands unchanged and
> every row now carries a `repair_path`. Reopening restores active
> investigation, never asserted truth — a ruling can reopen a question, it
> cannot delete a counterexample. Of the three lawful moves in §2,
> `OWNER-REOPENED` is the only one by which **a terminal row itself** returns to
> a live status — `NARROWED` assigns a different status, and an `RQ` row is a new
> row, not this one. It requires a ruling receipt on disk, an intact
> counterexample, a recorded prior status, and a repair path; the validator
> enforces all four.
>
> Separately, the typed **numeric/projective reciprocal facts** are retained by
> proof rather than ruling; no Titan equation is restored — see `TR-01` and
> [`45_THE_TITAN_INVERSION_STRUCTURE.md`](../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md).

Every dead form from [K-7 §2](../11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md)
is here with its status, what actually killed it, and where its live successor
sits. **This is the resurrection**: twenty of the twenty-two are resurrected —
twelve by a live successor alone, carrying the honest weaker claim, and eight by
a newly opened question in §6 — while two are closed with neither. `DF-06` and
`DF-19` carry both a wager successor and an `RQ`, so fourteen rows name a live
successor in all; the disjoint partition is the count table below.

| ID | Dead form | Status | What killed it | Live successor |
|---|---|---|---|---|
| `DF-01` | unification by derivation | `FORMALLY-REFUTED` | four structural breaks (`126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md` §5) | `NARROWED` → candidate translation grammar, GP-11 |
| `DF-02` | ethic-as-theorem | `CATEGORY-ERROR` | is→ought bypass by redefinition | `E8` vow + `W6` conditional lemma |
| `DF-03` | seven-as-forced / Rosetta-universal | `EMPIRICALLY-REFUTED` | planetary confound; one lineage (`130_ROSETTA_ALGEBRA_OBJECTION_ADJUDICATED_2026_07_13.md`, `132_TOMBSTONES_HALAHALA_REAUDIT_2026_07_19.md`) | `W10` inherited grammar |
| `DF-04` | product-uniqueness as keel | `FORMALLY-REFUTED` | `FV-12` — min instantiates the same boundary | `W3` product interior |
| `DF-05` | `φν=1` as conserved discovery | `CATEGORY-ERROR` | coordinate identity read as world law | **none — closed.** `FV-01` is the surviving use |
| `DF-06` | balance hump as empirical law | `EMPIRICALLY-REFUTED` | Munnell trough; GFS retracted | `W5` + **RQ-01** (instrument) |
| `DF-07` | the squid as `η=0` witness | `EMPIRICALLY-REFUTED` | *D. gigas* panmictic, semelparous, weak-targeting | **RQ-02** (new witness search) |
| `DF-08` | literal `D6≡D0` | `FORMALLY-REFUTED` | loop-as-equation fails | `W12`, `D6≈roleD0` |
| `DF-09` | forced Titan-3 | `FORMALLY-REFUTED` | `FV-07` — inversion fixes two points | `W11` dark twin |
| `DF-10` | force bijection | `FORMALLY-REFUTED` | electroweak unification collapses D2/D3 above ~246 GeV | `W7a–W7e`, modular |
| `DF-11` | `N=3`-forced | `FORMALLY-REFUTED` | explicit `ℤ₅` counterexample; the group lemma is false | **RQ-03** (any forcing hypotheses?) |
| `DF-12` | Gödel universal lift | `FORMALLY-REFUTED` | Presburger and real-closed fields are complete and decidable | `E9` as apparatus, not law |
| `DF-13` | three substrates minimum | `EMPIRICALLY-REFUTED` | one human martyr satisfies the framework's own falsifier | **RQ-04** (weak) |
| `DF-14` | frame/operand exclusivity for ordinary numbers | `NARROWED` | ordinary identities are operands | `KSC-04` — opaque `TitanFrame` by explicit type |
| `DF-15` | convergence-as-proof | `CATEGORY-ERROR` | fifteen renderings of one shape are one datum | **RQ-05** (lineage independence) |
| `DF-16` | "extraction is irrational" as Nash | `FORMALLY-REFUTED` in general | private side-payments break it | `W6`; Model A remains valid **in Model A** |
| `DF-17` | civilizational physics | `NOT-WELL-POSED` | `[C]` analogy asserted as physics | **RQ-06** |
| `DF-18` | "dissolves Hard Problem / is-ought / death / free will" | `NOT-WELL-POSED` | unfalsifiable frame-trick; mechanism asserted | Human Condition §11 — re-posed as open |
| `DF-19` | ektropy / F5 as teleological force | `FORMALLY-REFUTED` | `(φ−ν)²` supplies no trajectory | `W7e` + **RQ-07** (declare a dynamics) |
| `DF-20` | numeric coincidences as derivations | `CATEGORY-ERROR` | overlay, not derivation; horn-torus killed by `151_HORN_TORUS_SR_FORMAL_AUDIT_2026_07_20.md` | **RQ-08** |
| `DF-21` | **CC-CORE-1** — kernel → ethics warrant | `FORMALLY-REFUTED` | the seam holds precisely *off* the catastrophe case | **none — closed.** `E8` is a choice |
| `DF-22` | Rosetta kill-criterion mislabel | `PROCESS-DEFECT` | a fired falsifier was logged as a pass | routed to `E9` enforcement, not to a wager |

### What the adjudication shows

| Count | Status | Rows |
|---|---|---|
| **10** | `FORMALLY-REFUTED` — counterexample inside the claim's own system; one-way, hardest class | `DF-01, 04, 08, 09, 10, 11, 12, 16, 19, 21` |
| **4** | `EMPIRICALLY-REFUTED` — the *instance* is closed; a new instance may be sought | `DF-03, 06, 07, 13` |
| **4** | `CATEGORY-ERROR` — no evidence repairs these; only retyping does | `DF-02, 05, 15, 20` |
| **2** | `NOT-WELL-POSED` — neither validated nor refuted until re-posed | `DF-17, 18` |
| **1** | `NARROWED` — weaker form already live | `DF-14` |
| **1** | `PROCESS-DEFECT` — never a claim | `DF-22` |

By successor: **12** already had a live successor under an existing owner, **8**
get a newly opened question in §6, and **2** are closed with no successor.

Only `DF-05` and `DF-21` are **closed**, and both for the same reason: they are
the seam-is-not-the-score error stated twice. Everything else either already had
a live successor or gets one below.

---

## 6 · `RQ-01…RQ-09` — the newly opened questions

These satisfy the §2 reopening protocol. Each is `[C]`, each is weaker or
retyped relative to its dead parent, and each carries the parent's counterexample.

| ID | Question | Parent | Why the parent's kill does not reach it | Discriminator | Kill |
|---|---|---|---|---|---|
| `RQ-01` | Is there an **instrument** that can test the equator-transfer claim at all? | `DF-06` | Revelation 3: a survey of standing respondents cannot test a zero-factor knockout — the dead do not answer questionnaires. The hump died partly of instrument, not only of fact | a design with survivorship-free sampling on premise-satisfying systems | no admissible instrument exists → `W5` stays untestable and must say so |
| `RQ-02` | Does **any** real system instantiate `η_move≈0` as a witness? | `DF-07` | the squid was refuted as *that* witness; the class was never searched | preregistered search across candidate mutualisms with bearer accounting | no candidate survives bearer-complete audit → the vow keeps zero empirical witnesses and remains purely chosen |
| `RQ-03` | Is there **any** hypothesis set under which `N=3` is forced? | `DF-11` | `ℤ₅` refutes the *stated* lemma; it says nothing about other hypotheses | exhibit hypotheses + proof, or a general no-go | no forcing result and no no-go after honest search → `N=3` is selected, permanently |
| `RQ-04` | Is there a non-trivial substrate-plurality claim surviving the martyr counterexample? | `DF-13` | "minimum three" is refuted; "plurality raises durability" was never the claim tested | matched comparison of single- vs multi-substrate persistence | no durability difference → drop the substrate line entirely |
| `RQ-05` | Can **lineage independence** be established for any convergence datum? | `DF-15` | the error was counting one datum as fifteen; genuinely independent lineages would be evidence | historical/philological demonstration of causal separation before counting | no separable lineage → convergence supplies zero evidential weight, permanently |
| `RQ-06` | Does the civilizational analogy yield a **discriminator**? | `DF-17` | the parent asserted physics; this asks only for a testable analogy | one held-out prediction the analogy makes and rival social science does not | no discriminator after honest attempt → retire the analogy as decoration |
| `RQ-07` | Under what **declared dynamics** does `(φ−ν)²→0`? | `DF-19` | the static theorem `(φ−ν)²≥0` is `[A]`; the parent's error was inferring a trajectory from it with no dynamics at all | state a dynamics, derive the trajectory, then test it | no dynamics makes the trajectory non-trivial → ektropy stays buried |
| `RQ-08` | Does any numeric overlay **predict** something not already known? | `DF-20` | the parent claimed derivation; this asks only for novel prediction | one held-out quantitative prediction from the overlay | none → overlays are mnemonic at most |
| `RQ-09` | Can `REACHABLE` be defined **non-circularly**? | `W1` (never a grave; the framework's own named `∅` debt) | this is the load-bearing open debt of `E4`, not a resurrection | a definition from declared initial conditions, allowed transformations, and finite/convergent resource bounds that excludes some target | no non-circular definition → the plenitude wager collapses to redescription and `E4` must say so |

`RQ-09` is not a grave. It is included because it is the single largest unpaid
debt in the corpus and belongs on the same board as everything else.

---

## 7 · What this register refuses

- It does not upgrade any claim. Appearing here is not evidence.
- It does not create an eighth kernel surface. K-1…K-7 own the content.
- It does not soften a counterexample into a "perspective."
- It does not let a reopened question inherit its parent's old strength.
- It does not treat the *absence* of a kill as support.

### Kill criterion for this register — **it fired, and is recorded, not reworded away**

The original criterion read:

> *if a row at `FORMALLY-REFUTED`, `EMPIRICALLY-REFUTED`, or `CATEGORY-ERROR` is
> ever edited into a live status **without a new ID and a new discriminator**,
> this surface has done the exact damage it was built to prevent, and it should
> be deleted rather than repaired.*

**It fired on 2026-07-29.** `174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md` moved all 22 grave rows to
`OWNER-REOPENED` — a live status — with no new IDs and no new discriminators.
Recorded here in the open, because a fired kill quietly logged as a pass is
`DF-22`, and this register exists to forbid exactly that.

**Why the surface is repaired rather than deleted.** The criterion tested for
the wrong thing. It asked for a *new ID*; the damage it names is a
**counterexample vanishing**. No counterexample vanished: all 22 rows retain
theirs, plus their prior status and a declared repair path, under a ruling
receipt on disk. The criterion was written before `OWNER-REOPENED` existed and
could not see a lawful mechanism when one arrived. That is a defective test, not
a defective act — so the test is replaced and the firing stays on the record.

**Amended criterion `[S]`.** This surface has failed, and should be deleted
rather than repaired, if any of the following is ever true:

1. a terminal row appears in a live status **with its counterexample removed,
   emptied, or softened**;
2. an `OWNER-REOPENED` row lacks any of its four preconditions — ruling receipt
   on disk, intact counterexample, recorded `status_before_reopening`, declared
   `repair_path`;
3. a reopened row is **cited as evidence that the refuted form is true**, rather
   than as an open question;
4. this criterion is ever narrowed, weakened, or deleted **without a dated
   receipt recording that it fired**.

**What is actually enforced, stated honestly.** Clauses 1 and 2 are checked by
`check_claim_status.py`, hardened and re-tested on 2026-07-29 against seven
adversarial mutations (`177_WP1_DEFECTIVE_VALIDATOR_HARDENED_2026_07_29.md`). **But nothing invokes it automatically** —
there is no CI job, no hook, no runner. Earlier wording here and in
`172_CLAIM_STATUS_REGISTER_AND_GRAVE_ADJUDICATION_2026_07_29.md`,
`174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md`,
`175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md`, and
`176_THE_FOUNDATION_SEATED_R0_ADOPTED_2026_07_29.md` called it "fail-closed" and said mutations "fail the build";
**there is no build**, and the checker is advisory until a gate exists. **Clauses 3
and 4 are not machine-checkable.** No validator can see a row being *cited* as
evidence elsewhere in the corpus, and none can compel a future editor to record
that this criterion fired before weakening it.

Clause 4 is therefore the one that matters most and the one with the least
protection. It rests on whoever edits this page next.

**Machine check:** [`claim_status/CLAIM_STATUS.yaml`](claim_status/CLAIM_STATUS.yaml)
carries these rows in the corpus JSON-subset form; run
`python3 09_TOOLS/01_SCRIPTS/check_claim_status.py` to enforce the one-way rule,
the reopening protocol, and cross-reference integrity against K-4 and K-7.

•   ⊙   ○ — *a grave with a door is still a grave; the door only opens outward, onto a different question.*

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
> word — *dead* — was carrying several epistemic states at once. This register
> separates them, preserves every grave, and routes any renewed inquiry through
> a different question ID.

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
| `NARROWED` | the strong form failed; a named weaker form survives under its own ID or owner while the parent retains its terminal status | citation of the weaker form only |

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

**Exactly two successor moves are lawful**:

| Move | Requires | Restores |
|---|---|---|
| a named weaker successor | its own ID or owner, with the weakening explicit | citation of the weaker form only; the parent remains terminal |
| a new `RQ` row | new ID · the weakening or retyping stated against the parent · the parent's counterexample carried · a discriminator · a kill · a survivor | a *different* question |

An owner ruling may authorize work on a successor or new question. That is a
workflow act, not a validation status, and it supplies no evidence. **A ruling
can authorize inquiry; it cannot thaw a grave or delete a counterexample.**

This is not conservatism. It is the whole content of E9 and Refusal 5. Without
it, "work in progress" becomes the mechanism by which a fired kill is quietly
logged as a pass — dead form **DF-22**, the exact move A7 exists to forbid.

### The investigation protocol `[S]`

A **new `RQ` row** requires all five of the following. There is no route by which
an existing grave changes to a live validation status.

1. a **new ID** (the old row is not edited);
2. the **weakening or retyping** stated explicitly against the refuted form;
3. the **counterexample that killed the parent**, and why it does not reach the successor;
4. a **discriminator** — what observation or proof would distinguish it from its strongest rival;
5. a **kill criterion** and the **survivor** if it fires.

Anything less is not a new investigation. It is the parent claim wearing a new coat.

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
| `FV-19` | a unique Möbius transformation maps any ordered triple of pairwise distinct source points pointwise to any ordered triple of pairwise distinct target points; two correspondences leave a non-trivial one-parameter stabilizer | projective normalization on `ℂP¹` only | `[A]` |
| `FV-20` | for the selected metric-gradient model, `sinh(2s(t))=sinh(2s₀)e^{-4t}` and `s→0` | selected reciprocal-chart potential, induced metric, and clock; no physical F5 inference | `[S]` |
| `FV-21` | finite words from `1` under successor and reciprocal reach exactly `ℚ⁺`; `√2` is not finitely reachable and `0,∞` are approached boundaries | declared positive-real carrier and finite-word system | `[A]` |

**`FV-12` is load-bearing and easy to misread.** It is a proof of
*non-uniqueness*. It is the counterexample that killed `DF-04`, not support for
the product.

---

## 4 · W-scope — wager rows and current status

The machine schema retains the historical bucket name `open`; it is a W-row
namespace, not an assertion that every row is live. The wager-form ledger
[`W0–W12`](../06_ONTOLOGY/04_THE_CONJECTURES.md) is the semantic owner. Status
is shown here; entry tiers and kills remain there.

| ID | Wager (compressed) | Status | Docket |
|---|---|---|---|
| `W0-CROWN` | necessary algebra may be instantiated as *das All* | `NOT-WELL-POSED`; optional creed survives | A2 |
| `W1` | `REACHABLE` definable existence-independently | `COMPONENT-SUPPORTED`; `FV-21` pays the model-relative component, domain contact remains open | A1 |
| `W2` | quantum record / history-space emergence | `COMPONENT-SUPPORTED` (decoherence is real; the integrated reading is not) | A6 |
| `W3` | product beats AND-class rivals in ≥1 preregistered domain | `OPEN-EMPIRICAL`; merged into W4A and blocked on GP-03 scale custody | A6 |
| `W4` | candidate two-factor `Φ×V` out-predicts one general factor under separately defended cardinal proxies | `OPEN-EMPIRICAL` | A6 |
| `W5` | the equator transfers to premise-satisfying real systems | `OPEN-EMPIRICAL` — see **RQ-01** | A6 |
| `W6` | the vow is load-bearing in a frozen domain set | `OPEN-EMPIRICAL` | A4 |
| `W7a–W7e` | five modular force role-affinities | `OPEN-EMPIRICAL`, five legs, independently killable | A6 |
| `W8` | model-mediated future influence | `COMPONENT-SUPPORTED` (future-cue analogues exist) | A5 |
| `W9` | the Egregoreotype five-marker criterion | `COMPONENT-SUPPORTED` (stigmergic trace evidence) | A7 |
| `W10` | the mirror grammar travels within scoped lineages | `OPEN-EMPIRICAL` | A7 |
| `W11` | the `−1` dark twin does functional work | `DECORATIVE`; ordinary mathematics and optional symbolism survive | A1 |
| `W12` | the apophatic boundary relation lives in practice | `OPEN-EMPIRICAL` (practice discrimination) | A5 |

The axioms `E1–E10` are not on this table: `E1–E7` are ontology and structure at
their own tiers, and `E8–E10` are *posited conduct*, which no test validates or
refutes. A vow is kept or abandoned, never proved.

---

## 5 · The graves, adjudicated — `DF-01…DF-22`

> **Reopening history and current state.** The 2026-07-29 owner ruling
> (`174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md`), corrected by
> `177_WP1_DEFECTIVE_VALIDATOR_HARDENED_2026_07_29.md`, reopened 21 of the 22
> parent forms for investigation; `DF-14` was already `NARROWED`. Receipt
> `239_OPEN_CLAIM_DISPOSITION_2026_08_01.md` completes that transition: twenty
> rows again show their recorded terminal class, `DF-13` is corrected
> from the prior empirical label to `NOT-WELL-POSED`, `DF-14` remains narrowed,
> twenty parent rows route only to explicit successor owners, and two close
> without a successor. Every counterexample, `status_before_reopening`, and
> repair history remains intact. No grave parent is counted as a second active
> investigation beside its successor.
>
> Separately, the typed **numeric/projective reciprocal facts** are retained by
> proof rather than ruling; no Titan equation is restored — see `TR-01` and
> [`45_THE_TITAN_INVERSION_STRUCTURE.md`](../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md).

Every dead form from [K-7 §2](../11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md)
is here with its current status, what killed it, and where any executable
successor sits. The reopening was a transition, not a permanent second claim:
twenty parent rows now merge into a named successor owner, while `DF-05` and
`DF-21` close without one. The disjoint status partition remains the count table
below; successor work never changes the parent result.

| ID | Dead form | Status | What killed it | Successor owner / current route |
|---|---|---|---|---|
| `DF-01` | unification by derivation | `FORMALLY-REFUTED` | four structural breaks (`126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md` §5) | `NARROWED` → candidate translation grammar, GP-11 |
| `DF-02` | ethic-as-theorem | `CATEGORY-ERROR` | is→ought bypass by redefinition | `E8` vow + `W6` conditional lemma |
| `DF-03` | seven-as-forced / Rosetta-universal | `EMPIRICALLY-REFUTED` | planetary confound; one lineage (`130_ROSETTA_ALGEBRA_OBJECTION_ADJUDICATED_2026_07_13.md`, `132_TOMBSTONES_HALAHALA_REAUDIT_2026_07_19.md`) | `W10` inherited grammar |
| `DF-04` | product-uniqueness as keel | `FORMALLY-REFUTED` | `FV-12` — min instantiates the same boundary | `W3` remains empirical only through W4A; neither restores uniqueness |
| `DF-05` | `φν=1` as conserved discovery | `CATEGORY-ERROR` | coordinate identity read as world law | **none — closed.** `FV-01` is the surviving use |
| `DF-06` | balance hump as empirical law | `EMPIRICALLY-REFUTED` | Munnell trough; GFS retracted | `W5` + **RQ-01** (instrument) |
| `DF-07` | the squid as `η=0` witness | `EMPIRICALLY-REFUTED` | *D. gigas* panmictic, semelparous, weak-targeting | **RQ-02** (new witness search) |
| `DF-08` | literal `D6≡D0` | `FORMALLY-REFUTED` | loop-as-equation fails | `W12`, `D6≈roleD0` |
| `DF-09` | forced Titan-3 | `FORMALLY-REFUTED` | `FV-07` — inversion fixes two points | `W11` adjudicated `DECORATIVE` |
| `DF-10` | force bijection | `FORMALLY-REFUTED` | `117_FORCE_LADDER_FORMALIZED_07B.md` and `117_PATH_D_NEGATIVE_RESULT.md` do not recover four force-specific slots; electroweak unification is supporting context | `W7a–W7e`, modular |
| `DF-11` | `N=3`-forced | `FORMALLY-REFUTED` | explicit `ℤ₅` counterexample; the group lemma is false | **RQ-03** narrowed to `FV-19` projective normalization only |
| `DF-12` | Gödel universal lift | `FORMALLY-REFUTED` | Presburger and real-closed fields are complete and decidable | `E9` as apparatus, not law |
| `DF-13` | three substrates minimum | `NOT-WELL-POSED` | signed universal retraction stands, but “substrate,” unit, horizon, and outcome were untyped; the martyr does not independently prove substrate cardinality | **RQ-04** adjudicated `NOT-WELL-POSED` |
| `DF-14` | frame/operand exclusivity for ordinary numbers | `NARROWED` | ordinary identities are operands | `KSC-04` — opaque `TitanFrame` by explicit type |
| `DF-15` | convergence-as-proof | `CATEGORY-ERROR` | fifteen renderings of one shape are one datum | **RQ-05** (lineage independence) |
| `DF-16` | "extraction is irrational" as Nash | `FORMALLY-REFUTED` in general | private side-payments break it | `W6`; Model A remains valid **in Model A** |
| `DF-17` | civilizational physics | `NOT-WELL-POSED` | `[C]` analogy asserted as physics | **RQ-06** |
| `DF-18` | "dissolves Hard Problem / is-ought / death / free will" | `NOT-WELL-POSED` | unfalsifiable frame-trick; mechanism asserted | Human Condition §11 — re-posed as open |
| `DF-19` | ektropy / F5 as teleological force | `FORMALLY-REFUTED` | `(φ−ν)²` alone supplies no trajectory | `RQ-07` narrowed to selected `FV-20`; `W7e` owns physical contact |
| `DF-20` | numeric coincidences as derivations | `CATEGORY-ERROR` | overlay, not derivation; horn-torus killed by `151_HORN_TORUS_SR_FORMAL_AUDIT_2026_07_20.md` | `RQ-08` narrowed to named W7 candidates |
| `DF-21` | **CC-CORE-1** — kernel → ethics warrant | `FORMALLY-REFUTED` | the seam holds precisely *off* the catastrophe case | **none — closed.** `E8` is a choice |
| `DF-22` | Rosetta kill-criterion mislabel | `PROCESS-DEFECT` | a fired falsifier was logged as a pass | routed to `E9` enforcement, not to a wager |

### What the adjudication shows

| Count | Status | Rows |
|---|---|---|
| **10** | `FORMALLY-REFUTED` — counterexample inside the claim's own system; one-way, hardest class | `DF-01, 04, 08, 09, 10, 11, 12, 16, 19, 21` |
| **3** | `EMPIRICALLY-REFUTED` — the *instance* is closed; a new instance may be sought | `DF-03, 06, 07` |
| **4** | `CATEGORY-ERROR` — no evidence repairs these; only retyping does | `DF-02, 05, 15, 20` |
| **3** | `NOT-WELL-POSED` — neither validated nor refuted until re-posed | `DF-13, 17, 18` |
| **1** | `NARROWED` — weaker form already live | `DF-14` |
| **1** | `PROCESS-DEFECT` — never a claim | `DF-22` |

By disposition: **20** parent rows route to an explicit successor owner and
**2** (`DF-05`, `DF-21`) are internally terminal with no successor. A routed
parent is not an additional confirmation or investigation; its counterexample
and terminal status remain the current parent-form result.

---

## 6 · `RQ-01…RQ-09` — reopened questions, now dispositioned

These satisfy the §2 reopening protocol. Each question remains `[C]`, each is
weaker or retyped relative to its parent, and each carries the parent's
counterexample. Status and route record the 2026-08-01 adjudication; an internal
narrowing does not become world evidence.

| ID | Question | Parent | Why the parent's kill does not reach it | Discriminator / result | Kill | Current status / route |
|---|---|---|---|---|---|---|
| `RQ-01` | Is there an **instrument** that can test the equator-transfer claim at all? | `DF-06` | a standing-respondent survey cannot test a zero-factor knockout | survivorship-free sampling on premise-satisfying systems | no admissible instrument → W5 stays untestable | `OPEN-EMPIRICAL`; merged into `W5A-SURVIVORSHIP-FREE-EQUATOR-TRANSFER-01` |
| `RQ-02` | Does **any** real system instantiate `η_move≈0` as a witness? | `DF-07` | the squid was refuted as that witness; the class was not exhausted | preregistered candidate search with bearer accounting | no candidate survives → the vow keeps zero witnesses | `OPEN-EMPIRICAL`; merged into `W6A-NONEXTRACTION-DURABILITY-TRUST-01` |
| `RQ-03` | Is there **any** hypothesis set under which `N=3` is forced? | `DF-11` | `ℤ₅` kills the universal group lemma, not every scoped problem | `FV-19`: ordered triples of pairwise distinct source and target points determine one Möbius map; two correspondences do not | counterexample to sharp three-transitivity/two-point non-uniqueness | `NARROWED`; projective normalization only, no Titan or ontology export |
| `RQ-04` | Is there a non-trivial substrate-plurality claim surviving the martyr counterexample? | `DF-13` | the martyr defeats three organisms/embodied agents, not substrate cardinality by itself | no test until substrate, unit, horizon, and outcome receive a new ID | current wording cannot supply those types without changing the claim | `NOT-WELL-POSED`; terminal, three-function/three-rail survivor retained |
| `RQ-05` | Can **lineage independence** be established for any convergence datum? | `DF-15` | the error was counting one lineage as many | causal separation before blind coding and counting | no separable lineage → zero convergence weight | `OPEN-EMPIRICAL`; merged into `W10-INDEPENDENT-POLARITY-LINEAGE-01` |
| `RQ-06` | Does the civilizational analogy yield a **discriminator**? | `DF-17` | the parent asserted physics; this asks only for comparative typology | one held-out increment beyond frozen rival typologies | no increment → retire as decoration | `OPEN-EMPIRICAL`; `RQ06-CIVILISATIONAL-DISCRIMINATOR-01` |
| `RQ-07` | Under what **declared dynamics** does `(φ−ν)²→0`? | `DF-19` | the static theorem alone supplied no trajectory | `FV-20`: the selected metric-gradient flow converges | counterexample to the declared ODE/solution | `NARROWED`; selected chart model only, W7e owns physical contact |
| `RQ-08` | Does any numeric overlay **predict** something not already known? | `DF-20` | novel prediction is distinct from claimed derivation | unnamed “any overlay” is unbounded; named W7 legs carry native-recovery and held-out kills | no typed named candidate → mnemonic only | `NARROWED`; routed to the named, independently killable W7 candidates |
| `RQ-09` | Can `REACHABLE` be defined **non-circularly**? | `W1` | this is E4's named debt, not a resurrection | `FV-21`: finite model-relative reachability derives a nontrivial exclusion | counterexample to the typed definition or finite-word theorem | `NARROWED`; W1 owns the domain-specific world bridge |

`RQ-09` is not a grave. Its definition-level debt is paid by `FV-21`; the larger
domain-specific actuality and discrimination debt remains with W1.

---

## 7 · What this register refuses

- It does not upgrade any claim. Appearing here is not evidence.
- It does not create an eighth kernel surface. K-1…K-7 own the content.
- It does not soften a counterexample into a "perspective."
- It does not let a successor investigation inherit its parent's old strength.
- It does not treat the *absence* of a kill as support.

### Kill criterion for this register — **it fired, and is recorded, not reworded away**

The original criterion read:

> *if a row at `FORMALLY-REFUTED`, `EMPIRICALLY-REFUTED`, or `CATEGORY-ERROR` is
> ever edited into a live status **without a new ID and a new discriminator**,
> this surface has done the exact damage it was built to prevent, and it should
> be deleted rather than repaired.*

**It fired on 2026-07-29.**
`174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md` purported to move all
22 grave rows to `OWNER-REOPENED` — a live status — with no new IDs and no new
discriminators. The enforced inventory later corrected that scope: 21 rows
made the transition, while `DF-14` was already `NARROWED`. Recorded here in the
open, because a fired kill quietly logged as a pass is `DF-22`, and this
register exists to forbid exactly that.

**Why the surface is repaired rather than deleted.** The criterion tested for
the wrong thing. It asked for a *new ID*; the damage it names is a
**counterexample vanishing**. No counterexample vanished: all 22 rows retain
theirs and a declared repair path, while the 21 rows that actually reopened
also retain their prior status, under a ruling receipt on disk. The criterion
was written before `OWNER-REOPENED` existed and
could not see a lawful mechanism when one arrived. That is a defective test, not
a defective act — so the test is replaced and the firing stays on the record.

**Amended criterion `[S]`.** This surface has failed, and should be deleted
rather than repaired, if any of the following is ever true:

1. any grave appears in a live status, regardless of owner authorization;
2. a grave's terminal status, counterexample or process defect is removed,
   emptied, softened or silently relabelled;
3. an investigation lacks a new ID, parent relation, discriminator, kill or
   survivor, or is cited as evidence that the parent is true;
4. a narrowed Titan survivor is promoted back into arithmetic or
   `FORMALLY-VALID`; or
5. this criterion is ever narrowed, weakened, or deleted **without a dated
   receipt recording that it fired**.

**What is actually enforced, stated honestly.** Clauses 1 and 2 are checked by
`check_claim_status.py`. The 2026-08-01 v2 contract adds explicit disposition,
owner, contract, resolution, merge, and 48-row lifecycle custody, including
duplicate-key rejection and mutation controls. `gate.sh` invokes the checker,
and `.github/workflows/gate.yml` invokes that gate in CI. Earlier wording here and in
`172_CLAIM_STATUS_REGISTER_AND_GRAVE_ADJUDICATION_2026_07_29.md`,
`174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md`,
`175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md`, and
`176_THE_FOUNDATION_SEATED_R0_ADOPTED_2026_07_29.md` called it "fail-closed" and said mutations "fail the build";
**there is no build**; that statement is historical and no longer current.
**Clauses 3 and 4 are not fully machine-checkable.** No validator can see every row being *cited* as
evidence elsewhere in the corpus, and none can compel a future editor to record
that this criterion fired before weakening it.

Clause 4 is therefore the one that matters most and the one with the least
protection. It rests on whoever edits this page next.

**Machine check:** [`claim_status/CLAIM_STATUS.yaml`](claim_status/CLAIM_STATUS.yaml)
carries these rows in the corpus JSON-subset form; run
`python3 09_TOOLS/01_SCRIPTS/check_claim_status.py` to enforce the one-way rule,
the investigation protocol, and cross-reference integrity against K-4 and K-7.

•   ⊙   ○ — *a grave with a door is still a grave; the door only opens outward, onto a different question.*

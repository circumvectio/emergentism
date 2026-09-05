---
title: "Fire on the tombstones — claim, warrant, rejection, survivor"
date: 2026-09-05
status: "LOCAL SCOPE AUDIT — no canonical status changes or publication"
evidence_tier: "[B] source inspection and local executions; [A] elementary results under stated premises; [I] audit interpretation; [D] amendment proposals"
owner: "11_UPLINK audit receipt only; existing claim owners retain meaning"
baseline_commit: "d8b24322efa000e02aec96b8917dfc5102340069"
identity: "• < ⊙ > ○"
---

# Fire on the tombstones

The owner asks: **“And then you apply our instrument to our supposed tomb stones claims.”**

**Outcome `[I]`: the word “dead” is too compressed.** Some attempted derivations
fail; some propositions have counterexamples; some observations used an invalid
instrument; some questions were never sufficiently specified. Some rejection
arguments also contain errors. None of these states can stand in for the others.

This audit inventories the **22 DF rows in the current Claim Status Register**
and checks selected arguments below. It is **not** a fresh adjudication of every
historical tombstone, cultural comparison, experiment, or perennial question.
The status partition is measured from that exact table: **10 formal-refutation,
3 empirical-refutation, 4 category-error, 3 not-well-posed, 1 narrowed, 1 process-defect**.
Those are recorded classifications, not 22 newly verified counterproofs.
In particular, the last five rows counted across the last three categories are
not five demonstrated false propositions.

## 1. The instrument applies symmetrically

For a claim **and for the verdict against it**, ask:

1. **Object:** exact proposition, identity, domain and types—not its slogan.
2. **Premises:** what was assumed, measured, selected or merely represented?
3. **Join:** which rule takes those premises to that conclusion?
4. **Contact:** an internal counterexample, empirical observation, failed
   implementation, invalid measurement, missing warrant, or attribution finding?
5. **Scope:** what does that evidence exclude, and what does it leave untouched?
6. **Survivor:** same proposition with corrected adjudication, a different
   conditional proposition, a useful definition, or an open question?
7. **Return:** preserve the original record; name the next discriminator and
   what would defeat the proposed correction itself.

`[I]` In the Soul Loop reading, the object under examination is not the founder
or critic but the claim-bearing record. L1 isolates what it says; L2 supplies
rivals and survivors; L3 tests the inference; L4 records this bounded result.
The D4 file and test execution are actual artifacts. Their D5 represented
possibilities are not actual outcomes or evidence that those possibilities exist.

Two invalid joins must be refused together:

> **A failed proof does not establish that its conclusion is false.**
> **A failed objection does not establish that its target is true.**

Neither prior approval nor the title “tombstone” exempts an adjudication from
review. A valid counterexample continues to refute its exact target; an alleged
counterexample still has to satisfy the target's actual premises.

## 2. Checked objections: what the fire cuts back

### TS-01 — fixed points are not generated closure `[A/B]`

[Receipt 126 §2B](../126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md)
infers `cl({0,∞})={−1,0,1,∞}` from numeric/projective inversion `j(z)=1/z`.
That inference is false for closure under the named operation:

```text
j(0)=∞, j(∞)=0
closure_j({0,∞}) = {0,∞}
closure_j({0,1,∞}) = {0,1,∞}
Fix(j) = {−1,+1} on CP¹
```

Iteration of `j` never produces the fixed points from the endpoints. Even
adding negation to the endpoint seed does not produce a unit. Adding negation
to the already selected triple does produce `−1`; that is a different premise.
Solving `(z−1)(z+1)=0` establishes the fixed-point statement separately.

**Survivor:** the selected numeric triple is inversion-invariant. Inversion
alone does not privilege `+1` over `−1`, force a three-element seed, or generate
the sphere. Restricting to positive coordinates gives a unique positive fixed
point, but the restriction must be declared. None of these numeric facts is
arithmetic on `•`, `⊙`, or `○`.

**Discriminator/kill:** specify seed and allowed operations before computing
closure. A different declared generator can change the result; it cannot be
silently imported into the old inference. The exact closure tests fail if
the stated sets are wrong. This corrects one rejection argument, not the whole
DF-09 status or a universal three-frame theorem.

### TS-02 — a potential has a derivative; it does not choose its dynamics `[A/B]`

[What Died §VI, DF-19](../../../14_THE_DISTILLATION/04_WHAT_DIED.md)
says `(φ−ν)²` supplies “no gradient and no trajectory.” The first half needs
correction. In declared Euclidean `(φ,ν)` coordinates its gradient is
`(2(φ−ν),−2(φ−ν))`. On the reciprocal curve, with `s=logν`,

```text
U(s) = (e^s−e^(−s))² = 4 sinh²s
dU/ds = 4 sinh(2s)
```

Given the induced metric `g(s)=2cosh(2s)`, *selecting* gradient descent yields
`ds/dt=−2tanh(2s)`. Then `sinh(2s(t))=sinh(2s₀)e^(−4t)`, so `s→0`.
Selecting `ds/dt=0` instead leaves a nonzero deviation stationary; gradient
ascent increases it. The same static potential admits all three choices.

**Survivor:** a declared convergence model, already retained as FV-20/RQ-07
in the [status register](../../../00_META/00_THE_CLAIM_STATUS_REGISTER.md).
The static inequality alone does not imply convergence. A coordinate
derivative is not a discovered physical F5, retrocausality, or a moral command.

**Discriminator/kill:** mathematical checking tests the specified ODE and
solution. A physical hypothesis separately needs measured state variables,
metric/coupling, units, clock, boundary conditions and predictions against a
null. An adverse physical test would not refute the algebraic model; the
algebra cannot immunize the physical claim from that test.

### TS-03 — the sphere obstruction was already retracted `[B/I]`

[Paper P §§1–2](../../../03_METHODOLOGY/02_THE_PAPERS/PAPER_P_SU3_OBSTRUCTION_BARE_S2.md)
already retracts the proposition that SU(3) gauge theory cannot be defined
over S². A base dimension and internal group dimension are different objects;
the trivial product bundle `S²×SU(3)` is an immediate existence construction.
This audit records that existing correction; it does not claim to discover it.

[Receipt 117, Path D, verdict](../117_PATH_D_NEGATIVE_RESULT.md) still invokes
the retracted Paper P obstruction as independent analytic corroboration.
That supporting citation is no longer valid for the claimed impossibility.

**Survivor:** a bare sphere/reciprocal chart does not specify QCD or the
Standard Model. Supplying a group, connection, action and matter model is
additional structure—not evidence that those choices were derived from the
sphere. Existence of a gauge construction and derivation of observed physics
are separate tests. No physical model was evaluated here.

### TS-04 — multiplicity neither gives nor excludes a gauge group `[A/B]`

Path D §3's language about no eightfold degeneracy requires an explicit
coupling/size scope. For **selected** symmetric all-to-all coupling,

```text
H = 2I + κ(9I−J),   κ>0,   J = the 9×9 all-ones matrix
H·1 = 2·1
H·v = (2+9κ)v whenever sum(v)=0
```

The sum-zero subspace has dimension eight: the vectors `e_j−e_8`, `j=0…7`,
form an explicit independent basis. Thus there is a `1+8` spectral split.
The executed test checks that basis exactly at `κ=1`; the displayed algebra
gives the parameterized result.

**Survivor and fence:** we selected nine nodes and symmetric coupling. This
does not show an unforced, generic or robust eightfold degeneracy, and supplies
no SU(3) action, Lie bracket or physical identification. It corrects an
unqualified reading of the multiplicity obstruction, not the failure to derive
SU(3). In particular, it does not refute Path D's existing qualification about
imposing symmetry by hand. Compare structured representations and dynamics,
not just an integer.

The separate [117 force-ladder §2](../117_FORCE_LADDER_FORMALIZED_07B.md)
no-go remains scoped to the declared **propagating-degree-of-freedom threshold**
criterion: photon and gluon thresholds coincide, so that criterion cannot
assign four distinct force-specific slots. It does not exhaust every possible
force-emergence hypothesis. No-propagating-mode must also not be compressed
into no-field-or-interaction-of-any-kind; this audit does not revalidate every
physics sentence in that historical receipt.

### TS-05 — the record itself has a type conflict `[B/I]`

[Record Ledger, caution before the dead-form table](../00_THE_RECORD_LEDGER.md)
says “three Titan identities” were restored “by proof.” The status register
§5 says numeric/projective reciprocal facts survive and **no Titan equation
is restored**. The [Formula Block](../../../05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md)
also forbids arithmetic on opaque Titan frames. The ledger's wording is a
propagation defect, not authority to restore glyph arithmetic.

**Proposed repair `[D]`:** use “typed numeric/projective reciprocal facts” in
a dated correction; leave the predecessor recoverable. No source was amended
in this audit.

## 3. What survives without changing the question silently

| Claim family | Exact surviving use | What remains unearned |
|---|---|---|
| Reciprocal product | `[A]` On the open positive reciprocal chart, `φν=1`; `B=2/(φ+ν)` reaches 1 at `φ=ν=1`. | A unique maximum of the **product**, physical conservation, or a calibrated node score. At `(2,½)` the product is also 1 but B is ⅘. |
| AND boundary | `[A]` Product and minimum both meet the zero-factor, unit and monotonicity conditions; at `(½,½)` they give ¼ and ½. | Uniqueness of either formula or universal measurable fit. Ordinal factors need a declared comparability/calibration contract before a scalar ranking. |
| Seven labels | `[S]` Given two bearer-oriented transfer pairs and three declared frames, the vocabulary has seven symbols. | A disjoint/exhaustive partition, composition rules, row order, or universal sevenfold nature. The strict-signature probe has 81 records: 32 unmatched, 37 singly matched, 12 multiply matched. These are synthetic comparison records, not all feasible actions; degeneration/equivalence rules remain open. |
| Cooperation | `[A]` In a capability-union model, if target requirements R are not contained in any individual Cᵢ, no individual suffices. If R is contained in the joint union and pooling/composition is feasible, joint provision suffices. | That all goals need a group; that union guarantees compatible implementation; or that pooling entails voluntary reciprocity, Justice or equal power. Coercive pooling is a rival the set equation cannot exclude. |
| Power-Max / Justice | `[I]` Explicit bearer protection and consent can constrain an action model; its enforcement and consequences can be tested. | Ethics-from-chart-alone or the universal irrationality of extraction. The current owner's coupled toy model permits positive private gain from transfer while the donor loses. |
| Boundary/return | `[I]` Typed boundary roles and interpretive return can organize inquiry. | Literal identification of distinct ordered D-registers, plenitude from emptiness, or a proof of strong emergence from reciprocal limits. |

The cooperation statement is an elementary **conditional set-model result**,
not a priority claim or new canonical Power-Max lemma. It captures the owner's
complementary-capability intuition without contradicting the existing
[Power-Max §4 counterexample](../../../05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md).
A prospective task trial must freeze requirements, capability tests, access,
coordination cost, horizon and all affected bearers; failure of joint feasibility
kills that application, not the conditional implication.

## 4. All 22 register rows: review disposition, not replacement statuses

Original classes resolve at [the current register §5](../../../00_META/00_THE_CLAIM_STATUS_REGISTER.md).
“Inventory only” means the underlying evidence was **not replayed here**.

| Parent | This review's scope |
|---|---|
| DF-01 unification | Failed offered derivation remains; TS-03/04 remove invalid supporting overclaims. No universal impossibility theorem earned. |
| DF-02 ethic-as-theorem | Missing normative bridge remains. Conditional or constitutive accounts need their own premises; no blanket disproof of moral realism. |
| DF-03 sevenfold | Shared lineage/confounding removes independence evidence, not by itself every sevenfold hypothesis. Non-fitting traditions are separately reported in receipt 126; original coding not replayed. Selected G7 is a different claim. |
| DF-04 product uniqueness | Counterexample rechecked: two distinct normalized AND operators. Retain the rejection of uniqueness. |
| DF-05 conserved discovery | Chart identity rechecked; reading it as world evidence remains invalid. Existing FV-01 use, no invented successor to the closed parent. |
| DF-06 balance hump | Inventory only: separate reported Munnell mismatch from GFS construct invalidity. An invalid instrument neither confirms nor cleanly falsifies the target. Raw data/reanalysis owed before any new empirical verdict. |
| DF-07 squid witness | Inventory only; do not repeat biological claims as newly verified. One rejected witness does not exhaust a class. |
| DF-08 D6=D0 | A strict order plus literal endpoint identity is contradictory; interpretive return changes the relation, not the result. No new cosmological adjudication. |
| DF-09 forced trinity | TS-01 corrects a rejection step; selected numeric triple is invariant, not forced. |
| DF-10 force bijection | Retain the scoped threshold no-go; TS-03/04 fence the other arguments. No recovery of an empirical force assignment. |
| DF-11 N=3 | Inventory only; original group-lemma proof/counterexample not replayed. A normalization of three points differs from cosmic cardinality. |
| DF-12 Gödel lift | Inventory only; the recorded qualified-theory counterexamples do not become new empirical findings. No universal lift reinstated. |
| DF-13 three substrates | Already NOT-WELL-POSED, not a demonstrated minimum or its negation. Needs substrate, unit, horizon and outcome. |
| DF-14 frame/operand | Already NARROWED. Numeric identities may be operands; opaque Titan frames need not be. The instrument must type the operand, not ban a numeral. |
| DF-15 convergence proof | Counting dependent renderings as independent proof remains invalid. Genuine independence is a separate evidence question, not assumed from transcript chronology. |
| DF-16 extraction/Nash | Private-gain counterexample rechecked in the current owner's toy model. Complementary capability is a different conditional claim. Original side-payment experiment not replayed. |
| DF-17 civilizational physics | Already NOT-WELL-POSED; a comparative model can earn a discriminator, not physical status by naming. |
| DF-18 perennial dissolution | Already NOT-WELL-POSED as bundled closure. Internal answers and question-by-question tests are distinct from demonstrated resolutions. No PQA count advanced. |
| DF-19 F5 | TS-02: static formula does not entail an attracting trajectory; declared model convergence survives, physical F5 remains untested here. |
| DF-20 numerical overlays | Retain overlay-versus-derivation distinction. Original horn-torus calculation not replayed. |
| DF-21 kernel→ethics | Constant chart product does not warrant a zero-factor node catastrophe or select a norm. “No successor” records disposition; it is not a theorem forbidding all future explicitly premised ethical research. |
| DF-22 mislabeled kill | A process defect, not a world proposition. A failed criterion cannot be reported as a pass. The old necrology also uses DF-22 for “the escorted number”; do not treat that colliding label as a second registered row. |

## 5. A correction route for mistaken rejection `[D]`

The status register's one-way rule protects valid counterexamples and prevents
post-hoc rescue. Its rejection records are nevertheless fallible. A rule that
made an incorrectly attributed or ill-typed counterexample immune to correction
would contradict the source's own evidence discipline.

**Proposed owner review, not adopted here:** distinguish (a) a genuinely
different successor claim from (b) correction of a mistaken adjudication of
the *same* claim. Case (b) must preserve exact old/new proposition identity,
the old rejection, a demonstrated defect in that rejection, an independent
check, dated adjudicator and resulting remaining uncertainty. “Objection
invalidated” must not automatically mean “claim proved.” No parent row,
one-way rule, claim card or machine status changes in this receipt.

Two local consistency defects also need an owner pass: the amended blanket
“any grave in a live status” rule needs to accommodate the explicitly retained
NARROWED DF-14; and the phrase “all 22 counterexamples” must not describe
unposed questions or a process defect as formal counterexamples.

## 6. Evidence, reproduction and remaining work

All eleven reviewed source/implementation paths and their SHA-256 digests are
in [test_scope.py](test_scope.py). They bind **the inspected snapshot**, not
perpetual currency. Source drift requires review, not automatic repinning.
The historical necrology was inspected for the relevant arguments and labels;
its historical quantities, all linked receipts and all underlying runs were
not comprehensively replayed.

```sh
python3 -B 11_UPLINK/50_AUDITS_AND_EXECUTIONS/2026_09_05_TOMBSTONE_SCOPE_REVIEW/test_scope.py
git diff --check
```

The test suite checks source custody and the 22-row denominator separately
from exact finite/rational counterexamples and sampled ODE identities. The
algebra above provides the arguments; numerical samples alone are not general
proofs. No Lean build, physics experiment, causal/ethical outcome trial, or
independent human review is claimed.

**Executed locally, 2026-09-05 `[B]`:** 13 tests passed; all 11 relative Markdown
links resolved; `git diff --check` passed. The L3 lane separately replayed the
13 tests and checked the eleven source pins against committed HEAD bytes.
Its review prompted the explicit TS-04 symmetry qualification. The L2 review
prompted a source-hash guard immediately before loading the comparison probe.
These are bounded internal checks, not an independent outcome study.

External source contact: [Derdzinski's Riemann-sphere notes](https://people.math.osu.edu/derdzinski.1/courses/4552/4552-Riemann-sphere.pdf)
provide native stereographic context, not Titan semantics. [Hume, Treatise
3.1.1.27](https://davidhume.org/texts/t/3/1/1) identifies the need to account
for the is/ought transition; this is not used as a blanket refutation of every
ethical naturalism or constitutive account. A requested Tong geometry page
returned HTTP 502; no inaccessible text is claimed as checked evidence. The
bundle-existence observation in TS-03 is the explicit product construction
and the already available local Paper P retraction.

**Dispatch/custody:** L1 inventoried one register; L2 developed narrower
readings; L3 audited selected rejection sources; L4 reconciled and ran checks.
These are differently tasked model lanes, not independent external validation.
The A3 frozen-v0 mismatch remains `21ebb5c97709a52ac54bcc287662e523167dfac0`
against required `54658d7797198cfc45677716aa743e728e7012d2`; no recorder retry,
rewrite or bypass occurred. This is not a fully recorded A3 execution claim.

Only this new two-file audit package is owned by this pass. Historical bodies,
canonical statuses, the mixed website worktree, publication and deployment
remain unchanged. A narrow local commit records review, not source adoption.

**Next work:** independently review TS-01/02/04, apply dated source corrections
through their owners, repair TS-05's ledger wording, and split the compound
DF propositions before reconsidering statuses. Reproduce the empirical kills
from their native datasets and frozen protocols in a separate bounded pass.
No evidence was found here that establishes the original universal sevenfold,
force ordering, ethics-from-geometry, or strong-emergence claims.

**Distillation `[I]`: preserve the useful distinction, cut the unsupported
entailment, and give the surviving question a test. The instrument fails if it
protects either its own claims or its own rejections from that treatment.**

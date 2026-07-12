# PD-11 Contact-Bearing Compatibilism — Design

**Status:** Approved in conversation on 2026-07-12; reconciled against `main@992a8382280d260b2440c140cc28568b468b1678` before user review.

**Purpose:** Repair the canonical free-will entry so it becomes a contact-bearing operational compatibilist model rather than a universal-solvent relabeling. Add a suite-wide contact gate that distinguishes a genuine reframe from a decorative register reassignment.

**Evidence ceiling:** `[S]` for internal Burri type grammar; `[I]` for the compatibilist crosswalk; `[C/open]` for metaphysical freedom, D5 irreducibility, or ultimate moral desert. No free-will conclusion is `[A]` or `[B]`.

## 1. Decision

Repair the existing owner in place:

- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_11_FREE_WILL_VS_DETERMINISM.md`

Do not create another paradox note. A duplicate would fork authority and deepen the corpus's coherence-without-contact failure.

Update the two standing route/control surfaces:

- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_00_INDEX.md`
- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/00_PARADOX_SUITE_AUDIT.md`

### Concurrency addendum

After the design was approved, canonical `main` gained:

- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/00_THE_LENS_AS_COMPASS_PENDING_K2.md` at `5c8aa38`;
- its signed-at-tier receipt `116` at `4520f26`; and
- the public `/compass/` surface in `4e9ad2b`, verified live by ship receipt `118` at `0934411`; and
- receipt `119` at `992a838`, which states explicitly that map-compression is maximal while territory-compression is unrun, and identifies contact as the next binding constraint.

The new Lens repeats the old PD-11 axis error by describing downward action as a μ-transition. Therefore the implementation must also update only the PD-11 row and contact-gate wording in:

- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/00_THE_LENS_AS_COMPASS_PENDING_K2.md`

Receipts `111`, `114`, and `116` remain immutable provenance. The public `/compass/` page is outside scope. The added derivative path is a required owner-first propagation, not a new paradox or scope expansion.

Receipt `119` strengthens the contact-gate requirement but does not change the implementation scope: the first territory test belongs to a separate preregistered empirical program, not to PD-11 prose.

## 2. Claim boundary

The Burri calculus dissolves one ambiguity, not the metaphysical free-will problem.

It shows that the following claims are jointly satisfiable:

1. actual causal evolution is lawful or deterministic; and
2. an embedded agent models counterfactual actions, responds to reasons, commits one action through embodied means, receives consequences, and updates its model and selector.

It does **not** establish:

- that the identical complete past and laws could produce a different action;
- that D5 is ontologically irreducible;
- libertarian freedom;
- consciousness-caused quantum collapse;
- control over an Everett branch or a Born-rule outcome;
- ultimate moral desert.

The honest result is **operational compatibilism** `[I]`.

## 3. Typed agency schema

Let:

```text
x_t ∈ X             actual causal state
Ω_t                 histories/actions represented as reachable
M_t                 fallible model
V_t                 embodied means, control, and authorization
G_t                 reasons, values, and selector state
a_t = χ_t(Ω_t,M_t,V_t,G_t)
R_{t+1} = r(x_t,a_t,x_{t+1})
(M_{t+1},G_{t+1}) = Loop(M_t,G_t,R_{t+1})
```

Define nomological determinism:

```text
Det(F) := ∀x ∈ X, ∃!x' ∈ X such that x' = F(x)
```

Define operational reasons-responsiveness:

```text
Resp(χ) := ∃r₁,r₂ [r₁ ≠ r₂ ∧ χ(do(r₁)) ≠ χ(do(r₂))]
```

`Det(F) ∧ Resp(χ)` is satisfiable. A deterministic selector may produce different actions under counterfactual changes in reasons, model, or means. The intervention changes an input; it does not hold the total past fixed.

Two modalities must remain distinct:

- **model-relative ability:** had reasons, model, or means differed, the action would have differed;
- **libertarian ability:** with the identical complete past and laws, another action could occur.

The schema supports the first. It does not settle the second.

Call χ a **typed agency schema**. The word **mechanism** becomes earned only when the variables, dynamics, intervention semantics, and comparative predictions are operationalized.

## 4. Burri register discipline

The repaired action loop is:

```text
D5 fallible option field + model + reasons
                  │
                  χ through D4 means and authorization
                  ▼
D4 enacted action ──▶ receipt ──▶ next model and selector
```

- μ is emergence upward: `D_n → D_{n+1}`.
- χ is finite commitment downward: D5 foresight/selection through D4 means to D4 action and receipt.
- χ does not turn a decision into a quantum measurement.
- Dasein is the situated finite agent who deliberates and commits, not a mind that selects a physical branch.
- Use **option cone**, never “widened physical light cone.” The physical light cone remains bounded by spacetime and `c`.

Any PD-11 sentence that calls D5→D4 commitment a μ-transition is a source error and must be removed.

## 5. Quantum quarantine

Quantum mechanics is optional correspondence, never dependency.

- Everett's relative-state formulation has no fundamental collapse.
- A von Neumann evolution/reduction distinction does not prove Burri registers.
- Conditional reversal of weak measurement prevents “measurement is irreversible” from serving as a clean transferred falsifier for free will.
- An agent selects an action from its modeled option set; it does not select a Born-rule outcome.

**Removal test:** delete every quantum sentence from PD-11. If the χ–receipt calculus changes, the operational claim was improperly depending on analogy.

No edit to PD-22A or the quantum owner spine is included here. Their repair belongs to the formal Kintsugi owner pass; PD-11 simply refuses to import their proof debt.

## 6. Decisive countermodels

The repaired document must include or answer these cases:

1. **Deterministic but irreversible:** `F(x)=0`. Determinism is not reversibility.
2. **Reversible but stochastic:** a symmetric two-state Markov chain can satisfy detailed balance while having more than one successor. Reversibility is not determinism.
3. **Deterministic agency:** `χ(r)=r` over `r∈{0,1}` is deterministic and reasons-responsive.
4. **Indeterminism without freedom:** a quantum-random selector that ignores reasons and consequences supplies alternatives without authorship.
5. **Unpredictability without freedom:** chaotic or cryptographic evolution can be unpredictable beforehand and deterministic.
6. **Manipulated selector:** a coherent, capable, reasons-responsive agent may have coercively installed values. χ alone does not establish ownership, consent, justice, or desert.

These prevent determinism, reversibility, unpredictability, randomness, authorship, and moral responsibility from being collapsed into one property.

## 7. The contact gate

A register distinction is necessary but insufficient. A paradox reframe counts as contact-bearing only when it supplies all five fields:

1. **Typed error:** the exact objects/registers that were fused.
2. **Discriminator:** a countermodel or observation that separates the proposed reading from a rival.
3. **Constraint:** a novel comparative prediction, intervention result, or forbidden outcome.
4. **Kill/downgrade rule:** what evidence retracts the mechanism claim or demotes it to vocabulary.
5. **Removal test:** proof that a Rosetta/quantum/domain analogy is non-load-bearing.

If any field is absent, status is `RELABELING/HEURISTIC`, not `REFRAMED-CONTACT` and never `DISSOLVED`.

### PD-11 contact program

- Hold D4 means approximately fixed.
- Measure the breadth/accuracy of represented options, reason weights, model accuracy, action, and receipt.
- Intervene separately on reasons, modeled options, and means.
- Compare held-out prediction and intervention stability against a simpler causal-policy baseline with no D5-labeled variables.
- Compare receipt-enabled learning with yoked/no-feedback controls.

Kill or demote the mechanism claim if:

- the simpler policy predicts equally well;
- option-model interventions have no stable effect;
- receipts reveal post-hoc narration rather than updating;
- register assignments can be fitted after every possible outcome; or
- lower-level dynamics derive the selector and outcomes without D5 primitives or explanatory compression.

The remaining vocabulary may still be useful `[I]`; it simply cannot claim mechanism or irreducibility.

## 8. Beauty, Truth, Justice

### Beauty

The compact χ–receipt Soul Loop unifies deliberation, commitment, consequence, and learning without importing quantum metaphysics.

### Truth

- overall PD-11 status: `REFRAMED/PARTIAL`;
- `[S]`: internal μ/χ and D4/D5 typing;
- `[I]`: compatibilist/Dasein interpretation;
- `[C/open]`: irreducibility, libertarian ability, and metaphysical freedom;
- quantum correspondence removable and explicitly non-evidentiary.

### Justice

Responsibility may scale with reasons-responsiveness, relevant knowledge, control, and available means, but it cannot be read from coherence/capability alone. Every application must inspect:

- coercion and selector provenance;
- authorization and consent;
- who bears cost and consequence;
- custody and reversibility;
- Grace Exit;
- whether another person's option cone contracts.

The manipulated-selector countermodel blocks automatic moral desert.

## 9. Per-file changes

### PD-11 owner

- Replace the binary “D4 determinism versus D5 freedom” mapping with the typed agency schema.
- Replace every downward μ claim with χ.
- Remove equator-as-proof-of-agency and Dasein-as-collapse language.
- Add modality distinction, countermodels, contact program, kill criteria, Justice boundary, and primary sources.
- Set status `REFRAMED/PARTIAL` and tier `[S/I/C]`.

### PD-00 index

- Change PD-11 tier from `[S/I]` to `[S/I/C]`.
- Change its status/summary to operational compatibilism, metaphysical question open.
- Add the five-field contact gate to the active dissolution pipeline.

### Paradox Suite Audit

- Add the universal-solvent warning: a reframe that cannot fail is relabeling.
- Record PD-11's μ/χ repair and honest ceiling.
- Add `RELABELING/HEURISTIC` versus `REFRAMED-CONTACT` dispositions.

### Lens as Compass derivative

- Update only the PD-11 row to χ and operational compatibilism.
- Add a concise contact-gate note near the “single move” pipeline.
- Preserve its signed-at-tier receipt as provenance; do not rewrite history.

## 10. Primary sources

- Harry Frankfurt, “Alternate Possibilities and Moral Responsibility” (1969), DOI `10.2307/2023833`.
- John Martin Fischer and Mark Ravizza, *Responsibility and Control* (reasons-responsiveness), used as philosophical comparison rather than proof.
- Hugh Everett III, “Relative State Formulation of Quantum Mechanics” (1957), DOI `10.1103/RevModPhys.29.454`, used only to fence branch-selection language.
- Nadav Katz et al., “Reversal of the Weak Measurement of a Quantum State” (2008), DOI `10.1103/PhysRevLett.101.200401`, used only to block a universal irreversibility falsifier.
- Klyubin, Polani, and Nehaniv, “Empowerment: A Universal Agent-Centric Measure of Control” (2005), DOI `10.1109/CEC.2005.1554676`, as one possible option-cone operationalization.

Primary-source citations do not upgrade the Emergentist crosswalk.

## 11. Verification contract

Implementation is accepted only if:

1. Markdown links resolve.
2. `git diff --check` passes.
3. No tracked or untracked change appears under `12_PUBLIC_SITE`, any `90_ARCHIVE`, or `91_COMPATIBILITY`.
4. Source-negative searches find no PD-11 downward “μ-limit transition,” quantum branch selection, Copenhagen collapse-as-action, widened physical light cone, or claim that determinism “lives at D3.”
5. PD-11, PD-00, the suite audit, and the Lens agree on χ, tier, status, and the open metaphysical remainder.
6. The quantum-removal test leaves the operational schema and contact program intact.
7. The manipulated-selector case prevents χ from implying consent, justice, or desert.
8. The contact gate makes an always-successful register reassignment fail as `RELABELING/HEURISTIC`.
9. Existing receipts remain byte-identical.
10. No K2 approval pause or countersign gate is added. Under the Open Canon Covenant, the repair records at its honest tier.

## 12. Non-goals

- proving free will;
- resolving quantum measurement or QM/GR;
- repairing the entire D4/D5 owner spine;
- rewriting all paradoxes;
- promoting the Lens or public Compass;
- changing the Open Canon Covenant;
- declaring Emergentism a unified science.

The design produces one honest keystone and one methodological antibody. It then stops expanding the catalogue.

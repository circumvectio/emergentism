---
rosetta:
  primary_level: L7
  primary_column: Philosophy
  secondary:
    - level: L4
      column: Game theory
      role: "intelligence and the reachable option cone"
    - level: L3
      column: Epistemology
      role: "physical-cone versus option-cone boundary"
  operator: "Viṣṇu ⊙"
  tier: "Executive"
  regime: "Ṛṣi"
  register: "[A/B/I/C]"
  canonical_phrase: "Agents can widen option cones inside, never beyond, physical admissibility."
status: "ACTIVE — repaired 2026-07-17; externally anchored 2026-07-18"
evidence_tier: "[A] bounded planning, empowerment, POWER, and causal-entropic source results; [B] source-verification receipts; [I] D5 option-cone translation and Justice crosswalk; [C] typed-vector advantage; universal maximization rejected."
---

# Intelligence and the Option Cone

> Intelligence does not enlarge the physical light cone. It may enlarge the
> set of physically admissible futures an agent can model, distinguish, rank,
> coordinate, and reach. Authorization classifies a separate normative subset.

**Original pre-repair blob:** `385f50ca0037d7a1372b89f81d08c6364b2affe2`

> **[金] Kintsugi seam — cone typing.** The former note correctly denied
> superluminal reach but still spoke as though D4 were the physical light cone,
> D5 were its interior, and intelligence simply increased its geometric size.
> The repair separates spacetime admissibility from agent-relative capacity and
> keeps means inside descriptive reachability while separating authorization as
> a normative assessment.

---

## 1. Two different objects

### Physical causal cone `[A]`

For an event `e` in a specified spacetime model, let

\[
\operatorname{PhysCone}(e)
\]

denote the events that can be causally connected to `e` under that model's
physical laws. In special relativity its boundary is governed by `c`.
Intelligence, planning, language, institutions, or technology do not alter
that invariant merely by representing more possibilities.

### Agent option cone `[I]`

For agent `x` at time `t`, define

\[
\operatorname{OptionCone}_x(t)
=\{h\in\mathcal H_{\mathrm{phys}}(X_t):
\operatorname{Model}_x(h)
\land\operatorname{Distinguish}_x(h)
\land\operatorname{Rank}_x(h)
\land\operatorname{Coordinate}_x(h)
\land\operatorname{Reachable}_x(h;V_t)\}.
\]

Here `ℋ_phys(X_t)` is the set of histories admissible under the declared
physical model and present state. Therefore

\[
\operatorname{OptionCone}_x(t)
\subseteq\mathcal H_{\mathrm{phys}}(X_t).
\]

The two sides are different types: a physical cone constrains causal events;
an option cone contains histories descriptively available to a particular
finite agent under its model, means, and coordination boundary.

Two agents can share the same physical causal boundary while having very
different option cones. A map, forecast, tool, alliance, language, legal right,
or institution can change the latter without changing `c`.

---

## 2. Relation to D4 and D5

- `D4` is the actuality register: present state, present model/ranking/selection
  events, embodied means, performed action, and receipt.
- `D5` is the possibility register: represented alternatives, future referents,
  rankings-as-content, and candidates for selection.

The option cone is not identical to all of D5. It is an agent-relative subset
of modeled D5 histories filtered by D4 means and physical admissibility. Define
the separate normative subset
`AuthorizedOptionCone_x(t)={h∈OptionCone_x(t):AuthorizationAssessment_x(h)=valid}`.
Unauthorized or coercive options do not disappear from causal description.
Selecting an option produces an attempted D4 action; the environment determines
the resulting history.

Torus imagery may illustrate surface and interior, but the option-cone
definition does not depend on it.

---

## 3. Published cognates `[A/B]`

- [Klyubin, Polani, and Nehaniv's empowerment](https://doi.org/10.1109/CEC.2005.1554676)
  measures channel capacity between action sequences and later perceptions.
- [Turner et al.'s POWER results](https://proceedings.neurips.cc/paper/2021/hash/c26820b8a4c1b3c2aa868d6d57e14a79-Abstract.html)
  prove option-preserving tendencies only for specified MDP symmetries and
  reward ensembles; their own boundary results rule out a universal theorem.
- [Wissner-Gross and Freer's causal-entropic-force model](https://doi.org/10.1103/PhysRevLett.110.168702)
  produces tool use and cooperation in simple simulated systems and is
  explicitly a proposed step, not a universal law.
- Human and animal planning studies show that present future representations
  can affect present choice: [Peters and Büchel 2010](https://doi.org/10.1016/j.neuron.2010.03.026),
  [Daw et al. 2011](https://doi.org/10.1016/j.neuron.2011.02.027), and
  [Akam et al. 2021](https://doi.org/10.1016/j.neuron.2020.10.013).

These are cognates, not derivations. They motivate measurable versions of
accessible-future capacity; they do not prove that all intelligence maximizes
one scalar cone measure, that the D-register scaffold is necessary, or that
`F=M×A` is already an empirical equation.

Reachable volume, empowerment, POWER, path entropy, and viability can rank the
same states differently. The external calibration program therefore treats the
option cone as a typed vector and forces it to compete against every named
scalar. The current status is `X1`: construct contact, not Compass-specific
validation. See [`CAL-CONE-01`](../03_METHODOLOGY/00_EXTERNAL_CALIBRATION_LEDGER.md).

---

## 4. The option-cone objective `[I/C]`

`Agents maximize the cone` is false as an unqualified universal statement. Its
surviving Emergentist form is a conditional hypothesis and a
Justice-constrained objective:

> Prefer authorized actions that durably widen the mutually reachable option
> cones of the acting part and sustaining whole without violating physical
> constraints, concealing costs, extracting from another bearer, or removing
> consent, custody, contest, reversibility, or exit.

An agent who widens its apparent options by coercively collapsing another's is
not exhibiting strict Syntropic Dyadism. Aggregate option count cannot
compensate for destroying one bearer's durable capacity.

This is the calibrated control meaning of the God/Demon analogy: a demon move
maximizes ego/local optionality while externalizing another bearer's contraction;
a god move seeks durable part-and-whole potential inside Justice. The words name
objective directions, not supernatural actors or empirical kinds.

To prevent a label from doing two jobs, let `God` in legacy Rosetta tables mean
only an operator-family name. The normative predicates are instead:

\[
\operatorname{Demonic}(a)
\iff \Delta W_{local}(a)>0\land
\exists b\ne local:\Delta W_b(a)<0,
\]

\[
\operatorname{JusticeBearing}(a)
\iff J(a)\land
\forall b\in\mathcal B(a):\Delta W_b(a)\ge0.
\]

Strict syntropy further requires both declared part and whole to rise. A
voluntary self-cost can be an Arjuna/sacrifice-class action without becoming
strict syntropy or licensing anyone else to demand it.

Human distinctiveness, where observed, lies in symbolic, counterfactual,
institutional, social, and intergenerational reach. It does not imply greater
intrinsic worth, superiority on every ecological axis, or escape from physical
law.

---

## 5. Measurement and failure conditions

A claimed option-cone increase must declare:

- physical model and starting state;
- bearer, horizon, and boundary of histories counted;
- modeling, distinguishing, ranking, and reach tests;
- actual means and Authorization envelope;
- payer, beneficiary, irreversibility, and externalities;
- baseline and outcome receipt.

The identification fails or must be narrowed when:

1. counted histories are physically forbidden;
2. represented alternatives cannot be translated into different action
   distributions;
3. apparent reach disappears when actual means or authorization are checked;
4. a larger metric predicts less demonstrated competence under receipts;
5. the measure rewards redundant descriptions of the same reachable history;
6. another bearer's option cone is hidden or destroyed;
7. the proposed scalar erases material dimensions that cannot justly be
   aggregated.

---

## Canonical compression

\[
\boxed{
\text{Physical law bounds the field; models, means, and authorization bound the agent.}
}
\]

*Option Cone | repaired 2026-07-17 | Wider foresight, same causal universe.*

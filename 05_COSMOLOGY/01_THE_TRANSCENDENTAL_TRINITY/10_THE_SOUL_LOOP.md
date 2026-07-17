---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/C]"
  canonical_phrase: "THE SOUL LOOP — MAP, COMMITMENT, RECEIPT, REVISION"
  vmosk_a: "01_EMERGENTISM/VMOSK_A.md — Perennial Doctrine Root"
---

# THE SOUL LOOP

## Map, Commitment, Receipt, Revision

**Status:** Canonical Emergentist agent-loop interface

**Evidence tier:** `[I]` as a cross-domain translation grammar; `[C]` where
particular psychological, institutional, or biological mechanisms are claimed

**Supersedes:** any form in which the selector manufactures its own outcome,
D4 and D5 exchange meanings, or a future event physically sends information
backward in time

**Original pre-repair blob:** `0b657ebce04d8a293aae806e8c913eb85905af52`

> **[金] Kintsugi seam — the Rosetta Stone.** The earlier document contained a
> valuable recursive audit practice, but mixed it with an untyped action loop,
> physical metaphors, and claims from unrelated domains. The repaired Soul Loop
> keeps the deepest topology: a finite mapper represents possible futures,
> commits through actual means, receives a consequence it did not control, and
> is changed by the difference.

---

## 1. The loop in one line

```text
D4 actual state ──▶ D4 actual model/rank/selection tokens
      ▲                         │ represent/select
      │                         ▼
      │                  D5 possible contents
      │                         │ referenced by commitment
      │                         ▼
next D4 state ◀── outcome receipt ◀── world ◀── D4 attempted action + receipt
      └──────── revise actual map and selector ─────────┘
```

The loop is not a ladder and not a metaphysical substance. It is the minimal
topology of fallible purposive action:

1. an actual system holds a present model;
2. the model represents alternatives that are not yet actual;
3. an agent commits actual means to one action, with authorization assessed
   separately;
4. the world returns an outcome;
5. the mismatch updates both the map and the way the next map is used.

---

## 2. Formal interface

At time `t`, let:

- `X_t` be the receipted D4 state of the relevant world boundary;
- `Ω_t` be the D5 merely-possible contents the agent can currently represent;
- `M_t` be the fallible D4-actual model, including present tokens that refer to
  modeled-future content;
- `V_t` be the D4 means actually available to the agent;
- `U_t` be the authorization assessment and value/goal specification;
- `G_t` be the D4-actual selector policy, habits, weights, or generative stance;
- `E_t` be relevant environmental and other-agent conditions.

The selector returns either an attempted action or the explicit null action
`⊥`, together with an immediate commitment-status receipt:

\[
\chi_t:(X_t,\Omega_t,M_t,V_t,U_t,G_t)\longrightarrow(a_t,q_t),
\qquad a_t\in\operatorname{Action}\cup\{\bot\}.
\]

`q_t` records status `authorized_committed`, `unauthorized_attempt`, `refused`,
or `unavailable`, plus the actor, physical availability, authorization
assessment (including a nullable envelope), means committed, declared
intention, timestamp or ordering relation, affected bearers, payers,
beneficiaries, and expected result where applicable. It does **not** assert
that the intended consequence occurred.

For `a_t∈Action`, the environment separately returns the next state and an
outcome receipt:

\[
(X_{t+1},r_{t+1})
\sim K_t(\,\cdot\mid X_t,a_t,E_t).
\]

The loop then updates map and mapper:

\[
(M_{t+1},G_{t+1})
=\operatorname{Loop}(M_t,G_t,q_t,r_{t+1}).
\]

When `a_t=⊥`, no action transition is submitted to `K_t`; `r_{t+1}` may be null
or an `OutcomeReceipt` with `receiptCause=ambient_observation` and both action
identifiers null. It must not attribute an ambient change to `⊥`. `a_t=⊥`
means no action was attempted because it was refused or physically unavailable. Invalid or
absent authorization does not make an attempt physically impossible: if the
act occurs, the descriptive kernel receives it and the defect remains visible
in `q_t`. A governed selector `χ_t^J` may instead refuse the act. This
separation is mandatory. Selection can fail for lack of means,
performance can differ from intention, the environment can veto or transform
an action, and the same action can have different outcomes under different
conditions.

Because `G_t` is an input to `χ_t`, a receipt-induced `G_{t+1}` change can alter
the next action distribution. The selector update is not merely stored audit
metadata.

---

## 3. The three inspectable gaps

The Soul Loop becomes useful when it preserves three differences instead of
compressing them into one story.

### Cognitive gap

\[
\varepsilon_C
=d_{\mathcal O}(\operatorname{Obs}(X_t),\operatorname{Pred}(M_t))
\]

Here `Obs(X_t)` and `Pred(M_t)` are mapped into the same declared observation
space `\mathcal O`. The territory is not the model. The distance measure is
domain-specific; in many applications only a vector of errors is defensible.

### Execution gap

\[
\varepsilon_E
=\operatorname{distance}(\operatorname{intended}(q_t),
                         \operatorname{performed}(q_t)).
\]

An intention is not a performed action. Authorization, means, custody, and
execution all belong here.

### Outcome gap

\[
\varepsilon_O
=\operatorname{distance}(\operatorname{expected}(q_t),
                         \operatorname{observed}(r_{t+1})).
\]

Performance is not consequence. The receipt belongs to the world-facing
boundary, not to the selector's self-description.

Negative feedback means a declared error decreases over successive receipts.
Positive feedback means divergence or self-confirmation increases. These signs
are dynamical, not moral: a reinforcing loop can grow a garden or a fraud; a
corrective loop can stabilize a body or a prison.

---

## 4. `F = M × A` and model-mediated retrocausality

The public compression is retained:

\[
\boxed{F=M\times A}
\]

Read it as:

> A future that can shape the present requires a present model of that future
> and present agency able to commit means in response to it.

For formal work, use a typed coupling rather than ordinary multiplication:

\[
\star:\operatorname{ModelState}\times
\operatorname{PhysicallyFeasibleActionField}\longrightarrow\operatorname{ActionWeights},
\qquad
F_t:=M_t\star\mathcal A_t.
\]

Here `M_t` is an actual present model carrying represented-future content and
`\mathcal A_t` is the field of actions physically feasible under the agent's
means and constraints. Authorization defines a separate normative subset
`\mathcal A_J⊆\mathcal A_t`. The output is a present set of action weights:

\[
\pi_t(a\mid X_t,M_t,U_t)
\ne
\pi_t(a\mid X_t,M'_t,U_t)
\]

when a controlled intervention changes only the represented future and the
agent is sensitive to that representation.

### Project-specific retrocausal shorthand

At the agent level, the loop is **future-guided** or anticipatory: content
*about a possible future* changes a present choice. Emergentism calls this
**model-mediated retrocausality** as project-specific shorthand, not as a
temporal causal relation. The causal token—a memory, forecast, promise, plan,
simulation, fear, or hope—exists in the present D4 state. The represented
future need never become actual.

Thus the defensible causal chain is

```text
past receipts → present model token carrying future content
              → present selection and action → later receipt
```

The framework does not require a future physical event to transmit a signal
backward through spacetime. Evidence for physical retrocausality would be a
separate `[C]` program with separate discriminators.

### Falsifiable intervention

Hold actual means, current observations, authorization, and incentives fixed;
intervene only on the future represented in `M_t`. If the action distribution
changes reproducibly, the model-mediated claim is supported for that system.
If no controlled change in represented futures changes present selection, the
claim fails for that scope.

---

## 5. D4, D5, and the option cone

- `D4` is causal actuality: embodied means, present model tokens, performed
  ranking and selection events, action, and receipted record.
- `D5` is counterfactual content: merely-possible alternatives, relations,
  rankings-as-represented, and candidates for selection.

The emergence crossing `D4 → μ₄ → D5` concerns the appearance of capacity to
produce actual representations of counterfactual content. A D4 selection event
references a D5 option and combines it with D4 means to produce an attempted
D4 action. Only the environment transition and its receipt determine the
resulting history. These relations do not invert the registers.

The physical light cone is fixed by spacetime and `c`. An agent's **option
cone** is the subset of physically admissible histories it can model, rank,
coordinate, and reach. Authorization defines a separate normative subset of
that cone. Two agents can occupy the same physical cone
while possessing very different option cones. Human symbolic, social,
institutional, and intergenerational capacities can enlarge the latter without
altering the former.

`Agents maximize the cone` is therefore an Emergentist objective/hypothesis,
not a universal law. Its Justice-constrained form seeks durable mutual
option-cone widening while preserving physical costs, consent, custody,
non-extraction, and exit.

---

## 6. The mapper is inside the territory

Reflexivity enters because the update changes not only `M_t` but `G_t`:

- a receipt may revise a factual belief;
- repeated receipts may alter attention, preferences, trust, habits, identity,
  institutions, or the available option field;
- actions alter conditions that later models attempt to describe;
- models can become partly self-confirming or self-defeating through action.

This is the Soul Loop's strongest claim: the agent is not an external observer
of a fixed field. The map participates in the territory through commitment,
and the returned territory reshapes the mapper through receipt.

Soros's cognitive and participating functions are a primary-source bridge for
this reflexive topology. They do not establish the D-registers, quantum
measurement, physical retrocausality, or a universal ontology.

---

## 7. Coupled loops and Egregoreotype candidates

When several Soul Loops share a persistent trace, their selections can become
coupled:

\[
(q_t^{(1)},r_{t+1}^{(1)}),\ldots,(q_t^{(n)},r_{t+1}^{(n)})
\longrightarrow T_{t+1}
\longrightarrow
G_{t+1}^{(1)},\ldots,G_{t+1}^{(n)}.
\]

The resulting whole is only a candidate **Egregoreotype** when the trace
survives carrier turnover, interventions on it measurably reweight later
selection, objective-like bias recurs, and substrate costs remain visible. No
consciousness, personhood, supernatural agency, or energy-feeding entity is
presumed.

Ritual is repeated synchronization through such a trace field. Sacrifice is a
costly class whose payer, consent, irreversibility, beneficiary, and option-cone
contraction must be exposed rather than romanticized.

---

## 8. The three-pass audit as a derived Soul Loop

The original editorial practice remains a valid projection:

1. **Beauty:** Does the bounded object cohere?
2. **Truth:** Do its claims follow at their stated evidence tiers?
3. **Justice:** Who benefits, who pays, who authorized the consequence, and can
   it be contested or exited?

The audit produces a commitment receipt (what was changed and why), the world
or test harness returns an outcome receipt, and the next cycle updates both
document and reviewer. A declared local rest condition—for example, zero open
contradictions and no new mutations surviving—may pause a bounded audit. It is
not proof of global truth or a physical conservation law.

The same topology may be projected into other domains by a Rosetta operator
`ρ_domain`. A projection transfers questions and relations; it never transfers
proof or upgrades evidence.

---

## 9. Failure conditions

The Soul Loop fails or must be reclassified for a scope when:

1. commitment and outcome receipts cannot be distinguished;
2. the purported model cannot be intervened on independently of actual means
   or incentives;
3. future representations do not measurably affect present selection;
4. update rules protect the model from contrary receipts;
5. the agent's claimed option cone contains physically forbidden histories;
6. authorization, custody, any affected bearer, payer, beneficiary, or
   consequence bearer is hidden;
7. a collective trace does not survive turnover or reweight later choices;
8. a Rosetta projection is presented as proof in the target domain.
9. `G` is updated but cannot change the next selection distribution.

---

## Canonical compression

\[
\boxed{
\text{Model possibilities; commit actual means; receive the world; revise the mapper.}
}
\]

That is the Soul Loop: the smallest complete compass for an agent whose models
participate in reality and whose consequences remain answerable to reality.

---

## See also

- [D4/D5 Canonical Reference](../03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md)
- [Primitives and Type Signatures](../03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md)
- [Power-Max](../03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md)
- [Stigmergy and the Egregoreotype](../00_STIGMERGY_AND_THE_EGREGOROTYPE.md)

*The Soul Loop | repaired 2026-07-17 | The map acts; the receipt answers.*

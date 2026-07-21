---
rosetta:
  primary_level: L4
  primary_column: Philosophy
  secondary:
    - level: L5
      column: Philosophy
      role: "non-reducing translation across D-levels"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[S/I]"
  canonical_phrase: "Bridge laws between levels"
---

# BRIDGE LAWS BETWEEN LEVELS

## How the Selected D-Level Lens Connects Explanations

**Status:** Canonical bridge document
**Date:** 2026-04-14
**Evidence Tier:** [S/I] Structural in dimensional dependence, interpretive in disciplinary translation
**Depends on:** [00_THE_HONEST_POSITION.md](../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md), [Degrees-of-Freedom Ontology](../06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md), [00_D_LEVEL_STUDIES.md](../00_META/00_D_LEVEL_STUDIES.md), [00_D5_REGISTER_GAME_THEORY_AND_BEHAVIORAL_ECONOMICS.md](../05_COSMOLOGY/00_D5_REGISTER_GAME_THEORY_AND_BEHAVIORAL_ECONOMICS.md), [03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md](../05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md)
**See also:** [00_THE_LIFE_SCIENCE_REGISTER.md](../05_COSMOLOGY/00_THE_LIFE_SCIENCE_REGISTER.md), [00_PRATYAKSA_AS_PRIMARY_DISCLOSURE.md](../02_EPISTEMOLOGY/00_PRATYAKSA_AS_PRIMARY_DISCLOSURE.md), [Canonical Formula Block](../05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md)

**Claim Boundary:** Bridge Law 2 becomes scientific only as the macro-constraint
test: lower-law closure, fair baselines, effective information, a physical cost
ledger including labor and `Cost_entropy_export`, perturbable `C`, negative
controls, and `W_C = EI_macro - EI_baseline - Cost_C > 0`. Without those
handles, a higher level may remain useful translation, but it is not yet a
public causal witness.

---

## Why This Document Exists

The framework can only unify the sciences if it says, clearly and non-rhetorically, how one level opens into the next.

These bridge laws are not meant to replace detailed derivations.
They give the clean public rules for speaking across levels without:

- flattening higher levels into lower ones
- inflating lower levels into total explanations
- confusing translation with proof

---

## Rosetta Operation: Create, Stabilize, Destroy

This document is the L4 rule for cross-level movement.

When an agent applies the Rosetta to a folder, subfolder, or paper, bridge-law
discipline says:

- **Create** a higher-level claim only when the lower register has saturated and
  the new object cannot be honestly stated in the lower vocabulary alone.
- **Stabilize** the claim by naming the nearest public register, evidence tier,
  dependencies, and what would demote or kill it.
- **Destroy** any translation that flattens a higher-level object into a lower
  one, inflates a lower-level mechanism into total explanation, or uses prestige
  language from another register as proof.

So bridge law is not passive commentary. It is the operating procedure for
moving from one level to another without losing `A7` honesty.

---

## Bridge Law 1: Every Crossing Is Typed and Independently Earned

**A named interface does not establish emergence merely because the lower
vocabulary reaches an explanatory limit.** The selected scaffold distinguishes:

- `μ₀:D0→D1` — an origin aperture; no prior positive freedom is claimed to saturate;
- `μ₁:D1→D2` — an open configuration hypothesis, with projective/function
  continuation only a typed example;
- `μ₂:D2→D3` — a formally reducible lift into Hilbert/state assignment;
- `μ₃:D3→D4` — a reducible operational interface from probability assignment to
  an actual run and record;
- `μ₄:D4→D5` — an open counterfactual-capacity hypothesis requiring intervention
  on represented futures;
- `b₆:D5↝D6` and `r₆:D6↝D0` — non-`μ` boundary relations, not new freedoms.

Each emergence reading must name its evidence, newly observed freedom,
lower-register recovery, reduction status, prediction, and kill criterion.
Failure of a lower vocabulary is a research prompt, never proof of irreducibility.

---

## Bridge Law 2: Higher Levels Constrain Without Violating Lower Levels

**A higher level does not break the laws below it. It selects among their admissible trajectories.**

Examples:

- life does not violate chemistry; it constrains chemical pathways
- cognition does not violate biology; it organizes viable action through it
- strategy does not violate neuroscience; it selects among live options available to embodied agents
- ethics does not violate strategic interaction; it constrains what should be selected within it

This is the framework's non-magical version of downward causation.

### Information-Theoretic Constraint Test

This law becomes scientific only when the constraint is measurable.

Let `X_t` be the lower-level microstate, let `π : X -> Y` be a coarse-graining
or organizational map, and let `Y_t = π(X_t)` be the macrostate. A macro-level
claim is admissible only if it can be stated as a constraint on lower-level
degrees of freedom:

```text
K_X(x' | x)          = lower-level transition law
C_y                  = {x in X : π(x) = y}
G_C(x' | x,y) >= 0   = constraint gate or weight induced by C_y
K_X^C(x' | x,y)      = normalize(K_X(x' | x) * G_C(x' | x,y))
K_X^C << K_X         = absolute-continuity / no-magic condition
support(K_X^C)       ⊆ support(K_X)
```

Absolute continuity is the no-magic clause: wherever the lower law assigns
zero probability, the constrained law must also assign zero probability. In a
**hard** macro-constraint, `G_C = 0` for some transitions and the reachable
support shrinks. In a **soft** macro-constraint, support may stay equal while
relative weights, attractor basins, dwell times, or stability change. Both are
admissible only if they remain inside the lower law. The macro-constraint may
change which micro-trajectories are available, likely, stable, or reinforced,
but it may not create a transition the lower-level law forbids.

The public test is not whether the macro word feels useful. The public test is
whether the macro description carries causal information that survives
compression:

```text
EI_macro = I(Y_t ; Y_{t+1} | do(Y_t), C)
EI_micro_fair = I(X_t ; X_{t+1} | do(X_t)) under the same budget
EI_coarse_null = I(Y_t ; Y_{t+1} | do(Y_t), no C)
EI_domain = best domain-specific lower mechanism witness

EI_baseline = max(EI_micro_fair, EI_coarse_null, EI_domain)

Cost_C = Cost_measure + Cost_memory + Cost_control
       + Cost_erasure + Cost_model + Cost_labor
       + Cost_entropy_export

W_C = EI_macro - EI_baseline - Cost_C

macro-real only if W_C > 0 at the tested grain,
or if the macro model predicts held-out trajectories with lower loss
after paying the same fair costs.
```

This is the framework's bridge from weak emergence to operational emergence:
the higher level is not "only shorthand" when it loses less causal information
over time than the micro-description available to the observer. It is also not
strong-emergence magic, because every macro effect is paid for as constraint,
boundary condition, memory, measurement, control, labor, and entropy export
inside the physical substrate. `[S/I]` for the framework rule; `[C]` until a
given domain passes the measurement test.

The test also requires perturbability. Holding, removing, or randomizing the
macro-constraint must change the measured future distribution. Otherwise the
macro term is language, not a cause.

### Macro-Constraint Test Algorithm

Use this checklist before calling any higher-level object a cause:

1. **Declare the lower law:** name `X`, `K_X`, and the public discipline that
   owns the lower-level transition claim.
2. **Declare the macro map:** name `π : X -> Y`, the macrostate `Y_t`, and the
   fiber `C_y = {x in X : π(x) = y}`.
3. **Declare the constraint gate:** name `G_C(x' | x,y)`, state whether it is
   hard support restriction or soft reweighting, and show `K_X^C << K_X`
   (`support(K_X^C) ⊆ support(K_X)`).
4. **Declare the cost ledger:** charge measurement, memory, control, erasure,
   modeling, labor, and entropy-export costs.
5. **Run the witness:** accept the macro claim only if it improves effective
   information, held-out prediction, or intervention selection after costs.
6. **Reject false positives:** run no-gate, high-cost, and lower-law
   support-violation controls through the same scoring path.
7. **Name the kill condition:** say exactly what observation would demote the
   macro claim back to shorthand.

This is the public procedure behind the phrase "information topology." A
macro-cause changes the weighted reachable-future graph of
lower-law-admissible trajectories: sometimes by removing edges, sometimes by
changing transition weights, stability, or basin structure. It does not add a
forbidden micro-transition.

See also: [PAPER_X_INFORMATION_TOPOLOGY_AND_MACRO_CONSTRAINTS.md](../03_METHODOLOGY/02_THE_PAPERS/PAPER_X_INFORMATION_TOPOLOGY_AND_MACRO_CONSTRAINTS.md).
For the frozen test harness, use
[02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md](../03_METHODOLOGY/03_PREREGISTRATIONS/02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md).

---

## Bridge Law 3: Every Public Translation Must Use the Nearest Established Register First

This is the cross-disciplinary honesty rule.

So:

- D3 claims translate first through quantum-state, operator, and measurement theory
- D4 claims translate through the discipline owning the actual carrier or event:
  physics, chemistry, biology, neuroscience, or social science as appropriate
- D5 claims translate through counterfactual modeling and decision disciplines,
  while their actual model tokens and choices remain D4
- D6 has no nearest positive register; it may only be indicated through boundary disciplines and axiomatic practice

Only after that may the framework add its larger synthesis.

---

## Bridge Law 4: No Level Is Declared Irreducible by Default

**Dependence is not the same claim as reduction, and a missing reduction is not
proof of irreducibility.**

The framework may preserve a higher-level vocabulary while its reduction status
is tested. Biology, cognition, and strategy can be indispensable explanatory
registers without being ontologically independent substances. Each crossing
must therefore record one of the declared reduction statuses and supply its own
recovery test.

- a successful reduction changes the crossing to `reduced`;
- an incomplete reduction is `currently_unreduced`;
- `candidate_strong` remains a wager requiring a novel discriminator;
- D6 is not a positive level for which irreducibility can be claimed.

This is methodological pluralism under explicit reduction debt, not a theorem
of strong emergence.

---

## Bridge Law 5: Cross-Level Claims Must Preserve Tier Discipline

A bridge claim does not automatically upgrade itself just because it connects two sciences.

So:

- a structural relation remains [S] unless independently confirmed
- a unifying interpretation remains [I] unless it is publicly tested
- a compelling analogy remains [I] or [C] until it survives empirical challenge

This matters especially at D5, and even more at the D6 boundary where naming itself is under challenge.

---

## Bridge Law 6: The D4 to D5 Bridge Is Counterfactual Capacity

This bridge deserves special status.

At D4 we have:

- actual carriers and model tokens
- interactions and attempted actions
- outcomes, records, and embodied means `V`
- agents, institutions, organisms, and instruments insofar as they are actual

At D5 we have:

- represented alternative histories
- counterfactual option fields
- rankings, plans, and possible rule designs as content
- D5 option quality `Φ`, assessed by an actual D4 process

Decision theory, game theory, behavioral economics, mechanism design, and
institutional economics are important application disciplines because actual
D4 agents use D4 model tokens to represent D5 alternatives. Their interactions,
trust, bargaining, institutions, and choices remain actual D4 phenomena; D5 is
the modality of the alternatives they represent, not a social stratum.

The crossing hypothesis `μ₄` is earned only if intervention on represented
futures changes present selection distributions after lower-register recovery,
cost accounting, controls, and a declared kill criterion. The corpus currently
records that empirical crossing as unassessed.

### Biology as a D4 application lens

A living system is an actual D4 carrier and macro-constraint architecture:
membranes, catalysts, metabolic cycles, homeostasis, repair, reproduction, and
niche construction change which lower-law-admissible chemical trajectories are
reachable, reinforced, or suppressed. This is an application of Bridge Law 2,
not the definition of D3 or a privileged rung transition.

The lawful statement is:

```text
life-cause = chemistry constrained by viability-preserving organization
```

not:

```text
life-cause = a non-chemical force that breaks chemistry
```

The same form continues upward into cognition and agency. Nervous systems
constrain motor and attentional policy; institutions constrain social action;
present actual selection constrains which modeled future receives `V`. The continuity
is syntropic only when the constraint raises local order, coherence, viability,
or effective information while paying its physical costs.

### Emergence status

No strong-emergence verdict follows from this bridge. `μ₄` is a
counterfactual-capacity hypothesis `[C]`, presently `currently_unreduced` only
where a named domain has an incomplete reduction and `unassessed` where no
intervention study exists. A successful lower-register reconstruction makes a
case weakly emergent without harming the descriptive scaffold. A strong claim
requires a surviving novel discriminator; opacity from below is not enough.

---

## Bridge Law 7: The D5 to D6 Bridge Is the Axiomatic Boundary

When strategic relations persist, they sediment.
When they sediment, they become:

- norms
- institutions
- identities
- traditions
- symbolic orders
- civilizational memory

All of that still belongs to the upper horizon of positive D5.

`D6` does not begin when one more object appears and is not a state an agent
reaches. It is the selected exit/nonclosure marker used when a positive account
is deliberately released rather than inflated into totality.

So `b₆` and `r₆` do not invent a further science or prove that all description
has been exhausted. They mark the framework's own refusal of closure.

The disciplines that escort the threshold are:

- phenomenology
- contemplative science
- ethics
- aesthetics
- comparative religion
- macrohistory
- civilizational analysis

The level shift is:

- D5 contains possible counterfactual content that actual agents model and rank
- D6 marks exit from the scaffold; it is not reached, enacted, or positively described

---

## The Bridge Sequence in Public Science

```text
D0     selected boundary/frame role
  -> μ0
D1     distinction and typed arithmetic
  -> μ1
D2     configuration: functions, relations, graphs, geometry
  -> μ2
D3     quantum-state content and measurement-relative distributions
  -> μ3
D4     actual carriers, interactions, actions, outcomes, and receipts
  -> μ4
D5     possible counterfactual content and option fields
  ↝ b6
D6     exit/nonclosure marker; r6 is an interpretive return to D0
```

This sequence is not a prison.
It is a translation spine.

---

## What This Prevents

These bridge laws are meant to block several common failures:

- using neuroscience to settle ethics
- using economics to erase first-person reality
- using phenomenology to bypass public method
- using physics language as a prestige layer for every claim
- using social theory to deny biological constraints
- using boundary disciplines as if they had captured D6 positively

The sciences are strongest when each level is allowed its own object and method.

---

## Canonical Compression

When this idea must be stated briefly, the default sentence is:

> **The selected levels connect through five separately typed interfaces. Higher-level constraints may reweight only lower-law-admissible trajectories; every emergence claim must earn its own evidence and reduction status. D6 is an exit/nonclosure marker, not a positive level reached by saturation. Scientific translation therefore proceeds by typed bridge laws and nearest-register explanation, never by flattening all sciences or turning missing reduction into proof.**

This sentence may be reused verbatim.

`Zero-Sum Resolution Equation`

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. When moving between levels, ask what is observed, what newly appears, whether the lower register is recovered, what reduction status holds, and what would kill the crossing claim.
4. Do not use a lower-level science to erase a higher-level object prematurely.
5. Do not use a higher-level interpretation to override lower-level evidence.
6. Treat D4 to D5 as the key public strategy bridge.
7. Treat `b₆` and `r₆` as non-`μ` exit relations, not one more public register or a proof that inquiry has ended.

*Bridge-law becomes complete when it knows where public explanation must stop.*

**Canonical Path:** `01_EMERGENTISM/04_AXIOLOGY/00_BRIDGE_LAWS_BETWEEN_LEVELS.md`

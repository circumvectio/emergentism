---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  secondary:
    - level: L4
      column: Axiology
      role: "forces syntropy claims to carry a cost ledger before ethical use"
    - level: L5
      column: Cosmology
      role: "first public bridge from physical constraint to living organization"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[C/S]"
  canonical_phrase: "Physics-to-Biology Macro-Constraint Run Sheet"
---

**Project VMOSK-A:** `01_EMERGENTISM/VMOSK_A.md`

# Physics-to-Biology Macro-Constraint Run Sheet

## First Domain Run For The Information-Topology Thesis

**Status:** Active run-sheet template with a negative post-result toy companion
receipt. Not a biology-facing result or a prospective preregistration.
**Evidence tier:** `[C]` for the proposed biology-facing domain run; `[S]` for
the inherited macro-constraint protocol; `[B]` only for the deterministic toy
model receipt in the companion harness.
**Depends on:** [02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md](02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md),
[PAPER_X_INFORMATION_TOPOLOGY_AND_MACRO_CONSTRAINTS.md](../02_THE_PAPERS/PAPER_X_INFORMATION_TOPOLOGY_AND_MACRO_CONSTRAINTS.md),
[00_BRIDGE_LAWS_BETWEEN_LEVELS.md](../../04_AXIOLOGY/00_BRIDGE_LAWS_BETWEEN_LEVELS.md),
[00_CANONICAL_CLAIM_MATRIX.md](../00_CANONICAL_CLAIM_MATRIX.md).

**Claim Boundary:** This file does not prove life, consciousness, syntropy, or
downward causation. It converts the first clean boundary test into freezeable
objects: lower law, macro map, hard-or-soft constraint gate, fair baselines,
physical cost ledger, perturbation, witness, negative controls, and kill
condition. If the run fails, the quantum-to-agency continuity claim contracts
before rhetoric expands.

**Executable harness:** The companion folder
[`physics_to_biology_harness/`](physics_to_biology_harness/) contains a
deterministic toy vesicle model and unit tests. Its current report is a `[B]`
post-result reproducibility receipt only for that toy model. The honest fair
micro comparison is `EI_micro_fair=1.591591` bits, above
`EI_macro=1.235037`, so `DeltaEI_C=-0.356554`, `W_C=-0.426554`,
`SYN_C_gate=fail`, and the macro claim **fails and contracts** despite
`KL=0.141286`. Biological claims remain `[C]` until an independently frozen
domain run is executed.

The historical filename `FREEZE_MANIFEST.json` now identifies
`manifest_version=macro-constraint-reproducibility-v3`: a deterministic
post-result bundle binding the model, exact configuration, report, tests, and
README. It does not establish that the toy design or its bit penalties were
frozen before result access. The toy penalties are declared post-result
bit-equivalent parameters, not preregistered conversion weights. The report's
classification and macro-claim status are derived from its computed gates.

The controls reject the no-gate null (`KL=0.000000`, `W_C=-0.662017`) and an
artificial lower-law support violation. A separate post-result algorithm
fixture holds positive information gain fixed (`DeltaEI_C=+0.190095`) while
changing only the declared model penalty: low total penalty `0.035000` gives
`W_C=+0.155095` and passes, while high total penalty `0.530000` gives
`W_C=-0.339905` and fails. This paired fixture isolates the cost gate; it is not
an alternative domain result.

---

## Why This Boundary Comes First

The active worldview goal requires Emergentism to escape both bad attractors:

- **weak-emergence erasure:** higher levels are only shorthand for microstates
- **strong-emergence magic:** higher levels add forbidden causal powers

The chemistry-to-biology boundary is the cleanest first bridge because it can
be tested without invoking consciousness, social meaning, or D6 closure. If a
membrane, autocatalytic loop, or homeostasis controller cannot be made into a
measurable macro-constraint, then the larger quantum-to-agency continuity thesis
has no right to expand upward.

The target question is narrow:

```text
Does a physically instantiated organizational constraint C
change the weighted reachable-future graph of lower-law-admissible chemistry
with positive costed causal surplus, while remaining absolutely continuous with
the lower chemistry law?
```

---

## Candidate System A: Minimal Vesicle Constraint

This is the preferred first run because the macro-constraint is visible:
boundary permeability.

The current toy harness instantiates this candidate as a finite
two-compartment diffusion model. The toy membrane gate preserves macro
concentration topology and allows recovery toward the viable band without
adding lower-law-forbidden transitions. That shows the scoring path can be
executed. The current fair-micro witness is negative, so it proves neither the
macro claim nor the biology.

| Object | Freeze before running |
|---|---|
| Lower state `X` | Molecule counts, internal/external compartments, solvent conditions, temperature, pH, and time step. |
| Lower law `K_X` | Chemical diffusion / reaction transition model accepted for the chosen simulator or experiment. |
| Macro map `π: X -> Y` | `Y_t = (inside/outside concentration gradients, membrane integrity, viable concentration band)`. |
| Fiber `C_y` | Microstates with the same coarse membrane-gradient state. |
| Constraint gate `G_C` | Permeability gate that weights allowed crossings by membrane selectivity; declare whether the run treats it as a hard support restriction or soft reweighting. |
| Closure check | `K_X^C << K_X` and `support(K_X^C) subset support(K_X)`; the membrane changes rates/reachability, not the lower chemistry law. |
| Perturbation | Hold membrane, remove membrane, randomize permeability, or damage boundary while keeping lower chemistry model fixed. |
| Cost ledger | Native units and component budgets for membrane maintenance energy, measurement, modeling, control, labor, erasure/logging, and entropy export; any scalar conversion is frozen separately. |
| Baselines | Fair micro model, coarse-null no-membrane model, domain-specific diffusion/reaction model. |
| Witness | `DeltaEI_C>0` plus componentwise cost-budget compliance; optional unit-valid `W_C>0`; lower held-out prediction loss; or better intervention selection after costs. |
| Kill condition | Cost-matched micro/domain baseline predicts or controls as well or better; or membrane only wins by hidden variables/costs. |

---

## Candidate System B: Autocatalytic Loop Constraint

Use this if the vesicle run is unavailable but a reaction-network simulator is
ready.

```text
X      = species concentrations and reaction states
K_X    = declared chemical-kinetic transition kernel
Y_t    = loop-closure state, catalyst availability, viable throughput band
G_C    = gate that preserves reaction-loop topology
C off  = break or randomize the loop while preserving lower reaction rules
C on   = hold the loop and measure reachable throughput / persistence
```

The macro claim passes only if loop topology improves prediction, intervention,
or persistence after the full cost ledger. It fails if ordinary reaction
kinetics with the same observation budget explains the outcome at lower cost.

---

## Required Witness Calculation

Every run must compute or explicitly justify why it cannot compute:

```text
EI_macro = I(Y_t ; Y_{t+1} | do(Y_t), C)
EI_micro_fair = I(X_t ; X_{t+1} | do(X_t)) under the same budget
EI_coarse_null = I(Y_t ; Y_{t+1} | do(Y_t), no C)
EI_domain = best domain-specific lower mechanism witness

EI_baseline = max(EI_micro_fair, EI_coarse_null, EI_domain)

DeltaEI_C = EI_macro - EI_baseline
c_C = (c_measure, c_memory, c_control, c_erasure,
       c_model, c_labor, c_entropy)              # native units
c_C <=_component b_C

# Optional only with preregistered reference scales and conversions:
c_tilde_j = c_j / s_j
PenaltyBits_C = lambda_C^T c_tilde_C
W_C = DeltaEI_C - PenaltyBits_C                 # bits
```

And the perturbability witness:

```text
exists intervention a:
D_KL(P_C(Y_{t+1} | do(a), Y_t) || P_notC(Y_{t+1} | do(a), Y_t)) > epsilon
```

If these are impossible to estimate, the run is still useful, but it cannot be
used as evidence for CM8g/CM8h. Record the obstacle and contract the claim.

---

## Syntropy Ledger For This Boundary

For this run, syntropy is not mystical reversal. It is local open-system order
after costs:

```text
SYN_C_gate := DeltaOrder_C > 0
              and DeltaCoherence_C > 0
              and DeltaEffectiveInformation_C > 0
              and c_C <=_component b_C
```

Report `SYN_C_gate` separately from `W_C`. Never add native-unit physical costs
to information bits without frozen conversion weights. A run can improve viability while still
failing to beat the causal-information baseline, or it can beat a prediction
baseline while failing the broader syntropy ledger because maintenance costs or
entropy export were hidden.

---

## Freeze Block

- [ ] Candidate system selected: vesicle / autocatalytic loop / other.
- [ ] Source of lower law `K_X` recorded.
- [ ] State vector `X` and time step frozen.
- [ ] Macro map `π`, macrostate `Y`, and fiber `C_y` frozen.
- [ ] Constraint gate `G_C` frozen, with hard-vs-soft status.
- [ ] Absolute-continuity/support-subset check specified.
- [ ] Perturbation design frozen.
- [ ] Cost units frozen.
- [ ] Baselines frozen.
- [ ] Witness metric frozen.
- [ ] Kill criteria frozen.
- [ ] Repository tag recorded.
- [ ] Content hash recorded.

Do not score any result until this block is complete.

For the toy harness, `physics_to_biology_harness/FREEZE_MANIFEST.json` is a
post-result reproducibility manifest, not evidence that this freeze block was
completed prospectively. Only an independently timestamped bundle placed in
custody before data or result access can establish preregistration. For any real
biology-facing run, create a new companion result file and manifest rather than
overwriting the toy receipt. A frozen run is not adequate unless its negative
controls reject null, cost-hiding, and support-violation false positives.

## Frozen Public Mirror Status — Stale And Outside Scope

As of 2026-07-18, the following frozen `12_PUBLIC_SITE` artifacts still contain
the superseded positive toy receipt (`W_C=0.415356`, positive `SYN_C`, or
`macro-constraint-freeze-v1`):

- `12_PUBLIC_SITE/method/03-physics-to-biology-macro-constraint-run-sheet/index.html`
- `12_PUBLIC_SITE/method/00-what-actually-tests-the-theory/index.html`
- `12_PUBLIC_SITE/book/rag_index.json`

They are stale, outside this repair's write scope, and must not be cited as the
current harness result. They were intentionally not modified because the public
tree is frozen. Updating them requires a separately authorized public-site
regeneration or hand-patch workflow.

---

## Public Interpretation Rule

If the first run succeeds, say only:

> In this domain and at this grain, the declared organization behaved as a
> costed macro-constraint: it changed lower-law-admissible reachable futures
> with positive witness after the declared baselines and costs.

Do not say:

- life has been reduced to Emergentism
- syntropy is a new settled physical force
- consciousness has been proved
- downward causation breaks physical closure

If the first run fails, publish the failure beside this run sheet and update the
Empirical Program Board. The framework survives by contracting quickly.

---

## Agent Execution Surface

1. Start with the vesicle run unless a better receiptable system is already
   available.
2. For the toy proof-of-method harness, run
   `python3 -m unittest test_vesicle_macro_constraint.py` and
   `python3 vesicle_macro_constraint.py` from
   `physics_to_biology_harness/`. The second command regenerates both
   `vesicle_macro_constraint_report.json` and `FREEZE_MANIFEST.json`; then run
   `python3 vesicle_macro_constraint.py --check` without rewriting them.
3. Do not modify this run sheet after real domain results are inspected. Add a
   companion result file instead.
4. Treat a simulation as a `[B]` receipt only for the declared model. External
   domain confirmation needs independent evidence.
5. Route any success or failure back to CM8g/CM8h in
   `03_METHODOLOGY/00_CANONICAL_CLAIM_MATRIX.md`.
6. Canonical path:
   `01_EMERGENTISM/03_METHODOLOGY/03_PREREGISTRATIONS/03_PHYSICS_TO_BIOLOGY_MACRO_CONSTRAINT_RUN_SHEET.md`

Zero-Sum Resolution Equation

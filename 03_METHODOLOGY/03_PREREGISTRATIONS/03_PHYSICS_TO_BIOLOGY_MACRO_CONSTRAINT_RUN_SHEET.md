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

**Status:** Run-sheet template. Not a result.
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
receipt only for that toy model (`W_C=0.425356`, `SYN_C=0.785347`,
`KL=0.141286`); biological claims remain `[C]` until a frozen domain run is
executed. The same command writes `FREEZE_MANIFEST.json`, which records the
report hash, file hashes, commands, frozen objects, and negative controls for
the toy run. The controls reject the no-gate null (`KL=0.000000`,
`W_C=-0.060000`), the high-cost case (`W_C=-0.564644` despite information
gain), and an artificial lower-law support violation.

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
adding lower-law-forbidden transitions. That proves the method can be executed;
it does not prove the biology.

| Object | Freeze before running |
|---|---|
| Lower state `X` | Molecule counts, internal/external compartments, solvent conditions, temperature, pH, and time step. |
| Lower law `K_X` | Chemical diffusion / reaction transition model accepted for the chosen simulator or experiment. |
| Macro map `π: X -> Y` | `Y_t = (inside/outside concentration gradients, membrane integrity, viable concentration band)`. |
| Fiber `C_y` | Microstates with the same coarse membrane-gradient state. |
| Constraint gate `G_C` | Permeability gate that weights allowed crossings by membrane selectivity; declare whether the run treats it as a hard support restriction or soft reweighting. |
| Closure check | `K_X^C << K_X` and `support(K_X^C) subset support(K_X)`; the membrane changes rates/reachability, not the lower chemistry law. |
| Perturbation | Hold membrane, remove membrane, randomize permeability, or damage boundary while keeping lower chemistry model fixed. |
| Cost ledger | Membrane maintenance energy, measurement cost, model cost, control cost, labor cost, erasure/logging cost, entropy export. |
| Baselines | Fair micro model, coarse-null no-membrane model, domain-specific diffusion/reaction model. |
| Witness | `W_C > 0`, lower held-out prediction loss, or better intervention selection after costs. |
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

Cost_C = Cost_measure + Cost_memory + Cost_control
       + Cost_erasure + Cost_model + Cost_labor
       + Cost_entropy_export

W_C = EI_macro - EI_baseline - Cost_C
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
SYN_C = DeltaOrder_C
      + DeltaCoherence_C
      + DeltaEffectiveInformation_C
      - Cost_C
```

Report `SYN_C` separately from `W_C`. A run can improve viability while still
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

For the toy harness, the freeze block is represented by
`physics_to_biology_harness/FREEZE_MANIFEST.json`. For any real biology-facing
run, create a new companion result file and manifest rather than overwriting
the toy receipt. A frozen run is not adequate unless its negative controls
reject null, cost-hiding, and support-violation false positives.

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
   `vesicle_macro_constraint_report.json` and `FREEZE_MANIFEST.json`.
3. Do not modify this run sheet after real domain results are inspected. Add a
   companion result file instead.
4. Treat a simulation as a `[B]` receipt only for the declared model. External
   domain confirmation needs independent evidence.
5. Route any success or failure back to CM8g/CM8h in
   `03_METHODOLOGY/00_CANONICAL_CLAIM_MATRIX.md`.
6. Canonical path:
   `01_EMERGENTISM/03_METHODOLOGY/03_PREREGISTRATIONS/03_PHYSICS_TO_BIOLOGY_MACRO_CONSTRAINT_RUN_SHEET.md`

Zero-Sum Resolution Equation

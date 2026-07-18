# Physics-to-Biology Harness

**Status:** executable post-result reproducibility bundle with a negative result;
not a prospective preregistration and not biological evidence.
**Evidence tier:** `[B]` only for this deterministic repository receipt;
`[C]` for any claim about biology until an independently frozen domain run is
executed.

`FREEZE_MANIFEST.json` is a historical filename. The current manifest binds the
model, exact configuration, generated report, tests, and documentation after
the result was already available. It does not prove that the design was frozen
before result access. Only an independently timestamped, pre-result freeze could
establish preregistration status.

This folder instantiates the first macro-constraint boundary run as a minimal
two-compartment vesicle model.

```bash
python3 -m unittest test_vesicle_macro_constraint.py
python3 vesicle_macro_constraint.py
python3 vesicle_macro_constraint.py --check
```

The second command writes both:

- `vesicle_macro_constraint_report.json`
- `FREEZE_MANIFEST.json`

The harness declares:

- `X`: internal molecule count in a finite two-compartment system
- `K_X`: binomial diffusion transition kernel
- `pi: X -> Y`: macro map to `low`, `viable`, and `high`
- `G_C`: membrane gate that preserves macro concentration topology without
  adding lower-law-forbidden transitions
- `CostPenaltyBits_C`: toy measurement, memory, control, erasure, model, labor,
  and entropy-export bit penalties declared after result access for this toy
  reproducibility bundle; they are not preregistered conversion weights, and no
  raw mixed-unit physical-cost inference is claimed
- witness: `W_C = EI_macro - EI_baseline - PenaltyBits_C`
- fair micro baseline: micro effective information on `K_X^C` under uniform
  `do(X_t)`, matching the constraint condition used by `EI_macro`; the
  unconstrained lower-micro value is also reported
- syntropy gate: positive component deltas plus the separately declared penalty
  budget; heterogeneous quantities are not summed
- perturbability: average macro-channel `D_KL(C || notC)`

`result.classification` and `result.macro_claim_status` are derived from the
computed macro-constraint and syntropy gates. They are not fixed result labels.
The test suite exercises both passing and failing verdict branches.

Current deterministic report:

```text
EI_macro             = 1.235037 bits
EI_micro_lower       = 1.341697 bits
EI_micro_constrained = 1.591591 bits
EI_micro_fair        = 1.591591 bits
DeltaEI_C            = -0.356554 bits
PenaltyBits_C        = 0.070000 bits
W_C                  = -0.426554 bits
SYN_GATE             = fail
KL                    = 0.141286 bits
macro claim           = fails and contracts
```

Even the less conservative unconstrained lower-micro comparison would give
`W_C=-0.176660` bits. The three-state coarse null (`0.749680` bits) is not a
micro baseline and is no longer assigned to `EI_micro_fair`. The declared
configuration is retained; no parameter was tuned to restore a positive result.

Negative controls:

```text
no_gate        = rejected; KL=0.000000, W_C=-0.662017
cost fixture   = post-result algorithm branch test; matched non-default dynamics
  low cost     = DeltaEI_C=+0.190095, penalty=0.035000, W_C=+0.155095, pass
  high cost    = DeltaEI_C=+0.190095, penalty=0.530000, W_C=-0.339905, fail
  changed      = penalty_bits_model only; information_metrics_match=true
  isolates_cost_gate = true
forbidden_edge = rejected; support violation detected
all_controls_reject = true
```

The cost fixture is not an alternative scientific result and was not selected
prospectively. It exists solely to ensure the algorithm can produce a genuine
positive `DeltaEI_C` and that the same information result changes from pass to
fail when only the declared toy penalty changes. Exact known-channel and
non-default-configuration tests fail if EI is constantized or cost subtraction
is removed.

Current freeze manifest:

```text
manifest_version = macro-constraint-reproducibility-v3
bundle_kind      = post_result_reproducibility_bundle
report_sha256    = recorded in FREEZE_MANIFEST.json
file_hashes      = README.md, test_vesicle_macro_constraint.py, vesicle_macro_constraint.py
bindings         = exact model hash, canonical config hash/value, report hash
frozen_objects   = X, K_X, pi, Y, G_C, CostPenaltyBits_C, epsilon
```

`python3 vesicle_macro_constraint.py --check` does not rewrite the report or
manifest and fails if the manifest, current model, configuration, report,
tests, or README do not match.
Manifest generation also rejects a report/config or report/model mismatch.

Safe interpretation:

> In this post-result toy run, the membrane improves several macro-level
> viability diagnostics but does not beat the fair micro causal-information
> baseline. The declared macro-constraint and syntropy witnesses fail at this
> grain, so the claim contracts.

Unsafe interpretation:

- life has been explained
- syntropy is a settled new physical force
- downward causation breaks physical closure
- this toy receipt upgrades any biology claim above `[C]`
- this post-result bundle establishes a preregistration

# Physics-to-Biology Harness

**Status:** executable toy-model harness, not biological evidence.
**Evidence tier:** `[B]` only for this deterministic repository receipt;
`[C]` for any claim about biology until an independently frozen domain run is
executed.

This folder instantiates the first macro-constraint boundary run as a minimal
two-compartment vesicle model.

```bash
python3 -m unittest test_vesicle_macro_constraint.py
python3 vesicle_macro_constraint.py
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
- `Cost_C`: measurement, memory, control, erasure, model, and entropy-export
  ledger
- witness: `W_C = EI_macro - EI_baseline - Cost_C`
- perturbability: average macro-channel `D_KL(C || notC)`

Current deterministic report:

```text
W_C   = 0.425356
SYN_C = 0.785347
KL    = 0.141286
```

Current freeze manifest:

```text
manifest_version = macro-constraint-freeze-v1
report_sha256    = recorded in FREEZE_MANIFEST.json
file_hashes      = README.md, test_vesicle_macro_constraint.py, vesicle_macro_constraint.py
frozen_objects   = X, K_X, pi, Y, G_C, Cost_C, epsilon
```

The manifest is the freeze receipt for this toy run. If any harness file or the
report changes, regenerate it before citing the receipt.

Safe interpretation:

> In this toy model and at this grain, the declared organization behaves as a
> costed macro-constraint.

Unsafe interpretation:

- life has been explained
- syntropy is a settled new physical force
- downward causation breaks physical closure
- this toy receipt upgrades any biology claim above `[C]`

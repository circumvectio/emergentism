# Formal Reap — Lean 4 proof kernel

**Status:** `[B]` locally machine-checked proof support; `[S]` for formal implications; no automatic doctrine promotion.

This project tests the mathematical claims in `10_SEED/02_THE_REAP.md`. It proves the consequences that follow from explicit definitions and premises, and it supplies countermodels where the Reap's prose is stronger than those premises permit.

**Current checked surface:** 36 registered theorem/countermodel certificates,
each compiled and individually covered by `#print axioms`.

## Reproduce

```bash
export PATH="$HOME/.elan/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
cd 09_TOOLS/03_SIMULATIONS/formal_reap
lake build
python3 verify.py --write-receipt
```

Pinned inputs:

- Lean `v4.32.0` (`lean-toolchain`)
- Mathlib `v4.32.0` (`lakefile.toml`)

`lake build` compiles every proof from the checked-in manifest. `verify.py` rebuilds
the project; rejects `sorry`, `admit`, and custom `axiom`/`constant`
declarations; registers both `theorem` and `lemma` declarations; requires every
certificate to be expected, individually axiom-audited, and named in the proof
ledger; hashes all proof and support inputs; and fails if any verification input
changes during the run. With `--write-receipt`, it writes
`verification_receipt.json`.

## Modules

- `FormalReap/Arithmetic.lean` — reciprocal seam, inversion fixed points, AM–GM/equator peak, AND-class results, and the selected `P = ΦV` model.
- `FormalReap/Physics.lean` — exact normalized-hyperbola and null-coordinate-product equivalence to Einstein's one-axis mass shell, with nonzero mass/`c`; rest-energy branch and ratio bound.
- `FormalReap/Structure.lean` — conditional rung inheritance, reflexivity theorem and countermodel, typed frame/move fence, ordinary `0·∞` rejection, operator-mask/valence independence, and D6 role-return.
- `FormalReap/Ethics.lean` — scoped host-collapse certificate, persistence and non-extraction countermodels, is/ought independence, finite utility results, cone/horizon underdetermination, and the bearer-level dyadic anti-laundering gate.
- `FormalReap/Audit.lean` — `#print axioms` audit for exported certificates.
- `PROOF_LEDGER.md` — claim-by-claim adjudication against the Reap.

## What “machine proved” means

Lean certifies a theorem **relative to its formal types, definitions, and hypotheses**. It does not certify that:

- the physical world instantiates a selected model;
- the D-rungs are actual cosmological history;
- the `μ` transition exists in nature;
- `P = ΦV` is the unique or empirically correct power law;
- the Landauer principle entails the full D5 interpretation;
- an ethical bridge or `η = 0` is forced by descriptive facts;
- a narrative interpretation has been adopted as canon.

Those boundaries are part of the proof result, not exceptions to it.

## Trusted logical base

`#print axioms` may report Mathlib's standard Lean foundations:

- `propext`
- `Classical.choice`
- `Quot.sound`

This project declares no domain axiom and contains no admitted proof.

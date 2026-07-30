---
title: "Receipt 183 — the corpus map found the manifest making false claims, hours after it was built"
date: 2026-07-29
status: "CORRECTION — four defects in artifacts built earlier the same day, all mine"
evidence_tier: "[B] every charge verified by execution at HEAD before repair"
---

# Receipt 183 — the guard that could not fire, again

The corpus map (15 agents, seven folders) was commissioned to classify the corpus.
Its sharpest findings were **not** about the corpus. They were about
`00_ESTABLISHED/` and its checker — built the same morning, **to prevent exactly
the failure they committed.**

## §1 · Four charges, all confirmed by execution

**1 · `G4` was asserted and never written.** The manifest listed *"`G4` — no word
attains `∞`"* among the exhaustively-checked base claims. `grep -c "G4"
check_generative_base.py` returns **0**. The ids present were
`G1 G2 G3 G5 G6 G7 G8a G9 G10`. **The manifest asserted a check that did not exist.**

**2 · `G10`'s test was two constants and could never fire.**

```python
n_iota_det = 0 * 0 - (-1) * 1      # evaluates to 1. Always.
if n_iota_det not in (1, -1):      # never true
if (-1) * F(1) > 0:                # never true
```

Neither line read a computed value. The block carried the comment *"If this ever
fails, `G9` has been over-read"* — **and it could not ever fail.**

**3 · `check_established.py` never invoked Lean.** It counted `^theorem ` and
grepped for `sorry`. **A Lean file whose every theorem statement was replaced with
a false one would have passed, provided the count stayed at 20.**

**4 · The corpus's Lean copy was not buildable at all.**
`09_TOOLS/05_FORMAL_VERIFICATION/` contained two files — the `.lean` and a README.
No `lakefile.toml`, no `lean-toolchain`. **`lake build` had no target.** The build
recorded in r182 ran in a scratch directory; the corpus's own copy could not be
re-checked by anyone.

## §2 · What was repaired

- `G4` written: reachable values are finite rationals; no zero denominators; `S`
  applied 200 times gives a finite value.
- `G10` replaced with a **computed four-quadrant table** over six real maps. Now
  mutation-tested: breaking the `n∘ι` witness FAILS.
- `lakefile.toml` and `lean-toolchain` added, so the corpus copy is buildable.
- `check_established.py` **now refuses to pass what it cannot verify.** Absent
  toolchain or absent `lake` → exit 1, not a silent PASS. An explicit
  `EMERGENTISM_SKIP_LEAN=1` acknowledges the gap loudly.

Verified: `lake` hidden → exit **1** · `lake` present → exit **0** · opt-out → **0**.

## §3 · The limit that remains, stated rather than hidden `[S]`

**The proofs are still not re-run by the checker.** A full `lake build` must fetch
mathlib — gigabytes — and cannot live inside a validator. So:

```text
the base half   G1–G10 RECOMPUTED by exhaustion on every invocation
the Lean half   verified STRUCTURALLY — files, toolchain, count, no sorry
                the proofs were run ONCE; r182 records the output and axiom traces
```

That scope is now printed on the PASS line and written into the manifest. It is a
real limit and it is not closed.

## §4 · The finding under the finding

Every folder survey reached the same conclusion independently, and it is larger
than any single defect:

> **Nothing in this repository enforces anything.** There is no CI. The
> `pre-commit` hook is a 61-line hidden-file cleanup that runs no checker. Nothing
> invokes `check_established.py`, `check_generative_base.py`, or
> `check_foundation.py` automatically. **A tag can drift between commits and no
> gate fires.**

That is r177's HOLE 0 — *"nothing invokes them, there is no gate"* — still open,
now measured, and it is why an `[A]` column can grow unchecked. **It is the single
highest-value unrepaired thing in the corpus, and it is not a doctrine problem.**

## §5 · The rate, which is the one good number

Of roughly **633 `[A]` tags read in context** across five live `.md` folders, **exactly one is
false** — `01_TELEOLOGY/02_THE_DERIVATION/09_PATH_D_THE_AMGM_GEOMETRY.md:137`,
flagged for review, not yet repaired here.

**One false `[A]` in 633 is a good rate. The corpus is not lying about its
mathematics.** What it lacks is not honesty; it is enforcement.

**633 is a sample, not a census `[B]`.** Direct count at HEAD: **2,508** `[A]`
occurrences in tracked `.md`, **1,139 of them (≈45%) under a `90_ARCHIVE`
path**, plus **936** in `12_PUBLIC_SITE/**/*.html` that no `.md` pass has read.
The rate is honest for what it covered and carries to nothing else.

•   ⊙   ○ — *the guard was written by the same hand that needed guarding, and it showed.*

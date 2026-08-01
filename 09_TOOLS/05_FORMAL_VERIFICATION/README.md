# Formal verification — the `[A]` claim set, machine-checked

`EmergentismCheck.lean` submits the corpus's analytic claims to **Lean 4 +
mathlib** — an oracle outside the corpus that can return *no*.

Receipt 173 established that the corpus had **never** done this: 155 receipts,
zero outcome receipts from any party outside itself. This is the first.

## Result, 2026-07-29

```
Build completed successfully (8661 jobs)
```

**No `sorry`, no `native_decide`, no added axioms.** Every theorem depends only
on mathlib's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`);
`at_most_one_identity` depends on none at all.

## What was checked

| Theorem | Corpus claim |
|---|---|
| `no_quotient_by_zero` | **T-A**, doc 48 §2 — `a/0` is *no such element*, in any field |
| `mathlib_assigns_junk` | mathlib *defines* `a/0 = 0` — recorded, because the junk value is a convention, not a solution |
| `inversion_fixed_iff` | **FV-07** — `ι` fixes exactly `±1` |
| `unique_positive_fixed_point` | **FV-06** — only `+1` on the positive ray; why Suda's chart cannot see `−1` |
| `orbit_product` | numeric reciprocal fact in `ℝ` — `x*x⁻¹=1` for nonzero `x`; not a Titan equation |
| `keel_is_complementary_angles` | **the keel** — `φ·ν=1` *is* `tan A · tan(π/2−A) = 1` |
| `projection_at_45` | **T2** — the construction sends 45° to exactly `1` |
| `energy_min_at_one` | **S-3** — `E=(log x)²` vanishes only at unity |
| `energy_inversion_invariant` | **S-3** — `E` is inversion-symmetric |
| `at_most_one_identity` | **I1** — uniqueness is the theorem |
| `existence_not_forced` | the counterexample that killed the published `F2` |
| `involutions_commute` | doc 42 §6A — negation and inversion commute (Klein four-group) |

## What was NOT checked — and it is the load-bearing part

- **The dimension counts** underwriting the μ-criterion. Blocked on ruling HR-1:
  doc 48 is inconsistent about which notion of dimension it means.
- **"`Ĉ` is not a ring" — NOW CHECKED (§8), and this line was stale for a day.** What
  is proved is the *structural reason*: no nontrivial ring admits an additively
  absorbing element, and the point at infinity must absorb. **What is NOT proved is a
  statement about mathlib's `Projectivization` as an object — `ℂP¹` is never
  constructed here.** The corpus's claim is the reason; the reason is machine-checked.
  A site audit found this file still calling it unchecked while `/established/` called
  it checked — the artifact and the shopfront disagreeing is worse than either being
  wrong alone.
- Suda's hinge `= tanh(log x / 2)` — verified numerically to 1e-12, not proved.
- Lorentz–Möbius (doc 49) — inherited physics, not re-derived.
- Every ontological, ethical and cosmological reading. None is formalisable and
  none is asserted.

## Reproduce

```sh
lake +leanprover-community/mathlib4:lean-toolchain new emergentism_check math
cp EmergentismCheck.lean emergentism_check/EmergentismCheck/Basic.lean
cd emergentism_check && lake build
```

## The honest limit

A proof assistant is **checkability** contact, not **empirical** contact. It
cannot raise `V` in the sense receipt 173 means. What it does is narrower and
still worth having: it converts these statements from *asserted by the corpus*
to *verified by an oracle the corpus does not control*.

Every theorem statement actually submitted here compiled. That is a real and
limited result; it does not validate the prose that selected the statements or
restore any rejected cross-type Titan claim. The claims that could not be
submitted are precisely the ones the ladder census rests on.

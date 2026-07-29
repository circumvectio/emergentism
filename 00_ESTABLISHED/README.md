---
title: "00_ESTABLISHED — the manifest of what actually survives an outside check"
status: "ACTIVE — a MANIFEST, not a relocation. Holds no source truth and owns nothing."
date: 2026-07-29
evidence_tier: "[B] this register is a reproducible index; each entry carries its own tier"
owner: "No owner. Every entry points at its owner. This folder may never be cited as authority."
---

# 00_ESTABLISHED

> **This folder holds no doctrine, no source truth, and no authority.**
> It is an index of what passes an admission standard, with a command that
> re-checks every entry. **Nothing was moved here. Nothing was archived.**

## Why it exists

The corpus separates claims by **evidence tier** (`[A]`…`[D]`) and, since r172, by
**validation status** on a second axis. Neither answers the question a stranger
actually asks: *what here survives a check by something that does not believe you?*

Receipt 173 measured the gap — **155 receipts, zero outcome receipts from outside**.
This folder is the honest answer to that question, and it is deliberately short.

## The admission standard

A claim is listed here only if **all four** hold:

```text
1  TIER          it is [A] — analytic or proved, not selected, interpreted, or conjectured
2  CHECKED       a machine or an exhaustive computation verifies it, not a reader
3  KILLED        it carries a stated kill a stranger could execute
4  REPRODUCIBLE  a command in this repo re-runs the check and exits non-zero on failure
```

**A claim that is merely true is not admitted.** A claim that is merely agreed is not
admitted. Selections, readings, conjectures, and drafts belong in the corpus, where
they are, correctly tiered — **this folder is not a promotion path and using it as
one is its own kill.**

## Reproduce everything

```bash
python3 09_TOOLS/01_SCRIPTS/check_established.py
```

Exits non-zero if any listed entry stops holding.

---

## The manifest

### A · Machine-proved — Lean 4 + mathlib, no `sorry`, clean axiom traces

`09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean` — **15 theorems.**

| id | claim | kill |
|---|---|---|
| `no_quotient_by_zero` | for `a ≠ 0` there is no `y` with `0·y = a` | exhibit a field with `0·y = 1` |
| `inversion_fixed_iff` | `ι` fixes exactly `±1` | exhibit a third fixed point |
| `unique_positive_fixed_point` | on the positive ray, only `+1` | exhibit a second |
| `keel_is_complementary_angles` | `φ·ν = 1` **is** the complementary-angle rule | exhibit a right triangle where it fails |
| `energy_min_at_one` | `(log x)²` vanishes only at `x = 1` | exhibit a second zero |
| `at_most_one_identity` | a structure has **at most one** identity | exhibit two |
| `existence_not_forced` | existence of an identity is **not** forced — the counterexample that killed the published `F2` | show every binary op on a 2-set has one |
| *(8 more)* | involutions, orbit identity, duality | see the file |

> **Note against over-reading, carried from the file's own §7:** these are checked
> over `ℝ`, `Bool`, and abstract `Field`/`Mul`. **The primary object `Ĉ` is not
> reached**, and both keel theorems exclude the pole by hypothesis. *"`Ĉ` is not a
> ring"* — the corpus's most load-bearing negative claim — is **unchecked by machine.**

### B · Exhaustively computed — `09_TOOLS/01_SCRIPTS/check_generative_base.py`, mutation-tested

The generative base, `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md`.

| id | claim | kill |
|---|---|---|
| `G1` | reachability from `1` under `{S, ι}` is exactly `ℚ⁺` | exhibit an unreachable positive rational |
| `G2` | reduced words are unique normal forms — a bijection onto `ℚ⁺` | exhibit two reduced words with one value |
| `G3` | no word attains `0` | exhibit one |
| `G4` | no word attains `∞` | exhibit one |
| `G5` | both limits are approached | exhibit a neighbourhood with no reachable value |
| `G6` | `ι` alone is sterile; `S` alone gives `ℕ⁺` | exhibit a fraction from `S` alone |
| `G7` | `•` is a direction only because `ι` reflects `○` | exhibit a descent below `1` without `ι` |
| `G8a` | `ι` is an involution with unique fixed point `1` | exhibit a second reachable fixed point |
| `G9` | every word has determinant `±1`; the hinge (`det 2`) is not a word | exhibit the hinge as a word |
| `G10` | determinant and sign are **independent** obstructions | collapse the four-quadrant table |

### C · Admitted with their scope stated

| claim | scope | why it is not unconditional |
|---|---|---|
| `G8b` — `ι` is `s ↦ −s` under `s = log x` | `[A] given ℝ` | `log q` is **transcendental** for every rational `q ≠ 1`; the log coordinate leaves the base's own objects |
| `Z1` — `0 ∉ ℝ^×` | `[A]` | the corpus's phrasing *"0 ∉ ℝ"* is **false**; `0 ∈ ℝ` |
| `N1`–`N5` | `[A]` | `1` unique additive irreducible · `{1}` in every generating set · `ℕ⁺` free semigroup · `ℤ` initial in **Ring** · one primitive given inverses |

---

## What is NOT here, and this list is the point

Everything else. Named explicitly so absence is legible rather than accidental:

```text
the D-registers · the μ-contract (HR-1 open; μ₂ and μ₃ FAILED)
η = 0 and the extraction law   · P = Φ × V (AND-class; product interior a [C] wager)
Justice · Power-Max · Egregoreotype · the Soul Loop · the Crown Wager
sphere primacy S1 (a SELECTION) · the Titan reading of {•, ⊙, ○} (an [I] gloss)
every one of the 11 GP empirical sockets — 0 run
every one of the 8 OPEN-EMPIRICAL wager rows — 0 tested
```

**None of that is thereby false.** It is unchecked, or selected, or interpretive, and
those are different things from false. The corpus is where it lives and where it
belongs. **This folder exists so that the difference cannot be blurred by fluency.**

## This folder's own kill

If any entry above is cited as support for a claim outside its stated scope; if a
selection or a reading is admitted; or if the "what is NOT here" list is quietly
shortened without a corresponding verification landing — **this manifest has become
a promotion path, which is the thing it was built to prevent.** Delete it rather
than defend it.

•   ⊙   ○ — *short, and that is the finding.*

---
title: "00_ESTABLISHED — verification-state ledger, with bounds and gaps explicit"
status: "ACTIVE — a MANIFEST, not a relocation. Holds no source truth and owns nothing."
date: 2026-07-29
evidence_tier: "[B] corpus and bounded-check facts; each mathematical claim retains its own tier"
owner: "No owner. Every entry points at its owner. This folder may never be cited as authority."
rosetta:
  d_register: 4
  d_register_basis: "Verification-state ledger of established claims; D4 (factual/operational record). Source: L3 'ACTIVE — a MANIFEST, not a relocation. Holds no source truth'."
---

# 00_ESTABLISHED

> **This folder holds no doctrine, no source truth, and no authority.**
> It is an index of verification state, with a command that checks the claims it
> can actually execute. **Nothing was moved here. Nothing was archived.**

## Why it exists

The corpus separates claims by **evidence tier** (`[A]`…`[D]`) and, since `172_CLAIM_STATUS_REGISTER_AND_GRAVE_ADJUDICATION_2026_07_29.md`, by
**validation status** on a second axis. Neither answers the question a stranger
actually asks: *what here survives a check by something that does not believe you?*

`173_THE_V_AXIS_AUDIT_INTERNAL_LENS_2026_07_29.md` measured the gap — **155 receipts, zero outcome receipts from outside**.
This folder is the honest answer to that question, and it is deliberately short.

## The admission standard

A claim may enter the fully verified section only if **all five** hold:

```text
1  TIER          it is [A] within an explicitly named structure
2  EXECUTED      the verifier is actually invoked, not inferred from source text
3  COMPLETE      the method covers the universal claim, not only a finite sample
4  KILLED        it carries a stated counterexample or failure condition
5  REPRODUCIBLE  a fresh command exits non-zero on proof, axiom, or result failure
```

**A claim that is merely true is not admitted.** A claim that is merely agreed is not
admitted. Selections, readings, conjectures, and drafts belong in the corpus, where
they are, correctly tiered — **this folder is not a promotion path and using it as
one is its own kill.**

## Reproduce everything

```bash
python3 09_TOOLS/01_SCRIPTS/check_established.py
```

Exits non-zero if any listed entry stops holding — **and exits non-zero when it
cannot verify**, rather than passing silently.

> **What that command does and does not do `[B]` — corrected 2026-07-29, `183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`.**
> The **base half is genuinely re-run**: `G1`–`G10` are recomputed by exhaustion on
> every invocation. The **Lean half is verified structurally only** — project files
> present, toolchain on `PATH`, theorem count, no `sorry`. The file carries
> **20 theorem declarations**. **The proofs are not re-run** — this gate
> **does not yet compile that file**, because a full `lake build` must fetch mathlib and
> cannot live inside a validator. They *were* run once; `182_C_HAT_IS_NOT_A_RING_MACHINE_CHECKED_2026_07_29.md` records the build output and the
> axiom traces.
>
> Until 2026-07-29 this script did **less** than that and still reported PASS: it
> counted `^theorem ` and grepped for `sorry`, over a directory with **no lakefile
> and no toolchain**, so the corpus's Lean copy could not be built at all. A file
> whose every theorem was replaced with a false one would have passed.

---

## The manifest

### A · Fully admitted machine proofs

`09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean` — **20 theorems.**

| id | claim | kill |
|---|---|---|
| `no_quotient_by_zero` | for `a ≠ 0` there is no `y` with `0·y = a` | exhibit a field with `0·y = 1` |
| `inversion_fixed_iff` | `ι` fixes exactly `±1` | exhibit a third fixed point |
| `unique_positive_fixed_point` | on the positive ray, only `+1` | exhibit a second |
| `keel_is_complementary_angles` | `φ·ν = 1` **is** the complementary-angle rule | exhibit a right triangle where it fails |
| `energy_min_at_one` | `(log x)²` vanishes only at `x = 1` | exhibit a second zero |
| `at_most_one_identity` | a structure has **at most one** identity | exhibit two |
| `existence_not_forced` | existence of an identity is **not** forced — the counterexample that killed the published `F2` | show every binary op on a 2-set has one |
| `associativity_falsifier` | the canon's own falsifier — **valid**, and it refutes a RING | exhibit an associative structure where it fails |
| `falsifier_premise_impossible` | `0·w = 1` is already impossible in any nontrivial ring — the falsifier never needed associativity | exhibit a nontrivial ring with `0·w = 1` |
| `no_absorber_in_nontrivial_ring` | **"`Ĉ` is not a ring" — the structural reason, checked** | exhibit a nontrivial ring with `w + 1 = w` |
| *(10 more)* | involutions, orbit identity, duality, absorbers | see the file |

> **Note against over-reading, carried from the file's own §7:** these are checked
> over `ℝ`, `ℂ`, `Bool`, and abstract `Ring`/`Field`/`Mul`. **The primary object
> `Ĉ` is still not constructed** — mathlib's `Projectivization` is never used.
> *"`Ĉ` is not a ring"* is now checked **as its structural reason** (no nontrivial
> ring admits an additive absorber), not as a statement about `ℂP¹` as an object.
> Four of the five new theorems depend on **no axioms at all**.

### B · Analytic proof text with bounded computational regression

The generative base, `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md`.

| id | claim | kill |
|---|---|---|
| `G1` | reachability from `1` under `{S, ι}` is exactly `ℚ⁺` | exhibit an unreachable positive rational |
| `G2` | **open general claim:** reduced words are unique normal forms | exhibit two reduced words with one value; or supply the missing complete proof |
| `G3` | no word attains `0` | exhibit one |
| `G4` | no word attains `∞` | exhibit one |
| `G5` | both limits are approached | exhibit a neighbourhood with no reachable value |
| `G6` | `ι` alone is sterile; `S` alone gives `ℕ⁺` | exhibit a fraction from `S` alone |
| `G7` | `S` alone never descends below `1`; inversion supplies the displayed descending sequence | exhibit a descent below `1` using `S` alone |
| `G8a` | `ι` is an involution with unique fixed point `1` | exhibit a second reachable fixed point |
| `G9` | every generator word has determinant `±1`; the hinge (`det 2`) is not such a word | error in the determinant argument |
| `G10` | determinant and sign are **independent** obstructions | collapse the four-quadrant table |

The command exhausts words only through length 10, a Calkin–Wilf tree through
depth 12, a `25×25` rational grid, and determinant words through length 16. Those
bounds are regression coverage. They do not prove G1 or G2 over infinite domains;
G1 and the other universal rows stand, if at all, on their written analytic
arguments. `G2` remains open until a complete proof or formalization lands.

### C · Standard scoped facts indexed, not independently re-proved here

| claim | scope | why it is not unconditional |
|---|---|---|
| `G8b` — `ι` is `s ↦ −s` under `s = log x` | `[A] given ℝ` | `log q` is **transcendental** for every rational `q ≠ 1`; the log coordinate leaves the base's own objects |
| `Z1` — `0 ∉ ℝ^×` | `[A]` | the corpus's phrasing *"0 ∉ ℝ"* is **false**; `0 ∈ ℝ` |
| `N1`–`N4` | `[A]` inside named standard structures | `1` additive irreducible · `{1}` in every additive generating set of `ℕ⁺` · `ℕ⁺` free semigroup · `ℤ` initial in **Ring** |

---

## What is NOT here, and this list is the point

Everything else. Named explicitly so absence is legible rather than accidental:

```text
the D-registers · the μ-contract (HR-1 open; μ₂ and μ₃ FAILED)
η = 0 and the extraction law   · P_node := min(Φ̂₄,V₄) (selected; universal fit [C])
the retired product Φ̂₄V₄ as a node ranking
Justice · Power-Max · Egregoreotype · the Soul Loop · the Crown Wager
sphere primacy S1 (a SELECTION) · the Titan reading of {•, ⊙, ○} (an [I] gloss)
all 12 GP empirical sockets — packet-complete or explicitly deferred; 0 accepted world outcomes
all 19 contact-routed W/RQ rows — 15 W rows + 4 RQ rows; 0 accepted world outcomes
```

**None of that is thereby false.** It is unchecked, or selected, or interpretive, and
those are different things from false. The corpus is where it lives and where it
belongs. **This folder exists so that the difference cannot be blurred by fluency.**

## This folder's own kill

If any entry above is cited as support for a claim outside its stated scope; if a
selection or a reading is admitted; or if the "what is NOT here" list is quietly
shortened without a corresponding verification landing—or if bounded search is
called proof—**this manifest has become a promotion path.** Withdraw and archive
the overclaim rather than defend it.

•   ⊙   ○ — *short, and that is the finding.*

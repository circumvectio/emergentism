---
title: "00_ESTABLISHED — verification-state ledger, with bounds and gaps explicit"
status: "ACTIVE — a MANIFEST, not a relocation. Holds no source truth and owns nothing."
date: 2026-07-29
evidence_tier: "[B] corpus and bounded-check facts; each mathematical claim retains its own tier"
owner: "No owner. Every entry points at its owner. This folder may never be cited as authority."
---

# 00_ESTABLISHED

> **This folder holds no doctrine, no source truth, and no authority.**
> It is an index of verification state, with a command that checks the claims it
> can actually execute. **Nothing was moved here. Nothing was archived.**

## Why it exists

The corpus separates claims by **evidence tier** (`[A]`…`[D]`) and, since r172, by
**validation status** on a second axis. Neither answers the question a stranger
actually asks: *what here survives a check by something that does not believe you?*

Receipt 173 measured the gap—**155 receipts, zero outcome receipts from outside**.
This folder must not rename internal scripts as outside review. It is deliberately
short and may legitimately contain no fully admitted new claim.

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

Exits non-zero if the ledger overstates what its executable checks establish.

---

## The manifest

### A · Fully admitted machine proofs

**None currently admitted from the 2026-07-29 addition.**

`09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean` contains **15 theorem
declarations**, but `check_established.py` does not yet compile that file in a
pinned Lean/mathlib project or inspect axiom traces. Source presence and absence
of `sorry` are lint facts, not a proof receipt. The declarations are therefore
**proof candidates**, not machine-established entries.

Even after compilation, their scope would remain `ℝ`, `Bool`, and abstract
`Field`/`Mul`; they would not establish a global operation on `Ĉ`, Titan
arithmetic, ontology, or any world claim.

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
shortened without a corresponding verification landing—or if bounded search is
called proof—**this manifest has become a promotion path.** Withdraw and archive
the overclaim rather than defend it.

•   ⊙   ○ — *short, and that is the finding.*

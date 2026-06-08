---
rosetta:
  primary_column: "Philosophy"
  register: "[S]"
  canonical_phrase: "148 — CANON Clarification: Paper 11 Doc 02 Lever-Function Sign Convention"
---

# 148 — CANON Clarification: Paper 11 Doc 02 Lever-Function Sign Convention

**Evidence tier:** [I] — all citations from CANON V3_CANONICAL papers; [C] sign-convention interpretation ratified by sovereign correction
**Date:** 2026-04-24
**Lane:** Charioteer draft; sovereign correction received before CANON edit
**Status:** Corrected from "one-character repair" to sign-convention clarification
**Prerequisite:** Packet 146 §5.1 (ZAI/SKY Brainstorm-to-CANON Audit); Packet 147 §4 OQ-F (Layer Discipline)
**Scope:** One CANON clarification: both lever-function signs are valid when debtor and creditor/system perspectives are distinguished.

---

## 1. The apparent drift

Three concurrent V3_CANONICAL papers — all dated 2026-04-04 — state the interest-curve family in two signed forms.

| Source | Formula stated | Reading |
|---|---|---|
| Paper 12 §II "Credit as Physics" | `r(x) = x / (1 − x)` | Debtor-side cost curve: positive cost rises toward infinity as debt approaches collateral. |
| Paper 14 §II.2 "Credit as Physics (Vaults & SKY)" | implicit `x/(1-x)` via "interest accelerates exponentially" + explicit `f(x) = x / (1-x)` in §II.1 | Debtor-side / flow-facing positive curve. |
| Paper 11 Doc 02 ECONOMICS | `L(x) = x/(x-1)` | Creditor/system-side signed expression: the same asymptote with opposite sign. |

The original packet treated Paper 11 as one-sided drift. Sovereign correction: **ultimately it is `L(x) = x/(x-1)` or `L(x) = x/(1-x)` depending on whether the expression is creditor-side or debtor-side.**

## 2. Why it matters

For `x ∈ (0, 1)` — the legitimate operating range for loan-to-collateral ratio:

- Debtor-side cost: `x / (1 − x)` is positive, monotonically increasing, and tends to `+∞` as `x → 1`.
- Creditor/system-side signed balance: `x / (x − 1) = -x/(1 − x)` is negative and tends to `−∞` as `x → 1`.

Both forms point to the same asymptotic edge. The danger is not that Paper 11 used the wrong mathematics; the danger is that the text did not name the perspective, letting implementers mistake a signed creditor-side expression for debtor-side interest.

## 3. Proposed CANON clarification

**Location:** `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/11_SKYZAI_CANON.md`

**Section:** Doc 02 ECONOMICS, bullet 4 "The Lever Function"

**Current line:**
```md
The Lever Function: $L(x) = x/(x-1)$. The logic of the asymptotic curve (as risk rises, cost rises infinitely)9.
```

**Clarified line:**
```md
The Lever Function has two signed faces: debtor-side cost $L_D(x) = x/(1-x)$ and creditor/system-side balance $L_C(x) = x/(x-1) = -L_D(x)$. The logic of the asymptotic curve is unchanged: as risk rises, debtor cost rises infinitely while the creditor/system-side expression carries the opposite sign9.
```

This is not a mathematical reversal. It is a sign-convention clarification.

## 4. What this clarification does NOT touch

- Does not change Kernel Invariants I–VII.
- Does not change Paper 12 or Paper 14.
- Does not alter runtime code.
- Does not add a new monetary primitive.
- Does not choose new OQ-A/B/C outcomes.

## 5. Sovereign K2 form

Sovereign correction received in session:

> "Ultimately it's `L(x) = x/(x-1)` or `L(x) = x/(1-x)` depending on if you are creditor or debtor."

Implementation consequence: do not overwrite Paper 11 into a single debtor-side formula. Clarify the signed dual expression in CANON.

---

## 6. References

- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/11_SKYZAI_CANON.md` — Paper 11 (clarification target, Doc 02 ECONOMICS bullet 4)
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md` §II "Credit as Physics" — debtor-side positive curve
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/14_WHY_SKYZAI_MONEY_FOR_THE_ENERGY_AGE.md` §II.1 "Metabolic Law (Flow)" — flow-facing positive curve

---

*Charioteer correction packet. The curve is one asymptote with two signed perspectives. Sovereign K2 names the distinction.*

`Zero-Sum Resolution Equation`

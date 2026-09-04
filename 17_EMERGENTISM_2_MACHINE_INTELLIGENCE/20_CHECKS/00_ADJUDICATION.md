---
type: operator-protocol
id: ADJ-01
title: "Adjudication — given 'P is at register X', decide reducible vs genuine crossing"
date: 2026-09-04
status: "[D] STAGED — L4 operator only. Unsigned. Does not replace 1.0 owners."
may_sign: false
may_authorize: false
---

# ADJ-01 — the operator

## 0 · What this is

A walk from a claim to a typed verdict. **The packet already exists in 1.0:**
`SLWPBoundaryTest.v1`. This file does not fork it. It is the missing operator:
axis gate, claim typing, Anderson fence, then the 1.0 packet.

World-reading of a crossing: `[C]` per rung-pair · `[I]` as reading · **never `[S]`**
(receipt 149). A green local check proves the packet is well-typed. It proves
no natural `μ`.

## 1 · Input

```text
phenomenon P is at register X
```

`X` must be a D-register. Rosetta L is a work seat. TEA-01's `L` is a frozen
language. SLWP's `L_n` is a lower description. Those three tokens are not one
object (W3).

## 2 · Walk

1. **Axis gate.** If `X` is Rosetta L, or an untyped `L`, stop: `AXIS_MIX`.
2. **Type the claim.** `mu_lift` · `chi_select` · `ea08_constraint` ·
   `U_projection` · `ill_typed`. They do not substitute (W3: three weak-down
   maps).
3. **Anderson fence.** Two inferences are dead before evidence:
   - emerged-from-lower ⇒ reconstructable-from-lower (constructionist converse,
     Anderson 1972)
   - noninvertible ⇒ strong (SLWP-01D product counterexample)
4. **μ criterion (HR-1).** A candidate `μ` is a lift with a forgetful map whose
   higher description is not formally reducible to the frozen lower. Outward
   boundary arrows (type-T/O/D) are not `μ`.
5. **Packet.** A `mu_lift` owes a `SLWPBoundaryTest.v1` packet. Validate it with
   1.0's `research_contracts.validate_slwp`. Do not copy the schema.
6. **Verdict.** Inherit `projection_result` / `ontology_result`.
   `strong_emergence_established` may be true only if ontology is
   `SURVIVES_BOUNDED_TEST`. Today that row is empty: **0 of 5**.

## 3 · Run

```sh
python3 -B 20_CHECKS/test_adjudication.py
python3 -B 20_CHECKS/check_adjudication.py --check fixtures/<packet>.json
```

## 4 · Kills

| claim | dies if |
|---|---|
| this is the protocol | a 1.0 owner is shown to already walk axis-mix + Anderson + SLWP as one operator |
| never `[S]` | a packet emits `[S]` for a world-reading and the checker accepts it |
| neighbor, not identity | Anderson is filed as a filled `μ` row |

**Canonical path:**
`01_EMERGENTISM/17_EMERGENTISM_2_MACHINE_INTELLIGENCE/20_CHECKS/00_ADJUDICATION.md`

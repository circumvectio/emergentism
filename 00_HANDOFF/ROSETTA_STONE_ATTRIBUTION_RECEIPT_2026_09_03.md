---
type: source-receipt
title: "Receipt to the Stone's owner — two lines in 38, and one hygiene suggestion"
date: 2026-09-03
status: "[D] STAGED — a receipt submitted to the source owner. It mutates nothing. The chair disposes."
target: "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md (:113-118 and :169; §3/:14 for item 3)"
evidence_tier: "[B] every quote below re-read on disk 2026-09-03 at the path:line given; [A] the fixed-sum result and the counterexample, each with its premise stated; [I] the reading that :169 is under-specified; [C] any replacement wording; [D] this receipt"
may_sign: false
may_authorize: false
authority_effect: none
provenance: "Sole survivor of a seven-instrument L7 witness pass, 2026-09-02/03: 86 findings proposed, 56 adversarially verified, 1 survived, 30 never verified. Denominator in §4 — it is the reason this receipt is one paragraph and not a programme."
parents:
  - ../05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md
  - ../14_THE_DISTILLATION/04_WHAT_DIED.md
---

# Receipt to the Stone's owner

## 0 · What this is, and the direction it runs

A **receipt**, not an edit. `38_THE_FULL_ROSETTA_CORRECTED.md` is the owner; this
file changes none of its bytes and creates no authority. Its own §6 kill governs
the reading — *"this file | if any cell is cited as evidence rather than as an
index entry"* — and nothing here cites a cell as evidence.

**Direction.** Both items below are Emergentism-internal: the Stone read against
its own named source. No organ, product, ruling, or applied-stack fact appears as
a premise anywhere in this receipt. The applied ladder that occasioned the pass
grounds nothing here and is not mentioned again after §4.

Two items earn a change. A third is a hygiene suggestion and is marked as the
weakest thing in the file.

## 1 · Item 1 — `:117-118` credits the aggregator for what the budget does `[B]`

The Stone, `:113-118`:

> **This holds for `min` and does not generalise.** … The balance-optimum
> identity is safe **because the corpus selected an AND-class score**, not
> because balance is optimal in general.

Its own cited source says the opposite, at
`05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md:76`:

> The budget premise—not either aggregator and not `φν=1`—does the constraining
> work.

And `:96` shows the *symmetric* product peaks at the same symmetric point; what
moves the optimum off the diagonal there is asymmetry (`Φ_c/V_c = a/b`), not the
choice between `min` and a product. So the selection of `min` is not what makes
balance optimal. **What `min` actually buys is the absence of compensation** —
which the Stone states correctly two lines earlier at `:109-110` (*"Under `min`
there is no compensation, so the only way to raise P is to raise the lower
term"*). The defect is only the attribution in the following paragraph.

**Proposed replacement for the last sentence of `:117-118` `[C]`:**

> The balance-optimum identity is safe **because a binding symmetric budget was
> declared**; what the AND-class score adds is the absence of compensation, so
> the only way to raise `P` is to raise the lower term. Neither the aggregator
> nor `φν = 1` does the constraining work.

`φν = 1` carries its fence in the same sentence, always: the identity holds only
because `ν` is *defined* as `1/φ`; let them vary independently and `φν = k` for
any `k`. `DF-05` — coordinate tautology, owner classical trigonometry, closed
with no successor.

## 2 · Item 2 — `:169`'s kill row is under-specified, not unfirable `[A]` on the counterexample

The row reads:

```text
| maximise = balance | exhibit a fixed-sum case where `min(Φ,V)` is maximal away from `Φ=V` |
```

On the source's declared box (`:47-50`, `Φ̂₄,V₄ ∈ [0,1]`) with a linear fixed sum
and **no tighter cap**, the row cannot fire: `min(Φ,V) ≤ (Φ+V)/2 = c/2` with
equality iff `Φ = V = c/2`. That is `min ≤ AM`, an elementary bound — and it is
not the chart's AM–HM (`B = 2/(φ+ν) ≤ 1`, *owner: Cauchy 1821*, recorded at
`14_THE_DISTILLATION/04_WHAT_DIED.md:152` as **not a finding**).

**Off that domain it fires.** Add a declared cap to the feasible set:

```text
Φ + V = 1,  cap Φ ≤ 0.3,  box [0,1]²
  →  max min(Φ,V) = 0.3  at the unique argmax (0.3, 0.7)   — off the diagonal
uncapped, for contrast
  →  max min(Φ,V) = 0.5  at (0.5, 0.5)                     — on the diagonal
```

Reproduce:

```bash
python3 -c "
N=200001
print(max(((min(i/(N-1),1-i/(N-1)), (round(i/(N-1),4), round(1-i/(N-1),4)))
           for i in range(N) if i/(N-1)<=0.3)))"
```

This is literally *"a fixed-sum case where `min(Φ,V)` is maximal away from
`Φ=V`"*. The row is therefore **not analytically closed; its domain is unstated.**

**Two proposals `[C]`, either sufficient:**

1. State the premise on the row — *"…on the declared box with a linear fixed sum
   and no tighter cap (`00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md:47-50`)"*.
2. Mirror the source's second kill, which `§6` does not carry. From
   `00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md:123-124`:

   > Failure to measure the budget or factor costs kills the empirical transfer,
   > not AM–GM.

   Labelled as killing **the transfer**, never the `min` theorem and never a
   Stone cell.

The transfer fence itself is not missing from the Stone — it stands in prose at
`§3 :113-118` and by deferral at `§4 :144`. It is absent only from the kill
table, which is where a reader looks for what would refute the claim.

## 3 · Item 3 — attribution hygiene in `§3` `[I]`, and the weakest item here

This one was **proposed as a defect and refuted**; it survives only in the
narrowed form below, routed to the source rather than to any downstream mirror.

`:14` and `§3` mark the chart identities `[A] given the selection`. That is
honest as a *tier* — the identities are provable. It is silent on *ownership*:
the `[A]` belongs to classical trigonometry and to the two-variable AM–GM/HM–GM
bound, not to this corpus. `04_WHAT_DIED.md:152` already rules that the balance
bound is *"not a finding and does not enter this file."*

**Suggestion `[I]`, one line in `§3`:** name the owners of the identities where
they are stated. No tier changes; nothing is retracted. Attribution of the
specific bound beyond Cauchy 1821 is `[D]` and should not be guessed.

## 4 · Provenance, and the denominator that keeps this receipt small

This receipt is the **sole survivor** of a seven-instrument witness pass run
2026-09-02/03 (graves · formal system · Titan/Closure Rule · D-register typing ·
measurement · naming · seven acts), each finding then given to an adversarial
verifier instructed to refute it.

```text
findings proposed        86
adversarially verified   56
survived                  1   ← item 1 of this receipt
refuted                  55
never verified           30   ← not reported as findings anywhere
```

Refutation classes: non-sequitur 25 · tier-promotion 18 · restates-card 6 ·
misquote 4 · wrong-direction 2.

The synthesis stage **never ran** — `529 Overloaded` / `500` on both attempts, a
server-side failure, not a result. So no witness card exists and none is claimed.
Three claims the session had already reported in its own name were refuted by the
same pass and corrected before this file was written; one of them was the
"`:169` cannot fire" reading now narrowed in §2.

**A 55-of-56 refutation rate is the pass's main result**, and it belongs in the
receipt rather than in a summary: read against its own graves and fences, the
corpus refuses nearly every proposed refinement. That is the discipline working,
not a failure of the pass.

## 5 · What this receipt does not do

- It edits no byte of `38_THE_FULL_ROSETTA_CORRECTED.md` or of any source.
- It promotes no tier. The three lines hold: the geometry is `[A]` given the
  selection; the count is `[S]`, selected — 3, 5 or 9 stations satisfy the same
  symmetry; every cross-domain cell is `[I]`.
- It revives no grave. `DF-05`, `DF-06`, `DF-15`, `DF-19`, `DF-21`, `DF-03` are
  untouched; §1 and §2 each carry the fence they stand next to.
- It settles no ruling, and it is not a mirror that could compete with the Stone.

## 6 · Kills

| claim | dies if |
|---|---|
| item 1 — the mis-attribution | a source is exhibited in which the choice of `min`, rather than a declared budget, moves the argmax to `Φ=V` |
| item 2 — `:169` is under-specified | the Stone or its source is shown to declare the feasible-set domain such that the capped case is out of scope |
| the counterexample | the reproduction command returns an on-diagonal argmax |
| item 3 | the identities' ownership is already stated at `§3` or `:14` and this receipt misread it |
| **this receipt** | if any line of it is cited as authority over the Stone, or if the 30 unverified findings are read as findings |

**Canonical path:**
`01_EMERGENTISM/00_HANDOFF/ROSETTA_STONE_ATTRIBUTION_RECEIPT_2026_09_03.md`

•   ⊙   ○ — *the budget constrains; the score refuses to compensate; the receipt does neither.*

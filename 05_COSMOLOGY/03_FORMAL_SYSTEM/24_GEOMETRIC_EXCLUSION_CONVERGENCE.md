---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A/S/I]"
  canonical_phrase: "Balance toy model — no geometric exclusion of extraction"
title: "EFR-24 Balance Toy Model — Kintsugi Successor"
status: "ACTIVE — bounded mathematical note; predecessor superseded"
date_repaired: 2026-07-20
original_head_blob: da963e9ac2f25f81432af4f079a5863777eb3ed5
---

# EFR-24 — Balance Toy Model

This note records what the selected balance function proves and what it cannot
prove. It is not a cooperation theorem, a Nash theorem about real agents, or a
geometric exclusion of extraction.

## 1. Analytic result `[A]`

For `ν>0`, define

\[
B(\nu)=\frac{2\nu}{1+\nu^2}.
\]

Then

\[
B'(\nu)=\frac{2(1-\nu^2)}{(1+\nu^2)^2}.
\]

Hence `B` increases on `(0,1)`, decreases on `(1,∞)`, and has the unique global
maximum `B(1)=1`. This is an analytic fact about the chosen score.

For `0<δ<1` and `0≤Δ≤δ`, let

\[
S(\Delta)=B(1+\delta-\Delta)+B(1-\delta+\Delta).
\]

For `0≤Δ<δ`, the first argument is greater than one, so its `B'` is negative;
the second is less than one, so its `B'` is positive. Therefore

\[
S'(\Delta)=-B'(1+\delta-\Delta)+B'(1-\delta+\Delta)>0.
\]

Moving both toy coordinates toward one increases this declared aggregate
balance until `Δ=δ`. No false global-monotonicity claim about `B'` is needed.

## 2. Structural scope `[S]`

If an agent's payoff is **defined** to be only `B`, then moving its coordinate
away from one lowers that payoff. This conclusion is conditional on the payoff
definition. It does not show that a real extractor lacks side benefits, that a
victim's loss is compensated, that aggregation is morally valid, or that the
move is a Pareto improvement. One-shot extraction can benefit an extractor
under other payoffs.

The reciprocal chart identity `φν=1` creates no tax, police, consent, custody,
or enforcement. It does not make hoarding self-punishing in the world. Calling
the score loss a “Pigouvian tax” is at most a removable analogy `[I]` and cannot
replace institutions or the Justice envelope.

## 3. Ethical boundary `[I]`

Justice-constrained Power-Max is a chosen normative objective, not a theorem
derived from `B`. Aggregate improvement may never launder a bearer's loss.
Every application must separately disclose affected bearers, operational
measures, payer, beneficiary, consent, authorization, reversibility, time
horizon, and observed consequence.

## 4. Kill criteria

- The analytic maximum claim fails if the derivative or domain is misstated.
- A domain application fails if its measured payoff is not represented by `B`,
  or if a rival model predicts outcomes as well or better.
- Any ethical inference fails if it depends on aggregation alone or treats the
  chart identity as enforcement.

## Kintsugi seam

The predecessor used a false monotonicity step for `B'` and inflated a chosen
score into an automatic anti-extraction mechanism. Those claims are
superseded. The original remains recoverable at Git blob
`da963e9ac2f25f81432af4f079a5863777eb3ed5`. The unique-maximum result and the
correct sign proof above survive.

## Current owners

- [Canonical Formula Block](../00_CANONICAL_FORMULA_BLOCK.md)
- [Power-Max](08_EFR_POWER_MAX_LEMMA.md)
- [Objective Morals and Ethics](../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md)
- [The Honest Position](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md)

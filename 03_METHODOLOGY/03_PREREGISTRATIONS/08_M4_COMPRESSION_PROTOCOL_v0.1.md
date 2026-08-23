---
title: "M4-01 — Frozen Comparator Protocol for the Four-Axis Game-Space Compression"
id: "M4-01"
protocol_version: "0.1.0"
date: 2026-08-23
status: "DRAFT TO FREEZE [D] — no corpus scored; maximality untested"
evidence_tier: "[D] selected protocol; [C] compression and maximality claims; later measurements retain their own tiers"
owner: "03_METHODOLOGY preregistration surface"
source_claim: "The Burrisphere/Rosetta chart may compress a declared strategy corpus; it does not exhaust game theory"
---

# M4-01 — Four-Axis Game-Space Compression Protocol

## 1. Claim under test

The proposed chart uses four declared strategic contrasts—ego/collective,
taking/giving, physical/represented power, and short/long horizon—to encode a
bounded corpus of games or policies. The empirical question is whether this
encoding preserves more decision-relevant structure per unit description than
frozen comparators.

“M4” is a protocol label. It is not a proof that four metaphysical dimensions
exist, that the chart is complete, or that every game has one true placement.

## 2. Required frozen object

Every run instantiates `M4Compression.v1` and declares, before scoring:

- the exact corpus, version, hashes, sampling rule, and exclusions;
- a native encoder supplied without Emergentist coordinates;
- the prediction, retrieval, clustering, transfer, or decision target;
- code length, parameter count, and the treatment of missing placements;
- a distortion metric and a minimum performance floor;
- train, validation, and held-out splits;
- all comparator implementations and equal-resource constraints; and
- the kill, survivor, uncertainty method, and independent-review plan.

## 3. Frozen comparator class

The minimum comparator class contains all of:

1. `NATIVE` — the corpus's own labels or standard domain representation;
2. `ONE_AXIS` — the strongest one-axis reduction selected on development data;
3. `ALTERNATE_TWO_AXIS` — a non-Emergentist two-axis representation;
4. `ADDED_AXIS` — the proposed representation plus at least one additional
   independently motivated axis;
5. `LEARNED_NO_PLACEMENT` — an equal-budget learned representation with no
   predetermined chart placement.

A weaker or omitted comparator blocks a maximality statement.

## 4. Decision rule

The proposed encoding survives only if it reaches the frozen performance floor,
beats `NATIVE`, `ONE_AXIS`, `ALTERNATE_TWO_AXIS`, and
`LEARNED_NO_PLACEMENT` on the held-out target after complexity penalties, and
the `ADDED_AXIS` comparator fails to produce a practically material gain at
the frozen uncertainty threshold.

The only permitted positive wording is:

> Within the frozen corpus, task, metric, resource budget, and comparator
> class, the four-axis encoding was the shortest representation meeting the
> declared performance and distortion floors.

This is **class-relative compression maximality**, not global maximality.

## 5. Kills

Kill or narrow the compression claim if:

- results depend materially on an undisclosed placement rule;
- a native or generic learned representation matches it at lower code length;
- an added axis produces a material held-out gain;
- performance falls below the frozen floor;
- rankings change under reasonable metric or split perturbations; or
- the corpus was selected using the desired placements or results.

If killed, the chart may survive as a visualization, interpretive vocabulary,
or hypothesis generator. It does not survive as a measured optimal code.

## 6. Relation to the Burrisphere and Rosetta

The Burrisphere supplies a geometric visualization; the Rosetta supplies a
typed translation discipline. Neither supplies the measurement result. The
four-axis proposal may be a powerful human-scale compression while leaving
game theory's mathematical strategy spaces, equilibrium concepts, information
structures, dynamics, and mechanism classes open.

## 7. Acceptance boundary

This version stops at deterministic schemas, synthetic fixtures, negative
tests, and manifest checks. No corpus has been selected, no model has been run,
and no compression or maximality result has been observed.

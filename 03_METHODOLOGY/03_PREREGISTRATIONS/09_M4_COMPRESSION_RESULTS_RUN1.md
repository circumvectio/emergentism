---
title: "M4-01 run 1 — the four-axis encoding measured against the frozen comparator class"
id: "M4-01-RUN-1"
protocol: "08_M4_COMPRESSION_PROTOCOL_v0.1.md"
protocol_version: "0.1.0"
date: 2026-09-11
status: "[B] MEASURED — first run of this instrument. Disposition of the protocol's own status line is the owner's."
evidence_tier: "[B] the measurement; [A] the corpus construction and the ground-truth labels; [S] the kill conditions, quoted from the protocol"
owner: "Yves R. Burri — K2. Source authority remains with 08_M4_COMPRESSION_PROTOCOL_v0.1.md."
may_sign: false
authority_effect: none
result_state: KILLED
---

# M4-01 run 1

`•  ⊙  ○`

## 0 · What changed

`08_M4_COMPRESSION_PROTOCOL_v0.1.md` §7 said, since 2026-08-23:

> **No corpus has been selected, no model has been run, and no compression or
> maximality result has been observed.**

A corpus has now been selected, a model has been run, and a result has been
observed. **This is the first measurement ever taken with this instrument.**

The contract instance is `m4_compression_harness/M4Compression.v1.instance.json`.
It validates clean against `v2_2_contracts/research_contracts.py::validate_m4`
and against the JSON schema with `additionalProperties: false`.

---

## 1 · The corpus, and why this one

**`ORDINAL_2X2_COMPLETE`, n = 78, sha256 `a2c4d3bf…`**

§5 lists a kill: *"the corpus was selected using the desired placements or
results."* The only corpus immune to that kill is a **complete enumeration** —
there is no sampling rule to bias because nothing is sampled.

Generated from the definition by `game_corpus.py`: two players, each holding a
strict ordinal ranking over four outcome cells, giving `24 × 24 = 576` ordered
pairs, reduced under the order-8 relabelling group (swap row labels, swap column
labels, exchange player roles) to **78 orbits**.

That 78 is the classical count for this space — Rapoport & Guyer (1966). The
generator reproduces it from first principles without being told it, which is an
independent check on the construction. The literature is cited as the external
provenance of the space, never as authority for the count.

**Ground truth is computed, not interpreted.** `pure_ne_count`, `nash_pareto`,
`is_dilemma`, `row_dominant` all follow from the payoff ranks by definition.

---

## 2 · The placement rules, declared — including the two that do not exist

§5 kills a result that *"depends materially on an undisclosed placement rule."*
So every axis states its rule:

| axis | rule on this corpus |
|---|---|
| **ego / collective** | is a player's own best cell also the joint-rank maximiser? Per player, summed. **Declared, computable.** |
| **taking / giving** | at a player's best cell, does the opponent receive rank ≥ 3? Per player, summed. **Declared, computable.** |
| **physical / represented power** | **no referent.** A one-shot ordinal game carries no beliefs, models, signals or information structure. Nothing here denotes "represented power." |
| **short / long horizon** | **no referent.** A one-shot game has one period. |

The two unassignable axes were recorded as **costed missing placements**, which
is what the schema's own `missing_placement_costed: true` field exists for — not
assigned by invention, which would have been the §5 kill.

**Reporting two of four axes as having no referent is a result, not an evasion.**

---

## 3 · The measurement

Identical learner for every representation — a depth-3, 8-leaf decision tree,
deterministic, pure Python — over identical deterministic stratified 6-fold
rotations. `ONE_AXIS` and `LEARNED_NO_PLACEMENT` selected their features on
development folds only.

**Primary target — `pure_ne_count`:**

| representation | macro-F1 | (min–max) | bits |
|---|---:|---|---:|
| `ALTERNATE_TWO_AXIS` — dominance × conflict sign | **0.9407** | 0.82–1.00 | 273 |
| `ADDED_AXIS` — the four axes **plus dominance** | 0.8963 | 0.78–1.00 | 667 |
| `NATIVE` — the eight ordinal ranks | 0.7195 | 0.55–0.92 | 1065 |
| `ONE_AXIS` — dominance alone | 0.5778 | 0.56–0.60 | **135** |
| `LEARNED_NO_PLACEMENT` | 0.5778 | 0.56–0.60 | 219 |
| **`M4_FOUR_AXIS` — the proposal** | **0.2817** | 0.28–0.29 | 542 |
| `M4_TWO_LIVE_AXES` — proposal minus the missing-placement cost | 0.2817 | 0.28–0.29 | 279 |
| *majority baseline* | *0.2815* | — | *0* |

**The proposal scores the majority baseline.** It carries no information about
the target beyond naming the most common class.

**And the missing-placement penalty is not the cause.** `M4_TWO_LIVE_AXES` — the
two axes that *do* have a referent, carrying no missing-placement cost — scores
identically, on this and on every other target. The two live axes carry the
failure by themselves.

### The fairness check

`pure_ne_count` is equilibrium structure, and the four axes are about
motivational orientation. So the run was repeated on three further targets,
including the one that is the axes' own home ground:

| target | proposal | majority baseline | best comparator |
|---|---:|---:|---|
| `pure_ne_count` | 0.2817 | 0.2815 | 0.9407 `ALTERNATE_TWO_AXIS` |
| **`nash_pareto`** — does self-interest reach the joint optimum | **0.4464** | **0.4545** | 0.8396 `ADDED_AXIS` / `LEARNED` |
| `is_dilemma` | 0.6538 | 0.4868 | 0.6538 `ONE_AXIS` **at 89 bits vs 536** |
| `row_dominant` | 0.3429 | 0.3710 | 1.0000 `NATIVE` / `ONE_AXIS` |

**On `nash_pareto` — the ego/collective question, the axes' home turf — the
proposal scores below the majority baseline.** On `is_dilemma`, where it ties for
best, a single mechanical rank comparison matches it exactly at one-sixth the
code length.

---

## 4 · Verdict: `KILLED`, and precisely how

Three of §5's kill conditions fired, and §4's decision rule was not met.

| §5 condition | fired | evidence |
|---|---|---|
| a native or generic learned representation matches it at lower code length | **yes** | `ONE_AXIS` 0.5778 at 135 bits vs 0.2817 at 542; on `is_dilemma`, exact match at 89 bits vs 536 |
| an added axis produces a material held-out gain | **yes** | one added axis: +0.61 macro-F1 (primary), +0.39 (`nash_pareto`), +0.48 (`row_dominant`) |
| performance falls below the frozen floor | **yes** | floor `macro_f1 ≥ 0.8`; reached on no target |
| results depend on an undisclosed placement rule | no | every rule declared in §2 above; the two unassignable axes costed, not invented |
| corpus selected using desired placements or results | **cannot fire** | complete enumeration |
| rankings change under reasonable perturbation | not fired | ordering stable across four targets and six folds |

§4 requires beating `NATIVE`, `ONE_AXIS`, `ALTERNATE_TWO_AXIS` and
`LEARNED_NO_PLACEMENT` on the held-out target. **It beat none of them, on any
target.**

---

## 5 · What survives, stated narrowly

§5: *"If killed, the chart may survive as a visualization, interpretive
vocabulary, or hypothesis generator. It does not survive as a measured optimal
code."* That is the disposition.

**The scope of this kill, and it is narrow:** one corpus, one-shot strictly
ordinal 2×2 games, complete at n = 78; four targets; one learner; one comparator
class. Fold sizes are 13, and per-fold ranges are reported rather than hidden.

**Half the chart was never tested.** Axes 3 and 4 have no referent in a one-shot
game. This run therefore says nothing about the four-axis encoding on corpora
where those axes denote — repeated games, policies, corpora carrying an
information structure or a horizon. **That is the obvious next run, and the
harness accepts a new corpus unchanged.**

What this run does establish is narrower and still worth having: **on the
cleanest complete strategic corpus available, the two axes that do have a
referent carry no measurable decision-relevant structure, and cheap standard
descriptors carry a great deal.** Dominance and conflict-sign — two ordinary
game-theoretic descriptors, nine cells, 273 bits — reach 0.94.

---

## 6 · Kills on this document

| claim | tier | kill |
|---|---|---|
| The corpus is the complete ordinal 2×2 space at n = 78 | `[A]` | re-run `game_corpus.py`; a different orbit count under the stated group kills it |
| The proposal scores the majority baseline on the primary target | `[B]` | re-run `run_m4_compression.py`; any material difference kills it |
| The missing-placement cost is not the cause of the failure | `[B]` | show `M4_TWO_LIVE_AXES` diverging from `M4_FOUR_AXIS` on any target |
| Three §5 conditions fired | `[S]` | show any of the three quoted conditions unmet on these numbers |
| The kill is corpus-scoped, not general | `[S]` | this document fails if it is ever cited as killing the compression claim generally |

**This document's own kill.** If it is cited to show the Rosetta or the
Burrisphere is refuted, it has been misread and should be withdrawn. It measured
one declared four-axis encoding against one comparator class on one corpus. The
protocol said that is all it could ever do — §6: *"Neither supplies the
measurement result."*

---

`•  ⊙  ○` — *the instrument was built to be able to say no, and it said no.*

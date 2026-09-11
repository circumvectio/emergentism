---
title: "M4-01 run 2 — the four-axis encoding where all four axes denote"
id: "M4-01-RUN-2"
protocol: "08_M4_COMPRESSION_PROTOCOL_v0.1.md"
protocol_version: "0.1.0"
date: 2026-09-11
status: "[B] MEASURED — second run. Disposition of the protocol's status line is the owner's."
evidence_tier: "[B] the measurement; [A] the corpus construction and the exact cycle-payoff ground truth; [S] the kill conditions, quoted; [I] axis 4's placement rule, declared"
owner: "Yves R. Burri — K2. Source authority remains with 08_M4_COMPRESSION_PROTOCOL_v0.1.md."
may_sign: false
authority_effect: none
result_state: KILLED
supersedes_scope_of: "09_M4_COMPRESSION_RESULTS_RUN1.md — closes its 'half the chart was never tested' limitation"
---

# M4-01 run 2

`•  ⊙  ○`

## 0 · What this closes

Run 1 killed the four-axis encoding but scoped the kill honestly: on one-shot
ordinal 2×2 games, **two of the four axes had no referent at all.** A one-shot
game has one period, so no horizon; and no beliefs, models or signals, so no
represented power. Half the chart went untested and the kill said so.

**This run closes that hole.** On the complete space of deterministic memory-one
IPD strategies, all four axes denote and are computed from the strategy
specification alone.

## 1 · The corpus

**`IPD_MEMORY1_COMPLETE`, n = 32, sha256 `07dd7c46…`**

A strategy is `(opening, rule)` where the rule maps `(my_last, opp_last)` to an
action: `2⁴ = 16` rules × 2 openings = **32, complete, nothing sampled.** The §5
kill *"the corpus was selected using the desired placements or results"* cannot
fire on a complete enumeration.

Ground truth is exact, not simulated. Play between two deterministic memory-one
strategies is a deterministic walk on four states, so it cycles; the long-run
average payoff is computed from the cycle. **No simulation, no seed, no horizon
truncation artifact.** Payoffs are standard PD: `T=5 > R=3 > P=1 > S=0`, `2R > T+S`.

## 2 · The four axes, all with referents

| axis | rule on this corpus | run 1 |
|---|---|---|
| ego / collective | does the rule sustain mutual cooperation and decline to exploit a cooperator? | denoted |
| taking / giving | in how many of the four states does it cooperate? | denoted |
| **short / long horizon** | does the action depend on history at all? A constant rule is literally memoryless. | **no referent** |
| **physical / represented power** | does it condition on the **opponent's** last move — what the world did — or on **its own**, a representation of itself? | **no referent** |

Every axis is computed from the specification, never from tournament outcomes,
so **no axis can leak the target.**

> **Axis 4 is an interpretation, declared.** Reading self-conditioning as
> "represented power" is a choice, not a derivation. It is the most contestable
> decision in this run and it is stated in the open so it can be attacked.

## 3 · The measurement

Run 1's learner, imported **unchanged**, so the two runs are directly comparable.

**Primary target — `tournament_tier`** (top/middle/bottom third by round-robin score):

| representation | macro-F1 | bits |
|---|---:|---:|
| `NATIVE` — the strategy's own spec | **0.7241** | 225 |
| `LEARNED_NO_PLACEMENT` | 0.5556 | 148 |
| `ALTERNATE_TWO_AXIS` — **Axelrod's nice × provocable** | 0.4873 | **91** |
| `ONE_AXIS` | 0.4537 | **43** |
| `ADDED_AXIS` — four axes + forgiveness | 0.3889 | 319 |
| **`M4_FOUR_AXIS` — the proposal** | **0.3463** | 278 |
| *majority baseline* | *0.1818* | *0* |

**Axelrod's two descriptors from 1984 beat the proposal at one third of its code
length.**

| target | proposal | baseline | best comparator |
|---|---:|---:|---|
| `tournament_tier` | 0.3463 | 0.1818 | 0.7241 `NATIVE` |
| `nash_vs_self` | 0.4845 | 0.3962 | 0.6147 `ALTERNATE_TWO_AXIS` |
| `is_nice` | 0.4296 | 0.4286 | **1.0000** — four comparators tie |

## 4 · Verdict: `KILLED`

§4 requires beating `NATIVE`, `ONE_AXIS`, `ALTERNATE_TWO_AXIS` and
`LEARNED_NO_PLACEMENT` on the held-out target. **On the primary target it beat
none of them.** The 0.8 floor was reached on no target. A generic representation
matched or beat it at lower code length on every target.

**And the run-1 escape route is now closed.** The encoding was not failing
because half of it was untested. Given all four axes a referent, it still loses.

## 5 · What favours it, recorded rather than buried

Two results run the other way and belong in the record:

**It is not empty this time.** Run 1 put it *at* the majority baseline. Here it
is clearly above: 0.3463 against 0.1818, and 0.4845 against 0.3962. **The
encoding carries real signal. It is dominated, not vacuous** — a materially
different and better failure than run 1's.

**The added-axis kill did not fire.** Adding an independently motivated fifth
axis produced no material gain, and on the primary target made things worse.
That is weak evidence the four are not obviously missing a neighbour *in their
own terms*.

## 6 · Scope

Per §5 the chart survives as visualization, interpretive vocabulary and
hypothesis generator; it does not survive as a measured optimal code.

Two corpora now, both complete enumerations, one comparator class, one learner,
n = 78 and n = 32. Small. Axis 4's placement rule is `[I]` and contestable.
Nothing here tests policies, institutions, or any corpus with genuine incomplete
information rather than a proxy for it.

## 7 · Kills

| claim | tier | kill |
|---|---|---|
| n = 32 complete; ground truth exact from cycles | `[A]` | re-run `strategy_corpus.py`; a different hash or count kills it |
| the proposal loses to every required comparator on the primary target | `[B]` | re-run `run_m4_compression_run2.py` |
| all four axes denote here | `[S]` | show an axis whose rule is not computable from the spec |
| it carries signal, unlike run 1 | `[B]` | show the margin over baseline is within fold noise |
| axis 4's rule is an interpretation | `[I]` | derive self-conditioning as represented power from an owner |

**This document's own kill.** If it is cited as refuting the Rosetta, the
Burrisphere, or the Titan type discipline, it has been misread. It measured one
declared four-axis encoding against one comparator class on one more corpus.

---

`•  ⊙  ○` — *the second receipt, and it says no again.*

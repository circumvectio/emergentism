#!/usr/bin/env python3
"""M4-01 run 2 corpus: the complete space of deterministic memory-one IPD strategies.

WHY THIS CORPUS
---------------
Run 1 killed the four-axis encoding on one-shot ordinal 2x2 games -- but two of
the four axes had NO REFERENT there. A one-shot game has one period (no horizon)
and no beliefs, models or signals (no represented power). So half the chart went
untested, and the kill was scoped accordingly.

This corpus is chosen so that all four axes denote. A memory-one strategy for the
iterated Prisoner's Dilemma:

  * has a HORIZON in a real sense -- its action may or may not depend on history
    at all, and a rule that ignores history is literally memoryless;
  * distinguishes PHYSICAL from REPRESENTED power in a computable way -- a rule
    may condition on the OPPONENT's last move (what the world did) or on ITS OWN
    last move (a representation of itself), and these are separable;
  * still supports ego/collective and taking/giving as before.

And it remains a COMPLETE ENUMERATION, so the protocol §5 kill "the corpus was
selected using the desired placements or results" cannot fire.

CONSTRUCTION
------------
A strategy is (opening, rule) where rule maps the pair (my_last, opp_last) to an
action. Four input states, two actions: 2^4 = 16 rules. Two openings. 32
strategies, complete, no sampling.

Play between two deterministic memory-one strategies is a deterministic walk on
four states, so it enters a cycle. Long-run average payoff is computed EXACTLY
from the cycle -- no simulation noise, no random seeds, no horizon truncation
artifact.

Payoffs are the standard Prisoner's Dilemma: T=5 > R=3 > P=1 > S=0, with
2R > T+S so that mutual cooperation beats alternating exploitation.

GROUND TRUTH, computed by definition and never interpreted:
  * mean_score        -- average over a round robin against all 32 including self
  * tournament_tier   -- top / middle / bottom third by mean score
  * nash_vs_self      -- is the strategy a best response to itself in this space?
  * is_nice           -- never the first to defect against a cooperating partner

Usage:
    python3 -B strategy_corpus.py [--out corpus_ipd_memory1.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from pathlib import Path

C, D = 0, 1
PAYOFF = {(C, C): (3, 3), (C, D): (0, 5), (D, C): (5, 0), (D, D): (1, 1)}
STATES = ((C, C), (C, D), (D, C), (D, D))   # (my_last, opp_last)


def strategies():
    """All 32: a 4-bit response rule over (my_last, opp_last), plus an opening."""
    out = []
    for bits in product((C, D), repeat=4):
        for opening in (C, D):
            rule = {s: bits[i] for i, s in enumerate(STATES)}
            out.append({"opening": opening, "rule": rule, "bits": list(bits)})
    return out


def act(strategy, my_last, opp_last):
    if my_last is None:
        return strategy["opening"]
    return strategy["rule"][(my_last, opp_last)]


def exact_average(a, b):
    """Long-run average payoff for (a, b). Deterministic play cycles; use the cycle."""
    seen = {}
    history = []
    my, opp = None, None
    for step in range(64):
        move_a = act(a, my, opp)
        move_b = act(b, opp, my)
        state = (move_a, move_b)
        if state in seen:                      # cycle closed
            start = seen[state]
            cycle = history[start:]
            sa = sum(PAYOFF[s][0] for s in cycle) / len(cycle)
            sb = sum(PAYOFF[s][1] for s in cycle) / len(cycle)
            return sa, sb
        seen[state] = len(history)
        history.append(state)
        my, opp = move_a, move_b
    tail = history[-8:]
    return (sum(PAYOFF[s][0] for s in tail) / len(tail),
            sum(PAYOFF[s][1] for s in tail) / len(tail))


def is_nice(s):
    """Never the first to defect: opens C and does not defect from mutual cooperation."""
    return s["opening"] == C and s["rule"][(C, C)] == C


def build():
    pool = strategies()
    scores = []
    for a in pool:
        total = sum(exact_average(a, b)[0] for b in pool)
        scores.append(total / len(pool))

    order = sorted(range(len(pool)), key=lambda i: -scores[i])
    tier = {}
    third = len(pool) // 3
    for rank, idx in enumerate(order):
        tier[idx] = 0 if rank < third else (1 if rank < 2 * third else 2)

    rows = []
    for i, s in enumerate(pool):
        own = exact_average(s, s)[0]
        best = max(exact_average(alt, s)[0] for alt in pool)
        rows.append({
            "id": f"S{i:02d}",
            "opening": s["opening"],
            "bits": s["bits"],
            "mean_score": round(scores[i], 4),
            "tournament_tier": tier[i],
            "nash_vs_self": abs(own - best) < 1e-9,
            "is_nice": is_nice(s),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path,
                    default=Path(__file__).with_name("corpus_ipd_memory1.json"))
    args = ap.parse_args()

    games = build()
    payload = json.dumps(games, sort_keys=True, separators=(",", ":")).encode()
    sha = hashlib.sha256(payload).hexdigest()
    doc = {
        "id": "IPD_MEMORY1_COMPLETE",
        "version": "v1",
        "sha256": sha,
        "count": len(games),
        "equivalence": "none — every (opening, rule) pair is a distinct strategy and all are kept",
        "sampling_rule": "none — complete enumeration of 2^4 response rules x 2 openings",
        "exclusions": "none",
        "payoffs": "standard PD: T=5 > R=3 > P=1 > S=0, with 2R > T+S",
        "scoring": "exact long-run average over the cycle of deterministic play; no simulation, no seed",
        "citation": "Axelrod, The Evolution of Cooperation (1984); Nowak & Sigmund on memory-one strategies (1993) — external provenance of the space",
        "games": games,
    }
    args.out.write_text(json.dumps(doc, indent=1), encoding="utf-8")

    print(f"strategies (2^4 rules x 2 openings)  {len(games)}")
    print(f"corpus sha256                        {sha}")
    print("\ntournament_tier balance:")
    for k, v in sorted(Counter(g["tournament_tier"] for g in games).items()):
        print(f"  tier {k}   {v:3d}")
    print(f"\nnash_vs_self true                    {sum(g['nash_vs_self'] for g in games)}")
    print(f"nice strategies                      {sum(g['is_nice'] for g in games)}")
    top = sorted(games, key=lambda g: -g["mean_score"])[:3]
    print("\ntop by mean score:")
    for g in top:
        print(f"  {g['id']}  open={'CD'[g['opening']]}  rule={''.join('CD'[b] for b in g['bits'])}  {g['mean_score']}")
    print(f"\nwritten: {args.out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

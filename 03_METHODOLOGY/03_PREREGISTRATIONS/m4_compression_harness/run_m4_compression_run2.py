#!/usr/bin/env python3
"""M4-01 run 2 — the four-axis encoding where ALL FOUR axes have a referent.

Run 1 killed the encoding on one-shot ordinal 2x2 games, but scoped the kill
honestly: two of the four axes had no referent there, so half the chart was
never tested. This run closes that gap on the complete space of deterministic
memory-one IPD strategies, where all four denote.

THE PLACEMENT RULES, DECLARED — §5 kills a result that depends on an
undisclosed one. Every axis is computed from the STRATEGY SPECIFICATION only,
never from tournament outcomes, so no axis can leak the target.

  axis 1  ego / collective
          Does the rule sustain mutual cooperation (rule[CC] = C) and decline to
          exploit a cooperating partner (rule[DC] = C)? Scored 0-2.

  axis 2  taking / giving
          How many of the four states does it defect in? Scored 0-4 as the count
          of cooperative responses, so higher = more giving.

  axis 3  short / long horizon        <-- NO REFERENT IN RUN 1
          Does the action depend on history at all? A constant rule is literally
          memoryless: one period is all it uses. Scored as the number of distinct
          outputs the rule produces across its four inputs, 1 = memoryless.

  axis 4  physical / represented power  <-- NO REFERENT IN RUN 1
          Does the rule condition on the OPPONENT's last move -- what the world
          actually did -- or on ITS OWN last move, which is a representation of
          itself rather than an observation of the world? These are separable and
          both are computable. 0 = neither, 1 = opponent only (physical),
          2 = self only (represented), 3 = both.

  Axis 4's reading of self-conditioning as "represented power" is an
  INTERPRETATION, declared here and not derived. It is the most contestable
  choice in this run and it is stated in the open so it can be attacked.

COMPARATOR NOTE. ALTERNATE_TWO_AXIS is Axelrod's own pair -- nice (never the
first to defect) and provocable (defects in response to defection) -- the two
descriptors that organised the 1980 tournament results. Genuinely external,
genuinely two-axis, and with a stronger pedigree than the proposal.

Usage:
    python3 -B run_m4_compression_run2.py
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE / "corpus_ipd_memory1.json"
OUT = HERE / "m4_run2_result.json"

# Reuse run 1's learner UNCHANGED so the two runs are directly comparable.
_spec = importlib.util.spec_from_file_location("run1", HERE / "run_m4_compression.py")
run1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run1)

C, D = 0, 1
STATES = ((C, C), (C, D), (D, C), (D, D))   # (my_last, opp_last)

MAX_DEPTH, MAX_LEAVES, FOLDS = run1.MAX_DEPTH, run1.MAX_LEAVES, run1.FOLDS


def rule_of(row):
    return {s: row["bits"][i] for i, s in enumerate(STATES)}


# ---- the four declared axes ------------------------------------------------

def axis_ego_collective(row):
    r = rule_of(row)
    return int(r[(C, C)] == C) + int(r[(D, C)] == C)


def axis_take_give(row):
    return sum(1 for s in STATES if rule_of(row)[s] == C)


def axis_horizon(row):
    """1 = memoryless (constant rule); 2 = the action varies with history."""
    return len({rule_of(row)[s] for s in STATES})


def axis_physical_represented(row):
    r = rule_of(row)
    opp = any(r[(m, C)] != r[(m, D)] for m in (C, D))     # world-sensitive
    own = any(r[(C, o)] != r[(D, o)] for o in (C, D))     # self-sensitive
    return (1 if opp else 0) + (2 if own else 0)


def rep_m4_four_axis(row):
    return (axis_ego_collective(row), axis_take_give(row),
            axis_horizon(row), axis_physical_represented(row))


# ---- comparators -----------------------------------------------------------

def rep_native(row):
    """The strategy's own specification: opening plus the four rule bits."""
    return (row["opening"],) + tuple(row["bits"])


def is_nice(row):
    return int(row["opening"] == C and rule_of(row)[(C, C)] == C)


def is_provocable(row):
    """Defects in response to the opponent having defected."""
    r = rule_of(row)
    return int(r[(C, D)] == D or r[(D, D)] == D)


def rep_alternate_two_axis(row):
    """Axelrod's own pair: nice x provocable."""
    return (is_nice(row), is_provocable(row))


def is_forgiving(row):
    """Returns to cooperation from mutual defection."""
    return int(rule_of(row)[(D, D)] == C)


def rep_added_axis(row):
    return rep_m4_four_axis(row) + (is_forgiving(row),)


def candidate_features(row):
    r = rule_of(row)
    feats = {
        "ego_collective": axis_ego_collective(row),
        "take_give": axis_take_give(row),
        "horizon": axis_horizon(row),
        "phys_repr": axis_physical_represented(row),
        "nice": is_nice(row),
        "provocable": is_provocable(row),
        "forgiving": is_forgiving(row),
        "opening": row["opening"],
    }
    for i, s in enumerate(STATES):
        feats[f"bit_{'CD'[s[0]]}{'CD'[s[1]]}"] = r[s]
    return feats


REPS = OrderedDict([
    ("M4_FOUR_AXIS", (rep_m4_four_axis, 0)),      # no missing placements this time
    ("NATIVE", (rep_native, 0)),
    ("ALTERNATE_TWO_AXIS", (rep_alternate_two_axis, 0)),
    ("ADDED_AXIS", (rep_added_axis, 0)),
])


def stratified_folds(rows, k, target):
    folds = [[] for _ in range(k)]
    by_class = {}
    for g in sorted(rows, key=lambda x: x["id"]):
        by_class.setdefault(g[target], []).append(g)
    for _, members in sorted(by_class.items(), key=lambda kv: str(kv[0])):
        for i, g in enumerate(members):
            folds[i % k].append(g)
    return folds


def evaluate(rows, encode, target, missing=0):
    folds = stratified_folds(rows, FOLDS, target)
    f1s, lengths, truth, pred = [], [], [], []
    for i in range(FOLDS):
        test = folds[i]
        train = [g for j, f in enumerate(folds) if j != i for g in f]
        if not test or not train:
            continue
        Xtr = [encode(g) for g in train]
        ytr = [g[target] for g in train]
        Xte = [encode(g) for g in test]
        yte = [g[target] for g in test]
        tree, leaves = run1.grow(Xtr, ytr, 0, MAX_LEAVES)
        p = [run1.predict(tree, x) for x in Xte]
        f1s.append(run1.macro_f1(yte, p))
        truth += yte
        pred += p
        lengths.append(run1.code_length_bits(Xtr + Xte, max(leaves - 1, 1),
                                             len(Xtr[0]), missing))
    return {
        "macro_f1_mean": round(sum(f1s) / len(f1s), 4),
        "macro_f1_min": round(min(f1s), 4),
        "macro_f1_max": round(max(f1s), 4),
        "accuracy": round(sum(1 for t, p in zip(truth, pred) if t == p) / len(truth), 4),
        "code_length_bits": round(sum(lengths) / len(lengths), 1),
    }


def select_on_dev(rows, n, target):
    folds = stratified_folds(rows, FOLDS, target)
    dev = [g for f in folds[:-2] for g in f]
    names = sorted(candidate_features(dev[0]))
    labels = [g[target] for g in dev]
    base = run1.entropy(labels)
    scored = []
    for name in names:
        col = [candidate_features(g)[name] for g in dev]
        rem = 0.0
        for v in set(col):
            sub = [labels[i] for i, x in enumerate(col) if x == v]
            rem += len(sub) / len(col) * run1.entropy(sub)
        scored.append((-(base - rem), name))
    scored.sort()
    return [n for _, n in scored[:n]]


def main() -> int:
    doc = json.loads(CORPUS.read_text())
    rows = doc["games"]

    all_results = {}
    for target in ("tournament_tier", "nash_vs_self", "is_nice"):
        bal = Counter(g[target] for g in rows)
        if len(bal) < 2:
            continue
        maj = bal.most_common(1)[0][0]
        baseline = run1.macro_f1([g[target] for g in rows], [maj] * len(rows))

        res = {}
        for name, (fn, miss) in REPS.items():
            res[name] = evaluate(rows, fn, target, miss)
        one = select_on_dev(rows, 1, target)
        res["ONE_AXIS"] = evaluate(rows, lambda g, k=one: tuple(candidate_features(g)[x] for x in k), target)
        res["ONE_AXIS"]["selected"] = one
        lr = select_on_dev(rows, 2, target)
        res["LEARNED_NO_PLACEMENT"] = evaluate(rows, lambda g, k=lr: tuple(candidate_features(g)[x] for x in k), target)
        res["LEARNED_NO_PLACEMENT"]["selected"] = lr
        res["MAJORITY_BASELINE"] = {"macro_f1_mean": round(baseline, 4),
                                    "accuracy": round(bal[maj] / len(rows), 4),
                                    "code_length_bits": 0.0}
        all_results[target] = res

        print(f"\n### target={target}   balance={dict(bal)}   majority-macroF1={baseline:.4f}")
        for n, r in sorted(res.items(), key=lambda kv: -kv[1]["macro_f1_mean"]):
            flag = "  <-- proposal" if n == "M4_FOUR_AXIS" else ""
            sel = f"  {r['selected']}" if "selected" in r else ""
            print(f"   {n:<22} F1={r['macro_f1_mean']:.4f}  acc={r['accuracy']:.3f}"
                  f"  bits={r['code_length_bits']:>7.0f}{flag}{sel}")

    OUT.write_text(json.dumps({
        "corpus": {k: doc[k] for k in ("id", "version", "sha256", "count", "sampling_rule")},
        "axes_all_denote": True,
        "learner": {"kind": "depth-limited decision tree (imported unchanged from run 1)",
                    "max_depth": MAX_DEPTH, "max_leaves": MAX_LEAVES, "folds": FOLDS},
        "results": all_results,
    }, indent=1), encoding="utf-8")
    print(f"\nwritten: {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

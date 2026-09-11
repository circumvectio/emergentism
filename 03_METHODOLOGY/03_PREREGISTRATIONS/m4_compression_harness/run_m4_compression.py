#!/usr/bin/env python3
"""M4-01 run: score the four-axis encoding against the frozen comparator class.

This is the first measurement ever taken with this instrument. Everything it
needs is declared here in code, so the run is reproducible from the file.

WHAT IS BEING TESTED
--------------------
`08_M4_COMPRESSION_PROTOCOL_v0.1.md` §1: whether the four declared strategic
contrasts -- ego/collective, taking/giving, physical/represented power,
short/long horizon -- "preserve more decision-relevant structure per unit
description than frozen comparators."

The protocol is explicit that "M4" here is a protocol label, NOT the M4 move-set
of the Rosetta, and NOT a claim that four metaphysical dimensions exist.

THE PLACEMENT RULES ARE DECLARED, BECAUSE HIDING THEM IS A NAMED KILL
---------------------------------------------------------------------
§5: kill if "results depend materially on an undisclosed placement rule." So
every axis states its rule, including the two that have none:

  axis 1  ego/collective   -- is a player's best cell also the joint-rank
                              maximiser? Declared, computable.
  axis 2  taking/giving    -- at a player's best cell, does the opponent get a
                              high or low rank? Declared, computable.
  axis 3  physical/repr.   -- NO REFERENT. A one-shot ordinal game carries no
                              beliefs, models, signals or information structure,
                              so there is nothing for "represented power" to
                              denote. Any assignment would be exactly the
                              undisclosed rule §5 kills. Recorded as a MISSING
                              PLACEMENT and costed, per the schema's own
                              `missing_placement_costed: true`.
  axis 4  short/long       -- NO REFERENT. A one-shot game has one period.
                              Same treatment.

Reporting two of four axes as unassignable is a result, not an evasion. The
protocol anticipated missing placements and required them to be priced.

FAIRNESS
--------
Every representation is reduced to small-cardinality categorical features, run
through the SAME depth-limited decision tree with the same depth and leaf
budget, over the SAME deterministic stratified folds. ONE_AXIS and
LEARNED_NO_PLACEMENT select their features on development folds only.

Usage:
    python3 -B run_m4_compression.py
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE / "corpus_2x2_ordinal.json"
OUT = HERE / "m4_run_result.json"
INSTANCE = HERE / "M4Compression.v1.instance.json"

TARGET = "pure_ne_count"     # 0, 1 or 2 pure-strategy Nash equilibria
MAX_DEPTH = 3                # identical for every representation
MAX_LEAVES = 8               # identical for every representation
FOLDS = 6                    # deterministic stratified folds


# --------------------------------------------------------------------------
# feature helpers over a game matrix m[row][col] = (row_rank, col_rank)
# --------------------------------------------------------------------------

def matrix(game):
    m = game["matrix"]
    return ((tuple(m[0][0]), tuple(m[0][1])), (tuple(m[1][0]), tuple(m[1][1])))


CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))


def best_cell(m, player):
    return max(CELLS, key=lambda rc: m[rc[0]][rc[1]][player])


def joint_max_cell(m):
    return max(CELLS, key=lambda rc: m[rc[0]][rc[1]][0] + m[rc[0]][rc[1]][1])


def axis_ego_collective(m):
    """Per player: is your best cell the joint-rank maximiser? 0=both ego … 2=both collective."""
    jm = joint_max_cell(m)
    return sum(1 for p in (0, 1) if best_cell(m, p) == jm)


def axis_take_give(m):
    """Per player: at your best cell, does the opponent get rank >= 3? 0=both take … 2=both give."""
    out = 0
    for p in (0, 1):
        rc = best_cell(m, p)
        if m[rc[0]][rc[1]][1 - p] >= 3:
            out += 1
    return out


def dominance_count(m):
    """How many players hold a dominant strategy (0, 1 or 2). Classic descriptor."""
    n = 0
    for mine in (0, 1):
        if all(m[0][c][0] > m[1][c][0] for c in (0, 1)) or all(m[1][c][0] > m[0][c][0] for c in (0, 1)):
            n += 1
            break
    for _ in (0,):
        if all(m[r][0][1] > m[r][1][1] for r in (0, 1)) or all(m[r][1][1] > m[r][0][1] for r in (0, 1)):
            n += 1
    return n


def conflict_index(m):
    """Sign of the rank covariance between the players across the four cells.

    A standard, non-Emergentist descriptor: do the two players' preferences run
    together (coordination-like) or against each other (conflict-like)?
    """
    rows = [m[r][c][0] for r, c in CELLS]
    cols = [m[r][c][1] for r, c in CELLS]
    mr = sum(rows) / 4
    mc = sum(cols) / 4
    cov = sum((a - mr) * (b - mc) for a, b in zip(rows, cols))
    return 0 if cov < -1e-9 else (1 if abs(cov) <= 1e-9 else 2)


MISSING = -1  # the costed symbol for an axis with no referent


def rep_m4_four_axis(m):
    """The proposal. Axes 3 and 4 have no referent here and are costed as missing."""
    return (axis_ego_collective(m), axis_take_give(m), MISSING, MISSING)


def rep_m4_two_live(m):
    """The proposal's two axes that DO have a referent, with no missing-placement cost.

    Not a protocol comparator — reported alongside so the missing-placement
    penalty can be separated from the axes' actual signal.
    """
    return (axis_ego_collective(m), axis_take_give(m))


def rep_native(m):
    """The corpus's own standard representation: the eight ordinal ranks."""
    return tuple(m[r][c][p] for r, c in CELLS for p in (0, 1))


def rep_alternate_two_axis(m):
    """Non-Emergentist two-axis: dominance structure x conflict sign."""
    return (dominance_count(m), conflict_index(m))


def rep_added_axis(m):
    """The proposal plus one independently motivated axis (dominance structure)."""
    return rep_m4_four_axis(m) + (dominance_count(m),)


# candidate pool for ONE_AXIS and LEARNED_NO_PLACEMENT — mechanical, no chart
def candidate_features(m):
    feats = {
        "ego_collective": axis_ego_collective(m),
        "take_give": axis_take_give(m),
        "dominance": dominance_count(m),
        "conflict": conflict_index(m),
    }
    # all pairwise rank comparisons inside the matrix: purely mechanical
    flat = [(f"{'RC'[p]}{r}{c}", m[r][c][p]) for r, c in CELLS for p in (0, 1)]
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            feats[f"cmp_{flat[i][0]}_{flat[j][0]}"] = int(flat[i][1] > flat[j][1])
    return feats


# --------------------------------------------------------------------------
# a small deterministic decision tree — identical learner for every rep
# --------------------------------------------------------------------------

def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in Counter(labels).values() if c)


def grow(rows, labels, depth, leaves_left):
    """rows: list of feature tuples. Returns a tree; deterministic tie-breaking."""
    majority = Counter(labels).most_common()
    majority.sort(key=lambda kv: (-kv[1], kv[0]))
    leaf = ("leaf", majority[0][0])
    if depth >= MAX_DEPTH or leaves_left <= 1 or len(set(labels)) <= 1:
        return leaf, 1

    base = entropy(labels)
    best = None
    n_feat = len(rows[0]) if rows else 0
    for f in range(n_feat):
        values = sorted({r[f] for r in rows})
        for v in values[:-1] if len(values) > 1 else []:
            li = [i for i, r in enumerate(rows) if r[f] <= v]
            ri = [i for i, r in enumerate(rows) if r[f] > v]
            if not li or not ri:
                continue
            ll = [labels[i] for i in li]
            rl = [labels[i] for i in ri]
            gain = base - (len(ll) * entropy(ll) + len(rl) * entropy(rl)) / len(labels)
            key = (-gain, f, v)
            if best is None or key < best[0]:
                best = (key, f, v, li, ri)
    if best is None or -best[0][0] <= 1e-12:
        return leaf, 1

    _, f, v, li, ri = best
    left, nl = grow([rows[i] for i in li], [labels[i] for i in li], depth + 1, leaves_left - 1)
    right, nr = grow([rows[i] for i in ri], [labels[i] for i in ri], depth + 1, leaves_left - nl)
    return ("node", f, v, left, right), nl + nr


def predict(tree, row):
    while tree[0] == "node":
        _, f, v, left, right = tree
        tree = left if row[f] <= v else right
    return tree[1]


def macro_f1(truth, pred):
    classes = sorted(set(truth) | set(pred))
    scores = []
    for c in classes:
        tp = sum(1 for t, p in zip(truth, pred) if t == c and p == c)
        fp = sum(1 for t, p in zip(truth, pred) if t != c and p == c)
        fn = sum(1 for t, p in zip(truth, pred) if t == c and p != c)
        if tp == 0:
            scores.append(0.0)
        else:
            prec, rec = tp / (tp + fp), tp / (tp + fn)
            scores.append(2 * prec * rec / (prec + rec))
    return sum(scores) / len(scores) if scores else 0.0


# --------------------------------------------------------------------------
# code length in bits
# --------------------------------------------------------------------------

def code_length_bits(rows, n_nodes, n_features, missing_slots):
    """Dictionary + data + model, all in bits. Missing placements are priced.

    data       : per game, sum over features of log2(cardinality)
    dictionary : per feature, 6 bits to name it out of a 64-slot declared pool
    model      : per internal node, feature index + threshold + structure
    missing    : a missing placement still occupies a slot and must be encoded
                 as one symbol of its axis's full declared cardinality (3)
    """
    if not rows:
        return 0.0
    card = [len({r[f] for r in rows}) or 1 for f in range(len(rows[0]))]
    per_game = sum(math.log2(c) for c in card if c > 0)
    data = per_game * len(rows)
    dictionary = 6.0 * n_features
    model = n_nodes * (math.log2(max(n_features, 2)) + 3.0 + 1.0)
    missing = missing_slots * len(rows) * math.log2(3)
    return data + dictionary + model + missing


# --------------------------------------------------------------------------
# folds
# --------------------------------------------------------------------------

def stratified_folds(games, k):
    """Deterministic: within each class, assign by position in id order."""
    folds = [[] for _ in range(k)]
    by_class = {}
    for g in sorted(games, key=lambda x: x["id"]):
        by_class.setdefault(g[TARGET], []).append(g)
    for _, members in sorted(by_class.items()):
        for i, g in enumerate(members):
            folds[i % k].append(g)
    return folds


REPS = {
    "M4_FOUR_AXIS": (rep_m4_four_axis, 2),
    "M4_TWO_LIVE_AXES": (rep_m4_two_live, 0),
    "NATIVE": (rep_native, 0),
    "ALTERNATE_TWO_AXIS": (rep_alternate_two_axis, 0),
    "ADDED_AXIS": (rep_added_axis, 2),
}


def evaluate(games, encode, missing_slots):
    folds = stratified_folds(games, FOLDS)
    f1s, lengths, truth_all, pred_all = [], [], [], []
    for i in range(FOLDS):
        test = folds[i]
        train = [g for j, f in enumerate(folds) if j != i for g in f]
        Xtr = [encode(matrix(g)) for g in train]
        ytr = [g[TARGET] for g in train]
        Xte = [encode(matrix(g)) for g in test]
        yte = [g[TARGET] for g in test]
        tree, n_leaves = grow(Xtr, ytr, 0, MAX_LEAVES)
        preds = [predict(tree, x) for x in Xte]
        f1s.append(macro_f1(yte, preds))
        truth_all += yte
        pred_all += preds
        lengths.append(code_length_bits(Xtr + Xte, max(n_leaves - 1, 1),
                                        len(Xtr[0]), missing_slots))
    return {
        "macro_f1_mean": round(sum(f1s) / len(f1s), 4),
        "macro_f1_min": round(min(f1s), 4),
        "macro_f1_max": round(max(f1s), 4),
        "pooled_macro_f1": round(macro_f1(truth_all, pred_all), 4),
        "accuracy": round(sum(1 for t, p in zip(truth_all, pred_all) if t == p) / len(truth_all), 4),
        "code_length_bits": round(sum(lengths) / len(lengths), 1),
    }


def select_on_dev(games, pool_fn, n_features):
    """Pick the n best candidate features using DEVELOPMENT folds only."""
    folds = stratified_folds(games, FOLDS)
    dev = [g for f in folds[:-2] for g in f]           # never touches the last two folds
    names = sorted(pool_fn(matrix(dev[0])))
    labels = [g[TARGET] for g in dev]
    scored = []
    for name in names:
        col = [pool_fn(matrix(g))[name] for g in dev]
        base = entropy(labels)
        rem = 0.0
        for v in set(col):
            sub = [labels[i] for i, x in enumerate(col) if x == v]
            rem += len(sub) / len(col) * entropy(sub)
        scored.append((-(base - rem), name))
    scored.sort()
    return [n for _, n in scored[:n_features]]


def main() -> int:
    doc = json.loads(CORPUS.read_text())
    games = doc["games"]

    results = {}
    for name, (fn, missing) in REPS.items():
        results[name] = evaluate(games, fn, missing)

    one = select_on_dev(games, candidate_features, 1)
    results["ONE_AXIS"] = evaluate(
        games, lambda m, k=one: tuple(candidate_features(m)[x] for x in k), 0)
    results["ONE_AXIS"]["selected"] = one

    learned = select_on_dev(games, candidate_features, 2)
    results["LEARNED_NO_PLACEMENT"] = evaluate(
        games, lambda m, k=learned: tuple(candidate_features(m)[x] for x in k), 0)
    results["LEARNED_NO_PLACEMENT"]["selected"] = learned

    majority = Counter(g[TARGET] for g in games).most_common(1)[0][0]
    results["MAJORITY_BASELINE"] = {
        "macro_f1_mean": round(macro_f1([g[TARGET] for g in games],
                                        [majority] * len(games)), 4),
        "accuracy": round(sum(1 for g in games if g[TARGET] == majority) / len(games), 4),
        "code_length_bits": 0.0,
    }

    OUT.write_text(json.dumps({
        "corpus": {k: doc[k] for k in ("id", "version", "sha256", "count", "sampling_rule")},
        "target": TARGET,
        "learner": {"kind": "depth-limited decision tree", "max_depth": MAX_DEPTH,
                    "max_leaves": MAX_LEAVES, "folds": FOLDS,
                    "identical_for_every_representation": True},
        "results": results,
    }, indent=1), encoding="utf-8")

    width = max(len(k) for k in results)
    print(f"corpus {doc['id']} n={doc['count']}  target={TARGET}  sha={doc['sha256'][:12]}…\n")
    print(f"{'representation'.ljust(width)}  macroF1  (min–max)      acc    bits")
    order = sorted(results, key=lambda k: -results[k]["macro_f1_mean"])
    for k in order:
        r = results[k]
        rng = f"({r.get('macro_f1_min', 0):.2f}–{r.get('macro_f1_max', 0):.2f})" if "macro_f1_min" in r else " " * 13
        print(f"{k.ljust(width)}   {r['macro_f1_mean']:.4f}  {rng}  {r['accuracy']:.3f}  {r['code_length_bits']:>8.0f}")
    print(f"\nONE_AXIS selected            {results['ONE_AXIS']['selected']}")
    print(f"LEARNED_NO_PLACEMENT selected {results['LEARNED_NO_PLACEMENT']['selected']}")
    print(f"\nwritten: {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

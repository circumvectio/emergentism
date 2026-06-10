#!/usr/bin/env python3
"""
R9 v2 -- the haystack / propagule model (proper multilevel selection).

R9 v1 was VOID: fixed deme sizes meant mutualist and parasite demes contributed
equally to the next generation, so there was NO differential group productivity
and hence NO group selection -- each isolated deme just replayed R8 and went
parasite. That is a structural omission, not a refutation. (Logged per A7.)

v2 implements the standard mechanism group selection actually requires
(Maynard Smith's haystack model; Wilson trait-group; the Price equation
decomposition into within- and between-group components):

  1. A global pool of strategies (p in [0,1]; p=0 mutualist/symbiont, p=1 parasite).
  2. FOUNDING: partition the pool into M demes of FOUNDER SIZE F, by random
     sampling. Small F -> high between-group variance in parasite fraction
     (some demes are founded mostly-mutualist by chance). This is the realistic
     route to new individuality: a holobiont founds from a few symbionts with
     vertical transmission.
  3. ECOLOGY: each deme runs the R8 substrate ecology for T_eco steps. Parasites
     free-ride and out-earn their dememates WITHIN a deme; but mutualist-founded
     demes keep their substrate clean and are far more PRODUCTIVE in total.
  4. DISPERSAL: the next pool is sampled across ALL agents proportional to
     individual fitness (so high-productivity mutualist demes contribute more
     total offspring), with mutation. Re-found and repeat.

Total population is held ~constant while founder size F is swept, so F isolates
group size: M = P_TOT / F. The Price equation says mutualism wins when the
between-group selection (favoring productive mutualist demes) beats within-group
selection (favoring parasites), which happens at small F (high between-group
variance).

REGISTERED PREDICTIONS (2026-06-10, pre-run):
  P1: small founder size F -> mutualism persists/dominates (the holobiont regime);
      large F -> parasites fixate (well-mixed / R8). A critical F* between.
  P2: the holobiont claim -- in the mutualist regime, demes are stable
      high-productivity symbiont baskets; parasite-founded demes self-terminate
      (low productivity, few descendants).
  P3: system productivity is far higher in the small-F (holobiont) regime.
  FALSIFIER: if parasites fixate at EVERY founder size including F=2, the
      holobiont/multilevel claim fails in this model -- report it plainly.

Stdlib only. Deterministic given SEEDS.
"""

import random
import statistics

P_TOT = 600
GENERATIONS = 30
T_ECO = 250
DRIFT = 0.006
DEATH = 0.0
START_LO, START_HI = 0.35, 0.95
B_REG = 0.5
E_ENTROPY = 0.020
KAPPA = 0.30
REGEN_BASE = 0.012
G0 = 1.0
RHO = 0.020
DEPLETE = 0.9
MUT_RATE = 0.05
MUT_STEP = 0.20
FOUNDER_SIZES = (2, 4, 8, 20, 60)
SEEDS = range(6)


def run_deme_eco(p_vals, rng):
    n = len(p_vals)
    h = [rng.uniform(START_LO, START_HI) for _ in range(n)]
    g = G0
    alive = [True] * n
    fit = [0.0] * n
    for t in range(T_ECO):
        g = min(G0, g + RHO * (G0 - g))
        any_alive = False
        pollution = 0.0
        for i in range(n):
            if not alive[i]:
                continue
            any_alive = True
            h[i] -= DRIFT
            if h[i] > B_REG:
                h[i] += REGEN_BASE * (g / G0)
            p = p_vals[i]
            h[i] -= KAPPA * (1.0 - p) * E_ENTROPY
            pollution += p * E_ENTROPY * DEPLETE
        g = max(0.0, g - pollution / max(n, 1))
        if not any_alive:
            break
        for i in range(n):
            if alive[i] and h[i] > DEATH:
                fit[i] += max(0.0, h[i])
            elif alive[i]:
                alive[i] = False
    return fit


def fitness_sample(strategies, weights, k, rng):
    """Sample k strategies proportional to weights (with replacement), mutated."""
    total = sum(weights)
    out = []
    if total <= 0:
        for _ in range(k):
            out.append(rng.choice(strategies))
    else:
        cum = []
        acc = 0.0
        for w in weights:
            acc += w
            cum.append(acc)
        import bisect
        for _ in range(k):
            r = rng.random() * total
            idx = bisect.bisect_left(cum, r)
            idx = min(idx, len(strategies) - 1)
            out.append(strategies[idx])
    # mutate
    res = []
    for p in out:
        if rng.random() < MUT_RATE:
            p = min(1.0, max(0.0, p + rng.choice([-1, 1]) * MUT_STEP))
        res.append(p)
    return res


def run(founder, seed, init_parasite_frac=0.5):
    rng = random.Random(seed)
    pool = [1.0 if rng.random() < init_parasite_frac else 0.0 for _ in range(P_TOT)]
    history = []
    last_holo = last_sys = 0
    for gen in range(GENERATIONS):
        rng.shuffle(pool)
        n_demes = max(1, P_TOT // founder)
        demes = [pool[d * founder:(d + 1) * founder] for d in range(n_demes)]
        demes = [dm for dm in demes if dm]

        all_strat, all_fit = [], []
        holo = 0
        sys_fit = 0.0
        for dm in demes:
            fit = run_deme_eco(dm, rng)
            all_strat.extend(dm)
            all_fit.extend(fit)
            sys_fit += sum(fit)
            if statistics.mean(dm) < 0.30 and statistics.mean(fit) > 50:
                holo += 1
        history.append(statistics.mean(all_strat))
        last_holo = holo / len(demes)
        last_sys = sys_fit

        pool = fitness_sample(all_strat, all_fit, P_TOT, rng)

    return statistics.mean(pool), last_holo, last_sys, history


if __name__ == "__main__":
    print(f"P_TOT={P_TOT} generations={GENERATIONS} eco_steps={T_ECO} kappa={KAPPA} "
          f"deplete={DEPLETE} mut={MUT_RATE} seeds={len(list(SEEDS))}")
    print("Haystack model. F = founder size (small F = high between-group variance). "
          "p=0 symbiont, p=1 parasite.\n")
    print(f"{'founder F':9s} {'n_demes':>8s} | {'final mean p':>12s} | "
          f"{'holobiont frac':>14s} | {'sys productivity':>16s} | outcome")
    print("-" * 86)
    for F in FOUNDER_SIZES:
        rows = [run(F, s) for s in SEEDS]
        mp = statistics.mean(r[0] for r in rows)
        holo = statistics.mean(r[1] for r in rows)
        sysf = statistics.mean(r[2] for r in rows)
        outcome = ("SYMBIONT/holobiont" if mp < 0.4 else
                   "parasite (self-consuming)" if mp > 0.6 else "mixed/contested")
        print(f"{F:9d} {P_TOT // F:8d} | {mp:12.2f} | {holo:13.1%} | {sysf:16.0f} | {outcome}")

    print("\n=== mean parasitism trajectory (smallest founder F) ===")
    _, _, _, hist = run(FOUNDER_SIZES[0], 0)
    step = max(1, GENERATIONS // 12)
    print("gen: " + " ".join(f"{k:5d}" for k in range(0, GENERATIONS, step)))
    print("p̄ : " + " ".join(f"{hist[k]:5.2f}" for k in range(0, GENERATIONS, step)))
    print("\nP1 small F -> mutualism wins | P2 holobionts persist, parasite demes self-terminate | "
          "P3 small F -> higher system productivity")

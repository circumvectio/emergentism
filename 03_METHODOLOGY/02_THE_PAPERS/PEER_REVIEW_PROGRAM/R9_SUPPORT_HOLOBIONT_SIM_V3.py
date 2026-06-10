#!/usr/bin/env python3
"""
R9 v3 -- the haystack model PLUS within-deme policing (the missing ingredient).

R9 v2 (correctly built haystack group selection) showed group structure ALONE
does NOT save mutualism: parasites fixate even at founder size 2, because
within-group selection refills parasites faster than differential group
extinction purges parasite demes. This is the mainstream result (Maynard Smith &
Szathmary: every major evolutionary transition required SUPPRESSION OF
WITHIN-UNIT COMPETITION -- policing, not group structure alone).

v3 adds exactly that suppression: within each deme, low-p agents (cooperators /
the would-be holobiont's immune system) pay a tax to reduce high-p agents'
health -- the corpus's licensed, fenced 'demon' operators / an immune response /
Frank's policing. This is the same mechanism R7's PUNISH condition used, ported
into the group-structured (haystack) model to test it through an INDEPENDENT
channel.

TESTED CLAIM (not "mutualism wins" -- the corpus's architectural claim):
  policing is the ingredient that converts a basket of symbionts into a stable
  holobiont. Group structure provides the between-group variance; policing
  suppresses the within-group parasite advantage; together they should let the
  holobiont form where neither did alone.

REGISTERED PREDICTIONS (2026-06-10, pre-run):
  P1: with policing, small-founder demes become stable mutualist holobionts
      (mean p low, high productivity); the effect is strongest at small F.
  P2: policing carries a cost -- system productivity is somewhat lower than the
      (unreachable) policing-free mutualist ideal, echoing R7 F16 (the fences
      cost welfare but prevent collapse).
  FALSIFIER: if parasites fixate even WITH policing at every founder size, then
      the corpus's enforcement claim fails through this channel -- a real problem,
      reported plainly. (R7 already supports enforcement via reciprocity, so a
      failure here would mean the result is mechanism-specific, itself worth knowing.)

Stdlib only. Deterministic given SEEDS.
"""

import bisect
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
POLICE_TAX = 0.0008      # cost a cooperator pays per step to police
POLICE_HIT = 0.004       # health removed from a high-p target per policing event
POLICE_THRESH = 0.5      # agents with p above this are policed
FOUNDER_SIZES = (2, 4, 8, 20, 60)
SEEDS = range(6)


def run_deme_eco(p_vals, rng, policing):
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

        # within-deme policing: cooperators tax themselves to harm parasites
        if policing and any_alive:
            police_targets = [i for i in range(n) if alive[i] and p_vals[i] > POLICE_THRESH]
            police_agents = [i for i in range(n) if alive[i] and p_vals[i] <= POLICE_THRESH]
            if police_targets and police_agents:
                for i in police_agents:
                    h[i] -= POLICE_TAX
                for j in police_targets:
                    h[j] -= POLICE_HIT * len(police_agents) / max(len(police_targets), 1)

        if not any_alive:
            break
        for i in range(n):
            if alive[i] and h[i] > DEATH:
                fit[i] += max(0.0, h[i])
            elif alive[i]:
                alive[i] = False
    return fit


def fitness_sample(strategies, weights, k, rng):
    total = sum(weights)
    out = []
    if total <= 0:
        return [rng.choice(strategies) for _ in range(k)]
    cum, acc = [], 0.0
    for w in weights:
        acc += w
        cum.append(acc)
    for _ in range(k):
        r = rng.random() * total
        idx = min(bisect.bisect_left(cum, r), len(strategies) - 1)
        p = strategies[idx]
        if rng.random() < MUT_RATE:
            p = min(1.0, max(0.0, p + rng.choice([-1, 1]) * MUT_STEP))
        out.append(p)
    return out


def run(founder, seed, policing, init_parasite_frac=0.5):
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
        holo, sys_fit = 0, 0.0
        for dm in demes:
            fit = run_deme_eco(dm, rng, policing)
            all_strat.extend(dm)
            all_fit.extend(fit)
            sys_fit += sum(fit)
            if statistics.mean(dm) < 0.30 and statistics.mean(fit) > 50:
                holo += 1
        history.append(statistics.mean(all_strat))
        last_holo, last_sys = holo / len(demes), sys_fit
        pool = fitness_sample(all_strat, all_fit, P_TOT, rng)
    return statistics.mean(pool), last_holo, last_sys, history


if __name__ == "__main__":
    print(f"P_TOT={P_TOT} gen={GENERATIONS} eco={T_ECO} police_tax={POLICE_TAX} "
          f"police_hit={POLICE_HIT} seeds={len(list(SEEDS))}")
    print("Haystack + within-deme policing (immune response / fenced demons). "
          "p=0 symbiont, p=1 parasite.\n")
    print(f"{'founder F':9s} {'policing':9s} | {'final mean p':>12s} | "
          f"{'holobiont frac':>14s} | {'sys productivity':>16s} | outcome")
    print("-" * 90)
    for police in (False, True):
        for F in FOUNDER_SIZES:
            rows = [run(F, s, police) for s in SEEDS]
            mp = statistics.mean(r[0] for r in rows)
            holo = statistics.mean(r[1] for r in rows)
            sysf = statistics.mean(r[2] for r in rows)
            outcome = ("SYMBIONT/holobiont" if mp < 0.4 else
                       "parasite (self-consuming)" if mp > 0.6 else "mixed/contested")
            tag = "ON " if police else "off"
            print(f"{F:9d} {tag:>9s} | {mp:12.2f} | {holo:13.1%} | {sysf:16.0f} | {outcome}")
        print("-" * 90)
    print("P1 policing+small F -> holobiont forms | P2 policing costs some productivity | "
          "FALSIFIER: parasites fixate even with policing")

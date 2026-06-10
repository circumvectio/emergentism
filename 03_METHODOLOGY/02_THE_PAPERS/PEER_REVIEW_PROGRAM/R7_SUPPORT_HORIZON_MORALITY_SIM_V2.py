#!/usr/bin/env python3
"""
R7 v2 -- rescuing the conjecture with the corpus's own reciprocity machinery.

R7 v1 result: long horizon + shared-fate coupling was NOT enough -- defectors
free-ride on the public good and win selection. Claim 4 as literally stated
("pure self-interest + long horizon -> morality") is FALSE for a pure public good.

The rigorous fix (Axelrod; Nowak's 5 rules for cooperation; Fehr-Gachter costly
punishment) is RECIPROCITY / ASSORTMENT / PUNISHMENT. The corpus already contains
exactly this: K* (reciprocate; do not extract from cooperators) and the licensed
immune response (the 'demon' operators permitted ONLY against defectors). So this
version adds a single knob -- ALLOCATION -- testing whether the corpus's own
conditional machinery rescues the conjecture:

  PUBLIC     : pool shared among the neediest of ALL living agents (v1; free-ridable)
  RECIPROCAL : pool shared among the neediest CONTRIBUTORS only (cooperators).
               This is K*/eta=0 made concrete -- you receive if you give. Defectors
               are excluded from the club good (assortment), not actively harmed.
  PUNISH     : RECIPROCAL plus a costly-punishment term -- cooperators each pay a
               small tax to reduce nearby defectors' health (Fehr-Gachter; the
               corpus's licensed immune response / 'Kali as tit-for-tat').

Same 2x2 of {SHORT, LONG} x {ISOLATED, COUPLED}, now x {PUBLIC, RECIPROCAL, PUNISH}.

REGISTERED PREDICTIONS (2026-06-10, pre-run):
  P4: Under RECIPROCAL + LONG horizon, cooperators finally win selection and
      out-earn defectors -> the conjecture is RESCUED, but the true precondition
      is long horizon AND reciprocity (assortment), not long horizon alone.
  P5: PUNISH widens the cooperator advantage further (and may win even where
      RECIPROCAL ties), at a cost to total welfare (punishment burns health) --
      explaining why the corpus LICENSES the demon-operators rather than banning
      them: conditional retaliation is what makes the gods evolutionarily stable.
  P6: SHORT horizon still favors defectors regardless of allocation -- no
      reciprocity mechanism rescues cooperation when the future never arrives.

Stdlib only. Deterministic given SEEDS.
"""

import random
import statistics

N = 200
T = 800
DRIFT = 0.004
DEATH = 0.0
START_LO, START_HI = 0.25, 0.95
COST = 0.010
B_REG = 0.5
REGEN_BASE = 0.010
PUNISH_TAX = 0.004        # cost a cooperator pays to punish
PUNISH_HIT = 0.012        # health removed from a targeted defector
HORIZONS = {"SHORT": 0.0, "LONG": REGEN_BASE}
COUPLINGS = {"ISOLATED": 0.0, "COUPLED": 1.5}
ALLOCATIONS = ("PUBLIC", "RECIPROCAL", "PUNISH")
POOL_TARGETS = 10
SEEDS = range(16)


def run(beta, regen_base, alloc, seed, coop_frac=0.5):
    rng = random.Random(seed)
    h = [rng.uniform(START_LO, START_HI) for _ in range(N)]
    is_coop = [i < int(coop_frac * N) for i in range(N)]
    rng.shuffle(is_coop)
    alive = [True] * N
    lifetime_w = [0.0] * N
    born_coop = sum(is_coop)
    born_def = N - born_coop

    for t in range(T):
        living = [i for i in range(N) if alive[i]]
        if not living:
            break
        frac = len(living) / N

        for i in living:
            h[i] -= DRIFT
            if h[i] > B_REG:
                h[i] += regen_base * (frac ** beta)

        # cooperators contribute
        pool = 0.0
        contributors = []
        for i in living:
            if is_coop[i] and h[i] > COST:
                h[i] -= COST
                pool += COST
                contributors.append(i)

        # allocation of the pool
        if pool > 0:
            if alloc == "PUBLIC":
                candidates = living
            else:  # RECIPROCAL or PUNISH: club good among contributors
                candidates = contributors if contributors else living
            neediest = sorted(candidates, key=lambda i: h[i])[:POOL_TARGETS]
            if neediest:
                share = pool / len(neediest)
                for i in neediest:
                    h[i] += share

        # costly punishment of defectors (PUNISH only)
        if alloc == "PUNISH":
            living_defs = [i for i in living if not is_coop[i] and alive[i]]
            for i in contributors:
                if h[i] > PUNISH_TAX and living_defs:
                    h[i] -= PUNISH_TAX
                    target = living_defs[rng.randrange(len(living_defs))]
                    h[target] -= PUNISH_HIT

        for i in living:
            if h[i] <= DEATH:
                alive[i] = False
            else:
                lifetime_w[i] += max(0.0, h[i])

    coop_alive = sum(1 for i in range(N) if alive[i] and is_coop[i])
    def_alive = sum(1 for i in range(N) if alive[i] and not is_coop[i])
    coop_w = [lifetime_w[i] for i in range(N) if is_coop[i]]
    def_w = [lifetime_w[i] for i in range(N) if not is_coop[i]]
    final = coop_alive + def_alive
    return {
        "coop_frac_final": coop_alive / final if final else 0,
        "coop_w": statistics.mean(coop_w) if coop_w else 0,
        "def_w": statistics.mean(def_w) if def_w else 0,
        "total_w": sum(lifetime_w),
    }


def agg(rows, key):
    return statistics.mean(r[key] for r in rows)


if __name__ == "__main__":
    print(f"N={N} T={T} cost={COST} punish_tax={PUNISH_TAX} punish_hit={PUNISH_HIT} "
          f"seeds={len(list(SEEDS))}")
    print("Mixed 50/50. winner = higher individual lifetime welfare "
          "(is being moral individually rational?)\n")
    print(f"{'alloc':10s} {'horizon':7s} {'coupling':9s} | {'final coop%':>11s} | "
          f"{'coop_welf':>9s} {'def_welf':>9s} | {'total_w':>9s} | {'winner':>10s}")
    print("-" * 96)
    for alloc in ALLOCATIONS:
        for hname, regen in HORIZONS.items():
            for cname, beta in COUPLINGS.items():
                rows = [run(beta, regen, alloc, s) for s in SEEDS]
                cf = agg(rows, "coop_frac_final")
                cw, dw = agg(rows, "coop_w"), agg(rows, "def_w")
                tw = agg(rows, "total_w")
                if abs(cw - dw) < 0.02 * max(cw, dw, 1):
                    winner = "tie"
                else:
                    winner = "COOP(god)" if cw > dw else "DEF(demon)"
                print(f"{alloc:10s} {hname:7s} {cname:9s} | {cf:11.2%} | "
                      f"{cw:9.1f} {dw:9.1f} | {tw:9.0f} | {winner:>10s}")
        print("-" * 96)
    print("P4 RECIPROCAL+LONG -> COOP wins | P5 PUNISH widens it (lower total_w) | "
          "P6 SHORT -> DEF regardless")

#!/usr/bin/env python3
"""
R3 v2 -- regeneration variant (the registered experiment from
R3_TRANSFER_ASYMMETRY_RESULTS.md section 4).

Registered conjecture (2026-06-10, pre-run): giving wins exactly when it
changes the recipient's DYNAMICS (lifts them into the self-sustaining regime),
not merely their position.

Model: as v1 (southern hemisphere, B = sin theta, drift toward the pole,
absorption at theta >= pi - 0.02), plus one new rule -- REGENERATION:
agents with B above a threshold B_REG partially or fully self-restore
(climb toward the equator at rate REGEN); agents below the threshold are
too depleted to climb and only drift.

Two regimes:
  WEAK   regime: REGEN < DRIFT  -> everyone still descends; above-threshold
         agents descend at half speed. All mortal.
  STRONG regime: REGEN > DRIFT  -> above-threshold agents net-climb (the
         threshold is a survival cliff); below-threshold agents sink.

Policies (ANGLE currency only; v1 settled the currency question):
  NONE     : drift/regeneration only
  GIVE     : donor = max-B living; recipient = min-B living (v1's giving)
  TRIAGE   : donor = max-B living; recipient = the agent with the HIGHEST B
             among those below the regeneration threshold (cheapest possible
             dynamics-conversion); falls back to min-B if none below
  RANDOM   : random donor, random recipient
  TAKE     : min-B debited, max-B credited

Stdlib only. Deterministic given SEEDS.
"""

import math
import random
import statistics

PI = math.pi
N = 100
T = 600
DRIFT = 0.004
DEATH = PI - 0.02
K = 10
DTHETA = 0.02
B_REG = 0.5                       # regeneration threshold (theta ~ 0.833*pi)
REGIMES = {"WEAK": 0.002, "STRONG": 0.006}   # REGEN rates
SEEDS = range(20)
EQUATOR = PI / 2


def balance(theta):
    return math.sin(theta)


def alive(theta):
    return theta < DEATH


def init_agents(rng):
    return [rng.uniform(0.55 * PI, 0.92 * PI) for _ in range(N)]


def apply_transfers(thetas, policy, rng):
    if policy == "NONE":
        return
    for _ in range(K):
        living = [i for i, th in enumerate(thetas) if alive(th)]
        if len(living) < 2:
            return
        if policy in ("GIVE", "TRIAGE"):
            src = max(living, key=lambda i: balance(thetas[i]))
            if policy == "TRIAGE":
                below = [i for i in living if balance(thetas[i]) < B_REG and i != src]
                if below:
                    dst = max(below, key=lambda i: balance(thetas[i]))
                else:
                    dst = min(living, key=lambda i: balance(thetas[i]))
            else:
                dst = min(living, key=lambda i: balance(thetas[i]))
        elif policy == "TAKE":
            src = min(living, key=lambda i: balance(thetas[i]))
            dst = max(living, key=lambda i: balance(thetas[i]))
        elif policy == "RANDOM":
            src, dst = rng.sample(living, 2)
        else:
            raise ValueError(policy)
        if src == dst:
            continue
        thetas[src] = min(thetas[src] + DTHETA, PI)
        thetas[dst] = max(thetas[dst] - DTHETA, EQUATOR)


def run(policy, regen, seed):
    rng = random.Random(seed)
    thetas = init_agents(rng)
    deaths = [None] * N
    b_integral = 0.0
    for t in range(T):
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                step = DRIFT - (regen if balance(thetas[i]) > B_REG else 0.0)
                thetas[i] = max(thetas[i] + step, EQUATOR)
                any_alive = True
        if not any_alive:
            break
        apply_transfers(thetas, policy, rng)
        for i in range(N):
            if alive(thetas[i]):
                b_integral += balance(thetas[i])
            elif deaths[i] is None:
                deaths[i] = t
    lifespans = [(d if d is not None else T) for d in deaths]
    survivors = sum(1 for th in thetas if alive(th))
    return b_integral, statistics.mean(lifespans), survivors


def summarize(policy, regime, regen):
    rows = [run(policy, regen, s) for s in SEEDS]
    cols = list(zip(*rows))

    def ms(vals):
        return statistics.mean(vals), statistics.stdev(vals)

    bi, ls, sv = ms(cols[0]), ms(cols[1]), ms(cols[2])
    print(f"{regime:6s} {policy:7s} | B-integral {bi[0]:9.0f} +/- {bi[1]:6.0f} | "
          f"mean lifespan {ls[0]:6.1f} +/- {ls[1]:5.1f} | survivors@T {sv[0]:5.1f}")


if __name__ == "__main__":
    print(f"N={N} T={T} drift={DRIFT} K={K} dtheta={DTHETA} "
          f"B_reg={B_REG} regen(weak)={REGIMES['WEAK']} regen(strong)={REGIMES['STRONG']} "
          f"seeds={len(list(SEEDS))}")
    print("-" * 90)
    for regime, regen in REGIMES.items():
        for pol in ("NONE", "GIVE", "TRIAGE", "RANDOM", "TAKE"):
            summarize(pol, regime, regen)
        print("-" * 90)

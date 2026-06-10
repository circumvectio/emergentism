#!/usr/bin/env python3
"""
R3 v3 -- robustness suite for the triage-inversion result.

Three questions a referee will ask, answered by experiment:

A. CONCAVITY SWEEP: does the dynamic inversion (GIVE-to-poorest < NONE) depend
   on the specific welfare function B = sin(theta), or does it hold for any
   concave welfare -- and what happens at linear and convex controls?
   Welfare is defined on normalized health s in (0,1] (s = scaled distance
   from the death boundary; s=1 at the equator, s->0 at absorption):
     SIN   : sin(s * pi/2)         (baseline, concave)
     SQRT  : sqrt(s)               (concave, steep near 0)
     LOG   : log(1+9s)/log(10)     (concave, steeper near 0)
     LIN   : s                     (linear control -- no static Jensen gain)
     SQ    : s^2                   (convex control -- static Jensen reversed)
   Registered predictions (2026-06-10, pre-run): the inversion persists for
   ALL concave welfare (it is trajectory-driven, not curvature-driven), and
   persists even at LIN (lifetime welfare from drift-to-absorption is
   s0^2-shaped, i.e. convex in initial health, so equalizing initial health
   lowers the integral); RANDOM's small static gain shrinks toward LIN and
   reverses at SQ.

B. TRANSFER-VOLUME SWEEP: K in {2, 10, 30} transfers/step (0.1x, 0.5x, 1.5x
   of total drift volume). Prediction: inversion at all volumes (theta-
   conserving transfers cannot change total descent), deepening with K.

C. OBJECTIVE SWEEP (same runs, baseline SIN): rank policies under
   (i) welfare-time integral, (ii) discounted welfare (gamma=0.995),
   (iii) Rawlsian minimum lifetime welfare, (iv) mean per-living-capita
   welfare per step, (v) total lifespan. Prediction: per-capita ranking
   flips for TAKE (culling the depleted raises the average) -- the choice
   of objective is morally load-bearing and must be reported.

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
EQUATOR = PI / 2
DTHETA = 0.02
SEEDS = range(12)
GAMMA = 0.995
SPAN = DEATH - EQUATOR


def health(theta):
    """normalized health s in (0,1]: 1 at equator, 0 at death boundary"""
    return max(0.0, (DEATH - theta) / SPAN)


WELFARE = {
    "SIN":  lambda s: math.sin(s * PI / 2),
    "SQRT": lambda s: math.sqrt(s),
    "LOG":  lambda s: math.log(1 + 9 * s) / math.log(10),
    "LIN":  lambda s: s,
    "SQ":   lambda s: s * s,
}


def alive(theta):
    return theta < DEATH


def init_agents(rng):
    return [rng.uniform(0.55 * PI, 0.92 * PI) for _ in range(N)]


def apply_transfers(thetas, policy, k, w, rng):
    if policy == "NONE":
        return
    for _ in range(k):
        living = [i for i, th in enumerate(thetas) if alive(th)]
        if len(living) < 2:
            return
        if policy == "GIVE":
            src = max(living, key=lambda i: thetas[i] * -1)   # highest health
            dst = max(living, key=lambda i: thetas[i])        # lowest health
        elif policy == "TAKE":
            src = max(living, key=lambda i: thetas[i])
            dst = min(living, key=lambda i: thetas[i])
        elif policy == "RANDOM":
            src, dst = rng.sample(living, 2)
        else:
            raise ValueError(policy)
        if src == dst:
            continue
        thetas[src] = min(thetas[src] + DTHETA, PI)
        thetas[dst] = max(thetas[dst] - DTHETA, EQUATOR)


def run(policy, wname, k, seed):
    w = WELFARE[wname]
    rng = random.Random(seed)
    thetas = init_agents(rng)
    deaths = [None] * N
    lifetime_w = [0.0] * N
    w_integral = 0.0
    w_discounted = 0.0
    percap_sum = 0.0
    percap_steps = 0
    for t in range(T):
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                thetas[i] += DRIFT
                any_alive = True
        if not any_alive:
            break
        apply_transfers(thetas, policy, k, w, rng)
        step_w = 0.0
        living_n = 0
        for i in range(N):
            if alive(thetas[i]):
                wi = w(health(thetas[i]))
                step_w += wi
                lifetime_w[i] += wi
                living_n += 1
            elif deaths[i] is None:
                deaths[i] = t
        w_integral += step_w
        w_discounted += (GAMMA ** t) * step_w
        if living_n:
            percap_sum += step_w / living_n
            percap_steps += 1
    lifespans = [(d if d is not None else T) for d in deaths]
    return {
        "W": w_integral,
        "Wdisc": w_discounted,
        "rawls": min(lifetime_w),
        "percap": percap_sum / max(percap_steps, 1),
        "life": statistics.mean(lifespans),
    }


def agg(rows, key):
    vals = [r[key] for r in rows]
    return statistics.mean(vals), statistics.stdev(vals)


if __name__ == "__main__":
    print(f"N={N} T={T} drift={DRIFT} dtheta={DTHETA} seeds={len(list(SEEDS))} gamma={GAMMA}")

    print("\n=== A. CONCAVITY SWEEP (K=10): welfare-time integral W ===")
    print(f"{'welfare':6s} " + "".join(f"{p:>16s}" for p in ("NONE", "GIVE", "RANDOM", "TAKE")))
    ratios = {}
    for wname in ("SIN", "SQRT", "LOG", "LIN", "SQ"):
        cells = []
        means = {}
        for pol in ("NONE", "GIVE", "RANDOM", "TAKE"):
            rows = [run(pol, wname, 10, s) for s in SEEDS]
            m, sd = agg(rows, "W")
            means[pol] = m
            cells.append(f"{m:9.0f}±{sd:5.0f}")
        ratios[wname] = (means["GIVE"] / means["NONE"], means["RANDOM"] / means["NONE"])
        print(f"{wname:6s} " + "".join(f"{c:>16s}" for c in cells))
    print("GIVE/NONE ratios: " + ", ".join(f"{k}={v[0]:.3f}" for k, v in ratios.items()))
    print("RAND/NONE ratios: " + ", ".join(f"{k}={v[1]:.3f}" for k, v in ratios.items()))

    print("\n=== B. TRANSFER-VOLUME SWEEP (SIN): welfare-time integral W ===")
    print(f"{'K':>3s} {'volume/drift':>13s} " + "".join(f"{p:>16s}" for p in ("NONE", "GIVE", "RANDOM")))
    for k in (2, 10, 30):
        cells = []
        for pol in ("NONE", "GIVE", "RANDOM"):
            rows = [run(pol, "SIN", k, s) for s in SEEDS]
            m, sd = agg(rows, "W")
            cells.append(f"{m:9.0f}±{sd:5.0f}")
        ratio = k * DTHETA / (N * DRIFT)
        print(f"{k:3d} {ratio:13.2f} " + "".join(f"{c:>16s}" for c in cells))

    print("\n=== C. OBJECTIVE SWEEP (SIN, K=10): does the ranking depend on the objective? ===")
    print(f"{'policy':7s} {'W (sum)':>14s} {'W disc.':>14s} {'Rawls min':>11s} "
          f"{'per-capita':>11s} {'lifespan':>10s}")
    for pol in ("NONE", "GIVE", "RANDOM", "TAKE"):
        rows = [run(pol, "SIN", 10, s) for s in SEEDS]
        w, wsd = agg(rows, "W")
        d, _ = agg(rows, "Wdisc")
        rmin, _ = agg(rows, "rawls")
        pc, _ = agg(rows, "percap")
        lf, _ = agg(rows, "life")
        print(f"{pol:7s} {w:9.0f}±{wsd:4.0f} {d:14.0f} {rmin:11.1f} {pc:11.3f} {lf:10.1f}")

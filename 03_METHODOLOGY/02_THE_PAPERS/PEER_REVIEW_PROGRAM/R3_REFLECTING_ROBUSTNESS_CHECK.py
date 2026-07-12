#!/usr/bin/env python3
"""
Robustness companion for R3_REFLECTING_BOUNDARY_CONTROL.py.

Two questions:
 (A) Is the persistence of the triage inversion under the reflecting boundary
     an artifact of where exactly we placed the floor? Sweep FLOOR across a
     range of latitudes (always strictly inside the alive region) and report
     GIVE/NONE under reflection at each.
 (B) Is the GIVE<NONE effect under reflection statistically real, or within
     seed noise? Paired-difference test across the 20 seeds (mean diff, its
     SEM, and a crude z = mean/SEM).

Also reports the elastic-reflection variant (reflect about the wall, conserving
the excess drift) as a sanity check that the qualitative result does not hinge
on the hard-floor reflection rule.

Stdlib only.
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
K = 10
DTHETA = 0.02
B_REG = 0.5
SEEDS = list(range(20))


def balance(theta):
    return math.sin(theta)


def alive(theta):
    return theta < DEATH


def init_agents(rng):
    return [rng.uniform(0.55 * PI, 0.92 * PI) for _ in range(N)]


def apply_transfers(thetas, policy, donor_cap, rng):
    if policy == "NONE":
        return
    for _ in range(K):
        idx = [i for i in range(N) if alive(thetas[i])]
        if len(idx) < 2:
            return
        if policy == "GIVE":
            src = max(idx, key=lambda i: balance(thetas[i]))
            dst = min(idx, key=lambda i: balance(thetas[i]))
        elif policy == "TRIAGE":
            src = max(idx, key=lambda i: balance(thetas[i]))
            below = [i for i in idx if balance(thetas[i]) < B_REG and i != src]
            dst = (max(below, key=lambda i: balance(thetas[i])) if below
                   else min(idx, key=lambda i: balance(thetas[i])))
        elif policy == "TAKE":
            src = min(idx, key=lambda i: balance(thetas[i]))
            dst = max(idx, key=lambda i: balance(thetas[i]))
        elif policy == "RANDOM":
            src, dst = rng.sample(idx, 2)
        else:
            raise ValueError(policy)
        if src == dst:
            continue
        thetas[src] = min(thetas[src] + DTHETA, donor_cap)
        thetas[dst] = max(thetas[dst] - DTHETA, EQUATOR)


def run_floor(policy, floor, seed):
    """Hard-floor reflecting boundary at `floor` (floor < DEATH strictly)."""
    rng = random.Random(seed)
    thetas = init_agents(rng)
    b_integral = 0.0
    donor_cap = floor
    for t in range(T):
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                thetas[i] = min(thetas[i] + DRIFT, floor)
                any_alive = True
        if not any_alive:
            break
        apply_transfers(thetas, policy, donor_cap, rng)
        for i in range(N):
            if alive(thetas[i]):
                b_integral += balance(thetas[i])
    return b_integral


def run_elastic(policy, seed):
    """Elastic reflecting boundary: reflect about DEATH, conserving excess.

    If theta+DRIFT would cross DEATH, bounce: theta <- 2*DEATH - (theta+DRIFT),
    clamped to be < DEATH. Donors pushed past DEATH by a transfer bounce the
    same way. Agents never leave.
    """
    rng = random.Random(seed)
    thetas = init_agents(rng)
    b_integral = 0.0

    def reflect(new):
        # bounce about DEATH until inside the alive region
        while new >= DEATH:
            new = 2 * DEATH - new
            if new >= DEATH:        # numerical guard
                new = DEATH - 1e-12
        return new

    def donor_push(src_theta):
        return reflect(src_theta + DTHETA)

    for t in range(T):
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                thetas[i] = reflect(thetas[i] + DRIFT)
                any_alive = True
        if not any_alive:
            break
        # transfers with elastic donor reflection
        if True:
            pol = policy
            for _ in range(K):
                idx = [i for i in range(N) if alive(thetas[i])]
                if len(idx) < 2:
                    break
                if pol == "GIVE":
                    src = max(idx, key=lambda i: balance(thetas[i]))
                    dst = min(idx, key=lambda i: balance(thetas[i]))
                elif pol == "TRIAGE":
                    src = max(idx, key=lambda i: balance(thetas[i]))
                    below = [i for i in idx if balance(thetas[i]) < B_REG and i != src]
                    dst = (max(below, key=lambda i: balance(thetas[i])) if below
                           else min(idx, key=lambda i: balance(thetas[i])))
                elif pol == "TAKE":
                    src = min(idx, key=lambda i: balance(thetas[i]))
                    dst = max(idx, key=lambda i: balance(thetas[i]))
                elif pol == "RANDOM":
                    src, dst = rng.sample(idx, 2)
                else:
                    break
                if src == dst:
                    continue
                thetas[src] = donor_push(thetas[src])
                thetas[dst] = max(thetas[dst] - DTHETA, EQUATOR)
        for i in range(N):
            if alive(thetas[i]):
                b_integral += balance(thetas[i])
    return b_integral


def paired_stats(pol_none, pol_give, runner, **kw):
    none_vals = [runner("NONE", s, **kw) for s in SEEDS]
    give_vals = [runner(pol_give, s, **kw) for s in SEEDS]
    diffs = [g - n for g, n in zip(give_vals, none_vals)]
    m_none = statistics.mean(none_vals)
    m_give = statistics.mean(give_vals)
    m_diff = statistics.mean(diffs)
    sem_diff = statistics.stdev(diffs) / math.sqrt(len(diffs))
    z = m_diff / sem_diff if sem_diff > 0 else float("inf")
    return m_none, m_give, m_diff, sem_diff, z


print("=" * 80)
print("(A) FLOOR-POSITION SWEEP under hard-floor reflection: GIVE vs NONE")
print("    floor shown as B(floor) so positions are comparable")
print("=" * 80)
print(f"{'B(floor)':>9s} {'NONE':>9s} {'GIVE':>9s} {'ratio':>7s} {'delta%':>7s}")
for k in range(1, 8):
    floor = DEATH - k * DRIFT
    none_vals = [run_floor("NONE", floor, s) for s in SEEDS]
    give_vals = [run_floor("GIVE", floor, s) for s in SEEDS]
    mn, mg = statistics.mean(none_vals), statistics.mean(give_vals)
    print(f"{balance(floor):9.4f} {mn:9.0f} {mg:9.0f} {mg/mn:7.3f} "
          f"{100*(mg-mn)/mn:+7.1f}")

print()
print("=" * 80)
print("(B) PAIRED SEED TEST, hard-floor reflection, FLOOR = DEATH - DRIFT")
print("    (the control's primary configuration)")
print("=" * 80)
for pol in ("GIVE", "TRIAGE", "RANDOM", "TAKE"):
    mn, mg, md, sem, z = paired_stats(pol, pol, run_floor,
                                      floor=DEATH - DRIFT)
    print(f"  {pol:7s}: NONE={mn:8.0f}  {pol}={mg:8.0f}  "
          f"diff={md:+8.0f} +/- {sem:6.0f}  z={z:+6.2f}")

print()
print("=" * 80)
print("(C) ELASTIC REFLECTION (bounce about the wall, excess conserved)")
print("    sanity check that the rule form does not drive the conclusion")
print("=" * 80)
print(f"{'policy':>8s} {'NONE':>9s} {'policy':>9s} {'ratio':>7s} {'delta%':>7s}")
for pol in ("GIVE", "TRIAGE", "RANDOM", "TAKE"):
    none_vals = [run_elastic("NONE", s) for s in SEEDS]
    pol_vals = [run_elastic(pol, s) for s in SEEDS]
    mn, mp = statistics.mean(none_vals), statistics.mean(pol_vals)
    print(f"{pol:>8s} {mn:9.0f} {mp:9.0f} {mp/mn:7.3f} "
          f"{100*(mp-mn)/mn:+7.1f}")

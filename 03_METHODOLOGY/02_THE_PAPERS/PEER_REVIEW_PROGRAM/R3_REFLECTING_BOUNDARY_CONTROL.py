#!/usr/bin/env python3
"""
R3 -- reflecting-boundary CONTROL experiment.

This is the control the R3 paper owes its referees. R3's central claim is that
the triage inversion (PROGRESSIVE / GIVE-to-the-poorest REDUCES aggregate
welfare-time relative to NONE, even though every transfer is instantaneously
Pigou-Dalton-positive) is driven by the ABSORBING mortality boundary, NOT by
curvature of the welfare function.

The v3 robustness suite already proved the curvature half: the inversion
persists at LINEAR welfare (no static Jensen effect), so it is trajectory-
driven, not curvature-driven. But "trajectory-driven" could still mean
"absorption-driven" or "something about drift itself." The reflecting boundary
isolates the absorption contribution directly:

    If we change NOTHING but the boundary -- same population, same welfare
    function B = sin(theta), same drift, same transfer rules -- except that an
    agent that would be absorbed is instead REFLECTED (set to a floor and kept
    in the population), then:

      * if PROGRESSIVE still harms welfare  -> inversion is NOT absorption-driven;
                                                 R3's claim needs revision.
      * if PROGRESSIVE no longer harms       -> absorption is the driver; R3's
                                                 claim is strengthened.

We run BOTH boundaries in the same script from a single code base so the only
difference between the ABSORBING and REFLECTING columns is the boundary rule.
The ABSORBING column must reproduce the archived v1/v2 numbers (within Monte
Carlo noise) -- that is the code-validation check.

MODEL (identical to R3_SUPPORT_TRANSFER_SIM.py / V2.py unless noted):
  N agents, theta in [pi/2, pi), B = sin(theta) (concave; B=1 at equator,
  B->0 at the pole). Each step every living agent drifts toward the pole,
  theta += DRIFT (delta = 0.004).
  ABSORBING:  agent with theta >= pi-0.02 is removed (alive=False; stops
              drifting, stops contributing to the welfare integral).
  REFLECTING: agent that would reach pi-0.02 is instead set to the floor
              FLOOR = pi-0.02 and KEPT in the population (it continues to
              drift, but each step is immediately re-floored, so it sits at
              B = sin(pi-0.02) ~= 0.02 for the rest of the run). Agent count
              stays at N forever.
  Welfare metric: B-integral = sum over steps of sum over *living* agents of
              B(theta_i). Under REFLECTING every agent is always "living," so
              the integral is over all N at every step.

POLICIES (ANGLE currency only; v1 settled that the latitude-denominated
transfer is the clean Pigou-Dalton case -- Σtheta is conserved per transfer):
  NONE       : drift only (the baseline)
  GIVE       : max-B donor -> min-B recipient  (the PROGRESSIVE / Pigou-Dalton
               transfer; textbook "give to the poorest")
  TAKE       : min-B debited -> max-B credited  (EXTRACTION)
  TRIAGE     : max-B donor -> the highest-B agent BELOW the regeneration
               threshold B_REG=0.5 (cheapest dynamics-conversion target);
               falls back to min-B if none below threshold. This is the
               corpus's "ARJUNA" giving operator -- targeted discernment.
  RANDOM     : random donor, random recipient.

Registered prediction (before running, 2026-07-12): under the reflecting
boundary the triage inversion DISAPPEARS -- GIVE and TRIAGE no longer
underperform NONE on the B-integral, because there is no absorption to
convert "rescue parking mass at low B" into "lost high-B donor lifetime."
(The floor agents still contribute a trickle of B, and donors are never
killed by repeated withdrawal.) If the inversion persists, R3's absorption
claim is refuted and curvature/trajectory effects must be re-examined.

Stdlib only (math, random, statistics). Deterministic given SEEDS.
"""

import math
import random
import statistics

PI = math.pi
N = 100                  # agents
T = 600                  # max steps
DRIFT = 0.004            # latitude drift toward dispersal pole per step
DEATH = PI - 0.02        # absorbing boundary location (the pole, operationally)
# Reflecting-boundary floor. Must sit STRICTLY inside the alive region
# (theta < DEATH) so a reflected agent stays alive -- otherwise alive()=False
# at the floor and the reflection is operationally identical to absorption.
# We place the floor one drift-step inside the wall so a reflected agent
# contributes B = sin(DEATH-DRIFT) ~= 0.0239 per step (essentially the same
# trickle a just-pre-death agent contributes in the absorbing model). The two
# boundaries thus sit at the SAME latitude (the wall at pi-0.02); they differ
# only in whether an agent reaching it LEAVES or STAYS.
FLOOR = DEATH - DRIFT    # = pi - 0.024; alive(FLOOR) is True
EQUATOR = PI / 2
K = 10                   # transfers per step
DTHETA = 0.02            # ANGLE currency quantum (radians)
B_REG = 0.5              # regeneration threshold for TRIAGE (matches V2)
SEEDS = range(20)


def balance(theta):
    return math.sin(theta)


def alive(theta):
    """Liveness is a function of CURRENT theta (matches v1/v2/v3 semantics).

    An agent pushed past DEATH by a transfer is dead for integration purposes
    in the SAME step -- this is what makes TAKE's death-timing match v1.
    """
    return theta < DEATH


def init_agents(rng):
    # identical initialization to v1/v2/v3
    return [rng.uniform(0.55 * PI, 0.92 * PI) for _ in range(N)]


def apply_transfers(thetas, policy, boundary, rng):
    """ANGLE-currency transfers, identical selection logic to v1/v2.

    Liveness is read dynamically via alive(theta), so the set of transfer-
    eligible agents updates within the step exactly as in v1.

    Boundary only affects the DONOR cap (the agent pushed TOWARD the pole).
    The recipient is pushed toward the equator and can never die, so its cap
    is boundary-independent. Under ABSORBING the donor is capped at PI (matches
    v1: a donor reaching/past DEATH dies and is removed); under REFLECTING the
    donor is capped at FLOOR so it is reflected, not removed. This is the only
    place transfers interact with the boundary.
    """
    donor_cap = PI if boundary == "ABSORBING" else FLOOR
    if policy == "NONE":
        return
    for _ in range(K):
        idx = [i for i in range(N) if alive(thetas[i])]
        if len(idx) < 2:
            return
        if policy == "GIVE":
            src = max(idx, key=lambda i: balance(thetas[i]))   # abundant pays
            dst = min(idx, key=lambda i: balance(thetas[i]))   # scarce receives
        elif policy == "TRIAGE":
            src = max(idx, key=lambda i: balance(thetas[i]))
            below = [i for i in idx if balance(thetas[i]) < B_REG and i != src]
            if below:
                dst = max(below, key=lambda i: balance(thetas[i]))
            else:
                dst = min(idx, key=lambda i: balance(thetas[i]))
        elif policy == "TAKE":
            src = min(idx, key=lambda i: balance(thetas[i]))   # scarce debited
            dst = max(idx, key=lambda i: balance(thetas[i]))   # abundant receives
        elif policy == "RANDOM":
            src, dst = rng.sample(idx, 2)
        else:
            raise ValueError(policy)
        if src == dst:
            continue
        # ANGLE currency: theta-conserving (Pigou-Dalton per transfer).
        # Recipient cap is the equator; donor cap is boundary-dependent.
        thetas[src] = min(thetas[src] + DTHETA, donor_cap)
        thetas[dst] = max(thetas[dst] - DTHETA, EQUATOR)


def run(policy, boundary, seed):
    """Single run. boundary in {"ABSORBING", "REFLECTING"}.

    Returns (b_integral, mean_lifespan, survivors_at_T).
    Under REFLECTING there are no deaths, so mean_lifespan is T for everyone
    and survivors_at_T is N; we report them anyway for column parity.

    Step order matches v1 exactly: drift -> transfer -> integrate. The ONLY
    difference between boundaries is the drift rule at the wall:
      ABSORBING : theta >= DEATH  -> agent stays put, alive() becomes False,
                                    it drops out (recorded dead at first such t).
      REFLECTING: theta would reach DEATH -> floored at FLOOR, kept alive forever.
    """
    rng = random.Random(seed)
    thetas = init_agents(rng)
    death_time = [None] * N      # first step at which i was found dead (absorbing)
    b_integral = 0.0

    for t in range(T):
        # 1. drift every still-alive agent toward the pole
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                if boundary == "REFLECTING":
                    # floor at the wall: never crosses DEATH, never dies
                    thetas[i] = min(thetas[i] + DRIFT, FLOOR)
                else:  # ABSORBING: drift freely; alive() will flip at the wall
                    thetas[i] = thetas[i] + DRIFT
                any_alive = True
        if not any_alive:
            break

        # 2. transfers among the currently-alive (dynamic alive() check)
        apply_transfers(thetas, policy, boundary, rng)

        # 3. welfare integral over living agents; record deaths (absorbing only)
        for i in range(N):
            if alive(thetas[i]):
                b_integral += balance(thetas[i])
            elif death_time[i] is None:
                death_time[i] = t

    lifespans = [(T if d is None else d) for d in death_time]
    survivors = sum(1 for th in thetas if alive(th))
    return b_integral, statistics.mean(lifespans), survivors


def summarize(policy, boundary):
    rows = [run(policy, boundary, s) for s in SEEDS]
    cols = list(zip(*rows))
    mean_w = statistics.mean(cols[0])
    # standard ERROR of the mean (1/sqrt(n)), matching what a referee expects
    sem_w = statistics.stdev(cols[0]) / math.sqrt(len(SEEDS))
    mean_life = statistics.mean(cols[1])
    surv = statistics.mean(cols[2])
    return mean_w, sem_w, mean_life, surv


def main():
    header = (f"N={N} T={T} drift={DRIFT} K={K} dtheta={DTHETA} "
              f"B_reg={B_REG} floor={FLOOR:.5f} (=DEATH) seeds={len(list(SEEDS))}")
    print(header)
    print("-" * len(header))

    # Validation print of the static unit check (must be +0.017989, matches v1)
    td, tr = 1.65, 3.00
    b0 = balance(td) + balance(tr)
    da = (balance(td + DTHETA) + balance(tr - DTHETA)) - b0
    print(f"unit check GIVE | ANGLE  : dSumB = {da:+.6f}  (expect +0.017989)")
    print()

    policies = ("NONE", "GIVE", "TRIAGE", "RANDOM", "TAKE")
    boundaries = ("ABSORBING", "REFLECTING")

    results = {}
    for bnd in boundaries:
        results[bnd] = {}
        for pol in policies:
            results[bnd][pol] = summarize(pol, bnd)

    # ---- table: side by side ----
    col_w = 22
    print("B-integral (mean +/- SEM)              | ABSORBING              | REFLECTING")
    print("-" * 78)
    for pol in policies:
        a = results["ABSORBING"][pol]
        r = results["REFLECTING"][pol]
        print(f"{pol:8s} (welfare-time)      | {a[0]:9.0f} +/- {a[1]:6.0f}     | "
              f"{r[0]:9.0f} +/- {r[1]:6.0f}")

    print()
    print("mean lifespan                          | ABSORBING   | REFLECTING")
    print("-" * 60)
    for pol in policies:
        a = results["ABSORBING"][pol]
        r = results["REFLECTING"][pol]
        print(f"{pol:8s}                       | {a[2]:11.1f} | {r[2]:11.1f}")

    print()
    print("survivors @ T                          | ABSORBING   | REFLECTING")
    print("-" * 60)
    for pol in policies:
        a = results["ABSORBING"][pol]
        r = results["REFLECTING"][pol]
        print(f"{pol:8s}                       | {a[3]:11.1f} | {r[3]:11.1f}")

    # ---- the diagnostic: GIVE vs NONE under each boundary ----
    print()
    print("=" * 78)
    print("DIAGNOSTIC: triage inversion (GIVE-to-poorest welfare vs NONE)")
    print("=" * 78)
    for bnd in boundaries:
        nw, _, _, _ = results[bnd]["NONE"]
        gw, _, _, _ = results[bnd]["GIVE"]
        tw, _, _, _ = results[bnd]["TRIAGE"]
        ratio = gw / nw
        delta_pct = 100.0 * (gw - nw) / nw
        verdict = "INVERTED (GIVE harms)" if gw < nw else "NOT inverted (GIVE helps/neut.)"
        print(f"  {bnd:11s}: NONE={nw:8.0f}  GIVE={gw:8.0f}  "
              f"(ratio {ratio:.3f}, {delta_pct:+5.1f}%)  -> {verdict}")
        print(f"  {'':11s}  TRIAGE={tw:8.0f}  "
              f"(vs NONE {100.0*(tw-nw)/nw:+5.1f}%)")


if __name__ == "__main__":
    main()

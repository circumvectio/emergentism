#!/usr/bin/env python3
"""
R3 support artifact -- transfer-asymmetry demonstrator on the balance hemisphere.

Model-internal verification of Paper W's "Descent Theorem" claims.

Model: N agents at latitude theta in [pi/2, pi) on the balance sphere,
balance B = sin(theta) (B = 1 at the equator, B -> 0 at the dispersal pole).
Every agent drifts toward the pole (theta -> pi) each step -- the DBC arrow.
Death (absorption) at theta >= pi - 0.02.

Transfer policies redistribute between a payer and a receiver each step:
  GIVE   : most-equatorial (abundant) agent pays, most-polar (scarce) receives
  TAKE   : most-polar (scarce) agent is debited, most-equatorial receives
  RANDOM : random payer, random receiver (tests whether targeting matters)
  NONE   : drift only

Two exchange currencies:
  ANGLE   : transfers are denominated in latitude (d-theta quanta).
            Total theta is conserved by each transfer.
  BALANCE : transfers are denominated in balance itself (dB quanta).
            Total B is conserved by each transfer (instantaneously).

The question put to the model: does "giving down-gradient is net-positive"
(Paper W section 3) actually follow from the geometry -- and under which
implicit assumptions?

Stdlib only. Deterministic given SEEDS.
"""

import math
import random
import statistics

PI = math.pi
N = 100             # agents
T = 600             # max steps
DRIFT = 0.004       # latitude drift toward dispersal pole per step
DEATH = PI - 0.02   # absorbing boundary (the pole, operationally)
K = 10              # transfers per step
DTHETA = 0.02       # ANGLE currency quantum (radians)
TAU = 0.01          # BALANCE currency quantum (balance units)
SEEDS = range(20)


def balance(theta):
    return math.sin(theta)


def theta_from_balance(b):
    # southern-hemisphere branch: theta in [pi/2, pi]
    b = min(max(b, 0.0), 1.0)
    return PI - math.asin(b)


def alive(theta):
    return theta < DEATH


def init_agents(rng):
    return [rng.uniform(0.55 * PI, 0.92 * PI) for _ in range(N)]


def apply_transfers(thetas, policy, currency, rng):
    if policy == "NONE":
        return
    for _ in range(K):
        living = [i for i, th in enumerate(thetas) if alive(th)]
        if len(living) < 2:
            return
        if policy == "GIVE":
            src = max(living, key=lambda i: balance(thetas[i]))  # abundant pays
            dst = min(living, key=lambda i: balance(thetas[i]))  # scarce receives
        elif policy == "TAKE":
            src = min(living, key=lambda i: balance(thetas[i]))  # scarce debited
            dst = max(living, key=lambda i: balance(thetas[i]))  # abundant receives
        elif policy == "RANDOM":
            src, dst = rng.sample(living, 2)
        else:
            raise ValueError(policy)
        if src == dst:
            continue
        if currency == "ANGLE":
            thetas[src] = min(thetas[src] + DTHETA, PI)
            thetas[dst] = max(thetas[dst] - DTHETA, PI / 2)
        elif currency == "BALANCE":
            thetas[src] = theta_from_balance(balance(thetas[src]) - TAU)
            thetas[dst] = theta_from_balance(balance(thetas[dst]) + TAU)
        else:
            raise ValueError(currency)


def run(policy, currency, seed):
    rng = random.Random(seed)
    thetas = init_agents(rng)
    deaths = [None] * N
    b_integral = 0.0
    for t in range(T):
        any_alive = False
        for i in range(N):
            if alive(thetas[i]):
                thetas[i] += DRIFT  # the descent: spontaneous drift toward the pole
                any_alive = True
        if not any_alive:
            break
        apply_transfers(thetas, policy, currency, rng)
        for i in range(N):
            if alive(thetas[i]):
                b_integral += balance(thetas[i])
            elif deaths[i] is None:
                deaths[i] = t
    lifespans = [(d if d is not None else T) for d in deaths]
    survivors = sum(1 for th in thetas if alive(th))
    return b_integral, statistics.mean(lifespans), survivors


def summarize(policy, currency):
    rows = [run(policy, currency, s) for s in SEEDS]
    cols = list(zip(*rows))

    def ms(vals):
        return statistics.mean(vals), statistics.stdev(vals)

    bi, ls, sv = ms(cols[0]), ms(cols[1]), ms(cols[2])
    print(f"{policy:7s} {currency:8s} | B-integral {bi[0]:9.0f} +/- {bi[1]:6.0f} | "
          f"mean lifespan {ls[0]:6.1f} +/- {ls[1]:5.1f} | survivors@T {sv[0]:5.1f}")


def unit_check():
    """Single-transfer sign check: donor near equator, recipient near pole."""
    td, tr = 1.65, 3.00
    b0 = balance(td) + balance(tr)
    da = (balance(td + DTHETA) + balance(tr - DTHETA)) - b0
    db = (balance(theta_from_balance(balance(td) - TAU)) +
          balance(theta_from_balance(balance(tr) + TAU))) - b0
    ca = (td + DTHETA + tr - DTHETA) - (td + tr)
    cb = (theta_from_balance(balance(td) - TAU) +
          theta_from_balance(balance(tr) + TAU)) - (td + tr)
    print(f"unit check GIVE | ANGLE   currency: dSumB = {da:+.6f}  (Sum-theta change {ca:+.6f})")
    print(f"unit check GIVE | BALANCE currency: dSumB = {db:+.6f}  (Sum-theta change {cb:+.6f})")


if __name__ == "__main__":
    print(f"N={N} T={T} drift={DRIFT} K={K} dtheta={DTHETA} tau={TAU} "
          f"seeds={len(list(SEEDS))}")
    unit_check()
    print("-" * 86)
    summarize("NONE", "-")
    for cur in ("ANGLE", "BALANCE"):
        for pol in ("GIVE", "RANDOM", "TAKE"):
            summarize(pol, cur)

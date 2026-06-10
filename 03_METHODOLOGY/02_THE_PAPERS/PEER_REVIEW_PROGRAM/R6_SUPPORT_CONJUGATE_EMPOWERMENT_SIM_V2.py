#!/usr/bin/env python3
"""
R6 v2 -- the repair: is BALANCE the optimum of empowerment-UNDER-MORTALITY?

R6 v1 found: empowerment's conjugate decomposition is ADDITIVE (a reach/precision
simplex, not a phi.nu sphere) and empowerment-maximization is REACH-DOMINATED --
balance is never optimal. F-R6-4 conjectured the repair: balance becomes optimal
only when low coherence is FATAL (incoherence -> you can't reliably reach a needed
state -> you die), which is exactly the absorbing-mortality cost of R3/R7/R8. This
would unify the teleology thread with the cooperation/mortality threads: coherence
matters because incoherence kills, not because options are fewer.

MODEL: the R6 v1 channel (circle of K cells, r evenly-spaced targets, budgeted
precision sigma=s0*sqrt(r)). Each step the agent gains empowerment E(r) (options/
throughput) but faces a death rate that rises with INCOHERENCE:
    death_rate(r) = base + mu * (1 - phi_n(r))      # incoherence kills, scale mu
    expected_lifetime L(r) = 1 / death_rate(r)
    lifetime value      V(r; mu) = E(r) * L(r)       # empowerment accrued over a life
mu = 0 recovers pure empowerment (reach-dominated, R6 v1). Raising mu prices
incoherence. Where does the optimum land?

REGISTERED PREDICTIONS (2026-06-10, pre-run):
  P1: mu=0 -> optimum reach-dominated (recovers R6 v1: nu >> phi).
  P2: as mu rises, the optimum moves monotonically toward higher coherence (lower r).
  P3: there is a critical mu* where the optimum sits at BALANCE (phi_n ~ nu_n) --
      the corpus's equator, RECOVERED as empowerment-under-mortality. This would
      vindicate the balance ideal, on a simplex, via a coherence/mortality cost.
  P4: beyond mu*, the optimum overshoots to precision-dominated -- so balance is a
      critical point on a mortality continuum, not a universal attractor (honest nuance).
  KILL: if the optimum never reaches balance for any mu (jumps reach->precision with
      no balanced regime), then mortality does NOT recover the equator and F-R6-4 fails.

Stdlib only. Deterministic.
"""

import math

K = 64
S0 = 2.0
HMAX = math.log2(K)
TOL = 1           # survival tolerance: must land within +/-TOL cells of target
BASE_DEATH = 0.04
MUS = (0.0, 0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20)


def entropy(p):
    return -sum(pi * math.log2(pi) for pi in p if pi > 0.0)


def blur_dist(t, sigma):
    sigma = min(sigma, float(K))
    m_wrap = max(3, int(3 * sigma / K) + 1)
    inv = 1.0 / (2 * sigma * sigma)
    ps = []
    for s in range(K):
        acc = 0.0
        for m in range(-m_wrap, m_wrap + 1):
            d = s - t - m * K
            acc += math.exp(-d * d * inv)
        ps.append(acc)
    z = sum(ps)
    return [x / z for x in ps]


def analyze(r):
    sigma = S0 * (r ** 0.5)              # budgeted precision (the interior-optimum regime)
    targets = [round(j * K / r) % K for j in range(r)]
    conds = [blur_dist(t, sigma) for t in targets]
    ps = [sum(c[s] for c in conds) / len(conds) for s in range(K)]
    HS = entropy(ps)
    HSA = sum(entropy(c) for c in conds) / len(conds)
    E = HS - HSA
    phi_n = 1.0 - HSA / HMAX
    nu_n = HS / HMAX
    # survival precision: prob of landing within +/-TOL of the intended target
    t0 = targets[0]
    hit = sum(conds[0][(t0 + dd) % K] for dd in range(-TOL, TOL + 1))
    return {"r": r, "E": E, "phi_n": phi_n, "nu_n": nu_n, "hit": hit}


def classify(phi, nu):
    if abs(phi - nu) < 0.08:
        return "BALANCED"
    return "reach-dominated" if nu > phi else "precision-dominated"


def cost_models(d):
    return {
        "A:1-phi_n (entropy incoherence)": 1.0 - d["phi_n"],
        "B:1-hit (miss the target)": 1.0 - d["hit"],
        "C:(1-hit)^2 (steep miss)": (1.0 - d["hit"]) ** 2,
    }


if __name__ == "__main__":
    print(f"K={K} S0={S0} budgeted precision sigma=S0*sqrt(r); base_death={BASE_DEATH}\n")
    rows = [analyze(r) for r in range(1, K + 1)]

    print("STRUCTURE of the achievable reach/precision set (why balance is hard):")
    print(f"{'r':>3} {'E':>5} {'phi_n':>6} {'nu_n':>6} {'hit':>5}  regime")
    for d in [x for x in rows if x["r"] in (1, 2, 3, 4, 6, 8, 16, 32)]:
        print(f"{d['r']:>3} {d['E']:5.2f} {d['phi_n']:6.3f} {d['nu_n']:6.3f} {d['hit']:5.2f}  "
              f"{classify(d['phi_n'], d['nu_n'])}")
    # the most-balanced point and its empowerment
    mb = min(rows, key=lambda d: abs(d["phi_n"] - d["nu_n"]))
    e0 = max(rows, key=lambda d: d["E"])
    print(f"\n  most-balanced point: r={mb['r']}, |phi-nu|={abs(mb['phi_n']-mb['nu_n']):.3f}, "
          f"E={mb['E']:.2f}   <- note its empowerment")
    print(f"  empowerment-optimum: r={e0['r']}, E={e0['E']:.2f}, "
          f"phi={e0['phi_n']:.3f} nu={e0['nu_n']:.3f} ({classify(e0['phi_n'],e0['nu_n'])})")
    print(f"  => balance sits at the {'LOW-empowerment' if mb['E'] < 0.5*e0['E'] else 'high-E'} "
          f"end of the achievable set.\n")

    print("empowerment-UNDER-MORTALITY optimum, three principled cost models x mu sweep:")
    any_balanced = {}
    for label in cost_models(rows[0]):
        print(f"\n  cost = {label}")
        print(f"  {'mu':>6} | {'r*':>3} {'phi_n':>6} {'nu_n':>6} {'E':>5} | regime")
        balanced_at = None
        for mu in MUS:
            best = None
            for d in rows:
                death = BASE_DEATH + mu * cost_models(d)[label]
                V = d["E"] / death
                if best is None or V > best[0]:
                    best = (V, d)
            d = best[1]
            reg = classify(d["phi_n"], d["nu_n"])
            if reg == "BALANCED" and balanced_at is None:
                balanced_at = mu
            print(f"  {mu:6.2f} | {d['r']:>3} {d['phi_n']:6.3f} {d['nu_n']:6.3f} "
                  f"{d['E']:5.2f} | {reg}")
        any_balanced[label] = balanced_at

    print("\nverdict (F-R6-4: does a mortality cost recover the balanced equator?):")
    for label, m in any_balanced.items():
        print(f"  {label:40s} -> {'balance at mu~'+str(m) if m is not None else 'NEVER balanced'}")
    if all(m is None for m in any_balanced.values()):
        print("  ROBUST NEGATIVE: no principled mortality cost recovers balance. The "
              "balanced point is empowerment-dead (E~0), so an empowerment-based\n"
              "  objective -- even gated by mortality -- structurally cannot prefer it. "
              "F-R6-4 falsified; the corpus's equator is NOT an empowerment attractor.")

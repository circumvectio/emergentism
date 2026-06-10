#!/usr/bin/env python3
"""
R7 -- does cooperation emerge from SELF-INTEREST as a function of time horizon?

Direct test of the founder's "greatest conjecture", claim 4:
  "Pure self-interest leads to objective morality given a LONG time horizon
   (the 2 gods), and immorality given a SHORT time horizon (the 2 demons),
   under the power-max lemma, maximizing the individual's potential light cone."

Unlike R3 (where GIVE/TAKE were imposed policies), here agents are evolutionary
STRATEGIES competing on their own survival/welfare. We ask: under what conditions
does selection -- pure self-interest -- favor the cooperator (the 'god') over the
defector (the 'demon')?

The mechanism that could make giving self-interested is the corpus's own claim:
the individual's reachable future (light cone) is LARGER when the collective
survives. We model this as a SHARED-FATE COUPLING beta: each agent's regeneration
rate scales with (living fraction)^beta -- your opportunity to recover grows with
how many co-actors remain alive (cf. Wissner-Gross & Freer 2013: future-path-
maximization yields cooperation). beta=0 is the isolated world (no coupling);
beta>0 is the coupled world.

TIME HORIZON is set by the regeneration regime -- how long an agent can persist,
i.e. how long the shadow of the future is:
  SHORT horizon: no regeneration -- everyone descends to death; consequences are
                 short-lived (your help to others rarely returns to you).
  LONG horizon:  regeneration can outrun drift above a threshold -- agents persist,
                 so the future in which cooperation pays off actually arrives.

Strategies:
  COOPERATOR ('god'): each step pays cost c into a pool redistributed to the
                      neediest living agents (raises living fraction -> raises
                      everyone's regen via beta).
  DEFECTOR  ('demon'): pays nothing, receives pool share like everyone.

We measure, in MIXED 50/50 populations:
  - final cooperator fraction (does self-interested selection favor the god?)
  - each strategy's mean lifetime welfare (is being moral individually rational?)
across the 2x2 of {SHORT, LONG} horizon x {beta=0 isolated, beta=1.5 coupled}.

REGISTERED PREDICTIONS (2026-06-10, pre-run), stated so the test can fail:
  P1: In the LONG+COUPLED cell, cooperators win selection AND out-earn defectors
      -> the conjecture holds: long-horizon self-interest is moral.
  P2: In SHORT horizon (any beta), defectors win -> demons rule the short horizon.
  P3: In LONG+ISOLATED (beta=0), defectors win despite the long horizon
      -> THE HIDDEN PRECONDITION: the conjecture needs the light-cone/collective
         coupling, not merely a long horizon. (If P3 fails and coops win even
         uncoupled, the mechanism is something other than shared-fate.)
  The honest headline either way: name the precondition the conjecture omits.

Stdlib only. Deterministic given SEEDS.
"""

import random
import statistics

N = 200
T = 800
DRIFT = 0.004
DEATH = 0.0
START_LO, START_HI = 0.25, 0.95
COST = 0.010              # cooperator's per-step contribution (health units)
B_REG = 0.5               # regeneration threshold (health)
REGEN_BASE = 0.010        # base regen rate above threshold in LONG regime
HORIZONS = {"SHORT": 0.0, "LONG": REGEN_BASE}   # base regen rate
COUPLINGS = {"ISOLATED": 0.0, "COUPLED": 1.5}   # beta
POOL_TARGETS = 10         # neediest agents that share the pool each step
SEEDS = range(16)


def welfare(h):
    return max(0.0, h)     # welfare linear in health (R3 v3 showed results are
                           # trajectory- not curvature-driven; linear is cleanest)


def run(beta, regen_base, seed, coop_frac=0.5):
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

        # 1. drift + regeneration (regen gated by threshold, scaled by coupling)
        for i in living:
            h[i] -= DRIFT
            if h[i] > B_REG:
                h[i] += regen_base * (frac ** beta)

        # 2. cooperators contribute to a pool; pool redistributed to neediest
        pool = 0.0
        for i in living:
            if is_coop[i] and h[i] > COST:
                h[i] -= COST
                pool += COST
        if pool > 0:
            neediest = sorted([i for i in living if alive[i]], key=lambda i: h[i])[:POOL_TARGETS]
            if neediest:
                share = pool / len(neediest)
                for i in neediest:
                    h[i] += share

        # 3. deaths + welfare accrual
        for i in living:
            if h[i] <= DEATH:
                alive[i] = False
            else:
                lifetime_w[i] += welfare(h[i])

    coop_alive = sum(1 for i in range(N) if alive[i] and is_coop[i])
    def_alive = sum(1 for i in range(N) if alive[i] and not is_coop[i])
    coop_w = [lifetime_w[i] for i in range(N) if is_coop[i]]
    def_w = [lifetime_w[i] for i in range(N) if not is_coop[i]]
    final_living = coop_alive + def_alive
    return {
        "coop_surv": coop_alive / born_coop if born_coop else 0,
        "def_surv": def_alive / born_def if born_def else 0,
        "coop_frac_final": coop_alive / final_living if final_living else 0,
        "coop_w": statistics.mean(coop_w) if coop_w else 0,
        "def_w": statistics.mean(def_w) if def_w else 0,
        "total_w": sum(lifetime_w),
    }


def agg(rows, key):
    return statistics.mean(r[key] for r in rows)


if __name__ == "__main__":
    print(f"N={N} T={T} drift={DRIFT} cost={COST} B_reg={B_REG} "
          f"regen_base={REGEN_BASE} pool_targets={POOL_TARGETS} seeds={len(list(SEEDS))}")
    print("Mixed 50/50 cooperator/defector populations. Selection = pure survival/welfare.\n")
    print(f"{'horizon':7s} {'coupling':9s} | {'coop_surv':>9s} {'def_surv':>9s} | "
          f"{'final coop%':>11s} | {'coop_welf':>9s} {'def_welf':>9s} | {'winner':>10s}")
    print("-" * 92)
    for hname, regen in HORIZONS.items():
        for cname, beta in COUPLINGS.items():
            rows = [run(beta, regen, s) for s in SEEDS]
            cs, ds = agg(rows, "coop_surv"), agg(rows, "def_surv")
            cf = agg(rows, "coop_frac_final")
            cw, dw = agg(rows, "coop_w"), agg(rows, "def_w")
            # winner by individual welfare (is being moral individually rational?)
            if abs(cw - dw) < 0.02 * max(cw, dw, 1):
                winner = "tie"
            else:
                winner = "COOP(god)" if cw > dw else "DEF(demon)"
            print(f"{hname:7s} {cname:9s} | {cs:9.2%} {ds:9.2%} | {cf:11.2%} | "
                  f"{cw:9.1f} {dw:9.1f} | {winner:>10s}")
    print("\nP1 long+coupled -> COOP wins | P2 short -> DEF wins | "
          "P3 long+isolated -> DEF wins (the omitted precondition)")

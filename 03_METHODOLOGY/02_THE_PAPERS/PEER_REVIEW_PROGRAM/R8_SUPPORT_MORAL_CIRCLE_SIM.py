#!/usr/bin/env python3
"""
R8 -- moral-circle radius, symbiosis, and time horizon.

Tests the founder's claim: morality = the radius of the boundary across which you
externalize entropy (Singer's expanding circle in thermodynamic terms), PLUS the
symbiont/replicator-stack extension: parasitism vs mutualism is a TIME-HORIZON
strategy, because longer-horizon agents live long enough to eat their own
externalities. geno < pheno < extended-pheno < meme < egregore in horizon ->
predicted increasing pressure toward mutualism up the replicator stack.

Operationalization. A "moral-circle radius" is encoded as a parasitism level
p in [0,1] (inverse circle): each agent must dispose of E entropy per step.
  - INTERNALIZE fraction (1-p): pay a direct health cost kappa*(1-p)*E now
    (clean up after yourself; the substrate stays pristine). = MUTUALIST end.
  - EXTERNALIZE fraction p: dump p*E into the LOCAL shared substrate, spread over
    a neighborhood of radius w (pollute the commons you and your neighbors live
    in). = PARASITE end.
So p high = small moral circle (self only) = parasite; p low = large circle
(the commons is inside your circle) = mutualist; p mid = commensal.

The return mechanism (why externalities come back): agents are STATIC on a ring;
regeneration depends on LOCAL substrate quality g/G0; pollution lowers g locally;
g recovers slowly and diffuses. So over a long enough horizon your own
neighborhood's degradation lowers your own regeneration -- you eat your pollution.

TIME HORIZON is set by the regeneration regime (as in R7): SHORT = no regen
(agents descend and die in a few hundred steps, before the commons fully crashes);
LONG = regen can sustain agents (so substrate dynamics reach into each agent's
own future).

REGISTERED PREDICTIONS (2026-06-10, pre-run), stated so the test can fail:
  P1: SHORT horizon -> high p (parasite / small circle) earns most: you avoid the
      internalization cost and die before the commons crash bites.
  P2: LONG horizon -> low p (mutualist / large circle) earns most: you live long
      enough that local degradation crushes your own regeneration.
  P3: The optimal p DECREASES monotonically as horizon lengthens -> a critical
      horizon tau* (the externality return time) above which morality (a larger
      circle) becomes the self-interested strategy. This tau* is the gods/demons
      boundary for THIS mechanism, distinct from R7's reciprocity boundary.
  P4 (invasion / evolutionary stability): at LONG horizon, a mutualist world
      resists parasite invasion AND mutualists invade a parasite world; at SHORT
      horizon, the reverse. Map horizon -> replicator level: parasitism is the
      short-horizon (gene-like) strategy, mutualism the long-horizon (egregore-
      like) strategy. If the flip does NOT occur, the moral-circle/horizon claim
      is false in this model and we say so.
  Honest control C0: if regen is DECOUPLED from substrate (pollution harmless),
      parasites must win at every horizon -- isolating substrate-return as the
      necessary precondition (the analogue of R7's reciprocity precondition).

Stdlib only. Deterministic given SEEDS.
"""

import random
import statistics

N = 200                 # agents on a ring
T = 900
DRIFT = 0.004
DEATH = 0.0
START_LO, START_HI = 0.30, 0.95
B_REG = 0.5
E_ENTROPY = 0.020       # entropy each agent must dispose of per step
KAPPA = 0.30            # health cost per unit internalized entropy.
                        # MUST be tuned so internalization is survivable: the
                        # mutualist's per-step cost KAPPA*E (=0.006) must be < the
                        # max regen REGEN_BASE (=0.012), else "clean up after
                        # yourself" is fatal by construction and the test is void
                        # (the v1 bug: KAPPA=1.0 gave cost 0.020 > regen 0.012).
W = 2                   # pollution spread radius (neighbors hit on each side)
G0 = 1.0                # max substrate quality
RHO = 0.020             # substrate recovery rate toward G0
DEPLETE = 1.6           # substrate lost per unit externalized entropy
DIFFUSE = 0.10          # substrate diffusion coefficient along the ring
REGEN_BASE = 0.012      # base regeneration above threshold, scaled by g/G0
HORIZONS = {"SHORT": 0.0, "MED": 0.006, "LONG": REGEN_BASE}
P_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
SEEDS = range(12)


def simulate(p_of_agent, regen_base, seed, substrate_coupled=True):
    rng = random.Random(seed)
    h = [rng.uniform(START_LO, START_HI) for _ in range(N)]
    g = [G0] * N
    alive = [True] * N
    lifetime_w = [0.0] * N
    for t in range(T):
        # substrate recovery + ring diffusion
        newg = g[:]
        for i in range(N):
            left, right = g[(i - 1) % N], g[(i + 1) % N]
            newg[i] = g[i] + RHO * (G0 - g[i]) + DIFFUSE * (left + right - 2 * g[i])
            newg[i] = min(G0, max(0.0, newg[i]))
        g = newg

        any_alive = False
        for i in range(N):
            if not alive[i]:
                continue
            any_alive = True
            h[i] -= DRIFT
            quality = (g[i] / G0) if substrate_coupled else 1.0
            if h[i] > B_REG:
                h[i] += regen_base * quality
            p = p_of_agent[i]
            # internalize cost
            h[i] -= KAPPA * (1.0 - p) * E_ENTROPY
            # externalize: pollute local neighborhood
            if p > 0:
                load = (p * E_ENTROPY * DEPLETE) / (2 * W + 1)
                for dj in range(-W, W + 1):
                    j = (i + dj) % N
                    g[j] = max(0.0, g[j] - load)

        if not any_alive:
            break
        for i in range(N):
            if alive[i]:
                if h[i] <= DEATH:
                    alive[i] = False
                else:
                    lifetime_w[i] += max(0.0, h[i])
    return lifetime_w, alive


def monomorphic(p, regen_base, coupled=True):
    rows = []
    for s in SEEDS:
        lw, _ = simulate([p] * N, regen_base, s, coupled)
        rows.append(statistics.mean(lw))
    return statistics.mean(rows)


def invasion(resident_p, mutant_p, regen_base):
    """10% mutants among 90% residents; return (mutant_welf, resident_welf)."""
    mut_w, res_w = [], []
    for s in SEEDS:
        rng = random.Random(1000 + s)
        is_mut = [rng.random() < 0.10 for _ in range(N)]
        p_of = [mutant_p if is_mut[i] else resident_p for i in range(N)]
        lw, _ = simulate(p_of, regen_base, s)
        mw = [lw[i] for i in range(N) if is_mut[i]]
        rw = [lw[i] for i in range(N) if not is_mut[i]]
        if mw:
            mut_w.append(statistics.mean(mw))
        if rw:
            res_w.append(statistics.mean(rw))
    return statistics.mean(mut_w), statistics.mean(res_w)


if __name__ == "__main__":
    print(f"N={N} T={T} drift={DRIFT} E={E_ENTROPY} kappa={KAPPA} w={W} "
          f"deplete={DEPLETE} diffuse={DIFFUSE} regen_base(LONG)={REGEN_BASE} "
          f"seeds={len(list(SEEDS))}")
    print("p = parasitism (inverse moral-circle radius). p=0 mutualist, p=1 parasite.\n")

    print("=== A. MONOMORPHIC: mean lifetime welfare by (horizon x p); * = best p in row ===")
    print(f"{'horizon':7s} | " + "".join(f"p={p:<6.2f}" for p in P_LEVELS) + "  optimal p")
    for hname, regen in HORIZONS.items():
        vals = [monomorphic(p, regen) for p in P_LEVELS]
        best = P_LEVELS[max(range(len(vals)), key=lambda k: vals[k])]
        cells = "".join(f"{v:8.0f}" for v in vals)
        print(f"{hname:7s} | {cells}   optimal p = {best}")

    print("\n=== B. CONTROL C0 (substrate DECOUPLED -- pollution harmless): parasite must win ===")
    for hname, regen in HORIZONS.items():
        vals = [monomorphic(p, regen, coupled=False) for p in P_LEVELS]
        best = P_LEVELS[max(range(len(vals)), key=lambda k: vals[k])]
        print(f"{hname:7s} | " + "".join(f"{v:8.0f}" for v in vals) + f"   optimal p = {best}")

    print("\n=== C. INVASION (evolutionary stability): mutant vs resident, 10% mutants ===")
    print(f"{'horizon':7s} {'resident':9s} {'mutant':7s} | {'mut_welf':>8s} {'res_welf':>8s} | invader wins?")
    scenarios = [("MUTUALIST", 0.0, "PARASITE", 1.0), ("PARASITE", 1.0, "MUTUALIST", 0.0)]
    for hname, regen in HORIZONS.items():
        for rname, rp, mname, mp in scenarios:
            mw, rw = invasion(rp, mp, regen)
            wins = "YES (mutant invades)" if mw > rw * 1.02 else ("no (resident stable)" if rw > mw * 1.02 else "tie")
            print(f"{hname:7s} {rname:9s} {mname:7s} | {mw:8.0f} {rw:8.0f} | {wins}")
        print()
    print("P1 short->high p | P2 long->low p | P3 optimal p falls with horizon | "
          "P4 long: mutualist stable+invades; short: parasite stable+invades")

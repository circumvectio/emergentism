#!/usr/bin/env python3
"""
R9 -- "a basket of parasites can never be a holobiont": multilevel selection.

R7/R8 showed parasites WIN the within-group invasion. The founder's deeper claim:
they lose the war. A basket of parasites consumes itself; only a basket of
mutualists (symbionts) can integrate into a HOLOBIONT -- a higher-order
individual (Margulis endosymbiosis; Maynard Smith & Szathmary, major evolutionary
transitions; Wilson-Sober multilevel selection; virulence evolution / the
'prudent parasite'). The next level of individuality just IS the suppression of
within-level parasitism, so it can only be built from mutualists.

This adds GROUP STRUCTURE to R8. M demes, each a well-mixed group with its own
shared substrate. Within a deme, R8 ecology runs: parasites (p high) avoid the
internalization cost but pollute the deme substrate; mutualists (p low) pay the
cost but keep the substrate clean; substrate quality drives regeneration.
Generations: agents reproduce proportional to lifetime welfare (fitness),
offspring inherit strategy p with small mutation; with MIGRATION rate m, an
offspring is placed in a random deme (horizontal transmission) instead of its
parent's deme (vertical transmission). A deme overrun by parasites collapses
(substrate crashes -> low fitness -> contributes few offspring locally -> its
slots are refilled by migrants from successful mutualist demes = differential
group extinction + recolonization).

The migration rate m is the control: low m = strong group structure (vertical
transmission; group selection can act); high m = well-mixed (recovers R8, where
parasites win).

REGISTERED PREDICTIONS (2026-06-10, pre-run), stated so the test can fail:
  P1: At LOW migration, mutualism persists or dominates globally across
      generations -- group selection (differential deme extinction) beats the
      within-deme parasite advantage. At HIGH migration, parasites take over
      (R8 recovered). => a critical migration m* (the boundary between "parasites
      win" and "the holobiont forms").
  P2 (the holobiont claim): persistent high-welfare demes are mutualist-dominated
      and stable across generations ("baskets of symbionts" = holobionts);
      parasite-dominated demes are transient -- they spike in parasite fraction
      then collapse (self-terminate). A deme never persists as a stable
      high-welfare parasite basket.
  P3: total system welfare across generations is higher at low migration (the
      holobiont regime) than high migration (the parasite regime) -- integration
      pays at the system level.
  If mutualism is wiped out at ALL migration rates, the holobiont claim is false
      in this model and we say so. (Honest failure mode: if even m=0 lets
      parasites fixate, group selection is too weak here -- report it.)

Stdlib only. Deterministic given SEEDS.
"""

import random
import statistics

M_DEMES = 30
N_PER = 20
GENERATIONS = 40
T_ECO = 300
DRIFT = 0.006
DEATH = 0.0
START_LO, START_HI = 0.35, 0.95
B_REG = 0.5
E_ENTROPY = 0.020
KAPPA = 0.30            # internalization cost (cost 0.006 < regen 0.012; survivable)
REGEN_BASE = 0.012
G0 = 1.0
RHO = 0.020            # deme substrate recovery
DEPLETE = 0.9          # substrate lost per unit externalized entropy (per-deme, well-mixed)
MUT_RATE = 0.05        # strategy mutation probability per birth
MUT_STEP = 0.20        # mutation magnitude
MIGRATIONS = (0.0, 0.02, 0.10, 0.40)
SEEDS = range(8)


def run_deme_eco(p_vals, rng):
    """One ecological generation for one deme. Returns per-agent fitness."""
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
        g = max(0.0, g - pollution / n)
        if not any_alive:
            break
        for i in range(n):
            if alive[i]:
                if h[i] <= DEATH:
                    alive[i] = False
                else:
                    fit[i] += max(0.0, h[i])
    return fit


def weighted_choice(items, weights, rng):
    total = sum(weights)
    if total <= 0:
        return rng.choice(items)
    r = rng.random() * total
    acc = 0.0
    for it, w in zip(items, weights):
        acc += w
        if r <= acc:
            return it
    return items[-1]


def run(migration, seed, init_parasite_frac=0.5):
    rng = random.Random(seed)
    # init: each deme N_PER agents, strategy 0 (mutualist) or 1 (parasite)
    demes = [[1.0 if rng.random() < init_parasite_frac else 0.0
              for _ in range(N_PER)] for _ in range(M_DEMES)]
    history = []
    holobiont_counts = []
    for gen in range(GENERATIONS):
        # ecology: fitness per agent per deme
        deme_fit = [run_deme_eco(demes[d], rng) for d in range(M_DEMES)]
        # global pool for migrants
        global_parents = [(d, i) for d in range(M_DEMES) for i in range(N_PER)]
        global_w = [deme_fit[d][i] for (d, i) in global_parents]

        # record stats (this generation's realized state)
        all_p = [p for deme in demes for p in deme]
        mean_p = statistics.mean(all_p)
        # holobiont = deme that is mutualist-dominated AND high-fitness
        holo = 0
        for d in range(M_DEMES):
            mp = statistics.mean(demes[d])
            mf = statistics.mean(deme_fit[d])
            if mp < 0.30 and mf > 50:
                holo += 1
        history.append(mean_p)
        holobiont_counts.append(holo)

        # reproduction -> next generation
        new_demes = []
        for d in range(M_DEMES):
            local_parents = list(range(N_PER))
            local_w = deme_fit[d]
            new_deme = []
            for _ in range(N_PER):
                if rng.random() < migration:
                    pd, pi = weighted_choice(global_parents, global_w, rng)
                    parent_p = demes[pd][pi]
                else:
                    pi = weighted_choice(local_parents, local_w, rng)
                    parent_p = demes[d][pi]
                child = parent_p
                if rng.random() < MUT_RATE:
                    child += rng.choice([-1, 1]) * MUT_STEP
                    child = min(1.0, max(0.0, child))
                new_deme.append(child)
            new_demes.append(new_deme)
        demes = new_demes

    final_mean_p = history[-1]
    final_holo = holobiont_counts[-1]
    # total system welfare in the final generation
    final_fit = sum(sum(run_deme_eco(demes[d], rng)) for d in range(M_DEMES))
    return final_mean_p, final_holo, final_fit, history


if __name__ == "__main__":
    print(f"M={M_DEMES} demes x N={N_PER} | generations={GENERATIONS} eco_steps={T_ECO} "
          f"| kappa={KAPPA} deplete={DEPLETE} mut={MUT_RATE} seeds={len(list(SEEDS))}")
    print("Init 50% parasite. p=0 mutualist (symbiont), p=1 parasite. "
          "Holobiont = deme mutualist-dominated (mean p<0.30) AND high-fitness.\n")
    print(f"{'migration':9s} | {'final mean p':>12s} | {'holobiont demes':>15s} | "
          f"{'final sys welfare':>17s} | outcome")
    print("-" * 86)
    for mig in MIGRATIONS:
        rows = [run(mig, s) for s in SEEDS]
        mp = statistics.mean(r[0] for r in rows)
        holo = statistics.mean(r[1] for r in rows)
        fit = statistics.mean(r[2] for r in rows)
        outcome = ("SYMBIONT/holobiont regime" if mp < 0.4 else
                   "parasite regime" if mp > 0.6 else "mixed")
        print(f"{mig:9.2f} | {mp:12.2f} | {holo:13.1f}/{M_DEMES} | {fit:17.0f} | {outcome}")

    print("\n=== trajectory of mean parasitism over generations (lowest migration) ===")
    _, _, _, hist = run(MIGRATIONS[0], 0)
    pts = [hist[k] for k in range(0, GENERATIONS, max(1, GENERATIONS // 12))]
    print("gen:  " + " ".join(f"{k:5d}" for k in range(0, GENERATIONS, max(1, GENERATIONS // 12))))
    print("p̄  :  " + " ".join(f"{v:5.2f}" for v in pts))
    print("\nP1 low mig -> mutualism persists (group selection) | "
          "P2 persistent high-welfare demes are mutualist (holobionts) | "
          "P3 low mig -> higher system welfare")

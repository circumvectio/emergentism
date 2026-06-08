#!/usr/bin/env python3
"""
R* Extraction Threshold Simulation v2
======================================
Agent-based model testing the Emergentism conjecture R* ~ 1.5:
  "When parasitic extraction exceeds 1.5 x Phi_base, host collapse
   becomes inevitable."

Evidence tier: [C] Conjecture -- until results are verified.

Model:
  - N agents on a square lattice (configurable topology)
  - Each agent has coordinates (phi_i, nu_i) satisfying phi_i * nu_i = 1
  - "Host" agents have equatorial restoring force F = -dH/dphi
  - "Parasitic" agents extract Delta_nu from neighbors each timestep
  - Balance function B(nu) = 2*nu / (1 + nu^2) is the fitness function
  - Fermi update rule for strategy imitation

Key outputs:
  - Survival probability of hosts
  - Time-to-collapse
  - Phase transition identification: critical extraction rate eta_c
  - Test: does eta_c relate to R* ~ 1.5 x Phi_base?

Usage:
  python r_star_simulation_v2.py --N 100 --eta 1.5 --parasites 10
  python r_star_simulation_v2.py --sweep
  python r_star_simulation_v2.py --sweep --quick

Dependencies: Python 3.8+, NumPy (only).
"""

import argparse
import csv
import sys
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def balance(nu: np.ndarray) -> np.ndarray:
    """B(nu) = 2*nu / (1 + nu^2). Peaks at nu=1 where B=1."""
    return 2.0 * nu / (1.0 + nu * nu)


def phi_from_nu(nu: np.ndarray) -> np.ndarray:
    """Constraint: phi * nu = 1, so phi = 1/nu."""
    return 1.0 / nu


def restoring_force(nu: np.ndarray, strength: float = 0.1) -> np.ndarray:
    """
    Equatorial restoring force.

    The Hamiltonian is H = -B(nu) = -2*nu/(1+nu^2).
    dH/dnu = -2(1 - nu^2)/(1 + nu^2)^2.
    Force F = -dH/dnu = 2(1 - nu^2)/(1 + nu^2)^2.

    This pushes nu toward 1 (the equator):
      nu < 1 => F > 0 (push nu up)
      nu > 1 => F < 0 (push nu down)
      nu = 1 => F = 0 (equilibrium)
    """
    denom = (1.0 + nu * nu) ** 2
    return strength * 2.0 * (1.0 - nu * nu) / denom


# ---------------------------------------------------------------------------
# Network topology
# ---------------------------------------------------------------------------

def build_square_lattice_neighbors(side: int) -> List[List[int]]:
    """
    Build von Neumann (4-connected) neighbor list for a side x side
    square lattice with periodic boundaries.
    Returns list of lists: neighbors[i] = [j1, j2, j3, j4].
    """
    N = side * side
    neighbors = [[] for _ in range(N)]
    for r in range(side):
        for c in range(side):
            idx = r * side + c
            # up, down, left, right with periodic wrapping
            neighbors[idx] = [
                ((r - 1) % side) * side + c,
                ((r + 1) % side) * side + c,
                r * side + (c - 1) % side,
                r * side + (c + 1) % side,
            ]
    return neighbors


# ---------------------------------------------------------------------------
# Simulation engine
# ---------------------------------------------------------------------------

@dataclass
class SimConfig:
    """Configuration for a single simulation run."""
    N: int = 100                   # total agents (will use sqrt(N) x sqrt(N) lattice)
    eta_extract: float = 1.5       # extraction rate (fraction of host nu taken)
    n_parasites: int = 10          # number of parasitic agents
    timesteps: int = 500           # max timesteps
    restoring_strength: float = 0.1  # strength of equatorial restoring force
    kT: float = 0.1                # Fermi update noise (selection intensity)
    seed: int = 42
    collapse_threshold: float = 0.3  # nu below this = collapsed
    topology: str = "square"       # only "square" for now


@dataclass
class SimResult:
    """Results from a single simulation run."""
    config: SimConfig
    host_survival_frac: float      # fraction of hosts surviving at end
    time_to_collapse: int          # timestep where >50% hosts collapsed (-1 if never)
    mean_nu_trajectory: list       # mean nu of hosts over time
    mean_phi_nu_product: list      # mean phi*nu product over time (should stay ~1)
    mean_balance_trajectory: list  # mean B(nu) over time
    parasite_nu_trajectory: list   # mean nu of parasites over time
    final_host_nu: float           # mean nu of surviving hosts
    final_parasite_nu: float       # mean nu of parasites at end
    collapsed: bool                # did majority of hosts collapse?


def run_single(cfg: SimConfig) -> SimResult:
    """
    Run one simulation with the given configuration.

    Model:
      - All agents start at equator: nu_i = 1, phi_i = 1.
      - Parasites are randomly placed on the lattice.
      - Each timestep:
        1. Parasites extract eta_extract * (1/n_neighbors) from each neighbor's nu
        2. Hosts apply restoring force toward equator
        3. phi is updated to maintain phi*nu = 1
        4. Fermi imitation: agents may copy strategy of better-fit neighbor
        5. Record diagnostics
    """
    rng = np.random.default_rng(cfg.seed)

    # Determine lattice side (closest square <= N)
    side = int(np.sqrt(cfg.N))
    actual_N = side * side
    if actual_N != cfg.N:
        actual_N = side * side  # use perfect square

    # Build neighbor structure
    neighbors = build_square_lattice_neighbors(side)

    # Initialize all agents at equator
    nu = np.ones(actual_N, dtype=np.float64)
    # is_parasite: True = parasitic extractor, False = host
    is_parasite = np.zeros(actual_N, dtype=bool)
    parasite_indices = rng.choice(actual_N, size=min(cfg.n_parasites, actual_N), replace=False)
    is_parasite[parasite_indices] = True

    # Diagnostics
    host_mask = ~is_parasite
    n_hosts = host_mask.sum()
    mean_nu_hosts = []
    mean_phi_nu = []
    mean_balance = []
    mean_nu_parasites = []
    time_to_collapse = -1

    for t in range(cfg.timesteps):
        # --- Record diagnostics ---
        host_nu = nu[host_mask]
        para_nu = nu[is_parasite]

        mean_nu_hosts.append(float(np.mean(host_nu)) if len(host_nu) > 0 else 0.0)
        phi = phi_from_nu(nu)
        mean_phi_nu.append(float(np.mean(phi * nu)))
        mean_balance.append(float(np.mean(balance(host_nu))) if len(host_nu) > 0 else 0.0)
        mean_nu_parasites.append(float(np.mean(para_nu)) if len(para_nu) > 0 else 0.0)

        # Check collapse: >50% of hosts below threshold
        collapsed_hosts = np.sum(host_nu < cfg.collapse_threshold)
        if time_to_collapse == -1 and collapsed_hosts > n_hosts * 0.5:
            time_to_collapse = t

        # --- Step 1: Parasitic extraction ---
        # Each parasite takes eta_extract / n_neighbors from each neighbor's nu
        for p_idx in parasite_indices:
            nbrs = neighbors[p_idx]
            extraction_per_neighbor = cfg.eta_extract / len(nbrs)
            for n_idx in nbrs:
                # Only extract from hosts (or other parasites -- parasites are greedy)
                amount = min(extraction_per_neighbor, nu[n_idx] * 0.5)  # can't take more than half
                nu[n_idx] -= amount
                nu[p_idx] += amount * 0.5  # parasites only capture half (thermodynamic loss)

        # --- Step 2: Restoring force for hosts ---
        force = restoring_force(nu, cfg.restoring_strength)
        # Only hosts get restoring force
        nu[host_mask] += force[host_mask]

        # --- Step 3: Clamp nu to prevent pathological values ---
        nu = np.clip(nu, 0.01, 100.0)

        # --- Step 4: Fermi imitation ---
        # Each agent compares fitness with a random neighbor
        # and may switch strategy (host <-> parasite)
        fitness = balance(nu)
        new_parasite = is_parasite.copy()

        for i in range(actual_N):
            nbrs = neighbors[i]
            j = nbrs[rng.integers(len(nbrs))]
            # Fermi probability of adopting j's strategy
            delta_f = fitness[j] - fitness[i]
            prob = 1.0 / (1.0 + np.exp(-delta_f / cfg.kT))
            if rng.random() < prob:
                new_parasite[i] = is_parasite[j]

        is_parasite = new_parasite
        host_mask = ~is_parasite
        n_hosts = host_mask.sum()
        parasite_indices = np.where(is_parasite)[0]

        # If all agents become parasites or all become hosts, stop early
        if n_hosts == 0 or n_hosts == actual_N:
            # Fill remaining trajectory
            for _ in range(t + 1, cfg.timesteps):
                mean_nu_hosts.append(mean_nu_hosts[-1] if mean_nu_hosts else 0.0)
                mean_phi_nu.append(mean_phi_nu[-1] if mean_phi_nu else 1.0)
                mean_balance.append(mean_balance[-1] if mean_balance else 0.0)
                mean_nu_parasites.append(mean_nu_parasites[-1] if mean_nu_parasites else 0.0)
            break

    # Final diagnostics
    host_nu_final = nu[host_mask]
    para_nu_final = nu[is_parasite]
    surviving_hosts = np.sum(host_nu_final >= cfg.collapse_threshold) if len(host_nu_final) > 0 else 0
    survival_frac = surviving_hosts / max(n_hosts, 1)

    return SimResult(
        config=cfg,
        host_survival_frac=float(survival_frac),
        time_to_collapse=time_to_collapse,
        mean_nu_trajectory=mean_nu_hosts,
        mean_phi_nu_product=mean_phi_nu,
        mean_balance_trajectory=mean_balance,
        parasite_nu_trajectory=mean_nu_parasites,
        final_host_nu=float(np.mean(host_nu_final)) if len(host_nu_final) > 0 else 0.0,
        final_parasite_nu=float(np.mean(para_nu_final)) if len(para_nu_final) > 0 else 0.0,
        collapsed=time_to_collapse >= 0,
    )


# ---------------------------------------------------------------------------
# Sweep mode: find eta_c
# ---------------------------------------------------------------------------

def run_sweep(quick: bool = False, seed: int = 42) -> list:
    """
    Sweep across extraction rates and parasite fractions to find
    the critical extraction rate eta_c.

    Returns list of SimResult.
    """
    if quick:
        N_values = [64]
        eta_values = np.arange(0.0, 3.1, 0.5)
        parasite_fracs = [0.05, 0.10, 0.20]
        timesteps = 200
        n_trials = 2
    else:
        N_values = [100, 225]
        eta_values = np.arange(0.0, 3.1, 0.25)
        parasite_fracs = [0.05, 0.10, 0.20, 0.30, 0.50]
        timesteps = 500
        n_trials = 3

    results = []
    total_runs = len(N_values) * len(eta_values) * len(parasite_fracs) * n_trials
    run_count = 0

    print(f"Sweep: {total_runs} total runs")
    print(f"  N values: {N_values}")
    print(f"  eta values: {list(np.round(eta_values, 2))}")
    print(f"  parasite fractions: {parasite_fracs}")
    print(f"  timesteps: {timesteps}, trials per config: {n_trials}")
    print()

    for N in N_values:
        side = int(np.sqrt(N))
        actual_N = side * side
        for eta in eta_values:
            for p_frac in parasite_fracs:
                n_parasites = max(1, int(actual_N * p_frac))
                trial_results = []
                for trial in range(n_trials):
                    cfg = SimConfig(
                        N=actual_N,
                        eta_extract=float(eta),
                        n_parasites=n_parasites,
                        timesteps=timesteps,
                        seed=seed + trial * 1000 + int(eta * 100) + int(p_frac * 1000),
                    )
                    result = run_single(cfg)
                    trial_results.append(result)
                    run_count += 1

                    if run_count % 20 == 0:
                        print(f"  Progress: {run_count}/{total_runs} runs completed", flush=True)

                # Average over trials
                avg_survival = np.mean([r.host_survival_frac for r in trial_results])
                avg_collapse_time = np.mean([r.time_to_collapse for r in trial_results if r.time_to_collapse >= 0]) if any(r.time_to_collapse >= 0 for r in trial_results) else -1
                n_collapsed = sum(1 for r in trial_results if r.collapsed)

                results.append({
                    "N": actual_N,
                    "eta": float(eta),
                    "parasite_frac": p_frac,
                    "n_parasites": n_parasites,
                    "avg_survival": float(avg_survival),
                    "avg_collapse_time": float(avg_collapse_time),
                    "collapse_probability": n_collapsed / n_trials,
                    "avg_final_host_nu": float(np.mean([r.final_host_nu for r in trial_results])),
                    "avg_final_parasite_nu": float(np.mean([r.final_parasite_nu for r in trial_results])),
                    "avg_final_balance": float(np.mean([r.mean_balance_trajectory[-1] for r in trial_results])),
                })

    return results


def find_eta_c(results: list) -> dict:
    """
    Identify critical extraction rate eta_c where collapse probability
    crosses 0.5 for each (N, parasite_frac) combination.
    """
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in results:
        key = (r["N"], r["parasite_frac"])
        grouped[key].append(r)

    eta_c_results = {}
    for key, group in sorted(grouped.items()):
        group.sort(key=lambda x: x["eta"])
        etas = [g["eta"] for g in group]
        collapse_probs = [g["collapse_probability"] for g in group]

        # Find crossing point where collapse_probability crosses 0.5
        eta_c = None
        for i in range(1, len(etas)):
            if collapse_probs[i - 1] < 0.5 <= collapse_probs[i]:
                # Linear interpolation
                if collapse_probs[i] != collapse_probs[i - 1]:
                    eta_c = etas[i - 1] + (0.5 - collapse_probs[i - 1]) / (
                        collapse_probs[i] - collapse_probs[i - 1]
                    ) * (etas[i] - etas[i - 1])
                else:
                    eta_c = etas[i]
                break

        if eta_c is None:
            # Check if always or never collapsed
            if all(p >= 0.5 for p in collapse_probs):
                eta_c = 0.0  # collapses even at eta=0
            elif all(p < 0.5 for p in collapse_probs):
                eta_c = float("inf")  # never collapses in range

        eta_c_results[key] = {
            "eta_c": eta_c,
            "etas": etas,
            "collapse_probs": collapse_probs,
        }

    return eta_c_results


def save_results_csv(results: list, path: str):
    """Save sweep results to CSV."""
    if not results:
        return
    keys = results[0].keys()
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"  Results saved to {path}")


# ---------------------------------------------------------------------------
# Single run display
# ---------------------------------------------------------------------------

def display_single_result(result: SimResult):
    """Print a formatted summary of a single run."""
    cfg = result.config
    print()
    print("=" * 64)
    print("R* EXTRACTION THRESHOLD SIMULATION v2 — SINGLE RUN")
    print("=" * 64)
    print()
    print("Configuration:")
    print(f"  Agents (N):           {cfg.N} ({int(np.sqrt(cfg.N))}x{int(np.sqrt(cfg.N))} lattice)")
    print(f"  Extraction rate (eta): {cfg.eta_extract:.2f}")
    print(f"  Parasites:            {cfg.n_parasites} ({cfg.n_parasites/cfg.N*100:.1f}%)")
    print(f"  Timesteps:            {cfg.timesteps}")
    print(f"  Restoring strength:   {cfg.restoring_strength}")
    print(f"  Fermi noise (kT):     {cfg.kT}")
    print(f"  Collapse threshold:   nu < {cfg.collapse_threshold}")
    print(f"  Topology:             {cfg.topology} lattice")
    print()
    print("Results:")
    print(f"  Host survival fraction:    {result.host_survival_frac:.4f}")
    print(f"  Time to collapse:          {'never' if result.time_to_collapse < 0 else result.time_to_collapse}")
    print(f"  System collapsed:          {'YES' if result.collapsed else 'NO'}")
    print(f"  Final host mean nu:        {result.final_host_nu:.4f}")
    print(f"  Final parasite mean nu:    {result.final_parasite_nu:.4f}")
    print(f"  Final mean phi*nu product: {result.mean_phi_nu_product[-1]:.6f}")
    print()
    print("Trajectory (sampled every 10% of timesteps):")
    print(f"  {'Step':>6}  {'Host nu':>10}  {'Para nu':>10}  {'B(host)':>10}  {'phi*nu':>10}")
    n_points = len(result.mean_nu_trajectory)
    step = max(1, n_points // 10)
    for i in range(0, n_points, step):
        print(f"  {i:>6}  {result.mean_nu_trajectory[i]:>10.4f}  "
              f"{result.parasite_nu_trajectory[i]:>10.4f}  "
              f"{result.mean_balance_trajectory[i]:>10.4f}  "
              f"{result.mean_phi_nu_product[i]:>10.6f}")
    # Always show last
    i = n_points - 1
    print(f"  {i:>6}  {result.mean_nu_trajectory[i]:>10.4f}  "
          f"{result.parasite_nu_trajectory[i]:>10.4f}  "
          f"{result.mean_balance_trajectory[i]:>10.4f}  "
          f"{result.mean_phi_nu_product[i]:>10.6f}")
    print()


def display_sweep_results(results: list, eta_c_map: dict):
    """Print formatted sweep summary."""
    print()
    print("=" * 64)
    print("R* EXTRACTION THRESHOLD SIMULATION v2 — SWEEP RESULTS")
    print("=" * 64)
    print()

    # Phase transition table
    print("Phase Transition Table:")
    print(f"  {'N':>6}  {'Para%':>6}  {'eta_c':>8}  {'R* = 1.5?':>10}  {'Ratio eta_c/Phi':>16}")
    print(f"  {'---':>6}  {'---':>6}  {'---':>8}  {'---':>10}  {'---':>16}")

    Phi_base = 1.0  # Phi_base at equator = 1

    for (N, p_frac), data in sorted(eta_c_map.items()):
        eta_c = data["eta_c"]
        if eta_c is None or eta_c == float("inf"):
            eta_c_str = ">3.0"
            ratio_str = "N/A"
            match_str = "?"
        elif eta_c == 0.0:
            eta_c_str = "~0.0"
            ratio_str = "~0.0"
            match_str = "NO"
        else:
            eta_c_str = f"{eta_c:.2f}"
            ratio = eta_c / Phi_base
            ratio_str = f"{ratio:.2f}"
            match_str = "YES" if 1.2 <= ratio <= 1.8 else "NO"

        print(f"  {N:>6}  {p_frac*100:>5.0f}%  {eta_c_str:>8}  {match_str:>10}  {ratio_str:>16}")

    print()

    # Detailed collapse probability table
    print("Collapse Probability by eta and parasite fraction:")
    # Get unique values
    etas = sorted(set(r["eta"] for r in results))
    p_fracs = sorted(set(r["parasite_frac"] for r in results))
    Ns = sorted(set(r["N"] for r in results))

    for N in Ns:
        print(f"\n  N = {N}:")
        header = f"  {'eta':>6} |" + "".join(f" {pf*100:>5.0f}%" for pf in p_fracs)
        print(header)
        print(f"  {'---':>6} |" + "------" * len(p_fracs))

        for eta in etas:
            row = f"  {eta:>6.2f} |"
            for pf in p_fracs:
                match = [r for r in results if r["N"] == N and abs(r["eta"] - eta) < 0.01 and r["parasite_frac"] == pf]
                if match:
                    cp = match[0]["collapse_probability"]
                    row += f"  {cp:>4.2f} "
                else:
                    row += "   --- "
            print(row)

    print()

    # Assessment
    print("=" * 64)
    print("ASSESSMENT")
    print("=" * 64)
    print()

    # Check if any eta_c is near 1.5
    valid_eta_c = [d["eta_c"] for d in eta_c_map.values()
                   if d["eta_c"] is not None and d["eta_c"] != float("inf") and d["eta_c"] > 0]

    if valid_eta_c:
        mean_eta_c = np.mean(valid_eta_c)
        std_eta_c = np.std(valid_eta_c)
        print(f"  Mean eta_c across conditions: {mean_eta_c:.2f} +/- {std_eta_c:.2f}")
        print(f"  Phi_base (equatorial):        {Phi_base:.2f}")
        print(f"  Ratio eta_c / Phi_base:       {mean_eta_c/Phi_base:.2f}")
        print()

        if 1.2 <= mean_eta_c / Phi_base <= 1.8:
            print("  RESULT: eta_c ~ 1.5 x Phi_base  -- CONSISTENT with R* conjecture [C]")
            print("  The conjecture that extraction beyond 1.5x the host's coherent")
            print("  integration parameter causes inevitable collapse is SUPPORTED.")
        elif mean_eta_c / Phi_base < 1.2:
            print(f"  RESULT: eta_c < 1.5 x Phi_base  (actual: {mean_eta_c/Phi_base:.2f}x)")
            print("  The system is MORE fragile than R* ~ 1.5 predicts.")
            print("  Collapse occurs at lower extraction rates than conjectured.")
        else:
            print(f"  RESULT: eta_c > 1.5 x Phi_base  (actual: {mean_eta_c/Phi_base:.2f}x)")
            print("  The system is MORE resilient than R* ~ 1.5 predicts.")
            print("  Hosts can withstand higher extraction than conjectured.")
    else:
        print("  No valid eta_c found in sweep range.")
        print("  Either all configs collapsed (even eta=0) or none did.")

    print()
    print("  Evidence tier: [C] Conjecture")
    print("  Status: Awaiting independent replication.")
    print()
    print("  The balance function B(nu) = 2*nu/(1+nu^2) creates a coordination")
    print("  game where cooperation is universally dominant (confirmed by v1).")
    print("  This v2 simulation tests the EXTRACTION threshold specifically:")
    print("  at what rate does parasitic drain overwhelm the restoring force?")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="R* Extraction Threshold Simulation v2 (Emergentism framework)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  Single run:   python r_star_simulation_v2.py --N 100 --eta 1.5 --parasites 10
  Quick sweep:  python r_star_simulation_v2.py --sweep --quick
  Full sweep:   python r_star_simulation_v2.py --sweep
  Custom:       python r_star_simulation_v2.py --N 225 --eta 2.0 --parasites 20 --timesteps 1000
""",
    )
    parser.add_argument("--N", type=int, default=100,
                        help="Number of agents (rounded down to nearest perfect square, default: 100)")
    parser.add_argument("--eta", type=float, default=1.5,
                        help="Extraction rate of parasitic agents (default: 1.5)")
    parser.add_argument("--parasites", type=int, default=10,
                        help="Number of parasitic agents (default: 10)")
    parser.add_argument("--timesteps", type=int, default=500,
                        help="Max timesteps per run (default: 500)")
    parser.add_argument("--restoring", type=float, default=0.1,
                        help="Restoring force strength (default: 0.1)")
    parser.add_argument("--kT", type=float, default=0.1,
                        help="Fermi noise / selection intensity (default: 0.1)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--sweep", action="store_true",
                        help="Run full parameter sweep to find eta_c")
    parser.add_argument("--quick", action="store_true",
                        help="Use reduced parameters for faster sweep")
    parser.add_argument("--csv", type=str, default="/tmp/r_star_v2_results.csv",
                        help="Path to save CSV results (default: /tmp/r_star_v2_results.csv)")

    args = parser.parse_args()

    start_time = time.time()

    if args.sweep:
        print("=" * 64)
        print("R* EXTRACTION THRESHOLD SIMULATION v2 — PARAMETER SWEEP")
        print("=" * 64)
        print()

        results = run_sweep(quick=args.quick, seed=args.seed)
        eta_c_map = find_eta_c(results)
        save_results_csv(results, args.csv)
        display_sweep_results(results, eta_c_map)

    else:
        # Single run
        side = int(np.sqrt(args.N))
        actual_N = side * side

        cfg = SimConfig(
            N=actual_N,
            eta_extract=args.eta,
            n_parasites=min(args.parasites, actual_N),
            timesteps=args.timesteps,
            restoring_strength=args.restoring,
            kT=args.kT,
            seed=args.seed,
        )

        result = run_single(cfg)
        display_single_result(result)

        # Also save single-run trajectory to CSV
        traj_path = args.csv.replace(".csv", "_trajectory.csv")
        with open(traj_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestep", "host_mean_nu", "parasite_mean_nu",
                             "host_mean_balance", "phi_nu_product"])
            for t in range(len(result.mean_nu_trajectory)):
                writer.writerow([
                    t,
                    f"{result.mean_nu_trajectory[t]:.6f}",
                    f"{result.parasite_nu_trajectory[t]:.6f}",
                    f"{result.mean_balance_trajectory[t]:.6f}",
                    f"{result.mean_phi_nu_product[t]:.6f}",
                ])
        print(f"  Trajectory saved to {traj_path}")

    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.1f} seconds.")
    print()
    print("Evidence tier: [C] Conjecture -- awaiting independent replication.")
    print("The framework gives you instruments. If you can access phi directly,")
    print("you do not need this simulation. Put it down.")
    print()
    print("  ⊙ = • × ○")


if __name__ == "__main__":
    main()

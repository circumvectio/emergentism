---
rosetta:
  primary_level: L5
  primary_column: R-Star Simulation Design
  secondary:
    - level: L3
      column: Result Audit
      role: "route falsification and threshold measurements to the paired results paper"
    - level: L4
      column: Script Execution
      role: "keep run commands and dependency requirements explicit"
    - level: L6
      column: Conjecture Boundary
      role: "demote the R* percolation coincidence from active claim to tested conjecture"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/C]"
  canonical_phrase: "R* Cooperation Threshold Simulation"
title: "R* Cooperation Threshold Simulation"
status: "ACTIVE — simulation design note"
evidence_tier: "[B] for local script/run instructions; [S] for structural B(ν) payoff claims; [C] for the R*≈p_c conjecture, now partially falsified in paired results."
---

# R* Cooperation Threshold Simulation

## What This Tests

The Emergentism framework predicts a critical cooperation threshold **R\* ~ 0.60** on the Burri Sphere (S^2). Below this density, cooperation collapses to extinction; above it, cooperation becomes self-sustaining and goes to fixation.

This simulation tests whether that threshold coincides with the **site percolation threshold** on a 2D square lattice, commonly estimated numerically near **p_c = 0.5927...**

The hypothesis: cooperation becomes self-sustaining precisely when cooperators can form a spanning (percolating) cluster -- a connected path across the entire lattice. The geometry of the framework (B = sin theta peaking at the equator where phi = nu = 1) predicts this transition at R* ~ 0.60, which is within 1.2% of p_c.

Evidence tier: **[C] Conjecture — PARTIALLY FALSIFIED.** See `R_STAR_SIMULATION_RESULTS.md` for 2026-04-04 findings. The R* ≈ p_c numerical coincidence is NOT confirmed. However, the underlying result — that cooperation is universally dominant under B(ν) — IS confirmed [S].

> **Canon ground.** The `S²` geometry, `B = sin θ`, and the equator `φ = ν = 1` this simulation tests are owned by [`../../05_COSMOLOGY/00_THE_BURRISPHERE.md`](../../05_COSMOLOGY/00_THE_BURRISPHERE.md). The moral reading — cooperation is *coupling* (`η = 0`), extraction is *closure* (`η > 0`), sorted by the bond `φ × ν` and never by any pole or person — is [`../../05_COSMOLOGY/00_THE_DYADIC_COUPLING_LAW.md`](../../05_COSMOLOGY/00_THE_DYADIC_COUPLING_LAW.md). This note is a downstream test, not a re-statement of canon.

## How It Works

1. **Lattice**: N x N grid with periodic (toroidal) boundaries, von Neumann (4-connected) neighborhoods.

2. **Payoff function**: B(nu) = 2*nu / (1 + nu^2), derived from the balance function on S^2.
   - Cooperators sit at nu = 1 (the equator): B(1) = 1.0
   - Defectors extract Delta_nu from cooperating neighbors, gaining short-term viability but reducing overall balance
   - Crucially, B(1 + delta) < B(1): extraction is self-defeating

3. **Dynamics**: Fermi imitation rule -- each agent randomly selects a neighbor and copies their strategy with probability sigmoid(payoff_difference / kT).

4. **Measurement**: For each initial cooperation fraction p in [0, 1], run 1000 generations and record the final cooperation fraction. The critical threshold p* is where the sigmoid-like transition crosses 0.5.

5. **Percolation check**: At each final density, test whether cooperators form a spanning cluster (top-to-bottom or left-to-right).

## Requirements

- Python 3.8+
- numpy
- matplotlib

```bash
pip install numpy matplotlib
```

## Usage

Default run (100x100 grid, 1000 generations):

```bash
python r_star_simulation.py
```

Faster test run:

```bash
python r_star_simulation.py --grid_size 50 --generations 500 --trials 2
```

Full options:

```bash
python r_star_simulation.py \
    --grid_size 100 \
    --generations 1000 \
    --trials 3 \
    --seed 42 \
    --output /tmp/r_star_phase_diagram.png
```

## Output

- **Phase diagram** saved to `/tmp/r_star_phase_diagram.png` (or custom path via `--output`)
- **Console output** with measured p*, comparison to p_c and R*, and match assessment

## Interpreting Results

**2026-04-04 UPDATE: p* = 0.85, NOT 0.60.** The R* ≈ p_c conjecture is not confirmed at default parameters. The reason: B(ν) creates a *coordination game*, not a Prisoner's Dilemma. Cooperation is universally dominant (B(D|C) < B(C|C) for all Δν). The threshold p* is governed by noise (kT), not by a fundamental constant. See `R_STAR_SIMULATION_RESULTS.md` for full analysis.

- The green shaded region in the plot marks where spanning clusters exist.
- The three vertical lines show p_c (known), R* (predicted), and p* (measured).

## Caveats

- The payoff structure (Delta_nu = 0.3, kT = 0.1) affects the exact threshold. These are reasonable defaults but not uniquely determined by the framework.
- Finite-size effects: larger grids give sharper transitions closer to the thermodynamic limit.
- The percolation test at final density uses a random proxy; a direct cluster analysis on the evolved grid would be more precise.
- [C] This is one simulation geometry (square lattice). Any cross-lattice version of the prediction needs retesting with the appropriate threshold estimate and dynamics.

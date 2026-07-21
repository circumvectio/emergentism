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

This model tested a conjectured cooperation threshold **R\* ~ 0.60** in one
specified lattice simulation. It did not establish a universal Emergentist
threshold. Below or above the fitted threshold, extinction or fixation is an
outcome of this update rule and payoff specification only.

This simulation tests whether that threshold coincides with the **site percolation threshold** on a 2D square lattice, commonly estimated numerically near **p_c = 0.5927...**

The tested hypothesis was that cooperation becomes self-sustaining when
cooperators form a spanning cluster. The numerical proximity between the
chosen `R*` and the square-lattice site-percolation value motivated the test;
the reciprocal-chart geometry did not derive that lattice threshold.

Evidence tier: **[C] Conjecture — PARTIALLY FALSIFIED.** See
`R_STAR_SIMULATION_RESULTS.md` for the 2026-04-04 findings. The `R*≈p_c`
coincidence was not confirmed. Any dominance result is structural only inside
the implemented payoff and update rules; it is not a universal fact about
cooperation.

> **Canon ground.** The `S²` geometry, `B = sin θ`, and the equator `φ = ν = 1` this simulation tests are owned by [`../../05_COSMOLOGY/00_THE_BURRISPHERE.md`](../../05_COSMOLOGY/00_THE_BURRISPHERE.md). In this simulation, “cooperate” and “defect” are strategy labels and `η_observed` is a descriptive transfer measure. Neither the labels nor the sign of `η_observed` supplies a moral verdict. Emergentist value judgments require the separately declared, bearer-complete Justice envelope. This note is a downstream model test, not a restatement of canon.

## How It Works

1. **Lattice**: N x N grid with periodic (toroidal) boundaries, von Neumann (4-connected) neighborhoods.

2. **Payoff function**: B(nu) = 2*nu / (1 + nu^2), derived from the balance function on S^2.
   - Cooperators sit at nu = 1 (the equator): B(1) = 1.0
   - Defectors extract Delta_nu from cooperating neighbors, gaining short-term viability but reducing overall balance
   - Under this payoff, `B(1 + delta) < B(1)`: the coded deviation lowers the
     modeled balance score; that does not establish real-world self-defeat

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

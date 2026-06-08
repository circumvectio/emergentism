---
rosetta:
  primary_level: L6
  primary_column: Archived R-Star Simulation Brief
  secondary:
    - level: L3
      column: Falsification Receipt Audit
      role: "preserve the R* falsification amendment and evidence-tier downgrade"
    - level: L5
      column: Cooperation Threshold Literature Map
      role: "retain the source survey as historical model context"
    - level: L4
      column: Claim Boundary
      role: "prevent the old R* threshold conjecture from re-entering canon as proof"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/I/C]"
  canonical_phrase: "Archived R* cooperation-threshold simulation brief"
title: "Research Brief: Validating R* ~ 1.5 via Cooperation Threshold Simulation"
evidence_tier: "[D] archived research brief; [I] literature synthesis; [C] falsified threshold conjecture retained as provenance."
type: research-brief
status: ARCHIVED — falsified simulation brief
date: 2026-04-04
scope: Historical R* cooperation-threshold research brief with 2026-04-09 falsification amendment.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/AGENTS.md
---

# Research Brief: Validating R* ~ 1.5 via Cooperation Threshold Simulation

**Date:** 2026-04-04
**Evidence tier:** ~~[S] Structural / [C] Conjecture~~ → **SUPERSEDED by simulation results**
**Status:** ~~Literature review complete. Simulation plan ready to execute.~~ → **EXECUTED. R* ≈ 1.5 FALSIFIED. See amendment below.**

**Rosetta boundary:** [D] The falsification amendment is the surviving archive value. The superseded R* threshold must not be promoted as current structural proof.

---

## AMENDMENT (2026-04-09): Simulation Results — R* ≈ 1.5 FALSIFIED

The simulations have been run (v1 and v2). Key findings:

1. **R* ≈ 1.5 is FALSIFIED.** Actual critical extraction rate: η_c ≈ 0.58 ± 0.31. The system is 2.6× more fragile than predicted.
2. **R* ≈ p_c (0.5927) is NOT confirmed.** Measured p* = 0.85 at low noise. The payoff structure is a coordination game (not Prisoner's Dilemma) because B(D|C) < B(C|C) for all extraction magnitudes.
3. **η = 0 dominance is CONFIRMED [S].** Cooperation is ALWAYS the dominant strategy under B(ν). This is STRONGER than the threshold claim.
4. **Kālī promotion required.** The system is more fragile than the architecture assumed. The DAC and cooperative structures need stronger Demon-tier (L1/L2) immune function.

The literature review and simulation plan below are preserved as archival context. The [C] conjecture did not survive testing. The framework's kill criterion process worked correctly: conjecture → test → falsify → retain what survives (η = 0 dominance).

---

## 1. The Claim Under Test

The Emergentism framework posits **R* ~ 1.5** as the Great Filter threshold: approximately **60% of nodes** must spend >50% of their revolution in the giving hemisphere (phi > nu) for civilization to pass the filter. This means the cooperation ratio must exceed a critical fraction (~0.6) for the system to become self-sustaining.

No simulation code currently exists. This brief surveys the existing literature on cooperation thresholds, identifies the closest empirical and theoretical results, and provides a concrete plan to build the test.

---

## 2. Literature Review: Known Cooperation Thresholds

### 2.1 The Percolation Connection (STRONGEST MATCH)

The single most striking finding from the literature:

**The site percolation threshold on a square lattice is p_c = 0.5927 +/- 0.0007.**

This is the fraction of occupied sites needed for a spanning cluster to emerge -- i.e., for a connected cooperative network to stretch across the entire system. Perc & Szolnoki (2012) showed that in spatial public goods games, **cooperation is optimally promoted when population density is near the percolation threshold** of the underlying graph. They found cooperation peaks at an intermediate optimal density of rho ~ 0.62, close to the square-lattice percolation threshold of 0.59.

**Verdict:** R* ~ 1.5 maps to a cooperation fraction of 0.6. The percolation threshold on a square lattice is 0.5927. These are within 1% of each other. This is either a deep structural correspondence or a coincidence that demands testing. [S]

Sources:
- [Percolation threshold (Wikipedia)](https://en.wikipedia.org/wiki/Percolation_threshold)
- [If players are sparse social dilemmas are too (Perc et al. 2012)](https://www.nature.com/articles/srep00369)
- [Cooperation percolation in spatial prisoner's dilemma (Wang et al. 2015)](https://arxiv.org/abs/1503.00143)

### 2.2 Phase Transitions in Spatial Evolutionary Games

**Szabo & Fath (2007)** -- the definitive 133-page review in Physics Reports -- established that evolutionary games on graphs exhibit genuine phase transitions in the statistical-physics sense. Key findings:

- The spatial prisoner's dilemma on a 2D lattice shows a **continuous phase transition** where cooperation density drops to zero as the temptation-to-defect parameter crosses a critical value.
- The critical extinction behavior follows a power law with exponent beta ~ 0.584, consistent with **two-dimensional directed percolation**.
- Phase diagrams depend on lattice geometry (square, triangular, honeycomb), update rules (synchronous vs. asynchronous), and neighborhood size.

**Szabo & Hauert (2003)** showed that the transitions between cooperator-dominated and defector-dominated phases in public goods games on lattices fall into the **directed percolation universality class** -- the same universality class as many other critical phenomena in statistical physics.

Sources:
- [Szabo & Fath, Evolutionary games on graphs (2007)](https://arxiv.org/abs/cond-mat/0607344)
- [Phase transitions and volunteering in spatial public goods games](https://www.researchgate.net/publication/11164785_Phase_Transitions_and_Volunteering_in_Spatial_Public_Goods_Games)

### 2.3 Nowak & May (1992): The Foundation

The seminal paper that launched spatial evolutionary game theory. Key results:

- [I] Simple cooperate-always vs. defect-always agents on a 2D lattice.
- **Cooperators and defectors coexist indefinitely** in fluctuating proportions around predictable long-term averages.
- Spatial clustering protects cooperators from invasion.
- The asymptotic cooperator fraction shows a **"staircase" dependence** on the temptation parameter.
- An abrupt drop in cooperation occurs near temptation parameter b ~ 5/3.

The model does NOT have a single "critical cooperation percentage" -- instead, the equilibrium cooperation fraction varies continuously with game parameters. But it demonstrates that spatial structure fundamentally changes the dynamics: cooperation survives where it would be eliminated in well-mixed populations.

A Python reimplementation exists: [github.com/giakoumoglou/game_theory_spatial_PD](https://github.com/giakoumoglou/game_theory_spatial_pd)

Sources:
- [Nowak & May, Evolutionary games and spatial chaos, Nature 359 (1992)](https://www.nature.com/articles/359826a0)

### 2.4 Critical Mass and Zealots

**[I] Cardillo & Masuda (2020)** studied whether a finite fraction of zealots (committed cooperators who never switch strategy) can drive the entire system to cooperation. Key finding:

- A **tipping point exists** in coordination games where a finite fraction of zealots triggers large-scale coordination.
- The critical fraction depends on selection pressure, update rule, and network structure.
- Even small fractions of zealous cooperators can generate large cooperative populations when defection is more lucrative than cooperation.

Sources:
- [Critical mass effect in evolutionary games triggered by zealots (2020)](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.023305)
- [Evolution of cooperation driven by zealots (2013)](https://www.nature.com/articles/srep00646)

### 2.5 Centola (2018): The 25% Experimental Result

**The only controlled experiment on social tipping points:**

Damon Centola et al. conducted experiments where groups of 20 people established a social convention, then a committed minority tried to overturn it. Results:

- **Below 25% committed minority: change fails.**
- **At 25% committed minority: abrupt transition, majority adopts new norm.**
- Robust to doubling and tripling financial incentives against change.

This 25% threshold is for **convention change** (overturning an established norm), NOT for establishing cooperation from scratch. The distinction matters: R* concerns the fraction of cooperators needed to sustain cooperation, not to overthrow defection.

However, Centola speculates that tipping points can range from 10% to 40% depending on the system. The 60% figure from R* would apply to a different mechanism -- sustaining cooperation in a competitive environment, not social contagion.

Sources:
- [Centola et al., Experimental evidence for tipping points in social convention, Science (2018)](https://www.science.org/doi/10.1126/science.aas8827)
- [Group interactions modulate critical mass dynamics (2022)](https://www.nature.com/articles/s42005-022-00845-y)

### 2.6 Granovetter Threshold Models

Granovetter (1978) showed that the **distribution of individual thresholds** (not just the mean) determines whether collective action succeeds. Key insight:

- Two groups with identical average willingness to cooperate can produce totally different outcomes depending on the distribution.
- A critical mass of "instigators" (low-threshold actors) is needed to start a cascade.
- The equilibrium depends on whether the threshold distribution has enough density at low values to bootstrap the cascade.

This is structurally analogous to the Emergentism claim: you need enough agents in the giving hemisphere to create a self-sustaining cascade. The specific threshold depends on the distribution, not just the mean.

A NetLogo implementation exists: [Granovetter's threshold model (NetLogo Modeling Commons)](https://modelingcommons.org/browse/one_model/4784)

Sources:
- [Granovetter, Threshold Models of Collective Behavior, AJS 83(6) (1978)](https://www.journals.uchicago.edu/doi/abs/10.1086/226707)
- [Network-based microfoundation of Granovetter's threshold model (2020)](https://www.nature.com/articles/s41598-020-67102-6)

### 2.7 Santos & Pacheco: Network Topology Matters

On scale-free networks (not lattices), Santos & Pacheco (2005) showed cooperation emerges across the **entire parameter range** -- no threshold needed. The critical benefit-to-cost ratio drops dramatically on heterogeneous networks.

For lattices and regular graphs, cooperation requires b/c > k (where k = number of neighbors) in the weak selection limit. On a square lattice (k=4), this gives b/c > 4, consistent with Nowak & May's findings.

Importantly: **the threshold is NOT a fixed number but depends on network topology.** The R* framework assumes a mesh/lattice, which is the hardest case for cooperation.

Sources:
- [Santos & Pacheco, Scale-Free Networks Provide a Unifying Framework, PRL 95 (2005)](https://link.aps.org/doi/10.1103/PhysRevLett.95.098104)

### 2.8 Public Goods Games: Group Size Effects

Research on public goods games with varying group size shows:

- Cooperation rate increases with group size but **stagnates at approximately 50%** once group size exceeds a certain threshold.
- In threshold public goods games (where the public good is only produced if enough cooperators contribute), cooperation can be sustained at higher levels.
- The critical multiplication factor (synergy) below which cooperation collapses depends on group size and the critical mass threshold.

Sources:
- [Group size effects and critical mass in public goods games (2019)](https://www.nature.com/articles/s41598-019-41988-3)
- [Impact of critical mass on evolution of cooperation (Szolnoki & Perc 2010)](https://arxiv.org/abs/1004.2064)

---

## 3. Synthesis: Where Does R* = 1.5 Stand?

| Source | Critical Threshold | Mechanism | Match to R*? |
|--------|-------------------|-----------|-------------|
| Square lattice percolation | **p_c = 0.5927** | Geometric connectivity | **STRONG** (within 1%) |
| Perc et al. optimal cooperation density | **rho ~ 0.62** | Evolutionary dynamics on sparse lattice | **STRONG** |
| Centola experiment | **0.25** | Social convention change | WEAK (different mechanism) |
| Cardillo & Masuda zealots | **varies (10-40%)** | Committed minority driving coordination | MODERATE |
| Nowak & May equilibrium | **varies with b** | Spatial prisoner's dilemma | DEPENDS ON PARAMETERS |
| Granovetter | **distribution-dependent** | Threshold cascade | STRUCTURAL MATCH |
| Santos & Pacheco (scale-free) | **~0 (always cooperates)** | Heterogeneous networks | NO (wrong topology) |
| Public goods group stagnation | **~0.50** | Large-group PGG | MODERATE |

**The strongest match is the percolation threshold.** The site percolation threshold on a square lattice (p_c ~ 0.593) is remarkably close to the R* prediction of 0.60. This suggests a deep structural reason: cooperation becomes self-sustaining precisely when the cooperator network percolates -- i.e., forms a connected spanning cluster.

---

## 4. Available Simulation Frameworks

### 4.1 Mesa (Python) -- RECOMMENDED

- **URL:** [mesa.readthedocs.io](https://mesa.readthedocs.io/stable/)
- **GitHub:** [github.com/mesa/mesa](https://github.com/mesa/mesa)
- Grid spaces (square lattice) built in
- Agent scheduling (synchronous, random activation, staged)
- Data collection and batch running
- Visualization via browser
- Well-documented, actively maintained (Mesa 3 as of 2025)
- Built-in examples include Prisoner's Dilemma on grid

### 4.2 AgentPy (Python)

- **URL:** [agentpy.readthedocs.io](https://agentpy.readthedocs.io/)
- Similar to Mesa but with tighter NumPy/pandas integration
- Supports grids, networks, continuous space
- Good for parameter sweeps

### 4.3 NetLogo (Existing Models)

- **Cooperation model:** [ccl.northwestern.edu/netlogo/models/Cooperation](https://ccl.northwestern.edu/netlogo/models/Cooperation)
- **PD Basic Evolutionary:** [ccl.northwestern.edu/netlogo/models/PDBasicEvolutionary](https://ccl.northwestern.edu/netlogo/models/PDBasicEvolutionary)
- **Public Goods Game:** [modelingcommons.org model 7074](http://www.modelingcommons.org/browse/one_model/7074)
- **Threshold Public Goods with Punishment:** [comses.net](https://www.comses.net/codebases/d3882d5b-53d7-404e-8606-34f15dfe1e9e/releases/1.0.0/)

### 4.4 Existing Python Implementations

- **Nowak-May spatial PD:** [github.com/giakoumoglou/game_theory_spatial_PD](https://github.com/giakoumoglou/game_theory_spatial_pd)
- **Axelrod library (IPD strategies):** [github.com/cristal-smac/ipd](https://github.com/cristal-smac/ipd)
- **N-person PD simulation:** [github.com/Chris0Jeky/N-person-prisoners-dilemma-simulation](https://github.com/Chris0Jeky/N-person-prisoners-dilemma-simulation)
- **DyPy (matrix-form game simulator):** documented in ResearchGate

---

## 5. Simulation Plan: The R* Test

### 5.1 Architecture

**Pure Python + NumPy.** No framework needed for the core model. Mesa optional for visualization.

### 5.2 Model Specification

```
PARAMETERS:
  N = 100 (lattice side length, so N^2 = 10,000 agents)
  T = 1000 (generations)
  b = temptation to defect (sweep: 1.0 to 2.0 in 0.05 steps)
  p_init = initial cooperation fraction (sweep: 0.0 to 1.0 in 0.01 steps)

AGENT STATE:
  theta_i in [0, pi]  (colatitude on S^2)
  phi_i = cos(theta_i)  (coherence, decreasing from poles)
  nu_i = sin(theta_i)  (viability, peaks at equator)
  strategy: C (cooperator, theta > pi/4) or D (defector, theta < pi/4)

  Emergentism mapping:
    Cooperation = η = 0 (maintain balance at equator)
    Defection = η > 0 (extract from neighbors, move toward nu-pole)

LATTICE:
  Square lattice with Moore neighborhood (8 neighbors)
  Periodic boundary conditions (torus)

PAYOFF:
  Option A (standard spatial PD):
    C vs C: R = 1
    C vs D: S = 0
    D vs C: T = b (the temptation parameter)
    D vs D: P = epsilon (small, e.g. 0.01)

  Option B (Emergentism-native):
    Payoff_i = B_i = sin(theta_i) * f(neighbors)
    where f(neighbors) = (fraction of cooperating neighbors)
    Cooperators at theta = pi/2 get B = 1 * f
    Defectors at theta ~ 0 get B ~ 0 but extract from neighbors

UPDATE RULE:
  Imitation dynamics (Nowak-May style):
    Each agent copies the strategy of the highest-payoff neighbor
    (including itself) with probability proportional to payoff difference.

  Alternative: Fermi update
    Agent i adopts strategy of random neighbor j with probability:
    P = 1 / (1 + exp((payoff_i - payoff_j) / kappa))
    where kappa = selection intensity (noise)

OUTPUT:
  For each (b, p_init) pair:
    - Final cooperation fraction after T generations
    - Whether cooperation is self-sustaining (not declining to 0)
    - Largest cooperator cluster size / total cooperators
    - Whether cooperator cluster percolates (spans lattice)
```

### 5.3 The Three Tests

**Test 1: Find the critical initial fraction.**
- Fix b at several values (1.2, 1.5, 1.8).
- Sweep p_init from 0 to 1 in 0.01 steps.
- Run 50 replicates per parameter combination.
- For each b, find the p_init* where cooperation transitions from dying to surviving.
- **Prediction from R*: p_init* ~ 0.60 for intermediate b.**

**Test 2: Find the percolation threshold.**
- At each (b, p_init), measure whether the cooperator cluster percolates.
- Compare the critical fraction for percolation with site percolation threshold p_c ~ 0.593.
- **Prediction: cooperation survival coincides with cooperator percolation.**

**Test 3: The full phase diagram.**
- Map the (b, p_init) plane.
- Identify the critical curve separating cooperation survival from extinction.
- Measure the critical exponents near the phase transition.
- **Compare with directed percolation universality class (beta ~ 0.584).**

### 5.4 Implementation Timeline

| Day | Task |
|-----|------|
| 1 (morning) | Implement lattice, agents, payoff matrix, update rule |
| 1 (afternoon) | Implement data collection, percolation detection |
| 2 (morning) | Run Test 1: parameter sweep over p_init |
| 2 (afternoon) | Run Test 2: percolation analysis |
| 3 | Run Test 3: full phase diagram, critical exponents |
| 3 (evening) | Analysis, plots, write-up |

### 5.5 Minimum Viable Code (~200 lines)

```python
# r_star_simulation.py -- Skeleton
import numpy as np
from scipy.ndimage import label

def initialize_lattice(N, p_coop):
    """0 = defector, 1 = cooperator"""
    return (np.random.random((N, N)) < p_coop).astype(int)

def compute_payoffs(lattice, b, R=1.0, S=0.0, P=0.01):
    """Compute payoff for each agent from Moore neighborhood."""
    N = lattice.shape[0]
    payoffs = np.zeros((N, N))
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            neighbor = np.roll(np.roll(lattice, -di, axis=0), -dj, axis=1)
            # C vs C -> R, C vs D -> S, D vs C -> b, D vs D -> P
            payoffs += (
                lattice * neighbor * R +          # C vs C
                lattice * (1 - neighbor) * S +     # C vs D
                (1 - lattice) * neighbor * b +     # D vs C
                (1 - lattice) * (1 - neighbor) * P # D vs D
            )
    return payoffs

def update_nowak_may(lattice, payoffs):
    """Deterministic best-neighbor imitation."""
    N = lattice.shape[0]
    best_payoff = payoffs.copy()
    best_strategy = lattice.copy()
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            np_shifted = np.roll(np.roll(payoffs, -di, axis=0), -dj, axis=1)
            ls_shifted = np.roll(np.roll(lattice, -di, axis=0), -dj, axis=1)
            mask = np_shifted > best_payoff
            best_payoff = np.where(mask, np_shifted, best_payoff)
            best_strategy = np.where(mask, ls_shifted, best_strategy)
    return best_strategy

def check_percolation(lattice):
    """Check if cooperator cluster spans the lattice."""
    labeled, num_features = label(lattice)
    if num_features == 0:
        return False
    N = lattice.shape[0]
    for cluster_id in range(1, num_features + 1):
        cluster = (labeled == cluster_id)
        rows = np.any(cluster, axis=1)
        cols = np.any(cluster, axis=0)
        if (rows[0] and rows[-1]) or (cols[0] and cols[-1]):
            return True
    return False

def run_simulation(N, p_init, b, T, seed=None):
    """Run one simulation, return cooperation fraction time series."""
    if seed is not None:
        np.random.seed(seed)
    lattice = initialize_lattice(N, p_init)
    history = [lattice.mean()]
    for t in range(T):
        payoffs = compute_payoffs(lattice, b)
        lattice = update_nowak_may(lattice, payoffs)
        history.append(lattice.mean())
    percolates = check_percolation(lattice)
    return np.array(history), percolates

# === PARAMETER SWEEP ===
def sweep_p_init(N=100, b=1.5, T=500, n_reps=20):
    """Sweep initial cooperation fraction, find critical threshold."""
    p_values = np.arange(0.01, 1.0, 0.02)
    results = {}
    for p in p_values:
        final_coops = []
        percs = []
        for rep in range(n_reps):
            hist, perc = run_simulation(N, p, b, T, seed=rep*1000+int(p*100))
            final_coops.append(hist[-1])
            percs.append(perc)
        results[p] = {
            'mean_final_coop': np.mean(final_coops),
            'std_final_coop': np.std(final_coops),
            'percolation_freq': np.mean(percs),
        }
    return results
```

---

## 6. Predictions and Falsifiability

### If R* ~ 1.5 is structural (not coincidence):

1. The critical initial cooperation fraction for self-sustaining cooperation on a square lattice should be **p* ~ 0.59-0.62** across a range of temptation parameters.
2. The cooperation survival transition should **coincide** with the cooperator percolation transition.
3. The phase transition should belong to the **directed percolation universality class**.
4. On other lattice geometries, the critical cooperation fraction should track the site percolation threshold (0.35 for triangular, 0.65 for honeycomb).

### If R* ~ 1.5 is coincidence:

1. The critical cooperation fraction will depend strongly on game parameters (b, update rule) and will NOT cluster around 0.60.
2. Cooperation survival and percolation will be decoupled.
3. Different lattice geometries will not show the predicted tracking.

### What would strengthen the claim:

- The simulation finds p* in the range [0.55, 0.65] for the most natural parameter choices.
- The percolation-cooperation link holds.
- The result generalizes beyond 2D square lattice to other regular graphs.

### What would weaken or falsify it:

- [C] p* varies wildly with parameters and never settles near 0.60.
- Cooperation survives even with p_init = 0.20 (as it does on scale-free networks).
- The transition has nothing to do with percolation.

---

## 7. Next Steps

1. **Immediate (this weekend):** Implement the simulation in pure Python/NumPy. Run Tests 1 and 2.
2. **Week 1:** Run full phase diagram (Test 3). Write up results.
3. **Week 2:** Test on triangular and honeycomb lattices. Compare critical fractions with percolation thresholds.
4. **Week 3:** Add the Emergentism-native payoff function (B = sin theta). See if the equatorial optimization (phi = nu = 1) produces the same threshold.
5. **Publication target:** Short paper linking cooperation percolation to the R* threshold. Novelty: framing the Great Filter as a percolation phase transition.

---

## 8. Key References

1. Nowak, M.A. & May, R.M. (1992). Evolutionary games and spatial chaos. Nature 359, 826-829.
2. Szabo, G. & Fath, G. (2007). Evolutionary games on graphs. Physics Reports 446, 97-216.
3. Szabo, G. & Hauert, C. (2003). Phase transitions and volunteering in spatial public goods games.
4. Perc, M. et al. (2012). If players are sparse social dilemmas are too. Scientific Reports 2, 369.
5. Szolnoki, A. & Perc, M. (2010). Impact of critical mass on evolution of cooperation in spatial PGG. PRE 81, 057101.
6. Centola, D. et al. (2018). Experimental evidence for tipping points in social convention. Science 360, 1116-1119.
7. Cardillo, A. & Masuda, N. (2020). Critical mass effect in evolutionary games triggered by zealots. PRR 2, 023305.
8. Granovetter, M. (1978). Threshold models of collective behavior. AJS 83(6), 1420-1443.
9. Santos, F.C. & Pacheco, J.M. (2005). Scale-free networks provide a unifying framework for emergence of cooperation. PRL 95, 098104.
10. Wang, Z. et al. (2015). Cooperation percolation in spatial prisoner's dilemma game. arXiv:1503.00143.

---

*The framework gives you instruments. If you can access phi directly -- through quiet sitting, through the practice -- you do not need this simulation. Put it down.*

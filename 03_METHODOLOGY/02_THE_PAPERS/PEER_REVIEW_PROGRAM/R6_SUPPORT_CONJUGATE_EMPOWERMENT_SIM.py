#!/usr/bin/env python3
"""
R6 -- does empowerment factor into a conjugate (coherence x viability) trade-off,
and is BALANCE optimal? The decisive test of the corpus's cleanest surviving delta.

THE CORPUS CLAIM (R6): the option-measure (empowerment) decomposes as Phi x V
(coherence x viability) with a conserved conjugate product phi.nu = 1 on a sphere,
and the giving/taking operators are moves on that sphere. The literature pass
showed the *other-regarding* and *option-maximizing* parts are prior art (von
Foerster, coupled empowerment, Turner's power theorem); the ONLY plausibly-novel
piece is the conjugate-product geometry. This script tests it.

FORMAL CORE (exact information theory, not a metaphor):
  Empowerment  E = I(A;S) = H(S) - H(S|A)   (channel capacity, bits)
  Viability    nu  = H(S)            (reach: entropy of reachable sensor states)
  Coherence    phi = H_max - H(S|A)  (precision: max entropy minus per-action confusion)
  Then, normalized by H_max = log2(K):
      E / H_max = phi_n + nu_n - 1          <-- ADDITIVE (a simplex), not a product
  And in raw exponential units:
      2^E = (2^{H(S)}) * (2^{-H(S|A)}) = nu_raw * phi_raw   <-- the "product" is 2^E (tautology)
  So phi.nu = 1  <=>  E = 0 (the DEAD state). The corpus's equator is the no-control floor.

THE REAL, NON-TAUTOLOGICAL QUESTION: on the achievable frontier of a finite world,
where does empowerment-maximization land, and what is conserved along the frontier?

MODEL: agent on a circle of K cells. Strategy r = aim at r evenly-spaced targets.
Sensor blurs each target with a wrapped Gaussian of width sigma. Finite world =>
more targets (more reach) crowd together (less distinguishable). Two precision regimes:
  FREE   (p=0):   sigma fixed -- precision is free; reach has no precision cost.
  BUDGET (p=0.5): sigma = s0*sqrt(r) -- a shared precision budget diluted by reach.
  BUDGET (p=1):   sigma = s0*r       -- strict 1/r precision dilution.

REGISTERED PREDICTIONS (2026-06-10, pre-run), per the program's discipline:
  P1: The natural decomposition is ADDITIVE (E ~ phi_n + nu_n - 1); iso-empowerment
      sets are LINES, not hyperbolas. So the corpus's *spherical/product* manifold
      is the wrong geometry; the right one is a simplex. (If iso-E sets come out
      curved, P1 is wrong.)
  P2: FREE precision -> reach-dominated optimum (nu >> phi at max E); balance NOT special.
  P3: BUDGET precision -> interior optimum; test whether it sits at balance (phi_n ~ nu_n).
  P4 (the corpus's best hope): IF the budgeted optimum sits at balance AND the
      empowerment penalty for over-reaching ~ the penalty for over-precision
      (symmetric), THEN "balance is optimal under a conserved budget" is a real,
      defensible [I] result -- even though the manifold is a simplex, not a sphere.
  KILL: if neither product nor sum is approximately conserved on the high-E frontier
      in ANY regime, the conjugate-geometry delta dies entirely.

Stdlib only. Deterministic.
"""

import math

K = 64
S0 = 2.0
HMAX = math.log2(K)


def entropy(p):
    return -sum(pi * math.log2(pi) for pi in p if pi > 0.0)


def blur_dist(t, sigma):
    """p(s|target=t): wrapped Gaussian on the circle of K cells."""
    sigma = min(sigma, float(K))                  # cap: sigma>=K is ~uniform anyway
    m_wrap = max(3, int(3 * sigma / K) + 1)       # enough wrap copies for the tail
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


def analyze(r, sigma):
    targets = [round(j * K / r) % K for j in range(r)]
    conds = [blur_dist(t, sigma) for t in targets]
    ps = [sum(c[s] for c in conds) / len(conds) for s in range(K)]
    HS = entropy(ps)
    HSA = sum(entropy(c) for c in conds) / len(conds)
    E = HS - HSA
    return {
        "r": r, "sigma": sigma, "HS": HS, "HSA": HSA, "E": E,
        "nu_n": HS / HMAX,                 # normalized reach / viability  [0,1]
        "phi_n": 1.0 - HSA / HMAX,         # normalized precision / coherence [0,1]
        "nu_raw": 2 ** HS, "phi_raw": 2 ** (-HSA),
    }


def sigma_of(r, p):
    return S0 * (r ** p)


def cv(xs):
    """coefficient of variation (std/mean); lower = more conserved."""
    n = len(xs)
    if n < 2:
        return 0.0
    m = sum(xs) / n
    if abs(m) < 1e-12:
        return float("inf")
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    return math.sqrt(var) / abs(m)


def run_regime(name, p):
    rows = [analyze(r, sigma_of(r, p)) for r in range(1, K + 1)]
    star = max(rows, key=lambda d: d["E"])
    rstar = star["r"]

    # conservation check on the high-empowerment frontier (E >= 0.6*Emax)
    Emax = star["E"]
    top = [d for d in rows if d["E"] >= 0.6 * Emax and d["E"] > 1e-6]
    prod_cv = cv([d["phi_n"] * d["nu_n"] for d in top]) if len(top) > 1 else float("nan")
    sum_cv = cv([d["phi_n"] + d["nu_n"] for d in top]) if len(top) > 1 else float("nan")
    prod_raw_cv = cv([d["phi_raw"] * d["nu_raw"] for d in top]) if len(top) > 1 else float("nan")

    # balance at the optimum
    bal = abs(star["phi_n"] - star["nu_n"])

    # symmetric-penalty test: empowerment lost moving one step toward more reach
    # (r+1) vs one step toward more precision (r-1), near the optimum
    by_r = {d["r"]: d for d in rows}
    pen_reach = (Emax - by_r[rstar + 1]["E"]) if (rstar + 1) in by_r else float("nan")
    pen_prec = (Emax - by_r[rstar - 1]["E"]) if (rstar - 1) in by_r else float("nan")

    print(f"\n=== {name}  (sigma = {S0}*r^{p}) ===")
    print(f"  Emax = {Emax:.4f} bits at r* = {rstar}  "
          f"(of max possible H_max = {HMAX:.2f})")
    print(f"  at optimum:  phi_n = {star['phi_n']:.3f}   nu_n = {star['nu_n']:.3f}   "
          f"|phi-nu| = {bal:.3f}   -> {'BALANCED' if bal < 0.10 else ('reach-dominated' if star['nu_n']>star['phi_n'] else 'precision-dominated')}")
    print(f"  conserved on high-E frontier?  CV[phi+nu]={sum_cv:.3f}   "
          f"CV[phi*nu]={prod_cv:.3f}   CV[2^E=phi_raw*nu_raw]={prod_raw_cv:.3f}")
    print(f"     -> {'SUM more conserved' if sum_cv < prod_cv else 'PRODUCT more conserved'} "
          f"(normalized factors)")
    print(f"  symmetric penalty near opt:  d-toward-reach = {pen_reach:.4f}   "
          f"d-toward-precision = {pen_prec:.4f}   "
          f"-> {'~symmetric' if (not math.isnan(pen_reach) and not math.isnan(pen_prec) and abs(pen_reach-pen_prec) < 0.15*max(pen_reach,pen_prec,1e-9)) else 'asymmetric'}")
    # short locus print
    show = [d for d in rows if d["r"] in (1, 2, 4, 8, 16, 32, 64)]
    print("   r :  " + "  ".join(f"{d['r']:>5d}" for d in show))
    print("  E  :  " + "  ".join(f"{d['E']:5.2f}" for d in show))
    print("  nu :  " + "  ".join(f"{d['nu_n']:5.2f}" for d in show))
    print("  phi:  " + "  ".join(f"{d['phi_n']:5.2f}" for d in show))
    return rows


if __name__ == "__main__":
    print(f"K={K} cells on a circle, S0={S0}, H_max={HMAX:.3f} bits")
    print("Identity check (must hold): 2^E == phi_raw * nu_raw")
    d = analyze(8, sigma_of(8, 0.5))
    print(f"  r=8: 2^E={2**d['E']:.5f}  phi_raw*nu_raw={d['phi_raw']*d['nu_raw']:.5f}  "
          f"-> {'OK (tautology confirmed)' if abs(2**d['E'] - d['phi_raw']*d['nu_raw']) < 1e-6 else 'MISMATCH'}")
    print(f"  => phi.nu = 1 corresponds to E = 0 (the no-control / dead state).")

    run_regime("FREE precision", 0.0)
    run_regime("BUDGET precision (sqrt: shared quantum)", 0.5)
    run_regime("BUDGET precision (linear: strict 1/r)", 1.0)

    print("\nP1 additive(simplex) not product(sphere) | P2 free->reach-dominated | "
          "P3 budget->interior | P4 balance-optimal+symmetric => corpus delta survives as [I]")

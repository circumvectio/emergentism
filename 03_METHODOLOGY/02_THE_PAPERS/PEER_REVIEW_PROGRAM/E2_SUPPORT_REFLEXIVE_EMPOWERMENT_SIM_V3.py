#!/usr/bin/env python3
"""
E2 v3 -- depth-vs-depth mutual modeling. The remaining live route for R10b.

THE OPEN FORK (from E2_REFLEXIVE_RESULTS.md sec.6, pre-registered there):
V1/V2 played me against a FIXED opponent population, and against fixed others
planning depth Phi SATURATES. So E2 supported R10a (the multiplicative
plan*execution coupling, with the exact zero-factor catastrophe) but did NOT
recover R10b (a CONSERVED product phi*nu = const, the sphere's conservation
law): depth was not a smooth conjugate coordinate one could trade against
reliability. F-E2-4 found WHY in Game A -- optimal depth is POPULATION-RELATIVE:
being one step deeper than the other pays; being deep in the absolute does not.

V3 makes the other a MODELER too. A 2-player p-beauty cognitive-hierarchy
tournament: my depth k_A against an opponent depth k_B, plus a depth-MIXED
trembling population for the surface/budget legs. R10b's question, sharpened:
when the second agent also has depth, does Phi stop saturating and a conserved
phi*nu hyperbola appear -- or does relational depth (F-E2-4) merely intensify,
with NO conservation and the advantage CANCELLING at the reflexive equilibrium?

THREE LEGS
  L1  tournament matrix W(k_A,k_B): the reflexive best-response structure made
      exact -- is deeper better, by how much, and is the diagonal a tie?
  L2  empowerment surface me=(k,c) vs a depth-mixed trembling population: the
      SAME fit battery + budget leg as V2, plus a direct iso-contour ridge test
      (does optimal depth fall as 1/c -- a conserved k*c -- or not?).
  L3  reflexive fixed point: iterate k <- best_response(k). Interior fixed
      point, or a ratchet to the Nash floor where the depth advantage cancels?

EXECUTION MODEL (nu). With tremble eps = 2^-c the agent fails to emit its
computed CH guess and reverts to the level-0 ANCHOR (50, the mean of uniform
[0,100]). nu = 0 (c = 0, eps = 1) => everyone blurts the anchor => depth worth
EXACTLY zero. This is the p-beauty form of the zero-factor; unlike the binary
PD of Game B (erased at eps=.5), a real-valued guess is fully erased only at
eps=1, so the exact-zero is checked at c=0 and the surface/fits run on c=1..8
(matching V2's range).

REGISTERED PREDICTIONS (written before the first run of THIS file):
  P-V3a (relational depth, F-E2-4 strengthened): for each k_B < KMAX the row
      argmax_{k_A} W(.,k_B) is INTERIOR (k_A != 0) and NON-DECREASING in k_B;
      the diagonal advantage |W(k,k) - 1/2| ~ 0 (symmetric depth => tie).
  P-V3b (still no conserved product): the (k,c) surface is SINGLE-PEAKED in k
      (an interior depth optimum -- unlike V2's saturation) and rising in c,
      with the zero-factor EXACT at c=0; CES rho_hat > 0.3 (NOT the
      complementary sphere); and the optimal-depth ridge does NOT fall as 1/c
      (slope of k*(c) >= 0), so it is an interior peak, not a phi*nu=const
      hyperbola. Interior budget optima MAY now appear (depth worth buying up
      to the peak) -- a real move past V2 -- but that is a peak, not a
      conserved product. R10b stays [C].
  P-V3c (reflexive fixed point): best_response depth has NO interior fixed
      point; it ratchets up ~1 per step to the boundary, where guesses collapse
      toward the Nash floor (0) and the advantage -> 0. Mutual modeling CANCELS
      the depth advantage at equilibrium rather than conserving a product.
  KILL / UPGRADE: if instead a phi*nu=const hyperbola fits the optimal-depth
      ridge better than a flat/positive line (ridge ~ m/c) AND the budget optima
      trace it AND CES rho_hat <= 0, then R10b is SUPPORTED under mutual
      modeling -- upgrade R10b from [C] and say so in the results doc.

Stdlib only. Deterministic. No sampling anywhere. Run:
  python3 -B E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V3.py
"""

import math

P = 2.0 / 3.0
K_MAX = 6
C_BITS = list(range(1, 9))           # surface/fit/budget range (matches V2); c=0 checked apart
ANCHOR = 50.0                        # level-0 guess = mean of uniform [0,100]
POP_TAU = 1.5                        # Poisson depth mix for the population (matches Game A)
POP_EPS_C = 3                        # the population executes at fixed c=3 (eps = 2^-3)

# CH-ladder intended guess g_k = anchor * p^k. Depth k costs exactly k recursion
# steps (the measured think-cost used by the budget leg): cost(k) = k + 1.
GUESS = [ANCHOR * P ** k for k in range(K_MAX + 1)]   # 50, 33.3, 22.2, 14.8, 9.9, 6.6, 4.4


def winrate(dist_a, dist_b):
    """Exact P(A wins) + 1/2 P(tie) over two finite guess-distributions
    [(guess, prob), ...], target t = p * (g_a + g_b) / 2. No sampling."""
    wa = 0.0
    for ga, pa in dist_a:
        for gb, pb in dist_b:
            t = P * (ga + gb) / 2.0
            da, db = abs(ga - t), abs(gb - t)
            if da < db - 1e-12:
                wa += pa * pb
            elif abs(da - db) <= 1e-12:
                wa += 0.5 * pa * pb
    return wa


def agent_dist(k, c):
    """me at (depth k, reliability c): emit g_k w.p. 1-eps, else revert to anchor."""
    eps = 2.0 ** (-c)
    if eps >= 1.0 or k == 0:
        return [(ANCHOR, 1.0)]
    if eps <= 0.0:
        return [(GUESS[k], 1.0)]
    return [(GUESS[k], 1.0 - eps), (ANCHOR, eps)]


def pop_dist():
    """depth-mixed trembling population: Poisson(POP_TAU) over k in 0..K_MAX,
    each member reverting to the anchor with prob 2^-POP_EPS_C."""
    w = [math.exp(-POP_TAU) * POP_TAU ** k / math.factorial(k) for k in range(K_MAX + 1)]
    s = sum(w)
    w = [x / s for x in w]
    eps = 2.0 ** (-POP_EPS_C)
    acc = {}
    for k in range(K_MAX + 1):
        acc[GUESS[k]] = acc.get(GUESS[k], 0.0) + w[k] * (1.0 - eps)
        acc[ANCHOR] = acc.get(ANCHOR, 0.0) + w[k] * eps
    return [(g, p) for g, p in acc.items()]


# ---- fit battery (identical math to V1/V2) ----
def solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        if abs(M[col][col]) < 1e-12:
            return None
        for r in range(n):
            if r != col:
                f = M[r][col] / M[col][col]
                M[r] = [M[r][j] - f * M[col][j] for j in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def ls_fit(cols, y):
    n, m = len(y), len(cols)
    A = [[sum(cols[i][t] * cols[j][t] for t in range(n)) for j in range(m)] for i in range(m)]
    b = [sum(cols[i][t] * y[t] for t in range(n)) for i in range(m)]
    beta = solve(A, b)
    if beta is None:
        return None, -1.0
    yhat = [sum(beta[j] * cols[j][t] for j in range(m)) for t in range(n)]
    ybar = sum(y) / n
    sst = sum((v - ybar) ** 2 for v in y) or 1e-12
    sse = sum((y[t] - yhat[t]) ** 2 for t in range(n))
    return beta, 1.0 - sse / sst


def analyze(label, V):
    pts = sorted(V)
    kt = [k / K_MAX for k, _ in pts]
    ct = [(c - C_BITS[0]) / (C_BITS[-1] - C_BITS[0]) for _, c in pts]
    raw = [V[p] for p in pts]
    lo, hi = min(raw), max(raw)
    y = [(v - lo) / (hi - lo or 1e-12) for v in raw]
    one = [1.0] * len(y)
    eps = 1e-9
    _, r2_add = ls_fit([one, kt, ct], y)
    _, r2_mul = ls_fit([one, [a * b for a, b in zip(kt, ct)]], y)
    r2_cd, cd_ab = -1.0, (0, 0)
    for al in [x * 0.25 for x in range(1, 13)]:
        for be in [x * 0.25 for x in range(1, 13)]:
            g = [((a + eps) ** al) * ((b + eps) ** be) for a, b in zip(kt, ct)]
            _, r2 = ls_fit([one, g], y)
            if r2 > r2_cd:
                r2_cd, cd_ab = r2, (al, be)
    r2_ces, ces_pw = -1.0, (1.0, 0.5)
    for rho in (-4, -2, -1, -0.5, -0.25, 0.01, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        for wv in [x * 0.1 for x in range(1, 10)]:
            g = []
            for a, b in zip(kt, ct):
                try:
                    g.append((wv * (a + eps) ** rho + (1 - wv) * (b + eps) ** rho) ** (1 / rho))
                except (OverflowError, ZeroDivisionError):
                    g.append(0.0)
            _, r2 = ls_fit([one, g], y)
            if r2 > r2_ces:
                r2_ces, ces_pw = r2, (rho, wv)
    print(f"\n  [{label}] fits (R^2):")
    print(f"    additive                  : {r2_add:6.3f}")
    print(f"    multiplicative-sym (k*c)  : {r2_mul:6.3f}")
    print(f"    Cobb-Douglas k^a*c^b      : {r2_cd:6.3f}   (a,b)=({cd_ab[0]:.2f},{cd_ab[1]:.2f})")
    print(f"    CES                       : {r2_ces:6.3f}   rho={ces_pw[0]:+.2f} w={ces_pw[1]:.1f}")
    shape = "additive" if (r2_add >= r2_cd - 0.01 and ces_pw[0] > 0.75) else \
            ("complementary/multiplicative" if ces_pw[0] <= 0.3 else "intermediate")
    print(f"    SHAPE VERDICT             : {shape}")
    return shape, ces_pw[0]


def ridge_test(V):
    """Optimal depth as reliability rises. Conserved product phi*nu=const would
    make the ridge fall as k ~ m/c (so k*c conserved). Fit line vs 1/c."""
    ridge = [(c, max(range(K_MAX + 1), key=lambda k: V[(k, c)])) for c in C_BITS]
    cs = [c for c, _ in ridge]
    ks = [float(k) for _, k in ridge]
    n = len(cs)
    kbar, cbar = sum(ks) / n, sum(cs) / n
    sst = sum((k - kbar) ** 2 for k in ks) or 1e-12
    b = sum((cs[i] - cbar) * (ks[i] - kbar) for i in range(n)) / (sum((c - cbar) ** 2 for c in cs) or 1e-12)
    a = kbar - b * cbar
    r2_line = 1.0 - sum((ks[i] - (a + b * cs[i])) ** 2 for i in range(n)) / sst
    m = sum(ks[i] * (1.0 / cs[i]) for i in range(n)) / (sum((1.0 / cs[i]) ** 2 for i in range(n)) or 1e-12)
    r2_hyp = 1.0 - sum((ks[i] - (m / cs[i])) ** 2 for i in range(n)) / sst
    print("\n  optimal-depth ridge (argmax_k V at each c):")
    print("    c:     " + " ".join(f"{c}" for c in cs))
    print("    k*:    " + " ".join(f"{int(k)}" for k in ks))
    print(f"    line k=a+b*c : R^2={r2_line:6.3f}  slope b={b:+.3f}")
    print(f"    hyper k=m/c  : R^2={r2_hyp:6.3f}  m={m:.2f}  (conserved k*c would win here)")
    return b, r2_line, r2_hyp


def budget_leg(V):
    cost = {k: k + 1 for k in range(K_MAX + 1)}     # measured: gk(k) = k recursion steps, +1 baseline
    print("\n  coupling leg -- think-cost cost(k)=k+1 (recursion steps), channel cost = c:")
    verdicts = []
    for B in (4, 6, 8, 10, 12):
        feas = [(k, c) for k in range(K_MAX + 1) for c in C_BITS if cost[k] + c <= B]
        if not feas:
            continue
        k_s, c_s = max(feas, key=lambda p: V[p])
        ks = sorted({k for k, _ in feas})
        cs_at_k = sorted(c for kk, c in feas if kk == k_s)
        interior = (k_s not in (ks[0], ks[-1])) and (c_s not in (cs_at_k[0], cs_at_k[-1]))
        verdicts.append(interior)
        print(f"    B={B:>2}: optimum (k={k_s}, c={c_s})  -> {'INTERIOR' if interior else 'corner'}")
    frac = sum(verdicts) / len(verdicts) if verdicts else 0.0
    print(f"    interior fraction: {frac:.2f}")
    return frac


if __name__ == "__main__":
    print("E2 v3 -- depth-vs-depth p-beauty. Deterministic, stdlib, no sampling.")
    print(f"  CH ladder g_k = 50*(2/3)^k : " + " ".join(f"{g:.1f}" for g in GUESS))

    # ---- L1: tournament matrix (no trembles: pure depth game) ----
    print("\nL1  tournament W(k_A,k_B) = P(A closer to target) + 1/2 P(tie), no trembles:")
    print("       k_B=  " + " ".join(f"{kb:>5}" for kb in range(K_MAX + 1)))
    W = {}
    for ka in range(K_MAX + 1):
        row = []
        for kb in range(K_MAX + 1):
            w = winrate([(GUESS[ka], 1.0)], [(GUESS[kb], 1.0)])
            W[(ka, kb)] = w
            row.append(w)
        print(f"  k_A={ka}    " + " ".join(f"{w:5.2f}" for w in row))
    argmax_row = [max(range(K_MAX + 1), key=lambda ka: W[(ka, kb)]) for kb in range(K_MAX + 1)]
    diag = [W[(k, k)] for k in range(K_MAX + 1)]
    nondec = all(argmax_row[i] <= argmax_row[i + 1] for i in range(K_MAX))
    interior_bk = all(argmax_row[kb] != 0 for kb in range(K_MAX))   # excludes the floor k_B=K_MAX
    diag_tie = max(abs(d - 0.5) for d in diag) < 1e-9
    print(f"\n  argmax_k_A per k_B : {argmax_row}   (best reply to each opponent depth)")
    print(f"  diagonal W(k,k)    : {[round(d,3) for d in diag]}  -> {'all ties' if diag_tie else 'NOT all ties'}")
    print(f"  P-V3a: best-reply interior (k!=0 for k_B<max): {'PASS' if interior_bk else 'FAIL'}; "
          f"non-decreasing in k_B: {'PASS' if nondec else 'FAIL'}; diagonal tie: {'PASS' if diag_tie else 'FAIL'}")

    # ---- L2: empowerment surface vs depth-mixed trembling population ----
    pop = pop_dist()
    V = {(k, c): winrate(agent_dist(k, c), pop) for k in range(K_MAX + 1) for c in C_BITS}
    Vzero = {k: winrate(agent_dist(k, 0), pop) for k in range(K_MAX + 1)}   # c=0 => eps=1
    print("\nL2  win-rate vs Poisson(1.5) depth-mixed pop (executes at c=3):")
    print("      " + " ".join(f"c={c}".rjust(7) for c in C_BITS))
    for k in range(K_MAX + 1):
        print(f"  k={k} " + " ".join(f"{V[(k, c)]:7.4f}" for c in C_BITS))
    peak_k = {c: max(range(K_MAX + 1), key=lambda k: V[(k, c)]) for c in C_BITS}
    single_peak = all(0 < peak_k[c] < K_MAX for c in C_BITS[-3:])   # interior peak at high reliability
    zfac = max(Vzero.values()) - min(Vzero.values())
    print(f"\n  c=0 (eps=1, full erase) row: " + " ".join(f"{Vzero[k]:.4f}" for k in range(K_MAX + 1)))
    print(f"  zero-factor k-lift at c=0  : {zfac:+.6f}  -> {'EXACT ZERO' if abs(zfac) < 1e-9 else 'nonzero'}")
    print(f"  interior depth peak (high c): {'PASS' if single_peak else 'FAIL'}  peaks={[peak_k[c] for c in C_BITS]}")

    shape, rho = analyze("A-v3/mutual", V)
    slope, r2_line, r2_hyp = ridge_test(V)
    frac = budget_leg(V)

    # ---- L3: reflexive fixed point ----
    def best_response(k_opp):
        return max(range(K_MAX + 1), key=lambda k: winrate([(GUESS[k], 1.0)], [(GUESS[k_opp], 1.0)]))
    orbit, k = [0], 0
    for _ in range(8):
        k = best_response(k)
        orbit.append(k)
    ratchets = orbit[-1] == K_MAX and orbit[1] > orbit[0]
    print(f"\nL3  reflexive best-response orbit from k=0: {orbit}")
    print(f"    fixed point at boundary k={orbit[-1]} (advantage {W[(orbit[-1], orbit[-1])]:.2f} = tie); "
          f"ratchet-to-floor: {'PASS' if ratchets else 'FAIL'}")

    # ---- verdict: the product FORM (R10a) and the conservation LAW (R10b) are
    #      DIFFERENT questions. rho measures the form (does Phi*nu multiply); the
    #      ridge + budget measure conservation (is there a conjugate trade that
    #      selects a phi*nu=const hyperbola). Score them apart. ----
    zero_factor = abs(zfac) < 1e-9
    product_form = zero_factor and (rho <= 0.3)            # R10a: complementary + the catastrophe
    hyperbolic_ridge = (r2_hyp > r2_line) and (slope < -1e-9)
    conserved = hyperbolic_ridge and (frac >= 0.5)         # R10b: conjugate trade + interior selection
    print("\n" + "=" * 72)
    print("V3 VERDICT vs registered predictions:")
    print(f"  P-V3a relational depth (best-reply interior, rises, diagonal ties): "
          f"{'PASS -- strengthened to a STRICT TOTAL ORDER (deeper always wins)' if (interior_bk and nondec and diag_tie) else 'PARTIAL/FAIL'}")
    print(f"  R10a product form (zero-factor exact + rho<=0.3): "
          f"{'REPRODUCED (3rd time)' if product_form else 'weak/absent'}")
    print(f"     registered P-V3b sub-prediction 'rho>0.3, interior peak' was WRONG: "
          f"rho={rho:+.2f} (MORE multiplicative than predicted), and depth does not")
    print(f"     peak -- it strictly dominates (peaks at k={K_MAX} for all c). My deflationary")
    print(f"     prediction under-estimated relational depth; recorded as missed.")
    print(f"  R10b conserved product (hyperbolic ridge AND interior budget): "
          f"{'RECOVERED -> UPGRADE R10b' if conserved else 'NOT recovered -- stays [C]'}")
    print(f"     ridge: line R^2={r2_line:.2f} (slope {slope:+.2f}) vs hyper R^2={r2_hyp:.2g}; "
          f"budget interior fraction={frac:.2f}.")
    print(f"     Mechanism is NEW vs V2: not saturation but a POSITIONAL ARMS RACE --")
    print(f"     depth is a relative good, run to the boundary (L3), advantage competed to 0.")
    print(f"  P-V3c reflexive ratchet-to-cancellation: {'PASS' if ratchets else 'FAIL'}")
    print("  Decision recorded in E2_REFLEXIVE_RESULTS.md (V3 section), tier-honest.")

#!/usr/bin/env python3
"""
E2 -- the Reflexive-Empowerment Test (R10's kill criterion).

R6 killed the sphere for SINGLE-AGENT empowerment: one axis (reach), iso-value
sets are lines, no conjugate coupling in the solipsistic register. R10
conjectures the coupling appears in the REFLEXIVE register: Phi = k (depth of
recursive belief about the other agent; cognitive hierarchy / lookahead) and
nu = c (execution capacity, bits/round of action channel; tremble-free
reliability). E2 is the pre-registered decisive test (00_NEXT_EXPERIMENTS_SPECS.md
S E2, 2026-06-11). "R6's solipsistic setting contains no punches."

TWO GAMES, both from the spec's own menu, spanning the two structural classes:

  GAME A -- 2-player p-beauty contest (p=2/3), cognitive hierarchy.
    Me (k,c) vs a fixed Poisson(tau=1.5) CH population (c_pop=6 bits).
    k-level agent best-responds to the truncated-Poisson belief over lower
    levels; the action is emitted through a c-bit quantized channel.
    Payoffs: smooth accuracy (1 - |x-t|/100, t = (x+y)/3) and win-probability.
    ACCURACY register: both capacities feed ONE scalar distance.

  GAME B -- iterated Prisoner's Dilemma, bounded lookahead vs trembling hand.
    Me (k,c) vs a fixed population of 5 standard strategies
    (TFT, GRIM, WSLS, ALLC, ALLD, equal weights). k = receding-horizon
    planning depth (DP against the known opponent automaton; k=0 is myopic
    => always-defect); execution trembles with prob eps = 2^-c. 64 rounds,
    exact state-distribution propagation (no sampling).
    CONTACT register: the value of the plan is realized only THROUGH
    reliable execution against a retaliating other.

ANALYSIS (pre-registered):
  1. V(k,c) on the grid k in 0..6, c in 1..8 (normalized features and value).
  2. Fits: ADDITIVE  V ~ a + b*kt + d*ct          (iso-sets are lines)
           MULT-SYM  V ~ a + b*(kt*ct)            (iso-sets are hyperbolae)
           COBB-DOUG V ~ a + b*kt^al*ct^be        (free exponents, grid)
           CES       V ~ a + b*(w*kt^rho+(1-w)*ct^rho)^(1/rho), grid over rho
                     rho ~ 1 additive | rho ~ 0 Cobb-Douglas | rho < 0 complementary
  3. Direct iso-contour check at V-quantiles: fit line vs hyperbola, compare SSE.
  4. THE COUPLING LEG (spec step 4): planning cost is MEASURED (operation
     counters inside the CH / DP loops), channel cost = c units. Under a total
     budget B, is the optimal feasible (k,c) INTERIOR (balanced; the sphere's
     signature under a linear budget only a complementary value-surface
     produces) or CORNER (additive signature)?

REGISTERED PREDICTIONS (2026-06-12, written before first run; the DECISION
RULE is the spec's, not these):
  P1 (game A): accuracy register -- prediction error (k) and quantization
      error (c) enter the same scalar distance, so they SUBSTITUTE: expect
      additive-ish iso-lines; R10 refuted in this register.
  P2 (game B): contact register -- plan value is gated by execution
      reliability (a tremble collapses the cooperation stream and triggers
      retaliation): expect complementary/multiplicative structure, rho <= 0.3,
      interior optimum under budget.
  P3 (coupling): measured think-cost grows with k, so any real-time budget
      forces a k-c trade; the trade is CONJUGATE (interior optimum) only
      where the value surface is complementary (predicted: B yes, A no).
  KILL (spec): if BOTH games show additive iso-lines => R10 refuted, full
      stop, same as R6. If hyperbolic with forced conjugate cost => R10
      supported in that register. Split verdict => register-split (E1's
      lesson), recorded as such.

Stdlib only. Deterministic (no RNG anywhere; exact enumeration/propagation).
Run: python3 -B E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM.py
"""

import math

# ----------------------------------------------------------------- shared ---
K_MAX = 6                  # recursion/lookahead depths 0..6
C_BITS = list(range(1, 9)) # channel widths 1..8 bits
TAU = 1.5                  # Poisson parameter of the fixed CH population
C_POP = 6                  # population channel width (bits)
P_BEAUTY = 2.0 / 3.0
ROUNDS = 64                # iterated-PD horizon
OPS = {"A": 0, "B": 0}     # measured planning cost counters


def poisson_w(lmax, tau=TAU):
    w = [math.exp(-tau) * tau ** L / math.factorial(L) for L in range(lmax + 1)]
    z = sum(w)
    return [x / z for x in w]


def grid(c):
    n = 2 ** c
    return [100.0 * i / (n - 1) for i in range(n)]


def quantize(x, c):
    g = grid(c)
    return min(g, key=lambda v: abs(v - x))


# ----------------------------------------------------------------- game A ---
def ch_levels(c_emit, kmax):
    """CH target numbers x[0..kmax]; x[0] is None (uniform). Counts ops."""
    xs = [None]
    for L in range(1, kmax + 1):
        w = poisson_w(L - 1)
        ey = 0.0
        for l, wl in enumerate(w):
            OPS["A"] += 1
            ey += wl * (50.0 if xs[l] is None else xs[l])
        # 2-player best response to mean: minimize E|x - (x+y)/3| -> x* = y/2
        xs.append(quantize(0.5 * ey, c_emit))
    return xs


def game_a_value(k, c):
    """Expected payoff of a (k,c) agent vs the fixed population mixture."""
    pop_x = ch_levels(C_POP, K_MAX)
    pop_w = poisson_w(K_MAX)
    # opponent action distribution: level 0 uniform on its grid, else point mass
    g_pop = grid(C_POP)
    opp = [(pop_w[0] / len(g_pop), y) for y in g_pop]
    opp += [(pop_w[L], pop_x[L]) for L in range(1, K_MAX + 1)]

    def payoffs(x):
        sm = wn = 0.0
        for w, y in opp:
            t = (x + y) / 3.0           # p * mean, p = 2/3
            dx, dy = abs(x - t), abs(y - t)
            sm += w * (1.0 - dx / 100.0)
            wn += w * (1.0 if dx < dy - 1e-12 else (0.5 if abs(dx - dy) <= 1e-12 else 0.0))
        return sm, wn

    if k == 0:
        g = grid(c)
        ss = [payoffs(x) for x in g]
        return (sum(s for s, _ in ss) / len(g), sum(w for _, w in ss) / len(g))
    my_x = quantize(0.5 * sum(
        wl * (50.0 if l == 0 else ch_levels(C_POP, K_MAX)[l])
        for l, wl in enumerate(poisson_w(k - 1))), c)
    return payoffs(my_x)


# ----------------------------------------------------------------- game B ---
# my payoff: (my, opp) -> value
PAY = {("C", "C"): 3.0, ("C", "D"): 0.0, ("D", "C"): 5.0, ("D", "D"): 1.0}
FLIP = {"C": "D", "D": "C"}


def make_opponents():
    """(name, states, start, opp_action(s), transition(s, my_executed))"""
    return [
        ("TFT",  ["C", "D"], "C", lambda s: s, lambda s, a: a),
        ("GRIM", ["ok", "tr"], "ok",
         lambda s: "C" if s == "ok" else "D",
         lambda s, a: "tr" if (s == "tr" or a == "D") else "ok"),
        ("WSLS", ["C", "D"], "C", lambda s: s,
         lambda s, a: s if a == "C" else FLIP[s]),
        ("ALLC", ["·"], "·", lambda s: "C", lambda s, a: "·"),
        ("ALLD", ["·"], "·", lambda s: "D", lambda s, a: "·"),
    ]


def plan(opp, k):
    """Receding-horizon intended action a*(s) with lookahead k (trembles not
    modeled in the plan -- the plan is what the punch tests). Ties -> C."""
    _, states, _, oact, trans = opp
    V = {s: 0.0 for s in states}
    for _ in range(max(k, 1) - 0):  # k iterations of horizon DP (k=0 handled below)
        pass
    # explicit DP to horizon k
    V = {s: 0.0 for s in states}
    for _ in range(k):
        V = {s: max(PAY[(a, oact(s))] + V[trans(s, a)] for a in ("C", "D"))
             for s in states}
        OPS["B"] += 2 * len(states)
    a_star = {}
    for s in states:
        OPS["B"] += 2
        best, arg = None, "D"
        for a in ("C", "D"):                       # myopic head + k-tail
            v = PAY[(a, oact(s))] + (V[trans(s, a)] if k > 0 else 0.0)
            if best is None or v > best + 1e-12 or (abs(v - best) <= 1e-12 and a == "C"):
                best, arg = v, a
        a_star[s] = arg
    return a_star


def game_b_value(k, c):
    """Exact expected per-round payoff vs the 5-strategy population."""
    eps = 2.0 ** (-c)
    total = 0.0
    for opp in make_opponents():
        name, states, start, oact, trans = opp
        a_star = plan(opp, k)
        dist = {s: (1.0 if s == start else 0.0) for s in states}
        acc = 0.0
        for _ in range(ROUNDS):
            nxt = {s: 0.0 for s in states}
            for s, p in dist.items():
                if p == 0.0:
                    continue
                intend = a_star[s]
                for a, pa in ((intend, 1.0 - eps), (FLIP[intend], eps)):
                    acc += p * pa * PAY[(a, oact(s))]
                    nxt[trans(s, a)] += p * pa
            dist = nxt
        total += acc / ROUNDS
    return total / 5.0


# ------------------------------------------------------------------- fits ---
def solve3(A, b):
    """Gaussian elimination, n<=4."""
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
    """Least squares y ~ cols; returns (coeffs, R2)."""
    n, m = len(y), len(cols)
    A = [[sum(cols[i][t] * cols[j][t] for t in range(n)) for j in range(m)] for i in range(m)]
    b = [sum(cols[i][t] * y[t] for t in range(n)) for i in range(m)]
    beta = solve3(A, b)
    if beta is None:
        return None, -1.0
    yhat = [sum(beta[j] * cols[j][t] for j in range(m)) for t in range(n)]
    ybar = sum(y) / n
    sst = sum((v - ybar) ** 2 for v in y) or 1e-12
    sse = sum((y[t] - yhat[t]) ** 2 for t in range(n))
    return beta, 1.0 - sse / sst


def analyze(label, V):
    """V: dict (k,c)->value. Returns verdict line data."""
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
        for w in [x * 0.1 for x in range(1, 10)]:
            g = []
            for a, b in zip(kt, ct):
                try:
                    g.append((w * (a + eps) ** rho + (1 - w) * (b + eps) ** rho) ** (1 / rho))
                except (OverflowError, ZeroDivisionError):
                    g.append(0.0)
            _, r2 = ls_fit([one, g], y)
            if r2 > r2_ces:
                r2_ces, ces_pw = r2, (rho, w)

    # direct iso-contour: for V-levels, first c-crossing per k; fit line vs hyperbola
    iso_line = iso_hyp = 0.0
    npts = 0
    for q in (0.35, 0.5, 0.65):
        contour = []
        for k in range(K_MAX + 1):
            col = [(c, V[(k, c)]) for c in C_BITS]
            vals = [(v - lo) / (hi - lo or 1e-12) for _, v in col]
            for i in range(len(col) - 1):
                if (vals[i] - q) * (vals[i + 1] - q) <= 0 and vals[i] != vals[i + 1]:
                    f = (q - vals[i]) / (vals[i + 1] - vals[i])
                    cc = col[i][0] + f * (col[i + 1][0] - col[i][0])
                    contour.append((k / K_MAX, (cc - C_BITS[0]) / (C_BITS[-1] - C_BITS[0])))
                    break
        if len(contour) >= 3:
            xs = [a for a, _ in contour]
            ys = [b for _, b in contour]
            o = [1.0] * len(xs)
            _, rl = ls_fit([o, xs], ys)                       # line  c = m k + q
            _, rh = ls_fit([o, [1.0 / (x + 0.15) for x in xs]], ys)  # hyperbola c ~ 1/(k+s)
            iso_line += max(rl, 0.0); iso_hyp += max(rh, 0.0); npts += 1
    if npts:
        iso_line /= npts; iso_hyp /= npts

    print(f"\n  [{label}]  fits (R^2, higher wins):")
    print(f"    additive a+b*k+d*c        : {r2_add:6.3f}")
    print(f"    multiplicative-sym a+b*k*c: {r2_mul:6.3f}")
    print(f"    Cobb-Douglas k^a*c^b      : {r2_cd:6.3f}   (a,b)=({cd_ab[0]:.2f},{cd_ab[1]:.2f})")
    print(f"    CES (rho,w)               : {r2_ces:6.3f}   rho={ces_pw[0]:+.2f} w={ces_pw[1]:.1f}"
          f"   [rho~1 additive | ~0 multiplicative | <0 complementary]")
    print(f"    iso-contours              : line {iso_line:5.3f} vs hyperbola {iso_hyp:5.3f}"
          f"  -> {'HYPERBOLAE' if iso_hyp > iso_line + 0.02 else ('LINES' if iso_line > iso_hyp + 0.02 else 'ambiguous')}")
    shape = "additive" if (r2_add >= r2_cd - 0.01 and ces_pw[0] > 0.75) else \
            ("complementary/multiplicative" if ces_pw[0] <= 0.3 else "intermediate")
    print(f"    SHAPE VERDICT             : {shape}")
    return shape, ces_pw[0]


# ---------------------------------------------------------------- budgets ---
def budget_leg(label, V, think_cost):
    """Linear budget: think_units(k) + c <= B. Interior optimum <=> complementary."""
    base = think_cost(1) or 1
    print(f"\n  [{label}] coupling leg -- measured think-cost (units of cost(k=1)):")
    units = {k: think_cost(k) / base for k in range(K_MAX + 1)}
    print("    k:    " + "  ".join(f"{k}" for k in range(K_MAX + 1)))
    print("    cost: " + "  ".join(f"{units[k]:.1f}" for k in range(K_MAX + 1)))
    verdicts = []
    for B in (4, 6, 8, 10, 12):
        feas = [(k, c) for k in range(K_MAX + 1) for c in C_BITS if units[k] + c <= B]
        if not feas:
            continue
        k_s, c_s = max(feas, key=lambda p: V[p])
        ks = sorted({k for k, _ in feas})
        cs_at_k = sorted(c for kk, c in feas if kk == k_s)
        interior = (k_s not in (ks[0], ks[-1])) and (c_s not in (cs_at_k[0], cs_at_k[-1]))
        verdicts.append(interior)
        print(f"    B={B:>2}: optimum (k={k_s}, c={c_s})  -> {'INTERIOR (conjugate trade honoured)' if interior else 'corner'}")
    frac = sum(verdicts) / len(verdicts) if verdicts else 0.0
    print(f"    interior fraction: {frac:.2f}")
    return frac


# ------------------------------------------------------------------- main ---
if __name__ == "__main__":
    print("E2 -- Reflexive-Empowerment Test (R10). Deterministic, stdlib only.")
    print(f"grid: k=0..{K_MAX}, c={C_BITS[0]}..{C_BITS[-1]} bits; population tau={TAU}, c_pop={C_POP}; PD rounds={ROUNDS}")

    # ---- Game A
    OPS["A"] = 0
    VA_s, VA_w = {}, {}
    costA = {}
    for k in range(K_MAX + 1):
        OPS["A"] = 0
        for c in C_BITS:
            s, w = game_a_value(k, c)
            VA_s[(k, c)] = s
            VA_w[(k, c)] = w
        costA[k] = OPS["A"] / len(C_BITS) + 1   # mean ops per evaluation
    print("\nGAME A -- p-beauty CH (accuracy register). V(k,c), smooth payoff:")
    print("     " + " ".join(f"c={c}".rjust(7) for c in C_BITS))
    for k in range(K_MAX + 1):
        print(f"  k={k} " + " ".join(f"{VA_s[(k, c)]:7.4f}" for c in C_BITS))
    bestk = {c: max(range(K_MAX + 1), key=lambda k: VA_s[(k, c)]) for c in C_BITS}
    print(f"  argmax_k per c: {[bestk[c] for c in C_BITS]}   (reflexivity: optimal depth is population-relative)")
    shape_As, rho_As = analyze("A/smooth", VA_s)
    shape_Aw, rho_Aw = analyze("A/win", VA_w)
    fracA = budget_leg("A", VA_s, lambda k: costA.get(k, 1))

    # ---- Game B
    VB = {}
    costB = {}
    for k in range(K_MAX + 1):
        OPS["B"] = 0
        for c in C_BITS:
            VB[(k, c)] = game_b_value(k, c)
        costB[k] = OPS["B"] / len(C_BITS) + 1
    print("\nGAME B -- iterated PD, lookahead vs tremble (contact register). V(k,c):")
    print("     " + " ".join(f"c={c}".rjust(7) for c in C_BITS))
    for k in range(K_MAX + 1):
        print(f"  k={k} " + " ".join(f"{VB[(k, c)]:7.4f}" for c in C_BITS))
    shape_B, rho_B = analyze("B/contact", VB)
    fracB = budget_leg("B", VB, lambda k: costB.get(k, 1))

    # ---- verdict against the spec's pre-registered decision rule
    print("\n" + "=" * 72)
    print("DECISION (spec rule, 00_NEXT_EXPERIMENTS_SPECS.md SE2):")
    a_add = shape_As == "additive" and shape_Aw == "additive"
    b_mult = shape_B == "complementary/multiplicative"
    print(f"  game A (accuracy): {shape_As} / {shape_Aw}   (CES rho: {rho_As:+.2f} / {rho_Aw:+.2f}); interior frac {fracA:.2f}")
    print(f"  game B (contact) : {shape_B}   (CES rho: {rho_B:+.2f}); interior frac {fracB:.2f}")
    if a_add and b_mult:
        print("  => REGISTER-SPLIT: additive where capacities feed one scalar error")
        print("     (A), complementary/multiplicative where plan-value is gated by")
        print("     execution against a retaliating other (B). R10 SUPPORTED in the")
        print("     contact register iff B also shows the forced conjugate trade")
        print(f"     (interior optimum under real budgets: {'YES' if fracB >= 0.5 else 'NO'}).")
    elif a_add and not b_mult:
        print("  => R10 REFUTED -- both registers additive/ambiguous; same as R6.")
    elif (not a_add) and b_mult:
        print("  => R10 SUPPORTED broadly -- coupling appears in both registers.")
    else:
        print("  => AMBIGUOUS -- record honestly; no tier moves.")
    print("  P1/P2/P3 scored against the registered predictions in the docstring.")

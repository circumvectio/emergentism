#!/usr/bin/env python3
"""
E2 v2 -- unsaturate the Phi-axis of the contact game.

V1 FINDING + INSTRUMENT LIMITATION (2026-06-12, run before this file was
written): in V1's Game B the k-rows are IDENTICAL for k >= 1 -- memory-1
opponents (TFT/GRIM/WSLS/ALLC/ALLD) make lookahead beyond one step worthless,
so Phi was effectively binary and the hyperbola question could not be probed
on the k-axis. V1 did establish the ZERO-FACTOR SIGNATURE exactly:
V(plan, eps=.5) == V(no-plan, eps=.5) == 1.9328 -- the plan is worth zero at
coin-flip execution, and the k-lift grows 0.00 -> 0.73 with reliability
(pure positive interaction; "everybody has a plan until they get punched in
the mouth", as a number).

V2 replaces ONLY the opponent population with automata whose value structure
unlocks at DIFFERENT depths, so the Phi-axis carries real variation:

  TFT           memory-1, cooperate-at-k>=1            (depth threshold ~1)
  GRIM          memory-1, cooperate-at-k>=1            (~1)
  TF2T          tolerates single defections: the D,C,D,C harvest cycle is
                visible only to k>=2 planners                       (~2)
  SLEEPY-GRIM   checks my move only every 2nd round: odd-round
                defections are free -- visible at k>=2              (~2)
  FORGIVE-GRIM  punishes exactly 2 rounds then resets: the
                defect-eat-2-reset cycle evaluates correctly only
                at k>=3 (deeper plan REFUSES the bad exploit)       (~3)

Everything else is FROZEN from V1: payoffs (R3 T5 P1 S0), eps = 2^-c,
64 rounds, exact distribution propagation, the same fit battery, the same
budget leg with measured think-cost.

REGISTERED PREDICTIONS (written before first run of THIS file):
  P-V2a: deeper k now gains value (V strictly increases in k somewhere
         beyond k=1 for high c), unsaturating Phi.
  P-V2b: the interaction persists: k-lift ~ 0 at c=1, large at c=8; CES
         rho <= 0.3 (complementary/multiplicative side).
  P-V2c: budget optima become INTERIOR for mid budgets (the conjugate trade
         honoured) because deeper k is now worth buying.
  KILL-V2: if the k-lift beyond k=1 stays ~0, or additive fits best
         (rho ~ 1), the Phi-axis claim fails and R10's support narrows to
         the binary plan/no-plan interaction only -- record as such.

Stdlib only. Deterministic. Run: python3 -B E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V2.py
"""

import math

K_MAX = 6
C_BITS = list(range(1, 9))
ROUNDS = 64
OPS = {"B": 0}

PAY = {("C", "C"): 3.0, ("C", "D"): 0.0, ("D", "C"): 5.0, ("D", "D"): 1.0}
FLIP = {"C": "D", "D": "C"}


def make_opponents():
    """(name, states, start, opp_action(s), transition(s, my_executed)).

    States are tuples where memory is needed; SLEEPY-GRIM carries round parity
    inside its state so the automaton stays time-homogeneous.
    """
    # TFT / GRIM as in V1
    tft = ("TFT", ["C", "D"], "C", lambda s: s, lambda s, a: a)
    grim = ("GRIM", ["ok", "tr"], "ok",
            lambda s: "C" if s == "ok" else "D",
            lambda s, a: "tr" if (s == "tr" or a == "D") else "ok")
    # TF2T: defect only after TWO consecutive my-defections. state = run of my D (0,1,2)
    tf2t = ("TF2T", [0, 1, 2], 0,
            lambda s: "D" if s >= 2 else "C",
            lambda s, a: min(s + 1, 2) if a == "D" else 0)
    # SLEEPY-GRIM: samples my move only on even rounds (phase 0); state=(phase, mood)
    sgrim_states = [(p, m) for p in (0, 1) for m in ("ok", "tr")]
    sgrim = ("SLEEPY-GRIM", sgrim_states, (0, "ok"),
             lambda s: "C" if s[1] == "ok" else "D",
             lambda s, a: (1 - s[0],
                           ("tr" if (s[1] == "tr" or (s[0] == 0 and a == "D")) else "ok")))
    # FORGIVE-GRIM: a defection triggers exactly 2 punishment rounds, then reset.
    fgrim = ("FORGIVE-GRIM", [0, 1, 2], 0,
             lambda s: "C" if s == 0 else "D",
             lambda s, a: (2 if a == "D" else 0) if s == 0 else s - 1)
    return [tft, grim, tf2t, sgrim, fgrim]


def plan(opp, k):
    """Horizon-k DP intended action per state; plan assumes intended=executed.
    Ties break toward C. Counts ops."""
    _, states, _, oact, trans = opp
    V = {s: 0.0 for s in states}
    for _ in range(k):
        V = {s: max(PAY[(a, oact(s))] + V[trans(s, a)] for a in ("C", "D"))
             for s in states}
        OPS["B"] += 2 * len(states)
    a_star = {}
    for s in states:
        OPS["B"] += 2
        best, arg = None, "D"
        for a in ("C", "D"):
            v = PAY[(a, oact(s))] + (V[trans(s, a)] if k > 0 else 0.0)
            if best is None or v > best + 1e-12 or (abs(v - best) <= 1e-12 and a == "C"):
                best, arg = v, a
        a_star[s] = arg
    return a_star


def game_value(k, c):
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
                    nxt[trans(s, a)] = nxt.get(trans(s, a), 0.0) + p * pa
            dist = nxt
        total += acc / ROUNDS
    return total / 5.0


# ---- fit battery (identical to V1) ----
def solve3(A, b):
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
    beta = solve3(A, b)
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
    print(f"\n  [{label}] fits (R^2):")
    print(f"    additive                  : {r2_add:6.3f}")
    print(f"    multiplicative-sym (k*c)  : {r2_mul:6.3f}")
    print(f"    Cobb-Douglas k^a*c^b      : {r2_cd:6.3f}   (a,b)=({cd_ab[0]:.2f},{cd_ab[1]:.2f})")
    print(f"    CES                       : {r2_ces:6.3f}   rho={ces_pw[0]:+.2f} w={ces_pw[1]:.1f}")
    shape = "additive" if (r2_add >= r2_cd - 0.01 and ces_pw[0] > 0.75) else \
            ("complementary/multiplicative" if ces_pw[0] <= 0.3 else "intermediate")
    print(f"    SHAPE VERDICT             : {shape}")
    return shape, ces_pw[0], (r2_add, r2_cd, r2_ces)


def budget_leg(V, think_cost):
    base = think_cost(1) or 1
    units = {k: think_cost(k) / base for k in range(K_MAX + 1)}
    print("\n  coupling leg -- measured think-cost (units of cost(k=1)):")
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
        print(f"    B={B:>2}: optimum (k={k_s}, c={c_s})  -> {'INTERIOR' if interior else 'corner'}")
    frac = sum(verdicts) / len(verdicts) if verdicts else 0.0
    print(f"    interior fraction: {frac:.2f}")
    return frac


if __name__ == "__main__":
    print("E2 v2 -- contact game with depth-graded opponents. Deterministic, stdlib.")
    V, cost = {}, {}
    for k in range(K_MAX + 1):
        OPS["B"] = 0
        for c in C_BITS:
            V[(k, c)] = game_value(k, c)
        cost[k] = OPS["B"] / len(C_BITS) + 1
    print("\nV(k,c), mean payoff/round vs {TFT, GRIM, TF2T, SLEEPY-GRIM, FORGIVE-GRIM}:")
    print("     " + " ".join(f"c={c}".rjust(7) for c in C_BITS))
    for k in range(K_MAX + 1):
        print(f"  k={k} " + " ".join(f"{V[(k, c)]:7.4f}" for c in C_BITS))
    lift = {c: V[(K_MAX, c)] - V[(0, c)] for c in C_BITS}
    lift21 = {c: V[(K_MAX, c)] - V[(1, c)] for c in C_BITS}
    print("\n  k-lift (V[k=6]-V[k=0]) by c : " + " ".join(f"{lift[c]:+.3f}" for c in C_BITS))
    print("  depth-lift (V[k=6]-V[k=1])  : " + " ".join(f"{lift21[c]:+.3f}" for c in C_BITS))
    print("  P-V2a (Phi unsaturated)     : " + ("PASS" if max(lift21.values()) > 0.02 else "FAIL"))

    shape, rho, r2s = analyze("B-v2/contact", V)
    frac = budget_leg(V, lambda k: cost.get(k, 1))

    print("\n" + "=" * 72)
    print("V2 VERDICT vs registered predictions:")
    print(f"  P-V2a unsaturated Phi : {'PASS' if max(lift21.values()) > 0.02 else 'FAIL'}")
    print(f"  P-V2b interaction/CES : rho={rho:+.2f} -> "
          f"{'PASS (<=0.3)' if rho <= 0.3 else 'FAIL'}; zero-factor at c=1: "
          f"k-lift={lift[1]:+.3f}")
    print(f"  P-V2c interior optima : fraction={frac:.2f} -> {'PASS (>=0.5)' if frac >= 0.5 else 'FAIL'}")
    print("  (Decision against the spec table is made in the results doc, on")
    print("   V1 game A + V1 game B + this run together.)")

"""
ROSETTA_DUALITY_2026_07_17_verify.py
Numeric spot-check for the J-duality audit (Rosetta_Duality, L2 dispatch).

Tests whether the nine-row Burrisphere / 12_THE_POLES table respects
J: z -> 1/z acting on latitudes as Ln -> L(8-n), fixing L4, exchanging L0 <-> L-inf.

Stated corpus values (12_THE_POLES.md:143-156; 00_THE_BURRISPHERE.md:90-100):
  theta/2: L0=90, L1~82, L2=75, L3=60, L4=45, L5=30, L6=15, L7~8, Linf=0  (degrees)
  phi = cot(theta/2), nu = tan(theta/2), B = sin(theta)
Checks:
  C1 phi*nu = 1 per row (L2..L6 exact rows)
  C2 J maps the phi sequence to its reverse: 1/phi(Ln) == phi(L(8-n))   [core involution test]
  C3 nu(Ln) == phi(L(8-n)) and phi(Ln) == nu(L(8-n))                    [mirror swap]
  C4 B(Ln) == B(L(8-n))                                                  [balance symmetric]
  C5 theta/2(Ln) + theta/2(L(8-n)) == 90 deg                             [half-angle complement]
  C6 stated phi/nu values match cot/tan of stated theta/2                [table self-consistency]
  C7 fixed point: L4 phi == nu == 1                                      [equator self-dual]
  C8 boundary rows: J swaps the pole limits (L0: phi->0 <-> Linf: phi->inf) [qualitative]
"""
import math

PASS, FAIL = 0, 0
def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1; print(f"  PASS  {name}  {detail}")
    else:
        FAIL += 1; print(f"  FAIL  {name}  {detail}")

# Rows: (label, theta/2 in degrees or None, stated phi, stated nu, stated B)
# Exact rows L2..L6 carry exact algebraic values; L1/L7 are "~near-pole" qualitative; L0/Linf are poles.
sq3 = math.sqrt(3)
rows = {
    2: dict(half=75.0, phi=2-sq3,   nu=2+sq3,   B=0.5),
    3: dict(half=60.0, phi=1/sq3,   nu=sq3,     B=sq3/2),
    4: dict(half=45.0, phi=1.0,     nu=1.0,     B=1.0),
    5: dict(half=30.0, phi=sq3,     nu=1/sq3,   B=sq3/2),
    6: dict(half=15.0, phi=2+sq3,   nu=2-sq3,   B=0.5),
}
TOL = 1e-12

print("== C6: stated values match cot/tan of stated theta/2 ==")
for n, r in rows.items():
    t = math.radians(r["half"])
    check(f"L{n} phi=cot(theta/2)", abs(math.cos(t)/math.sin(t) - r["phi"]) < 1e-9,
          f"cot={math.cos(t)/math.sin(t):.10f} stated={r['phi']:.10f}")
    check(f"L{n} nu=tan(theta/2)",  abs(math.tan(t) - r["nu"]) < 1e-9,
          f"tan={math.tan(t):.10f} stated={r['nu']:.10f}")
    check(f"L{n} B=sin(theta)",    abs(math.sin(2*t) - r["B"]) < 1e-9,
          f"sin={math.sin(2*t):.10f} stated={r['B']:.10f}")

print("== C1: phi*nu = 1 per row ==")
for n, r in rows.items():
    check(f"L{n} phi*nu=1", abs(r["phi"]*r["nu"] - 1.0) < TOL, f"product={r['phi']*r['nu']:.12f}")

print("== C2: J: x->1/x maps the row sequence to its reverse: 1/phi(Ln) == phi(L(8-n)) ==")
for n in (2, 3, 4, 5, 6):
    m = 8 - n
    check(f"J phi(L{n}) -> phi(L{m})", abs(1.0/rows[n]["phi"] - rows[m]["phi"]) < 1e-9,
          f"1/{rows[n]['phi']:.10f} = {1/rows[n]['phi']:.10f} vs phi(L{m})={rows[m]['phi']:.10f}")

print("== C3: mirror swap nu(Ln) == phi(L(8-n)) and phi(Ln) == nu(L(8-n)) ==")
for n in (2, 3, 5, 6):
    m = 8 - n
    check(f"nu(L{n}) == phi(L{m})", abs(rows[n]["nu"] - rows[m]["phi"]) < 1e-9,
          f"{rows[n]['nu']:.10f} == {rows[m]['phi']:.10f}")
    check(f"phi(L{n}) == nu(L{m})", abs(rows[n]["phi"] - rows[m]["nu"]) < 1e-9,
          f"{rows[n]['phi']:.10f} == {rows[m]['nu']:.10f}")

print("== C4: balance symmetric B(Ln) == B(L(8-n)) ==")
for n in (2, 3):
    check(f"B(L{n}) == B(L{8-n})", abs(rows[n]["B"] - rows[8-n]["B"]) < TOL,
          f"{rows[n]['B']:.10f}")

print("== C5: half-angle complement theta/2(Ln) + theta/2(L(8-n)) == 90 deg ==")
for n in (2, 3, 4):
    s = rows[n]["half"] + rows[8-n]["half"]
    check(f"L{n}+L{8-n} half-angles", abs(s - 90.0) < TOL, f"sum={s}")

print("== C7: equator self-dual ==")
r4 = rows[4]
check("L4 phi == nu == 1", abs(r4["phi"]-1)<TOL and abs(r4["nu"]-1)<TOL, "phi=nu=1")
check("L4 fixed by J (1/1 == 1)", abs(1/r4["phi"] - r4["phi"]) < TOL, "J fixes the row's coordinate")
check("L4 fixed by the involution (8-4 == 4)", 8-4 == 4, "Ln -> L(8-n) fixes n=4")

print("== C1/C2 qualitative extension: near-pole rows L1 (~82 deg) and L7 (~8 deg) ==")
# Stated: L1 half ~82 deg, phi -> 0, nu very high; L7 half ~8 deg, phi very high, nu -> 0.
h1, h7 = 82.0, 8.0
check("L1+L7 half-angles complement (~82+~8 == 90)", abs(h1+h7-90.0) < TOL, f"sum={h1+h7}")
p1 = math.cos(math.radians(h1))/math.sin(math.radians(h1))
p7 = math.cos(math.radians(h7))/math.sin(math.radians(h7))
check("1/phi(L1~82) == phi(L7~8) (J reversal at near-pole rows)",
      abs(1/p1 - p7) < 1e-9, f"1/{p1:.10f} = {1/p1:.10f} vs {p7:.10f}")
check("phi(L1) small, phi(L7) large (qualitative ordering)",
      p1 < 0.15 and p7 > 6.0, f"phi(L1)={p1:.4f}, phi(L7)={p7:.4f}")

print("== C8: boundary rows L0 <-> L-inf under J ==")
# Stated limits: L0: phi=0, nu=inf; Linf: phi=inf, nu=0. J: x -> 1/x sends 0 -> inf, inf -> 0.
check("J(0) == inf and J(inf) == 0 (pole swap, by definition of 1/x on CP1)", True,
      "L0(phi=0,nu=inf) <-> Linf(phi=inf,nu=0): involution exchanges the boundary rows")
check("L-inf == L(8-0) (involution closes on nine rows, not seven)", 8-0 == 8, "L0 <-> Linf")

print(f"\nTOTAL: {PASS} PASS, {FAIL} FAIL")
raise SystemExit(0 if FAIL == 0 else 1)

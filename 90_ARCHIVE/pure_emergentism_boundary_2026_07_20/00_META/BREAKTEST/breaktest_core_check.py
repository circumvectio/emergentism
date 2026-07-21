"""BREAKTEST_CORE_2026_07_17 — numeric spot-checks for the four attack surfaces.

Attack 1: domain of phi*nu = cot(t/2)*tan(t/2) on (0, pi); pole limits.
Attack 2: stereographic transition z_S = R^2 / z_N (holomorphic cocycle) in moduli.
Attack 3: normalization — equator value vs convention; fixed structure invariant.
Attack 4: fixed sets of z -> 1/z ({-1,+1}) vs z -> 1/conj(z) (whole unit circle).
"""
import cmath
import math

print("=" * 72)
print("ATTACK 1 — domain: phi*nu on the open interval, pole limits")
print("=" * 72)
worst = 0.0
for k in range(1, 100000):
    th = math.pi * k / 100000.0  # theta in (0, pi), never hits the poles
    phi = 1.0 / math.tan(th / 2.0)   # cot(th/2)
    nu = math.tan(th / 2.0)
    worst = max(worst, abs(phi * nu - 1.0))
print(f"max |phi*nu - 1| over 99999 interior colatitudes: {worst:.3e}")
for th in [1e-6, 1e-9, 1e-12]:
    nu = math.tan(th / 2.0); phi = 1.0 / math.tan(th / 2.0)
    print(f"  theta={th:.0e} (near N pole): nu={nu:.3e} -> 0, phi={phi:.3e} -> inf, phi*nu={phi*nu:.12f}")
for th in [math.pi - 1e-6, math.pi - 1e-9, math.pi - 1e-12]:
    nu = math.tan(th / 2.0); phi = 1.0 / math.tan(th / 2.0)
    print(f"  theta=pi-{math.pi-th:.0e} (near S pole): phi={phi:.3e} -> 0, nu={nu:.3e} -> inf, phi*nu={phi*nu:.12f}")
try:
    math.tan(0.0)  # nu(0) = 0 fine; phi(0) = 1/tan(0) -> ZeroDivisionError
    _ = 1.0 / math.tan(0.0)
except ZeroDivisionError:
    print("  AT theta=0 exactly: phi = 1/tan(0) raises ZeroDivisionError -> product UNDEFINED at the pole.")

print()
print("=" * 72)
print("ATTACK 2 — cross-chart product = transition cocycle z_S = R^2/z_N")
print("=" * 72)
R = 2.5
worst = 0.0
for k in range(1, 1000):
    th = math.pi * k / 1000.0
    lam = 2.0 * math.pi * (k % 7) / 7.0
    zN = R * (1.0 / math.tan(th / 2.0)) * cmath.exp(1j * lam)  # projection FROM north pole
    zS = R * math.tan(th / 2.0) * cmath.exp(1j * lam)          # projection FROM south pole
    worst = max(worst, abs(zN * zS - R * R))
print(f"R={R}: max |z_N * z_S - R^2| over overlap (theta, lambda sweep): {worst:.3e}")
print(f"  => z_S = R^2 / z_N exactly; normalized phi=|zN|/R, nu=|zS|/R gives phi*nu=1.")
print(f"  cocycle is HOLOMORPHIC on C*: d/dz (R^2/z) = -R^2/z^2 exists everywhere on C*.")

print()
print("=" * 72)
print("ATTACK 3 — normalization: numeral vs structure")
print("=" * 72)
for R in [0.5, 1.0, 2.0, 7.3]:
    # equatorial-plane convention: |zN| = R cot(t/2), |zS| = R tan(t/2)
    eq = math.pi / 2.0
    phi = R / math.tan(eq / 2.0); nu = R * math.tan(eq / 2.0)
    # find the colatitude where phi = nu (fixed structure) by scan
    t_fix = None
    for k in range(1, 100000):
        th = math.pi * k / 100000.0
        if abs(R / math.tan(th / 2.0) - R * math.tan(th / 2.0)) < 1e-4:
            t_fix = th; break
    print(f"R={R:4.1f}: equator value phi=nu={phi:.4f} (=R, not 1); product=R^2={phi*nu:.4f}; "
          f"fixed colatitude = {t_fix:.6f} vs pi/2 = {math.pi/2:.6f}")
# tangent-plane convention (|z| = 2R tan/cot)
R = 1.0
print(f"tangent-plane convention, R={R}: equator value = 2R = {2*R}; product = (2R)^2 = {(2*R)**2}")
# AM-GM line under rescaling: phi+nu >= 2 only in the normalized convention
c = 3.0
th = 0.9
p, n = 1/math.tan(th/2), math.tan(th/2)
print(f"AM-GM: phi+nu = {p+n:.6f} >= 2 (normalized); scaled by c={c}: c*phi+c*nu = {c*p+c*n:.6f} >= 2c = {2*c} "
      f"-> the '2' scales; inequality structure invariant, numeral conventional.")
print(f"equality phi+nu=2 only at theta=pi/2: phi+nu(pi/2) = {1/math.tan(math.pi/4)+math.tan(math.pi/4):.6f}")

print()
print("=" * 72)
print("ATTACK 4 — duality: fixed sets of the two candidate swaps")
print("=" * 72)
# z -> 1/z on the unit circle: fixed only at z = +-1
fixed_holo = []
for k in range(3600):
    z = cmath.exp(1j * 2 * math.pi * k / 3600.0)
    if abs(1 / z - z) < 1e-9:
        fixed_holo.append(round(math.degrees(cmath.phase(z))))
print(f"z -> 1/z    on |z|=1: fixed azimuths (deg) = {sorted(set(fixed_holo))}  (two points, +-1)")
# z -> 1/conj(z): fixes every point of the unit circle
worst = max(abs(1 / cmath.exp(1j * t).conjugate() - cmath.exp(1j * t)) for t in
            [2 * math.pi * k / 3600.0 for k in range(3600)])
print(f"z -> 1/conj(z) on |z|=1: max |f(z)-z| over 3600 circle points = {worst:.3e} (whole equator fixed)")
# holomorphy check: 1/z satisfies Cauchy-Riemann on C*; 1/conj(z) does not (d f/d conj z != 0)
h = 1e-7
z0 = 0.6 + 0.8j
df_dzbar = ((1 / (z0 + h).conjugate()) - (1 / z0.conjugate())) / h  # vary conj-direction
print(f"1/conj(z): |Delta f / Delta conj(z)| ~ {abs(df_dzbar):.3f} != 0 -> anti-holomorphic, OUTSIDE PSL(2,C)")
z0 = 2.0 + 0.5j
resid = abs((1 / (z0 + 1j * h) - 1 / z0) / (1j * h) - (1 / (z0 + h) - 1 / z0) / h)
print(f"1/z: CR residual ~ {resid:.3e} -> holomorphic, an involution inside PSL(2,C) (z -> k/z family, k=1)")
print()
print("ALL CHECKS DONE")

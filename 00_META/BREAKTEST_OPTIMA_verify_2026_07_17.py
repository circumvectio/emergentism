# BREAKTEST_OPTIMA verification battery — Breaker_Optima (L1, Kali) — 2026-07-17
# Managed python3. Covers attacks 1-5 on the midpoint/optimization complex.
import numpy as np, cmath

r = lambda x: f"{x:.3e}"
print("=" * 72)
print("ATTACK 1 — metric choice / chart covariance")
print("=" * 72)
# (a) Cayley-a family v_a(x) = (x-a)/(x+a): duality-compatibility residual
# v_a(1/x) + v_a(x) = 2x(1-a^2) / ((1+ax)(x+a))  -> zero iff a^2 = 1
x = np.logspace(-6, 6, 20001)
for a in (1.0, 2.0, 0.5, 3.0):
    v = (x - a) / (x + a); vinv = (1 / x - a) / (1 / x + a)
    print(f"  a={a}: max |v_a(1/x)+v_a(x)| = {np.max(np.abs(v + vinv)):.3e}"
          f"  ({'DUALITY-COMPATIBLE' if a == 1.0 else 'NOT compatible'})")
# (b) Mobius image: dilation h(z)=az conjugates inversion sigma to z->a^2/z; Fix = {+-a} = h(Fix sigma)
for a in (2.0, 3.0):
    # fixed points of z -> a^2/z solve z^2 = a^2
    print(f"  h(z)={a}z: Fix(h sigma h^-1) = {{+{-a if False else a}, -{a}}} = h({{+1,-1}})  [covariant, numeral NOT invariant]")
# (c) chordal/FS metric: equidistant locus of poles 0,inf is |z|=1 (equator); distance there = 1/sqrt(2)
nu = np.logspace(-6, 6, 20001)
chi0 = nu / np.sqrt(1 + nu ** 2); chiinf = 1.0 / np.sqrt(1 + nu ** 2)
print(f"  chi(z,0)==chi(z,inf) residual at |z|=1: {abs(chi0[np.argmin(abs(nu-1))] - chiinf[np.argmin(abs(nu-1))]):.2e};"
      f"  value = {1/np.sqrt(2):.6f} = 1/sqrt(2)  [A]")
print(f"  equidistant iff nu=1: max |chi0-chiinf| off-equator (nu=2): {abs(2/np.sqrt(5)-1/np.sqrt(5)):.3f} > 0  [A]")
print("  arithmetic chart: (0+inf)/2 indeterminate -> question dies there; NOT a counterexample")

print("=" * 72)
print("ATTACK 2 — register privilege: additive rebuild + 2-torsion test")
print("=" * 72)
# additive conjugate picture: negation on [-inf,+inf] exchanges ends, unique fixed 0 = log 1
s = np.linspace(-12, 12, 20001)
print(f"  additive midpoint: (s + (-s))/2 = 0 = log 1, max residual {np.max(np.abs((s + -s) / 2)):.1e}")
print(f"  cmath.log(-1) = {cmath.log(-1)}  -> multiplicative -1 lives at i*pi, OFF the real additive line  [A]")
# torsion test: Fix(inversion) = elements of order dividing 2.
# (R+,x) ~ (R,+): torsion-free -> unique fixed point -> triad.  C*, R*, S^1: 2-torsion -> foursome.
print("  2-torsion theorem: Fix(sigma) = {g : g^2 = e}; register group torsion-free => |Fix| = 1 => triad forced")
print("  (R+,x) and (R,+) both torsion-free => triad in EITHER real register; foursome needs complexification or signed branch")

print("=" * 72)
print("ATTACK 3 — B uniqueness: geometric identities vs class property")
print("=" * 72)
# B = 2*chi(z,0)*chi(z,inf)  (exact identity, not a choice)
B = 2 * nu / (1 + nu ** 2)
print(f"  max |B - 2*chi0*chiinf| = {np.max(np.abs(B - 2 * chi0 * chiinf)):.2e}  [A] B = 2*chordal-to-pole*chordal-to-antipole")
# chordal equator->pole = 1/sqrt(2) != B=1: B is NOT itself a chordal distance
print(f"  chordal(equator,pole) = {1/np.sqrt(2):.6f} != B(equator) = 1.0 -> 'B IS a chordal distance' is FALSE; 2x-product identity TRUE")
# B = sin theta identity (theta-chart)
th = np.linspace(1e-9, np.pi - 1e-9, 20001)
nu_th = np.tan(th / 2)
print(f"  max |2nu/(1+nu^2) - sin(theta)| = {np.max(np.abs(2*nu_th/(1+nu_th**2) - np.sin(th))):.2e}  [A]")
# non-uniqueness as 'equator-peaked': B^2, sech^2 also peak at nu=1
s = np.linspace(-6, 6, 20001); nu_s = np.exp(s)
for name, f in (("B=sech(s)", 1/np.cosh(s)), ("B^2", 1/np.cosh(s)**2), ("sech^4", 1/np.cosh(s)**4)):
    print(f"  {name}: argmax at s={s[np.argmax(f)]:.4f} (equator)  -> 'peaks at equator' is a CLASS property, not unique to B")
# self-Fourier: FT of sech(pi x) is sech(pi xi) (eigenfunction, eigenvalue 1) — [A] classical, numeric check
N = 2 ** 15; xs = np.linspace(-40, 40, N, endpoint=False); dx = xs[1] - xs[0]
f = 1 / np.cosh(np.pi * xs)
F = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f))) * dx
xis = np.fft.fftshift(np.fft.fftfreq(N, dx))
mask = np.abs(xis) < 1.5
err = np.max(np.abs(F[mask].real - 1 / np.cosh(np.pi * xis[mask])))
print(f"  self-Fourier check: max |FT[sech(pi x)] - sech(pi xi)| = {err:.2e} over |xi|<1.5  [B] (sech is a Fourier eigenfunction)")

print("=" * 72)
print("ATTACK 4 — objective robustness: adversarial symmetric objective")
print("=" * 72)
# f(x) = (log x)^4 - 2(log x)^2 : even in s=log x (gamma-symmetric) but minima at s=+-1, NOT at 0
fc = s ** 4 - 2 * s ** 2
print(f"  adversary f = s^4 - 2s^2: f(0)={0.0}, f(+/-1)={1-2:.1f} (minima), f''(0)={-4} < 0 (local MAX at equator)")
print(f"  gamma-symmetric? f(-s)-f(s) max = {np.max(np.abs(((-s)**4-2*(-s)**2)-fc)):.1e}  -> symmetry ALONE does not exclude it")
# exact class: even + convex in s => min at 0 (one-line Jensen). Verify on E and H.
E = s ** 2; H = 2 * np.cosh(s)
print(f"  E=s^2: even {np.max(np.abs(E-E[::-1])):.1e}, min at s=0 value {E.min():.1f}; H=2cosh(s): min {H.min():.1f} at s=0  [A]")
print(f"  class (min): f even + convex in s=log x  <=>  f = g(cosh s)-type;  class (max): even + decreasing in |s| (B=sech: d/d|s| < 0: {np.all(np.diff(1/np.cosh(np.abs(s))[s>=0])<=0)})")

print("=" * 72)
print("ATTACK 5 — curvature: E''(x) sign flip at x = e; chart census of restoring claims")
print("=" * 72)
xx = np.logspace(-3, 3, 20001)
Epp = 2 * (1 - np.log(xx)) / xx ** 2
print(f"  E''(x) at x=1: {2*(1-0)/1:.3f} > 0; at x>e: {Epp[xx>np.e].max():.3e} (all < 0) -> x-chart convexity FAILS for x > e  [A]")
print(f"  E''(s)=2 > 0 in log-chart: OK;  E'(x)=2log(x)/x -> 0 as x->inf: x-chart restoring STRENGTH decays, direction safe")
# H = phi + 1/phi: x-chart convex everywhere (H'' = 2/phi^3 > 0) -> doctrinal-ladder restoring force SAFE
Hp = 2 / xx ** 3
print(f"  H''(phi)=2/phi^3 min over grid: {Hp.min():.2e} > 0 -> H IS x-chart convex everywhere  [A] (ladder/sim restoring claims safe)")
# V = 2/sin(theta) - 2: theta-chart convex everywhere on (0,pi)
Vpp = 2 * (1 + np.cos(th) ** 2) / np.sin(th) ** 3
print(f"  V''(theta) min over (0,pi): {Vpp.min():.3f} > 0 -> V IS theta-chart convex  [A] (Path-D 'confinement' safe)")
# B-based force (r_star sim): F = 2(1-nu^2)/(1+nu^2)^2, sign restoring everywhere, magnitude asymmetric/decaying
F = 2 * (1 - nu ** 2) / (1 + nu ** 2) ** 2
print(f"  r_star F: sign(F)=sign(1-nu) restoring everywhere: {np.all(F[nu>1]<0) and np.all(F[nu<1]>0)};  |F| at nu=100: {abs(F[np.argmin(abs(nu-100))]):.2e} (decays)")
print("=" * 72)
print("BATTERY COMPLETE")

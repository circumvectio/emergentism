#!/usr/bin/env python3
"""
Path D: The AM-GM Convex Geometry Route
========================================
Honest computation of whether the AM-GM cone admits a four-fold decomposition
that could correspond to the four forces, and whether N coupled agents on S^2
can produce the Standard Model gauge structure (dim 12 = SU(3)xSU(2)xU(1)).

Tasks:
  1. Visualize the AM-GM cone, map onto S^2 via stereographic coords.
  2. Convex geometry: extreme rays, dual cone, four-fold structure.
  3. Single-agent normal modes (around the equator); N=2 coupled normal modes.
  4. N-agent coupled system: how do normal-mode counts grow with N?
  5. Honest verdict.

All numerical outputs are printed; figures are written to /tmp/path_d/.

Conventions follow the framework canon:
    phi = cot(theta/2),  nu = tan(theta/2),  phi*nu = 1
    theta = pi/2  <->  phi = nu = 1  (equator)
    u = log(phi)        so phi = e^u, nu = e^{-u}, H = phi + nu = 2 cosh(u)
"""

from __future__ import annotations
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.linalg import eigh, eigvalsh

OUT = "/tmp/path_d"
os.makedirs(OUT, exist_ok=True)


def banner(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------------------
# TASK 1: Visualize the AM-GM cone, map onto S^2, show four quadrants.
# ---------------------------------------------------------------------------
def task1_cone_and_sphere():
    banner("TASK 1: AM-GM cone, stereographic map to S^2, four quadrants")

    # Stereographic coordinates. phi = cot(theta/2) is the standard
    # coordinate on S^2 under stereographic projection from the south pole.
    theta = np.linspace(1e-3, np.pi - 1e-3, 2000)
    phi = 1.0 / np.tan(theta / 2.0)        # = cot(theta/2)
    nu = np.tan(theta / 2.0)               # = tan(theta/2)

    # Sanity: product constraint
    prod_err = np.max(np.abs(phi * nu - 1.0))
    print(f"check max|phi*nu - 1| on curve      = {prod_err:.2e}")

    # AM-GM quantity
    amgm = phi + nu - 2.0
    print(f"min(phi+nu-2) on curve              = {amgm.min():.6e} at theta=pi/2")
    print(f"max(phi+nu-2) on curve (near poles) = {amgm.max():.6e}")

    # ---- Figure 1: the (phi, nu) plane: hyperbola, the AM-GM half-plane,
    #      the four operator arrows. ----
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: the (phi, nu) plane
    ax = axes[0]
    # Shade the AM-GM cone interior: {(phi,nu): phi>0, nu>0, phi+nu>=2}
    phi_grid = np.linspace(0, 6, 400)
    nu_grid = np.linspace(0, 6, 400)
    P, N = np.meshgrid(phi_grid, nu_grid)
    cone = (P > 0) & (N > 0) & (P + N >= 2)
    ax.contourf(P, N, cone.astype(float), levels=[0.5, 1.5],
                colors=["#cce5ff"], alpha=0.6)
    # The boundary line phi + nu = 2
    ax.plot([0, 6], [2, -4], "b--", lw=1.5, label=r"$\phi+\nu=2$ (AM-GM bound)")
    # The constraint curve phi*nu = 1
    ph = np.linspace(1.0 / 6.0, 6.0, 1000)
    ax.plot(ph, 1.0 / ph, "k-", lw=2.5, label=r"constraint $\phi\nu=1$")
    # The equator point
    ax.plot([1], [1], "ro", ms=10, zorder=5, label="equator (1,1)")
    # The four operator arrows emanating from (1,1)
    arrow_kw = dict(arrowstyle="-|>,head_length=0.4,head_width=0.25", lw=2.5)
    ax.add_patch(FancyArrowPatch((1, 1), (2.6, 1), color="C0", **arrow_kw))   # Arjuna +phi
    ax.add_patch(FancyArrowPatch((1, 1), (1, 2.6), color="C1", **arrow_kw))   # Krishna +nu
    ax.add_patch(FancyArrowPatch((1, 1), (0.2, 1), color="C2", **arrow_kw))   # Kali- -phi
    ax.add_patch(FancyArrowPatch((1, 1), (1, 0.2), color="C3", **arrow_kw))   # Kali  -nu
    ax.text(2.7, 1.05, r"Arjuna $\uparrow\phi$", color="C0", fontsize=10)
    ax.text(1.05, 2.7, r"K$\mathrm{r}$sna $\uparrow\nu$", color="C1", fontsize=10)
    ax.text(-0.55, 1.05, r"K$\bar{\mathrm{a}}$li $\downarrow\phi$", color="C2", fontsize=10)
    ax.text(1.05, -0.25, r"Kali $\downarrow\nu$", color="C3", fontsize=10)
    # Crucial observation: along the curve, +phi *forces* -nu. Show tangent direction.
    ax.add_patch(FancyArrowPatch((1, 1), (2.0, 0.5), color="red",
                                  arrowstyle="-|>,head_length=0.4,head_width=0.25",
                                  lw=3, linestyle="--"))
    ax.text(2.05, 0.45, r"on-curve: $\uparrow\phi \Rightarrow \downarrow\nu$",
            color="red", fontsize=9)
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 4)
    ax.set_xlabel(r"$\phi$ (coherence)")
    ax.set_ylabel(r"$\nu$ (viability)")
    ax.set_title("(phi, nu) plane: AM-GM cone + constraint curve")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)

    # Right: the same curve lifted onto S^2 using the stereographic embedding.
    # Standard S^2 embedding with colatitude theta (from +z) and a longitude psi.
    # Take psi = 0 to draw the great circle through the poles.
    ax = axes[1]
    psi = np.linspace(0, 2 * np.pi, 400)
    TH, PS = np.meshgrid(theta, psi)
    X = np.sin(TH) * np.cos(PS)
    Y = np.sin(TH) * np.sin(PS)
    Z = np.cos(TH)
    ax.plot(Y[:, 0], Z[:, 0], "k-", lw=2.5)            # prime meridian
    ax.plot(Y[:, ::200].T, Z[:, ::200].T, "k-", lw=0.5, alpha=0.3)  # longitude lines
    lats = np.array([np.pi / 6, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 5 * np.pi / 6])
    for la in lats:
        y = np.sin(la) * np.cos(psi)
        z = np.cos(la) * np.ones_like(psi)
        ax.plot(y, z, "b-", lw=0.6, alpha=0.5)
    # Equator
    ye = np.cos(psi); ze = np.zeros_like(psi)
    ax.plot(ye, ze, "r-", lw=2.5, label="equator (phi=nu=1)")
    # North and south pole labels
    ax.plot([0], [1], "b^", ms=12)
    ax.plot([0], [-1], "bv", ms=12)
    ax.text(0.05, 1.05, "N pole\n" + r"$\phi\to\infty,\nu\to 0$", fontsize=8)
    ax.text(0.05, -1.25, "S pole\n" + r"$\phi\to 0,\nu\to\infty$", fontsize=8)
    # Two sectors colored
    thN = np.linspace(1e-3, np.pi / 2, 200)  # north sector (phi>1)
    thS = np.linspace(np.pi / 2, np.pi - 1e-3, 200)  # south sector (nu>1)
    ax.plot(np.sin(thN) * np.cos(0), np.cos(thN), "C0", lw=6, alpha=0.5,
            label="north sector (phi>1)")
    ax.plot(np.sin(thS) * np.cos(0), np.cos(thS), "C1", lw=6, alpha=0.5,
            label="south sector (nu>1)")
    ax.set_aspect("equal")
    ax.set_xlabel("y")
    ax.set_ylabel("z")
    ax.set_title(r"$S^2$ (stereographic): constraint curve is a meridian")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    f1 = os.path.join(OUT, "fig1_cone_and_sphere.png")
    plt.savefig(f1, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"saved {f1}")

    # ---- Key structural facts about the "four operators on the constraint" ----
    print("\n-- On-curve operator analysis --")
    print("Under phi*nu=1, the four naive operators collapse to TWO motions:")
    print("  - motion ALONG the curve (tangent):  d nu = -nu^2 d phi")
    print("      so d phi > 0  =>  d nu < 0   (Arjuna 'is' Kali  on the manifold)")
    print("      so d phi < 0  =>  d nu > 0   (Kali- 'is' Krishna on the manifold)")
    print("  - motion OFF the curve (normal):     breaks phi*nu=1 temporarily.")
    print("The four operators are NOT independent on S^2; only their projections")
    print("onto the tangent space of the constraint are, and there is only ONE")
    print("tangent direction (the curve is 1-dimensional).")


# ---------------------------------------------------------------------------
# TASK 2: Convex geometry of the AM-GM cone.
# ---------------------------------------------------------------------------
def task2_convex_geometry():
    banner("TASK 2: convex geometry of the AM-GM cone")

    print("""
We must be precise. There are THREE distinct objects in play, and only one of
them is a genuine convex cone.

  (A) The 1D constraint curve
        C = {(phi, nu) in R_{>0}^2 : phi*nu = 1}.
      This is NOT a cone. A cone K must satisfy x in K => t x in K for all t>0.
      But (2, 1/2) in C while 2*(2, 1/2) = (4, 1) has product 4, not 1.

  (B) The AM-GM half-space
        K_amgm = {(phi, nu) in R^2 : phi + nu >= 2}.
      This IS a convex cone with apex (1,1) (an "affine cone"): for any x in K
      and t>0, (1,1) + t*(x-(1,1)) is still in K. Translating the apex to the
      origin via y = x - (1,1):
        K0 = {y in R^2 : y1 + y2 >= 0}  =  {y : <(1,1), y> >= 0}.
      K0 is a HALF-PLANE. A half-plane cone has exactly ONE facet (the boundary
      line y1+y2=0) and NO extreme rays in the strict sense (the boundary is a
      line, not a ray). Any two non-collinear vectors in K0 generate it.

  (C) The AM-GM half-space RESTRICTED to the first quadrant
        K_+ = {(phi, nu) : phi >= 0, nu >= 0, phi + nu >= 2}.
      This is what 10A_PATH_D_COMPUTATION.md calls "the AM-GM cone." It is the
      intersection of the half-plane (B) with the closed first quadrant. The
      first-quadrant restriction is NOT conical after translating the apex: the
      constraints phi>=0, nu>=0 become y1>=-1, y2>=-1, which are inhomogeneous.
      So K_+ is an affine cone (apex (1,1)) whose translated version has three
      bounding half-spaces, only one of which is a true cone through the origin.

We analyze both (B) and (C).
""")

    # ---- (B) The pure AM-GM cone K0 (half-plane through origin) ----
    print("--- Object B: pure AM-GM cone K0 = {y : y1+y2 >= 0} ---")
    print("Facets (as inequalities <a,y> >= 0): a single one, a = (1,1).")
    print("Boundary: the line y1 + y2 = 0, spanned by the vector (1,-1).")
    print("Extreme rays: NONE in the strict sense. The boundary is a line,")
    print("  not a ray. Equivalently, the cone is generated by, e.g.,")
    print("  {(1,0), (-1,1)} or any two non-collinear vectors inside it.")
    print("This is a NON-POINTED cone (it contains the line through (1,-1)).")
    print("Dimension: 2. Lineality space: span{(1,-1)}, dimension 1.")
    print()

    # ---- (C) The restricted set K_+ ----
    print("--- Object C: restricted set K_+ (the 'AM-GM cone' of 10A) ---")
    print("In apex-translated coordinates y = (phi-1, nu-1):")
    print("  K_+ = {y : y1 >= -1, y2 >= -1, y1 + y2 >= 0}.")
    print("This is NOT a cone through origin (the constants -1 break homogeneity).")
    print("It is a 2D polyhedron: a wedge with apex at y=(0,0) cut by two")
    print("half-planes at y1=-1 and y2=-1.")

    # Find its vertices (intersections of pairs of boundary lines)
    print("\nVertices of K_+ (intersection of pairs of boundary lines):")
    lines = [  # (a, b) such that a.y = b
        (np.array([1.0, 0.0]), -1.0),   # y1 = -1
        (np.array([0.0, 1.0]), -1.0),   # y2 = -1
        (np.array([1.0, 1.0]), 0.0),    # y1+y2 = 0
    ]
    verts = []
    for i in range(3):
        for j in range(i + 1, 3):
            M = np.vstack([lines[i][0], lines[j][0]])
            rhs = np.array([lines[i][1], lines[j][1]])
            try:
                v = np.linalg.solve(M, rhs)
            except np.linalg.LinAlgError:
                continue
            # Check feasibility
            ok = True
            for k in range(3):
                a, b = lines[k]
                # constraint is a.y {>=,>=,>=} b  i.e. y1>=-1, y2>=-1, y1+y2>=0
                if a @ v < b - 1e-9:
                    ok = False
                    break
            if ok:
                verts.append(v)
                phi_v, nu_v = v[0] + 1, v[1] + 1
                print(f"  lines {i},{j}: y = {np.round(v,3)}  "
                      f"(phi,nu) = ({phi_v:.3f},{nu_v:.3f})")
    verts = np.array(verts)
    print(f"\nK_+ has {len(verts)} vertices.")
    if len(verts) >= 2:
        # Direction rays from apex (0,0) through each vertex
        print("Direction rays from apex (y=0) through each vertex:")
        rays = []
        for v in verts:
            d = v / np.linalg.norm(v)
            rays.append(d)
            print(f"  direction {np.round(d,4)} (phi,nu) direction "
                  f"({d[0]+0:.3f},{d[1]+0:.3f})")

    # ---- Dual cones ----
    # Object B (pure AM-GM cone): K0 = {y : <(1,1), y> >= 0}.
    # Dual K0* = { z : <z,y> >= 0 for all y in K0 }.
    # For a half-plane {y : <a,y> >= 0}, the dual is the ray {t*a : t >= 0}.
    print("\n--- Dual cones ---")
    print("Dual of K0 (object B):  K0* = { t*(1,1) : t >= 0 }  -- a single ray.")
    print("  Reason: K0 is a half-plane bounded by the line orthogonal to (1,1);")
    print("  only vectors parallel to (1,1) make a non-negative inner product")
    print("  with EVERY vector in K0. So the dual is 1-dimensional.")
    print()
    print("Dual of K_+ (object C):  the apex-translated K_+ is not a cone through")
    print("  the origin (the constraints y1>=-1, y2>=-1 are inhomogeneous), so it")
    print("  has no dual cone in the standard sense. Its recession cone is K0,")
    print("  whose dual is again the ray {t*(1,1) : t>=0}.")
    print()
    print("DUAL FOUR-FOLD CHECK:")
    print("  Pure AM-GM dual:    1 ray  ->  ONE-fold, not four.")
    print("  Restricted dual:    same 1 ray (recession-cone dual).")
    print("  Neither object B nor C has a dual with four natural sectors.")

    # ---- Plot: primal half-plane (object B) and its dual ray ----
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    # Left: object B (half-plane y1+y2 >= 0) with the constraint curve overlaid
    ax = axes[0]
    yy1, yy2 = np.meshgrid(np.linspace(-3, 4, 400), np.linspace(-3, 4, 400))
    half = (yy1 + yy2 >= 0).astype(float)
    ax.contourf(yy1, yy2, half, levels=[0.5, 1.5], colors=["#cce5ff"], alpha=0.6)
    ax.contour(yy1, yy2, yy1 + yy2, levels=[0], colors="b", linewidths=1.5)
    # constraint curve phi*nu=1 in y-coordinates: (y1+1)(y2+1)=1 -> y2 = -y1/(y1+1)
    y1c = np.linspace(-0.999, 3, 400)
    y2c = -y1c / (y1c + 1)
    ax.plot(y1c, y2c, "k-", lw=2.5, label=r"constraint $\phi\nu=1$")
    y1c2 = np.linspace(-3, -1.001, 200)
    y2c2 = -y1c2 / (y1c2 + 1)
    ax.plot(y1c2, y2c2, "k-", lw=2.5)
    ax.plot([0], [0], "ro", ms=10, label="equator (apex)")
    # the lineality direction (1,-1)
    t = np.linspace(-2, 2, 2)
    ax.plot(t, -t, "g--", lw=1.5, label="lineality span{(1,-1)}")
    ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
    ax.set_xlim(-3, 4); ax.set_ylim(-3, 4); ax.set_aspect("equal")
    ax.set_xlabel(r"$y_1 = \phi-1$"); ax.set_ylabel(r"$y_2 = \nu-1$")
    ax.set_title("Object B: pure AM-GM cone K0 (half-plane)\n1 facet, 0 extreme rays")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)

    # Right: the dual ray {t*(1,1) : t>=0}
    ax = axes[1]
    tt = np.linspace(0, 4, 2)
    ax.plot(tt, tt, "r-", lw=3, label=r"dual ray $\{t(1,1): t\geq 0\}$")
    ax.plot([0], [0], "ko", ms=8)
    ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
    ax.set_xlim(-2, 4); ax.set_ylim(-2, 4); ax.set_aspect("equal")
    ax.set_xlabel(r"$z_1$"); ax.set_ylabel(r"$z_2$")
    ax.set_title("Dual K0*: a single ray\n1-dimensional, NOT four-fold")
    ax.legend(fontsize=10); ax.grid(alpha=0.3)

    plt.tight_layout()
    f2 = os.path.join(OUT, "fig2_primal_dual_cones.png")
    plt.savefig(f2, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"\nsaved {f2}")

    print("""
VERDICT (Task 2):
  Object B (the PURE AM-GM cone {y : y1+y2>=0}) is a 2D HALF-PLANE. It has
    - ONE facet (the boundary line y1+y2=0),
    - NO extreme rays (the boundary is a whole line, not a ray),
    - a 1D lineality space span{(1,-1)}.
  Its dual is the 1D ray {t*(1,1) : t>=0}.

  Object C (the AM-GM-cone-restricted-to-the-quadrant, used informally in 10A)
  is a wedge with TWO direction rays (from apex to its two corner vertices).
  Still not four.

  Neither object B nor object C has a natural four-fold structure. The number
  that convex geometry hands you is ONE (object B's facet count), TWO (object
  C's direction-ray count), or ZERO (object B's extreme rays). It is never four.

  The framework's four operators (Arjuna, Krsna, Kali-, Kali) are four
  DIRECTIONS in the (phi,nu) plane, but the constraint phi*nu=1 collapses them
  to TWO on-curve motions (the tangent direction has only +1 and -1).
  Off-curve, they are 4 axis-aligned vectors; the cone they span is the full
  first quadrant, not a four-fold decomposition of the AM-GM structure.

  This is a decisive negative result for the "convex geometry => four forces"
  reading.
""")


# ---------------------------------------------------------------------------
# TASK 3: Normal modes. Single agent (recap), then N=2 coupled.
# ---------------------------------------------------------------------------
def single_agent_expansion():
    """Expand around the equator; compute the quadratic (harmonic) mode and the
    quartic (anharmonic) correction analytically; verify numerically."""
    banner("TASK 3a: single-agent expansion around the equator")

    print("phi = 1 + eps,  nu = 1/(1+eps) = 1 - eps + eps^2 - eps^3 + eps^4 - ...")
    eps = np.array([1e-3])
    # Taylor coefficients of nu(eps) = 1/(1+eps)
    # Symbolic check via numpy.polynomial
    from numpy.polynomial import polynomial as P
    # 1/(1+x) = 1 - x + x^2 - x^3 + x^4 - ...
    coeffs_nu = np.array([1, -1, 1, -1, 1, -1])  # up to eps^5
    print("nu(eps) Taylor coeffs (c0, c1, ...):", coeffs_nu)

    # H(eps) = phi + nu = (1+eps) + 1/(1+eps)
    # c_k for H: c0=2, c1 = 1 + (-1) = 0, c2 = 0 + 1 = 1, c3 = -1, c4 = 1, ...
    coeffs_H = np.array([2, 0, 1, -1, 1, -1])
    print("H(eps) Taylor coeffs              :", coeffs_H)

    # V(eps) = H(eps) - 2
    coeffs_V = coeffs_H.copy(); coeffs_V[0] = 0.0
    print("V(eps) = H-2 Taylor coeffs         :", coeffs_V)
    print()
    print("=> V(eps) = eps^2 - eps^3 + eps^4 - eps^5 + ...")
    print("=> Leading harmonic:  V ~ eps^2,  so omega^2 = 2 * (1/2)*(d^2 V / d eps^2)")
    print("   Here d^2 V / d eps^2 |0 = 2 * c2 = 2,  so with Lagrangian L = (1/2) eps_dot^2 - V,")
    print("   omega^2 = V''(0) = 2,  omega = sqrt(2) ~ 1.4142")
    print()
    print("ONE normal mode. Frequency sqrt(2). This matches the Lagrangian Question's")
    print("finding that a single scalar field gives ONE mode, not four.")
    print()
    print("The cubic term -eps^3 BREAKS the phi<->nu symmetry: the potential is")
    print("anharmonic, so the spectrum is NOT the equally-spaced harmonic ladder.")
    print("This explains why 12_THE_SPECTRUM_RESULTS.md finds growing gaps, not 1,2,3,...")

    # Verify by directly computing the weighted sphere spectrum
    # (reproduce the canonical baseline)
    E = weighted_sphere_spectrum(num_points=1200, num_states=6)
    print("\nWeighted sphere spectrum (reproduced baseline):")
    for i, e in enumerate(E):
        print(f"  E_{i} = {e:.6f}")


def weighted_sphere_spectrum(num_points=1200, num_states=10):
    """Reproduce the framework's canonical weighted sphere baseline.
    Operator: -(1/2) d/dtheta (sin theta dpsi/dtheta) + V(theta) sin theta psi
              = E sin theta psi,  V = 2/sin(theta) - 2.
    Discretized as a generalized eigenvalue problem A psi = E B psi."""
    h = np.pi / (num_points + 1)
    theta = np.linspace(h, np.pi - h, num_points)
    s = np.sin(theta)
    s_minus = np.sin(theta - h / 2.0)
    s_plus = np.sin(theta + h / 2.0)
    potential = 2.0 / s - 2.0

    operator = np.zeros((num_points, num_points))
    diag = 0.5 * (s_plus + s_minus) / h ** 2 + potential * s
    upper = -0.5 * s_plus[:-1] / h ** 2
    lower = -0.5 * s_minus[1:] / h ** 2
    operator[np.diag_indices(num_points)] = diag
    operator[np.arange(num_points - 1), np.arange(1, num_points)] = upper
    operator[np.arange(1, num_points), np.arange(num_points - 1)] = lower
    weight = np.diag(s)
    eigenvalues, _ = eigh(operator, weight, subset_by_index=[0, num_states - 1])
    return eigenvalues


def task3_coupled_two_agents():
    """Two agents (phi_i, nu_i) with phi_i*nu_i=1 each, coupled by an interaction.
    Find the normal modes of the coupled system."""
    banner("TASK 3b: N=2 coupled agents on the AM-GM constraint")

    print("""
Setup:
  Two agents, each on its own AM-GM constraint:
      phi_1 * nu_1 = 1,   phi_2 * nu_2 = 1.
  Use log coordinates  u_i = log(phi_i),  so nu_i = e^{-u_i}.
  Each agent's self-energy:
      H_i = phi_i + nu_i = 2 cosh(u_i).
  Near the equator  u_i = 0:
      H_i ~ 2 + u_i^2 + (1/12) u_i^4 + ...

  Coupling: the SIMPLEST symmetric interaction preserving u -> -u on each agent
  is a quadratic spring between the two log-coordinates:
      V_coup = (kappa/2) (u_1 - u_2)^2.

  Total potential (drop the constant 2+2=4):
      V(u_1, u_2) = u_1^2 + u_2^2 + (kappa/2)(u_1 - u_2)^2 + (anharmonic).

  The Hessian at the origin is
      H = [[2 + kappa,  -kappa],
           [-kappa,     2 + kappa]]
  Eigenvalues:  lambda_+ = 2          (eigenvector (1, 1)/sqrt2 : IN-PHASE)
                lambda_- = 2 + 2 kappa (eigenvector (1,-1)/sqrt2 : OUT-OF-PHASE)

  So the number of normal modes = number of degrees of freedom = N = 2.
  The frequencies are sqrt(2) and sqrt(2 + 2 kappa).
""")

    kappas = [0.0, 0.1, 0.5, 1.0, 2.0]
    print(f"{'kappa':>8}  {'omega_in':>12}  {'omega_out':>12}")
    for kappa in kappas:
        H = np.array([[2 + kappa, -kappa],
                      [-kappa, 2 + kappa]])
        eigs = np.sort(np.linalg.eigvalsh(H))
        print(f"{kappa:8.3f}  {np.sqrt(eigs[0]):12.6f}  {np.sqrt(eigs[1]):12.6f}")

    print("""
OBSERVATION: For N=2 coupled agents, you get exactly 2 normal modes.
  - In-phase (center-of-mass): BOTH agents oscillate together along the curve.
  - Out-of-phase (relative):   agents swap, one goes +phi while other goes -phi.

The two modes have frequencies sqrt(2) and sqrt(2 + 2 kappa). The coupling kappa
is a FREE PARAMETER. It is NOT fixed by the AM-GM geometry. To get a specific
spectrum you must choose kappa externally. This is the first sign that the
geometry alone does not determine the gauge structure.
""")

    # Numerical verification: solve the coupled weighted sphere problem on the
    # 2D product manifold and confirm the mode count.
    # We will solve a 2D Schrodinger problem on (theta_1, theta_2) in (0,pi)^2
    # with V(theta_1, theta_2) = (2/sin theta_1 - 2) + (2/sin theta_2 - 2)
    #                            + kappa * (log cot(theta_1/2) - log cot(theta_2/2))^2
    # Use a coarse grid (Kronecker-product Laplacian) and report the lowest modes.
    kappa_test = 1.0
    n1 = 80  # grid per dimension -> 6400 unknowns; OK with sparse
    E2 = coupled_sphere_spectrum_2d(n1, kappa_test, num_states=6)
    print(f"Numerical check: 2D coupled problem, kappa = {kappa_test}, grid {n1}x{n1}")
    print("Lowest eigenvalues:")
    for i, e in enumerate(E2):
        print(f"  E_{i} = {e:.6f}")
    # Predicted: modes are combinations of one-particle excitations.
    # omega_in^2 = 2, omega_out^2 = 2 + 2 kappa = 4.
    # Ground state energy shift ~ omega_in/2 + omega_out/2 ... but this is the
    # full weighted-spectrum, not the flat harmonic one. So we just confirm the
    # qualitative mode count: the lowest 3 states should be (0,0), (1,0), (0,1)-ish.

    # Plot the two single-agent modes and the coupled-mode splitting
    fig, ax = plt.subplots(figsize=(8, 5))
    kappas_plot = np.linspace(0, 3, 100)
    omega_in = np.sqrt(2 + 0 * kappas_plot)
    omega_out = np.sqrt(2 + 2 * kappas_plot)
    ax.plot(kappas_plot, omega_in, "C0-", lw=2, label=r"in-phase $\sqrt{2}$")
    ax.plot(kappas_plot, omega_out, "C1-", lw=2,
            label=r"out-of-phase $\sqrt{2+2\kappa}$")
    ax.axhline(np.sqrt(2), color="C0", ls=":", alpha=0.5)
    ax.set_xlabel(r"coupling $\kappa$")
    ax.set_ylabel(r"normal-mode frequency $\omega$")
    ax.set_title("N=2 coupled agents: 2 normal modes (frequencies depend on free kappa)")
    ax.legend(); ax.grid(alpha=0.3)
    f3 = os.path.join(OUT, "fig3_two_agent_modes.png")
    plt.savefig(f3, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"saved {f3}")


def coupled_sphere_spectrum_2d(n, kappa, num_states=6):
    """Solve the 2D coupled weighted-sphere problem on a product grid using
    sparse Kronecker operators. Returns the lowest eigenvalues.

    V(theta1, theta2) = V1 + V2 + kappa*(u1 - u2)^2,
    with u_i = log cot(theta_i/2), V_i = 2/sin(theta_i) - 2.
    Operator (weighted by sin theta1 sin theta2):
       -(1/2) [d_t1 (sin t1 d_t1) + d_t2 (sin t2 d_t2)] + V * sin t1 sin t2
    """
    from scipy.sparse import diags, kron, eye, csr_matrix
    from scipy.sparse.linalg import eigsh

    h = np.pi / (n + 1)
    t = np.linspace(h, np.pi - h, n)
    s = np.sin(t)
    sm = np.sin(t - h / 2)
    sp = np.sin(t + h / 2)

    # 1D weighted operator A1 (size n x n):  -0.5 * d/dt (sin t d/dt)
    main = 0.5 * (sp + sm) / h ** 2
    off = -0.5 * sp[:-1] / h ** 2
    A1 = diags([off, main, off], [-1, 0, 1], format="csr")

    W1 = diags([s], [0], format="csr")  # weight sin(t)

    # 2D: A = kron(A1, W1) + kron(W1, A1)   [standard product-form weighted Laplacian]
    I = eye(n, format="csr")
    A2 = kron(A1, W1, format="csr") + kron(W1, A1, format="csr")
    W2 = kron(W1, W1, format="csr")

    # Potential
    V1 = 2.0 / s - 2.0
    u = np.log(np.cos(t / 2) / np.sin(t / 2))  # = log cot(t/2)
    # Broadcast on the 2D grid (i index = t1, j index = t2). kron indexing: flatten
    # in row-major; eigsh with default uses column-major but consistent with kron.
    T1, T2 = np.meshgrid(t, t, indexing="ij")
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    U1, U2 = np.meshgrid(u, u, indexing="ij")
    V_grid = (2.0 / S1 - 2.0) + (2.0 / S2 - 2.0) + kappa * (U1 - U2) ** 2
    weight_grid = S1 * S2
    # Total operator: A2 + diag(V * weight), generalized eigenproblem with B = diag(weight)
    V_total = V_grid * weight_grid
    op = A2 + diags([V_total.ravel(order="C")], [0], format="csr")
    B = diags([weight_grid.ravel(order="C")], [0], format="csr")

    E = eigsh(op, k=num_states, M=B, which="SM", return_eigenvectors=False,
              tol=1e-8)
    return np.sort(E)


# ---------------------------------------------------------------------------
# TASK 4: N coupled agents; mode count vs N; can we hit dim 12?
# ---------------------------------------------------------------------------
def task4_n_agents_mode_count():
    banner("TASK 4: N coupled agents on S^2; mode-count growth; gauge-structure check")

    print("""
We have N agents on the constraint phi_i nu_i = 1. In log coordinates u_i,
each has a self-H_i = 2 cosh(u_i). Near the ground state (all u_i = 0) we expand
to quadratic order:

    V_2(u_1, ..., u_N) = sum_i u_i^2  +  (1/2) sum_{i,j} kappa_{ij} (u_i - u_j)^2.

The quadratic form lives on R^N. The Hessian is an N x N matrix, so it has
EXACTLY N eigenvalues. Therefore the linearized system has exactly N normal
modes. The mode count grows LINEARLY in N.
""")

    # Demonstrate with explicit diagonalization for several N
    print("Mode counts vs N (with uniform all-to-all coupling kappa_{ij} = kappa/N):")
    print(f"{'N':>4}  {'# modes':>10}  {'# Goldstone-like (kappa=0)':>26}")
    for N in [1, 2, 3, 4, 5, 6, 7, 8, 12]:
        # Build Hessian
        kappa = 1.0
        H = np.zeros((N, N))
        for i in range(N):
            H[i, i] += 2.0  # self u_i^2
        for i in range(N):
            for j in range(i + 1, N):
                kij = kappa / N
                H[i, i] += kij
                H[j, j] += kij
                H[i, j] -= kij
                H[j, i] -= kij
        eigs = np.linalg.eigvalsh(H)
        zero_like = np.sum(np.abs(eigs) < 1e-9)
        print(f"{N:>4}  {N:>10}  {zero_like:>26}")
        if N in (1, 2, 3):
            print(f"        frequencies^2: {np.round(eigs, 4)}")

    print("""
Universal result:
    # normal modes  =  N    (linear in N)
    # zero modes    =  1 if kappa=0,  else 0
       (the "center-of-mass" or in-phase direction becomes the only flat
        direction when the coupling vanishes).

Target: Standard Model gauge group SU(3) x SU(2) x U(1) has dimension
    dim SU(3) = 3^2 - 1 = 8
    dim SU(2) = 2^2 - 1 = 3
    dim U(1)  = 1
    total      = 12.

To get 12 normal modes from N agents on the AM-GM constraint, we need N = 12.
""")

    # Check whether for N=2 or N=3 we ever see a degeneracy pattern matching
    # any Standard Model subgroup dimensions (e.g., 1+3+8 = 12; 1+3 = 4; 8; 3; 1).
    print("Checking whether any natural coupling symmetry yields SM-like degeneracies:")

    # Try three coupling topologies for N agents and look at the eigenvalue
    # multiplicity structure.
    def make_hessian(topology, N, kappa=1.0):
        H = np.zeros((N, N))
        for i in range(N):
            H[i, i] += 2.0
        if topology == "all_to_all":
            for i in range(N):
                for j in range(i + 1, N):
                    kij = kappa / max(N - 1, 1)
                    H[i, i] += kij; H[j, j] += kij
                    H[i, j] -= kij; H[j, i] -= kij
        elif topology == "ring":
            for i in range(N):
                j = (i + 1) % N
                H[i, i] += kappa; H[j, j] += kappa
                H[i, j] -= kappa; H[j, i] -= kappa
        elif topology == "chain":
            for i in range(N - 1):
                H[i, i] += kappa; H[i + 1, i + 1] += kappa
                H[i, i + 1] -= kappa; H[i + 1, i] -= kappa
        return H

    for topology in ["all_to_all", "ring", "chain"]:
        print(f"\n  Topology: {topology}")
        for N in [2, 3, 4, 8, 12]:
            H = make_hessian(topology, N)
            eigs = np.linalg.eigvalsh(H)
            freqs = np.sqrt(np.clip(eigs, 0, None))
            # Group by rounded value
            from collections import Counter
            c = Counter(np.round(freqs, 4))
            mults = sorted(c.values(), reverse=True)
            # Does the multiplicity structure hit any SM-like pattern?
            hits = []
            if mults == [1, 1] and N == 2:
                hits.append("U(1)xU(1)")
            if 8 in mults:
                hits.append("SU(3)-adjoint dim 8")
            if 3 in mults:
                hits.append("SU(2)-adjoint dim 3")
            if 1 in mults:
                hits.append("U(1) dim 1")
            hits_str = ", ".join(hits) if hits else "-"
            print(f"    N={N:>2}: mults={mults}   possible SM dim hits: {hits_str}")

    print("""
VERDICT (Task 4):
  - The mode count grows as N, not N^2.
  - No natural coupling topology on the AM-GM constraint produces an 8-fold
    degeneracy (SU(3) adjoint) from N=2 or N=3. The only way to get 8 modes
    in a single multiplet is to put N=8 agents and arrange a coupling that
    has an SO(8) symmetry, which is then circular reasoning.
  - To get the full SM gauge dimension 12 you need N = 12 agents, and even
    then the degeneracy structure is dictated by the coupling, not by AM-GM.

PARTIAL POSITIVE WORTH NOTING (not a derivation, but a real pattern):
  All-to-all symmetric coupling on N=4 agents yields a 3+1 frequency split
  (a 3-fold-degenerate "relative" manifold plus a 1-fold "center-of-mass").
  The dimensions 3 and 1 ARE the dimensions of the SU(2) adjoint and U(1)
  respectively. This is the only SM-like multiplet structure that emerges
  from a natural coupling topology without external symmetry input.
  However:
    - The 3+1 split is generic for any fully-symmetric coupling on 4 bodies
      (it is the standard center-of-mass vs. relative decomposition), so it
      carries little information specific to AM-GM.
    - It still misses SU(3) entirely (no 8-fold degeneracy anywhere).
    - The coupling kappa is a free parameter; the split's existence does not
      depend on phi*nu=1.

The gauge structure cannot emerge from the AM-GM geometry. The barrier stated
in 10A_PATH_D_COMPUTATION.md and 12_THE_SPECTRUM_RESULTS.md is REPRODUCED and
CONFIRMED: bare S^2 (or N copies of it) cannot yield SU(3).
""")


# ---------------------------------------------------------------------------
# TASK 5: Verdict synthesis (printed; no figure).
# ---------------------------------------------------------------------------
def task5_verdict():
    banner("TASK 5: honest verdict on Path D")

    print("""
PATH D VERDICT: PARTIALLY OPEN, STRUCTURALLY BLOCKED ON THE FOUR-FORCES CLAIM

What Path D succeeds at [S, structural]:
  1. The AM-GM inequality + the constraint phi*nu=1 gives a clean 1D dynamical
     system on a meridian of S^2, with a globally-attracting equator.
  2. The local expansion V(eps) = eps^2 - eps^3 + eps^4 - ... is a stable,
     non-pathological anharmonic oscillator. The local harmonic frequency is
     omega = sqrt(2). The anharmonic correction is what makes the canonical
     weighted-sphere spectrum's gaps grow (matching the framework's own
     audit in 12_THE_SPECTRUM_RESULTS.md). Reproduced baseline:
       E_0=0.5966, E_1=2.6501, E_2=5.4677, E_3=9.1242, E_4=13.6720.
  3. The pure AM-GM cone (object B) is a 2D half-plane with one facet, zero
     extreme rays, and a 1D dual. The quadrant-restricted version (object C)
     is a wedge with two direction rays. Neither is four-fold.

Where Path D is BLOCKED [S, structural, decisive negative]:
  1. FOUR OPERATORS COLLAPSE TO TWO.
     On the constraint phi*nu=1, the four operators {+phi, -phi, +nu, -nu}
     reduce to a single tangent direction (with two signs). There is no
     independent four-fold structure on the curve.
  2. THE AM-GM CONE IS A HALF-PLANE (OR A 2-RAY WEDGE), NOT A FOUR-SECTOR OBJECT.
     Object B has ONE facet and a 1D dual ray; object C has TWO direction rays.
     Convex geometry hands you the numbers 0, 1, or 2 -- never 4.
  3. SU(3) CANNOT EMERGE.
     N coupled AM-GM agents produce exactly N normal modes (linear growth).
     For N=2: 2 modes. For N=3: 3 modes. No topology yields an 8-fold
     degeneracy (the SU(3) adjoint dimension) without first building in
     SO(8)-style symmetry by hand, which is circular.
  4. N=12 MODES FOR THE FULL SM REQUIRES N=12 AGENTS AND AN EXTERNAL COUPLING.
     The gauge structure is dictated by the coupling tensor kappa_{ij}, which
     the AM-GM geometry does not determine. The geometry contributes only the
     universal self-frequency sqrt(2); everything else is a free parameter.

The single PARTIAL POSITIVE [C, structural coincidence, not a derivation]:
  All-to-all symmetric coupling on N=4 agents yields a 3+1 frequency split:
  a 3-fold-degenerate "relative" manifold plus a 1-fold "center-of-mass".
  The numbers 3 and 1 coincide with the dimensions of the SU(2) adjoint and
  U(1) respectively. This is suggestive, but:
    - It is generic for ANY symmetric 4-body coupling (it is just the
      center-of-mass vs. relative decomposition), so it carries little
      information specific to AM-GM.
    - It still misses SU(3) entirely.
    - It does not depend on phi*nu=1; it would arise from four coupled
      harmonic oscillators of any kind.

What Path D DOES NOT prove but leaves open [I/C]:
  - The structural correspondence between "the AM-GM lower bound is a
    confinement-like restoring force" (already noted in 09_PATH_D_THE_AMGM_GEOMETRY.md)
    remains a suggestive qualitative analogy. It is not a derivation of the
    strong coupling constant.
  - The P-D1 prediction (alpha_s ~ sin(theta)) is not falsified by this
    computation, but it is not derived either. It remains an Ansatz.

BOTTOM LINE FOR THE FRAMEWORK:
  Path D is the most original route, and it produced three clean negative
  results:
    (i)   the four operators are not independent on S^2,
    (ii)  the AM-GM cone is a half-plane (1 facet, 1D dual), not a four-fold
          object; the quadrant-restricted version has 2 direction rays,
    (iii) N agents give N modes (linear), and no natural coupling yields the
          8-fold SU(3) adjoint.
  Combined with the prior spectral barrier (no degeneracy 8 on S^2), the
  "four forces = four lines" reading cannot be derived from the AM-GM
  geometry alone. Path D as a STANDALONE route to the SM gauge structure is
  BLOCKED.

  Path D remains valuable as an internal consistency check on the framework's
  dynamical story (equator as attractor, anharmonic correction explains the
  non-harmonic spectrum). But it cannot complete the four-force map without
  importing structure from outside (Path A: extra dimensions; Path B: CFT).

  This is a NEGATIVE result on the most original path, and the framework's
  own kill-criterion (item 1 of the Lagrangian Question: spectral modes do
  not match SM gauge structure) is now satisfied FOR PATH D specifically.
""")


def main():
    task1_cone_and_sphere()
    task2_convex_geometry()
    single_agent_expansion()
    task3_coupled_two_agents()
    task4_n_agents_mode_count()
    task5_verdict()


if __name__ == "__main__":
    main()

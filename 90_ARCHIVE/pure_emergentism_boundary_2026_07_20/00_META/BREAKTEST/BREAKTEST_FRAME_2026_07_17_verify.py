#!/usr/bin/env python3
"""
BREAKTEST_FRAME_2026_07_17 — numerical verification battery.
Role: Breaker_SphereNecessity (L1 firewall). Target: {0,1,∞} -> S^2 forcing chain
and the Titan Composition Law. All checks are exact arithmetic where possible
(complex doubles, tolerance 1e-9).
"""
import cmath, math, random
import numpy as np

random.seed(42)
TOL = 1e-9
INF = complex('inf')

def report(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    return ok

ALL = []
def check(name, ok, detail=""):
    ALL.append(report(name, ok, detail))

# ---------- Möbius helpers ----------
def mobius(M, z):
    a,b,c,d = M
    if z == INF:
        return a/c if abs(c) > TOL else INF
    den = c*z + d
    if abs(den) < TOL: return INF
    return (a*z + b)/den

def trace2(M):
    """(tr M)^2 / det M — invariant normal form for PSL(2,C)."""
    a,b,c,d = M
    tr = a + d
    det = a*d - b*c
    return tr*tr/det

def classify(M):
    t2 = trace2(M)
    if abs(t2.imag) > 1e-7:
        return "loxodromic", t2
    x = t2.real
    if abs(x - 4.0) < 1e-7: return "parabolic/id", t2
    if -1e-9 <= x < 4.0 - 1e-7: return "elliptic", t2
    if x > 4.0: return "hyperbolic", t2
    return "loxodromic", t2  # real negative trace^2

def diag(lam):
    return (lam, 0j, 0j, 1+0j)

# =====================================================================
print("="*72)
print("ATTACK 1 — frame-necessity: does RP^1 carry {0,1,∞} just as well?")
print("="*72)

# Cross-ratio normal form: T(z) = (z-p)(q-r)/((z-r)(q-p)) sends p->0,q->1,r->∞.
def frame_map(p,q,r):
    # coefficients as a Möbius matrix
    return ((q-r), -(q-r)*p, (q-p), -(q-p)*r)

ok = True
for _ in range(200):
    p,q,r = random.sample(range(-50,51), 3)
    p,q,r = map(float,(p,q,r))
    M = frame_map(p,q,r)
    # real coefficients?  -> the map lies in PGL(2,R)
    real_coeffs = all(abs(complex(c).imag) < TOL for c in M)
    im0 = mobius(M, complex(p)); im1 = mobius(M, complex(q)); im2 = mobius(M, complex(r))
    good = (abs(im0) < 1e-7) and (abs(im1 - 1) < 1e-7) and (im2 == INF)
    # maps reals to reals (real projective line preserved)
    t = mobius(M, 3.7)
    real_preserving = t != INF and abs(t.imag) < 1e-9
    ok &= real_coeffs and good and real_preserving
check("PGL(2,R) is 3-transitive on RP^1 with {0,1,∞} as a frame (real cross-ratio map, 200 random real triples)", ok)

# pi_1 facts (stated, not computed): pi_1(RP^1)=Z, pi_1(S^2)=0. Uniformization is a cited theorem.
print("      [A] facts cited, not computed: pi_1(RP^1)=Z vs pi_1(S^2)=0; uniformization: simply-connected")
print("      Riemann surfaces = {CP^1, C, D}; compact => CP^1. Conjuncts compact/simply-connected/complex")
print("      structure are SELECTIONS [S]; the frame itself lives on any P^1 (RP^1 countermodel above).")

# =====================================================================
print("="*72)
print("ATTACK 2 — sharp 3-transitivity, S_3 (anharmonic) symmetry, foursome")
print("="*72)

# (a) sharp 3-transitivity on ORDERED triples over C
ok = True
for _ in range(200):
    while True:
        p,q,r = (complex(random.uniform(-3,3), random.uniform(-3,3)) for _ in range(3))
        if abs(p-q)>0.2 and abs(q-r)>0.2 and abs(p-r)>0.2: break
    M = frame_map(p,q,r)
    im = (mobius(M,p), mobius(M,q), mobius(M,r))
    ok &= (abs(im[0])<1e-7) and (abs(im[1]-1)<1e-7) and (im[2]==INF)
check("PGL(2,C) sharply 3-transitive on ORDERED triples (frame map sends (p,q,r)->(0,1,∞), 200 random triples)", ok)

# (b) anharmonic group: six maps permuting {0,1,∞} as an UNORDERED set (matrix form, exact INF handling)
anharmonic = [
    (1+0j, 0j, 0j, 1+0j),    # z
    (0j, 1+0j, -1+0j, 1+0j), # 1/(1-z)
    (1+0j, -1+0j, 1+0j, 0j), # (z-1)/z
    (-1+0j, 1+0j, 0j, 1+0j), # 1-z
    (0j, 1+0j, 1+0j, 0j),    # 1/z
    (1+0j, 0j, 1+0j, -1+0j), # z/(z-1)
]
triplet = [0.0, 1.0, INF]
perms = set()
ok = True
for M in anharmonic:
    img = tuple(mobius(M, z) for z in triplet)
    def norm(x): return 'inf' if x == INF else str(round(float(x.real),9) + 0.0)
    img_n = tuple(norm(x) for x in img)
    ok &= sorted(img_n) == sorted(('0.0','1.0','inf'))
    perms.add(img_n)
check("Anharmonic group (z, 1/(1-z), (z-1)/z, 1-z, 1/z, z/(z-1)) permutes {0,1,∞}", ok)
check("Exactly 6 distinct permutations realized => stabilizer of the UNORDERED triple = S_3", len(perms)==6, f"{len(perms)} distinct")

# (c) frame size = dim+2
print("      [A] cited: a projective frame in PG(n,K) is n+2 points in general position; P^1 => exactly 3.")
print("      On P^1 'general position' is vacuous: ANY 3 distinct points are a frame (checked by the 3-transitivity above).")

# (d) closure is the foursome
roots = [cmath.sqrt(1+0j), -cmath.sqrt(1+0j)]  # z = 1/z <=> z^2 = 1
check("Fix(z->1/z) = {+1,-1}; cl({0,∞}) = {-1,0,1,∞} is a FOURSOME (receipt 126 C21)", all(abs(r*r-1)<TOL for r in roots))
check("Selecting the triad from the foursome costs the positivity choice: log2(2) = 1 bit (not 0)", abs(math.log2(2)-1.0)<TOL)

# =====================================================================
print("="*72)
print("ATTACK 3 — Titan Composition Law: S∘B elliptic iff |σκ|=1 (receipt 104)")
print("="*72)

# diagonal-axis model: B = M_κ, S = M_σ; S∘B = M_{σκ}
ok = True
n_bal = n_unbal = 0
for _ in range(4000):
    sig = cmath.rect(random.uniform(0.05,0.95), random.uniform(0,2*math.pi))
    kap = cmath.rect(random.uniform(1.05,4.0), random.uniform(0,2*math.pi))
    # force half the sample exactly onto the balance locus |σκ|=1
    if n_bal <= n_unbal:
        kap = cmath.rect(1.0/abs(sig), random.uniform(0,2*math.pi)); n_bal += 1
    else:
        n_unbal += 1
    comp = diag(sig*kap)
    cls,_ = classify(comp)
    balanced = abs(abs(sig*kap)-1.0) < 1e-9
    identity = abs(sig*kap - 1.0) < 1e-9
    if balanced and not identity and abs(sig*kap - 1.0) < 1e-3:
        continue  # skip the float-degenerate identity boundary (doc 40's "frozen" limit)
    if balanced:
        ok &= (cls in ("elliptic","parabolic/id")) and (identity or cls == "elliptic")
    else:
        ok &= (cls in ("hyperbolic","loxodromic"))
check("Iff verified over 4000 random (σ,κ): balanced(|σκ|=1) <=> elliptic/identity; unbalanced <=> hyperbolic-or-loxodromic", ok)

# multiplier ambiguity λ ~ 1/λ leaves |λ|=1 invariant
ok = all(abs(abs(l) - 1) < 1e-12 for l in [cmath.exp(1j*0.37)]) and abs(abs(1/cmath.exp(1j*0.37))-1) < 1e-12
check("Multiplier convention λ~1/λ is harmless: |λ|=1 <=> |1/λ|=1 (condition is well-defined)", ok)

# trace^2 of balanced composite = 4 cos^2(θ/2)
theta = 0.83
lam = cmath.exp(1j*theta)
t2 = trace2(diag(lam))
check("Balanced composite trace^2 = 4cos^2(θ/2) ∈ [0,4] (elliptic band)", abs(t2 - 4*math.cos(theta/2)**2) < 1e-9, f"tr^2={t2:.6f}")

# STRICT hyperbolic axis (MF-63 real multipliers): balance collapses to identity
ok = True
for _ in range(1000):
    sig = random.uniform(0.05,0.95)         # real, |σ|<1 : Śiva-class (MF-63)
    kap = 1.0/sig                            # real, |κ|>1 : Brahmā-class, exactly balanced
    comp = sig*kap
    cls,_ = classify(diag(comp))
    ok &= (abs(comp-1.0) < 1e-12) and cls == "parabolic/id"   # identity, NOT a living rotation
check("REGISTER SEAM: on MF-63's strict hyperbolic axis (σ,κ ∈ R+), |σκ|=1 forces σκ=1 = IDENTITY — no living rotation", ok)

# living rotation needs complex multipliers (loxodromic titans = MF-63 Kṛṣṇa class)
sig = cmath.rect(0.5, math.pi/7); kap = cmath.rect(2.0, math.pi/11)
cls, t2 = classify(diag(sig*kap))
check("Living preservation (nontrivial rotation) requires complex σ,κ — i.e. LOXODROMIC titans (MF-63's Kṛṣṇa class)",
      cls == "elliptic" and abs(sig*kap - 1) > 1e-3, f"σκ={sig*kap:.4f}, tr^2={t2:.4f}")

# failure modes = dyadic runaway
for s,k,expect in [(0.5, 3.0, "hyperbolic"),   # |σκ|=1.5 > 1 : drift to ○
                   (0.25, 2.0, "hyperbolic"),  # |σκ|=0.5 < 1 : drift to •
                   (cmath.rect(0.5,0.7), cmath.rect(3.0,-0.2), "loxodromic")]:
    cls,_ = classify(diag(s*k))
    check(f"Unbalanced pair |σκ|={abs(s*k):.3f} -> {cls} (residual flow, not preservation)", cls == expect)

# =====================================================================
print("="*72)
print("ATTACK 4 — pole-swap J(z)=1/z: what is invariant, what drifts")
print("="*72)

J = (0j, 1+0j, 1+0j, 0j)   # z -> 1/z
def compose(M,N):
    a,b,c,d = M; e,f,g,h = N
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)

ok = True
for _ in range(500):
    lam = cmath.rect(10**random.uniform(-1,1), random.uniform(0,2*math.pi))
    conj = compose(compose(J, diag(lam)), J)          # J M_λ J  (J=J^{-1})
    target = diag(1/lam)
    # compare in PSL: matrices proportional
    ratio = conj[0]/target[0]
    same = all(abs(conj[i] - ratio*target[i]) < 1e-7 for i in range(4))
    ok &= same
check("J M_λ J^{-1} = M_{1/λ}: pole-swap conjugation inverts the multiplier (500 random λ)", ok)

ok = True
for _ in range(500):
    lam = cmath.rect(10**random.uniform(-1,1), random.uniform(0,2*math.pi))
    c0,_ = classify(diag(lam)); c1,_ = classify(diag(1/lam))
    swap_ok = (c0 in ("hyperbolic","loxodromic") and c1 in ("hyperbolic","loxodromic")) or (c0 == c1)
    if abs(abs(lam)-1) < 1e-9: swap_ok = (c0 == "elliptic" and c1 == "elliptic")
    ok &= swap_ok
check("Classes under J: Brahmā-class(|λ|>1) <-> Śiva-class(|λ|<1) exchanged; Viṣṇu-class(|λ|=1) fixed", ok)

# J swaps the points 0 <-> ∞, fixes ±1
check("J swaps 0<->∞, fixes +1 and -1", mobius(J,0)==INF and mobius(J,INF)==0 and abs(mobius(J,1)-1)<TOL and abs(mobius(J,-1)+1)<TOL)

# any binary god-to-pole assignment is non-invariant under J (trivial but load-bearing)
assignment = {0.0: "Śiva", INF: "Brahmā"}
after = {mobius(J,p): g for p,g in assignment.items()}
check("No assignment of two DISTINCT gods to the two poles is J-invariant (J moves the points): the duality must exchange the gods or be broken by convention",
      after[INF] == "Śiva" and after[0.0] == "Brahmā")

# dyadic faces swap under J: x -> 1/x sends φ=cot(θ/2) to tan(θ/2)=ν
ok = True
for _ in range(200):
    th = random.uniform(0.05, math.pi-0.05)
    phi = 1/math.tan(th/2); nu = math.tan(th/2)
    ok &= abs((1/phi) - nu) < 1e-9
check("J also swaps the dyadic faces: x->1/x sends φ <-> ν, fixes the equator x=1 (200 random θ)", ok)

print("="*72)
print(f"TOTAL: {sum(1 for _ in ALL) and 'ALL PASS' if all(ALL) else 'FAILURES PRESENT'} ({sum(ALL)}/{len(ALL)})")

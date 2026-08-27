"""Saturation Lemma — numerical check and adversarial probe.

CLAIM. Freedom F, compensator C on [0,1]. Two premises:
  P1 compensation is costly:      A(c) available capacity, decreasing, A(1)=0
  P2 uncompensated freedom dies:  S(c) persistence,        increasing, S(0)=0
Then F = A*S is 0 at both ends, positive inside => INTERIOR MAXIMUM.
Question 1: is the interior max guaranteed? Question 2: is F UNIMODAL?
"""
import math, random

def interior_max(A, S, n=20001):
    xs = [i/(n-1) for i in range(n)]
    F  = [A(x)*S(x) for x in xs]
    i  = max(range(n), key=lambda k: F[k])
    return xs[i], F[i], F

def peaks(F, eps=1e-12):
    """count strict local maxima on the interior"""
    return sum(1 for k in range(1, len(F)-1)
               if F[k] > F[k-1]+eps and F[k] > F[k+1]+eps)

print("=== 1 · does an interior maximum appear across many admissible A,S? ===")
random.seed(7)
fails = 0
for t in range(2000):
    a, b = random.uniform(.2,6), random.uniform(.2,6)
    A = lambda c,a=a: (1-c)**a          # decreasing, A(1)=0
    S = lambda c,b=b: c**b              # increasing,  S(0)=0
    x,f,_ = interior_max(A,S,2001)
    if not (0 < x < 1 and f > 0): fails += 1
print(f"  2000 random (A,S) pairs · interior max failed in {fails}")
print(f"  and the optimum is exact: for A=(1-c)^a, S=c^b, argmax = b/(a+b)")
for a,b in [(1,1),(2,1),(1,3),(5,2)]:
    x,_,_ = interior_max(lambda c: (1-c)**a, lambda c: c**b, 200001)
    print(f"    a={a} b={b}  numeric {x:.5f}  closed-form {b/(a+b):.5f}")

print("\n=== 2 · ADVERSARIAL: is UNIMODALITY guaranteed? (I predict NO) ===")
# S increasing, S(0)=0, but wavy; A decreasing, A(1)=0.
A = lambda c: (1-c)
def S(c):
    # increasing overall (monotone check below) but with plateaus/ripples
    return c*(1 + 0.9*math.sin(18*c)**2)/1.9
xs=[i/20000 for i in range(20001)]
mono = all(S(xs[k+1]) >= S(xs[k]) - 1e-12 for k in range(len(xs)-1))
x,f,F = interior_max(A,S)
p = peaks(F)
print(f"  S monotone increasing? {mono}   S(0)={S(0):.3f}  A(1)={A(1):.3f}")
print(f"  interior maxima found: {p}")
print(f"  => interior max guaranteed: YES.  Unimodality: {'GUARANTEED' if p==1 else 'NOT GUARANTEED — counterexample found'}")

print("\n=== 3 · what restores unimodality? log-concavity of both factors ===")
def logconc(g, n=4001):
    xs=[1e-9+i*(1-2e-9)/(n-1) for i in range(n)]
    ys=[math.log(g(x)) if g(x)>0 else -1e9 for x in xs]
    h=xs[1]-xs[0]
    return all(ys[k+1]-2*ys[k]+ys[k-1] <= 1e-7*h*h*abs(ys[k]) + 1e-9 for k in range(1,n-1))
print(f"  A=(1-c)^2 log-concave: {logconc(lambda c:(1-c)**2)}")
print(f"  S=c^3     log-concave: {logconc(lambda c:c**3)}")
print(f"  wavy S    log-concave: {logconc(S)}")
x,f,F = interior_max(lambda c:(1-c)**2, lambda c:c**3)
print(f"  both log-concave -> peaks: {peaks(F)}  (log-concavity is closed under product)")

print("\n=== 4 · the boundary cases that KILL the lemma ===")
for name, A2, S2 in [
    ("A(1)>0  (compensation never exhausts the budget)", lambda c: 1-0.5*c, lambda c: c),
    ("S(0)>0  (freedom persists uncompensated)",         lambda c: 1-c,     lambda c: 0.5+0.5*c),
]:
    x,f,F = interior_max(A2,S2)
    edge = (x < 1e-4) or (x > 1-1e-4)
    print(f"  {name}\n     argmax={x:.4f} -> {'BOUNDARY optimum: lemma FAILS as predicted' if edge else 'interior'}")
"""Honest retry: can F=A*S have MULTIPLE interior peaks when the premises actually hold?
P1: A decreasing, A(1)=0.   P2: S increasing, S(0)=0.
"""
import math

n=200001
xs=[i/(n-1) for i in range(n)]

def check(A,S,label):
    a=[A(x) for x in xs]; s=[S(x) for x in xs]
    Adec = all(a[k+1] <= a[k] + 1e-12 for k in range(n-1))
    Sinc = all(s[k+1] >= s[k] - 1e-12 for k in range(n-1))
    F=[a[k]*s[k] for k in range(n)]
    pk=sum(1 for k in range(1,n-1) if F[k]>F[k-1]+1e-15 and F[k]>F[k+1]+1e-15)
    print(f"  {label}")
    print(f"    A decreasing:{Adec}  A(1)={a[-1]:.2e}   S increasing:{Sinc}  S(0)={s[0]:.2e}")
    print(f"    premises hold: {Adec and Sinc and abs(a[-1])<1e-9 and abs(s[0])<1e-9}   interior peaks: {pk}")
    return Adec and Sinc, pk

print("=== a VALID probe: S strictly increasing, S(0)=0, but with oscillating growth rate ===")
# S' = 1 + 0.995*cos(kc)  >= 0.005 > 0  =>  S strictly increasing
k=40.0
S = lambda c: c + 0.995*math.sin(k*c)/k
A = lambda c: (1-c)
ok,pk = check(A,S,"A=(1-c),  S=c+0.995*sin(40c)/40")

print("\n=== so the honest statement of the lemma ===")
if ok and pk>1:
    print("  INTERIOR MAXIMUM: guaranteed by the two premises.")
    print("  UNIMODALITY:      NOT guaranteed — a valid counterexample exists.")
    print("  The extra condition that buys unimodality is LOG-CONCAVITY of A and S")
    print("  (log-concavity is closed under multiplication, so log F is concave => one peak).")
else:
    print("  probe inconclusive — need a stronger construction")

print("\n=== confirm log-concavity fixes it, on the SAME family ===")
# make S log-concave: S=c^b is log-concave; keep A=(1-c)^a
for (a_,b_) in [(1,1),(3,2),(0.5,4)]:
    ok2,pk2 = check(lambda c,a_=a_:(1-c)**a_, lambda c,b_=b_:c**b_, f"A=(1-c)^{a_}, S=c^{b_}")
    print(f"    -> argmax should be b/(a+b) = {b_/(a_+b_):.4f}")

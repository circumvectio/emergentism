"""FALSWEEP-C numeric spot-checks, 2026-07-17. Hunter_CrossFile."""
import math

print("== P(i): Cayley square u(1/x) = -u(x) ==")
u = lambda x: (x - 1) / (x + 1)
mx = 0.0
for i in range(-12, 13):
    x = 10.0 ** (i / 4)
    mx = max(mx, abs(u(1 / x) + u(x)))
print("max |u(1/x)+u(x)| over sweep:", mx)

print("\n== P(iii): H = phi+nu = 2*AM = 2 cosh(s), s = log nu ==")
mx1 = mx2 = 0.0
for k in range(1, 180):
    th = math.pi * k / 180
    phi = 1 / math.tan(th / 2)
    nu = math.tan(th / 2)
    H = phi + nu
    AM = (phi + nu) / 2
    mx1 = max(mx1, abs(H - 2 * AM))
    mx2 = max(mx2, abs(H - 2 * math.cosh(math.log(nu))))
print("max |H-2*AM|:", mx1, " max |H-2cosh(s)|:", mx2)

print("\n== P(v): cos th = (1-nu^2)/(1+nu^2) = -u(nu^2) = -tanh(log nu) ==")
m = [0.0] * 5
for k in range(1, 360):
    th = math.pi * k / 360
    nu = math.tan(th / 2)
    s = math.log(nu)
    m[0] = max(m[0], abs(math.cos(th) - (1 - nu ** 2) / (1 + nu ** 2)))
    m[1] = max(m[1], abs(math.cos(th) + u(nu ** 2)))
    m[2] = max(m[2], abs(math.cos(th) + math.tanh(s)))
    m[3] = max(m[3], abs(math.sin(th) - 2 * nu / (1 + nu ** 2)))
    m[4] = max(m[4], abs(1 / math.cosh(s) ** 2 + math.tanh(s) ** 2 - 1))
print("cos vs (1-nu^2)/(1+nu^2):", m[0])
print("cos vs -u(nu^2):        ", m[1])
print("cos vs -tanh(s):        ", m[2])
print("sin vs 2nu/(1+nu^2):    ", m[3])
print("sech^2+tanh^2 = 1:      ", m[4])

print("\n== F-check: tat-tvam-asi Step-1 assignment phi=sin th, nu=cos th ==")
worst = 0.0
for k in range(1, 360):
    th = math.pi * k / 360
    worst = max(worst, abs(math.sin(th) * math.cos(th)))
print("max |sin th * cos th| over (0,pi):", worst, "  <-- claimed to equal 1 (phi*nu=1)")

#!/usr/bin/env python3
"""
BALANCE-HUMP test — the Burri anthropic sphere claim:
  Phi x V is multiplicative BUT the payoff is maximized at BALANCE (Phi = V),
  i.e. B = sin(theta) = 2/(Phi+Nu) peaks at 1 when Phi=Nu and falls off with imbalance.

This is a *different* claim from the unbounded Cobb-Douglas fit in run_prodfn.py.
Cobb-Douglas is MONOTONIC in the factor ratio (no interior optimum). The anthropic
claim needs an interior HUMP: holding scale fixed, output should peak at balance and
DECLINE as one factor dominates.

Decompose the two inputs into SCALE and BALANCE (normalization-robust):
  S = (logL + logK)/2         (log geometric-mean scale)
  d = logL - logK             (log ratio; d=0 is balance in normalized units)

Models (predict logY), 10-fold CV RMSE on Y:
  M0 scale-only:          logY = c + s*S                    (balance irrelevant)
  M1 cobb-douglas:        logY = c + s*S + b1*d             (ratio LINEAR: no hump)
  M2 balance-HUMP:        logY = c + s*S + b1*d + b2*d^2    (b2<0 => interior optimum)

Framework anthropic claim needs:  b2 < 0 AND significant (a real hump exists),
and (strong form) the optimum d* ~ 0 (symmetric, at Phi=Nu).
KEY invariant test: does a hump EXIST at all? (b2<0 significant, and M2 beats M1 out-of-sample)
"""
import csv, math, os, random
import numpy as np
random.seed(20260703); np.random.seed(20260703)
HERE = os.path.dirname(__file__)
rows = list(csv.DictReader(open(os.path.join(HERE, "data", "Produc.csv"))))
Y = np.array([float(r["gsp"]) for r in rows])
L = np.array([float(r["emp"]) for r in rows])
K = np.array([float(r["pc"]) + float(r["pcap"]) for r in rows])
n = len(Y)
L = L/np.exp(np.mean(np.log(L))); K = K/np.exp(np.mean(np.log(K)))
lY = np.log(Y); S = (np.log(L)+np.log(K))/2.0; d = np.log(L)-np.log(K)

def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X@b; resid = y-yhat
    dof = len(y)-X.shape[1]
    s2 = (resid@resid)/dof
    cov = s2*np.linalg.inv(X.T@X)
    se = np.sqrt(np.diag(cov))
    return b, se, resid

def kfold(nn,k=10):
    idx=list(range(nn)); random.shuffle(idx); return [idx[i::k] for i in range(k)]
folds = kfold(n,10)
def cv_rmse(cols):
    errs=[]
    for te in folds:
        tr=[i for i in range(n) if i not in set(te)]
        Xtr=np.column_stack([np.ones(len(tr))]+[c[tr] for c in cols])
        b,*_=np.linalg.lstsq(Xtr,lY[tr],rcond=None)
        resid=lY[tr]-Xtr@b; smear=np.mean(np.exp(resid))
        Xte=np.column_stack([np.ones(len(te))]+[c[te] for c in cols])
        yhat=np.exp(Xte@b)*smear
        errs.append(np.sqrt(np.mean((Y[te]-yhat)**2)))
    return float(np.mean(errs))

# full-sample fits (for coefficients + significance)
b0,se0,_ = ols(np.column_stack([np.ones(n),S]), lY)
b1,se1,_ = ols(np.column_stack([np.ones(n),S,d]), lY)
b2,se2,_ = ols(np.column_stack([np.ones(n),S,d,d**2]), lY)

r0=cv_rmse([S]); r1=cv_rmse([S,d]); r2=cv_rmse([S,d,d**2])

print("="*72)
print("BALANCE-HUMP TEST  (Burri anthropic: multiplicative, max at balance Phi=Nu)")
print("="*72)
print(f"data: Munnell US-states  n={n}   Y=gsp  L=emp  K=pc+pcap  (normalized)")
print(f"S=(logL+logK)/2 scale ; d=logL-logK ratio (d=0 = balance)\n")
print("--- 10-fold CV RMSE on Y (lower=better) ---")
print(f"  M0 scale-only     : {r0:10.1f}")
print(f"  M1 cobb-douglas   : {r1:10.1f}   (ratio linear, NO hump)")
print(f"  M2 balance-HUMP   : {r2:10.1f}   (adds d^2)")
print()
print("--- M2 coefficients (the hump test) ---")
names=["intercept","S (scale)","d (ratio)","d^2 (curvature)"]
for nm,coef,se in zip(names,b2,se2):
    t=coef/se
    print(f"  {nm:16s} = {coef:+8.4f}   se={se:.4f}   t={t:+6.2f}"
          + ("  <-- HUMP if <0 & |t|>2" if nm.startswith('d^2') else ""))
b2c=b2[3]; b1c=b2[2]
print()
print("--- interpretation ---")
hump = (b2c < 0) and (abs(b2c/se2[3])>2)
print(f"  interior balance optimum exists (d^2<0, |t|>2)? {'YES' if hump else 'NO'}")
if b2c!=0:
    dstar = -b1c/(2*b2c)
    print(f"  optimum log-ratio d* = {dstar:+.3f}   (d*=0 => symmetric Phi=Nu)")
    print(f"    => optimum L/K (normalized) = {math.exp(dstar):.2f} : 1")
better = r2 < r1
print(f"  balance-hump beats cobb-douglas out-of-sample? {'YES' if better else 'NO'}"
      f"  ({r2:.0f} vs {r1:.0f})")
print()
print("--- PRE-REGISTERED KILL ---")
print(f"  ANTHROPIC (a real balance hump exists): {'PASS' if hump and better else 'FAIL'}")
if hump:
    dstar=-b1c/(2*b2c)
    print(f"  SYMMETRIC (optimum at Phi=Nu, d*~0):    {'PASS' if abs(dstar)<0.25 else 'FAIL'}")
else:
    print(f"  SYMMETRIC (optimum at Phi=Nu):           N/A (no hump to locate)")

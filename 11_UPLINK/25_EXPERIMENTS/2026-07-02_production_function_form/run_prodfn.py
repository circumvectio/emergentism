#!/usr/bin/env python3
"""
Production-function form test — the AGENCY-register operationalization of P = Phi x V.

Framework claim (agency gloss, D5 Register): output/flourishing = Phi x V, where
Phi = foresight/skill, V = means/tool/execution. In production terms: output = labor x capital.
That is a SYMMETRIC, unit-elasticity, constant-returns PRODUCT (the B=sin(theta) / L4-apex
superstructure needs the symmetric balance-product specifically, not just "conjunction").

We fit competing functional forms on real output data and let cross-validation decide:
  (A) ADDITIVE (levels):        Y = c + a*L + b*K            <- the "sum" the framework opposes
  (B) COBB-DOUGLAS general:     Y = e^c * L^a * K^b          <- multiplicative, FREE elasticities
  (C) PRODUCT-UNIT (framework): Y = e^c * L^1 * K^1          <- the SPECIFIC symmetric phi x nu
  (D) LEONTIEF / min:           Y = c * min(L/mL, K/mK)      <- perfect complements
  (E) CES (nests all):          Y = A*[d L^-rho + (1-d) K^-rho]^(-s/rho); best rho tells the form
                                   rho->0 = Cobb-Douglas, rho->inf = Leontief, rho=-1 = linear

Data: Munnell US-states panel (Rdatasets/plm/Produc.csv). Y=gsp, L=emp, K=pc+pcap.
Kill-criteria (pre-registered here):
  K1 multiplicative-over-additive: Cobb-Douglas must beat ADDITIVE out-of-sample. (framework's weak leg)
  KC2 symmetric-balance-product:   (a,b) ~ (equal, sum~1) AND product-unit ~ general CD.
                                   If a != b (asymmetric) the phi=nu equator optimum is FALSE.
  K3 right substitution family:    best CES rho ~ 0 (Cobb-Douglas). rho far from 0 => wrong form.
"""
import csv, math, os, random
import numpy as np

random.seed(20260702); np.random.seed(20260702)
HERE = os.path.dirname(__file__)
rows = list(csv.DictReader(open(os.path.join(HERE, "data", "Produc.csv"))))

Y = np.array([float(r["gsp"]) for r in rows])
L = np.array([float(r["emp"]) for r in rows])
K = np.array([float(r["pc"]) + float(r["pcap"]) for r in rows])
n = len(Y)
# normalize inputs to geometric mean 1 (keeps powers well-scaled; does not change form)
L = L / np.exp(np.mean(np.log(L)))
K = K / np.exp(np.mean(np.log(K)))
mL, mK = L.mean(), K.mean()
lY, lL, lK = np.log(Y), np.log(L), np.log(K)

def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta

def kfold(nn, k=10):
    idx = list(range(nn)); random.shuffle(idx)
    return [idx[i::k] for i in range(k)]

folds = kfold(n, 10)

def cv_rmse(predict_fn):
    """predict_fn(tr_idx, te_idx) -> yhat (levels) on te_idx. RMSE on Y (levels)."""
    errs = []
    for te in folds:
        tr = [i for i in range(n) if i not in set(te)]
        yhat = predict_fn(tr, te)
        e = Y[te] - yhat
        errs.append(np.sqrt(np.mean(e**2)))
    return float(np.mean(errs))

# (A) additive in levels
def pred_add(tr, te):
    X = np.column_stack([np.ones(len(tr)), L[tr], K[tr]])
    b = ols(X, Y[tr])
    return b[0] + b[1]*L[te] + b[2]*K[te]

# (B) Cobb-Douglas general (log-log OLS), predict Y with smearing (Duan) correction
def pred_cd(tr, te):
    X = np.column_stack([np.ones(len(tr)), lL[tr], lK[tr]])
    b = ols(X, lY[tr])
    resid = lY[tr] - X @ b
    smear = np.mean(np.exp(resid))
    return np.exp(b[0] + b[1]*lL[te] + b[2]*lK[te]) * smear

# (C) product-unit: log Y - logL - logK = c  (only intercept free)
def pred_prod(tr, te):
    off_tr = lY[tr] - lL[tr] - lK[tr]
    c = np.mean(off_tr)
    resid = off_tr - c
    smear = np.mean(np.exp(resid))
    return np.exp(c + lL[te] + lK[te]) * smear

# (D) Leontief / min
def pred_min(tr, te):
    m_tr = np.minimum(L[tr]/mL, K[tr]/mK)
    X = np.column_stack([np.ones(len(tr)), m_tr])
    b = ols(X, Y[tr])
    m_te = np.minimum(L[te]/mL, K[te]/mK)
    return b[0] + b[1]*m_te

# (E) CES via (rho, delta) grid; fit log Y = c + s*log(index); s = returns to scale
RHOS = [-0.9,-0.7,-0.5,-0.3,-0.15,-0.05,0.0,0.05,0.15,0.3,0.5,1.0,2.0,4.0,8.0]
DELTAS = [round(d,2) for d in np.arange(0.1,0.91,0.05)]
def ces_index(rho, delta, Lx, Kx):
    if abs(rho) < 1e-6:  # Cobb-Douglas limit
        return delta*np.log(Lx) + (1-delta)*np.log(Kx)      # already log-index
    inner = delta*Lx**(-rho) + (1-delta)*Kx**(-rho)
    return (-1.0/rho)*np.log(inner)                          # log CES index
def pred_ces_factory(rho, delta):
    def f(tr, te):
        ix_tr = ces_index(rho, delta, L[tr], K[tr])
        X = np.column_stack([np.ones(len(tr)), ix_tr])
        b = ols(X, lY[tr])
        resid = lY[tr] - X @ b
        smear = np.mean(np.exp(resid))
        ix_te = ces_index(rho, delta, L[te], K[te])
        return np.exp(b[0] + b[1]*ix_te) * smear
    return f

# choose best CES (rho,delta) by CV
best = None
for rho in RHOS:
    for d in DELTAS:
        r = cv_rmse(pred_ces_factory(rho, d))
        if best is None or r < best[0]:
            best = (r, rho, d)
ces_rmse, ces_rho, ces_delta = best

results = {
    "A additive(levels)":  cv_rmse(pred_add),
    "B cobb-douglas(free)": cv_rmse(pred_cd),
    "C product-unit(phi x nu)": cv_rmse(pred_prod),
    "D leontief(min)":     cv_rmse(pred_min),
    f"E CES(best rho={ces_rho}, d={ces_delta})": ces_rmse,
}

# full-sample Cobb-Douglas elasticities (the symmetry / returns test)
Xfull = np.column_stack([np.ones(n), lL, lK]); b = ols(Xfull, lY)
a_hat, b_hat = b[1], b[2]

print("="*72)
print("PRODUCTION-FUNCTION FORM TEST  (agency register: output = labor x capital)")
print("="*72)
print(f"data: Munnell US-states panel  n={n}  (48 states x 17 yrs, 1970-1986)")
print(f"Y=gsp  L=emp  K=pc+pcap  | 10-fold CV RMSE on output Y (lower = better)\n")
for k,v in sorted(results.items(), key=lambda kv: kv[1]):
    print(f"  {v:12.1f}   {k}")
print()
print("--- Cobb-Douglas elasticities (full sample) ---")
print(f"  labor a = {a_hat:.3f}   capital b = {b_hat:.3f}   a+b = {a_hat+b_hat:.3f}")
print(f"  symmetric (a==b)?  |a-b| = {abs(a_hat-b_hat):.3f}")
print(f"  constant returns (a+b==1)?  a+b-1 = {a_hat+b_hat-1:+.3f}")
print()
print("--- CES substitution family ---")
print(f"  best CES rho = {ces_rho}   (rho~0 => Cobb-Douglas; rho->inf => Leontief/min; rho=-1 => additive)")
print()
print("--- PRE-REGISTERED KILL-CRITERIA ---")
k1 = results["B cobb-douglas(free)"] < results["A additive(levels)"]
print(f"  K1 multiplicative beats additive:        {'PASS' if k1 else 'FAIL'}  "
      f"(CD {results['B cobb-douglas(free)']:.0f} vs ADD {results['A additive(levels)']:.0f})")
sym = abs(a_hat-b_hat) < 0.15 and abs(a_hat+b_hat-1) < 0.15
print(f"  KC2 SYMMETRIC balance-product (a~b, a+b~1): {'PASS' if sym else 'FAIL'}  "
      f"(a={a_hat:.2f}, b={b_hat:.2f})")
prod_close = results["C product-unit(phi x nu)"] <= 1.05*results["B cobb-douglas(free)"]
print(f"  K2b product-unit ~ general CD:           {'PASS' if prod_close else 'FAIL'}  "
      f"(prod {results['C product-unit(phi x nu)']:.0f} vs CD {results['B cobb-douglas(free)']:.0f})")
k3 = abs(ces_rho) <= 0.15
print(f"  K3 CES rho ~ 0 (Cobb-Douglas family):    {'PASS' if k3 else 'FAIL'}  (rho={ces_rho})")

#!/usr/bin/env python3
"""
Pooled GFS multiplicative (phi x nu) vs additive (phi + nu) verdict.

Runs the pooled meta-analysis Wave-1 deferred (Next Steps #1 of 00_GFS_WAVE1_RESULTS.md)
on the per-country fits already on disk. This is a re-pooling of existing fits, NOT a
re-fit on raw microdata (raw n=207,920 microdata not on disk; that reconciliation stays open).

Model coding in the source CSV:
  m1 = additive          (alpha*phi + beta*nu)
  m2 = additive + interaction (adds phi x nu term)  <- the multiplicative claim
  m3 = + curvature (higher order)

The framework's claim (H1): the phi x nu interaction adds explanatory power AND its
coefficient is POSITIVE (framework-consistent: high-phi & high-nu together => MORE flourishing).

Audit kill-criterion (packet #1): phi x nu must beat phi + nu, framework-consistent,
in >= 15/23 countries. Pre-registered kill (AK1): additive explains >= variance pooled.
"""
import csv, math, os

CSV = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                   "09_TOOLS", "04_DATA_PIPELINES", "gfs_results_20260409.csv")

rows = list(csv.DictReader(open(CSV)))
def f(r, k):
    try: return float(r[k])
    except Exception: return float("nan")

N = len(rows)
total_n = sum(int(float(r["n"])) for r in rows)

# AIC-based model comparison (AIC penalizes the extra parameter, so this is a fair test)
m2_beats_m1 = 0          # interaction improves AIC at all
m2_beats_m1_substantial = 0  # dAIC > 2
fw_consistent = 0        # interaction improves AIC AND beta_interaction > 0
h1_supported = 0         # pipeline's own flag
sig = 0                  # p_interaction < 0.05
sig_pos = 0
sig_neg = 0

sumAIC_m1 = sumAIC_m2 = sumAIC_m3 = 0.0
# AIC weights per country (m1 vs m2 only), and n-weighted mean interaction beta
nw_beta_num = nw_beta_den = 0.0

per = []
for r in rows:
    a1, a2, a3 = f(r,"aic_m1"), f(r,"aic_m2"), f(r,"aic_m3")
    b, p = f(r,"beta_interaction"), f(r,"p_interaction")
    n = float(r["n"])
    sumAIC_m1 += a1; sumAIC_m2 += a2; sumAIC_m3 += a3
    d = a1 - a2   # positive => m2 (multiplicative) better
    if d > 0: m2_beats_m1 += 1
    if d > 2: m2_beats_m1_substantial += 1
    if d > 0 and b > 0: fw_consistent += 1
    if str(r["h1_supported"]).strip().lower() == "true": h1_supported += 1
    if p < 0.05:
        sig += 1
        if b > 0: sig_pos += 1
        else: sig_neg += 1
    nw_beta_num += n * b; nw_beta_den += n
    # Akaike weight of m2 vs m1
    amin = min(a1, a2)
    w1 = math.exp(-(a1-amin)/2); w2 = math.exp(-(a2-amin)/2)
    per.append((r["country"], int(n), round(d,1), round(b,3), round(p,4),
                round(w2/(w1+w2),3)))

nw_beta = nw_beta_num / nw_beta_den

print("="*70)
print("POOLED GFS  —  multiplicative (phi x nu)  vs  additive (phi + nu)")
print("="*70)
print(f"countries: {N}   total respondents: {total_n:,}")
print()
print("--- AIC model comparison (lower AIC = better; penalizes extra term) ---")
print(f"  interaction improves AIC (any):            {m2_beats_m1}/{N}")
print(f"  interaction improves AIC substantially(>2):{m2_beats_m1_substantial}/{N}")
print(f"  FRAMEWORK-CONSISTENT (improves AIC & beta>0): {fw_consistent}/{N}   <-- the real claim")
print(f"  pipeline h1_supported flag:                {h1_supported}/{N}")
print()
print("--- direction of SIGNIFICANT interactions (p<0.05) ---")
print(f"  significant total: {sig}/{N}")
print(f"    positive (framework-consistent): {sig_pos}")
print(f"    negative (framework-INCONSISTENT): {sig_neg}")
print()
print("--- pooled effect ---")
print(f"  n-weighted mean interaction beta: {nw_beta:+.4f}")
print(f"  (prior random-effects meta on disk: beta=-0.0533, p=0.60, I^2=75.8%)")
print()
print("--- pooled AIC totals (sum over independent country samples) ---")
print(f"  Sum AIC additive (m1):        {sumAIC_m1:,.0f}")
print(f"  Sum AIC multiplicative (m2):  {sumAIC_m2:,.0f}   (dvs m1: {sumAIC_m1-sumAIC_m2:+,.0f})")
print(f"  Sum AIC + curvature (m3):     {sumAIC_m3:,.0f}")
print()
print("--- KILL-CRITERION EVALUATION ---")
kill = 15
print(f"  audit kill: framework-consistent multiplicative win in >= {kill}/{N}")
print(f"  observed framework-consistent: {fw_consistent}/{N}  ->  "
      + ("PASS" if fw_consistent >= kill else "FAIL"))
print()
print("--- per-country (country, n, dAIC[m1-m2], beta_int, p, Akaike w(m2)) ---")
for c in per:
    print("  " + "  ".join(str(x).rjust(9) for x in c))

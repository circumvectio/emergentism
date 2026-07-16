#!/usr/bin/env python3
"""
GFS AND-class discriminator — 2026-07-12
==========================================

The April 2026 GFS Wave-2 test (gfs_22_country_analysis_wave2.py, results
gfs_results_20260409.csv, receipt 03_METHODOLOGY/00_GFS_WAVE1_RESULTS.md)
compared the multiplicative interaction model only against the ADDITIVE
baseline. The 2026-07-12 formal-logic audit convicted that comparison as a
false binary: the Zero-Factor Catastrophe selects an AND-CLASS of laws
(min/Liebig, CES, geometric mean, product), and a x-vs-+ test cannot
distinguish the product from its AND-class siblings.

This script runs the discriminating comparison the kill criterion actually
needs. Same pre-registered proxy construction as the April pipeline
(validation gate: replicate r2_m1/r2_m2 per country against
gfs_results_20260409.csv before extending).

Models (per country, and pooled with country fixed effects), all predicting
z-scored flourishing:

  On z-scored inputs (exact April replication):
    M1_add   F ~ phi + nu
    M2_int   F ~ phi + nu + phi*nu

  On unit-scaled inputs u,v in [0,1] (min-max within country; AND-class
  forms need a positive scale — documented design choice, with a
  percentile-rank robustness variant):
    A_add    F ~ u + v                       (2 slopes)
    A_int    F ~ u + v + u*v                 (3 slopes)
    A_prod   F ~ u*v                         (1 slope)
    A_min    F ~ min(u,v)                    (1 slope; Liebig)
    A_geo    F ~ sqrt(u*v)                   (1 slope; CES rho->0)
    A_ces    F ~ CES_rho(u,v), rho on grid   (1 slope + 1 shape, CV-chosen)

  CES_rho(u,v) = ((u^rho + v^rho)/2)^(1/rho); rho=1 is the mean (additive
  ordering), rho->0 geometric mean, rho->-inf min. eps-floor 1e-6 on u,v.

Primary metric: 5-fold cross-validated out-of-sample R^2 (fixed seed 108).
Secondary: AIC. Readout: per-country OOS ranking + fitted rho_hat.

Honest expectations, stated before running: survey z-composites usually
favor additive models; the April interaction result was mixed (signal in
7/23, split sign). If additive wins OOS everywhere, that is the result and
it will be reported as such. The manifold identity phi*nu=1 on S^2 is not
at stake here (chart identity, [A]); at stake is only the finite-node
functional-form wager, and only as far as these survey proxies reach (see
the instrument-validity caveat in 00_GFS_WAVE1_RESULTS.md).

Tier: [B] receipt for whatever this produces; interpretation stays [I].
"""

import sys
import numpy as np
import pandas as pd
from scipy import stats as sp_stats

import os
DATA = os.environ.get(
    "GFS_DTA",
    "/Users/Yves/Library/CloudStorage/GoogleDrive-burri.yves@gmail.com/"
    "My Drive/08 \U0001F4E6 Archives & Large ZIP Files/☀️ Emergentism_org/"
    "01_FRAMEWORK/00_INTAKE/gfs_all_countries_wave2.dta")
APRIL = "gfs_results_20260409.csv"

PHI_ITEMS = ["LIFE_PURPOSE_Y2", "WORTHWHILE_Y2", "PROMOTE_GOOD_Y2",
             "GRATEFUL_Y2", "PEOPLE_HELP_Y2", "SAT_RELATNSHP_Y2"]
NU_ITEMS = ["MENTAL_HEALTH_Y2", "PHYSICAL_HLTH_Y2",
            "INCOME_FEELINGS_Y2", "EXPENSES_Y2"]
DV_ITEMS = ["LIFE_SAT_Y2", "HAPPY_Y2"]

RHO_GRID = [-25.0, -10.0, -5.0, -3.0, -2.0, -1.0, -0.5, 1e-9, 0.5, 1.0, 2.0, 3.0]
KFOLD = 5
SEED = 108
EPS = 1e-6


def load():
    cols = ["COUNTRY"] + PHI_ITEMS + NU_ITEMS + DV_ITEMS
    df = pd.read_stata(DATA, columns=cols, convert_categoricals=False)
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def build_country(df, country):
    """Exact April construction: reverse-code INCOME_FEELINGS, domain means,
    complete cases, z-standardize within country."""
    cdf = df[df["COUNTRY"] == country].copy()
    v = cdf["INCOME_FEELINGS_Y2"]
    ok = v.between(1, 4)
    cdf.loc[ok, "INCOME_FEELINGS_Y2"] = 5 - v[ok]
    cdf["phi_raw"] = cdf[PHI_ITEMS].mean(axis=1)
    cdf["nu_raw"] = cdf[NU_ITEMS].mean(axis=1)
    cdf["flourishing"] = cdf[DV_ITEMS].mean(axis=1)
    cdf = cdf.dropna(subset=["phi_raw", "nu_raw", "flourishing"])
    if len(cdf) < 200:
        return None
    cdf["phi"] = sp_stats.zscore(cdf["phi_raw"])
    cdf["nu"] = sp_stats.zscore(cdf["nu_raw"])
    cdf["F"] = sp_stats.zscore(cdf["flourishing"])
    # unit scale for AND-class forms (min-max within country, eps floor)
    for src, dst in (("phi_raw", "u"), ("nu_raw", "v")):
        x = cdf[src]
        rng = x.max() - x.min()
        cdf[dst] = ((x - x.min()) / rng).clip(EPS, 1.0) if rng > 0 else EPS
    # percentile-rank robustness variant
    cdf["u_pr"] = cdf["phi_raw"].rank(pct=True).clip(EPS, 1.0)
    cdf["v_pr"] = cdf["nu_raw"].rank(pct=True).clip(EPS, 1.0)
    return cdf


def ces(u, v, rho):
    if abs(rho) < 1e-8:
        return np.sqrt(u * v)
    return ((u ** rho + v ** rho) / 2.0) ** (1.0 / rho)


def ols_fit_predict(Xtr, ytr, Xte):
    Xtr1 = np.column_stack([np.ones(len(Xtr)), Xtr])
    Xte1 = np.column_stack([np.ones(len(Xte)), Xte])
    beta, *_ = np.linalg.lstsq(Xtr1, ytr, rcond=None)
    return Xte1 @ beta


def ols_insample(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    resid = y - X1 @ beta
    rss = float(resid @ resid)
    n, k = X1.shape
    r2 = 1 - rss / float(((y - y.mean()) ** 2).sum())
    aic = n * np.log(rss / n) + 2 * (k + 1)
    return r2, aic


def design(name, cdf, uu="u", vv="v", rho=None):
    u, v = cdf[uu].values, cdf[vv].values
    if name == "add":
        return np.column_stack([u, v])
    if name == "int":
        return np.column_stack([u, v, u * v])
    if name == "prod":
        return (u * v).reshape(-1, 1)
    if name == "min":
        return np.minimum(u, v).reshape(-1, 1)
    if name == "geo":
        return np.sqrt(u * v).reshape(-1, 1)
    if name == "ces":
        return ces(u, v, rho).reshape(-1, 1)
    raise ValueError(name)


def cv_r2(cdf, name, uu="u", vv="v", rho=None):
    """5-fold OOS R^2. For CES, rho is chosen inside each training fold
    (nested on the same grid) to avoid leakage."""
    y = cdf["F"].values
    n = len(y)
    rng = np.random.default_rng(SEED)
    idx = rng.permutation(n)
    folds = np.array_split(idx, KFOLD)
    press, chosen_rhos = 0.0, []
    for i in range(KFOLD):
        te = folds[i]
        tr = np.concatenate([folds[j] for j in range(KFOLD) if j != i])
        ctr, cte = cdf.iloc[tr], cdf.iloc[te]
        r = rho
        if name == "ces" and r is None:
            best, r = -np.inf, 1.0
            for cand in RHO_GRID:
                Xtr = design("ces", ctr, uu, vv, cand)
                r2_tr, _ = ols_insample(Xtr, ctr["F"].values)
                if r2_tr > best:
                    best, r = r2_tr, cand
            chosen_rhos.append(r)
        pred = ols_fit_predict(design(name, ctr, uu, vv, r), ctr["F"].values,
                               design(name, cte, uu, vv, r))
        press += float(((cte["F"].values - pred) ** 2).sum())
    oos = 1 - press / float(((y - y.mean()) ** 2).sum())
    return oos, (np.median(chosen_rhos) if chosen_rhos else rho)


def main():
    print("Loading GFS Wave 2 (.dta, columns subset)...")
    df = load()
    countries = sorted(df["COUNTRY"].dropna().unique())
    print(f"n={len(df)}, countries={len(countries)}")

    april = pd.read_csv(APRIL).set_index("country") if pd.io.common.file_exists(APRIL) else None

    rows = []
    for c in countries:
        cdf = build_country(df, c)
        if cdf is not None:
            rows.append((c, cdf))
    # April regressed raw 'flourishing' (unstandardized DV). R^2 is
    # scale-invariant, so the z-scored F used for CV gives identical R^2;
    # the replication gate below checks against the raw-DV April numbers.

    out = []
    for c, cdf in rows:
        y = cdf["flourishing"].values  # April DV (R^2 identical under z)
        Xm1 = np.column_stack([cdf["phi"], cdf["nu"]])
        Xm2 = np.column_stack([cdf["phi"], cdf["nu"], cdf["phi"] * cdf["nu"]])
        r2_m1, _ = ols_insample(Xm1, y)
        r2_m2, _ = ols_insample(Xm2, y)
        rep = {}
        if april is not None and c in april.index:
            rep = {"april_r2_m1": april.loc[c, "r2_m1"],
                   "april_r2_m2": april.loc[c, "r2_m2"],
                   "replicates": bool(abs(april.loc[c, "r2_m1"] - r2_m1) < 5e-3
                                      and abs(april.loc[c, "r2_m2"] - r2_m2) < 5e-3)}

        rec = {"country": int(c), "n": len(cdf), "r2_m1": r2_m1, "r2_m2": r2_m2, **rep}
        for name in ["add", "int", "prod", "min", "geo", "ces"]:
            oos, rho_hat = cv_r2(cdf, name)
            rec[f"oos_{name}"] = oos
            if name == "ces":
                rec["rho_hat"] = rho_hat
            X = design(name, cdf, rho=rho_hat if name == "ces" else None)
            r2, aic = ols_insample(X, cdf["F"].values)
            rec[f"aic_{name}"] = aic
        # robustness: percentile-rank inputs, ALL forms. NOTE (post-run
        # diagnosis 2026-07-12): the min-max scale is defined by a handful of
        # extreme respondents (sd(u) ~ 0.03-0.13), which compresses the bulk
        # of the sample and makes min-max winners leverage-artifacts. The
        # rank scaling is the robust primary reading; min-max is kept for
        # the record.
        for name in ["add", "int", "prod", "min", "geo", "ces"]:
            oos, rho_pr = cv_r2(cdf, name, uu="u_pr", vv="v_pr")
            rec[f"oos_{name}_pr"] = oos
            if name == "ces":
                rec["rho_hat_pr"] = rho_pr
        ranked_pr = sorted([k for k in rec if k.endswith("_pr") and k.startswith("oos_")],
                           key=lambda k: -rec[k])
        rec["oos_winner_pr"] = ranked_pr[0].replace("oos_", "").replace("_pr", "")
        rec["oos_margin_vs_add_pr"] = rec[ranked_pr[0]] - rec["oos_add_pr"]
        ranked = sorted([k for k in rec if k.startswith("oos_") and not k.endswith("_pr")],
                        key=lambda k: -rec[k])
        rec["oos_winner"] = ranked[0].replace("oos_", "")
        rec["oos_margin_vs_add"] = rec[ranked[0]] - rec["oos_add"]
        out.append(rec)
        print(f"country {int(c):2d} n={len(cdf):6d} winner={rec['oos_winner']:4s} "
              f"rho_hat={rec.get('rho_hat', float('nan')):6.2f} "
              f"repl={rec.get('replicates', 'n/a')}")

    res = pd.DataFrame(out)
    res.to_csv("gfs_and_class_results_20260712.csv", index=False)

    # pooled, country fixed effects (within-country z DV). Rank inputs are
    # the primary pooled scaling: min-max slopes vary ~8x across countries
    # (range-dependent), so a single pooled min-max slope misfits everything
    # (in-sample R^2 collapses 0.08 -> 0.003). Both are written for the record.
    print("\n=== POOLED (country fixed effects; rank primary) ===")
    pool = pd.concat([cdf for _, cdf in rows], ignore_index=True)
    precs = []
    for label, (uu, vv) in (("POOLED_rank", ("u_pr", "v_pr")),
                            ("POOLED_minmax_artifact", ("u", "v"))):
        prec = {"country": label, "n": len(pool)}
        for name in ["add", "int", "prod", "min", "geo", "ces"]:
            oos, rho_hat = cv_r2(pool, name, uu=uu, vv=vv)
            prec[f"oos_{name}"] = oos
            if name == "ces":
                prec["rho_hat"] = rho_hat
        print(prec)
        precs.append(prec)
    pd.DataFrame(precs).to_csv("gfs_and_class_pooled_20260712.csv", index=False)

    n_rep = int(res.get("replicates", pd.Series(dtype=bool)).sum())
    print(f"\nReplication gate: {n_rep}/{len(res)} countries match April r2 within 5e-3")
    print("Winners (minmax, artifact-prone):", res["oos_winner"].value_counts().to_dict())
    print("Winners (rank, primary):", res["oos_winner_pr"].value_counts().to_dict())
    print("Median rho_hat (minmax):", float(res["rho_hat"].median()),
          "| median rho_hat (rank):", float(res["rho_hat_pr"].median()))
    print("min beats add under rank:", int((res["oos_min_pr"] > res["oos_add_pr"]).sum()), "countries")


if __name__ == "__main__":
    sys.exit(main())

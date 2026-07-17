#!/usr/bin/env python3
"""
GFS 22-Country Analysis: Multiplicative vs. Additive Models of Flourishing
===========================================================================

PREREGISTERED CONFIRMATORY TEST

This script implements the analysis plan from:
  13_PEER_REVIEW/GFS_PREREGISTRATION_DRAFT.md

Tests H1: phi x nu > phi + nu for predicting flourishing
Tests H2: Balance (-|phi - nu|) adds incremental prediction
Tests H3: Effects replicate across 15+ of 22 countries

Data: Global Flourishing Study Wave 1 (VanderWeele et al.)
Expected release: April 8, 2026
Access: https://www.cos.io/gfs-access-data

Evidence tier: [C] Conjecture until results confirm or falsify.

Author: Yves R. Burri / Emergentism.org
Date: 2026-04-05
License: CC BY-SA 4.0
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from datetime import datetime

try:
    from scipy import stats as sp_stats
    import statsmodels.api as sm
    from statsmodels.stats.anova import anova_lm
except ImportError:
    print("Missing dependencies. Install: pip install pandas scipy statsmodels")
    exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

SIG_THRESHOLD = 0.005        # Benjamin et al. (2018)
H1_COUNTRY_THRESHOLD = 15    # of 22 countries
H2_COUNTRY_THRESHOLD = 11    # simple majority
EFFECT_SIZE_FLOOR = 0.02     # minimum meaningful ΔR²

# GFS country list (22 countries)
GFS_COUNTRIES = [
    "Argentina", "Australia", "Brazil", "Egypt", "Germany",
    "Hong_Kong", "India", "Indonesia", "Israel", "Japan",
    "Kenya", "Mexico", "Nigeria", "Philippines", "Poland",
    "South_Africa", "Spain", "Sweden", "Tanzania", "Turkey",
    "United_Kingdom", "United_States"
]

# Cultural clusters for H3 cross-cultural test
CULTURAL_CLUSTERS = {
    "East_Asian": ["Hong_Kong", "Japan"],
    "South_Asian": ["India", "Indonesia", "Philippines"],
    "Sub_Saharan_African": ["Kenya", "Nigeria", "South_Africa", "Tanzania"],
    "Latin_American": ["Argentina", "Brazil", "Mexico"],
    "Western_European": ["Australia", "Germany", "Spain", "Sweden", "United_Kingdom", "United_States"],
    "Eastern_European": ["Poland", "Turkey"],
    "Middle_Eastern": ["Egypt", "Israel"],
}

# GFS Domain mapping to phi/nu
# phi (coherence): Meaning/Purpose (D2) + Character/Virtue (D3)
# nu (viability): Close Relationships (D4) + Financial Stability (D5) + Health (D6)
# DV: Happiness/Life Satisfaction (D1)

# =============================================================================
# DATA LOADING
# =============================================================================

def load_gfs_data(data_path: str) -> pd.DataFrame:
    """
    Load GFS Wave 1 data. Adjust column names after seeing actual data format.

    Expected columns (adjust after data release):
    - country: country identifier
    - D1_happiness, D1_life_sat: Happiness and Life Satisfaction items
    - D2_worthwhile, D2_purpose: Meaning and Purpose items
    - D3_promote_good, D3_delay_gratification: Character and Virtue items
    - D4_friendships, D4_relationships: Close Social Relationships items
    - D5_expenses (reverse), D5_food (reverse): Financial Stability items
    - D6_overall_health, D6_mental_health: Physical and Mental Health items
    - age, gender, education, religion: covariates
    - survey_weight: if provided
    """
    ext = Path(data_path).suffix.lower()
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        df = pd.read_csv(data_path, sep=sep)
    elif ext in (".sav",):
        df = pd.read_spss(data_path)
    elif ext in (".dta",):
        df = pd.read_stata(data_path)
    elif ext in (".rds", ".rda"):
        print("R data format detected. Convert to CSV first:")
        print("  R: write.csv(data, 'gfs_wave1.csv', row.names=FALSE)")
        exit(1)
    else:
        df = pd.read_csv(data_path)

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns[:20])}...")
    return df


def construct_composites(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Construct phi, nu composites from GFS domain scores.

    CORRECTED 2026-04-07: Variable names now match GFS Codebook v2 exactly
    (same as gfs_multiplicative_test_v3.py). Previous version used descriptive
    snake_case names that don't match the actual GFS data file.

    GFS Codebook v2 variable names (https://osf.io/cg76b):
    Phi (coherence/integration):
      - LIFE_PURPOSE, WORTHWHILE, PROMOTE_GOOD, GRATEFUL, PEOPLE_HELP, SAT_RELATNSHP
    Nu (viability/material basis):
      - MENTAL_HEALTH, PHYSICAL_HLTH, INCOME_FEELINGS (reverse-coded), EXPENSES
    DV: LIFE_SAT, HAPPY
    Covariates: country, age, gender, education (if available)
    """
    # ---- GFS Codebook v2 Variable Names (EXACT) ----
    PHI_ITEMS = [
        "LIFE_PURPOSE", "WORTHWHILE", "PROMOTE_GOOD",
        "GRATEFUL", "PEOPLE_HELP", "SAT_RELATNSHP",
    ]
    NU_ITEMS = [
        "MENTAL_HEALTH", "PHYSICAL_HLTH", "INCOME_FEELINGS", "EXPENSES",
    ]
    DV_ITEMS = ["LIFE_SAT", "HAPPY"]
    COVARIATE_COLS = ["age", "gender", "education"]
    # ---- END MAPPING ----

    # Reverse-code INCOME_FEELINGS (1=Comfortable, 4=Very difficult → reverse so higher=better)
    cdf = df[df["country"] == country].copy()
    if "INCOME_FEELINGS" in cdf.columns:
        valid = cdf["INCOME_FEELINGS"].between(1, 4)
        cdf.loc[valid, "INCOME_FEELINGS"] = 5 - cdf.loc[valid, "INCOME_FEELINGS"]

    # EXPENSES: Already correctly coded (0=Worry all the time, 10=Never worry)

    # Filter to available items
    phi_available = [c for c in PHI_ITEMS if c in cdf.columns]
    nu_available = [c for c in NU_ITEMS if c in cdf.columns]
    dv_available = [c for c in DV_ITEMS if c in cdf.columns]

    if not phi_available or not nu_available or not dv_available:
        raise ValueError(
            f"Missing required columns for country {country}. "
            f"Phi: {len(phi_available)}/{len(PHI_ITEMS)}, "
            f"Nu: {len(nu_available)}/{len(NU_ITEMS)}, "
            f"DV: {len(dv_available)}/{len(DV_ITEMS)}. "
            f"Available cols: {list(cdf.columns[:30])}"
        )

    # Domain means
    cdf["phi_raw"] = cdf[phi_available].mean(axis=1)
    cdf["nu_raw"] = cdf[nu_available].mean(axis=1)
    cdf["flourishing"] = cdf[dv_available].mean(axis=1)

    # Complete cases
    required = ["phi_raw", "nu_raw", "flourishing"]
    cdf = cdf.dropna(subset=required)

    # Standardize within country
    cdf["phi"] = sp_stats.zscore(cdf["phi_raw"])
    cdf["nu"] = sp_stats.zscore(cdf["nu_raw"])

    # Derived variables
    cdf["phi_x_nu"] = cdf["phi"] * cdf["nu"]
    cdf["balance"] = -np.abs(cdf["phi"] - cdf["nu"])
    cdf["phi_sq"] = cdf["phi"] ** 2
    cdf["nu_sq"] = cdf["nu"] ** 2

    # Covariates
    for col in COVARIATE_COLS:
        if col in cdf.columns:
            if col == "age":
                cdf["age_centered"] = cdf[col] - cdf[col].mean()

    return cdf


# =============================================================================
# MODEL FITTING
# =============================================================================

def fit_country_models(cdf: pd.DataFrame, country: str, use_weights: bool = False) -> dict:
    """
    Fit the three preregistered models for one country.
    Returns dict with all results needed for meta-analysis.
    """
    y = cdf["flourishing"]
    n = len(y)

    # Build predictor matrices
    predictors_m1 = ["phi", "nu"]
    predictors_m2 = ["phi", "nu", "phi_x_nu"]
    predictors_m3 = ["phi", "nu", "phi_x_nu", "balance"]

    # Add available covariates
    covariates = []
    if "age_centered" in cdf.columns:
        covariates.append("age_centered")
    if "gender" in cdf.columns:
        covariates.append("gender")
    if "education" in cdf.columns:
        covariates.append("education")

    X1 = sm.add_constant(cdf[predictors_m1 + covariates])
    X2 = sm.add_constant(cdf[predictors_m2 + covariates])
    X3 = sm.add_constant(cdf[predictors_m3 + covariates])

    # Fit models (HC1 robust SE for primary, OLS for F-tests)
    m1 = sm.OLS(y, X1).fit(cov_type="HC1")
    m2 = sm.OLS(y, X2).fit(cov_type="HC1")
    m3 = sm.OLS(y, X3).fit(cov_type="HC1")

    m1_ols = sm.OLS(y, X1).fit()
    m2_ols = sm.OLS(y, X2).fit()
    m3_ols = sm.OLS(y, X3).fit()

    # F-tests
    f_12 = anova_lm(m1_ols, m2_ols)
    f_23 = anova_lm(m2_ols, m3_ols)

    # Curvilinearity robustness
    X1q = sm.add_constant(cdf[predictors_m1 + ["phi_sq", "nu_sq"] + covariates])
    X2q = sm.add_constant(cdf[predictors_m2 + ["phi_sq", "nu_sq"] + covariates])
    m1q = sm.OLS(y, X1q).fit()
    m2q = sm.OLS(y, X2q).fit()
    f_q = anova_lm(m1q, m2q)

    return {
        "country": country,
        "n": n,
        # Model R²
        "r2_m1": m1.rsquared,
        "r2_m2": m2.rsquared,
        "r2_m3": m3.rsquared,
        # ΔR²
        "delta_r2_12": m2.rsquared - m1.rsquared,
        "delta_r2_23": m3.rsquared - m2.rsquared,
        # Interaction coefficient (for meta-analysis)
        "beta_interaction": m2.params.get("phi_x_nu", np.nan),
        "se_interaction": m2.bse.get("phi_x_nu", np.nan),
        "p_interaction": m2.pvalues.get("phi_x_nu", np.nan),
        # Balance coefficient
        "beta_balance": m3.params.get("balance", np.nan),
        "se_balance": m3.bse.get("balance", np.nan),
        "p_balance": m3.pvalues.get("balance", np.nan),
        # F-tests
        "f_12": f_12.iloc[1]["F"],
        "p_f_12": f_12.iloc[1]["Pr(>F)"],
        "f_23": f_23.iloc[1]["F"],
        "p_f_23": f_23.iloc[1]["Pr(>F)"],
        # Curvilinearity robustness
        "p_curv": f_q.iloc[1]["Pr(>F)"],
        "interaction_survives_curv": f_q.iloc[1]["Pr(>F)"] < SIG_THRESHOLD,
        # AIC/BIC
        "aic_m1": m1.aic, "aic_m2": m2.aic, "aic_m3": m3.aic,
        "bic_m1": m1.bic, "bic_m2": m2.bic, "bic_m3": m3.bic,
        # Hypothesis tests
        "h1_supported": (f_12.iloc[1]["Pr(>F)"] < SIG_THRESHOLD and
                         m2_ols.params.get("phi_x_nu", 0) > 0),
        "h2_supported": (f_23.iloc[1]["Pr(>F)"] < SIG_THRESHOLD and
                         m3_ols.params.get("balance", 0) > 0),
    }


# =============================================================================
# META-ANALYSIS
# =============================================================================

def random_effects_meta(betas: np.ndarray, ses: np.ndarray) -> dict:
    """
    Random-effects meta-analysis (DerSimonian-Laird estimator).
    Returns pooled estimate, CI, heterogeneity stats.
    """
    k = len(betas)
    w_fixed = 1.0 / (ses ** 2)
    beta_fixed = np.sum(w_fixed * betas) / np.sum(w_fixed)

    Q = np.sum(w_fixed * (betas - beta_fixed) ** 2)
    df = k - 1
    C = np.sum(w_fixed) - np.sum(w_fixed ** 2) / np.sum(w_fixed)

    tau2 = max(0, (Q - df) / C)
    w_re = 1.0 / (ses ** 2 + tau2)
    beta_re = np.sum(w_re * betas) / np.sum(w_re)
    se_re = 1.0 / np.sqrt(np.sum(w_re))

    ci_lower = beta_re - 1.96 * se_re
    ci_upper = beta_re + 1.96 * se_re
    z = beta_re / se_re
    p = 2 * (1 - sp_stats.norm.cdf(abs(z)))

    I2 = max(0, (Q - df) / Q) * 100 if Q > 0 else 0

    return {
        "beta": beta_re,
        "se": se_re,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p": p,
        "z": z,
        "tau2": tau2,
        "Q": Q,
        "I2": I2,
        "k": k,
    }


# =============================================================================
# REPORTING
# =============================================================================

def print_country_table(results: list):
    """Print formatted results table for all countries."""
    print("\n" + "=" * 100)
    print("COUNTRY-LEVEL RESULTS")
    print("=" * 100)
    print(f"{'Country':<20} {'N':>6} {'R²_M1':>7} {'R²_M2':>7} {'ΔR²':>8} "
          f"{'β_int':>7} {'p_int':>10} {'H1':>4} {'β_bal':>7} {'p_bal':>10} {'H2':>4}")
    print("-" * 100)

    for r in sorted(results, key=lambda x: x["country"]):
        print(f"{r['country']:<20} {r['n']:>6} {r['r2_m1']:>7.4f} {r['r2_m2']:>7.4f} "
              f"{r['delta_r2_12']:>8.5f} {r['beta_interaction']:>7.4f} "
              f"{r['p_interaction']:>10.2e} {'✓' if r['h1_supported'] else '✗':>4} "
              f"{r['beta_balance']:>7.4f} {r['p_balance']:>10.2e} "
              f"{'✓' if r['h2_supported'] else '✗':>4}")

    print("-" * 100)


def print_verdict(results: list, meta_int: dict, meta_bal: dict):
    """Print the final verdict."""
    h1_count = sum(1 for r in results if r["h1_supported"])
    h2_count = sum(1 for r in results if r["h2_supported"])
    n_countries = len(results)

    # Check cultural cluster coverage for H3
    clusters_with_support = set()
    for r in results:
        if r["h1_supported"] or r["h2_supported"]:
            for cluster, countries in CULTURAL_CLUSTERS.items():
                if r["country"] in countries:
                    clusters_with_support.add(cluster)

    print("\n" + "=" * 80)
    print("VERDICT")
    print("=" * 80)

    # H1
    print(f"\nH1 (multiplicative > additive): {h1_count}/{n_countries} countries")
    print(f"  Threshold: {H1_COUNTRY_THRESHOLD}/{n_countries}")
    if h1_count >= H1_COUNTRY_THRESHOLD:
        print(f"  → H1 CONFIRMED")
    elif h1_count >= 11:
        print(f"  → AMBIGUOUS (between 11 and {H1_COUNTRY_THRESHOLD})")
    else:
        print(f"  → H1 FALSIFIED")

    # Meta-analysis
    print(f"\n  Meta-analytic interaction: β = {meta_int['beta']:.4f} "
          f"[{meta_int['ci_lower']:.4f}, {meta_int['ci_upper']:.4f}]")
    print(f"  p = {meta_int['p']:.2e}, I² = {meta_int['I2']:.1f}%")
    ci_excludes_zero = meta_int["ci_lower"] > 0 or meta_int["ci_upper"] < 0
    print(f"  95% CI excludes zero: {'YES' if ci_excludes_zero else 'NO'}")

    # H2
    print(f"\nH2 (balance effect): {h2_count}/{n_countries} countries")
    print(f"  Threshold: {H2_COUNTRY_THRESHOLD}/{n_countries}")
    if h2_count >= H2_COUNTRY_THRESHOLD:
        print(f"  → H2 CONFIRMED")
    else:
        print(f"  → H2 NOT CONFIRMED")

    print(f"\n  Meta-analytic balance: β = {meta_bal['beta']:.4f} "
          f"[{meta_bal['ci_lower']:.4f}, {meta_bal['ci_upper']:.4f}]")
    print(f"  p = {meta_bal['p']:.2e}")

    # H3
    print(f"\nH3 (cross-cultural): {len(clusters_with_support)}/7 cultural clusters with support")
    print(f"  Clusters: {', '.join(sorted(clusters_with_support))}")
    if len(clusters_with_support) >= 7:
        print(f"  → H3 CONFIRMED (all clusters represented)")
    else:
        missing = set(CULTURAL_CLUSTERS.keys()) - clusters_with_support
        print(f"  → H3 PARTIAL (missing: {', '.join(sorted(missing))})")

    # Falsification
    print(f"\n--- FALSIFICATION CHECK ---")
    if h1_count >= H1_COUNTRY_THRESHOLD and meta_int["beta"] > 0 and ci_excludes_zero:
        print("STRONG CONFIRMATION: Multiplicative model wins in supermajority.")
        print("Evidence tier: [I] → [S] Structural (pending independent replication for [E])")
    elif h1_count >= 11:
        print("AMBIGUOUS: Multiplicative signal present but not universal.")
        print("Evidence tier: remains [I] Interpretive. Boundary conditions needed.")
    elif h1_count < 11 and meta_int["beta"] <= 0:
        print("STRONG FALSIFICATION: Additive model dominates. Interaction absent or negative.")
        print("Evidence tier: remains [I]. Multiplicative prediction NOT supported.")
    else:
        print("MODERATE FALSIFICATION: Fewer than 15 countries, but interaction may be culture-specific.")

    print("\n--- EVIDENCE TIER ---")
    print("This is a CONFIRMATORY test on preregistered data.")
    print("Upgrade to [E] Established requires independent replication on non-GFS data.")


# =============================================================================
# MAIN
# =============================================================================

def run_analysis(data_path: str):
    """Run the full preregistered analysis."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 80)
    print("GFS 22-Country Confirmatory Analysis")
    print("Multiplicative vs. Additive Models of Human Flourishing")
    print(f"Run: {timestamp}")
    print("=" * 80)
    print(f"\nSignificance threshold: p < {SIG_THRESHOLD}")
    print(f"H1 country threshold: {H1_COUNTRY_THRESHOLD}/22")
    print(f"H2 country threshold: {H2_COUNTRY_THRESHOLD}/22")

    # Load data
    df = load_gfs_data(data_path)

    # Get available countries
    if "country" not in df.columns:
        print("\nERROR: No 'country' column found.")
        print("Available columns:", list(df.columns[:30]))
        print("Please adjust the column mapping in construct_composites()")
        return

    available = df["country"].unique()
    print(f"\nCountries in data: {len(available)}")

    # Run per-country analysis
    results = []
    for country in sorted(available):
        try:
            cdf = construct_composites(df, country)
            if len(cdf) < 500:
                print(f"  SKIP {country}: N={len(cdf)} < 500")
                continue
            r = fit_country_models(cdf, country)
            results.append(r)
            status = "✓" if r["h1_supported"] else "✗"
            print(f"  {status} {country}: N={r['n']}, ΔR²={r['delta_r2_12']:.5f}, "
                  f"β_int={r['beta_interaction']:.4f}, p={r['p_interaction']:.2e}")
        except Exception as e:
            print(f"  ERROR {country}: {e}")

    if not results:
        print("\nNo countries analyzed. Check data format and column mapping.")
        return

    # Country table
    print_country_table(results)

    # Meta-analysis
    betas_int = np.array([r["beta_interaction"] for r in results])
    ses_int = np.array([r["se_interaction"] for r in results])
    meta_int = random_effects_meta(betas_int, ses_int)

    betas_bal = np.array([r["beta_balance"] for r in results])
    ses_bal = np.array([r["se_balance"] for r in results])
    meta_bal = random_effects_meta(betas_bal, ses_bal)

    print(f"\n{'='*80}")
    print("META-ANALYSIS (Random Effects, DerSimonian-Laird)")
    print(f"{'='*80}")
    print(f"\nInteraction (phi x nu):")
    print(f"  Pooled β = {meta_int['beta']:.4f} (SE = {meta_int['se']:.4f})")
    print(f"  95% CI = [{meta_int['ci_lower']:.4f}, {meta_int['ci_upper']:.4f}]")
    print(f"  z = {meta_int['z']:.3f}, p = {meta_int['p']:.2e}")
    print(f"  τ² = {meta_int['tau2']:.6f}, I² = {meta_int['I2']:.1f}%")

    print(f"\nBalance (-|phi - nu|):")
    print(f"  Pooled β = {meta_bal['beta']:.4f} (SE = {meta_bal['se']:.4f})")
    print(f"  95% CI = [{meta_bal['ci_lower']:.4f}, {meta_bal['ci_upper']:.4f}]")
    print(f"  z = {meta_bal['z']:.3f}, p = {meta_bal['p']:.2e}")

    # Verdict
    print_verdict(results, meta_int, meta_bal)

    # Save results
    results_df = pd.DataFrame(results)
    output_path = "gfs_results_" + datetime.now().strftime("%Y%m%d") + ".csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

    # Save meta-analysis
    meta_path = "gfs_meta_analysis_" + datetime.now().strftime("%Y%m%d") + ".txt"
    with open(meta_path, "w") as f:
        f.write("GFS Meta-Analysis Results\n")
        f.write(f"Date: {timestamp}\n\n")
        f.write(f"Interaction: β={meta_int['beta']:.4f}, p={meta_int['p']:.2e}, I²={meta_int['I2']:.1f}%\n")
        f.write(f"Balance: β={meta_bal['beta']:.4f}, p={meta_bal['p']:.2e}\n")
        f.write(f"\nH1: {sum(1 for r in results if r['h1_supported'])}/{len(results)} countries\n")
        f.write(f"H2: {sum(1 for r in results if r['h2_supported'])}/{len(results)} countries\n")
    print(f"Meta-analysis saved to: {meta_path}")

    print("\n⊙ = • × ○")


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="GFS 22-Country Confirmatory Analysis: φ×ν vs φ+ν")
    parser.add_argument("data_path", help="Path to GFS Wave 1 data file (CSV/TSV/SAV/DTA)")
    parser.add_argument("--sig", type=float, default=0.005,
                        help="Significance threshold (default: 0.005)")
    args = parser.parse_args()

    SIG_THRESHOLD = args.sig
    run_analysis(args.data_path)

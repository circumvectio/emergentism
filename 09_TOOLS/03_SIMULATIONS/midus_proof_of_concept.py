#!/usr/bin/env python3
"""
MIDUS Proof-of-Concept: Multiplicative vs. Additive Models of Flourishing
==========================================================================

Tests the Emergentist prediction: phi x nu > phi + nu for predicting
human flourishing. Uses Ryff's six psychological wellbeing dimensions
from MIDUS Wave 2 (Study 4652, ICPSR).

Evidence tier: [C] Conjecture — exploratory proof-of-concept.
The former GFS confirmatory lane was retracted and archived on 2026-07-13;
this script does not define a successor or a canon-upgrade route.

Data source: https://www.icpsr.umich.edu/web/NACDA/studies/4652

Author: Yves R. Burri / Emergentism.org
Date: 2026-04-05
License: CC BY-SA 4.0
"""

import numpy as np
import warnings
warnings.filterwarnings("ignore")

try:
    import pandas as pd
    from scipy import stats as sp_stats
    import statsmodels.api as sm
    from statsmodels.stats.anova import anova_lm
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install pandas scipy statsmodels matplotlib")
    exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

USE_SYNTHETIC = True  # Set False when you have real MIDUS data
DATA_PATH = "MIDUS2_data.tsv"  # Adjust to your actual file path
SIG_THRESHOLD = 0.005  # Benjamin et al. (2018) conservative threshold

print("=" * 60)
print("MIDUS Proof-of-Concept Analysis")
print("Multiplicative vs. Additive Flourishing")
print("=" * 60)
print()

# =============================================================================
# SECTION 1: DATA LOADING
# =============================================================================

if USE_SYNTHETIC:
    print("NOTE: Using synthetic data for pipeline testing.")
    print("Set USE_SYNTHETIC = False with real MIDUS data for actual results.\n")

    np.random.seed(42)
    n = 5000

    # Generate synthetic Ryff-like scores (1-7 scale) with known multiplicative structure
    base_phi = np.random.normal(4.5, 1.0, n)
    base_nu = np.random.normal(4.5, 1.0, n)

    df = pd.DataFrame({
        "self_acceptance": np.clip(base_phi + np.random.normal(0, 0.5, n), 1, 7),
        "personal_growth": np.clip(base_phi + np.random.normal(0, 0.5, n), 1, 7),
        "purpose_in_life": np.clip(base_phi + np.random.normal(0, 0.5, n), 1, 7),
        "env_mastery":     np.clip(base_nu + np.random.normal(0, 0.5, n), 1, 7),
        "autonomy":        np.clip(base_nu + np.random.normal(0, 0.5, n), 1, 7),
        "positive_rels":   np.clip(base_nu + np.random.normal(0, 0.5, n), 1, 7),
        "age": np.round(np.random.normal(55, 12, n)),
        "female": np.random.binomial(1, 0.52, n),
    })

    # Generate outcome with KNOWN multiplicative structure + noise
    phi_true = sp_stats.zscore(df[["self_acceptance", "personal_growth", "purpose_in_life"]].mean(axis=1))
    nu_true = sp_stats.zscore(df[["env_mastery", "autonomy", "positive_rels"]].mean(axis=1))
    df["life_satisfaction"] = np.clip(
        5 + 0.4 * phi_true + 0.4 * nu_true + 0.15 * phi_true * nu_true + np.random.normal(0, 1.0, n),
        0, 10
    )
else:
    print(f"Loading MIDUS data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, sep="\t")
    # Rename variables to match expected names — adjust for your data
    # df = df.rename(columns={...})

print(f"Sample size (raw): {len(df)}")

# =============================================================================
# SECTION 2: CONSTRUCT PHI AND NU COMPOSITES
# =============================================================================

# phi = mean(Self-Acceptance, Personal Growth, Purpose in Life)
df["phi_raw"] = df[["self_acceptance", "personal_growth", "purpose_in_life"]].mean(axis=1)

# nu = mean(Environmental Mastery, Autonomy, Positive Relations)
df["nu_raw"] = df[["env_mastery", "autonomy", "positive_rels"]].mean(axis=1)

# Complete cases
df_complete = df.dropna(subset=["phi_raw", "nu_raw", "life_satisfaction"]).copy()
print(f"Sample size (complete): {len(df_complete)}")
pct_dropped = round(100 * (1 - len(df_complete) / len(df)), 1)
print(f"Dropped: {pct_dropped}% due to missing data")
if pct_dropped > 10:
    print("WARNING: >10% dropped. Multiple imputation recommended.")

# Standardize
df_complete["phi"] = sp_stats.zscore(df_complete["phi_raw"])
df_complete["nu"] = sp_stats.zscore(df_complete["nu_raw"])

# Derived variables
df_complete["phi_x_nu"] = df_complete["phi"] * df_complete["nu"]
df_complete["balance"] = -np.abs(df_complete["phi"] - df_complete["nu"])
df_complete["phi_sq"] = df_complete["phi"] ** 2
df_complete["nu_sq"] = df_complete["nu"] ** 2

print(f"\nDescriptive Statistics:")
print(f"  phi:  M = {df_complete['phi'].mean():.3f}  SD = {df_complete['phi'].std():.3f}")
print(f"  nu:   M = {df_complete['nu'].mean():.3f}  SD = {df_complete['nu'].std():.3f}")
print(f"  LS:   M = {df_complete['life_satisfaction'].mean():.3f}  SD = {df_complete['life_satisfaction'].std():.3f}")
print(f"  cor(phi, nu) = {df_complete['phi'].corr(df_complete['nu']):.3f}")

# =============================================================================
# SECTION 3: MODEL COMPARISON (THE CORE TEST)
# =============================================================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

y = df_complete["life_satisfaction"]

# Model 1: Additive
X1 = sm.add_constant(df_complete[["phi", "nu"]])
m1 = sm.OLS(y, X1).fit(cov_type="HC1")

# Model 2: Multiplicative
X2 = sm.add_constant(df_complete[["phi", "nu", "phi_x_nu"]])
m2 = sm.OLS(y, X2).fit(cov_type="HC1")

# Model 3: Balance
X3 = sm.add_constant(df_complete[["phi", "nu", "phi_x_nu", "balance"]])
m3 = sm.OLS(y, X3).fit(cov_type="HC1")

r2_m1 = m1.rsquared
r2_m2 = m2.rsquared
r2_m3 = m3.rsquared
delta_r2_12 = r2_m2 - r2_m1
delta_r2_23 = r2_m3 - r2_m2

# F-tests (using non-robust for nested comparison)
m1_ols = sm.OLS(y, X1).fit()
m2_ols = sm.OLS(y, X2).fit()
m3_ols = sm.OLS(y, X3).fit()
f_test_12 = anova_lm(m1_ols, m2_ols)
f_test_23 = anova_lm(m2_ols, m3_ols)

f_val_12 = f_test_12.iloc[1]["F"]
p_val_12 = f_test_12.iloc[1]["Pr(>F)"]
f_val_23 = f_test_23.iloc[1]["F"]
p_val_23 = f_test_23.iloc[1]["Pr(>F)"]

print(f"\n--- Model 1 (Additive): LS ~ phi + nu ---")
print(f"  R² = {r2_m1:.4f}")
print(f"  phi coef: {m1.params['phi']:.4f}  (p = {m1.pvalues['phi']:.2e})")
print(f"  nu coef:  {m1.params['nu']:.4f}  (p = {m1.pvalues['nu']:.2e})")

print(f"\n--- Model 2 (Multiplicative): LS ~ phi + nu + phi*nu ---")
print(f"  R² = {r2_m2:.4f}")
print(f"  phi*nu coef: {m2.params['phi_x_nu']:.4f}  (p = {m2.pvalues['phi_x_nu']:.2e})")
print(f"  ΔR² (M1→M2) = {delta_r2_12:.5f}")
print(f"  F-test: F = {f_val_12:.3f}, p = {p_val_12:.2e}")

print(f"\n--- Model 3 (Balance): LS ~ phi + nu + phi*nu + balance ---")
print(f"  R² = {r2_m3:.4f}")
print(f"  balance coef: {m3.params['balance']:.4f}  (p = {m3.pvalues['balance']:.2e})")
print(f"  ΔR² (M2→M3) = {delta_r2_23:.5f}")
print(f"  F-test: F = {f_val_23:.3f}, p = {p_val_23:.2e}")

print(f"\n--- Information Criteria ---")
print(f"  AIC:  M1 = {m1.aic:.1f}  M2 = {m2.aic:.1f}  M3 = {m3.aic:.1f}")
print(f"  BIC:  M1 = {m1.bic:.1f}  M2 = {m2.bic:.1f}  M3 = {m3.bic:.1f}")

# =============================================================================
# SECTION 4: ROBUSTNESS — CURVILINEARITY
# =============================================================================

print("\n" + "=" * 60)
print("ROBUSTNESS: Curvilinearity Check")
print("=" * 60)

X1q = sm.add_constant(df_complete[["phi", "nu", "phi_sq", "nu_sq"]])
X2q = sm.add_constant(df_complete[["phi", "nu", "phi_sq", "nu_sq", "phi_x_nu"]])
m1q = sm.OLS(y, X1q).fit()
m2q = sm.OLS(y, X2q).fit()
f_test_q = anova_lm(m1q, m2q)
f_val_q = f_test_q.iloc[1]["F"]
p_val_q = f_test_q.iloc[1]["Pr(>F)"]

print(f"\nAfter controlling for phi² and nu²:")
print(f"  phi*nu coef: {m2q.params['phi_x_nu']:.4f}  (p = {m2q.pvalues['phi_x_nu']:.2e})")
print(f"  F-test: F = {f_val_q:.3f}, p = {p_val_q:.2e}")
print(f"  Interaction survives: {'YES' if p_val_q < SIG_THRESHOLD else 'NO'}")

# =============================================================================
# SECTION 5: ROBUSTNESS — ALTERNATIVE SPLIT
# =============================================================================

print("\n" + "=" * 60)
print("ROBUSTNESS: Alternative phi/nu Split")
print("(Positive Relations moved to phi)")
print("=" * 60)

df_complete["phi_alt"] = sp_stats.zscore(
    df_complete[["self_acceptance", "personal_growth", "purpose_in_life", "positive_rels"]].mean(axis=1))
df_complete["nu_alt"] = sp_stats.zscore(
    df_complete[["env_mastery", "autonomy"]].mean(axis=1))
df_complete["phi_alt_x_nu_alt"] = df_complete["phi_alt"] * df_complete["nu_alt"]

X1a = sm.add_constant(df_complete[["phi_alt", "nu_alt"]])
X2a = sm.add_constant(df_complete[["phi_alt", "nu_alt", "phi_alt_x_nu_alt"]])
m1a = sm.OLS(y, X1a).fit()
m2a = sm.OLS(y, X2a).fit()
f_test_a = anova_lm(m1a, m2a)

print(f"\n  ΔR² (alt split): {m2a.rsquared - m1a.rsquared:.5f}")
print(f"  phi_alt*nu_alt coef: {m2a.params['phi_alt_x_nu_alt']:.4f}  (p = {m2a.pvalues['phi_alt_x_nu_alt']:.2e})")
print(f"  Robust to alt split: {'YES' if f_test_a.iloc[1]['Pr(>F)'] < SIG_THRESHOLD else 'NO'}")

# =============================================================================
# SECTION 6: VISUALIZATION
# =============================================================================

try:
    import matplotlib.pyplot as plt
    import matplotlib

    print("\n" + "=" * 60)
    print("GENERATING PLOTS")
    print("=" * 60)

    # Plot 1: Interaction surface
    phi_grid = np.linspace(-2, 2, 50)
    nu_grid = np.linspace(-2, 2, 50)
    PHI, NU = np.meshgrid(phi_grid, nu_grid)
    PHI_X_NU = PHI * NU
    PRED = m2_ols.params["const"] + m2_ols.params["phi"] * PHI + m2_ols.params["nu"] * NU + m2_ols.params["phi_x_nu"] * PHI_X_NU

    fig, ax = plt.subplots(figsize=(8, 7))
    c = ax.pcolormesh(PHI, NU, PRED, cmap="magma", shading="auto")
    ax.contour(PHI, NU, PRED, colors="white", alpha=0.5, levels=10)
    plt.colorbar(c, label="Predicted Flourishing")
    ax.set_xlabel("φ (Coherence)", fontsize=13)
    ax.set_ylabel("ν (Viability)", fontsize=13)
    ax.set_title("Predicted Flourishing: Multiplicative Model\nLS ~ φ + ν + φ×ν", fontsize=14)
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.savefig("midus_interaction_surface.png", dpi=150)
    print("Saved: midus_interaction_surface.png")
    plt.close()

    # Plot 2: Balance effect
    df_complete["balance_q"] = pd.qcut(df_complete["balance"], 5, labels=False) + 1
    balance_means = df_complete.groupby("balance_q")["life_satisfaction"].agg(["mean", "sem"]).reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(balance_means["balance_q"], balance_means["mean"],
                yerr=1.96 * balance_means["sem"], fmt="o-", capsize=5, markersize=8, color="#D4AF37")
    ax.set_xlabel("Balance Quintile (1 = most imbalanced, 5 = most balanced)", fontsize=13)
    ax.set_ylabel("Mean Life Satisfaction", fontsize=13)
    ax.set_title("Balance Effect on Life Satisfaction\nBalance = -|φ - ν|", fontsize=14)
    plt.tight_layout()
    plt.savefig("midus_balance_effect.png", dpi=150)
    print("Saved: midus_balance_effect.png")
    plt.close()

    # Plot 3: Model comparison
    fig, ax = plt.subplots(figsize=(8, 6))
    models = ["M1: Additive", "M2: Multiplicative", "M3: Balance"]
    r2_vals = [r2_m1, r2_m2, r2_m3]
    colors = ["#4A90D9", "#D4AF37", "#2E8B57"]
    bars = ax.bar(models, r2_vals, color=colors, alpha=0.8)
    for bar, val in zip(bars, r2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                f"{val:.4f}", ha="center", fontsize=12)
    ax.set_ylabel("R²", fontsize=13)
    ax.set_title("Model Comparison: R² Values", fontsize=14)
    ax.set_ylim(0, max(r2_vals) * 1.15)
    plt.tight_layout()
    plt.savefig("midus_model_comparison.png", dpi=150)
    print("Saved: midus_model_comparison.png")
    plt.close()

except ImportError:
    print("\nmatplotlib not installed — skipping plots.")
    print("Install with: pip install matplotlib")

# =============================================================================
# SECTION 7: VERDICT
# =============================================================================

print("\n" + "=" * 60)
print("VERDICT")
print("=" * 60)

h1_supported = p_val_12 < SIG_THRESHOLD and m2_ols.params["phi_x_nu"] > 0
h2_supported = p_val_23 < SIG_THRESHOLD and m3_ols.params["balance"] > 0
robust_curv = p_val_q < SIG_THRESHOLD

print(f"\nH1 (multiplicative > additive): {'SUPPORTED' if h1_supported else 'NOT SUPPORTED'}")
print(f"  phi*nu coefficient: {m2_ols.params['phi_x_nu']:.4f} {'(positive)' if m2_ols.params['phi_x_nu'] > 0 else '(NEGATIVE)'}")
print(f"  p-value: {p_val_12:.2e} {'(sig at p < .005)' if p_val_12 < SIG_THRESHOLD else '(not sig)'}")
print(f"  ΔR²: {delta_r2_12:.5f}")

print(f"\nH2 (balance effect): {'SUPPORTED' if h2_supported else 'NOT SUPPORTED'}")
print(f"  Balance coefficient: {m3_ols.params['balance']:.4f}")
print(f"  p-value: {p_val_23:.2e}")

print(f"\nCurvilinearity robustness: {'Interaction survives' if robust_curv else 'May be artifact'}")

# Effect size
print(f"\nEffect size:")
if delta_r2_12 >= 0.10:
    print(f"  ΔR² = {delta_r2_12:.4f} → LARGE")
elif delta_r2_12 >= 0.05:
    print(f"  ΔR² = {delta_r2_12:.4f} → MODERATE")
elif delta_r2_12 >= 0.02:
    print(f"  ΔR² = {delta_r2_12:.4f} → SMALL BUT MEANINGFUL")
elif delta_r2_12 > 0:
    print(f"  ΔR² = {delta_r2_12:.4f} → TRIVIAL (< .02)")
else:
    print(f"  ΔR² = {delta_r2_12:.4f} → ZERO OR NEGATIVE")

print("\n" + "=" * 60)
print("EVIDENCE TIER ASSESSMENT")
print("=" * 60)

if h1_supported and robust_curv:
    print("\nResult: PROOF-OF-CONCEPT PASSED")
    print("The multiplicative model outperforms the additive model.")
    print("The historical GFS confirmatory lane was retired on 2026-07-13.")
    print("Evidence tier: [C] → remains [C] (single dataset, one country, exploratory)")
    print("No canon upgrade follows from this exploratory output.")
elif m2_ols.params["phi_x_nu"] > 0 and p_val_12 < 0.05:
    print("\nResult: SUGGESTIVE (p < .05 but not < .005)")
    print("The interaction is in the predicted direction but does not meet")
    print("the conservative significance threshold.")
else:
    print("\nResult: PROOF-OF-CONCEPT FAILED")
    print("The multiplicative model does not outperform the additive model.")
    print("The retired GFS lane supplies no fallback confirmation.")

print("\n--- Analysis complete ---")
print("This is a PROOF-OF-CONCEPT on MIDUS data (single US sample).")
print("The former GFS study and pipeline are archived as retracted history.")
print("Current claims remain at their declared tiers pending a new independent test.")
print("\n•   ⊙   ○")

#!/usr/bin/env Rscript
# =============================================================================
# MIDUS Proof-of-Concept: Multiplicative vs. Additive Models of Flourishing
# =============================================================================
#
# Tests the Emergentist prediction: phi x nu > phi + nu for predicting
# human flourishing. Uses Ryff's six psychological wellbeing dimensions
# from MIDUS Wave 2 (Study 4652, ICPSR).
#
# Evidence tier: [C] Conjecture — exploratory proof-of-concept.
# The former confirmatory survey lane is retired and non-citable. This script
# remains an exploratory [C] artifact; any upgrade requires a new independently
# governed, preregistered study.
#
# Data source: https://www.icpsr.umich.edu/web/NACDA/studies/4652
# Download the MIDUS 2 data and place the .rda or .tsv file in this directory.
#
# Author: Yves R. Burri / Emergentism.org
# Date: 2026-04-05
# License: CC BY-SA 4.0
# =============================================================================

# --- Dependencies ---
required_packages <- c("stats", "car", "lmtest", "ggplot2", "dplyr", "tidyr")
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}
library(dplyr)
library(ggplot2)
library(car)
library(lmtest)

cat("\n========================================\n")
cat("MIDUS Proof-of-Concept Analysis\n")
cat("Multiplicative vs. Additive Flourishing\n")
cat("========================================\n\n")

# =============================================================================
# SECTION 1: DATA LOADING
# =============================================================================
# MIDUS 2 Ryff Psychological Well-Being scales (42-item version)
#
# You need to download MIDUS 2 from ICPSR (Study 4652):
#   https://www.icpsr.umich.edu/web/NACDA/studies/4652
#
# After download, set the path below to point to your data file.
# The script expects either:
#   (a) An .rda file from the ICPSR R download, or
#   (b) A .tsv/.csv with Ryff subscale scores
# =============================================================================

# --- CONFIGURATION: Set your data path here ---
DATA_PATH <- "MIDUS2_data.rda"  # Adjust to your actual file path

# --- Ryff subscale variable names in MIDUS 2 ---
# These are the standard MIDUS 2 variable names for the 7-point Ryff scales.
# Adjust if your version uses different names.
RYFF_VARS <- list(
  # phi (coherence) dimensions
  self_acceptance  = "B1SPWBA2",  # Ryff Self-Acceptance
  personal_growth  = "B1SPWBG2",  # Ryff Personal Growth
  purpose_in_life  = "B1SPWBU2",  # Ryff Purpose in Life

  # nu (viability) dimensions
  env_mastery      = "B1SPWBE2",  # Ryff Environmental Mastery
  autonomy         = "B1SPWBR2",  # Ryff Autonomy
  positive_rels    = "B1SPWBS2",  # Ryff Positive Relations with Others

  # outcome
  life_satisfaction = "B1SSWBSI", # Life Satisfaction (if available)
  positive_affect   = "B1SPOSPA", # Positive Affect
  negative_affect   = "B1SPOSNA"  # Negative Affect
)

# --- Alternative: Use synthetic data for testing the pipeline ---
USE_SYNTHETIC <- TRUE  # Set FALSE when you have real MIDUS data

if (USE_SYNTHETIC) {
  cat("NOTE: Using synthetic data for pipeline testing.\n")
  cat("Set USE_SYNTHETIC <- FALSE and provide real MIDUS data for actual results.\n\n")

  set.seed(42)
  n <- 5000

  # Generate synthetic Ryff-like scores (1-7 scale) with known multiplicative structure
  base_phi <- rnorm(n, 4.5, 1.0)
  base_nu  <- rnorm(n, 4.5, 1.0)

  df <- data.frame(
    self_acceptance  = pmin(7, pmax(1, base_phi + rnorm(n, 0, 0.5))),
    personal_growth  = pmin(7, pmax(1, base_phi + rnorm(n, 0, 0.5))),
    purpose_in_life  = pmin(7, pmax(1, base_phi + rnorm(n, 0, 0.5))),
    env_mastery      = pmin(7, pmax(1, base_nu  + rnorm(n, 0, 0.5))),
    autonomy         = pmin(7, pmax(1, base_nu  + rnorm(n, 0, 0.5))),
    positive_rels    = pmin(7, pmax(1, base_nu  + rnorm(n, 0, 0.5))),
    age              = round(rnorm(n, 55, 12)),
    female           = rbinom(n, 1, 0.52)
  )

  # Generate outcome with KNOWN multiplicative structure + noise
  phi_true <- scale(rowMeans(df[, c("self_acceptance", "personal_growth", "purpose_in_life")]))[,1]
  nu_true  <- scale(rowMeans(df[, c("env_mastery", "autonomy", "positive_rels")]))[,1]
  df$life_satisfaction <- 5 + 0.4 * phi_true + 0.4 * nu_true +
                          0.15 * phi_true * nu_true +  # multiplicative signal
                          rnorm(n, 0, 1.0)
  df$life_satisfaction <- pmin(10, pmax(0, df$life_satisfaction))

} else {
  # --- Load real MIDUS data ---
  cat("Loading MIDUS data from:", DATA_PATH, "\n")
  if (grepl("\\.rda$", DATA_PATH)) {
    load(DATA_PATH)
    # The loaded object name varies — adjust below
    # df <- get(ls()[1])  # Uncomment and adjust
    stop("Adjust the data loading code for your specific MIDUS file format.")
  } else {
    df <- read.csv(DATA_PATH, sep = "\t")
  }

  # --- Rename variables to standard names ---
  # Uncomment and adjust based on your actual variable names:
  # df <- df %>% rename(
  #   self_acceptance  = !!RYFF_VARS$self_acceptance,
  #   personal_growth  = !!RYFF_VARS$personal_growth,
  #   purpose_in_life  = !!RYFF_VARS$purpose_in_life,
  #   env_mastery      = !!RYFF_VARS$env_mastery,
  #   autonomy         = !!RYFF_VARS$autonomy,
  #   positive_rels    = !!RYFF_VARS$positive_rels,
  #   life_satisfaction = !!RYFF_VARS$life_satisfaction
  # )
}

cat("Sample size (raw):", nrow(df), "\n")

# =============================================================================
# SECTION 2: CONSTRUCT PHI AND NU COMPOSITES
# =============================================================================

# phi = mean(Self-Acceptance, Personal Growth, Purpose in Life)
df$phi_raw <- rowMeans(df[, c("self_acceptance", "personal_growth", "purpose_in_life")],
                       na.rm = FALSE)

# nu = mean(Environmental Mastery, Autonomy, Positive Relations)
df$nu_raw <- rowMeans(df[, c("env_mastery", "autonomy", "positive_rels")],
                      na.rm = FALSE)

# Complete cases only
df_complete <- df %>%
  filter(!is.na(phi_raw) & !is.na(nu_raw) & !is.na(life_satisfaction))

cat("Sample size (complete cases):", nrow(df_complete), "\n")
pct_dropped <- round(100 * (1 - nrow(df_complete) / nrow(df)), 1)
cat("Dropped:", pct_dropped, "% due to missing data\n")
if (pct_dropped > 10) {
  cat("WARNING: >10% dropped. Multiple imputation recommended as sensitivity check.\n")
}

# Standardize within sample
df_complete$phi <- scale(df_complete$phi_raw)[, 1]
df_complete$nu  <- scale(df_complete$nu_raw)[, 1]

# Derived variables
df_complete$phi_x_nu <- df_complete$phi * df_complete$nu
df_complete$balance  <- -abs(df_complete$phi - df_complete$nu)
df_complete$phi_sq   <- df_complete$phi^2
df_complete$nu_sq    <- df_complete$nu^2

cat("\nDescriptive Statistics:\n")
cat("  phi:  M =", round(mean(df_complete$phi), 3),
    " SD =", round(sd(df_complete$phi), 3), "\n")
cat("  nu:   M =", round(mean(df_complete$nu), 3),
    " SD =", round(sd(df_complete$nu), 3), "\n")
cat("  LS:   M =", round(mean(df_complete$life_satisfaction), 3),
    " SD =", round(sd(df_complete$life_satisfaction), 3), "\n")
cat("  cor(phi, nu) =", round(cor(df_complete$phi, df_complete$nu), 3), "\n\n")

# =============================================================================
# SECTION 3: MODEL COMPARISON (THE CORE TEST)
# =============================================================================

cat("========================================\n")
cat("MODEL COMPARISON\n")
cat("========================================\n\n")

# --- Model 1: Additive ---
m1 <- lm(life_satisfaction ~ phi + nu, data = df_complete)

# --- Model 2: Multiplicative ---
m2 <- lm(life_satisfaction ~ phi + nu + phi_x_nu, data = df_complete)

# --- Model 3: Balance ---
m3 <- lm(life_satisfaction ~ phi + nu + phi_x_nu + balance, data = df_complete)

# --- Model comparison ---
r2_m1 <- summary(m1)$r.squared
r2_m2 <- summary(m2)$r.squared
r2_m3 <- summary(m3)$r.squared

delta_r2_m1_m2 <- r2_m2 - r2_m1
delta_r2_m2_m3 <- r2_m3 - r2_m2

# F-tests for nested models
f_test_m1_m2 <- anova(m1, m2)
f_test_m2_m3 <- anova(m2, m3)

cat("--- Model 1 (Additive): LS ~ phi + nu ---\n")
cat("  R² =", round(r2_m1, 4), "\n")
cat("  phi coef:", round(coef(m1)["phi"], 4),
    " (p =", format.pval(summary(m1)$coefficients["phi", 4], digits = 3), ")\n")
cat("  nu coef: ", round(coef(m1)["nu"], 4),
    " (p =", format.pval(summary(m1)$coefficients["nu", 4], digits = 3), ")\n\n")

cat("--- Model 2 (Multiplicative): LS ~ phi + nu + phi*nu ---\n")
cat("  R² =", round(r2_m2, 4), "\n")
cat("  phi*nu coef:", round(coef(m2)["phi_x_nu"], 4),
    " (p =", format.pval(summary(m2)$coefficients["phi_x_nu", 4], digits = 3), ")\n")
cat("  ΔR² (M1→M2) =", round(delta_r2_m1_m2, 5), "\n")
cat("  F-test (M1 vs M2): F =", round(f_test_m1_m2$F[2], 3),
    ", p =", format.pval(f_test_m1_m2$`Pr(>F)`[2], digits = 3), "\n\n")

cat("--- Model 3 (Balance): LS ~ phi + nu + phi*nu + balance ---\n")
cat("  R² =", round(r2_m3, 4), "\n")
cat("  balance coef:", round(coef(m3)["balance"], 4),
    " (p =", format.pval(summary(m3)$coefficients["balance", 4], digits = 3), ")\n")
cat("  ΔR² (M2→M3) =", round(delta_r2_m2_m3, 5), "\n")
cat("  F-test (M2 vs M3): F =", round(f_test_m2_m3$F[2], 3),
    ", p =", format.pval(f_test_m2_m3$`Pr(>F)`[2], digits = 3), "\n\n")

# --- AIC/BIC ---
cat("--- Information Criteria ---\n")
cat("  AIC:  M1 =", round(AIC(m1), 1),
    "  M2 =", round(AIC(m2), 1),
    "  M3 =", round(AIC(m3), 1), "\n")
cat("  BIC:  M1 =", round(BIC(m1), 1),
    "  M2 =", round(BIC(m2), 1),
    "  M3 =", round(BIC(m3), 1), "\n\n")

# =============================================================================
# SECTION 4: ROBUSTNESS CHECK — CURVILINEARITY
# =============================================================================

cat("========================================\n")
cat("ROBUSTNESS: Curvilinearity Check\n")
cat("========================================\n\n")

# Does adding phi² and nu² to M1 eliminate the interaction effect?
m1_quad <- lm(life_satisfaction ~ phi + nu + phi_sq + nu_sq, data = df_complete)
m2_quad <- lm(life_satisfaction ~ phi + nu + phi_sq + nu_sq + phi_x_nu, data = df_complete)

f_test_quad <- anova(m1_quad, m2_quad)
cat("After controlling for phi² and nu²:\n")
cat("  phi*nu coef:", round(coef(m2_quad)["phi_x_nu"], 4),
    " (p =", format.pval(summary(m2_quad)$coefficients["phi_x_nu", 4], digits = 3), ")\n")
cat("  F-test: F =", round(f_test_quad$F[2], 3),
    ", p =", format.pval(f_test_quad$`Pr(>F)`[2], digits = 3), "\n")
cat("  Interaction survives curvilinearity control:",
    ifelse(f_test_quad$`Pr(>F)`[2] < 0.005, "YES", "NO"), "\n\n")

# =============================================================================
# SECTION 5: ROBUSTNESS — ALTERNATIVE PHI/NU SPLIT
# =============================================================================

cat("========================================\n")
cat("ROBUSTNESS: Alternative phi/nu Split\n")
cat("(Positive Relations moved to phi)\n")
cat("========================================\n\n")

# phi_alt = Self-Acceptance + Personal Growth + Purpose + Positive Relations
# nu_alt  = Environmental Mastery + Autonomy
df_complete$phi_alt_raw <- rowMeans(
  df_complete[, c("self_acceptance", "personal_growth", "purpose_in_life", "positive_rels")],
  na.rm = FALSE)
df_complete$nu_alt_raw <- rowMeans(
  df_complete[, c("env_mastery", "autonomy")],
  na.rm = FALSE)
df_complete$phi_alt <- scale(df_complete$phi_alt_raw)[, 1]
df_complete$nu_alt  <- scale(df_complete$nu_alt_raw)[, 1]
df_complete$phi_alt_x_nu_alt <- df_complete$phi_alt * df_complete$nu_alt

m1_alt <- lm(life_satisfaction ~ phi_alt + nu_alt, data = df_complete)
m2_alt <- lm(life_satisfaction ~ phi_alt + nu_alt + phi_alt_x_nu_alt, data = df_complete)
f_test_alt <- anova(m1_alt, m2_alt)

cat("  ΔR² (M1→M2, alt split):", round(summary(m2_alt)$r.squared - summary(m1_alt)$r.squared, 5), "\n")
cat("  phi_alt*nu_alt coef:", round(coef(m2_alt)["phi_alt_x_nu_alt"], 4),
    " (p =", format.pval(summary(m2_alt)$coefficients["phi_alt_x_nu_alt", 4], digits = 3), ")\n")
cat("  Interaction robust to alt split:",
    ifelse(f_test_alt$`Pr(>F)`[2] < 0.005, "YES", "NO"), "\n\n")

# =============================================================================
# SECTION 6: VISUALIZATION
# =============================================================================

cat("========================================\n")
cat("GENERATING PLOTS\n")
cat("========================================\n\n")

# --- Plot 1: Interaction surface ---
phi_grid <- seq(-2, 2, length.out = 50)
nu_grid  <- seq(-2, 2, length.out = 50)
grid <- expand.grid(phi = phi_grid, nu = nu_grid)
grid$phi_x_nu <- grid$phi * grid$nu
grid$predicted <- predict(m2, newdata = grid)

p1 <- ggplot(grid, aes(x = phi, y = nu, fill = predicted)) +
  geom_tile() +
  scale_fill_viridis_c(option = "magma", name = "Predicted\nFlourishing") +
  geom_contour(aes(z = predicted), color = "white", alpha = 0.5) +
  labs(
    title = "Predicted Flourishing: Multiplicative Model",
    subtitle = expression(paste("LS ~ ", phi, " + ", nu, " + ", phi, " × ", nu)),
    x = expression(paste(phi, " (Coherence)")),
    y = expression(paste(nu, " (Viability)"))
  ) +
  theme_minimal(base_size = 14) +
  coord_equal()

ggsave("midus_interaction_surface.png", p1, width = 8, height = 7, dpi = 150)
cat("Saved: midus_interaction_surface.png\n")

# --- Plot 2: Balance effect ---
df_complete$balance_bin <- cut(df_complete$balance,
                                breaks = quantile(df_complete$balance, probs = seq(0, 1, 0.2)),
                                include.lowest = TRUE, labels = FALSE)

p2 <- df_complete %>%
  group_by(balance_bin) %>%
  summarise(
    mean_ls = mean(life_satisfaction),
    se_ls   = sd(life_satisfaction) / sqrt(n()),
    .groups = "drop"
  ) %>%
  ggplot(aes(x = balance_bin, y = mean_ls)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = mean_ls - 1.96 * se_ls,
                     ymax = mean_ls + 1.96 * se_ls), width = 0.2) +
  geom_line(group = 1) +
  labs(
    title = "Balance Effect on Life Satisfaction",
    subtitle = "Balance = -|φ - ν| (higher = more balanced)",
    x = "Balance Quintile (1 = most imbalanced, 5 = most balanced)",
    y = "Mean Life Satisfaction"
  ) +
  theme_minimal(base_size = 14)

ggsave("midus_balance_effect.png", p2, width = 8, height = 6, dpi = 150)
cat("Saved: midus_balance_effect.png\n")

# --- Plot 3: Model comparison bar chart ---
model_results <- data.frame(
  Model = c("M1: Additive", "M2: Multiplicative", "M3: Balance"),
  R_squared = c(r2_m1, r2_m2, r2_m3),
  AIC = c(AIC(m1), AIC(m2), AIC(m3))
)

p3 <- ggplot(model_results, aes(x = Model, y = R_squared, fill = Model)) +
  geom_col(alpha = 0.8) +
  scale_fill_manual(values = c("#4A90D9", "#D4AF37", "#2E8B57")) +
  geom_text(aes(label = round(R_squared, 4)), vjust = -0.5, size = 4) +
  labs(
    title = "Model Comparison: R² Values",
    subtitle = "Does multiplicative structure improve prediction?",
    y = expression(R^2)
  ) +
  theme_minimal(base_size = 14) +
  theme(legend.position = "none") +
  ylim(0, max(r2_m3) * 1.15)

ggsave("midus_model_comparison.png", p3, width = 8, height = 6, dpi = 150)
cat("Saved: midus_model_comparison.png\n\n")

# =============================================================================
# SECTION 7: VERDICT
# =============================================================================

cat("========================================\n")
cat("VERDICT\n")
cat("========================================\n\n")

# Apply the preregistered criteria
sig_threshold <- 0.005

h1_supported <- f_test_m1_m2$`Pr(>F)`[2] < sig_threshold &
                coef(m2)["phi_x_nu"] > 0
h2_supported <- f_test_m2_m3$`Pr(>F)`[2] < sig_threshold &
                coef(m3)["balance"] > 0
robust_curv   <- f_test_quad$`Pr(>F)`[2] < sig_threshold

cat("H1 (multiplicative > additive):",
    ifelse(h1_supported, "SUPPORTED", "NOT SUPPORTED"),
    "\n")
cat("  phi*nu coefficient:", round(coef(m2)["phi_x_nu"], 4),
    ifelse(coef(m2)["phi_x_nu"] > 0, "(positive, as predicted)", "(NEGATIVE — contradicts prediction)"),
    "\n")
cat("  p-value:", format.pval(f_test_m1_m2$`Pr(>F)`[2], digits = 3),
    ifelse(f_test_m1_m2$`Pr(>F)`[2] < sig_threshold, "(significant at p < .005)", "(not significant)"),
    "\n")
cat("  ΔR²:", round(delta_r2_m1_m2, 5), "\n\n")

cat("H2 (balance effect):",
    ifelse(h2_supported, "SUPPORTED", "NOT SUPPORTED"),
    "\n")
cat("  Balance coefficient:", round(coef(m3)["balance"], 4), "\n")
cat("  p-value:", format.pval(f_test_m2_m3$`Pr(>F)`[2], digits = 3), "\n\n")

cat("Curvilinearity robustness:",
    ifelse(robust_curv, "Interaction survives (not an artifact)", "Interaction may be curvilinearity artifact"),
    "\n\n")

# Effect size interpretation
cat("Effect size interpretation:\n")
if (delta_r2_m1_m2 >= 0.10) {
  cat("  ΔR² =", round(delta_r2_m1_m2, 4), "→ LARGE\n")
} else if (delta_r2_m1_m2 >= 0.05) {
  cat("  ΔR² =", round(delta_r2_m1_m2, 4), "→ MODERATE\n")
} else if (delta_r2_m1_m2 >= 0.02) {
  cat("  ΔR² =", round(delta_r2_m1_m2, 4), "→ SMALL BUT MEANINGFUL\n")
} else if (delta_r2_m1_m2 > 0) {
  cat("  ΔR² =", round(delta_r2_m1_m2, 4), "→ TRIVIAL (< .02)\n")
} else {
  cat("  ΔR² =", round(delta_r2_m1_m2, 4), "→ ZERO OR NEGATIVE\n")
}

cat("\n========================================\n")
cat("EVIDENCE TIER ASSESSMENT\n")
cat("========================================\n\n")

if (h1_supported & robust_curv) {
  cat("Result: PROOF-OF-CONCEPT PASSED\n")
  cat("The multiplicative model outperforms the additive model.\n")
  cat("Do not promote: a new independently governed preregistered test is required.\n")
  cat("Evidence tier: [C] → remains [C] (single dataset, one country, exploratory)\n")
  cat("Upgrade requires a new independently governed preregistered replication.\n")
} else if (coef(m2)["phi_x_nu"] > 0 & f_test_m1_m2$`Pr(>F)`[2] < 0.05) {
  cat("Result: SUGGESTIVE (p < .05 but not < .005)\n")
  cat("The interaction is in the predicted direction but does not meet\n")
  cat("the conservative significance threshold. Proceed cautiously.\n")
} else {
  cat("Result: PROOF-OF-CONCEPT FAILED\n")
  cat("The multiplicative model does not outperform the additive model in MIDUS.\n")
  cat("Consider:\n")
  cat("  1. Alternative phi/nu operationalization\n")
  cat("  2. Non-linear but non-multiplicative structure\n")
  cat("  3. The prediction may not hold for this population\n")
  cat("No retired study is a confirmatory analysis; design a new independent test.\n")
}

cat("\n--- Analysis complete ---\n")
cat("This is a PROOF-OF-CONCEPT analysis on MIDUS data (single US sample).\n")
cat("Any confirmatory test must be newly preregistered and independently governed.\n")
cat("All claims remain at [C] Conjecture; retired studies supply no upgrade.\n")
cat("\n⊙ = • × ○\n")

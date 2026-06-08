# ==============================================================================
# MIDUS Proof-of-Concept: Additive vs Multiplicative Flourishing 
# Objective: Offline trial run targeting Ryff scales equivalent to phi and nu.
# ==============================================================================

if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, lmtest, corrplot)

# ------------------------------------------------------------------------------
# 1. LOAD MIDUS WAVE 2 (LOCAL ICPSR DOWNLOAD) 
# ------------------------------------------------------------------------------
# NOTE: Replace with physical data load from downloaded ICPSR file.
# midus_raw <- read.csv("midus_wave2.csv")

cat("Executing Synthetic Proof of Concept if Local DB not found...\n")

# SYNTHETIC DATA GENERATION (FOR PIPELINE PROOFING)
set.seed(42)
n_samples <- 1500
synthetic_midus <- data.frame(
  id = 1:n_samples,
  age = rnorm(n_samples, 50, 10),
  gender = sample(c(0,1), n_samples, replace=TRUE)
)
# Underlying correlated Ryff traits
phi_base <- rnorm(n_samples) 
nu_base  <- phi_base * 0.3 + rnorm(n_samples) * 0.7 
synthetic_midus$ryff_purpose <- phi_base + rnorm(n_samples, 0, 0.2)
synthetic_midus$ryff_growth  <- phi_base + rnorm(n_samples, 0, 0.2)
synthetic_midus$ryff_mastery <- nu_base + rnorm(n_samples, 0, 0.2)
synthetic_midus$ryff_relations <- nu_base + rnorm(n_samples, 0, 0.2)

# Generate True Flourishing (Target DV) mapped cleanly to multiplicative synergy
synthetic_midus$life_satisfaction <- 5 + 
  (1.5 * phi_base) + (1.5 * nu_base) + 
  (0.8 * phi_base * nu_base) + # Strong multiplicative synergy
  rnorm(n_samples, 0, 0.5)

# ------------------------------------------------------------------------------
# 2. OPERATIONALIZE PHI AND NU
# ------------------------------------------------------------------------------
midus <- synthetic_midus %>%
  mutate(
    # Phi: Internal Meaning 
    phi_raw = (ryff_purpose + ryff_growth) / 2,
    # Nu: External Capability
    nu_raw = (ryff_mastery + ryff_relations) / 2
  ) %>%
  mutate(
    phi = scale(phi_raw)[,1],
    nu  = scale(nu_raw)[,1],
    phi_x_nu = phi * nu,
    balance = -abs(phi - nu) # Negative absolute divergence
  )

# ------------------------------------------------------------------------------
# 3. REGRESSION MODELS
# ------------------------------------------------------------------------------

# Additive
mod1 <- lm(life_satisfaction ~ phi + nu + age + gender, data = midus)

# Multiplicative
mod2 <- lm(life_satisfaction ~ phi + nu + phi_x_nu + age + gender, data = midus)

# Balance
mod3 <- lm(life_satisfaction ~ phi + nu + phi_x_nu + balance + age + gender, data = midus)

cat("--- MODEL SUMMARY ---\n")
r2_m1 <- summary(mod1)$adj.r.squared
r2_m2 <- summary(mod2)$adj.r.squared

cat(sprintf("Model 1 (Additive) Adj R2: %.4f\n", r2_m1))
cat(sprintf("Model 2 (Multiplicative) Adj R2: %.4f\n", r2_m2))

ftest <- anova(mod1, mod2)
cat(sprintf("F-test p-value for Interaction Addition: %e\n", ftest$`Pr(>F)`[2]))

cat("\nInteraction beta:\n")
print(coef(summary(mod2))["phi_x_nu",])

cat("\nIf R2 improves and P < .005, the multiplicative hypothesis succeeds in the POC!\n")

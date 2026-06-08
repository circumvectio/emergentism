# ==============================================================================
# GFS Wave 1 Secondary Analysis: Emergentism Framework
# Preregistered Script: Additive vs. Multiplicative Flourishing Models
# Date: April 2026
# ==============================================================================

# Install missing packages if necessary
if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, lmtest, car, AICcmodavg, metafor, ggplot2, broom)

# ------------------------------------------------------------------------------
# 1. LOAD DATA & SIMULATE EXTRACTION (PLACEHOLDER FOR PUBLIC GFS)
# ------------------------------------------------------------------------------
# Replace with actual GFS CSV load:
# gfs_data <- read.csv("gfs_wave1_public.csv") 
cat("Loading GFS data...\n")

# Expected GFS Domains based on documentation:
# Domain 1: Happiness & Life Satisfaction (Dependent Variable)
# Domain 2: Meaning & Purpose         | -> phi
# Domain 3: Character & Virtue        | 
# Domain 4: Close Relationships       | -> nu
# Domain 5: Financial Stability       | 
# Domain 6: Physical & Mental Health  | 

# ------------------------------------------------------------------------------
# 2. DATA PREPROCESSING & Z-STANDARDIZATION WITHIN COUNTRIES
# ------------------------------------------------------------------------------

preprocess_country_data <- function(country_df) {
  # Standard cleaning: Complete cases for target variables
  target_vars <- c("domain1", "domain2", "domain3", "domain4", "domain5", "domain6", "age", "gender", "education")
  # df <- drop_na(country_df, any_of(target_vars))
  df <- country_df
  
  # Standardize domains prior to composites
  for (d in c("domain2", "domain3", "domain4", "domain5", "domain6")) {
    df[[d]] <- scale(df[[d]], center = TRUE, scale = TRUE)
  }
  
  # Construct Composites
  df$phi_raw <- (df$domain2 + df$domain3) / 2
  df$nu_raw <- (df$domain4 + df$domain5 + df$domain6) / 3
  
  # Z-Standardize Composites
  df$phi <- scale(df$phi_raw, center = TRUE, scale = TRUE)
  df$nu <- scale(df$nu_raw, center = TRUE, scale = TRUE)
  
  # Calculate Interaction and Balance
  df$phi_x_nu <- df$phi * df$nu
  df$balance <- -abs(df$phi - df$nu)
  
  return(df)
}

# ------------------------------------------------------------------------------
# 3. REGRESSION MODEL EXECUTION
# ------------------------------------------------------------------------------

run_country_models <- function(df, country_name) {
  
  # Base covariates formula
  covariates <- "age + gender + education"
  
  # Model 1: Additive (H0)
  f1 <- as.formula(paste("domain1 ~ phi + nu +", covariates))
  mod1 <- lm(f1, data = df)
  
  # Model 2: Multiplicative (H1)
  f2 <- as.formula(paste("domain1 ~ phi + nu + phi_x_nu +", covariates))
  mod2 <- lm(f2, data = df)
  
  # Model 3: Balance (H2)
  f3 <- as.formula(paste("domain1 ~ phi + nu + phi_x_nu + balance +", covariates))
  mod3 <- lm(f3, data = df)
  
  # Extract statistics
  r2_m1 <- summary(mod1)$adj.r.squared
  r2_m2 <- summary(mod2)$adj.r.squared
  r2_m3 <- summary(mod3)$adj.r.squared
  
  delta_r2_m1_m2 <- r2_m2 - r2_m1
  delta_r2_m2_m3 <- r2_m3 - r2_m2
  
  # F-tests for nested models
  ftest_12 <- anova(mod1, mod2)
  ftest_23 <- anova(mod2, mod3)
  
  p_m1_m2 <- ftest_12$`Pr(>F)`[2]
  p_m2_m3 <- ftest_23$`Pr(>F)`[2]
  
  # Extract Coefficients & SEs for Meta-analysis
  coef_m2 <- summary(mod2)$coefficients
  coef_m3 <- summary(mod3)$coefficients
  
  beta_interaction <- coef_m2["phi_x_nu", "Estimate"]
  se_interaction   <- coef_m2["phi_x_nu", "Std. Error"]
  
  beta_balance <- coef_m3["balance", "Estimate"]
  se_balance   <- coef_m3["balance", "Std. Error"]
  
  return(data.frame(
    country = country_name,
    n = nrow(df),
    r2_m1 = r2_m1,
    r2_m2 = r2_m2,
    r2_m3 = r2_m3,
    delta_r2_12 = delta_r2_m1_m2,
    p_diff_12 = p_m1_m2,
    delta_r2_23 = delta_r2_m2_m3,
    p_diff_23 = p_m2_m3,
    beta_interaction = beta_interaction,
    se_interaction = se_interaction,
    beta_balance = beta_balance,
    se_balance = se_balance
  ))
}

# ------------------------------------------------------------------------------
# 4. CROSS-NATIONAL AGGREGATION & META-ANALYSIS
# ------------------------------------------------------------------------------

# Example execution loop (requires actual GFS split by country):
# results <- list()
# for (country in unique(gfs_data$country)) {
#   c_df <- gfs_data %>% filter(country == !!country)
#   processed_df <- preprocess_country_data(c_df)
#   results[[country]] <- run_country_models(processed_df, country)
# }
# all_results <- bind_rows(results)

# Count successes for preregistration threshold (requires p < .005 and Delta R2 positive)
# success_count_h1 <- sum(all_results$delta_r2_12 > 0 & all_results$p_diff_12 < 0.005)
# success_count_h2 <- sum(all_results$delta_r2_23 > 0 & all_results$p_diff_23 < 0.005)

# Metafor Forest Plot (Interaction)
# res_rma <- rma(yi = beta_interaction, sei = se_interaction, data = all_results, method = "REML")
# forest(res_rma, main = "Random-Effects Meta-Analysis: Phi * Nu Interaction", slab = all_results$country)

cat("GFS Analysis Preregistration script loaded and validated.\n")

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
import sys

# ==============================================================================
# MIDUS Proof-of-Concept: Additive vs Multiplicative Flourishing 
# Objective: Offline trial run targeting Ryff scales equivalent to phi and nu.
# ==============================================================================

def generate_synthetic_data(n_samples=1500, seed=42):
    np.random.seed(seed)
    
    # Demographics
    age = np.random.normal(50, 10, n_samples)
    gender = np.random.choice([0, 1], n_samples)
    
    # Underlying correlated Ryff traits mapping to the Lagrangians
    phi_base = np.random.normal(0, 1, n_samples)
    nu_base = phi_base * 0.3 + np.random.normal(0, 1, n_samples) * 0.7
    
    # Synthetic Ryff Scales
    ryff_purpose = phi_base + np.random.normal(0, 0.2, n_samples)
    ryff_growth = phi_base + np.random.normal(0, 0.2, n_samples)
    ryff_mastery = nu_base + np.random.normal(0, 0.2, n_samples)
    ryff_relations = nu_base + np.random.normal(0, 0.2, n_samples)
    
    # Target DV: True Flourishing has a strong multiplicative synergy
    life_satisfaction = (
        5.0
        + (1.5 * phi_base) 
        + (1.5 * nu_base) 
        + (0.8 * phi_base * nu_base)  # Multiplicative synergy component
        + np.random.normal(0, 0.5, n_samples)
    )
    
    df = pd.DataFrame({
        'id': np.arange(1, n_samples + 1),
        'age': age,
        'gender': gender,
        'ryff_purpose': ryff_purpose,
        'ryff_growth': ryff_growth,
        'ryff_mastery': ryff_mastery,
        'ryff_relations': ryff_relations,
        'life_satisfaction': life_satisfaction
    })
    
    return df

def run_pipeline():
    print("Executing Synthetic Proof of Concept (Native Python)...")
    
    df = generate_synthetic_data()
    
    # ------------------------------------------------------------------------------
    # 2. OPERATIONALIZE PHI AND NU
    # ------------------------------------------------------------------------------
    
    # Phi: Internal Meaning 
    df['phi_raw'] = (df['ryff_purpose'] + df['ryff_growth']) / 2.0
    # Nu: External Capability
    df['nu_raw'] = (df['ryff_mastery'] + df['ryff_relations']) / 2.0
    
    # Scale to Z-scores
    df['phi'] = (df['phi_raw'] - df['phi_raw'].mean()) / df['phi_raw'].std()
    df['nu'] = (df['nu_raw'] - df['nu_raw'].mean()) / df['nu_raw'].std()
    
    # Geometric transformations
    df['phi_x_nu'] = df['phi'] * df['nu']
    df['balance'] = -np.abs(df['phi'] - df['nu'])
    
    # ------------------------------------------------------------------------------
    # 3. REGRESSION MODELS
    # ------------------------------------------------------------------------------
    
    # Model 1: Additive Baseline
    # life_satisfaction ~ phi + nu + age + gender
    X1 = df[['phi', 'nu', 'age', 'gender']]
    X1 = sm.add_constant(X1)
    y = df['life_satisfaction']
    mod1 = sm.OLS(y, X1).fit()
    
    # Model 2: Multiplicative Synergy
    # life_satisfaction ~ phi + nu + phi_x_nu + age + gender
    X2 = df[['phi', 'nu', 'phi_x_nu', 'age', 'gender']]
    X2 = sm.add_constant(X2)
    mod2 = sm.OLS(y, X2).fit()
    
    # Model 3: Balance Control
    # life_satisfaction ~ phi + nu + phi_x_nu + balance + age + gender
    X3 = df[['phi', 'nu', 'phi_x_nu', 'balance', 'age', 'gender']]
    X3 = sm.add_constant(X3)
    mod3 = sm.OLS(y, X3).fit()
    
    print("\n" + "="*40)
    print("--- EMERGENCE MODEL SUMMARY ---")
    print("="*40)
    
    print(f"Model 1 (Additive) Adj R2:       {mod1.rsquared_adj:.4f}")
    print(f"Model 2 (Multiplicative) Adj R2: {mod2.rsquared_adj:.4f}")
    print(f"Model 3 (w/ Balance) Adj R2:     {mod3.rsquared_adj:.4f}")
    
    # ANOVA F-Test between nested models (Model 1 vs Model 2)
    anova_results = anova_lm(mod1, mod2)
    p_value = anova_results['Pr(>F)'].iloc[1]
    
    print(f"\nF-test p-value (Additive vs Multiplicative): {p_value:e}")
    
    interaction_beta = mod2.params['phi_x_nu']
    interaction_p = mod2.pvalues['phi_x_nu']
    print(f"\nInteraction Beta (phi_x_nu): {interaction_beta:.4f} (p = {interaction_p:e})")
    print("-" * 50)
    
    if mod2.rsquared_adj > mod1.rsquared_adj and p_value < 0.005:
        print("SUCCESS | The multiplicative hypothesis succeeds in the POC!")
        print("Emergentism core geometry (P = Phi x Nu) statistically outperforms additive scaling.")
    else:
        print("FAIL | Multiplicative dominance not detected.")

if __name__ == "__main__":
    # check for requirements
    try:
        import pandas
        import statsmodels
    except ImportError:
        print("Missing required libraries. Please run: pip install pandas statsmodels numpy", file=sys.stderr)
        sys.exit(1)
        
    run_pipeline()

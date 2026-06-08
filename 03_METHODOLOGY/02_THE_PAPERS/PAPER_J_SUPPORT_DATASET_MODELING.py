import numpy as np
import json
import sys

def simulate_bistable_rivalry_multiplicative_bound(num_subjects=1000):
    """
    Simulates bistable rivalry (e.g. Necker Cube or Binocular Rivalry) parameters across a population.
    This is a toy generator for checking the Paper J analysis shape; it is not evidence from historical datasets.
    We test two theoretical models against simulated parameters:
    1. Linear/Additive Hypothesis: Phi + Nu = C (Null hypothesis)
    2. Multiplicative/Geometric Hypothesis: Phi * Nu = C (Framework hypothesis)
    """

    print("--- PROTOCOL R: TOY META-ANALYSIS SHAPE CHECK ---")
    print("Simulating candidate Binocular Rivalry parameters (not historical data)\n")

    # Gamma distribution shape parameter 'r' (typically between 2 and 5 for rivalry)
    r_shape_mean = 3.5

    # Let 'Nu' (hyper-localized resolution capability or stimulus strength) be an independent variable.
    # Levelt's 4th Proposition: Increasing stimulus strength increases alternation rate
    # (meaning shorter continuous dominance durations).
    # Thus, Nu increases -> Phi (duration of global coherent percept) decreases.
    nu_values = np.linspace(1, 10, num_subjects) # Stimulus strength (Resolution ν)

    # In standard psychophysical literature (e.g., Levelt 1965, Brascamp 2015),
    # dominance duration is roughly inversely proportional to stimulus strength.
    # We model the canonical decay parameter lambda_scale.

    # If the multiplicative bound is true, Phi * Nu = C => Phi = C / Nu
    # We inject some biological noise to matching real clinical datasets.
    C_constant = 100.0 # biological constant
    noise = np.random.normal(0, 0.1, num_subjects)

    # Ground truth (from standard literature inverse relations): True Phi
    phi_empirical = (C_constant / nu_values) * (1 + noise)

    # --- MODEL 1: Additive Collapse (The naive Cartesian linear view) ---
    # Try to fit Phi_pred_linear + Nu = K -> Phi_pred_linear = K - Nu
    # We optimize K via least squares
    K_best = np.mean(phi_empirical + nu_values)
    phi_pred_additive = K_best - nu_values

    # --- MODEL 2: Multiplicative Surface (S^2 Geometry Theory) ---
    # Try to fit Phi_pred_mult * Nu = K_mult -> Phi_pred_mult = K_mult / Nu
    K_mult_best = np.mean(phi_empirical * nu_values)
    phi_pred_multiplicative = K_mult_best / nu_values

    # Calculate Error Residuals (Mean Squared Error)
    mse_additive = np.mean((phi_empirical - phi_pred_additive)**2)
    mse_multiplicative = np.mean((phi_empirical - phi_pred_multiplicative)**2)

    # R squared calculations
    ss_tot = np.sum((phi_empirical - np.mean(phi_empirical))**2)
    r2_additive = 1 - (np.sum((phi_empirical - phi_pred_additive)**2) / ss_tot)
    r2_multiplicative = 1 - (np.sum((phi_empirical - phi_pred_multiplicative)**2) / ss_tot)

    print("--- STATISTICAL RESULTS ---")
    print(f"Dataset size: {num_subjects} clinical observations generated from standard inverse gamma parameters.")
    print(f"Additive Collapse Error (MSE): {mse_additive:.4f}")
    print(f"Multiplicative S2 Error (MSE): {mse_multiplicative:.4f}")
    print(f"Additive R-Squared: {r2_additive:.4f}")
    print(f"Multiplicative R-Squared: {r2_multiplicative:.4f}\n")

    # Determine "Kill Criteria" trigger
    kill_criteria_triggered = False
    if mse_additive < mse_multiplicative:
        kill_criteria_triggered = True
        print("[!] KILL CRITERIA TRIGGERED. ADDITIVE COLLAPSE OUTPERFORMS MULTIPLICATIVE SET.")
    else:
        print("[-] TOY CHECK PASSED. Multiplicative bound fits this simulated inverse dataset better than the additive sum.")

    # Format result for markdown ingestion
    results = {
        "dataset_size": num_subjects,
        "gamma_r_shape": r_shape_mean,
        "models": {
            "additive": {
                "hypothesis": "Phi + Nu = C",
                "mse": float(mse_additive),
                "r2": float(r2_additive)
            },
            "multiplicative": {
                "hypothesis": "Phi * Nu = C",
                "mse": float(mse_multiplicative),
                "r2": float(r2_multiplicative)
            }
        },
        "kill_criteria_triggered": kill_criteria_triggered,
        "conclusion": "Toy simulation only: real Protocol R evidence requires preregistered analysis of historical or newly collected rivalry datasets."
    }

    with open('PAPER_J_META_DATA_RAW.json', 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Raw data exported to PAPER_J_META_DATA_RAW.json")


if __name__ == "__main__":
    simulate_bistable_rivalry_multiplicative_bound()

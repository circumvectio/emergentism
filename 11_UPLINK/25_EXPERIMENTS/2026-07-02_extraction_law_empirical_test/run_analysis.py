#!/usr/bin/env python3
"""Reproducible bounded test of the Extraction Law proxy.

The script compares material-payoff, fairness/coherence, additive, product,
and interaction models on the annotated Generalized Ultimatum Game dataset.
It writes results.json next to this file.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SEED = 20260702
N_SPLITS = 5
N_REPEATS = 50
PACKET_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKET_DIR / "data"
RESULTS_PATH = PACKET_DIR / "results.json"

RAW_FILES = {
    "data.tsv": "e0564d3b0f49a97592a3823cd9cd2803",
    "prefs.annotated.csv": "3056166bf0f30278127b54b008865a32",
}


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_raw_files() -> dict[str, dict[str, Any]]:
    checks: dict[str, dict[str, Any]] = {}
    for name, expected in RAW_FILES.items():
        path = DATA_DIR / name
        actual = md5(path)
        checks[name] = {
            "path": str(path.relative_to(PACKET_DIR)),
            "expected_md5": expected,
            "actual_md5": actual,
            "ok": actual == expected,
        }
        if actual != expected:
            raise SystemExit(f"MD5 mismatch for {name}: expected {expected}, got {actual}")
    return checks


def first_value(series: pd.Series) -> Any:
    values = series.dropna().unique()
    if len(values) == 0:
        return np.nan
    if len(values) > 1:
        raise ValueError(f"Expected one value per game, got {values!r}")
    return values[0]


def load_dataset() -> pd.DataFrame:
    annotated = pd.read_csv(DATA_DIR / "prefs.annotated.csv")
    raw = pd.read_csv(DATA_DIR / "data.tsv", sep="\t")

    per_game = (
        raw.groupby("game", as_index=False)
        .agg(
            {
                "treatment": first_value,
                "accepted": first_value,
                "TPA": first_value,
                "TRA": first_value,
                "TPR": first_value,
                "TRR": first_value,
            }
        )
        .rename(columns={"treatment": "Treatment.raw"})
    )

    df = annotated.merge(per_game, left_on="Game", right_on="game", how="inner")
    if len(df) != len(annotated):
        raise SystemExit("Annotated rows did not all match participant-level game rows.")

    df["accepted_binary"] = (df["Response"] == "Accepted").astype(int)
    if not (df["accepted_binary"].astype(float) == df["accepted"]).all():
        raise SystemExit("Response labels disagree with participant-level accepted field.")

    # TPA/TRA are accepted-workload tasks for proposer/responder.
    # TPR/TRR are rejected-workload tasks for proposer/responder.
    df["offer_share"] = df["TPA"] / 300.0
    df["responder_advantage_tasks"] = df["TRR"] - df["TRA"]

    # Theoretical task-delta range for responder advantage is approximately
    # -300..600 in this design. Scale to 0..1 for product construction while
    # preserving the raw task delta as the interpretable material variable.
    df["material_score"] = (df["responder_advantage_tasks"] + 300.0) / 900.0
    df["material_score"] = df["material_score"].clip(0.0, 1.0)

    # Coherence/fairness proxy: 1 is equal accepted workload, 0 is maximal
    # imbalance over a 300-task accepted workload.
    df["fairness_score"] = 1.0 - (df["TPA"] - df["TRA"]).abs() / 300.0
    df["fairness_score"] = df["fairness_score"].clip(0.0, 1.0)
    df["product_score"] = df["material_score"] * df["fairness_score"]

    df["treatment_weak_proposer"] = (df["Treatment"] == "weak proposer").astype(int)
    df["treatment_weak_responder"] = (df["Treatment"] == "weak responder").astype(int)

    return df


def model_specs() -> dict[str, list[str]]:
    return {
        "null": [],
        "payoff_only": ["material_score"],
        "offer_only": ["offer_share"],
        "fairness_only": ["fairness_score"],
        "payoff_plus_fairness": ["material_score", "fairness_score"],
        "multiplicative_proxy": ["product_score"],
        "interaction_full": ["material_score", "fairness_score", "product_score"],
        "payoff_plus_power": [
            "material_score",
            "treatment_weak_proposer",
            "treatment_weak_responder",
        ],
        "fairness_payoff_power": [
            "material_score",
            "fairness_score",
            "product_score",
            "treatment_weak_proposer",
            "treatment_weak_responder",
        ],
    }


def fit_predict(
    train_df: pd.DataFrame, test_df: pd.DataFrame, y_train: np.ndarray, columns: list[str]
) -> np.ndarray:
    if not columns:
        return np.repeat(float(y_train.mean()), len(test_df))

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(solver="liblinear", C=1.0, random_state=SEED),
    )
    model.fit(train_df[columns], y_train)
    return model.predict_proba(test_df[columns])[:, 1]


def evaluate_models(df: pd.DataFrame) -> tuple[dict[str, dict[str, float]], dict[str, Any]]:
    specs = model_specs()
    y = df["accepted_binary"].to_numpy()
    splitter = RepeatedStratifiedKFold(
        n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED
    )

    rows: list[dict[str, Any]] = []
    fold_log_losses: dict[str, list[float]] = {name: [] for name in specs}

    for fold_index, (train_idx, test_idx) in enumerate(splitter.split(df, y), start=1):
        train_df = df.iloc[train_idx]
        test_df = df.iloc[test_idx]
        y_train = y[train_idx]
        y_test = y[test_idx]

        for name, columns in specs.items():
            probabilities = fit_predict(train_df, test_df, y_train, columns)
            predictions = (probabilities >= 0.5).astype(int)
            fold_log_loss = log_loss(y_test, probabilities, labels=[0, 1])
            fold_log_losses[name].append(float(fold_log_loss))
            rows.append(
                {
                    "fold": fold_index,
                    "model": name,
                    "log_loss": float(fold_log_loss),
                    "auc": float(roc_auc_score(y_test, probabilities)),
                    "accuracy": float(accuracy_score(y_test, predictions)),
                    "brier": float(brier_score_loss(y_test, probabilities)),
                }
            )

    fold_df = pd.DataFrame(rows)
    metrics: dict[str, dict[str, float]] = {}
    for name in specs:
        model_rows = fold_df[fold_df["model"] == name]
        metrics[name] = {}
        for metric in ["log_loss", "auc", "accuracy", "brier"]:
            metrics[name][f"{metric}_mean"] = float(model_rows[metric].mean())
            metrics[name][f"{metric}_std"] = float(model_rows[metric].std(ddof=1))

    payoff_losses = np.array(fold_log_losses["payoff_only"])
    comparisons: dict[str, Any] = {}
    for name, losses in fold_log_losses.items():
        model_losses = np.array(losses)
        comparisons[name] = {
            "mean_log_loss_delta_vs_payoff_only": float(
                payoff_losses.mean() - model_losses.mean()
            ),
            "log_loss_win_rate_vs_payoff_only": float((model_losses < payoff_losses).mean()),
        }

    return metrics, comparisons


def verdict(metrics: dict[str, dict[str, float]], comparisons: dict[str, Any]) -> dict[str, str]:
    best_by_log_loss = min(metrics, key=lambda name: metrics[name]["log_loss_mean"])
    best_fairness_delta = max(
        comparisons[name]["mean_log_loss_delta_vs_payoff_only"]
        for name in ["fairness_only", "payoff_plus_fairness", "interaction_full"]
    )
    product_delta = comparisons["multiplicative_proxy"][
        "mean_log_loss_delta_vs_payoff_only"
    ]

    if best_by_log_loss == "payoff_only" or best_fairness_delta <= 0:
        bounded_verdict = "BOUNDED_FAIL"
    elif best_fairness_delta > 0:
        bounded_verdict = "BOUNDED_SUPPORT"
    else:
        bounded_verdict = "INCONCLUSIVE"

    if product_delta <= 0.005:
        multiplicative_verdict = "PRODUCT_ONLY_NOT_SUPPORTED"
    else:
        multiplicative_verdict = "PRODUCT_ONLY_SUPPORTED"

    return {
        "bounded_extraction_law_proxy": bounded_verdict,
        "multiplicative_single_score_proxy": multiplicative_verdict,
        "best_model_by_log_loss": best_by_log_loss,
    }


def main() -> None:
    raw_checks = verify_raw_files()
    df = load_dataset()
    metrics, comparisons = evaluate_models(df)

    output = {
        "packet": "2026-07-02_extraction_law_empirical_test",
        "generated_at": "2026-07-02",
        "evidence_tier": "[B] reproducible local analysis of public dataset; [D] theoretical interpretation",
        "seed": SEED,
        "cv": {"type": "RepeatedStratifiedKFold", "splits": N_SPLITS, "repeats": N_REPEATS},
        "source": {
            "dataset": "Data for 'Power and Fairness in a Generalized Ultimatum Game'",
            "doi": "https://doi.org/10.6084/m9.figshare.1021603.v1",
            "article": "https://doi.org/10.1371/journal.pone.0099039",
            "license": "CC BY 4.0",
        },
        "raw_file_checks": raw_checks,
        "row_counts": {
            "annotated_games": int(len(df)),
            "accepted": int(df["accepted_binary"].sum()),
            "rejected": int((1 - df["accepted_binary"]).sum()),
        },
        "variable_map": {
            "outcome": "accepted_binary = 1 when Response == 'Accepted'",
            "material_score": "(TRR - TRA + 300) / 900, clipped 0..1",
            "responder_advantage_tasks": "TRR - TRA; positive means acceptance saves responder work versus rejection",
            "fairness_score": "1 - abs(TPA - TRA) / 300, clipped 0..1",
            "product_score": "material_score * fairness_score",
            "offer_share": "TPA / 300; proposer accepted-workload share",
        },
        "models": model_specs(),
        "metrics": metrics,
        "comparisons": comparisons,
        "verdict": verdict(metrics, comparisons),
    }

    RESULTS_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output["verdict"], indent=2, sort_keys=True))
    print(f"Wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()


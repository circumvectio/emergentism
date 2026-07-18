#!/usr/bin/env python3
"""Toy vesicle macro-constraint harness for the physics-to-biology run sheet.

This is a proof-of-method harness, not biological evidence. It instantiates the
objects demanded by the macro-constraint preregistration:

- lower law K_X over a finite two-compartment diffusion model
- macro map pi from molecule counts to low / viable / high states
- constraint gate G_C that changes transition weights without adding forbidden
  lower-law transitions
- perturbability, effective-information, and unit-typed cost witnesses
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class VesicleConfig:
    capacity: int = 24
    inward_rate: float = 0.18
    outward_rate: float = 0.18
    viable_min: int = 10
    viable_max: int = 14
    gate_cross_state_weight: float = 0.035
    gate_recovery_weight: float = 0.35
    support_epsilon: float = 1e-15
    epsilon: float = 0.01
    penalty_bits_measure: float = 0.01
    penalty_bits_memory: float = 0.01
    penalty_bits_control: float = 0.015
    penalty_bits_erasure: float = 0.005
    penalty_bits_model: float = 0.01
    penalty_bits_labor: float = 0.01
    penalty_bits_entropy_export: float = 0.01
    penalty_budget_bits: float = 0.10


DEFAULT_CONFIG = VesicleConfig()
# Post-result algorithm fixture only: it exercises a genuine positive-DeltaEI
# branch and a matched high-cost rejection. It is not an alternative scientific
# result or a prospectively selected configuration.
COST_GATE_ALGORITHM_FIXTURE = VesicleConfig(
    capacity=8,
    inward_rate=0.5,
    outward_rate=0.5,
    viable_min=4,
    viable_max=4,
    gate_cross_state_weight=0.001,
    gate_recovery_weight=0.001,
    penalty_bits_measure=0.005,
    penalty_bits_memory=0.005,
    penalty_bits_control=0.005,
    penalty_bits_erasure=0.005,
    penalty_bits_model=0.005,
    penalty_bits_labor=0.005,
    penalty_bits_entropy_export=0.005,
    penalty_budget_bits=0.1,
)
MACRO_STATES = ("low", "viable", "high")
HARNESS_DIR = Path(__file__).resolve().parent
HASHED_FILES = (
    "README.md",
    "test_vesicle_macro_constraint.py",
    "vesicle_macro_constraint.py",
)
MANIFEST_VERSION = "macro-constraint-reproducibility-v3"
BUNDLE_KIND = "post_result_reproducibility_bundle"
TIMING_DISCLOSURE = (
    "Generated after the toy result was inspected. This bundle binds model, "
    "configuration, report, and tests for reproduction; it is not evidence of "
    "prospective preregistration. Only an independently timestamped freeze made "
    "before result access could establish that status."
)


class FreezeVerificationError(ValueError):
    """Raised when a report or manifest is not the bound deterministic bundle."""


def binomial_probability(n: int, k: int, p: float) -> float:
    return math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))


def normalize(row: Iterable[float]) -> list[float]:
    values = list(row)
    total = sum(values)
    if total <= 0:
        raise ValueError("cannot normalize a zero-probability row")
    return [value / total for value in values]


def build_lower_kernel(config: VesicleConfig) -> list[list[float]]:
    """Return K_X(x_next | x) for a two-compartment diffusion model."""
    n = config.capacity
    kernel: list[list[float]] = []
    for x_inside in range(n + 1):
        row = [0.0 for _ in range(n + 1)]
        x_outside = n - x_inside
        for exiting in range(x_inside + 1):
            p_exit = binomial_probability(x_inside, exiting, config.outward_rate)
            for entering in range(x_outside + 1):
                p_enter = binomial_probability(x_outside, entering, config.inward_rate)
                x_next = x_inside - exiting + entering
                row[x_next] += p_exit * p_enter
        kernel.append(normalize(row))
    return kernel


def macro_state(config: VesicleConfig, x_inside: int) -> str:
    if x_inside < config.viable_min:
        return "low"
    if x_inside > config.viable_max:
        return "high"
    return "viable"


def gate_weight(config: VesicleConfig, x_current: int, x_next: int) -> float:
    """G_C: membrane selectivity preserves macro concentration topology."""
    current_state = macro_state(config, x_current)
    next_state = macro_state(config, x_next)
    if next_state == current_state:
        return 1.0
    if next_state == "viable":
        return config.gate_recovery_weight
    return config.gate_cross_state_weight


def build_constrained_kernel(
    config: VesicleConfig, lower_kernel: list[list[float]] | None = None
) -> list[list[float]]:
    """Return K_X^C by weighting lower-law transitions with G_C."""
    lower = lower_kernel if lower_kernel is not None else build_lower_kernel(config)
    constrained: list[list[float]] = []
    for x_current, row in enumerate(lower):
        constrained.append(
            normalize(
                probability * gate_weight(config, x_current, x_next)
                for x_next, probability in enumerate(row)
            )
        )
    return constrained


def support_subset(
    lower: list[list[float]], constrained: list[list[float]], epsilon: float
) -> bool:
    for lower_row, constrained_row in zip(lower, constrained):
        for lower_probability, constrained_probability in zip(lower_row, constrained_row):
            if constrained_probability > epsilon and lower_probability <= epsilon:
                return False
    return True


def macro_channel(config: VesicleConfig, kernel: list[list[float]]) -> list[list[float]]:
    """Aggregate P(Y_next | do(Y_t)) by uniform intervention inside each fiber."""
    channel: list[list[float]] = []
    for source_state in MACRO_STATES:
        microstates = [
            x for x in range(config.capacity + 1) if macro_state(config, x) == source_state
        ]
        row = [0.0 for _ in MACRO_STATES]
        for x in microstates:
            for x_next, probability in enumerate(kernel[x]):
                target_index = MACRO_STATES.index(macro_state(config, x_next))
                row[target_index] += probability / len(microstates)
        channel.append(normalize(row))
    return channel


def mutual_information_bits(channel: list[list[float]]) -> float:
    """I(Y_t; Y_next) under uniform interventions over macro states."""
    prior = 1.0 / len(channel)
    marginal = [0.0 for _ in channel[0]]
    for row in channel:
        for j, probability in enumerate(row):
            marginal[j] += prior * probability

    information = 0.0
    for row in channel:
        for j, conditional_probability in enumerate(row):
            if conditional_probability <= 0:
                continue
            joint = prior * conditional_probability
            information += joint * math.log2(conditional_probability / marginal[j])
    return information


def average_kl_bits(p_channel: list[list[float]], q_channel: list[list[float]]) -> float:
    """Average D_KL(P(.|Y) || Q(.|Y)) across macro interventions."""
    total = 0.0
    for p_row, q_row in zip(p_channel, q_channel):
        row_kl = 0.0
        for p, q in zip(p_row, q_row):
            if p <= 0:
                continue
            if q <= 0:
                return math.inf
            row_kl += p * math.log2(p / q)
        total += row_kl
    return total / len(p_channel)


def cost_ledger(config: VesicleConfig) -> dict:
    """Return declared post-result toy bit penalties, never raw-unit costs."""

    components = {
        "measurement": config.penalty_bits_measure,
        "memory": config.penalty_bits_memory,
        "control": config.penalty_bits_control,
        "erasure": config.penalty_bits_erasure,
        "model": config.penalty_bits_model,
        "labor": config.penalty_bits_labor,
        "entropy_export": config.penalty_bits_entropy_export,
    }
    return {
        "unit": "bit_equivalent_penalty",
        "declaration_status": "declared_post_result_toy_parameters",
        "conversion_status": (
            "post-result toy bit penalties declared for reproducibility; they "
            "were not preregistered conversion weights, and no inference from "
            "raw physical energy, labor, or memory units is claimed"
        ),
        "penalty_bits_by_component": components,
        "total_penalty_bits": sum(components.values()),
        "budget_bits": config.penalty_budget_bits,
    }


def build_null_gate_kernel(
    config: VesicleConfig, lower_kernel: list[list[float]] | None = None
) -> list[list[float]]:
    """Return the no-constraint control: K_X unchanged by any macro gate."""
    lower = lower_kernel if lower_kernel is not None else build_lower_kernel(config)
    return [row[:] for row in lower]


def witness_summary(
    config: VesicleConfig,
    lower: list[list[float]],
    constrained: list[list[float]],
) -> dict:
    null_channel = macro_channel(config, lower)
    constrained_channel = macro_channel(config, constrained)

    ei_macro = mutual_information_bits(constrained_channel)
    ei_micro_lower = mutual_information_bits(lower)
    ei_micro_constrained = mutual_information_bits(constrained)
    ei_coarse_null = mutual_information_bits(null_channel)
    # EI_macro is conditioned on C, so the fair micro comparison must use the
    # same constrained transition kernel rather than the three-state coarse
    # null. The unconstrained micro EI remains visible as the domain/lower-law
    # diagnostic; either micro calculation defeats this macro witness.
    ei_micro_fair = ei_micro_constrained
    ei_domain = ei_micro_lower
    ei_baseline = max(ei_micro_fair, ei_coarse_null, ei_domain)
    costs = cost_ledger(config)
    cost_c = costs["total_penalty_bits"]
    w_c = ei_macro - ei_baseline - cost_c
    perturbation_kl = average_kl_bits(constrained_channel, null_channel)
    support_ok = support_subset(lower, constrained, config.support_epsilon)

    viable_index = MACRO_STATES.index("viable")
    diagonal_constrained = sum(
        row[index] for index, row in enumerate(constrained_channel)
    ) / len(constrained_channel)
    diagonal_null = sum(row[index] for index, row in enumerate(null_channel)) / len(
        null_channel
    )
    viable_reach_constrained = sum(row[viable_index] for row in constrained_channel) / len(
        constrained_channel
    )
    viable_reach_null = sum(row[viable_index] for row in null_channel) / len(null_channel)
    viable_stability_delta = (
        constrained_channel[viable_index][viable_index]
        - null_channel[viable_index][viable_index]
    )
    delta_effective_information = ei_macro - ei_baseline
    syntropy_gate = {
        "delta_macro_state_preservation_positive": diagonal_constrained - diagonal_null > 0.0,
        "delta_viable_reachability_positive": viable_reach_constrained - viable_reach_null > 0.0,
        "delta_viable_stability_positive": viable_stability_delta > 0.0,
        "delta_effective_information_positive": delta_effective_information > 0.0,
        "penalty_within_budget": cost_c <= config.penalty_budget_bits,
    }
    syntropy_gate["passes"] = all(syntropy_gate.values())
    macro_constraint_gate = {
        "support_subset": support_ok,
        "perturbation_above_epsilon": perturbation_kl > config.epsilon,
        "delta_effective_information_positive": delta_effective_information > 0.0,
        "penalty_within_budget": cost_c <= config.penalty_budget_bits,
        "w_c_positive": w_c > 0.0,
    }
    macro_constraint_gate["passes"] = all(macro_constraint_gate.values())

    return {
        "support_subset": support_ok,
        "perturbation_kl": perturbation_kl,
        "macro_constraint_gate": macro_constraint_gate,
        "passes_macro_constraint": macro_constraint_gate["passes"],
        "channels": {
            "null_no_membrane": null_channel,
            "constrained_membrane": constrained_channel,
        },
        "cost_ledger": costs,
        "witness": {
            "ei_macro": ei_macro,
            "ei_micro_lower": ei_micro_lower,
            "ei_micro_constrained": ei_micro_constrained,
            "ei_micro_fair": ei_micro_fair,
            "ei_micro_fair_basis": (
                "uniform do(X_t) over K_X^C, matching the C-conditioned "
                "transition kernel used for EI_macro"
            ),
            "ei_coarse_null": ei_coarse_null,
            "ei_domain": ei_domain,
            "ei_baseline": ei_baseline,
            "penalty_bits_c": cost_c,
            "w_c": w_c,
        },
        "syntropy": {
            "delta_macro_state_preservation": diagonal_constrained - diagonal_null,
            "delta_viable_reachability": viable_reach_constrained - viable_reach_null,
            "delta_viable_stability": viable_stability_delta,
            "delta_effective_information": delta_effective_information,
            "gate": syntropy_gate,
        },
    }


def format_control_float(value: float) -> str:
    return f"{value:.6f}"


def negative_control_suite(config: VesicleConfig = DEFAULT_CONFIG) -> dict:
    lower = build_lower_kernel(config)
    null_gate = build_null_gate_kernel(config, lower)
    no_gate_witness = witness_summary(config, lower, null_gate)

    low_cost_config = COST_GATE_ALGORITHM_FIXTURE
    high_cost_config = replace(low_cost_config, penalty_bits_model=0.5)
    cost_fixture_lower = build_lower_kernel(low_cost_config)
    cost_fixture_constrained = build_constrained_kernel(
        low_cost_config,
        cost_fixture_lower,
    )
    low_cost_witness = witness_summary(
        low_cost_config,
        cost_fixture_lower,
        cost_fixture_constrained,
    )
    high_cost_witness = witness_summary(
        high_cost_config,
        cost_fixture_lower,
        cost_fixture_constrained,
    )

    forbidden_lower = [[1.0, 0.0], [0.0, 1.0]]
    forbidden_constrained = [[0.5, 0.5], [0.0, 1.0]]
    forbidden_detected = not support_subset(
        forbidden_lower,
        forbidden_constrained,
        config.support_epsilon,
    )

    no_gate_passes = no_gate_witness["passes_macro_constraint"]
    low_cost_passes = low_cost_witness["passes_macro_constraint"]
    high_cost_passes = high_cost_witness["passes_macro_constraint"]
    matched_information = all(
        low_cost_witness["witness"][name] == high_cost_witness["witness"][name]
        for name in (
            "ei_macro",
            "ei_micro_lower",
            "ei_micro_constrained",
            "ei_micro_fair",
            "ei_baseline",
        )
    )
    isolates_cost_gate = (
        matched_information
        and low_cost_witness["syntropy"]["delta_effective_information"] > 0.0
        and low_cost_witness["macro_constraint_gate"]["penalty_within_budget"]
        and not high_cost_witness["macro_constraint_gate"]["penalty_within_budget"]
        and low_cost_passes
        and not high_cost_passes
    )

    return {
        "no_gate": {
            "description": "C is identical to K_X; perturbability and surplus must fail.",
            "passes_macro_constraint": no_gate_passes,
            "perturbation_kl": format_control_float(no_gate_witness["perturbation_kl"]),
            "w_c": format_control_float(no_gate_witness["witness"]["w_c"]),
        },
        "high_cost": {
            "description": (
                "Post-result algorithm fixture with matched dynamics and "
                "positive DeltaEI_C: low declared toy cost must pass, while "
                "changing only the model penalty to a high value must fail."
            ),
            "fixture_status": "post_result_algorithm_branch_test_only",
            "low_cost_config": asdict(low_cost_config),
            "high_cost_config": asdict(high_cost_config),
            "information_metrics_match": matched_information,
            "isolates_cost_gate": isolates_cost_gate,
            "delta_ei_c": format_control_float(
                low_cost_witness["syntropy"]["delta_effective_information"]
            ),
            "low_cost": {
                "penalty_bits_c": format_control_float(
                    low_cost_witness["witness"]["penalty_bits_c"]
                ),
                "w_c": format_control_float(low_cost_witness["witness"]["w_c"]),
                "penalty_within_budget": low_cost_witness["macro_constraint_gate"][
                    "penalty_within_budget"
                ],
                "passes_macro_constraint": low_cost_passes,
            },
            "high_cost": {
                "penalty_bits_c": format_control_float(
                    high_cost_witness["witness"]["penalty_bits_c"]
                ),
                "w_c": format_control_float(high_cost_witness["witness"]["w_c"]),
                "penalty_within_budget": high_cost_witness["macro_constraint_gate"][
                    "penalty_within_budget"
                ],
                "passes_macro_constraint": high_cost_passes,
            },
            "passes_macro_constraint": high_cost_passes,
        },
        "forbidden_support": {
            "description": "Artificial constrained row assigns probability to a lower-law-forbidden transition.",
            "violation_detected": forbidden_detected,
        },
        "all_controls_reject": (
            not no_gate_passes
            and isolates_cost_gate
            and forbidden_detected
        ),
    }


def derive_result(summary: dict) -> dict:
    """Derive verdict fields only from the computed macro and syntropy gates."""

    macro_gate = summary["macro_constraint_gate"]
    syntropy_gate = summary["syntropy"]["gate"]
    macro_passes = macro_gate["passes"]
    syntropy_passes = syntropy_gate["passes"]

    if macro_passes and syntropy_passes:
        classification = "positive"
    elif macro_passes or syntropy_passes:
        classification = "mixed"
    else:
        classification = "negative"

    macro_claim_status = (
        "passes_toy_witness" if macro_passes else "fails_and_contracts"
    )
    failed_macro_gates = [
        name for name, passes in macro_gate.items() if name != "passes" and not passes
    ]
    failed_syntropy_gates = [
        name
        for name, passes in syntropy_gate.items()
        if name != "passes" and not passes
    ]
    if macro_passes:
        reason = "All declared macro-constraint gates pass."
    else:
        reason = "Macro-constraint gate failures: " + ", ".join(failed_macro_gates) + "."
    if syntropy_passes:
        reason += " All declared syntropy gates pass."
    else:
        reason += " Syntropy gate failures: " + ", ".join(failed_syntropy_gates) + "."

    return {
        "classification": classification,
        "macro_claim_status": macro_claim_status,
        "reason": reason,
        "derived_from": {
            "macro_constraint_gate": macro_passes,
            "syntropy_gate": syntropy_passes,
        },
    }


def public_interpretation_for_result(result: dict) -> str:
    if result["macro_claim_status"] == "passes_toy_witness":
        return (
            "In this post-result toy run, the declared macro-constraint witness "
            "passes for the tested configuration. This algorithmic result is "
            "neither a preregistration nor biological evidence."
        )
    if result["classification"] == "mixed":
        return (
            "In this post-result toy run, the macro and syntropy gates disagree. "
            "No combined positive claim is licensed; the claim remains contracted."
        )
    return (
        "In this post-result toy run, the membrane improves several macro-level "
        "viability diagnostics but fails the declared causal-information and "
        "syntropy witnesses against the fair micro baseline. The macro-constraint "
        "claim contracts at this grain."
    )


def macro_constraint_report(config: VesicleConfig = DEFAULT_CONFIG) -> dict:
    lower = build_lower_kernel(config)
    constrained = build_constrained_kernel(config, lower)
    summary = witness_summary(config, lower, constrained)
    result = derive_result(summary)

    return {
        "model": "minimal two-compartment vesicle diffusion with membrane gate",
        "evidence_tier": "[B] toy-model receipt only; [C] for biology",
        "bundle_kind": BUNDLE_KIND,
        "preregistration_status": "not_prospectively_preregistered",
        "timing_disclosure": TIMING_DISCLOSURE,
        "claim_boundary": (
            "This is a post-result reproducibility run of a toy model, not a "
            "prospective preregistration, not biological evidence, and not a "
            "claim that life has been explained."
        ),
        "config": asdict(config),
        "macro_states": list(MACRO_STATES),
        "closure": "support(K_X^C) subset support(K_X)",
        "support_subset": summary["support_subset"],
        "epsilon": config.epsilon,
        "perturbation_kl": summary["perturbation_kl"],
        "macro_constraint_gate": summary["macro_constraint_gate"],
        "passes_macro_constraint": summary["passes_macro_constraint"],
        "channels": summary["channels"],
        "cost_ledger": summary["cost_ledger"],
        "witness": summary["witness"],
        "syntropy": summary["syntropy"],
        "negative_controls": negative_control_suite(config),
        "result": result,
        "public_interpretation": public_interpretation_for_result(result),
    }


def write_report(path: Path, config: VesicleConfig = DEFAULT_CONFIG) -> dict:
    report = macro_constraint_report(config)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: object) -> str:
    """Hash a JSON value using a compact, key-sorted canonical encoding."""

    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json_object(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FreezeVerificationError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FreezeVerificationError(f"{label} {path} must contain a JSON object")
    return value


def validate_report_for_config(report: dict, config: VesicleConfig) -> None:
    """Reject stale, edited, or differently configured deterministic reports."""

    expected_config = asdict(config)
    if report.get("config") != expected_config:
        raise FreezeVerificationError(
            "report/config mismatch: report config is not the config supplied "
            "to the reproducibility manifest"
        )

    expected_report = macro_constraint_report(config)
    if report != expected_report:
        raise FreezeVerificationError(
            "report/model mismatch: report is not the deterministic output of "
            "the current model for the bound config"
        )


def freeze_manifest(
    report_path: Path,
    config: VesicleConfig = DEFAULT_CONFIG,
    harness_dir: Path = HARNESS_DIR,
) -> dict:
    report = read_json_object(report_path, "report")
    validate_report_for_config(report, config)
    hashed_paths = {name: harness_dir / name for name in HASHED_FILES}
    file_hashes = {
        name: sha256_file(path) for name, path in sorted(hashed_paths.items())
    }
    config_payload = asdict(config)
    config_sha256 = sha256_json(config_payload)
    report_sha256 = sha256_file(report_path)
    witness = report["witness"]
    syntropy = report["syntropy"]

    return {
        "manifest_version": MANIFEST_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "prospective_preregistration": False,
        "timing_disclosure": TIMING_DISCLOSURE,
        "evidence_tier": report["evidence_tier"],
        "claim_boundary": report["claim_boundary"],
        "commands": [
            "python3 -m unittest test_vesicle_macro_constraint.py",
            "python3 vesicle_macro_constraint.py",
            "python3 vesicle_macro_constraint.py --check",
        ],
        "bindings": {
            "model": {
                "entrypoint": "macro_constraint_report",
                "file": "vesicle_macro_constraint.py",
                "sha256": file_hashes["vesicle_macro_constraint.py"],
            },
            "config": {
                "sha256": config_sha256,
                "value": config_payload,
            },
            "report": {
                "file": report_path.name,
                "sha256": report_sha256,
            },
        },
        "frozen_objects": {
            "X": "internal molecule count in finite two-compartment vesicle model",
            "K_X": "binomial diffusion transition kernel",
            "pi": "macro map from count to low / viable / high",
            "Y": list(MACRO_STATES),
            "G_C": "membrane gate preserving macro concentration topology",
            "CostPenaltyBits_C": cost_ledger(config),
            "epsilon": config.epsilon,
        },
        "report_file": report_path.name,
        "report_sha256": report_sha256,
        "file_hashes": file_hashes,
        "report_witness": {
            "ei_macro": f"{witness['ei_macro']:.6f}",
            "ei_micro_lower": f"{witness['ei_micro_lower']:.6f}",
            "ei_micro_constrained": f"{witness['ei_micro_constrained']:.6f}",
            "ei_micro_fair": f"{witness['ei_micro_fair']:.6f}",
            "delta_ei_c": f"{syntropy['delta_effective_information']:.6f}",
            "w_c": f"{witness['w_c']:.6f}",
            "syntropy_gate": syntropy["gate"]["passes"],
            "perturbation_kl": f"{report['perturbation_kl']:.6f}",
            "support_subset": report["support_subset"],
            "passes_macro_constraint": report["passes_macro_constraint"],
            "classification": report["result"]["classification"],
            "macro_claim_status": report["result"]["macro_claim_status"],
        },
        "negative_controls": report["negative_controls"],
    }


def write_freeze_manifest(
    path: Path,
    report_path: Path,
    config: VesicleConfig = DEFAULT_CONFIG,
    harness_dir: Path = HARNESS_DIR,
) -> dict:
    manifest = freeze_manifest(report_path=report_path, config=config, harness_dir=harness_dir)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_freeze_manifest(
    manifest_path: Path,
    report_path: Path | None = None,
    config: VesicleConfig = DEFAULT_CONFIG,
    harness_dir: Path = HARNESS_DIR,
) -> dict:
    """Verify the current model/config/report bundle against its manifest."""

    manifest = read_json_object(manifest_path, "manifest")
    if report_path is None:
        report_name = manifest.get("report_file")
        if not isinstance(report_name, str) or Path(report_name).name != report_name:
            raise FreezeVerificationError(
                "manifest report_file must be a local filename"
            )
        report_path = manifest_path.parent / report_name

    expected = freeze_manifest(
        report_path=report_path,
        config=config,
        harness_dir=harness_dir,
    )
    if manifest != expected:
        raise FreezeVerificationError(
            "manifest mismatch: current model, config, report, tests, or README "
            "do not match the recorded reproducibility bundle"
        )

    return {
        "valid": True,
        "manifest_version": manifest["manifest_version"],
        "bundle_kind": manifest["bundle_kind"],
        "config_sha256": manifest["bindings"]["config"]["sha256"],
        "report_sha256": manifest["report_sha256"],
        "macro_claim_status": manifest["report_witness"]["macro_claim_status"],
        "w_c": manifest["report_witness"]["w_c"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run or verify the toy vesicle macro-constraint bundle."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify without rewriting the report or manifest",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=HARNESS_DIR / "vesicle_macro_constraint_report.json",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=HARNESS_DIR / "FREEZE_MANIFEST.json",
    )
    args = parser.parse_args(argv)

    if args.check:
        try:
            verification = verify_freeze_manifest(
                manifest_path=args.manifest,
                report_path=args.report,
            )
        except FreezeVerificationError as exc:
            print(f"bundle verification failed: {exc}", file=sys.stderr)
            return 1
        print(
            f"{args.manifest.name}: verified {verification['bundle_kind']}; "
            f"macro_claim={verification['macro_claim_status']}, "
            f"W_C={verification['w_c']}"
        )
        return 0

    report = write_report(args.report)
    write_freeze_manifest(args.manifest, report_path=args.report)
    verification = verify_freeze_manifest(
        manifest_path=args.manifest,
        report_path=args.report,
    )
    print(
        f"{args.report.name}: W_C={report['witness']['w_c']:.6f}, "
        f"SYN_GATE={'pass' if report['syntropy']['gate']['passes'] else 'fail'}, "
        f"KL={report['perturbation_kl']:.6f}; "
        f"macro_claim={report['result']['macro_claim_status']}; "
        f"{args.manifest.name} written and verified={verification['valid']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

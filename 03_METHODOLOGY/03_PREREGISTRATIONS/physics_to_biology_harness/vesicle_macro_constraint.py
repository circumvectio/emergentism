#!/usr/bin/env python3
"""Toy vesicle macro-constraint harness for the physics-to-biology run sheet.

This is a proof-of-method harness, not biological evidence. It instantiates the
objects demanded by the macro-constraint preregistration:

- lower law K_X over a finite two-compartment diffusion model
- macro map pi from molecule counts to low / viable / high states
- constraint gate G_C that changes transition weights without adding forbidden
  lower-law transitions
- perturbability, effective-information, and cost-ledger witnesses
"""

from __future__ import annotations

import json
import math
import hashlib
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
    cost_measure: float = 0.01
    cost_memory: float = 0.01
    cost_control: float = 0.015
    cost_erasure: float = 0.005
    cost_model: float = 0.01
    cost_labor: float = 0.01
    cost_entropy_export: float = 0.01


DEFAULT_CONFIG = VesicleConfig()
MACRO_STATES = ("low", "viable", "high")
HARNESS_DIR = Path(__file__).resolve().parent
HASHED_FILES = (
    "README.md",
    "test_vesicle_macro_constraint.py",
    "vesicle_macro_constraint.py",
)


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


def cost_ledger(config: VesicleConfig) -> dict[str, float]:
    return {
        "Cost_measure": config.cost_measure,
        "Cost_memory": config.cost_memory,
        "Cost_control": config.cost_control,
        "Cost_erasure": config.cost_erasure,
        "Cost_model": config.cost_model,
        "Cost_labor": config.cost_labor,
        "Cost_entropy_export": config.cost_entropy_export,
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
    ei_coarse_null = mutual_information_bits(null_channel)
    ei_micro_fair = ei_coarse_null
    ei_domain = ei_coarse_null
    ei_baseline = max(ei_micro_fair, ei_coarse_null, ei_domain)
    costs = cost_ledger(config)
    cost_c = sum(costs.values())
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
    syn_c = (
        (diagonal_constrained - diagonal_null)
        + viable_stability_delta
        + delta_effective_information
        - cost_c
    )

    return {
        "support_subset": support_ok,
        "perturbation_kl": perturbation_kl,
        "passes_macro_constraint": (
            support_ok
            and perturbation_kl > config.epsilon
            and w_c > 0.0
        ),
        "channels": {
            "null_no_membrane": null_channel,
            "constrained_membrane": constrained_channel,
        },
        "cost_ledger": costs,
        "witness": {
            "ei_macro": ei_macro,
            "ei_micro_fair": ei_micro_fair,
            "ei_coarse_null": ei_coarse_null,
            "ei_domain": ei_domain,
            "ei_baseline": ei_baseline,
            "cost_c": cost_c,
            "w_c": w_c,
        },
        "syntropy": {
            "delta_macro_state_preservation": diagonal_constrained - diagonal_null,
            "delta_viable_reachability": viable_reach_constrained - viable_reach_null,
            "delta_viable_stability": viable_stability_delta,
            "delta_effective_information": delta_effective_information,
            "syn_c": syn_c,
        },
    }


def format_control_float(value: float) -> str:
    return f"{value:.6f}"


def negative_control_suite(config: VesicleConfig = DEFAULT_CONFIG) -> dict:
    lower = build_lower_kernel(config)
    null_gate = build_null_gate_kernel(config, lower)
    no_gate_witness = witness_summary(config, lower, null_gate)

    high_cost_config = replace(config, cost_model=1.0)
    high_cost_lower = build_lower_kernel(high_cost_config)
    high_cost_constrained = build_constrained_kernel(high_cost_config, high_cost_lower)
    high_cost_witness = witness_summary(
        high_cost_config,
        high_cost_lower,
        high_cost_constrained,
    )

    forbidden_lower = [[1.0, 0.0], [0.0, 1.0]]
    forbidden_constrained = [[0.5, 0.5], [0.0, 1.0]]
    forbidden_detected = not support_subset(
        forbidden_lower,
        forbidden_constrained,
        config.support_epsilon,
    )

    no_gate_passes = no_gate_witness["passes_macro_constraint"]
    high_cost_passes = high_cost_witness["passes_macro_constraint"]

    return {
        "no_gate": {
            "description": "C is identical to K_X; perturbability and surplus must fail.",
            "passes_macro_constraint": no_gate_passes,
            "perturbation_kl": format_control_float(no_gate_witness["perturbation_kl"]),
            "w_c": format_control_float(no_gate_witness["witness"]["w_c"]),
        },
        "high_cost": {
            "description": "C changes the macro channel, but the declared cost ledger overwhelms surplus.",
            "passes_macro_constraint": high_cost_passes,
            "ei_macro_minus_baseline": format_control_float(
                high_cost_witness["witness"]["ei_macro"]
                - high_cost_witness["witness"]["ei_baseline"]
            ),
            "w_c": format_control_float(high_cost_witness["witness"]["w_c"]),
        },
        "forbidden_support": {
            "description": "Artificial constrained row assigns probability to a lower-law-forbidden transition.",
            "violation_detected": forbidden_detected,
        },
        "all_controls_reject": (
            not no_gate_passes
            and not high_cost_passes
            and forbidden_detected
        ),
    }


def macro_constraint_report(config: VesicleConfig = DEFAULT_CONFIG) -> dict:
    lower = build_lower_kernel(config)
    constrained = build_constrained_kernel(config, lower)
    summary = witness_summary(config, lower, constrained)

    return {
        "model": "minimal two-compartment vesicle diffusion with membrane gate",
        "evidence_tier": "[B] toy-model receipt only; [C] for biology",
        "claim_boundary": (
            "This is an executable proof-of-method for the macro-constraint "
            "protocol, not biological evidence and not a claim that life has "
            "been explained."
        ),
        "config": asdict(config),
        "macro_states": list(MACRO_STATES),
        "closure": "support(K_X^C) subset support(K_X)",
        "support_subset": summary["support_subset"],
        "epsilon": config.epsilon,
        "perturbation_kl": summary["perturbation_kl"],
        "passes_macro_constraint": summary["passes_macro_constraint"],
        "channels": summary["channels"],
        "cost_ledger": summary["cost_ledger"],
        "witness": summary["witness"],
        "syntropy": summary["syntropy"],
        "negative_controls": negative_control_suite(config),
        "public_interpretation": (
            "If this were a frozen domain run, the only safe wording would be: "
            "in this toy model and at this grain, the declared organization "
            "behaved as a costed macro-constraint."
        ),
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


def freeze_manifest(
    report_path: Path,
    config: VesicleConfig = DEFAULT_CONFIG,
    harness_dir: Path = HARNESS_DIR,
) -> dict:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    hashed_paths = {name: harness_dir / name for name in HASHED_FILES}
    file_hashes = {
        name: sha256_file(path) for name, path in sorted(hashed_paths.items())
    }
    witness = report["witness"]
    syntropy = report["syntropy"]

    return {
        "manifest_version": "macro-constraint-freeze-v1",
        "evidence_tier": report["evidence_tier"],
        "claim_boundary": report["claim_boundary"],
        "commands": [
            "python3 -m unittest test_vesicle_macro_constraint.py",
            "python3 vesicle_macro_constraint.py",
        ],
        "frozen_objects": {
            "X": "internal molecule count in finite two-compartment vesicle model",
            "K_X": "binomial diffusion transition kernel",
            "pi": "macro map from count to low / viable / high",
            "Y": list(MACRO_STATES),
            "G_C": "membrane gate preserving macro concentration topology",
            "Cost_C": cost_ledger(config),
            "epsilon": config.epsilon,
        },
        "report_file": report_path.name,
        "report_sha256": sha256_file(report_path),
        "file_hashes": file_hashes,
        "report_witness": {
            "w_c": f"{witness['w_c']:.6f}",
            "syn_c": f"{syntropy['syn_c']:.6f}",
            "perturbation_kl": f"{report['perturbation_kl']:.6f}",
            "support_subset": report["support_subset"],
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


def main() -> int:
    output = Path(__file__).with_name("vesicle_macro_constraint_report.json")
    report = write_report(output)
    manifest_output = Path(__file__).with_name("FREEZE_MANIFEST.json")
    write_freeze_manifest(manifest_output, report_path=output)
    print(
        f"{output.name}: W_C={report['witness']['w_c']:.6f}, "
        f"SYN_C={report['syntropy']['syn_c']:.6f}, "
        f"KL={report['perturbation_kl']:.6f}; "
        f"{manifest_output.name} written"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

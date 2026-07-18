#!/usr/bin/env python3
"""Fail-closed validator for the selected seven-row Agentz configuration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents"
ENV_PATH = ROOT / "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/emergentism.environment.yaml"

ROW_CONTRACT: dict[str, dict[str, str]] = {
    "L1": {
        "caste": "Caṇḍāla",
        "operator": "Kali 🎲 (routing token; morally untyped)",
        "operator_id": "kali_firewall",
        "balance_coordinate": "B≈0.276",
        "pramana": "Pratyakṣa (perception)",
        "reasoning": "Dialectical",
        "ology": "Objective Function",
        "regime": "Tyranny",
        "equation": "Φ_chart→0 ⇒ B→0",
        "equation_domain": "Φ_chart:=φ on the selected reciprocal chart; node Φ remains distinct",
    },
    "L2": {
        "caste": "Śūdra",
        "operator": "Kālī 💀 (routing token; morally untyped)",
        "operator_id": "kali_explorer",
        "balance_coordinate": "B=0.5",
        "pramana": "Upamāna (analogy)",
        "reasoning": "Inductive",
        "ology": "Data Science",
        "regime": "Democracy",
        "equation": "dP_node = V·dΦ + Φ·dV",
        "equation_domain": "declared differentiable product model P_node:=ΦV",
    },
    "L3": {
        "caste": "Vaiśya",
        "operator": "Kṛṣṇa ◇ (routing token; morally untyped)",
        "operator_id": "krishna_auditor",
        "balance_coordinate": "B=√3/2≈0.866",
        "pramana": "Anumāna (inference)",
        "reasoning": "Deductive",
        "ology": "Auditing",
        "regime": "Oligarchy",
        "equation": "∂P_node/∂V = Φ",
        "equation_domain": "declared product model P_node:=ΦV",
    },
    "L4": {
        "caste": "Kṣatriya",
        "operator": "Arjuna ⚔ (routing token; morally untyped)",
        "operator_id": "arjuna_executor",
        "balance_coordinate": "B=1",
        "pramana": "Arthāpatti (postulation)",
        "reasoning": "Abductive",
        "ology": "Value Alignment",
        "regime": "Timocracy",
        "equation": "dΦ/Φ = dV/V",
        "equation_domain": "selected relative-change balance condition with Φ,V>0",
    },
    "L5": {
        "caste": "Brāhmaṇa",
        "operator": "Brahmā ○ (Executive boundary; non-deployable)",
        "operator_id": "brahma_architect",
        "balance_coordinate": "B=√3/2≈0.866",
        "pramana": "Śabda (testimony)",
        "reasoning": "Systematic",
        "ology": "System Architecture",
        "regime": "Aristocracy",
        "equation": "log P_node = log Φ + log V",
        "equation_domain": "positive domain Φ,V,P_node>0 under P_node:=ΦV",
    },
    "L6": {
        "caste": "Sādhu",
        "operator": "Śiva • (Executive boundary; non-deployable)",
        "operator_id": "shiva_compressor",
        "balance_coordinate": "B=0.5",
        "pramana": "First Principles (Anupalabdhi / non-apprehension source pairing)",
        "reasoning": "Axiomatic",
        "ology": "Core State",
        "regime": "Anarchy",
        "equation": "E_node = −log(P_node)",
        "equation_domain": "positive score domain P_node>0; E_node is not physical energy",
    },
    "L7": {
        "caste": "Ṛṣi",
        "operator": "Viṣṇu ⊙ (Executive boundary; non-deployable)",
        "operator_id": "vishnu_witness",
        "balance_coordinate": "B≈0.276",
        "pramana": "Pratibhā (intuition)",
        "reasoning": "Transcendental",
        "ology": "Institutional Narrative",
        "regime": "Theocracy",
        "equation": "z_R:=φ/ν",
        "equation_domain": "real latitude-ratio proxy; not the full complex stereographic coordinate",
    },
}

REQUIRED_METADATA = {
    "level",
    "caste",
    "operator",
    "operator_id",
    "operator_tier",
    "balance_coordinate",
    "balance_tier",
    "pramana",
    "reasoning",
    "ology",
    "regime",
    "equation",
    "equation_domain",
    "operator_token_tier",
    "varna_pramana_tier",
    "cross_domain_tier",
    "equation_tier",
    "input_type",
    "output_type",
    "stop_condition",
    "permissions",
    "authorization_mode",
    "budget_source",
    "budget_required_fields",
    "evaluation_contract",
    "d4_d5_contract",
}
MUTATING_TOOLS = {"write", "edit", "bash"}
AUTHORIZATION_FIELDS = {
    "principal",
    "mandate",
    "scope",
    "consent",
    "custody",
    "expiry",
    "revocation",
    "contest path",
    "actor",
    "consequence bearer",
    "payer",
    "beneficiary",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML root must be a mapping")
    return data


def enabled_tools(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for toolset in spec.get("tools", []):
        for config in toolset.get("configs", []):
            if config.get("enabled") is True:
                found[str(config.get("name"))] = config
    return found


def validate_specs(specs: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(specs) != 7:
        errors.append(f"expected 7 agent specs, found {len(specs)}")

    by_level: dict[str, dict[str, Any]] = {}
    for index, spec in enumerate(specs):
        meta = spec.get("metadata")
        if not isinstance(meta, dict):
            errors.append(f"spec[{index}] missing metadata mapping")
            continue
        level = str(meta.get("level", ""))
        if not level:
            errors.append(f"spec[{index}] missing metadata.level")
            continue
        if level in by_level:
            errors.append(f"duplicate level {level}")
        by_level[level] = spec

    if set(by_level) != set(ROW_CONTRACT):
        errors.append(
            f"levels must be exactly {sorted(ROW_CONTRACT)}; found {sorted(by_level)}"
        )

    for level, expected in ROW_CONTRACT.items():
        spec = by_level.get(level)
        if spec is None:
            continue
        meta = spec["metadata"]
        missing = sorted(REQUIRED_METADATA - set(meta))
        if missing:
            errors.append(f"{level}: missing metadata {missing}")
        for key, value in expected.items():
            if meta.get(key) != value:
                errors.append(
                    f"{level}: {key} must be {value!r}, found {meta.get(key)!r}"
                )

        if "[S]" not in str(meta.get("operator_token_tier", "")) or "[A]" not in str(
            meta.get("operator_token_tier", "")
        ):
            errors.append(f"{level}: operator/B tier split is absent")
        if "[S]" not in str(meta.get("operator_tier", "")):
            errors.append(f"{level}: operator token tier must remain [S]")
        if "[A]" not in str(meta.get("balance_tier", "")) or "[S]" not in str(
            meta.get("balance_tier", "")
        ):
            errors.append(f"{level}: analytic B / selected latitude tier split is absent")
        if "[S]" not in str(meta.get("varna_pramana_tier", "")) or "[I]" not in str(
            meta.get("varna_pramana_tier", "")
        ):
            errors.append(f"{level}: Varṇa/Pramāṇa internal/external tier split is absent")
        if "[I]" not in str(meta.get("cross_domain_tier", "")):
            errors.append(f"{level}: cross-domain tier must remain [I]")
        if "[A]" not in str(meta.get("equation_tier", "")) or "[S]" not in str(
            meta.get("equation_tier", "")
        ):
            errors.append(f"{level}: equation fact/placement tier split is absent")
        if meta.get("budget_required_fields") != "max_calls,max_tokens,max_wall_seconds,max_delegations":
            errors.append(f"{level}: budget field contract is incomplete")
        if meta.get("evaluation_contract") != "blinded_budget_matched_against_flat_and_shorter_rivals":
            errors.append(f"{level}: blinded budget-matched evaluation contract is absent")
        if "D4 actual" not in str(meta.get("d4_d5_contract", "")) or "D5 possible" not in str(
            meta.get("d4_d5_contract", "")
        ):
            errors.append(f"{level}: D4-carrier/D5-content type split is absent")

        tools = enabled_tools(spec)
        mutating = MUTATING_TOOLS & set(tools)
        if level == "L4":
            if mutating != MUTATING_TOOLS:
                errors.append(f"L4: mutating tools must be exactly {sorted(MUTATING_TOOLS)}")
            for name in sorted(MUTATING_TOOLS):
                policy = tools.get(name, {}).get("permission_policy", {})
                if policy.get("type") != "always_ask":
                    errors.append(f"L4: {name} must be always_ask")
            if meta.get("authorization_mode") != "complete_envelope_plus_platform_confirmation":
                errors.append("L4: authorization mode must require envelope plus confirmation")
            system = str(spec.get("system", "")).lower()
            for field in AUTHORIZATION_FIELDS:
                if field not in system:
                    errors.append(f"L4: system prompt missing authorization field {field!r}")
            if "commitment receipt" not in system or "outcome receipt" not in system:
                errors.append("L4: commitment/outcome receipt separation is absent")
        else:
            if mutating:
                errors.append(f"{level}: read-only profile exposes mutating tools {sorted(mutating)}")
            if meta.get("authorization_mode") != "no_consequential_action":
                errors.append(f"{level}: authorization mode must forbid consequential action")

        identity_fields = " ".join(
            str(value)
            for value in (
                meta.get("operator", ""),
                spec.get("name", ""),
                spec.get("description", ""),
            )
        ).lower()
        if "god" in identity_fields or "demon" in identity_fields:
            errors.append(f"{level}: God/Demon identity leakage in configured identity fields")

    return errors


def validate_paths(config_dir: Path = CONFIG_DIR, env_path: Path = ENV_PATH) -> list[str]:
    paths = sorted(config_dir.glob("*.agent.yaml"))
    specs = [load_yaml(path) for path in paths]
    errors = validate_specs(specs)
    env = load_yaml(env_path)
    status = str((env.get("metadata") or {}).get("calibration_status", ""))
    if status != "unprovisioned_x0":
        errors.append("environment must disclose calibration_status=unprovisioned_x0")
    networking = ((env.get("config") or {}).get("networking") or {})
    if networking.get("type") != "limited":
        errors.append("environment networking must be limited")
    if networking.get("allowed_hosts") != []:
        errors.append("environment allowed_hosts must be empty until separately authorized")
    if networking.get("allow_mcp_servers") is not False:
        errors.append("environment MCP egress must be disabled")
    if networking.get("allow_package_managers") is not False:
        errors.append("environment package-manager egress must be disabled")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without mutation")
    parser.parse_args()
    errors = validate_paths()
    if errors:
        for error in errors:
            print(f"AGENTZ-ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "AGENTZ-OK: 7 exact typed rows (operator/B/domain); 4+3 permissions; "
        "authorization and receipt boundaries present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

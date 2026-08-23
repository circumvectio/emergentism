#!/usr/bin/env python3
"""Offline validators and deterministic fixture generator for v2.2 research contracts."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
FORCE_FIXTURE = HERE / "fixtures" / "force_24.json"
INTERACTIONS = ("S", "E", "W", "G")
REGISTERS = ("D1", "D2", "D3", "D4")
COMPARATORS = {"NATIVE", "ONE_AXIS", "ALTERNATE_TWO_AXIS", "ADDED_AXIS", "LEARNED_NO_PLACEMENT"}
FORCE_RIVALS = {"R0_NO_MAPPING", "R2_MANY_TO_MANY", "R3_ELECTROWEAK_UNIFICATION"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_m4(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema_id") != "M4Compression.v1":
        return ["M4 identity mismatch"]
    required_objects = ("corpus", "native_encoder", "target", "code_length", "distortion_metric", "performance_floor", "splits", "resource_parity")
    for field in required_objects:
        if not isinstance(value.get(field), dict) or not value[field]:
            errors.append(f"M4.{field} must be a non-empty object")
    comparator_rows = value.get("comparators")
    if not isinstance(comparator_rows, list):
        errors.append("M4.comparators must be an array")
    else:
        kinds = {row.get("kind") for row in comparator_rows if isinstance(row, dict)}
        if kinds != COMPARATORS:
            errors.append(f"M4 comparator class drift: {sorted(str(row) for row in kinds)}")
    if value.get("maximality_scope") != "FROZEN_COMPARATOR_CLASS_ONLY":
        errors.append("M4 maximality must remain comparator-class relative")
    if value.get("global_game_theory_exhausted") is not False:
        errors.append("M4 cannot claim to exhaust game theory")
    if value.get("result_state") not in {"UNRUN", "PARTIAL", "SURVIVES", "KILLED"}:
        errors.append("M4.result_state is invalid")
    if not _text(value.get("kill")) or not _text(value.get("survivor")):
        errors.append("M4 kill and survivor are required")
    return errors


def validate_slwp(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema_id") != "SLWPBoundaryTest.v1":
        return ["SLWP boundary-test identity mismatch"]
    if value.get("mu_id") not in {"mu0", "mu1", "mu2", "mu3", "mu4"}:
        errors.append("SLWP.mu_id is invalid")
    for field in ("lower_freeze", "higher_candidate", "projection_map", "section_map", "fiber_witness", "recovery_result", "reducible_counterexample"):
        if not isinstance(value.get(field), dict) or not value[field]:
            errors.append(f"SLWP.{field} must be a non-empty object")
    recovery = value.get("recovery_result", {})
    if value.get("projection_result") == "PROJECTION_ASYMMETRY_PROVEN":
        if recovery.get("U_after_s_identity") is not True or recovery.get("s_after_U_identity") is not False:
            errors.append("projection asymmetry requires U-after-s identity and nonidentity in the reverse composition")
    if value.get("ontology_result") in {"OPEN", "REDUCED", "KILLED"} and value.get("strong_emergence_established") is not False:
        errors.append("an open, reduced, or killed ontology result cannot establish strong emergence")
    if value.get("strong_emergence_established") is True and value.get("ontology_result") != "SURVIVES_BOUNDED_TEST":
        errors.append("strong emergence can only survive a bounded test, never follow from the fiber lemma alone")
    if not _text(value.get("novelty_discriminator")) or not _text(value.get("held_out_prediction")):
        errors.append("SLWP novelty discriminator and held-out prediction are required")
    if not _text(value.get("kill")) or not _text(value.get("survivor")):
        errors.append("SLWP kill and survivor are required")
    return errors


def force_fixture() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for assignment in itertools.permutations(INTERACTIONS):
        code = "".join(assignment)
        candidates.append(
            {
                "candidate_id": f"W7-4P-{code}",
                "assignment": dict(zip(REGISTERS, assignment)),
                "origin_reference": code == "SEWG",
                "native_recovery": "NOT_RUN",
                "held_out_prediction": "NOT_RUN",
                "status": "UNSCORED",
            }
        )
    return {
        "schema_id": "ForcePermutationTrial.v1",
        "trial_id": "w7-force-permutations-unrun-v1",
        "registers": list(REGISTERS),
        "interactions": list(INTERACTIONS),
        "candidates": candidates,
        "rivals": [
            {"rival_id": "R0_NO_MAPPING", "description": "Standard Model plus GR/EFT without a D-placement."},
            {"rival_id": "R2_MANY_TO_MANY", "description": "Several D structures may relate to one interaction."},
            {"rival_id": "R3_ELECTROWEAK_UNIFICATION", "description": "Low-energy E/W separation need not define serial stages."},
        ],
        "d3_quantum_specific_gate": {
            "generic_quantumness_sufficient": False,
            "weak_specific_if_W_at_D3": ["left-chiral or parity-violating structure", "charged-current flavor transition", "held-out weak-specific observable"],
        },
        "agreement_with_burri_counts_as_correctness": False,
        "primary_scalar": None,
        "selected_candidate": None,
        "evaluation_count": 0,
        "result_state": "UNRUN",
    }


def validate_force(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema_id") != "ForcePermutationTrial.v1":
        return ["force-permutation identity mismatch"]
    if tuple(value.get("registers", [])) != REGISTERS or tuple(value.get("interactions", [])) != INTERACTIONS:
        errors.append("force registers/interactions drift")
    candidates = value.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 24:
        errors.append("force trial must contain exactly 24 candidates")
        candidates = []
    expected = set(itertools.permutations(INTERACTIONS))
    observed: set[tuple[str, ...]] = set()
    ids: set[str] = set()
    for row in candidates:
        if not isinstance(row, dict):
            errors.append("force candidate must be an object")
            continue
        candidate_id = row.get("candidate_id")
        if candidate_id in ids:
            errors.append(f"duplicate force candidate ID: {candidate_id}")
        ids.add(candidate_id)
        assignment = row.get("assignment", {})
        if not isinstance(assignment, dict) or tuple(assignment) != REGISTERS:
            errors.append(f"candidate {candidate_id} register order drift")
            continue
        permutation = tuple(assignment[register] for register in REGISTERS)
        observed.add(permutation)
        if set(permutation) != set(INTERACTIONS):
            errors.append(f"candidate {candidate_id} is not bijective")
        if row.get("status") != "UNSCORED" or row.get("native_recovery") != "NOT_RUN" or row.get("held_out_prediction") != "NOT_RUN":
            errors.append(f"candidate {candidate_id} cannot carry a result at null launch")
        if row.get("origin_reference") is not (permutation == ("S", "E", "W", "G")):
            errors.append(f"candidate {candidate_id} origin-reference marker drift")
    if observed != expected:
        errors.append("force permutation universe is incomplete or duplicated")
    rival_ids = {row.get("rival_id") for row in value.get("rivals", []) if isinstance(row, dict)}
    if not FORCE_RIVALS.issubset(rival_ids):
        errors.append("force trial is missing no-map, many-to-many, or electroweak rival")
    if value.get("agreement_with_burri_counts_as_correctness") is not False:
        errors.append("agreement with the Burri order cannot count as correctness")
    if value.get("primary_scalar") is not None or value.get("selected_candidate") is not None:
        errors.append("unrun force trial cannot select or rank a candidate")
    if value.get("evaluation_count") != 0 or value.get("result_state") != "UNRUN":
        errors.append("force trial null state drift")
    gate = value.get("d3_quantum_specific_gate", {})
    if gate.get("generic_quantumness_sufficient") is not False:
        errors.append("generic quantumness cannot satisfy the D3 force gate")
    return errors


def validate_document(value: Any) -> list[str]:
    schema_id = value.get("schema_id") if isinstance(value, dict) else None
    if schema_id == "M4Compression.v1":
        return validate_m4(value)
    if schema_id == "SLWPBoundaryTest.v1":
        return validate_slwp(value)
    if schema_id == "ForcePermutationTrial.v1":
        return validate_force(value)
    return [f"unsupported schema_id: {schema_id}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = force_fixture()
    if args.generate:
        write_json(FORCE_FIXTURE, expected)
    if args.check:
        errors: list[str] = []
        for name in ("m4_dev.json", "slwp_dev.json", "force_24.json"):
            path = HERE / "fixtures" / name
            if not path.is_file():
                errors.append(f"missing fixture: {name}")
                continue
            value = load_json(path)
            errors.extend(f"{name}: {row}" for row in validate_document(value))
        if FORCE_FIXTURE.is_file() and load_json(FORCE_FIXTURE) != expected:
            errors.append("force_24.json deterministic generation drift")
        if errors:
            print("V2.2 RESEARCH CONTRACTS: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 2
        print("V2.2 RESEARCH CONTRACTS: PASS · M4 null · SLWP typed · 24 force permutations unscored")
    if not args.generate and not args.check:
        parser.error("select --generate and/or --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

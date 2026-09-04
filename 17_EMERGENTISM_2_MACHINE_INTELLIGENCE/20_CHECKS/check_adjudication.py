#!/usr/bin/env python3
"""ADJ-01: validate an adjudication packet. Does not replace SLWPBoundaryTest.v1."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
EMERGENTISM_ROOT = HERE.parents[1]
CONTRACTS_PY = (
    EMERGENTISM_ROOT
    / "03_METHODOLOGY"
    / "03_PREREGISTRATIONS"
    / "v2_2_contracts"
    / "research_contracts.py"
)
if not CONTRACTS_PY.is_file():
    raise SystemExit(f"1.0 packet owner missing: {CONTRACTS_PY}")
_spec = importlib.util.spec_from_file_location("research_contracts", CONTRACTS_PY)
if _spec is None or _spec.loader is None:
    raise SystemExit(f"cannot load {CONTRACTS_PY}")
_contracts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_contracts)
load_json = _contracts.load_json
validate_slwp = _contracts.validate_slwp

SCHEMA_ID = "Adjudication.v0"
D_REGISTER = re.compile(r"^D[0-6]$")
MU_IDS = {"mu0", "mu1", "mu2", "mu3", "mu4"}
CLAIM_TYPES = {
    "mu_lift",
    "chi_select",
    "ea08_constraint",
    "U_projection",
    "ill_typed",
}
INFERENCES = {
    "none",
    "emerged_implies_reconstructable",
    "noninvertible_implies_strong",
}
AXES = {"PASS", "AXIS_MIX"}
VERDICTS = {
    "INCOMPLETE",
    "ILL_TYPED",
    "AXIS_MIX",
    "REDUCED",
    "OPEN",
    "SURVIVES_BOUNDED_TEST",
    "KILLED",
}
WORLD_TIERS = {"C", "I", "D"}
PROJECTION = {"PROJECTION_ASYMMETRY_PROVEN", "NOT_ESTABLISHED", "KILLED", None}
ONTOLOGY = {"OPEN", "SURVIVES_BOUNDED_TEST", "REDUCED", "KILLED", None}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _axis_mixed(packet: dict[str, Any]) -> bool:
    register = packet.get("register")
    kind = packet.get("register_kind")
    if kind != "D":
        return True
    if not isinstance(register, str) or not D_REGISTER.match(register):
        return True
    return False


def _load_slwp(ref: Any) -> tuple[dict[str, Any] | None, list[str]]:
    if ref is None:
        return None, []
    if isinstance(ref, dict) and ref.get("schema_id") == "SLWPBoundaryTest.v1":
        return ref, [f"inline SLWP: {row}" for row in validate_slwp(ref)]
    if isinstance(ref, dict) and _text(ref.get("path")):
        path = (EMERGENTISM_ROOT / ref["path"]).resolve()
        if not path.is_file():
            return None, [f"SLWP path missing: {ref['path']}"]
        value = load_json(path)
        return value, [f"SLWP {ref['path']}: {row}" for row in validate_slwp(value)]
    return None, ["slwp_packet must be null, an inline SLWPBoundaryTest.v1, or {path}"]


def validate_adjudication(packet: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet, dict) or packet.get("schema_id") != SCHEMA_ID:
        return ["Adjudication identity mismatch"]

    required = (
        "claim_id",
        "phenomenon",
        "register",
        "register_kind",
        "claim_type",
        "claimed_inference",
        "axis",
        "anderson_inference",
        "verdict",
        "world_reading_tier",
        "strong_emergence_established",
        "kill",
        "survivor",
    )
    for field in required:
        if field not in packet:
            errors.append(f"missing {field}")

    if not _text(packet.get("claim_id")) or not _text(packet.get("phenomenon")):
        errors.append("claim_id and phenomenon are required text")
    if packet.get("claim_type") not in CLAIM_TYPES:
        errors.append("claim_type is invalid")
    if packet.get("claimed_inference") not in INFERENCES:
        errors.append("claimed_inference is invalid")
    if packet.get("axis") not in AXES:
        errors.append("axis is invalid")
    if packet.get("verdict") not in VERDICTS:
        errors.append("verdict is invalid")
    if packet.get("world_reading_tier") not in WORLD_TIERS:
        errors.append("world_reading_tier must be C, I, or D — never S")
    if packet.get("projection_result") not in PROJECTION:
        errors.append("projection_result is invalid")
    if packet.get("ontology_result") not in ONTOLOGY:
        errors.append("ontology_result is invalid")
    if not isinstance(packet.get("strong_emergence_established"), bool):
        errors.append("strong_emergence_established must be a boolean")
    if not _text(packet.get("kill")) or not _text(packet.get("survivor")):
        errors.append("kill and survivor are required")

    mixed = _axis_mixed(packet)
    if mixed and packet.get("axis") != "AXIS_MIX":
        errors.append("axis-mix missed: non-D register must set axis=AXIS_MIX")
    if mixed and packet.get("verdict") != "AXIS_MIX":
        errors.append("axis-mix missed: non-D register must verdict AXIS_MIX")
    if not mixed and packet.get("axis") == "AXIS_MIX":
        errors.append("axis=AXIS_MIX on a D-register seating")

    inference = packet.get("claimed_inference")
    if inference == "emerged_implies_reconstructable":
        if packet.get("anderson_inference") != "FIRED_CONSTRUCTIONIST":
            errors.append("constructionist converse must set anderson_inference=FIRED_CONSTRUCTIONIST")
        if packet.get("verdict") != "KILLED":
            errors.append("constructionist converse is dead (Anderson 1972); verdict must be KILLED")
    elif inference == "noninvertible_implies_strong":
        if packet.get("anderson_inference") != "FIRED_NONINVERTIBILITY_AS_STRONG":
            errors.append("noninvertibility-as-strong must set FIRED_NONINVERTIBILITY_AS_STRONG")
        if packet.get("verdict") != "KILLED":
            errors.append("noninvertibility is not strong emergence (SLWP-01D); verdict must be KILLED")
    elif inference == "none" and packet.get("anderson_inference") != "NOT_USED":
        errors.append("claimed_inference=none requires anderson_inference=NOT_USED")

    if packet.get("same_register_ends") is True:
        if packet.get("claim_type") != "ill_typed" or packet.get("verdict") != "ILL_TYPED":
            errors.append(
                "same-register ends are not a lift; claim_type=ill_typed and verdict=ILL_TYPED"
            )

    if packet.get("representation_relation") is True:
        if packet.get("claim_type") == "mu_lift":
            errors.append("D4-token/D5-content is representation, not a lift")
        if packet.get("verdict") not in {"ILL_TYPED", "AXIS_MIX"}:
            errors.append("a representation relation cannot verdict as a μ crossing")

    claim_type = packet.get("claim_type")
    mu_id = packet.get("mu_id")
    if claim_type == "mu_lift":
        if mu_id not in MU_IDS:
            errors.append("mu_lift requires mu_id in mu0…mu4")
        slwp, slwp_errors = _load_slwp(packet.get("slwp_packet"))
        errors.extend(slwp_errors)
        if slwp is None and packet.get("verdict") not in {"INCOMPLETE", "AXIS_MIX", "KILLED"}:
            errors.append("mu_lift without an SLWP packet must verdict INCOMPLETE")
        if slwp is not None:
            if packet.get("projection_result") != slwp.get("projection_result"):
                errors.append("projection_result must inherit the SLWP packet")
            if packet.get("ontology_result") != slwp.get("ontology_result"):
                errors.append("ontology_result must inherit the SLWP packet")
            if (
                slwp.get("ontology_result") == "REDUCED"
                and packet.get("verdict") not in {"REDUCED", "AXIS_MIX", "KILLED"}
            ):
                errors.append("SLWP ontology REDUCED must not be restated as OPEN or SURVIVES")
    elif mu_id not in {None, ""}:
        errors.append("mu_id is only for mu_lift")

    if packet.get("strong_emergence_established") is True:
        if packet.get("ontology_result") != "SURVIVES_BOUNDED_TEST":
            errors.append("strong emergence can only survive a bounded test")
        if packet.get("verdict") != "SURVIVES_BOUNDED_TEST":
            errors.append("strong_emergence_established requires verdict SURVIVES_BOUNDED_TEST")

    if packet.get("claim_type") == "ill_typed" and packet.get("verdict") not in {
        "ILL_TYPED",
        "AXIS_MIX",
    }:
        errors.append("ill_typed claims must verdict ILL_TYPED (or AXIS_MIX if the axis gate fired first)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="adjudication packet to validate")
    args = parser.parse_args()
    if args.check is None:
        parser.error("select --check PATH")
    packet = load_json(args.check)
    errors = validate_adjudication(packet)
    if errors:
        print(f"ADJ-01: FAIL {args.check}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    print(
        f"ADJ-01: PASS · axis={packet.get('axis')} · verdict={packet.get('verdict')} · "
        f"strong={packet.get('strong_emergence_established')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

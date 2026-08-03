#!/usr/bin/env python3
"""Validate the typed corpus-coherence profile without claiming world contact.

The three internal axes have a deterministic worst-state reduction. World
contact is deliberately a separate type: local gates may support the
operational axis, but they are not admissible world-contact evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = Path("09_TOOLS/01_SCRIPTS/coherence_profile.json")
SCHEMA = "emergentism/coherence-profile/v1"

INTERNAL_AXES = ("semantic", "routing", "operational")
INTERNAL_STATES = ("PASS", "PASS_WITH_DEBT", "QUARANTINE", "BLOCK")
STATE_SEVERITY = {state: rank for rank, state in enumerate(INTERNAL_STATES)}
WORLD_STATES = {"OPEN", "PARTIAL", "ESTABLISHED", "REFUTED"}
WORLD_EVIDENCE_KINDS = {
    "external_observation",
    "independent_replication",
    "external_review",
}
WORLD_OUTCOMES = {"supports", "mixed", "contradicts"}
DEBT_ID = re.compile(r"^[A-Z0-9][A-Z0-9._:-]*$")


class ProfileError(ValueError):
    """Raised when a profile violates the closed contract."""


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProfileError(f"{label}: expected object")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProfileError(f"{label}: expected non-empty string")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ProfileError(f"{label}: expected list")
    return value


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unknown {', '.join(extra)}")
        raise ProfileError(f"{label}: {'; '.join(details)}")


def _unique_strings(value: Any, label: str) -> list[str]:
    items = _require_list(value, label)
    strings = [_require_string(item, f"{label}[]") for item in items]
    if len(strings) != len(set(strings)):
        raise ProfileError(f"{label}: duplicate values are not allowed")
    return strings


def _validate_repository_ref(root: Path, ref: str, label: str) -> None:
    rel = Path(ref)
    if rel.is_absolute() or ".." in rel.parts:
        raise ProfileError(f"{label}: must be a repository-relative path")
    candidate = (root / rel).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ProfileError(f"{label}: missing authority file {ref}")


def _validate_internal_axis(
    name: str,
    value: Any,
    authority_refs: set[str],
    root: Path,
) -> str:
    axis = _require_object(value, f"axes.{name}")
    _require_exact_keys(axis, {"state", "basis_refs", "debt_ids"}, f"axes.{name}")
    state = _require_string(axis.get("state"), f"axes.{name}.state")
    if state not in INTERNAL_STATES:
        raise ProfileError(f"axes.{name}.state: invalid internal state {state}")

    basis_refs = _unique_strings(axis.get("basis_refs"), f"axes.{name}.basis_refs")
    if not basis_refs:
        raise ProfileError(f"axes.{name}.basis_refs: at least one authority reference is required")
    basis_text: list[str] = []
    for ref in basis_refs:
        if ref not in authority_refs:
            raise ProfileError(f"axes.{name}.basis_refs: undeclared authority reference {ref}")
        _validate_repository_ref(root, ref, f"axes.{name}.basis_refs")
        basis_text.append((root / ref).read_text(encoding="utf-8"))

    debt_ids = _unique_strings(axis.get("debt_ids"), f"axes.{name}.debt_ids")
    if any(not DEBT_ID.fullmatch(debt_id) for debt_id in debt_ids):
        raise ProfileError(f"axes.{name}.debt_ids: invalid debt identifier")
    if state == "PASS" and debt_ids:
        raise ProfileError(f"axes.{name}: PASS cannot retain debt_ids")
    if state != "PASS" and not debt_ids:
        raise ProfileError(f"axes.{name}: {state} requires at least one debt_id")
    joined_basis = "\n".join(basis_text)
    for debt_id in debt_ids:
        if debt_id not in joined_basis:
            raise ProfileError(
                f"axes.{name}.debt_ids: {debt_id} is not named by a basis authority"
            )
    return state


def _validate_world_contact(value: Any, root: Path) -> str:
    world = _require_object(value, "axes.world_contact")
    _require_exact_keys(
        world,
        {"state", "evidence", "open_requirements"},
        "axes.world_contact",
    )
    state = _require_string(world.get("state"), "axes.world_contact.state")
    if state not in WORLD_STATES:
        raise ProfileError(f"axes.world_contact.state: invalid world-contact state {state}")

    requirements = _unique_strings(
        world.get("open_requirements"),
        "axes.world_contact.open_requirements",
    )
    evidence = _require_list(world.get("evidence"), "axes.world_contact.evidence")
    kinds: set[str] = set()
    outcomes: set[str] = set()
    evidence_refs: set[str] = set()
    for index, raw_record in enumerate(evidence):
        label = f"axes.world_contact.evidence[{index}]"
        record = _require_object(raw_record, label)
        _require_exact_keys(record, {"kind", "ref", "outcome"}, label)
        kind = _require_string(record.get("kind"), f"{label}.kind")
        ref = _require_string(record.get("ref"), f"{label}.ref")
        outcome = _require_string(record.get("outcome"), f"{label}.outcome")
        if kind not in WORLD_EVIDENCE_KINDS:
            raise ProfileError(
                f"{label}.kind: {kind} is not world-contact evidence; "
                "internal gates are inadmissible here"
            )
        if outcome not in WORLD_OUTCOMES:
            raise ProfileError(f"{label}.outcome: invalid outcome {outcome}")
        _validate_repository_ref(root, ref, f"{label}.ref")
        if ref in evidence_refs:
            raise ProfileError(f"axes.world_contact.evidence: duplicate ref {ref}")
        kinds.add(kind)
        outcomes.add(outcome)
        evidence_refs.add(ref)

    if state == "OPEN":
        if evidence:
            raise ProfileError("axes.world_contact: OPEN requires an empty evidence list")
        if not requirements:
            raise ProfileError("axes.world_contact: OPEN requires named open requirements")
    elif state == "PARTIAL":
        if not evidence or not requirements:
            raise ProfileError(
                "axes.world_contact: PARTIAL requires evidence and remaining requirements"
            )
    elif state == "ESTABLISHED":
        needed = {"external_observation", "independent_replication"}
        if not needed <= kinds:
            raise ProfileError(
                "axes.world_contact: ESTABLISHED requires external observation "
                "and independent replication"
            )
        if requirements:
            raise ProfileError(
                "axes.world_contact: ESTABLISHED cannot retain open requirements"
            )
        if "contradicts" in outcomes:
            raise ProfileError(
                "axes.world_contact: ESTABLISHED cannot contain a contradicting outcome"
            )
    elif not evidence or "contradicts" not in outcomes:
        raise ProfileError(
            "axes.world_contact: REFUTED requires discriminating contradictory evidence"
        )
    return state


def validate_profile(profile: Any, root: Path = ROOT) -> tuple[str, str]:
    root = root.resolve()
    document = _require_object(profile, "profile")
    _require_exact_keys(
        document,
        {"schema", "profile_id", "scope", "authority_refs", "axes", "overall"},
        "profile",
    )
    if document.get("schema") != SCHEMA:
        raise ProfileError(f"profile.schema: expected {SCHEMA}")
    _require_string(document.get("profile_id"), "profile.profile_id")
    _require_string(document.get("scope"), "profile.scope")

    authority_refs = _unique_strings(document.get("authority_refs"), "profile.authority_refs")
    if not authority_refs:
        raise ProfileError("profile.authority_refs: at least one source owner is required")
    for ref in authority_refs:
        _validate_repository_ref(root, ref, "profile.authority_refs")
    authority_set = set(authority_refs)

    axes = _require_object(document.get("axes"), "profile.axes")
    _require_exact_keys(axes, {*INTERNAL_AXES, "world_contact"}, "profile.axes")
    states = [
        _validate_internal_axis(name, axes.get(name), authority_set, root)
        for name in INTERNAL_AXES
    ]
    world_state = _validate_world_contact(axes.get("world_contact"), root)

    overall = _require_object(document.get("overall"), "profile.overall")
    _require_exact_keys(overall, {"scope", "state"}, "profile.overall")
    if overall.get("scope") != "internal":
        raise ProfileError(
            "profile.overall.scope: must be internal; world contact is a separate axis"
        )
    declared_state = _require_string(overall.get("state"), "profile.overall.state")
    if declared_state not in INTERNAL_STATES:
        raise ProfileError(f"profile.overall.state: invalid internal state {declared_state}")
    computed_state = max(states, key=STATE_SEVERITY.__getitem__)
    if declared_state != computed_state:
        raise ProfileError(
            f"profile.overall.state: declared {declared_state}, computed {computed_state}"
        )
    return computed_state, world_state


def read_profile(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileError(f"{path}: unreadable profile: {exc}") from exc
    return _require_object(value, str(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=ROOT / PROFILE_PATH)
    args = parser.parse_args(argv)
    profile_path = args.profile.resolve()
    try:
        overall_state, world_state = validate_profile(read_profile(profile_path), ROOT)
    except ProfileError as exc:
        print("COHERENCE PROFILE: FAIL", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    print(
        "COHERENCE PROFILE: PASS "
        f"(overall_internal={overall_state}; world_contact={world_state})"
    )
    print(
        "  scope: validates a typed declaration; it does not turn an internal "
        "gate into world-contact evidence"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

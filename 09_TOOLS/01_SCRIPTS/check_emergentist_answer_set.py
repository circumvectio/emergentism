#!/usr/bin/env python3
"""Validate the machine projection of the ten Emergentist answers."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "00_META/internal_answers/EmergentistAnswerSet.v1.json"
EXPECTED_IDS = [f"EA-{number:02d}" for number in range(1, 11)]
STATE_AXES = {
    "owner_adoption",
    "internal_review",
    "empirical_contact",
    "pqa_adjudication",
    "publication",
}
EXPECTED_TOP_STATE = {
    "owner_adoption": "ADOPTED",
    "internal_review": "PASS",
    "empirical_contact": "NOT_RUN",
    "pqa_adjudication": "NOT_EVALUATED",
    "publication": "WITHHELD",
}
ALLOWED_STATE_VALUES = {
    "owner_adoption": {"PROPOSED", "ADOPTED", "RETIRED"},
    "internal_review": {"NOT_RUN", "PASS", "RETURN", "FAIL"},
    "empirical_contact": {
        "NOT_RUN",
        "COMPONENT_SUPPORTED",
        "NULL",
        "KILLED",
        "REPLICATED",
    },
    "pqa_adjudication": {"NOT_EVALUATED", "UNDER_REVIEW", "EARNED", "REJECTED"},
    "publication": {"WITHHELD", "PUBLIC"},
}
CLAIM_TYPES = {
    "STIPULATION",
    "ANALYTIC",
    "STRUCTURAL",
    "INTERPRETIVE",
    "CONJECTURAL",
    "EMPIRICAL",
}
REQUIRED_ANSWER_FIELDS = {
    "id",
    "name",
    "question",
    "selected_internal_answer",
    "semantic_owners",
    "dependencies",
    "anti_dependencies",
    "claim_atoms",
    "forbidden_inflations",
    "rivals",
    "discriminator",
    "kill",
    "survivor",
    "residual",
    "state",
}
BARRED_IN_SELECTED_ANSWERS = {
    "externally validated",
    "independently validated",
    "proved by ccc",
    "ccc proves",
    "consciousness causes collapse",
    "d5 directly causes",
    "established fifth physical force",
    "derives the born rule",
}
ANSWER_MODE_REQUIREMENTS = {
    "EA-02": "constitutive_reframe",
    "EA-06": "conditional_framework_answer",
    "EA-10": "constitutive_reframe",
}


def nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(nonempty(item) for item in value)
    return value is not None


def source_path(source: str) -> Path:
    return ROOT / source.split("#", 1)[0]


def source_anchor_exists(source: str) -> bool:
    """Require an explicit stable HTML id whenever a source names a fragment."""
    source_file, separator, anchor = source.partition("#")
    if not separator:
        return True
    if not anchor:
        return False
    try:
        text = (ROOT / source_file).read_text(encoding="utf-8")
    except OSError:
        return False
    return f'id="{anchor}"' in text or f"id='{anchor}'" in text


def validate() -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {CONTRACT.relative_to(ROOT)}: {exc}"]

    if data.get("schema") != "emergentism/EmergentistAnswerSet.v1":
        errors.append("schema must be emergentism/EmergentistAnswerSet.v1")
    if data.get("id") != "EAS-10@1":
        errors.append("id must be EAS-10@1")
    if data.get("state_axes") != EXPECTED_TOP_STATE:
        errors.append("top-level state_axes must preserve the frozen launch state")
    if set(data.get("state_axes", {})) != STATE_AXES:
        errors.append("state_axes must contain exactly the five independent axes")

    contract = data.get("epistemic_contract", {})
    if contract.get("state_independence") is not True:
        errors.append("epistemic_contract.state_independence must be true")
    for key in (
        "owner_adoption_implies_truth",
        "internal_review_implies_independent_review",
        "publication_implies_validation",
    ):
        if contract.get(key) is not False:
            errors.append(f"epistemic_contract.{key} must be false")
    if contract.get("pqa_54_state") != (
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved"
    ):
        errors.append("PQA-54 launch state drifted")

    for field in ("semantic_owner", "direction"):
        value = data.get(field)
        if not isinstance(value, str) or not source_path(value).is_file():
            errors.append(f"{field} must resolve to an existing file")

    answers = data.get("answers")
    if not isinstance(answers, list):
        return errors + ["answers must be a list"]
    ids = [answer.get("id") for answer in answers if isinstance(answer, dict)]
    if ids != EXPECTED_IDS:
        errors.append(f"answer IDs/order must be {EXPECTED_IDS}, got {ids}")

    seen_names: set[str] = set()
    for index, answer in enumerate(answers):
        label = f"answers[{index}]"
        if not isinstance(answer, dict):
            errors.append(f"{label} must be an object")
            continue
        answer_id = answer.get("id", label)
        missing = REQUIRED_ANSWER_FIELDS - set(answer)
        if missing:
            errors.append(f"{answer_id}: missing fields {sorted(missing)}")
        for field in REQUIRED_ANSWER_FIELDS - {"state", "claim_atoms"}:
            if field in answer and not nonempty(answer[field]):
                errors.append(f"{answer_id}: {field} must be non-empty")

        name = answer.get("name")
        if isinstance(name, str):
            if name in seen_names:
                errors.append(f"{answer_id}: duplicate name {name}")
            seen_names.add(name)

        selected = str(answer.get("selected_internal_answer", "")).lower()
        for phrase in BARRED_IN_SELECTED_ANSWERS:
            if phrase in selected:
                errors.append(f"{answer_id}: selected answer contains barred inflation {phrase!r}")

        required_mode = ANSWER_MODE_REQUIREMENTS.get(str(answer_id))
        if required_mode is not None:
            if answer.get("answer_mode") != required_mode:
                errors.append(
                    f"{answer_id}: answer_mode must be {required_mode!r}"
                )
            if not nonempty(answer.get("native_question_debt")):
                errors.append(f"{answer_id}: native_question_debt must be non-empty")

        state = answer.get("state")
        if not isinstance(state, dict) or set(state) != STATE_AXES:
            errors.append(f"{answer_id}: state must contain exactly the five axes")
        else:
            for axis, value in state.items():
                if value not in ALLOWED_STATE_VALUES[axis]:
                    errors.append(f"{answer_id}: invalid {axis} value {value!r}")
            if state.get("owner_adoption") != "ADOPTED":
                errors.append(f"{answer_id}: owner_adoption must be ADOPTED")
            if state.get("internal_review") != "PASS":
                errors.append(f"{answer_id}: internal_review must be PASS")
            if state.get("pqa_adjudication") != "NOT_EVALUATED":
                errors.append(f"{answer_id}: adoption may not advance PQA adjudication")
            if state.get("publication") != "WITHHELD":
                errors.append(f"{answer_id}: this local packet must remain WITHHELD")

        owners = answer.get("semantic_owners", [])
        if isinstance(owners, list):
            for owner in owners:
                if not isinstance(owner, str) or not source_path(owner).is_file():
                    errors.append(f"{answer_id}: semantic owner does not resolve: {owner!r}")
        else:
            errors.append(f"{answer_id}: semantic_owners must be a list")

        atoms = answer.get("claim_atoms")
        if not isinstance(atoms, list) or not atoms:
            errors.append(f"{answer_id}: claim_atoms must be a non-empty list")
            continue
        for atom_index, atom in enumerate(atoms):
            atom_label = f"{answer_id}.claim_atoms[{atom_index}]"
            if not isinstance(atom, dict):
                errors.append(f"{atom_label} must be an object")
                continue
            for field in ("text", "claim_type", "tier", "source"):
                if not nonempty(atom.get(field)):
                    errors.append(f"{atom_label}.{field} must be non-empty")
            if atom.get("claim_type") not in CLAIM_TYPES:
                errors.append(f"{atom_label}: invalid claim_type {atom.get('claim_type')!r}")
            tier = atom.get("tier")
            if not isinstance(tier, str) or not re.fullmatch(r"\[[A-Z](?:/[A-Z])?\]", tier):
                errors.append(f"{atom_label}: malformed tier {tier!r}")
            source = atom.get("source")
            if not isinstance(source, str) or not source_path(source).is_file():
                errors.append(f"{atom_label}: source does not resolve: {source!r}")
            elif not source_anchor_exists(source):
                errors.append(f"{atom_label}: source anchor does not resolve: {source!r}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} Emergentist answer-set error(s)")
        return 1
    print("PASS: EmergentistAnswerSet.v1 — 10 answers, 5 independent axes, debts retained")
    return 0


if __name__ == "__main__":
    sys.exit(main())

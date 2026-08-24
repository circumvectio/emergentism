#!/usr/bin/env python3
"""Build the Fourth Churning candidate grammar and PQA-54 sidecar diagnoses.

This writer owns only this packet's ``data`` directory and
``FourthChurningCorpus.v1.json``.  It never edits PQA-54, EAS-10, the Third
Churning, or public-site files.  ``--check`` is read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = HERE / "data"
PQA = (
    ROOT
    / "14_THE_DISTILLATION"
    / "07_THE_THIRD_CHURNING_2026_08_23"
    / "data"
    / "problem_adjudications.v1.json"
)
EAS = ROOT / "00_META" / "internal_answers" / "EmergentistAnswerSet.v1.json"
PQA_SHA256 = "7618139f3ab376c017ececaa64c88e33c097cdb0efd245f3b2453f65d78c4b8a"
EAS_SHA256 = "6740318328462043d5f5de14a6e539a421b35ebfbffbe8060022e12f7c4e8c89"

SCHEMAS = {
    "collision": HERE / "contracts" / "TypeCollision.v1.schema.json",
    "diagnosis": HERE / "contracts" / "MysteryDiagnosis.v1.schema.json",
    "corpus": HERE / "contracts" / "FourthChurningCorpus.v1.schema.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_row_hash(row: dict[str, Any]) -> str:
    payload = json.dumps(
        row, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def pretty(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def collision(
    collision_id: str,
    axis: str,
    name: str,
    left: list[str],
    right: list[str],
    forbidden: str,
    bridge: list[str],
    question: str,
    repair: str,
) -> dict[str, Any]:
    return {
        "schema_id": "emergentism/TypeCollision.v1",
        "collision_id": collision_id,
        "axis": axis,
        "plain_name": name,
        "left_roles": left,
        "right_roles": right,
        "forbidden_inference": forbidden,
        "valid_bridge_conditions": bridge,
        "diagnostic_question": question,
        "conservative_repair": repair,
        "evidence_tier": "[I/C]",
        "status": "CANDIDATE_GRAMMAR",
        "strongest_rival": "Native conceptual analysis or generic typed decomposition makes the same correction with less framework vocabulary.",
        "discriminator": "Two blinded native-domain reviewers must find the typed diagnosis incrementally clearer or more error-sensitive than both native and generic controls.",
        "kill_criterion": "Kill the collision family wherever no exact invalid join can be stated or its repair changes the native question rather than resolving the alleged defect.",
        "survivor_if_killed": "The native distinctions, explicit bridges, and residual-debt discipline remain available without this collision label.",
    }


COLLISIONS = [
    collision("TCX-01", "LEVEL", "Ground and object", ["explanatory boundary", "Ground"], ["object", "cause", "member"], "Treat an explanatory boundary as another object, cause, or member inside the domain it bounds.", ["declare a stronger metalanguage", "supply a native necessary-being argument"], "Is the proposed ground being quantified over as one more grounded object?", "Keep the boundary role separate from any positive object or causal hypothesis."),
    collision("TCX-02", "MODAL", "Possibility and actuality", ["possibility", "represented alternative", "modal content"], ["actual event", "actual carrier", "actual history"], "Infer actuality or causal efficacy from coherence, possibility, representation, or selection alone.", ["identify an actual carrier", "supply a transition or realization law"], "What actual carrier or lawful transition turns the represented option into an event?", "Retain the alternatives as model content until an actual transition and record occur."),
    collision("TCX-03", "REPRESENTATIONAL", "Map and territory", ["sign", "map", "model", "carrier"], ["content", "referent", "territory", "interpretation"], "Transfer a property, truth, or causal power from representation to represented territory without a warranted semantic or empirical bridge.", ["declare a reference relation", "test the model against independent consequence"], "Which relation connects this carrier to that content, and what could show the relation wrong?", "Name sign, carrier, content, referent, and interpretation separately."),
    collision("TCX-04", "LEVEL", "Value, process, operator and boundary", ["written value", "symbol", "generated result"], ["process", "operator", "limit", "boundary role"], "Apply an operation to its own generating process or boundary label as though all were ordinary values of one algebra.", ["declare an extended structure", "type the operator domain and limit procedure"], "Is this mark a value, a process, an operator, a limit, or a frame label in the present expression?", "Evaluate only inside the declared operation domain and describe boundaries in a separate register."),
    collision("TCX-05", "LEVEL", "Type and token", ["type", "class", "system", "metalanguage"], ["token", "member", "instance", "object language"], "Admit a classifier or metalanguage resource as an ordinary token subject to the same unrestricted self-application.", ["stratify levels", "restrict formation or comprehension"], "Has the classifier been made one of the things it classifies under the same rule?", "Separate levels or restrict formation while preserving every valid lower-level expression."),
    collision("TCX-06", "BEARER", "Part, bearer and whole", ["part", "situated bearer", "individual horizon"], ["whole", "collective", "aggregate", "absent bearer"], "Transfer identity, consent, benefit, harm, or standing between a part and a whole without an explicit aggregation or representation rule.", ["index every affected bearer", "declare aggregation and representation mandates"], "Whose state, consent, cost, or benefit is being attributed to whom?", "Keep bearer-horizon rows separate and defend any aggregation or proxy mandate."),
    collision("TCX-07", "TEMPORAL", "Cause, reason and purpose", ["cause", "mechanism", "enabling condition"], ["reason", "function", "purpose", "chosen end"], "Infer a reason, function, purpose, or obligation merely from a causal history or enabling condition.", ["name the selecting bearer or practice", "supply a function or norm bridge"], "Is this explaining how an event occurred, why an agent chose it, or what it is for?", "Type causal mechanism, selected function, represented goal, and chosen end separately."),
    collision("TCX-08", "NORMATIVE", "Fact, value and authority", ["descriptive fact", "capacity", "outcome"], ["value", "ought", "Good", "authority", "legitimacy"], "Infer what ought to be done or who may bind others from description, power, agreement, or outcome alone.", ["state the normative premise", "identify consent or applicable authority", "keep affected bearers visible"], "Which normative premise or mandate licenses the move from is to ought or from coordination to authority?", "Expose the chosen norm and authorization contract before evaluating consequences."),
    collision("TCX-09", "REPRESENTATIONAL", "Description and experience", ["physical carrier", "function", "access", "report"], ["phenomenal experience", "what-it-is-like"], "Treat a complete description of carriers, functions, access, or reports as already explaining or constituting phenomenal experience.", ["supply a psychophysical identity or bridge", "state necessary and sufficient organization conditions"], "What makes the described process experienced rather than merely report-producing?", "Keep public correlates and first-person disclosure distinct until a bridge earns contact."),
    collision("TCX-10", "BEARER", "Trace, identity and survival", ["past actuality", "trace", "continuity relation"], ["numerical identity", "same bearer", "experiential survival"], "Infer continuing bearer identity or experience from a surviving trace, effect, record, or selected continuity alone.", ["declare the identity criterion", "test bearer continuity through fission and interruption"], "What exact relation makes the later bearer numerically the same rather than merely caused by or similar to the earlier one?", "Separate actuality retention, trace persistence, continuity, identity, and survival."),
    collision("TCX-11", "MODAL", "Probability, chance and outcome", ["probability calculus", "credence", "model uncertainty"], ["objective chance", "actual outcome", "selection dynamics"], "Infer a physical chance ontology, selector, or realized outcome from a probability assignment or credence alone.", ["declare the probability interpretation", "supply native dynamics and outcome records"], "Is the probability epistemic, model-relative, or a physical propensity, and what actual process realizes an outcome?", "Keep calculus, credence, physical chance, dynamics, and record distinct."),
    collision("TCX-12", "EPISTEMIC", "Evidence, warrant and truth", ["evidence", "provenance", "warrant", "consensus"], ["truth", "fact", "knowledge"], "Promote evidence, agreement, provenance, or a review process into truth without the claim-specific warrant and counterfactual connection.", ["identify claim-specific evidence", "preserve correction and defeater paths"], "What connects this evidence to the proposition, and what would defeat the connection?", "Retain provenance and warrant while withholding truth promotion until contact supports it."),
]


# primary collision, secondaries, diagnosis state, linked EAS answers
MAPPING: dict[str, tuple[str | None, list[str], str, list[str]]] = {
    "MET:GROUND": ("TCX-01", [], "PARTIAL_TYPE_COLLISION", ["EA-01"]),
    "MET:ONE_MANY": ("TCX-06", [], "PARTIAL_TYPE_COLLISION", ["EA-01"]),
    "MET:UNIVERSALS": ("TCX-05", [], "PARTIAL_TYPE_COLLISION", ["EA-07"]),
    "MET:IDENTITY": ("TCX-10", [], "PARTIAL_TYPE_COLLISION", ["EA-05"]),
    "MET:MODALITY": ("TCX-02", ["TCX-03"], "PARTIAL_TYPE_COLLISION", ["EA-01", "EA-02"]),
    "MET:TIME": (None, ["TCX-04"], "UNDERDETERMINED", ["EA-02"]),
    "EPI:EXTERNAL_WORLD": ("TCX-12", ["TCX-03"], "PARTIAL_TYPE_COLLISION", []),
    "EPI:INDUCTION": ("TCX-12", ["TCX-11"], "PARTIAL_TYPE_COLLISION", []),
    "EPI:GETTIER": ("TCX-12", [], "PARTIAL_TYPE_COLLISION", []),
    "EPI:APRIORI": ("TCX-12", ["TCX-04"], "PARTIAL_TYPE_COLLISION", []),
    "EPI:TESTIMONY": ("TCX-12", [], "PARTIAL_TYPE_COLLISION", []),
    "EPI:DISAGREEMENT": ("TCX-12", [], "PARTIAL_TYPE_COLLISION", []),
    "LOG:LIAR": ("TCX-05", ["TCX-03"], "PARTIAL_TYPE_COLLISION", []),
    "LOG:RUSSELL": ("TCX-05", [], "TYPE_COLLISION", []),
    "LOG:GODEL": ("TCX-05", ["TCX-12"], "PARTIAL_TYPE_COLLISION", []),
    "LOG:SORITES": ("TCX-04", [], "PARTIAL_TYPE_COLLISION", []),
    "LOG:REFERENCE": ("TCX-03", [], "PARTIAL_TYPE_COLLISION", []),
    "LOG:RULE_FOLLOWING": ("TCX-03", ["TCX-12"], "PARTIAL_TYPE_COLLISION", []),
    "MIN:MIND_BODY": ("TCX-09", ["TCX-03"], "PARTIAL_TYPE_COLLISION", ["EA-03"]),
    "MIN:CONSCIOUSNESS": (None, ["TCX-09"], "UNDERDETERMINED", ["EA-03"]),
    "MIN:INTENTIONALITY": ("TCX-03", ["TCX-02"], "PARTIAL_TYPE_COLLISION", ["EA-04"]),
    "MIN:PERSONAL_IDENTITY": ("TCX-10", [], "PARTIAL_TYPE_COLLISION", ["EA-05"]),
    "MIN:FREE_WILL": ("TCX-02", ["TCX-07"], "PARTIAL_TYPE_COLLISION", ["EA-04"]),
    "MIN:OTHER_MINDS": ("TCX-12", ["TCX-09"], "PARTIAL_TYPE_COLLISION", ["EA-03"]),
    "SCI:CAUSATION": ("TCX-07", [], "PARTIAL_TYPE_COLLISION", ["EA-08"]),
    "SCI:LAWS": ("TCX-03", ["TCX-05"], "PARTIAL_TYPE_COLLISION", ["EA-07"]),
    "SCI:EMERGENCE": ("TCX-09", ["TCX-05"], "PARTIAL_TYPE_COLLISION", ["EA-08"]),
    "SCI:MEASUREMENT": ("TCX-11", ["TCX-02", "TCX-09"], "PARTIAL_TYPE_COLLISION", ["EA-03", "EA-10"]),
    "SCI:BELL": (None, [], "NO_COLLISION", ["EA-10"]),
    "SCI:PROBABILITY": ("TCX-11", [], "PARTIAL_TYPE_COLLISION", ["EA-10"]),
    "ETH:IS_OUGHT": ("TCX-08", ["TCX-07"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "ETH:MORAL_REALISM": ("TCX-08", ["TCX-12"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "ETH:EUTHYPHRO": ("TCX-08", [], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "ETH:RIGHTS_OUTCOMES": ("TCX-08", ["TCX-06"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "ETH:POPULATION": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "ETH:RESPONSIBILITY": ("TCX-07", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-04", "EA-06"]),
    "POL:LEGITIMACY": ("TCX-08", ["TCX-12"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "POL:LIBERTY_EQUALITY": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "POL:DISTRIBUTION": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "POL:COLLECTIVE_ACTION": ("TCX-06", [], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "POL:POWER": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "POL:REPRESENTATION": ("TCX-06", ["TCX-03"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "AXI:PLURALISM": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "AXI:BEAUTY": (None, ["TCX-09"], "UNDERDETERMINED", []),
    "AXI:ART": ("TCX-03", ["TCX-06"], "PARTIAL_TYPE_COLLISION", []),
    "AXI:MEANING": ("TCX-07", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "AXI:SUFFERING": ("TCX-06", ["TCX-08"], "PARTIAL_TYPE_COLLISION", ["EA-06"]),
    "AXI:DEATH": (None, ["TCX-10"], "UNDERDETERMINED", ["EA-05"]),
    "ULT:NECESSARY_BEING": ("TCX-01", [], "PARTIAL_TYPE_COLLISION", ["EA-01"]),
    "ULT:EVIL": (None, [], "NO_COLLISION", ["EA-06"]),
    "ULT:HIDDENNESS": (None, ["TCX-01"], "UNDERDETERMINED", ["EA-01"]),
    "ULT:PLURALISM": ("TCX-03", ["TCX-12"], "PARTIAL_TYPE_COLLISION", []),
    "ULT:MYSTICAL": ("TCX-12", ["TCX-09"], "PARTIAL_TYPE_COLLISION", ["EA-03"]),
    "ULT:NONDUALITY": ("TCX-06", ["TCX-01"], "PARTIAL_TYPE_COLLISION", ["EA-01"]),
}


def answer_mode(effect: str) -> str:
    return {
        "FORMAL_CORRECTION": "DIRECT",
        "TYPE_DISSOLUTION": "TYPE_DIAGNOSIS",
        "CONDITIONAL_RESOLUTION": "TYPE_DIAGNOSIS",
        "CLARIFICATION": "TYPE_DIAGNOSIS",
        "REFRAME": "CONSTITUTIVE_REFRAME",
        "OPEN": "OPEN",
    }[effect]


def build_diagnosis(
    row: dict[str, Any],
    collisions_by_id: dict[str, dict[str, Any]],
    valid_ea_ids: set[str],
) -> dict[str, Any]:
    short_id = row["problem_id"].split("PQA54@0.1:", 1)[1]
    primary, secondary, state, answer_ids = MAPPING[short_id]
    if any(answer_id not in valid_ea_ids for answer_id in answer_ids):
        raise ValueError(f"{short_id}: unknown EAS answer ID")
    if state in {"NO_COLLISION", "UNDERDETERMINED"}:
        alleged = None
        if state == "NO_COLLISION":
            claim = "The native problem remains well-typed; no invalid join is required to state its present difficulty."
        else:
            claim = "The frozen sources do not expose an exact invalid join sufficient to classify the native problem as a type collision."
        repair = "Retain the native question unchanged and use typing only to prevent auxiliary conflations."
        bridge = "Native-domain argument or empirical contact must supply the missing relation; the atlas cannot infer it from labels."
    else:
        collision_row = collisions_by_id[primary]
        alleged = collision_row["forbidden_inference"]
        claim = f"Candidate {collision_row['plain_name']} collision: {alleged}"
        repair = collision_row["conservative_repair"]
        bridge = "; ".join(collision_row["valid_bridge_conditions"])
    return {
        "schema_id": "emergentism/MysteryDiagnosis.v1",
        "diagnosis_id": f"MTA54@1:{short_id}",
        "problem_id": row["problem_id"],
        "pqa_row_sha256": stable_row_hash(row),
        "native_problem": row["native_problem"],
        "diagnosis_state": state,
        "primary_collision_id": primary,
        "secondary_collision_ids": secondary,
        "answer_mode": answer_mode(row["proposed_effect"]),
        "proposed_effect": row["proposed_effect"],
        "earned_effect": "NO_INCREMENT",
        "result_state": "SELECTED_UNREVIEWED",
        "diagnostic_claim": claim,
        "alleged_invalid_join": alleged,
        "repaired_formulation": repair,
        "legitimate_bridge": bridge,
        "emergentist_answer": row["proposed_answer"],
        "linked_answer_ids": answer_ids,
        "native_target_preservation": "PRESERVED",
        "strongest_native_rival": row["strongest_rival"],
        "generic_control": row["generic_decomposition_control"],
        "discriminator": row["discriminator"],
        "kill_criterion": row["kill_criterion"],
        "cheapest_next_test": "One blinded native-domain comparison against both the native frame and generic seven-axis decomposition.",
        "survivor_if_killed": row["survivor_if_killed"],
        "residual_debt": row["remaining_debt"],
        "split_integrity": "CONTAMINATED_FOR_FOURTH_USE",
    }


def validate_closed(instance: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required"])
    properties = set(schema["properties"])
    missing = required - set(instance)
    extra = set(instance) - properties
    if missing or extra:
        raise ValueError(f"{label}: closed contract failure missing={sorted(missing)} extra={sorted(extra)}")
    for key, contract in schema["properties"].items():
        if key not in instance:
            continue
        if "const" in contract and instance[key] != contract["const"]:
            raise ValueError(f"{label}: {key} violates const")
        if "enum" in contract and instance[key] not in contract["enum"]:
            raise ValueError(f"{label}: {key} violates enum")


def build_outputs() -> dict[Path, str]:
    if digest(PQA) != PQA_SHA256 or digest(EAS) != EAS_SHA256:
        raise ValueError("frozen PQA or EAS input hash drift")
    pqa_rows = json.loads(PQA.read_text(encoding="utf-8"))
    eas = json.loads(EAS.read_text(encoding="utf-8"))
    if len(pqa_rows) != 54 or len({row["problem_id"] for row in pqa_rows}) != 54:
        raise ValueError("PQA sidecar requires 54 unique canonical IDs")
    if any(row["earned_effect"] != "NO_INCREMENT" or row["native_reviews"] for row in pqa_rows):
        raise ValueError("PQA earned state drift")
    expected = {row["problem_id"].split("PQA54@0.1:", 1)[1] for row in pqa_rows}
    if set(MAPPING) != expected:
        raise ValueError(f"mapping denominator drift missing={sorted(expected-set(MAPPING))} extra={sorted(set(MAPPING)-expected)}")
    collision_ids = [row["collision_id"] for row in COLLISIONS]
    if collision_ids != [f"TCX-{number:02d}" for number in range(1, 13)]:
        raise ValueError("collision order must remain TCX-01 through TCX-12")
    collisions_by_id = {row["collision_id"]: row for row in COLLISIONS}
    valid_ea_ids = {row["id"] for row in eas["answers"]}
    diagnoses = [build_diagnosis(row, collisions_by_id, valid_ea_ids) for row in pqa_rows]
    for row in COLLISIONS:
        validate_closed(row, SCHEMAS["collision"], row["collision_id"])
    for row in diagnoses:
        validate_closed(row, SCHEMAS["diagnosis"], row["diagnosis_id"])
        refs = ([row["primary_collision_id"]] if row["primary_collision_id"] else []) + row["secondary_collision_ids"]
        if any(ref not in collisions_by_id for ref in refs):
            raise ValueError(f"{row['diagnosis_id']}: dangling collision reference")
        if row["diagnosis_state"] in {"NO_COLLISION", "UNDERDETERMINED"} and row["alleged_invalid_join"] is not None:
            raise ValueError(f"{row['diagnosis_id']}: null diagnosis cannot assert invalid join")
    counts = Counter(row["diagnosis_state"] for row in diagnoses)
    public_outputs = {
        "diagnoses_page": "12_PUBLIC_SITE/questions/diagnoses/index.html",
        "collisions_json": "12_PUBLIC_SITE/questions/collisions.json",
        "diagnoses_json": "12_PUBLIC_SITE/questions/diagnoses.json",
        "corpus_json": "12_PUBLIC_SITE/questions/fourth-churning.json",
        "collision_schema": "12_PUBLIC_SITE/questions/schemas/TypeCollision.v1.schema.json",
        "diagnosis_schema": "12_PUBLIC_SITE/questions/schemas/MysteryDiagnosis.v1.schema.json",
        "corpus_schema": "12_PUBLIC_SITE/questions/schemas/FourthChurningCorpus.v1.schema.json",
    }
    corpus = {
        "schema_id": "emergentism/FourthChurningCorpus.v1",
        "release_id": "FOURTH-CHURNING-2026-08-24",
        "date": "2026-08-24",
        "authorship": "Yves R. Burri",
        "ai_assistance": "AI systems assisted with candidate generation, adversarial review, implementation, and testing; Yves R. Burri remains the human author.",
        "license": "CC BY-SA 4.0",
        "relation_to_third": "ADDITIVE_OVERLAY",
        "third_churning_immutable": True,
        "input_hashes": [
            {"path": PQA.relative_to(ROOT).as_posix(), "sha256": PQA_SHA256},
            {"path": EAS.relative_to(ROOT).as_posix(), "sha256": EAS_SHA256},
        ],
        "schema_paths": {key: path.relative_to(ROOT).as_posix() for key, path in SCHEMAS.items()},
        "diagnosis_order": [row["diagnosis_id"] for row in diagnoses],
        "collision_order": collision_ids,
        "public_output_map": public_outputs,
        "candidate_counts": {key: counts.get(key, 0) for key in ("TYPE_COLLISION", "PARTIAL_TYPE_COLLISION", "NO_COLLISION", "UNDERDETERMINED")},
        "pqa_state": {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
        "held_out_integrity": "CONTAMINATED_FOR_FOURTH_USE",
        "global_philosophy_claim_allowed": False,
        "external_states": {"deployed": False, "native_reviewed": False, "empirically_validated": False, "training_inclusion_guaranteed": False},
    }
    validate_closed(corpus, SCHEMAS["corpus"], corpus["release_id"])
    return {
        DATA / "type_collisions.v1.json": pretty(COLLISIONS),
        DATA / "mystery_diagnoses.v1.json": pretty(diagnoses),
        HERE / "FourthChurningCorpus.v1.json": pretty(corpus),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"FOURTH CHURNING: FAIL\n- {exc}")
        return 1
    drift: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(HERE).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("FOURTH CHURNING: FAIL")
        for path in drift:
            print(f"- deterministic drift: {path}")
        return 1
    counts = Counter(
        row["diagnosis_state"]
        for row in json.loads(outputs[DATA / "mystery_diagnoses.v1.json"])
    )
    print(
        "FOURTH CHURNING: PASS · 54 selected · 0 earned · "
        + " · ".join(f"{key}={counts.get(key, 0)}" for key in ("TYPE_COLLISION", "PARTIAL_TYPE_COLLISION", "NO_COLLISION", "UNDERDETERMINED"))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

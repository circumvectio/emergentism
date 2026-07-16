from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from .diagnostics import Issue
from .records import (
    RECEIPT_IDENTITIES,
    SOURCE_ROLE_MATRIX,
    core_record_shape_issues,
    malformed_core_issue,
    ordered_issues,
    valid_id,
    validate_record_graph,
)


EVIDENCE_ORDER = {"C": 0, "I": 1, "S": 2, "A": 3}
INDEPENDENCE_ORDER = {
    "NOT_INDEPENDENT": 0,
    "PARTIALLY_INDEPENDENT": 1,
    "INDEPENDENT": 2,
}
MODALITIES = frozenset({
    "ACTUAL", "POSSIBLE", "NECESSARY", "NORMATIVE", "DEFINITIONAL", "CONJECTURAL",
})
VERDICT_MATRIX = {
    "VALID_SOUND": frozenset({("VALID", "SUPPORTED")}),
    "VALID_CONDITIONAL": frozenset({("VALID", "CONDITIONALLY_SUPPORTED")}),
    "VALID_UNSUPPORTED_PREMISE": frozenset({("VALID", "UNSUPPORTED")}),
    "INVALID": frozenset({("INVALID", "NOT_APPLICABLE")}),
    "UNDERDETERMINED": frozenset({("INVALID", "NOT_APPLICABLE")}),
    "DEFINITIONAL": frozenset({("NOT_APPLICABLE", "NOT_APPLICABLE")}),
    "OPEN_CONJECTURE": frozenset({
        ("NOT_APPLICABLE", "UNSUPPORTED"),
        ("NOT_APPLICABLE", "CONDITIONALLY_SUPPORTED"),
    }),
    "REFUTED": frozenset({("VALID", "REFUTED"), ("NOT_APPLICABLE", "REFUTED")}),
}
SEMANTIC_EVALUATORS = frozenset({
    "VERDICT_MATRIX",
    "JUSTICE_CONTEXT",
    "RECEIPT_ROLE",
    "REGISTER_INDEX",
    "QUANTUM_MEASURE",
    "OPTION_CONE",
    "TROPHIC_AGGREGATOR",
    "ROSETTA_TRANSFER",
})


def _issue(path: str, code: str, message: str) -> Issue:
    return Issue(path, code, message)


def _typed_collection_issues(
    core: dict[str, Any], names: Iterable[str], *, code: str, root: str
) -> list[Issue]:
    result: list[Issue] = []
    for name in names:
        value = core.get(name)
        if not isinstance(value, list):
            result.append(_issue(
                f"{root}.{name}", code, f"{name} must be a list of objects",
            ))
        elif any(not isinstance(record, dict) for record in value):
            result.append(_issue(
                f"{root}.{name}", code, f"{name} must contain only objects",
            ))
    return result


def _identifier_list(value: Any) -> bool:
    return isinstance(value, list) and all(valid_id(item) for item in value)


def _text_list(value: Any) -> bool:
    return isinstance(value, list) and all(_scalar_text(item) for item in value)


def _records(core: dict[str, Any], name: str) -> list[dict[str, Any]]:
    value = core.get(name, [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _index(core: dict[str, Any], name: str, *, key: str = "id") -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in _records(core, name):
        value = record.get(key)
        if isinstance(value, str) and value not in result:
            result[value] = record
    return result


def _verdict_valid(record: dict[str, Any]) -> bool:
    return (
        record.get("validityVerdict"), record.get("soundnessVerdict")
    ) in VERDICT_MATRIX.get(record.get("verdict"), frozenset())


def _justice_context_shape(context: Any) -> bool:
    if not isinstance(context, dict) or set(context) != {
        "individual", "whole", "eta", "beneficiary", "costBearer", "consent",
        "custody", "reversibility", "exit", "optionConeEffect", "authority",
    }:
        return False
    text_fields = ("individual", "whole", "eta", "custody", "exit")
    if any(not _scalar_text(context.get(field)) for field in text_fields):
        return False
    for field in ("beneficiary", "costBearer"):
        values = context.get(field)
        if not isinstance(values, list) or not values or any(
            not _scalar_text(value) for value in values
        ):
            return False
    consent = context.get("consent")
    if not isinstance(consent, dict) or set(consent) != {"status", "basis"}:
        return False
    consent_status = consent.get("status")
    if (
        type(consent_status) is not str
        or consent_status not in {"OBTAINED", "NOT_REQUIRED", "MISSING"}
        or not _scalar_text(consent.get("basis"))
    ):
        return False
    reversibility = context.get("reversibility")
    if (
        type(reversibility) is not str
        or reversibility not in {"REVERSIBLE", "PARTIAL", "IRREVERSIBLE"}
    ):
        return False
    option = context.get("optionConeEffect")
    if not isinstance(option, dict) or set(option) != {"direction", "rationale"}:
        return False
    direction = option.get("direction")
    if (
        type(direction) is not str
        or direction not in {"WIDENS", "NEUTRAL", "CONTRACTS", "MIXED"}
        or not _scalar_text(option.get("rationale"))
    ):
        return False
    authority = context.get("authority")
    if not isinstance(authority, dict) or set(authority) != {"regime", "mechanism", "basis"}:
        return False
    regime = authority.get("regime")
    mechanism = authority.get("mechanism")
    return (
        type(regime) is str
        and regime in {"NOT_APPLICABLE", "PRIVATE_DAV", "PUBLIC_DAV", "OTHER"}
        and type(mechanism) is str
        and mechanism in {
            "NONE", "K2_NATURAL_PERSON", "PRISM_PUBLIC_GOVERNANCE",
            "CONSTITUTIONAL_AUTO_ENFORCEMENT", "OTHER",
        }
        and _scalar_text(authority.get("basis"))
    )


def _authority_valid(
    *, claim_type: Any, modality: Any, justice_scope: Any,
    authority_scope: Any, authority_effect: Any, lifecycle: Any,
    context: Any,
) -> bool:
    requires_context = (
        justice_scope in {"COLLECTIVE", "NORMATIVE", "COLLECTIVE_NORMATIVE"}
        or authority_effect != "NONE"
    )
    if claim_type == "NORMATIVE" or modality == "NORMATIVE":
        if justice_scope not in {"NORMATIVE", "COLLECTIVE_NORMATIVE"}:
            return False
    if requires_context and not isinstance(context, dict):
        return False
    if isinstance(context, dict) and not _justice_context_shape(context):
        return False
    if not requires_context and context is not None:
        return False
    if authority_effect == "NONE":
        if authority_scope != "NONE":
            return False
        if context is None:
            return True
        authority = context.get("authority")
        return isinstance(authority, dict) and (
            authority.get("regime"), authority.get("mechanism")
        ) == ("NOT_APPLICABLE", "NONE")
    if not isinstance(context, dict) or not isinstance(context.get("authority"), dict):
        return False
    authority = context["authority"]
    if authority_scope not in {"PRIVATE_DAV", "PUBLIC_DAV", "OTHER"}:
        return False
    if authority.get("regime") != authority_scope:
        return False
    mechanism = authority.get("mechanism")
    if authority_effect == "DESCRIPTIVE":
        if lifecycle == "RETIRED":
            return mechanism in {
                "NONE", "K2_NATURAL_PERSON", "PRISM_PUBLIC_GOVERNANCE",
                "CONSTITUTIONAL_AUTO_ENFORCEMENT", "OTHER",
            }
        return mechanism in {
            "PRIVATE_DAV": {"K2_NATURAL_PERSON"},
            "PUBLIC_DAV": {"PRISM_PUBLIC_GOVERNANCE", "CONSTITUTIONAL_AUTO_ENFORCEMENT"},
            "OTHER": {"OTHER"},
        }[authority_scope]
    if authority_effect in {"DISCRETIONARY", "CONSEQUENTIAL"}:
        return mechanism == {
            "PRIVATE_DAV": "K2_NATURAL_PERSON",
            "PUBLIC_DAV": "PRISM_PUBLIC_GOVERNANCE",
            "OTHER": "OTHER",
        }[authority_scope]
    if authority_effect == "CONSTITUTIONAL_AUTOMATIC":
        return authority_scope == "PUBLIC_DAV" and mechanism == "CONSTITUTIONAL_AUTO_ENFORCEMENT"
    return False


def _kill_shape_valid(criterion: Any, *, strength: Any, lifecycle: Any) -> bool:
    if not isinstance(criterion, dict):
        return False
    kind = criterion.get("kind")
    if lifecycle == "RETIRED":
        return kind == "NONE" and set(criterion) == {"kind", "rationale"}
    if kind != "TESTABLE":
        return False
    testability = criterion.get("testability")
    disposition = criterion.get("disposition")
    expected = {"kind", "testability", "trigger", "method", "disposition"}
    if testability == "DEFERRED":
        expected |= {"deferredReason", "unblockCondition"}
    elif testability != "ACTIVE":
        return False
    if disposition == "RETRACT":
        return set(criterion) == expected
    if disposition != "RETIER" or "resultingStrength" not in criterion:
        return False
    expected.add("resultingStrength")
    return (
        set(criterion) == expected
        and strength in EVIDENCE_ORDER
        and criterion.get("resultingStrength") in EVIDENCE_ORDER
        and EVIDENCE_ORDER[criterion["resultingStrength"]] < EVIDENCE_ORDER[strength]
    )


def _excluded_claim_ids(manifest: dict[str, Any]) -> set[str]:
    return {
        item.get("claimId")
        for item in manifest.get("excludedClaimIds", [])
        if isinstance(item, dict) and isinstance(item.get("claimId"), str)
    }


def _admissible_evidence_trials(
    core: dict[str, Any], *, phase: str | None = None,
    receipt_id: str | None = None,
) -> dict[str, set[str]]:
    """Return claim->trial IDs transported by the selected or verified inputs.

    A globally resolving claim is deliberately insufficient.  The current
    receipt transports only the non-excluded claim/trial inventory of its own
    manifest.  A dependency transports the same inventory only when the
    selected receipt names it and its receipt is VERIFIED with a bound bundle
    digest and path.
    """
    manifests = _index(core, "manifests")
    receipts = _index(core, "phaseReceipts")
    trials = _records(core, "trials")
    selected = [
        receipt for receipt in receipts.values()
        if (
            (receipt_id is not None and receipt.get("id") == receipt_id)
            or (
                receipt_id is None
                and phase is not None
                and receipt.get("phase") == phase
            )
        )
    ]
    result: dict[str, set[str]] = {}

    def add_transport(receipt: dict[str, Any], *, dependency: bool) -> None:
        manifest = manifests.get(receipt.get("manifestId"))
        if (
            manifest is None
            or manifest.get("phase") != receipt.get("phase")
            or (
                dependency
                and not (
                    receipt.get("status") == "VERIFIED"
                    and isinstance(receipt.get("validationBundlePath"), str)
                    and isinstance(receipt.get("validationDigest"), str)
                )
            )
        ):
            return
        allowed_claims = (
            set(manifest.get("harvestedClaimIds", []))
            & set(manifest.get("trialedClaimIds", []))
            & set(receipt.get("claimIds", []))
        ) - _excluded_claim_ids(manifest)
        listed_trials = set(receipt.get("trialIds", []))
        for trial in trials:
            claim_id = trial.get("claimId")
            trial_id = trial.get("id")
            if (
                claim_id in allowed_claims
                and trial_id in listed_trials
                and trial.get("manifestId") == manifest.get("id")
                and trial.get("receiptId") == receipt.get("id")
                and isinstance(claim_id, str)
                and isinstance(trial_id, str)
            ):
                result.setdefault(claim_id, set()).add(trial_id)

    for receipt in selected:
        add_transport(receipt, dependency=False)
        for dependency_id in receipt.get("dependsOnReceiptIds", []):
            dependency_receipt = receipts.get(dependency_id)
            if dependency_receipt is not None:
                add_transport(dependency_receipt, dependency=True)
        selected_manifest = manifests.get(receipt.get("manifestId"))
        if selected_manifest is not None:
            for claim_id in _excluded_claim_ids(selected_manifest):
                result.pop(claim_id, None)
    return result


def _supporting_trial(
    claim_id: str, trials_by_claim: dict[str, list[dict[str, Any]]], *,
    target_a: bool, admissible_trial_ids: dict[str, set[str]],
) -> bool:
    eligible = [
        trial for trial in trials_by_claim.get(claim_id, [])
        if trial.get("id") in admissible_trial_ids.get(claim_id, set())
        and trial.get("status") == "CLOSED"
        and trial.get("breakState") == "NONE"
        and trial.get("verdict") in (
            {"VALID_SOUND"} if target_a else {"VALID_SOUND", "VALID_CONDITIONAL"}
        )
        and _verdict_valid(trial)
    ]
    return bool(eligible)


def _validate_claims(core: dict[str, Any], *, phase: str | None) -> list[Issue]:
    result: list[Issue] = []
    claims = _index(core, "claims")
    receipts = _records(core, "phaseReceipts")
    trials_by_claim: dict[str, list[dict[str, Any]]] = {}
    for trial in _records(core, "trials"):
        claim_id = trial.get("claimId")
        if isinstance(claim_id, str):
            trials_by_claim.setdefault(claim_id, []).append(trial)
    admissibility_by_claim: dict[str, list[dict[str, set[str]]]] = {}
    if phase is None:
        admissibility_by_receipt: dict[str, dict[str, set[str]]] = {}
        for receipt in receipts:
            receipt_id = receipt.get("id")
            if isinstance(receipt_id, str):
                admissibility_by_receipt[receipt_id] = _admissible_evidence_trials(
                    core, receipt_id=receipt_id
                )
        for receipt in receipts:
            context = admissibility_by_receipt.get(receipt.get("id"))
            if context is None:
                continue
            for claim_id in receipt.get("claimIds", []):
                if isinstance(claim_id, str):
                    admissibility_by_claim.setdefault(claim_id, []).append(context)
    else:
        selected_context = _admissible_evidence_trials(core, phase=phase)

    for position, claim in enumerate(_records(core, "claims")):
        base = f"core.claims[{position}]"
        admissibility_contexts = (
            admissibility_by_claim.get(claim.get("id"), [])
            if phase is None else [selected_context]
        )
        is_normative = claim.get("claimType") == "NORMATIVE" or claim.get("modality") == "NORMATIVE"
        if is_normative:
            normative_premise = any(
                isinstance(premise, dict) and premise.get("role") == "NORMATIVE"
                for premise in claim.get("premises", [])
            )
            normative_dependency = any(
                dependency_id in claims and (
                    claims[dependency_id].get("claimType") == "NORMATIVE"
                    or claims[dependency_id].get("modality") == "NORMATIVE"
                )
                for dependency_id in claim.get("dependencyClaimIds", [])
            )
            if not (normative_premise or normative_dependency):
                result.append(_issue(base, "KIN-E-VERDICT", "normative conclusion lacks a normative premise or dependency"))

        dependencies = [
            claims[value] for value in claim.get("dependencyClaimIds", []) if value in claims
        ]
        if dependencies and not any(
            dependency.get("modality") == claim.get("modality") for dependency in dependencies
        ):
            result.append(_issue(
                f"{base}.modality", "KIN-E-VERDICT",
                "cross-modal conclusion lacks an explicit entailing dependency of the declared modality",
            ))

        evidence = claim.get("evidence", {})
        if not _kill_shape_valid(
            claim.get("killCriterion"), strength=evidence.get("strength"),
            lifecycle=evidence.get("lifecycle"),
        ):
            result.append(_issue(f"{base}.killCriterion", "KIN-E-STATE", "kill criterion does not match evidence strength/lifecycle"))
        if not _authority_valid(
            claim_type=claim.get("claimType"), modality=claim.get("modality"),
            justice_scope=claim.get("justiceScope"),
            authority_scope=claim.get("authorityScope"),
            authority_effect=claim.get("authorityEffect"),
            lifecycle=evidence.get("lifecycle"), context=claim.get("justiceContext"),
        ):
            result.append(_issue(f"{base}.justiceContext", "KIN-E-JUSTICE", "Justice/authority context is inconsistent"))

        for link_index, link in enumerate(claim.get("supportLinks", [])):
            if not isinstance(link, dict):
                continue
            path = f"{base}.supportLinks[{link_index}]"
            supporting = claims.get(link.get("supportingClaimId"))
            mode = link.get("mode")
            independence = link.get("independenceStatus")
            ceiling = link.get("evidenceCeiling")
            ceiling_valid = True
            if supporting is not None:
                support_evidence = supporting.get("evidence", {})
                ceiling_valid = (
                    ceiling in EVIDENCE_ORDER
                    and support_evidence.get("strength") in EVIDENCE_ORDER
                    and EVIDENCE_ORDER[ceiling] <= EVIDENCE_ORDER[support_evidence["strength"]]
                )
                if not ceiling_valid:
                    result.append(_issue(path, "KIN-E-VERDICT", "link ceiling exceeds the supporting claim"))
            if mode in {"ANALOGY", "ROSETTA_TRANSFER"}:
                if (independence, ceiling) != ("NOT_APPLICABLE", "I"):
                    result.append(_issue(path, "KIN-E-VERDICT", "analogy/Rosetta support is fixed at I/NOT_APPLICABLE"))
                continue
            if independence == "NOT_APPLICABLE":
                result.append(_issue(path, "KIN-E-VERDICT", "entailing support mode cannot use NOT_APPLICABLE independence"))
            if supporting is None:
                continue
            support_evidence = supporting.get("evidence", {})
            if not ceiling_valid:
                continue
            target_a = ceiling == "A"
            support_is_admissible = bool(admissibility_contexts) and all(
                _supporting_trial(
                    supporting.get("id"), trials_by_claim, target_a=target_a,
                    admissible_trial_ids=context,
                )
                for context in admissibility_contexts
            )
            if (
                support_evidence.get("lifecycle") != "ACTIVE"
                or not support_is_admissible
            ):
                result.append(_issue(path, "KIN-E-VERDICT", "supporting claim lacks one closed admissible active trial"))
            if target_a and (
                support_evidence.get("strength") != "A" or not support_evidence.get("sourced")
            ):
                result.append(_issue(path, "KIN-E-VERDICT", "A ceiling requires a sourced A supporting claim"))
    return result


def _validate_trial_states(core: dict[str, Any]) -> list[Issue]:
    result: list[Issue] = []
    discriminators = _index(core, "discriminators")
    for position, trial in enumerate(_records(core, "trials")):
        base = f"core.trials[{position}]"
        if not _verdict_valid(trial):
            result.append(_issue(base, "KIN-E-VERDICT", "trial verdict axes are inconsistent"))
        state = trial.get("breakState")
        status = trial.get("status")
        defect = trial.get("defectClass")
        severity = trial.get("severity")
        seam_id = trial.get("seamId")
        if state == "NONE":
            valid = status == "CLOSED" and defect is None and severity is None and seam_id is None
        elif state == "ALLEGED":
            valid = status in {"TRIED", "DISPUTED"} and defect is not None and severity is not None and seam_id is None
        elif state == "CONFIRMED":
            valid = status in {"ADJUDICATED", "CLOSED"} and defect is not None and severity is not None and seam_id is not None
        else:
            valid = False
        if not valid:
            result.append(_issue(base, "KIN-E-STATE", "trial break state fields are inconsistent"))
        if (
            state in {"ALLEGED", "CONFIRMED"}
            and trial.get("countermodel", {}).get("defeatedConclusion") == "NONE_FOUND"
            and not trial.get("discriminatorIds")
        ):
            result.append(_issue(base, "KIN-E-STATE", "open countermodel requires a discriminator"))
        for value in trial.get("discriminatorIds", []):
            discriminator = discriminators.get(value)
            if discriminator is not None and discriminator.get("claimId") != trial.get("claimId"):
                result.append(_issue(base, "KIN-E-STATE", "trial discriminator belongs to another claim"))
    return result


def _qualifying_upgrade(
    seam: dict[str, Any], claims: dict[str, dict[str, Any]],
    trials_by_claim: dict[str, list[dict[str, Any]]],
    admissible_trial_ids: dict[str, set[str]],
) -> bool:
    after = seam.get("evidenceAfter", {}).get("strength")
    criterion = seam.get("priorUpgradeCriterion")
    if not isinstance(criterion, dict) or criterion.get("kind") != "AVAILABLE":
        return False
    if criterion.get("targetStrength") != after:
        return False
    if (
        criterion.get("minimumEvidenceCeiling") not in EVIDENCE_ORDER
        or after not in EVIDENCE_ORDER
        or EVIDENCE_ORDER[criterion["minimumEvidenceCeiling"]] < EVIDENCE_ORDER[after]
    ):
        return False
    links = {
        link.get("id"): link for link in seam.get("supportLinks", []) if isinstance(link, dict)
    }
    link_ids = seam.get("upgradeEvidenceLinkIds")
    if not isinstance(link_ids, list) or not link_ids:
        return False
    has_independent_a = False
    for link_id in link_ids:
        link = links.get(link_id)
        if link is None or link.get("mode") != criterion.get("requiredMode"):
            return False
        independence = link.get("independenceStatus")
        minimum = criterion.get("minimumIndependence")
        if independence not in INDEPENDENCE_ORDER or minimum not in INDEPENDENCE_ORDER:
            return False
        if INDEPENDENCE_ORDER[independence] < INDEPENDENCE_ORDER[minimum]:
            return False
        ceiling = link.get("evidenceCeiling")
        minimum_ceiling = criterion.get("minimumEvidenceCeiling")
        if (
            ceiling not in EVIDENCE_ORDER
            or EVIDENCE_ORDER[ceiling] < EVIDENCE_ORDER[after]
            or EVIDENCE_ORDER[ceiling] < EVIDENCE_ORDER[minimum_ceiling]
        ):
            return False
        supporting = claims.get(link.get("supportingClaimId"))
        if supporting is None:
            return False
        evidence = supporting.get("evidence", {})
        if evidence.get("lifecycle") != "ACTIVE" or not _supporting_trial(
            supporting.get("id"), trials_by_claim, target_a=after == "A",
            admissible_trial_ids=admissible_trial_ids,
        ):
            return False
        if after == "A":
            has_independent_a = has_independent_a or (
                independence == "INDEPENDENT" and ceiling == "A"
                and evidence.get("strength") == "A" and evidence.get("sourced") is True
            )
    return after != "A" or has_independent_a


def _validate_seams(core: dict[str, Any], *, phase: str | None) -> list[Issue]:
    result: list[Issue] = []
    claims = _index(core, "claims")
    trials_by_claim: dict[str, list[dict[str, Any]]] = {}
    for trial in _records(core, "trials"):
        if isinstance(trial.get("claimId"), str):
            trials_by_claim.setdefault(trial["claimId"], []).append(trial)
    admissibility_by_receipt: dict[str | None, dict[str, set[str]]] = {}
    for position, seam in enumerate(_records(core, "seams")):
        base = f"core.seams[{position}]"
        claim = claims.get(seam.get("claimId"))
        if not _verdict_valid(seam):
            result.append(_issue(base, "KIN-E-VERDICT", "seam verdict axes are inconsistent"))
        lifecycle = (
            seam.get("evidenceAfter", {}).get("lifecycle")
            if seam.get("status") in {"REPAIRED", "RETRACTED", "VERIFIED"}
            else seam.get("evidenceBefore", {}).get("lifecycle")
        )
        if not _authority_valid(
            claim_type=seam.get("claimType"), modality=seam.get("modality"),
            justice_scope=seam.get("justiceScope"), authority_scope=seam.get("authorityScope"),
            authority_effect=seam.get("authorityEffect"), lifecycle=lifecycle,
            context=seam.get("justiceContext"),
        ):
            result.append(_issue(f"{base}.justiceContext", "KIN-E-JUSTICE", "seam Justice/authority context is inconsistent"))

        status = seam.get("status")
        prior_contract = (
            seam.get("priorSupportLinks"), seam.get("priorUpgradeCriterion"),
            seam.get("priorKillCriterion"), seam.get("priorSurvivingIfKilled"),
        )
        current_contract = (
            seam.get("supportLinks"), seam.get("upgradeCriterion"),
            seam.get("killCriterion"), seam.get("survivingIfKilled"),
        )
        if status in {"CONFIRMED", "HELD_OPEN"} and prior_contract != current_contract:
            result.append(_issue(base, "KIN-E-STATE", "unrepaired seam must preserve its prospective contract exactly"))
        if status in {"REPAIRED", "RETRACTED", "VERIFIED"} and claim is not None:
            expected = (
                claim.get("supportLinks"), claim.get("upgradeCriterion"),
                claim.get("killCriterion"), claim.get("survivingIfKilled"),
            )
            if current_contract != expected or seam.get("evidenceAfter") != claim.get("evidence"):
                result.append(_issue(base, "KIN-E-STATE", "repaired seam does not synchronize the current claim contract"))

        before = seam.get("evidenceBefore", {}).get("strength")
        after = seam.get("evidenceAfter", {}).get("strength") if isinstance(seam.get("evidenceAfter"), dict) else before
        repair_kind = seam.get("repairKind")
        changed = before != after
        evidence_before = seam.get("evidenceBefore", {})
        evidence_after = seam.get("evidenceAfter")
        before_lifecycle = evidence_before.get("lifecycle") if isinstance(evidence_before, dict) else None
        after_lifecycle = evidence_after.get("lifecycle") if isinstance(evidence_after, dict) else None
        receipt_id = seam.get("receiptId") if isinstance(seam.get("receiptId"), str) else None
        if receipt_id not in admissibility_by_receipt:
            admissibility_by_receipt[receipt_id] = _admissible_evidence_trials(
                core, phase=phase if receipt_id is None else None,
                receipt_id=receipt_id,
            )
        admissible_trial_ids = admissibility_by_receipt[receipt_id]
        if repair_kind == "RETIER":
            if (
                before_lifecycle not in {"DRAFT", "ACTIVE"}
                or after_lifecycle != before_lifecycle
            ):
                result.append(_issue(
                    base, "KIN-E-VERDICT",
                    "RETIER must preserve one non-retired evidence lifecycle",
                ))
            if not changed or before not in EVIDENCE_ORDER or after not in EVIDENCE_ORDER:
                result.append(_issue(base, "KIN-E-VERDICT", "RETIER requires unequal evidence strengths"))
            elif EVIDENCE_ORDER[after] > EVIDENCE_ORDER[before]:
                if not _qualifying_upgrade(
                    seam, claims, trials_by_claim, admissible_trial_ids
                ):
                    result.append(_issue(base, "KIN-E-VERDICT", "upward RETIER lacks its prospective criterion and qualifying evidence links"))
            else:
                kill = seam.get("priorKillCriterion")
                if not (
                    isinstance(kill, dict) and kill.get("kind") == "TESTABLE"
                    and kill.get("disposition") == "RETIER"
                    and kill.get("resultingStrength") == after
                ):
                    result.append(_issue(base, "KIN-E-VERDICT", "downward RETIER is not authorized by the prior kill criterion"))
                if seam.get("upgradeEvidenceLinkIds") is not None:
                    result.append(_issue(base, "KIN-E-VERDICT", "downward RETIER cannot carry upgrade-evidence links"))
        elif changed and status != "RETRACTED":
            result.append(_issue(base, "KIN-E-VERDICT", "only RETIER may change evidence strength"))

        if after_lifecycle == "RETIRED" and not (
            status == "RETRACTED" and repair_kind == "RETRACT"
        ):
            result.append(_issue(
                base, "KIN-E-VERDICT",
                "only a typed RETRACTED/RETRACT seam may retire evidence",
            ))

        if status == "RETRACTED":
            prior_kill = seam.get("priorKillCriterion")
            if not (
                repair_kind == "RETRACT" and before == after
                and seam.get("evidenceAfter", {}).get("lifecycle") == "RETIRED"
                and isinstance(prior_kill, dict) and prior_kill.get("kind") == "TESTABLE"
                and prior_kill.get("disposition") == "RETRACT"
                and seam.get("killCriterion", {}).get("kind") == "NONE"
                and claim is not None and claim.get("evidence", {}).get("lifecycle") == "RETIRED"
            ):
                result.append(_issue(base, "KIN-E-VERDICT", "RETRACTED must preserve strength and synchronize a retired claim"))
        if status == "HELD_OPEN" and not (
            isinstance(seam.get("containment"), dict)
            and isinstance(seam.get("residualRisk"), dict)
            and bool(seam.get("discriminatorIds"))
            and seam.get("repairKind") is None
            and seam.get("evidenceAfter") is None
        ):
            result.append(_issue(base, "KIN-E-STATE", "HELD_OPEN requires containment, residual risk, and a discriminator without repair"))
        current_evidence = seam.get("evidenceAfter") if isinstance(seam.get("evidenceAfter"), dict) else seam.get("evidenceBefore", {})
        if not _kill_shape_valid(
            seam.get("killCriterion"), strength=current_evidence.get("strength"),
            lifecycle=current_evidence.get("lifecycle"),
        ):
            result.append(_issue(f"{base}.killCriterion", "KIN-E-STATE", "seam kill criterion does not match current evidence"))
    return result


def _validate_gates(core: dict[str, Any]) -> list[Issue]:
    result: list[Issue] = []
    receipts = _index(core, "phaseReceipts")
    for position, seam in enumerate(_records(core, "seams")):
        base = f"core.seams[{position}]"
        receipt = receipts.get(seam.get("receiptId"))
        if receipt is None:
            continue
        status = receipt.get("status")
        gates = {
            "truthGate": receipt.get("logicReviewPath"),
            "beautyGate": receipt.get("btjReviewPath"),
            "justiceGate": receipt.get("btjReviewPath"),
        }
        for field, reviewer_path in gates.items():
            gate = seam.get(field)
            if not isinstance(gate, dict):
                result.append(_issue(f"{base}.{field}", "KIN-E-STATE", "gate object is absent"))
                continue
            if status == "DRAFT":
                valid = gate.get("status") == "PENDING" and gate.get("reviewerPath") is None
            else:
                valid = gate.get("status") == "PASS" and gate.get("reviewerPath") == reviewer_path
            if not valid:
                result.append(_issue(f"{base}.{field}", "KIN-E-STATE", "gate state/path does not match the referencing receipt"))
        if seam.get("status") == "VERIFIED" and any(
            seam.get(field, {}).get("status") != "PASS" for field in gates
        ):
            result.append(_issue(base, "KIN-E-STATE", "VERIFIED seam requires all PASS gates"))
    return result


def _validate_core_records_unchecked(
    core: dict[str, object], *, phase: str | None = None, bootstrap: bool = False
) -> list[Issue]:
    result = list(validate_record_graph(core, phase=phase, bootstrap=bootstrap))
    if core.get("program", {}).get("noK2Gate") is not True:
        result.append(_issue("core.program.noK2Gate", "KIN-E-JUSTICE", "Kintsugi has no K2 gate"))
    result.extend(_validate_claims(core, phase=phase))
    result.extend(_validate_trial_states(core))
    result.extend(_validate_seams(core, phase=phase))
    result.extend(_validate_gates(core))
    result.extend(_validate_antibody_contract(core))
    return ordered_issues(result)


def validate_core_records(
    core: dict[str, object], *, phase: str | None = None, bootstrap: bool = False
) -> list[Issue]:
    shape_issues = core_record_shape_issues(core)
    if shape_issues:
        return shape_issues
    try:
        return _validate_core_records_unchecked(
            core,
            phase=phase,
            bootstrap=bootstrap,
        )
    except Exception:
        return [malformed_core_issue()]


def _public_queue_shape_issues(
    queue: dict[str, Any], core: dict[str, Any]
) -> list[Issue]:
    result = _typed_collection_issues(
        core, ("manifests", "phaseReceipts", "sources", "claims", "seams"),
        code="KIN-E-QUEUE", root="core",
    )
    for field in ("manifestId", "receiptId"):
        if not valid_id(queue.get(field)):
            result.append(_issue(
                f"publicQueue.{field}", "KIN-E-QUEUE",
                f"{field} must be a canonical identifier",
            ))
    items = queue.get("items")
    if not isinstance(items, list):
        result.append(_issue(
            "publicQueue.items", "KIN-E-QUEUE", "queue items must be a list",
        ))
        return ordered_issues(result)
    for position, item in enumerate(items):
        base = f"publicQueue.items[{position}]"
        if not isinstance(item, dict):
            result.append(_issue(base, "KIN-E-QUEUE", "queue item must be an object"))
            continue
        public_file = item.get("publicFile")
        if not _scalar_text(public_file):
            result.append(_issue(
                f"{base}.publicFile", "KIN-E-QUEUE",
                "public file must be non-empty Unicode scalar text",
            ))
        else:
            try:
                _safe_path_segments(public_file, pattern=False)
            except ValueError as exc:
                result.append(_issue(f"{base}.publicFile", "KIN-E-QUEUE", str(exc)))
        current = item.get("currentEvidence")
        if (
            not isinstance(current, dict)
            or type(current.get("strength")) is not str
            or current.get("strength") not in EVIDENCE_ORDER
        ):
            result.append(_issue(
                f"{base}.currentEvidence", "KIN-E-QUEUE",
                "current evidence must carry a closed evidence strength",
            ))
        maximum = item.get("maximumPublicStrength")
        if type(maximum) is not str or maximum not in EVIDENCE_ORDER:
            result.append(_issue(
                f"{base}.maximumPublicStrength", "KIN-E-QUEUE",
                "maximum public strength must use the closed evidence order",
            ))
        ownership = item.get("ownership")
        if type(ownership) is not str or ownership not in {"OWNED", "OWNERLESS"}:
            result.append(_issue(
                f"{base}.ownership", "KIN-E-QUEUE",
                "ownership must use the closed queue union",
            ))
            continue
        if ownership == "OWNED":
            for field in ("ownerSourceId", "claimId"):
                if not valid_id(item.get(field)):
                    result.append(_issue(
                        f"{base}.{field}", "KIN-E-QUEUE",
                        f"{field} must be a canonical identifier",
                    ))
            if not _identifier_list(item.get("seamIds")):
                result.append(_issue(
                    f"{base}.seamIds", "KIN-E-QUEUE",
                    "owned seam IDs must be a list of canonical identifiers",
                ))
        else:
            search = item.get("ownerSearchEvidence")
            if not isinstance(search, dict):
                result.append(_issue(
                    f"{base}.ownerSearchEvidence", "KIN-E-QUEUE",
                    "ownerless item requires typed search evidence",
                ))
                continue
            for field in ("manifestIds", "searchedSourceIds"):
                if not _identifier_list(search.get(field)):
                    result.append(_issue(
                        f"{base}.ownerSearchEvidence.{field}", "KIN-E-QUEUE",
                        f"{field} must be a list of canonical identifiers",
                    ))
            if not _text_list(item.get("candidateOwners")):
                result.append(_issue(
                    f"{base}.candidateOwners", "KIN-E-QUEUE",
                    "candidate owners must be a list of Unicode paths",
                ))
    return ordered_issues(result)


def validate_public_queue(
    queue: dict[str, object], core: dict[str, object]
) -> list[Issue]:
    if not isinstance(queue, dict) or not isinstance(core, dict):
        return [_issue("publicQueue", "KIN-E-QUEUE", "queue and core must be objects")]
    try:
        shape_issues = _public_queue_shape_issues(queue, core)
        if shape_issues:
            return shape_issues
        return _validate_public_queue_unchecked(queue, core)
    except Exception:
        return [_issue(
            "publicQueue", "KIN-E-QUEUE",
            "queue validation failed safely on malformed nested data",
        )]


def _validate_public_queue_unchecked(
    queue: dict[str, object], core: dict[str, object]
) -> list[Issue]:
    result: list[Issue] = []
    manifests = _index(core, "manifests")
    receipts = _index(core, "phaseReceipts")
    sources = _index(core, "sources")
    claims = _index(core, "claims")
    seams = _index(core, "seams")
    manifest = manifests.get(queue.get("manifestId"))
    receipt = receipts.get(queue.get("receiptId"))
    manifest_paths = {
        record.get("path") for record in manifest.get("includedFiles", [])
        if isinstance(record, dict)
    } if manifest is not None else set()
    manifest_claim_ids = (
        set(manifest.get("harvestedClaimIds", [])) - _excluded_claim_ids(manifest)
        if manifest is not None else set()
    )
    expected_receipt = RECEIPT_IDENTITIES["C"]
    if manifest is None or manifest.get("phase") != "C":
        result.append(_issue("publicQueue.manifestId", "KIN-E-QUEUE", "queue manifest must resolve to Phase C"))
    if (
        receipt is None
        or receipt.get("phase") != "C"
        or receipt.get("manifestId") != queue.get("manifestId")
        or (receipt.get("id"), receipt.get("path")) != expected_receipt[:2]
    ):
        result.append(_issue("publicQueue.receiptId", "KIN-E-QUEUE", "queue receipt must resolve to the same Phase-C manifest"))

    for position, item in enumerate(queue.get("items", [])):
        if not isinstance(item, dict):
            result.append(_issue(f"publicQueue.items[{position}]", "KIN-E-QUEUE", "queue item must be an object"))
            continue
        base = f"publicQueue.items[{position}]"
        if manifest is not None and item.get("publicFile") not in manifest_paths:
            result.append(_issue(
                f"{base}.publicFile", "KIN-E-QUEUE",
                "public file is outside the selected Phase-C manifest inventory",
            ))
        current = item.get("currentEvidence", {}).get("strength")
        maximum = item.get("maximumPublicStrength")
        if current in EVIDENCE_ORDER and maximum in EVIDENCE_ORDER and EVIDENCE_ORDER[current] > EVIDENCE_ORDER[maximum]:
            result.append(_issue(base, "KIN-E-QUEUE", "current public evidence exceeds its declared maximum"))
        if item.get("ownership") == "OWNED":
            source = sources.get(item.get("ownerSourceId"))
            claim = claims.get(item.get("claimId"))
            if source is None or source.get("authorityRole") != "SEMANTIC_OWNER":
                result.append(_issue(f"{base}.ownerSourceId", "KIN-E-QUEUE", "owned item source is not a semantic owner"))
            if claim is None or claim.get("ownerSourceId") != item.get("ownerSourceId"):
                result.append(_issue(f"{base}.claimId", "KIN-E-QUEUE", "owned item claim/owner membership does not agree"))
            if (
                manifest is not None
                and (
                    item.get("claimId") not in manifest_claim_ids
                    or receipt is None
                    or item.get("claimId") not in receipt.get("claimIds", [])
                )
            ):
                result.append(_issue(
                    f"{base}.claimId", "KIN-E-QUEUE",
                    "owned claim is not admissible in the selected Phase-C manifest and receipt",
                ))
            if manifest is not None and source is not None:
                if manifest.get("phase") not in source.get("phases", []) or source.get("path") not in manifest_paths:
                    result.append(_issue(f"{base}.ownerSourceId", "KIN-E-QUEUE", "owned source is not eligible under the selected manifest"))
            owner_strength = claim.get("evidence", {}).get("strength") if claim is not None else None
            if (
                owner_strength in EVIDENCE_ORDER
                and maximum in EVIDENCE_ORDER
                and EVIDENCE_ORDER[maximum] > EVIDENCE_ORDER[owner_strength]
            ):
                result.append(_issue(base, "KIN-E-QUEUE", "maximum public strength exceeds the owner claim"))
            if (
                owner_strength in EVIDENCE_ORDER
                and current in EVIDENCE_ORDER
                and EVIDENCE_ORDER[current] > EVIDENCE_ORDER[owner_strength]
            ):
                result.append(_issue(base, "KIN-E-QUEUE", "current public evidence exceeds the owner claim"))
            if item.get("requiredAction") == "KEEP" and (
                item.get("driftClass") is not None or item.get("severity") is not None
            ):
                result.append(_issue(base, "KIN-E-QUEUE", "KEEP requires null drift and severity"))
            for seam_id in item.get("seamIds", []):
                seam = seams.get(seam_id)
                if seam is None:
                    result.append(_issue(f"{base}.seamIds", "KIN-E-QUEUE", "owned queue seam does not resolve"))
                elif (
                    seam.get("claimId") != item.get("claimId")
                    or seam.get("ownerSource") != item.get("ownerSourceId")
                ):
                    result.append(_issue(
                        f"{base}.seamIds", "KIN-E-QUEUE",
                        "owned queue seam belongs to another claim or owner",
                    ))
        elif item.get("ownership") == "OWNERLESS":
            if item.get("requiredAction") not in {"RETRACT", "REGENERATE"}:
                result.append(_issue(f"{base}.requiredAction", "KIN-E-QUEUE", "ownerless item permits only RETRACT or REGENERATE"))
            search = item.get("ownerSearchEvidence")
            if not isinstance(search, dict):
                result.append(_issue(f"{base}.ownerSearchEvidence", "KIN-E-QUEUE", "ownerless item lacks typed search evidence"))
                continue
            selected_manifests: list[dict[str, Any]] = []
            for manifest_id in search.get("manifestIds", []):
                selected = manifests.get(manifest_id)
                if selected is None:
                    result.append(_issue(f"{base}.ownerSearchEvidence.manifestIds", "KIN-E-QUEUE", "owner-search manifest does not resolve"))
                else:
                    selected_manifests.append(selected)
            searched_ids = set(search.get("searchedSourceIds", []))
            if any(source_id not in sources for source_id in searched_ids):
                result.append(_issue(f"{base}.ownerSearchEvidence.searchedSourceIds", "KIN-E-QUEUE", "owner-search source does not resolve"))
            eligible_ids: set[str] = set()
            for selected in selected_manifests:
                paths = {
                    record.get("path") for record in selected.get("includedFiles", [])
                    if isinstance(record, dict)
                }
                for source_id, source in sources.items():
                    if (
                        source.get("authorityRole") == "SEMANTIC_OWNER"
                        and selected.get("phase") in source.get("phases", [])
                        and source.get("path") in paths
                    ):
                        eligible_ids.add(source_id)
            if not searched_ids.issubset(eligible_ids):
                result.append(_issue(
                    f"{base}.ownerSearchEvidence.searchedSourceIds", "KIN-E-QUEUE",
                    "owner search includes a source outside the manifest-bounded semantic-owner set",
                ))
            candidates = item.get("candidateOwners", [])
            if not candidates and searched_ids != eligible_ids:
                result.append(_issue(f"{base}.ownerSearchEvidence", "KIN-E-QUEUE", "empty candidates require a complete manifest-bounded owner search"))
            searched_paths = {
                sources[source_id].get("path")
                for source_id in searched_ids
                if source_id in eligible_ids and source_id in sources
            }
            if any(candidate not in searched_paths for candidate in candidates):
                result.append(_issue(f"{base}.candidateOwners", "KIN-E-QUEUE", "candidate is outside the searched semantic-owner set"))
        else:
            result.append(_issue(f"{base}.ownership", "KIN-E-QUEUE", "unknown queue ownership union"))
    return ordered_issues(result)


def _semantic_verdict(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    return _verdict_valid(payload)


def _semantic_justice(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    return _authority_valid(
        claim_type=payload.get("claimType"), modality=payload.get("modality"),
        justice_scope=payload.get("justiceScope"), authority_scope=payload.get("authorityScope"),
        authority_effect=payload.get("authorityEffect"), lifecycle=payload.get("evidenceLifecycle"),
        context=payload.get("justiceContext"),
    )


def _semantic_receipt_role(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    requested = payload.get("requestedUse")
    if payload.get("recordKind") == "SOURCE_RECORD":
        if any(payload.get(field) is not None for field in ("receiptId", "phase", "status")):
            return False
        kind = payload.get("sourceKind")
        role = payload.get("authorityRole")
        if role not in SOURCE_ROLE_MATRIX.get(kind, frozenset()):
            return False
        return (
            (requested == "PROVENANCE" and role == "PROVENANCE")
            or (requested == "CLAIM_OWNER" and (kind, role) == ("OWNER", "SEMANTIC_OWNER"))
        )
    if payload.get("recordKind") != "PHASE_RECEIPT":
        return False
    if payload.get("sourceKind") is not None or payload.get("authorityRole") is not None:
        return False
    phase = payload.get("phase")
    expected = RECEIPT_IDENTITIES.get(phase)
    if expected is None or (payload.get("receiptId"), payload.get("path")) != expected[:2]:
        return False
    if payload.get("status") not in {"DRAFT", "COMPLETE", "VERIFIED"}:
        return False
    if requested in {"PROVENANCE", "CANONICAL_PHASE_RECEIPT"}:
        return True
    return requested == "PHASE_DEPENDENCY" and payload.get("status") == "VERIFIED"


def _semantic_register(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    if payload.get("requestedInference") != "TYPED_REFERENCE":
        return False
    same = payload.get("fromRegister") == payload.get("toRegister")
    relation = payload.get("relation")
    bridge = payload.get("bridgeClaimId")
    claims = _index(core, "claims")
    return (
        (same and relation == "SAME_REGISTER" and bridge is None)
        or (not same and relation == "DISTINCT_TYPED_TERM" and bridge is None)
        or (not same and relation == "EXPLICIT_BRIDGE" and bridge in claims)
    )


def _semantic_quantum(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    pair = (payload.get("probabilityObject"), payload.get("requestedOperation"))
    return pair in {
        ("EVENT_MEASURE", "SAMPLE_OUTCOME"),
        ("NORMALIZATION_SCALAR", "CHECK_NORMALIZATION"),
    } and payload.get("interpretiveClaim") in {"NONE", "CORRESPONDENCE"}


def _semantic_option(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    return tuple(payload.get(field) for field in (
        "physicalConstraint", "optionClaim", "futureInfluence", "commitmentKind",
    )) == ("C_BOUNDED", "MODELED_REACHABILITY", "ANTICIPATORY_MODEL", "PARTIAL_RELATION")


def _semantic_trophic(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    inference = payload.get("requestedInference")
    if inference == "LITERAL_ENERGY_LAW":
        return False
    proxy = (
        payload.get("quantityKind") == "HUMAN_INVESTMENT_PROXY"
        and payload.get("aggregationBasis") == "DECLARED_PROXY"
        and payload.get("conservationClaim") == "NONE"
    )
    physical = (
        payload.get("quantityKind") == "PHYSICAL_ENERGY"
        and payload.get("aggregationBasis") == "MEASURED_PHYSICAL_SUM"
        and payload.get("conservationClaim") == "EMPIRICALLY_TESTED"
    )
    if inference == "DESCRIPTIVE_AGGREGATION":
        return proxy or physical
    return inference == "EGREGOREOTYPE_CANDIDATE" and proxy and all(
        payload.get(field) is True for field in (
            "persistentSharedTrace", "carrierTurnoverObserved", "laterSelectionReweightingObserved",
        )
    )


def _semantic_rosetta(payload: dict[str, Any], core: dict[str, Any]) -> bool:
    claims = _index(core, "claims")
    if payload.get("targetClaimId") not in claims:
        return False
    bridge = payload.get("bridgeClaimId")
    if bridge is not None and bridge not in claims:
        return False
    return payload.get("requestedTransfer") in {"VOCABULARY", "QUESTION", "TOPOLOGY"}


def _scalar_text(value: Any, *, nonempty: bool = True) -> bool:
    if not isinstance(value, str) or (nonempty and not value):
        return False
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        return False
    return True


_MAX_INNER_JSON_CODEPOINTS = 262_144
_MAX_INNER_JSON_DEPTH = 64
_MAX_INNER_JSON_NODES = 16_384


def _preflight_inner_json(raw: Any) -> None:
    if not _scalar_text(raw):
        raise ValueError("semantic fixture payload must be non-empty Unicode scalar JSON text")
    if len(raw) > _MAX_INNER_JSON_CODEPOINTS:
        raise ValueError("semantic fixture payload exceeds the deterministic text bound")
    stack: list[str] = []
    in_string = False
    escaped = False
    containers = 0
    pairs = {"}": "{", "]": "["}
    for character in raw:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            stack.append(character)
            containers += 1
            if len(stack) > _MAX_INNER_JSON_DEPTH:
                raise ValueError("semantic fixture payload exceeds the deterministic depth bound")
            if containers > _MAX_INNER_JSON_NODES:
                raise ValueError("semantic fixture payload exceeds the deterministic node bound")
        elif character in "]}":
            if not stack or stack.pop() != pairs[character]:
                raise ValueError("semantic fixture payload has mismatched containers")
    if in_string or stack:
        raise ValueError("semantic fixture payload has an unterminated string or container")


def _bounded_inner_json_tree(value: Any) -> None:
    pending: list[tuple[Any, int]] = [(value, 0)]
    nodes = 0
    while pending:
        child, depth = pending.pop()
        nodes += 1
        if nodes > _MAX_INNER_JSON_NODES:
            raise ValueError("semantic fixture payload exceeds the deterministic node bound")
        if depth > _MAX_INNER_JSON_DEPTH:
            raise ValueError("semantic fixture payload exceeds the deterministic depth bound")
        if isinstance(child, dict):
            for key, nested in child.items():
                if not _scalar_text(key):
                    raise ValueError("semantic fixture object keys must be Unicode scalar text")
                pending.append((nested, depth + 1))
        elif isinstance(child, list):
            pending.extend((nested, depth + 1) for nested in child)
        elif isinstance(child, str):
            if not _scalar_text(child, nonempty=False):
                raise ValueError("semantic fixture text must contain only Unicode scalars")
        elif child is None or type(child) in {bool, int}:
            continue
        elif type(child) is float:
            if not math.isfinite(child):
                raise ValueError("semantic fixture numbers must be finite")
        else:
            raise ValueError("semantic fixture payload contains a non-JSON value")


def _decode_semantic_payload(raw: Any) -> Any:
    _preflight_inner_json(raw)

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = child
        return value

    decoded = json.loads(
        raw,
        object_pairs_hook=closed_object,
        parse_constant=reject_constant,
    )
    _bounded_inner_json_tree(decoded)
    return decoded


def _closed_enum(*values: str) -> Callable[[Any], bool]:
    allowed = frozenset(values)
    return lambda value: type(value) is str and value in allowed


def _nullable(validator: Callable[[Any], bool]) -> Callable[[Any], bool]:
    return lambda value: value is None or validator(value)


def _identifier(value: Any) -> bool:
    return (
        _scalar_text(value)
        and "A" <= value[0] <= "Z"
        and all(
            "A" <= character <= "Z"
            or "0" <= character <= "9"
            or character in "_-"
            for character in value[1:]
        )
    )


def _register_id(value: Any) -> bool:
    return (
        _scalar_text(value)
        and "A" <= value[0] <= "Z"
        and all(
            "A" <= character <= "Z"
            or "0" <= character <= "9"
            or character == "_"
            for character in value[1:]
        )
    )


def _schema_path(value: Any) -> bool:
    if (
        not _scalar_text(value)
        or value.startswith("/")
        or value.endswith("/")
        or "\\" in value
    ):
        return False
    segments = value.split("/")
    return all(segment and segment not in {".", ".."} for segment in segments)


def _justice_payload_context(value: Any) -> bool:
    return value is None or _justice_context_shape(value)


_CLAIM_TYPE = _closed_enum(
    "MATHEMATICAL", "STRUCTURAL", "INTERPRETIVE", "EMPIRICAL", "NORMATIVE",
    "METAPHORICAL",
)
_MODALITY = _closed_enum(*sorted(MODALITIES))
_JUSTICE_SCOPE = _closed_enum(
    "NONE", "INDIVIDUAL", "COLLECTIVE", "NORMATIVE", "COLLECTIVE_NORMATIVE",
)


SEMANTIC_PAYLOAD_FIELDS: dict[str, dict[str, Callable[[Any], bool]]] = {
    "VERDICT_MATRIX": {
        "validityVerdict": _closed_enum("VALID", "INVALID", "NOT_APPLICABLE"),
        "soundnessVerdict": _closed_enum(
            "SUPPORTED", "CONDITIONALLY_SUPPORTED", "UNSUPPORTED", "REFUTED",
            "NOT_APPLICABLE",
        ),
        "verdict": _closed_enum(*VERDICT_MATRIX),
    },
    "JUSTICE_CONTEXT": {
        "claimType": _CLAIM_TYPE,
        "modality": _MODALITY,
        "justiceScope": _JUSTICE_SCOPE,
        "authorityScope": _closed_enum("NONE", "PRIVATE_DAV", "PUBLIC_DAV", "OTHER"),
        "authorityEffect": _closed_enum(
            "NONE", "DESCRIPTIVE", "DISCRETIONARY", "CONSEQUENTIAL",
            "CONSTITUTIONAL_AUTOMATIC",
        ),
        "evidenceLifecycle": _closed_enum("DRAFT", "ACTIVE", "RETIRED"),
        "justiceContext": _justice_payload_context,
    },
    "RECEIPT_ROLE": {
        "recordKind": _closed_enum("SOURCE_RECORD", "PHASE_RECEIPT"),
        "sourceKind": _nullable(_closed_enum(
            "OWNER", "SUPPORT", "COMPRESSION", "PUBLIC", "RECEIPT",
        )),
        "authorityRole": _nullable(_closed_enum(
            "SEMANTIC_OWNER", "EVIDENCE", "DERIVATIVE", "PROVENANCE",
        )),
        "receiptId": _nullable(_identifier),
        "phase": _nullable(_closed_enum("A", "B", "C")),
        "path": _schema_path,
        "status": _nullable(_closed_enum("DRAFT", "COMPLETE", "VERIFIED")),
        "requestedUse": _closed_enum(
            "PROVENANCE", "CLAIM_OWNER", "PHASE_DEPENDENCY", "EVIDENCE_UPGRADE",
            "CANONICAL_PHASE_RECEIPT",
        ),
    },
    "REGISTER_INDEX": {
        "symbol": _scalar_text,
        "fromRegister": _register_id,
        "toRegister": _register_id,
        "relation": _closed_enum(
            "SAME_REGISTER", "DISTINCT_TYPED_TERM", "EXPLICIT_BRIDGE",
            "UNMARKED_SUBSTITUTION",
        ),
        "bridgeClaimId": _nullable(_identifier),
        "requestedInference": _closed_enum("TYPED_REFERENCE", "ENTAILMENT", "MECHANISM"),
    },
    "QUANTUM_MEASURE": {
        "probabilityObject": _closed_enum("EVENT_MEASURE", "NORMALIZATION_SCALAR"),
        "requestedOperation": _closed_enum("SAMPLE_OUTCOME", "CHECK_NORMALIZATION"),
        "interpretiveClaim": _closed_enum(
            "NONE", "CORRESPONDENCE", "LITERAL_EXTRA_DIMENSION", "UNIVERSAL_COLLAPSE",
        ),
    },
    "OPTION_CONE": {
        "physicalConstraint": _closed_enum("C_BOUNDED", "SUPERLUMINAL"),
        "optionClaim": _closed_enum("MODELED_REACHABILITY", "PHYSICAL_CONE_EXPANSION"),
        "futureInfluence": _closed_enum("ANTICIPATORY_MODEL", "PHYSICAL_RETROCAUSALITY"),
        "commitmentKind": _closed_enum("PARTIAL_RELATION", "TOTAL_PREDICTOR"),
    },
    "TROPHIC_AGGREGATOR": {
        "quantityKind": _closed_enum("HUMAN_INVESTMENT_PROXY", "PHYSICAL_ENERGY"),
        "aggregationBasis": _closed_enum(
            "DECLARED_PROXY", "MEASURED_PHYSICAL_SUM", "METAPHORICAL",
        ),
        "conservationClaim": _closed_enum("NONE", "EMPIRICALLY_TESTED", "ASSUMED"),
        "persistentSharedTrace": lambda value: type(value) is bool,
        "carrierTurnoverObserved": lambda value: type(value) is bool,
        "laterSelectionReweightingObserved": lambda value: type(value) is bool,
        "requestedInference": _closed_enum(
            "DESCRIPTIVE_AGGREGATION", "EGREGOREOTYPE_CANDIDATE", "LITERAL_ENERGY_LAW",
        ),
    },
    "ROSETTA_TRANSFER": {
        "targetClaimId": _identifier,
        "bridgeClaimId": _nullable(_identifier),
        "fromRegister": _register_id,
        "toRegister": _register_id,
        "requestedTransfer": _closed_enum(
            "VOCABULARY", "QUESTION", "TOPOLOGY", "ENTAILMENT", "MECHANISM",
            "NECESSITY", "EVIDENCE_UPGRADE",
        ),
    },
}


SEMANTIC_DISPATCH: dict[
    str, tuple[set[str], Callable[[dict[str, Any], dict[str, Any]], bool]]
] = {
    "VERDICT_MATRIX": (
        {"validityVerdict", "soundnessVerdict", "verdict"}, _semantic_verdict,
    ),
    "JUSTICE_CONTEXT": ({
        "claimType", "modality", "justiceScope", "authorityScope", "authorityEffect",
        "evidenceLifecycle", "justiceContext",
    }, _semantic_justice),
    "RECEIPT_ROLE": ({
        "recordKind", "sourceKind", "authorityRole", "receiptId", "phase", "path",
        "status", "requestedUse",
    }, _semantic_receipt_role),
    "REGISTER_INDEX": ({
        "symbol", "fromRegister", "toRegister", "relation", "bridgeClaimId",
        "requestedInference",
    }, _semantic_register),
    "QUANTUM_MEASURE": (
        {"probabilityObject", "requestedOperation", "interpretiveClaim"}, _semantic_quantum,
    ),
    "OPTION_CONE": (
        {"physicalConstraint", "optionClaim", "futureInfluence", "commitmentKind"},
        _semantic_option,
    ),
    "TROPHIC_AGGREGATOR": ({
        "quantityKind", "aggregationBasis", "conservationClaim", "persistentSharedTrace",
        "carrierTurnoverObserved", "laterSelectionReweightingObserved", "requestedInference",
    }, _semantic_trophic),
    "ROSETTA_TRANSFER": ({
        "targetClaimId", "bridgeClaimId", "fromRegister", "toRegister",
        "requestedTransfer",
    }, _semantic_rosetta),
}


@dataclass(frozen=True)
class _SemanticExecution:
    predicate_passed: bool | None
    execution_issues: tuple[Issue, ...]


def _execute_semantic_fixture(
    evaluator: Any, payload: Any, core: Any
) -> _SemanticExecution:
    try:
        entry = SEMANTIC_DISPATCH.get(evaluator)
        if entry is None:
            return _SemanticExecution(None, (_issue(
                "semanticFixture.evaluator", "KIN-E-FIXTURE",
                "unknown semantic evaluator",
            ),))
        _bounded_inner_json_tree(payload)
        keys, predicate = entry
        fields = SEMANTIC_PAYLOAD_FIELDS[evaluator]
        if (
            not isinstance(payload, dict)
            or set(payload) != keys
            or set(fields) != keys
            or any(not validator(payload[field]) for field, validator in fields.items())
        ):
            return _SemanticExecution(None, (_issue(
                "semanticFixture.payload", "KIN-E-FIXTURE",
                "semantic payload does not match the exact named evaluator definition",
            ),))
        passed = predicate(payload, core if isinstance(core, dict) else {})
        if type(passed) is not bool:
            raise TypeError("semantic predicate must return bool")
    except Exception:
        return _SemanticExecution(None, (_issue(
            "semanticFixture.payload", "KIN-E-FIXTURE",
            "semantic payload validation failed safely",
        ),))
    return _SemanticExecution(passed, ())


def evaluate_semantic_fixture(
    evaluator: str, payload: dict[str, object], core: dict[str, object]
) -> list[Issue]:
    execution = _execute_semantic_fixture(evaluator, payload, core)
    if execution.execution_issues:
        return list(execution.execution_issues)
    return [] if execution.predicate_passed else [_issue(
        "semanticFixture.payload", "KIN-E-FIXTURE",
        f"{evaluator} structural predicate failed",
    )]


class _RegexSyntax(ValueError):
    pass


_ESCAPABLE = frozenset(".^$|?*+()[]-\\")


class _RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.position = 0

    def peek(self) -> str | None:
        return self.pattern[self.position] if self.position < len(self.pattern) else None

    def take(self) -> str:
        value = self.peek()
        if value is None:
            raise _RegexSyntax("unexpected end of pattern")
        self.position += 1
        return value

    def parse(self) -> tuple[Any, bool, bool]:
        anchored_start = self.peek() == "^"
        if anchored_start:
            self.position += 1
        ast = self.expression(stop=None)
        anchored_end = False
        if self.peek() == "$" and self.position == len(self.pattern) - 1:
            anchored_end = True
            self.position += 1
        if self.position != len(self.pattern):
            raise _RegexSyntax("unsupported or misplaced token")
        return ast, anchored_start, anchored_end

    def expression(self, stop: str | None) -> Any:
        branches = [self.branch(stop)]
        while self.peek() == "|":
            self.position += 1
            branches.append(self.branch(stop))
        return branches[0] if len(branches) == 1 else ("alt", tuple(branches))

    def branch(self, stop: str | None) -> Any:
        pieces: list[Any] = []
        while (
            self.peek() is not None
            and self.peek() != "|"
            and self.peek() != stop
            and self.peek() != "$"
        ):
            pieces.append(self.piece())
        if not pieces:
            raise _RegexSyntax("empty regex branch")
        return pieces[0] if len(pieces) == 1 else ("concat", tuple(pieces))

    def piece(self) -> Any:
        atom = self.atom()
        if self.peek() in {"?", "*", "+"}:
            quantifier = self.take()
            atom = ("quant", quantifier, atom)
        if self.peek() in {"?", "*", "+"}:
            raise _RegexSyntax("multiple quantifiers on one atom")
        return atom

    def escaped(self) -> str:
        self.take()
        value = self.take()
        if value not in _ESCAPABLE:
            raise _RegexSyntax("escape may quote only a declared metacharacter")
        return value

    def atom(self) -> Any:
        value = self.peek()
        if value is None:
            raise _RegexSyntax("missing atom")
        if value == ".":
            self.position += 1
            return ("dot",)
        if value == "\\":
            return ("literal", self.escaped())
        if value == "(":
            self.position += 1
            nested = self.expression(stop=")")
            if self.peek() != ")":
                raise _RegexSyntax("unclosed group")
            self.position += 1
            return nested
        if value == "[":
            return self.character_class()
        if value in "^$|?*+()[]":
            raise _RegexSyntax("unsupported or misplaced metacharacter")
        self.position += 1
        return ("literal", value)

    def class_literal(self) -> str:
        value = self.peek()
        if value is None:
            raise _RegexSyntax("unclosed character class")
        if value == "\\":
            return self.escaped()
        if value in "]-":
            raise _RegexSyntax("malformed character-class item")
        self.position += 1
        return value

    def character_class(self) -> Any:
        self.take()
        negated = self.peek() == "^"
        if negated:
            self.position += 1
        ranges: list[tuple[int, int]] = []
        while self.peek() not in {None, "]"}:
            start = self.class_literal()
            end = start
            if self.peek() == "-":
                self.position += 1
                end = self.class_literal()
                if ord(end) < ord(start):
                    raise _RegexSyntax("character-class ranges must ascend")
            ranges.append((ord(start), ord(end)))
        if self.peek() != "]":
            raise _RegexSyntax("unclosed character class")
        self.position += 1
        if not ranges:
            raise _RegexSyntax("empty character class")
        return ("class", negated, tuple(ranges))


@dataclass
class _NfaState:
    epsilon: set[int]
    edges: list[tuple[Any, int]]


class _NfaCompiler:
    def __init__(self):
        self.states: list[_NfaState] = []

    def new(self) -> int:
        if len(self.states) >= 1024:
            raise _RegexSyntax("compiled NFA exceeds 1024 states")
        self.states.append(_NfaState(set(), []))
        return len(self.states) - 1

    def compile(self, node: Any) -> tuple[int, int]:
        kind = node[0]
        if kind in {"literal", "dot", "class"}:
            start, end = self.new(), self.new()
            self.states[start].edges.append((node, end))
            return start, end
        if kind == "concat":
            fragments = [self.compile(child) for child in node[1]]
            for (_, left_end), (right_start, _) in zip(fragments, fragments[1:]):
                self.states[left_end].epsilon.add(right_start)
            return fragments[0][0], fragments[-1][1]
        if kind == "alt":
            start, end = self.new(), self.new()
            for child in node[1]:
                child_start, child_end = self.compile(child)
                self.states[start].epsilon.add(child_start)
                self.states[child_end].epsilon.add(end)
            return start, end
        if kind == "quant":
            quantifier, child = node[1], node[2]
            start, end = self.new(), self.new()
            child_start, child_end = self.compile(child)
            self.states[start].epsilon.add(child_start)
            self.states[child_end].epsilon.add(end)
            if quantifier in {"?", "*"}:
                self.states[start].epsilon.add(end)
            if quantifier in {"*", "+"}:
                self.states[child_end].epsilon.add(child_start)
            return start, end
        raise _RegexSyntax("unknown regex AST node")


def _epsilon_closure(states: list[_NfaState], seeds: Iterable[int]) -> frozenset[int]:
    result = set(seeds)
    pending = list(result)
    while pending:
        state = pending.pop()
        for target in states[state].epsilon:
            if target not in result:
                result.add(target)
                pending.append(target)
    return frozenset(result)


def _matches(matcher: Any, character: str) -> bool:
    kind = matcher[0]
    if kind == "literal":
        return character == matcher[1]
    if kind == "dot":
        return character != "\n"
    codepoint = ord(character)
    inside = any(start <= codepoint <= end for start, end in matcher[2])
    return not inside if matcher[1] else inside


def safe_regex_search(pattern: str, source: str) -> tuple[bool, list[Issue]]:
    try:
        if not isinstance(pattern, str) or not isinstance(source, str):
            raise _RegexSyntax("pattern and source must be Unicode strings")
        pattern.encode("utf-8", errors="strict")
        source.encode("utf-8", errors="strict")
        if len(pattern) > 256:
            raise _RegexSyntax("pattern exceeds 256 Unicode code points")
        ast, anchored_start, anchored_end = _RegexParser(pattern).parse()
        compiler = _NfaCompiler()
        start, accept = compiler.compile(ast)
        states = compiler.states
        start_closure = _epsilon_closure(states, (start,))
        current = start_closure
        if accept in current and not anchored_end:
            return True, []
        for character in source:
            advanced: set[int] = set()
            for state in current:
                for matcher, target in states[state].edges:
                    if _matches(matcher, character):
                        advanced.add(target)
            current = _epsilon_closure(states, advanced)
            if not anchored_start:
                current = frozenset(set(current) | set(start_closure))
            if accept in current and not anchored_end:
                return True, []
        return accept in current, []
    except (UnicodeError, _RegexSyntax, ValueError, OverflowError) as exc:
        return False, [_issue("regex", "KIN-E-FIXTURE", str(exc))]


def _safe_path_segments(value: Any, *, pattern: bool) -> tuple[str, ...]:
    if (
        not _scalar_text(value) or value.startswith("/")
        or value.endswith("/") or "\\" in value
    ):
        raise ValueError("path/glob must be a non-empty repository-relative POSIX path")
    segments = tuple(value.split("/"))
    if any(not segment or segment in {".", ".."} for segment in segments):
        raise ValueError("path/glob contains an empty or dot segment")
    if pattern:
        for segment in segments:
            if any(character in segment for character in "?[]\\{}()!+@"):
                raise ValueError("safe glob contains syntax outside the closed * and ** grammar")
            if "**" in segment and segment != "**":
                raise ValueError("** is legal only as a complete segment")
    elif any(
        "*" in segment or any(character in segment for character in "?[]")
        for segment in segments
    ):
        raise ValueError("repository path contains glob syntax")
    return segments


def _segment_match(pattern: str, value: str) -> bool:
    pattern_index = value_index = 0
    star = -1
    retry = 0
    while value_index < len(value):
        if pattern_index < len(pattern) and pattern[pattern_index] == value[value_index]:
            pattern_index += 1
            value_index += 1
        elif pattern_index < len(pattern) and pattern[pattern_index] == "*":
            star = pattern_index
            retry = value_index
            pattern_index += 1
        elif star >= 0:
            retry += 1
            value_index = retry
            pattern_index = star + 1
        else:
            return False
    return all(character == "*" for character in pattern[pattern_index:])


def _glob_match(pattern: str, path: str) -> bool:
    pattern_segments = _safe_path_segments(pattern, pattern=True)
    path_segments = _safe_path_segments(path, pattern=False)

    def epsilon_closure(states: set[int]) -> set[int]:
        closed = set(states)
        pending = list(states)
        while pending:
            index = pending.pop()
            if index < len(pattern_segments) and pattern_segments[index] == "**":
                target = index + 1
                if target not in closed:
                    closed.add(target)
                    pending.append(target)
        return closed

    states = epsilon_closure({0})
    for segment in path_segments:
        advanced: set[int] = set()
        for index in states:
            if index >= len(pattern_segments):
                continue
            token = pattern_segments[index]
            if token == "**":
                advanced.add(index)
            elif _segment_match(token, segment):
                advanced.add(index + 1)
        states = epsilon_closure(advanced)
        if not states:
            return False
    return len(pattern_segments) in states


def _antibody_shape_issues(core: dict[str, Any]) -> list[Issue]:
    result = _typed_collection_issues(
        core, ("antibodies",), code="KIN-E-FIXTURE", root="core",
    )
    antibodies = core.get("antibodies")
    if not isinstance(antibodies, list):
        return ordered_issues(result)
    seen_ids: set[str] = set()
    for position, antibody in enumerate(antibodies):
        base = f"core.antibodies[{position}]"
        if not isinstance(antibody, dict):
            continue
        antibody_id = antibody.get("id")
        if not valid_id(antibody_id):
            result.append(_issue(
                f"{base}.id", "KIN-E-FIXTURE",
                "antibody ID must be a canonical identifier",
            ))
        elif antibody_id in seen_ids:
            result.append(_issue(
                f"{base}.id", "KIN-E-FIXTURE", "antibody ID must be unique",
            ))
        else:
            seen_ids.add(antibody_id)
        mode = antibody.get("matchMode")
        if type(mode) is not str or mode not in {
            "LITERAL", "REGEX", "SEMANTIC_FIXTURE",
        }:
            result.append(_issue(
                f"{base}.matchMode", "KIN-E-FIXTURE",
                "antibody match mode is outside the closed registry",
            ))
        if not _scalar_text(antibody.get("pattern")):
            result.append(_issue(
                f"{base}.pattern", "KIN-E-FIXTURE",
                "antibody pattern must be non-empty Unicode scalar text",
            ))
        evaluator = antibody.get("semanticEvaluator")
        if mode == "SEMANTIC_FIXTURE":
            if type(evaluator) is not str or evaluator not in SEMANTIC_EVALUATORS:
                result.append(_issue(
                    f"{base}.semanticEvaluator", "KIN-E-FIXTURE",
                    "semantic evaluator is outside the closed registry",
                ))
        elif mode in {"LITERAL", "REGEX"} and evaluator is not None:
            result.append(_issue(
                f"{base}.semanticEvaluator", "KIN-E-FIXTURE",
                "text antibody must have a null semantic evaluator",
            ))
        for field in ("scopeGlobs", "excludeGlobs"):
            if not _text_list(antibody.get(field)):
                result.append(_issue(
                    f"{base}.{field}", "KIN-E-FIXTURE",
                    "glob inventory must be a list of Unicode scalar strings",
                ))
    return ordered_issues(result)


def _fixture_shape_issues(core: dict[str, Any]) -> list[Issue]:
    result = _typed_collection_issues(
        core, ("fixtures",), code="KIN-E-FIXTURE", root="core",
    )
    result.extend(_antibody_shape_issues(core))
    fixtures = core.get("fixtures")
    if not isinstance(fixtures, list):
        return ordered_issues(result)
    seen_ids: set[str] = set()
    for position, fixture in enumerate(fixtures):
        base = f"core.fixtures[{position}]"
        if not isinstance(fixture, dict):
            continue
        fixture_id = fixture.get("id")
        if not valid_id(fixture_id):
            result.append(_issue(
                f"{base}.id", "KIN-E-FIXTURE",
                "fixture ID must be a canonical identifier",
            ))
        elif fixture_id in seen_ids:
            result.append(_issue(
                f"{base}.id", "KIN-E-FIXTURE", "fixture ID must be unique",
            ))
        else:
            seen_ids.add(fixture_id)
        kind = fixture.get("kind")
        if type(kind) is not str or kind not in {
            "POSITIVE", "NEGATIVE", "QUOTATION", "HISTORICAL", "MUTATION",
        }:
            result.append(_issue(
                f"{base}.kind", "KIN-E-FIXTURE",
                "fixture kind is outside the closed registry",
            ))
        payload_kind = fixture.get("payloadKind")
        if type(payload_kind) is not str or payload_kind not in {"TEXT", "JSON"}:
            result.append(_issue(
                f"{base}.payloadKind", "KIN-E-FIXTURE",
                "fixture payload kind must be TEXT or JSON",
            ))
        if not _scalar_text(fixture.get("payload"), nonempty=False):
            result.append(_issue(
                f"{base}.payload", "KIN-E-FIXTURE",
                "fixture payload must be Unicode scalar text",
            ))
        for field in ("antibodyIds", "expectedAntibodyIds"):
            if not _identifier_list(fixture.get(field)):
                result.append(_issue(
                    f"{base}.{field}", "KIN-E-FIXTURE",
                    f"{field} must be a list of canonical identifiers",
                ))
    return ordered_issues(result)


def _text_match(antibody: dict[str, Any], source: str) -> tuple[bool, list[Issue]]:
    if not _scalar_text(source, nonempty=False):
        return False, [_issue("fixture.payload", "KIN-E-FIXTURE", "text payload must contain only Unicode scalar text")]
    if antibody.get("matchMode") == "LITERAL":
        pattern = antibody.get("pattern")
        if not _scalar_text(pattern):
            return False, [_issue("antibody.pattern", "KIN-E-FIXTURE", "literal pattern must be non-empty Unicode scalar text")]
        return pattern in source, []
    if antibody.get("matchMode") == "REGEX":
        return safe_regex_search(antibody.get("pattern"), source)
    return False, [_issue("antibody.matchMode", "KIN-E-FIXTURE", "text fixture requires LITERAL or REGEX")]


def evaluate_antibody_fixture(
    core: dict[str, object], fixture_id: str
) -> list[Issue]:
    if not isinstance(core, dict):
        return [_issue("fixture", "KIN-E-FIXTURE", "core must be an object")]
    if not valid_id(fixture_id):
        return [_issue(
            "fixture.id", "KIN-E-FIXTURE",
            "fixture ID must be a canonical identifier",
        )]
    try:
        shape_issues = _fixture_shape_issues(core)
        if shape_issues:
            return shape_issues
        return _evaluate_antibody_fixture_unchecked(core, fixture_id)
    except Exception:
        return [_issue(
            "fixture", "KIN-E-FIXTURE",
            "fixture execution failed safely on malformed nested data",
        )]


def _evaluate_antibody_fixture_unchecked(
    core: dict[str, object], fixture_id: str
) -> list[Issue]:
    fixtures = _index(core, "fixtures")
    antibodies = _index(core, "antibodies")
    fixture = fixtures.get(fixture_id)
    if fixture is None:
        return [_issue("fixture.id", "KIN-E-FIXTURE", "fixture does not resolve")]
    if fixture.get("kind") == "MUTATION":
        return []
    actual: list[str] = []
    execution_issues: list[Issue] = []
    context = fixture.get("kind")
    for antibody_id in fixture.get("antibodyIds", []):
        antibody = antibodies.get(antibody_id)
        if antibody is None:
            execution_issues.append(_issue("fixture.antibodyIds", "KIN-E-FIXTURE", "fixture antibody does not resolve"))
            continue
        mode = antibody.get("matchMode")
        triggered = False
        if mode in {"LITERAL", "REGEX"}:
            if fixture.get("payloadKind") != "TEXT":
                execution_issues.append(_issue("fixture.payloadKind", "KIN-E-FIXTURE", "text antibody requires a TEXT fixture"))
                continue
            triggered, match_issues = _text_match(antibody, fixture.get("payload"))
            execution_issues.extend(match_issues)
        elif mode == "SEMANTIC_FIXTURE":
            if fixture.get("payloadKind") != "JSON":
                execution_issues.append(_issue("fixture.payloadKind", "KIN-E-FIXTURE", "semantic antibody requires a JSON fixture"))
                continue
            try:
                payload = _decode_semantic_payload(fixture.get("payload"))
            except Exception:
                execution_issues.append(_issue("fixture.payload", "KIN-E-FIXTURE", "semantic fixture payload is invalid JSON"))
                continue
            execution = _execute_semantic_fixture(
                antibody.get("semanticEvaluator"), payload, core
            )
            if execution.execution_issues:
                execution_issues.extend(execution.execution_issues)
                continue
            triggered = execution.predicate_passed is False
        else:
            execution_issues.append(_issue("antibody.matchMode", "KIN-E-FIXTURE", "unknown antibody match mode"))
        if triggered and context in {"POSITIVE", "NEGATIVE"}:
            actual.append(antibody_id)
    if execution_issues:
        return ordered_issues(execution_issues)
    if tuple(sorted(actual)) != tuple(sorted(fixture.get("expectedAntibodyIds", []))):
        return [_issue(
            "fixture.expectedAntibodyIds", "KIN-E-FIXTURE",
            "actual trigger IDs do not deep-equal the expected set",
        )]
    return []


def scan_antibodies(
    core: dict[str, object], documents: dict[str, str]
) -> tuple[dict[str, Any], list[Issue]]:
    empty: dict[str, Any] = {"included": {}, "excluded": {}, "triggers": {}}
    if not isinstance(core, dict) or not isinstance(documents, dict):
        return empty, [_issue("scan", "KIN-E-FIXTURE", "core and documents must be objects")]
    try:
        shape_issues = _antibody_shape_issues(core)
        if shape_issues:
            return empty, shape_issues
        return _scan_antibodies_unchecked(core, documents)
    except Exception:
        return empty, [_issue(
            "scan", "KIN-E-FIXTURE",
            "antibody scan failed safely on malformed nested data",
        )]


def _scan_antibodies_unchecked(
    core: dict[str, object], documents: dict[str, str]
) -> tuple[dict[str, Any], list[Issue]]:
    empty: dict[str, Any] = {"included": {}, "excluded": {}, "triggers": {}}
    antibodies = sorted([
        antibody for antibody in _records(core, "antibodies")
        if antibody.get("matchMode") in {"LITERAL", "REGEX"}
    ], key=lambda antibody: antibody.get("id", ""))
    issues: list[Issue] = []
    for position, antibody in enumerate(antibodies):
        for field in ("scopeGlobs", "excludeGlobs"):
            patterns = antibody.get(field)
            if not isinstance(patterns, list) or any(not isinstance(item, str) for item in patterns):
                issues.append(_issue(
                    f"core.antibodies[{position}].{field}", "KIN-E-FIXTURE",
                    "glob inventory must be a list of Unicode strings",
                ))
                continue
            for pattern in sorted(patterns):
                try:
                    _safe_path_segments(pattern, pattern=True)
                except ValueError as exc:
                    issues.append(_issue(f"core.antibodies[{position}].{field}", "KIN-E-FIXTURE", str(exc)))
        if antibody.get("matchMode") == "REGEX":
            _, regex_issues = safe_regex_search(antibody.get("pattern"), "")
            issues.extend(regex_issues)
    if issues:
        return empty, ordered_issues(issues)

    decoded_documents: dict[str, str] = {}
    for path, raw_source in documents.items():
        try:
            _safe_path_segments(path, pattern=False)
        except ValueError as exc:
            issues.append(_issue("scan.documents.path", "KIN-E-FIXTURE", str(exc)))
            continue
        if isinstance(raw_source, bytes):
            try:
                source = raw_source.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                issues.append(_issue(path, "KIN-E-FIXTURE", "source is not strict UTF-8"))
                continue
        elif isinstance(raw_source, str):
            source = raw_source
            try:
                source.encode("utf-8", errors="strict")
            except UnicodeEncodeError:
                issues.append(_issue(path, "KIN-E-FIXTURE", "source is not strict UTF-8"))
                continue
        else:
            issues.append(_issue(path, "KIN-E-FIXTURE", "source must be str or bytes"))
            continue
        decoded_documents[path] = source
    if issues:
        return empty, ordered_issues(issues)

    included: dict[str, tuple[str, ...]] = {}
    excluded: dict[str, tuple[str, ...]] = {}
    selected_by_path: dict[str, list[dict[str, Any]]] = {}
    paths = tuple(sorted(decoded_documents))
    for antibody in antibodies:
        scopes = tuple(sorted(antibody["scopeGlobs"]))
        excludes = tuple(sorted(antibody["excludeGlobs"]))
        resolved_includes = tuple(
            path for path in paths if any(_glob_match(pattern, path) for pattern in scopes)
        )
        resolved_excludes = tuple(
            path for path in paths if any(_glob_match(pattern, path) for pattern in excludes)
        )
        included[antibody["id"]] = resolved_includes
        excluded[antibody["id"]] = resolved_excludes
        excluded_set = set(resolved_excludes)
        for path in resolved_includes:
            if path not in excluded_set:
                selected_by_path.setdefault(path, []).append(antibody)

    triggers_by_path: dict[str, tuple[str, ...]] = {}
    for path in sorted(selected_by_path):
        triggers: list[str] = []
        for antibody in selected_by_path[path]:
            matched, match_issues = _text_match(antibody, decoded_documents[path])
            issues.extend(match_issues)
            if matched:
                triggers.append(antibody["id"])
        triggers_by_path[path] = tuple(sorted(triggers))
    result = {
        "included": {key: included[key] for key in sorted(included)},
        "excluded": {key: excluded[key] for key in sorted(excluded)},
        "triggers": triggers_by_path,
    }
    return result, ordered_issues(issues)


def _validate_antibody_contract(core: dict[str, Any]) -> list[Issue]:
    result: list[Issue] = []
    execution_counts: dict[str, int] = {}
    for position, antibody in enumerate(_records(core, "antibodies")):
        base = f"core.antibodies[{position}]"
        mode = antibody.get("matchMode")
        evaluator = antibody.get("semanticEvaluator")
        if mode == "SEMANTIC_FIXTURE":
            if evaluator not in SEMANTIC_EVALUATORS:
                result.append(_issue(f"{base}.semanticEvaluator", "KIN-E-FIXTURE", "semantic evaluator is outside the closed registry"))
        elif evaluator is not None:
            result.append(_issue(f"{base}.semanticEvaluator", "KIN-E-FIXTURE", "text antibody must have a null semantic evaluator"))
        if mode == "REGEX":
            _, regex_issues = safe_regex_search(antibody.get("pattern"), "")
            result.extend(
                Issue(f"{base}.pattern", item.code, item.message) for item in regex_issues
            )
        for field in ("scopeGlobs", "excludeGlobs"):
            for pattern in antibody.get(field, []):
                try:
                    _safe_path_segments(pattern, pattern=True)
                except ValueError as exc:
                    result.append(_issue(f"{base}.{field}", "KIN-E-FIXTURE", str(exc)))
        for field in (
            "positiveFixtureIds", "negativeFixtureIds",
            "quotationFixtureIds", "historicalFixtureIds",
        ):
            for fixture_id in antibody.get(field, []):
                execution_counts[fixture_id] = execution_counts.get(fixture_id, 0) + 1
    for fixture in _records(core, "fixtures"):
        if fixture.get("kind") == "MUTATION":
            continue
        result.extend(evaluate_antibody_fixture(core, fixture.get("id")))
        if execution_counts.get(fixture.get("id"), 0) != len(fixture.get("antibodyIds", [])):
            result.append(_issue("core.fixtures", "KIN-E-FIXTURE", "fixture execution count is not exact"))
    return result


__all__ = [
    "EVIDENCE_ORDER",
    "INDEPENDENCE_ORDER",
    "MODALITIES",
    "SEMANTIC_EVALUATORS",
    "VERDICT_MATRIX",
    "evaluate_antibody_fixture",
    "evaluate_semantic_fixture",
    "safe_regex_search",
    "scan_antibodies",
    "validate_core_records",
    "validate_public_queue",
]

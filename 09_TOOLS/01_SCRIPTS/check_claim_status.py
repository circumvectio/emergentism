#!/usr/bin/env python3
"""Enforce the Claim Status Register contract.

The register separates *validation status* from *evidence tier*. Its whole
purpose is to keep refuted claims from quietly returning as live ones, so the
checks here fail closed on exactly that move.

Input is the JSON subset of YAML 1.2, matching the rest of the corpus tooling,
so this stays stdlib-only.

    python3 09_TOOLS/01_SCRIPTS/check_claim_status.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATUS_PATH = Path("00_META/claim_status/CLAIM_STATUS.yaml")
HUMAN_OWNER = Path("00_META/00_THE_CLAIM_STATUS_REGISTER.md")
CONJECTURES = Path("06_ONTOLOGY/04_THE_CONJECTURES.md")
RECORD_LEDGER = Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md")

DF_ID = re.compile(r"^DF-\d{2}$")
RQ_ID = re.compile(r"^RQ-\d{2}$")
FV_ID = re.compile(r"^FV-\d{2}$")
TR_ID = re.compile(r"^TR-\d{2}$")
WAGER_ID = re.compile(r"^W\d+[a-e]?(-[A-Z]+)?$")
DOCKET_ID = re.compile(r"^A[0-7]$")

# Successor targets that live under another governed owner rather than in this
# register. Exact identity and source custody are pinned; a syntactically tidy
# fake such as W99 or GP-99 is not an owner.
EXTERNAL_OWNER_FILES = {
    "E8": Path("06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md"),
    "E9": Path("06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md"),
    "GP-03": Path("03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md"),
    "GP-11": Path("03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md"),
    "HC-11": Path("06_ONTOLOGY/08_THE_HUMAN_CONDITION.md"),
    "KSC-04": Path("00_META/00_SETTLED_CANON_REGISTRY.md"),
}

REQUIRED_INVESTIGATION_FIELDS = (
    "parent",
    "question",
    "parent_kill_does_not_reach",
    "discriminator",
    "kill",
    "survivor",
)

CONTACT_KINDS = {"CONTACT-GATED", "MERGED-TO-CONTACT"}
INTERNAL_KINDS = {"INTERNAL-NARROWED", "INTERNAL-TERMINAL"}
GRAVE_KINDS = {"MERGED-TO-OWNER", "INTERNAL-TERMINAL"}
# RESTORED 2026-08-05. Both names below are USED in this file (INVESTIGATION_STATES
# once, PINNED_GRAVE_STATUS at the expected-status and missing-baseline checks) and
# were DEFINED NOWHERE: they were dropped by merge 80759036 ("conflicts resolved
# main-side"), which left this checker raising NameError on every run. Recovered
# verbatim from 1797138a. Receipt:
# 11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md
INVESTIGATION_STATES = {"OPEN", "DEFERRED", "CLOSED"}
PINNED_GRAVE_STATUS = {
    "DF-01": "FORMALLY-REFUTED", "DF-02": "CATEGORY-ERROR",
    "DF-03": "EMPIRICALLY-REFUTED", "DF-04": "FORMALLY-REFUTED",
    "DF-05": "CATEGORY-ERROR", "DF-06": "EMPIRICALLY-REFUTED",
    "DF-07": "EMPIRICALLY-REFUTED", "DF-08": "FORMALLY-REFUTED",
    "DF-09": "FORMALLY-REFUTED", "DF-10": "FORMALLY-REFUTED",
    "DF-11": "FORMALLY-REFUTED", "DF-12": "FORMALLY-REFUTED",
    "DF-13": "EMPIRICALLY-REFUTED", "DF-14": "FORMALLY-REFUTED",
    "DF-15": "CATEGORY-ERROR", "DF-16": "FORMALLY-REFUTED",
    "DF-17": "NOT-WELL-POSED", "DF-18": "NOT-WELL-POSED",
    "DF-19": "FORMALLY-REFUTED", "DF-20": "CATEGORY-ERROR",
    "DF-21": "FORMALLY-REFUTED", "DF-22": "PROCESS-DEFECT",
}
CONTRACT_FIELDS = {
    "contract_id", "component_id", "protocol_owner", "protocol_refs",
    "maturity", "blocked_by", "discriminator", "kill", "survivor",
    "component_support_refs", "integrated_support", "evidence_contract",
}
RESOLUTION_FIELDS = {
    "result_id", "result_status", "result_tier", "scope", "source_refs",
    "survivor", "reopen_when", "evidence_contract",
}
WORLD_REQUIRED_FIELDS = (
    "claim_id", "contract_id", "frozen_protocol_hash", "scope",
    "independent_party_identity", "independence_basis", "discriminating_protocol",
    "outcome", "verbatim_custody", "provenance", "null_harm_deviation_custody",
)
WORLD_INADMISSIBLE = (
    "commits", "gates", "AI review", "invitations", "preregistrations",
    "internal receipts", "URLs without filed outcome custody", "staged protocols",
)


# Pinned vocabularies. HOLE 5: previously these were read from the document under
# validation, so moving a status between lists silently disabled every check
# gated on it. A checker may not take its constitution from its subject.
LIVE = {"FORMALLY-VALID","RECEIPTED","OPEN-FORMAL","OPEN-EMPIRICAL",
        "COMPONENT-SUPPORTED","NARROWED"}
TERMINAL = {"FORMALLY-REFUTED","EMPIRICALLY-REFUTED","CATEGORY-ERROR",
            "NOT-WELL-POSED","DECORATIVE","PROCESS-DEFECT"}
ONE_WAY = {"FORMALLY-REFUTED","EMPIRICALLY-REFUTED","CATEGORY-ERROR"}
KNOWN_SECTIONS = {"schema","routing_role","human_owner","serialization",
                  "live_statuses","terminal_statuses","one_way_statuses","rules",
                  "disposition_policy","owner_reopening","validated","open","graves","reopened","restored"}
# HOLE 3: a counterexample must carry content, not merely be non-blank.
PLACEHOLDER = re.compile(r"^\s*(none|n/?a|tbd|todo|-+|\.+|x+|unknown|see above)\s*\.?\s*$", re.I)
MIN_COUNTEREXAMPLE = 25
EXPECTED_RULING = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md"
EXPECTED_ADJUDICATION = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/239_OPEN_CLAIM_DISPOSITION_2026_08_01.md"
EXPECTED_ROUTING_ROLE = "validation-status routing only; no semantic authority, no tier promotion"
EXPECTED_SERIALIZATION = "JSON subset of YAML 1.2 for deterministic stdlib parsing"
EXPECTED_RULES = (
    "Evidence tier and validation status are orthogonal axes; neither implies the other.",
    "A one-way row may never return to a live status AS THE CLAIM IT WAS. Exactly three moves are lawful: NARROWED with a named weaker form; a new RQ row with its own id, discriminator and kill; or OWNER-REOPENED under an owner ruling. The counterexample stays attached in every case.",
    "A one-way row must cite the counterexample that killed it.",
    "A reopened row must name its parent and state why the parent's counterexample does not reach it.",
    "Appearing in this register is not evidence for any claim.",
    "OWNER-REOPENED is the only lawful path from a terminal status back to live. It requires an owner ruling receipt, an intact counterexample, and a declared repair_path. It restores active investigation, never asserted truth.",
)


class ContractError(ValueError):
    """Raised when the register fails closed."""


def external_owner_marker_declared(path: Path, owner_id: str) -> bool:
    """Require a pinned external owner ID in a heading or first table cell."""

    if not path.is_file():
        return False
    token = re.compile(
        rf"(?<![A-Za-z0-9-]){re.escape(owner_id)}(?![A-Za-z0-9-])"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and token.search(stripped.lstrip("#").strip()):
            return True
        if stripped.startswith("|"):
            cells = stripped.split("|")
            if len(cells) > 2:
                first_cell = re.sub(r"[`*_~]", "", cells[1]).strip()
                if first_cell == owner_id:
                    return True
    return False


def load_document(path: Path) -> dict[str, Any]:
    """Load the JSON-subset source while rejecting duplicate object keys."""

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ContractError(f"duplicate JSON object key {key!r} in {path}")
            value[key] = item
        return value

    try:
        document = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"{path}: invalid JSON-subset YAML: {exc}") from exc
    if not isinstance(document, dict):
        raise ContractError(f"{path}: top level must be an object")
    return document


def lifecycle_rows(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every row whose current lifecycle Sprint 6 adjudicates."""
    return [
        row
        for section in ("open", "reopened", "graves")
        for row in document.get(section, [])
        if isinstance(row, dict)
    ]


def canonical_lifecycle_sha256(document: dict[str, Any]) -> str:
    payload = json.dumps(
        lifecycle_rows(document), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def canonical_contract_sha256(document: dict[str, Any]) -> str:
    """Bind the complete machine owner, including formal results and policy."""
    payload = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label}: expected a non-empty string")
    return value


def _rows(document: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = document.get(key)
    if not isinstance(value, list) or not value:
        raise ContractError(f"{key}: expected a non-empty list")
    for row in value:
        if not isinstance(row, dict):
            raise ContractError(f"{key}: every row must be an object")
    return value


def _exact_keys(value: dict[str, Any], expected: set[str], label: str, errors: list[str]) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{label}: missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: unknown keys: {', '.join(extra)}")


def _strings(value: Any, label: str, errors: list[str], *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        errors.append(f"{label}: expected {'a non-empty' if nonempty else 'a'} list")
        return []
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label}: every item must be a non-empty string")
        return []
    if len(value) != len(set(value)):
        errors.append(f"{label}: duplicate items are forbidden")
    return value


def _repo_file(root: Path, value: Any, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected a non-empty repo-relative path")
        return None
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{label}: path must be repo-relative and may not contain '..'")
        return None
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes the repository")
        return None
    if not target.is_file():
        errors.append(f"{label}: file does not exist: {value}")
        return None
    return value


def _policy_errors(document: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    policy = document.get("disposition_policy")
    if not isinstance(policy, dict):
        return ["disposition_policy: expected an object"]
    _exact_keys(
        policy,
        {"kinds", "world_evidence_contract", "internal_evidence_contract"},
        "disposition_policy",
        errors,
    )
    expected_kinds = CONTACT_KINDS | INTERNAL_KINDS | {"MERGED-TO-OWNER"}
    if set(_strings(policy.get("kinds"), "disposition_policy.kinds", errors)) != expected_kinds:
        errors.append("disposition_policy.kinds drifted from the pinned checker vocabulary")
    world = policy.get("world_evidence_contract")
    if not isinstance(world, dict):
        errors.append("world_evidence_contract: expected an object")
    else:
        _exact_keys(world, {"id", "outcome_owner", "required_fields", "inadmissible_inputs"}, "world_evidence_contract", errors)
        if world.get("id") != "WORLD-OUTCOME-V1":
            errors.append("world_evidence_contract.id must be WORLD-OUTCOME-V1")
        _repo_file(root, world.get("outcome_owner"), "world_evidence_contract.outcome_owner", errors)
        if tuple(_strings(world.get("required_fields"), "world required_fields", errors)) != WORLD_REQUIRED_FIELDS:
            errors.append("world evidence required fields drifted")
        if tuple(_strings(world.get("inadmissible_inputs"), "world inadmissible_inputs", errors)) != WORLD_INADMISSIBLE:
            errors.append("world evidence inadmissible inputs drifted")
    internal = policy.get("internal_evidence_contract")
    if not isinstance(internal, dict):
        errors.append("internal_evidence_contract: expected an object")
    else:
        _exact_keys(internal, {"id", "required_fields", "boundary"}, "internal_evidence_contract", errors)
        if internal.get("id") != "INTERNAL-VERDICT-V1":
            errors.append("internal_evidence_contract.id must be INTERNAL-VERDICT-V1")
        if set(_strings(internal.get("required_fields"), "internal required_fields", errors)) != RESOLUTION_FIELDS:
            errors.append("internal evidence required fields drifted")
        if not isinstance(internal.get("boundary"), str) or "no observation" not in internal.get("boundary", ""):
            errors.append("internal evidence boundary must refuse world-contact inheritance")
    return errors


def check(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    path = root / STATUS_PATH
    document = load_document(path)

    _exact_keys(document, KNOWN_SECTIONS, "claim_status", errors)
    if document.get("schema") != "emergentism/claim-status/v2":
        errors.append("schema must be emergentism/claim-status/v2")
    if document.get("routing_role") != EXPECTED_ROUTING_ROLE:
        errors.append("routing_role must retain the validation-only, no-promotion boundary")
    if document.get("human_owner") != HUMAN_OWNER.as_posix():
        errors.append(f"human_owner must be {HUMAN_OWNER.as_posix()}")
    _repo_file(root, document.get("human_owner"), "human_owner", errors)
    if document.get("serialization") != EXPECTED_SERIALIZATION:
        errors.append("serialization contract drifted")
    if tuple(_strings(document.get("rules"), "rules", errors)) != EXPECTED_RULES:
        errors.append("claim-status constitutional rules drifted")
    errors.extend(_policy_errors(document, root))

    for rel in (HUMAN_OWNER, CONJECTURES, RECORD_LEDGER):
        if not (root / rel).is_file():
            errors.append(f"missing cross-referenced owner: {rel.as_posix()}")

    live, terminal, one_way = LIVE, TERMINAL, ONE_WAY

    # The document's own vocabularies must MATCH the pinned ones, not define them.
    for name, pinned in (("live_statuses", LIVE), ("terminal_statuses", TERMINAL),
                         ("one_way_statuses", ONE_WAY)):
        declared = set(document.get(name) or [])
        if declared != pinned:
            errors.append(
                f"{name} drifted from the pinned vocabulary: "
                f"missing={sorted(pinned - declared)} extra={sorted(declared - pinned)}"
            )

    for owner_id, owner_path in EXTERNAL_OWNER_FILES.items():
        _repo_file(root, owner_path.as_posix(), f"external owner {owner_id}", errors)
        resolved_owner = root / owner_path
        if resolved_owner.is_file() and not external_owner_marker_declared(
            resolved_owner, owner_id
        ):
            errors.append(
                f"external owner {owner_id}: source does not declare its exact marker"
            )

    # 174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md remains transition
    # history after adjudication; 239_OPEN_CLAIM_DISPOSITION_2026_08_01.md owns
    # current status.
    reopening = document.get("owner_reopening")
    if not isinstance(reopening, dict):
        errors.append("owner_reopening history block is required")
    else:
        _exact_keys(
            reopening,
            {"ruling", "receipt", "scope", "what_it_does_not_do", "current_state", "adjudication_receipt"},
            "owner_reopening",
            errors,
        )
        if reopening.get("receipt") != EXPECTED_RULING:
            errors.append(
                "owner_reopening must retain the exact "
                "174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md ruling receipt"
            )
        if reopening.get("adjudication_receipt") != EXPECTED_ADJUDICATION:
            errors.append("owner_reopening must bind current dispositions to receipt 239")
        _repo_file(root, reopening.get("receipt"), "owner_reopening.receipt", errors)
        _repo_file(root, reopening.get("adjudication_receipt"), "owner_reopening.adjudication_receipt", errors)
        for field in ("ruling", "scope", "what_it_does_not_do", "current_state"):
            if not isinstance(reopening.get(field), str) or not reopening.get(field, "").strip():
                errors.append(f"owner_reopening: {field} is required")
        if "ADJUDICATED" not in str(reopening.get("current_state")):
            errors.append("owner_reopening.current_state must record the completed adjudication")

    seen: dict[str, str] = {}

    def claim_id(row_id: str, section: str) -> None:
        if row_id in seen:
            errors.append(f"duplicate id {row_id} in {section} and {seen[row_id]}")
        seen[row_id] = section

    raw_known_ids = {
        str(row.get("id"))
        for section in ("validated", "open", "graves", "reopened", "restored")
        for row in (document.get(section) or [])
        if isinstance(row, dict) and row.get("id") is not None
    }
    executable_blocker_ids = {
        str(row.get("id"))
        for section in ("open", "reopened")
        for row in (document.get(section) or [])
        if isinstance(row, dict)
        and row.get("status") in LIVE
        and isinstance(row.get("disposition"), dict)
        and row["disposition"].get("kind") in CONTACT_KINDS
    }
    contract_registry: dict[str, tuple[str, dict[str, Any]]] = {}
    merged_contact_rows: list[tuple[str, dict[str, Any]]] = []
    result_registry: dict[str, str] = {}
    blocker_graph: dict[str, set[str]] = {}

    def target_is_known(target: str) -> bool:
        return target in raw_known_ids or target in EXTERNAL_OWNER_FILES

    def blocker_is_governed(target: str) -> bool:
        return target in executable_blocker_ids or target in EXTERNAL_OWNER_FILES

    def validate_resolution(row_id: str, status: str, disposition: dict[str, Any]) -> None:
        resolution = disposition.get("resolution")
        if not isinstance(resolution, dict):
            errors.append(f"{row_id}: internal disposition requires a resolution object")
            return
        _exact_keys(resolution, RESOLUTION_FIELDS, f"{row_id}.resolution", errors)
        for field in ("result_id", "result_status", "result_tier", "scope", "survivor", "reopen_when", "evidence_contract"):
            try:
                _text(resolution.get(field), f"{row_id}.resolution.{field}")
            except ContractError as exc:
                errors.append(str(exc))
        if resolution.get("result_status") != status:
            errors.append(f"{row_id}: result_status must equal row status {status}")
        if resolution.get("result_tier") not in {"A", "B", "S", "I"}:
            errors.append(f"{row_id}: internal result_tier must be A, B, S, or I")
        if resolution.get("evidence_contract") != "INTERNAL-VERDICT-V1":
            errors.append(f"{row_id}: internal resolution must use INTERNAL-VERDICT-V1")
        result_id = str(resolution.get("result_id", ""))
        if result_id.startswith("IV-"):
            prior_owner = result_registry.get(result_id)
            if prior_owner is not None:
                errors.append(
                    f"{row_id}: duplicate IV result_id {result_id} already belongs to {prior_owner}"
                )
            else:
                result_registry[result_id] = row_id
            if not re.fullmatch(rf"IV-{re.escape(row_id)}-\d{{2}}", result_id):
                errors.append(f"{row_id}: IV result_id must be owned by its row id")
        refs = _strings(resolution.get("source_refs"), f"{row_id}.resolution.source_refs", errors)
        for index, ref in enumerate(refs):
            _repo_file(root, ref, f"{row_id}.resolution.source_refs[{index}]", errors)

    def validate_disposition(row: dict[str, Any], section: str) -> None:
        row_id = str(row.get("id"))
        status = str(row.get("status"))
        disposition = row.get("disposition")
        if not isinstance(disposition, dict):
            errors.append(f"{row_id}: missing disposition object")
            return
        kind = disposition.get("kind")
        if section == "graves":
            if kind not in GRAVE_KINDS:
                errors.append(f"{row_id}: grave disposition kind {kind!r} is not allowed")
                return
            if kind == "MERGED-TO-OWNER":
                _exact_keys(disposition, {"kind", "target_ids", "boundary"}, f"{row_id}.disposition", errors)
                targets = _strings(disposition.get("target_ids"), f"{row_id}.target_ids", errors)
                if row.get("successor") not in targets:
                    errors.append(f"{row_id}: merged grave targets must include its recorded successor")
                if row_id in targets or any(not target_is_known(target) for target in targets):
                    errors.append(f"{row_id}: merged grave has a self or unknown target")
                if not isinstance(disposition.get("boundary"), str) or not disposition.get("boundary", "").strip():
                    errors.append(f"{row_id}: merged grave requires a boundary")
            else:
                _exact_keys(disposition, {"kind", "resolution"}, f"{row_id}.disposition", errors)
                if status not in TERMINAL:
                    errors.append(f"{row_id}: INTERNAL-TERMINAL grave must carry a terminal status")
                if row.get("successor") is not None:
                    errors.append(f"{row_id}: terminal grave disposition requires no successor")
                validate_resolution(row_id, status, disposition)
            return

        if kind == "CONTACT-GATED":
            _exact_keys(disposition, {"kind", "claim_owner", "contracts"}, f"{row_id}.disposition", errors)
            if status not in {"OPEN-EMPIRICAL", "COMPONENT-SUPPORTED"}:
                errors.append(f"{row_id}: CONTACT-GATED requires OPEN-EMPIRICAL or COMPONENT-SUPPORTED")
            _repo_file(root, disposition.get("claim_owner"), f"{row_id}.claim_owner", errors)
            contracts = disposition.get("contracts")
            if not isinstance(contracts, list) or not contracts:
                errors.append(f"{row_id}: CONTACT-GATED requires at least one contract")
                return
            component_ids: set[str] = set()
            supported_components = 0
            for index, contract in enumerate(contracts):
                label = f"{row_id}.contracts[{index}]"
                if not isinstance(contract, dict):
                    errors.append(f"{label}: expected an object")
                    continue
                _exact_keys(contract, CONTRACT_FIELDS, label, errors)
                for field in ("contract_id", "component_id", "protocol_owner", "maturity", "discriminator", "kill", "survivor", "integrated_support", "evidence_contract"):
                    try:
                        _text(contract.get(field), f"{label}.{field}")
                    except ContractError as exc:
                        errors.append(str(exc))
                contract_id = str(contract.get("contract_id"))
                if contract_id in contract_registry:
                    errors.append(f"duplicate contact contract id {contract_id}")
                else:
                    contract_registry[contract_id] = (row_id, contract)
                component_id = str(contract.get("component_id"))
                if component_id in component_ids:
                    errors.append(f"{row_id}: duplicate component_id {component_id}")
                component_ids.add(component_id)
                _repo_file(root, contract.get("protocol_owner"), f"{label}.protocol_owner", errors)
                for field in ("protocol_refs", "component_support_refs"):
                    refs = _strings(contract.get(field), f"{label}.{field}", errors, nonempty=(field == "protocol_refs"))
                    for ref_index, ref in enumerate(refs):
                        _repo_file(root, ref, f"{label}.{field}[{ref_index}]", errors)
                maturity = contract.get("maturity")
                if maturity not in {"design-required", "blocked", "component-supported"}:
                    errors.append(f"{label}: unknown maturity {maturity!r}")
                blockers = _strings(contract.get("blocked_by"), f"{label}.blocked_by", errors, nonempty=False)
                if (maturity == "blocked") != bool(blockers):
                    errors.append(f"{label}: blocked maturity and blocked_by must occur together")
                if row_id in blockers or any(not blocker_is_governed(item) for item in blockers):
                    errors.append(
                        f"{label}: blocker is self-referential, terminal, or not a governed prerequisite"
                    )
                blocker_graph.setdefault(row_id, set()).update(
                    item for item in blockers if item in raw_known_ids
                )
                if maturity == "component-supported":
                    supported_components += 1
                    if not contract.get("component_support_refs"):
                        errors.append(f"{label}: component-supported maturity requires source custody")
                if contract.get("integrated_support") != "absent":
                    errors.append(f"{label}: integrated_support must remain absent")
                if contract.get("evidence_contract") != "WORLD-OUTCOME-V1":
                    errors.append(f"{label}: contact contract must use WORLD-OUTCOME-V1")
            if status == "COMPONENT-SUPPORTED" and supported_components == 0:
                errors.append(f"{row_id}: COMPONENT-SUPPORTED requires a supported component contract")
            return

        if kind == "MERGED-TO-CONTACT":
            _exact_keys(disposition, {"kind", "claim_owner", "target_ids", "contract_ids", "reason"}, f"{row_id}.disposition", errors)
            if status != "OPEN-EMPIRICAL":
                errors.append(f"{row_id}: MERGED-TO-CONTACT requires OPEN-EMPIRICAL")
            _repo_file(root, disposition.get("claim_owner"), f"{row_id}.claim_owner", errors)
            targets = _strings(disposition.get("target_ids"), f"{row_id}.target_ids", errors)
            contracts = _strings(disposition.get("contract_ids"), f"{row_id}.contract_ids", errors)
            if row_id in targets or any(not target_is_known(target) for target in targets):
                errors.append(f"{row_id}: merged contact row has a self or unknown target")
            if not isinstance(disposition.get("reason"), str) or not disposition.get("reason", "").strip():
                errors.append(f"{row_id}: merged contact row requires a reason")
            merged_contact_rows.append((row_id, disposition))
            return

        if kind in INTERNAL_KINDS:
            expected = {"kind", "claim_owner", "resolution"}
            if "target_ids" in disposition:
                expected.add("target_ids")
            _exact_keys(disposition, expected, f"{row_id}.disposition", errors)
            _repo_file(root, disposition.get("claim_owner"), f"{row_id}.claim_owner", errors)
            if kind == "INTERNAL-NARROWED" and status != "NARROWED":
                errors.append(f"{row_id}: INTERNAL-NARROWED requires NARROWED")
            if kind == "INTERNAL-TERMINAL" and status not in TERMINAL:
                errors.append(f"{row_id}: INTERNAL-TERMINAL requires a terminal status")
            targets = _strings(disposition.get("target_ids"), f"{row_id}.target_ids", errors) if "target_ids" in disposition else []
            if row_id in targets or any(not target_is_known(target) for target in targets):
                errors.append(f"{row_id}: internal disposition has a self or unknown target")
            validate_resolution(row_id, status, disposition)
            return

        errors.append(f"{row_id}: unknown disposition kind {kind!r}")

    # --- validated -------------------------------------------------------
    validated_ids: set[str] = set()
    for row in _rows(document, "validated"):
        row_id = _text(row.get("id"), "validated.id")
        validated_keys = {"id", "status", "tier", "system", "result"}
        if row_id == "FV-12":
            validated_keys.add("load_bearing")
        _exact_keys(row, validated_keys, row_id, errors)
        claim_id(row_id, "validated")
        validated_ids.add(row_id)
        if not FV_ID.fullmatch(row_id):
            errors.append(f"{row_id}: validated ids must look like FV-nn")
        if row.get("status") != "FORMALLY-VALID":
            errors.append(f"{row_id}: validated rows must carry FORMALLY-VALID")
        if row.get("tier") not in {"A", "S"}:
            errors.append(f"{row_id}: a proved result must be tier A or S, not {row.get('tier')!r}")
        for field in ("system", "result"):
            try:
                _text(row.get(field), f"{row_id}.{field}")
            except ContractError as exc:
                errors.append(str(exc))
        if row_id == "FV-12":
            try:
                _text(row.get("load_bearing"), "FV-12.load_bearing")
            except ContractError as exc:
                errors.append(str(exc))

    expected_validated_ids = {f"FV-{number:02d}" for number in range(1, 22)}
    if validated_ids != expected_validated_ids:
        errors.append(
            f"validated inventory drifted: missing={sorted(expected_validated_ids-validated_ids)} "
            f"extra={sorted(validated_ids-expected_validated_ids)}"
        )

    # --- open ------------------------------------------------------------
    open_ids: set[str] = set()
    for row in _rows(document, "open"):
        row_id = _text(row.get("id"), "open.id")
        _exact_keys(
            row,
            {"id", "status", "docket", "disposition"}
            | ({"note"} if "note" in row else set())
            | ({"reopened_as"} if "reopened_as" in row else set())
            | ({"see_also"} if "see_also" in row else set()),
            row_id,
            errors,
        )
        claim_id(row_id, "open")
        open_ids.add(row_id)
        if not WAGER_ID.fullmatch(row_id):
            errors.append(f"{row_id}: open rows must carry a wager id")
        status = _text(row.get("status"), f"{row_id}.status")
        if status not in live | terminal:
            errors.append(f"{row_id}: unknown status {status}")
        docket = row.get("docket")
        if not isinstance(docket, str) or not DOCKET_ID.fullmatch(docket):
            errors.append(f"{row_id}: open rows need an adequacy docket A0-A7")
        validate_disposition(row, "open")

    expected_open_ids = {
        "W0-CROWN", "W1", "W2", "W3", "W4", "W5", "W6", "W7a", "W7b",
        "W7c", "W7d", "W7e", "W8", "W9", "W10", "W11", "W12",
    }
    if open_ids != expected_open_ids:
        errors.append(
            f"W inventory drifted: missing={sorted(expected_open_ids-open_ids)} "
            f"extra={sorted(open_ids-expected_open_ids)}"
        )

    conjectures_text = (root / CONJECTURES).read_text(encoding="utf-8") if (root / CONJECTURES).is_file() else ""
    for row_id in sorted(open_ids):
        base = row_id.split("-")[0].rstrip("abcde") or row_id
        if conjectures_text and base not in conjectures_text:
            errors.append(f"{row_id}: no matching wager {base} found in {CONJECTURES.as_posix()}")

    # --- graves ----------------------------------------------------------
    grave_ids: set[str] = set()
    grave_successors: dict[str, str | None] = {}
    for row in _rows(document, "graves"):
        row_id = _text(row.get("id"), "graves.id")
        expected_grave_keys = {
            "id", "status", "form", "counterexample", "successor",
            "successor_kind", "repair_path", "disposition",
        }
        if "status_before_reopening" in row:
            expected_grave_keys.add("status_before_reopening")
        _exact_keys(row, expected_grave_keys, row_id, errors)
        claim_id(row_id, "graves")
        grave_ids.add(row_id)
        if not DF_ID.fullmatch(row_id):
            errors.append(f"{row_id}: grave ids must look like DF-nn")
        status = _text(row.get("status"), f"{row_id}.status")
        if status not in terminal:
            errors.append(f"{row_id}: every grave must retain a terminal status, found {status}")
        expected_status = PINNED_GRAVE_STATUS.get(row_id)
        if expected_status is not None and status != expected_status:
            errors.append(f"{row_id}: terminal status drifted; expected {expected_status}, found {status}")
        try:
            _text(row.get("form"), f"{row_id}.form")
            _text(row.get("counterexample"), f"{row_id}.counterexample")
        except ContractError as exc:
            errors.append(str(exc))
        cx = str(row.get("counterexample", "")).strip()
        if not cx:
            errors.append(f"{row_id}: a grave must cite the counterexample or process defect that killed it")
        if cx and (PLACEHOLDER.fullmatch(cx) or len(cx) < MIN_COUNTEREXAMPLE):
            errors.append(
                f"{row_id}: counterexample is a placeholder or too thin to be one ({cx!r}) — "
                "'intact' means content, not merely non-blank"
            )
        for forbidden in ("status_before_reopening", "repair_path", "investigation_state"):
            if forbidden in row:
                errors.append(f"{row_id}: {forbidden} belongs to history or a successor inquiry, not a grave")
        successor = row.get("successor")
        if successor is not None and not isinstance(successor, str):
            errors.append(f"{row_id}: successor must be a string id or null")
            successor = None
        if successor == row_id:
            errors.append(f"{row_id}: a grave cannot be its own successor")
        grave_successors[row_id] = successor
        if "successor_kind" not in row:
            errors.append(f"{row_id}: successor_kind is required, use closed_no_successor when there is none")
        if successor is None and row.get("successor_kind") != "closed_no_successor":
            errors.append(f"{row_id}: a null successor must be marked closed_no_successor")
        validate_disposition(row, "graves")

    missing_baseline = sorted(set(PINNED_GRAVE_STATUS) - grave_ids)
    if missing_baseline:
        errors.append(f"baseline graves may not disappear: {', '.join(missing_baseline)}")
    numbers = sorted(int(row_id.split("-")[1]) for row_id in grave_ids if DF_ID.fullmatch(row_id))
    if numbers and numbers != list(range(1, max(numbers) + 1)):
        errors.append("grave ids must remain contiguous from DF-01 through the newest grave")

    # --- investigations --------------------------------------------------
    investigation_ids: set[str] = set()
    reopened_ids: set[str] = set()
    for row in _rows(document, "investigations"):
        row_id = _text(row.get("id"), "reopened.id")
        _exact_keys(
            row,
            {"id", "parent", "tier", "status", "docket", "question",
             "parent_kill_does_not_reach", "discriminator", "kill", "survivor",
             "disposition"},
            row_id,
            errors,
        )
        claim_id(row_id, "reopened")
        reopened_ids.add(row_id)
        if not RQ_ID.fullmatch(row_id):
            errors.append(f"{row_id}: investigation ids must look like RQ-nn")
        state = row.get("investigation_state")
        if state not in INVESTIGATION_STATES:
            errors.append(f"{row_id}: invalid investigation_state {state!r}")
        for field in REQUIRED_INVESTIGATION_FIELDS:
            try:
                _text(row.get(field), f"{row_id}.{field}")
            except ContractError as exc:
                errors.append(str(exc))
        if row.get("tier") != "C":
            errors.append(f"{row_id}: an investigation is a conjecture and must be tier C")
        docket = row.get("docket")
        if not isinstance(docket, str) or not DOCKET_ID.fullmatch(docket):
            errors.append(f"{row_id}: investigations need an adequacy docket A0-A7")
        parent = row.get("parent")
        if isinstance(parent, str) and parent not in grave_ids and parent not in open_ids:
            errors.append(f"{row_id}: parent {parent} is neither a grave nor an open wager")
        status = _text(row.get("status"), f"{row_id}.status")
        if status not in live | terminal:
            errors.append(f"{row_id}: unknown status {status}")
        validate_disposition(row, "reopened")

    expected_reopened_ids = {f"RQ-{number:02d}" for number in range(1, 10)}
    if reopened_ids != expected_reopened_ids:
        errors.append(
            f"RQ inventory drifted: missing={sorted(expected_reopened_ids-reopened_ids)} "
            f"extra={sorted(reopened_ids-expected_reopened_ids)}"
        )

    # --- restored --------------------------------------------------------
    # HOLE 1b: `restored` was a KNOWN section whose rows were never validated, so a
    # refuted form could be appended there as FORMALLY-VALID and pass. It is the
    # DF-22 shape with a machine blessing, so it is checked like everything else.
    restored_ids: set[str] = set()
    for row in (document.get("restored") or []):
        if not isinstance(row, dict):
            errors.append("typed_survivors: every row must be an object")
            continue
        row_id = str(row.get("id", "")).strip()
        _exact_keys(
            row,
            {"id", "status", "tier", "claim", "was", "why_the_falsifier_misses", "ksc_04_status", "owner", "inherits"},
            row_id or "restored row",
            errors,
        )
        if not TR_ID.fullmatch(row_id):
            errors.append(f"typed_survivors: ids must look like TR-nn, got {row_id!r} — "
                          "a grave id here would assert a refuted form as valid")
            continue
        claim_id(row_id, "restored")
        restored_ids.add(row_id)
        if row.get("status") != "FORMALLY-VALID":
            errors.append(f"{row_id}: a restored row must carry FORMALLY-VALID")
        if row.get("tier") not in {"A", "S"}:
            errors.append(f"{row_id}: restored by proof means tier A or S, not {row.get('tier')!r}")
        for field in ("claim", "was", "why_the_falsifier_misses", "ksc_04_status", "owner", "inherits"):
            if not str(row.get(field, "")).strip():
                errors.append(f"{row_id}: restored rows must state {field}")
        _repo_file(root, row.get("owner"), f"{row_id}.owner", errors)

    if restored_ids != {"TR-01"}:
        errors.append(f"restored inventory drifted: expected TR-01, found {sorted(restored_ids)}")

    # --- successor resolution -------------------------------------------
    known = grave_ids | investigation_ids | open_ids
    for grave, successor in sorted(grave_successors.items()):
        if successor is None:
            continue
        if successor in known:
            continue
        if successor in EXTERNAL_OWNER_FILES:
            continue
        errors.append(f"{grave}: successor {successor} resolves to no known id or external owner")

    # Every grave-derived investigation must be claimed by its terminal parent.
    for row in document["investigations"]:
        parent = row.get("parent")
        row_id = row.get("id")
        if parent in grave_ids and grave_successors.get(parent) != row_id:
            errors.append(
                f"{row_id}: descends from {parent} but {parent} does not name it as successor"
            )

    # Merged contact rows share a direct target's contract; they never create a
    # second confirmation or merge through another merge row.
    row_by_id = {
        str(row.get("id")): row
        for section in ("open", "reopened", "graves")
        for row in document.get(section, ())
        if isinstance(row, dict)
    }
    for row_id, disposition in merged_contact_rows:
        targets = disposition.get("target_ids") or []
        target_set = set(targets)
        for target_id in targets:
            target = row_by_id.get(target_id)
            if target is None or target.get("disposition", {}).get("kind") != "CONTACT-GATED":
                errors.append(f"{row_id}: merge target {target_id} is not a direct CONTACT-GATED row")
            elif target_id in raw_known_ids:
                # A merged row waits on its direct contract owner. Record that
                # dependency so a target cannot in turn declare itself blocked
                # by the merged row and hide a two-node deadlock.
                blocker_graph.setdefault(row_id, set()).add(target_id)
        for contract_id in disposition.get("contract_ids") or []:
            owner = contract_registry.get(contract_id)
            if owner is None:
                errors.append(f"{row_id}: merged contract {contract_id} does not resolve")
            elif owner[0] not in target_set:
                errors.append(
                    f"{row_id}: merged contract {contract_id} belongs to {owner[0]}, not a named target"
                )

    # A blocked contract may wait on another governed row, but the resulting
    # dependency graph may not contain a cycle: that is an undisclosed deadlock,
    # not a maturity state.
    colors: dict[str, int] = {}
    stack: list[str] = []

    def visit_blockers(node: str) -> None:
        color = colors.get(node, 0)
        if color == 2:
            return
        if color == 1:
            start = stack.index(node) if node in stack else 0
            errors.append("contact blocker cycle: " + " -> ".join(stack[start:] + [node]))
            return
        colors[node] = 1
        stack.append(node)
        for dependency in sorted(blocker_graph.get(node, set())):
            visit_blockers(dependency)
        stack.pop()
        colors[node] = 2

    for blocker_owner in sorted(blocker_graph):
        visit_blockers(blocker_owner)

    # An FV-backed internal disposition must resolve to the proved row and carry
    # that row's tier. An IV result is a scoped routing verdict, never a theorem.
    validated_by_id = {
        str(row.get("id")): row for row in document["validated"] if isinstance(row, dict)
    }
    for row in lifecycle_rows(document):
        disposition = row.get("disposition")
        if not isinstance(disposition, dict):
            continue
        resolution = disposition.get("resolution")
        if not isinstance(resolution, dict):
            continue
        result_id = str(resolution.get("result_id", ""))
        if result_id.startswith("FV-"):
            proved = validated_by_id.get(result_id)
            if proved is None:
                errors.append(f"{row.get('id')}: result_id {result_id} is not a validated row")
            elif resolution.get("result_tier") != proved.get("tier"):
                errors.append(f"{row.get('id')}: FV result tier does not match {result_id}")
        elif not re.fullmatch(r"IV-(?:W\d+(?:-[A-Z]+)?|RQ-\d{2}|DF-\d{2})-\d{2}", result_id):
            errors.append(f"{row.get('id')}: internal result_id has no governed FV/IV shape")

    # Every historical reopening transition is now adjudicated. Parent forms are
    # terminal or narrowed; executable work lives only in explicit successors.
    still_reopened = [
        row.get("id") for row in document["graves"] if row.get("status") == "OWNER-REOPENED"
    ]
    if still_reopened:
        errors.append("grave parent transitions remain unadjudicated: " + ", ".join(still_reopened))
    if sum(row.get("status") == "NARROWED" for row in document["graves"]) != 1:
        errors.append("grave scope must retain exactly one narrowed parent form (DF-14)")

    # All 48 W/RQ/grave lifecycle rows must be explicitly dispositioned.
    if len(lifecycle_rows(document)) != 48:
        errors.append(f"expected 48 lifecycle rows, found {len(lifecycle_rows(document))}")

    return errors


def main() -> int:
    try:
        errors = check(ROOT)
    except ContractError as exc:
        print(f"CLAIM STATUS CONTRACT: FAIL\n- {exc}")
        return 1
    if errors:
        print("CLAIM STATUS CONTRACT: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    document = load_document(ROOT / STATUS_PATH)
    print(
        "CLAIM STATUS CONTRACT: PASS "
        f"({len(document['validated'])} validated, {len(document['open'])} open, "
        f"{len(document['graves'])} graves, {len(document['reopened'])} reopened; "
        f"48 lifecycle rows, lifecycle={canonical_lifecycle_sha256(document)[:12]}, "
        f"contract={canonical_contract_sha256(document)[:12]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

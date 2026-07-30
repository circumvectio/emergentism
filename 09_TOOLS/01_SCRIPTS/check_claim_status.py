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

# Successor targets that live under another owner rather than in this register.
EXTERNAL_OWNER_ID = re.compile(r"^(W\d+[a-e]?(-[A-Z]+)?|E\d+|GP-\d{2}|KSC-\d{2}|HC-\d{2})$")

REQUIRED_INVESTIGATION_FIELDS = (
    "parent",
    "question",
    "parent_kill_does_not_reach",
    "discriminator",
    "kill",
    "survivor",
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
                  "investigation_authorization","validated","open","graves",
                  "investigations","typed_survivors"}
# HOLE 3: a counterexample must carry content, not merely be non-blank.
PLACEHOLDER = re.compile(r"^\s*(none|n/?a|tbd|todo|-+|\.+|x+|unknown|see above)\s*\.?\s*$", re.I)
MIN_COUNTEREXAMPLE = 25
EXPECTED_AUTHORIZATION = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md"
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


class ContractError(ValueError):
    """Raised when the register fails closed."""


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


def check(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    path = root / STATUS_PATH
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"{STATUS_PATH}: invalid JSON-subset YAML: {exc}") from exc

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

    # HOLE 1: an unknown top-level section is unvalidated territory. A block of
    # live refuted claims appended under a new key used to pass.
    for key in document:
        if key not in KNOWN_SECTIONS:
            errors.append(f"unknown top-level section {key!r} — unvalidated territory, refused")

    # Owner authority may open a distinct investigation. It cannot alter a
    # grave's validation status and supplies no evidence for the new question.
    authorization = document.get("investigation_authorization")
    if not isinstance(authorization, dict):
        errors.append("investigation_authorization block is required")
    else:
        receipt = authorization.get("receipt")
        rp = Path(receipt) if isinstance(receipt, str) else None
        if rp is None or rp.is_absolute() or ".." in rp.parts:
            errors.append(f"investigation_authorization: receipt must be repo-relative, got {receipt!r}")
        elif receipt != EXPECTED_AUTHORIZATION:
            errors.append(f"investigation_authorization: unexpected receipt {receipt!r}")
        else:
            f = (root / rp).resolve()
            if not f.is_file() or not f.is_relative_to(root) or f.stat().st_size < 500:
                errors.append(f"investigation_authorization: receipt missing, outside repo, or empty: {receipt}")
        for field in ("instruction", "scope", "what_it_does_not_do"):
            if not str(authorization.get(field, "")).strip():
                errors.append(f"investigation_authorization: {field} is required")
        authorized = authorization.get("authorized_question_ids")
        if not isinstance(authorized, list) or any(not isinstance(x, str) for x in authorized):
            errors.append("investigation_authorization: authorized_question_ids must be a string list")

    seen: dict[str, str] = {}

    def claim_id(row_id: str, section: str) -> None:
        if row_id in seen:
            errors.append(f"duplicate id {row_id} in {section} and {seen[row_id]}")
        seen[row_id] = section

    # --- validated -------------------------------------------------------
    for row in _rows(document, "validated"):
        row_id = _text(row.get("id"), "validated.id")
        claim_id(row_id, "validated")
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

    # --- open ------------------------------------------------------------
    open_ids: set[str] = set()
    for row in _rows(document, "open"):
        row_id = _text(row.get("id"), "open.id")
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

    missing_baseline = sorted(set(PINNED_GRAVE_STATUS) - grave_ids)
    if missing_baseline:
        errors.append(f"baseline graves may not disappear: {', '.join(missing_baseline)}")
    numbers = sorted(int(row_id.split("-")[1]) for row_id in grave_ids if DF_ID.fullmatch(row_id))
    if numbers and numbers != list(range(1, max(numbers) + 1)):
        errors.append("grave ids must remain contiguous from DF-01 through the newest grave")

    # --- investigations --------------------------------------------------
    investigation_ids: set[str] = set()
    for row in _rows(document, "investigations"):
        row_id = _text(row.get("id"), "reopened.id")
        claim_id(row_id, "investigations")
        investigation_ids.add(row_id)
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

    authorized_ids = set(authorization.get("authorized_question_ids", [])) if isinstance(authorization, dict) else set()
    if authorized_ids != investigation_ids:
        errors.append(
            "investigation_authorization must name exactly the current RQ rows: "
            f"missing={sorted(investigation_ids - authorized_ids)} extra={sorted(authorized_ids - investigation_ids)}"
        )

    # --- typed survivors -------------------------------------------------
    # A retyped survivor may narrow a failed claim. It may not restore the
    # arithmetic-looking Titan form or inherit FORMALLY-VALID by relabelling.
    for row in (document.get("typed_survivors") or []):
        if not isinstance(row, dict):
            errors.append("typed_survivors: every row must be an object")
            continue
        row_id = str(row.get("id", "")).strip()
        if not TR_ID.fullmatch(row_id):
            errors.append(f"typed_survivors: ids must look like TR-nn, got {row_id!r} — "
                          "a grave id here would assert a refuted form as valid")
            continue
        claim_id(row_id, "typed_survivors")
        if row.get("status") != "NARROWED":
            errors.append(f"{row_id}: a typed survivor must carry NARROWED, never restored validity")
        if row.get("tier") != "S":
            errors.append(f"{row_id}: typed survivor must be selected tier S")
        survivors = row.get("survivors")
        if not isinstance(survivors, list) or len(survivors) != 3 or any(not str(x).strip() for x in survivors):
            errors.append(f"{row_id}: exactly three typed survivor statements are required")
        for field in ("original_claim", "disposition", "owner", "boundary"):
            if not str(row.get(field, "")).strip():
                errors.append(f"{row_id}: typed survivor rows must state {field}")

    # --- successor resolution -------------------------------------------
    known = grave_ids | investigation_ids | open_ids
    for grave, successor in sorted(grave_successors.items()):
        if successor is None:
            continue
        if successor in known:
            continue
        if EXTERNAL_OWNER_ID.fullmatch(successor):
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
    document = json.loads((ROOT / STATUS_PATH).read_text(encoding="utf-8"))
    print(
        "CLAIM STATUS CONTRACT: PASS "
        f"({len(document['validated'])} validated, {len(document['open'])} open, "
        f"{len(document['graves'])} graves, {len(document['investigations'])} investigations)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

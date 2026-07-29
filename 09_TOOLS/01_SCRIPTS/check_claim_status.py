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
WAGER_ID = re.compile(r"^W\d+[a-e]?(-[A-Z]+)?$")
DOCKET_ID = re.compile(r"^A[0-7]$")

# Successor targets that live under another owner rather than in this register.
EXTERNAL_OWNER_ID = re.compile(r"^(W\d+[a-e]?(-[A-Z]+)?|E\d+|GP-\d{2}|KSC-\d{2}|HC-\d{2})$")

REQUIRED_REOPEN_FIELDS = (
    "parent",
    "question",
    "parent_kill_does_not_reach",
    "discriminator",
    "kill",
    "survivor",
)


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
    errors: list[str] = []
    path = root / STATUS_PATH
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"{STATUS_PATH}: invalid JSON-subset YAML: {exc}") from exc

    for rel in (HUMAN_OWNER, CONJECTURES, RECORD_LEDGER):
        if not (root / rel).is_file():
            errors.append(f"missing cross-referenced owner: {rel.as_posix()}")

    live = set(document.get("live_statuses") or [])
    terminal = set(document.get("terminal_statuses") or [])
    one_way = set(document.get("one_way_statuses") or [])
    if not live or not terminal:
        raise ContractError("status vocabularies must be declared")
    if live & terminal:
        errors.append(f"a status cannot be both live and terminal: {sorted(live & terminal)}")
    if not one_way <= terminal:
        errors.append("every one-way status must also be terminal")

    # An owner reopening is a ruling, and a ruling needs a receipt on disk.
    if any(
        isinstance(row, dict) and row.get("status") == "OWNER-REOPENED"
        for row in (document.get("graves") or [])
    ):
        reopening = document.get("owner_reopening")
        if not isinstance(reopening, dict):
            errors.append("OWNER-REOPENED rows require an owner_reopening block")
        else:
            receipt = reopening.get("receipt")
            if not isinstance(receipt, str) or not (root / receipt).is_file():
                errors.append(f"owner_reopening: missing ruling receipt {receipt!r}")
            for field in ("ruling", "scope", "what_it_does_not_do"):
                if not str(reopening.get(field, "")).strip():
                    errors.append(f"owner_reopening: {field} is required")

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
        if status not in live | terminal:
            errors.append(f"{row_id}: unknown status {status}")
        try:
            _text(row.get("form"), f"{row_id}.form")
            _text(row.get("counterexample"), f"{row_id}.counterexample")
        except ContractError as exc:
            errors.append(str(exc))
        if status in one_way and not str(row.get("counterexample", "")).strip():
            errors.append(f"{row_id}: a one-way status must cite the counterexample that killed it")
        # The one-way rule, mechanically. Once a counterexample is on the record a
        # row may never drift back into a live status. Exactly three lawful moves
        # exist: NARROWED with a named successor, a brand-new RQ row, or an
        # explicit OWNER-REOPENED ruling that keeps the counterexample and
        # declares how the claim could return.
        if str(row.get("counterexample", "")).strip() and status in live:
            if status == "NARROWED":
                if row.get("successor") is None:
                    errors.append(f"{row_id}: NARROWED requires the surviving weaker form to be named")
            elif status == "OWNER-REOPENED":
                if not str(row.get("status_before_reopening", "")).strip():
                    errors.append(f"{row_id}: OWNER-REOPENED must record the status it was reopened from")
                if not str(row.get("repair_path", "")).strip():
                    errors.append(f"{row_id}: OWNER-REOPENED must declare a repair_path")
            else:
                errors.append(
                    f"{row_id}: cites a counterexample but carries live status {status}; "
                    "open a new reopened row instead of reviving the parent"
                )
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

    if len(grave_ids) != 22:
        errors.append(f"expected the 22 recorded dead forms, found {len(grave_ids)}")
    missing = [f"DF-{n:02d}" for n in range(1, 23) if f"DF-{n:02d}" not in grave_ids]
    if missing:
        errors.append(f"grave ids are not contiguous, missing: {', '.join(missing)}")

    # --- reopened --------------------------------------------------------
    reopened_ids: set[str] = set()
    for row in _rows(document, "reopened"):
        row_id = _text(row.get("id"), "reopened.id")
        claim_id(row_id, "reopened")
        reopened_ids.add(row_id)
        if not RQ_ID.fullmatch(row_id):
            errors.append(f"{row_id}: reopened ids must look like RQ-nn")
        for field in REQUIRED_REOPEN_FIELDS:
            try:
                _text(row.get(field), f"{row_id}.{field}")
            except ContractError as exc:
                errors.append(str(exc))
        if row.get("tier") != "C":
            errors.append(f"{row_id}: a reopened question is a conjecture and must be tier C")
        docket = row.get("docket")
        if not isinstance(docket, str) or not DOCKET_ID.fullmatch(docket):
            errors.append(f"{row_id}: reopened rows need an adequacy docket A0-A7")
        parent = row.get("parent")
        if isinstance(parent, str) and parent not in grave_ids and parent not in open_ids:
            errors.append(f"{row_id}: parent {parent} is neither a grave nor an open wager")

    # --- successor resolution -------------------------------------------
    known = grave_ids | reopened_ids | open_ids
    for grave, successor in sorted(grave_successors.items()):
        if successor is None:
            continue
        if successor in known:
            continue
        if EXTERNAL_OWNER_ID.fullmatch(successor):
            continue
        errors.append(f"{grave}: successor {successor} resolves to no known id or external owner")

    # Every reopened question must be claimed by the grave it descends from,
    # so a resurrection can never float free of the record.
    for row in document["reopened"]:
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
        f"{len(document['graves'])} graves, {len(document['reopened'])} reopened)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

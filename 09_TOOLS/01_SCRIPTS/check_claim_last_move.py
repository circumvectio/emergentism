#!/usr/bin/env python3
"""Forward-only last_move contract for CLAIM_STATUS.yaml.

A status change without a last_move triple is red.
A well-formed triple is green.
A triple whose evidence path does not exist is red.

Presence is not shape: last_move must be {mover, date, evidence}.
This checker does not invent movers and does not back-fill folklore.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATUS_PATH = Path("00_META/claim_status/CLAIM_STATUS.yaml")
BUCKETS = ("validated", "open", "graves", "investigations", "reopened", "typed_survivors", "restored")
LAST_MOVE_KEYS = {"mover", "date", "evidence"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER = re.compile(r"^(none|n/?a|tbd|todo|unknown|yves|ai|agent)$", re.I)

# Frozen statuses at the last_move contract's introduction.
# Changing a status without a last_move triple fails. Updating this pin
# without a matching last_move on the row is not a substitute for the triple.
PINNED_STATUS = {
    "FV-01": "FORMALLY-VALID",
    "FV-02": "FORMALLY-VALID",
    "FV-03": "FORMALLY-VALID",
    "FV-04": "FORMALLY-VALID",
    "FV-05": "FORMALLY-VALID",
    "FV-06": "FORMALLY-VALID",
    "FV-07": "FORMALLY-VALID",
    "FV-08": "FORMALLY-VALID",
    "FV-09": "FORMALLY-VALID",
    "FV-10": "FORMALLY-VALID",
    "FV-11": "FORMALLY-VALID",
    "FV-12": "FORMALLY-VALID",
    "FV-13": "FORMALLY-VALID",
    "FV-14": "FORMALLY-VALID",
    "FV-15": "FORMALLY-VALID",
    "FV-16": "FORMALLY-VALID",
    "FV-17": "FORMALLY-VALID",
    "FV-18": "FORMALLY-VALID",
    "FV-19": "FORMALLY-VALID",
    "FV-20": "FORMALLY-VALID",
    "FV-21": "FORMALLY-VALID",
    "W0-CROWN": "NOT-WELL-POSED",
    "W1": "COMPONENT-SUPPORTED",
    "W2": "COMPONENT-SUPPORTED",
    "W3": "OPEN-EMPIRICAL",
    "W4": "OPEN-EMPIRICAL",
    "W5": "OPEN-EMPIRICAL",
    "W6": "OPEN-EMPIRICAL",
    "W7a": "OPEN-EMPIRICAL",
    "W7b": "OPEN-EMPIRICAL",
    "W7c": "OPEN-EMPIRICAL",
    "W7d": "OPEN-EMPIRICAL",
    "W7e": "OPEN-EMPIRICAL",
    "W8": "COMPONENT-SUPPORTED",
    "W9": "COMPONENT-SUPPORTED",
    "W10": "OPEN-EMPIRICAL",
    "W11": "DECORATIVE",
    "W12": "OPEN-EMPIRICAL",
    "DF-01": "FORMALLY-REFUTED",
    "DF-02": "CATEGORY-ERROR",
    "DF-03": "EMPIRICALLY-REFUTED",
    "DF-04": "FORMALLY-REFUTED",
    "DF-05": "CATEGORY-ERROR",
    "DF-06": "EMPIRICALLY-REFUTED",
    "DF-07": "EMPIRICALLY-REFUTED",
    "DF-08": "FORMALLY-REFUTED",
    "DF-09": "FORMALLY-REFUTED",
    "DF-10": "FORMALLY-REFUTED",
    "DF-11": "FORMALLY-REFUTED",
    "DF-12": "FORMALLY-REFUTED",
    "DF-13": "NOT-WELL-POSED",
    "DF-14": "FORMALLY-REFUTED",
    "DF-15": "CATEGORY-ERROR",
    "DF-16": "FORMALLY-REFUTED",
    "DF-17": "NOT-WELL-POSED",
    "DF-18": "NOT-WELL-POSED",
    "DF-19": "FORMALLY-REFUTED",
    "DF-20": "CATEGORY-ERROR",
    "DF-21": "FORMALLY-REFUTED",
    "DF-22": "PROCESS-DEFECT",
    "RQ-01": "OPEN-EMPIRICAL",
    "RQ-02": "OPEN-EMPIRICAL",
    "RQ-03": "NARROWED",
    "RQ-04": "NOT-WELL-POSED",
    "RQ-05": "OPEN-EMPIRICAL",
    "RQ-06": "OPEN-EMPIRICAL",
    "RQ-07": "NARROWED",
    "RQ-08": "NARROWED",
    "RQ-09": "NARROWED",
    "TR-01": "FORMALLY-VALID",
}


def load_document(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"{path}: top level must be an object")
    return document


def claim_rows(document: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for bucket in BUCKETS:
        for row in document.get(bucket) or []:
            if isinstance(row, dict) and row.get("id"):
                rows.append((bucket, row))
    return rows


def evidence_path(value: str) -> str:
    rel = value.strip()
    if ":" in rel:
        head, tail = rel.rsplit(":", 1)
        if re.fullmatch(r"\d+(-\d+)?", tail):
            rel = head
    return rel


def validate_last_move(
    row: dict[str, Any],
    *,
    root: Path,
    pinned: dict[str, str],
) -> list[str]:
    row_id = str(row.get("id"))
    status = str(row.get("status", ""))
    errors: list[str] = []
    move = row.get("last_move")
    pinned_status = pinned.get(row_id)
    if move is None:
        if pinned_status is None:
            errors.append(f"{row_id}: new row requires last_move")
        elif status != pinned_status:
            errors.append(f"{row_id}: status changed without last_move")
        return errors
    if not isinstance(move, dict):
        errors.append(f"{row_id}: last_move must be an object")
        return errors
    missing = sorted(LAST_MOVE_KEYS - set(move))
    extra = sorted(set(move) - LAST_MOVE_KEYS)
    if missing:
        errors.append(f"{row_id}: last_move missing {', '.join(missing)}")
    if extra:
        errors.append(f"{row_id}: last_move unknown keys: {', '.join(extra)}")
    mover = move.get("mover")
    date = move.get("date")
    evidence = move.get("evidence")
    if not isinstance(mover, str) or not mover.strip() or PLACEHOLDER.match(mover.strip()):
        errors.append(f"{row_id}: last_move.mover must be a named adjudicator")
    if not isinstance(date, str) or not DATE.match(date):
        errors.append(f"{row_id}: last_move.date must be YYYY-MM-DD")
    if not isinstance(evidence, str) or not evidence.strip():
        errors.append(f"{row_id}: last_move.evidence is required")
        return errors
    rel = evidence_path(evidence)
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{row_id}: last_move.evidence must be repo-relative")
        return errors
    if not (root / rel).is_file():
        errors.append(f"{row_id}: last_move.evidence does not exist: {rel}")
    return errors


def check(document: dict[str, Any] | None = None, root: Path = ROOT) -> list[str]:
    root = root.resolve()
    if document is None:
        document = load_document(root / STATUS_PATH)
    errors: list[str] = []
    seen: set[str] = set()
    for _bucket, row in claim_rows(document):
        row_id = str(row["id"])
        if row_id in seen:
            errors.append(f"duplicate id {row_id}")
        seen.add(row_id)
        errors.extend(validate_last_move(row, root=root, pinned=PINNED_STATUS))
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("CLAIM LAST_MOVE: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("CLAIM LAST_MOVE: PASS (forward-only triple; no folklore back-fill)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

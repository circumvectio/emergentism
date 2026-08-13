#!/usr/bin/env python3
"""Validate the staged open-problem register.

A green run proves the register is well-typed. It does not pay a problem,
does not raise world contact, and does not say the Amrita has emerged.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "12_PUBLIC_SITE/record/problems.json"
EUB_PROTOCOL_REL = Path(
    "03_METHODOLOGY/03_PREREGISTRATIONS/"
    "04_EMERGENCE_UNFOLDING_BENCHMARK_v0.1.md"
)
REQUIRED = (
    "id",
    "class",
    "tier",
    "title",
    "statement",
    "acceptance",
    "kill_framing",
    "best_attempt",
    "why_fails",
    "owner",
    "runnable",
)
CLASSES = {"executable_internal", "well_posed_unpaid", "underdefined"}
BANNED = (
    "the amrita has emerged",
    "halāhala is contained",
    "halahala is contained",
)


def main() -> int:
    data = json.loads(REG.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema") != "emergentism/open-problems/v0":
        errors.append("schema drift")
    if data.get("world_contact_accepted") != 0:
        errors.append("register must not mint world contact")
    if data.get("attention_capture") is not False:
        errors.append("attention_capture must be false")
    if data.get("k_star") != 0:
        errors.append("k_star must remain 0")
    seen: set[str] = set()
    eub_row: dict[str, object] | None = None
    for row in data.get("problems") or []:
        rid = row.get("id", "?")
        for key in REQUIRED:
            if key not in row:
                errors.append(f"{rid}: missing {key}")
        if rid in seen:
            errors.append(f"duplicate id {rid}")
        seen.add(rid)
        if rid == "ASI-UNFOLD-00":
            eub_row = row
        if row.get("class") not in CLASSES:
            errors.append(f"{rid}: bad class")
        blob = " ".join(str(row.get(k, "")) for k in ("title", "statement", "acceptance", "best_attempt")).lower()
        for phrase in BANNED:
            if phrase in blob:
                errors.append(f"{rid}: banned crown phrase")
        runnable = row.get("runnable") is True
        if row.get("class") == "executable_internal":
            if not runnable:
                errors.append(f"{rid}: executable_internal must be runnable")
            cmd = row.get("command", "")
            if not isinstance(cmd, str) or "python3" not in cmd:
                errors.append(f"{rid}: executable row needs a python3 command")
            else:
                script = cmd.split()[-1]
                if not (ROOT / script).is_file():
                    errors.append(f"{rid}: command target missing: {script}")
        if row.get("class") == "underdefined" and runnable:
            errors.append(f"{rid}: underdefined must not be runnable")
        owner = row.get("owner", "")
        if owner and not (ROOT / owner).exists():
            errors.append(f"{rid}: owner missing: {owner}")
    if eub_row is None:
        errors.append("missing ASI-UNFOLD-00")
    else:
        if eub_row.get("class") != "underdefined":
            errors.append("ASI-UNFOLD-00: must remain underdefined until freeze gates close")
        if eub_row.get("runnable") is not False:
            errors.append("ASI-UNFOLD-00: must remain non-runnable until a harness exists")
        if eub_row.get("owner") != EUB_PROTOCOL_REL.as_posix():
            errors.append("ASI-UNFOLD-00: must route to the EUB-1 methodology owner")
    protocol = ROOT / EUB_PROTOCOL_REL
    if not protocol.is_file():
        errors.append(f"EUB-1 protocol missing: {EUB_PROTOCOL_REL}")
    else:
        protocol_text = protocol.read_text(encoding="utf-8")
        for marker in (
            "Track A — hidden-ground-truth synthetic lineages",
            "Track B — disclosed real-system lineage",
            "Track-by-dimension applicability",
            "INVALID-RUN",
            "None of these states is “ASI.”",
        ):
            if marker not in protocol_text:
                errors.append(f"EUB-1 protocol missing boundary marker: {marker}")
    if errors:
        print("OPEN PROBLEMS: FAIL")
        print("\n".join(errors))
        return 1
    print(
        f"OPEN PROBLEMS: PASS ({len(seen)} holes typed; "
        "none paid; Amrita not emerged)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

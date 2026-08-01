#!/usr/bin/env python3
"""Re-check 00_WORK_IN_PROGRESS/README.md against the corpus it describes.

WHY. A manifest of open work has one characteristic failure: it drifts in the
direction that flatters us. Items quietly disappear when they go stale, counts stop
matching the registers they were copied from, and the folder slowly becomes a list of
things we have decided not to think about. 00_ESTABLISHED has a guard against
becoming a promotion path; this is the mirror guard against becoming a graveyard.

WHAT IS CHECKED
  · every count the manifest states is RECOMPUTED and must match
  · the entries that are still genuinely open must still be listed
  · the folder must keep declaring that it owns nothing
  · the "must never become" fences must survive

Exits 0 if the manifest still tells the truth, 1 otherwise.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "00_WORK_IN_PROGRESS" / "README.md"
REGISTER = ROOT / "00_META" / "00_THE_CLAIM_STATUS_REGISTER.md"
# THE AUTHORITY. The .md above is a human mirror; this is the machine source. An
# earlier draft of this checker validated the manifest against its own parse of the
# mirror, which is circular AND disagreed with check_claim_status.py.
STATUS_YAML = ROOT / "00_META" / "claim_status" / "CLAIM_STATUS.yaml"
RECEIPT_DIRS = (
    ROOT / "11_UPLINK" / "50_AUDITS_AND_EXECUTIONS",
    ROOT / "11_UPLINK" / "60_SESSION_PACKETS",
)
CLOSURE_RECEIPT_DIR = ROOT / "11_UPLINK" / "50_AUDITS_AND_EXECUTIONS"

# Items that are open as of 2026-07-30. Removing one from the manifest requires a
# ruling to point at; this list is what makes "it went quiet" insufficient.
# G-0 was removed from this list on 2026-07-30 because it was RULED on 2026-07-29 and
# the manifest had been listing it as open — the guard was pinning a stale entry, which
# is the mirror of the failure it exists to prevent. It stays referenced in the manifest
# as CLOSED, and the checker below verifies that rather than its openness.
MUST_STAY_LISTED = ["GP-03"]
LANDED_CLOSURES = {
    "§5.1": "193_FIVE_RULINGS_SIGNED_2026_07_31.md",
    "G-0": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "G-0b": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "FOUNDATION-KSC-04": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "KSC-02-ACTIVE-PROJECTION-DRIFT": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "BODY-SURVEY-04-06": "234_FULL_CORPUS_ADJUDICATION_AND_COHERENCE_CALIBRATION_2026_08_01.md",
    "PUBLIC-LIFECYCLE": "238_PUBLIC_LIFECYCLE_CLOSURE_2026_08_01.md",
    "CLAIM-DISPOSITION": "239_OPEN_CLAIM_DISPOSITION_2026_08_01.md",
}

FENCES = [
    "holds no doctrine",
    "owns nothing",
    "A promotion path",
    "A graveyard",
    "An authority",
]


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print("WORK IN PROGRESS: FAIL\n- 00_WORK_IN_PROGRESS/README.md is missing")
        return 1
    text = MANIFEST.read_text(encoding="utf-8")

    # --- A · the receipt-file count must match ------------------------------
    n_receipts = sum(
        1
        for d in RECEIPT_DIRS
        if d.is_dir()
        for p in d.rglob("*.md")
        if re.match(r"^\d{2,3}[_A-Za-z]", p.name)
    )
    # accepts "306 numbered receipts" or "306 receipt files" — the manifest says the
    # former, because 336 .md files live in those folders and 30 of them are READMEs,
    # AGENTS.md and CLAUDE.md. Counting those as receipts inflated a published figure.
    claimed = re.search(r"(\d+)\s+numbered receipts", text) or re.search(r"(\d+) receipt files", text)
    if not claimed:
        errors.append("the manifest states no receipt-file count")
    elif int(claimed.group(1)) != n_receipts:
        errors.append(
            f"manifest says {claimed.group(1)} receipt files; there are {n_receipts}. "
            "Recount, or say why the scope differs."
        )

    # --- B · the claim-status counts must match THE MACHINE SOURCE ----------
    if STATUS_YAML.exists():
        import json

        try:
            data = json.loads(STATUS_YAML.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"CLAIM_STATUS.yaml is unreadable: {exc}")
            data = {}
        for bucket in ("validated", "open", "graves", "reopened"):
            rows = data.get(bucket)
            if not isinstance(rows, list):
                # Was a silent `continue`: a bucket that went missing or changed shape
                # made its count unverifiable AND unmentioned, so the checker passed
                # while checking one fewer thing than its message claims.
                errors.append(
                    f"CLAIM_STATUS.yaml bucket '{bucket}' is missing or is not a list "
                    f"(got {type(rows).__name__}); its count could not be checked"
                )
                continue
            actual = len(rows)
            m = re.search(rf"^\s*(\d+)\s+{bucket}\b", text, re.M)
            if not m:
                errors.append(f"the manifest does not state a count for '{bucket}'")
            elif int(m.group(1)) != actual:
                errors.append(
                    f"manifest says {m.group(1)} {bucket}; CLAIM_STATUS.yaml has {actual}"
                )
    else:
        errors.append("00_META/claim_status/CLAIM_STATUS.yaml is missing — no authority to check against")

    # --- C · the ambiguous-receipt figure must match its own checker --------
    cc = ROOT / "09_TOOLS" / "01_SCRIPTS" / "check_receipt_citations.py"
    if cc.exists():
        src = cc.read_text(encoding="utf-8")
        m = re.search(r"AMBIGUOUS_BASELINE\s*=\s*(\d+)", src)
        if m:
            baseline = m.group(1)
            if baseline not in text:
                errors.append(
                    f"the citation checker holds {baseline} ambiguous receipt numbers; "
                    f"the manifest does not state that figure. The two must agree or a "
                    f"reader cannot tell which is stale."
                )

    # --- D · open items may not vanish without a ruling ---------------------
    for item in MUST_STAY_LISTED:
        if item not in text:
            errors.append(
                f"'{item}' was removed from the open list. Removal requires a landed "
                "ruling or result to cite; going quiet is not resolution, and this "
                "manifest's own kill has fired."
            )

    for item, receipt in LANDED_CLOSURES.items():
        if not (CLOSURE_RECEIPT_DIR / receipt).is_file():
            errors.append(
                f"landed closure '{item}' points at missing source '{receipt}'"
            )
        closure_row = re.search(
            rf"^\|[^\n]*{re.escape(item)}[^\n]*CLOSED[^\n]*$", text, re.M | re.I
        )
        if not closure_row or receipt not in closure_row.group(0):
            errors.append(
                f"landed closure '{item}' is not retained with its source '{receipt}'"
            )

    # --- E · the fences must survive ---------------------------------------
    for f in FENCES:
        if f not in text:
            errors.append(f"the fence '{f}' is missing — the folder could be cited as authority")

    if errors:
        print("WORK IN PROGRESS: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    open_label = "open item" if len(MUST_STAY_LISTED) == 1 else "open items"
    print(
        f"WORK IN PROGRESS: PASS ({n_receipts} receipt files counted; claim-register "
        f"counts agree; {len(MUST_STAY_LISTED)} {open_label} still listed; "
        f"{len(LANDED_CLOSURES)} landed closures retained; "
        f"{len(FENCES)} fences intact)"
    )
    print(
        "  scope: this proves the manifest's COUNTS match the corpus and its open items "
        "are still listed. It does NOT prove the list is complete — an open question "
        "nobody wrote down is invisible here too."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

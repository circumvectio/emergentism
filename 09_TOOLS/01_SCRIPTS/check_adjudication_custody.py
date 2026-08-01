#!/usr/bin/env python3
"""Replay the durable custody contract for the 229-finding adjudication.

The three JSONL files are dated evidence, not live doctrine or an authority to
change a finding. This checker verifies their frozen bytes, typed partitions,
and additive-review relationships against Receipt 234. It deliberately does
not read the external raw reconstruction, workflow journal, or source session
whose hashes the ledgers retain, and it does not re-adjudicate any claim.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = Path("09_TOOLS/08_AUDIT_ARTIFACTS")
FIRST_LEDGER_REL = AUDIT_DIR / "2026_08_01_FIRST_60_ADJUDICATION.jsonl"
REMAINING_LEDGER_REL = AUDIT_DIR / "2026_08_01_REMAINING_169_ADJUDICATION.jsonl"
SUPPLEMENT_REL = AUDIT_DIR / "2026_08_01_REMAINING_169_INDEPENDENT_REVIEW_SUPPLEMENT.jsonl"
RECEIPT_REL = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
    "234_FULL_CORPUS_ADJUDICATION_AND_COHERENCE_CALIBRATION_2026_08_01.md"
)

FROZEN_DIGESTS = {
    FIRST_LEDGER_REL: "7ee2f5389d4d53c3142259f54a142390af96b19e982d53e082827eb024041e92",  # pragma: allow-secret
    REMAINING_LEDGER_REL: "af3520a7583148bc382538aa0595be6fb3611139ff6d02004bf98541540eb19f",  # pragma: allow-secret
    SUPPLEMENT_REL: "92931867a86b49a26f8629adb772770678d92ec4ac788c892bc768033e72bb7d",  # pragma: allow-secret
}
RECEIPT_DIGEST = "b1bd590719cc8cf83d5cf51dbcf12967af1cd939adf10aee0b84654b9f191c25"
FIRST_META = {
    "record_type": "meta",
    "schema": "emergentism/adjudication-ledger/v1",
    "scope": "first 60 of 229 actionable findings",
    "count": 60,
    "real": 37,
    "false": 23,
    "source_journal_sha256": "b12986fb977ce6cfec0e38bd8fc134014d2ad35d4d650df6caa1a69d5908b0ca",
    "ordering_note": (
        "journal_result_ordinal records asynchronous verification-result arrival order; "
        "file and line are the stable finding identity"
    ),
}
REMAINING_META = {
    "record_type": "meta",
    "schema": "emergentism/adjudication-ledger/v1",
    "scope": "remaining 169 of 229 actionable findings",
    "count": 169,
    "original_verdict_counts": {
        "REAL_FIXED": 54,
        "REAL_OPEN": 98,
        "FALSE": 8,
        "DUPLICATE": 4,
        "OWNER_GATE": 5,
    },
    "raw_findings_sha256": "93f72d87e899122c18945045f259a3223f101fa9df5187c721c32cd7fb805e6c",
    "source_workflow_journal_sha256": "b12986fb977ce6cfec0e38bd8fc134014d2ad35d4d650df6caa1a69d5908b0ca",
    "source_session_sha256": "0666bf47f049438301b17239cae26b393a14c1c5376c40505999abceab921c13",
    "ordering_note": (
        "remaining_ordinal 1 is global actionable finding 61; global_actionable_id = "
        "60 + remaining_ordinal"
    ),
}
SUPPLEMENT_META = {
    "record_type": "meta",
    "schema": "emergentism/adjudication-review-supplement/v1",
    "scope": "independent read-only review of remaining actionable findings 61-229",
    "source_ledger": REMAINING_LEDGER_REL.name,
    "source_ledger_sha256": FROZEN_DIGESTS[REMAINING_LEDGER_REL],
    "correction_count": 2,
    "closure_confirmation_count": 7,
    "gate_preservation_count": 1,
    "docket_count": 1,
    "immutability_note": (
        "The source ledger is retained byte-for-byte. Corrections below control later "
        "claims about reviewed disposition without rewriting the original adjudication "
        "evidence."
    ),
}

FIRST_RECORD_KEYS = {"journal_result_ordinal", "verdict", "file", "line"}
REMAINING_RECORD_KEYS = {
    "remaining_ordinal",
    "global_actionable_id",
    "lane",
    "file",
    "line",
    "kind",
    "severity",
    "original_verdict",
    "final_disposition",
}
REMAINING_FINAL_COUNTS = {
    "FIXED_PREEXISTING_OR_INHERITED": 54,
    "FIXED_IN_THIS_ADJUDICATION": 95,
    "RESOLVED_SOURCE_OWNER_ROUTE": 1,
    "RESOLVED_SYNTAX_ONLY": 2,
    "DISMISSED_FALSE": 8,
    "DEDUPLICATED": 4,
    "FENCED_ACTIVE_PENDING_K3_ARCHIVE": 1,
    "QUARANTINED_MISSING_CUSTODY": 2,
    "OWNER_GATE_OPEN_TOPOLOGY": 1,
    "OWNER_GATE_HELD_PUBLIC_DOCS": 1,
}
REMAINING_DEDUPLICATION_MAP = {
    156: 157,
    217: 198,
    219: 196,
    220: 197,
}
REVIEW_CORRECTIONS = {
    66: ("FIXED_IN_THIS_ADJUDICATION", "SUPERSEDED_FROZEN_CUSTODY"),
    183: ("FIXED_IN_THIS_ADJUDICATION", "QUARANTINED_ACTIVE_TYPE_CONFLICT"),
}
REVIEW_CLOSURES = {70, 85, 89, 130, 185, 198, 205}
REVIEW_GATE = (210, "OWNER_GATE_OPEN_TOPOLOGY")
REVIEW_DOCKET = {
    "docket_id": "KSC-02-ACTIVE-PROJECTION-DRIFT",
    "reviewed_disposition": "OPEN_FOR_SPRINT_2",
    "evidence": (
        "02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md",
        "03_METHODOLOGY/README.md",
        "01_TELEOLOGY/00_THE_GOAL.md",
        "06_ONTOLOGY/00_ONTOLOGY_ACROSS_DIMENSIONS.md",
        "05_COSMOLOGY/00_THE_ONTOLOGY_INDEX.md",
        "06_ONTOLOGY/05_THE_CREED_AND_SPIRAL.md",
        "10_SEED/01_THE_SEED_LADDER/00_THE_SEED.md",
        "10_SEED/01_THE_SEED_LADDER/D5_THE_GAME.md",
        "05_COSMOLOGY/00_D5_REGISTER_GAME_THEORY_AND_BEHAVIORAL_ECONOMICS.md",
        "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/README.md",
    ),
}
EFFECTIVE_PARTITION = {
    "repaired_or_resolved_or_safely_superseded": 151,
    "dismissed_false": 8,
    "deduplicated": 4,
    "explicitly_constrained": 6,
}


class DuplicateJsonKeyError(ValueError):
    """Reject shadowed JSON fields before they become custody evidence."""


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def contained_regular_file(root: Path, relative: Path, label: str) -> Path:
    """Resolve a constant corpus path without permitting symlink traversal."""

    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label} path must be safe and repository-relative")
    candidate = root / relative
    cursor = root
    try:
        for component in relative.parts:
            cursor /= component
            if cursor.is_symlink():
                raise ValueError(f"{label} path must not traverse a symlink")
        root_resolved = root.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing") from exc
    except (OSError, RuntimeError, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith(label):
            raise
        raise ValueError(f"{label} is unreadable: {exc}") from exc
    if not resolved.is_relative_to(root_resolved):
        raise ValueError(f"{label} path resolves outside the corpus")
    if not resolved.is_file():
        raise ValueError(f"{label} must be a regular file")
    return resolved


def load_jsonl(root: Path, relative: Path, label: str) -> tuple[list[dict[str, Any]], str]:
    """Read one nonempty JSONL artifact and its SHA-256, rejecting ambiguous bytes."""

    path = contained_regular_file(root, relative, label)
    try:
        payload = path.read_bytes()
        text = payload.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"{label} is unreadable: {exc.__class__.__name__}") from exc
    if text.startswith("\ufeff") or "\r" in text or not text.endswith("\n"):
        raise ValueError(f"{label} must be newline-terminated UTF-8 JSONL without BOM or CR")
    lines = text.splitlines()
    if not lines or any(not line.strip() for line in lines):
        raise ValueError(f"{label} must contain no blank JSONL records")
    records: list[dict[str, Any]] = []
    for ordinal, line in enumerate(lines, start=1):
        try:
            record = json.loads(line, object_pairs_hook=unique_json_object)
        except (DuplicateJsonKeyError, json.JSONDecodeError) as exc:
            raise ValueError(f"{label} line {ordinal} is invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{label} line {ordinal} must be a JSON object")
        records.append(record)
    return records, hashlib.sha256(payload).hexdigest()


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_evidence_paths(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    if not all(nonempty_string(path) for path in value) or len(value) != len(set(value)):
        return False
    for path in value:
        posix_path = PurePosixPath(path)
        windows_path = PureWindowsPath(path)
        if (
            "\\" in path
            or "\x00" in path
            or posix_path.is_absolute()
            or windows_path.is_absolute()
            or bool(windows_path.drive)
            or bool(windows_path.root)
            or ".." in posix_path.parts
            or ".." in windows_path.parts
        ):
            return False
    return True


def validate_first(records: list[dict[str, Any]], errors: list[str]) -> None:
    if len(records) != 61:
        errors.append(f"first-60 ledger must contain 61 records, found {len(records)}")
        return
    if records[0] != FIRST_META:
        errors.append("first-60 ledger metadata drifted from its frozen custody contract")
    findings = records[1:]
    ordinals: list[int] = []
    verdicts: Counter[str] = Counter()
    for index, finding in enumerate(findings, start=1):
        if set(finding) != FIRST_RECORD_KEYS:
            errors.append(f"first-60 finding {index} has an unexpected schema")
            continue
        ordinal = finding.get("journal_result_ordinal")
        if type(ordinal) is not int:
            errors.append(f"first-60 finding {index} has a non-integer result ordinal")
        else:
            ordinals.append(ordinal)
        verdict = finding.get("verdict")
        if verdict not in {"REAL", "FALSE"}:
            errors.append(f"first-60 finding {index} has an invalid verdict")
        else:
            verdicts[verdict] += 1
        if not nonempty_string(finding.get("file")) or type(finding.get("line")) is not int:
            errors.append(f"first-60 finding {index} has an invalid stable finding locator")
    if sorted(ordinals) != list(range(1, 61)):
        errors.append("first-60 result ordinals must be exactly 1 through 60")
    if verdicts != Counter({"REAL": 37, "FALSE": 23}):
        errors.append("first-60 verdict partition must remain 37 REAL / 23 FALSE")


def validate_remaining(records: list[dict[str, Any]], errors: list[str]) -> dict[int, dict[str, Any]]:
    if len(records) != 170:
        errors.append(f"remaining-169 ledger must contain 170 records, found {len(records)}")
        return {}
    if records[0] != REMAINING_META:
        errors.append("remaining-169 ledger metadata drifted from its frozen custody contract")
    findings = records[1:]
    ordinals: list[int] = []
    global_ids: list[int] = []
    original_verdicts: Counter[str] = Counter()
    final_dispositions: Counter[str] = Counter()
    by_global: dict[int, dict[str, Any]] = {}
    duplicate_map: dict[int, int] = {}
    for index, finding in enumerate(findings, start=1):
        final_disposition = finding.get("final_disposition")
        expected_keys = set(REMAINING_RECORD_KEYS)
        if final_disposition == "DEDUPLICATED":
            expected_keys.add("duplicate_of_global_actionable_id")
        if set(finding) != expected_keys:
            errors.append(f"remaining finding {index} has an unexpected schema")
            continue
        ordinal = finding.get("remaining_ordinal")
        global_id = finding.get("global_actionable_id")
        if type(ordinal) is not int or type(global_id) is not int:
            errors.append(f"remaining finding {index} has non-integer custody ordinals")
        else:
            ordinals.append(ordinal)
            global_ids.append(global_id)
            if global_id != 60 + ordinal:
                errors.append(f"remaining finding {index} violates global_actionable_id = 60 + ordinal")
            if global_id in by_global:
                errors.append(f"remaining finding {index} duplicates global actionable id {global_id}")
            by_global[global_id] = finding
        if not all(nonempty_string(finding.get(key)) for key in ("lane", "file", "kind", "severity")):
            errors.append(f"remaining finding {index} has an invalid finding locator")
        if type(finding.get("line")) is not int or finding.get("line") < 0:
            errors.append(f"remaining finding {index} has an invalid source line")
        original = finding.get("original_verdict")
        if original not in REMAINING_META["original_verdict_counts"]:
            errors.append(f"remaining finding {index} has an invalid original verdict")
        else:
            original_verdicts[original] += 1
        if final_disposition not in REMAINING_FINAL_COUNTS:
            errors.append(f"remaining finding {index} has an invalid final disposition")
        else:
            final_dispositions[final_disposition] += 1
        if final_disposition == "DEDUPLICATED":
            duplicate_of = finding.get("duplicate_of_global_actionable_id")
            if type(duplicate_of) is not int or duplicate_of == global_id or not 1 <= duplicate_of <= 229:
                errors.append(f"remaining finding {index} has an invalid duplicate target")
            elif type(global_id) is int:
                duplicate_map[global_id] = duplicate_of
    if sorted(ordinals) != list(range(1, 170)):
        errors.append("remaining ordinals must be exactly 1 through 169")
    if sorted(global_ids) != list(range(61, 230)):
        errors.append("remaining global actionable ids must be exactly 61 through 229")
    if dict(original_verdicts) != REMAINING_META["original_verdict_counts"]:
        errors.append("remaining original-verdict partition drifted")
    if dict(final_dispositions) != REMAINING_FINAL_COUNTS:
        errors.append("remaining final-disposition partition drifted")
    if duplicate_map != REMAINING_DEDUPLICATION_MAP:
        errors.append("remaining duplicate mappings drifted from the frozen custody contract")
    for duplicate_id, target_id in duplicate_map.items():
        target = by_global.get(target_id)
        if target is None:
            errors.append(f"remaining duplicate {duplicate_id} names a missing target {target_id}")
        elif target.get("final_disposition") == "DEDUPLICATED":
            errors.append(f"remaining duplicate {duplicate_id} may not target another duplicate")
    return by_global


def validate_supplement(
    records: list[dict[str, Any]],
    remaining_by_global: dict[int, dict[str, Any]],
    errors: list[str],
) -> None:
    if len(records) != 12:
        errors.append(f"review supplement must contain 12 records, found {len(records)}")
        return
    if records[0] != SUPPLEMENT_META:
        errors.append("review supplement metadata drifted from its frozen custody contract")
    corrections: dict[int, tuple[str, str]] = {}
    closures: set[int] = set()
    gate_records: list[dict[str, Any]] = []
    docket_records: list[dict[str, Any]] = []
    for index, record in enumerate(records[1:], start=1):
        record_type = record.get("record_type")
        if record_type == "disposition_correction":
            expected_keys = {
                "record_type",
                "global_actionable_id",
                "source_disposition",
                "reviewed_disposition",
                "reason",
                "evidence",
            }
        elif record_type == "closure_confirmation":
            expected_keys = {
                "record_type",
                "global_actionable_id",
                "reviewed_disposition",
                "reason",
                "evidence",
            }
        elif record_type == "gate_preservation":
            expected_keys = {
                "record_type",
                "global_actionable_id",
                "reviewed_disposition",
                "reason",
                "evidence",
            }
        elif record_type == "open_docket":
            expected_keys = {"record_type", "docket_id", "reviewed_disposition", "reason", "evidence"}
        else:
            errors.append(f"review supplement record {index} has an unknown record type")
            continue
        if set(record) != expected_keys:
            errors.append(f"review supplement record {index} has an unexpected schema")
            continue
        if not nonempty_string(record.get("reason")) or not valid_evidence_paths(record.get("evidence")):
            errors.append(f"review supplement record {index} has invalid retained evidence metadata")
        if record_type == "open_docket":
            docket_records.append(record)
            continue
        global_id = record.get("global_actionable_id")
        source = remaining_by_global.get(global_id) if type(global_id) is int else None
        if source is None:
            errors.append(f"review supplement record {index} names no remaining-ledger finding")
            continue
        reviewed = record.get("reviewed_disposition")
        if not nonempty_string(reviewed):
            errors.append(f"review supplement record {index} has no reviewed disposition")
            continue
        if record_type == "disposition_correction":
            source_disposition = record.get("source_disposition")
            if source_disposition != source.get("final_disposition"):
                errors.append(f"review correction {global_id} no longer names its source disposition")
            corrections[global_id] = (source_disposition, reviewed)
        elif record_type == "closure_confirmation":
            if (
                reviewed != "FIXED_IN_THIS_ADJUDICATION"
                or reviewed != source.get("final_disposition")
            ):
                errors.append(f"review closure {global_id} no longer confirms its source disposition")
            closures.add(global_id)
        else:
            if (global_id, reviewed) != REVIEW_GATE or reviewed != source.get("final_disposition"):
                errors.append(f"review gate {global_id} no longer preserves its source disposition")
            gate_records.append(record)
    if corrections != REVIEW_CORRECTIONS:
        errors.append("review supplement must retain exactly the two controlling disposition corrections")
    if closures != REVIEW_CLOSURES:
        errors.append("review supplement must retain exactly the seven closure confirmations")
    if len(gate_records) != 1 or (
        gate_records
        and (
            gate_records[0].get("global_actionable_id"),
            gate_records[0].get("reviewed_disposition"),
        )
        != REVIEW_GATE
    ):
        errors.append("review supplement must retain the topology owner-gate preservation")
    if len(docket_records) != 1 or (
        docket_records
        and (
            docket_records[0].get("docket_id"),
            docket_records[0].get("reviewed_disposition"),
            tuple(docket_records[0].get("evidence", [])),
        )
        != (
            REVIEW_DOCKET["docket_id"],
            REVIEW_DOCKET["reviewed_disposition"],
            REVIEW_DOCKET["evidence"],
        )
    ):
        errors.append("review supplement must retain the KSC-02 downstream-drift docket")
    effective = Counter(
        finding.get("final_disposition") for finding in remaining_by_global.values()
    )
    for global_id, (source_disposition, reviewed_disposition) in corrections.items():
        if global_id in remaining_by_global:
            effective[source_disposition] -= 1
            effective[reviewed_disposition] += 1
    repaired = sum(
        effective[disposition]
        for disposition in {
            "FIXED_PREEXISTING_OR_INHERITED",
            "FIXED_IN_THIS_ADJUDICATION",
            "RESOLVED_SOURCE_OWNER_ROUTE",
            "RESOLVED_SYNTAX_ONLY",
            "SUPERSEDED_FROZEN_CUSTODY",
        }
    )
    constrained = sum(
        effective[disposition]
        for disposition in {
            "FENCED_ACTIVE_PENDING_K3_ARCHIVE",
            "QUARANTINED_MISSING_CUSTODY",
            "QUARANTINED_ACTIVE_TYPE_CONFLICT",
            "OWNER_GATE_OPEN_TOPOLOGY",
            "OWNER_GATE_HELD_PUBLIC_DOCS",
        }
    )
    partition = {
        "repaired_or_resolved_or_safely_superseded": repaired,
        "dismissed_false": effective["DISMISSED_FALSE"],
        "deduplicated": effective["DEDUPLICATED"],
        "explicitly_constrained": constrained,
    }
    if partition != EFFECTIVE_PARTITION:
        errors.append("reviewed effective partition must remain 151 / 8 / 4 / 6")


def validate_receipt(root: Path, errors: list[str]) -> None:
    """Require Receipt 234 to state the same three frozen artifact identities."""

    try:
        receipt_path = contained_regular_file(root, RECEIPT_REL, "Receipt 234")
        receipt_bytes = receipt_path.read_bytes()
        receipt = receipt_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        errors.append(f"Receipt 234 is unreadable: {exc}")
        return
    if hashlib.sha256(receipt_bytes).hexdigest() != RECEIPT_DIGEST:
        errors.append("Receipt 234 digest drifted from its dated custody boundary")
    labels = {
        FIRST_LEDGER_REL: "First-60 adjudication ledger",
        REMAINING_LEDGER_REL: "Remaining-169 adjudication ledger",
        SUPPLEMENT_REL: "Remaining-169 independent-review supplement",
    }
    for relative, digest in FROZEN_DIGESTS.items():
        expected_row = f"| {labels[relative]} | `sha256:{digest}` |"
        if expected_row not in receipt:
            errors.append(f"Receipt 234 no longer binds {relative.name} to its frozen SHA-256")
        parent = f"- ../../{relative.as_posix()}"
        if parent not in receipt:
            errors.append(f"Receipt 234 no longer names {relative.name} as a parent artifact")
    declared_hashes = {
        "Reconstructed raw findings": REMAINING_META["raw_findings_sha256"],
        "Workflow journal": REMAINING_META["source_workflow_journal_sha256"],
        "Source session": REMAINING_META["source_session_sha256"],
    }
    declared_hashes.update(
        {labels[relative]: digest for relative, digest in FROZEN_DIGESTS.items()}
    )
    for label, digest in declared_hashes.items():
        expected_row = f"| {label} | `sha256:{digest}` |"
        if expected_row not in receipt:
            errors.append(f"Receipt 234 no longer declares the frozen SHA-256 for {label}")


def adjudication_custody_errors(root: Path = ROOT) -> list[str]:
    """Return every frozen-custody error without using external reconstruction paths."""

    errors: list[str] = []
    loaded: dict[Path, tuple[list[dict[str, Any]], str]] = {}
    labels = {
        FIRST_LEDGER_REL: "first-60 adjudication ledger",
        REMAINING_LEDGER_REL: "remaining-169 adjudication ledger",
        SUPPLEMENT_REL: "remaining-169 review supplement",
    }
    for relative, label in labels.items():
        try:
            records, digest = load_jsonl(root, relative, label)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        loaded[relative] = (records, digest)
        if digest != FROZEN_DIGESTS[relative]:
            errors.append(f"{label} digest drifted from the dated Receipt 234 boundary")
    first = loaded.get(FIRST_LEDGER_REL)
    if first is not None:
        validate_first(first[0], errors)
    remaining = loaded.get(REMAINING_LEDGER_REL)
    remaining_by_global: dict[int, dict[str, Any]] = {}
    if remaining is not None:
        remaining_by_global = validate_remaining(remaining[0], errors)
    supplement = loaded.get(SUPPLEMENT_REL)
    if supplement is not None:
        validate_supplement(supplement[0], remaining_by_global, errors)
    validate_receipt(root, errors)
    return errors


def main() -> int:
    errors = adjudication_custody_errors()
    if errors:
        print("ADJUDICATION CUSTODY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "ADJUDICATION CUSTODY: PASS (durable custody replay; 229 actionable findings; "
        "first=37/23; reviewed remaining=151/8/4/6; three frozen ledgers and Receipt "
        "234 match their hashes)"
    )
    print(
        "  scope: replays dated internal custody only; it does not re-adjudicate findings, "
        "read external raw journals, establish authority, or establish world contact."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

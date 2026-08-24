#!/usr/bin/env python3
"""Validate the non-owning conjecture/proof-attempt manifest.

The manifest is a pointer and drift surface. It never decides whether a claim
is true, promotes a tier, adopts a wager, or replaces a semantic owner.

    python3 -B 09_TOOLS/01_SCRIPTS/check_conjecture_proof_attempt_manifest.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "00_META/conjectures_and_proof_attempts/MANIFEST.json"
CLAIM_STATUS_PATH = ROOT / "00_META/claim_status/CLAIM_STATUS.yaml"

SCHEMA = "emergentism/conjecture-proof-attempt-manifest/v1"
ROUTING_ROLE = (
    "discoverability and dated completeness accounting only; no semantic "
    "authority, tier promotion, validation, or adoption"
)

TOP_KEYS = {
    "schema_version",
    "as_of_date",
    "baseline_commit",
    "routing_role",
    "scope_rules",
    "authorities",
    "catalog_snapshot",
    "source_manifest",
    "entries",
    "excluded_with_reason",
    "unresolved_discovery_debt",
    "inventory_digest",
}

ENTRY_KEYS = {
    "entry_id",
    "source_ids",
    "kind",
    "lifecycle",
    "evidence_tier",
    "validation_status_ref",
    "owner_path",
    "partition",
    "summary",
    "target_entry_ids",
    "outcome",
    "rival",
    "discriminator",
    "kill",
    "survivor",
    "relations",
}

SOURCE_KEYS = {"path", "sha256", "role"}
RELATION_KEYS = {"type", "target"}
EXCLUSION_KEYS = {"path_class", "reason"}

KINDS = {
    "CATALOG",
    "WAGER_SET",
    "CONJECTURE",
    "HYPOTHESIS",
    "FORMAL_RESULT",
    "PROOF_ATTEMPT",
    "REFUTATION",
    "ADJUDICATION",
    "MODEL",
    "STAGED_DRAFT",
    "RESEARCH_BOUNDARY",
}

LIFECYCLES = {
    "active",
    "proposal",
    "staged",
    "superseded",
    "retracted",
    "historical",
    "mixed",
}

PARTITIONS = {"live", "historical_evidence"}
SOURCE_ROLES = {
    "status_owner",
    "semantic_owner",
    "conjecture_owner",
    "formal_owner",
    "proof_attempt",
    "refutation",
    "provenance",
    "research_boundary",
    "machine_support",
}

CATALOG_SECTIONS = (
    "validated",
    "open",
    "graves",
    "investigations",
    "typed_survivors",
)

FORBIDDEN_LIVE_PREFIXES = (
    "90_ARCHIVE/",
    "91_COMPATIBILITY/",
    "12_PUBLIC_SITE/",
    "13_BOOKS/",
)

ENTRY_ID = re.compile(r"^[A-Z0-9][A-Z0-9._:-]*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path.relative_to(ROOT)}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected object in {path.relative_to(ROOT)}")
    return value


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _text(value: Any, label: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected a non-empty string")
        return ""
    return value.strip()


def _strings(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label}: expected a list")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        text = _text(item, f"{label}[{index}]", errors)
        if text:
            result.append(text)
    return result


def _exact_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected an object")
        return False
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing or extra:
        errors.append(f"{label}: key drift missing={missing} extra={extra}")
        return False
    return True


def _repo_path(raw: Any, label: str, errors: list[str]) -> Path | None:
    text = _text(raw, label, errors)
    if not text:
        return None
    pure = PurePosixPath(text)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        errors.append(f"{label}: expected normalized repository-relative path, found {text!r}")
        return None
    path = ROOT.joinpath(*pure.parts)
    try:
        path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{label}: escapes repository root")
        return None
    if not path.is_file():
        errors.append(f"{label}: dangling path {text}")
        return None
    return path


def _claim_id(row: Any) -> str | None:
    if not isinstance(row, dict):
        return None
    value = row.get("id")
    return value if isinstance(value, str) and value else None


def _inventory_payload(document: dict[str, Any]) -> dict[str, Any]:
    return {
        key: document[key]
        for key in (
            "scope_rules",
            "authorities",
            "catalog_snapshot",
            "source_manifest",
            "entries",
            "excluded_with_reason",
            "unresolved_discovery_debt",
        )
    }


def inventory_digest(document: dict[str, Any]) -> str:
    payload = json.dumps(
        _inventory_payload(document),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check() -> list[str]:
    errors: list[str] = []
    try:
        document = _load_json(MANIFEST_PATH)
        claim_status = _load_json(CLAIM_STATUS_PATH)
    except ValueError as exc:
        return [str(exc)]

    _exact_keys(document, TOP_KEYS, "manifest", errors)
    if document.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    if document.get("as_of_date") != "2026-08-24":
        errors.append("as_of_date must retain the frozen 2026-08-24 census date")
    if document.get("routing_role") != ROUTING_ROLE:
        errors.append("routing_role drifted from the non-owning boundary")
    if not COMMIT.fullmatch(str(document.get("baseline_commit", ""))):
        errors.append("baseline_commit must be a full 40-character Git OID")

    scope = document.get("scope_rules")
    if _exact_keys(
        scope,
        {
            "version",
            "definition_of_all",
            "included_roots",
            "excluded_roots",
            "admission_rule",
            "completeness_kill",
        },
        "scope_rules",
        errors,
    ):
        if scope.get("version") != "v1":
            errors.append("scope_rules.version must be v1")
        for key in ("definition_of_all", "admission_rule", "completeness_kill"):
            _text(scope.get(key), f"scope_rules.{key}", errors)
        _strings(scope.get("included_roots"), "scope_rules.included_roots", errors)
        _strings(scope.get("excluded_roots"), "scope_rules.excluded_roots", errors)

    authorities = document.get("authorities")
    if _exact_keys(
        authorities,
        {"wager_ledger", "validation_status", "evidence_tiers", "record_ledger"},
        "authorities",
        errors,
    ):
        for key, raw in authorities.items():
            _repo_path(raw, f"authorities.{key}", errors)

    catalog = document.get("catalog_snapshot")
    if not isinstance(catalog, dict) or set(catalog) != set(CATALOG_SECTIONS):
        errors.append(
            "catalog_snapshot must contain exactly " + ", ".join(CATALOG_SECTIONS)
        )
    else:
        for section in CATALOG_SECTIONS:
            declared = _strings(catalog.get(section), f"catalog_snapshot.{section}", errors)
            actual = [
                row_id
                for row in claim_status.get(section, [])
                if (row_id := _claim_id(row)) is not None
            ]
            if declared != actual:
                errors.append(
                    f"catalog_snapshot.{section} drifted: declared={declared} actual={actual}"
                )

    sources = document.get("source_manifest")
    source_paths: dict[str, str] = {}
    if not isinstance(sources, list) or not sources:
        errors.append("source_manifest: expected a non-empty list")
        sources = []
    for index, source in enumerate(sources):
        label = f"source_manifest[{index}]"
        if not _exact_keys(source, SOURCE_KEYS, label, errors):
            continue
        raw_path = _text(source.get("path"), f"{label}.path", errors)
        expected_hash = _text(source.get("sha256"), f"{label}.sha256", errors)
        role = _text(source.get("role"), f"{label}.role", errors)
        if role and role not in SOURCE_ROLES:
            errors.append(f"{label}.role: unsupported role {role!r}")
        if raw_path in source_paths:
            errors.append(f"duplicate source path {raw_path}")
        else:
            source_paths[raw_path] = expected_hash
        if expected_hash and not SHA256.fullmatch(expected_hash):
            errors.append(f"{label}.sha256: malformed digest")
        path = _repo_path(raw_path, f"{label}.path", errors)
        if path is not None and SHA256.fullmatch(expected_hash or ""):
            actual_hash = _hash(path)
            if actual_hash != expected_hash:
                errors.append(
                    f"{raw_path}: source hash drifted expected={expected_hash} actual={actual_hash}"
                )

    entries = document.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries: expected a non-empty list")
        entries = []
    by_id: dict[str, dict[str, Any]] = {}
    deferred_relations: list[tuple[str, str, str]] = []
    for index, entry in enumerate(entries):
        label = f"entries[{index}]"
        if not _exact_keys(entry, ENTRY_KEYS, label, errors):
            continue
        entry_id = _text(entry.get("entry_id"), f"{label}.entry_id", errors)
        if entry_id and not ENTRY_ID.fullmatch(entry_id):
            errors.append(f"{label}.entry_id: malformed locator {entry_id!r}")
        if entry_id in by_id:
            errors.append(f"duplicate entry_id {entry_id}")
        elif entry_id:
            by_id[entry_id] = entry

        _strings(entry.get("source_ids"), f"{entry_id}.source_ids", errors)
        kind = _text(entry.get("kind"), f"{entry_id}.kind", errors)
        lifecycle = _text(entry.get("lifecycle"), f"{entry_id}.lifecycle", errors)
        tier = _text(entry.get("evidence_tier"), f"{entry_id}.evidence_tier", errors)
        if kind and kind not in KINDS:
            errors.append(f"{entry_id}.kind: unsupported value {kind!r}")
        if lifecycle and lifecycle not in LIFECYCLES:
            errors.append(f"{entry_id}.lifecycle: unsupported value {lifecycle!r}")
        if tier and "[" not in tier:
            errors.append(f"{entry_id}.evidence_tier: must preserve bracketed tier syntax")
        _strings(
            entry.get("validation_status_ref"),
            f"{entry_id}.validation_status_ref",
            errors,
        )
        owner = _text(entry.get("owner_path"), f"{entry_id}.owner_path", errors)
        if owner and owner not in source_paths:
            errors.append(f"{entry_id}.owner_path is absent from source_manifest: {owner}")
        partition = _text(entry.get("partition"), f"{entry_id}.partition", errors)
        if partition and partition not in PARTITIONS:
            errors.append(f"{entry_id}.partition: unsupported value {partition!r}")
        if partition == "live" and owner.startswith(FORBIDDEN_LIVE_PREFIXES):
            errors.append(f"{entry_id}: archive/public projection presented as live owner")

        for field in ("summary", "outcome", "rival", "discriminator", "kill", "survivor"):
            _text(entry.get(field), f"{entry_id}.{field}", errors)

        for target in _strings(
            entry.get("target_entry_ids"), f"{entry_id}.target_entry_ids", errors
        ):
            deferred_relations.append((entry_id, "target", target))

        relations = entry.get("relations")
        if not isinstance(relations, list):
            errors.append(f"{entry_id}.relations: expected a list")
            relations = []
        for relation_index, relation in enumerate(relations):
            relation_label = f"{entry_id}.relations[{relation_index}]"
            if not _exact_keys(relation, RELATION_KEYS, relation_label, errors):
                continue
            relation_type = _text(
                relation.get("type"), f"{relation_label}.type", errors
            )
            target = _text(relation.get("target"), f"{relation_label}.target", errors)
            if target:
                deferred_relations.append((entry_id, relation_type, target))

    for source, relation_type, target in deferred_relations:
        if target not in by_id:
            errors.append(f"{source}: {relation_type} points to unknown entry {target}")

    exclusions = document.get("excluded_with_reason")
    if not isinstance(exclusions, list) or not exclusions:
        errors.append("excluded_with_reason: expected a non-empty list")
        exclusions = []
    for index, exclusion in enumerate(exclusions):
        label = f"excluded_with_reason[{index}]"
        if _exact_keys(exclusion, EXCLUSION_KEYS, label, errors):
            _text(exclusion.get("path_class"), f"{label}.path_class", errors)
            _text(exclusion.get("reason"), f"{label}.reason", errors)

    debts = _strings(
        document.get("unresolved_discovery_debt"),
        "unresolved_discovery_debt",
        errors,
    )
    if not debts:
        errors.append("unresolved_discovery_debt must state at least one bounded debt")

    # New-result anti-laundering invariants.
    slwp = by_id.get("SLWP-01")
    if slwp is None:
        errors.append("missing required SLWP-01 entry")
    else:
        if slwp.get("kind") != "CONJECTURE" or slwp.get("lifecycle") != "proposal":
            errors.append("SLWP-01 must remain a proposal conjecture")
        if slwp.get("validation_status_ref") != []:
            errors.append("SLWP-01 must not claim canonical validation status")
        if any("W19" in value for value in slwp.get("source_ids", [])):
            errors.append("SLWP-01 must not masquerade as W19")

    bil = by_id.get("BIL-01")
    if bil is None:
        errors.append("missing required BIL-01 entry")
    else:
        if bil.get("kind") != "FORMAL_RESULT" or bil.get("evidence_tier") != "[A]":
            errors.append("BIL-01 must remain an [A] formal result")
        if bil.get("validation_status_ref") != []:
            errors.append("BIL-01 canonical FV adoption is deferred in this manifest")

    attempt = by_id.get("PA-SLWP-01")
    if attempt is None:
        errors.append("missing required PA-SLWP-01 entry")
    elif "PARTIAL" not in str(attempt.get("outcome", "")):
        errors.append("PA-SLWP-01 must preserve its partial/failed-bridge result")

    tea = by_id.get("TEA-01")
    if tea is None:
        errors.append("missing required TEA-01 entry")
    else:
        if tea.get("kind") != "FORMAL_RESULT" or tea.get("evidence_tier") != "[A]":
            errors.append("TEA-01 must remain an [A] relative formal result")
        if tea.get("validation_status_ref") != []:
            errors.append("TEA-01 must not silently advance canonical claim status")

    answer_set = by_id.get("EAS-10")
    if answer_set is None:
        errors.append("missing required EAS-10 entry")
    else:
        if answer_set.get("kind") != "MODEL" or answer_set.get("lifecycle") != "active":
            errors.append("EAS-10 must remain an active non-validating answer model")
        if answer_set.get("validation_status_ref") != []:
            errors.append("EAS-10 owner adoption must not become canonical validation")

    raw_claim_ids = {
        row_id
        for section in CATALOG_SECTIONS
        for row in claim_status.get(section, [])
        if (row_id := _claim_id(row)) is not None
    }
    if "SLWP-01" in raw_claim_ids or any(value.startswith("W19") for value in raw_claim_ids):
        errors.append("canonical claim status silently adopted SLWP-01/W19")

    bil_path = ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md"
    slwp_path = ROOT / "06_ONTOLOGY/12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md"
    if bil_path.is_file():
        text = bil_path.read_text(encoding="utf-8")
        for token in (
            "There is no function",
            "does not prove strong emergence",
            "D0 is not numeric zero",
            "not multiplication",
        ):
            if token not in text:
                errors.append(f"BIL-01 lost required boundary token: {token!r}")
    if slwp_path.is_file():
        text = slwp_path.read_text(encoding="utf-8")
        for token in (
            "PARTIAL / BRIDGE NOT ESTABLISHED",
            "not `W19`",
            "does not establish `μ₀`",
            "Noninvertibility is not strong emergence",
            "RELATIVE_TYPE_ASYMMETRY_PROVEN",
            "NATURAL_STRONG_EMERGENCE_OPEN",
        ):
            if token not in text:
                errors.append(f"SLWP-01 lost required boundary token: {token!r}")

    declared_digest = str(document.get("inventory_digest", ""))
    if not SHA256.fullmatch(declared_digest):
        errors.append("inventory_digest must be a lowercase SHA-256")
    else:
        actual_digest = inventory_digest(document)
        if actual_digest != declared_digest:
            errors.append(
                f"inventory_digest drifted expected={declared_digest} actual={actual_digest}"
            )

    return errors


def main() -> int:
    errors = check()
    if errors:
        print("CONJECTURE / PROOF-ATTEMPT MANIFEST: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    document = _load_json(MANIFEST_PATH)
    catalog_count = sum(len(document["catalog_snapshot"][key]) for key in CATALOG_SECTIONS)
    print(
        "CONJECTURE / PROOF-ATTEMPT MANIFEST: PASS "
        f"({len(document['entries'])} entries, {len(document['source_manifest'])} sources, "
        f"{catalog_count} claim-status IDs, digest={document['inventory_digest'][:12]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

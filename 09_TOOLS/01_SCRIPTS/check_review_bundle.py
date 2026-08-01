#!/usr/bin/env python3
"""Verify the frozen FPE-REVIEW-01 packet without collapsing custody into contact.

Each versioned manifest hashes the exact packet a future reviewer would receive.
Version 3 replaces the mutable lifecycle registry with an immutable allow-list
projection so that the registry can bind the manifest afterwards without a
self-hash cycle. Passing proves local packet custody only; it never proves that
a reviewer was found, contacted, independent, or persuaded.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "finity_practice"
REGISTRY_REL = Path("03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/GATE_REGISTRY.json")
REGISTRY = ROOT / REGISTRY_REL
VERSIONED_BUNDLE = re.compile(r"^REVIEW_BUNDLE_v(?P<version>[1-9][0-9]*)\.(?P<kind>json|md)$")
BINDING_MODE = "static-review-registry-projection-v1"
SNAPSHOT_SCHEMA = "emergentism/finity-review-registry-snapshot/v1"
BINDING_RECEIPT_SCHEMA = "emergentism/finity-review-bundle-binding-receipt/v1"
REQUIRED_BINDING_KEYS = {
    "mode",
    "snapshot",
    "binding_contract",
    "live_registry",
    "binding_receipt",
    "excludes",
}
REQUIRED_SNAPSHOT_KEYS = {
    "schema",
    "frozen",
    "purpose",
    "binding_contract",
    "projection",
    "projection_sha256",
}
REQUIRED_RECEIPT_KEYS = {
    "schema",
    "kind",
    "date",
    "scope",
    "manifest",
    "snapshot",
    "binding_contract",
    "live_registry",
    "does_not_establish",
}
REMAINING_REVIEW_PREREQUISITES = {
    "complete_review_materials_bundle",
    "conflict_form",
    "reviewer_scope_form",
    "compensation_terms",
    "publication_permission",
    "applicability_determination_recorded",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def bundle_inventory() -> tuple[dict[int, Path], dict[int, Path]]:
    manifests: dict[int, Path] = {}
    documents: dict[int, Path] = {}
    for path in DIR.glob("REVIEW_BUNDLE_v*.*"):
        match = VERSIONED_BUNDLE.fullmatch(path.name)
        if not match:
            continue
        version = int(match.group("version"))
        target = manifests if match.group("kind") == "json" else documents
        target[version] = path
    return manifests, documents


def review_gate_data(registry: Path = REGISTRY) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the one declared FPE-REVIEW-01 row and its containing registry."""

    data = json.loads(registry.read_text(encoding="utf-8"))
    matches = [
        gate
        for gate in data.get("gates", [])
        if isinstance(gate, dict) and gate.get("gate_id") == "FPE-REVIEW-01"
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one FPE-REVIEW-01 gate, found {len(matches)}")
    return data, matches[0]


def review_execution_state(registry: Path = REGISTRY) -> str:
    """Return the one declared FPE-REVIEW-01 execution state."""

    _, gate = review_gate_data(registry)
    execution = gate.get("execution")
    state = execution.get("state") if isinstance(execution, dict) else None
    if not isinstance(state, str) or not state.strip():
        raise ValueError("FPE-REVIEW-01 execution state is missing")
    return state


def review_registry_projection(registry: dict[str, Any]) -> dict[str, Any]:
    """Return the immutable, non-runtime contract a review bundle may carry."""

    matches = [
        gate
        for gate in registry.get("gates", [])
        if isinstance(gate, dict) and gate.get("gate_id") == "FPE-REVIEW-01"
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one FPE-REVIEW-01 gate, found {len(matches)}")
    gate = matches[0]
    execution = gate.get("execution")
    if not isinstance(execution, dict) or not isinstance(execution.get("prerequisites"), dict):
        raise ValueError("FPE-REVIEW-01 execution prerequisites are missing")
    return {
        "registry_schema": registry["schema"],
        "program": {
            "program_id": registry["program_id"],
            "authority": registry["authority"],
            "definition_source": registry["definition_source"],
            "semantic_owner_ids": registry["semantic_owner_ids"],
            "claim_card_path": registry["claim_card_path"],
            "claim_card_ids": registry["claim_card_ids"],
            "docket_ids": registry["docket_ids"],
            "packet_status_vocabulary": registry["packet_status_vocabulary"],
            "contact_status_vocabulary": registry["contact_status_vocabulary"],
            "program_boundary": registry["program_boundary"],
            "external_custody_contract": registry["external_custody_contract"],
        },
        "review_gate": {
            "gate_id": gate["gate_id"],
            "title": gate["title"],
            "packet": gate["packet"],
            "packet_sha256": gate["packet_sha256"],
            "claim_card_ids": gate["claim_card_ids"],
            "docket_ids": gate["docket_ids"],
            "depends_on": gate["depends_on"],
            "moves_if_passed": gate["moves_if_passed"],
            "does_not_move": gate["does_not_move"],
            "kill_or_revise": gate["kill_or_revise"],
            "prerequisite_names": sorted(execution["prerequisites"]),
            "ready_when": execution["ready_when"],
        },
    }


def document_status_errors(document_text: str, execution_state: str) -> list[str]:
    """Keep the human packet status consistent with the machine gate state."""

    normalized = " ".join(document_text.split())
    lowered = normalized.lower()
    errors: list[str] = []
    for needed in ("not sent", "review received", "does not work here"):
        if needed not in lowered:
            errors.append(f"packet no longer states {needed!r}")
    if execution_state == "blocked":
        if "contact blocked" not in lowered:
            errors.append("blocked review gate is not labeled CONTACT BLOCKED")
        positive_readiness = (
            r"(?<!not\s)\bready[- ]to[- ]send\b",
            r"(?<!not\s)\bcontact[- ]ready\b",
            r"\b(?:may|can)\s+now\s+be\s+sent\b",
        )
        if any(re.search(pattern, lowered) for pattern in positive_readiness):
            errors.append("blocked review gate still asserts contact readiness")
    return errors


def _path_string(path: Path) -> str:
    return path.as_posix()


def contained_manifest_file(relative: object) -> tuple[Path | None, str | None]:
    """Resolve one manifest entry only if it is a safe, regular corpus file."""

    if not isinstance(relative, str) or not relative:
        return None, "manifest file path must be a non-empty string"
    raw = Path(relative)
    if (
        raw.is_absolute()
        or ".." in raw.parts
        or raw.as_posix() != relative
        or "\\" in relative
        or "\x00" in relative
    ):
        return None, f"{relative!r}: manifest file path must be safe and repository-relative"
    candidate = ROOT / raw
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, ValueError):
        return None, f"{relative}: listed in the bundle and MISSING from the tree"
    if not resolved.is_relative_to(ROOT.resolve()):
        return None, f"{relative}: manifest file path resolves outside the repository"
    if candidate.is_symlink():
        return None, f"{relative}: manifest file path must not be a symlink"
    if not resolved.is_file():
        return None, f"{relative}: listed in the bundle but is not a regular file"
    return resolved, None


def _sha_record_errors(record: Any, path: Path, label: str) -> list[str]:
    if not isinstance(record, str) or not re.fullmatch(r"[0-9a-f]{64}", record):
        return [f"{label} must carry a lowercase SHA-256"]
    if not path.is_file():
        return [f"{label} file is missing"]
    return [] if record == sha256(path) else [f"{label} digest drifted"]


def acyclic_binding_errors(
    manifest_path: Path,
    manifest: dict[str, Any],
    registry: dict[str, Any],
    gate: dict[str, Any],
    version: int,
) -> list[str]:
    """Check the v3+ static-projection graph and current fail-closed state."""

    errors: list[str] = []
    files = manifest.get("files")
    if not isinstance(files, dict):
        return ["manifest files must be an object before acyclic binding can be checked"]

    manifest_rel = _path_string(manifest_path.relative_to(ROOT))
    expected_snapshot = (
        "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
        f"REVIEW_REGISTRY_SNAPSHOT_v{version}.json"
    )
    expected_receipt = (
        "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
        f"REVIEW_BUNDLE_v{version}_BINDING_RECEIPT.json"
    )
    binding = manifest.get("registry_binding")
    if not isinstance(binding, dict) or set(binding) != REQUIRED_BINDING_KEYS:
        errors.append("manifest registry_binding must carry the exact acyclic binding keys")
        return errors
    if binding.get("mode") != BINDING_MODE:
        errors.append("manifest registry_binding uses an unknown mode")
    if binding.get("snapshot") != expected_snapshot:
        errors.append("manifest registry_binding does not name its matching snapshot")
    if binding.get("live_registry") != REGISTRY_REL.as_posix():
        errors.append("manifest registry_binding does not name the live registry")
    if binding.get("binding_receipt") != expected_receipt:
        errors.append("manifest registry_binding does not name its matching binding receipt")
    contract_rel = binding.get("binding_contract")
    if not isinstance(contract_rel, str) or not contract_rel:
        errors.append("manifest registry_binding has no binding-contract path")
    excluded = binding.get("excludes")
    expected_exclusions = {REGISTRY_REL.as_posix(), manifest_rel, expected_receipt}
    if not isinstance(excluded, list) or set(excluded) != expected_exclusions:
        errors.append("manifest registry_binding must exclude raw registry, self, and receipt")

    forbidden = expected_exclusions.intersection(files)
    if forbidden:
        errors.append("manifest must not hash mutable/self-binding files: " + ", ".join(sorted(forbidden)))
    if expected_snapshot not in files:
        errors.append("manifest does not hash its static registry snapshot")
    if isinstance(contract_rel, str) and contract_rel not in files:
        errors.append("manifest does not hash its binding contract")

    snapshot_path = ROOT / expected_snapshot
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"static registry snapshot is unreadable: {exc}")
        snapshot = None
    if isinstance(snapshot, dict):
        if set(snapshot) != REQUIRED_SNAPSHOT_KEYS:
            errors.append("static registry snapshot has unexpected keys")
        if snapshot.get("schema") != SNAPSHOT_SCHEMA:
            errors.append("static registry snapshot uses an unknown schema")
        if snapshot.get("binding_contract") != contract_rel:
            errors.append("static registry snapshot names a different binding contract")
        projection = review_registry_projection(registry)
        if snapshot.get("projection") != projection:
            errors.append("static registry snapshot no longer equals the allow-list projection")
        want_projection_digest = hashlib.sha256(canonical_json(projection)).hexdigest()
        if snapshot.get("projection_sha256") != want_projection_digest:
            errors.append("static registry snapshot projection digest drifted")

    execution = gate.get("execution")
    prerequisites = execution.get("prerequisites") if isinstance(execution, dict) else None
    if not isinstance(prerequisites, dict):
        return errors + ["review gate prerequisites are unreadable"]
    record = prerequisites.get("bundle_manifest")
    if not isinstance(record, dict):
        errors.append("review gate has no bundle_manifest evidence record")
        return errors
    if record.get("state") != "satisfied":
        errors.append("acyclic v3+ bundle_manifest must be satisfied")
        return errors
    if record.get("artifact") != manifest_rel:
        errors.append("bundle_manifest does not bind the current manifest")
    errors.extend(_sha_record_errors(record.get("sha256"), manifest_path, "bundle_manifest artifact"))
    receipt_rel = record.get("receipt")
    if receipt_rel != expected_receipt:
        errors.append("bundle_manifest does not bind the matching local receipt")
    receipt_path = ROOT / expected_receipt
    errors.extend(_sha_record_errors(record.get("receipt_sha256"), receipt_path, "bundle_manifest receipt"))

    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"binding receipt is unreadable: {exc}")
        receipt = None
    if isinstance(receipt, dict):
        if set(receipt) != REQUIRED_RECEIPT_KEYS:
            errors.append("binding receipt has unexpected keys")
        if receipt.get("schema") != BINDING_RECEIPT_SCHEMA:
            errors.append("binding receipt uses an unknown schema")
        if receipt.get("kind") != "internal-acyclic-manifest-binding":
            errors.append("binding receipt records the wrong event kind")
        for label, expected_path in (
            ("manifest", manifest_rel),
            ("snapshot", expected_snapshot),
            ("binding_contract", contract_rel),
        ):
            item = receipt.get(label)
            if not isinstance(item, dict) or item.get("path") != expected_path:
                errors.append(f"binding receipt does not bind {label}")
                continue
            if isinstance(expected_path, str):
                errors.extend(
                    _sha_record_errors(
                        item.get("sha256"), ROOT / expected_path, f"binding receipt {label}"
                    )
                )
        live_registry = receipt.get("live_registry")
        if live_registry != {
            "path": REGISTRY_REL.as_posix(),
            "excluded_from_manifest": True,
        }:
            errors.append("binding receipt does not state the live-registry exclusion")

    if execution.get("state") != "blocked":
        errors.append("acyclic binding must not make review execution ready")
    for name in REMAINING_REVIEW_PREREQUISITES:
        current = prerequisites.get(name)
        if not isinstance(current, dict) or current.get("state") != "missing":
            errors.append(f"{name} must remain missing after acyclic binding")
            continue
        if any(current.get(key) is not None for key in ("artifact", "sha256", "receipt", "receipt_sha256")):
            errors.append(f"{name} is missing but carries evidence")
    return errors


def main() -> int:
    manifests, documents = bundle_inventory()
    versions = sorted(set(manifests) | set(documents))
    if not versions:
        print("REVIEW BUNDLE: PASS (no bundle document and no manifest — nothing frozen)")
        print("  scope: this is the genuinely-empty state. It does NOT mean a bundle was")
        print("  checked; it means none exists.")
        return 0

    errors: list[str] = []
    if versions != list(range(1, versions[-1] + 1)):
        errors.append(f"bundle version history is not contiguous: {versions}")
    for version in versions:
        if version not in manifests:
            errors.append(f"REVIEW_BUNDLE_v{version}.md has no matching JSON manifest")
        if version not in documents:
            errors.append(f"REVIEW_BUNDLE_v{version}.json has no matching Markdown document")
    if errors:
        print("REVIEW BUNDLE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    latest = versions[-1]
    manifest_path = manifests[latest]
    document = documents[latest]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"REVIEW BUNDLE: FAIL\n- manifest unreadable: {exc}")
        return 1

    if manifest.get("bundleVersion") != f"v{latest}":
        errors.append(
            f"{manifest_path.name}: bundleVersion must be v{latest}, got {manifest.get('bundleVersion')!r}"
        )
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        errors.append("the manifest lists no files")
        files = {}
    for rel, want in files.items():
        if not isinstance(rel, str) or not isinstance(want, str):
            errors.append("manifest file entries must map string paths to SHA-256 values")
            continue
        path, path_error = contained_manifest_file(rel)
        if path_error:
            errors.append(path_error)
            continue
        got = "sha256:" + sha256(path)
        if got != want:
            errors.append(
                f"{rel}: hash moved.\n    frozen {want}\n    now    {got}\n"
                f"    This is a material amendment. Bump the bundle to v{latest + 1} and treat any "
                "existing review as not covering it."
            )

    try:
        registry, gate = review_gate_data()
        execution_state = review_execution_state()
        if latest >= 3:
            errors.extend(acyclic_binding_errors(manifest_path, manifest, registry, gate, latest))
    except (json.JSONDecodeError, OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"review gate registry unreadable or ambiguous: {exc}")
        execution_state = "unknown"

    doc = document.read_text(encoding="utf-8")
    for error in document_status_errors(doc, execution_state):
        errors.append(f"{document.name}: {error}")

    if errors:
        print("REVIEW BUNDLE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    binding = "acyclic-binding=verified; " if latest >= 3 else ""
    print(
        f"REVIEW BUNDLE: PASS ({len(files)} files, {len(versions)} versions in custody; "
        f"{binding}all hashes match bundle {manifest.get('bundleVersion', '?')} "
        f"frozen {manifest.get('frozen', '?')}; execution={execution_state})"
    )
    print("  scope: proves the packet has not drifted. It does NOT mean a reviewer was")
    print("  found, contacted, or replied.")
    print("  known limit: a technical bundle binding cannot establish a reviewer, owner")
    print("  decision, ethics determination, permission, compensation, or external verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

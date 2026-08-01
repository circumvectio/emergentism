#!/usr/bin/env python3
"""Verify the frozen FPE-REVIEW-01 packet without collapsing custody into contact.

The current versioned manifest hashes the exact packet a future reviewer would
receive. Earlier manifest artifacts are retained with their historical source
drift reported rather than silently replayed against mutable current paths.
Version 3 replaces the mutable lifecycle registry with an immutable allow-list
projection so that the registry can bind the manifest afterwards without a
self-hash cycle. Passing proves local packet custody only; it never proves that
a reviewer was found, contacted, independent, or persuaded.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "finity_practice"
REGISTRY_REL = Path("03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/GATE_REGISTRY.json")
REGISTRY = ROOT / REGISTRY_REL
VERSIONED_BUNDLE = re.compile(r"^REVIEW_BUNDLE_v(?P<version>[1-9][0-9]*)\.(?P<kind>json|md)$")
BINDING_MODE_V1 = "static-review-registry-projection-v1"
BINDING_MODE_V2 = "static-review-registry-projection-v2"
SNAPSHOT_SCHEMA_V1 = "emergentism/finity-review-registry-snapshot/v1"
SNAPSHOT_SCHEMA_V2 = "emergentism/finity-review-registry-snapshot/v2"
BINDING_RECEIPT_SCHEMA = "emergentism/finity-review-bundle-binding-receipt/v1"
BINDING_PROFILES = {
    BINDING_MODE_V1: SNAPSHOT_SCHEMA_V1,
    BINDING_MODE_V2: SNAPSHOT_SCHEMA_V2,
}
BINDING_CONTRACTS_BY_VERSION = {
    3: "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_BINDING_CONTRACT_v1.md",
    4: "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_BINDING_CONTRACT_v2.md",
}
PROVENANCE_CONTRACT_SCHEMA = "emergentism/finity-review-prerequisite-provenance/v1"
REVIEW_PROVENANCE_ACCEPTANCE = "v4-internal-bundle-custody-only"
HISTORICAL_ARTIFACT_CUSTODY_SCHEMA = (
    "emergentism/finity-review-historical-artifact-custody/v1"
)
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
REQUIRED_PROVENANCE_CONTRACT_KEYS = {"schema", "acceptance", "owner_authority", "assignments"}
REQUIRED_OWNER_AUTHORITY_KEYS = {"docket_id", "state_at_freeze", "selection"}
REQUIRED_PROVENANCE_ASSIGNMENT_KEYS = {
    "kind",
    "requires_owner_authority",
    "requires_external_state",
}
OWNER_AUTHORITY_STATES = {"unset"}
REVIEW_PROVENANCE_ASSIGNMENTS = {
    "bundle_manifest": {
        "kind": "technical_binding",
        "requires_owner_authority": False,
        "requires_external_state": None,
    },
    "complete_review_materials_bundle": {
        "kind": "technical_materials_bundle",
        "requires_owner_authority": True,
        "requires_external_state": None,
    },
    "conflict_form": {
        "kind": "external_declaration",
        "requires_owner_authority": True,
        "requires_external_state": "reviewers_engaged",
    },
    "reviewer_scope_form": {
        "kind": "external_declaration",
        "requires_owner_authority": True,
        "requires_external_state": "reviewers_engaged",
    },
    "compensation_terms": {
        "kind": "owner_attestation",
        "requires_owner_authority": True,
        "requires_external_state": None,
    },
    "publication_permission": {
        "kind": "external_declaration",
        "requires_owner_authority": True,
        "requires_external_state": "reviewers_engaged",
    },
    "applicability_determination_recorded": {
        "kind": "applicability_determination",
        "requires_owner_authority": True,
        "requires_external_state": "ethics_determination_obtained",
    },
}
REMAINING_REVIEW_PREREQUISITES = {
    "complete_review_materials_bundle",
    "conflict_form",
    "reviewer_scope_form",
    "compensation_terms",
    "publication_permission",
    "applicability_determination_recorded",
}

# These are immutable packet artifacts, not claims that the historical source
# paths still replay against the current tree. The v4 packet copies this exact
# contract, binds the retained bytes, and checks their Git content commits when
# those objects are available locally. A version-created commit and a later
# corrected artifact-content commit are deliberately separate facts.
HISTORICAL_BUNDLE_CUSTODY = {
    1: {
        "version_created_commit": "92c24841532f3f027c0afb21cdedfedd5fd73729",
        "artifacts": {
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v1.json": {
                "sha256": "96e17101b9c27ac2b343fd6848289aacef9459b40f997132d4f763ea243e3782",
                "content_commit": "92c24841532f3f027c0afb21cdedfedd5fd73729",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v1.md": {
                "sha256": "dcf67bc4d540241c778b83916db88413fa361b81fc7bc0be1285397b7b0bd607",
                "content_commit": "92c24841532f3f027c0afb21cdedfedd5fd73729",
            },
        },
    },
    2: {
        "version_created_commit": "b7e0d00dd47d1d784b6c563a4246dc2c3e1a98f8",
        "artifacts": {
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v2.json": {
                "sha256": "68b70aaf105156be42cfc09f56c7ce156e4908e441be20a4d1a47150fd291c96",
                "content_commit": "b7e0d00dd47d1d784b6c563a4246dc2c3e1a98f8",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v2.md": {
                "sha256": "04968407f1103af8d8e75e93005ed10028a4ab259f0e38d5f1e6f5c2187a79c2",
                "content_commit": "eeb7b6ac0ae294a4e65a59bfdd6dfbb10367108e",
            },
        },
    },
    3: {
        "version_created_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
        "artifacts": {
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v3.json": {
                "sha256": "31e79197496597707ccf8fc75d9a03664bd85ec9038ae1f003098caca66d638a",
                "content_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v3.md": {
                "sha256": "ce66480aa0d22e9b71f9f7cbf9b8fb54ff5b6538a7e73775ac60af0d201c27e2",
                "content_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_REGISTRY_SNAPSHOT_v3.json": {
                "sha256": "a051b82c8d0d26a4a87472d2a5416b36046c7c393fad14d6e1326cdab5211e74",
                "content_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v3_BINDING_RECEIPT.json": {
                "sha256": "da56b7661efa94976df25af6d65e76481d0df41856b3eb920181ed5bebc3f33b",
                "content_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
            },
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_BINDING_CONTRACT_v1.md": {
                "sha256": "26f331d07a15eb9fe624c226b6c7688549f224c3718420b2e147a2f1691d3c5b",
                "content_commit": "ea2c94e52809e8cf251ed52242afff8f5055c811",
            },
        },
    },
}

REQUIRED_CURRENT_PACKET_FILES_BY_VERSION = {
    4: frozenset(
        {
            "01_TELEOLOGY/04_THE_LIVED_COMPASS.md",
            "00_META/claim_cards/finity_practice.yaml",
            "00_META/ADEQUACY_DOCKETS.yaml",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_REGISTRY_SNAPSHOT_v4.json",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_BINDING_CONTRACT_v2.md",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v4.md",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/README.md",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/01_FRESH_READER_COMPREHENSION.md",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/02_INDEPENDENT_REVIEW.md",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/03_CONTROLLED_FINITY_COMPARISON.md",
            "00_META/00_IMMUNE_PROTOCOL.md",
            "09_TOOLS/01_SCRIPTS/claim_policy.py",
        }
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


class DuplicateJsonKeyError(ValueError):
    """Reject ambiguous JSON before it can become custody evidence."""


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    """Load one unambiguous JSON object from an already-contained file."""

    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_object
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise ValueError(f"{label} is not unambiguous structured JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


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

    try:
        relative = registry.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise ValueError("review gate registry lies outside the corpus") from exc
    safe_registry, path_error = contained_manifest_file(relative)
    if path_error or safe_registry is None:
        raise ValueError(path_error or "review gate registry is not a safe regular file")
    data = load_json_object(safe_registry, "review gate registry")
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


def review_registry_projection(
    registry: dict[str, Any], mode: str = BINDING_MODE_V2
) -> dict[str, Any]:
    """Return the immutable, non-runtime contract a review bundle may carry."""

    if mode not in BINDING_PROFILES:
        raise ValueError(f"unknown review-registry projection mode: {mode}")

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
    projection = {
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
    if mode == BINDING_MODE_V2:
        contract = execution.get("provenance_contract")
        if not isinstance(contract, dict):
            raise ValueError("FPE-REVIEW-01 provenance contract is missing")
        projection["review_gate"]["provenance_contract"] = contract
    return projection


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


def historical_artifact_custody_contract() -> dict[str, Any]:
    """Return the exact v4-retained historical-artifact contract."""

    return {
        "schema": HISTORICAL_ARTIFACT_CUSTODY_SCHEMA,
        "versions": {
            f"v{version}": {
                "version_created_commit": custody["version_created_commit"],
                "artifacts": {
                    relative: {
                        "sha256": artifact["sha256"],
                        "content_commit": artifact["content_commit"],
                    }
                    for relative, artifact in custody["artifacts"].items()
                },
            }
            for version, custody in HISTORICAL_BUNDLE_CUSTODY.items()
        },
    }


def required_manifest_files(version: int) -> frozenset[str] | None:
    """Return the exact immutable inventory for a version with a fixed contract."""

    current = REQUIRED_CURRENT_PACKET_FILES_BY_VERSION.get(version)
    if current is None:
        return None
    historical = {
        relative
        for custody in HISTORICAL_BUNDLE_CUSTODY.values()
        for relative in custody["artifacts"]
    }
    return current | frozenset(historical)


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
    cursor = ROOT
    for component in raw.parts:
        cursor /= component
        if cursor.is_symlink():
            return None, f"{relative}: manifest file path must not traverse a symlink"
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, ValueError):
        return None, f"{relative}: listed in the bundle and MISSING from the tree"
    if not resolved.is_relative_to(ROOT.resolve()):
        return None, f"{relative}: manifest file path resolves outside the repository"
    if not resolved.is_file():
        return None, f"{relative}: listed in the bundle but is not a regular file"
    return resolved, None


def _sha_record_errors(record: Any, path: Path, label: str) -> list[str]:
    if not isinstance(record, str) or not re.fullmatch(r"[0-9a-f]{64}", record):
        return [f"{label} must carry a lowercase SHA-256"]
    if not path.is_file():
        return [f"{label} file is missing"]
    return [] if record == sha256(path) else [f"{label} digest drifted"]


def _git_commit_unavailable(commit: str, label: str) -> str | None:
    """Describe a missing local Git object without invalidating retained bytes."""

    try:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError as exc:
        return f"{label} Git history is not locally available: {exc.__class__.__name__}"
    if result.returncode:
        return f"{label} Git commit is not locally available"
    return None


def _git_blob_digest(
    commit: str, relative: str, label: str
) -> tuple[str | None, str | None, str | None]:
    """Read a historical blob, separating unavailable history from a mismatch."""

    unavailable = _git_commit_unavailable(commit, label)
    if unavailable:
        return None, None, unavailable
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{relative}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError as exc:
        return None, None, f"{label} Git history cannot be read: {exc.__class__.__name__}"
    if result.returncode:
        return None, f"{label} Git artifact is absent at its declared content commit", None
    return hashlib.sha256(result.stdout).hexdigest(), None, None


def historical_custody_errors(
    latest: int,
    current_files: dict[str, Any],
    manifest: dict[str, Any] | None = None,
    historical_unavailable: list[str] | None = None,
) -> list[str]:
    """Require retained bytes; report missing optional Git reconstruction separately."""

    if latest < 4:
        return []
    errors: list[str] = []
    expected_versions = set(range(1, latest))
    if set(HISTORICAL_BUNDLE_CUSTODY) != expected_versions:
        errors.append("historical artifact custody map must cover every earlier bundle version")
        return errors
    if manifest is None or manifest.get("historical_artifact_custody") != historical_artifact_custody_contract():
        errors.append("current bundle must freeze the exact historical-artifact custody contract")
    unavailable_commits: set[str] = set()

    def report_unavailable(commit: str, detail: str) -> None:
        if historical_unavailable is not None and commit not in unavailable_commits:
            historical_unavailable.append(detail)
            unavailable_commits.add(commit)

    for version, custody in HISTORICAL_BUNDLE_CUSTODY.items():
        commit = custody.get("version_created_commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append(f"v{version} historical custody has an invalid version-created commit")
        else:
            creation_unavailable = _git_commit_unavailable(commit, f"v{version} version-created")
            if creation_unavailable:
                report_unavailable(commit, creation_unavailable)
        artifacts = custody.get("artifacts")
        if not isinstance(artifacts, dict) or not artifacts:
            errors.append(f"v{version} historical custody has no artifact map")
            continue
        version_manifest = (
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
            f"REVIEW_BUNDLE_v{version}.json"
        )
        for relative, artifact in artifacts.items():
            if not isinstance(artifact, dict):
                errors.append(f"v{version} historical custody has an unreadable artifact record")
                continue
            digest = artifact.get("sha256")
            content_commit = artifact.get("content_commit")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"v{version} historical custody has an invalid artifact digest")
                continue
            if not isinstance(content_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", content_commit):
                errors.append(f"v{version} historical custody has an invalid artifact content commit")
                continue
            if current_files.get(relative) != f"sha256:{digest}":
                errors.append(f"current bundle does not hash-lock retained v{version} artifact {relative}")
            path, path_error = contained_manifest_file(relative)
            if path_error or path is None:
                errors.append(path_error or f"retained v{version} artifact path is invalid")
                continue
            errors.extend(_sha_record_errors(digest, path, f"retained v{version} artifact"))
            historical_digest, historical_error, history_unavailable = _git_blob_digest(
                content_commit,
                relative,
                f"retained v{version} artifact",
            )
            if historical_error:
                errors.append(historical_error)
            elif history_unavailable:
                report_unavailable(content_commit, history_unavailable)
            elif historical_digest != digest:
                errors.append(f"retained v{version} artifact content commit does not match its frozen digest")
            if relative == version_manifest and commit != content_commit:
                errors.append(f"v{version} version-created commit must anchor its JSON manifest")
    return errors


def historical_source_drift(
    manifests: dict[int, Path], latest: int
) -> dict[int, list[str]]:
    """Report, but never replay as current, source drift of retained manifests."""

    drift: dict[int, list[str]] = {}
    for version in range(1, latest):
        manifest_path = manifests.get(version)
        if manifest_path is None:
            continue
        try:
            relative = manifest_path.relative_to(ROOT).as_posix()
        except ValueError:
            drift[version] = ["manifest-outside-corpus"]
            continue
        safe_manifest, path_error = contained_manifest_file(relative)
        if path_error or safe_manifest is None:
            drift[version] = ["manifest-not-safe"]
            continue
        try:
            manifest = load_json_object(safe_manifest, f"historical v{version} manifest")
        except ValueError:
            drift[version] = ["manifest-unreadable"]
            continue
        files = manifest.get("files")
        if not isinstance(files, dict):
            drift[version] = ["manifest-files-unreadable"]
            continue
        moved: list[str] = []
        for relative, digest in files.items():
            path, path_error = contained_manifest_file(relative)
            if path_error or path is None or not isinstance(digest, str):
                moved.append(str(relative))
            elif f"sha256:{sha256(path)}" != digest:
                moved.append(relative)
        drift[version] = sorted(moved)
    return drift


def _owner_authority_errors(authority: Any) -> list[str]:
    """Keep v4 strictly pre-authority; selection needs a later schema."""

    if not isinstance(authority, dict) or set(authority) != REQUIRED_OWNER_AUTHORITY_KEYS:
        return ["review provenance owner_authority has unexpected keys"]
    if authority.get("docket_id") != "D-OWNER-03":
        return ["review provenance must bind D-OWNER-03"]
    if authority.get("state_at_freeze") not in OWNER_AUTHORITY_STATES:
        return [
            "v4 accepts only unset owner authority; a selected route requires a "
            "new reviewed schema and an external verification boundary"
        ]
    return [] if authority.get("selection") is None else [
        "unset owner authority must carry no selection evidence"
    ]


def review_provenance_errors(registry: dict[str, Any], gate: dict[str, Any]) -> list[str]:
    """Fail closed: v4 admits internal bundle custody, not human evidence."""

    errors: list[str] = []
    execution = gate.get("execution")
    if not isinstance(execution, dict):
        return ["review execution is unreadable for provenance checking"]
    prerequisites = execution.get("prerequisites")
    contract = execution.get("provenance_contract")
    if not isinstance(prerequisites, dict):
        return ["review prerequisites are unreadable for provenance checking"]
    if not isinstance(contract, dict) or set(contract) != REQUIRED_PROVENANCE_CONTRACT_KEYS:
        return ["review provenance contract has unexpected keys"]
    if contract.get("schema") != PROVENANCE_CONTRACT_SCHEMA:
        errors.append("review provenance contract uses an unknown schema")
    if contract.get("acceptance") != REVIEW_PROVENANCE_ACCEPTANCE:
        errors.append("review provenance contract has an unsafe acceptance mode")
    assignments = contract.get("assignments")
    if not isinstance(assignments, dict) or set(assignments) != set(prerequisites):
        errors.append("review provenance assignments must cover exactly the review prerequisites")
    else:
        assignment_drift = False
        for name, assignment in assignments.items():
            if not isinstance(assignment, dict) or set(assignment) != REQUIRED_PROVENANCE_ASSIGNMENT_KEYS:
                errors.append(f"{name} provenance assignment has unexpected keys")
                assignment_drift = True
                continue
            owner_required = assignment.get("requires_owner_authority")
            external_required = assignment.get("requires_external_state")
            if type(owner_required) is not bool:
                errors.append(f"{name} provenance requires_owner_authority must be a JSON boolean")
            if external_required is not None and type(external_required) is not str:
                errors.append(f"{name} provenance requires_external_state must be a string or null")
            expected_assignment = REVIEW_PROVENANCE_ASSIGNMENTS[name]
            if assignment != expected_assignment:
                errors.append(f"{name} provenance assignment drifted from the fail-closed contract")
                assignment_drift = True
        if assignment_drift:
            errors.append("review provenance assignments drifted from the fail-closed contract")

    authority = contract.get("owner_authority")
    errors.extend(_owner_authority_errors(authority))
    if gate.get("packet_status") != "typed":
        errors.append("unset owner authority must keep the review packet typed")
    if gate.get("contact_status") != "deferred":
        errors.append("unset owner authority must keep review contact deferred")
    if execution.get("state") != "blocked":
        errors.append("unset owner authority must keep review execution blocked")
    external_state = registry.get("external_state")
    if not isinstance(external_state, dict) or any(
        not isinstance(record, dict) or record.get("state") != "absent"
        for record in external_state.values()
    ):
        errors.append("v4 accepts no external-state evidence in its custody-only registry")
    for name in REMAINING_REVIEW_PREREQUISITES:
        record = prerequisites.get(name)
        if not isinstance(record, dict) or record.get("state") != "missing":
            errors.append(f"unset owner authority requires {name} to remain missing")
            continue
        if any(record.get(key) is not None for key in ("artifact", "sha256", "receipt", "receipt_sha256")):
            errors.append(f"unset owner authority requires {name} to carry no evidence")
    return errors


def acyclic_binding_errors(
    manifest_path: Path,
    manifest: dict[str, Any],
    registry: dict[str, Any],
    gate: dict[str, Any],
    version: int,
    historical_unavailable: list[str] | None = None,
) -> list[str]:
    """Check the v3+ static-projection graph and current fail-closed state."""

    if version not in BINDING_CONTRACTS_BY_VERSION:
        return [
            f"bundle v{version} is unsupported: register a successor binding contract "
            "and independently reviewed verification boundary before checking it"
        ]
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
    mode = binding.get("mode")
    snapshot_schema = BINDING_PROFILES.get(mode)
    if snapshot_schema is None:
        errors.append("manifest registry_binding uses an unknown mode")
    expected_mode = BINDING_MODE_V1 if version == 3 else BINDING_MODE_V2
    if mode != expected_mode:
        errors.append(
            f"bundle v{version} must use {expected_mode}, not {mode!r}"
        )
    if binding.get("snapshot") != expected_snapshot:
        errors.append("manifest registry_binding does not name its matching snapshot")
    if binding.get("live_registry") != REGISTRY_REL.as_posix():
        errors.append("manifest registry_binding does not name the live registry")
    if binding.get("binding_receipt") != expected_receipt:
        errors.append("manifest registry_binding does not name its matching binding receipt")
    contract_rel = binding.get("binding_contract")
    if not isinstance(contract_rel, str) or not contract_rel:
        errors.append("manifest registry_binding has no binding-contract path")
    expected_contract = BINDING_CONTRACTS_BY_VERSION.get(version)
    if expected_contract is not None and contract_rel != expected_contract:
        errors.append(
            f"bundle v{version} must bind {expected_contract}, not {contract_rel!r}"
        )
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
    expected_predecessor = f"REVIEW_BUNDLE_v{version - 1}.json"
    if manifest.get("supersedes") != expected_predecessor:
        errors.append("manifest does not name its immediate predecessor")
    required_files = required_manifest_files(version)
    if required_files is not None:
        actual_files = set(files)
        missing = required_files - actual_files
        unexpected = actual_files - required_files
        if missing:
            errors.append(
                "bundle v4 must preserve its exact current packet inventory; missing: "
                + ", ".join(sorted(missing))
            )
        if unexpected:
            errors.append(
                "bundle v4 must preserve its exact current packet inventory; unexpected: "
                + ", ".join(sorted(repr(path) for path in unexpected))
            )
    errors.extend(historical_custody_errors(version, files, manifest, historical_unavailable))

    snapshot_path, snapshot_path_error = contained_manifest_file(expected_snapshot)
    if snapshot_path_error or snapshot_path is None:
        errors.append(snapshot_path_error or "static registry snapshot is not a safe regular file")
        snapshot = None
    else:
        try:
            snapshot = load_json_object(snapshot_path, "static registry snapshot")
        except ValueError as exc:
            errors.append(str(exc))
            snapshot = None
    if isinstance(snapshot, dict):
        if set(snapshot) != REQUIRED_SNAPSHOT_KEYS:
            errors.append("static registry snapshot has unexpected keys")
        if snapshot.get("schema") != snapshot_schema:
            errors.append("static registry snapshot uses an unknown schema")
        if snapshot.get("binding_contract") != contract_rel:
            errors.append("static registry snapshot names a different binding contract")
        if snapshot_schema is not None:
            projection = review_registry_projection(registry, mode)
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
    receipt_path, receipt_path_error = contained_manifest_file(expected_receipt)
    if receipt_path_error or receipt_path is None:
        errors.append(receipt_path_error or "binding receipt is not a safe regular file")
        receipt = None
    else:
        errors.extend(_sha_record_errors(record.get("receipt_sha256"), receipt_path, "bundle_manifest receipt"))
        try:
            receipt = load_json_object(receipt_path, "binding receipt")
        except ValueError as exc:
            errors.append(str(exc))
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
                expected_file, expected_file_error = contained_manifest_file(expected_path)
                if expected_file_error or expected_file is None:
                    errors.append(expected_file_error or f"binding receipt {label} path is invalid")
                else:
                    errors.extend(
                        _sha_record_errors(
                            item.get("sha256"), expected_file, f"binding receipt {label}"
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
    if mode == BINDING_MODE_V1:
        for name in REMAINING_REVIEW_PREREQUISITES:
            current = prerequisites.get(name)
            if not isinstance(current, dict) or current.get("state") != "missing":
                errors.append(f"{name} must remain missing after acyclic binding")
                continue
            if any(current.get(key) is not None for key in ("artifact", "sha256", "receipt", "receipt_sha256")):
                errors.append(f"{name} is missing but carries evidence")
    if mode == BINDING_MODE_V2:
        errors.extend(review_provenance_errors(registry, gate))
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
    historical_unavailable: list[str] = []
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

    for version in versions:
        manifest_candidate = manifests[version]
        document_candidate = documents[version]
        try:
            manifest_relative = manifest_candidate.relative_to(ROOT).as_posix()
            document_relative = document_candidate.relative_to(ROOT).as_posix()
        except ValueError:
            errors.append(f"bundle v{version} entrypoint lies outside the corpus")
            continue
        safe_manifest, manifest_path_error = contained_manifest_file(manifest_relative)
        safe_document, document_path_error = contained_manifest_file(document_relative)
        if manifest_path_error or safe_manifest is None:
            errors.append(manifest_path_error or f"bundle v{version} manifest is not a safe regular file")
            continue
        if document_path_error or safe_document is None:
            errors.append(document_path_error or f"bundle v{version} document is not a safe regular file")
            continue
        manifests[version] = safe_manifest
        documents[version] = safe_document
        try:
            historical_manifest = load_json_object(safe_manifest, f"bundle v{version} manifest")
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if historical_manifest.get("bundleVersion") != f"v{version}":
            errors.append(f"bundle v{version} manifest names the wrong bundleVersion")
        expected_predecessor = None if version == 1 else f"REVIEW_BUNDLE_v{version - 1}.json"
        if historical_manifest.get("supersedes") != expected_predecessor:
            errors.append(f"bundle v{version} does not name its immediate predecessor")
    if errors:
        print("REVIEW BUNDLE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    latest = versions[-1]
    manifest_path = manifests[latest]
    document = documents[latest]
    try:
        manifest = load_json_object(manifest_path, f"bundle v{latest} manifest")
    except ValueError as exc:
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

    historical_drift = historical_source_drift(manifests, latest)
    try:
        registry, gate = review_gate_data()
        execution_state = review_execution_state()
        if latest >= 3:
            errors.extend(
                acyclic_binding_errors(
                    manifest_path,
                    manifest,
                    registry,
                    gate,
                    latest,
                    historical_unavailable,
                )
            )
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
        f"REVIEW BUNDLE: PASS (current {manifest.get('bundleVersion', '?')}: {len(files)} files hash-verified; "
        f"{binding}current hashes match bundle {manifest.get('bundleVersion', '?')} "
        f"frozen {manifest.get('frozen', '?')}; execution={execution_state})"
    )
    if historical_drift:
        drift_summary = ", ".join(
            f"v{version}={len(paths)}" for version, paths in sorted(historical_drift.items())
        )
        commits = ", ".join(
            f"v{version}={custody['version_created_commit'][:12]}"
            for version, custody in sorted(HISTORICAL_BUNDLE_CUSTODY.items())
        )
        print(
            "  historical context: v1-v3 are retained manifest artifacts; their "
            "per-artifact Git content commits are hash-checked when locally available, "
            "while their source lists are not replayed against mutable current paths "
            f"({drift_summary} drifted; initial versions {commits})."
        )
    if historical_unavailable:
        print(
            "  historical reconstruction: Git objects were unavailable for "
            f"{len(historical_unavailable)} declared commit(s); retained current bytes remain "
            "hash-verified, but Git-origin reconstruction was not replayed."
        )
    print("  scope: proves the packet has not drifted. It does NOT mean a reviewer was")
    print("  found, contacted, or replied.")
    print("  known limit: a technical bundle binding cannot establish a reviewer, owner")
    print("  decision, ethics determination, permission, compensation, or external verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

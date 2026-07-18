#!/usr/bin/env python3
"""Validate the claim-level external calibration contract.

The validator is deliberately small and read-only.  It validates source
provenance, claim typing, calibration-stage gates, discriminator completeness,
and selected source-negative statements.  It cannot fetch literature, judge a
paper, run an experiment, or promote an evidence tier.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit


DEFAULT_RELATIVE_PATH = Path("03_METHODOLOGY/00_EXTERNAL_CALIBRATION_CLAIMS.json")
REQUIRED_TITLE = "Emergentist Compass External Calibration Claims"
REQUIRED_AUTHORITY_BOUNDARY = (
    "Machine-readable calibration records only. The Markdown ledger owns semantic wording. "
    "This file cannot create doctrine, validate the whole Compass, or promote evidence tiers."
)
ALLOWED_STAGES = {
    "X0_internal_only",
    "X1_construct_anchor",
    "X2_independent_data_discrimination",
    "X3_independent_preregistered_replication",
    "X4_cross_domain_replication",
    "not_applicable",
}
COMPONENT_STAGE_ORDER = (
    "X0_internal_only",
    "X1_construct_anchor",
    "X2_independent_data_discrimination",
    "X3_independent_preregistered_replication",
    "X4_cross_domain_replication",
    "not_applicable",
)
EMPIRICAL_STAGES = {
    "X0_internal_only",
    "X1_construct_anchor",
    "X2_independent_data_discrimination",
    "X3_independent_preregistered_replication",
    "X4_cross_domain_replication",
}
ALLOWED_CLASSES = {
    "analytic",
    "structural",
    "empirical",
    "normative",
    "correspondence",
    "symbolic",
}
ALLOWED_DISTANCES = {
    "direct_construct",
    "partial_overlap",
    "analogy",
    "normative_precedent",
    "not_applicable",
}
NON_EMPIRICAL_CLASSES = {"analytic", "normative", "correspondence", "symbolic"}
X2_DATA_STATUSES = {"result_receipted"}
X2_PREREG_STATUSES = {"frozen_before_access", "independent_preregistered"}
X3_PREREG_STATUSES = {"independent_preregistered"}
X2_ACCESS_BY_GENERATION = {
    "published_preexisting": "published_preexisting_frozen_before_access",
    "new_independent_after_preregistration": "new_independent_collection_after_preregistration",
}
ALLOWED_EVIDENCE_TIERS = {"I", "I/C", "S/I/C", "B", "B/I/C", "A", "A/B/I/C"}
ALLOWED_DATA_INDEPENDENCE = {
    "external_source",
    "external_source_required",
    "external_evaluator_required",
    "independent_team",
    "not_applicable",
}
ALLOWED_DATA_GENERATION = {
    "published_preexisting",
    "prospective_independent_collection_required",
    "new_independent_after_preregistration",
    "not_applicable",
}
ALLOWED_DATA_STATUSES = {
    "identified_not_run",
    "not_selected",
    "not_applicable",
    "analyzed_independent",
    "result_receipted",
}
ALLOWED_PREREG_STATUSES = {
    "prospective_protocol",
    "consequence_protocol_only",
    "design_required",
    "not_applicable",
    "frozen_before_access",
    "independent_preregistered",
}
REQUIRED_CLAIM_IDS = {
    "CAL-AGENCY-01",
    "CAL-CONE-01",
    "CAL-AGGREGATOR-01",
    "CAL-CONSTRAINT-01",
    "CAL-MU-01",
    "CAL-EGREGORE-01",
    "CAL-REFLEXIVITY-01",
    "CAL-SYNTROPY-01",
    "CAL-JUSTICE-CONSEQUENCE-01",
    "CAL-SPHERE-01",
    "CAL-DISPATCH-01",
    "CAL-CORRESPONDENCE-01",
}
REQUIRED_SOURCE_IDS = {
    "SRC-AKAM-2021",
    "SRC-BURRI",
    "SRC-CARPENTER-2011",
    "SRC-CENTOLA-2018",
    "SRC-COMPASS",
    "SRC-DAW-2011",
    "SRC-DOLL-2015",
    "SRC-FEHR-2002",
    "SRC-FLACK-2017",
    "SRC-HEEMEIJER-2009",
    "SRC-HOEL-2013",
    "SRC-KLYUBIN-2005",
    "SRC-LENS",
    "SRC-MONTEVIL-2015",
    "SRC-MUCHNIK-2013",
    "SRC-NASH-1950",
    "SRC-PETERS-2010",
    "SRC-RAND-2009",
    "SRC-RATCLIFF-2012",
    "SRC-ROSAS-2020",
    "SRC-SALGANIK-2006",
    "SRC-SALGE-2014",
    "SRC-SASAKI-2017",
    "SRC-SEN-1970",
    "SRC-SMITH-1988",
    "SRC-SOROS-2009",
    "SRC-THERAULAZ-1999",
    "SRC-TURNER-2021",
    "SRC-VICSEK-1995",
    "SRC-WEST-2015",
    "SRC-WISSNERGROSS-2013",
}
# Canonical JSON of the source records, sorted by id with sorted object keys.
# This freezes citations, source types, independence flags, and locations while
# allowing harmless source-array reordering.
REQUIRED_SOURCE_REGISTRY_SHA256 = (
    "0af94fe017eb13d9acee949e89c488fd9b17f7441ffed11698d0ed9caa4fb8e5"
)
IMMUTABLE_CLAIM_FIELDS = (
    "id",
    "title",
    "claimClass",
    "compassClaim",
    "sourceDistance",
    "sourceIds",
    "variables",
    "intervention",
    "outcomes",
    "rivals",
    "prediction",
    "killCriteria",
    "scopeBoundary",
)
REQUIRED_CLAIM_CONTRACT_SHA256 = (
    "5e0573bdd8125863885cbde00c4b29fe85ed6d1ddfdafc18ea2cbefc6b94d45e"
)
REQUIRED_NEGATIVE_CHECKS = {
    "NEG-WHOLE-VALIDATION": {
        "pattern": "whole Compass is externally validated",
        "paths": [
            "00_THE_COMPASS.md",
            "03_METHODOLOGY/00_EXTERNAL_CALIBRATION_LEDGER.md",
        ],
    },
    "NEG-PHYSICAL-RETRO": {
        "pattern": "future state physically causes the present",
        "paths": [
            "00_THE_COMPASS.md",
            "03_METHODOLOGY/00_EXTERNAL_CALIBRATION_LEDGER.md",
        ],
    },
    "NEG-UNIVERSAL-CONE": {
        "pattern": "all agents maximize reachable futures",
        "paths": ["00_THE_COMPASS.md"],
    },
    "NEG-DECISIVE-R": {
        "pattern": "THE decisive geometry test",
        "paths": [
            "03_METHODOLOGY/00_WHAT_ACTUALLY_TESTS_THE_THEORY.md",
            "03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md",
        ],
    },
    "NEG-REALITY-GEOMETRY": {
        "pattern": "This is a claim about the geometry of reality",
        "paths": ["03_METHODOLOGY/00_WHAT_ACTUALLY_TESTS_THE_THEORY.md"],
    },
}
TOP_LEVEL_KEYS = {
    "schemaVersion",
    "title",
    "asOf",
    "authorityBoundary",
    "wholeCompassVerdict",
    "calibrationStages",
    "claimClasses",
    "sourceDistances",
    "sources",
    "claims",
    "sourceNegativeChecks",
}
WHOLE_KEYS = {
    "calibrationStage",
    "componentStages",
    "evidenceTier",
    "validated",
    "wording",
}
SOURCE_KEYS = {"id", "citation", "sourceType", "independentOfCompass"}
CLAIM_KEYS = {
    "id",
    "title",
    "claimClass",
    "compassClaim",
    "currentVerdict",
    "calibrationStage",
    "sourceDistance",
    "evidenceTier",
    "sourceIds",
    "variables",
    "intervention",
    "outcomes",
    "rivals",
    "prediction",
    "killCriteria",
    "dataset",
    "preregistration",
    "scopeBoundary",
}
DATASET_KEYS = {
    "status",
    "independence",
    "dataGeneration",
    "access",
    "resultReceipt",
    "replicationReceipt",
    "resultVerdict",
    "replicationVerdict",
    "teams",
    "domains",
}
PREREG_KEYS = {"status", "path"}
NEGATIVE_KEYS = {"id", "pattern", "paths"}
RESULT_RECEIPT_KEYS = {
    "schemaVersion",
    "receiptKind",
    "claimId",
    "dataArtifact",
    "dataSha256",
    "preregSha256",
    "analysisManifest",
    "analysisManifestSha256",
    "analysisCommit",
    "freezeCommit",
    "outcome",
    "rivals",
    "date",
    "teamIds",
    "domains",
    "newIndependentObservations",
}
ANALYSIS_MANIFEST_KEYS = {
    "schemaVersion",
    "claimId",
    "datasetLocator",
    "datasetChecksum",
    "candidateModel",
    "rivals",
    "variables",
    "outcomes",
    "preprocessingSteps",
    "exclusions",
    "stoppingRule",
    "foldCount",
    "randomSeeds",
    "analysisCode",
    "environmentLock",
    "costPlan",
    "accessAttestation",
    "semanticReview",
}
DATASET_CHECKSUM_KEYS = {"mechanism", "expectedSha256"}
MODEL_SPEC_KEYS = {"name", "specification", "fitProcedure", "complexityPenalty"}
VARIABLE_SPEC_KEYS = {"name", "operationalDefinition", "unit"}
OUTCOME_SPEC_KEYS = {
    "name",
    "operationalDefinition",
    "unit",
    "primary",
    "decisionRule",
}
PREPROCESSING_STEP_KEYS = {"id", "operation", "parameters"}
EXCLUSION_KEYS = {"criterion", "rationale"}
STOPPING_RULE_KEYS = {"kind", "target", "unit", "interimLooks"}
FILE_BINDING_KEYS = {"path", "sha256"}
COST_PLAN_KEYS = {"budgets", "scalarization"}
COST_BUDGET_KEYS = {"category", "unit", "maximum"}
ACCESS_ATTESTATION_KEYS = {
    "status",
    "attestedBy",
    "attestedAt",
    "custodian",
    "custodyProtocol",
    "accessLog",
}
SEMANTIC_REVIEW_KEYS = {
    "status",
    "reviewedAt",
    "reviewerTeamIds",
    "independenceAttested",
    "checklist",
    "reviewReceipt",
}
SEMANTIC_REVIEW_CHECKS = {
    "datasetFitness",
    "candidateSpecification",
    "rivalCompleteness",
    "variableOperationalization",
    "outcomeDecisionRules",
    "preprocessingAndExclusions",
    "stoppingAndResampling",
    "costAndCustody",
}
RESULT_OUTCOMES = {"supported", "null", "failed", "mixed"}
RESULT_RECEIPT_KINDS = {"x2_discriminator", "x3_replication"}
KNOWN_PREFREEZE_PACKET_PREFIXES = (
    "11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form/",
    "11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/",
)
KNOWN_PREFREEZE_ARTIFACT_SHA256 = {
    "0ae6f766a76edf82d27fa31a594a3735d6370ae7807566752d5ac28ff57c4523",
    "0e33fffd7132cc7346a7c4ed4b4ec734c7a78cdffc5d6bb40d20aa7f00a7dd69",
    "19135f2afa0923ca98193f29b2c6e944161db964a00ca567f53af900f2a2cd95",
    "92b0d2338ddbc122cd0b324e7955793378777791088c1159418b0f1a57a3792c",
    "c32f302e697f36e9c2c750a6e210366396ba60f24301448d11ade569a3ec483c",
    "ea39aec1ac05d86fb4084dda547112ae78b917aa6127547f3b94f482dd6d4aa8",
}
WHOLE_PROMOTION_RE = re.compile(
    r"\b(?:validat\w*|verif\w*|prov(?:e|es|ed|en|ing)|proofs?|confirm\w*|"
    r"establish\w*|demonstrat\w*|certif\w*|corroborat\w*|conclus(?:ive|ively)|"
    r"settled|vindicat\w*|warranted|true|correct(?:ness)?|calibrat(?:e[ds]?|ing)|support\w*|"
    r"substantiat\w*|accept\w*|ratif\w*)\b",
    re.IGNORECASE,
)
WHOLE_SUBJECT_RE = re.compile(
    r"\b(?:whole[- ]system|whole compass|entire (?:compass|framework|worldview|theory)|"
    r"(?:compass|framework|worldview|theory) as a whole|"
    r"(?:the )?(?:compass|framework|worldview) (?:is|was|has|stands|remains))\b",
    re.IGNORECASE,
)
RESERVED_HOST_SUFFIXES = (".example", ".invalid", ".localhost", ".test")
VACUOUS_TEXT_RE = re.compile(
    r"^(?:tbd|todo|n/?a|none|unknown|placeholder|later|x+|test|fill\s+me)$",
    re.IGNORECASE,
)
IMMUTABLE_DATASET_ID_RE = re.compile(r"(?:artifact|repository):sha256:[0-9a-f]{64}")
X2_INFLATION_RE = re.compile(
    r"\b(?:validat\w*|verif\w*|prov(?:e|es|ed|en|ing)|proofs?|confirm\w*|"
    r"establish\w*|demonstrat\w*|certif\w*|universal|decisive(?:ly)?|"
    r"whole[- ]system|worldview|laws? of nature|geometry of reality)\b",
    re.IGNORECASE,
)


class CalibrationError(ValueError):
    """A stable validation failure."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CalibrationError(message)


def _exact_keys(
    record: dict[str, Any],
    allowed: set[str],
    label: str,
    *,
    required: set[str] | None = None,
) -> None:
    required_keys = allowed if required is None else required
    missing = sorted(required_keys - set(record))
    unknown = sorted(set(record) - allowed)
    _require(not missing, f"{label} missing keys: {missing}")
    _require(not unknown, f"{label} unknown keys: {unknown}")


def _tier_tokens(value: str) -> set[str]:
    return {token.strip() for token in value.split("/") if token.strip()}


def _nonempty_list(value: Any, label: str) -> list[Any]:
    _require(
        isinstance(value, list) and bool(value), f"{label} must be a nonempty list"
    )
    return value


def _substantive_text(value: Any, label: str, *, minimum: int = 8) -> str:
    _require(
        isinstance(value, str) and value.strip() == value,
        f"{label} must be trimmed text",
    )
    _require(
        len(value) >= minimum and VACUOUS_TEXT_RE.fullmatch(value) is None,
        f"{label} must be substantive, not a placeholder",
    )
    return value


def _unique_ids(records: Iterable[dict[str, Any]], label: str) -> set[str]:
    seen: set[str] = set()
    for record in records:
        _require(isinstance(record, dict), f"{label} record must be an object")
        record_id = record.get("id")
        _require(
            isinstance(record_id, str) and record_id, f"{label} id must be nonempty"
        )
        _require(record_id not in seen, f"duplicate {label} id: {record_id}")
        seen.add(record_id)
    return seen


def _inside_root(root: Path, relative: str, label: str) -> Path:
    root = root.resolve()
    path = (root / relative).resolve()
    _require(
        path == root or root in path.parents,
        f"{label} escapes repository root: {relative}",
    )
    return path


def _repository_file(root: Path, relative: Any, label: str) -> Path:
    _require(
        isinstance(relative, str) and relative.strip() == relative and relative,
        f"{label} must be a repository-relative path",
    )
    _require(
        not Path(relative).is_absolute(), f"{label} must be a repository-relative path"
    )
    _require(
        ":" not in relative and not re.search(r"[\x00\r\n]", relative),
        f"{label} contains unsafe path characters",
    )
    return _inside_root(root, relative, label)


def _sha256_file(path: Path, label: str) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise CalibrationError(f"{label} cannot be read: {exc}") from exc
    return digest.hexdigest()


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise CalibrationError(f"cannot execute Git provenance check: {exc}") from exc


def _validate_git_commit(root: Path, value: Any, label: str) -> str:
    commit = str(value or "")
    _require(
        bool(re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit)),
        f"{label} needs a full Git commit id",
    )
    result = _git(root, "rev-parse", "--verify", f"{commit}^{{commit}}")
    resolved = result.stdout.decode("ascii", errors="replace").strip()
    _require(
        result.returncode == 0 and resolved == commit,
        f"{label} does not identify an existing Git commit",
    )
    return commit


def _require_git_ancestor(root: Path, earlier: str, later: str, label: str) -> None:
    _require(earlier != later, f"{label} commits must be distinct")
    result = _git(root, "merge-base", "--is-ancestor", earlier, later)
    _require(result.returncode == 0, f"{label} commits are not ordered by ancestry")


def _require_git_path(root: Path, commit: str, relative: str, label: str) -> None:
    result = _git(root, "cat-file", "-e", f"{commit}:{relative}")
    _require(result.returncode == 0, f"{label} is not present at commit {commit}")


def _git_path_exists(root: Path, commit: str, relative: str) -> bool:
    return _git(root, "cat-file", "-e", f"{commit}:{relative}").returncode == 0


def _git_blob_sha256(root: Path, commit: str, relative: str, label: str) -> str:
    result = _git(root, "cat-file", "blob", f"{commit}:{relative}")
    _require(
        result.returncode == 0,
        f"{label} is not present as a data artifact at commit {commit}",
    )
    return hashlib.sha256(result.stdout).hexdigest()


def _validate_https_url(value: Any, label: str) -> None:
    _require(
        isinstance(value, str) and value.strip() == value and value,
        f"{label} URL must be a nonempty string",
    )
    _require(
        not any(character.isspace() for character in value),
        f"{label} URL may not contain whitespace",
    )
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise CalibrationError(f"{label} URL is malformed: {exc}") from exc
    _require(parsed.scheme == "https", f"{label} URL must use https")
    _require(
        bool(parsed.hostname) and bool(parsed.netloc),
        f"{label} URL must include a hostname",
    )
    _require(
        parsed.username is None and parsed.password is None,
        f"{label} URL may not embed credentials",
    )
    _require(port in {None, 443}, f"{label} URL may only use the default HTTPS port")
    _require(not parsed.fragment, f"{label} URL may not use a fragment as provenance")
    host = str(parsed.hostname).casefold().rstrip(".")
    _require(
        "." in host and host != "localhost", f"{label} URL hostname is not meaningful"
    )
    _require(
        not host.endswith(RESERVED_HOST_SUFFIXES),
        f"{label} URL may not use a reserved placeholder hostname",
    )
    _require(bool(parsed.path.strip("/")), f"{label} URL must identify a source path")


def _validate_dataset_locator(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and value.strip() == value,
        f"{label} must be trimmed text",
    )
    if value.startswith("https://"):
        _validate_https_url(value, label)
    else:
        _require(
            IMMUTABLE_DATASET_ID_RE.fullmatch(value) is not None,
            f"{label} must be HTTPS or an immutable artifact/repository identifier",
        )
    return value


def _validate_file_binding(root: Path, value: Any, label: str) -> tuple[str, Path, str]:
    _require(isinstance(value, dict), f"{label} must be an object")
    _exact_keys(value, FILE_BINDING_KEYS, label)
    relative = value.get("path")
    path = _repository_file(root, relative, f"{label}.path")
    _require(path.is_file(), f"{label}.path must be an existing file: {relative}")
    declared_hash = str(value.get("sha256", ""))
    _require(
        re.fullmatch(r"[0-9a-f]{64}", declared_hash) is not None,
        f"{label}.sha256 must be a SHA-256 digest",
    )
    _require(
        _sha256_file(path, label) == declared_hash,
        f"{label}.sha256 does not match the local file",
    )
    return str(relative), path, declared_hash


def _validate_analysis_code(path: Path, label: str) -> None:
    _require(path.suffix == ".py", f"{label} must bind a Python source file")
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        raise CalibrationError(f"{label} must be parseable Python: {exc}") from exc
    _require(
        len(source.encode("utf-8")) >= 32 and bool(tree.body),
        f"{label} cannot be empty or trivial",
    )
    _require(
        any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            for node in tree.body
        ),
        f"{label} must define an executable analysis function or class",
    )


def _validate_environment_lock(path: Path, label: str) -> None:
    _require(path.suffix == ".json", f"{label} must bind a JSON environment lock")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CalibrationError(f"{label} must be valid JSON: {exc}") from exc
    _require(
        isinstance(value, dict)
        and isinstance(value.get("runtime"), str)
        and isinstance(value.get("runtimeVersion"), str)
        and isinstance(value.get("platform"), str)
        and isinstance(value.get("dependencies"), dict)
        and bool(value["dependencies"]),
        f"{label} must specify runtime, version, platform, and dependencies",
    )


def _validate_access_log(path: Path, label: str) -> None:
    _require(
        path.suffix in {".log", ".jsonl"},
        f"{label} must bind an append-only log file",
    )
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CalibrationError(f"{label} must be readable text: {exc}") from exc
    entries = [line.strip() for line in content.splitlines() if line.strip()]
    _require(
        bool(entries) and all(len(entry) >= 24 for entry in entries),
        f"{label} must contain substantive frozen custody entries",
    )


def _validate_semantic_review_receipt(path: Path, claim_id: str, label: str) -> None:
    _require(path.suffix == ".md", f"{label} must bind a Markdown review receipt")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CalibrationError(f"{label} must be readable text: {exc}") from exc
    required_tokens = {claim_id, *SEMANTIC_REVIEW_CHECKS}
    _require(
        len(content.strip()) >= 256
        and all(token in content for token in required_tokens),
        f"{label} must document the claim and every semantic-review check",
    )


def _validate_analysis_manifest(
    root: Path,
    claim_id: str,
    receipt: dict[str, Any],
    expected_kind: str,
    claim_rivals: list[str],
    claim_variables: list[str],
    claim_outcomes: list[str],
) -> tuple[str, Path, str, dict[str, Any], list[tuple[str, str]]]:
    relative = receipt.get("analysisManifest")
    path = _repository_file(root, relative, f"{claim_id} analysisManifest")
    _require(
        path.suffix == ".json" and path.is_file(),
        f"{claim_id} analysisManifest must be an existing JSON file: {relative}",
    )
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CalibrationError(f"{claim_id} invalid analysisManifest: {exc}") from exc
    _require(
        isinstance(manifest, dict), f"{claim_id} analysisManifest must be an object"
    )
    _exact_keys(manifest, ANALYSIS_MANIFEST_KEYS, f"{claim_id}.analysisManifest")
    _require(
        manifest.get("schemaVersion") == "2.0",
        f"{claim_id} analysisManifest schema must be 2.0",
    )
    _require(
        manifest.get("claimId") == claim_id,
        f"{claim_id} analysisManifest claimId mismatch",
    )
    _validate_dataset_locator(
        manifest.get("datasetLocator"), f"{claim_id}.analysisManifest.datasetLocator"
    )

    checksum = manifest.get("datasetChecksum")
    _require(
        isinstance(checksum, dict), f"{claim_id} datasetChecksum must be an object"
    )
    _exact_keys(checksum, DATASET_CHECKSUM_KEYS, f"{claim_id}.datasetChecksum")
    expected_data_hash = checksum.get("expectedSha256")
    if expected_kind == "x2_discriminator":
        _require(
            checksum.get("mechanism") in {"publisher_sha256", "repository_sha256"},
            f"{claim_id} X2 datasetChecksum needs a frozen publisher/repository mechanism",
        )
        _require(
            isinstance(expected_data_hash, str)
            and re.fullmatch(r"[0-9a-f]{64}", expected_data_hash) is not None,
            f"{claim_id} X2 datasetChecksum needs an expected SHA-256",
        )
    else:
        _require(
            checksum.get("mechanism") == "compute_on_first_custody"
            and expected_data_hash is None,
            f"{claim_id} X3 datasetChecksum must defer the unknown hash to first custody",
        )

    candidate = manifest.get("candidateModel")
    _require(
        isinstance(candidate, dict), f"{claim_id} candidateModel must be an object"
    )
    _exact_keys(candidate, MODEL_SPEC_KEYS, f"{claim_id}.candidateModel")
    for field in MODEL_SPEC_KEYS:
        _substantive_text(
            candidate.get(field), f"{claim_id}.candidateModel.{field}", minimum=8
        )

    rivals = _nonempty_list(
        manifest.get("rivals"), f"{claim_id}.analysisManifest.rivals"
    )
    rival_names: list[str] = []
    for index, rival in enumerate(rivals):
        label = f"{claim_id}.analysisManifest.rivals[{index}]"
        _require(isinstance(rival, dict), f"{label} must be an object")
        _exact_keys(rival, MODEL_SPEC_KEYS, label)
        rival_names.append(str(rival.get("name", "")))
        for field in ("specification", "fitProcedure", "complexityPenalty"):
            _substantive_text(rival.get(field), f"{label}.{field}", minimum=8)
    _require(
        len(rival_names) == len(set(rival_names)),
        f"{claim_id} analysisManifest rivals must be unique",
    )
    _require(
        set(rival_names) == set(claim_rivals),
        f"{claim_id} analysisManifest rivals must match the claim contract",
    )

    variables = _nonempty_list(
        manifest.get("variables"), f"{claim_id}.analysisManifest.variables"
    )
    variable_names: list[str] = []
    for index, variable in enumerate(variables):
        label = f"{claim_id}.analysisManifest.variables[{index}]"
        _require(isinstance(variable, dict), f"{label} must be an object")
        _exact_keys(variable, VARIABLE_SPEC_KEYS, label)
        variable_names.append(str(variable.get("name", "")))
        _substantive_text(
            variable.get("operationalDefinition"),
            f"{label}.operationalDefinition",
            minimum=12,
        )
        _substantive_text(variable.get("unit"), f"{label}.unit", minimum=2)
    _require(
        len(variable_names) == len(set(variable_names))
        and set(variable_names) == set(claim_variables),
        f"{claim_id} analysisManifest variables must match the claim contract",
    )

    outcomes = _nonempty_list(
        manifest.get("outcomes"), f"{claim_id}.analysisManifest.outcomes"
    )
    outcome_names: list[str] = []
    for index, outcome in enumerate(outcomes):
        label = f"{claim_id}.analysisManifest.outcomes[{index}]"
        _require(isinstance(outcome, dict), f"{label} must be an object")
        _exact_keys(outcome, OUTCOME_SPEC_KEYS, label)
        outcome_names.append(str(outcome.get("name", "")))
        _substantive_text(
            outcome.get("operationalDefinition"),
            f"{label}.operationalDefinition",
            minimum=12,
        )
        _substantive_text(outcome.get("unit"), f"{label}.unit", minimum=2)
        _require(
            isinstance(outcome.get("primary"), bool), f"{label}.primary must be boolean"
        )
        _substantive_text(
            outcome.get("decisionRule"), f"{label}.decisionRule", minimum=12
        )
    _require(
        len(outcome_names) == len(set(outcome_names))
        and set(outcome_names) == set(claim_outcomes),
        f"{claim_id} analysisManifest outcomes must match the claim contract",
    )
    _require(
        any(outcome["primary"] for outcome in outcomes),
        f"{claim_id} analysisManifest needs at least one primary outcome",
    )

    preprocessing = _nonempty_list(
        manifest.get("preprocessingSteps"),
        f"{claim_id}.analysisManifest.preprocessingSteps",
    )
    preprocessing_ids: list[str] = []
    for index, step in enumerate(preprocessing):
        label = f"{claim_id}.analysisManifest.preprocessingSteps[{index}]"
        _require(isinstance(step, dict), f"{label} must be an object")
        _exact_keys(step, PREPROCESSING_STEP_KEYS, label)
        step_id = str(step.get("id", ""))
        _require(
            re.fullmatch(r"step-[1-9][0-9]*", step_id) is not None,
            f"{label}.id must use step-N",
        )
        preprocessing_ids.append(step_id)
        _substantive_text(step.get("operation"), f"{label}.operation", minimum=12)
        _require(
            isinstance(step.get("parameters"), dict) and bool(step["parameters"]),
            f"{label}.parameters must be a nonempty object",
        )
    _require(
        len(preprocessing_ids) == len(set(preprocessing_ids)),
        f"{claim_id} preprocessing step ids must be unique",
    )

    exclusions = _nonempty_list(
        manifest.get("exclusions"), f"{claim_id}.analysisManifest.exclusions"
    )
    for index, exclusion in enumerate(exclusions):
        label = f"{claim_id}.analysisManifest.exclusions[{index}]"
        _require(isinstance(exclusion, dict), f"{label} must be an object")
        _exact_keys(exclusion, EXCLUSION_KEYS, label)
        _substantive_text(exclusion.get("criterion"), f"{label}.criterion", minimum=12)
        _substantive_text(exclusion.get("rationale"), f"{label}.rationale", minimum=12)

    stopping = manifest.get("stoppingRule")
    _require(isinstance(stopping, dict), f"{claim_id} stoppingRule must be an object")
    _exact_keys(stopping, STOPPING_RULE_KEYS, f"{claim_id}.stoppingRule")
    _require(
        stopping.get("kind")
        in {"fixed_sample", "fixed_duration", "exhaustive_artifact"},
        f"{claim_id} stoppingRule kind is invalid",
    )
    _require(
        isinstance(stopping.get("target"), int)
        and not isinstance(stopping["target"], bool)
        and stopping["target"] > 0,
        f"{claim_id} stoppingRule target must be a positive integer",
    )
    _require(
        stopping.get("unit") in {"observations", "sessions", "days", "artifacts"},
        f"{claim_id} stoppingRule unit is invalid",
    )
    _require(
        isinstance(stopping.get("interimLooks"), int)
        and not isinstance(stopping["interimLooks"], bool)
        and stopping["interimLooks"] >= 0,
        f"{claim_id} stoppingRule interimLooks must be a nonnegative integer",
    )

    fold_count = manifest.get("foldCount")
    _require(
        isinstance(fold_count, int)
        and not isinstance(fold_count, bool)
        and 2 <= fold_count <= 20,
        f"{claim_id} foldCount must be an integer from 2 through 20",
    )
    seeds = _nonempty_list(
        manifest.get("randomSeeds"), f"{claim_id}.analysisManifest.randomSeeds"
    )
    _require(
        all(
            isinstance(seed, int)
            and not isinstance(seed, bool)
            and 0 <= seed <= 2**32 - 1
            for seed in seeds
        )
        and len(seeds) == len(set(seeds)),
        f"{claim_id} randomSeeds must be unique unsigned 32-bit integers",
    )

    frozen_files: list[tuple[str, str]] = []
    analysis_code_relative, analysis_code_path, analysis_code_hash = (
        _validate_file_binding(
            root,
            manifest.get("analysisCode"),
            f"{claim_id}.analysisManifest.analysisCode",
        )
    )
    _validate_analysis_code(
        analysis_code_path, f"{claim_id}.analysisManifest.analysisCode"
    )
    frozen_files.append((analysis_code_relative, analysis_code_hash))
    environment_relative, environment_path, environment_hash = _validate_file_binding(
        root,
        manifest.get("environmentLock"),
        f"{claim_id}.analysisManifest.environmentLock",
    )
    _validate_environment_lock(
        environment_path, f"{claim_id}.analysisManifest.environmentLock"
    )
    frozen_files.append((environment_relative, environment_hash))

    cost_plan = manifest.get("costPlan")
    _require(isinstance(cost_plan, dict), f"{claim_id} costPlan must be an object")
    _exact_keys(cost_plan, COST_PLAN_KEYS, f"{claim_id}.costPlan")
    _require(
        cost_plan.get("scalarization") == "none",
        f"{claim_id} costPlan scalarization must remain none",
    )
    budgets = _nonempty_list(cost_plan.get("budgets"), f"{claim_id}.costPlan.budgets")
    budget_categories: list[str] = []
    for index, budget in enumerate(budgets):
        label = f"{claim_id}.costPlan.budgets[{index}]"
        _require(isinstance(budget, dict), f"{label} must be an object")
        _exact_keys(budget, COST_BUDGET_KEYS, label)
        budget_categories.append(str(budget.get("category", "")))
        _substantive_text(budget.get("unit"), f"{label}.unit", minimum=2)
        _require(
            isinstance(budget.get("maximum"), (int, float))
            and not isinstance(budget["maximum"], bool)
            and budget["maximum"] >= 0,
            f"{label}.maximum must be a nonnegative number",
        )
    _require(
        set(budget_categories) == {"compute", "data_acquisition", "labor"}
        and len(budget_categories) == 3,
        f"{claim_id} costPlan must separately budget compute, data acquisition, and labor",
    )

    attestation = manifest.get("accessAttestation")
    _require(
        isinstance(attestation, dict), f"{claim_id} accessAttestation must be an object"
    )
    _exact_keys(attestation, ACCESS_ATTESTATION_KEYS, f"{claim_id}.accessAttestation")
    expected_status = (
        "not_accessed_before_freeze"
        if expected_kind == "x2_discriminator"
        else "not_collected_before_freeze"
    )
    _require(
        attestation.get("status") == expected_status,
        f"{claim_id} accessAttestation must declare {expected_status}",
    )
    _substantive_text(
        attestation.get("attestedBy"), f"{claim_id}.accessAttestation.attestedBy"
    )
    _substantive_text(
        attestation.get("custodian"), f"{claim_id}.accessAttestation.custodian"
    )
    _substantive_text(
        attestation.get("custodyProtocol"),
        f"{claim_id}.accessAttestation.custodyProtocol",
        minimum=12,
    )
    access_log_relative, access_log_path, access_log_hash = _validate_file_binding(
        root,
        attestation.get("accessLog"),
        f"{claim_id}.accessAttestation.accessLog",
    )
    _validate_access_log(
        access_log_path, f"{claim_id}.accessAttestation.accessLog"
    )
    frozen_files.append((access_log_relative, access_log_hash))
    date_text = str(attestation.get("attestedAt", ""))
    try:
        attested_date = dt.date.fromisoformat(date_text)
    except ValueError as exc:
        raise CalibrationError(
            f"{claim_id} accessAttestation needs a real ISO date"
        ) from exc
    _require(
        attested_date.isoformat() == date_text and attested_date <= dt.date.today(),
        f"{claim_id} accessAttestation needs a real non-future ISO date",
    )

    semantic_review = manifest.get("semanticReview")
    _require(
        isinstance(semantic_review, dict),
        f"{claim_id} semanticReview must be an object",
    )
    _exact_keys(semantic_review, SEMANTIC_REVIEW_KEYS, f"{claim_id}.semanticReview")
    _require(
        semantic_review.get("status") == "approved_for_frozen_run",
        f"{claim_id} semanticReview must approve the frozen run",
    )
    _require(
        semantic_review.get("independenceAttested") is True,
        f"{claim_id} semanticReview must attest reviewer independence",
    )
    reviewer_team_ids = _nonempty_list(
        semantic_review.get("reviewerTeamIds"),
        f"{claim_id}.semanticReview.reviewerTeamIds",
    )
    _require(
        all(
            isinstance(team_id, str)
            and team_id.strip() == team_id
            and len(team_id) >= 8
            for team_id in reviewer_team_ids
        )
        and len(reviewer_team_ids) == len(set(reviewer_team_ids)),
        f"{claim_id} semanticReview reviewerTeamIds must be unique substantive names",
    )
    _require(
        set(reviewer_team_ids).isdisjoint(
            {attestation["attestedBy"], attestation["custodian"]}
        ),
        f"{claim_id} semantic reviewer cannot be the access attester or custodian",
    )
    review_date_text = str(semantic_review.get("reviewedAt", ""))
    try:
        review_date = dt.date.fromisoformat(review_date_text)
    except ValueError as exc:
        raise CalibrationError(
            f"{claim_id} semanticReview needs a real ISO date"
        ) from exc
    _require(
        review_date.isoformat() == review_date_text
        and review_date <= dt.date.today(),
        f"{claim_id} semanticReview needs a real non-future ISO date",
    )
    checklist = semantic_review.get("checklist")
    _require(isinstance(checklist, dict), f"{claim_id} semanticReview checklist must be an object")
    _exact_keys(checklist, SEMANTIC_REVIEW_CHECKS, f"{claim_id}.semanticReview.checklist")
    _require(
        all(value is True for value in checklist.values()),
        f"{claim_id} semanticReview checklist must approve every required check",
    )
    review_relative, review_path, review_hash = _validate_file_binding(
        root,
        semantic_review.get("reviewReceipt"),
        f"{claim_id}.semanticReview.reviewReceipt",
    )
    _validate_semantic_review_receipt(
        review_path, claim_id, f"{claim_id}.semanticReview.reviewReceipt"
    )
    frozen_files.append((review_relative, review_hash))
    _require(
        len({relative_file for relative_file, _ in frozen_files}) == len(frozen_files),
        f"{claim_id} analysisCode, environmentLock, accessLog, and semanticReview receipt must be distinct files",
    )
    declared_hash = str(receipt.get("analysisManifestSha256", ""))
    _require(
        bool(re.fullmatch(r"[0-9a-f]{64}", declared_hash)),
        f"{claim_id} result receipt needs a SHA-256 analysisManifestSha256",
    )
    _require(
        _sha256_file(path, f"{claim_id} analysisManifest") == declared_hash,
        f"{claim_id} analysisManifestSha256 does not match the local manifest",
    )
    return str(relative), path, declared_hash, manifest, frozen_files


def _validate_result_receipt(
    root: Path,
    claim_id: str,
    relative: Any,
    prereg_path: str,
    expected_kind: str,
    claim_rivals: list[str],
    claim_variables: list[str],
    claim_outcomes: list[str],
    require_current_prereg: bool,
) -> dict[str, Any]:
    _require(
        isinstance(relative, str) and relative,
        f"{claim_id} X2+ requires a result receipt",
    )
    path = _repository_file(root, relative, f"{claim_id} result receipt")
    prereg = _repository_file(root, prereg_path, f"{claim_id} preregistration")
    _require(
        path != prereg,
        f"{claim_id} result receipt must be distinct from preregistration",
    )
    _require(
        path.suffix == ".json" and path.is_file(),
        f"{claim_id} result receipt must be an existing JSON file: {relative}",
    )
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CalibrationError(f"{claim_id} invalid result receipt: {exc}") from exc
    _require(isinstance(receipt, dict), f"{claim_id} result receipt must be an object")
    _exact_keys(receipt, RESULT_RECEIPT_KEYS, f"{claim_id}.resultReceipt")
    _require(
        receipt.get("schemaVersion") == "2.1",
        f"{claim_id} result receipt schema must be 2.1",
    )
    _require(
        receipt.get("receiptKind") in RESULT_RECEIPT_KINDS,
        f"{claim_id} result receipt has invalid receiptKind",
    )
    _require(
        receipt.get("receiptKind") == expected_kind,
        f"{claim_id} result receipt must be {expected_kind}",
    )
    _require(
        receipt.get("claimId") == claim_id,
        f"{claim_id} result receipt claimId mismatch",
    )
    artifact_relative = receipt.get("dataArtifact")
    artifact = _repository_file(root, artifact_relative, f"{claim_id} dataArtifact")
    _require(
        artifact.is_file(),
        f"{claim_id} dataArtifact must be an existing local file: {artifact_relative}",
    )
    _require(
        artifact not in {path, prereg},
        f"{claim_id} dataArtifact must be distinct from receipt and preregistration",
    )
    (
        manifest_relative,
        manifest_path,
        declared_manifest_hash,
        analysis_manifest,
        frozen_manifest_files,
    ) = _validate_analysis_manifest(
        root,
        claim_id,
        receipt,
        expected_kind,
        claim_rivals,
        claim_variables,
        claim_outcomes,
    )
    _require(
        manifest_path not in {path, prereg, artifact},
        f"{claim_id} analysisManifest must be distinct from receipt, preregistration, and dataArtifact",
    )
    declared_hash = str(receipt.get("dataSha256", ""))
    _require(
        bool(re.fullmatch(r"[0-9a-f]{64}", declared_hash)),
        f"{claim_id} result receipt needs a SHA-256 dataSha256",
    )
    _require(
        _sha256_file(artifact, f"{claim_id} dataArtifact") == declared_hash,
        f"{claim_id} dataSha256 does not match the local data artifact",
    )
    _require(
        not any(
            artifact.relative_to(root.resolve()).as_posix().startswith(prefix)
            for prefix in KNOWN_PREFREEZE_PACKET_PREFIXES
        ),
        f"{claim_id} cannot promote a disclosed pre-freeze packet path",
    )
    _require(
        declared_hash not in KNOWN_PREFREEZE_ARTIFACT_SHA256,
        f"{claim_id} cannot promote a disclosed pre-freeze packet hash",
    )
    declared_prereg_hash = str(receipt.get("preregSha256", ""))
    _require(
        bool(re.fullmatch(r"[0-9a-f]{64}", declared_prereg_hash)),
        f"{claim_id} result receipt needs a SHA-256 preregSha256",
    )
    freeze_commit = _validate_git_commit(
        root, receipt.get("freezeCommit"), f"{claim_id} freezeCommit"
    )
    analysis_commit = _validate_git_commit(
        root, receipt.get("analysisCommit"), f"{claim_id} analysisCommit"
    )
    _require_git_ancestor(
        root, freeze_commit, analysis_commit, f"{claim_id} freeze/analysis"
    )
    _require_git_path(root, freeze_commit, prereg_path, f"{claim_id} preregistration")
    _require_git_path(
        root, freeze_commit, manifest_relative, f"{claim_id} analysisManifest"
    )
    frozen_manifest_hash = _git_blob_sha256(
        root, freeze_commit, manifest_relative, f"{claim_id} analysisManifest"
    )
    _require(
        frozen_manifest_hash == declared_manifest_hash,
        f"{claim_id} freezeCommit does not bind the declared analysisManifest hash",
    )
    for frozen_relative, frozen_hash in frozen_manifest_files:
        bound_hash = _git_blob_sha256(
            root,
            freeze_commit,
            frozen_relative,
            f"{claim_id} frozen manifest dependency {frozen_relative}",
        )
        _require(
            bound_hash == frozen_hash,
            f"{claim_id} freezeCommit does not bind {frozen_relative} at its declared hash",
        )
    _require(
        not _git_path_exists(root, freeze_commit, str(artifact_relative)),
        f"{claim_id} dataArtifact already existed at the freeze commit",
    )
    frozen_prereg_hash = _git_blob_sha256(
        root, freeze_commit, prereg_path, f"{claim_id} preregistration"
    )
    _require(
        frozen_prereg_hash == declared_prereg_hash,
        f"{claim_id} freezeCommit does not bind the declared preregistration hash",
    )
    if require_current_prereg:
        _require(
            _sha256_file(prereg, f"{claim_id} preregistration") == declared_prereg_hash,
            f"{claim_id} current preregistration differs from the frozen preregistration",
        )
    analysis_bindings = [
        (prereg_path, declared_prereg_hash, "preregistration"),
        (manifest_relative, declared_manifest_hash, "analysisManifest"),
        *(
            (relative, expected_hash, f"manifest dependency {relative}")
            for relative, expected_hash in frozen_manifest_files
        ),
    ]
    for relative, expected_hash, label in analysis_bindings:
        analysis_hash = _git_blob_sha256(
            root,
            analysis_commit,
            relative,
            f"{claim_id} analysis-time {label}",
        )
        _require(
            analysis_hash == expected_hash,
            f"{claim_id} analysisCommit does not retain {relative} at its frozen hash",
        )
    committed_hash = _git_blob_sha256(
        root, analysis_commit, artifact_relative, f"{claim_id} dataArtifact"
    )
    _require(
        committed_hash == declared_hash,
        f"{claim_id} analysisCommit does not bind the declared data artifact/hash",
    )
    expected_data_hash = analysis_manifest["datasetChecksum"]["expectedSha256"]
    if expected_data_hash is not None:
        _require(
            declared_hash == expected_data_hash,
            f"{claim_id} dataSha256 does not match the frozen expected dataset hash",
        )
    locator = analysis_manifest["datasetLocator"]
    if locator.startswith(("artifact:sha256:", "repository:sha256:")):
        _require(
            locator.rsplit(":", 1)[-1] == declared_hash,
            f"{claim_id} immutable dataset identifier does not match dataSha256",
        )
    _require(
        receipt.get("outcome") in RESULT_OUTCOMES,
        f"{claim_id} result receipt has invalid outcome",
    )
    rivals = _nonempty_list(receipt.get("rivals"), f"{claim_id}.resultReceipt.rivals")
    _require(
        all(isinstance(rival, str) and rival.strip() for rival in rivals),
        f"{claim_id} result receipt rivals must contain names",
    )
    _require(
        len(rivals) == len(set(rivals)),
        f"{claim_id} result receipt rivals must be unique",
    )
    _require(
        set(rivals) == set(claim_rivals),
        f"{claim_id} result receipt rivals must match the claim rivals",
    )
    date_text = str(receipt.get("date", ""))
    try:
        receipt_date = dt.date.fromisoformat(date_text)
    except ValueError as exc:
        raise CalibrationError(
            f"{claim_id} result receipt needs a real ISO date"
        ) from exc
    _require(
        receipt_date.isoformat() == date_text,
        f"{claim_id} result receipt needs a real ISO date",
    )
    _require(
        receipt_date <= dt.date.today(),
        f"{claim_id} result receipt date cannot be in the future",
    )
    for field in ("teamIds", "domains"):
        values = _nonempty_list(receipt.get(field), f"{claim_id}.resultReceipt.{field}")
        _require(
            all(isinstance(value, str) and value.strip() for value in values),
            f"{claim_id} result receipt {field} must contain names",
        )
        _require(
            len(values) == len(set(values)),
            f"{claim_id} result receipt {field} must be unique",
        )
    _require(
        set(receipt["teamIds"]).isdisjoint(
            analysis_manifest["semanticReview"]["reviewerTeamIds"]
        ),
        f"{claim_id} semantic-review teams must be distinct from the analysis team",
    )
    _require(
        isinstance(receipt.get("newIndependentObservations"), bool),
        f"{claim_id} result receipt newIndependentObservations must be boolean",
    )
    return receipt


def _validate_sources(payload: dict[str, Any], root: Path) -> tuple[set[str], set[str]]:
    sources = _nonempty_list(payload.get("sources"), "sources")
    source_ids = _unique_ids(sources, "source")
    for source in sources:
        source_id = source["id"]
        _exact_keys(
            source, SOURCE_KEYS | {"url", "path"}, source_id, required=SOURCE_KEYS
        )
        _require(
            isinstance(source.get("citation"), str) and source["citation"].strip(),
            f"{source_id} missing citation",
        )
        _require(
            isinstance(source.get("sourceType"), str) and source["sourceType"].strip(),
            f"{source_id} missing sourceType",
        )
        independent = source.get("independentOfCompass")
        _require(
            isinstance(independent, bool), f"{source_id} independence must be boolean"
        )
        has_url = "url" in source
        has_path = "path" in source
        _require(
            has_url ^ has_path, f"{source_id} must declare exactly one of url or path"
        )
        if has_url:
            url = source["url"]
            _validate_https_url(url, source_id)
            _require(
                independent,
                f"external source {source_id} must be independent of Compass",
            )
        else:
            path = source["path"]
            _require(
                isinstance(path, str) and path, f"{source_id} path must be nonempty"
            )
            _require(
                _inside_root(root, path, source_id).is_file(),
                f"internal source path missing: {path}",
            )
            _require(
                not independent,
                f"internal source {source_id} cannot be marked independent",
            )
    _require(
        source_ids == REQUIRED_SOURCE_IDS,
        f"source registry drift: expected {sorted(REQUIRED_SOURCE_IDS)}, got {sorted(source_ids)}",
    )
    canonical = json.dumps(
        sorted(sources, key=lambda source: source["id"]),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    registry_hash = hashlib.sha256(canonical).hexdigest()
    _require(
        registry_hash == REQUIRED_SOURCE_REGISTRY_SHA256,
        "source registry content drift",
    )
    independent_ids = {
        source["id"] for source in sources if source["independentOfCompass"]
    }
    return source_ids, independent_ids


def _validate_claims(
    payload: dict[str, Any],
    source_ids: set[str],
    independent_source_ids: set[str],
    root: Path,
) -> set[str]:
    claims = _nonempty_list(payload.get("claims"), "claims")
    claim_ids = _unique_ids(claims, "claim")
    _require(
        claim_ids == REQUIRED_CLAIM_IDS,
        f"claim registry drift: expected {sorted(REQUIRED_CLAIM_IDS)}, got {sorted(claim_ids)}",
    )
    for claim in claims:
        claim_id = claim["id"]
        _exact_keys(claim, CLAIM_KEYS, claim_id)
        claim_class = claim.get("claimClass")
        stage = claim.get("calibrationStage")
        distance = claim.get("sourceDistance")
        _require(
            claim_class in ALLOWED_CLASSES,
            f"{claim_id} invalid claimClass: {claim_class}",
        )
        _require(
            stage in ALLOWED_STAGES, f"{claim_id} invalid calibrationStage: {stage}"
        )
        _require(
            distance in ALLOWED_DISTANCES,
            f"{claim_id} invalid sourceDistance: {distance}",
        )
        for field in (
            "title",
            "compassClaim",
            "currentVerdict",
            "evidenceTier",
            "prediction",
            "scopeBoundary",
        ):
            _require(
                isinstance(claim.get(field), str) and claim[field].strip(),
                f"{claim_id} missing {field}",
            )

        refs = _nonempty_list(claim.get("sourceIds"), f"{claim_id}.sourceIds")
        _require(
            all(isinstance(ref, str) and ref.strip() for ref in refs),
            f"{claim_id}.sourceIds must contain names",
        )
        unknown = sorted(set(refs) - source_ids)
        _require(not unknown, f"{claim_id} references unknown sources: {unknown}")
        _require(len(refs) == len(set(refs)), f"{claim_id} repeats sourceIds")
        outcomes = _nonempty_list(claim.get("outcomes"), f"{claim_id}.outcomes")
        _require(
            all(isinstance(outcome, str) and outcome.strip() for outcome in outcomes),
            f"{claim_id}.outcomes must contain text",
        )
        claim_rivals = _nonempty_list(claim.get("rivals"), f"{claim_id}.rivals")
        _require(
            all(isinstance(rival, str) and rival.strip() for rival in claim_rivals),
            f"{claim_id}.rivals must contain names",
        )
        _require(
            len(claim_rivals) == len(set(claim_rivals)),
            f"{claim_id}.rivals must be unique",
        )
        kill_criteria = _nonempty_list(
            claim.get("killCriteria"), f"{claim_id}.killCriteria"
        )
        _require(
            all(
                isinstance(criterion, str) and criterion.strip()
                for criterion in kill_criteria
            ),
            f"{claim_id}.killCriteria must contain text",
        )
        _require(
            isinstance(claim.get("intervention"), str)
            and claim["intervention"].strip(),
            f"{claim_id} missing intervention",
        )
        variables = claim.get("variables")
        _require(isinstance(variables, list), f"{claim_id}.variables must be a list")
        _require(
            all(
                isinstance(variable, str) and variable.strip() for variable in variables
            ),
            f"{claim_id}.variables must contain text",
        )

        dataset = claim.get("dataset")
        prereg = claim.get("preregistration")
        _require(isinstance(dataset, dict), f"{claim_id} missing dataset record")
        _require(isinstance(prereg, dict), f"{claim_id} missing preregistration record")
        _exact_keys(
            dataset,
            DATASET_KEYS,
            f"{claim_id}.dataset",
            required={"status", "independence", "dataGeneration", "access"},
        )
        _exact_keys(prereg, PREREG_KEYS, f"{claim_id}.preregistration")
        _require(
            bool(dataset.get("status"))
            and bool(dataset.get("independence"))
            and bool(dataset.get("access")),
            f"{claim_id} dataset record incomplete",
        )
        _require(
            dataset.get("status") in ALLOWED_DATA_STATUSES,
            f"{claim_id} invalid dataset status",
        )
        _require(
            dataset.get("independence") in ALLOWED_DATA_INDEPENDENCE,
            f"{claim_id} invalid dataset independence",
        )
        _require(
            dataset.get("dataGeneration") in ALLOWED_DATA_GENERATION,
            f"{claim_id} invalid data generation status",
        )
        _require(
            prereg.get("status") in ALLOWED_PREREG_STATUSES,
            f"{claim_id} invalid preregistration status",
        )
        has_result_receipt = "resultReceipt" in dataset
        has_replication_receipt = "replicationReceipt" in dataset
        if dataset.get("status") == "result_receipted":
            _require(
                has_result_receipt
                and isinstance(dataset.get("resultReceipt"), str)
                and bool(dataset["resultReceipt"]),
                f"{claim_id} result_receipted status requires resultReceipt",
            )
        else:
            _require(
                not has_result_receipt,
                f"{claim_id} resultReceipt requires result_receipted status",
            )
            _require(
                not has_replication_receipt,
                f"{claim_id} replicationReceipt requires result_receipted status",
            )
        if has_replication_receipt:
            _require(
                isinstance(dataset.get("replicationReceipt"), str)
                and bool(dataset["replicationReceipt"]),
                f"{claim_id} replicationReceipt must be a nonempty path",
            )
            _require(
                has_result_receipt,
                f"{claim_id} replicationReceipt requires a prior resultReceipt",
            )
        prereg_path = prereg.get("path")
        _require(
            isinstance(prereg_path, str)
            and _inside_root(root, prereg_path, claim_id).is_file(),
            f"{claim_id} preregistration path missing: {prereg_path}",
        )

        if claim_class in NON_EMPIRICAL_CLASSES:
            _require(
                stage == "not_applicable",
                f"{claim_id} non-empirical class cannot receive empirical calibration stage",
            )
            _require(
                dataset.get("dataGeneration") == "not_applicable",
                f"{claim_id} non-empirical class needs not_applicable data generation",
            )
        else:
            _require(
                stage in EMPIRICAL_STAGES,
                f"{claim_id} empirical/structural claim needs X0-X4 stage",
            )
            _nonempty_list(variables, f"{claim_id}.variables")

        if stage in {
            "X1_construct_anchor",
            "X2_independent_data_discrimination",
            "X3_independent_preregistered_replication",
            "X4_cross_domain_replication",
        }:
            _require(
                bool(set(refs) & independent_source_ids),
                f"{claim_id} X1 requires an independent external source",
            )
            _require(
                distance != "not_applicable",
                f"{claim_id} X1 requires a declared source distance",
            )

        tier = claim.get("evidenceTier")
        _require(
            tier in ALLOWED_EVIDENCE_TIERS, f"{claim_id} invalid evidenceTier: {tier}"
        )
        tier_tokens = _tier_tokens(tier)
        if stage in {"X0_internal_only", "X1_construct_anchor", "not_applicable"}:
            _require("A" not in tier_tokens, f"{claim_id} cannot claim A before X3")
            _require(
                not has_result_receipt and not has_replication_receipt,
                f"{claim_id} cannot carry a result receipt before X2",
            )
            _require(
                "resultVerdict" not in dataset and "replicationVerdict" not in dataset,
                f"{claim_id} cannot carry typed result verdicts before X2",
            )
        if stage == "X2_independent_data_discrimination":
            _require(
                "B" in tier_tokens and "A" not in tier_tokens,
                f"{claim_id} X2 requires bounded B evidence",
            )
            _require(
                not has_replication_receipt,
                f"{claim_id} X2 cannot carry replicationReceipt",
            )
        if stage in {
            "X3_independent_preregistered_replication",
            "X4_cross_domain_replication",
        }:
            _require("A" in tier_tokens, f"{claim_id} X3+ requires bounded A evidence")
        verdict_text = f"{claim.get('currentVerdict', '')} {claim.get('scopeBoundary', '')}".casefold()
        if stage in {"X0_internal_only", "X1_construct_anchor"}:
            _require(
                "externally validated" not in verdict_text,
                f"{claim_id} cannot claim external validation at {stage}",
            )
            _require(
                "confirmed universal law" not in verdict_text,
                f"{claim_id} cannot claim a confirmed universal law",
            )
        if stage == "X2_independent_data_discrimination":
            _require(
                X2_INFLATION_RE.search(str(claim.get("scopeBoundary", ""))) is None,
                f"{claim_id} X2 verdict cannot claim proof, confirmation, universality, or whole-system reach",
            )

        if stage in {
            "X2_independent_data_discrimination",
            "X3_independent_preregistered_replication",
            "X4_cross_domain_replication",
        }:
            _require(
                dataset.get("status") in X2_DATA_STATUSES,
                f"{claim_id} X2+ requires analyzed independent data",
            )
            _require(
                dataset.get("independence") in {"external_source", "independent_team"},
                f"{claim_id} X2+ requires independent data provenance",
            )
            _require(
                dataset.get("dataGeneration")
                in {"published_preexisting", "new_independent_after_preregistration"},
                f"{claim_id} X2+ requires a completed data-generation status",
            )
            _require(
                dataset.get("access")
                == X2_ACCESS_BY_GENERATION[dataset["dataGeneration"]],
                f"{claim_id} X2+ has invalid frozen-access declaration",
            )
            _require(
                prereg.get("status") in X2_PREREG_STATUSES,
                f"{claim_id} X2+ requires a frozen discriminator",
            )
            result_receipt = _validate_result_receipt(
                root,
                claim_id,
                dataset.get("resultReceipt"),
                prereg_path,
                "x2_discriminator",
                claim_rivals,
                variables,
                outcomes,
                stage == "X2_independent_data_discrimination",
            )
            _require(
                dataset.get("resultVerdict") == result_receipt["outcome"],
                f"{claim_id} resultVerdict must equal the X2 receipt outcome",
            )
            if stage == "X2_independent_data_discrimination":
                _require(
                    "replicationVerdict" not in dataset,
                    f"{claim_id} X2 cannot carry replicationVerdict",
                )
                expected_token = f"X2 outcome={result_receipt['outcome']}"
                _require(
                    claim["currentVerdict"] == expected_token,
                    f"{claim_id} currentVerdict must equal {expected_token}",
                )
        if stage in {
            "X3_independent_preregistered_replication",
            "X4_cross_domain_replication",
        }:
            _require(
                prereg.get("status") in X3_PREREG_STATUSES,
                f"{claim_id} X3+ requires independent preregistration",
            )
            _require(
                dataset.get("independence") == "independent_team",
                f"{claim_id} X3+ requires an independent team",
            )
            _require(
                dataset.get("dataGeneration")
                == "new_independent_after_preregistration",
                f"{claim_id} X3+ requires newly collected independent observations",
            )
            _require(
                has_replication_receipt,
                f"{claim_id} X3+ requires a separate replicationReceipt",
            )
            _require(
                dataset["replicationReceipt"] != dataset["resultReceipt"],
                f"{claim_id} X3+ receipts must be distinct",
            )
            replication_receipt = _validate_result_receipt(
                root,
                claim_id,
                dataset.get("replicationReceipt"),
                prereg_path,
                "x3_replication",
                claim_rivals,
                variables,
                outcomes,
                True,
            )
            _require(
                dataset.get("replicationVerdict") == replication_receipt["outcome"],
                f"{claim_id} replicationVerdict must equal the X3 receipt outcome",
            )
            expected_token = (
                f"X2 outcome={result_receipt['outcome']}; "
                f"X3 outcome={replication_receipt['outcome']}"
            )
            _require(
                claim["currentVerdict"] == expected_token,
                f"{claim_id} currentVerdict must equal {expected_token}",
            )
            _require(
                replication_receipt.get("newIndependentObservations") is True,
                f"{claim_id} X3+ receipt must bind newly collected independent observations",
            )
            _require(
                result_receipt["dataArtifact"] != replication_receipt["dataArtifact"],
                f"{claim_id} X3+ requires a distinct new-data artifact",
            )
            _require(
                result_receipt["dataSha256"] != replication_receipt["dataSha256"],
                f"{claim_id} X3+ requires a distinct new-data hash",
            )
            all_commits = {
                result_receipt["freezeCommit"],
                result_receipt["analysisCommit"],
                replication_receipt["freezeCommit"],
                replication_receipt["analysisCommit"],
            }
            _require(
                len(all_commits) == 4,
                f"{claim_id} X3+ freeze/analysis commits must all be distinct",
            )
            _require_git_ancestor(
                root,
                result_receipt["analysisCommit"],
                replication_receipt["freezeCommit"],
                f"{claim_id} prior-X2/replication",
            )
            prior_receipt_path = _repository_file(
                root, dataset["resultReceipt"], f"{claim_id} prior X2 result receipt"
            )
            prior_receipt_hash = _sha256_file(
                prior_receipt_path, f"{claim_id} prior X2 result receipt"
            )
            committed_prior_receipt_hash = _git_blob_sha256(
                root,
                replication_receipt["freezeCommit"],
                dataset["resultReceipt"],
                f"{claim_id} prior X2 result receipt",
            )
            _require(
                committed_prior_receipt_hash == prior_receipt_hash,
                f"{claim_id} X3+ replication freeze does not bind the prior X2 result receipt",
            )
            _require(
                dt.date.fromisoformat(result_receipt["date"])
                <= dt.date.fromisoformat(replication_receipt["date"]),
                f"{claim_id} X3+ replication receipt predates the prior X2 result",
            )
            _require(
                set(result_receipt["teamIds"]).isdisjoint(
                    replication_receipt["teamIds"]
                ),
                f"{claim_id} X3+ replication team must be distinct from the X2 team",
            )
            teams = dataset.get("teams")
            _require(
                isinstance(teams, list) and bool(teams),
                f"{claim_id} X3+ requires named independent teams",
            )
            _require(
                set(teams) == set(replication_receipt["teamIds"]),
                f"{claim_id} dataset teams must match replication receipt",
            )
        if stage == "X4_cross_domain_replication":
            _require(
                isinstance(dataset.get("teams"), list)
                and len(set(dataset["teams"])) >= 2,
                f"{claim_id} X4 requires at least two independent teams",
            )
            _require(
                isinstance(dataset.get("domains"), list)
                and len(set(dataset["domains"])) >= 2,
                f"{claim_id} X4 requires at least two domains",
            )
            _require(
                set(dataset["domains"]) == set(replication_receipt["domains"]),
                f"{claim_id} dataset domains must match replication receipt",
            )
        if stage in {
            "X3_independent_preregistered_replication",
            "X4_cross_domain_replication",
        }:
            raise CalibrationError(
                f"{claim_id} X3+ is blocked: no externally controlled independence-attestation verifier is configured"
            )

    contract_records = []
    for claim in claims:
        record = {field: claim[field] for field in IMMUTABLE_CLAIM_FIELDS}
        record["preregistrationPath"] = claim["preregistration"]["path"]
        contract_records.append(record)
    contract_bytes = json.dumps(
        sorted(contract_records, key=lambda record: record["id"]),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    _require(
        hashlib.sha256(contract_bytes).hexdigest() == REQUIRED_CLAIM_CONTRACT_SHA256,
        "immutable claim contract drift",
    )
    return claim_ids


def _validate_whole_verdict(payload: dict[str, Any]) -> None:
    verdict = payload.get("wholeCompassVerdict")
    _require(isinstance(verdict, dict), "wholeCompassVerdict missing")
    _exact_keys(verdict, WHOLE_KEYS, "wholeCompassVerdict")
    _require(
        verdict.get("validated") is False,
        "whole Compass may not be marked validated by claim-level calibration",
    )
    _require(
        verdict.get("calibrationStage") == "not_assigned",
        "whole Compass calibration stage must remain unassigned",
    )
    _require(
        verdict.get("evidenceTier") == "I", "whole Compass evidence tier must remain I"
    )
    actual_stages = {
        claim.get("calibrationStage") for claim in payload.get("claims", [])
    }
    expected_profile = [
        stage for stage in COMPONENT_STAGE_ORDER if stage in actual_stages
    ]
    _require(
        verdict.get("componentStages") == expected_profile,
        "whole Compass componentStages must be the ordered profile derived from claim stages",
    )
    wording = str(verdict.get("wording", "")).lower()
    _require(
        "pending" in wording,
        "whole Compass verdict must name pending discrimination or replication",
    )
    _require(
        WHOLE_PROMOTION_RE.search(wording) is None,
        "whole Compass verdict cannot use validation, verification, proof, confirmation, establishment, or demonstration language",
    )


def _walk_strings(value: Any, label: str) -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield label, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_strings(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_strings(child, f"{label}[{index}]")


def _validate_no_whole_system_promotion(payload: dict[str, Any]) -> None:
    for index, claim in enumerate(payload.get("claims", [])):
        for label, text in _walk_strings(claim, f"claims[{index}]"):
            if WHOLE_SUBJECT_RE.search(text) and WHOLE_PROMOTION_RE.search(text):
                raise CalibrationError(
                    f"{label} cannot self-certify the whole Compass/framework"
                )


def _validate_registries(payload: dict[str, Any]) -> None:
    _require(
        set(payload.get("calibrationStages", [])) == ALLOWED_STAGES,
        "calibrationStages registry drift",
    )
    _require(
        set(payload.get("claimClasses", [])) == ALLOWED_CLASSES,
        "claimClasses registry drift",
    )
    _require(
        set(payload.get("sourceDistances", [])) == ALLOWED_DISTANCES,
        "sourceDistances registry drift",
    )


def _validate_source_negative_checks(payload: dict[str, Any], root: Path) -> None:
    checks = _nonempty_list(payload.get("sourceNegativeChecks"), "sourceNegativeChecks")
    _unique_ids(checks, "negative check")
    canonical = {
        check["id"]: {"pattern": check.get("pattern"), "paths": check.get("paths")}
        for check in checks
    }
    _require(
        canonical == REQUIRED_NEGATIVE_CHECKS, "sourceNegativeChecks registry drift"
    )
    for check in checks:
        _exact_keys(check, NEGATIVE_KEYS, check["id"])
        pattern = check.get("pattern")
        paths = check.get("paths")
        _require(isinstance(pattern, str) and pattern, f"{check['id']} missing pattern")
        _nonempty_list(paths, f"{check['id']}.paths")
        for relative in paths:
            _require(
                isinstance(relative, str) and relative,
                f"{check['id']} has invalid path",
            )
            path = _inside_root(root, relative, check["id"])
            _require(path.is_file(), f"{check['id']} path missing: {relative}")
            text = path.read_text(encoding="utf-8")
            _require(
                pattern.casefold() not in text.casefold(),
                f"{check['id']} forbidden wording found in {relative}: {pattern}",
            )


def validate_payload(payload: dict[str, Any], root: Path) -> tuple[int, int]:
    """Validate a decoded calibration payload and return source/claim counts."""

    _exact_keys(payload, TOP_LEVEL_KEYS, "calibration root")
    _require(payload.get("schemaVersion") == "1.0", "unsupported schemaVersion")
    _require(payload.get("title") == REQUIRED_TITLE, "calibration title drift")
    _require(
        payload.get("authorityBoundary") == REQUIRED_AUTHORITY_BOUNDARY,
        "authority boundary drift",
    )
    _validate_registries(payload)
    _validate_whole_verdict(payload)
    _validate_no_whole_system_promotion(payload)
    source_ids, independent_source_ids = _validate_sources(payload, root)
    claim_ids = _validate_claims(payload, source_ids, independent_source_ids, root)
    _validate_source_negative_checks(payload, root)
    return len(source_ids), len(claim_ids)


def load_payload(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CalibrationError(f"cannot read calibration JSON: {exc}") from exc
    _require(isinstance(value, dict), "calibration root must be an object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--json", type=Path, default=None, dest="json_path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    path = args.json_path.resolve() if args.json_path else root / DEFAULT_RELATIVE_PATH
    try:
        payload = load_payload(path)
        source_count, claim_count = validate_payload(payload, root)
    except CalibrationError as exc:
        print(f"CAL-ERROR: {exc}", file=sys.stderr)
        return 1
    profile = ",".join(payload["wholeCompassVerdict"]["componentStages"])
    print(
        f"CAL-OK sources={source_count} claims={claim_count} "
        f"whole=not_assigned component_stages={profile} source_scan=full validated=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Adversarial mutation tests for the external-calibration contract."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Callable

from validate_external_calibration import (
    CalibrationError,
    COMPONENT_STAGE_ORDER,
    build_parser,
    validate_payload,
)


ROOT = Path(__file__).resolve().parents[2]
CLAIMS_PATH = ROOT / "03_METHODOLOGY/00_EXTERNAL_CALIBRATION_CLAIMS.json"
X2_ARTIFACT_BYTES = b'{"row": 1, "source": "independent"}\n'
X3_ARTIFACT_BYTES = b'{"row": 2, "source": "new-independent"}\n'


def payload() -> dict:
    return json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))


def claim_by_id(data: dict, claim_id: str) -> dict:
    return next(claim for claim in data["claims"] if claim["id"] == claim_id)


def sync_component_profile(data: dict) -> None:
    stages = {claim["calibrationStage"] for claim in data["claims"]}
    data["wholeCompassVerdict"]["componentStages"] = [
        stage for stage in COMPONENT_STAGE_ORDER if stage in stages
    ]


def promote_to_x2(claim: dict) -> None:
    claim["calibrationStage"] = "X2_independent_data_discrimination"
    claim["evidenceTier"] = "B"
    claim["dataset"].update(
        {
            "status": "result_receipted",
            "independence": "external_source",
            "dataGeneration": "published_preexisting",
            "access": "published_preexisting_frozen_before_access",
        }
    )
    claim["preregistration"]["status"] = "frozen_before_access"


def promote_to_x3(claim: dict) -> None:
    claim["calibrationStage"] = "X3_independent_preregistered_replication"
    claim["evidenceTier"] = "A"
    claim["dataset"].update(
        {
            "status": "result_receipted",
            "independence": "independent_team",
            "dataGeneration": "new_independent_after_preregistration",
            "access": "new_independent_collection_after_preregistration",
            "teams": ["replication-team"],
            "domains": ["planning"],
        }
    )
    claim["preregistration"]["status"] = "independent_preregistered"


def materialize_contract_files(data: dict, root: Path) -> None:
    required_paths = {source["path"] for source in data["sources"] if "path" in source}
    required_paths |= {claim["preregistration"]["path"] for claim in data["claims"]}
    required_paths |= {
        path for check in data["sourceNegativeChecks"] for path in check["paths"]
    }
    for relative in required_paths:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("clean fixture\n", encoding="utf-8")


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def init_git(root: Path) -> None:
    run_git(root, "init", "-q")
    run_git(root, "config", "user.name", "Calibration Fixture")
    run_git(root, "config", "user.email", "calibration-fixture@example.invalid")


def commit_all(root: Path, message: str) -> str:
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", message)
    return run_git(root, "rev-parse", "HEAD")


def write_artifact(root: Path, claim_id: str, label: str, content: bytes) -> str:
    relative = f"03_METHODOLOGY/04_RESULTS/data/{claim_id}-{label}.jsonl"
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return relative


def read_json(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def write_json(root: Path, relative: str, value: dict) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_analysis_manifest(
    root: Path,
    claim: dict,
    *,
    kind: str,
    expected_data: bytes | None,
    relative: str | None = None,
) -> str:
    if relative is None:
        suffix = "x2" if kind == "x2_discriminator" else "x3"
        relative = f"03_METHODOLOGY/04_RESULTS/{claim['id']}-{suffix}-manifest.json"
    access_status = (
        "not_accessed_before_freeze"
        if kind == "x2_discriminator"
        else "not_collected_before_freeze"
    )
    tag = "x2" if kind == "x2_discriminator" else "x3"
    analysis_code = f"03_METHODOLOGY/04_RESULTS/support/{claim['id']}-{tag}-analysis.py"
    environment_lock = (
        f"03_METHODOLOGY/04_RESULTS/support/{claim['id']}-{tag}-environment.json"
    )
    access_log = f"03_METHODOLOGY/04_RESULTS/support/{claim['id']}-{tag}-access.log"
    code_path = root / analysis_code
    code_path.parent.mkdir(parents=True, exist_ok=True)
    code_path.write_text(
        "def score(candidate, rivals, rows):\n"
        "    return {'candidate': candidate, 'rivals': rivals, 'rows': len(rows)}\n",
        encoding="utf-8",
    )
    write_json(
        root,
        environment_lock,
        {
            "python": "3.12.4",
            "dependencies": {"standard-library": "3.12.4"},
            "platform": "fixture-linux-x86_64",
        },
    )
    access_path = root / access_log
    access_path.parent.mkdir(parents=True, exist_ok=True)
    access_path.write_text(
        "2026-07-18 custody opened; no outcome artifact accessed or collected\n",
        encoding="utf-8",
    )
    expected_hash = (
        hashlib.sha256(expected_data).hexdigest() if expected_data is not None else None
    )
    write_json(
        root,
        relative,
        {
            "schemaVersion": "2.0",
            "claimId": claim["id"],
            "datasetLocator": (
                f"artifact:sha256:{expected_hash}"
                if expected_hash is not None
                else "https://zenodo.org/records/123456/files/new-observations.jsonl"
            ),
            "datasetChecksum": {
                "mechanism": (
                    "repository_sha256"
                    if expected_hash is not None
                    else "compute_on_first_custody"
                ),
                "expectedSha256": expected_hash,
            },
            "candidateModel": {
                "name": f"Emergentist candidate {claim['id']}",
                "specification": "Predict every registered outcome from the frozen claim variables.",
                "fitProcedure": "Fit only on training folds and score held-out folds once.",
                "complexityPenalty": "Apply the same information-criterion penalty to every model.",
            },
            "rivals": [
                {
                    "name": rival,
                    "specification": f"Frozen operational specification for rival model {rival}.",
                    "fitProcedure": "Fit only on training folds and score held-out folds once.",
                    "complexityPenalty": "Apply the same information-criterion penalty to every model.",
                }
                for rival in claim["rivals"]
            ],
            "variables": [
                {
                    "name": variable,
                    "operationalDefinition": f"Registered measurement protocol for {variable}.",
                    "unit": "registered unit",
                }
                for variable in claim["variables"]
            ],
            "outcomes": [
                {
                    "name": outcome,
                    "operationalDefinition": f"Held-out registered measurement for {outcome}.",
                    "unit": "registered unit",
                    "primary": index == 0,
                    "decisionRule": "Compare held-out score with every rival under the frozen threshold.",
                }
                for index, outcome in enumerate(claim["outcomes"])
            ],
            "preprocessingSteps": [
                {
                    "id": "step-1",
                    "operation": "Validate the frozen record schema before model fitting.",
                    "parameters": {"on_invalid": "exclude_and_report"},
                },
                {
                    "id": "step-2",
                    "operation": "Standardize continuous predictors using training folds only.",
                    "parameters": {"center": True, "scale": True},
                },
            ],
            "exclusions": [
                {
                    "criterion": "Exclude records that fail the frozen input schema.",
                    "rationale": "Malformed records cannot instantiate the registered variables.",
                }
            ],
            "stoppingRule": {
                "kind": "fixed_sample",
                "target": 100,
                "unit": "observations",
                "interimLooks": 0,
            },
            "foldCount": 5,
            "randomSeeds": [1729, 2718, 31415],
            "analysisCode": {
                "path": analysis_code,
                "sha256": hashlib.sha256(code_path.read_bytes()).hexdigest(),
            },
            "environmentLock": {
                "path": environment_lock,
                "sha256": hashlib.sha256(
                    (root / environment_lock).read_bytes()
                ).hexdigest(),
            },
            "costPlan": {
                "budgets": [
                    {"category": "compute", "unit": "cpu hours", "maximum": 10},
                    {
                        "category": "data_acquisition",
                        "unit": "US dollars",
                        "maximum": 100,
                    },
                    {"category": "labor", "unit": "person hours", "maximum": 40},
                ],
                "scalarization": "none",
            },
            "accessAttestation": {
                "status": access_status,
                "attestedBy": "fixture-analysis-team",
                "attestedAt": "2026-07-18",
                "custodian": "fixture-data-custodian",
                "custodyProtocol": "Append-only access log controlled by the named custodian.",
                "accessLog": {
                    "path": access_log,
                    "sha256": hashlib.sha256(access_path.read_bytes()).hexdigest(),
                },
            },
        },
    )
    return relative


def write_result_receipt(
    root: Path,
    claim: dict,
    *,
    kind: str,
    artifact: str,
    manifest: str,
    freeze_commit: str,
    analysis_commit: str,
    outcome: str = "supported",
    rivals: list[str] | None = None,
    date: str = "2026-07-18",
    team_ids: list[str] | None = None,
    domains: list[str] | None = None,
    new_observations: bool = False,
    relative: str | None = None,
) -> str:
    if relative is None:
        suffix = "x2" if kind == "x2_discriminator" else "x3"
        relative = f"03_METHODOLOGY/04_RESULTS/{claim['id']}-{suffix}.json"
    artifact_hash = hashlib.sha256((root / artifact).read_bytes()).hexdigest()
    write_json(
        root,
        relative,
        {
            "schemaVersion": "2.1",
            "receiptKind": kind,
            "claimId": claim["id"],
            "dataArtifact": artifact,
            "dataSha256": artifact_hash,
            "preregSha256": hashlib.sha256(
                (root / claim["preregistration"]["path"]).read_bytes()
            ).hexdigest(),
            "analysisManifest": manifest,
            "analysisManifestSha256": hashlib.sha256(
                (root / manifest).read_bytes()
            ).hexdigest(),
            "analysisCommit": analysis_commit,
            "freezeCommit": freeze_commit,
            "outcome": outcome,
            "rivals": list(claim["rivals"] if rivals is None else rivals),
            "date": date,
            "teamIds": team_ids or ["x2-analysis-team"],
            "domains": domains or ["planning"],
            "newIndependentObservations": new_observations,
        },
    )
    return relative


def mutate_analysis_manifest(
    root: Path, receipt_relative: str, mutation: Callable[[dict], None]
) -> dict:
    receipt = read_json(root, receipt_relative)
    manifest = read_json(root, receipt["analysisManifest"])
    mutation(manifest)
    write_json(root, receipt["analysisManifest"], manifest)
    receipt["analysisManifestSha256"] = hashlib.sha256(
        (root / receipt["analysisManifest"]).read_bytes()
    ).hexdigest()
    write_json(root, receipt_relative, receipt)
    return manifest


def build_x2_fixture(data: dict, root: Path) -> tuple[dict, str, str, str]:
    claim = claim_by_id(data, "CAL-AGENCY-01")
    promote_to_x2(claim)
    sync_component_profile(data)
    materialize_contract_files(data, root)
    init_git(root)
    manifest = write_analysis_manifest(
        root, claim, kind="x2_discriminator", expected_data=X2_ARTIFACT_BYTES
    )
    freeze_commit = commit_all(root, "freeze discriminator")
    artifact = write_artifact(root, claim["id"], "x2", X2_ARTIFACT_BYTES)
    analysis_commit = commit_all(root, "bind x2 data artifact")
    receipt = write_result_receipt(
        root,
        claim,
        kind="x2_discriminator",
        artifact=artifact,
        manifest=manifest,
        freeze_commit=freeze_commit,
        analysis_commit=analysis_commit,
    )
    claim["dataset"]["resultReceipt"] = receipt
    claim["dataset"]["resultVerdict"] = "supported"
    claim["currentVerdict"] = "X2 outcome=supported"
    return claim, receipt, freeze_commit, analysis_commit


def build_x3_fixture(
    data: dict,
    root: Path,
    *,
    replication_content: bytes = X3_ARTIFACT_BYTES,
) -> tuple[dict, str, str]:
    claim, x2_receipt, _, _ = build_x2_fixture(data, root)
    promote_to_x3(claim)
    sync_component_profile(data)
    prereg_path = root / claim["preregistration"]["path"]
    prereg_path.write_text("independent replication freeze\n", encoding="utf-8")
    manifest = write_analysis_manifest(
        root, claim, kind="x3_replication", expected_data=None
    )
    replication_freeze = commit_all(root, "freeze independent replication")
    artifact = write_artifact(root, claim["id"], "x3", replication_content)
    replication_analysis = commit_all(root, "bind x3 replication data artifact")
    replication_receipt = write_result_receipt(
        root,
        claim,
        kind="x3_replication",
        artifact=artifact,
        manifest=manifest,
        freeze_commit=replication_freeze,
        analysis_commit=replication_analysis,
        team_ids=["replication-team"],
        new_observations=True,
    )
    claim["dataset"]["resultReceipt"] = x2_receipt
    claim["dataset"]["replicationReceipt"] = replication_receipt
    claim["dataset"]["resultVerdict"] = "supported"
    claim["dataset"]["replicationVerdict"] = "supported"
    claim["currentVerdict"] = "X2 outcome=supported; X3 outcome=supported"
    return claim, x2_receipt, replication_receipt


class ExternalCalibrationTests(unittest.TestCase):
    def assert_rejected(self, data: dict, fragment: str, *, root: Path = ROOT) -> None:
        with self.assertRaisesRegex(CalibrationError, fragment):
            validate_payload(data, root)

    def test_canonical_payload_passes(self) -> None:
        self.assertEqual(validate_payload(payload(), ROOT), (31, 12))

    def test_current_claims_remain_x0_x1_or_not_applicable(self) -> None:
        stages = {claim["calibrationStage"] for claim in payload()["claims"]}
        self.assertEqual(
            stages,
            {"X0_internal_only", "X1_construct_anchor", "not_applicable"},
        )

    def test_whole_compass_cannot_self_validate(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["validated"] = True
        self.assert_rejected(data, "whole Compass may not be marked validated")

    def test_whole_compass_cannot_receive_a_stage(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["calibrationStage"] = "X1_construct_anchor"
        self.assert_rejected(
            data, "whole Compass calibration stage must remain unassigned"
        )

    def test_whole_compass_tier_cannot_inflate(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["evidenceTier"] = "A"
        self.assert_rejected(data, "whole Compass evidence tier must remain I")

    def test_whole_component_profile_is_derived_and_ordered(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["componentStages"] = list(
            reversed(data["wholeCompassVerdict"]["componentStages"])
        )
        self.assert_rejected(data, "ordered profile derived from claim stages")

    def test_whole_verdict_schema_is_closed(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["proofStatus"] = "proven"
        self.assert_rejected(data, "wholeCompassVerdict unknown keys")

    def test_whole_verdict_rejects_proven_synonym(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["wording"] = (
            "The worldview is proven; replication remains pending."
        )
        self.assert_rejected(data, "cannot use validation, verification, proof")

    def test_whole_verdict_rejects_validation_complete_synonym(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["wording"] = (
            "External validation is complete; replication remains pending."
        )
        self.assert_rejected(data, "cannot use validation, verification, proof")

    def test_whole_verdict_rejects_certified_correct_synonym(self) -> None:
        data = payload()
        data["wholeCompassVerdict"]["wording"] = (
            "The worldview is certified correct; replication remains pending."
        )
        self.assert_rejected(data, "cannot use validation, verification, proof")

    def test_whole_verdict_rejects_calibrated_supported_and_substantiated(self) -> None:
        attacks = (
            "The whole Compass is externally calibrated; replication remains pending.",
            "The whole Compass is fully supported; replication remains pending.",
            "The whole Compass is scientifically substantiated; replication remains pending.",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                data = payload()
                data["wholeCompassVerdict"]["wording"] = attack
                self.assert_rejected(data, "cannot use validation, verification, proof")

    def test_authority_boundary_cannot_hide_whole_proof_claim(self) -> None:
        data = payload()
        data["authorityBoundary"] = (
            "This file cannot create doctrine. The whole Compass is proven."
        )
        self.assert_rejected(data, "authority boundary drift")

    def test_claim_cannot_hide_whole_system_promotion(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["scopeBoundary"] = (
            "The Compass as a whole has been verified."
        )
        self.assert_rejected(data, "cannot self-certify the whole Compass/framework")

    def test_duplicate_claim_id_fails(self) -> None:
        data = payload()
        data["claims"].append(copy.deepcopy(data["claims"][0]))
        self.assert_rejected(data, "duplicate claim id")

    def test_same_count_claim_substitution_fails(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-MU-01")["id"] = "CAL-BOGUS"
        self.assert_rejected(data, "claim registry drift")

    def test_same_id_claim_semantic_substitution_fails(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["compassClaim"] = "The Moon is cheese."
        self.assert_rejected(data, "immutable claim contract drift")

    def test_claim_contract_lists_require_text_elements(self) -> None:
        for field in ("variables", "outcomes", "killCriteria"):
            with self.subTest(field=field):
                data = payload()
                claim_by_id(data, "CAL-AGENCY-01")[field] = [{}]
                self.assert_rejected(data, rf"{field} must contain text")

    def test_unknown_source_fails(self) -> None:
        data = payload()
        data["claims"][0]["sourceIds"].append("SRC-NOT-REAL")
        self.assert_rejected(data, "references unknown sources")

    def test_same_count_source_substitution_fails(self) -> None:
        data = payload()
        data["sources"][0]["id"] = "SRC-SUBSTITUTE"
        self.assert_rejected(data, "source registry drift")

    def test_source_metadata_substitution_fails(self) -> None:
        data = payload()
        data["sources"][0]["citation"] = "A different paper with the same id"
        self.assert_rejected(data, "source registry content drift")

    def test_external_source_requires_https(self) -> None:
        data = payload()
        data["sources"][0]["url"] = "http://example.invalid/paper"
        self.assert_rejected(data, "URL must use https")

    def test_external_source_requires_meaningful_hostname(self) -> None:
        data = payload()
        data["sources"][0]["url"] = "https:///paper"
        self.assert_rejected(data, "URL must include a hostname")

    def test_external_source_rejects_placeholder_hostname(self) -> None:
        data = payload()
        data["sources"][0]["url"] = "https://paper.invalid/study"
        self.assert_rejected(data, "reserved placeholder hostname")

    def test_external_source_rejects_embedded_credentials(self) -> None:
        data = payload()
        data["sources"][0]["url"] = "https://user:password@doi.org/10.1/test"
        self.assert_rejected(data, "may not embed credentials")

    def test_empirical_claim_requires_named_rivals(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["rivals"] = []
        self.assert_rejected(data, "rivals must be a nonempty list")

    def test_claim_rivals_must_be_unique(self) -> None:
        data = payload()
        claim = claim_by_id(data, "CAL-AGENCY-01")
        claim["rivals"].append(claim["rivals"][0])
        self.assert_rejected(data, "rivals must be unique")

    def test_normative_claim_cannot_take_empirical_stage(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-SYNTROPY-01")["calibrationStage"] = "X1_construct_anchor"
        sync_component_profile(data)
        self.assert_rejected(
            data, "non-empirical class cannot receive empirical calibration stage"
        )

    def test_x0_claim_cannot_claim_a_evidence(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-SPHERE-01")["evidenceTier"] = "A"
        self.assert_rejected(data, "cannot claim A before X3")

    def test_claim_level_validated_flag_is_rejected(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["validated"] = True
        self.assert_rejected(data, "unknown keys")

    def test_x1_requires_independent_external_source(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["sourceIds"] = ["SRC-COMPASS"]
        self.assert_rejected(data, "X1 requires an independent external source")

    def test_result_receipted_status_requires_receipt(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["dataset"]["status"] = "result_receipted"
        self.assert_rejected(data, "result_receipted status requires resultReceipt")

    def test_result_receipt_requires_result_receipted_status(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-AGENCY-01")["dataset"]["resultReceipt"] = "fake.json"
        self.assert_rejected(data, "resultReceipt requires result_receipted status")

    def test_x0_cannot_carry_result_receipted_status(self) -> None:
        data = payload()
        claim = claim_by_id(data, "CAL-SPHERE-01")
        claim["dataset"]["status"] = "result_receipted"
        self.assert_rejected(data, "result_receipted status requires resultReceipt")

    def test_replication_receipt_requires_prior_result_receipt(self) -> None:
        data = payload()
        claim = claim_by_id(data, "CAL-AGENCY-01")
        claim["dataset"].update(
            {"status": "result_receipted", "replicationReceipt": "replication.json"}
        )
        self.assert_rejected(data, "result_receipted status requires resultReceipt")

    def test_x2_requires_result_receipted_status(self) -> None:
        data = payload()
        claim = claim_by_id(data, "CAL-AGENCY-01")
        promote_to_x2(claim)
        claim["dataset"]["status"] = "analyzed_independent"
        claim["dataset"].pop("resultReceipt", None)
        sync_component_profile(data)
        self.assert_rejected(data, r"X2\+ requires analyzed independent data")

    def test_x2_requires_independent_dataset_provenance(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["dataset"]["independence"] = "external_source_required"
            self.assert_rejected(
                data, r"X2\+ requires independent data provenance", root=root
            )

    def test_x2_requires_frozen_discriminator(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["preregistration"]["status"] = "prospective_protocol"
            self.assert_rejected(
                data, r"X2\+ requires a frozen discriminator", root=root
            )

    def test_x2_rejects_post_hoc_preregistration_edit(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            (root / claim["preregistration"]["path"]).write_text(
                "POST HOC CHANGED PREDICTIONS\n", encoding="utf-8"
            )
            self.assert_rejected(
                data,
                "current preregistration differs from the frozen preregistration",
                root=root,
            )

    def test_x2_rejects_inflated_universal_proof_verdict(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["currentVerdict"] = (
                "Confirmed universal law and decisively proves nature."
            )
            self.assert_rejected(
                data, "currentVerdict must equal X2 outcome=supported", root=root
            )

    def test_x2_rejects_post_access_protocol_declaration(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["dataset"]["access"] = (
                "authors inspected all outcomes before writing protocol"
            )
            self.assert_rejected(data, "invalid frozen-access declaration", root=root)

    def test_x2_cannot_reuse_preregistration_as_result_receipt(self) -> None:
        data = payload()
        claim = claim_by_id(data, "CAL-AGENCY-01")
        promote_to_x2(claim)
        claim["dataset"]["resultReceipt"] = claim["preregistration"]["path"]
        sync_component_profile(data)
        self.assert_rejected(
            data, "result receipt must be distinct from preregistration"
        )

    def test_typed_x2_result_receipt_passes(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build_x2_fixture(data, root)
            self.assertEqual(validate_payload(data, root), (31, 12))

    def test_x2_rejects_suffix_prose_after_canonical_outcome_token(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["currentVerdict"] = (
                "X2 outcome=supported. The Compass edge was supported on the frozen independent dataset."
            )
            self.assert_rejected(
                data,
                "currentVerdict must equal X2 outcome=supported",
                root=root,
            )

    def test_x2_requires_claim_specific_manifest(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt.pop("analysisManifest")
            receipt.pop("analysisManifestSha256")
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "resultReceipt missing keys", root=root)

    def test_x2_manifest_rejects_one_character_and_vacuous_prose(self) -> None:
        attacks = (
            (
                "one-character",
                lambda manifest: manifest["candidateModel"].update(
                    {"specification": "x"}
                ),
            ),
            (
                "placeholder",
                lambda manifest: manifest["preprocessingSteps"][0].update(
                    {"operation": "TBD"}
                ),
            ),
        )
        for label, mutation in attacks:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)
                mutate_analysis_manifest(root, receipt_path, mutation)
                self.assert_rejected(data, "must be substantive", root=root)

    def test_x2_manifest_rejects_empty_required_protocol_lists(self) -> None:
        attacks = (
            (
                "preprocessingSteps",
                lambda manifest: manifest.update({"preprocessingSteps": []}),
            ),
            ("exclusions", lambda manifest: manifest.update({"exclusions": []})),
            ("randomSeeds", lambda manifest: manifest.update({"randomSeeds": []})),
        )
        for field, mutation in attacks:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)
                mutate_analysis_manifest(root, receipt_path, mutation)
                self.assert_rejected(data, "must be a nonempty list", root=root)

    def test_x2_manifest_requires_immutable_locator_and_expected_checksum(self) -> None:
        attacks = (
            (
                "mutable-locator",
                lambda manifest: manifest.update(
                    {"datasetLocator": "local-folder/latest-data.csv"}
                ),
                "must be HTTPS or an immutable",
            ),
            (
                "missing-expected-hash",
                lambda manifest: manifest["datasetChecksum"].update(
                    {"expectedSha256": None}
                ),
                "needs an expected SHA-256",
            ),
        )
        for label, mutation, error in attacks:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)
                mutate_analysis_manifest(root, receipt_path, mutation)
                self.assert_rejected(data, error, root=root)

    def test_x2_manifest_rejects_nonexistent_code_and_environment_files(self) -> None:
        attacks = (
            ("analysisCode", "missing-analysis.py"),
            ("environmentLock", "missing-environment.json"),
        )
        for field, name in attacks:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)

                def mutation(manifest: dict) -> None:
                    manifest[field]["path"] = (
                        f"03_METHODOLOGY/04_RESULTS/support/{name}"
                    )

                mutate_analysis_manifest(root, receipt_path, mutation)
                self.assert_rejected(data, "path must be an existing file", root=root)

    def test_x2_manifest_rejects_code_and_environment_hash_mismatch(self) -> None:
        for field in ("analysisCode", "environmentLock"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)
                mutate_analysis_manifest(
                    root,
                    receipt_path,
                    lambda manifest, field=field: manifest[field].update(
                        {"sha256": "f" * 64}
                    ),
                )
                self.assert_rejected(
                    data, "sha256 does not match the local file", root=root
                )

    def test_x2_manifest_rejects_wrong_folds_and_stopping_rules(self) -> None:
        attacks = (
            (
                "fold-low",
                lambda manifest: manifest.update({"foldCount": 1}),
                "foldCount",
            ),
            (
                "fold-high",
                lambda manifest: manifest.update({"foldCount": 21}),
                "foldCount",
            ),
            (
                "post-hoc-stop",
                lambda manifest: manifest["stoppingRule"].update(
                    {"kind": "stop_when_supported"}
                ),
                "stoppingRule kind",
            ),
            (
                "zero-target",
                lambda manifest: manifest["stoppingRule"].update({"target": 0}),
                "stoppingRule target",
            ),
        )
        for label, mutation, error in attacks:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                _, receipt_path, _, _ = build_x2_fixture(data, root)
                mutate_analysis_manifest(root, receipt_path, mutation)
                self.assert_rejected(data, error, root=root)

    def test_x2_manifest_dependencies_must_exist_at_freeze(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim = claim_by_id(data, "CAL-AGENCY-01")
            promote_to_x2(claim)
            sync_component_profile(data)
            materialize_contract_files(data, root)
            init_git(root)
            manifest = write_analysis_manifest(
                root,
                claim,
                kind="x2_discriminator",
                expected_data=X2_ARTIFACT_BYTES,
            )
            manifest_record = read_json(root, manifest)
            code_path = root / manifest_record["analysisCode"]["path"]
            code_bytes = code_path.read_bytes()
            code_path.unlink()
            freeze = commit_all(root, "invalid freeze without analysis code")
            code_path.write_bytes(code_bytes)
            artifact = write_artifact(root, claim["id"], "x2", X2_ARTIFACT_BYTES)
            analysis = commit_all(root, "bind late analysis code and data")
            receipt = write_result_receipt(
                root,
                claim,
                kind="x2_discriminator",
                artifact=artifact,
                manifest=manifest,
                freeze_commit=freeze,
                analysis_commit=analysis,
            )
            claim["dataset"]["resultReceipt"] = receipt
            claim["dataset"]["resultVerdict"] = "supported"
            claim["currentVerdict"] = "X2 outcome=supported"
            self.assert_rejected(
                data,
                "frozen manifest dependency.*is not present",
                root=root,
            )

    def test_x2_analysis_commit_must_retain_every_frozen_protocol_binding(self) -> None:
        bindings = (
            "preregistration",
            "analysisManifest",
            "analysisCode",
            "environmentLock",
            "accessLog",
        )
        for binding in bindings:
            with self.subTest(binding=binding), tempfile.TemporaryDirectory() as temp:
                data = payload()
                root = Path(temp)
                claim = claim_by_id(data, "CAL-AGENCY-01")
                promote_to_x2(claim)
                sync_component_profile(data)
                materialize_contract_files(data, root)
                init_git(root)
                manifest = write_analysis_manifest(
                    root,
                    claim,
                    kind="x2_discriminator",
                    expected_data=X2_ARTIFACT_BYTES,
                )
                manifest_record = read_json(root, manifest)
                relative = {
                    "preregistration": claim["preregistration"]["path"],
                    "analysisManifest": manifest,
                    "analysisCode": manifest_record["analysisCode"]["path"],
                    "environmentLock": manifest_record["environmentLock"]["path"],
                    "accessLog": manifest_record["accessAttestation"]["accessLog"][
                        "path"
                    ],
                }[binding]
                target = root / relative
                frozen_bytes = target.read_bytes()
                freeze = commit_all(root, f"freeze protocol before {binding} drift")
                target.write_bytes(frozen_bytes + b"\n")
                artifact = write_artifact(
                    root, claim["id"], "x2", X2_ARTIFACT_BYTES
                )
                analysis = commit_all(root, f"analysis with altered {binding}")
                target.write_bytes(frozen_bytes)
                receipt = write_result_receipt(
                    root,
                    claim,
                    kind="x2_discriminator",
                    artifact=artifact,
                    manifest=manifest,
                    freeze_commit=freeze,
                    analysis_commit=analysis,
                )
                claim["dataset"]["resultReceipt"] = receipt
                claim["dataset"]["resultVerdict"] = "supported"
                claim["currentVerdict"] = "X2 outcome=supported"
                self.assert_rejected(
                    data,
                    "analysisCommit does not retain.*at its frozen hash",
                    root=root,
                )

    def test_x2_frozen_expected_dataset_hash_must_match_acquired_bytes(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim = claim_by_id(data, "CAL-AGENCY-01")
            promote_to_x2(claim)
            sync_component_profile(data)
            materialize_contract_files(data, root)
            init_git(root)
            manifest = write_analysis_manifest(
                root,
                claim,
                kind="x2_discriminator",
                expected_data=b"publisher-declared-but-wrong-bytes\n",
            )
            freeze = commit_all(root, "freeze incorrect publisher checksum")
            artifact = write_artifact(root, claim["id"], "x2", X2_ARTIFACT_BYTES)
            analysis = commit_all(root, "bind differently hashed data")
            receipt = write_result_receipt(
                root,
                claim,
                kind="x2_discriminator",
                artifact=artifact,
                manifest=manifest,
                freeze_commit=freeze,
                analysis_commit=analysis,
            )
            claim["dataset"]["resultReceipt"] = receipt
            claim["dataset"]["resultVerdict"] = "supported"
            claim["currentVerdict"] = "X2 outcome=supported"
            self.assert_rejected(
                data,
                "dataSha256 does not match the frozen expected dataset hash",
                root=root,
            )

    def test_x2_rejects_manifest_not_bound_at_freeze(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, analysis_commit = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            late = "03_METHODOLOGY/04_RESULTS/late-manifest.json"
            write_json(root, late, read_json(root, receipt["analysisManifest"]))
            receipt["analysisManifest"] = late
            receipt["analysisManifestSha256"] = hashlib.sha256(
                (root / late).read_bytes()
            ).hexdigest()
            receipt["analysisCommit"] = analysis_commit
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "analysisManifest is not present at commit", root=root
            )

    def test_x2_rejects_data_already_present_at_freeze(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim = claim_by_id(data, "CAL-AGENCY-01")
            promote_to_x2(claim)
            sync_component_profile(data)
            materialize_contract_files(data, root)
            init_git(root)
            known_data = b"known outcome\n"
            manifest = write_analysis_manifest(
                root,
                claim,
                kind="x2_discriminator",
                expected_data=known_data,
            )
            artifact = write_artifact(root, claim["id"], "prefreeze", known_data)
            freeze = commit_all(root, "invalid freeze with data")
            (root / "analysis-marker.txt").write_text("analysis\n", encoding="utf-8")
            analysis = commit_all(root, "later analysis marker")
            receipt = write_result_receipt(
                root,
                claim,
                kind="x2_discriminator",
                artifact=artifact,
                manifest=manifest,
                freeze_commit=freeze,
                analysis_commit=analysis,
            )
            claim["dataset"]["resultReceipt"] = receipt
            claim["dataset"]["resultVerdict"] = "supported"
            claim["currentVerdict"] = "X2 outcome=supported"
            self.assert_rejected(
                data, "already existed at the freeze commit", root=root
            )

    def test_x2_cannot_carry_unused_replication_receipt(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, receipt_path, _, _ = build_x2_fixture(data, root)
            claim["dataset"]["replicationReceipt"] = receipt_path
            self.assert_rejected(data, "X2 cannot carry replicationReceipt", root=root)

    def test_x2_rejects_nonexistent_data_artifact(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["dataArtifact"] = "03_METHODOLOGY/04_RESULTS/data/missing.jsonl"
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "dataArtifact must be an existing local file", root=root
            )

    def test_x2_rejects_fake_data_hash(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["dataSha256"] = "f" * 64
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "dataSha256 does not match", root=root)

    def test_x2_rejects_disclosed_prefreeze_packet_path(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            artifact = (
                "11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form/"
                "copied-result.json"
            )
            path = root / artifact
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("copied after freeze\n", encoding="utf-8")
            analysis = commit_all(root, "attempt path laundering")
            receipt["dataArtifact"] = artifact
            receipt["dataSha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            receipt["analysisCommit"] = analysis
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "cannot promote a disclosed pre-freeze packet path", root=root
            )

    def test_x2_rejects_disclosed_prefreeze_packet_hash_after_copy(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            source = ROOT / (
                "11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form/"
                "data/Produc.csv"
            )
            artifact = "03_METHODOLOGY/04_RESULTS/data/copied-known-data.csv"
            path = root / artifact
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(source.read_bytes())
            analysis = commit_all(root, "attempt hash laundering")
            receipt["dataArtifact"] = artifact
            receipt["dataSha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            receipt["analysisCommit"] = analysis
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "cannot promote a disclosed pre-freeze packet hash", root=root
            )

    def test_x2_rejects_fake_full_length_commit(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["analysisCommit"] = "f" * 40
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "does not identify an existing Git commit", root=root
            )

    def test_x2_rejects_same_freeze_and_analysis_commit(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, freeze_commit, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["analysisCommit"] = freeze_commit
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "freeze/analysis commits must be distinct", root=root
            )

    def test_x2_rejects_reversed_commit_order(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, freeze_commit, analysis_commit = build_x2_fixture(
                data, root
            )
            receipt = read_json(root, receipt_path)
            receipt["freezeCommit"] = analysis_commit
            receipt["analysisCommit"] = freeze_commit
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "commits are not ordered by ancestry", root=root)

    def test_x2_analysis_commit_must_bind_artifact(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, receipt_path, freeze_commit, analysis_commit = build_x2_fixture(
                data, root
            )
            artifact = write_artifact(
                root, claim["id"], "uncommitted", b"uncommitted\n"
            )
            receipt = read_json(root, receipt_path)
            receipt["dataArtifact"] = artifact
            receipt["dataSha256"] = hashlib.sha256(
                (root / artifact).read_bytes()
            ).hexdigest()
            receipt["freezeCommit"] = freeze_commit
            receipt["analysisCommit"] = analysis_commit
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "not present as a data artifact at commit", root=root
            )

    def test_x2_rejects_impossible_calendar_date(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["date"] = "2026-02-30"
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "needs a real ISO date", root=root)

    def test_x2_receipt_rivals_must_match_claim(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["rivals"] = ["registered-rival"]
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "rivals must match the claim rivals", root=root)

    def test_x2_stage_records_rigor_independent_of_outcome_sign(self) -> None:
        for outcome in ("supported", "failed", "null", "mixed"):
            with self.subTest(outcome=outcome):
                data = payload()
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    _, receipt_path, _, _ = build_x2_fixture(data, root)
                    receipt = read_json(root, receipt_path)
                    receipt["outcome"] = outcome
                    write_json(root, receipt_path, receipt)
                    claim = claim_by_id(data, "CAL-AGENCY-01")
                    claim["dataset"]["resultVerdict"] = outcome
                    claim["currentVerdict"] = f"X2 outcome={outcome}"
                    self.assertEqual(validate_payload(data, root), (31, 12))

    def test_x2_result_verdict_must_equal_receipt_for_every_outcome_sign(self) -> None:
        outcomes = ("supported", "failed", "null", "mixed")
        for index, outcome in enumerate(outcomes):
            with self.subTest(outcome=outcome):
                data = payload()
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    claim, receipt_path, _, _ = build_x2_fixture(data, root)
                    receipt = read_json(root, receipt_path)
                    receipt["outcome"] = outcome
                    write_json(root, receipt_path, receipt)
                    wrong = outcomes[(index + 1) % len(outcomes)]
                    claim["dataset"]["resultVerdict"] = wrong
                    claim["currentVerdict"] = f"X2 outcome={wrong}"
                    self.assert_rejected(
                        data,
                        "resultVerdict must equal the X2 receipt outcome",
                        root=root,
                    )

    def test_x2_public_verdict_cannot_reverse_failed_receipt(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["outcome"] = "failed"
            write_json(root, receipt_path, receipt)
            claim["dataset"]["resultVerdict"] = "failed"
            claim["currentVerdict"] = "X2 outcome=supported"
            self.assert_rejected(
                data, "currentVerdict must equal X2 outcome=failed", root=root
            )

    def test_x2_rejects_exact_contradictory_prefix_mutant(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["outcome"] = "failed"
            write_json(root, receipt_path, receipt)
            claim["dataset"]["resultVerdict"] = "failed"
            claim["currentVerdict"] = (
                "X2 outcome=failed. X2 outcome=supported; the candidate won."
            )
            self.assert_rejected(
                data, "currentVerdict must equal X2 outcome=failed", root=root
            )

    def test_x2_receipt_kind_must_be_discriminator(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["receiptKind"] = "x3_replication"
            write_json(root, receipt_path, receipt)
            self.assert_rejected(data, "must be x2_discriminator", root=root)

    def test_x3_requires_separate_replication_receipt(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            promote_to_x3(claim)
            sync_component_profile(data)
            self.assert_rejected(
                data, r"X3\+ requires a separate replicationReceipt", root=root
            )

    def test_x3_cannot_reuse_x2_receipt_with_new_observation_boolean(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["newIndependentObservations"] = True
            write_json(root, receipt_path, receipt)
            promote_to_x3(claim)
            claim["dataset"]["replicationReceipt"] = receipt_path
            sync_component_profile(data)
            self.assert_rejected(data, r"X3\+ receipts must be distinct", root=root)

    def test_x3_requires_new_observations_in_replication_receipt(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, replication_path = build_x3_fixture(data, root)
            receipt = read_json(root, replication_path)
            receipt["newIndependentObservations"] = False
            write_json(root, replication_path, receipt)
            self.assert_rejected(
                data, "must bind newly collected independent observations", root=root
            )

    def test_x3_rejects_reusing_data_present_at_replication_freeze(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, x2_path, replication_path = build_x3_fixture(data, root)
            x2_receipt = read_json(root, x2_path)
            replication = read_json(root, replication_path)
            replication["dataArtifact"] = x2_receipt["dataArtifact"]
            replication["dataSha256"] = x2_receipt["dataSha256"]
            write_json(root, replication_path, replication)
            self.assert_rejected(
                data, "dataArtifact already existed at the freeze commit", root=root
            )

    def test_x3_requires_distinct_new_data_hash(self) -> None:
        data = payload()
        same_bytes = b'{"row": 1, "source": "independent"}\n'
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build_x3_fixture(data, root, replication_content=same_bytes)
            self.assert_rejected(
                data, r"X3\+ requires a distinct new-data hash", root=root
            )

    def test_x3_requires_distinct_commit_chain(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, x2_path, replication_path = build_x3_fixture(data, root)
            x2_receipt = read_json(root, x2_path)
            replication = read_json(root, replication_path)
            x2_receipt["analysisCommit"] = replication["freezeCommit"]
            write_json(root, x2_path, x2_receipt)
            self.assert_rejected(
                data,
                r"analysisCommit does not retain|X3\+ freeze/analysis commits must all be distinct",
                root=root,
            )

    def test_x3_freeze_must_already_bind_prior_x2_receipt(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, x2_path, _ = build_x3_fixture(data, root)
            late_copy = "03_METHODOLOGY/04_RESULTS/CAL-AGENCY-01-late-x2.json"
            write_json(root, late_copy, read_json(root, x2_path))
            claim["dataset"]["resultReceipt"] = late_copy
            self.assert_rejected(
                data,
                "prior X2 result receipt is not present as a data artifact at commit",
                root=root,
            )

    def test_x3_replication_team_must_differ_from_x2_team(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, replication_path = build_x3_fixture(data, root)
            replication = read_json(root, replication_path)
            replication["teamIds"] = ["x2-analysis-team"]
            write_json(root, replication_path, replication)
            self.assert_rejected(
                data, "replication team must be distinct from the X2 team", root=root
            )

    def test_x3_rejects_suffix_prose_after_canonical_outcome_token(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _ = build_x3_fixture(data, root)
            claim["currentVerdict"] = (
                "X2 outcome=supported; X3 outcome=supported. Replication won."
            )
            self.assert_rejected(
                data,
                "currentVerdict must equal X2 outcome=supported; X3 outcome=supported",
                root=root,
            )

    def test_complete_x3_still_requires_external_independence_gate(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build_x3_fixture(data, root)
            self.assert_rejected(
                data,
                "no externally controlled independence-attestation verifier is configured",
                root=root,
            )

    def test_self_authored_independence_attestation_field_is_rejected(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _ = build_x3_fixture(data, root)
            claim["dataset"]["independenceAttestation"] = {"verified": True}
            self.assert_rejected(data, "dataset unknown keys", root=root)

    def test_source_negative_registry_is_not_self_revocable(self) -> None:
        data = payload()
        data["sourceNegativeChecks"].pop()
        self.assert_rejected(data, "sourceNegativeChecks registry drift")

    def test_source_negative_scan_fires(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            materialize_contract_files(data, root)
            target = root / data["sourceNegativeChecks"][0]["paths"][0]
            target.write_text(
                data["sourceNegativeChecks"][0]["pattern"], encoding="utf-8"
            )
            self.assert_rejected(data, "forbidden wording found", root=root)

    def test_internal_source_path_cannot_escape_root(self) -> None:
        data = payload()
        source = next(item for item in data["sources"] if item["id"] == "SRC-COMPASS")
        source["path"] = "../outside.md"
        self.assert_rejected(data, "escapes repository root")

    def test_cli_has_no_source_scan_bypass(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build_parser().parse_args(["--no-source-scan"])

    def test_correspondence_has_no_empirical_stage(self) -> None:
        data = payload()
        claim_by_id(data, "CAL-CORRESPONDENCE-01")["calibrationStage"] = (
            "X1_construct_anchor"
        )
        sync_component_profile(data)
        self.assert_rejected(
            data, "non-empirical class cannot receive empirical calibration stage"
        )


if __name__ == "__main__":
    unittest.main()

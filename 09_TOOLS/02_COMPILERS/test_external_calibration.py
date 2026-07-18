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

from validate_external_calibration import (
    CalibrationError,
    COMPONENT_STAGE_ORDER,
    build_parser,
    validate_payload,
)


ROOT = Path(__file__).resolve().parents[2]
CLAIMS_PATH = ROOT / "03_METHODOLOGY/00_EXTERNAL_CALIBRATION_CLAIMS.json"


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


def write_result_receipt(
    root: Path,
    claim: dict,
    *,
    kind: str,
    artifact: str,
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
            "schemaVersion": "2.0",
            "receiptKind": kind,
            "claimId": claim["id"],
            "dataArtifact": artifact,
            "dataSha256": artifact_hash,
            "preregSha256": hashlib.sha256(
                (root / claim["preregistration"]["path"]).read_bytes()
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


def build_x2_fixture(data: dict, root: Path) -> tuple[dict, str, str, str]:
    claim = claim_by_id(data, "CAL-AGENCY-01")
    promote_to_x2(claim)
    sync_component_profile(data)
    materialize_contract_files(data, root)
    init_git(root)
    freeze_commit = commit_all(root, "freeze discriminator")
    artifact = write_artifact(
        root, claim["id"], "x2", b'{"row": 1, "source": "independent"}\n'
    )
    analysis_commit = commit_all(root, "bind x2 data artifact")
    receipt = write_result_receipt(
        root,
        claim,
        kind="x2_discriminator",
        artifact=artifact,
        freeze_commit=freeze_commit,
        analysis_commit=analysis_commit,
    )
    claim["dataset"]["resultReceipt"] = receipt
    return claim, receipt, freeze_commit, analysis_commit


def build_x3_fixture(
    data: dict,
    root: Path,
    *,
    replication_content: bytes = b'{"row": 2, "source": "new-independent"}\n',
) -> tuple[dict, str, str]:
    claim, x2_receipt, _, _ = build_x2_fixture(data, root)
    promote_to_x3(claim)
    sync_component_profile(data)
    prereg_path = root / claim["preregistration"]["path"]
    prereg_path.write_text("independent replication freeze\n", encoding="utf-8")
    replication_freeze = commit_all(root, "freeze independent replication")
    artifact = write_artifact(root, claim["id"], "x3", replication_content)
    replication_analysis = commit_all(root, "bind x3 replication data artifact")
    replication_receipt = write_result_receipt(
        root,
        claim,
        kind="x3_replication",
        artifact=artifact,
        freeze_commit=replication_freeze,
        analysis_commit=replication_analysis,
        team_ids=["replication-team"],
        new_observations=True,
    )
    claim["dataset"]["resultReceipt"] = x2_receipt
    claim["dataset"]["replicationReceipt"] = replication_receipt
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
                data, "X2 verdict cannot claim proof, confirmation", root=root
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

    def test_x2_can_report_bounded_component_support(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claim, _, _, _ = build_x2_fixture(data, root)
            claim["currentVerdict"] = (
                "The Compass edge was supported on the frozen independent dataset."
            )
            self.assertEqual(validate_payload(data, root), (31, 12))

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

    def test_x2_failed_outcome_cannot_promote(self) -> None:
        data = payload()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, receipt_path, _, _ = build_x2_fixture(data, root)
            receipt = read_json(root, receipt_path)
            receipt["outcome"] = "failed"
            write_json(root, receipt_path, receipt)
            self.assert_rejected(
                data, "requires a successful supported discriminator outcome", root=root
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

    def test_x3_requires_distinct_data_artifact(self) -> None:
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
                data, r"X3\+ requires a distinct new-data artifact", root=root
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
                data, r"X3\+ freeze/analysis commits must all be distinct", root=root
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

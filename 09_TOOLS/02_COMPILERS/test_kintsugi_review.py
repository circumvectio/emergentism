from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


COMPILER = Path(__file__).resolve().parent
ROOT = COMPILER.parents[1]
sys.path.insert(0, str(COMPILER))

from kintsugi_kernel import codec, markdown, schema as schema_module  # noqa: E402
from kintsugi_kernel import review  # noqa: E402
from kintsugi_kernel.diagnostics import KintsugiError  # noqa: E402
from kintsugi_kernel.records import attempt_paths  # noqa: E402
import kintsugi_test_support as support  # noqa: E402


SCHEMA = json.loads(
    (ROOT / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json").read_text(
        encoding="utf-8"
    )
)


def issue_codes(issues):
    return [issue.code for issue in issues]


def review_core(*, attempt_id="RVA-A-001"):
    core = support.build_semantic_core(bootstrap=False)
    manifest = core["manifests"][0]
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])
    paths = list(attempt_paths(attempt_id))
    manifest["closureOnlyPaths"] = paths
    manifest["allowedChangePaths"] = sorted(
        set(manifest["allowedChangePaths"]) | set(paths)
    )
    receipt = core["phaseReceipts"][0]
    receipt["reviewAttemptId"] = attempt_id
    attempt = {
        "id": attempt_id,
        "phase": "A",
        "receiptId": receipt["id"],
        "supersedesAttemptId": None,
        "reviewSubjectDigest": None,
        "reviewTargetPath": paths[0],
        "logicReviewPath": paths[1],
        "btjReviewPath": paths[2],
        "validationBundlePath": paths[3],
        "logicAttestationId": None,
        "btjAttestationId": None,
        "status": "PENDING",
        "abandonReason": None,
    }
    artifact = {
        "attemptId": attempt_id,
        "reviewTargetSha256": None,
        "logicReviewSha256": None,
        "btjReviewSha256": None,
    }
    core["reviewAttempts"] = [attempt]
    core["reviewAttemptArtifacts"] = [artifact]
    return core, attempt, artifact


def control_snapshot(core):
    receipt = core["phaseReceipts"][0]
    schema_bytes = codec.canonical_json_bytes(SCHEMA)
    ledger_bytes = support.build_ledger_markdown(core["seams"])
    receipt_bytes = support.build_receipt_markdown(receipt)
    sync = markdown.synchronize_ledger_markdown(ledger_bytes, core["seams"])
    sections = [
        {
            "id": section.id,
            "narrativeRawSha256": section.narrative_raw_sha256,
            "seamProjection": copy.deepcopy(section.seam_projection),
        }
        for section in sync.sections
    ]
    return schema_bytes, ledger_bytes, receipt_bytes, sections


def frozen_target(core):
    schema_bytes, ledger_bytes, receipt_bytes, sections = control_snapshot(core)
    target = review.build_review_target_from_control_bytes(
        SCHEMA,
        core,
        phase="A",
        attempt_id=core["phaseReceipts"][0]["reviewAttemptId"],
        ledger_sections=sections,
        semantic_diff_paths=[
            "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
        ],
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=receipt_bytes,
        enforce_subject_digest=False,
    )
    core["reviewAttempts"][-1]["reviewSubjectDigest"] = target[
        "reviewSubjectDigest"
    ]
    return review.build_review_target_from_control_bytes(
        SCHEMA,
        core,
        phase="A",
        attempt_id=core["phaseReceipts"][0]["reviewAttemptId"],
        ledger_sections=sections,
        semantic_diff_paths=[
            "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
        ],
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=receipt_bytes,
    )


def attestation(core, kind, verdict="PASS", findings=None, reviewer=None):
    findings = findings or []
    attempt = core["reviewAttempts"][-1]
    artifact = core["reviewAttemptArtifacts"][-1]
    severe = sorted(
        finding["id"]
        for finding in findings
        if finding["severity"] in {"CRITICAL", "MAJOR"}
    )
    return {
        "id": f"ATT-{kind}-A-{attempt['id'].rsplit('-', 1)[1]}",
        "kind": kind,
        "path": attempt["logicReviewPath" if kind == "LOGIC" else "btjReviewPath"],
        "receiptId": attempt["receiptId"],
        "reviewerId": reviewer or f"independent-{kind.lower()}",
        "reviewerRole": f"Independent {kind} reviewer",
        "independenceStatement": "No implementation role in this attempt.",
        "reviewTargetDigest": artifact["reviewTargetSha256"],
        "verdict": verdict,
        "findingIds": sorted(finding["id"] for finding in findings),
        "openSevereFindingIds": severe if verdict == "FAIL" else [],
        "approvedUpgradeSeamIds": [],
        "approvedGateSeamIds": [],
        "attemptId": attempt["id"],
    }


def finding(core, kind="LOGIC", severity="MAJOR"):
    attempt = core["reviewAttempts"][-1]
    return {
        "id": f"FND-A-{kind}-001",
        "attemptId": attempt["id"],
        "reviewKind": kind,
        "category": "LOGIC" if kind == "LOGIC" else "JUSTICE",
        "severity": severity,
        "statement": "A bounded synthetic finding.",
        "claimIds": [core["claims"][0]["id"]],
        "seamIds": [],
        "ledgerSectionIds": [],
        "receiptIds": [attempt["receiptId"]],
        "subjectPaths": [core["manifests"][0]["finalFiles"][0]["path"]],
    }


class ReviewSubjectDigestTests(unittest.TestCase):
    def test_attempt_number_history_and_derived_paths_do_not_change_subject(self):
        core, _, _ = review_core()
        first = frozen_target(core)
        retry = copy.deepcopy(first)
        prior = copy.deepcopy(core["reviewAttempts"][0])
        prior["status"] = "ABANDONED"
        prior["abandonReason"] = "A retry preserves the failed review history."
        new_id = "RVA-A-002"
        retry["currentAttemptId"] = new_id
        retry["priorReviewAttempts"] = [prior]
        retry["priorReviewAttemptArtifacts"] = copy.deepcopy(
            core["reviewAttemptArtifacts"]
        )
        old_paths = set(attempt_paths(prior["id"]))
        new_paths = set(attempt_paths(new_id))
        retry["manifest"]["closureOnlyPaths"] = sorted(old_paths | new_paths)
        retry["manifest"]["allowedChangePaths"] = sorted(
            {
                path
                for path in retry["manifest"]["allowedChangePaths"]
                if path not in old_paths
            }
            | old_paths
            | new_paths
        )
        retry["reviewSubjectDigest"] = support.RAW_HASH
        self.assertEqual(
            review.compute_review_subject_digest(first),
            review.compute_review_subject_digest(retry),
        )
        retry["claims"][0]["conclusion"] += " Changed."
        self.assertNotEqual(
            review.compute_review_subject_digest(first),
            review.compute_review_subject_digest(retry),
        )

    def test_unbound_or_incomplete_attempt_closure_fails_closed(self):
        core, _, _ = review_core()
        target = frozen_target(core)
        target["manifest"]["closureOnlyPaths"].pop()
        with self.assertRaises(KintsugiError) as raised:
            review.compute_review_subject_digest(target)
        self.assertEqual(raised.exception.code, "KIN-E-MANIFEST")


class ReviewTargetProjectionTests(unittest.TestCase):
    def test_target_binds_exact_control_and_typed_semantics(self):
        core, attempt, _ = review_core()
        target = frozen_target(core)
        schema_bytes, ledger_bytes, receipt_bytes, _ = control_snapshot(core)
        receipt_sync = markdown.synchronize_receipt_markdown(
            receipt_bytes, core["phaseReceipts"][0]
        )
        ledger_sync = markdown.synchronize_ledger_markdown(
            ledger_bytes, core["seams"]
        )
        self.assertEqual(target["currentAttemptId"], attempt["id"])
        self.assertEqual(target["receiptId"], attempt["receiptId"])
        self.assertEqual(target["schemaSha256"], codec.raw_hash(schema_bytes))
        self.assertEqual(
            target["receiptNarrativeRawSha256"],
            receipt_sync.narrative_raw_sha256,
        )
        self.assertEqual(
            target["ledgerPreambleRawSha256"], ledger_sync.preamble.raw_sha256
        )
        self.assertEqual(target["priorReviewAttempts"], [])
        self.assertEqual(
            schema_module.validate_named_definition(SCHEMA, "reviewTarget", target),
            [],
        )
        self.assertEqual(
            target["reviewSubjectDigest"],
            review.compute_review_subject_digest(target),
        )

    def test_any_control_narrative_or_declared_section_drift_is_rejected(self):
        core, _, _ = review_core()
        frozen_target(core)
        schema_bytes, ledger_bytes, receipt_bytes, sections = control_snapshot(core)
        cases = (
            {"schema_bytes": schema_bytes + b" "},
            {"ledger_bytes": ledger_bytes + b"drift\n"},
            {"receipt_bytes": receipt_bytes + b"drift\n"},
            {"ledger_sections": [{"id": "KIN-A-999"}]},
        )
        defaults = {
            "schema_bytes": schema_bytes,
            "ledger_bytes": ledger_bytes,
            "receipt_bytes": receipt_bytes,
            "ledger_sections": sections,
        }
        for changed in cases:
            with self.subTest(changed=tuple(changed)):
                values = defaults | changed
                with self.assertRaises(KintsugiError):
                    review.build_review_target_from_control_bytes(
                        SCHEMA,
                        core,
                        phase="A",
                        attempt_id="RVA-A-001",
                        semantic_diff_paths=[
                            "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
                        ],
                        **values,
                    )

    def test_terminal_ancestor_projection_is_root_to_leaf_and_complete(self):
        core, first, first_artifact = review_core()
        first.update({
            "status": "ABANDONED",
            "abandonReason": "The first review transport was invalid.",
        })
        second_id = "RVA-A-002"
        second_paths = attempt_paths(second_id)
        second = copy.deepcopy(first)
        second.update({
            "id": second_id,
            "supersedesAttemptId": first["id"],
            "reviewTargetPath": second_paths[0],
            "logicReviewPath": second_paths[1],
            "btjReviewPath": second_paths[2],
            "validationBundlePath": second_paths[3],
            "status": "PENDING",
            "abandonReason": None,
            "reviewSubjectDigest": None,
        })
        second_artifact = copy.deepcopy(first_artifact)
        second_artifact["attemptId"] = second_id
        core["reviewAttempts"].append(second)
        core["reviewAttemptArtifacts"].append(second_artifact)
        core["phaseReceipts"][0]["reviewAttemptId"] = second_id
        manifest = core["manifests"][0]
        manifest["closureOnlyPaths"] = sorted(
            set(manifest["closureOnlyPaths"]) | set(second_paths)
        )
        manifest["allowedChangePaths"] = sorted(
            set(manifest["allowedChangePaths"]) | set(second_paths)
        )
        history = review.project_terminal_review_history(core, "A", second_id)
        self.assertEqual([value["id"] for value in history["attempts"]], [first["id"]])
        self.assertEqual(
            [value["attemptId"] for value in history["artifacts"]], [first["id"]]
        )
        second["supersedesAttemptId"] = "RVA-A-999"
        with self.assertRaises(KintsugiError):
            review.project_terminal_review_history(core, "A", second_id)


class AttestationValidationTests(unittest.TestCase):
    def setUp(self):
        self.core, _, self.artifact = review_core()
        self.target = frozen_target(self.core)
        self.artifact["reviewTargetSha256"] = codec.raw_hash(
            codec.canonical_json_bytes(self.target)
        )

    def test_two_independent_passes_are_valid(self):
        reviews = [
            attestation(self.core, "LOGIC"),
            attestation(self.core, "BTJ"),
        ]
        self.assertEqual(
            review.validate_review_attestations(self.core, reviews, []), []
        )

    def test_reviewer_shopping_and_target_drift_fail(self):
        reviews = [
            attestation(self.core, "LOGIC", reviewer="same-person"),
            attestation(self.core, "BTJ", reviewer="same-person"),
        ]
        reviews[1]["reviewTargetDigest"] = "sha256:" + "1" * 64
        issues = review.validate_review_attestations(self.core, reviews, [])
        self.assertIn("KIN-E-STATE", issue_codes(issues))
        self.assertIn("KIN-E-REF", issue_codes(issues))

    def test_fail_requires_exact_open_severe_set_and_pass_only_minor(self):
        severe = finding(self.core)
        failed = attestation(self.core, "LOGIC", "FAIL", [severe])
        self.assertEqual(
            review.validate_review_attestations(self.core, [failed], [severe]), []
        )
        failed["openSevereFindingIds"] = []
        self.assertIn(
            "KIN-E-STATE",
            issue_codes(
                review.validate_review_attestations(self.core, [failed], [severe])
            ),
        )
        passed = attestation(self.core, "LOGIC", "PASS", [severe])
        self.assertIn(
            "KIN-E-STATE",
            issue_codes(
                review.validate_review_attestations(self.core, [passed], [severe])
            ),
        )

    def test_logic_and_btj_own_disjoint_finding_and_approval_axes(self):
        wrong = finding(self.core, kind="BTJ")
        wrong["category"] = "EVIDENCE"
        btj = attestation(self.core, "BTJ", "FAIL", [wrong])
        btj["approvedUpgradeSeamIds"] = ["KIN-A-001"]
        issues = review.validate_review_attestations(self.core, [btj], [wrong])
        self.assertIn("KIN-E-STATE", issue_codes(issues))


class TransitionStateTests(unittest.TestCase):
    def setUp(self):
        self.core, _, _ = review_core()
        self.target = frozen_target(self.core)
        self.target_bytes = codec.canonical_json_bytes(self.target)
        self.ready = review.transition_core_value(
            self.core,
            phase="A",
            stage="TARGET_READY",
            review_documents=[self.target_bytes],
        )

    def review_bytes(self, core, kind, verdict="PASS", findings=None):
        values = findings or []
        record = attestation(core, kind, verdict, values)
        return support.build_review_markdown(record, values)

    def test_target_ready_and_attested_change_only_frozen_state_paths(self):
        artifact = self.ready["reviewAttemptArtifacts"][0]
        self.assertEqual(artifact["reviewTargetSha256"], codec.raw_hash(self.target_bytes))
        logic_bytes = self.review_bytes(self.ready, "LOGIC")
        attested = review.transition_core_value(
            self.ready,
            phase="A",
            stage="ATTESTED",
            review_documents=[logic_bytes],
        )
        self.assertEqual(attested["reviewAttempts"][0]["status"], "PENDING")
        self.assertTrue(attested["reviewAttempts"][0]["logicAttestationId"])
        self.assertEqual(
            review.validate_state_transition(self.ready, attested, "ATTESTED"), []
        )
        poisoned = copy.deepcopy(attested)
        poisoned["claims"][0]["conclusion"] += " poisoned"
        self.assertIn(
            "KIN-E-STATE",
            issue_codes(
                review.validate_state_transition(self.ready, poisoned, "ATTESTED")
            ),
        )

    def test_fail_abandon_complete_and_verified_are_exact(self):
        severe = finding(self.ready)
        failed = review.transition_core_value(
            self.ready,
            phase="A",
            stage="FAILED",
            review_documents=[self.review_bytes(self.ready, "LOGIC", "FAIL", [severe])],
        )
        self.assertEqual(failed["reviewAttempts"][0]["status"], "FAILED")
        abandoned = review.transition_core_value(
            self.ready,
            phase="A",
            stage="ABANDONED",
            review_documents=[],
            abandon_reason="The bounded review transport was withdrawn.",
        )
        self.assertEqual(abandoned["reviewAttempts"][0]["status"], "ABANDONED")

        attested = review.transition_core_value(
            self.ready,
            phase="A",
            stage="ATTESTED",
            review_documents=[self.review_bytes(self.ready, "LOGIC")],
        )
        complete = review.transition_core_value(
            attested,
            phase="A",
            stage="COMPLETE",
            review_documents=[self.review_bytes(attested, "BTJ")],
        )
        self.assertEqual(complete["reviewAttempts"][0]["status"], "PASSED")
        self.assertEqual(complete["phaseReceipts"][0]["status"], "COMPLETE")

        schema_bytes, ledger_bytes, receipt_bytes, _ = control_snapshot(complete)
        bundle = review.build_validation_bundle_from_control_bytes(
            SCHEMA,
            complete,
            phase="A",
            attempt_id="RVA-A-001",
            review_target=self.target,
            public_queue=None,
            schema_bytes=schema_bytes,
            ledger_bytes=ledger_bytes,
            receipt_bytes=receipt_bytes,
        )
        bundle_bytes = codec.canonical_json_bytes(bundle)
        verified = review.transition_core_value(
            complete,
            phase="A",
            stage="VERIFIED",
            review_documents=[bundle_bytes],
        )
        receipt = verified["phaseReceipts"][0]
        self.assertEqual(receipt["status"], "VERIFIED")
        self.assertEqual(receipt["validationDigest"], codec.raw_hash(bundle_bytes))
        self.assertEqual(
            review.validate_state_transition(complete, verified, "VERIFIED"), []
        )

    def test_abandon_reason_is_stage_bound(self):
        with self.assertRaises(KintsugiError):
            review.transition_core_value(
                self.ready,
                phase="A",
                stage="ABANDONED",
                review_documents=[],
            )
        with self.assertRaises(KintsugiError):
            review.transition_core_value(
                self.ready,
                phase="A",
                stage="ATTESTED",
                review_documents=[],
                abandon_reason="Not permitted here.",
            )


class BundleProjectionTests(unittest.TestCase):
    def test_complete_closes_cited_gates_and_bundle_retains_full_seams(self):
        core, _, _ = review_core()
        support.add_retiered_seam(core, "S", "I")
        owned_trial = next(
            value
            for value in core["trials"]
            if value["id"] in core["phaseReceipts"][0]["trialIds"]
        )
        owned_trial["status"] = "CLOSED"
        target = frozen_target(core)
        ready = review.transition_core_value(
            core,
            phase="A",
            stage="TARGET_READY",
            review_documents=[codec.canonical_json_bytes(target)],
        )
        attested = review.transition_core_value(
            ready,
            phase="A",
            stage="ATTESTED",
            review_documents=[
                support.build_review_markdown(attestation(ready, "LOGIC"), [])
            ],
        )
        btj = attestation(attested, "BTJ")
        btj["approvedGateSeamIds"] = ["KIN-A-001"]
        complete = review.transition_core_value(
            attested,
            phase="A",
            stage="COMPLETE",
            review_documents=[
                support.build_review_markdown(btj, [])
            ],
        )
        seam = complete["seams"][0]
        receipt = complete["phaseReceipts"][0]
        self.assertEqual(
            seam["truthGate"],
            {
                "status": "PASS",
                "rationale": "Awaiting the independent review artifact.",
                "reviewerPath": receipt["logicReviewPath"],
            },
        )
        for field in ("beautyGate", "justiceGate"):
            self.assertEqual(seam[field]["status"], "PASS")
            self.assertEqual(seam[field]["reviewerPath"], receipt["btjReviewPath"])

        schema_bytes, ledger_bytes, receipt_bytes, _ = control_snapshot(complete)
        bundle = review.build_validation_bundle_from_control_bytes(
            SCHEMA,
            complete,
            phase="A",
            attempt_id="RVA-A-001",
            review_target=target,
            public_queue=None,
            schema_bytes=schema_bytes,
            ledger_bytes=ledger_bytes,
            receipt_bytes=receipt_bytes,
        )
        self.assertEqual(bundle["seams"], complete["seams"])
        self.assertEqual(
            [markdown.project_review_seam(value) for value in bundle["seams"]],
            target["seams"],
        )
        self.assertEqual(
            schema_module.validate_named_definition(
                SCHEMA, "validationBundle", bundle
            ),
            [],
        )

    def test_bundle_binds_full_history_raw_sections_and_receipt_projection(self):
        core, _, _ = review_core()
        target = frozen_target(core)
        target_bytes = codec.canonical_json_bytes(target)
        ready = review.transition_core_value(
            core, phase="A", stage="TARGET_READY", review_documents=[target_bytes]
        )
        attested = review.transition_core_value(
            ready,
            phase="A",
            stage="ATTESTED",
            review_documents=[
                support.build_review_markdown(attestation(ready, "LOGIC"), [])
            ],
        )
        complete = review.transition_core_value(
            attested,
            phase="A",
            stage="COMPLETE",
            review_documents=[
                support.build_review_markdown(attestation(attested, "BTJ"), [])
            ],
        )
        schema_bytes, ledger_bytes, receipt_bytes, _ = control_snapshot(complete)
        bundle = review.build_validation_bundle_from_control_bytes(
            SCHEMA,
            complete,
            phase="A",
            attempt_id="RVA-A-001",
            review_target=target,
            public_queue=None,
            schema_bytes=schema_bytes,
            ledger_bytes=ledger_bytes,
            receipt_bytes=receipt_bytes,
        )
        self.assertEqual(
            schema_module.validate_named_definition(
                SCHEMA, "validationBundle", bundle
            ),
            [],
        )
        self.assertEqual(bundle["reviewTargetDigest"], codec.raw_hash(target_bytes))
        self.assertEqual(bundle["receiptDescriptor"]["status"], "VERIFIED")
        self.assertEqual(bundle["reviewAttempts"], complete["reviewAttempts"])
        self.assertEqual(
            review.validate_validation_bundle(
                SCHEMA,
                complete,
                bundle,
                phase="A",
                attempt_id="RVA-A-001",
                review_target=target,
                public_queue=None,
            ),
            [],
        )
        drifted = copy.deepcopy(bundle)
        drifted["claims"][0]["conclusion"] += " drift"
        self.assertIn(
            "KIN-E-BUNDLE",
            issue_codes(
                review.validate_validation_bundle(
                    SCHEMA,
                    complete,
                    drifted,
                    phase="A",
                    attempt_id="RVA-A-001",
                    review_target=target,
                    public_queue=None,
                )
            ),
        )

    def test_live_wrappers_are_read_only_and_overlay_helper_detects_drift(self):
        core, _, _ = review_core()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            schema_path = root / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
            ledger_path = root / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
            receipt_path = root / core["phaseReceipts"][0]["path"]
            for path in (schema_path, ledger_path, receipt_path):
                path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.write_bytes(codec.canonical_json_bytes(SCHEMA))
            ledger_path.write_bytes(support.build_ledger_markdown(core["seams"]))
            receipt_path.write_bytes(
                support.build_receipt_markdown(core["phaseReceipts"][0])
            )
            before = {
                path: path.read_bytes()
                for path in (schema_path, ledger_path, receipt_path)
            }
            _, _, _, sections = control_snapshot(core)
            provisional = review.build_review_target_from_control_bytes(
                SCHEMA,
                core,
                phase="A",
                attempt_id="RVA-A-001",
                ledger_sections=sections,
                semantic_diff_paths=[
                    "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
                ],
                schema_bytes=before[schema_path],
                ledger_bytes=before[ledger_path],
                receipt_bytes=before[receipt_path],
                enforce_subject_digest=False,
            )
            core["reviewAttempts"][0]["reviewSubjectDigest"] = provisional[
                "reviewSubjectDigest"
            ]
            review.build_review_target_value(
                root,
                SCHEMA,
                core,
                phase="A",
                attempt_id="RVA-A-001",
                ledger_sections=sections,
                semantic_diff_paths=[
                    "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
                ],
            )
            self.assertEqual(
                before,
                {path: path.read_bytes() for path in before},
            )


if __name__ == "__main__":
    unittest.main()

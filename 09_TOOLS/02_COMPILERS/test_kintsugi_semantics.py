from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


COMPILER = Path(__file__).resolve().parent
ROOT = COMPILER.parents[1]
sys.path.insert(0, str(COMPILER))

import kintsugi_kernel as kernel  # noqa: E402
import kintsugi_test_support as support  # noqa: E402


SCHEMA = json.loads(
    (ROOT / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json").read_text(
        encoding="utf-8"
    )
)


def validate(core, *, phase="A", bootstrap=False):
    function = getattr(kernel, "validate_core_records", None)
    return [] if function is None else function(core, phase=phase, bootstrap=bootstrap)


def validate_queue(queue, core):
    function = getattr(kernel, "validate_public_queue", None)
    return [] if function is None else function(queue, core)


def evaluate(evaluator, payload, core):
    function = getattr(kernel, "evaluate_semantic_fixture", None)
    return [] if function is None else function(evaluator, payload, core)


def evaluate_fixture(core, fixture_id):
    function = getattr(kernel, "evaluate_antibody_fixture", None)
    return [] if function is None else function(core, fixture_id)


def regex_search(pattern, source):
    function = getattr(kernel, "safe_regex_search", None)
    return (False, []) if function is None else function(pattern, source)


def scan(core, documents):
    function = getattr(kernel, "scan_antibodies", None)
    empty = {"included": {}, "excluded": {}, "triggers": {}}
    return (empty, []) if function is None else function(core, documents)


def codes(issues):
    return [issue.code for issue in issues]


def semantic_issue(issues):
    return "KIN-E-FIXTURE" in codes(issues)


def issue_signature(issues):
    return tuple((issue.path, issue.code, issue.message) for issue in issues)


def replace_path(value, path, replacement):
    mutated = copy.deepcopy(value)
    cursor = mutated
    for component in path[:-1]:
        cursor = cursor[component]
    cursor[path[-1]] = copy.deepcopy(replacement)
    return mutated


def make_queue_core():
    core = support.build_semantic_core()
    manifest = core["manifests"][0]
    manifest.update({
        "id": "MAN-C-001",
        "phase": "C",
        "requiredClaimBindings": [],
    })
    for source in core["sources"]:
        source["phases"] = ["C"]
    for trial in core["trials"]:
        trial.update({"manifestId": "MAN-C-001", "receiptId": "REC-C-110"})
    receipt = core["phaseReceipts"][0]
    receipt.update({
        "id": "REC-C-110",
        "phase": "C",
        "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md",
        "manifestId": "MAN-C-001",
        "dependsOnReceiptIds": ["REC-A-108", "REC-B-109"],
    })
    for public_path in (
        "12_PUBLIC_SITE/compass/index.html",
        "12_PUBLIC_SITE/orphan/index.html",
    ):
        manifest["includedFiles"].append({
            "path": public_path,
            "kind": "FILE",
            "sha256": support.RAW_HASH,
        })
    queue = {
        "schemaVersion": "1.0.0",
        "manifestId": "MAN-C-001",
        "receiptId": "REC-C-110",
        "items": [{
            "route": "/compass/",
            "publicFile": "12_PUBLIC_SITE/compass/index.html",
            "publicQuote": "A bounded structural statement.",
            "ownership": "OWNED",
            "driftClass": None,
            "severity": None,
            "currentEvidence": copy.deepcopy(core["claims"][0]["evidence"]),
            "maximumPublicStrength": "A",
            "requiredAction": "KEEP",
            "verificationCommand": "python3 -m unittest",
            "ownerSourceId": core["claims"][0]["ownerSourceId"],
            "claimId": core["claims"][0]["id"],
            "seamIds": [],
        }],
    }
    return core, queue


def make_ownerless_item(core):
    manifest = core["manifests"][0]
    eligible = sorted(
        source["id"] for source in core["sources"]
        if source["authorityRole"] == "SEMANTIC_OWNER"
        and manifest["phase"] in source["phases"]
        and source["path"] in {item["path"] for item in manifest["includedFiles"]}
    )
    return {
        "route": "/orphan/",
        "publicFile": "12_PUBLIC_SITE/orphan/index.html",
        "publicQuote": "An ownerless public statement.",
        "ownership": "OWNERLESS",
        "driftClass": "AUTHORITY_DRIFT",
        "currentEvidence": {"strength": "C", "sourced": False, "lifecycle": "DRAFT"},
        "maximumPublicStrength": "C",
        "requiredAction": "RETRACT",
        "severity": "MAJOR",
        "verificationCommand": "python3 -m unittest",
        "ownerSearchEvidence": {
            "manifestIds": [manifest["id"]],
            "searchedSourceIds": eligible,
            "method": "Search every eligible semantic-owner source in the frozen manifest.",
            "result": "No owner was found.",
        },
        "candidateOwners": [],
        "disposition": "Retract until a semantic owner exists.",
    }


def complete_receipt_with_seam(core, *, verified=False):
    seam = support.add_confirmed_seam(core)
    attempt_id = "RVA-A-001"
    target_path = f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/review_target.json"
    logic_path = f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_LOGIC.md"
    btj_path = f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_BTJ.md"
    bundle_path = f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/validation_bundle.json"
    attempt = {
        "id": attempt_id,
        "phase": "A",
        "receiptId": "REC-A-108",
        "supersedesAttemptId": None,
        "reviewSubjectDigest": support.RAW_HASH,
        "reviewTargetPath": target_path,
        "logicReviewPath": logic_path,
        "btjReviewPath": btj_path,
        "validationBundlePath": bundle_path,
        "logicAttestationId": "ATT-LOGIC-A-001",
        "btjAttestationId": "ATT-BTJ-A-001",
        "status": "PASSED",
        "abandonReason": None,
    }
    core["reviewAttempts"] = [attempt]
    core["reviewAttemptArtifacts"] = [{
        "attemptId": attempt_id,
        "reviewTargetSha256": support.RAW_HASH,
        "logicReviewSha256": support.RAW_HASH,
        "btjReviewSha256": support.RAW_HASH,
    }]
    core["reviewAttestations"] = [
        {
            "id": f"ATT-{kind}-A-001",
            "kind": kind,
            "path": path,
            "receiptId": "REC-A-108",
            "reviewerId": f"independent-{kind.lower()}",
            "reviewerRole": f"Independent {kind} reviewer",
            "independenceStatement": "No implementation role in this attempt.",
            "reviewTargetDigest": support.RAW_HASH,
            "verdict": "PASS",
            "findingIds": [],
            "openSevereFindingIds": [],
            "approvedUpgradeSeamIds": [],
            "approvedGateSeamIds": [seam["id"]] if kind == "BTJ" else [],
            "attemptId": attempt_id,
        }
        for kind, path in (("LOGIC", logic_path), ("BTJ", btj_path))
    ]
    receipt = core["phaseReceipts"][0]
    receipt.update({
        "status": "VERIFIED" if verified else "COMPLETE",
        "reviewTargetDigest": support.RAW_HASH,
        "logicReviewPath": logic_path,
        "btjReviewPath": btj_path,
        "reviewAttemptId": attempt_id,
        "validationBundlePath": bundle_path if verified else None,
        "validationDigest": support.RAW_HASH if verified else None,
    })
    manifest = core["manifests"][0]
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])
    paths = [target_path, logic_path, btj_path, bundle_path]
    manifest["closureOnlyPaths"] = sorted(paths)
    manifest["allowedChangePaths"] = sorted(set(manifest["allowedChangePaths"]) | set(paths))
    seam["truthGate"] = {
        "status": "PASS", "rationale": "LOGIC review passed.", "reviewerPath": logic_path,
    }
    for gate_name in ("beautyGate", "justiceGate"):
        seam[gate_name] = {
            "status": "PASS", "rationale": "BTJ review passed.", "reviewerPath": btj_path,
        }
    return seam


class ModalityAndEvidenceTests(unittest.TestCase):
    def assertSchemaValid(self, core):
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])

    def test_all_six_modal_forces_are_preserved_without_an_ordering(self):
        modalities = ("ACTUAL", "POSSIBLE", "NECESSARY", "NORMATIVE", "DEFINITIONAL", "CONJECTURAL")
        for modality in modalities:
            core = support.build_semantic_core()
            claim = core["claims"][0]
            claim["modality"] = modality
            if modality == "NORMATIVE":
                claim.update({
                    "claimType": "NORMATIVE",
                    "justiceScope": "NORMATIVE",
                    "justiceContext": support.build_justice_context(),
                })
                claim["premises"][0]["role"] = "NORMATIVE"
            with self.subTest(modality=modality, case="preserved"):
                self.assertSchemaValid(core)
                self.assertEqual(validate(core), [])

            dependency = core["claims"][1]
            dependency["modality"] = "ACTUAL" if modality != "ACTUAL" else "POSSIBLE"
            claim["dependencyClaimIds"] = [dependency["id"]]
            with self.subTest(modality=modality, case="unmarked substitution"):
                self.assertIn("KIN-E-VERDICT", codes(validate(core)))

            core["claims"][2]["modality"] = modality
            if modality == "NORMATIVE":
                core["claims"][2].update({
                    "claimType": "NORMATIVE",
                    "justiceScope": "NORMATIVE",
                    "justiceContext": support.build_justice_context(),
                })
                core["claims"][2]["premises"][0]["role"] = "NORMATIVE"
            claim["dependencyClaimIds"].append(core["claims"][2]["id"])
            with self.subTest(modality=modality, case="typed entailing dependency"):
                self.assertNotIn("KIN-E-VERDICT", codes(validate(core)))

    def test_support_receipt_authority_and_lifecycle_do_not_change_modality(self):
        core = support.build_semantic_core()
        claim = core["claims"][0]
        claim["modality"] = "POSSIBLE"
        claim["supportLinks"] = [{
            "id": "SUP-A-001",
            "supportingClaimId": core["claims"][1]["id"],
            "mode": "ROSETTA_TRANSFER",
            "independenceStatus": "NOT_APPLICABLE",
            "evidenceCeiling": "I",
            "rationale": "A correspondence-only edge.",
        }]
        self.assertEqual(validate(core), [])
        self.assertEqual(claim["modality"], "POSSIBLE")

    def test_link_ceiling_mode_and_supporting_claim_warrant_are_bounded(self):
        base = support.build_semantic_core()
        target, supporting = base["claims"][:2]
        target["supportLinks"] = [{
            "id": "SUP-A-001", "supportingClaimId": supporting["id"],
            "mode": "CORROBORATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "A qualifying support edge.",
        }]
        self.assertEqual(validate(base), [])

        rows = []
        weak = copy.deepcopy(base)
        weak["claims"][1]["evidence"]["strength"] = "C"
        rows.append(("ceiling exceeds support", weak))
        unsourced = copy.deepcopy(base)
        unsourced["claims"][1]["evidence"]["sourced"] = False
        rows.append(("A unsourced", unsourced))
        open_trial = copy.deepcopy(base)
        open_trial["trials"][1]["status"] = "TRIED"
        rows.append(("trial not closed", open_trial))
        retired = copy.deepcopy(base)
        retired["claims"][1]["evidence"]["lifecycle"] = "RETIRED"
        retired["claims"][1]["killCriterion"] = {"kind": "NONE", "rationale": "Retired."}
        rows.append(("retired support", retired))
        conditional_a = copy.deepcopy(base)
        conditional_a["trials"][1].update({
            "verdict": "VALID_CONDITIONAL",
            "validityVerdict": "VALID",
            "soundnessVerdict": "CONDITIONALLY_SUPPORTED",
        })
        rows.append(("A not sound", conditional_a))
        for label, core in rows:
            with self.subTest(label=label):
                self.assertIn("KIN-E-VERDICT", codes(validate(core)))

        analogy = support.build_semantic_core()
        analogy["claims"][0]["supportLinks"] = [{
            "id": "SUP-A-ANALOGY", "supportingClaimId": analogy["claims"][1]["id"],
            "mode": "ANALOGY", "independenceStatus": "NOT_APPLICABLE",
            "evidenceCeiling": "I", "rationale": "Analogy remains interpretive.",
        }]
        self.assertEqual(validate(analogy), [])
        analogy["claims"][0]["supportLinks"][0]["evidenceCeiling"] = "S"
        self.assertIn("KIN-E-VERDICT", codes(validate(analogy)))

    def test_repetition_does_not_aggregate_into_a_tier(self):
        core = support.build_semantic_core()
        target = core["claims"][0]
        for supporting in core["claims"][1:4]:
            supporting["evidence"]["strength"] = "C"
            supporting["upgradeCriterion"] = {"kind": "NONE", "rationale": "No upgrade asserted."}
        target["supportLinks"] = [
            {
                "id": f"SUP-A-{index:03d}",
                "supportingClaimId": supporting["id"],
                "mode": "CORROBORATION",
                "independenceStatus": "INDEPENDENT",
                "evidenceCeiling": "C",
                "rationale": "One weak corroborating record.",
            }
            for index, supporting in enumerate(core["claims"][1:4], start=1)
        ]
        self.assertEqual(validate(core), [])
        self.assertEqual(target["evidence"]["strength"], "A")

    def test_all_twelve_retier_directions_require_the_asymmetric_warrant(self):
        order = "CISA"
        pairs = [(left, right) for left in order for right in order if left != right]
        for before, after in pairs:
            core = support.build_semantic_core()
            support.add_retiered_seam(core, before, after)
            with self.subTest(before=before, after=after, case="warranted"):
                self.assertSchemaValid(core)
                self.assertEqual(validate(core), [])

            mutated = copy.deepcopy(core)
            broken = mutated["seams"][0]
            if order.index(after) > order.index(before):
                broken["upgradeEvidenceLinkIds"] = ["SUP-MISSING"]
            else:
                broken["priorKillCriterion"]["resultingStrength"] = before
            with self.subTest(before=before, after=after, case="unwarranted"):
                self.assertIn("KIN-E-VERDICT", codes(validate(mutated)))

    def test_equal_retier_non_retier_strength_change_and_retraction_are_distinct(self):
        equal = support.build_semantic_core()
        seam = support.add_retiered_seam(equal, "C", "I")
        seam["evidenceAfter"]["strength"] = "C"
        equal["claims"][0]["evidence"]["strength"] = "C"
        self.assertIn("KIN-E-VERDICT", codes(validate(equal)))

        wrong_kind = support.build_semantic_core()
        seam = support.add_retiered_seam(wrong_kind, "I", "S")
        seam["repairKind"] = "NARROW"
        self.assertIn("KIN-E-VERDICT", codes(validate(wrong_kind)))

        for strength in "CISA":
            core = support.build_semantic_core()
            support.add_retracted_seam(core, strength)
            with self.subTest(strength=strength):
                self.assertSchemaValid(core)
                self.assertEqual(validate(core), [])
            core["seams"][0]["evidenceAfter"]["strength"] = "C" if strength != "C" else "I"
            self.assertIn("KIN-E-VERDICT", codes(validate(core)))

    def test_kill_criterion_lifecycle_and_prior_current_sync_are_exact(self):
        deferred = support.build_semantic_core()
        deferred["claims"][0]["killCriterion"] = {
            "kind": "TESTABLE", "testability": "DEFERRED",
            "trigger": "The deferred test becomes feasible.",
            "method": "Run the declared future protocol.",
            "disposition": "RETRACT",
            "deferredReason": "The instrument does not yet exist.",
            "unblockCondition": "A calibrated instrument exists.",
        }
        self.assertSchemaValid(deferred)
        self.assertEqual(validate(deferred), [])
        del deferred["claims"][0]["killCriterion"]["unblockCondition"]
        self.assertIn("KIN-E-STATE", codes(validate(deferred)))

        sync = support.build_semantic_core()
        support.add_retiered_seam(sync, "I", "S")
        sync["seams"][0]["survivingIfKilled"]["rationale"] = "Drifted current contract."
        self.assertIn("KIN-E-STATE", codes(validate(sync)))

    def test_upgrade_minimum_ceiling_and_non_upgrade_link_field_are_enforced(self):
        upward = support.build_semantic_core()
        support.add_retiered_seam(upward, "C", "S")
        upward["seams"][0]["priorUpgradeCriterion"]["minimumEvidenceCeiling"] = "A"
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", upward), [])
        self.assertIn("KIN-E-VERDICT", codes(validate(upward)))

        downward = support.build_semantic_core()
        support.add_retiered_seam(downward, "A", "S")
        downward["seams"][0]["upgradeEvidenceLinkIds"] = ["SUP-LEAK"]
        self.assertIn("KIN-E-VERDICT", codes(validate(downward)))

    def test_analogy_ceiling_and_support_trial_quantifiers_are_universal_and_existential(self):
        analogy = support.build_semantic_core()
        target, supporting = analogy["claims"][:2]
        supporting["evidence"]["strength"] = "C"
        target["supportLinks"] = [{
            "id": "SUP-A-ANALOGY",
            "supportingClaimId": supporting["id"],
            "mode": "ANALOGY",
            "independenceStatus": "NOT_APPLICABLE",
            "evidenceCeiling": "I",
            "rationale": "An analogy cannot outrun its supporting claim.",
        }]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", analogy), [])
        self.assertIn("KIN-E-VERDICT", codes(validate(analogy)))

        repeated = support.build_semantic_core()
        target, supporting = repeated["claims"][:2]
        target["supportLinks"] = [{
            "id": "SUP-A-REPEATED",
            "supportingClaimId": supporting["id"],
            "mode": "CORROBORATION",
            "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A",
            "rationale": "At least one admissible trial is sufficient.",
        }]
        second_trial = copy.deepcopy(repeated["trials"][1])
        second_trial["id"] = "TRL-A-099"
        second_trial["triedQuote"] = "An independent replication of the supporting claim."
        second_trial["triedHash"] = kernel.text_hash(second_trial["triedQuote"])
        repeated["trials"].append(second_trial)
        repeated["phaseReceipts"][0]["trialIds"].append(second_trial["id"])
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", repeated), [])
        self.assertEqual(validate(repeated), [])

    def test_target_a_upgrade_needs_any_independent_witness_and_every_ordinary_link(self):
        core = support.build_semantic_core()
        seam = support.add_retiered_seam(core, "C", "A")
        second = {
            "id": "SUP-KIN-A-002",
            "supportingClaimId": core["claims"][2]["id"],
            "mode": "CORROBORATION",
            "independenceStatus": "PARTIALLY_INDEPENDENT",
            "evidenceCeiling": "A",
            "rationale": "A second ordinary qualifying A link need not itself be independent.",
        }
        core["claims"][0]["supportLinks"].append(copy.deepcopy(second))
        seam["supportLinks"].append(copy.deepcopy(second))
        seam["upgradeEvidenceLinkIds"].append(second["id"])
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertEqual(validate(core), [])

        second["independenceStatus"] = "NOT_INDEPENDENT"
        core["claims"][0]["supportLinks"][1] = copy.deepcopy(second)
        seam["supportLinks"][1] = copy.deepcopy(second)
        self.assertIn("KIN-E-VERDICT", codes(validate(core)))

    def _verify_phase_a_receipt(self, core):
        receipt = core["phaseReceipts"][0]
        manifest = core["manifests"][0]
        attempt_id = "RVA-A-900"
        target_path = (
            "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/"
            f"{attempt_id}/review_target.json"
        )
        logic_path = (
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/"
            f"{attempt_id}_LOGIC.md"
        )
        btj_path = (
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/"
            f"{attempt_id}_BTJ.md"
        )
        bundle_path = (
            "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/"
            f"{attempt_id}/validation_bundle.json"
        )
        logic_id = "ATT-LOGIC-A-900"
        btj_id = "ATT-BTJ-A-900"
        core["reviewAttempts"].append({
            "id": attempt_id,
            "phase": "A",
            "receiptId": receipt["id"],
            "supersedesAttemptId": None,
            "reviewSubjectDigest": support.RAW_HASH,
            "reviewTargetPath": target_path,
            "logicReviewPath": logic_path,
            "btjReviewPath": btj_path,
            "validationBundlePath": bundle_path,
            "logicAttestationId": logic_id,
            "btjAttestationId": btj_id,
            "status": "PASSED",
            "abandonReason": None,
        })
        core["reviewAttemptArtifacts"].append({
            "attemptId": attempt_id,
            "reviewTargetSha256": support.RAW_HASH,
            "logicReviewSha256": support.RAW_HASH,
            "btjReviewSha256": support.RAW_HASH,
        })
        for kind, attestation_id, path in (
            ("LOGIC", logic_id, logic_path),
            ("BTJ", btj_id, btj_path),
        ):
            core["reviewAttestations"].append({
                "id": attestation_id,
                "kind": kind,
                "path": path,
                "receiptId": receipt["id"],
                "reviewerId": f"independent-{kind.lower()}-reviewer",
                "reviewerRole": f"Independent {kind} reviewer",
                "independenceStatement": "No implementation role in this attempt.",
                "reviewTargetDigest": support.RAW_HASH,
                "verdict": "PASS",
                "findingIds": [],
                "openSevereFindingIds": [],
                "approvedUpgradeSeamIds": [],
                "approvedGateSeamIds": [],
                "attemptId": attempt_id,
            })
        derived_paths = [target_path, logic_path, btj_path, bundle_path]
        manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
        manifest["finalFileCount"] = len(manifest["finalFiles"])
        manifest["closureOnlyPaths"] = sorted(derived_paths)
        manifest["allowedChangePaths"] = sorted(
            set(manifest["allowedChangePaths"]) | set(derived_paths)
        )
        receipt.update({
            "status": "VERIFIED",
            "reviewTargetDigest": support.RAW_HASH,
            "validationBundlePath": bundle_path,
            "validationDigest": support.RAW_HASH,
            "logicReviewPath": logic_path,
            "btjReviewPath": btj_path,
            "reviewAttemptId": attempt_id,
        })

    def _append_draft_phase_b_claim(self, core):
        vessel = support.build_core_data()
        manifest = copy.deepcopy(vessel["manifests"][0])
        source = copy.deepcopy(vessel["sources"][0])
        claim = copy.deepcopy(vessel["claims"][0])
        trial = copy.deepcopy(vessel["trials"][0])
        receipt = copy.deepcopy(vessel["phaseReceipts"][0])
        manifest.update({
            "finalFiles": [],
            "finalFileCount": 0,
            "harvestedClaimIds": [claim["id"]],
            "eligibleClaimCount": 1,
            "trialedClaimIds": [claim["id"]],
            "trialedClaimCount": 1,
            "closureOnlyPaths": [],
        })
        receipt.update({
            "claimIds": [claim["id"]],
            "trialIds": [trial["id"]],
        })
        core["manifests"].append(manifest)
        core["sources"].append(source)
        core["claims"].append(claim)
        core["trials"].append(trial)
        core["phaseReceipts"].append(receipt)
        return manifest, claim

    def _select_phase_b_with_phase_a_dependency(self, core, *, verified):
        target = core["claims"][0]
        clean_target_trial = copy.deepcopy(next(
            item for item in core["trials"] if item["claimId"] == target["id"]
        ))
        seam = support.add_retiered_seam(core, "C", "S")
        source = next(item for item in core["sources"] if item["id"] == target["ownerSourceId"])
        source["phases"] = sorted(set(source["phases"] + ["B"]))
        target_trial = copy.deepcopy(next(
            item for item in core["trials"] if item["claimId"] == target["id"]
        ))
        target_trial.update({
            "id": "TRL-B-900",
            "manifestId": "MAN-B-001",
            "receiptId": "REC-B-109",
            "triedQuote": "A Phase-B target formulation is repaired at the declared tier.",
            "triedHash": kernel.text_hash(
                "A Phase-B target formulation is repaired at the declared tier."
            ),
        })
        core["trials"][0] = clean_target_trial
        core["trials"].append(target_trial)
        seam.update({
            "receiptId": "REC-B-109",
            "beforeQuote": target_trial["triedQuote"],
            "beforeHash": target_trial["triedHash"],
        })
        core["phaseReceipts"][0]["seamIds"] = []

        manifest = copy.deepcopy(core["manifests"][0])
        manifest.update({
            "id": "MAN-B-001",
            "phase": "B",
            "requiredClaimBindings": [],
            "harvestedClaimIds": [target["id"]],
            "excludedClaimIds": [],
            "eligibleClaimCount": 1,
            "trialedClaimIds": [target["id"]],
            "trialedClaimCount": 1,
            "finalFiles": [],
            "finalFileCount": 0,
            "closureOnlyPaths": [],
        })
        manifest["discoveryRules"][0]["id"] = "DISC-B-001"
        core["manifests"].append(manifest)

        receipt = copy.deepcopy(core["phaseReceipts"][0])
        receipt.update({
            "id": "REC-B-109",
            "phase": "B",
            "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
            "status": "DRAFT",
            "manifestId": "MAN-B-001",
            "dependsOnReceiptIds": ["REC-A-108"],
            "claimIds": [target["id"]],
            "trialIds": [target_trial["id"]],
            "seamIds": [seam["id"]],
            "propagationIds": [],
            "reviewTargetDigest": None,
            "validationBundlePath": None,
            "validationDigest": None,
            "logicReviewPath": None,
            "btjReviewPath": None,
            "reviewAttemptId": None,
        })
        core["phaseReceipts"].append(receipt)
        if verified:
            self._verify_phase_a_receipt(core)
        return seam

    def test_upgrade_evidence_is_admissible_only_through_selected_or_verified_inventory(self):
        current = support.build_semantic_core()
        support.add_retiered_seam(current, "C", "S")
        self.assertSchemaValid(current)
        self.assertNotIn("KIN-E-VERDICT", codes(validate(current, phase="A")))

        excluded = support.build_semantic_core()
        support.add_retiered_seam(excluded, "C", "S")
        supporting_id = excluded["claims"][1]["id"]
        supporting_trial = next(
            item for item in excluded["trials"] if item["claimId"] == supporting_id
        )
        manifest = excluded["manifests"][0]
        manifest["harvestedClaimIds"].remove(supporting_id)
        manifest["trialedClaimIds"].remove(supporting_id)
        manifest["excludedClaimIds"].append({
            "claimId": supporting_id,
            "reason": "The supporting claim is explicitly excluded from this manifest.",
        })
        manifest["eligibleClaimCount"] -= 1
        manifest["trialedClaimCount"] -= 1
        excluded["phaseReceipts"][0]["claimIds"].remove(supporting_id)
        excluded["phaseReceipts"][0]["trialIds"].remove(supporting_trial["id"])
        self.assertSchemaValid(excluded)
        self.assertIn("KIN-E-VERDICT", codes(validate(excluded, phase="A")))

        unselected = support.build_semantic_core()
        support.add_retiered_seam(unselected, "C", "S")
        supporting_id = unselected["claims"][1]["id"]
        supporting_trial = next(
            item for item in unselected["trials"] if item["claimId"] == supporting_id
        )
        selected_manifest = unselected["manifests"][0]
        selected_manifest["harvestedClaimIds"].remove(supporting_id)
        selected_manifest["trialedClaimIds"].remove(supporting_id)
        selected_manifest["eligibleClaimCount"] -= 1
        selected_manifest["trialedClaimCount"] -= 1
        unselected["phaseReceipts"][0]["claimIds"].remove(supporting_id)
        unselected["phaseReceipts"][0]["trialIds"].remove(supporting_trial["id"])
        other_manifest = copy.deepcopy(selected_manifest)
        other_manifest.update({
            "id": "MAN-B-999", "phase": "B", "requiredClaimBindings": [],
            "harvestedClaimIds": [supporting_id], "excludedClaimIds": [],
            "eligibleClaimCount": 1, "trialedClaimIds": [supporting_id],
            "trialedClaimCount": 1,
        })
        unselected["manifests"].append(other_manifest)
        other_receipt = copy.deepcopy(unselected["phaseReceipts"][0])
        other_receipt.update({
            "id": "REC-B-109", "phase": "B",
            "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
            "manifestId": "MAN-B-999", "dependsOnReceiptIds": ["REC-A-108"],
            "claimIds": [supporting_id], "trialIds": [supporting_trial["id"]],
            "seamIds": [],
        })
        unselected["phaseReceipts"].append(other_receipt)
        supporting_trial.update({"manifestId": "MAN-B-999", "receiptId": "REC-B-109"})
        self.assertSchemaValid(unselected)
        self.assertIn("KIN-E-VERDICT", codes(validate(unselected, phase="A")))

        for verified in (True, False):
            dependency = support.build_semantic_core()
            self._select_phase_b_with_phase_a_dependency(
                dependency, verified=verified
            )
            self.assertSchemaValid(dependency)
            with self.subTest(route="verified dependency" if verified else "unverified dependency"):
                if verified:
                    self.assertEqual(validate(dependency, phase="B"), [])
                else:
                    self.assertIn(
                        "KIN-E-VERDICT", codes(validate(dependency, phase="B"))
                    )

    def test_bare_multi_phase_validation_preserves_each_receipts_admissible_evidence(self):
        core = support.build_semantic_core()
        self._select_phase_b_with_phase_a_dependency(core, verified=True)
        self.assertSchemaValid(core)

        self.assertEqual(validate(core, phase="A"), [])
        self.assertEqual(validate(core, phase="B"), [])
        self.assertEqual(validate(core, phase=None), [])

    def test_bare_validation_does_not_launder_future_or_unrelated_receipt_support(self):
        core = support.build_semantic_core()
        self._verify_phase_a_receipt(core)
        _, supporting = self._append_draft_phase_b_claim(core)
        target = core["claims"][0]
        target["supportLinks"] = [{
            "id": "SUP-KIN-A-900",
            "supportingClaimId": supporting["id"],
            "mode": "CORROBORATION",
            "independenceStatus": "NOT_INDEPENDENT",
            "evidenceCeiling": "A",
            "rationale": "A future unrelated receipt cannot support its Phase-A predecessor.",
        }]
        link_path = "core.claims[0].supportLinks[0]"

        self.assertSchemaValid(core)
        self.assertTrue(any(
            issue.path == link_path and issue.code == "KIN-E-VERDICT"
            for issue in validate(core, phase="A")
        ))
        self.assertFalse(any(
            issue.path == link_path for issue in validate(core, phase="B")
        ))
        self.assertTrue(any(
            issue.path == link_path and issue.code == "KIN-E-VERDICT"
            for issue in validate(core, phase=None)
        ))

    def test_bare_validation_rejects_excluded_or_unverified_cross_phase_support(self):
        rows = []
        excluded = support.build_semantic_core()
        self._select_phase_b_with_phase_a_dependency(excluded, verified=True)
        supporting_id = excluded["claims"][1]["id"]
        excluded["manifests"][1]["excludedClaimIds"].append({
            "claimId": supporting_id,
            "reason": "Phase B explicitly excludes this cross-phase support.",
        })
        rows.append(("excluded", excluded))

        unverified = support.build_semantic_core()
        self._select_phase_b_with_phase_a_dependency(unverified, verified=False)
        rows.append(("unverified dependency", unverified))

        link_path = "core.claims[0].supportLinks[0]"
        for label, core in rows:
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                self.assertTrue(any(
                    issue.path == link_path and issue.code == "KIN-E-VERDICT"
                    for issue in validate(core, phase="B")
                ))
                self.assertTrue(any(
                    issue.path == link_path and issue.code == "KIN-E-VERDICT"
                    for issue in validate(core, phase=None)
                ))

    def test_retier_preserves_a_live_lifecycle_and_cannot_launder_retirement(self):
        rows = []
        for before, after in (("C", "S"), ("A", "S")):
            core = support.build_semantic_core()
            seam = support.add_retiered_seam(core, before, after)
            seam["evidenceAfter"]["lifecycle"] = "RETIRED"
            core["claims"][0]["evidence"]["lifecycle"] = "RETIRED"
            retired_kill = {"kind": "NONE", "rationale": "Retirement is not a RETIER effect."}
            seam["killCriterion"] = copy.deepcopy(retired_kill)
            core["claims"][0]["killCriterion"] = copy.deepcopy(retired_kill)
            rows.append((f"{before}->{after} retired", core))

        lifecycle_change = support.build_semantic_core()
        seam = support.add_retiered_seam(lifecycle_change, "C", "S")
        seam["evidenceBefore"]["lifecycle"] = "DRAFT"
        rows.append(("DRAFT->ACTIVE RETIER", lifecycle_change))

        non_retract = support.build_semantic_core()
        seam = support.add_confirmed_seam(non_retract)
        claim = non_retract["claims"][0]
        claim["evidence"]["lifecycle"] = "RETIRED"
        claim["killCriterion"] = {"kind": "NONE", "rationale": "Only RETRACT may retire."}
        seam.update({
            "status": "REPAIRED",
            "repairKind": "NARROW",
            "afterQuote": "A narrowed formulation that improperly retires the claim.",
            "evidenceAfter": copy.deepcopy(claim["evidence"]),
            "supportLinks": copy.deepcopy(claim["supportLinks"]),
            "upgradeCriterion": copy.deepcopy(claim["upgradeCriterion"]),
            "killCriterion": copy.deepcopy(claim["killCriterion"]),
            "survivingIfKilled": copy.deepcopy(claim["survivingIfKilled"]),
        })
        rows.append(("non-RETRACT retirement", non_retract))

        for label, core in rows:
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                self.assertIn("KIN-E-VERDICT", codes(validate(core)))


class JusticeGateAndQueueTests(unittest.TestCase):
    def assertStableQueueFailure(self, queue, core):
        first = validate_queue(copy.deepcopy(queue), copy.deepcopy(core))
        second = validate_queue(copy.deepcopy(queue), copy.deepcopy(core))
        self.assertTrue(first)
        self.assertEqual(issue_signature(first), issue_signature(second))
        self.assertTrue(all(issue.code == "KIN-E-QUEUE" for issue in first))

    def configure_authority(self, claim, *, effect, scope, regime, mechanism, lifecycle="ACTIVE"):
        claim.update({
            "authorityEffect": effect,
            "authorityScope": scope,
            "justiceContext": support.build_justice_context(regime, mechanism),
        })
        claim["evidence"]["lifecycle"] = lifecycle
        if lifecycle == "RETIRED":
            claim["killCriterion"] = {"kind": "NONE", "rationale": "Retired historical claim."}

    def test_all_authority_effects_and_regimes_preserve_truth_axes(self):
        rows = (
            ("NONE", "NONE", None, None, "ACTIVE", True),
            ("DESCRIPTIVE", "PRIVATE_DAV", "PRIVATE_DAV", "PRISM_PUBLIC_GOVERNANCE", "RETIRED", True),
            ("DESCRIPTIVE", "PUBLIC_DAV", "PUBLIC_DAV", "K2_NATURAL_PERSON", "ACTIVE", False),
            ("CONSEQUENTIAL", "PRIVATE_DAV", "PRIVATE_DAV", "K2_NATURAL_PERSON", "ACTIVE", True),
            ("DISCRETIONARY", "PUBLIC_DAV", "PUBLIC_DAV", "PRISM_PUBLIC_GOVERNANCE", "ACTIVE", True),
            ("CONSEQUENTIAL", "PUBLIC_DAV", "PUBLIC_DAV", "PRISM_PUBLIC_GOVERNANCE", "ACTIVE", True),
            ("CONSTITUTIONAL_AUTOMATIC", "PUBLIC_DAV", "PUBLIC_DAV", "CONSTITUTIONAL_AUTO_ENFORCEMENT", "ACTIVE", True),
            ("DISCRETIONARY", "OTHER", "OTHER", "OTHER", "ACTIVE", True),
        )
        for effect, scope, regime, mechanism, lifecycle, expected in rows:
            core = support.build_semantic_core()
            claim = core["claims"][0]
            axes = (claim["modality"], copy.deepcopy(claim["evidence"]))
            if effect != "NONE":
                self.configure_authority(
                    claim, effect=effect, scope=scope, regime=regime,
                    mechanism=mechanism, lifecycle=lifecycle,
                )
            issues = validate(core)
            with self.subTest(effect=effect, scope=scope, mechanism=mechanism):
                self.assertEqual("KIN-E-JUSTICE" not in codes(issues), expected)
                self.assertEqual((claim["modality"], claim["evidence"]), axes if lifecycle == "ACTIVE" else (axes[0], claim["evidence"]))

    def test_none_authority_uses_absence_or_exact_not_applicable_context(self):
        absent = support.build_semantic_core()
        self.assertEqual(validate(absent), [])

        collective = support.build_semantic_core()
        claim = collective["claims"][0]
        claim.update({
            "justiceScope": "COLLECTIVE",
            "justiceContext": support.build_justice_context("NOT_APPLICABLE", "NONE"),
        })
        self.assertEqual(validate(collective), [])
        claim["justiceContext"]["authority"] = {
            "regime": "PRIVATE_DAV", "mechanism": "K2_NATURAL_PERSON", "basis": "Fabricated gate.",
        }
        self.assertIn("KIN-E-JUSTICE", codes(validate(collective)))

        missing = support.build_semantic_core()
        self.configure_authority(
            missing["claims"][0], effect="CONSEQUENTIAL", scope="PUBLIC_DAV",
            regime="PUBLIC_DAV", mechanism="PRISM_PUBLIC_GOVERNANCE",
        )
        del missing["claims"][0]["justiceContext"]
        self.assertIn("KIN-E-JUSTICE", codes(validate(missing)))

    def test_justice_context_requires_every_typed_person_whole_and_exit_field(self):
        core = support.build_semantic_core()
        claim = core["claims"][0]
        claim.update({
            "justiceScope": "COLLECTIVE",
            "justiceContext": {
                "authority": {
                    "regime": "NOT_APPLICABLE",
                    "mechanism": "NONE",
                    "basis": "An incomplete context must not pass.",
                },
            },
        })
        self.assertIn("KIN-E-JUSTICE", codes(validate(core)))

    def test_draft_and_terminal_receipts_own_gate_state_and_paths(self):
        draft = support.build_semantic_core()
        seam = support.add_confirmed_seam(draft)
        self.assertEqual(validate(draft), [])
        seam["truthGate"] = {
            "status": "PASS", "rationale": "Premature pass.", "reviewerPath": "review.md",
        }
        self.assertIn("KIN-E-STATE", codes(validate(draft)))

        for verified in (False, True):
            core = support.build_semantic_core()
            seam = complete_receipt_with_seam(core, verified=verified)
            with self.subTest(verified=verified):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
                self.assertEqual(validate(core), [])
            seam["beautyGate"]["reviewerPath"] = core["phaseReceipts"][0]["logicReviewPath"]
            self.assertIn("KIN-E-STATE", codes(validate(core)))

    def test_held_open_seam_requires_containment_risk_and_discriminator(self):
        core = support.build_semantic_core()
        seam = support.add_confirmed_seam(core)
        seam["status"] = "HELD_OPEN"
        self.assertIn("KIN-E-STATE", codes(validate(core)))

    def test_public_queue_owned_and_ownerless_unions_resolve_purely(self):
        core, queue = make_queue_core()
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", queue), [])
        self.assertEqual(validate_queue(queue, core), [])

        ownerless = copy.deepcopy(queue)
        ownerless["items"] = [make_ownerless_item(core)]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", ownerless), [])
        self.assertEqual(validate_queue(ownerless, core), [])

        mutations = []
        bad_manifest = copy.deepcopy(queue)
        bad_manifest["manifestId"] = "MAN-C-999"
        mutations.append(("manifest", bad_manifest))
        wrong_owner = copy.deepcopy(queue)
        wrong_owner["items"][0]["ownerSourceId"] = core["sources"][1]["id"]
        mutations.append(("owned claim membership", wrong_owner))
        incomplete = copy.deepcopy(ownerless)
        incomplete["items"][0]["ownerSearchEvidence"]["searchedSourceIds"].pop()
        mutations.append(("complete owner search", incomplete))
        bad_candidate = copy.deepcopy(ownerless)
        bad_candidate["items"][0]["candidateOwners"] = ["not/in/search.md"]
        mutations.append(("candidate membership", bad_candidate))
        bad_action = copy.deepcopy(ownerless)
        bad_action["items"][0]["requiredAction"] = "KEEP"
        mutations.append(("ownerless disposition", bad_action))
        ineligible_owner = copy.deepcopy(queue)
        owner_id = ineligible_owner["items"][0]["ownerSourceId"]
        next(source for source in core["sources"] if source["id"] == owner_id)["phases"] = ["A"]
        mutations.append(("owner outside manifest", ineligible_owner))
        for label, mutated in mutations:
            with self.subTest(label=label):
                self.assertIn("KIN-E-QUEUE", codes(validate_queue(mutated, core)))

    def test_public_queue_closes_manifest_receipt_owner_and_evidence_boundaries(self):
        core, queue = make_queue_core()
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])

        rows = []
        absent_public = copy.deepcopy(queue)
        absent_public["items"][0]["publicFile"] = "12_PUBLIC_SITE/not-in-manifest.html"
        rows.append(("public file inventory", core, absent_public))

        wrong_receipt_path = copy.deepcopy(core)
        wrong_receipt_path["phaseReceipts"][0]["path"] = "11_UPLINK/wrong-receipt.md"
        rows.append(("canonical receipt identity", wrong_receipt_path, copy.deepcopy(queue)))

        wrong_seam_core = copy.deepcopy(core)
        seam = support.add_confirmed_seam(wrong_seam_core)
        seam["claimId"] = wrong_seam_core["claims"][1]["id"]
        seam["ownerSource"] = wrong_seam_core["claims"][1]["ownerSourceId"]
        wrong_seam_queue = copy.deepcopy(queue)
        wrong_seam_queue["items"][0]["seamIds"] = [seam["id"]]
        rows.append(("same claim and owner seam", wrong_seam_core, wrong_seam_queue))

        weak_owner = copy.deepcopy(core)
        weak_owner["claims"][0]["evidence"]["strength"] = "C"
        over_maximum = copy.deepcopy(queue)
        over_maximum["items"][0]["currentEvidence"]["strength"] = "C"
        rows.append(("maximum bounded by owner", weak_owner, over_maximum))
        over_current = copy.deepcopy(queue)
        over_current["items"][0]["maximumPublicStrength"] = "A"
        rows.append(("current bounded by owner", weak_owner, over_current))

        for label, candidate_core, candidate_queue in rows:
            with self.subTest(label=label):
                if label != "canonical receipt identity":
                    self.assertEqual(
                        kernel.validate_schema_instance(SCHEMA, "coreData", candidate_core), []
                    )
                else:
                    self.assertTrue(
                        kernel.validate_schema_instance(SCHEMA, "coreData", candidate_core)
                    )
                self.assertEqual(
                    kernel.validate_schema_instance(SCHEMA, "publicQueue", candidate_queue), []
                )
                self.assertIn("KIN-E-QUEUE", codes(validate_queue(candidate_queue, candidate_core)))

    def test_owned_public_claim_must_be_harvested_by_the_selected_phase_c_manifest(self):
        core, queue = make_queue_core()
        claim_id = queue["items"][0]["claimId"]
        manifest = core["manifests"][0]
        manifest["harvestedClaimIds"].remove(claim_id)
        manifest["trialedClaimIds"].remove(claim_id)
        manifest["eligibleClaimCount"] -= 1
        manifest["trialedClaimCount"] -= 1
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", queue), [])
        self.assertIn("KIN-E-QUEUE", codes(validate_queue(queue, core)))

    def test_ownerless_candidates_are_bounded_to_searched_semantic_owners(self):
        core, queue = make_queue_core()
        derivative = copy.deepcopy(core["sources"][0])
        derivative.update({
            "id": "SRC-C-999",
            "kind": "SUPPORT",
            "authorityRole": "PROVENANCE",
            "path": "05_COSMOLOGY/derivative-source.md",
        })
        core["sources"].append(derivative)
        core["manifests"][0]["includedFiles"].append({
            "path": derivative["path"], "kind": "FILE", "sha256": support.RAW_HASH,
        })
        ownerless = make_ownerless_item(core)
        ownerless["ownerSearchEvidence"]["searchedSourceIds"] = [derivative["id"]]
        ownerless["candidateOwners"] = [derivative["path"]]
        queue["items"] = [ownerless]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", queue), [])
        self.assertIn("KIN-E-QUEUE", codes(validate_queue(queue, core)))

    def test_public_queue_boundary_is_total_for_bounded_json_shape_mutations(self):
        core, queue = make_queue_core()
        scalar_shapes = (None, False, 0, 1.5, "", [], {})

        for malformed in scalar_shapes:
            with self.subTest(surface="queue", shape=type(malformed).__name__):
                self.assertStableQueueFailure(malformed, core)
            with self.subTest(surface="core", shape=type(malformed).__name__):
                self.assertStableQueueFailure(queue, malformed)

        queue_scalar_paths = (
            ("manifestId",),
            ("receiptId",),
            ("items", 0, "publicFile"),
            ("items", 0, "ownerSourceId"),
            ("items", 0, "claimId"),
            ("items", 0, "maximumPublicStrength"),
        )
        for path in queue_scalar_paths:
            for malformed in scalar_shapes:
                candidate = replace_path(queue, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableQueueFailure(candidate, core)

        for path in (("items",), ("items", 0, "currentEvidence"), ("items", 0, "seamIds")):
            for malformed in (None, False, 0, 1.5, "", {}, [None], [{}]):
                candidate = replace_path(queue, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableQueueFailure(candidate, core)

        ownerless = copy.deepcopy(queue)
        ownerless["items"] = [make_ownerless_item(core)]
        ownerless_paths = (
            ("items", 0, "ownerSearchEvidence"),
            ("items", 0, "ownerSearchEvidence", "manifestIds"),
            ("items", 0, "ownerSearchEvidence", "searchedSourceIds"),
            ("items", 0, "candidateOwners"),
        )
        for path in ownerless_paths:
            for malformed in (None, False, 0, 1.5, "", {}, [None], [{}]):
                candidate = replace_path(ownerless, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableQueueFailure(candidate, core)


class SafeRegexGlobAndAntibodyTests(unittest.TestCase):
    def assertStableFixtureFailure(self, core, fixture_id):
        first = evaluate_fixture(copy.deepcopy(core), copy.deepcopy(fixture_id))
        second = evaluate_fixture(copy.deepcopy(core), copy.deepcopy(fixture_id))
        self.assertTrue(first)
        self.assertEqual(issue_signature(first), issue_signature(second))
        self.assertTrue(all(issue.code == "KIN-E-FIXTURE" for issue in first))

    def assertStableScanFailure(self, core, documents):
        first_result, first_issues = scan(copy.deepcopy(core), copy.deepcopy(documents))
        second_result, second_issues = scan(copy.deepcopy(core), copy.deepcopy(documents))
        empty = {"included": {}, "excluded": {}, "triggers": {}}
        self.assertEqual(first_result, empty)
        self.assertEqual(second_result, empty)
        self.assertTrue(first_issues)
        self.assertEqual(issue_signature(first_issues), issue_signature(second_issues))
        self.assertTrue(all(issue.code == "KIN-E-FIXTURE" for issue in first_issues))

    def test_complete_safe_regex_grammar_and_anchors(self):
        positives = (
            ("abc", "xxabczz"),
            ("^abc$", "abc"),
            ("a.c", "aβc"),
            ("(ab|cd)+", "xxabcdcdyy"),
            ("ab?c", "ac"),
            ("ab*c", "abbbc"),
            ("ab+c", "abc"),
            ("[a-c]+", "zzabcczz"),
            ("[^a]+", "aaaββaaa"),
            ("[α-ω]+", "--αλφα--"),
            (r"\.\^\$\|\?\*\+\(\)\[\]\-\\", ".^$|?*+()[]-\\"),
            ("a{2}", "xxa{2}yy"),
            ("a*", "anything"),
        )
        negatives = (
            ("^abc$", "xabc"),
            ("a.c", "a\nc"),
            ("[a-c]+", "xyz"),
        )
        for pattern, source in positives:
            with self.subTest(pattern=pattern, result=True):
                matched, issues = regex_search(pattern, source)
                self.assertEqual(issues, [])
                self.assertTrue(matched)
        for pattern, source in negatives:
            with self.subTest(pattern=pattern, result=False):
                matched, issues = regex_search(pattern, source)
                self.assertEqual(issues, [])
                self.assertFalse(matched)

    def test_invalid_regex_corpus_fails_closed(self):
        invalid = (
            "", "a|", "|a", "a||b", "()", "(", ")", "[", "[]", "[z-a]",
            "\\", r"\d", "a^b", "a$b", "*a", "a??", "a[--b]",
            "a" * 257,
        )
        for pattern in invalid:
            with self.subTest(pattern=pattern[:20]):
                matched, issues = regex_search(pattern, "aaaa")
                self.assertFalse(matched)
                self.assertIn("KIN-E-FIXTURE", codes(issues))

        matched, issues = regex_search("a", "\ud800")
        self.assertFalse(matched)
        self.assertIn("KIN-E-FIXTURE", codes(issues))

    def test_nested_quantifier_near_match_uses_bounded_state_sets(self):
        matched, issues = regex_search("(a+)+$", "a" * 20000 + "!")
        self.assertEqual(issues, [])
        self.assertFalse(matched)

    def test_safe_segment_globs_scope_exclude_and_live_quotation_visibility(self):
        core = support.build_semantic_core()
        support.add_antibody_fixture_set(core)
        documents = {
            "active/a.md": "forbidden",
            "active/nested/b.md": "A quotation says forbidden.",
            "active/excluded/c.md": "forbidden",
            "other/d.md": "forbidden",
            "active/clean.md": "clean",
        }
        result, issues = scan(core, documents)
        self.assertEqual(issues, [])
        self.assertEqual(result["included"], {
            "AB-LITERAL-001": (
                "active/a.md", "active/clean.md", "active/excluded/c.md",
                "active/nested/b.md",
            ),
        })
        self.assertEqual(result["excluded"], {
            "AB-LITERAL-001": ("active/excluded/c.md",),
        })
        self.assertEqual(result["triggers"], {
            "active/a.md": ("AB-LITERAL-001",),
            "active/clean.md": (),
            "active/nested/b.md": ("AB-LITERAL-001",),
        })

    def test_invalid_safe_globs_and_utf8_fail_fixture_execution(self):
        invalid = (
            "/absolute/**", "a\\b", "a//b", "a/./b", "a/../b", "a/?/b",
            "a/[x]/b", "a/**x/b", "a/", "a/{x,y}.md", "a/!(x).md",
            "a/@(x).md", "a/+(x).md", "a/*(x).md",
        )
        for pattern in invalid:
            core = support.build_semantic_core()
            antibody = support.add_antibody_fixture_set(core)
            antibody["scopeGlobs"] = [pattern]
            with self.subTest(pattern=pattern):
                _, issues = scan(core, {"a/x/b": "forbidden"})
                self.assertIn("KIN-E-FIXTURE", codes(issues))

        core = support.build_semantic_core()
        support.add_antibody_fixture_set(core)
        _, issues = scan(core, {"active/bad.md": b"\xff"})
        self.assertIn("KIN-E-FIXTURE", codes(issues))

    def test_glob_matching_is_iterative_and_scan_inputs_are_total_unicode_scalars(self):
        core = support.build_semantic_core()
        antibody = support.add_antibody_fixture_set(core)
        antibody["scopeGlobs"] = ["**"]
        long_path = "/".join(["a"] * 1200)
        result, issues = scan(core, {long_path: "forbidden"})
        self.assertEqual(issues, [])
        self.assertEqual(result["included"][antibody["id"]], (long_path,))
        self.assertEqual(result["triggers"][long_path], (antibody["id"],))

        malformed = (
            ({"active/\ud800.md": "forbidden"}, "surrogate path"),
            ({"active/a.md": "\ud800"}, "surrogate source"),
            ({1: "forbidden"}, "non-text path"),
            ({"active/a.md": object()}, "non-text source"),
        )
        for documents, label in malformed:
            with self.subTest(label=label):
                _, malformed_issues = scan(core, documents)
                self.assertIn("KIN-E-FIXTURE", codes(malformed_issues))

        positive_id = antibody["positiveFixtureIds"][0]
        fixture = next(item for item in core["fixtures"] if item["id"] == positive_id)
        fixture["payload"] = 7
        self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, positive_id)))
        fixture["payload"] = "\ud800"
        self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, positive_id)))

    def test_literal_regex_and_all_fixture_contexts_dispatch_exactly_once(self):
        for mode, pattern in (("LITERAL", "forbidden"), ("REGEX", "for+bidden")):
            core = support.build_semantic_core()
            antibody = support.add_antibody_fixture_set(core, match_mode=mode, pattern=pattern)
            for kind, field in (
                ("POSITIVE", "positiveFixtureIds"),
                ("NEGATIVE", "negativeFixtureIds"),
                ("QUOTATION", "quotationFixtureIds"),
                ("HISTORICAL", "historicalFixtureIds"),
            ):
                with self.subTest(mode=mode, kind=kind):
                    self.assertEqual(evaluate_fixture(core, antibody[field][0]), [])
            antibody["negativeFixtureIds"] = antibody["positiveFixtureIds"][:]
            self.assertIn(
                "KIN-E-FIXTURE",
                codes(validate(core)),
            )

    def test_fixture_context_registration_is_exactly_once(self):
        core = support.build_semantic_core()
        antibody = support.add_antibody_fixture_set(core)
        fixture_id = antibody["positiveFixtureIds"][0]
        antibody["negativeFixtureIds"].append(fixture_id)
        self.assertIn("KIN-E-FIXTURE", codes(validate(core)))

    def test_fixture_boundary_is_total_for_bounded_json_shape_mutations(self):
        core = support.build_semantic_core()
        antibody = support.add_antibody_fixture_set(core)
        fixture_id = antibody["positiveFixtureIds"][0]
        scalar_shapes = (None, False, 0, 1.5, "", [], {})

        for malformed in scalar_shapes:
            with self.subTest(surface="core", shape=type(malformed).__name__):
                self.assertStableFixtureFailure(malformed, fixture_id)
            with self.subTest(surface="fixtureId", shape=type(malformed).__name__):
                self.assertStableFixtureFailure(core, malformed)

        paths = (
            ("antibodies", 0, "id"),
            ("antibodies", 0, "matchMode"),
            ("antibodies", 0, "pattern"),
            ("fixtures", 1, "id"),
            ("fixtures", 1, "kind"),
            ("fixtures", 1, "payloadKind"),
            ("fixtures", 1, "payload"),
        )
        positive_position = next(
            position for position, fixture in enumerate(core["fixtures"])
            if fixture.get("id") == fixture_id
        )
        normalized_paths = tuple(
            path if path[:2] != ("fixtures", 1)
            else ("fixtures", positive_position, *path[2:])
            for path in paths
        )
        for path in normalized_paths:
            for malformed in scalar_shapes:
                candidate = replace_path(core, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableFixtureFailure(candidate, fixture_id)

        list_paths = (
            ("antibodies", 0, "scopeGlobs"),
            ("antibodies", 0, "excludeGlobs"),
            ("fixtures", positive_position, "antibodyIds"),
            ("fixtures", positive_position, "expectedAntibodyIds"),
        )
        for path in list_paths:
            for malformed in (None, False, 0, 1.5, "", {}, [None], [{}]):
                candidate = replace_path(core, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableFixtureFailure(candidate, fixture_id)

        semantic_core = support.build_semantic_core()
        payload = {
            "physicalConstraint": "C_BOUNDED",
            "optionClaim": "MODELED_REACHABILITY",
            "futureInfluence": "ANTICIPATORY_MODEL",
            "commitmentKind": "PARTIAL_RELATION",
        }
        forbidden = copy.deepcopy(payload)
        forbidden["physicalConstraint"] = "SUPERLUMINAL"
        semantic = support.add_semantic_antibody_fixture_set(
            semantic_core, "OPTION_CONE", payload, forbidden
        )
        semantic_fixture_id = semantic["positiveFixtureIds"][0]
        for malformed in scalar_shapes:
            candidate = replace_path(
                semantic_core, ("antibodies", 0, "semanticEvaluator"), malformed
            )
            with self.subTest(path="semanticEvaluator", shape=type(malformed).__name__):
                self.assertStableFixtureFailure(candidate, semantic_fixture_id)

    def test_scan_boundary_is_total_for_bounded_json_shape_mutations(self):
        core = support.build_semantic_core()
        support.add_antibody_fixture_set(core)
        documents = {"active/a.md": "forbidden"}

        for malformed in (None, False, 0, 1.5, "", []):
            with self.subTest(surface="core", shape=type(malformed).__name__):
                self.assertStableScanFailure(malformed, documents)
            with self.subTest(surface="documents", shape=type(malformed).__name__):
                self.assertStableScanFailure(core, malformed)

        scalar_paths = (
            ("antibodies", 0, "id"),
            ("antibodies", 0, "matchMode"),
            ("antibodies", 0, "pattern"),
        )
        for path in scalar_paths:
            malformed_values = (None, False, 0, 1.5, "", [], {})
            if path[-1] != "pattern":
                malformed_values += ("bad id",)
            for malformed in malformed_values:
                candidate = replace_path(core, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableScanFailure(candidate, documents)

        for path in (("antibodies", 0, "scopeGlobs"), ("antibodies", 0, "excludeGlobs")):
            for malformed in (None, False, 0, 1.5, "", {}, [None], [{}]):
                candidate = replace_path(core, path, malformed)
                with self.subTest(path=path, shape=type(malformed).__name__):
                    self.assertStableScanFailure(candidate, documents)

        for malformed in (None, False, 0, 1.5, [], {}):
            with self.subTest(documentValue=type(malformed).__name__):
                self.assertStableScanFailure(core, {"active/a.md": malformed})
        for path in ("", "/absolute/a.md", "active/../a.md", "active/\ud800.md"):
            with self.subTest(documentPath=repr(path)):
                self.assertStableScanFailure(core, {path: "forbidden"})

    def test_semantics_public_boundaries_do_not_swallow_process_control(self):
        class RaisingDict(dict):
            signal = KeyboardInterrupt

            def get(self, *args, **kwargs):
                raise self.signal("process-control probe")

        for signal in (KeyboardInterrupt, SystemExit):
            RaisingDict.signal = signal
            with self.subTest(signal=signal.__name__, boundary="fixture"):
                with self.assertRaises(signal):
                    evaluate_fixture(RaisingDict(), "FXT-A-001")
            with self.subTest(signal=signal.__name__, boundary="scan"):
                with self.assertRaises(signal):
                    scan(RaisingDict(), {})
            with self.subTest(signal=signal.__name__, boundary="queue"):
                with self.assertRaises(signal):
                    validate_queue(RaisingDict(), RaisingDict())


class SemanticEvaluatorTests(unittest.TestCase):
    def payload_rows(self, core):
        claim_id = core["claims"][0]["id"]
        source_path = core["sources"][0]["path"]
        return {
            "VERDICT_MATRIX": (
                {"validityVerdict": "VALID", "soundnessVerdict": "SUPPORTED", "verdict": "VALID_SOUND"},
                {"validityVerdict": "INVALID", "soundnessVerdict": "SUPPORTED", "verdict": "VALID_SOUND"},
            ),
            "JUSTICE_CONTEXT": (
                {
                    "claimType": "STRUCTURAL", "modality": "ACTUAL", "justiceScope": "NONE",
                    "authorityScope": "NONE", "authorityEffect": "NONE",
                    "evidenceLifecycle": "ACTIVE", "justiceContext": None,
                },
                {
                    "claimType": "NORMATIVE", "modality": "NORMATIVE", "justiceScope": "NONE",
                    "authorityScope": "NONE", "authorityEffect": "NONE",
                    "evidenceLifecycle": "ACTIVE", "justiceContext": None,
                },
            ),
            "RECEIPT_ROLE": (
                {
                    "recordKind": "SOURCE_RECORD", "sourceKind": "SUPPORT", "authorityRole": "PROVENANCE",
                    "receiptId": None, "phase": None, "path": source_path, "status": None,
                    "requestedUse": "PROVENANCE",
                },
                {
                    "recordKind": "SOURCE_RECORD", "sourceKind": "RECEIPT", "authorityRole": "PROVENANCE",
                    "receiptId": None, "phase": None, "path": source_path, "status": None,
                    "requestedUse": "EVIDENCE_UPGRADE",
                },
            ),
            "REGISTER_INDEX": (
                {
                    "symbol": "x", "fromRegister": "D4", "toRegister": "D5",
                    "relation": "DISTINCT_TYPED_TERM", "bridgeClaimId": None,
                    "requestedInference": "TYPED_REFERENCE",
                },
                {
                    "symbol": "x", "fromRegister": "D4", "toRegister": "D5",
                    "relation": "UNMARKED_SUBSTITUTION", "bridgeClaimId": None,
                    "requestedInference": "ENTAILMENT",
                },
            ),
            "QUANTUM_MEASURE": (
                {
                    "probabilityObject": "EVENT_MEASURE", "requestedOperation": "SAMPLE_OUTCOME",
                    "interpretiveClaim": "CORRESPONDENCE",
                },
                {
                    "probabilityObject": "NORMALIZATION_SCALAR", "requestedOperation": "SAMPLE_OUTCOME",
                    "interpretiveClaim": "LITERAL_EXTRA_DIMENSION",
                },
            ),
            "OPTION_CONE": (
                {
                    "physicalConstraint": "C_BOUNDED", "optionClaim": "MODELED_REACHABILITY",
                    "futureInfluence": "ANTICIPATORY_MODEL", "commitmentKind": "PARTIAL_RELATION",
                },
                {
                    "physicalConstraint": "SUPERLUMINAL", "optionClaim": "PHYSICAL_CONE_EXPANSION",
                    "futureInfluence": "PHYSICAL_RETROCAUSALITY", "commitmentKind": "TOTAL_PREDICTOR",
                },
            ),
            "TROPHIC_AGGREGATOR": (
                {
                    "quantityKind": "HUMAN_INVESTMENT_PROXY", "aggregationBasis": "DECLARED_PROXY",
                    "conservationClaim": "NONE", "persistentSharedTrace": True,
                    "carrierTurnoverObserved": True, "laterSelectionReweightingObserved": True,
                    "requestedInference": "EGREGOREOTYPE_CANDIDATE",
                },
                {
                    "quantityKind": "PHYSICAL_ENERGY", "aggregationBasis": "METAPHORICAL",
                    "conservationClaim": "ASSUMED", "persistentSharedTrace": False,
                    "carrierTurnoverObserved": False, "laterSelectionReweightingObserved": False,
                    "requestedInference": "LITERAL_ENERGY_LAW",
                },
            ),
            "ROSETTA_TRANSFER": (
                {
                    "targetClaimId": claim_id, "bridgeClaimId": None,
                    "fromRegister": "D4", "toRegister": "D5", "requestedTransfer": "TOPOLOGY",
                },
                {
                    "targetClaimId": claim_id, "bridgeClaimId": core["claims"][1]["id"],
                    "fromRegister": "D4", "toRegister": "D5", "requestedTransfer": "EVIDENCE_UPGRADE",
                },
            ),
        }

    def test_all_eight_closed_evaluators_have_positive_and_negative_rows(self):
        core = support.build_semantic_core()
        for evaluator, (good, bad) in self.payload_rows(core).items():
            with self.subTest(evaluator=evaluator, row="positive"):
                self.assertEqual(evaluate(evaluator, good, core), [])
            with self.subTest(evaluator=evaluator, row="negative"):
                self.assertTrue(semantic_issue(evaluate(evaluator, bad, core)))

    def test_verdict_matrix_is_exhaustive_and_bidirectional(self):
        valid = {
            "VALID_SOUND": [("VALID", "SUPPORTED")],
            "VALID_CONDITIONAL": [("VALID", "CONDITIONALLY_SUPPORTED")],
            "VALID_UNSUPPORTED_PREMISE": [("VALID", "UNSUPPORTED")],
            "INVALID": [("INVALID", "NOT_APPLICABLE")],
            "UNDERDETERMINED": [("INVALID", "NOT_APPLICABLE")],
            "DEFINITIONAL": [("NOT_APPLICABLE", "NOT_APPLICABLE")],
            "OPEN_CONJECTURE": [("NOT_APPLICABLE", "UNSUPPORTED"), ("NOT_APPLICABLE", "CONDITIONALLY_SUPPORTED")],
            "REFUTED": [("VALID", "REFUTED"), ("NOT_APPLICABLE", "REFUTED")],
        }
        core = support.build_semantic_core()
        for verdict, pairs in valid.items():
            for validity, soundness in pairs:
                payload = {"validityVerdict": validity, "soundnessVerdict": soundness, "verdict": verdict}
                with self.subTest(verdict=verdict, validity=validity, soundness=soundness):
                    self.assertEqual(evaluate("VERDICT_MATRIX", payload, core), [])
            invalid = {"validityVerdict": "VALID", "soundnessVerdict": "SUPPORTED", "verdict": verdict}
            if ("VALID", "SUPPORTED") not in pairs:
                self.assertTrue(semantic_issue(evaluate("VERDICT_MATRIX", invalid, core)))

    def test_rosetta_allows_correspondence_only_even_with_a_bridge(self):
        core = support.build_semantic_core()
        for requested in ("VOCABULARY", "QUESTION", "TOPOLOGY"):
            payload = {
                "targetClaimId": core["claims"][0]["id"],
                "bridgeClaimId": core["claims"][1]["id"],
                "fromRegister": "D4", "toRegister": "D5", "requestedTransfer": requested,
            }
            self.assertEqual(evaluate("ROSETTA_TRANSFER", payload, core), [])
        for requested in ("ENTAILMENT", "MECHANISM", "NECESSITY", "EVIDENCE_UPGRADE"):
            payload["requestedTransfer"] = requested
            with self.subTest(requested=requested):
                self.assertTrue(semantic_issue(evaluate("ROSETTA_TRANSFER", payload, core)))
        payload["requestedTransfer"] = "TOPOLOGY"
        payload["bridgeClaimId"] = "CLM-A-999"
        self.assertTrue(semantic_issue(evaluate("ROSETTA_TRANSFER", payload, core)))

    def test_payload_keys_are_closed_and_semantic_antibody_dispatch_is_structural_only(self):
        core = support.build_semantic_core()
        good, bad = self.payload_rows(core)["OPTION_CONE"]
        extra = copy.deepcopy(good)
        extra["proof"] = True
        self.assertTrue(semantic_issue(evaluate("OPTION_CONE", extra, core)))

        antibody = support.add_semantic_antibody_fixture_set(core, "OPTION_CONE", good, bad)
        for field in (
            "positiveFixtureIds", "negativeFixtureIds", "quotationFixtureIds", "historicalFixtureIds",
        ):
            self.assertEqual(evaluate_fixture(core, antibody[field][0]), [])

        negative_id = antibody["negativeFixtureIds"][0]
        negative = next(fixture for fixture in core["fixtures"] if fixture["id"] == negative_id)
        negative["payload"] = (
            '{"physicalConstraint":"SUPERLUMINAL","physicalConstraint":"C_BOUNDED",'
            '"optionClaim":"MODELED_REACHABILITY","futureInfluence":"ANTICIPATORY_MODEL",'
            '"commitmentKind":"PARTIAL_RELATION"}'
        )
        self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, negative_id)))

    def test_every_semantic_payload_field_matches_its_named_schema_definition(self):
        core = support.build_semantic_core()
        definition_names = {
            "VERDICT_MATRIX": "verdictMatrixPayload",
            "JUSTICE_CONTEXT": "justiceContextPayload",
            "RECEIPT_ROLE": "receiptRolePayload",
            "REGISTER_INDEX": "registerIndexPayload",
            "QUANTUM_MEASURE": "quantumMeasurePayload",
            "OPTION_CONE": "optionConePayload",
            "TROPHIC_AGGREGATOR": "trophicAggregatorPayload",
            "ROSETTA_TRANSFER": "rosettaTransferPayload",
        }
        invalid_values = {
            "VERDICT_MATRIX": {
                "validityVerdict": None, "soundnessVerdict": [], "verdict": "UNKNOWN",
            },
            "JUSTICE_CONTEXT": {
                "claimType": None, "modality": [], "justiceScope": {},
                "authorityScope": 0, "authorityEffect": False,
                "evidenceLifecycle": "UNKNOWN", "justiceContext": [],
            },
            "RECEIPT_ROLE": {
                "recordKind": None, "sourceKind": [], "authorityRole": {},
                "receiptId": [], "phase": {}, "path": None, "status": [],
                "requestedUse": 0,
            },
            "REGISTER_INDEX": {
                "symbol": None, "fromRegister": None, "toRegister": {},
                "relation": [], "bridgeClaimId": [], "requestedInference": 0,
            },
            "QUANTUM_MEASURE": {
                "probabilityObject": None, "requestedOperation": [],
                "interpretiveClaim": {},
            },
            "OPTION_CONE": {
                "physicalConstraint": None, "optionClaim": [],
                "futureInfluence": {}, "commitmentKind": 0,
            },
            "TROPHIC_AGGREGATOR": {
                "quantityKind": None, "aggregationBasis": [],
                "conservationClaim": {}, "persistentSharedTrace": "true",
                "carrierTurnoverObserved": None,
                "laterSelectionReweightingObserved": 1,
                "requestedInference": False,
            },
            "ROSETTA_TRANSFER": {
                "targetClaimId": None, "bridgeClaimId": [],
                "fromRegister": {}, "toRegister": 0, "requestedTransfer": False,
            },
        }
        for evaluator, (good, _) in self.payload_rows(core).items():
            definition = definition_names[evaluator]
            self.assertEqual(kernel.validate_named_definition(SCHEMA, definition, good), [])
            for field, invalid in invalid_values[evaluator].items():
                payload = copy.deepcopy(good)
                payload[field] = invalid
                with self.subTest(evaluator=evaluator, field=field):
                    self.assertTrue(
                        kernel.validate_named_definition(SCHEMA, definition, payload)
                    )
                    self.assertTrue(semantic_issue(evaluate(evaluator, payload, core)))

    def test_outer_fixture_json_string_cannot_hide_an_invalid_named_payload(self):
        core = support.build_semantic_core()
        good, bad = self.payload_rows(core)["REGISTER_INDEX"]
        antibody = support.add_semantic_antibody_fixture_set(
            core, "REGISTER_INDEX", good, bad
        )
        fixture_id = antibody["negativeFixtureIds"][0]
        fixture = next(item for item in core["fixtures"] if item["id"] == fixture_id)
        fixture["payload"] = json.dumps({
            "symbol": None,
            "fromRegister": None,
            "toRegister": {},
            "relation": "DISTINCT_TYPED_TERM",
            "bridgeClaimId": None,
            "requestedInference": "TYPED_REFERENCE",
        }, sort_keys=True, separators=(",", ":"))
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, fixture_id)))
        self.assertIn("KIN-E-FIXTURE", codes(validate(core)))

    def test_wrong_shaped_payload_is_execution_failure_in_every_fixture_context(self):
        contexts = (
            ("POSITIVE", "positiveFixtureIds"),
            ("NEGATIVE", "negativeFixtureIds"),
            ("QUOTATION", "quotationFixtureIds"),
            ("HISTORICAL", "historicalFixtureIds"),
        )
        for evaluator in self.payload_rows(support.build_semantic_core()):
            for context, fixture_field in contexts:
                core = support.build_semantic_core()
                good, bad = self.payload_rows(core)[evaluator]
                antibody = support.add_semantic_antibody_fixture_set(
                    core, evaluator, good, bad
                )
                fixture_id = antibody[fixture_field][0]
                fixture = next(
                    item for item in core["fixtures"] if item["id"] == fixture_id
                )
                fixture["payload"] = "{}"
                with self.subTest(evaluator=evaluator, context=context):
                    self.assertEqual(
                        kernel.validate_schema_instance(SCHEMA, "coreData", core), []
                    )
                    self.assertIn(
                        "KIN-E-FIXTURE",
                        codes(evaluate_fixture(core, fixture_id)),
                    )
                    self.assertIn("KIN-E-FIXTURE", codes(validate(core)))

    def test_justice_nested_enums_are_exception_total_for_lists_and_objects(self):
        core = support.build_semantic_core()
        payload = {
            "claimType": "STRUCTURAL",
            "modality": "ACTUAL",
            "justiceScope": "COLLECTIVE",
            "authorityScope": "NONE",
            "authorityEffect": "NONE",
            "evidenceLifecycle": "ACTIVE",
            "justiceContext": support.build_justice_context(),
        }
        enum_paths = (
            ("consent", "status"),
            ("reversibility",),
            ("optionConeEffect", "direction"),
            ("authority", "regime"),
            ("authority", "mechanism"),
        )
        for path in enum_paths:
            for wrong_type in ([], {}):
                mutated = copy.deepcopy(payload)
                cursor = mutated["justiceContext"]
                for component in path[:-1]:
                    cursor = cursor[component]
                cursor[path[-1]] = wrong_type
                with self.subTest(path=path, wrong_type=type(wrong_type).__name__):
                    self.assertTrue(semantic_issue(evaluate("JUSTICE_CONTEXT", mutated, core)))

                fixture_core = support.build_semantic_core()
                antibody = support.add_semantic_antibody_fixture_set(
                    fixture_core, "JUSTICE_CONTEXT", payload, mutated
                )
                fixture_id = antibody["negativeFixtureIds"][0]
                fixture = next(
                    item for item in fixture_core["fixtures"] if item["id"] == fixture_id
                )
                fixture["payload"] = json.dumps(
                    mutated, sort_keys=True, separators=(",", ":")
                )
                with self.subTest(
                    path=path, wrong_type=type(wrong_type).__name__, boundary="decoded fixture"
                ):
                    self.assertEqual(
                        kernel.validate_schema_instance(SCHEMA, "coreData", fixture_core), []
                    )
                    self.assertIn(
                        "KIN-E-FIXTURE", codes(evaluate_fixture(fixture_core, fixture_id))
                    )

    def test_every_nested_justice_text_leaf_rejects_lone_surrogates(self):
        core = support.build_semantic_core()
        base = {
            "claimType": "STRUCTURAL",
            "modality": "ACTUAL",
            "justiceScope": "COLLECTIVE",
            "authorityScope": "NONE",
            "authorityEffect": "NONE",
            "evidenceLifecycle": "ACTIVE",
            "justiceContext": support.build_justice_context(),
        }
        text_paths = (
            ("individual",),
            ("whole",),
            ("eta",),
            ("beneficiary", 0),
            ("costBearer", 0),
            ("consent", "basis"),
            ("custody",),
            ("exit",),
            ("optionConeEffect", "rationale"),
            ("authority", "basis"),
        )
        for path in text_paths:
            mutated = copy.deepcopy(base)
            cursor = mutated["justiceContext"]
            for component in path[:-1]:
                cursor = cursor[component]
            cursor[path[-1]] = "\ud800"
            with self.subTest(path=path, boundary="direct mirror"):
                self.assertTrue(semantic_issue(evaluate("JUSTICE_CONTEXT", mutated, core)))

            fixture_core = support.build_semantic_core()
            good = copy.deepcopy(base)
            bad = copy.deepcopy(mutated)
            antibody = support.add_semantic_antibody_fixture_set(
                fixture_core, "JUSTICE_CONTEXT", good, bad
            )
            fixture_id = antibody["negativeFixtureIds"][0]
            fixture = next(item for item in fixture_core["fixtures"] if item["id"] == fixture_id)
            fixture["payload"] = json.dumps(
                bad, sort_keys=True, separators=(",", ":"), ensure_ascii=True
            )
            with self.subTest(path=path, boundary="decoded fixture"):
                self.assertEqual(
                    kernel.validate_schema_instance(SCHEMA, "coreData", fixture_core), []
                )
                self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(fixture_core, fixture_id)))

    def test_deep_inner_arrays_and_objects_fail_as_typed_fixture_issues(self):
        for label, raw_payload in (
            ("array", "[" * 2000 + "0" + "]" * 2000),
            ("object", '{"x":' * 2000 + "0" + "}" * 2000),
        ):
            core = support.build_semantic_core()
            good, bad = self.payload_rows(core)["OPTION_CONE"]
            antibody = support.add_semantic_antibody_fixture_set(
                core, "OPTION_CONE", good, bad
            )
            fixture_id = antibody["negativeFixtureIds"][0]
            fixture = next(item for item in core["fixtures"] if item["id"] == fixture_id)
            fixture["payload"] = raw_payload
            with self.subTest(label=label):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
                self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, fixture_id)))


if __name__ == "__main__":
    unittest.main()

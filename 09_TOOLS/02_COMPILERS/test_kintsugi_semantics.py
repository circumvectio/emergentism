from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


COMPILER = Path(__file__).resolve().parent
ROOT = COMPILER.parents[1]
sys.path.insert(0, str(COMPILER))

import kintsugi_kernel as kernel
import kintsugi_test_support as support


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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())

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
            seam = support.add_retiered_seam(core, before, after)
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", upward), ())
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", analogy), ())
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
        second_trial["triedHash"] = "sha256-text-lf:" + "1" * 64
        repeated["trials"].append(second_trial)
        repeated["phaseReceipts"][0]["trialIds"].append(second_trial["id"])
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", repeated), ())
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(validate(core), [])

        second["independenceStatus"] = "NOT_INDEPENDENT"
        core["claims"][0]["supportLinks"][1] = copy.deepcopy(second)
        seam["supportLinks"][1] = copy.deepcopy(second)
        self.assertIn("KIN-E-VERDICT", codes(validate(core)))


class JusticeGateAndQueueTests(unittest.TestCase):
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
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", queue), ())
        self.assertEqual(validate_queue(queue, core), [])

        ownerless = copy.deepcopy(queue)
        ownerless["items"] = [make_ownerless_item(core)]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", ownerless), ())
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())

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
                        kernel.validate_schema_instance(SCHEMA, "coreData", candidate_core), ()
                    )
                else:
                    self.assertNotEqual(
                        kernel.validate_schema_instance(SCHEMA, "coreData", candidate_core), ()
                    )
                self.assertEqual(
                    kernel.validate_schema_instance(SCHEMA, "publicQueue", candidate_queue), ()
                )
                self.assertIn("KIN-E-QUEUE", codes(validate_queue(candidate_queue, candidate_core)))

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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "publicQueue", queue), ())
        self.assertIn("KIN-E-QUEUE", codes(validate_queue(queue, core)))


class SafeRegexGlobAndAntibodyTests(unittest.TestCase):
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
            self.assertEqual(kernel.validate_named_definition(SCHEMA, definition, good), ())
            for field, invalid in invalid_values[evaluator].items():
                payload = copy.deepcopy(good)
                payload[field] = invalid
                with self.subTest(evaluator=evaluator, field=field):
                    self.assertNotEqual(
                        kernel.validate_named_definition(SCHEMA, definition, payload), ()
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertIn("KIN-E-FIXTURE", codes(evaluate_fixture(core, fixture_id)))
        self.assertIn("KIN-E-FIXTURE", codes(validate(core)))


if __name__ == "__main__":
    unittest.main()

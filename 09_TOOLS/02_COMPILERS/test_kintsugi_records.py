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


def validate(core, *, phase=None, bootstrap=False):
    function = getattr(kernel, "validate_core_records", None)
    if function is None:
        return []
    return function(core, phase=phase, bootstrap=bootstrap)


def codes(issues):
    return [issue.code for issue in issues]


def messages(issues):
    return "\n".join(issue.message for issue in issues)


def pending_attempt(core, *, number=1, supersedes=None):
    attempt_id = f"RVA-A-{number:03d}"
    receipt = core["phaseReceipts"][0]
    manifest = core["manifests"][0]
    attempt = {
        "id": attempt_id,
        "phase": "A",
        "receiptId": receipt["id"],
        "supersedesAttemptId": supersedes,
        "reviewSubjectDigest": support.RAW_HASH,
        "reviewTargetPath": f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/review_target.json",
        "logicReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_LOGIC.md",
        "btjReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_BTJ.md",
        "validationBundlePath": f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/validation_bundle.json",
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
    core["reviewAttempts"].append(attempt)
    core["reviewAttemptArtifacts"].append(artifact)
    receipt["reviewAttemptId"] = attempt_id
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])
    derived = [
        attempt["reviewTargetPath"],
        attempt["logicReviewPath"],
        attempt["btjReviewPath"],
        attempt["validationBundlePath"],
    ]
    manifest["closureOnlyPaths"] = sorted(
        set(manifest["closureOnlyPaths"]) | set(derived)
    )
    manifest["allowedChangePaths"] = sorted(
        set(manifest["allowedChangePaths"]) | set(derived)
    )
    return attempt, artifact


def fail_then_successor(core):
    predecessor, artifact = pending_attempt(core, number=1)
    finding = {
        "id": "FND-A-001",
        "attemptId": predecessor["id"],
        "reviewKind": "LOGIC",
        "category": "LOGIC",
        "severity": "MAJOR",
        "statement": "A typed synthetic finding remains open.",
        "claimIds": [core["claims"][0]["id"]],
        "seamIds": [],
        "ledgerSectionIds": ["LEDGER-PREAMBLE"],
        "receiptIds": [core["phaseReceipts"][0]["id"]],
        "subjectPaths": [core["manifests"][0]["includedFiles"][0]["path"]],
    }
    attestation = {
        "id": "ATT-LOGIC-A-001",
        "kind": "LOGIC",
        "path": predecessor["logicReviewPath"],
        "receiptId": predecessor["receiptId"],
        "reviewerId": "independent-logic-reviewer",
        "reviewerRole": "Independent LOGIC reviewer",
        "independenceStatement": "No implementation role in this attempt.",
        "reviewTargetDigest": support.RAW_HASH,
        "verdict": "FAIL",
        "findingIds": [finding["id"]],
        "openSevereFindingIds": [finding["id"]],
        "approvedUpgradeSeamIds": [],
        "approvedGateSeamIds": [],
        "attemptId": predecessor["id"],
    }
    predecessor.update({
        "logicAttestationId": attestation["id"],
        "status": "FAILED",
    })
    artifact.update({
        "reviewTargetSha256": support.RAW_HASH,
        "logicReviewSha256": support.RAW_HASH,
    })
    successor, _ = pending_attempt(core, number=2, supersedes=predecessor["id"])
    disposition = {
        "id": "RFD-RVA-A-002-001",
        "findingId": finding["id"],
        "fromAttemptId": predecessor["id"],
        "successorAttemptId": successor["id"],
        "disposition": "ADDRESSED",
        "rationale": "The successor changes the named claim endpoint.",
        "claimIds": [core["claims"][0]["id"]],
        "seamIds": [],
        "ledgerSectionIds": [],
        "receiptIds": [],
        "subjectPaths": [],
        "discriminatorIds": [],
        "evidenceFiles": [],
    }
    core["reviewAttestations"] = [attestation]
    core["reviewFindings"] = [finding]
    core["reviewFindingDispositions"] = [disposition]
    return predecessor, successor, finding, attestation, disposition


def passed_attempt(core, *, receipt_status="COMPLETE"):
    attempt, artifact = pending_attempt(core)
    attestations = []
    for kind in ("LOGIC", "BTJ"):
        review_path = attempt["logicReviewPath" if kind == "LOGIC" else "btjReviewPath"]
        attestation = {
            "id": f"ATT-{kind}-A-001",
            "kind": kind,
            "path": review_path,
            "receiptId": attempt["receiptId"],
            "reviewerId": f"independent-{kind.lower()}-reviewer",
            "reviewerRole": f"Independent {kind} reviewer",
            "independenceStatement": "No implementation role in this attempt.",
            "reviewTargetDigest": support.RAW_HASH,
            "verdict": "PASS",
            "findingIds": [],
            "openSevereFindingIds": [],
            "approvedUpgradeSeamIds": [],
            "approvedGateSeamIds": [],
            "attemptId": attempt["id"],
        }
        attestations.append(attestation)
    attempt.update({
        "logicAttestationId": attestations[0]["id"],
        "btjAttestationId": attestations[1]["id"],
        "status": "PASSED",
    })
    artifact.update({
        "reviewTargetSha256": support.RAW_HASH,
        "logicReviewSha256": support.RAW_HASH,
        "btjReviewSha256": support.RAW_HASH,
    })
    core["reviewAttestations"] = attestations
    receipt = core["phaseReceipts"][0]
    if receipt_status in {"COMPLETE", "VERIFIED"}:
        receipt.update({
            "status": receipt_status,
            "reviewTargetDigest": support.RAW_HASH,
            "logicReviewPath": attempt["logicReviewPath"],
            "btjReviewPath": attempt["btjReviewPath"],
        })
    if receipt_status == "VERIFIED":
        receipt.update({
            "validationBundlePath": attempt["validationBundlePath"],
            "validationDigest": support.RAW_HASH,
        })
    return attempt, artifact, attestations


def one_pass_attestation(core, attempt, artifact, *, kind="LOGIC"):
    review_key = "logicReviewPath" if kind == "LOGIC" else "btjReviewPath"
    artifact_key = "logicReviewSha256" if kind == "LOGIC" else "btjReviewSha256"
    slot = "logicAttestationId" if kind == "LOGIC" else "btjAttestationId"
    attestation = {
        "id": f"ATT-{kind}-A-001",
        "kind": kind,
        "path": attempt[review_key],
        "receiptId": attempt["receiptId"],
        "reviewerId": f"independent-{kind.lower()}-reviewer",
        "reviewerRole": f"Independent {kind} reviewer",
        "independenceStatement": "No implementation role in this attempt.",
        "reviewTargetDigest": support.RAW_HASH,
        "verdict": "PASS",
        "findingIds": [],
        "openSevereFindingIds": [],
        "approvedUpgradeSeamIds": [],
        "approvedGateSeamIds": [],
        "attemptId": attempt["id"],
    }
    attempt[slot] = attestation["id"]
    artifact.update({"reviewTargetSha256": support.RAW_HASH, artifact_key: support.RAW_HASH})
    core["reviewAttestations"] = [attestation]
    return attestation


class VesselAndIdentityTests(unittest.TestCase):
    def assertSchemaValid(self, value):
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", value), ())

    def assertPrimary(self, core, expected, *, phase="A", bootstrap=False):
        issues = validate(core, phase=phase, bootstrap=bootstrap)
        self.assertTrue(issues)
        self.assertEqual(issues, sorted(set(issues)))
        self.assertEqual(issues[0].code, expected, issues)

    def test_complete_phase_a_vessel_is_schema_valid_and_semantically_closed(self):
        core = support.build_semantic_core()
        self.assertSchemaValid(core)
        self.assertEqual(validate(core, phase="A"), [])

    def test_global_id_table_rejects_duplicates_malformed_ids_and_reserved_id(self):
        rows = []
        duplicate = support.build_semantic_core()
        duplicate["sources"][0]["id"] = duplicate["claims"][0]["id"]
        rows.append(("global duplicate", duplicate))
        malformed = support.build_semantic_core()
        malformed["claims"][0]["id"] = "bad id"
        rows.append(("malformed", malformed))
        reserved = support.build_semantic_core()
        reserved["claims"][0]["id"] = "LEDGER-PREAMBLE"
        rows.append(("reserved", reserved))
        for label, core in rows:
            with self.subTest(label=label):
                self.assertPrimary(core, "KIN-E-ID")

    def test_wrong_kind_and_dangling_references_fail_before_semantic_use(self):
        rows = []
        wrong_kind = support.build_semantic_core()
        wrong_kind["claims"][0]["ownerSourceId"] = wrong_kind["trials"][0]["id"]
        rows.append(("wrong kind", wrong_kind))
        dangling = support.build_semantic_core()
        dangling["claims"][0]["supportLinks"] = [{
            "id": "SUP-A-DANGLING", "supportingClaimId": "CLM-A-999",
            "mode": "CORROBORATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "A deliberately dangling endpoint.",
        }]
        rows.append(("dangling", dangling))
        for label, core in rows:
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                self.assertPrimary(core, "KIN-E-REF")

    def test_source_kind_authority_matrix_and_provenance_firewall(self):
        matrix = {
            "OWNER": {"SEMANTIC_OWNER"},
            "SUPPORT": {"EVIDENCE", "PROVENANCE"},
            "COMPRESSION": {"DERIVATIVE"},
            "PUBLIC": {"DERIVATIVE"},
            "RECEIPT": {"PROVENANCE"},
        }
        for kind, allowed in matrix.items():
            for role in {"SEMANTIC_OWNER", "EVIDENCE", "DERIVATIVE", "PROVENANCE"}:
                core = support.build_semantic_core()
                source = copy.deepcopy(core["sources"][0])
                source.update({
                    "id": "SRC-A-MATRIX", "path": "00_META/source-role-matrix.md",
                    "kind": kind, "authorityRole": role,
                })
                core["sources"].append(source)
                issues = validate(core, phase="A")
                with self.subTest(kind=kind, role=role):
                    self.assertEqual("KIN-E-REF" in codes(issues), role not in allowed)

        for use in ("owner", "premise warrant"):
            core = support.build_semantic_core()
            source = core["sources"][0]
            source.update({"kind": "RECEIPT", "authorityRole": "PROVENANCE"})
            if use == "owner":
                core["claims"][0]["ownerSourceId"] = source["id"]
            else:
                core["claims"][0]["premises"][0]["sourceIds"] = [source["id"]]
            with self.subTest(use=use):
                self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))

        seam_core = support.build_semantic_core()
        seam = support.add_confirmed_seam(seam_core)
        provenance = copy.deepcopy(seam_core["sources"][0])
        provenance.update({
            "id": "SRC-A-PROVENANCE",
            "path": "11_UPLINK/receipt.md",
            "kind": "RECEIPT",
            "authorityRole": "PROVENANCE",
        })
        seam_core["sources"].append(provenance)
        seam["sourceIds"] = [provenance["id"]]
        self.assertIn("KIN-E-REF", codes(validate(seam_core, phase="A")))

    def test_provenance_source_cannot_alias_any_canonical_phase_receipt_path(self):
        for receipt_path in (
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md",
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md",
        ):
            core = support.build_semantic_core()
            source = copy.deepcopy(core["sources"][0])
            source.update({
                "id": "SRC-PROV-A-999",
                "path": receipt_path,
                "kind": "RECEIPT",
                "authorityRole": "PROVENANCE",
            })
            core["sources"].append(source)
            with self.subTest(path=receipt_path):
                self.assertSchemaValid(core)
                self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))


class ClaimGraphTests(unittest.TestCase):
    def assertSchemaValid(self, core):
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())

    def test_dependency_support_and_mixed_cycles_are_rejected_canonically(self):
        cases = []
        dependency = support.build_semantic_core()
        dependency["claims"][0]["dependencyClaimIds"] = [dependency["claims"][1]["id"]]
        dependency["claims"][1]["dependencyClaimIds"] = [dependency["claims"][0]["id"]]
        cases.append(("dependency", dependency))
        support_cycle = support.build_semantic_core()
        support_cycle["claims"][0]["supportLinks"] = [{
            "id": "SUP-A-001", "supportingClaimId": support_cycle["claims"][1]["id"],
            "mode": "CORROBORATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "Independent support.",
        }]
        support_cycle["claims"][1]["supportLinks"] = [{
            "id": "SUP-A-002", "supportingClaimId": support_cycle["claims"][0]["id"],
            "mode": "REPLICATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "Independent replication.",
        }]
        cases.append(("support", support_cycle))
        mixed = support.build_semantic_core()
        mixed["claims"][0]["dependencyClaimIds"] = [mixed["claims"][1]["id"]]
        mixed["claims"][1]["supportLinks"] = [{
            "id": "SUP-A-003", "supportingClaimId": mixed["claims"][0]["id"],
            "mode": "CORROBORATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "A mixed circular edge.",
        }]
        cases.append(("mixed", mixed))
        for label, core in cases:
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                issues = validate(core, phase="A")
                self.assertIn("KIN-E-CYCLE", codes(issues))
                cycle_messages = [issue.message for issue in issues if issue.code == "KIN-E-CYCLE"]
                self.assertEqual(cycle_messages, sorted(cycle_messages))

    def test_duplicate_self_support_and_dependency_support_overlap_fail(self):
        base_link = {
            "id": "SUP-A-001", "supportingClaimId": "CLM-A-002",
            "mode": "CORROBORATION", "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": "A", "rationale": "A typed supporting edge.",
        }
        rows = []
        duplicate = support.build_semantic_core()
        duplicate["claims"][0]["supportLinks"] = [
            copy.deepcopy(base_link),
            {**copy.deepcopy(base_link), "id": "SUP-A-002"},
        ]
        rows.append(("duplicate edge", duplicate))
        self_link = support.build_semantic_core()
        link = copy.deepcopy(base_link)
        link["supportingClaimId"] = self_link["claims"][0]["id"]
        self_link["claims"][0]["supportLinks"] = [link]
        rows.append(("self edge", self_link))
        overlap = support.build_semantic_core()
        overlap["claims"][0]["dependencyClaimIds"] = ["CLM-A-002"]
        overlap["claims"][0]["supportLinks"] = [copy.deepcopy(base_link)]
        rows.append(("dependency overlap", overlap))
        for label, core in rows:
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))

    def test_survivor_cannot_be_self_or_transitively_depend_on_killed_claim(self):
        self_ref = support.build_semantic_core()
        self_ref["claims"][0]["survivingIfKilled"]["claimIds"] = ["CLM-A-001"]
        transitive = support.build_semantic_core()
        transitive["claims"][0]["survivingIfKilled"]["claimIds"] = ["CLM-A-002"]
        transitive["claims"][1]["dependencyClaimIds"] = ["CLM-A-003"]
        transitive["claims"][2]["dependencyClaimIds"] = ["CLM-A-001"]
        for label, core in (("self", self_ref), ("transitive", transitive)):
            with self.subTest(label=label):
                self.assertSchemaValid(core)
                self.assertIn("KIN-E-CYCLE", codes(validate(core, phase="A")))

    def test_typed_terms_are_unique_by_symbol_and_semantic_register(self):
        distinct = support.build_semantic_core()
        term = copy.deepcopy(distinct["claims"][0]["typedTerms"][0])
        term.update({"semanticRegister": "D5", "definition": "The same symbol in D5."})
        distinct["claims"][0]["typedTerms"].append(term)
        self.assertSchemaValid(distinct)
        self.assertEqual(validate(distinct, phase="A"), [])

        duplicate = support.build_semantic_core()
        term = copy.deepcopy(duplicate["claims"][0]["typedTerms"][0])
        term.update({"type": "Different prose type", "definition": "Different prose."})
        duplicate["claims"][0]["typedTerms"].append(term)
        self.assertSchemaValid(duplicate)
        self.assertIn("KIN-E-ID", codes(validate(duplicate, phase="A")))

    def test_normative_claim_requires_normative_entailing_input(self):
        core = support.build_semantic_core()
        claim = core["claims"][0]
        claim.update({
            "claimType": "NORMATIVE",
            "modality": "NORMATIVE",
            "justiceScope": "NORMATIVE",
            "justiceContext": support.build_justice_context(),
        })
        self.assertSchemaValid(core)
        self.assertIn("KIN-E-VERDICT", codes(validate(core, phase="A")))
        claim["premises"][0]["role"] = "NORMATIVE"
        self.assertEqual(validate(core, phase="A"), [])

    def test_deep_acyclic_claim_graph_is_iterative_and_total(self):
        core = support.build_semantic_core()
        template = copy.deepcopy(core["claims"][-1])
        deep_claims = []
        for index in range(1, 1201):
            claim = copy.deepcopy(template)
            claim["id"] = f"CLM-DEEP-{index:04d}"
            claim["typedTerms"][0]["symbol"] = f"deep{index}"
            claim["dependencyClaimIds"] = [f"CLM-DEEP-{index + 1:04d}"] if index < 1200 else []
            deep_claims.append(claim)
        core["claims"].extend(deep_claims)
        self.assertEqual(validate(core, phase="A"), [])


class ReceiptBindingAndBootstrapTests(unittest.TestCase):
    def test_exact_phase_a_binding_table_is_closed(self):
        core = support.build_semantic_core()
        self.assertEqual(validate(core, phase="A"), [])
        mutations = []
        wrong_hash = support.build_semantic_core()
        wrong_hash["trials"][0]["triedHash"] = support.TEXT_HASH
        mutations.append(("fingerprint", wrong_hash))
        wrong_anchor = support.build_semantic_core()
        wrong_anchor["claims"][0]["ownerAnchor"] = "## Wrong"
        mutations.append(("anchor", wrong_anchor))
        duplicate_claim = support.build_semantic_core()
        duplicate_claim["manifests"][0]["requiredClaimBindings"][1]["claimId"] = "CLM-A-001"
        mutations.append(("unique claim", duplicate_claim))
        wrong_owner = support.build_semantic_core()
        wrong_owner["sources"][0]["path"] = "00_META/wrong-owner.md"
        mutations.append(("owner path", wrong_owner))
        for label, mutated in mutations:
            with self.subTest(label=label):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", mutated), ())
                self.assertIn("KIN-E-RECEIPT", codes(validate(mutated, phase="A")))

    def test_phase_b_and_c_forbid_phase_a_requirement_bindings(self):
        for phase in ("B", "C"):
            core = support.build_semantic_core()
            manifest = core["manifests"][0]
            manifest["phase"] = phase
            manifest["id"] = f"MAN-{phase}-001"
            with self.subTest(phase=phase):
                self.assertIn("KIN-E-RECEIPT", codes(validate(core, phase=phase)))

    def test_receipt_identity_path_dependency_order_and_member_kinds(self):
        rows = []
        wrong_path = support.build_semantic_core()
        wrong_path["phaseReceipts"][0]["path"] = "11_UPLINK/wrong.md"
        rows.append(("path", wrong_path))
        wrong_manifest = support.build_semantic_core()
        wrong_manifest["phaseReceipts"][0]["manifestId"] = wrong_manifest["claims"][0]["id"]
        rows.append(("manifest kind", wrong_manifest))
        future_dependency = support.build_semantic_core()
        future_dependency["phaseReceipts"][0]["dependsOnReceiptIds"] = ["REC-B-109"]
        rows.append(("future dependency", future_dependency))
        for label, core in rows:
            with self.subTest(label=label):
                self.assertIn("KIN-E-RECEIPT", codes(validate(core, phase="A")))

    def test_only_explicit_phase_a_bootstrap_accepts_empty_trials(self):
        core = support.build_semantic_core(bootstrap=True)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(validate(core, phase="A", bootstrap=True), [])
        for phase, bootstrap in (("A", False), ("B", True), ("C", True)):
            with self.subTest(phase=phase, bootstrap=bootstrap):
                self.assertIn(
                    "KIN-E-RECEIPT",
                    codes(validate(core, phase=phase, bootstrap=bootstrap)),
                )

    def test_bootstrap_requires_the_canonical_phase_a_manifest_identity(self):
        core = support.build_semantic_core(bootstrap=True)
        core["manifests"][0]["id"] = "MAN-A-999"
        core["phaseReceipts"][0]["manifestId"] = "MAN-A-999"
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertIn("KIN-E-RECEIPT", codes(validate(core, phase="A", bootstrap=True)))

    def test_attempt_sensitive_final_snapshot_and_closure_union(self):
        core = support.build_semantic_core()
        attempt, _ = pending_attempt(core)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(validate(core, phase="A"), [])

        missing_final = copy.deepcopy(core)
        missing_final["manifests"][0]["finalFiles"] = []
        missing_final["manifests"][0]["finalFileCount"] = 0
        self.assertIn("KIN-E-RECEIPT", codes(validate(missing_final, phase="A")))

        bad_closure = copy.deepcopy(core)
        bad_closure["manifests"][0]["closureOnlyPaths"].remove(attempt["btjReviewPath"])
        self.assertIn("KIN-E-RECEIPT", codes(validate(bad_closure, phase="A")))

        stale_pointer = copy.deepcopy(core)
        stale_pointer["phaseReceipts"][0]["reviewAttemptId"] = None
        self.assertIn("KIN-E-RECEIPT", codes(validate(stale_pointer, phase="A")))

    def test_receipt_state_and_closure_fields_bind_the_current_attempt_exactly(self):
        draft = support.build_semantic_core()
        passed_attempt(draft, receipt_status="DRAFT")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", draft), ())
        self.assertIn("KIN-E-RECEIPT", codes(validate(draft, phase="A")))

        complete = support.build_semantic_core()
        attempt, _, _ = passed_attempt(complete, receipt_status="COMPLETE")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", complete), ())
        self.assertEqual(validate(complete, phase="A"), [])
        complete_rows = []
        for field in ("logicReviewPath", "btjReviewPath"):
            mutated = copy.deepcopy(complete)
            mutated["phaseReceipts"][0][field] = f"11_UPLINK/false-{field}.md"
            complete_rows.append((field, mutated))
        wrong_target = copy.deepcopy(complete)
        wrong_target["phaseReceipts"][0]["reviewTargetDigest"] = "sha256:" + "1" * 64
        complete_rows.append(("reviewTargetDigest", wrong_target))
        for label, mutated in complete_rows:
            with self.subTest(status="COMPLETE", field=label):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", mutated), ())
                self.assertIn("KIN-E-RECEIPT", codes(validate(mutated, phase="A")))

        verified = support.build_semantic_core()
        attempt, _, _ = passed_attempt(verified, receipt_status="VERIFIED")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", verified), ())
        self.assertEqual(validate(verified, phase="A"), [])
        wrong_bundle = copy.deepcopy(verified)
        wrong_bundle["phaseReceipts"][0]["validationBundlePath"] = (
            "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/RVA-A-999/validation_bundle.json"
        )
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_bundle), ())
        self.assertIn("KIN-E-RECEIPT", codes(validate(wrong_bundle, phase="A")))


class TrialFixtureAndReviewHistoryTests(unittest.TestCase):
    def test_verdict_matrix_and_trial_state_laws(self):
        verdict_rows = {
            "VALID_SOUND": ("VALID", "SUPPORTED"),
            "VALID_CONDITIONAL": ("VALID", "CONDITIONALLY_SUPPORTED"),
            "VALID_UNSUPPORTED_PREMISE": ("VALID", "UNSUPPORTED"),
            "INVALID": ("INVALID", "NOT_APPLICABLE"),
            "UNDERDETERMINED": ("INVALID", "NOT_APPLICABLE"),
            "DEFINITIONAL": ("NOT_APPLICABLE", "NOT_APPLICABLE"),
            "OPEN_CONJECTURE": ("NOT_APPLICABLE", "UNSUPPORTED"),
            "REFUTED": ("VALID", "REFUTED"),
        }
        for verdict, (validity, soundness) in verdict_rows.items():
            core = support.build_semantic_core()
            trial = core["trials"][0]
            trial.update({
                "verdict": verdict,
                "validityVerdict": validity,
                "soundnessVerdict": soundness,
            })
            with self.subTest(verdict=verdict):
                self.assertNotIn("KIN-E-VERDICT", codes(validate(core, phase="A")))
                trial["soundnessVerdict"] = "SUPPORTED" if soundness != "SUPPORTED" else "REFUTED"
                self.assertIn("KIN-E-VERDICT", codes(validate(core, phase="A")))

        alleged = support.build_semantic_core()
        trial = alleged["trials"][0]
        trial.update({
            "breakState": "ALLEGED", "defectClass": "TYPE_ERROR", "severity": "MAJOR",
            "status": "TRIED", "seamId": None,
            "countermodel": {**trial["countermodel"], "defeatedConclusion": "NONE_FOUND"},
            "discriminatorIds": [],
        })
        self.assertIn("KIN-E-STATE", codes(validate(alleged, phase="A")))

    def test_fixture_cardinality_and_exact_antibody_dispatch_membership(self):
        core = support.build_semantic_core()
        antibody = support.add_antibody_fixture_set(core)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(validate(core, phase="A"), [])
        core["fixtures"] = [
            fixture for fixture in core["fixtures"]
            if fixture["id"] != antibody["quotationFixtureIds"][0]
        ]
        self.assertIn("KIN-E-FIXTURE", codes(validate(core, phase="A")))

    def test_trial_seam_and_seam_discriminators_preserve_claim_and_receipt_identity(self):
        wrong_claim = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_claim)
        seam.update({
            "claimId": wrong_claim["claims"][1]["id"],
            "ownerSource": wrong_claim["claims"][1]["ownerSourceId"],
            "ownerAnchor": wrong_claim["claims"][1]["ownerAnchor"],
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_claim), ())
        self.assertIn("KIN-E-REF", codes(validate(wrong_claim, phase="A")))

        wrong_discriminator = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_discriminator)
        discriminator = {
            "id": "DISC-A-999",
            "claimId": wrong_discriminator["claims"][1]["id"],
            "question": "Does an unrelated claim survive its own test?",
            "method": "Inspect the unrelated claim fixture.",
            "cheapestTest": "Compare the two claim IDs.",
            "expectedObservations": ["The claim IDs remain distinct."],
            "decisionRule": "Treat distinct IDs as different propositions.",
            "status": "QUEUED",
        }
        wrong_discriminator["discriminators"].append(discriminator)
        seam["discriminatorIds"] = [discriminator["id"]]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_discriminator), ())
        self.assertIn("KIN-E-REF", codes(validate(wrong_discriminator, phase="A")))

    def test_seam_claim_projection_has_local_typed_term_and_support_id_uniqueness(self):
        duplicate_term = support.build_semantic_core()
        seam = support.add_confirmed_seam(duplicate_term)
        term = copy.deepcopy(seam["typedTerms"][0])
        term.update({"type": "Different projected prose type", "definition": "Different projected prose."})
        seam["typedTerms"].append(term)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", duplicate_term), ())
        self.assertIn("KIN-E-ID", codes(validate(duplicate_term, phase="A")))

        duplicate_link = support.build_semantic_core()
        seam = support.add_confirmed_seam(duplicate_link)
        links = [
            {
                "id": "SUP-SEAM-A-001",
                "supportingClaimId": duplicate_link["claims"][1]["id"],
                "mode": "CORROBORATION",
                "independenceStatus": "INDEPENDENT",
                "evidenceCeiling": "A",
                "rationale": "First projected support endpoint.",
            },
            {
                "id": "SUP-SEAM-A-001",
                "supportingClaimId": duplicate_link["claims"][2]["id"],
                "mode": "CORROBORATION",
                "independenceStatus": "INDEPENDENT",
                "evidenceCeiling": "A",
                "rationale": "Second projected support endpoint.",
            },
        ]
        seam["priorSupportLinks"] = copy.deepcopy(links)
        seam["supportLinks"] = copy.deepcopy(links)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", duplicate_link), ())
        self.assertIn("KIN-E-ID", codes(validate(duplicate_link, phase="A")))

    def test_review_attempt_artifact_bijection_paths_and_round_trip_id(self):
        core = support.build_semantic_core()
        attempt, _ = pending_attempt(core)
        self.assertEqual(validate(core, phase="A"), [])
        rows = []
        no_artifact = copy.deepcopy(core)
        no_artifact["reviewAttemptArtifacts"] = []
        rows.append(("artifact bijection", no_artifact))
        wrong_path = copy.deepcopy(core)
        wrong_path["reviewAttempts"][0]["logicReviewPath"] = "11_UPLINK/wrong.md"
        rows.append(("derived path", wrong_path))
        wrong_phase = copy.deepcopy(core)
        wrong_phase["reviewAttempts"][0]["phase"] = "B"
        rows.append(("phase agreement", wrong_phase))
        noncanonical = copy.deepcopy(core)
        noncanonical["reviewAttempts"][0]["id"] = "RVA-A-0001"
        noncanonical["reviewAttemptArtifacts"][0]["attemptId"] = "RVA-A-0001"
        noncanonical["phaseReceipts"][0]["reviewAttemptId"] = "RVA-A-0001"
        rows.append(("round trip", noncanonical))
        for label, mutated in rows:
            with self.subTest(label=label):
                self.assertIn("KIN-E-REF", codes(validate(mutated, phase="A")))

    def test_review_chain_is_root_to_leaf_acyclic_and_passed_is_terminal(self):
        core = support.build_semantic_core()
        predecessor, successor, *_ = fail_then_successor(core)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertEqual(validate(core, phase="A"), [])

        reversed_chain = copy.deepcopy(core)
        reversed_chain["reviewAttempts"].reverse()
        reversed_chain["reviewAttemptArtifacts"].reverse()
        self.assertIn("KIN-E-REF", codes(validate(reversed_chain, phase="A")))

        cycle = copy.deepcopy(core)
        cycle["reviewAttempts"][0]["supersedesAttemptId"] = successor["id"]
        self.assertIn("KIN-E-CYCLE", codes(validate(cycle, phase="A")))

        passed_parent = copy.deepcopy(core)
        passed_parent["reviewAttempts"][0]["status"] = "PASSED"
        self.assertIn("KIN-E-STATE", codes(validate(passed_parent, phase="A")))

        two_leaves = copy.deepcopy(core)
        extra = copy.deepcopy(two_leaves["reviewAttempts"][1])
        extra["id"] = "RVA-A-003"
        extra["supersedesAttemptId"] = predecessor["id"]
        for key in ("reviewTargetPath", "logicReviewPath", "btjReviewPath", "validationBundlePath"):
            extra[key] = extra[key].replace("RVA-A-002", "RVA-A-003")
        two_leaves["reviewAttempts"].append(extra)
        extra_artifact = copy.deepcopy(two_leaves["reviewAttemptArtifacts"][1])
        extra_artifact["attemptId"] = "RVA-A-003"
        two_leaves["reviewAttemptArtifacts"].append(extra_artifact)
        self.assertIn("KIN-E-REF", codes(validate(two_leaves, phase="A")))

    def test_attestation_finding_disposition_and_typed_endpoints_resolve_exactly(self):
        core = support.build_semantic_core()
        _, _, finding, attestation, disposition = fail_then_successor(core)
        self.assertEqual(validate(core, phase="A"), [])
        mutations = []
        orphan_finding = copy.deepcopy(core)
        orphan_finding["reviewAttestations"][0]["findingIds"] = []
        orphan_finding["reviewAttestations"][0]["openSevereFindingIds"] = []
        mutations.append(("orphan finding", orphan_finding))
        dangling_endpoint = copy.deepcopy(core)
        dangling_endpoint["reviewFindings"][0]["claimIds"] = ["CLM-A-999"]
        mutations.append(("typed claim endpoint", dangling_endpoint))
        bad_ledger = copy.deepcopy(core)
        bad_ledger["reviewFindings"][0]["ledgerSectionIds"] = ["LEDGER-UNKNOWN"]
        mutations.append(("typed ledger endpoint", bad_ledger))
        orphan_disposition = copy.deepcopy(core)
        orphan_disposition["reviewFindingDispositions"][0]["findingId"] = "FND-A-999"
        mutations.append(("orphan disposition", orphan_disposition))
        wrong_successor = copy.deepcopy(core)
        wrong_successor["reviewFindingDispositions"][0]["successorAttemptId"] = "RVA-A-001"
        mutations.append(("successor agreement", wrong_successor))
        for label, mutated in mutations:
            with self.subTest(label=label):
                self.assertIn("KIN-E-REF", codes(validate(mutated, phase="A")))

        self.assertEqual(finding["id"], attestation["findingIds"][0])
        self.assertEqual(finding["id"], disposition["findingId"])

    def test_attestation_slots_are_role_bound_and_distinct_in_every_attempt_state(self):
        pending = support.build_semantic_core()
        attempt, artifact = pending_attempt(pending)
        one_pass_attestation(pending, attempt, artifact, kind="LOGIC")
        self.assertEqual(validate(pending, phase="A"), [])
        wrong_pending_slot = copy.deepcopy(pending)
        wrong_pending_slot["reviewAttempts"][0]["logicAttestationId"] = None
        wrong_pending_slot["reviewAttempts"][0]["btjAttestationId"] = "ATT-LOGIC-A-001"
        wrong_pending_slot["reviewAttemptArtifacts"][0]["logicReviewSha256"] = None
        wrong_pending_slot["reviewAttemptArtifacts"][0]["btjReviewSha256"] = support.RAW_HASH
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_pending_slot), ())
        self.assertIn("KIN-E-REF", codes(validate(wrong_pending_slot, phase="A")))

        failed = support.build_semantic_core()
        predecessor, _, _, _, _ = fail_then_successor(failed)
        predecessor["btjAttestationId"] = predecessor["logicAttestationId"]
        failed["reviewAttemptArtifacts"][0]["btjReviewSha256"] = support.RAW_HASH
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", failed), ())
        self.assertIn("KIN-E-STATE", codes(validate(failed, phase="A")))

        abandoned = support.build_semantic_core()
        attempt, artifact = pending_attempt(abandoned)
        attestation = one_pass_attestation(abandoned, attempt, artifact, kind="LOGIC")
        attempt.update({
            "btjAttestationId": attestation["id"],
            "status": "ABANDONED",
            "abandonReason": "The duplicated review role invalidated this attempt.",
        })
        artifact["btjReviewSha256"] = support.RAW_HASH
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", abandoned), ())
        self.assertIn("KIN-E-STATE", codes(validate(abandoned, phase="A")))

        for receipt_status in ("COMPLETE", "VERIFIED"):
            terminal = support.build_semantic_core()
            attempt, _, attestations = passed_attempt(terminal, receipt_status=receipt_status)
            terminal["reviewAttestations"] = [attestations[0]]
            attempt["btjAttestationId"] = attempt["logicAttestationId"]
            with self.subTest(receipt_status=receipt_status):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", terminal), ())
                self.assertIn("KIN-E-STATE", codes(validate(terminal, phase="A")))

    def test_review_findings_and_dispositions_are_scoped_to_their_attempt_subject(self):
        finding_core = support.build_semantic_core()
        fail_then_successor(finding_core)
        unrelated = copy.deepcopy(finding_core["claims"][0])
        unrelated.update({
            "id": "CLM-A-999",
            "proposition": "An unrelated global claim is outside the review subject.",
            "conclusion": "The unrelated global claim remains outside the review subject.",
        })
        unrelated["typedTerms"][0]["symbol"] = "outsideSubject"
        unrelated["premises"][0]["id"] = "PREM-A-999"
        finding_core["claims"].append(unrelated)
        finding_core["reviewFindings"][0]["claimIds"] = [unrelated["id"]]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", finding_core), ())
        self.assertIn("KIN-E-REF", codes(validate(finding_core, phase="A")))

        disposition_core = support.build_semantic_core()
        fail_then_successor(disposition_core)
        unrelated = copy.deepcopy(disposition_core["claims"][0])
        unrelated.update({
            "id": "CLM-A-999",
            "proposition": "An unrelated disposition endpoint is outside the successor subject.",
            "conclusion": "The unrelated disposition endpoint remains outside the successor subject.",
        })
        unrelated["typedTerms"][0]["symbol"] = "outsideSuccessor"
        unrelated["premises"][0]["id"] = "PREM-A-999"
        disposition_core["claims"].append(unrelated)
        disposition_core["reviewFindingDispositions"][0]["claimIds"] = [unrelated["id"]]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", disposition_core), ())
        self.assertIn("KIN-E-REF", codes(validate(disposition_core, phase="A")))

        path_core = support.build_semantic_core()
        fail_then_successor(path_core)
        candidate_only = {
            "path": "03_METHODOLOGY/candidate-only.md",
            "kind": "FILE",
            "sha256": support.RAW_HASH,
        }
        path_core["manifests"][0]["candidateFiles"].append(candidate_only)
        path_core["manifests"][0]["candidateFileCount"] += 1
        path_core["reviewFindings"][0]["subjectPaths"] = [candidate_only["path"]]
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", path_core), ())
        self.assertIn("KIN-E-REF", codes(validate(path_core, phase="A")))

    def test_process_invalid_evidence_is_scoped_to_the_successor_manifest(self):
        core = support.build_semantic_core()
        fail_then_successor(core)
        file_record = {
            "path": "03_METHODOLOGY/unrelated-phase-b-final.md",
            "kind": "FILE",
            "sha256": support.RAW_HASH,
        }
        unrelated_manifest = copy.deepcopy(core["manifests"][0])
        unrelated_manifest.update({
            "id": "MAN-B-999",
            "phase": "B",
            "discoveryRules": [{
                "id": "DISC-B-999",
                "includeGlobs": ["03_METHODOLOGY/*.md"],
                "excludeGlobs": ["90_ARCHIVE/**"],
                "parser": "MARKDOWN",
                "rationale": "An unrelated manifest used only as an adversarial fixture.",
            }],
            "candidateFiles": [copy.deepcopy(file_record)],
            "candidateFileCount": 1,
            "includedFiles": [copy.deepcopy(file_record)],
            "finalFiles": [copy.deepcopy(file_record)],
            "finalFileCount": 1,
            "eligibleFileCount": 1,
            "scannedFileCount": 1,
            "requiredClaimBindings": [],
            "trialedClaimIds": [core["claims"][0]["id"]],
            "trialedClaimCount": 1,
            "inventoryReviewPaths": ["03_METHODOLOGY/unrelated-phase-b-review.md"],
            "closureOnlyPaths": [],
        })
        core["manifests"].append(unrelated_manifest)
        disposition = core["reviewFindingDispositions"][0]
        disposition.update({
            "disposition": "PROCESS_INVALID",
            "claimIds": [],
            "evidenceFiles": [{"path": file_record["path"], "sha256": file_record["sha256"]}],
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), ())
        self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))

    def test_review_artifact_hashes_and_process_evidence_are_typed(self):
        core = support.build_semantic_core()
        fail_then_successor(core)
        missing_review_hash = copy.deepcopy(core)
        missing_review_hash["reviewAttemptArtifacts"][0]["logicReviewSha256"] = None
        self.assertIn("KIN-E-STATE", codes(validate(missing_review_hash, phase="A")))

        invalid_process = copy.deepcopy(core)
        disposition = invalid_process["reviewFindingDispositions"][0]
        disposition.update({
            "disposition": "PROCESS_INVALID",
            "claimIds": [],
            "evidenceFiles": [{
                "path": "03_METHODOLOGY/unbound-process-note.md",
                "sha256": support.RAW_HASH,
            }],
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", invalid_process), ())
        self.assertIn("KIN-E-REF", codes(validate(invalid_process, phase="A")))

        missing_attestation = support.build_semantic_core()
        attempt, artifact = pending_attempt(missing_attestation)
        attempt["logicAttestationId"] = "ATT-LOGIC-A-MISSING"
        artifact.update({
            "reviewTargetSha256": support.RAW_HASH,
            "logicReviewSha256": support.RAW_HASH,
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", missing_attestation), ())
        self.assertIn("KIN-E-REF", codes(validate(missing_attestation, phase="A")))


if __name__ == "__main__":
    unittest.main()

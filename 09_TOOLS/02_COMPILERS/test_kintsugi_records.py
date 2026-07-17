from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import tracemalloc
import unittest
from pathlib import Path
from unittest import mock


COMPILER = Path(__file__).resolve().parent
ROOT = COMPILER.parents[1]
sys.path.insert(0, str(COMPILER))

import kintsugi_kernel as kernel  # noqa: E402
from kintsugi_kernel import records as records_module  # noqa: E402
import kintsugi_test_support as support  # noqa: E402


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


def append_draft_phase(core, phase, *, include_trial=True):
    """Append a schema-valid pre-review B/C vessel to a Phase-A core."""
    vessel = support.build_core_data()
    manifest = copy.deepcopy(vessel["manifests"][0])
    source = copy.deepcopy(vessel["sources"][0])
    claim = copy.deepcopy(vessel["claims"][0])
    trial = copy.deepcopy(vessel["trials"][0])
    receipt = copy.deepcopy(vessel["phaseReceipts"][0])

    if phase == "C":
        manifest["id"] = "MAN-C-001"
        manifest["phase"] = "C"
        manifest["discoveryRules"][0]["id"] = "DISC-C-001"
        source["id"] = "SRC-C-001"
        source["phases"] = ["C"]
        claim["id"] = "CLM-C-001"
        claim["ownerSourceId"] = source["id"]
        claim["typedTerms"][0]["symbol"] = "xc"
        claim["premises"][0]["id"] = "PREM-C-001"
        claim["premises"][0]["sourceIds"] = [source["id"]]
        trial.update({
            "id": "TRL-C-001",
            "claimId": claim["id"],
            "manifestId": manifest["id"],
            "receiptId": "REC-C-110",
        })
        receipt.update({
            "id": "REC-C-110",
            "phase": "C",
            "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md",
            "manifestId": manifest["id"],
            "dependsOnReceiptIds": ["REC-A-108", "REC-B-109"],
        })

    manifest.update({
        "finalFiles": [],
        "finalFileCount": 0,
        "harvestedClaimIds": [claim["id"]],
        "eligibleClaimCount": 1,
        "trialedClaimIds": [claim["id"]] if include_trial else [],
        "trialedClaimCount": 1 if include_trial else 0,
        "closureOnlyPaths": [],
    })
    receipt.update({
        "claimIds": [claim["id"]],
        "trialIds": [trial["id"]] if include_trial else [],
    })
    core["manifests"].append(manifest)
    core["sources"].append(source)
    core["claims"].append(claim)
    if include_trial:
        core["trials"].append(trial)
    core["phaseReceipts"].append(receipt)
    return manifest, claim, trial, receipt


def verify_latest_draft_phase(core, phase):
    """Close the latest phase with one role-correct PASSED review attempt."""
    manifest = core["manifests"][-1]
    receipt = core["phaseReceipts"][-1]
    attempt_id = f"RVA-{phase}-001"
    target_path, logic_path, btj_path, bundle_path = records_module.attempt_paths(
        attempt_id
    )
    logic_id = f"ATT-LOGIC-{phase}-001"
    btj_id = f"ATT-BTJ-{phase}-001"
    attempt = {
        "id": attempt_id,
        "phase": phase,
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
    }
    core["reviewAttempts"].append(attempt)
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
            "reviewerId": f"independent-{kind.lower()}-{phase.lower()}-reviewer",
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
        "reviewAttemptId": attempt_id,
        "status": "VERIFIED",
        "reviewTargetDigest": support.RAW_HASH,
        "logicReviewPath": logic_path,
        "btjReviewPath": btj_path,
        "validationBundlePath": bundle_path,
        "validationDigest": support.RAW_HASH,
    })


def long_failed_review_chain(core, *, count):
    """Install a lawful linear attempt history with one finding per predecessor."""
    manifest = core["manifests"][0]
    receipt = core["phaseReceipts"][0]
    claim_id = core["claims"][0]["id"]
    subject_path = manifest["includedFiles"][0]["path"]
    attempts = []
    artifacts = []
    attestations = []
    findings = []
    dispositions = []
    derived_paths = []

    for number in range(1, count + 1):
        attempt_id = f"RVA-A-{number:03d}"
        predecessor_id = f"RVA-A-{number - 1:03d}" if number > 1 else None
        is_leaf = number == count
        target_path, logic_path, btj_path, bundle_path = records_module.attempt_paths(
            attempt_id
        )
        finding_id = f"FND-A-{number:05d}"
        attestation_id = f"ATT-LOGIC-A-{number:05d}"
        attempts.append({
            "id": attempt_id,
            "phase": "A",
            "receiptId": receipt["id"],
            "supersedesAttemptId": predecessor_id,
            "reviewSubjectDigest": support.RAW_HASH,
            "reviewTargetPath": target_path,
            "logicReviewPath": logic_path,
            "btjReviewPath": btj_path,
            "validationBundlePath": bundle_path,
            "logicAttestationId": None if is_leaf else attestation_id,
            "btjAttestationId": None,
            "status": "PENDING" if is_leaf else "FAILED",
            "abandonReason": None,
        })
        artifacts.append({
            "attemptId": attempt_id,
            "reviewTargetSha256": None if is_leaf else support.RAW_HASH,
            "logicReviewSha256": None if is_leaf else support.RAW_HASH,
            "btjReviewSha256": None,
        })
        derived_paths.extend((target_path, logic_path, btj_path, bundle_path))

        if not is_leaf:
            findings.append({
                "id": finding_id,
                "attemptId": attempt_id,
                "reviewKind": "LOGIC",
                "category": "LOGIC",
                "severity": "MAJOR",
                "statement": "A typed synthetic finding remains open.",
                "claimIds": [claim_id],
                "seamIds": [],
                "ledgerSectionIds": ["LEDGER-PREAMBLE"],
                "receiptIds": [receipt["id"]],
                "subjectPaths": [subject_path],
            })
            attestations.append({
                "id": attestation_id,
                "kind": "LOGIC",
                "path": logic_path,
                "receiptId": receipt["id"],
                "reviewerId": f"independent-logic-reviewer-{number}",
                "reviewerRole": "Independent LOGIC reviewer",
                "independenceStatement": "No implementation role in this attempt.",
                "reviewTargetDigest": support.RAW_HASH,
                "verdict": "FAIL",
                "findingIds": [finding_id],
                "openSevereFindingIds": [finding_id],
                "approvedUpgradeSeamIds": [],
                "approvedGateSeamIds": [],
                "attemptId": attempt_id,
            })
        if predecessor_id is not None:
            predecessor_finding_id = f"FND-A-{number - 1:05d}"
            dispositions.append({
                "id": f"RFD-{attempt_id}-001",
                "findingId": predecessor_finding_id,
                "fromAttemptId": predecessor_id,
                "successorAttemptId": attempt_id,
                "disposition": "ADDRESSED",
                "rationale": "The direct successor changes the named claim endpoint.",
                "claimIds": [claim_id],
                "seamIds": [],
                "ledgerSectionIds": [],
                "receiptIds": [],
                "subjectPaths": [],
                "discriminatorIds": [],
                "evidenceFiles": [],
            })

    core["reviewAttempts"] = attempts
    core["reviewAttemptArtifacts"] = artifacts
    core["reviewAttestations"] = attestations
    core["reviewFindings"] = findings
    core["reviewFindingDispositions"] = dispositions
    receipt["reviewAttemptId"] = attempts[-1]["id"]
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])
    manifest["closureOnlyPaths"] = sorted(derived_paths)
    manifest["allowedChangePaths"] = sorted(
        set(manifest["allowedChangePaths"]) | set(derived_paths)
    )


def many_process_invalid_dispositions(core, *, count):
    """Install many process findings that share one successor final snapshot."""
    predecessor, successor, finding, attestation, disposition = fail_then_successor(core)
    manifest = core["manifests"][0]
    receipt = core["phaseReceipts"][0]
    subject_path = manifest["includedFiles"][0]["path"]
    extra_files = [
        {
            "path": f"03_METHODOLOGY/process-evidence-{number:05d}.md",
            "kind": "FILE",
            "sha256": support.RAW_HASH,
        }
        for number in range(1, count + 1)
    ]
    manifest["candidateFiles"].extend(copy.deepcopy(extra_files))
    manifest["candidateFileCount"] = len(manifest["candidateFiles"])
    manifest["includedFiles"].extend(copy.deepcopy(extra_files))
    manifest["eligibleFileCount"] = len(manifest["includedFiles"])
    manifest["scannedFileCount"] = len(manifest["candidateFiles"])
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])

    findings = []
    dispositions = []
    for ordinal in range(1, count + 1):
        finding_id = f"FND-A-{ordinal:05d}"
        next_finding = copy.deepcopy(finding)
        next_finding.update({
            "id": finding_id,
            "statement": f"Process finding {ordinal} remains open.",
            "subjectPaths": [subject_path],
        })
        findings.append(next_finding)
        next_disposition = copy.deepcopy(disposition)
        next_disposition.update({
            "id": f"RFD-{successor['id']}-{ordinal:03d}",
            "findingId": finding_id,
            "disposition": "PROCESS_INVALID",
            "rationale": "The predecessor review artifact proves the process defect.",
            "claimIds": [],
            "ledgerSectionIds": [],
            "evidenceFiles": [{
                "path": predecessor["reviewTargetPath"],
                "sha256": support.RAW_HASH,
            }],
        })
        dispositions.append(next_disposition)

    attestation["findingIds"] = [item["id"] for item in findings]
    attestation["openSevereFindingIds"] = list(attestation["findingIds"])
    core["reviewFindings"] = findings
    core["reviewFindingDispositions"] = dispositions
    receipt["reviewAttemptId"] = successor["id"]
    return manifest


def many_ancestor_process_invalid_dispositions(core, *, count):
    """Point resolving ancestor findings at one non-direct final leaf."""
    long_failed_review_chain(core, count=count + 1)
    manifest = core["manifests"][0]
    extra_files = [
        {
            "path": f"03_METHODOLOGY/ancestor-process-evidence-{number:05d}.md",
            "kind": "FILE",
            "sha256": support.RAW_HASH,
        }
        for number in range(1, count + 1)
    ]
    manifest["candidateFiles"].extend(copy.deepcopy(extra_files))
    manifest["candidateFileCount"] = len(manifest["candidateFiles"])
    manifest["includedFiles"].extend(copy.deepcopy(extra_files))
    manifest["eligibleFileCount"] = len(manifest["includedFiles"])
    manifest["scannedFileCount"] = len(manifest["candidateFiles"])
    manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
    manifest["finalFileCount"] = len(manifest["finalFiles"])

    attempts = {
        attempt["id"]: attempt for attempt in core["reviewAttempts"]
    }
    leaf_id = core["reviewAttempts"][-1]["id"]
    for ordinal, disposition in enumerate(
        core["reviewFindingDispositions"], start=1
    ):
        predecessor = attempts[disposition["fromAttemptId"]]
        disposition.update({
            "id": f"RFD-{leaf_id}-{ordinal:03d}",
            "successorAttemptId": leaf_id,
            "disposition": "PROCESS_INVALID",
            "rationale": "The resolving ancestor artifact proves the process defect.",
            "claimIds": [],
            "seamIds": [],
            "ledgerSectionIds": [],
            "receiptIds": [],
            "subjectPaths": [],
            "discriminatorIds": [],
            "evidenceFiles": [{
                "path": predecessor["reviewTargetPath"],
                "sha256": support.RAW_HASH,
            }],
        })
    return manifest


class CountingDict(dict):
    def __init__(self, *args, counter, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = counter

    def items(self):
        self.counter["finding_steps"] += len(self)
        return super().items()


class CountingList(list):
    def __init__(self, *args, counter, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = counter

    def __iter__(self):
        self.counter["disposition_steps"] += len(self)
        return super().__iter__()


class SubjectCountingList(list):
    def __init__(self, *args, counter, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = counter

    def __iter__(self):
        if self.counter["review_subject_active"]:
            self.counter["claim_membership_scans"] += 1
        return super().__iter__()


class ProcessEvidenceCountingList(list):
    def __init__(self, *args, counter, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = counter

    def __iter__(self):
        if self.counter["review_history_active"]:
            self.counter["final_file_steps"] += len(self)
        return super().__iter__()


class VesselAndIdentityTests(unittest.TestCase):
    def assertSchemaValid(self, value):
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", value), [])

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

    def test_no_source_role_can_relabel_a_canonical_receipt_path_as_evidence(self):
        receipt_path = (
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
            "108_FORMAL_STRESS_LEDGER_2026_07_11.md"
        )
        valid_pairs = (
            ("OWNER", "SEMANTIC_OWNER"),
            ("SUPPORT", "EVIDENCE"),
            ("SUPPORT", "PROVENANCE"),
            ("COMPRESSION", "DERIVATIVE"),
            ("PUBLIC", "DERIVATIVE"),
            ("RECEIPT", "PROVENANCE"),
        )
        for index, (kind, role) in enumerate(valid_pairs, start=1):
            core = support.build_semantic_core()
            source = copy.deepcopy(core["sources"][0])
            source.update({
                "id": f"SRC-RELABELED-{index:03d}",
                "path": receipt_path,
                "kind": kind,
                "authorityRole": role,
            })
            core["sources"].append(source)
            with self.subTest(kind=kind, role=role):
                self.assertSchemaValid(core)
                self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))


class ClaimGraphTests(unittest.TestCase):
    def assertSchemaValid(self, core):
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])

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

    def test_canonical_cycle_rotation_is_linear_space_and_preserves_ring_shape(self):
        size = 3000
        ring = [f"CLM-CYCLE-{index:05d}" for index in range(size)]
        rotated = ring[1731:] + ring[:1731]
        nodes = rotated + [rotated[0]]
        tracemalloc.start()
        try:
            canonical = records_module._canonical_cycle(nodes)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(canonical, tuple(ring + [ring[0]]))
        self.assertLess(peak, 8 * 1024 * 1024)


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
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", mutated), [])
                self.assertIn("KIN-E-RECEIPT", codes(validate(mutated, phase="A")))

    def test_phase_a_binding_hash_cannot_be_laundered_by_a_later_trial(self):
        core = support.build_semantic_core()
        passed_attempt(core, receipt_status="VERIFIED")
        manifest_b, _, trial_b, receipt_b = append_draft_phase(core, "B")
        target = core["claims"][0]
        phase_a_trial = next(
            item for item in core["trials"] if item["claimId"] == target["id"]
        )
        frozen_hash = core["manifests"][0]["requiredClaimBindings"][0]["targetHash"]
        phase_a_trial["triedHash"] = support.TEXT_HASH
        trial_b.update({"claimId": target["id"], "triedHash": frozen_hash})
        manifest_b.update({
            "harvestedClaimIds": [target["id"]],
            "trialedClaimIds": [target["id"]],
        })
        receipt_b["claimIds"] = [target["id"]]
        owner = next(
            item for item in core["sources"]
            if item["id"] == target["ownerSourceId"]
        )
        owner["phases"] = sorted(set(owner["phases"] + ["B"]))

        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        for phase in ("A", "B", None):
            with self.subTest(phase=phase):
                self.assertIn("KIN-E-RECEIPT", codes(validate(core, phase=phase)))

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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertEqual(validate(core, phase="A", bootstrap=True), [])
        for phase, bootstrap in (
            ("A", False), ("B", True), ("C", True), (None, False), (None, True)
        ):
            with self.subTest(phase=phase, bootstrap=bootstrap):
                self.assertIn(
                    "KIN-E-RECEIPT",
                    codes(validate(core, phase=phase, bootstrap=bootstrap)),
                )

    def test_each_trial_is_owned_by_one_same_phase_receipt_manifest_and_claim(self):
        base = support.build_semantic_core()
        passed_attempt(base, receipt_status="VERIFIED")
        append_draft_phase(base, "B")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", base), [])
        self.assertEqual(validate(base, phase="B"), [])

        mutations = []
        cross_phase = copy.deepcopy(base)
        cross_trial = cross_phase["trials"][-1]
        cross_trial["receiptId"] = "REC-A-108"
        cross_phase["phaseReceipts"][0]["trialIds"].append(cross_trial["id"])
        cross_phase["phaseReceipts"][1]["trialIds"] = []
        mutations.append(("cross-phase receipt laundering", cross_phase))

        absent_receipt_claim = copy.deepcopy(base)
        absent_receipt_claim["phaseReceipts"][1]["claimIds"] = [
            absent_receipt_claim["claims"][0]["id"]
        ]
        mutations.append(("receipt claim membership", absent_receipt_claim))

        absent_harvest = copy.deepcopy(base)
        absent_harvest["manifests"][1]["harvestedClaimIds"] = [
            absent_harvest["claims"][0]["id"]
        ]
        mutations.append(("manifest harvested membership", absent_harvest))

        absent_trialed = copy.deepcopy(base)
        absent_trialed["manifests"][1]["trialedClaimIds"] = [
            absent_trialed["claims"][0]["id"]
        ]
        mutations.append(("manifest trialed membership", absent_trialed))

        for label, mutated in mutations:
            with self.subTest(label=label):
                self.assertEqual(
                    kernel.validate_schema_instance(SCHEMA, "coreData", mutated),
                    [],
                )
                self.assertIn("KIN-E-REF", codes(validate(mutated, phase="B")))

    def test_selected_nonbootstrap_phase_b_and_c_require_their_own_trials(self):
        for phase in ("B", "C"):
            core = support.build_semantic_core()
            passed_attempt(core, receipt_status="VERIFIED")
            if phase == "C":
                append_draft_phase(core, "B", include_trial=True)
            append_draft_phase(core, phase, include_trial=False)
            self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
            phase_issues = validate(core, phase=phase)
            with self.subTest(phase=phase):
                self.assertTrue(any(
                    issue.code == "KIN-E-RECEIPT"
                    and f"selected Phase-{phase}" in issue.message
                    and "requires at least one owned trial" in issue.message
                    for issue in phase_issues
                ), phase_issues)

        open_core = support.build_semantic_core()
        passed_attempt(open_core, receipt_status="VERIFIED")
        _, _, open_trial, _ = append_draft_phase(open_core, "B")
        open_trial.update({
            "breakState": "ALLEGED",
            "defectClass": "TYPE_ERROR",
            "severity": "MAJOR",
            "status": "TRIED",
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", open_core), [])
        open_issues = validate(open_core, phase="B")
        self.assertTrue(any(
            issue.code == "KIN-E-RECEIPT"
            and "requires at least one owned trial" in issue.message
            for issue in open_issues
        ), open_issues)

        terminal_core = support.build_semantic_core()
        passed_attempt(terminal_core, receipt_status="VERIFIED")
        append_draft_phase(terminal_core, "B")
        phase_a_trial_ids = set(terminal_core["phaseReceipts"][0]["trialIds"])
        terminal_core["trials"] = [
            trial for trial in terminal_core["trials"]
            if trial["id"] not in phase_a_trial_ids
        ]
        terminal_core["phaseReceipts"][0]["trialIds"] = []
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", terminal_core), [])
        terminal_issues = validate(terminal_core, phase="B")
        self.assertTrue(any(
            issue.path == "core.phaseReceipts[0].trialIds"
            and "requires at least one owned trial" in issue.message
            for issue in terminal_issues
        ), terminal_issues)

    def test_bare_cumulative_validation_checks_each_later_phase_coverage(self):
        rows = []
        for phase in ("B", "C"):
            empty = support.build_semantic_core()
            passed_attempt(empty, receipt_status="VERIFIED")
            if phase == "C":
                append_draft_phase(empty, "B", include_trial=True)
                verify_latest_draft_phase(empty, "B")
            append_draft_phase(empty, phase, include_trial=False)
            rows.append((f"empty Phase-{phase}", phase, empty))

            open_core = support.build_semantic_core()
            passed_attempt(open_core, receipt_status="VERIFIED")
            if phase == "C":
                append_draft_phase(open_core, "B", include_trial=True)
                verify_latest_draft_phase(open_core, "B")
            _, _, open_trial, _ = append_draft_phase(
                open_core, phase, include_trial=True
            )
            open_trial.update({
                "breakState": "ALLEGED",
                "defectClass": "TYPE_ERROR",
                "severity": "MAJOR",
                "status": "TRIED",
            })
            rows.append((f"open-only Phase-{phase}", phase, open_core))

        for label, selected_phase, core in rows:
            receipt_position = 1 if selected_phase == "B" else 2
            self.assertEqual(
                kernel.validate_schema_instance(SCHEMA, "coreData", core), [], label
            )
            for requested_phase in (None, selected_phase):
                with self.subTest(label=label, requested_phase=requested_phase):
                    phase_issues = validate(core, phase=requested_phase)
                    self.assertTrue(any(
                        issue.path
                        == f"core.phaseReceipts[{receipt_position}].trialIds"
                        and issue.code == "KIN-E-RECEIPT"
                        and "requires at least one owned trial" in issue.message
                        for issue in phase_issues
                    ), phase_issues)

    def test_bootstrap_requires_the_canonical_phase_a_manifest_identity(self):
        core = support.build_semantic_core(bootstrap=True)
        core["manifests"][0]["id"] = "MAN-A-999"
        core["phaseReceipts"][0]["manifestId"] = "MAN-A-999"
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertIn("KIN-E-RECEIPT", codes(validate(core, phase="A", bootstrap=True)))

    def test_attempt_sensitive_final_snapshot_and_closure_union(self):
        core = support.build_semantic_core()
        attempt, _ = pending_attempt(core)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", draft), [])
        self.assertIn("KIN-E-RECEIPT", codes(validate(draft, phase="A")))

        complete = support.build_semantic_core()
        attempt, _, _ = passed_attempt(complete, receipt_status="COMPLETE")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", complete), [])
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
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", mutated), [])
                self.assertIn("KIN-E-RECEIPT", codes(validate(mutated, phase="A")))

        verified = support.build_semantic_core()
        attempt, _, _ = passed_attempt(verified, receipt_status="VERIFIED")
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", verified), [])
        self.assertEqual(validate(verified, phase="A"), [])
        wrong_bundle = copy.deepcopy(verified)
        wrong_bundle["phaseReceipts"][0]["validationBundlePath"] = (
            "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/RVA-A-999/validation_bundle.json"
        )
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_bundle), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_claim), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_discriminator), [])
        self.assertIn("KIN-E-REF", codes(validate(wrong_discriminator, phase="A")))

    def test_seam_frozen_quote_hash_owner_and_anchor_match_one_owning_trial(self):
        rows = []
        wrong_quote = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_quote)
        seam["beforeQuote"] = "A different historical statement."
        rows.append(("quote", wrong_quote))

        wrong_hash = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_hash)
        seam["beforeHash"] = "sha256-text-lf:" + "f" * 64
        rows.append(("hash", wrong_hash))

        wrong_owner = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_owner)
        seam["ownerSource"] = wrong_owner["claims"][1]["ownerSourceId"]
        rows.append(("owner identity", wrong_owner))

        wrong_anchor = support.build_semantic_core()
        seam = support.add_confirmed_seam(wrong_anchor)
        seam["ownerAnchor"] = "## Drifted owner anchor"
        rows.append(("owner anchor", wrong_anchor))

        duplicate_owning_trial = support.build_semantic_core()
        seam = support.add_confirmed_seam(duplicate_owning_trial)
        extra_trial = copy.deepcopy(duplicate_owning_trial["trials"][0])
        extra_trial["id"] = "TRL-A-999"
        duplicate_owning_trial["trials"].append(extra_trial)
        duplicate_owning_trial["phaseReceipts"][0]["trialIds"].append(extra_trial["id"])
        rows.append(("exactly one owning trial", duplicate_owning_trial))

        for label, core in rows:
            with self.subTest(label=label):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
                self.assertIn("KIN-E-REF", codes(validate(core, phase="A")))

    def test_seam_claim_projection_has_local_typed_term_and_support_id_uniqueness(self):
        duplicate_term = support.build_semantic_core()
        seam = support.add_confirmed_seam(duplicate_term)
        term = copy.deepcopy(seam["typedTerms"][0])
        term.update({"type": "Different projected prose type", "definition": "Different projected prose."})
        seam["typedTerms"].append(term)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", duplicate_term), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", duplicate_link), [])
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

    def test_arbitrary_length_attempt_suffix_is_total_and_canonical(self):
        huge_canonical = "RVA-A-" + "1" + "0" * 4999
        huge_noncanonical = "RVA-A-" + "0" * 5000
        self.assertTrue(records_module.canonical_attempt(huge_canonical, "A"))
        self.assertFalse(records_module.canonical_attempt(huge_noncanonical, "A"))

        core = support.build_semantic_core()
        attempt, artifact = pending_attempt(core)
        old_id = attempt["id"]
        old_paths = set(records_module.attempt_paths(old_id))
        new_paths = records_module.attempt_paths(huge_canonical)
        attempt["id"] = huge_canonical
        artifact["attemptId"] = huge_canonical
        core["phaseReceipts"][0]["reviewAttemptId"] = huge_canonical
        for key, path in zip(
            ("reviewTargetPath", "logicReviewPath", "btjReviewPath", "validationBundlePath"),
            new_paths,
        ):
            attempt[key] = path
        manifest = core["manifests"][0]
        manifest["closureOnlyPaths"] = sorted(new_paths)
        manifest["allowedChangePaths"] = sorted(
            (set(manifest["allowedChangePaths"]) - old_paths) | set(new_paths)
        )
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
        self.assertEqual(validate(core, phase="A"), [])

    def test_review_chain_is_root_to_leaf_acyclic_and_passed_is_terminal(self):
        core = support.build_semantic_core()
        predecessor, successor, *_ = fail_then_successor(core)
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
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

    def test_large_lawful_review_chain_uses_linear_history_joins(self):
        schema_probe = support.build_semantic_core()
        long_failed_review_chain(schema_probe, count=25)
        self.assertEqual(
            kernel.validate_schema_instance(SCHEMA, "coreData", schema_probe), []
        )
        self.assertEqual(validate(schema_probe, phase="A"), [])

        count = 5000
        core = support.build_semantic_core()
        long_failed_review_chain(core, count=count)
        counter = {"finding_steps": 0, "disposition_steps": 0}
        original_collection_index = records_module._collection_index
        original_items = records_module.items

        def counted_collection_index(value, collection):
            index = original_collection_index(value, collection)
            if collection == "reviewFindings":
                return CountingDict(index, counter=counter)
            return index

        def counted_items(value, collection):
            records = original_items(value, collection)
            if value is core and collection == "reviewFindingDispositions":
                return CountingList(records, counter=counter)
            return records

        with (
            mock.patch.object(
                records_module, "_collection_index", counted_collection_index
            ),
            mock.patch.object(records_module, "items", counted_items),
        ):
            self.assertEqual(validate(core, phase="A"), [])

        self.assertLessEqual(counter["finding_steps"], count * 3, counter)
        self.assertLessEqual(counter["disposition_steps"], count * 8, counter)

    def test_review_subject_membership_is_precomputed_once_per_receipt(self):
        core = support.build_semantic_core()
        long_failed_review_chain(core, count=25)
        counter = {
            "review_subject_active": False,
            "claim_membership_scans": 0,
        }
        receipt = core["phaseReceipts"][0]
        receipt["claimIds"] = SubjectCountingList(
            receipt["claimIds"], counter=counter
        )
        original_validate_review_history = records_module._validate_review_history

        def counted_validate_review_history(value, indexes):
            counter["review_subject_active"] = True
            try:
                return original_validate_review_history(value, indexes)
            finally:
                counter["review_subject_active"] = False

        with mock.patch.object(
            records_module,
            "_validate_review_history",
            counted_validate_review_history,
        ):
            self.assertEqual(validate(core, phase="A"), [])

        self.assertEqual(counter["claim_membership_scans"], 1, counter)

    def test_process_invalid_final_inventory_is_scanned_once_per_attempt_pair(self):
        schema_probe = support.build_semantic_core()
        many_process_invalid_dispositions(schema_probe, count=25)
        self.assertEqual(
            kernel.validate_schema_instance(SCHEMA, "coreData", schema_probe), []
        )
        self.assertEqual(validate(schema_probe, phase="A"), [])

        count = 200
        core = support.build_semantic_core()
        manifest = many_process_invalid_dispositions(core, count=count)
        counter = {"review_history_active": False, "final_file_steps": 0}
        manifest["finalFiles"] = ProcessEvidenceCountingList(
            manifest["finalFiles"], counter=counter
        )
        original_validate_review_history = records_module._validate_review_history

        def counted_validate_review_history(value, indexes):
            counter["review_history_active"] = True
            try:
                return original_validate_review_history(value, indexes)
            finally:
                counter["review_history_active"] = False

        with mock.patch.object(
            records_module,
            "_validate_review_history",
            counted_validate_review_history,
        ):
            self.assertEqual(validate(core, phase="A"), [])

        self.assertLessEqual(
            counter["final_file_steps"], 3 * len(manifest["finalFiles"]), counter
        )

    def test_resolving_ancestor_joins_scan_successor_final_inventory_linearly(self):
        schema_probe = support.build_semantic_core()
        many_ancestor_process_invalid_dispositions(schema_probe, count=25)
        self.assertEqual(
            kernel.validate_schema_instance(SCHEMA, "coreData", schema_probe), []
        )
        first_issues = validate(schema_probe, phase="A")
        second_issues = validate(schema_probe, phase="A")
        self.assertEqual(first_issues, second_issues)
        self.assertEqual(len(first_issues), 25)
        self.assertEqual(set(codes(first_issues)), {"KIN-E-REF"})
        self.assertEqual(
            sum(
                issue.code == "KIN-E-REF"
                and issue.message == (
                    "disposition does not join a finding to its direct successor"
                )
                for issue in first_issues
            ),
            24,
        )

        count = 100
        core = support.build_semantic_core()
        manifest = many_ancestor_process_invalid_dispositions(core, count=count)
        counter = {"review_history_active": False, "final_file_steps": 0}
        manifest["finalFiles"] = ProcessEvidenceCountingList(
            manifest["finalFiles"], counter=counter
        )
        original_validate_review_history = records_module._validate_review_history

        def counted_validate_review_history(value, indexes):
            counter["review_history_active"] = True
            try:
                return original_validate_review_history(value, indexes)
            finally:
                counter["review_history_active"] = False

        with mock.patch.object(
            records_module,
            "_validate_review_history",
            counted_validate_review_history,
        ):
            issues = validate(core, phase="A")

        self.assertEqual(
            sum(
                issue.code == "KIN-E-REF"
                and issue.message == (
                    "disposition does not join a finding to its direct successor"
                )
                for issue in issues
            ),
            count - 1,
        )
        self.assertLessEqual(
            counter["final_file_steps"], 3 * len(manifest["finalFiles"]), counter
        )

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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", wrong_pending_slot), [])
        self.assertIn("KIN-E-REF", codes(validate(wrong_pending_slot, phase="A")))

        failed = support.build_semantic_core()
        predecessor, _, _, _, _ = fail_then_successor(failed)
        predecessor["btjAttestationId"] = predecessor["logicAttestationId"]
        failed["reviewAttemptArtifacts"][0]["btjReviewSha256"] = support.RAW_HASH
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", failed), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", abandoned), [])
        self.assertIn("KIN-E-STATE", codes(validate(abandoned, phase="A")))

        for receipt_status in ("COMPLETE", "VERIFIED"):
            terminal = support.build_semantic_core()
            attempt, _, attestations = passed_attempt(terminal, receipt_status=receipt_status)
            terminal["reviewAttestations"] = [attestations[0]]
            attempt["btjAttestationId"] = attempt["logicAttestationId"]
            with self.subTest(receipt_status=receipt_status):
                self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", terminal), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", finding_core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", disposition_core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", path_core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", core), [])
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
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", invalid_process), [])
        self.assertIn("KIN-E-REF", codes(validate(invalid_process, phase="A")))

        missing_attestation = support.build_semantic_core()
        attempt, artifact = pending_attempt(missing_attestation)
        attempt["logicAttestationId"] = "ATT-LOGIC-A-MISSING"
        artifact.update({
            "reviewTargetSha256": support.RAW_HASH,
            "logicReviewSha256": support.RAW_HASH,
        })
        self.assertEqual(kernel.validate_schema_instance(SCHEMA, "coreData", missing_attestation), [])
        self.assertIn("KIN-E-REF", codes(validate(missing_attestation, phase="A")))


class RecordValidationBoundaryTests(unittest.TestCase):
    JSON_SHAPES = (None, False, 0, "malformed", [], {})
    TOP_LEVEL_COLLECTIONS = (
        "manifests",
        "sources",
        "claims",
        "trials",
        "seams",
        "antibodies",
        "discriminators",
        "fixtures",
        "propagations",
        "phaseReceipts",
        "reviewAttempts",
        "reviewAttemptArtifacts",
        "reviewAttestations",
        "reviewFindings",
        "reviewFindingDispositions",
    )
    NESTED_PATHS = (
        ("claims", 0, "claimType"),
        ("claims", 0, "typedTerms"),
        ("claims", 0, "premises"),
        ("claims", 0, "evidence"),
        ("trials", 0, "verdict"),
        ("trials", 0, "discriminatorIds"),
        ("trials", 0, "countermodel"),
        ("seams", 0, "status"),
        ("seams", 0, "evidenceAfter"),
        ("seams", 0, "truthGate"),
        ("phaseReceipts", 0, "status"),
        ("phaseReceipts", 0, "claimIds"),
        ("phaseReceipts", 0, "dependsOnReceiptIds"),
        ("reviewAttempts", 0, "status"),
        ("reviewAttempts", 0, "logicAttestationId"),
        ("reviewAttemptArtifacts", 0, "logicReviewSha256"),
        ("reviewAttestations", 0, "verdict"),
        ("reviewAttestations", 0, "findingIds"),
        ("reviewFindings", 0, "severity"),
        ("reviewFindings", 0, "claimIds"),
        ("reviewFindingDispositions", 0, "disposition"),
        ("reviewFindingDispositions", 0, "evidenceFiles"),
    )

    @staticmethod
    def _complete_core():
        core = support.build_semantic_core()
        support.add_confirmed_seam(core)
        fail_then_successor(core)
        return core

    @staticmethod
    def _replace(core, path, value):
        parent = core
        for component in path[:-1]:
            parent = parent[component]
        parent[path[-1]] = copy.deepcopy(value)

    def test_json_shaped_depth_three_mutation_matrix_is_total_deterministic_and_pure(self):
        paths = (("program",),) + tuple(
            (collection,) for collection in self.TOP_LEVEL_COLLECTIONS
        ) + self.NESTED_PATHS
        self.assertTrue(all(1 <= len(path) <= 3 for path in paths))

        for path in paths:
            for value in self.JSON_SHAPES:
                label = ".".join(str(component) for component in path)
                with self.subTest(path=label, value=repr(value)):
                    core = self._complete_core()
                    self._replace(core, path, value)
                    frozen_input = copy.deepcopy(core)
                    first = validate(core, phase="A")
                    second = validate(core, phase="A")
                    self.assertEqual(first, second)
                    self.assertEqual(core, frozen_input)
                    self.assertTrue(all(isinstance(item, kernel.Issue) for item in first))

    def test_known_program_enum_and_nested_container_crashes_fail_closed(self):
        mutations = (
            (("program",), None),
            (("trials", 0, "verdict"), []),
            (("claims", 0, "evidence"), []),
            (("reviewFindings", 0, "claimIds"), None),
        )
        for path, value in mutations:
            with self.subTest(path=path):
                core = self._complete_core()
                self._replace(core, path, value)
                issues = validate(core, phase="A")
                self.assertTrue(issues)
                self.assertTrue(all(item.code == "KIN-E-REF" for item in issues))
                self.assertTrue(all(item.path.startswith("core") for item in issues))

    def test_malformed_nested_boundary_is_stable_and_typed(self):
        core = self._complete_core()
        core["trials"][0]["verdict"] = []
        expected = [kernel.Issue(
            "core",
            "KIN-E-REF",
            "core record validation failed safely on malformed nested data",
        )]
        self.assertEqual(validate(core, phase="A"), expected)
        self.assertEqual(validate(core, phase="A"), expected)

    def test_boundary_does_not_intercept_process_control_base_exceptions(self):
        core = self._complete_core()
        for exception in (KeyboardInterrupt(), SystemExit(17)):
            with self.subTest(exception=type(exception).__name__):
                with mock.patch.object(
                    records_module,
                    "_validate_source_roles",
                    side_effect=exception,
                ):
                    with self.assertRaises(type(exception)):
                        validate(core, phase="A")


class ReadOnlyOrchestrationTests(unittest.TestCase):
    def invoke_with_stage_mocks(
        self,
        *,
        phase="C",
        public_queue=True,
        record_issues=(),
        review_issues=(),
        markdown_issues=(),
        manifest_issues=(),
        queue_schema_issues=(),
        public_issues=(),
    ):
        from kintsugi_kernel import orchestration

        events = []
        schema = {"$defs": {}}
        core = {"program": {}}
        queue = {"items": []}
        data_path = Path("/synthetic/data.json")
        queue_path = Path("/synthetic/queue.json") if public_queue else None

        def load_schema(path):
            events.append(("load-schema", path))
            return schema

        def load_json(path):
            events.append(("load-json", path))
            return queue if path == queue_path else core

        def schema_instance(_schema, role, value):
            events.append(("schema-instance", role, value))
            return list(queue_schema_issues) if role == "publicQueue" else []

        def records(value, *, phase, bootstrap):
            events.append(("records", value, phase, bootstrap))
            return list(record_issues)

        def review_history(value):
            events.append(("review-history", value))
            return list(review_issues)

        def markdown(root, value, ledger):
            events.append(("markdown", root, value, ledger))
            return list(markdown_issues)

        def manifest(root, canonical, value, phase, base_ref):
            events.append(("manifest", root, canonical, value, phase, base_ref))
            return list(manifest_issues)

        def public(value, bound_core):
            events.append(("public-queue", value, bound_core))
            return list(public_issues)

        with mock.patch.object(orchestration, "load_schema", side_effect=load_schema), \
             mock.patch.object(orchestration, "load_canonical_json", side_effect=load_json), \
             mock.patch.object(orchestration, "validate_schema_instance", side_effect=schema_instance), \
             mock.patch.object(orchestration, "validate_core_records", side_effect=records), \
             mock.patch.object(orchestration, "validate_review_history", side_effect=review_history), \
             mock.patch.object(orchestration, "validate_markdown_sync", side_effect=markdown), \
             mock.patch.object(orchestration, "validate_manifest", side_effect=manifest), \
             mock.patch.object(orchestration, "validate_public_queue", side_effect=public):
            issues = orchestration.validate_inputs(
                root=Path("/synthetic/root"),
                data_path=data_path,
                schema_path=Path("/synthetic/schema.json"),
                ledger_path=Path("/synthetic/ledger.md"),
                phase=phase,
                bootstrap=False,
                base_ref="MANIFEST" if phase is not None else None,
                canonical_root=(
                    Path("/synthetic/canonical") if phase is not None else None
                ),
                public_queue_path=queue_path,
            )
        return events, issues

    def test_orchestration_order_and_phase_c_queue_are_exact(self):
        events, issues = self.invoke_with_stage_mocks()

        self.assertEqual(issues, [])
        self.assertEqual(
            [event[0] if event[0] != "schema-instance" else f"schema-{event[1]}"
             for event in events],
            [
                "load-schema",
                "load-json",
                "schema-coreData",
                "records",
                "review-history",
                "markdown",
                "manifest",
                "load-json",
                "schema-publicQueue",
                "public-queue",
            ],
        )

    def test_bare_or_phase_b_checks_skip_queue_unless_explicit(self):
        bare_events, bare_issues = self.invoke_with_stage_mocks(
            phase=None,
            public_queue=False,
        )
        self.assertEqual(bare_issues, [])
        self.assertNotIn("manifest", [event[0] for event in bare_events])
        self.assertNotIn("public-queue", [event[0] for event in bare_events])

        phase_events, phase_issues = self.invoke_with_stage_mocks(
            phase="B",
            public_queue=False,
        )
        self.assertEqual(phase_issues, [])
        self.assertIn("manifest", [event[0] for event in phase_events])
        self.assertNotIn("public-queue", [event[0] for event in phase_events])

        explicit_events, explicit_issues = self.invoke_with_stage_mocks(
            phase="B",
            public_queue=True,
        )
        self.assertEqual(explicit_issues, [])
        self.assertIn("public-queue", [event[0] for event in explicit_events])

    def test_primary_stage_issue_stops_every_downstream_stage_and_is_sorted(self):
        from kintsugi_kernel import orchestration

        high = kernel.Issue("z", "KIN-E-SCHEMA", "later sort key")
        low = kernel.Issue("a", "KIN-E-SCHEMA", "earlier sort key")
        with mock.patch.object(orchestration, "load_schema", return_value={}), \
             mock.patch.object(orchestration, "load_canonical_json", return_value={}), \
             mock.patch.object(
                 orchestration,
                 "validate_schema_instance",
                 return_value=[high, low],
             ), \
             mock.patch.object(orchestration, "validate_core_records") as records, \
             mock.patch.object(orchestration, "validate_markdown_sync") as markdown, \
             mock.patch.object(orchestration, "validate_manifest") as manifest:
            issues = orchestration.validate_inputs(
                root=Path("/synthetic/root"),
                data_path=Path("/synthetic/data.json"),
                schema_path=Path("/synthetic/schema.json"),
                ledger_path=Path("/synthetic/ledger.md"),
                phase="A",
                bootstrap=True,
                base_ref="MANIFEST",
                canonical_root=Path("/synthetic/canonical"),
                public_queue_path=None,
            )

        self.assertEqual(issues, [low, high])
        records.assert_not_called()
        markdown.assert_not_called()
        manifest.assert_not_called()

    def test_manifest_issue_prevents_public_queue_evaluation(self):
        failure = kernel.Issue("manifest", "KIN-E-MANIFEST", "synthetic")
        events, issues = self.invoke_with_stage_mocks(
            manifest_issues=(failure,),
        )

        self.assertEqual(issues, [failure])
        self.assertNotIn("public-queue", [event[0] for event in events])

    def test_every_returned_issue_boundary_stops_downstream_without_deduplication(self):
        high = kernel.Issue("z", "KIN-E-SEMANTIC", "later")
        low = kernel.Issue("a", "KIN-E-SEMANTIC", "earlier")
        rows = (
            ("records", {"record_issues": (high, low, low)}, "review-history"),
            (
                "review-history",
                {"review_issues": (high, low, low)},
                "markdown",
            ),
            ("markdown", {"markdown_issues": (high, low, low)}, "manifest"),
            (
                "queue-schema",
                {"queue_schema_issues": (high, low, low)},
                "public-queue",
            ),
            ("public", {"public_issues": (high, low, low)}, None),
        )
        for label, keyword, forbidden in rows:
            with self.subTest(stage=label):
                events, issues = self.invoke_with_stage_mocks(**keyword)
                self.assertEqual(issues, [low, low, high])
                if forbidden is not None:
                    self.assertNotIn(forbidden, [event[0] for event in events])

    def test_loader_exception_propagates_and_prevents_semantic_evaluation(self):
        from kintsugi_kernel import orchestration

        failure = kernel.KintsugiError("KIN-E-IO", "data", "synthetic")
        with mock.patch.object(orchestration, "load_schema", return_value={}), \
             mock.patch.object(
                 orchestration, "load_canonical_json", side_effect=failure
             ), \
             mock.patch.object(orchestration, "validate_schema_instance") as schema, \
             mock.patch.object(orchestration, "validate_core_records") as records:
            with self.assertRaises(kernel.KintsugiError) as caught:
                orchestration.validate_inputs(
                    root=Path("/synthetic/root"),
                    data_path=Path("/synthetic/data.json"),
                    schema_path=Path("/synthetic/schema.json"),
                    ledger_path=Path("/synthetic/ledger.md"),
                )

        self.assertIs(caught.exception, failure)
        schema.assert_not_called()
        records.assert_not_called()

    def test_malformed_core_and_queue_json_fail_with_typed_diagnostics(self):
        from kintsugi_kernel import orchestration

        malformed_payloads = (
            (
                "nesting",
                b"[" * 2000 + b"0" + b"]" * 2000,
                "KIN-E-JSON",
            ),
            (
                "integer-limit",
                b'{"value":' + b"9" * 5000 + b"}\n",
                "KIN-E-JSON",
            ),
            ("lone-surrogate", b'"\\ud800"\n', "KIN-E-CANONICAL"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema_path = root / "schema.json"
            valid_core_path = root / "core.json"
            schema_path.write_bytes(
                (
                    ROOT
                    / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
                ).read_bytes()
            )
            valid_core_path.write_bytes(
                kernel.canonical_json_bytes(support.build_semantic_core())
            )
            for location in ("core", "queue"):
                for label, payload, expected_code in malformed_payloads:
                    with self.subTest(location=location, payload=label):
                        malformed_path = root / f"{location}-{label}.json"
                        malformed_path.write_bytes(payload)
                        with mock.patch.object(
                            orchestration, "validate_markdown_sync", return_value=[]
                        ), self.assertRaises(kernel.KintsugiError) as caught:
                            orchestration.validate_inputs(
                                root=root,
                                data_path=(
                                    malformed_path
                                    if location == "core"
                                    else valid_core_path
                                ),
                                schema_path=schema_path,
                                ledger_path=None,
                                public_queue_path=(
                                    malformed_path if location == "queue" else None
                                ),
                            )
                        self.assertEqual(caught.exception.code, expected_code)
                        self.assertEqual(caught.exception.path, str(malformed_path))

    def test_phase_c_direct_api_requires_a_public_queue(self):
        from kintsugi_kernel.orchestration import validate_inputs

        with self.assertRaises(kernel.KintsugiError) as caught:
            validate_inputs(
                root=Path("/synthetic/root"),
                data_path=Path("/synthetic/data.json"),
                schema_path=Path("/synthetic/schema.json"),
                ledger_path=Path("/synthetic/ledger.md"),
                phase="C",
                bootstrap=False,
                base_ref="MANIFEST",
                canonical_root=Path("/synthetic/canonical"),
                public_queue_path=None,
            )

        self.assertEqual(caught.exception.code, "KIN-E-CLI")
        self.assertEqual(caught.exception.path, "public-queue")

    def test_real_phase_orchestration_preserves_inputs_and_git_state(self):
        from kintsugi_kernel import orchestration

        def snapshot_tree(root: Path) -> dict[str, tuple[str, bytes | str]]:
            snapshot: dict[str, tuple[str, bytes | str]] = {}
            for path in sorted(root.rglob("*")):
                relative = path.relative_to(root).as_posix()
                if path.is_symlink():
                    snapshot[relative] = ("SYMLINK", os.readlink(path))
                elif path.is_file():
                    snapshot[relative] = ("FILE", path.read_bytes())
            return snapshot

        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            fixture = support.build_synthetic_git_repository(
                parent, include_phase_a_artifacts=True
            )
            core = support.build_synthetic_manifest_core(
                fixture, include_verified_phase_a=True
            )
            data_path = parent / "phase-b-core.json"
            schema_path = parent / "schema.json"
            data_path.write_bytes(kernel.canonical_json_bytes(core))
            schema_path.write_bytes(
                (
                    ROOT
                    / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
                ).read_bytes()
            )
            before = {
                "canonical": snapshot_tree(fixture.canonical_root),
                "isolated": snapshot_tree(fixture.isolated_root),
                "data": data_path.read_bytes(),
                "schema": schema_path.read_bytes(),
            }

            with mock.patch.object(
                orchestration, "validate_schema_instance", return_value=[]
            ), mock.patch.object(
                orchestration, "validate_core_records", return_value=[]
            ), mock.patch.object(
                orchestration, "validate_markdown_sync", return_value=[]
            ):
                issues = orchestration.validate_inputs(
                    root=fixture.isolated_root,
                    data_path=data_path,
                    schema_path=schema_path,
                    ledger_path=None,
                    phase="B",
                    bootstrap=False,
                    base_ref="MANIFEST",
                    canonical_root=fixture.canonical_root,
                    public_queue_path=None,
                )

            after = {
                "canonical": snapshot_tree(fixture.canonical_root),
                "isolated": snapshot_tree(fixture.isolated_root),
                "data": data_path.read_bytes(),
                "schema": schema_path.read_bytes(),
            }

        self.assertEqual(issues, [])
        self.assertEqual(after, before)

    def test_real_orchestration_is_read_only_even_when_markdown_fails(self):
        from kintsugi_kernel.orchestration import validate_inputs

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema_path = root / "schema.json"
            data_path = root / "data.json"
            ledger_path = root / "ledger.md"
            schema_path.write_bytes(
                (ROOT / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json").read_bytes()
            )
            core = support.build_semantic_core()
            data_path.write_bytes(kernel.canonical_json_bytes(core))
            ledger_path.write_bytes(support.build_ledger_markdown(core["seams"]))
            before = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }

            issues = validate_inputs(
                root=root,
                data_path=data_path,
                schema_path=schema_path,
                ledger_path=ledger_path,
                phase=None,
                bootstrap=False,
                base_ref=None,
                canonical_root=None,
                public_queue_path=None,
            )

            after = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
        self.assertTrue(issues)
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()

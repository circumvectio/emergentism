from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


COMPILER = Path(__file__).resolve().parent
RAW_HASH = "sha256:" + "0" * 64
TEXT_HASH = "sha256-text-lf:" + "0" * 64
COMMIT_HASH = "0" * 40
ATTEMPT_ID = "RVA-B-001"
RECEIPT_ID = "REC-B-109"
MANIFEST_ID = "MAN-B-001"
SOURCE_ID = "SRC-B-001"
CLAIM_ID = "CLM-B-001"
TRIAL_ID = "TRL-B-001"


def _copy(value: Any) -> Any:
    return copy.deepcopy(value)


def _file(path: str) -> dict[str, str]:
    return {"path": path, "kind": "FILE", "sha256": RAW_HASH}


_MANIFEST = {
    "id": MANIFEST_ID,
    "phase": "B",
    "baseCommit": COMMIT_HASH,
    "canonicalBranch": "main",
    "canonicalCommit": COMMIT_HASH,
    "discoveryRules": [{
        "id": "DISC-B-001",
        "includeGlobs": ["03_METHODOLOGY/**/*.md"],
        "excludeGlobs": ["90_ARCHIVE/**"],
        "parser": "MARKDOWN",
        "rationale": "Deterministic synthetic discovery boundary.",
    }],
    "candidateFiles": [_file("03_METHODOLOGY/owner.md")],
    "candidateFileCount": 1,
    "includedFiles": [_file("03_METHODOLOGY/owner.md")],
    "finalFiles": [_file("03_METHODOLOGY/owner.md")],
    "finalFileCount": 1,
    "excludedPaths": [],
    "eligibleFileCount": 1,
    "scannedFileCount": 1,
    "harvestedClaimIds": [CLAIM_ID],
    "requiredClaimBindings": [],
    "excludedClaimIds": [],
    "eligibleClaimCount": 1,
    "trialedClaimIds": [CLAIM_ID],
    "trialedClaimCount": 1,
    "inventoryReviewPaths": ["03_METHODOLOGY/review.md"],
    "protectedProvenance": [{
        "path": "12_PUBLIC_SITE/index.html",
        "mode": "FULL_FILE",
        "sha256": RAW_HASH,
    }],
    "protectedPaths": ["12_PUBLIC_SITE"],
    "protectedTreeSnapshots": {
        "isolated": [_file("12_PUBLIC_SITE/index.html")],
        "canonical": [_file("12_PUBLIC_SITE/index.html")],
    },
    "allowedChangePaths": [
        "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json",
    ],
    "closureOnlyPaths": [],
    "allowedPreexistingUntracked": {"isolated": [], "canonical": []},
}


_SOURCE = {
    "id": SOURCE_ID,
    "path": "03_METHODOLOGY/owner.md",
    "kind": "OWNER",
    "phases": ["B"],
    "sha256": RAW_HASH,
    "authorityRole": "SEMANTIC_OWNER",
}


_CLAIM = {
    "id": CLAIM_ID,
    "ownerSourceId": SOURCE_ID,
    "ownerAnchor": "## Synthetic owner anchor",
    "proposition": "A declared state remains inside its typed register.",
    "claimType": "STRUCTURAL",
    "typedTerms": [{
        "symbol": "x",
        "type": "State",
        "definition": "A synthetic state used only by tests.",
        "semanticRegister": "D4",
    }],
    "premises": [{
        "id": "PREM-B-001",
        "proposition": "The state is explicitly typed.",
        "evidence": {"strength": "A", "sourced": True, "lifecycle": "ACTIVE"},
        "sourceIds": [SOURCE_ID],
        "role": "DEFINITIONAL",
    }],
    "conclusion": "The state is interpreted in D4.",
    "inference": {"rule": "DEFINITION", "formalization": "typed(x,D4)"},
    "quantifiers": [{"variable": "x", "kind": "FOR_ALL", "domain": "Synthetic states"}],
    "modality": "ACTUAL",
    "scope": {
        "domain": "Synthetic fixture",
        "population": "One declared state",
        "timeHorizon": "Test execution",
        "conditions": [],
    },
    "justiceScope": "NONE",
    "authorityScope": "NONE",
    "authorityEffect": "NONE",
    "evidence": {"strength": "A", "sourced": True, "lifecycle": "ACTIVE"},
    "dependencyClaimIds": [],
    "supportLinks": [],
    "upgradeCriterion": {"kind": "NONE", "rationale": "Already at the schema ceiling."},
    "killCriterion": {
        "kind": "TESTABLE",
        "testability": "ACTIVE",
        "trigger": "The typed declaration is absent.",
        "method": "Inspect the frozen fixture.",
        "disposition": "RETRACT",
    },
    "survivingIfKilled": {"claimIds": [], "rationale": "No dependent kernel is asserted."},
}


_TRIAL = {
    "id": TRIAL_ID,
    "claimId": CLAIM_ID,
    "manifestId": MANIFEST_ID,
    "triedQuote": "A declared state remains inside its typed register.",
    "triedHash": TEXT_HASH,
    "steelman": "The claim is purely structural and explicitly scoped.",
    "countermodel": {
        "description": "No countermodel defeats a definitionally typed fixture.",
        "construction": "Inspect the fixture declaration.",
        "defeatedConclusion": "No conclusion was defeated.",
    },
    "breakState": "NONE",
    "defectClass": None,
    "severity": None,
    "validityVerdict": "VALID",
    "soundnessVerdict": "SUPPORTED",
    "verdict": "VALID_SOUND",
    "discriminatorIds": [],
    "seamId": None,
    "receiptId": RECEIPT_ID,
    "status": "CLOSED",
}


_PHASE_RECEIPT = {
    "id": RECEIPT_ID,
    "phase": "B",
    "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
    "status": "DRAFT",
    "manifestId": MANIFEST_ID,
    "dependsOnReceiptIds": ["REC-A-108"],
    "claimIds": [CLAIM_ID],
    "trialIds": [TRIAL_ID],
    "seamIds": [],
    "propagationIds": [],
    "reviewTargetDigest": None,
    "validationBundlePath": None,
    "validationDigest": None,
    "logicReviewPath": None,
    "btjReviewPath": None,
    "reviewAttemptId": None,
}


_CORE_DATA = {
    "schemaVersion": "1.0.0",
    "program": {
        "id": "KINTSUGI-A0B",
        "title": "Synthetic Kintsugi vessel",
        "phaseOrder": ["A", "B", "C"],
        "protectedPaths": ["12_PUBLIC_SITE"],
        "semanticAuthority": "docs/superpowers/specs/kintsugi.md",
        "noK2Gate": True,
    },
    "manifests": [_MANIFEST],
    "sources": [_SOURCE],
    "claims": [_CLAIM],
    "trials": [_TRIAL],
    "seams": [],
    "antibodies": [],
    "discriminators": [],
    "fixtures": [],
    "propagations": [],
    "phaseReceipts": [_PHASE_RECEIPT],
    "reviewAttempts": [],
    "reviewAttemptArtifacts": [],
    "reviewAttestations": [],
    "reviewFindings": [],
    "reviewFindingDispositions": [],
}


_PUBLIC_QUEUE = {
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
        "currentEvidence": {"strength": "S", "sourced": True, "lifecycle": "ACTIVE"},
        "maximumPublicStrength": "S",
        "requiredAction": "KEEP",
        "verificationCommand": "python3 -m unittest",
        "ownerSourceId": "SRC-C-001",
        "claimId": "CLM-C-001",
        "seamIds": [],
    }],
}


_BASELINE_ALLOWLIST = json.loads(
    (COMPILER / "kintsugi_baseline_failures.json").read_text(encoding="utf-8")
)


def build_core_data() -> dict[str, Any]:
    return _copy(_CORE_DATA)


def build_public_queue() -> dict[str, Any]:
    return _copy(_PUBLIC_QUEUE)


def build_baseline_allowlist() -> dict[str, Any]:
    return _copy(_BASELINE_ALLOWLIST)


def build_review_attempt(
    status: str = "PENDING",
    *,
    logic_attestation_id: str | None = None,
    btj_attestation_id: str | None = None,
) -> dict[str, Any]:
    reason = "The review attempt was explicitly abandoned." if status == "ABANDONED" else None
    return {
        "id": ATTEMPT_ID,
        "phase": "B",
        "receiptId": RECEIPT_ID,
        "supersedesAttemptId": None,
        "reviewSubjectDigest": RAW_HASH,
        "reviewTargetPath": f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{ATTEMPT_ID}/review_target.json",
        "logicReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{ATTEMPT_ID}_LOGIC.md",
        "btjReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{ATTEMPT_ID}_BTJ.md",
        "validationBundlePath": f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{ATTEMPT_ID}/validation_bundle.json",
        "logicAttestationId": logic_attestation_id,
        "btjAttestationId": btj_attestation_id,
        "status": status,
        "abandonReason": reason,
    }


def build_review_attempt_artifact() -> dict[str, Any]:
    return {
        "attemptId": ATTEMPT_ID,
        "reviewTargetSha256": RAW_HASH,
        "logicReviewSha256": RAW_HASH,
        "btjReviewSha256": RAW_HASH,
    }


def build_review_attestation(kind: str = "LOGIC", verdict: str = "PASS") -> dict[str, Any]:
    is_fail = verdict == "FAIL"
    return {
        "id": f"ATT-{kind}-001",
        "kind": kind,
        "path": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/{kind.lower()}-review.md",
        "receiptId": RECEIPT_ID,
        "reviewerId": f"reviewer-{kind.lower()}",
        "reviewerRole": f"Independent {kind} reviewer",
        "independenceStatement": "No implementation role in this attempt.",
        "reviewTargetDigest": RAW_HASH,
        "verdict": verdict,
        "findingIds": ["FND-B-001"] if is_fail else [],
        "openSevereFindingIds": ["FND-B-001"] if is_fail else [],
        "approvedUpgradeSeamIds": [],
        "approvedGateSeamIds": [],
        "attemptId": ATTEMPT_ID,
    }


def build_review_finding() -> dict[str, Any]:
    return {
        "id": "FND-B-001",
        "attemptId": ATTEMPT_ID,
        "reviewKind": "LOGIC",
        "category": "LOGIC",
        "severity": "MAJOR",
        "statement": "A synthetic severe finding.",
        "claimIds": [CLAIM_ID],
        "seamIds": [],
        "ledgerSectionIds": [],
        "receiptIds": [RECEIPT_ID],
        "subjectPaths": ["03_METHODOLOGY/owner.md"],
    }


def build_review_process_evidence() -> dict[str, Any]:
    return {"path": "03_METHODOLOGY/process-evidence.txt", "sha256": RAW_HASH}


def build_review_finding_disposition(
    disposition: str = "ADDRESSED", *, include_ids: bool = True
) -> dict[str, Any]:
    record = {
        "id": "RFD-RVA-B-002-001",
        "findingId": "FND-B-001",
        "fromAttemptId": ATTEMPT_ID,
        "successorAttemptId": "RVA-B-002",
        "disposition": disposition,
        "rationale": "A deterministic synthetic disposition.",
        "claimIds": [],
        "seamIds": [],
        "ledgerSectionIds": [],
        "receiptIds": [],
        "subjectPaths": [],
        "discriminatorIds": [],
        "evidenceFiles": [],
    }
    if disposition == "ADDRESSED" and include_ids:
        record["claimIds"] = [CLAIM_ID]
    elif disposition == "DISPUTED" and include_ids:
        record["discriminatorIds"] = ["DISC-B-001"]
    elif disposition == "PROCESS_INVALID" and include_ids:
        record["evidenceFiles"] = [build_review_process_evidence()]
    return record


def build_review_finding_disposition_input(disposition: str = "ADDRESSED") -> dict[str, Any]:
    record = build_review_finding_disposition(disposition)
    for key in ("id", "fromAttemptId", "successorAttemptId"):
        del record[key]
    return record


def build_review_target() -> dict[str, Any]:
    core = build_core_data()
    return {
        "schemaVersion": "1.0.0",
        "phase": "B",
        "currentAttemptId": ATTEMPT_ID,
        "receiptId": RECEIPT_ID,
        "receiptNarrativeRawSha256": RAW_HASH,
        "reviewSubjectDigest": RAW_HASH,
        "manifest": core["manifests"][0],
        "sources": core["sources"],
        "claims": core["claims"],
        "trials": core["trials"],
        "seams": [],
        "propagations": [],
        "antibodies": [],
        "discriminators": [],
        "fixtures": [],
        "schemaSha256": RAW_HASH,
        "ledgerPreambleRawSha256": RAW_HASH,
        "ledgerSemanticSections": [],
        "semanticDiffPaths": ["03_METHODOLOGY/owner.md"],
        "priorReviewAttempts": [],
        "priorReviewAttemptArtifacts": [],
        "priorReviewAttestations": [],
        "priorReviewFindings": [],
        "priorReviewFindingDispositions": [],
    }


def build_receipt_descriptor() -> dict[str, Any]:
    return {
        "id": RECEIPT_ID,
        "phase": "B",
        "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
        "status": "VERIFIED",
        "manifestId": MANIFEST_ID,
        "dependsOnReceiptIds": ["REC-A-108"],
        "claimIds": [CLAIM_ID],
        "trialIds": [TRIAL_ID],
        "seamIds": [],
        "propagationIds": [],
        "reviewTargetDigest": RAW_HASH,
        "validationBundlePath": f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{ATTEMPT_ID}/validation_bundle.json",
        "logicReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{ATTEMPT_ID}_LOGIC.md",
        "btjReviewPath": f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{ATTEMPT_ID}_BTJ.md",
        "reviewAttemptId": ATTEMPT_ID,
    }


def build_validation_bundle() -> dict[str, Any]:
    core = build_core_data()
    attempt = build_review_attempt(
        "PASSED",
        logic_attestation_id="ATT-LOGIC-001",
        btj_attestation_id="ATT-BTJ-001",
    )
    return {
        "schemaVersion": "1.0.0",
        "phase": "B",
        "receiptDescriptor": build_receipt_descriptor(),
        "reviewTargetDigest": RAW_HASH,
        "manifest": core["manifests"][0],
        "sources": core["sources"],
        "claims": core["claims"],
        "trials": core["trials"],
        "seams": [],
        "propagations": [],
        "antibodies": [],
        "discriminators": [],
        "fixtures": [],
        "schemaSha256": RAW_HASH,
        "ledgerSections": [],
        "logicReviewSha256": RAW_HASH,
        "btjReviewSha256": RAW_HASH,
        "publicQueueSha256": None,
        "dependencyReceipts": [],
        "reviewAttempts": [attempt],
        "reviewAttemptArtifacts": [build_review_attempt_artifact()],
        "reviewAttestations": [
            build_review_attestation("LOGIC", "PASS"),
            build_review_attestation("BTJ", "PASS"),
        ],
        "reviewFindings": [],
        "reviewFindingDispositions": [],
        "receiptNarrativeRawSha256": RAW_HASH,
        "ledgerPreambleRawSha256": RAW_HASH,
    }


def build_semantic_payloads() -> dict[str, dict[str, Any]]:
    return _copy({
        "verdictMatrixPayload": {
            "validityVerdict": "VALID",
            "soundnessVerdict": "SUPPORTED",
            "verdict": "VALID_SOUND",
        },
        "justiceContextPayload": {
            "claimType": "STRUCTURAL",
            "modality": "ACTUAL",
            "justiceScope": "NONE",
            "authorityScope": "NONE",
            "authorityEffect": "NONE",
            "evidenceLifecycle": "ACTIVE",
            "justiceContext": None,
        },
        "receiptRolePayload": {
            "recordKind": "SOURCE_RECORD",
            "sourceKind": "OWNER",
            "authorityRole": "SEMANTIC_OWNER",
            "receiptId": None,
            "phase": None,
            "path": "03_METHODOLOGY/owner.md",
            "status": None,
            "requestedUse": "PROVENANCE",
        },
        "registerIndexPayload": {
            "symbol": "x",
            "fromRegister": "D4",
            "toRegister": "D5",
            "relation": "DISTINCT_TYPED_TERM",
            "bridgeClaimId": None,
            "requestedInference": "TYPED_REFERENCE",
        },
        "quantumMeasurePayload": {
            "probabilityObject": "EVENT_MEASURE",
            "requestedOperation": "SAMPLE_OUTCOME",
            "interpretiveClaim": "NONE",
        },
        "optionConePayload": {
            "physicalConstraint": "C_BOUNDED",
            "optionClaim": "MODELED_REACHABILITY",
            "futureInfluence": "ANTICIPATORY_MODEL",
            "commitmentKind": "PARTIAL_RELATION",
        },
        "trophicAggregatorPayload": {
            "quantityKind": "HUMAN_INVESTMENT_PROXY",
            "aggregationBasis": "DECLARED_PROXY",
            "conservationClaim": "NONE",
            "persistentSharedTrace": True,
            "carrierTurnoverObserved": True,
            "laterSelectionReweightingObserved": True,
            "requestedInference": "EGREGOREOTYPE_CANDIDATE",
        },
        "rosettaTransferPayload": {
            "targetClaimId": CLAIM_ID,
            "bridgeClaimId": None,
            "fromRegister": "D4",
            "toRegister": "D5",
            "requestedTransfer": "TOPOLOGY",
        },
    })


REQUIRED_PHASE_A_BINDINGS = _copy([
    {
        "requirementId": requirement,
        "claimId": f"CLM-A-{index:03d}",
        "ownerSourceId": f"SRC-A-{index:03d}",
        "ownerAnchor": anchor,
        "targetHash": target_hash,
        "rationale": "Synthetic structural binding.",
    }
    for index, (requirement, anchor, target_hash) in enumerate([
        ("REQ-A-PROTOCOL-SELF-TRIAL", "# The Kintsugi Protocol", "sha256-text-lf:9fe68c734bce6c709c5879e0f7e40b552cdacb4cd14121302371509fb13f7cc9"),
        ("REQ-A-TRIADIC-UNIQUENESS", "## The Uniqueness Theorem", "sha256-text-lf:438269d12273e6c169e2ba8bdb8c126dcb118378a1d28a55328aa4dbdaec17b8"),
        ("REQ-A-D6-AREA-DIRECTION", "### 2.2 The Coordinate Collapse Theorem", "sha256-text-lf:75893a2cd097580c3ee44a8a62f940e9b02d3dc09e4d73a5d3796e70de7d8e26"),
        ("REQ-A-POWER-MAX-CIRCULARITY", "## The Statement", "sha256-text-lf:8cb12ae6fb3b855cbe999d699041ae3a15c73d3c405362195f6bf58441019510"),
        ("REQ-A-D4-D5-REGISTER", "## I. THE FUNDAMENTAL DISTINCTION", "sha256-text-lf:dee381fece54b4fe926b1af1145ab8676263091cc698460a3b37962c77a6cca2"),
        ("REQ-A-QUANTUM-MEASURE", "## The Corrected Formula", "sha256-text-lf:41b8437a8e8715a7be6f8f7ddef46984b89757d9f9722494b554dc3e87d204fb"),
        ("REQ-A-OPTION-CONE", "### Worldline and Light-Cone Corollary", "sha256-text-lf:6749c86499b1e5d1a04de8afcbc6df283403617f1d0e40bdf9dbe66073412527"),
    ], start=1)
])

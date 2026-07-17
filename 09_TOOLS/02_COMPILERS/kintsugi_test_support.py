from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
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

_PHASE_A_ATTEMPT_ID = "RVA-A-001"
_PHASE_A_TARGET_PATH = (
    "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/"
    f"{_PHASE_A_ATTEMPT_ID}/review_target.json"
)
_PHASE_A_LOGIC_PATH = (
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/"
    f"{_PHASE_A_ATTEMPT_ID}_LOGIC.md"
)
_PHASE_A_BTJ_PATH = (
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/"
    f"{_PHASE_A_ATTEMPT_ID}_BTJ.md"
)
_PHASE_A_BUNDLE_PATH = (
    "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/"
    f"{_PHASE_A_ATTEMPT_ID}/validation_bundle.json"
)


def _canonical_fixture_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def _phase_a_dependency_artifacts() -> dict[str, Any]:
    """Return immutable, typed closure bytes for the synthetic verified dependency."""
    target_bytes = _canonical_fixture_bytes({"fixture": "verified Phase-A target"})
    target_hash = "sha256:" + hashlib.sha256(target_bytes).hexdigest()
    attestations: list[dict[str, Any]] = []
    review_bytes: dict[str, bytes] = {}
    for kind, path, reviewer in (
        ("LOGIC", _PHASE_A_LOGIC_PATH, "synthetic-logic-reviewer"),
        ("BTJ", _PHASE_A_BTJ_PATH, "synthetic-btj-reviewer"),
    ):
        attestation = {
            "id": f"ATT-{kind}-A-001",
            "kind": kind,
            "path": path,
            "receiptId": "REC-A-108",
            "reviewerId": reviewer,
            "reviewerRole": f"Independent synthetic {kind} reviewer",
            "independenceStatement": "This deterministic fixture did not author the subject.",
            "reviewTargetDigest": target_hash,
            "verdict": "PASS",
            "findingIds": [],
            "openSevereFindingIds": [],
            "approvedUpgradeSeamIds": [],
            "approvedGateSeamIds": [],
            "attemptId": _PHASE_A_ATTEMPT_ID,
        }
        attestations.append(attestation)
        review_bytes[kind] = build_review_markdown(attestation, [])
    bundle_bytes = _canonical_fixture_bytes({"fixture": "verified Phase-A bundle"})
    return {
        "targetBytes": target_bytes,
        "targetHash": target_hash,
        "attestations": attestations,
        "logicBytes": review_bytes["LOGIC"],
        "logicHash": "sha256:" + hashlib.sha256(review_bytes["LOGIC"]).hexdigest(),
        "btjBytes": review_bytes["BTJ"],
        "btjHash": "sha256:" + hashlib.sha256(review_bytes["BTJ"]).hexdigest(),
        "bundleBytes": bundle_bytes,
        "bundleHash": "sha256:" + hashlib.sha256(bundle_bytes).hexdigest(),
    }


@dataclass(frozen=True)
class SyntheticGitRepository:
    canonical_root: Path
    isolated_root: Path
    common_dir: Path
    base_commit: str


def _git_fixture_run(root: Path, *argv: str) -> bytes:
    environment = os.environ.copy()
    environment.update({
        "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+0000",
        "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+0000",
        "LC_ALL": "C",
    })
    return subprocess.run(
        ["git", *argv],
        cwd=root,
        env=environment,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def build_synthetic_git_repository(
    parent: Path, *, include_phase_a_artifacts: bool = False
) -> SyntheticGitRepository:
    canonical_root = parent / "main"
    isolated_root = parent / "isolated"
    canonical_root.mkdir(parents=True)
    _git_fixture_run(canonical_root, "init", "-b", "main")
    _git_fixture_run(canonical_root, "config", "user.name", "Kintsugi Fixture")
    _git_fixture_run(canonical_root, "config", "user.email", "fixture@example.invalid")

    tracked = {
        "03_METHODOLOGY/owner.md": b"# Synthetic owner\n",
        "03_METHODOLOGY/support.md": b"# Synthetic support\n",
        "03_METHODOLOGY/excluded.md": b"# Deliberately excluded synthetic candidate\n",
        "03_METHODOLOGY/phase-b-inventory-review.md": b"# Synthetic inventory review\n",
        "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json": b"{}\n",
        "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json": (
            COMPILER.parents[1]
            / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
        ).read_bytes(),
        "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md": b"# Synthetic ledger\n",
        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md": b"# Synthetic Phase B receipt\n",
        "12_PUBLIC_SITE/index.html": b"<!doctype html><title>Synthetic</title>\n",
        "12_PUBLIC_SITE/assets/base.css": b":root{color:#111}\n",
        "90_ARCHIVE/history.txt": b"archived synthetic bytes\n",
        "91_COMPATIBILITY/legacy.txt": b"compatibility synthetic bytes\n",
        "03_METHODOLOGY/phase-a-inventory-review.md": b"# Synthetic Phase A inventory review\n",
        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md": b"# Synthetic Phase A receipt\n",
    }
    if include_phase_a_artifacts:
        dependency_artifacts = _phase_a_dependency_artifacts()
        tracked.update({
            _PHASE_A_TARGET_PATH: dependency_artifacts["targetBytes"],
            _PHASE_A_LOGIC_PATH: dependency_artifacts["logicBytes"],
            _PHASE_A_BTJ_PATH: dependency_artifacts["btjBytes"],
            _PHASE_A_BUNDLE_PATH: dependency_artifacts["bundleBytes"],
        })
    bindings_by_owner: dict[str, list[tuple[str, str]]] = {}
    for requirement, owner_path, anchor, _ in PHASE_A_REQUIREMENTS:
        bindings_by_owner.setdefault(owner_path, []).append(
            (anchor, PHASE_A_QUOTES[requirement])
        )
    for owner_path, bindings in sorted(bindings_by_owner.items()):
        tracked[owner_path] = (
            "# Synthetic Phase A owner\n\n"
            + "\n\n".join(
                f"{anchor}\n\n{quote}" for anchor, quote in bindings
            )
            + "\n"
        ).encode("utf-8")
    for relative, payload in tracked.items():
        target = canonical_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    (canonical_root / "12_PUBLIC_SITE/assets-link").symlink_to("assets", target_is_directory=True)
    _git_fixture_run(canonical_root, "add", "--all")
    _git_fixture_run(canonical_root, "commit", "-m", "synthetic base")
    base_commit = _git_fixture_run(canonical_root, "rev-parse", "HEAD").decode("ascii").strip()
    _git_fixture_run(
        canonical_root,
        "worktree",
        "add",
        "-b",
        "isolated",
        str(isolated_root),
        base_commit,
    )

    for root in (canonical_root, isolated_root):
        untracked = root / "scratch/preexisting.txt"
        untracked.parent.mkdir(parents=True, exist_ok=True)
        untracked.write_bytes(b"pre-existing untracked bytes\n")

    common_raw = _git_fixture_run(canonical_root, "rev-parse", "--git-common-dir")
    common_path = Path(common_raw.decode("utf-8").strip())
    common_dir = (
        common_path if common_path.is_absolute() else canonical_root / common_path
    ).resolve()
    return SyntheticGitRepository(
        canonical_root=canonical_root.resolve(),
        isolated_root=isolated_root.resolve(),
        common_dir=common_dir,
        base_commit=base_commit,
    )


def _synthetic_file_record(root: Path, relative: str) -> dict[str, str]:
    path = root / relative
    if path.is_symlink():
        return {
            "path": relative,
            "kind": "SYMLINK",
            "sha256": "sha256:" + hashlib.sha256(os.readlink(path).encode("utf-8")).hexdigest(),
        }
    return {
        "path": relative,
        "kind": "FILE",
        "sha256": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def build_synthetic_manifest_core(
    fixture: SyntheticGitRepository,
    *,
    include_verified_phase_a: bool = False,
) -> dict[str, Any]:
    core = build_core_data()
    manifest = core["manifests"][0]
    candidates = (
        "03_METHODOLOGY/excluded.md",
        "03_METHODOLOGY/owner.md",
        "03_METHODOLOGY/support.md",
    )
    included = candidates[1:]
    protected = (
        "12_PUBLIC_SITE/assets-link",
        "12_PUBLIC_SITE/assets/base.css",
        "12_PUBLIC_SITE/index.html",
        "90_ARCHIVE/history.txt",
        "91_COMPATIBILITY/legacy.txt",
    )
    preexisting = "scratch/preexisting.txt"
    core_path = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
    ledger_path = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
    receipt_path = next(
        receipt["path"] for receipt in core["phaseReceipts"] if receipt["phase"] == "B"
    )

    manifest.update({
        "baseCommit": fixture.base_commit,
        "canonicalCommit": fixture.base_commit,
        "discoveryRules": [{
            "id": "DISC-B-001",
            "includeGlobs": list(candidates),
            "excludeGlobs": ["03_METHODOLOGY/excluded.md"],
            "parser": "MARKDOWN",
            "rationale": "Deterministic synthetic discovery boundary.",
        }],
        "candidateFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in candidates
        ],
        "candidateFileCount": len(candidates),
        "includedFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in included
        ],
        "finalFiles": [],
        "finalFileCount": 0,
        "excludedPaths": [{
            "path": "03_METHODOLOGY/excluded.md",
            "reason": "Synthetic exclusion.",
        }],
        "eligibleFileCount": len(included),
        "scannedFileCount": len(included),
        "inventoryReviewPaths": ["03_METHODOLOGY/phase-b-inventory-review.md"],
        "protectedProvenance": [
            {
                "path": "12_PUBLIC_SITE/index.html",
                "mode": "FULL_FILE",
                "sha256": _synthetic_file_record(
                    fixture.canonical_root, "12_PUBLIC_SITE/index.html"
                )["sha256"],
            },
            {
                "path": "90_ARCHIVE/history.txt",
                "mode": "EXACT_SPAN",
                "exactSpan": "archived synthetic bytes",
                "sha256": "sha256:" + hashlib.sha256(
                    b"archived synthetic bytes"
                ).hexdigest(),
            },
        ],
        "protectedPaths": ["12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"],
        "protectedTreeSnapshots": {
            "isolated": [
                _synthetic_file_record(fixture.isolated_root, relative)
                for relative in protected
            ],
            "canonical": [
                _synthetic_file_record(fixture.canonical_root, relative)
                for relative in protected
            ],
        },
        "allowedChangePaths": sorted({
            core_path,
            ledger_path,
            receipt_path,
            "03_METHODOLOGY/owner.md",
            "03_METHODOLOGY/support.md",
            "03_METHODOLOGY/phase-b-inventory-review.md",
        }),
        "closureOnlyPaths": [],
        "allowedPreexistingUntracked": {
            "isolated": [_synthetic_file_record(fixture.isolated_root, preexisting)],
            "canonical": [_synthetic_file_record(fixture.canonical_root, preexisting)],
        },
    })

    owner = core["sources"][0]
    owner["sha256"] = _synthetic_file_record(
        fixture.canonical_root, owner["path"]
    )["sha256"]
    support = _copy(owner)
    support.update({
        "id": "SRC-B-002",
        "path": "03_METHODOLOGY/support.md",
        "kind": "SUPPORT",
        "authorityRole": "EVIDENCE",
        "sha256": _synthetic_file_record(
            fixture.canonical_root, "03_METHODOLOGY/support.md"
        )["sha256"],
    })
    core["sources"] = [owner, support]
    if include_verified_phase_a:
        _prepend_verified_phase_a_dependency(core, fixture)
    else:
        phase_a_receipt = _copy(build_semantic_core(bootstrap=False)["phaseReceipts"][0])
        dependency_artifacts = _phase_a_dependency_artifacts()
        phase_a_receipt.update({
            "status": "VERIFIED",
            "claimIds": [],
            "trialIds": [],
            "seamIds": [],
            "propagationIds": [],
            "reviewTargetDigest": dependency_artifacts["targetHash"],
            "validationBundlePath": _PHASE_A_BUNDLE_PATH,
            "validationDigest": dependency_artifacts["bundleHash"],
            "logicReviewPath": _PHASE_A_LOGIC_PATH,
            "btjReviewPath": _PHASE_A_BTJ_PATH,
            "reviewAttemptId": None,
        })
        # Manifest-only fixtures need a valid dependency descriptor but no
        # review artifact namespace. Full review fixtures opt into the complete
        # Phase-A vessel above.
        core["phaseReceipts"] = [phase_a_receipt, *core["phaseReceipts"]]
    return core


def build_synthetic_phase_a_manifest_core(
    fixture: SyntheticGitRepository, *, bootstrap: bool
) -> dict[str, Any]:
    core = build_semantic_core(bootstrap=bootstrap)
    manifest = core["manifests"][0]
    phase_b_core = build_synthetic_manifest_core(fixture)
    phase_b_manifest = phase_b_core["manifests"][0]
    owner_paths = sorted({source["path"] for source in core["sources"]})
    core_path = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
    ledger_path = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
    receipt_path = core["phaseReceipts"][0]["path"]

    manifest.update({
        "baseCommit": fixture.base_commit,
        "canonicalCommit": fixture.base_commit,
        "discoveryRules": [{
            "id": "DISC-A-001",
            "includeGlobs": owner_paths,
            "excludeGlobs": ["90_ARCHIVE/**"],
            "parser": "MARKDOWN",
            "rationale": "The seven frozen Phase-A requirements select their exact owners.",
        }],
        "candidateFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in owner_paths
        ],
        "candidateFileCount": len(owner_paths),
        "includedFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in owner_paths
        ],
        "finalFiles": [],
        "finalFileCount": 0,
        "excludedPaths": [],
        "eligibleFileCount": len(owner_paths),
        "scannedFileCount": len(owner_paths),
        "inventoryReviewPaths": ["03_METHODOLOGY/phase-a-inventory-review.md"],
        "protectedProvenance": _copy(phase_b_manifest["protectedProvenance"]),
        "protectedPaths": _copy(phase_b_manifest["protectedPaths"]),
        "protectedTreeSnapshots": _copy(phase_b_manifest["protectedTreeSnapshots"]),
        "allowedChangePaths": sorted({
            core_path,
            ledger_path,
            receipt_path,
            "03_METHODOLOGY/phase-a-inventory-review.md",
            *owner_paths,
        }),
        "closureOnlyPaths": [],
        "allowedPreexistingUntracked": _copy(
            phase_b_manifest["allowedPreexistingUntracked"]
        ),
    })
    for source in core["sources"]:
        source["sha256"] = _synthetic_file_record(
            fixture.canonical_root, source["path"]
        )["sha256"]
    return core


def build_committed_predecessor_fixture(
    fixture: SyntheticGitRepository,
    *,
    terminal_status: str = "FAILED",
    include_verified_phase_a: bool = False,
) -> dict[str, Any]:
    if terminal_status not in {"FAILED", "ABANDONED"}:
        raise ValueError("terminal_status must be FAILED or ABANDONED")
    core = build_synthetic_manifest_core(
        fixture,
        include_verified_phase_a=include_verified_phase_a,
    )
    attempt = build_review_attempt(
        terminal_status,
        logic_attestation_id="ATT-LOGIC-001" if terminal_status == "FAILED" else None,
    )
    target_bytes = json.dumps(
        {"fixture": "terminal predecessor target"},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    target_hash = "sha256:" + hashlib.sha256(target_bytes).hexdigest()
    finding = build_review_finding() if terminal_status == "FAILED" else None
    attestation = build_review_attestation("LOGIC", "FAIL") if terminal_status == "FAILED" else None
    if attestation is not None and finding is not None:
        attestation["path"] = attempt["logicReviewPath"]
        attestation["reviewTargetDigest"] = target_hash
        review_bytes = build_review_markdown(attestation, [finding])
        review_hash = "sha256:" + hashlib.sha256(review_bytes).hexdigest()
        attempt["reviewSubjectDigest"] = target_hash
    else:
        review_bytes = None
        review_hash = None

    core["reviewAttempts"] = [
        attempt,
        *[
            existing
            for existing in core["reviewAttempts"]
            if existing.get("phase") != "B"
        ],
    ]
    core["reviewAttemptArtifacts"] = [{
        "attemptId": ATTEMPT_ID,
        "reviewTargetSha256": target_hash if terminal_status == "FAILED" else None,
        "logicReviewSha256": review_hash,
        "btjReviewSha256": None,
    }, *[
        existing
        for existing in core["reviewAttemptArtifacts"]
        if existing.get("attemptId") != ATTEMPT_ID
    ]]
    core["reviewAttestations"] = [
        *([attestation] if attestation is not None else []),
        *[
            existing
            for existing in core["reviewAttestations"]
            if existing.get("attemptId") != ATTEMPT_ID
        ],
    ]
    core["reviewFindings"] = [
        *([finding] if finding is not None else []),
        *[
            existing
            for existing in core["reviewFindings"]
            if existing.get("attemptId") != ATTEMPT_ID
        ],
    ]
    phase_b_receipt = next(
        value for value in core["phaseReceipts"] if value.get("phase") == "B"
    )
    phase_b_receipt["reviewAttemptId"] = ATTEMPT_ID
    manifest = core["manifests"][0]
    manifest["finalFiles"] = [
        _synthetic_file_record(fixture.isolated_root, record["path"])
        for record in manifest["includedFiles"]
    ]
    manifest["finalFileCount"] = len(manifest["finalFiles"])
    manifest["closureOnlyPaths"] = sorted((
        attempt["reviewTargetPath"],
        attempt["logicReviewPath"],
        attempt["btjReviewPath"],
        attempt["validationBundlePath"],
    ))
    manifest["allowedChangePaths"] = sorted(set(
        manifest["allowedChangePaths"] + manifest["closureOnlyPaths"]
    ))

    if terminal_status == "FAILED":
        target_path = fixture.isolated_root / attempt["reviewTargetPath"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(target_bytes)
        review_path = fixture.isolated_root / attempt["logicReviewPath"]
        review_path.parent.mkdir(parents=True, exist_ok=True)
        if review_bytes is None:
            raise AssertionError("FAILED predecessor review bytes were not built")
        review_path.write_bytes(review_bytes)
    receipt = phase_b_receipt
    (fixture.isolated_root / receipt["path"]).write_bytes(
        build_receipt_markdown(receipt)
    )
    core_path = fixture.isolated_root / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
    core_path.write_bytes(json.dumps(
        core,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n")
    relative_paths = [
        "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json",
        receipt["path"],
    ]
    if terminal_status == "FAILED":
        relative_paths.extend((attempt["reviewTargetPath"], attempt["logicReviewPath"]))
    _git_fixture_run(fixture.isolated_root, "add", "--", *relative_paths)
    _git_fixture_run(fixture.isolated_root, "commit", "-m", "terminal predecessor")
    return core


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
    "triedHash": "sha256-text-lf:31f95b540bf7ee77f2b18646510c4ac34f1d6850345e5fba3853b039615cbc0f",
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


def markdown_fence(label: str, value: Any, *, newline: bytes = b"\n") -> bytes:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return (
        b"```json " + label.encode("ascii") + newline
        + payload + newline
        + b"```" + newline
    )


def build_ledger_markdown(
    seams: list[dict[str, Any]],
    *,
    newline: bytes = b"\n",
    preamble: bytes | None = None,
    prefixes: list[bytes] | None = None,
    suffixes: list[bytes] | None = None,
) -> bytes:
    preamble = b"# Golden Seam Ledger" + newline + newline if preamble is None else preamble
    prefixes = prefixes or [b"Human narrative before the fence." for _ in seams]
    suffixes = suffixes or [b"Human narrative after the fence." for _ in seams]
    sections: list[bytes] = []
    for seam, prefix, suffix in zip(seams, prefixes, suffixes, strict=True):
        sections.append(
            b"## " + seam["id"].encode("ascii") + newline
            + prefix + newline
            + markdown_fence("kintsugi-seam", seam, newline=newline)
            + suffix + newline
        )
    return preamble + b"".join(sections)


def build_receipt_markdown(
    receipt: dict[str, Any],
    *,
    newline: bytes = b"\n",
    prefix: bytes = b"# Synthetic receipt\n\nFrozen human claim.\n",
    suffix: bytes = b"Human provenance note.\n",
) -> bytes:
    if newline != b"\n":
        prefix = prefix.replace(b"\n", newline)
        suffix = suffix.replace(b"\n", newline)
    return prefix + markdown_fence("kintsugi-receipt", receipt, newline=newline) + suffix


def build_review_markdown(
    attestation: dict[str, Any],
    findings: list[dict[str, Any]],
    *,
    newline: bytes = b"\n",
) -> bytes:
    return (
        b"# Independent review" + newline + newline
        + markdown_fence("kintsugi-review", attestation, newline=newline)
        + b"Review findings follow." + newline
        + markdown_fence("kintsugi-review-findings", findings, newline=newline)
    )


def build_public_queue_markdown(
    queue: dict[str, Any], *, newline: bytes = b"\n"
) -> bytes:
    return (
        b"# Phase-C public queue" + newline + newline
        + markdown_fence("kintsugi-public-queue", queue, newline=newline)
    )


def build_owner_sync_fixture(
    root: Path, *, newline: str = "\n"
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], Path]:
    relative = "03_METHODOLOGY/owner.md"
    owner = root / relative
    owner.parent.mkdir(parents=True, exist_ok=True)
    anchor = "## Synthetic owner anchor"
    before_quote = "The former owner claim.\nIts second line."
    after_quote = "The repaired owner claim.\nIts second line."
    text = f"# Owner\n\n{anchor}\n\n{after_quote}\n"
    raw = text.replace("\n", newline).encode("utf-8")
    owner.write_bytes(raw)

    def quote_hash(value: str) -> str:
        normalized = value.replace("\r\n", "\n").replace("\r", "\n")
        return "sha256-text-lf:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    source = {
        "id": "SRC-A-001",
        "path": relative,
        "kind": "OWNER",
        "phases": ["A"],
        "sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "authorityRole": "SEMANTIC_OWNER",
    }
    claim = {
        "id": "CLM-A-001",
        "ownerSourceId": source["id"],
        "ownerAnchor": anchor,
    }
    trial = {
        "id": "TRL-A-001",
        "claimId": claim["id"],
        "triedQuote": before_quote,
        "triedHash": quote_hash(before_quote),
    }
    seam = {
        "id": "KIN-A-001",
        "claimId": claim["id"],
        "ownerSource": source["id"],
        "ownerAnchor": anchor,
        "beforeQuote": before_quote,
        "beforeHash": quote_hash(before_quote),
        "afterQuote": after_quote,
        "status": "REPAIRED",
    }
    return source, claim, trial, seam, owner


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


PHASE_A_REQUIREMENTS = (
    (
        "REQ-A-PROTOCOL-SELF-TRIAL",
        "00_META/00_THE_KINTSUGI_PROTOCOL.md",
        "# The Kintsugi Protocol",
        "sha256-text-lf:9fe68c734bce6c709c5879e0f7e40b552cdacb4cd14121302371509fb13f7cc9",
    ),
    (
        "REQ-A-TRIADIC-UNIQUENESS",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/11_EFR_TRIADIC_STABILITY.md",
        "## The Uniqueness Theorem",
        "sha256-text-lf:438269d12273e6c169e2ba8bdb8c126dcb118378a1d28a55328aa4dbdaec17b8",
    ),
    (
        "REQ-A-D6-AREA-DIRECTION",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
        "### 2.2 The Coordinate Collapse Theorem",
        "sha256-text-lf:75893a2cd097580c3ee44a8a62f940e9b02d3dc09e4d73a5d3796e70de7d8e26",
    ),
    (
        "REQ-A-POWER-MAX-CIRCULARITY",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
        "## The Statement",
        "sha256-text-lf:8cb12ae6fb3b855cbe999d699041ae3a15c73d3c405362195f6bf58441019510",
    ),
    (
        "REQ-A-D4-D5-REGISTER",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "## I. THE FUNDAMENTAL DISTINCTION",
        "sha256-text-lf:dee381fece54b4fe926b1af1145ab8676263091cc698460a3b37962c77a6cca2",
    ),
    (
        "REQ-A-QUANTUM-MEASURE",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
        "## The Corrected Formula",
        "sha256-text-lf:41b8437a8e8715a7be6f8f7ddef46984b89757d9f9722494b554dc3e87d204fb",
    ),
    (
        "REQ-A-OPTION-CONE",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "### Worldline and Light-Cone Corollary",
        "sha256-text-lf:6749c86499b1e5d1a04de8afcbc6df283403617f1d0e40bdf9dbe66073412527",
    ),
)


PHASE_A_QUOTES = {
    "REQ-A-PROTOCOL-SELF-TRIAL": (
        "**A repaired claim outranks an untested one.** A seam is not an apology — it is\n"
        "a *verification mark*: this line was attacked by a named adversary, broke in a\n"
        "specific way, and the repair survived re-trial. Pristine surfaces carry no such\n"
        "evidence. Therefore: **seams are prestige, erasure is the only disgrace.**\n"
        "Corollary for readers: trust the seamed passage *more*."
    ),
    "REQ-A-TRIADIC-UNIQUENESS": (
        "**Theorem:** The triadic multiplicative structure Zero-Sum Resolution Equation "
        "is the unique stable configuration."
    ),
    "REQ-A-D6-AREA-DIRECTION": "(iv) As ν₀ → 0⁺: Area → 4π (the full sphere)",
    "REQ-A-POWER-MAX-CIRCULARITY": (
        "The individual optimum is searched only\n"
        "inside the admissible `η = 0` game; on that frontier, degrading the holobiont\n"
        "degrades the field that returns as the individual's future viability. Without\n"
        "the `η = 0` constraint, the derivative still shows interdependence, but it does\n"
        "not by itself make cooperation dominant."
    ),
    "REQ-A-D4-D5-REGISTER": (
        "| **Quantum** | Potential (Copenhagen pre-collapse) | Actuality — Many-Worlds "
        "(distributed D5) or Copenhagen selected (singular D5) |"
    ),
    "REQ-A-QUANTUM-MEASURE": (
        "μ(P→F) = lim[δt→0] { Sample[ ∫ |ψ(s)|² ds ] } = F"
    ),
    "REQ-A-OPTION-CONE": (
        "Humans differ because their light cone is **wider, longer, and generalized.**"
    ),
}


def build_justice_context(
    regime: str = "NOT_APPLICABLE", mechanism: str = "NONE"
) -> dict[str, Any]:
    return {
        "individual": "The affected natural person.",
        "whole": "The sustaining whole.",
        "eta": "Zero extraction is declared.",
        "beneficiary": ["The affected natural person"],
        "costBearer": ["The affected natural person"],
        "consent": {"status": "OBTAINED", "basis": "Explicit fixture consent."},
        "custody": "The person retains custody.",
        "reversibility": "REVERSIBLE",
        "exit": "Grace Exit remains available.",
        "optionConeEffect": {
            "direction": "WIDENS",
            "rationale": "The declared option set remains non-extractive.",
        },
        "authority": {
            "regime": regime,
            "mechanism": mechanism,
            "basis": "A typed synthetic authority boundary.",
        },
    }


def build_semantic_core(*, bootstrap: bool = False) -> dict[str, Any]:
    """Return a complete, schema-valid Phase-A vessel for semantic tests."""
    core = build_core_data()
    sources_by_path: dict[str, dict[str, Any]] = {}
    sources: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    trials: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []

    for index, (requirement, owner_path, anchor, target_hash) in enumerate(
        PHASE_A_REQUIREMENTS, start=1
    ):
        source = sources_by_path.get(owner_path)
        if source is None:
            source = _copy(_SOURCE)
            source["id"] = f"SRC-A-{len(sources) + 1:03d}"
            source["path"] = owner_path
            source["phases"] = ["A"]
            sources_by_path[owner_path] = source
            sources.append(source)

        claim = _copy(_CLAIM)
        claim_id = f"CLM-A-{index:03d}"
        proposition = f"The frozen Phase-A requirement {requirement} is explicitly trialed."
        claim.update({
            "id": claim_id,
            "ownerSourceId": source["id"],
            "ownerAnchor": anchor,
            "proposition": proposition,
            "conclusion": proposition,
        })
        claim["typedTerms"][0].update({
            "symbol": f"x{index}",
            "definition": f"The typed term for {requirement}.",
        })
        claim["premises"][0].update({
            "id": f"PREM-A-{index:03d}",
            "sourceIds": [source["id"]],
        })
        claims.append(claim)

        trial = _copy(_TRIAL)
        trial.update({
            "id": f"TRL-A-{index:03d}",
            "claimId": claim_id,
            "manifestId": "MAN-A-001",
            "triedQuote": PHASE_A_QUOTES[requirement],
            "triedHash": target_hash,
            "receiptId": "REC-A-108",
        })
        trials.append(trial)
        bindings.append({
            "requirementId": requirement,
            "claimId": claim_id,
            "ownerSourceId": source["id"],
            "ownerAnchor": anchor,
            "targetHash": target_hash,
            "rationale": "The exact frozen requirement is bound to one claim and trial.",
        })

    unique_paths = sorted(sources_by_path)
    manifest = _copy(_MANIFEST)
    manifest.update({
        "id": "MAN-A-001",
        "phase": "A",
        "discoveryRules": [{
            "id": "DISC-A-001",
            "includeGlobs": ["**/*.md"],
            "excludeGlobs": ["90_ARCHIVE/**"],
            "parser": "MARKDOWN",
            "rationale": "A closed synthetic Phase-A discovery boundary.",
        }],
        "candidateFiles": [_file(path) for path in unique_paths],
        "candidateFileCount": len(unique_paths),
        "includedFiles": [_file(path) for path in unique_paths],
        "finalFiles": [],
        "finalFileCount": 0,
        "eligibleFileCount": len(unique_paths),
        "scannedFileCount": len(unique_paths),
        "harvestedClaimIds": [claim["id"] for claim in claims],
        "requiredClaimBindings": bindings,
        "eligibleClaimCount": len(claims),
        "trialedClaimIds": [] if bootstrap else [claim["id"] for claim in claims],
        "trialedClaimCount": 0 if bootstrap else len(claims),
        "inventoryReviewPaths": ["03_METHODOLOGY/phase-a-inventory-review.md"],
        "closureOnlyPaths": [],
    })

    receipt = _copy(_PHASE_RECEIPT)
    receipt.update({
        "id": "REC-A-108",
        "phase": "A",
        "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md",
        "manifestId": "MAN-A-001",
        "dependsOnReceiptIds": [],
        "claimIds": [claim["id"] for claim in claims],
        "trialIds": [] if bootstrap else [trial["id"] for trial in trials],
    })

    core.update({
        "manifests": [manifest],
        "sources": sources,
        "claims": claims,
        "trials": [] if bootstrap else trials,
        "phaseReceipts": [receipt],
        "seams": [],
        "antibodies": [],
        "discriminators": [],
        "fixtures": [],
        "propagations": [],
        "reviewAttempts": [],
        "reviewAttemptArtifacts": [],
        "reviewAttestations": [],
        "reviewFindings": [],
        "reviewFindingDispositions": [],
    })
    return core


def _prepend_verified_phase_a_dependency(
    core: dict[str, Any], fixture: SyntheticGitRepository
) -> None:
    """Add the complete verified predecessor required by a Phase-B vessel.

    The synthetic Phase-B record remains first so legacy fixture mutations keep
    addressing the selected vessel. Production validators select records by
    typed phase/ID, never by array position.
    """
    phase_a = build_semantic_core(bootstrap=False)
    manifest = phase_a["manifests"][0]
    receipt = phase_a["phaseReceipts"][0]
    phase_b_manifest = next(
        value for value in core["manifests"] if value.get("phase") == "B"
    )
    owner_paths = sorted(source["path"] for source in phase_a["sources"])
    closure_paths = sorted((
        _PHASE_A_TARGET_PATH,
        _PHASE_A_LOGIC_PATH,
        _PHASE_A_BTJ_PATH,
        _PHASE_A_BUNDLE_PATH,
    ))
    manifest.update({
        "baseCommit": fixture.base_commit,
        "canonicalCommit": fixture.base_commit,
        "discoveryRules": [{
            "id": "DISC-A-001",
            "includeGlobs": owner_paths,
            "excludeGlobs": ["90_ARCHIVE/**"],
            "parser": "MARKDOWN",
            "rationale": "The verified synthetic predecessor freezes its exact owners.",
        }],
        "candidateFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in owner_paths
        ],
        "candidateFileCount": len(owner_paths),
        "includedFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in owner_paths
        ],
        "finalFiles": [
            _synthetic_file_record(fixture.canonical_root, relative)
            for relative in owner_paths
        ],
        "finalFileCount": len(owner_paths),
        "excludedPaths": [],
        "eligibleFileCount": len(owner_paths),
        "scannedFileCount": len(owner_paths),
        "inventoryReviewPaths": ["03_METHODOLOGY/phase-a-inventory-review.md"],
        "protectedProvenance": _copy(phase_b_manifest["protectedProvenance"]),
        "protectedPaths": _copy(phase_b_manifest["protectedPaths"]),
        "protectedTreeSnapshots": _copy(phase_b_manifest["protectedTreeSnapshots"]),
        "allowedChangePaths": sorted({
            "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json",
            "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md",
            receipt["path"],
            "03_METHODOLOGY/phase-a-inventory-review.md",
            *owner_paths,
            *closure_paths,
        }),
        "closureOnlyPaths": closure_paths,
        "allowedPreexistingUntracked": _copy(
            phase_b_manifest["allowedPreexistingUntracked"]
        ),
    })
    for source in phase_a["sources"]:
        source["sha256"] = _synthetic_file_record(
            fixture.canonical_root, source["path"]
        )["sha256"]

    artifacts = _phase_a_dependency_artifacts()
    attempt = {
        "id": _PHASE_A_ATTEMPT_ID,
        "phase": "A",
        "receiptId": receipt["id"],
        "supersedesAttemptId": None,
        "reviewTargetPath": _PHASE_A_TARGET_PATH,
        "logicReviewPath": _PHASE_A_LOGIC_PATH,
        "btjReviewPath": _PHASE_A_BTJ_PATH,
        "validationBundlePath": _PHASE_A_BUNDLE_PATH,
        "logicAttestationId": "ATT-LOGIC-A-001",
        "btjAttestationId": "ATT-BTJ-A-001",
        "status": "PASSED",
        "abandonReason": None,
        "reviewSubjectDigest": artifacts["targetHash"],
    }
    artifact = {
        "attemptId": _PHASE_A_ATTEMPT_ID,
        "reviewTargetSha256": artifacts["targetHash"],
        "logicReviewSha256": artifacts["logicHash"],
        "btjReviewSha256": artifacts["btjHash"],
    }
    receipt.update({
        "status": "VERIFIED",
        "reviewTargetDigest": artifacts["targetHash"],
        "validationBundlePath": _PHASE_A_BUNDLE_PATH,
        "validationDigest": artifacts["bundleHash"],
        "logicReviewPath": _PHASE_A_LOGIC_PATH,
        "btjReviewPath": _PHASE_A_BTJ_PATH,
        "reviewAttemptId": _PHASE_A_ATTEMPT_ID,
    })

    core["manifests"] = [*core["manifests"], manifest]
    core["sources"] = [*core["sources"], *phase_a["sources"]]
    core["claims"] = [*core["claims"], *phase_a["claims"]]
    core["trials"] = [*core["trials"], *phase_a["trials"]]
    # Receipt order is semantic and must remain A, B, C.
    core["phaseReceipts"] = [receipt, *core["phaseReceipts"]]
    core["reviewAttempts"] = [*core["reviewAttempts"], attempt]
    core["reviewAttemptArtifacts"] = [*core["reviewAttemptArtifacts"], artifact]
    core["reviewAttestations"] = [
        *core["reviewAttestations"],
        *_copy(artifacts["attestations"]),
    ]


def add_confirmed_seam(core: dict[str, Any], *, seam_id: str = "KIN-A-001") -> dict[str, Any]:
    claim = core["claims"][0]
    trial = next(trial for trial in core["trials"] if trial["claimId"] == claim["id"])
    receipt = next(
        value
        for value in core["phaseReceipts"]
        if value.get("id") == trial.get("receiptId")
    )
    fixture_id = f"FXT-{seam_id}"
    gate = {
        "status": "PENDING",
        "rationale": "Awaiting the independent review artifact.",
        "reviewerPath": None,
    }
    seam = {
        "id": seam_id,
        "claimId": claim["id"],
        "ownerSource": claim["ownerSourceId"],
        "ownerAnchor": claim["ownerAnchor"],
        "beforeQuote": trial["triedQuote"],
        "beforeHash": trial["triedHash"],
        "priorSeamIds": [],
        "claimType": claim["claimType"],
        "typedTerms": _copy(claim["typedTerms"]),
        "premises": _copy(claim["premises"]),
        "conclusion": claim["conclusion"],
        "inference": _copy(claim["inference"]),
        "quantifiers": _copy(claim["quantifiers"]),
        "modality": claim["modality"],
        "scope": _copy(claim["scope"]),
        "justiceScope": claim["justiceScope"],
        "authorityScope": claim["authorityScope"],
        "authorityEffect": claim["authorityEffect"],
        "evidenceBefore": _copy(claim["evidence"]),
        "sourceIds": [claim["ownerSourceId"]],
        "dependencyClaimIds": _copy(claim["dependencyClaimIds"]),
        "countermodel": {
            "description": "A declared countermodel fractures the tried formulation.",
            "construction": "Negate the tried conclusion inside its stated scope.",
            "defeatedConclusion": "The tried conclusion is defeated.",
        },
        "defectClass": "TYPE_ERROR",
        "severity": "MAJOR",
        "validityVerdict": "INVALID",
        "soundnessVerdict": "NOT_APPLICABLE",
        "verdict": "INVALID",
        "survivingKernel": "Only the explicitly typed lower-register statement survives.",
        "priorSupportLinks": _copy(claim["supportLinks"]),
        "priorUpgradeCriterion": _copy(claim["upgradeCriterion"]),
        "priorKillCriterion": _copy(claim["killCriterion"]),
        "priorSurvivingIfKilled": _copy(claim["survivingIfKilled"]),
        "supportLinks": _copy(claim["supportLinks"]),
        "upgradeCriterion": _copy(claim["upgradeCriterion"]),
        "killCriterion": _copy(claim["killCriterion"]),
        "survivingIfKilled": _copy(claim["survivingIfKilled"]),
        "beautyGate": _copy(gate),
        "truthGate": _copy(gate),
        "justiceGate": _copy(gate),
        "credit": {"displayName": "Synthetic reviewer", "role": "Fixture author"},
        "creditConsent": "ALIAS",
        "receiptId": receipt["id"],
        "regressionFixtureIds": [fixture_id],
        "discriminatorIds": [],
        "status": "CONFIRMED",
    }
    trial.update({
        "breakState": "CONFIRMED",
        "defectClass": "TYPE_ERROR",
        "severity": "MAJOR",
        "validityVerdict": "INVALID",
        "soundnessVerdict": "NOT_APPLICABLE",
        "verdict": "INVALID",
        "seamId": seam_id,
        "status": "ADJUDICATED",
        "countermodel": _copy(seam["countermodel"]),
    })
    fixture = {
        "id": fixture_id,
        "kind": "MUTATION",
        "payloadKind": "JSON",
        "payload": "{}",
        "mutationLevel": "SEMANTIC",
        "expectedExitCode": 1,
        "expectedErrorCodes": ["KIN-E-STATE"],
        "expectedAntibodyIds": [],
        "antibodyIds": [],
        "seamIds": [seam_id],
    }
    core["seams"].append(seam)
    core["fixtures"].append(fixture)
    receipt["seamIds"].append(seam_id)
    return seam


def add_antibody_fixture_set(
    core: dict[str, Any], *, match_mode: str = "LITERAL", pattern: str = "forbidden"
) -> dict[str, Any]:
    if not core["seams"]:
        add_confirmed_seam(core)
    antibody_id = f"AB-{match_mode}-001"
    fixture_ids = {
        "POSITIVE": f"FXT-{match_mode}-POS",
        "NEGATIVE": f"FXT-{match_mode}-NEG",
        "QUOTATION": f"FXT-{match_mode}-QUO",
        "HISTORICAL": f"FXT-{match_mode}-HIS",
    }
    antibody = {
        "id": antibody_id,
        "seamId": core["seams"][0]["id"],
        "pattern": pattern,
        "matchMode": match_mode,
        "semanticEvaluator": None,
        "scopeGlobs": ["active/**/*.md"],
        "excludeGlobs": ["active/excluded/**"],
        "positiveFixtureIds": [fixture_ids["POSITIVE"]],
        "negativeFixtureIds": [fixture_ids["NEGATIVE"]],
        "quotationFixtureIds": [fixture_ids["QUOTATION"]],
        "historicalFixtureIds": [fixture_ids["HISTORICAL"]],
    }
    live_match = "forbidden" if match_mode == "REGEX" else pattern
    payloads = {
        "POSITIVE": f"This is {live_match} in active prose.",
        "NEGATIVE": "This prose remains clean.",
        "QUOTATION": f"A quotation repeats {live_match}.",
        "HISTORICAL": f"History records {live_match}.",
    }
    for kind, fixture_id in fixture_ids.items():
        expected = [antibody_id] if kind == "POSITIVE" else []
        core["fixtures"].append({
            "id": fixture_id,
            "kind": kind,
            "payloadKind": "TEXT",
            "payload": payloads[kind],
            "mutationLevel": None,
            "expectedExitCode": 1 if kind == "POSITIVE" else 0,
            "expectedErrorCodes": ["KIN-E-FIXTURE"] if kind == "POSITIVE" else [],
            "expectedAntibodyIds": expected,
            "antibodyIds": [antibody_id],
            "seamIds": [core["seams"][0]["id"]] if kind == "POSITIVE" else [],
        })
    core["antibodies"].append(antibody)
    return antibody


def add_semantic_antibody_fixture_set(
    core: dict[str, Any], evaluator: str, good_payload: dict[str, Any], bad_payload: dict[str, Any]
) -> dict[str, Any]:
    if not core["seams"]:
        add_confirmed_seam(core)
    antibody_id = f"AB-SEM-{len(core['antibodies']) + 1:03d}"
    fixture_ids = {
        "POSITIVE": f"FXT-{antibody_id}-POS",
        "NEGATIVE": f"FXT-{antibody_id}-NEG",
        "QUOTATION": f"FXT-{antibody_id}-QUO",
        "HISTORICAL": f"FXT-{antibody_id}-HIS",
    }
    antibody = {
        "id": antibody_id,
        "seamId": core["seams"][0]["id"],
        "pattern": evaluator,
        "matchMode": "SEMANTIC_FIXTURE",
        "semanticEvaluator": evaluator,
        "scopeGlobs": ["active/**/*.md"],
        "excludeGlobs": [],
        "positiveFixtureIds": [fixture_ids["POSITIVE"]],
        "negativeFixtureIds": [fixture_ids["NEGATIVE"]],
        "quotationFixtureIds": [fixture_ids["QUOTATION"]],
        "historicalFixtureIds": [fixture_ids["HISTORICAL"]],
    }
    for kind, fixture_id in fixture_ids.items():
        expected = [antibody_id] if kind == "POSITIVE" else []
        payload = bad_payload if kind in {"POSITIVE", "QUOTATION", "HISTORICAL"} else good_payload
        core["fixtures"].append({
            "id": fixture_id,
            "kind": kind,
            "payloadKind": "JSON",
            "payload": json.dumps(payload, sort_keys=True, separators=(",", ":")),
            "mutationLevel": None,
            "expectedExitCode": 1 if kind == "POSITIVE" else 0,
            "expectedErrorCodes": ["KIN-E-FIXTURE"] if kind == "POSITIVE" else [],
            "expectedAntibodyIds": expected,
            "antibodyIds": [antibody_id],
            "seamIds": [core["seams"][0]["id"]] if kind == "POSITIVE" else [],
        })
    core["antibodies"].append(antibody)
    return antibody


def add_retiered_seam(
    core: dict[str, Any], before: str, after: str, *, seam_id: str = "KIN-A-001"
) -> dict[str, Any]:
    order = {"C": 0, "I": 1, "S": 2, "A": 3}
    if before == after:
        raise ValueError("the schema-valid RETIER helper requires unequal strengths")
    seam = add_confirmed_seam(core, seam_id=seam_id)
    claim = core["claims"][0]
    supporting_claim = core["claims"][1]
    upward = order[after] > order[before]

    claim["evidence"] = {"strength": after, "sourced": True, "lifecycle": "ACTIVE"}
    claim["upgradeCriterion"] = {
        "kind": "NONE",
        "rationale": "No further promotion is asserted by this repaired fixture.",
    }
    claim["killCriterion"] = {
        "kind": "TESTABLE",
        "testability": "ACTIVE",
        "trigger": "The repaired typed claim fails its declared test.",
        "method": "Run the frozen discriminator.",
        "disposition": "RETRACT",
    }

    if upward:
        link = {
            "id": f"SUP-{seam_id}",
            "supportingClaimId": supporting_claim["id"],
            "mode": "CORROBORATION",
            "independenceStatus": "INDEPENDENT",
            "evidenceCeiling": after,
            "rationale": "An independently trialed supporting claim.",
        }
        claim["supportLinks"] = [link]
        prior_upgrade = {
            "kind": "AVAILABLE",
            "targetStrength": after,
            "criterion": "A qualifying independent corroboration closes successfully.",
            "requiredMode": "CORROBORATION",
            "minimumIndependence": "PARTIALLY_INDEPENDENT",
            "minimumEvidenceCeiling": after,
        }
        prior_kill = {
            "kind": "TESTABLE",
            "testability": "ACTIVE",
            "trigger": "The prior claim fails its declared test.",
            "method": "Run the frozen discriminator.",
            "disposition": "RETRACT",
        }
        seam["upgradeEvidenceLinkIds"] = [link["id"]]
    else:
        prior_upgrade = {
            "kind": "NONE",
            "rationale": "No promotion criterion is implicated by a downgrade.",
        }
        prior_kill = {
            "kind": "TESTABLE",
            "testability": "ACTIVE",
            "trigger": "The prior tier ceiling is defeated.",
            "method": "Apply the declared kill discriminator.",
            "disposition": "RETIER",
            "resultingStrength": after,
        }

    seam.update({
        "status": "REPAIRED",
        "repairKind": "RETIER",
        "afterQuote": f"The repaired claim is explicitly bounded at {after}.",
        "evidenceBefore": {"strength": before, "sourced": True, "lifecycle": "ACTIVE"},
        "evidenceAfter": _copy(claim["evidence"]),
        "priorSupportLinks": [],
        "priorUpgradeCriterion": prior_upgrade,
        "priorKillCriterion": prior_kill,
        "supportLinks": _copy(claim["supportLinks"]),
        "upgradeCriterion": _copy(claim["upgradeCriterion"]),
        "killCriterion": _copy(claim["killCriterion"]),
        "survivingIfKilled": _copy(claim["survivingIfKilled"]),
    })
    return seam


def add_retracted_seam(
    core: dict[str, Any], strength: str = "C", *, seam_id: str = "KIN-A-001"
) -> dict[str, Any]:
    seam = add_confirmed_seam(core, seam_id=seam_id)
    claim = core["claims"][0]
    before = {"strength": strength, "sourced": True, "lifecycle": "ACTIVE"}
    claim["evidence"] = {"strength": strength, "sourced": True, "lifecycle": "RETIRED"}
    claim["killCriterion"] = {
        "kind": "NONE",
        "rationale": "The retracted claim has no live kill criterion.",
    }
    claim["upgradeCriterion"] = {
        "kind": "NONE",
        "rationale": "The retracted claim has no asserted upgrade path.",
    }
    seam.update({
        "status": "RETRACTED",
        "repairKind": "RETRACT",
        "afterQuote": "The claim is retracted while its historical tier is preserved.",
        "evidenceBefore": before,
        "evidenceAfter": _copy(claim["evidence"]),
        "priorSupportLinks": [],
        "priorUpgradeCriterion": _copy(claim["upgradeCriterion"]),
        "priorKillCriterion": {
            "kind": "TESTABLE",
            "testability": "ACTIVE",
            "trigger": "The claim's declared falsifier fires.",
            "method": "Apply the frozen discriminator.",
            "disposition": "RETRACT",
        },
        "supportLinks": [],
        "upgradeCriterion": _copy(claim["upgradeCriterion"]),
        "killCriterion": _copy(claim["killCriterion"]),
        "survivingIfKilled": _copy(claim["survivingIfKilled"]),
    })
    return seam

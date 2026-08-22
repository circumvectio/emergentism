#!/usr/bin/env python3
"""Re-check 00_WORK_IN_PROGRESS/README.md against the corpus it describes.

WHY. A manifest of open work has one characteristic failure: it drifts in the
direction that flatters us. Items quietly disappear when they go stale, counts stop
matching the registers they were copied from, and the folder slowly becomes a list of
things we have decided not to think about. 00_ESTABLISHED has a guard against
becoming a promotion path; this is the mirror guard against becoming a graveyard.

WHAT IS CHECKED
  · every count the manifest states is RECOMPUTED and must match
  · the entries that are still genuinely open must still be listed
  · the folder must keep declaring that it owns nothing
  · the "must never become" fences must survive

Exits 0 if the manifest still tells the truth, 1 otherwise.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
from posixpath import relpath as posix_relpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "00_WORK_IN_PROGRESS" / "README.md"
REGISTER = ROOT / "00_META" / "00_THE_CLAIM_STATUS_REGISTER.md"
# THE AUTHORITY. The .md above is a human mirror; this is the machine source. An
# earlier draft of this checker validated the manifest against its own parse of the
# mirror, which is circular AND disagreed with check_claim_status.py.
STATUS_YAML = ROOT / "00_META" / "claim_status" / "CLAIM_STATUS.yaml"
RECEIPT_DIRS = (
    ROOT / "11_UPLINK" / "50_AUDITS_AND_EXECUTIONS",
    ROOT / "11_UPLINK" / "60_SESSION_PACKETS",
)
CLOSURE_RECEIPT_DIR = ROOT / "11_UPLINK" / "50_AUDITS_AND_EXECUTIONS"
CONTACT_LIMITED_STATE_REL = Path("00_META/CONTACT_LIMITED_STATE.json")
COHERENCE_PROFILE_REL = Path("09_TOOLS/01_SCRIPTS/coherence_profile.json")
REVIEW_REGISTRY_REL = Path(
    "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/GATE_REGISTRY.json"
)
OWNER_DOCKET_REL = Path("00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md")
OWNER_DOCKET_WIP_PATH = posix_relpath(
    OWNER_DOCKET_REL.as_posix(), MANIFEST.parent.relative_to(ROOT).as_posix()
)
WIP_MANIFEST_REL = MANIFEST.relative_to(ROOT).as_posix()
CONTACT_LIMITED_STATE_SCHEMA = "emergentism/contact-limited-state/v1"
COHERENCE_PROFILE_SCHEMA = "emergentism/coherence-profile/v1"
REVIEW_REGISTRY_SCHEMA = "emergentism/finity-practice-gate-registry/v4"
ROUTING_BASIS_REF = (
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
    "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md"
)
ROUTING_BASIS_SHA256 = "623b237dead290986721ff3eed2aa8705a2c6a1afde0e7e6eff4d3c0f17f1905"

# Items that are open as of 2026-07-30. Removing one from the manifest requires a
# ruling to point at; this list is what makes "it went quiet" insufficient.
# G-0 was removed from this list on 2026-07-30 because it was RULED on 2026-07-29 and
# the manifest had been listing it as open — the guard was pinning a stale entry, which
# is the mirror of the failure it exists to prevent. It stays referenced in the manifest
# as CLOSED, and the checker below verifies that rather than its openness.
MUST_STAY_LISTED = ["GP-03"]
OWNER_HELD_SOURCE_ROWS = {
    "OWNER_GATE_HELD_PUBLIC_DOCS": {
        "docket_id": "D-OWNER-01",
        "state_debt": {
            "id": "OWNER_GATE_HELD_PUBLIC_DOCS",
            "owner": "01_EMERGENTISM editorial program",
            "question": (
                "Which numbered-doctrine-spine specification is the current public-document "
                "owner, and what custody should the byte-identical duplicate retain?"
            ),
            "close_when": (
                "A dated owner ruling names the current artifact and either routes or explicitly "
                "retains the duplicate, with both resulting paths checked."
            ),
            "evidence": [
                "00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md",
                "12_PUBLIC_SITE/_PLANS/specs/2026-06-05-numbered-doctrine-spine-design.md",
                "12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md",
                "09_TOOLS/01_SCRIPTS/coherence_profile.json",
            ],
            "receipt_ref": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_REPOSITORY_GATE_REPAIR_BASELINE_2026_08_22.md",
        },
        "question": (
            "Which byte-identical numbered-doctrine-spine copy is current planning "
            "owner, and what K3 custody does the other retain? **No selection is "
            "implied; the preselection guard keeps both copies regular, byte-identical, "
            "and excluded by the current local/predeploy deployment configuration.**"
        ),
        "blocks": "public planning/custody routing",
        "docket_decision": "Canonical owner for the byte-identical public planning duplicate",
        "docket_blocks": "current/custody routing of two public-site planning copies",
        "docket_selection_line": "- **Selected option:** **UNSET**.",
        "docket_principal_line": (
            "- **Principal:** **UNSET** (01_EMERGENTISM editorial owner must name one)."
        ),
    },
    "OWNER_GATE_OPEN_TOPOLOGY": {
        "docket_id": "D-OWNER-02",
        "state_debt": {
            "id": "OWNER_GATE_OPEN_TOPOLOGY",
            "owner": "01_EMERGENTISM editorial program",
            "question": (
                "How must the three grandfathered framework-support 00_META tombstones be "
                "disposed under the categorical root-only rule while preserving their custody?"
            ),
            "close_when": (
                "A dated owner ruling either amends the topology rule or supplies a complete "
                "migration or archival route; until then the exact path remains a hash-bound "
                "held violation."
            ),
            "evidence": [
                "00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md",
                "00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md",
                "08_FRAMEWORK_SUPPORT/00_META/CLAUDE.md",
                "08_FRAMEWORK_SUPPORT/00_META/00_MAGNUM_OPUS/CLAUDE.md",
                "08_FRAMEWORK_SUPPORT/00_META/02_ANALYSIS_DOCUMENTS/CLAUDE.md",
                "09_TOOLS/01_SCRIPTS/coherence_profile.json",
            ],
            "receipt_ref": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_REPOSITORY_GATE_REPAIR_BASELINE_2026_08_22.md",
        },
        "question": (
            "How must the three grandfathered tombstones under "
            "`08_FRAMEWORK_SUPPORT/00_META/` be disposed under the categorical root-only "
            "rule while preserving custody? **No move or conformance is implied; the "
            "preselection guard holds only the exact three hash-bound tombstones, reports "
            "the topology debt, and rejects any changed, missing, added, or symlinked entry.**"
        ),
        "blocks": "held topology violation",
        "docket_decision": (
            "Disposition of the grandfathered framework-support `00_META` tombstones "
            "under the root-only rule"
        ),
        "docket_blocks": "held topology violation",
        "docket_selection_line": "- **Selected option:** **UNSET**.",
        "docket_principal_line": (
            "- **Principal:** **UNSET** (01_EMERGENTISM editorial/topology owner must name one)."
        ),
    },
}
REVIEW_CONTACT_SOURCE_ROW = "FPE-REVIEW-CONTACT-AUTHORITY"
OPEN_SOURCE_MIRROR_ROWS = {
    **OWNER_HELD_SOURCE_ROWS,
    REVIEW_CONTACT_SOURCE_ROW: {
        "docket_id": "D-OWNER-03",
        "question": (
            "Who may make any later independent-review contact, under which bounded "
            "terms and ethics/applicability route? **No reviewer or contact is named.**"
        ),
        "blocks": "six review prerequisites and any invitation",
        "docket_decision": "Principal and bounded terms for any future independent-review contact",
        "docket_blocks": "the six nontechnical/material review prerequisites and any later invitation",
        "docket_selection_line": "- **Selected option:** **UNSET**.",
        "docket_principal_line": "- **Principal:** **UNSET**.",
    },
}
REVIEW_MISSING_PREREQUISITES = {
    "complete_review_materials_bundle",
    "conflict_form",
    "reviewer_scope_form",
    "compensation_terms",
    "publication_permission",
    "applicability_determination_recorded",
}
REVIEW_PREREQUISITE_IDS = REVIEW_MISSING_PREREQUISITES | {"bundle_manifest"}
REVIEW_EXTERNAL_STATE_IDS = {
    "data_collected",
    "ethics_determination_obtained",
    "independent_replication_exists",
    "participants_contacted",
    "preregistration_frozen",
    "results_exist",
    "reviewers_engaged",
}
LANDED_CLOSURES = {
    "§5.1": "193_FIVE_RULINGS_SIGNED_2026_07_31.md",
    "G-0": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "G-0b": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "FOUNDATION-KSC-04": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "KSC-02-ACTIVE-PROJECTION-DRIFT": "235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md",
    "BODY-SURVEY-04-06": "234_FULL_CORPUS_ADJUDICATION_AND_COHERENCE_CALIBRATION_2026_08_01.md",
    "PUBLIC-LIFECYCLE": "238_PUBLIC_LIFECYCLE_CLOSURE_2026_08_01.md",
    "CLAIM-DISPOSITION": "239_OPEN_CLAIM_DISPOSITION_2026_08_01.md",
}

FENCES = [
    "holds no doctrine",
    "owns nothing",
    "A promotion path",
    "A graveyard",
    "An authority",
]


def _load_review_bundle_policy():
    """Use the review bundle's source-owned provenance policy, not a WIP copy."""

    path = Path(__file__).with_name("check_review_bundle.py")
    spec = importlib.util.spec_from_file_location("review_bundle_policy_for_wip", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load review-bundle policy owner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_REVIEW_BUNDLE_POLICY = _load_review_bundle_policy()


def contained_regular_source(root: Path, relative: Path, label: str) -> Path:
    """Return one regular source file without crossing a symlink below ``root``."""

    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label} path must be safe and repository-relative")
    candidate = root / relative
    cursor = root
    try:
        for component in relative.parts:
            cursor /= component
            if cursor.is_symlink():
                raise ValueError(f"{label} path must not traverse a symlink")
        root_resolved = root.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing") from exc
    except (OSError, RuntimeError, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith(label):
            raise
        raise ValueError(f"{label} is unreadable: {exc}") from exc
    if not resolved.is_relative_to(root_resolved):
        raise ValueError(f"{label} path resolves outside the corpus")
    if not resolved.is_file():
        raise ValueError(f"{label} must be a regular file")
    return resolved


def read_source_text(root: Path, relative: Path, label: str) -> str:
    """Read a contained regular UTF-8 source file or return a diagnostic."""

    path = contained_regular_source(root, relative, label)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"{label} is unreadable: {exc.__class__.__name__}") from exc


def without_fenced_code_blocks(text: str) -> str | None:
    """Return visible Markdown; code, comments, and raw HTML fail closed."""

    if text.startswith("\ufeff") or "\r" in text:
        return None
    active: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^[ \t]*(`{3,}|~{3,})([^\n]*)", line)
        if fence is not None:
            if (
                match is not None
                and match.group(1)[0] == fence[0]
                and len(match.group(1)) >= fence[1]
                and not match.group(2).strip()
            ):
                fence = None
            continue
        if match is not None:
            fence = (match.group(1)[0], len(match.group(1)))
            continue
        active.append(line)
    if fence is not None:
        return None
    visible = re.sub(r"(?s)<!--.*?-->", "", "".join(active))
    if "<!--" in visible or "-->" in visible or "<" in visible:
        return None
    frontmatter_start = re.match(r"^---[ \t]*\n", visible)
    if frontmatter_start is not None:
        frontmatter_end = re.search(
            r"(?m)^(?:---|\.\.\.)[ \t]*(?:\n|\Z)",
            visible[frontmatter_start.end() :],
        )
        if frontmatter_end is None:
            return None
        visible = visible[frontmatter_start.end() + frontmatter_end.end() :]
    return visible


def load_json_object(root: Path, relative: Path, label: str) -> dict:
    """Load one unambiguous, contained JSON source object."""

    def reject_duplicate_keys(pairs):
        result: dict = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(
            read_source_text(root, relative, label), object_pairs_hook=reject_duplicate_keys
        )
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise ValueError(f"{label} is unreadable: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def owner_held_source_ids(root: Path) -> tuple[set[str], list[str]]:
    """Read the two owner-held rows from their state/profile machine owners."""

    errors: list[str] = []
    try:
        state = load_json_object(root, CONTACT_LIMITED_STATE_REL, "contact-limited state")
        profile = load_json_object(root, COHERENCE_PROFILE_REL, "coherence profile")
    except ValueError as exc:
        return set(), [str(exc)]
    if state.get("schema") != CONTACT_LIMITED_STATE_SCHEMA:
        errors.append("contact-limited state has an unexpected schema")
    if state.get("status") != "OPEN_INTERNAL":
        errors.append("contact-limited state must remain OPEN_INTERNAL")
    if profile.get("schema") != COHERENCE_PROFILE_SCHEMA:
        errors.append("coherence profile has an unexpected schema")
    overall = profile.get("overall")
    if not isinstance(overall, dict) or overall.get("state") != "PASS_WITH_DEBT":
        errors.append("coherence profile overall state must remain PASS_WITH_DEBT")
    owner_held = state.get("owner_held")
    if not isinstance(owner_held, dict):
        return set(), ["contact-limited state owner_held record is unreadable"]
    if owner_held.get("source_profile") != COHERENCE_PROFILE_REL.as_posix():
        errors.append("contact-limited owner_held record no longer names the coherence profile")
    debts = owner_held.get("debts")
    if not isinstance(debts, list):
        return set(), errors + ["contact-limited owner_held debts are unreadable"]
    state_ids = [item.get("id") for item in debts if isinstance(item, dict)]
    if len(state_ids) != len(debts) or not all(isinstance(item, str) for item in state_ids):
        return set(), errors + ["contact-limited owner_held debts need string ids"]
    if len(state_ids) != len(set(state_ids)):
        errors.append("contact-limited owner_held debts contain duplicate ids")

    axes = profile.get("axes")
    routing = axes.get("routing") if isinstance(axes, dict) else None
    if not isinstance(routing, dict):
        errors.append("coherence routing axis is unreadable")
        return set(state_ids), errors
    if routing.get("state") != "PASS_WITH_DEBT":
        errors.append("coherence routing state must remain PASS_WITH_DEBT")
    routing_basis_refs = routing.get("basis_refs")
    if (
        not isinstance(routing_basis_refs, list)
        or not routing_basis_refs
        or not all(isinstance(ref, str) and ref for ref in routing_basis_refs)
        or len(routing_basis_refs) != len(set(routing_basis_refs))
    ):
        errors.append("coherence routing basis_refs must be a non-empty unique string list")
    else:
        if routing_basis_refs != [ROUTING_BASIS_REF]:
            errors.append(
                "coherence routing basis_refs must remain the canonical receipt-only set"
            )
        try:
            wip_manifest = contained_regular_source(
                root, Path(WIP_MANIFEST_REL), "WIP manifest"
            )
        except ValueError as exc:
            errors.append(str(exc))
            wip_manifest = None
        for ref in routing_basis_refs:
            try:
                basis = contained_regular_source(
                    root, Path(ref), "coherence routing basis reference"
                )
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if wip_manifest is not None and basis.samefile(wip_manifest):
                errors.append("coherence routing basis_refs cannot cite the WIP manifest it mirrors")
            if ref == ROUTING_BASIS_REF:
                try:
                    digest = hashlib.sha256(basis.read_bytes()).hexdigest()
                except OSError as exc:
                    errors.append(
                        "coherence routing basis receipt is unreadable: "
                        f"{exc.__class__.__name__}"
                    )
                else:
                    if digest != ROUTING_BASIS_SHA256:
                        errors.append("coherence routing basis receipt digest drifted")
    profile_ids = routing.get("debt_ids")
    if not isinstance(profile_ids, list) or not all(isinstance(item, str) for item in profile_ids):
        errors.append("coherence routing debt_ids are unreadable")
        return set(state_ids), errors
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("coherence routing debt_ids contain duplicates")
    if set(state_ids) != set(profile_ids):
        errors.append("contact-limited owner-held debts drifted from coherence routing debt_ids")
    debts_by_id = {debt["id"]: debt for debt in debts if isinstance(debt, dict) and isinstance(debt.get("id"), str)}
    for debt_id, row in OWNER_HELD_SOURCE_ROWS.items():
        debt = debts_by_id.get(debt_id)
        if debt is not None and debt != row["state_debt"]:
            errors.append(
                f"contact-limited owner-held debt {debt_id} no longer matches its exact "
                "held source contract"
            )
    return set(state_ids), errors


def review_contact_authority_errors(root: Path) -> list[str]:
    """Keep the WIP contact row tied to the blocked, pre-authority review gate."""

    try:
        registry = load_json_object(root, REVIEW_REGISTRY_REL, "review gate registry")
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    if registry.get("schema") != REVIEW_REGISTRY_SCHEMA:
        errors.append("review gate registry has an unexpected schema")
    gates = registry.get("gates")
    if not isinstance(gates, list):
        return errors + ["review gate registry gates must be a list"]
    matches = [
        gate
        for gate in gates
        if isinstance(gate, dict) and gate.get("gate_id") == "FPE-REVIEW-01"
    ]
    if len(matches) != 1:
        return errors + [
            f"review gate registry must contain exactly one FPE-REVIEW-01, found {len(matches)}"
        ]
    gate = matches[0]
    execution = gate.get("execution")
    prerequisites = execution.get("prerequisites") if isinstance(execution, dict) else None
    if not isinstance(prerequisites, dict) or set(prerequisites) != REVIEW_PREREQUISITE_IDS:
        errors.append("FPE-REVIEW-01 prerequisites changed from the held review boundary")
    else:
        bundle = prerequisites["bundle_manifest"]
        if not isinstance(bundle, dict) or bundle.get("state") != "satisfied":
            errors.append("FPE-REVIEW-01 bundle_manifest must remain its bounded technical record")
        for name in REVIEW_MISSING_PREREQUISITES:
            record = prerequisites[name]
            if not isinstance(record, dict) or record.get("state") != "missing":
                errors.append(f"FPE-REVIEW-01 {name} is no longer missing")
    try:
        policy_errors = _REVIEW_BUNDLE_POLICY.review_provenance_errors(registry, gate)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"FPE-REVIEW-01 provenance is unreadable: {exc}")
        policy_errors = []
    errors.extend(f"FPE-REVIEW-01 provenance: {error}" for error in policy_errors)
    external_state = registry.get("external_state")
    if not isinstance(external_state, dict) or set(external_state) != REVIEW_EXTERNAL_STATE_IDS:
        errors.append("review external-state inventory changed from the held boundary")
    elif any(
        not isinstance(record, dict) or record.get("state") != "absent"
        for record in external_state.values()
    ):
        errors.append("review external-state evidence is no longer absent")
    return errors


def owner_docket_status_table(docket: str) -> str | None:
    """Return the one canonical status table, excluding narrative/code decoys."""

    docket = without_fenced_code_blocks(docket)
    if docket is None:
        return None
    sections = re.findall(
        r"(?ms)^## Status and boundary[ \t]*\n(.*?)(?=^## |\Z)", docket
    )
    if len(sections) != 1:
        return None
    tables = re.findall(
        r"(?m)^\| ID \| Decision \| Current state \| Blocks \|\n"
        r"\|---\|---\|---\|---\|\n"
        r"((?:\|[^\n]*\|\n?)*)",
        sections[0],
    )
    return tables[0] if len(tables) == 1 else None


def owner_docket_decision_section(docket: str, docket_id: str) -> str | None:
    """Return one structured owner-decision section outside code examples."""

    docket = without_fenced_code_blocks(docket)
    if docket is None:
        return None
    sections = re.findall(
        rf"(?ms)^## {re.escape(docket_id)}\b[^\n]*\n(.*?)(?=^## |\Z)", docket
    )
    if len(sections) != 1:
        return None
    return sections[0]


def owner_docket_unset_errors(root: Path) -> list[str]:
    """Require the named decision routes to remain visibly unset in their docket."""

    try:
        docket = read_source_text(root, OWNER_DOCKET_REL, "owner decision docket")
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    status_table = owner_docket_status_table(docket)
    if status_table is None:
        return ["owner decision docket must retain exactly one status-and-boundary section"]
    for row in OPEN_SOURCE_MIRROR_ROWS.values():
        docket_id = row["docket_id"]
        matches = re.findall(
            rf"(?m)^\|\s*`{re.escape(docket_id)}`\s*\|[^\n]*$", status_table
        )
        expected_status_row = (
            f"| `{docket_id}` | {row['docket_decision']} | **UNSET** | "
            f"{row['docket_blocks']} |"
        )
        if len(matches) != 1 or matches[0] != expected_status_row:
            errors.append(f"owner decision docket must retain exactly one UNSET {docket_id} row")
        decision_section = owner_docket_decision_section(docket, docket_id)
        if decision_section is None:
            errors.append(f"owner decision docket must retain one structured {docket_id} section")
            continue
        structured_lines = {
            "selection": re.findall(
                r"(?m)^-\s+\*\*Selected option:\*\*.*$", decision_section
            ),
            "principal": re.findall(
                r"(?m)^-\s+\*\*Principal:\*\*.*$", decision_section
            ),
        }
        expected_lines = {
            "selection": row["docket_selection_line"],
            "principal": row["docket_principal_line"],
        }
        for field, expected_line in expected_lines.items():
            if structured_lines[field] != [expected_line]:
                errors.append(
                    f"owner decision docket {docket_id} no longer has its exact UNSET "
                    f"{field} boundary"
                )
    return errors


def owner_rulings_section(text: str) -> str | None:
    """Isolate the only table where the manifest mirrors open owner decisions."""

    text = without_fenced_code_blocks(text)
    if text is None:
        return None
    sections = re.findall(
        r"(?ms)^## 1 · Owner rulings\b[^\n]*\n(.*?)(?=^## |\Z)", text
    )
    return sections[0] if len(sections) == 1 else None


def owner_rulings_table(text: str) -> str | None:
    """Return the one canonical owner-rulings table outside code examples."""

    section = owner_rulings_section(text)
    if section is None:
        return None
    tables = re.findall(
        r"(?m)^\| id \| question \| blocks \| source \|\n"
        r"\|---\|---\|---\|---\|\n"
        r"((?:\|[^\n]*\|\n?)*)",
        section,
    )
    return tables[0] if len(tables) == 1 else None


def source_mirror_errors(root: Path, manifest_text: str) -> list[str]:
    """Bind the manifest's open owner/contact rows to source-owned current state."""

    errors: list[str] = []
    owner_table = owner_rulings_table(manifest_text)
    if owner_table is None:
        errors.append("manifest must contain exactly one canonical owner-rulings table for source-mirror rows")
    else:
        scoped_ids = re.findall(
            r"(?m)^\|\s*`((?:OWNER_GATE_|FPE-REVIEW-)[^`]+)`\s*\|[^\n]*$",
            owner_table,
        )
        unknown = sorted(set(scoped_ids) - set(OPEN_SOURCE_MIRROR_ROWS))
        if unknown:
            errors.append(
                "manifest owner-rulings section has unknown source-mirror rows: "
                + ", ".join(unknown)
            )
        for item, row in OPEN_SOURCE_MIRROR_ROWS.items():
            matches = re.findall(
                rf"(?m)^\|\s*`{re.escape(item)}`\s*\|[^\n]*$", owner_table
            )
            if len(matches) != 1:
                errors.append(f"manifest must retain exactly one open source-mirror row for {item}")
                continue
            manifest_row = matches[0]
            expected_row = (
                f"| `{item}` | {row['question']} | {row['blocks']} | "
                f"`{OWNER_DOCKET_WIP_PATH}` (`{row['docket_id']}`) |"
            )
            if manifest_row != expected_row:
                errors.append(
                    f"manifest source-mirror row {item} no longer matches its exact "
                    "held source-mirror contract"
                )

    owner_ids, source_errors = owner_held_source_ids(root)
    errors.extend(source_errors)
    expected_owner_ids = set(OWNER_HELD_SOURCE_ROWS)
    if owner_ids != expected_owner_ids:
        errors.append(
            "owner-held source rows no longer match the manifest mirror: "
            f"source={sorted(owner_ids)}, manifest={sorted(expected_owner_ids)}"
        )
    errors.extend(review_contact_authority_errors(root))
    errors.extend(owner_docket_unset_errors(root))
    return errors


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print("WORK IN PROGRESS: FAIL\n- 00_WORK_IN_PROGRESS/README.md is missing")
        return 1
    text = MANIFEST.read_text(encoding="utf-8")

    # --- A · the receipt-file count must match ------------------------------
    n_receipts = sum(
        1
        for d in RECEIPT_DIRS
        if d.is_dir()
        for p in d.rglob("*.md")
        if re.match(r"^\d{2,3}[_A-Za-z]", p.name)
    )
    # accepts "306 numbered receipts" or "306 receipt files" — the manifest says the
    # former, because 336 .md files live in those folders and 30 of them are READMEs,
    # AGENTS.md and CLAUDE.md. Counting those as receipts inflated a published figure.
    claimed = re.search(r"(\d+)\s+numbered receipts", text) or re.search(r"(\d+) receipt files", text)
    if not claimed:
        errors.append("the manifest states no receipt-file count")
    elif int(claimed.group(1)) != n_receipts:
        errors.append(
            f"manifest says {claimed.group(1)} receipt files; there are {n_receipts}. "
            "Recount, or say why the scope differs."
        )

    # --- B · the claim-status counts must match THE MACHINE SOURCE ----------
    if STATUS_YAML.exists():
        try:
            data = json.loads(STATUS_YAML.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"CLAIM_STATUS.yaml is unreadable: {exc}")
            data = {}
        # CLAIM_STATUS v2 separates live investigations from the old
        # "reopened" bucket and carries one explicit typed-survivor row.
        for bucket in ("validated", "open", "investigations", "graves", "typed_survivors"):
            rows = data.get(bucket)
            if not isinstance(rows, list):
                # Was a silent `continue`: a bucket that went missing or changed shape
                # made its count unverifiable AND unmentioned, so the checker passed
                # while checking one fewer thing than its message claims.
                errors.append(
                    f"CLAIM_STATUS.yaml bucket '{bucket}' is missing or is not a list "
                    f"(got {type(rows).__name__}); its count could not be checked"
                )
                continue
            actual = len(rows)
            m = re.search(rf"^\s*(\d+)\s+{bucket}\b", text, re.M)
            if not m:
                errors.append(f"the manifest does not state a count for '{bucket}'")
            elif int(m.group(1)) != actual:
                errors.append(
                    f"manifest says {m.group(1)} {bucket}; CLAIM_STATUS.yaml has {actual}"
                )
    else:
        errors.append("00_META/claim_status/CLAIM_STATUS.yaml is missing — no authority to check against")

    # --- C · the ambiguous-receipt figure must match its own checker --------
    cc = ROOT / "09_TOOLS" / "01_SCRIPTS" / "check_receipt_citations.py"
    if cc.exists():
        src = cc.read_text(encoding="utf-8")
        m = re.search(r"AMBIGUOUS_BASELINE\s*=\s*(\d+)", src)
        if m:
            baseline = m.group(1)
            if baseline not in text:
                errors.append(
                    f"the citation checker holds {baseline} ambiguous receipt numbers; "
                    f"the manifest does not state that figure. The two must agree or a "
                    f"reader cannot tell which is stale."
                )

    # --- D · open items may not vanish without a ruling ---------------------
    for item in MUST_STAY_LISTED:
        if item not in text:
            errors.append(
                f"'{item}' was removed from the open list. Removal requires a landed "
                "ruling or result to cite; going quiet is not resolution, and this "
                "manifest's own kill has fired."
            )

    errors.extend(source_mirror_errors(ROOT, text))

    for item, receipt in LANDED_CLOSURES.items():
        if not (CLOSURE_RECEIPT_DIR / receipt).is_file():
            errors.append(
                f"landed closure '{item}' points at missing source '{receipt}'"
            )
        closure_row = re.search(
            rf"^\|[^\n]*{re.escape(item)}[^\n]*CLOSED[^\n]*$", text, re.M | re.I
        )
        if not closure_row or receipt not in closure_row.group(0):
            errors.append(
                f"landed closure '{item}' is not retained with its source '{receipt}'"
            )

    # --- E · the fences must survive ---------------------------------------
    for f in FENCES:
        if f not in text:
            errors.append(f"the fence '{f}' is missing — the folder could be cited as authority")

    if errors:
        print("WORK IN PROGRESS: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    open_label = "open item" if len(MUST_STAY_LISTED) == 1 else "open items"
    print(
        f"WORK IN PROGRESS: PASS ({n_receipts} receipt files counted; claim-register "
        f"counts agree; {len(MUST_STAY_LISTED)} {open_label} still listed; "
        f"{len(OPEN_SOURCE_MIRROR_ROWS)} owner/contact rows source-bound; "
        f"{len(LANDED_CLOSURES)} landed closures retained; "
        f"{len(FENCES)} fences intact)"
    )
    print(
        "  scope: this proves the manifest's COUNTS match the corpus and its open items "
        "are still listed. It does NOT prove the list is complete — an open question "
        "nobody wrote down is invisible here too."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

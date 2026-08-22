#!/usr/bin/env python3
"""Guard the contact-limited completion counters without pretending completion.

The state file is a receipted baseline, not a truth source.  This checker
rebuilds every count from the artifact that owns it and fails if a row
disappears, receives two lifecycle classes, or acquires evidence by assertion.
Passing means the bounded internal inventory is reproducible.  It does not mean
the owner-held or world-contact requirements have closed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = Path("00_META/CONTACT_LIMITED_STATE.json")
RECEIPT_INDEX = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_RECEIPT_DISAMBIGUATION_INDEX.json"
)
RECEIPT_CHECKER = Path("09_TOOLS/01_SCRIPTS/check_receipt_citations.py")
CLAIM_SOURCE = Path("00_META/claim_status/CLAIM_STATUS.yaml")
COHERENCE_SOURCE = Path("09_TOOLS/01_SCRIPTS/coherence_profile.json")
PUBLIC_DIR = Path("12_PUBLIC_SITE")
PUBLIC_RUNTIME_OUTPUT_DIRS = frozenset({".vercel"})
PUBLIC_PARITY = PUBLIC_DIR / "public_semantic_parity.json"
WITHHELD_REGISTRY = PUBLIC_DIR / "withheld-routes.json"
VERCEL_CONFIG = PUBLIC_DIR / "vercel.json"
VERCEL_IGNORE = PUBLIC_DIR / ".vercelignore"
PREDEPLOY_CHECKER = PUBLIC_DIR / "predeploy_check.py"
CLAIM_STATUS_CHECKER = Path("09_TOOLS/01_SCRIPTS/check_claim_status.py")
SITEMAP = PUBLIC_DIR / "sitemap.xml"

RECEIPT_LANES = (
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS"),
    Path("11_UPLINK/60_SESSION_PACKETS"),
)
RECEIPT_SKIP_DIRS = {
    "90_ARCHIVE",
    ".git",
    "node_modules",
    "__pycache__",
    ".vercel",
    ".lake",
    "12_PUBLIC_SITE",
}
RECEIPT_NAME = re.compile(r"^(\d{2,3})[_A-Za-z]")
DATED_RECEIPT_NAME = re.compile(
    r"^\d{2,3}[_A-Za-z].*20\d{2}_\d{2}_\d{2}\.md$", re.I
)
STATE_DIGEST_LINE = re.compile(
    r"^contact_limited_state_canonical_sha256: ([0-9a-f]{64})$", re.M
)
STATE_DIGEST_MARKER = b"contact_limited_state_canonical_sha256:"
SUPERSESSION = re.compile(
    r"^\s*(superseded_by|supersedes|supersession_note)\s*:"
    r"|^\s*status\s*:.*(supersed|DISPUTED|NOT CURRENT|dissent|CORRECTED)",
    re.I | re.M,
)


def _has_symlink_component(root: Path, relative: str) -> bool:
    """Reject a lexical path whose root or any in-repo component is a symlink."""

    candidate = root
    if candidate.is_symlink():
        return True
    for component in Path(relative).parts:
        candidate /= component
        if candidate.is_symlink():
            return True
    return False


def repo_file(root: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    """Require an existing repo-relative regular file without reading through links."""

    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty repo-relative path")
        return None
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{label} must not be absolute or contain '..': {value!r}")
        return None
    target = root / rel
    if _has_symlink_component(root, rel.as_posix()):
        errors.append(f"{label} must not traverse a symlink: {value}")
        return None
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} escapes the repository: {value!r}")
        return None
    if not target.is_file():
        errors.append(f"{label} does not exist as a file: {value}")
        return None
    return target


def _policy_file(root: Path, relative: Path, label: str) -> Path:
    """Resolve an executable policy only through the shared lexical file guard."""

    errors: list[str] = []
    path = repo_file(root, relative.as_posix(), label, errors)
    if path is None:
        raise RuntimeError("; ".join(errors))
    return path


def _load_receipt_citation_policy():
    path = _policy_file(ROOT, RECEIPT_CHECKER, "receipt citation policy")
    spec = importlib.util.spec_from_file_location("receipt_citation_policy_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load receipt citation policy owner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_RECEIPT_CITATION_POLICY = _load_receipt_citation_policy()
CITATION = _RECEIPT_CITATION_POLICY.CITATION
citation_is_negated = _RECEIPT_CITATION_POLICY.citation_is_negated


def _load_predeploy_policy():
    path = _policy_file(ROOT, PREDEPLOY_CHECKER, "public predeploy policy")
    spec = importlib.util.spec_from_file_location("public_predeploy_policy_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load public predeploy policy owner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PREDEPLOY_POLICY = _load_predeploy_policy()


def _load_claim_status_policy(
    root: Path = ROOT, relative: Path = CLAIM_STATUS_CHECKER
):
    path = _policy_file(root, relative, "claim-status policy")
    spec = importlib.util.spec_from_file_location("claim_status_policy_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load claim-status policy owner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_CLAIM_STATUS_POLICY = _load_claim_status_policy()

EXPECTED_DEBTS = {
    "OWNER_GATE_HELD_PUBLIC_DOCS",
    "OWNER_GATE_OPEN_TOPOLOGY",
}
EXPECTED_REUSED_PREFIXES = 101
EXPECTED_LIFECYCLE_ROWS = 50
EXPECTED_CURRENT_ROWS = 28
EXPECTED_GRAVE_ROWS = 22
EXPECTED_WORLD_REQUIREMENTS = (
    "Independent observations with discriminating outcomes",
    "Independent replication or external review filed as outcome custody",
)
PUBLIC_DOC_EVIDENCE = {
    "12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md",
    "12_PUBLIC_SITE/_PLANS/specs/2026-06-05-numbered-doctrine-spine-design.md",
}
PUBLIC_DOC_EXACT_IGNORE_PATTERNS = {
    (
        "12_PUBLIC_SITE/docs/superpowers/specs/"
        "2026-06-05-numbered-doctrine-spine-design.md"
    ): "docs/",
    (
        "12_PUBLIC_SITE/_PLANS/specs/"
        "2026-06-05-numbered-doctrine-spine-design.md"
    ): "_PLANS/",
}
TOPOLOGY_EVIDENCE = {
    "00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md",
    "08_FRAMEWORK_SUPPORT/00_META/CLAUDE.md",
    "08_FRAMEWORK_SUPPORT/00_META/00_MAGNUM_OPUS/CLAUDE.md",
    "08_FRAMEWORK_SUPPORT/00_META/02_ANALYSIS_DOCUMENTS/CLAUDE.md",
}
COHERENCE_PROFILE_EVIDENCE = COHERENCE_SOURCE.as_posix()
OWNER_DOCKET = Path("00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md")
OWNER_DOCKET_EVIDENCE = OWNER_DOCKET.as_posix()
PUBLIC_DOC_OWNER_DEBT_EVIDENCE = PUBLIC_DOC_EVIDENCE | {
    COHERENCE_PROFILE_EVIDENCE,
    OWNER_DOCKET_EVIDENCE,
}
TOPOLOGY_OWNER_DEBT_EVIDENCE = TOPOLOGY_EVIDENCE | {
    COHERENCE_PROFILE_EVIDENCE,
    OWNER_DOCKET_EVIDENCE,
}
HELD_NONROOT_META_VIOLATION_PATHS = {"08_FRAMEWORK_SUPPORT/00_META"}
HELD_TOPOLOGY_TOMBSTONE_SHA256 = {
    Path("08_FRAMEWORK_SUPPORT/00_META/CLAUDE.md"): (
        "0802649fc2b1a581ba59ed85fbb6d0867b37b61bfe9990d39991a2f4697a64da"
    ),
    Path("08_FRAMEWORK_SUPPORT/00_META/00_MAGNUM_OPUS/CLAUDE.md"): (
        "9ee14e3de1a691a50409ab7adea269c5b11f2cac6f0ccfc18c4fa9808aa9c2f7"
    ),
    Path("08_FRAMEWORK_SUPPORT/00_META/02_ANALYSIS_DOCUMENTS/CLAUDE.md"): (
        "1784d975a03340530a0e00344e84f64b662e68c1557ca20fefcb9c08f73f91cc"
    ),
}
HELD_TOPOLOGY_TOMBSTONES = tuple(HELD_TOPOLOGY_TOMBSTONE_SHA256)
HELD_TOPOLOGY_STATUS_LINE = (
    'status: "[B] tombstone. This directory\'s content was archived 2026-07-20 '
    'under the pure-Emergentism boundary. Nothing here owns doctrine."'
)
HELD_TOPOLOGY_TOMBSTONE_SENTINELS = (
    "**This lane no longer holds content.**",
    "Archived material is **provenance, not authority**.",
    "must not be cited as current canon.",
    "pure_emergentism_boundary_2026_07_20",
    "2026_07_22_tree_authority_reconciliation",
)
HELD_TOPOLOGY_OWNERSHIP_ASSERTION = re.compile(
    r"\b(?:this|the)\s+(?:directory|folder|lane|tombstone)\s+owns\s+"
    r"(?:active\s+)?(?:canon|doctrine|governance)\b"
    r"|\b(?:active\s+)?(?:canon|doctrine|governance)\s+(?:is|remains)\s+"
    r"owned\s+here\b",
    re.I,
)
OWNER_DOCKET_UNSET_CONTRACT = {
    "D-OWNER-01": {
        "status_row": (
            "| `D-OWNER-01` | Canonical owner for the byte-identical public planning "
            "duplicate | **UNSET** | current/custody routing of two public-site planning copies |"
        ),
        "selection": "- **Selected option:** **UNSET**.",
        "principal": (
            "- **Principal:** **UNSET** (01_EMERGENTISM editorial owner must name one)."
        ),
    },
    "D-OWNER-02": {
        "status_row": (
            "| `D-OWNER-02` | Disposition of the grandfathered framework-support "
            "`00_META` tombstones under the root-only rule | **UNSET** | held topology "
            "violation |"
        ),
        "selection": "- **Selected option:** **UNSET**.",
        "principal": (
            "- **Principal:** **UNSET** (01_EMERGENTISM editorial/topology owner must name one)."
        ),
    },
}
EXPECTED_TOPOLOGY_DEBT_QUESTION = (
    "How must the three grandfathered framework-support 00_META tombstones be "
    "disposed under the categorical root-only rule while preserving their custody?"
)
EXPECTED_TOPOLOGY_DEBT_CLOSE_WHEN = (
    "A dated owner ruling either amends the topology rule or supplies a complete "
    "migration or archival route; until then the exact path remains a hash-bound "
    "held violation."
)
NON_ACTIVE_META_SEGMENTS = {
    ".git",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
    "__pycache__",
    "node_modules",
}
EXPECTED_PRECEDENCE = (
    "withheld",
    "current",
    "provisional",
    "infrastructure",
    "frozen",
    "unclassified",
)
EXPECTED_ALIAS_COLLISIONS: list[dict[str, Any]] = []
EXPECTED_RAW_OVERLAP_CLASSES = {
    ("frozen", "infrastructure"),
    ("frozen", "withheld"),
}
EXPECTED_INFRASTRUCTURE_OVERLAP = ["offline/index.html"]
EXPECTED_FROZEN_WITHHELD_OVERLAP_COUNT = 253
EXPECTED_FROZEN_WITHHELD_OVERLAP_SHA256 = (
    "0f577b425e702436ca61d7e60abcd4f544de4394dd9db670fd97a271472a9ef5"  # pragma: allow-secret
)
EXPECTED_WORLD_REQUIRED_FIELDS = (
    "claim_id",
    "contract_id",
    "frozen_protocol_hash",
    "scope",
    "independent_party_identity",
    "independence_basis",
    "discriminating_protocol",
    "outcome",
    "verbatim_custody",
    "provenance",
    "null_harm_deviation_custody",
)
EXPECTED_WORLD_INADMISSIBLE = (
    "commits",
    "gates",
    "AI review",
    "invitations",
    "preregistrations",
    "internal receipts",
    "URLs without filed outcome custody",
    "staged protocols",
)
PATH_SET_HASH_RULE = (
    "SHA-256 over the canonical UTF-8 JSON array of unique repo-relative paths sorted "
    "lexicographically, with ensure_ascii=false and separators ',' and ':'."
)
DUPLICATE_GROUP_HASH_RULE = (
    "SHA-256 over canonical UTF-8 JSON mapping each reused prefix to its lexicographically "
    "sorted repo-relative paths, with object keys sorted and separators ',' and ':'."
)
PUBLIC_CATEGORIES = (
    "current",
    "provisional",
    "frozen",
    "withheld",
    "infrastructure",
    "unclassified",
)


class ContractError(Exception):
    """One or more ratchet invariants failed."""

    def __init__(self, errors: str | list[str]):
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("; ".join(self.errors))


def load_json(path: Path) -> Any:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ContractError(f"duplicate JSON object key {key!r} at {path}")
            value[key] = item
        return value

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except FileNotFoundError as exc:
        raise ContractError(f"missing machine owner: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON at {path}: {exc}") from exc


def _strict_tree_entries(root: Path, relative_root: Path, label: str) -> list[Path]:
    """Inventory a tree only when its root and every lexical entry are symlink-free."""

    relative = relative_root.as_posix()
    base = root / relative_root
    if _has_symlink_component(root, relative):
        raise ContractError(f"{label} root must not traverse a symlink: {relative}")
    if not base.is_dir():
        raise ContractError(f"missing {label} root: {relative}")
    try:
        entries = list(base.rglob("*"))
    except OSError as exc:
        raise ContractError(f"cannot inventory {label} root {relative}: {exc}") from exc
    for path in entries:
        rel = path.relative_to(root).as_posix()
        if _has_symlink_component(root, rel):
            raise ContractError(f"{label} entry must not traverse a symlink: {rel}")
    return entries


def _git_index_has_exact_regular_bytes(
    root: Path, relative: str, expected_bytes: bytes
) -> bool:
    """Require one stage-0 regular-file blob with the retained worktree bytes."""

    try:
        index = subprocess.run(
            ["git", "ls-files", "--stage", "-z", "--", relative],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return False
    if index.returncode != 0:
        return False
    records = [record for record in index.stdout.split(b"\0") if record]
    if len(records) != 1:
        return False
    metadata, separator, indexed_path = records[0].partition(b"\t")
    fields = metadata.split()
    if (
        not separator
        or indexed_path != relative.encode("utf-8")
        or len(fields) != 3
        or fields[0] != b"100644"
        or fields[2] != b"0"
    ):
        return False
    try:
        blob = subprocess.run(
            ["git", "cat-file", "blob", f":{relative}"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return False
    return blob.returncode == 0 and blob.stdout == expected_bytes


def visible_markdown(text: str) -> str | None:
    """Return visible Markdown; ambiguous fences/comments/HTML fail closed."""

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


def public_doc_owner_debt_errors(root: Path, evidence: set[str]) -> list[str]:
    """Keep the unresolved duplicate in non-deployable, byte-identical custody."""

    if evidence != PUBLIC_DOC_OWNER_DEBT_EVIDENCE:
        return [
            "public-doc owner debt evidence must exactly match the two retained "
            "documents, shared coherence profile, and UNSET owner docket"
        ]
    errors: list[str] = []
    left, right = sorted(PUBLIC_DOC_EVIDENCE)
    left_path, right_path = root / left, root / right
    if _has_symlink_component(root, left) or _has_symlink_component(root, right):
        errors.append("public-doc owner debt evidence must not traverse a symlink")
        return errors
    if not left_path.is_file() or not right_path.is_file():
        errors.append("public-doc owner debt evidence must remain regular files")
        return errors
    for path, target in ((left, left_path), (right, right_path)):
        if not _git_index_has_exact_regular_bytes(root, path, target.read_bytes()):
            errors.append(
                "public-doc owner debt evidence lacks exact regular-file Git index "
                f"custody: {path}"
            )
    if left_path.read_bytes() != right_path.read_bytes():
        errors.append("public-doc debt evidence is no longer byte-identical")
    ignore_errors: list[str] = []
    ignore_path = repo_file(
        root, VERCEL_IGNORE.as_posix(), "public deployment-ignore owner", ignore_errors
    )
    if ignore_path is None:
        return errors + ignore_errors
    patterns = _load_vercelignore(ignore_path)
    for path in (left, right):
        try:
            site_relative = Path(path).relative_to(PUBLIC_DIR).as_posix()
        except ValueError:
            errors.append(f"public-doc owner debt path escapes public-site lane: {path}")
            continue
        required_pattern = PUBLIC_DOC_EXACT_IGNORE_PATTERNS[path]
        if required_pattern not in patterns:
            errors.append(
                "public-doc owner debt lacks its exact deployment exclusion: "
                f"{required_pattern}"
            )
        elif not _is_vercel_ignored(site_relative, [required_pattern]):
            errors.append(
                "contact-limited matcher no longer honors public-doc deployment exclusion: "
                f"{required_pattern}"
            )
        elif not _PREDEPLOY_POLICY.is_vercel_ignored(
            site_relative, [required_pattern]
        ):
            errors.append(
                "predeploy matcher no longer honors public-doc deployment exclusion: "
                f"{required_pattern}"
            )
        if not _is_vercel_ignored(site_relative, patterns):
            errors.append(f"public-doc owner debt path is no longer ignored: {path}")
        if not _PREDEPLOY_POLICY.is_vercel_ignored(site_relative, patterns):
            errors.append(
                f"public-doc owner debt path is no longer ignored by predeploy policy: {path}"
            )
    return errors


def present_nonroot_meta_paths(root: Path) -> set[str]:
    """Discover lexical per-pillar 00_META entries without normalizing them."""

    present: set[str] = set()
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        # A directory symlink appears in dirnames, while a broken symlink or
        # regular file named 00_META appears in filenames. All are topology
        # entries and must be observed before pruning traversal.
        if "00_META" in set(dirnames) | set(filenames):
            candidate = Path(directory) / "00_META"
            relative = candidate.relative_to(root)
            if relative != Path("00_META"):
                present.add(relative.as_posix())
        dirnames[:] = [
            name for name in dirnames if name not in NON_ACTIVE_META_SEGMENTS
        ]
    return present


def unresolved_topology_errors(root: Path) -> list[str]:
    """Freeze the exact tombstone custody while D-OWNER-02 remains unselected."""

    actual = present_nonroot_meta_paths(root)
    missing = sorted(HELD_NONROOT_META_VIOLATION_PATHS - actual)
    unexpected = sorted(actual - HELD_NONROOT_META_VIOLATION_PATHS)
    symlinked = sorted(path for path in actual if (root / path).is_symlink())
    non_directories = sorted(
        path for path in actual if not (root / path).is_dir()
    )
    errors: list[str] = []
    detail: list[str] = []
    if missing:
        detail.append("missing=" + ", ".join(missing))
    if unexpected:
        detail.append("unexpected=" + ", ".join(unexpected))
    if symlinked:
        detail.append("symlink=" + ", ".join(symlinked))
    if non_directories:
        detail.append("non-directory=" + ", ".join(non_directories))
    if detail:
        errors.append(
            "held non-root 00_META violation custody drifted: "
            + "; ".join(detail)
        )
    if HELD_NONROOT_META_VIOLATION_PATHS <= actual:
        held_root = root / next(iter(HELD_NONROOT_META_VIOLATION_PATHS))
        expected_entries = {
            path.as_posix() for path in HELD_TOPOLOGY_TOMBSTONES
        } | {
            path.parent.as_posix()
            for path in HELD_TOPOLOGY_TOMBSTONES
            if path.parent != Path(next(iter(HELD_NONROOT_META_VIOLATION_PATHS)))
        }
        actual_entries = {
            path.relative_to(root).as_posix()
            for path in held_root.rglob("*")
        }
        if actual_entries != expected_entries:
            errors.append(
                "held 00_META tombstone inventory drifted: "
                f"missing={sorted(expected_entries - actual_entries)}, "
                f"unexpected={sorted(actual_entries - expected_entries)}"
            )
        for tombstone in HELD_TOPOLOGY_TOMBSTONES:
            relative = tombstone.as_posix()
            target = root / tombstone
            if _has_symlink_component(root, relative) or not target.is_file():
                errors.append(
                    "held 00_META tombstone must remain a regular, non-symlink file: "
                    + relative
                )
                continue
            try:
                body = target.read_text(encoding="utf-8")
                body_bytes = target.read_bytes()
            except OSError as exc:
                errors.append(
                    f"held 00_META tombstone is unreadable: {relative}: "
                    f"{exc.__class__.__name__}"
                )
                continue
            if not _git_index_has_exact_regular_bytes(root, relative, body_bytes):
                errors.append(
                    "held 00_META tombstone lacks exact regular-file Git index custody: "
                    + relative
                )
            if (
                hashlib.sha256(body_bytes).hexdigest()
                != HELD_TOPOLOGY_TOMBSTONE_SHA256[tombstone]
            ):
                errors.append(
                    "held 00_META tombstone SHA-256 drifted from grandfathered "
                    "custody: " + relative
                )
            visible = visible_markdown(body)
            if visible is None:
                errors.append(
                    "held 00_META tombstone Markdown boundary is ambiguous: " + relative
                )
                continue
            expected_title = (
                f'title: "{tombstone.parent.as_posix()} — archived lane, tombstone route"'
            )
            if body.count(expected_title) != 1 or body.count(HELD_TOPOLOGY_STATUS_LINE) != 1:
                errors.append(
                    "held 00_META tombstone lost its exact title/no-doctrine frontmatter: "
                    + relative
                )
            expected_heading = f"# {tombstone.parent.as_posix()} — archived"
            if visible.count(expected_heading) != 1:
                errors.append(
                    "held 00_META tombstone lost its exact archived heading: " + relative
                )
            missing_markers = [
                marker
                for marker in HELD_TOPOLOGY_TOMBSTONE_SENTINELS
                if marker not in visible
            ]
            if missing_markers:
                errors.append(
                    "held 00_META tombstone lost its exact no-doctrine/custody markers: "
                    f"{relative}: {missing_markers}"
                )
            if HELD_TOPOLOGY_OWNERSHIP_ASSERTION.search(visible):
                errors.append(
                    "held 00_META tombstone asserts active canon/doctrine/governance ownership: "
                    + relative
                )
    return errors


def topology_owner_debt_errors(root: Path, evidence: set[str]) -> list[str]:
    """Keep the unresolved topology evidence exact while its owner remains unset."""

    errors: list[str] = []
    if evidence != TOPOLOGY_OWNER_DEBT_EVIDENCE:
        errors.append(
            "topology owner debt evidence must exactly match the topology standard, "
            "three CLAUDE.md tombstones, and shared coherence profile"
        )
    errors.extend(unresolved_topology_errors(root))
    return errors


def owner_docket_unset_errors(root: Path) -> list[str]:
    """Require D-OWNER-01/02 to remain exact, visible, and unselected."""

    relative = OWNER_DOCKET.as_posix()
    target = root / OWNER_DOCKET
    if _has_symlink_component(root, relative) or not target.is_file():
        return ["contact-limited owner docket must remain a regular, non-symlink file"]
    try:
        body = target.read_text(encoding="utf-8")
        body_bytes = target.read_bytes()
    except OSError as exc:
        return [f"contact-limited owner docket is unreadable: {exc.__class__.__name__}"]
    errors: list[str] = []
    if not _git_index_has_exact_regular_bytes(root, relative, body_bytes):
        errors.append(
            "contact-limited owner docket lacks exact regular-file Git index custody"
        )
    visible = visible_markdown(body)
    if visible is None:
        return errors + [
            "contact-limited owner docket Markdown boundary is ambiguous"
        ]
    for docket_id, contract in OWNER_DOCKET_UNSET_CONTRACT.items():
        status_rows = re.findall(
            rf"(?m)^\|\s*`{re.escape(docket_id)}`\s*\|[^\n]*$", visible
        )
        if status_rows != [contract["status_row"]]:
            errors.append(
                f"contact-limited owner docket must retain one exact UNSET {docket_id} row"
            )
        sections = re.findall(
            rf"(?ms)^## {re.escape(docket_id)}\b[^\n]*\n(.*?)(?=^## |\Z)",
            visible,
        )
        if len(sections) != 1:
            errors.append(
                f"contact-limited owner docket must retain one {docket_id} section"
            )
            continue
        selection_lines = re.findall(
            r"(?m)^-\s+\*\*Selected option:\*\*.*$", sections[0]
        )
        principal_lines = re.findall(
            r"(?m)^-\s+\*\*Principal:\*\*.*$", sections[0]
        )
        if selection_lines != [contract["selection"]]:
            errors.append(
                f"contact-limited owner docket {docket_id} lost its exact UNSET selection"
            )
        if principal_lines != [contract["principal"]]:
            errors.append(
                f"contact-limited owner docket {docket_id} lost its exact UNSET principal"
            )
    return errors


def receipt_ref(root: Path, value: Any, label: str, errors: list[str]) -> None:
    target = repo_file(root, value, label, errors)
    if target is None:
        return
    rel = target.relative_to(root)
    if rel.parent not in RECEIPT_LANES or not DATED_RECEIPT_NAME.match(rel.name):
        errors.append(
            f"{label} must name a dated receipt in a live receipt lane: {rel}"
        )


def require_mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def require_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    return value


def exact_keys(
    value: dict[str, Any], expected: set[str], label: str, errors: list[str]
) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{label} is missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has ungoverned keys: {', '.join(extra)}")


def canonical_state_digest(state: dict[str, Any]) -> str:
    payload = json.dumps(
        state, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def path_set_sha256(paths: set[str] | list[str]) -> str:
    payload = json.dumps(
        sorted(set(paths)), separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def duplicate_groups_sha256(groups: dict[str, list[str] | set[str]]) -> str:
    normalized = {key: sorted(set(values)) for key, values in groups.items()}
    payload = json.dumps(
        normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise ContractError(f"cannot interrogate git custody: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ContractError(
            f"git custody command failed ({' '.join(args)}): {detail or result.returncode}"
        )
    return result


def _tree_receipt_bytes(root: Path, revision: str, rel: Path) -> bytes | None:
    listing = _run_git(
        root, "ls-tree", "-z", "--full-tree", revision, "--", rel.as_posix()
    ).stdout
    if not listing:
        return None
    records = [record for record in listing.split(b"\0") if record]
    if len(records) != 1 or b"\t" not in records[0]:
        raise ContractError(
            f"unexpected committed receipt tree entry for {rel} at {revision}"
        )
    metadata, recorded_path = records[0].split(b"\t", 1)
    try:
        recorded = recorded_path.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ContractError(f"committed receipt path is not UTF-8: {rel}") from exc
    fields = metadata.split()
    if recorded != rel.as_posix() or len(fields) != 3 or fields[1] != b"blob":
        raise ContractError(
            f"unexpected committed receipt object for {rel} at {revision}"
        )
    return _run_git(root, "cat-file", "blob", f"{revision}:{rel.as_posix()}").stdout


def _first_parent_revision(root: Path) -> str | None:
    """Verify repository ancestry and return HEAD's first parent when present."""
    top = _run_git(root, "rev-parse", "--show-toplevel").stdout.decode(
        "utf-8", errors="strict"
    ).strip()
    if Path(top).resolve() != root.resolve():
        raise ContractError(
            f"git custody root mismatch: expected {root.resolve()}, found {Path(top).resolve()}"
    )
    _run_git(root, "rev-parse", "--verify", "HEAD^{commit}")
    shallow_text = _run_git(root, "rev-parse", "--is-shallow-repository").stdout.decode(
        "ascii", errors="strict"
    ).strip()
    if shallow_text not in {"true", "false"}:
        raise ContractError(f"unexpected git shallow-state response: {shallow_text!r}")
    parents = _run_git(root, "rev-list", "--parents", "-n", "1", "HEAD").stdout.decode(
        "ascii", errors="strict"
    ).strip().split()
    if not parents:
        raise ContractError("git custody could not resolve HEAD ancestry")
    if len(parents) == 1:
        if shallow_text == "true":
            raise ContractError(
                "first-parent history unavailable in a shallow checkout; fetch at least "
                "two commits (actions/checkout fetch-depth: 2 or greater)"
            )
        return None

    first_parent = parents[1]
    try:
        _run_git(root, "cat-file", "-e", f"{first_parent}^{{commit}}")
    except ContractError as exc:
        raise ContractError(
            "first-parent history object is unavailable; fetch at least two commits "
            "(actions/checkout fetch-depth: 2 or greater)"
        ) from exc
    return first_parent


def receipt_history_bytes(root: Path, rel: Path) -> tuple[bytes | None, bytes | None]:
    """Return receipt bytes at HEAD and its first parent, with history fail-closed."""
    first_parent = _first_parent_revision(root)
    head_blob = _tree_receipt_bytes(root, "HEAD", rel)
    if first_parent is None:
        return head_blob, None
    parent_blob = _tree_receipt_bytes(root, first_parent, rel)
    return head_blob, parent_blob


def _git_marker_receipt_paths(root: Path, revision: str) -> set[Path]:
    args = [
        "git",
        "-C",
        str(root),
        "grep",
        "-l",
        "-F",
        "--full-name",
        STATE_DIGEST_MARKER.decode("ascii"),
        revision,
        "--",
        *(lane.as_posix() for lane in RECEIPT_LANES),
    ]
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise ContractError(f"cannot scan committed snapshot receipts: {exc}") from exc
    if result.returncode == 1 and not result.stdout:
        return set()
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ContractError(
            f"cannot scan snapshot receipts at {revision}: {detail or result.returncode}"
        )
    prefix = revision + ":"
    paths: set[Path] = set()
    for line in result.stdout.decode("utf-8", errors="strict").splitlines():
        if not line.startswith(prefix):
            raise ContractError(
                f"unexpected snapshot-receipt grep result at {revision}: {line!r}"
            )
        rel = Path(line[len(prefix) :])
        if not any(rel == lane or lane in rel.parents for lane in RECEIPT_LANES) or rel.suffix != ".md":
            raise ContractError(f"snapshot marker escaped the live receipt lanes: {rel}")
        paths.add(rel)
    return paths


def marker_receipt_custody_errors(root: Path) -> list[str]:
    """Lock every live receipt that has ever carried the snapshot digest marker."""
    first_parent = _first_parent_revision(root)
    head_markers = _git_marker_receipt_paths(root, "HEAD")
    parent_markers = (
        _git_marker_receipt_paths(root, first_parent)
        if first_parent is not None
        else set()
    )
    working_markers: set[Path] = set()
    for lane in RECEIPT_LANES:
        for path in _strict_tree_entries(root, lane, "marker-receipt custody"):
            if path.suffix != ".md" or not path.is_file():
                continue
            try:
                if STATE_DIGEST_MARKER in path.read_bytes():
                    working_markers.add(path.relative_to(root))
            except OSError as exc:
                raise ContractError(f"cannot read snapshot-marker candidate {path}: {exc}") from exc

    errors: list[str] = []
    for rel in sorted(working_markers | head_markers | parent_markers):
        working_path = root / rel
        if _has_symlink_component(root, rel.as_posix()):
            errors.append(f"snapshot marker receipt must not traverse a symlink: {rel}")
            continue
        try:
            working_blob = working_path.read_bytes() if working_path.is_file() else None
        except OSError as exc:
            errors.append(f"cannot read marker receipt {rel}: {exc}")
            continue
        head_blob = _tree_receipt_bytes(root, "HEAD", rel)
        parent_blob = (
            _tree_receipt_bytes(root, first_parent, rel)
            if first_parent is not None
            else None
        )
        if head_blob is not None and working_blob != head_blob:
            errors.append(
                f"snapshot marker receipt {rel} differs from HEAD or is deleted in the "
                "worktree; marker receipts are immutable"
            )
        if parent_blob is not None and head_blob is None:
            errors.append(
                f"snapshot marker receipt {rel} existed in the first parent but is deleted "
                "from HEAD; a new baseline must preserve old marker receipts"
            )
        elif parent_blob is not None and head_blob != parent_blob:
            errors.append(
                f"snapshot marker receipt {rel} differs from its first-parent bytes; "
                "rebaselining to a new receipt cannot rewrite an old marker receipt"
            )
    return errors


def committed_receipt_bytes(root: Path, rel: Path) -> bytes | None:
    """Compatibility wrapper returning the receipt blob at HEAD."""
    return receipt_history_bytes(root, rel)[0]


def snapshot_binding_errors(
    state: dict[str, Any],
    working_receipt: bytes,
    committed_receipt: bytes | None,
    parent_receipt: bytes | None = None,
) -> list[str]:
    """Validate digest consistency and immutable committed receipt custody."""
    errors: list[str] = []
    try:
        receipt_text = working_receipt.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return ["completion snapshot receipt is not UTF-8"]
    digest_lines = STATE_DIGEST_LINE.findall(receipt_text)
    actual_digest = canonical_state_digest(state)
    if len(digest_lines) != 1:
        errors.append(
            "completion snapshot receipt must contain exactly one canonical state digest line"
        )
    elif digest_lines[0] != actual_digest:
        errors.append(
            f"completion snapshot digest mismatch: receipt={digest_lines[0]}, "
            f"state={actual_digest}"
        )
    if committed_receipt is not None and working_receipt != committed_receipt:
        errors.append(
            "completion snapshot receipt differs from its committed HEAD bytes; "
            "a rebaseline requires a new dated receipt path"
        )
    if committed_receipt is None and parent_receipt is not None:
        errors.append(
            "completion snapshot receipt path existed in the first parent but is absent "
            "from HEAD; reusing a removed receipt path is not a new baseline"
        )
    if (
        committed_receipt is not None
        and parent_receipt is not None
        and committed_receipt != parent_receipt
    ):
        errors.append(
            "completion snapshot receipt was rewritten by the current commit relative "
            "to its first parent; a rebaseline requires a new dated receipt path"
        )
    return errors


def _receipt_files(root: Path) -> dict[str, list[Path]]:
    by_number: dict[str, list[Path]] = defaultdict(list)
    for lane in RECEIPT_LANES:
        for path in _strict_tree_entries(root, lane, "receipt namespace"):
            if path.suffix != ".md" or not path.is_file():
                continue
            rel = path.relative_to(root)
            if any(part in RECEIPT_SKIP_DIRS for part in rel.parts):
                continue
            match = RECEIPT_NAME.match(path.name)
            if match and match.group(1) != "00":
                by_number[match.group(1)].append(path)
    return by_number


def _prefixed_receipt_markdown_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for lane in RECEIPT_LANES:
        for path in _strict_tree_entries(root, lane, "receipt namespace"):
            if path.suffix != ".md" or not path.is_file():
                continue
            rel = path.relative_to(root)
            if any(part in RECEIPT_SKIP_DIRS for part in rel.parts):
                continue
            if RECEIPT_NAME.match(path.name):
                paths.add(rel.as_posix())
    return paths


def _dangling_citations(root: Path, by_number: dict[str, list[Path]]) -> list[str]:
    dangling: list[str] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in RECEIPT_SKIP_DIRS for part in rel.parts):
            continue
        if _has_symlink_component(root, rel.as_posix()):
            raise ContractError(
                f"receipt citation corpus entry must not traverse a symlink: {rel}"
            )
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in CITATION.finditer(text):
            number = match.group(1) or match.group(2)
            if number in by_number:
                continue
            line = text[: match.start()].count("\n")
            if citation_is_negated(text, match):
                continue
            dangling.append(f"{rel}:{line + 1}:r{number}")
    return dangling


def compute_receipt_namespace(root: Path) -> dict[str, Any]:
    by_number = _receipt_files(root)
    duplicate_groups = {
        number: paths for number, paths in by_number.items() if len(paths) > 1
    }
    dangerous = 0
    for paths in duplicate_groups.values():
        undeclared = [
            path
            for path in paths
            if not SUPERSESSION.search(
                path.read_text(encoding="utf-8", errors="ignore")[:2500]
            )
        ]
        if len(undeclared) > 1:
            dangerous += 1

    index_errors: list[str] = []
    index_path = repo_file(
        root, RECEIPT_INDEX.as_posix(), "receipt namespace machine owner", index_errors
    )
    if index_path is None:
        raise ContractError(index_errors)
    index = load_json(index_path)
    index_rows = require_mapping(index, str(RECEIPT_INDEX), []).get("rows", [])
    indexed: dict[str, set[str]] = {}
    if isinstance(index_rows, list):
        for row in index_rows:
            if not isinstance(row, dict) or not isinstance(row.get("entries"), list):
                raise ContractError(f"malformed row in {RECEIPT_INDEX}")
            indexed[str(row.get("number"))] = {
                str(entry.get("path"))
                for entry in row["entries"]
                if isinstance(entry, dict)
            }
    actual = {
        number: {str(path.relative_to(root)) for path in paths}
        for number, paths in duplicate_groups.items()
    }
    if index.get("ambiguousNumbers") != len(duplicate_groups) or indexed != actual:
        raise ContractError(
            f"{RECEIPT_INDEX} does not match the live duplicate receipt groups"
        )

    citable_paths = {
        path.relative_to(root).as_posix()
        for paths in by_number.values()
        for path in paths
    }
    convention_paths = _prefixed_receipt_markdown_paths(root)
    duplicate_path_groups = {
        number: {path.relative_to(root).as_posix() for path in paths}
        for number, paths in duplicate_groups.items()
    }

    return {
        "target_files": sum(len(paths) for paths in by_number.values()),
        "prefixed_markdown_including_00_convention": len(convention_paths),
        "unique_prefixes": len(by_number),
        "reused_prefixes": len(duplicate_groups),
        "legacy_heuristic_dangerous_prefixes": dangerous,
        "bare_unsafe_reused_prefixes": len(duplicate_groups),
        "dangling_citations": len(_dangling_citations(root, by_number)),
        "identity_hashes": {
            "citable_targets_sha256": path_set_sha256(citable_paths),
            "prefixed_including_00_sha256": path_set_sha256(convention_paths),
            "duplicate_groups_sha256": duplicate_groups_sha256(duplicate_path_groups),
        },
    }


def _load_vercelignore(path: Path) -> list[str]:
    if not path.is_file():
        raise ContractError(f"missing machine owner: {path}")
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _vercelignore_matches(rel_path: str, pattern: str) -> bool:
    rel_path = rel_path.replace("\\", "/")
    pattern = pattern.replace("\\", "/")
    anchored = pattern.startswith("/")
    if "[" in pattern or "]" in pattern:
        raise ContractError(
            f"unsupported character-class pattern in .vercelignore: {pattern!r}"
        )
    directory_only = pattern.endswith("/")
    if anchored:
        pattern = pattern[1:]
    if directory_only:
        pattern = pattern[:-1]
    if not pattern:
        raise ContractError("empty .vercelignore pattern is unsupported")

    regex: list[str] = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                while index + 1 < len(pattern) and pattern[index + 1] == "*":
                    index += 1
                if index + 1 < len(pattern) and pattern[index + 1] == "/":
                    # `**/` spans zero or more complete directory components.
                    regex.append(r"(?:[^/]+/)*")
                    index += 1
                else:
                    regex.append(r".*")
            else:
                regex.append(r"[^/]*")
        elif char == "?":
            regex.append(r"[^/]")
        else:
            regex.append(re.escape(char))
        index += 1
    expression = "".join(regex)
    candidate = rel_path.strip("/")
    parts = candidate.split("/") if candidate else []
    directory_parts = parts if rel_path.endswith("/") else parts[:-1]
    if directory_only:
        if not anchored and "/" not in pattern:
            return any(
                re.fullmatch(expression, part, flags=re.IGNORECASE) is not None
                for part in directory_parts
            )
        directory_prefixes = (
            "/".join(directory_parts[:index])
            for index in range(1, len(directory_parts) + 1)
        )
        return any(
            re.fullmatch(expression, prefix, flags=re.IGNORECASE) is not None
            for prefix in directory_prefixes
        )
    if "/" not in pattern and not anchored:
        return re.fullmatch(
            expression, parts[-1] if parts else "", flags=re.IGNORECASE
        ) is not None
    return re.fullmatch(expression, candidate, flags=re.IGNORECASE) is not None


def _is_vercel_ignored(rel_path: str, patterns: list[str]) -> bool:
    rel_path = rel_path.replace("\\", "/").strip("/")
    cache: dict[tuple[str, bool], bool] = {}

    def is_kept(candidate: str, *, directory: bool = False) -> bool:
        cache_key = (candidate, directory)
        if cache_key in cache:
            return cache[cache_key]
        parts = candidate.split("/") if candidate else []
        if len(parts) > 1:
            parent = "/".join(parts[:-1])
            if not is_kept(parent, directory=True):
                cache[cache_key] = False
                return False
        ignored = False
        match_path = candidate + "/" if directory else candidate
        for pattern in patterns:
            negated = pattern.startswith("!")
            raw = pattern[1:] if negated else pattern
            if _vercelignore_matches(match_path, raw):
                ignored = not negated
        cache[cache_key] = not ignored
        return not ignored

    return not is_kept(rel_path)


def _clean_route(artifact: str) -> str:
    if artifact == "index.html":
        return "/"
    if artifact.endswith("/index.html"):
        stem = artifact[: -len("/index.html")]
        return "/" + stem.strip("/") + "/"
    if artifact.endswith(".html"):
        stem = artifact[: -len(".html")]
        return "/" + stem.strip("/") + "/"
    raise ContractError(f"public lifecycle artifact is not HTML: {artifact}")


def _exact_sitemap_contract(root: Path, expected_routes: set[str]) -> dict[str, Any]:
    path_errors: list[str] = []
    path = repo_file(root, SITEMAP.as_posix(), "public sitemap owner", path_errors)
    if path is None:
        raise ContractError(path_errors)
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        raise ContractError(f"cannot parse {SITEMAP}: {exc}") from exc
    locations = [
        element.text.strip()
        for element in tree.getroot().iter()
        if element.tag.rsplit("}", 1)[-1] == "loc"
        and isinstance(element.text, str)
        and element.text.strip()
    ]
    routes: list[str] = []
    for location in locations:
        parsed = urlparse(location)
        if (
            parsed.scheme != "https"
            or parsed.netloc != "emergentism.org"
            or parsed.query
            or parsed.fragment
        ):
            raise ContractError(f"sitemap location escapes the canonical origin: {location}")
        route = parsed.path or "/"
        if route != "/" and not route.endswith("/"):
            raise ContractError(f"sitemap route is not a clean trailing-slash route: {route}")
        routes.append(route)
    if len(routes) != len(set(routes)):
        raise ContractError("public sitemap contains duplicate canonical routes")
    actual = set(routes)
    missing = sorted(expected_routes - actual)
    extra = sorted(actual - expected_routes)
    if missing or extra:
        detail = []
        if missing:
            detail.append("missing=" + ",".join(missing))
        if extra:
            detail.append("extra=" + ",".join(extra))
        raise ContractError(
            "public sitemap differs from current+provisional HTML routes: "
            + "; ".join(detail)
        )
    return {
        "artifact": str(SITEMAP),
        "classes": ["current", "provisional"],
        "routes": len(actual),
        "routes_sha256": path_set_sha256(actual),
    }


def _header_source_covers(source: str, route: str) -> bool:
    if source == route:
        return True
    if source.endswith("(.*)"):
        return route.startswith(source[:-4])
    return False


class _RobotsMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.directives: set[str] = set()

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.lower() != "meta":
            return
        names = [
            value.strip().lower()
            for key, value in attrs
            if key.lower() == "name" and value is not None
        ]
        if "robots" not in names:
            return
        for key, value in attrs:
            if key.lower() != "content" or value is None:
                continue
            self.directives.update(
                token for token in re.split(r"[\s,]+", value.strip().lower()) if token
            )


def _meta_robots_directives(path: Path) -> set[str]:
    parser = _RobotsMetaParser()
    try:
        parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
        parser.close()
    except OSError as exc:
        raise ContractError(f"cannot inspect robots metadata in {path}: {exc}") from exc
    return parser.directives


def _validated_withheld_artifacts(site: Path, artifacts: list[Any]) -> set[str]:
    if site.is_symlink() or not site.is_dir():
        raise ContractError("withheld artifact site root must be a regular, non-symlink directory")
    validated: set[str] = set()
    for index, item in enumerate(artifacts):
        if not isinstance(item, dict):
            raise ContractError(f"withheld artifact row {index} must be an object")
        value = item.get("artifact")
        if not isinstance(value, str) or not value:
            raise ContractError(f"withheld artifact row {index} has no artifact path")
        rel = Path(value)
        if (
            rel.is_absolute()
            or ".." in rel.parts
            or rel.as_posix() != value
            or rel.suffix.lower() != ".html"
        ):
            raise ContractError(f"withheld artifact path is unsafe or not HTML: {value!r}")
        target = site / rel
        if _has_symlink_component(site, value):
            raise ContractError(
                f"withheld artifact must not traverse a symlink: {value}"
            )
        try:
            target.resolve().relative_to(site.resolve())
        except ValueError as exc:
            raise ContractError(f"withheld artifact escapes the public site: {value}") from exc
        if not target.is_file() or target.is_symlink():
            raise ContractError(
                f"withheld artifact is missing or not a regular file: {value}"
            )
        try:
            body = target.read_bytes()
        except OSError as exc:
            raise ContractError(f"cannot read withheld artifact {value}: {exc}") from exc
        expected_bytes = item.get("bytes")
        if not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool):
            raise ContractError(f"withheld artifact {value} has invalid byte count")
        if expected_bytes != len(body):
            raise ContractError(
                f"withheld artifact {value} byte count drifted: "
                f"registry={expected_bytes}, actual={len(body)}"
            )
        expected_sha = item.get("sha256")
        if not isinstance(expected_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            raise ContractError(
                f"withheld artifact {value} must carry a lowercase SHA-256"
            )
        actual_sha = hashlib.sha256(body).hexdigest()
        if expected_sha != actual_sha:
            raise ContractError(
                f"withheld artifact {value} SHA-256 drifted: "
                f"registry={expected_sha}, actual={actual_sha}"
            )
        if value in validated:
            raise ContractError(f"withheld artifact registry repeats path {value}")
        validated.add(value)
    return validated


def _canonical_public_alias(route: str) -> str:
    if not isinstance(route, str) or not route.startswith("/"):
        raise ContractError(f"public alias must be root-relative: {route!r}")
    clean = route.split("#", 1)[0].split("?", 1)[0]
    if clean == "/":
        return "/"
    if clean.endswith("/index.html"):
        clean = clean[: -len("/index.html")]
    elif clean.endswith(".html"):
        clean = clean[: -len(".html")]
    return "/" + clean.strip("/") + "/"


def _artifact_has_directory_owner(site: Path, artifact: str) -> bool:
    """Whether a sibling directory owns the clean URL for ``foo.html``."""

    path = Path(artifact)
    return path.suffix == ".html" and path.name != "index.html" and (
        site / path.with_suffix("") / "index.html"
    ).is_file()


def _artifact_delivery_aliases(site: Path, artifact: str) -> set[str]:
    """Delivery aliases, preserving a sibling directory's clean URL ownership."""

    # A retained ``foo.html`` may coexist with ``foo/index.html``.  The latter
    # owns /foo and /foo/ under cleanUrls; the former is a raw custody artifact
    # addressed only as /foo.html.  Treating both as clean aliases created a
    # false two-owner delivery contract for an intentionally withheld pair.
    if _artifact_has_directory_owner(site, artifact):
        return {"/" + artifact.lstrip("/")}
    canonical = _clean_route(artifact)
    clean = canonical.rstrip("/") or "/"
    physical = "/" + artifact.lstrip("/")
    return {clean, canonical, physical}


def _expected_withheld_aliases(site: Path, artifact: str) -> set[str]:
    """Exact delivery forms, allowing raw-only custody behind a directory owner."""
    expected = _artifact_delivery_aliases(site, artifact)
    expected_count = 1 if _artifact_has_directory_owner(site, artifact) else 3
    if len(expected) != expected_count:
        raise ContractError(
            f"withheld artifact {artifact} does not yield {expected_count} distinct delivery aliases"
        )
    return expected


def compute_public_lifecycle(root: Path) -> dict[str, Any]:
    site = root / PUBLIC_DIR
    site_entries = _strict_tree_entries(root, PUBLIC_DIR, "public lifecycle")
    owner_paths: dict[Path, Path] = {}
    owner_errors: list[str] = []
    for relative, label in (
        (PUBLIC_PARITY, "public semantic-parity machine owner"),
        (WITHHELD_REGISTRY, "withheld-route machine owner"),
        (VERCEL_CONFIG, "public delivery-config machine owner"),
        (VERCEL_IGNORE, "public deployment-ignore machine owner"),
        (PREDEPLOY_CHECKER, "public deployment matcher"),
        (SITEMAP, "public sitemap machine owner"),
    ):
        path = repo_file(root, relative.as_posix(), label, owner_errors)
        if path is not None:
            owner_paths[relative] = path
    if owner_errors:
        raise ContractError(owner_errors)

    matcher_root = Path(str(getattr(_PREDEPLOY_POLICY, "BASE_DIR", "")))
    if matcher_root.resolve() != site.resolve():
        raise ContractError(
            "public predeploy matcher root differs from the contact-limited site root"
        )

    parity = load_json(owner_paths[PUBLIC_PARITY])
    withheld_registry = load_json(owner_paths[WITHHELD_REGISTRY])
    vercel = load_json(owner_paths[VERCEL_CONFIG])
    patterns = _load_vercelignore(owner_paths[VERCEL_IGNORE])

    artifacts = require_list(withheld_registry.get("artifacts"), "withheld artifacts", [])
    withheld_artifacts = _validated_withheld_artifacts(site, artifacts)

    def is_runtime_output(path: Path) -> bool:
        relative = path.relative_to(site)
        return bool(
            relative.parts and relative.parts[0] in PUBLIC_RUNTIME_OUTPUT_DIRS
        )

    # Vercel's local build tree is ignored by the uploader and by the public
    # predeploy walker.  It is workstation runtime output, not a source-owned
    # lifecycle artifact, so it must not perturb the frozen source census.
    html_entries = [
        path
        for path in site_entries
        if path.suffix.lower() == ".html" and not is_runtime_output(path)
    ]
    non_files = [path.relative_to(site).as_posix() for path in html_entries if not path.is_file()]
    if non_files:
        raise ContractError(
            "public HTML inventory contains non-regular entries: " + ", ".join(non_files)
        )
    present = {path.relative_to(site).as_posix() for path in html_entries}
    ignored = {rel for rel in present if _is_vercel_ignored(rel, patterns)}
    deployable = present - ignored
    nested_archive = "compass/_archive/index_2026_07_12_pre_restructure.html"
    if nested_archive not in ignored:
        raise ContractError(
            "gitignore-style _archive/ semantics no longer exclude the nested compass artifact"
        )

    predeploy_patterns = _PREDEPLOY_POLICY.load_vercelignore_patterns()
    if predeploy_patterns != patterns:
        raise ContractError(
            "public predeploy and contact-limited checkers loaded different .vercelignore patterns"
        )
    matcher_paths = {
        path.relative_to(site).as_posix()
        for path in site_entries
        if path.is_file() and not is_runtime_output(path)
    }
    matcher_mismatches = sorted(
        rel
        for rel in matcher_paths
        if _is_vercel_ignored(rel, patterns)
        != _PREDEPLOY_POLICY.is_vercel_ignored(rel, predeploy_patterns)
    )
    if matcher_mismatches:
        raise ContractError(
            "public deployment matcher drifted from the contact-limited matcher: "
            + ", ".join(matcher_mismatches[:10])
        )

    current = {
        item
        for item in require_list(parity.get("currentSurfaces"), "currentSurfaces", [])
        if isinstance(item, str) and item.endswith(".html")
    }
    provisional_block = require_mapping(
        parity.get("declaredProvisional"), "declaredProvisional", []
    )
    provisional = set(
        item
        for item in require_list(provisional_block.get("routes"), "provisional routes", [])
        if isinstance(item, str)
    )
    infrastructure_block = require_mapping(
        parity.get("infrastructureRoutes"), "infrastructureRoutes", []
    )
    infrastructure = set(
        item
        for item in require_list(
            infrastructure_block.get("routes"), "infrastructure routes", []
        )
        if isinstance(item, str)
    )
    boundary = require_mapping(withheld_registry.get("boundary"), "withheld boundary", [])
    boundary_artifact = boundary.get("artifactRoute")
    if not isinstance(boundary_artifact, str):
        raise ContractError("withheld boundary must name artifactRoute")
    withheld = set(withheld_artifacts) | {boundary_artifact}

    explicit = {
        "current": current,
        "provisional": provisional,
        "infrastructure": infrastructure,
        "withheld": withheld,
    }
    overlap_errors: list[str] = []
    names = list(explicit)
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            overlap = sorted(explicit[left] & explicit[right])
            if overlap:
                overlap_errors.append(
                    f"public artifacts classified as both {left} and {right}: "
                    + ", ".join(overlap)
                )
    if overlap_errors:
        raise ContractError(overlap_errors)

    sitemap_contract = _exact_sitemap_contract(
        root,
        {_clean_route(artifact) for artifact in current | provisional},
    )

    universe = deployable | withheld_artifacts
    for name, declared in explicit.items():
        missing = sorted(declared - universe)
        if missing:
            raise ContractError(
                f"{name} lifecycle artifacts are absent from the public universe: "
                + ", ".join(missing)
            )

    # Current and provisional are affirmative indexability assertions.  An
    # artifact cannot retain either class while its own HTML says noindex/none;
    # this is a contradiction, not another implicit frozen classification.
    for asserted_class in ("current", "provisional"):
        for artifact in sorted(explicit[asserted_class]):
            directives = _meta_robots_directives(site / artifact)
            hidden = sorted({"noindex", "none"} & directives)
            if hidden:
                raise ContractError(
                    f"{asserted_class} artifact {artifact} self-declares search hiding: "
                    + ", ".join(hidden)
                )

    if vercel.get("cleanUrls") is not True or vercel.get("trailingSlash") is not True:
        raise ContractError("public delivery alias contract requires cleanUrls + trailingSlash")

    # `frozen` is the response-header noindex/follow library lifecycle.  A
    # noindex/nofollow withholding response is a different raw class; conflating
    # the two hid the overlap boundary during the red-team pass.
    frozen_sources: list[str] = []
    withheld_header_sources: list[str] = []
    for rule in require_list(vercel.get("headers"), "vercel headers", []):
        if not isinstance(rule, dict) or not isinstance(rule.get("source"), str):
            continue
        robots: set[str] = set()
        for header in rule.get("headers", []):
            if (
                not isinstance(header, dict)
                or str(header.get("key", "")).lower() != "x-robots-tag"
            ):
                continue
            robots.update(
                token.strip().lower()
                for token in str(header.get("value", "")).split(",")
                if token.strip()
            )
        # X-Robots-Tag `none` is the standard shorthand for noindex,nofollow.
        # Aggregate every header occurrence so a later `index` value cannot
        # erase an earlier search-hiding directive in the same response rule.
        if "none" in robots:
            robots.update({"noindex", "nofollow"})
        if "noindex" in robots and "nofollow" in robots:
            withheld_header_sources.append(rule["source"])
        elif "noindex" in robots:
            frozen_sources.append(rule["source"])

    redirect_map: dict[str, tuple[str, bool]] = {}
    redirect_rules: list[tuple[str, str, bool]] = []
    for redirect in require_list(vercel.get("redirects"), "vercel redirects", []):
        if not isinstance(redirect, dict) or not isinstance(redirect.get("source"), str):
            continue
        value = (str(redirect.get("destination")), bool(redirect.get("permanent")))
        prior = redirect_map.get(redirect["source"])
        if prior is not None and prior != value:
            raise ContractError(f"conflicting redirects for {redirect['source']}")
        redirect_map[redirect["source"]] = value
        redirect_rules.append((redirect["source"], value[0], value[1]))

    boundary_route = boundary.get("publicRoute")
    if not isinstance(boundary_route, str):
        raise ContractError("withheld boundary must name publicRoute")
    raw_alias_owner: dict[str, str] = {}
    canonical_alias_owner: dict[str, str] = {}
    raw_alias_count = 0
    for item in artifacts:
        artifact = str(item.get("artifact"))
        aliases = require_list(item.get("publicRoutes"), f"{artifact}.publicRoutes", [])
        if not aliases:
            raise ContractError(f"withheld artifact {artifact} has no public aliases")
        if any(not isinstance(alias, str) for alias in aliases):
            raise ContractError(f"withheld artifact {artifact} has a non-string alias")
        expected_aliases = _expected_withheld_aliases(site, artifact)
        if len(aliases) != len(set(aliases)):
            raise ContractError(f"withheld artifact {artifact} repeats a public alias")
        if set(aliases) != expected_aliases:
            raise ContractError(
                f"withheld artifact {artifact} aliases drifted: "
                f"stored={sorted(aliases)}, expected={sorted(expected_aliases)}"
            )
        has_directory_owner = _artifact_has_directory_owner(site, artifact)
        expected_alias = _clean_route(artifact)
        for alias in aliases:
            raw_alias_count += 1
            previous = raw_alias_owner.get(alias)
            if previous is not None and previous != artifact:
                raise ContractError(
                    f"withheld public alias {alias} belongs to both {previous} and {artifact}"
                )
            raw_alias_owner[alias] = artifact
            canonical = _canonical_public_alias(alias)
            if not has_directory_owner and canonical != expected_alias:
                raise ContractError(
                    f"withheld alias {alias} canonicalizes to {canonical}, not {expected_alias} "
                    f"for {artifact}"
                )
            if not has_directory_owner:
                previous = canonical_alias_owner.get(canonical)
                if previous is not None and previous != artifact:
                    raise ContractError(
                        f"withheld canonical alias {canonical} belongs to both {previous} and {artifact}"
                    )
                canonical_alias_owner[canonical] = artifact
            if redirect_map.get(alias) != (boundary_route, False):
                raise ContractError(
                    f"withheld alias {alias} lacks the temporary redirect to {boundary_route}"
                )
            if not any(
                _header_source_covers(source, alias)
                for source in withheld_header_sources
            ):
                raise ContractError(
                    f"withheld alias {alias} lacks an effective noindex,nofollow response"
                )

    withheld_alias_counts = {
        "artifacts": len(artifacts),
        "raw_aliases": raw_alias_count,
        "canonical_aliases": len(canonical_alias_owner),
        "redirect_target": boundary_route,
        "required_response": "noindex,nofollow",
    }

    raw_memberships: dict[str, set[str]] = {}
    route_owners: dict[str, list[str]] = defaultdict(list)
    for artifact in sorted(universe):
        route = _clean_route(artifact)
        aliases = _artifact_delivery_aliases(site, artifact)
        # When ``foo.html`` coexists with ``foo/index.html``, the retained
        # flat file is a raw-only custody artifact.  It must retain its own
        # lifecycle checks, but it must not compete with the directory page
        # for the canonical clean ``/foo/`` delivery route.
        if not _artifact_has_directory_owner(site, artifact):
            route_owners[route].append(artifact)
        memberships = {
            name for name, values in explicit.items() if artifact in values
        }
        if any(
            _header_source_covers(source, alias)
            for source in frozen_sources
            for alias in aliases
        ):
            memberships.add("frozen")
        if any(
            _header_source_covers(source, alias)
            for source in withheld_header_sources
            for alias in aliases
        ):
            memberships.add("withheld")
        matching_redirects = [
            (source, destination, permanent, alias)
            for source, destination, permanent in redirect_rules
            for alias in aliases
            if _header_source_covers(source, alias)
        ]
        if matching_redirects:
            if artifact not in withheld_artifacts:
                details = ", ".join(
                    f"{source}->{destination} on {alias}"
                    for source, destination, _permanent, alias in matching_redirects
                )
                raise ContractError(
                    f"non-withheld artifact {artifact} has an effective redirect: {details}"
                )
            invalid_redirects = [
                (source, destination, permanent, alias)
                for source, destination, permanent, alias in matching_redirects
                if destination != boundary_route or permanent
            ]
            if invalid_redirects:
                raise ContractError(
                    f"withheld artifact {artifact} has a redirect outside its boundary contract"
                )
        if not memberships:
            memberships.add("unclassified")
        raw_memberships[artifact] = memberships

    alias_collisions: list[dict[str, Any]] = []
    for route, owners in sorted(route_owners.items()):
        if len(owners) < 2:
            continue
        lifecycle_sets = [raw_memberships[artifact] for artifact in owners]
        if any(item != lifecycle_sets[0] for item in lifecycle_sets[1:]):
            raise ContractError(
                f"canonical delivery alias {route} has lifecycle disagreement: "
                + "; ".join(
                    f"{artifact}={sorted(raw_memberships[artifact])}"
                    for artifact in owners
                )
            )
        shared = sorted(lifecycle_sets[0])
        if len(shared) != 1:
            raise ContractError(
                f"canonical delivery alias {route} has ambiguous shared raw lifecycle {shared}"
            )
        alias_collisions.append(
            {
                "route": route,
                "artifacts": sorted(owners),
                "shared_raw_lifecycle": shared[0],
            }
        )

    overlap_groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for artifact, memberships in raw_memberships.items():
        if len(memberships) > 1:
            overlap_groups[tuple(sorted(memberships))].append(artifact)
    raw_overlaps = [
        {"classes": list(classes), "artifacts": sorted(artifacts)}
        for classes, artifacts in sorted(overlap_groups.items())
    ]

    categories: dict[str, set[str]] = {
        "current": set(),
        "provisional": set(),
        "frozen": set(),
        "withheld": set(),
        "infrastructure": set(),
        "unclassified": set(),
    }
    for artifact, memberships in sorted(raw_memberships.items()):
        category = next(name for name in EXPECTED_PRECEDENCE if name in memberships)
        categories[category].add(artifact)

    classified_union = set().union(*categories.values())
    if classified_union != universe or sum(map(len, categories.values())) != len(universe):
        raise ContractError("public lifecycle classification is not exclusive and exhaustive")

    counts = {name: len(values) for name, values in categories.items()}
    counts = {"total": len(universe), **counts}
    membership_hashes = {
        "universe_sha256": path_set_sha256(universe),
        "category_sha256": {
            f"{name}_sha256": path_set_sha256(categories[name])
            for name in PUBLIC_CATEGORIES
        },
    }
    return {
        "ignore_counts": {
            "present_html": len(present),
            "ignored_html": len(ignored),
            "deployable_html": len(deployable),
            "withheld_artifacts_added_back": len(withheld_artifacts),
        },
        "alias_collisions": alias_collisions,
        "raw_overlaps": raw_overlaps,
        "withheld_alias_contract": withheld_alias_counts,
        "sitemap_contract": sitemap_contract,
        "matcher_conformance": {
            "checked_paths": len(matcher_paths),
            "ignored_paths": sum(
                _is_vercel_ignored(rel, patterns) for rel in matcher_paths
            ),
            "mismatches": matcher_mismatches,
        },
        "membership_hashes": membership_hashes,
        "counts": counts,
        "unclassified": sorted(categories["unclassified"]),
    }


def compute_claim_disposition(root: Path) -> dict[str, Any]:
    try:
        claim_errors = _CLAIM_STATUS_POLICY.check(root)
        source = _CLAIM_STATUS_POLICY.load_document(root / CLAIM_SOURCE)
    except _CLAIM_STATUS_POLICY.ContractError as exc:
        raise ContractError(str(exc)) from exc
    if claim_errors:
        raise ContractError([f"claim-status contract: {error}" for error in claim_errors])

    def required_rows(section: str) -> list[dict[str, Any]]:
        rows = source.get(section)
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ContractError(
                f"claim-status contract: {section} must be a list of row objects"
            )
        return list(rows)

    open_rows = required_rows("open")
    investigation_rows = required_rows("investigations")
    grave_rows = required_rows("graves")
    typed_survivor_rows = required_rows("typed_survivors")
    current_rows = [*open_rows, *investigation_rows]
    if len(current_rows) + len(grave_rows) != EXPECTED_LIFECYCLE_ROWS:
        raise ContractError(
            "claim-status contract: lifecycle must contain exactly "
            f"{EXPECTED_LIFECYCLE_ROWS} open/investigation/grave rows"
        )
    lifecycle_ids = {
        str(row.get("id")) for row in [*current_rows, *grave_rows]
    }
    survivor_ids = {str(row.get("id")) for row in typed_survivor_rows}
    if lifecycle_ids & survivor_ids:
        raise ContractError(
            "claim-status contract: typed survivors must remain outside the "
            "50-row open/investigation/grave lifecycle"
        )
    live_statuses = set(source["live_statuses"])
    terminal_statuses = set(source["terminal_statuses"])

    def ids_for(rows: list[dict[str, Any]], *kinds: str) -> list[str]:
        return [
            str(row["id"])
            for row in rows
            if row["disposition"]["kind"] in set(kinds)
        ]

    statuses = {str(row["id"]): str(row["status"]) for row in current_rows}
    grave_statuses = {str(row["id"]): str(row["status"]) for row in grave_rows}
    direct = ids_for(current_rows, "CONTACT-GATED")
    merged = ids_for(current_rows, "MERGED-TO-CONTACT")
    narrowed = ids_for(current_rows, "INTERNAL-NARROWED")
    internal_terminal = ids_for(current_rows, "INTERNAL-TERMINAL")
    grave_merged = ids_for(grave_rows, "MERGED-TO-OWNER")
    grave_terminal = ids_for(grave_rows, "INTERNAL-TERMINAL")
    contract_ids = sorted(
        contract["contract_id"]
        for row in current_rows
        if row["disposition"]["kind"] == "CONTACT-GATED"
        for contract in row["disposition"]["contracts"]
    )
    classified_current = set(direct) | set(merged) | set(narrowed) | set(internal_terminal)
    classified_graves = set(grave_merged) | set(grave_terminal)
    ambiguous = sorted(
        ({str(row["id"]) for row in current_rows} - classified_current)
        | ({str(row["id"]) for row in grave_rows} - classified_graves)
    )
    return {
        "lifecycle_rows_total": len(current_rows) + len(grave_rows),
        "lifecycle_rows_sha256": _CLAIM_STATUS_POLICY.canonical_lifecycle_sha256(source),
        "claim_status_contract_sha256": _CLAIM_STATUS_POLICY.canonical_contract_sha256(source),
        "unique_external_contracts": len(contract_ids),
        "external_contract_ids": contract_ids,
        "ambiguous_rows": ambiguous,
        "current_scope": {
            "rows": len(current_rows),
            "live_status_rows": sum(status in live_statuses for status in statuses.values()),
            "terminal_status_rows": sum(status in terminal_statuses for status in statuses.values()),
            "status_counts": dict(Counter(statuses.values())),
            "statuses": statuses,
            "direct_contact": direct,
            "merged_contact": merged,
            "contact_routed": direct + merged,
            "internal_narrowed": narrowed,
            "internal_terminal": internal_terminal,
        },
        "grave_scope": {
            "rows": len(grave_rows),
            "terminal_status_rows": sum(status in terminal_statuses for status in grave_statuses.values()),
            "narrowed_status_rows": sum(status == "NARROWED" for status in grave_statuses.values()),
            "status_counts": dict(Counter(grave_statuses.values())),
            "statuses": grave_statuses,
            "merged_to_owner": grave_merged,
            "internal_terminal": grave_terminal,
            "active_parent_investigations": 0,
        },
    }


def compute_owner_debts(root: Path) -> set[str]:
    docket_errors = owner_docket_unset_errors(root)
    if docket_errors:
        raise ContractError(docket_errors)
    profile = load_json(root / COHERENCE_SOURCE)
    axes = require_mapping(profile.get("axes"), "coherence axes", [])
    routing = require_mapping(axes.get("routing"), "coherence routing axis", [])
    if routing.get("state") != "PASS_WITH_DEBT":
        raise ContractError(
            "coherence routing axis must remain PASS_WITH_DEBT while owner dockets are unset"
        )
    debt_ids = require_list(routing.get("debt_ids"), "routing debt_ids", [])
    if any(not isinstance(item, str) for item in debt_ids) or len(set(debt_ids)) != len(
        debt_ids
    ):
        raise ContractError("coherence routing debt_ids must be unique strings")
    debts = set(debt_ids)
    if debts != EXPECTED_DEBTS:
        raise ContractError(
            "coherence routing axis must retain exactly the two unset owner debts"
        )
    overall = require_mapping(profile.get("overall"), "coherence overall", [])
    if overall.get("scope") != "internal" or overall.get("state") != "PASS_WITH_DEBT":
        raise ContractError(
            "coherence overall must remain internal PASS_WITH_DEBT while owner dockets are unset"
        )
    return debts


def compute_world_contact(root: Path) -> dict[str, Any]:
    profile = load_json(root / COHERENCE_SOURCE)
    axes = require_mapping(profile.get("axes"), "coherence axes", [])
    world = require_mapping(axes.get("world_contact"), "world_contact axis", [])
    evidence = require_list(world.get("evidence"), "world_contact evidence", [])
    requirements = require_list(
        world.get("open_requirements"), "world_contact open_requirements", []
    )
    return {
        "state": world.get("state"),
        "accepted_evidence_records": len(evidence),
        "open_requirements": requirements,
    }


def validate_state(state: Any, root: Path = ROOT) -> dict[str, Any]:
    errors: list[str] = []
    state = require_mapping(state, str(STATE_PATH), errors)
    exact_keys(
        state,
        {
            "schema",
            "status",
            "routing_role",
            "roadmap",
            "baseline_rule",
            "receipt_namespace",
            "public_lifecycle",
            "claim_disposition",
            "owner_held",
            "world_contact",
        },
        "contact-limited state",
        errors,
    )
    if state.get("schema") != "emergentism/contact-limited-state/v1":
        errors.append("unsupported contact-limited state schema")
    if state.get("status") != "OPEN_INTERNAL":
        errors.append("contact-limited status must remain OPEN_INTERNAL")
    for key in ("routing_role", "baseline_rule"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            errors.append(f"{key} must be a non-empty boundary statement")
    repo_file(root, state.get("roadmap"), "roadmap", errors)

    receipt_state = require_mapping(
        state.get("receipt_namespace"), "receipt_namespace", errors
    )
    exact_keys(
        receipt_state,
        {
            "receipt_ref",
            "source_index",
            "source_checker",
            "target_universe",
            "target_files",
            "prefixed_markdown_including_00_convention",
            "unique_prefixes",
            "reused_prefixes",
            "legacy_heuristic_dangerous_prefixes",
            "bare_unsafe_reused_prefixes",
            "bare_numeric_boundary",
            "identity_hash_contract",
            "dangling_citations",
        },
        "receipt_namespace",
        errors,
    )
    receipt_ref(root, receipt_state.get("receipt_ref"), "receipt_namespace.receipt_ref", errors)
    if receipt_state.get("source_index") != str(RECEIPT_INDEX):
        errors.append("receipt_namespace.source_index is not the machine owner")
    if receipt_state.get("source_checker") != str(RECEIPT_CHECKER):
        errors.append("receipt_namespace.source_checker is not the machine owner")
    repo_file(root, receipt_state.get("source_index"), "receipt source_index", errors)
    repo_file(root, receipt_state.get("source_checker"), "receipt source_checker", errors)
    if not isinstance(receipt_state.get("target_universe"), str) or "excluding the 00_" not in receipt_state.get(
        "target_universe", ""
    ):
        errors.append("receipt target_universe must distinguish citable targets from 00_* convention files")
    bare_boundary = str(receipt_state.get("bare_numeric_boundary", ""))
    legacy_dangerous = receipt_state.get("legacy_heuristic_dangerous_prefixes")
    expected_bare_boundary = (
        f"All {EXPECTED_REUSED_PREFIXES} reused prefixes remain unsafe as bare citations. "
        f"The live legacy heuristic marks {legacy_dangerous} dangerous prefixes but proves "
        "no target, direction, reciprocity, or cross-lane disambiguation."
    )
    if bare_boundary != expected_bare_boundary:
        errors.append(
            "bare_numeric_boundary must state the exact 101-prefix unsafe boundary "
            "without presenting the legacy heuristic as proof"
        )
    if (
        receipt_state.get("reused_prefixes") != EXPECTED_REUSED_PREFIXES
        or receipt_state.get("bare_unsafe_reused_prefixes")
        != EXPECTED_REUSED_PREFIXES
    ):
        errors.append(
            "receipt namespace must retain exactly 101 reused and bare-unsafe prefixes"
        )
    receipt_identity_state = require_mapping(
        receipt_state.get("identity_hash_contract"),
        "receipt_namespace.identity_hash_contract",
        errors,
    )
    exact_keys(
        receipt_identity_state,
        {
            "path_set_canonicalization",
            "duplicate_group_canonicalization",
            "citable_targets_sha256",
            "prefixed_including_00_sha256",
            "duplicate_groups_sha256",
        },
        "receipt_namespace.identity_hash_contract",
        errors,
    )
    if receipt_identity_state.get("path_set_canonicalization") != PATH_SET_HASH_RULE:
        errors.append("receipt path-set hash canonicalization drifted")
    if receipt_identity_state.get("duplicate_group_canonicalization") != DUPLICATE_GROUP_HASH_RULE:
        errors.append("receipt duplicate-group hash canonicalization drifted")

    public_state = require_mapping(state.get("public_lifecycle"), "public_lifecycle", errors)
    exact_keys(
        public_state,
        {
            "receipt_ref",
            "universe_definition",
            "sources",
            "deploy_ignore_contract",
            "delivery_contract",
            "membership_hash_contract",
            "counts",
            "unclassified",
        },
        "public_lifecycle",
        errors,
    )
    receipt_ref(root, public_state.get("receipt_ref"), "public_lifecycle.receipt_ref", errors)
    if not isinstance(public_state.get("universe_definition"), str) or not public_state.get(
        "universe_definition", ""
    ).strip():
        errors.append("public_lifecycle.universe_definition must be non-empty")
    public_sources = require_list(public_state.get("sources"), "public_lifecycle.sources", errors)
    expected_public_sources = {
        str(PUBLIC_PARITY),
        str(WITHHELD_REGISTRY),
        str(VERCEL_CONFIG),
        str(VERCEL_IGNORE),
        str(SITEMAP),
    }
    if set(item for item in public_sources if isinstance(item, str)) != expected_public_sources:
        errors.append("public_lifecycle.sources must name all five machine owners exactly")
    for index, source in enumerate(public_sources):
        repo_file(root, source, f"public_lifecycle.sources[{index}]", errors)

    membership_state = require_mapping(
        public_state.get("membership_hash_contract"),
        "public_lifecycle.membership_hash_contract",
        errors,
    )
    exact_keys(
        membership_state,
        {"canonicalization", "universe_sha256", "category_sha256"},
        "public_lifecycle.membership_hash_contract",
        errors,
    )
    if membership_state.get("canonicalization") != PATH_SET_HASH_RULE:
        errors.append("public membership hash canonicalization drifted")
    category_hash_state = require_mapping(
        membership_state.get("category_sha256"),
        "public_lifecycle.membership_hash_contract.category_sha256",
        errors,
    )
    exact_keys(
        category_hash_state,
        {f"{name}_sha256" for name in PUBLIC_CATEGORIES},
        "public_lifecycle.membership_hash_contract.category_sha256",
        errors,
    )

    ignore_state = require_mapping(
        public_state.get("deploy_ignore_contract"), "deploy_ignore_contract", errors
    )
    exact_keys(
        ignore_state,
        {
            "semantics",
            "present_html",
            "ignored_html",
            "deployable_html",
            "withheld_artifacts_added_back",
            "matcher_conformance",
        },
        "deploy_ignore_contract",
        errors,
    )
    if "at any depth" not in str(ignore_state.get("semantics", "")):
        errors.append("deploy-ignore semantics must pin unanchored directory matching at any depth")
    matcher_conformance = require_mapping(
        ignore_state.get("matcher_conformance"), "matcher_conformance", errors
    )
    exact_keys(
        matcher_conformance,
        {"state", "pattern", "excluded_artifact", "implementations", "evidence"},
        "matcher_conformance",
        errors,
    )
    if (
        matcher_conformance.get("state") != "CLOSED_LOCAL_PARITY"
        or matcher_conformance.get("pattern") != "_archive/"
    ):
        errors.append("deployment matcher conformance must remain closed on the _archive/ rule")
    if matcher_conformance.get("excluded_artifact") != "compass/_archive/index_2026_07_12_pre_restructure.html":
        errors.append("matcher conformance lost the nested compass archive artifact")
    expected_matcher_implementations = {
        str(PREDEPLOY_CHECKER),
        "09_TOOLS/01_SCRIPTS/check_contact_limited.py",
    }
    implementations = require_list(
        matcher_conformance.get("implementations"),
        "matcher_conformance.implementations",
        errors,
    )
    if set(item for item in implementations if isinstance(item, str)) != expected_matcher_implementations:
        errors.append("matcher conformance must name both local implementations exactly")
    for index, implementation in enumerate(implementations):
        repo_file(root, implementation, f"matcher_conformance.implementations[{index}]", errors)
    for index, evidence in enumerate(
        require_list(matcher_conformance.get("evidence"), "matcher_conformance.evidence", errors)
    ):
        repo_file(root, evidence, f"matcher_conformance.evidence[{index}]", errors)

    delivery_state = require_mapping(
        public_state.get("delivery_contract"), "delivery_contract", errors
    )
    exact_keys(
        delivery_state,
        {
            "cleanUrls",
            "trailingSlash",
            "precedence",
            "withheld_alias_contract",
            "sitemap_contract",
            "alias_collisions",
            "allowed_raw_overlaps",
        },
        "delivery_contract",
        errors,
    )
    if delivery_state.get("cleanUrls") is not True or delivery_state.get("trailingSlash") is not True:
        errors.append("delivery contract must pin cleanUrls + trailingSlash")
    if tuple(require_list(delivery_state.get("precedence"), "delivery precedence", errors)) != EXPECTED_PRECEDENCE:
        errors.append("delivery lifecycle precedence drifted")
    withheld_alias_state = require_mapping(
        delivery_state.get("withheld_alias_contract"), "withheld_alias_contract", errors
    )

    sitemap_state = require_mapping(
        delivery_state.get("sitemap_contract"), "sitemap_contract", errors
    )
    exact_keys(
        sitemap_state,
        {"artifact", "classes", "routes", "routes_sha256", "evidence"},
        "sitemap_contract",
        errors,
    )
    if sitemap_state.get("artifact") != str(SITEMAP):
        errors.append("sitemap contract points away from the public sitemap owner")
    if sitemap_state.get("classes") != ["current", "provisional"]:
        errors.append("sitemap contract must contain only current and provisional classes")
    for index, evidence in enumerate(
        require_list(sitemap_state.get("evidence"), "sitemap_contract.evidence", errors)
    ):
        repo_file(root, evidence, f"sitemap_contract.evidence[{index}]", errors)
    exact_keys(
        withheld_alias_state,
        {
            "artifacts",
            "raw_aliases",
            "canonical_aliases",
            "redirect_target",
            "required_response",
            "evidence",
        },
        "withheld_alias_contract",
        errors,
    )
    for index, evidence in enumerate(
        require_list(withheld_alias_state.get("evidence"), "withheld_alias_contract.evidence", errors)
    ):
        repo_file(root, evidence, f"withheld_alias_contract.evidence[{index}]", errors)
    withheld_alias_contract = {
        key: withheld_alias_state.get(key)
        for key in (
            "artifacts",
            "raw_aliases",
            "canonical_aliases",
            "redirect_target",
            "required_response",
        )
    }
    collision_state = require_list(
        delivery_state.get("alias_collisions"), "alias_collisions", errors
    )
    collision_contract = []
    for index, collision in enumerate(collision_state):
        collision = require_mapping(collision, f"alias_collisions[{index}]", errors)
        exact_keys(
            collision,
            {"route", "artifacts", "shared_raw_lifecycle", "evidence"},
            f"alias_collisions[{index}]",
            errors,
        )
        for evidence_index, evidence in enumerate(
            require_list(collision.get("evidence"), f"alias_collisions[{index}].evidence", errors)
        ):
            repo_file(
                root,
                evidence,
                f"alias_collisions[{index}].evidence[{evidence_index}]",
                errors,
            )
        collision_contract.append(
            {
                "route": collision.get("route"),
                "artifacts": collision.get("artifacts"),
                "shared_raw_lifecycle": collision.get("shared_raw_lifecycle"),
            }
        )
    overlap_state = require_list(
        delivery_state.get("allowed_raw_overlaps"), "allowed_raw_overlaps", errors
    )
    overlap_contract = []
    for index, overlap_row in enumerate(overlap_state):
        overlap_row = require_mapping(overlap_row, f"allowed_raw_overlaps[{index}]", errors)
        exact_keys(
            overlap_row,
            {"classes", "artifacts", "evidence"},
            f"allowed_raw_overlaps[{index}]",
            errors,
        )
        for evidence_index, evidence in enumerate(
            require_list(overlap_row.get("evidence"), f"allowed_raw_overlaps[{index}].evidence", errors)
        ):
            repo_file(
                root,
                evidence,
                f"allowed_raw_overlaps[{index}].evidence[{evidence_index}]",
                errors,
            )
        overlap_contract.append(
            {
                "classes": overlap_row.get("classes"),
                "artifacts": overlap_row.get("artifacts"),
            }
        )
    overlap_contract.sort(key=lambda row: tuple(row.get("classes") or []))

    claim_state = require_mapping(state.get("claim_disposition"), "claim_disposition", errors)
    exact_keys(
        claim_state,
        {
            "receipt_ref",
            "source",
            "lifecycle_rows_total",
            "lifecycle_rows_sha256",
            "claim_status_contract_sha256",
            "unique_external_contracts",
            "external_contract_ids",
            "ambiguous_rows",
            "current_scope",
            "grave_scope",
        },
        "claim_disposition",
        errors,
    )
    receipt_ref(root, claim_state.get("receipt_ref"), "claim_disposition.receipt_ref", errors)
    if claim_state.get("source") != str(CLAIM_SOURCE):
        errors.append("claim_disposition.source is not the claim-status machine owner")
    repo_file(root, claim_state.get("source"), "claim_disposition.source", errors)

    owner_state = require_mapping(state.get("owner_held"), "owner_held", errors)
    exact_keys(
        owner_state,
        {"receipt_ref", "source_profile", "debts"},
        "owner_held",
        errors,
    )
    receipt_ref(root, owner_state.get("receipt_ref"), "owner_held.receipt_ref", errors)
    if owner_state.get("source_profile") != str(COHERENCE_SOURCE):
        errors.append("owner_held.source_profile is not the coherence machine owner")
    repo_file(root, owner_state.get("source_profile"), "owner_held.source_profile", errors)

    world_state = require_mapping(state.get("world_contact"), "world_contact", errors)
    exact_keys(
        world_state,
        {
            "receipt_ref",
            "source_profile",
            "state",
            "accepted_evidence_records",
            "open_requirements",
            "boundary",
            "transition_gate",
        },
        "world_contact",
        errors,
    )
    receipt_ref(root, world_state.get("receipt_ref"), "world_contact.receipt_ref", errors)
    if world_state.get("source_profile") != str(COHERENCE_SOURCE):
        errors.append("world_contact.source_profile is not the coherence machine owner")
    repo_file(root, world_state.get("source_profile"), "world_contact.source_profile", errors)
    if not isinstance(world_state.get("boundary"), str) or not world_state.get(
        "boundary", ""
    ).strip():
        errors.append("world_contact.boundary must be non-empty")
    transition_gate = require_mapping(
        world_state.get("transition_gate"), "world_contact.transition_gate", errors
    )
    exact_keys(
        transition_gate,
        {"state", "required_fields", "inadmissible_inputs"},
        "world_contact.transition_gate",
        errors,
    )
    if transition_gate.get("state") != "FAIL_CLOSED_NO_EXTERNAL_EVIDENCE_VALIDATOR":
        errors.append("world transition gate must remain fail-closed until a typed validator exists")
    if tuple(
        require_list(transition_gate.get("required_fields"), "transition required_fields", errors)
    ) != EXPECTED_WORLD_REQUIRED_FIELDS:
        errors.append("world transition required-field schema drifted")
    if tuple(
        require_list(transition_gate.get("inadmissible_inputs"), "transition inadmissible_inputs", errors)
    ) != EXPECTED_WORLD_INADMISSIBLE:
        errors.append("world transition inadmissible-input boundary drifted")

    section_receipts = [
        receipt_state.get("receipt_ref"),
        public_state.get("receipt_ref"),
        claim_state.get("receipt_ref"),
        owner_state.get("receipt_ref"),
        world_state.get("receipt_ref"),
    ]
    if any(not isinstance(value, str) for value in section_receipts) or len(
        set(section_receipts)
    ) != 1:
        errors.append("all five completion-counter sections must share one snapshot receipt")
    else:
        snapshot_receipt = repo_file(
            root, section_receipts[0], "completion snapshot receipt", errors
        )
        if snapshot_receipt is not None:
            snapshot_rel = Path(section_receipts[0])
            try:
                committed, parent = receipt_history_bytes(root, snapshot_rel)
                errors.extend(
                    snapshot_binding_errors(
                        state, snapshot_receipt.read_bytes(), committed, parent
                    )
                )
            except (ContractError, OSError) as exc:
                if isinstance(exc, ContractError):
                    errors.extend(exc.errors)
                else:
                    errors.append(f"cannot read completion snapshot receipt: {exc}")
    try:
        errors.extend(marker_receipt_custody_errors(root))
    except ContractError as exc:
        errors.extend(exc.errors)

    computed: dict[str, Any] = {}
    for name, function in (
        ("receipt_namespace", compute_receipt_namespace),
        ("public_lifecycle", compute_public_lifecycle),
        ("claim_disposition", compute_claim_disposition),
        ("owner_held", compute_owner_debts),
        ("world_contact", compute_world_contact),
    ):
        try:
            computed[name] = function(root)
        except ContractError as exc:
            errors.extend(f"{name}: {item}" for item in exc.errors)

    receipts = computed.get("receipt_namespace")
    if receipts is not None:
        if (
            receipts.get("reused_prefixes") != EXPECTED_REUSED_PREFIXES
            or receipts.get("bare_unsafe_reused_prefixes")
            != EXPECTED_REUSED_PREFIXES
        ):
            errors.append(
                "computed receipt namespace must retain exactly 101 reused and "
                "bare-unsafe prefixes"
            )
        actual_counters = {
            key: value for key, value in receipts.items() if key != "identity_hashes"
        }
        stored = {key: receipt_state.get(key) for key in actual_counters}
        if stored != actual_counters:
            errors.append(
                f"stale receipt_namespace counters: stored={stored}, actual={actual_counters}"
            )
        stored_identity_hashes = {
            key: receipt_identity_state.get(key) for key in receipts["identity_hashes"]
        }
        if stored_identity_hashes != receipts["identity_hashes"]:
            errors.append(
                "receipt namespace identity hashes drifted: "
                f"stored={stored_identity_hashes}, actual={receipts['identity_hashes']}"
            )

    public = computed.get("public_lifecycle")
    if public is not None:
        stored_ignore_counts = {
            key: ignore_state.get(key) for key in public["ignore_counts"]
        }
        if stored_ignore_counts != public["ignore_counts"]:
            errors.append(
                f"deploy-ignore counters drifted: stored={stored_ignore_counts}, "
                f"actual={public['ignore_counts']}"
            )
        if collision_contract != public["alias_collisions"]:
            errors.append(
                f"canonical alias-collision ledger drifted: stored={collision_contract}, "
                f"actual={public['alias_collisions']}"
            )
        if collision_contract != EXPECTED_ALIAS_COLLISIONS:
            errors.append("canonical alias-collision baseline changed without a new ratchet contract")
        if overlap_contract != public["raw_overlaps"]:
            errors.append(
                f"raw lifecycle overlap ledger drifted: stored={overlap_contract}, "
                f"actual={public['raw_overlaps']}"
            )
        overlap_pairs = [
            tuple(row.get("classes") or []) for row in overlap_contract
        ]
        if (
            len(overlap_pairs) != len(set(overlap_pairs))
            or set(overlap_pairs) != EXPECTED_RAW_OVERLAP_CLASSES
        ):
            errors.append(
                "raw lifecycle overlap allowlist must retain exactly the "
                "frozen/infrastructure and frozen/withheld class pairs"
            )
        infrastructure_rows = [
            row
            for row in overlap_contract
            if tuple(row.get("classes") or []) == ("frozen", "infrastructure")
        ]
        if (
            len(infrastructure_rows) != 1
            or infrastructure_rows[0].get("artifacts")
            != EXPECTED_INFRASTRUCTURE_OVERLAP
        ):
            errors.append(
                "raw lifecycle infrastructure overlap must remain exactly offline/index.html"
            )
        frozen_withheld_rows = [
            row
            for row in overlap_contract
            if tuple(row.get("classes") or []) == ("frozen", "withheld")
        ]
        if len(frozen_withheld_rows) != 1:
            errors.append(
                "raw lifecycle frozen/withheld overlap must retain one exact inventory"
            )
        else:
            frozen_withheld_artifacts = frozen_withheld_rows[0].get("artifacts")
            if (
                not isinstance(frozen_withheld_artifacts, list)
                or any(
                    not isinstance(artifact, str)
                    for artifact in frozen_withheld_artifacts
                )
                or frozen_withheld_artifacts
                != sorted(set(frozen_withheld_artifacts))
            ):
                errors.append(
                    "raw lifecycle frozen/withheld overlap inventory must be a sorted "
                    "unique string list"
                )
            elif (
                len(frozen_withheld_artifacts)
                != EXPECTED_FROZEN_WITHHELD_OVERLAP_COUNT
                or path_set_sha256(frozen_withheld_artifacts)
                != EXPECTED_FROZEN_WITHHELD_OVERLAP_SHA256
            ):
                errors.append(
                    "raw lifecycle frozen/withheld overlap inventory drifted from "
                    f"the exact {EXPECTED_FROZEN_WITHHELD_OVERLAP_COUNT}-artifact "
                    "count/hash baseline"
                )
        if withheld_alias_contract != public["withheld_alias_contract"]:
            errors.append(
                f"withheld public-alias contract drifted: stored={withheld_alias_contract}, "
                f"actual={public['withheld_alias_contract']}"
            )
        stored_sitemap_contract = {
            key: sitemap_state.get(key) for key in public["sitemap_contract"]
        }
        if stored_sitemap_contract != public["sitemap_contract"]:
            errors.append(
                f"public sitemap contract drifted: stored={stored_sitemap_contract}, "
                f"actual={public['sitemap_contract']}"
            )
        stored_membership_hashes = {
            "universe_sha256": membership_state.get("universe_sha256"),
            "category_sha256": category_hash_state,
        }
        if stored_membership_hashes != public["membership_hashes"]:
            errors.append(
                "public lifecycle membership hashes drifted: "
                f"stored={stored_membership_hashes}, actual={public['membership_hashes']}"
            )
        if public_state.get("counts") != public["counts"]:
            errors.append(
                f"stale public lifecycle counts: stored={public_state.get('counts')}, "
                f"actual={public['counts']}"
            )
        if public_state.get("unclassified") != public["unclassified"]:
            errors.append(
                "public unclassified list drifted: "
                f"stored={public_state.get('unclassified')}, actual={public['unclassified']}"
            )
        if public["counts"]["unclassified"] != 0 or public["unclassified"]:
            errors.append(
                "public lifecycle closure requires zero unclassified artifacts; "
                f"found {public['counts']['unclassified']}"
            )

    claims = computed.get("claim_disposition")
    current_state = require_mapping(
        claim_state.get("current_scope"), "claim_disposition.current_scope", errors
    )
    grave_state = require_mapping(
        claim_state.get("grave_scope"), "claim_disposition.grave_scope", errors
    )
    exact_keys(
        current_state,
        {
            "rows", "live_status_rows", "terminal_status_rows", "status_counts",
            "id_status", "direct_contact", "merged_contact", "contact_routed",
            "internal_narrowed", "internal_terminal",
        },
        "claim_disposition.current_scope",
        errors,
    )
    exact_keys(
        grave_state,
        {
            "rows", "terminal_status_rows", "narrowed_status_rows", "status_counts",
            "id_status", "merged_to_owner", "internal_terminal",
            "active_parent_investigations",
        },
        "claim_disposition.grave_scope",
        errors,
    )
    claim_lists = {
        key: require_list(current_state.get(key), f"current_scope.{key}", errors)
        for key in (
            "direct_contact", "merged_contact", "contact_routed",
            "internal_narrowed", "internal_terminal",
        )
    }
    grave_lists = {
        key: require_list(grave_state.get(key), f"grave_scope.{key}", errors)
        for key in ("merged_to_owner", "internal_terminal")
    }
    for label, values in {**claim_lists, **{f"grave_{k}": v for k, v in grave_lists.items()}}.items():
        if len(values) != len(set(values)):
            errors.append(f"{label} contains duplicate ids")
    current_classes = (
        set(claim_lists["direct_contact"])
        | set(claim_lists["merged_contact"])
        | set(claim_lists["internal_narrowed"])
        | set(claim_lists["internal_terminal"])
    )
    classified_current_count = sum(
        len(claim_lists[key])
        for key in ("direct_contact", "merged_contact", "internal_narrowed", "internal_terminal")
    )
    if (
        len(current_classes) != EXPECTED_CURRENT_ROWS
        or classified_current_count != EXPECTED_CURRENT_ROWS
    ):
        errors.append("current claim disposition must cover exactly 28 distinct W/RQ rows")
    if claim_lists["contact_routed"] != claim_lists["direct_contact"] + claim_lists["merged_contact"]:
        errors.append("contact_routed must be the ordered direct+merged projection")
    if set(grave_lists["merged_to_owner"]) & set(grave_lists["internal_terminal"]):
        errors.append("grave parent has two disposition classes")
    if (
        len(
            set(grave_lists["merged_to_owner"])
            | set(grave_lists["internal_terminal"])
        )
        != EXPECTED_GRAVE_ROWS
    ):
        errors.append("grave disposition must cover exactly 22 distinct parent rows")
    if grave_state.get("active_parent_investigations") != 0:
        errors.append("grave parent forms must not remain separate active investigations")
    ambiguous = require_list(claim_state.get("ambiguous_rows"), "claim_disposition.ambiguous_rows", errors)
    if ambiguous:
        errors.append("claim disposition requires zero ambiguous rows")

    if claims is not None:
        if claims.get("lifecycle_rows_total") != EXPECTED_LIFECYCLE_ROWS:
            errors.append(
                "claim disposition must retain exactly 50 open/investigation/grave "
                "lifecycle rows"
            )
        scalar_keys = (
            "lifecycle_rows_total", "lifecycle_rows_sha256", "claim_status_contract_sha256",
            "unique_external_contracts",
            "external_contract_ids", "ambiguous_rows",
        )
        for key in scalar_keys:
            if claim_state.get(key) != claims[key]:
                errors.append(
                    f"stale claim disposition {key}: stored={claim_state.get(key)}, actual={claims[key]}"
                )
        stored_current_projection = {
            "rows": current_state.get("rows"),
            "live_status_rows": current_state.get("live_status_rows"),
            "terminal_status_rows": current_state.get("terminal_status_rows"),
            "status_counts": current_state.get("status_counts"),
            "statuses": current_state.get("id_status"),
            "direct_contact": current_state.get("direct_contact"),
            "merged_contact": current_state.get("merged_contact"),
            "contact_routed": current_state.get("contact_routed"),
            "internal_narrowed": current_state.get("internal_narrowed"),
            "internal_terminal": current_state.get("internal_terminal"),
        }
        if stored_current_projection != claims["current_scope"]:
            errors.append("current W/RQ disposition projection drifted from CLAIM_STATUS")
        stored_grave_projection = {
            "rows": grave_state.get("rows"),
            "terminal_status_rows": grave_state.get("terminal_status_rows"),
            "narrowed_status_rows": grave_state.get("narrowed_status_rows"),
            "status_counts": grave_state.get("status_counts"),
            "statuses": grave_state.get("id_status"),
            "merged_to_owner": grave_state.get("merged_to_owner"),
            "internal_terminal": grave_state.get("internal_terminal"),
            "active_parent_investigations": grave_state.get("active_parent_investigations"),
        }
        if stored_grave_projection != claims["grave_scope"]:
            errors.append("grave-parent disposition projection drifted from CLAIM_STATUS")

    profile_debts = computed.get("owner_held")
    debt_rows = require_list(owner_state.get("debts"), "owner_held.debts", errors)
    debt_ids = [row.get("id") for row in debt_rows if isinstance(row, dict)]
    if len(debt_rows) != 2 or set(debt_ids) != EXPECTED_DEBTS:
        errors.append("owner_held must contain exactly the two coherence-profile debts")
    if len(debt_ids) != len(set(debt_ids)):
        errors.append("owner_held contains duplicate debt ids")
    if profile_debts is not None and set(debt_ids) != profile_debts:
        errors.append(
            f"owner-held debts drifted from coherence profile: state={sorted(debt_ids)}, "
            f"actual={sorted(profile_debts)}"
        )
    owner_receipt_path = repo_file(
        root, owner_state.get("receipt_ref"), "owner_held.receipt_ref content", errors
    )
    if owner_receipt_path is not None:
        owner_receipt_text = owner_receipt_path.read_text(encoding="utf-8", errors="ignore")
        unnamed = sorted(EXPECTED_DEBTS - {item for item in EXPECTED_DEBTS if item in owner_receipt_text})
        if unnamed:
            errors.append(
                "owner-held baseline receipt does not name exact debt ids: "
                + ", ".join(unnamed)
            )
    for index, debt in enumerate(debt_rows):
        debt = require_mapping(debt, f"owner_held.debts[{index}]", errors)
        exact_keys(
            debt,
            {"id", "owner", "question", "close_when", "evidence", "receipt_ref"},
            f"owner_held.debts[{index}]",
            errors,
        )
        for key in ("owner", "question", "close_when"):
            if not isinstance(debt.get(key), str) or not debt.get(key, "").strip():
                errors.append(f"owner_held.debts[{index}].{key} must be non-empty")
        receipt_ref(root, debt.get("receipt_ref"), f"owner_held.debts[{index}].receipt_ref", errors)
        if debt.get("receipt_ref") != owner_state.get("receipt_ref"):
            errors.append(
                f"owner_held.debts[{index}] must share the owner-held baseline receipt"
            )
        evidence = require_list(
            debt.get("evidence"), f"owner_held.debts[{index}].evidence", errors
        )
        for evidence_index, path in enumerate(evidence):
            repo_file(
                root,
                path,
                f"owner_held.debts[{index}].evidence[{evidence_index}]",
                errors,
            )
        evidence_set = {item for item in evidence if isinstance(item, str)}
        if len(evidence) != len(evidence_set):
            errors.append(f"owner_held.debts[{index}].evidence contains duplicate paths")
        if debt.get("id") == "OWNER_GATE_HELD_PUBLIC_DOCS":
            errors.extend(public_doc_owner_debt_errors(root, evidence_set))
        if debt.get("id") == "OWNER_GATE_OPEN_TOPOLOGY":
            if debt.get("question") != EXPECTED_TOPOLOGY_DEBT_QUESTION:
                errors.append(
                    "OWNER_GATE_OPEN_TOPOLOGY question must describe the exact "
                    "grandfathered held violation"
                )
            if debt.get("close_when") != EXPECTED_TOPOLOGY_DEBT_CLOSE_WHEN:
                errors.append(
                    "OWNER_GATE_OPEN_TOPOLOGY close_when must require a dated "
                    "topology amendment or complete custody route"
                )
            errors.extend(topology_owner_debt_errors(root, evidence_set))

    world = computed.get("world_contact")
    expected_world = {
        "state": "OPEN",
        "accepted_evidence_records": 0,
        "open_requirements": list(EXPECTED_WORLD_REQUIREMENTS),
    }
    stored_world = {key: world_state.get(key) for key in expected_world}
    if stored_world != expected_world:
        errors.append(
            f"world-contact baseline must remain OPEN/0/2: stored={stored_world}"
        )
    if world is not None and world != expected_world:
        errors.append(
            f"world-contact machine owner drifted from OPEN/0/2: actual={world}"
        )

    if errors:
        raise ContractError(errors)
    return {
        "receipt_namespace": receipts,
        "public_lifecycle": public,
        "claim_disposition": {
            "lifecycle_rows": claims["lifecycle_rows_total"],
            "current_rows": claims["current_scope"]["rows"],
            "direct_contact": len(claims["current_scope"]["direct_contact"]),
            "merged_contact": len(claims["current_scope"]["merged_contact"]),
            "internal": len(claims["current_scope"]["internal_narrowed"])
            + len(claims["current_scope"]["internal_terminal"]),
            "grave_rows": claims["grave_scope"]["rows"],
            "active_parent_investigations": claims["grave_scope"]["active_parent_investigations"],
            "external_contracts": claims["unique_external_contracts"],
            "ambiguous": len(claims["ambiguous_rows"]),
        },
        "owner_held": len(debt_rows),
        "world_contact": world,
    }


def check(root: Path = ROOT) -> dict[str, Any]:
    errors: list[str] = []
    state_path = repo_file(
        root, STATE_PATH.as_posix(), "contact-limited state owner", errors
    )
    if state_path is None:
        raise ContractError(errors)
    return validate_state(load_json(state_path), root)


def main() -> int:
    try:
        report = check()
    except ContractError as exc:
        print("CONTACT-LIMITED RATCHET: FAIL")
        for error in exc.errors:
            print(f"- {error}")
        return 1

    receipts = report["receipt_namespace"]
    public = report["public_lifecycle"]["counts"]
    claims = report["claim_disposition"]
    world = report["world_contact"]
    print(
        "CONTACT-LIMITED RATCHET: PASS-WITH-DEBT "
        f"(receipts={receipts['target_files']}citable/"
        f"{receipts['prefixed_markdown_including_00_convention']}convention/"
        f"{receipts['unique_prefixes']}prefixes/{receipts['reused_prefixes']}reused/"
        f"{receipts['legacy_heuristic_dangerous_prefixes']}legacy/"
        f"{receipts['bare_unsafe_reused_prefixes']}unsafe/"
        f"{receipts['dangling_citations']}dangling; public={public['total']} "
        f"[{public['current']}/{public['provisional']}/{public['frozen']}/"
        f"{public['withheld']}/{public['infrastructure']}/{public['unclassified']}]; "
        f"alias-collisions={len(report['public_lifecycle']['alias_collisions'])}; "
        f"raw-overlaps={sum(len(row['artifacts']) for row in report['public_lifecycle']['raw_overlaps'])}; "
        f"matcher-drift={len(report['public_lifecycle']['matcher_conformance']['mismatches'])}; "
        f"claims={claims['lifecycle_rows']} lifecycle "
        f"[{claims['current_rows']} W/RQ: {claims['direct_contact']} direct-contact/"
        f"{claims['merged_contact']} merged-contact/{claims['internal']} internal; "
        f"{claims['grave_rows']} grave parents/{claims['active_parent_investigations']} active; "
        f"{claims['external_contracts']} contracts/{claims['ambiguous']} ambiguous]; "
        f"owner-held={report['owner_held']}; "
        f"world={world['state']}/{world['accepted_evidence_records']}/"
        f"{len(world['open_requirements'])})"
    )
    print(
        "  scope: reproducible internal inventory only; owner-held debts and independent "
        "world contact remain open."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

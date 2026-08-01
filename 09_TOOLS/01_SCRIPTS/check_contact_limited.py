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
import re
import subprocess
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = Path("00_META/CONTACT_LIMITED_STATE.json")
RECEIPT_INDEX = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_RECEIPT_DISAMBIGUATION_INDEX.json"
)
RECEIPT_CHECKER = Path("09_TOOLS/01_SCRIPTS/check_receipt_citations.py")
CLAIM_SOURCE = Path("00_META/claim_status/CLAIM_STATUS.yaml")
COHERENCE_SOURCE = Path("09_TOOLS/01_SCRIPTS/coherence_profile.json")
PUBLIC_DIR = Path("12_PUBLIC_SITE")
PUBLIC_PARITY = PUBLIC_DIR / "public_semantic_parity.json"
WITHHELD_REGISTRY = PUBLIC_DIR / "withheld-routes.json"
VERCEL_CONFIG = PUBLIC_DIR / "vercel.json"
VERCEL_IGNORE = PUBLIC_DIR / ".vercelignore"

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


def _load_receipt_citation_policy():
    path = Path(__file__).with_name("check_receipt_citations.py")
    spec = importlib.util.spec_from_file_location("receipt_citation_policy_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load receipt citation policy owner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_RECEIPT_CITATION_POLICY = _load_receipt_citation_policy()
CITATION = _RECEIPT_CITATION_POLICY.CITATION
citation_is_negated = _RECEIPT_CITATION_POLICY.citation_is_negated

EXPECTED_CONTACT = (
    "W2",
    "W4",
    "W5",
    "W6",
    "W7a",
    "W7b",
    "W7c",
    "W7d",
    "W7e",
    "W8",
    "W9",
    "W10",
    "W12",
)
EXPECTED_INTERNAL = ("W0-CROWN", "W1", "W3", "W11")
EXPECTED_RQ = tuple(f"RQ-{number:02d}" for number in range(1, 10))
EXPECTED_DEBTS = {
    "OWNER_GATE_HELD_PUBLIC_DOCS",
    "OWNER_GATE_OPEN_TOPOLOGY",
}
EXPECTED_WORLD_REQUIREMENTS = (
    "Independent observations with discriminating outcomes",
    "Independent replication or external review filed as outcome custody",
)
W3_RECEIPT = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/184_THE_PRODUCT_CONJECTURE_RULED_2026_07_30.md"
)
PUBLIC_DOC_EVIDENCE = {
    "12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md",
    "12_PUBLIC_SITE/_PLANS/specs/2026-06-05-numbered-doctrine-spine-design.md",
}
TOPOLOGY_EVIDENCE = {
    "00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md",
    "08_FRAMEWORK_SUPPORT/00_META/README.md",
}
EXPECTED_PRECEDENCE = (
    "withheld",
    "current",
    "provisional",
    "infrastructure",
    "frozen",
    "unclassified",
)
EXPECTED_ALIAS_COLLISIONS = [
    {
        "route": "/titans/",
        "artifacts": ["titans.html", "titans/index.html"],
        "shared_raw_lifecycle": "frozen",
    }
]
EXPECTED_RAW_OVERLAPS = [
    {
        "classes": ["frozen", "infrastructure"],
        "artifacts": ["offline/index.html"],
    },
    {
        "classes": ["frozen", "withheld"],
        "artifacts": [
            "burrisphere/index.html",
            "canon/the-complete-ontology-of-reality/index.html",
            "dasein/index.html",
            "operators/mf-283-the-orthogonality-theorem-v2/index.html",
            "operators/mf-285-dreams-are-unanchored-d5/index.html",
            "operators/mf-296-gravity-is-time/index.html",
            "operators/mf-298-dark-matter-is-mutual-information/index.html",
        ],
    },
]
EXPECTED_WORLD_REQUIRED_FIELDS = (
    "independent_party_identity",
    "independence_basis",
    "discriminating_protocol",
    "outcome",
    "verbatim_custody",
    "provenance",
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


def repo_file(root: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    """Require an existing repo-relative regular file that cannot escape root."""
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty repo-relative path")
        return None
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{label} must not be absolute or contain '..': {value!r}")
        return None
    target = root / rel
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} escapes the repository: {value!r}")
        return None
    if not target.is_file():
        errors.append(f"{label} does not exist as a file: {value}")
        return None
    return target


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
        base = root / lane
        if not base.is_dir():
            raise ContractError(f"missing receipt lane during marker custody scan: {lane}")
        for path in base.rglob("*.md"):
            try:
                if STATE_DIGEST_MARKER in path.read_bytes():
                    working_markers.add(path.relative_to(root))
            except OSError as exc:
                raise ContractError(f"cannot read snapshot-marker candidate {path}: {exc}") from exc

    errors: list[str] = []
    for rel in sorted(working_markers | head_markers | parent_markers):
        working_path = root / rel
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
        base = root / lane
        if not base.is_dir():
            raise ContractError(f"missing receipt lane: {lane}")
        for path in base.rglob("*.md"):
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
        for path in (root / lane).rglob("*.md"):
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

    index = load_json(root / RECEIPT_INDEX)
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
    if pattern.endswith("/"):
        prefix = pattern.strip("/")
        if "/" in prefix:
            return rel_path == prefix or rel_path.startswith(prefix + "/")
        # Gitignore's unanchored `name/` form matches that directory component
        # at every depth.  The public predeploy helper currently misses this
        # for compass/_archive; this ratchet intentionally exposes that drift.
        return prefix in Path(rel_path).parts[:-1]
    anchored = pattern.startswith("/")
    pattern = pattern.lstrip("/")
    if "[" in pattern or "]" in pattern:
        raise ContractError(
            f"unsupported character-class pattern in .vercelignore: {pattern!r}"
        )

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
    if "/" not in pattern and not anchored:
        return re.fullmatch(expression, Path(rel_path).name) is not None
    return re.fullmatch(expression, rel_path) is not None


def _is_vercel_ignored(rel_path: str, patterns: list[str]) -> bool:
    ignored = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw = pattern[1:] if negated else pattern
        if _vercelignore_matches(rel_path, raw):
            ignored = not negated
    return ignored


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


def _artifact_delivery_aliases(artifact: str) -> set[str]:
    """Clean, trailing-slash, and physical aliases (two for the root index)."""
    canonical = _clean_route(artifact)
    clean = canonical.rstrip("/") or "/"
    physical = "/" + artifact.lstrip("/")
    return {clean, canonical, physical}


def _expected_withheld_aliases(artifact: str) -> set[str]:
    """The exact three delivery forms required for a withheld artifact."""
    expected = _artifact_delivery_aliases(artifact)
    if len(expected) != 3:
        raise ContractError(
            f"withheld artifact {artifact} does not yield three distinct delivery aliases"
        )
    return expected


def compute_public_lifecycle(root: Path) -> dict[str, Any]:
    site = root / PUBLIC_DIR
    parity = load_json(root / PUBLIC_PARITY)
    withheld_registry = load_json(root / WITHHELD_REGISTRY)
    vercel = load_json(root / VERCEL_CONFIG)
    patterns = _load_vercelignore(root / VERCEL_IGNORE)

    if not site.is_dir():
        raise ContractError(f"missing public site: {PUBLIC_DIR}")
    artifacts = require_list(withheld_registry.get("artifacts"), "withheld artifacts", [])
    withheld_artifacts = _validated_withheld_artifacts(site, artifacts)

    present = {path.relative_to(site).as_posix() for path in site.rglob("*.html")}
    ignored = {rel for rel in present if _is_vercel_ignored(rel, patterns)}
    deployable = present - ignored
    nested_archive = "compass/_archive/index_2026_07_12_pre_restructure.html"
    if nested_archive not in ignored:
        raise ContractError(
            "gitignore-style _archive/ semantics no longer exclude the nested compass artifact"
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
        expected_aliases = _expected_withheld_aliases(artifact)
        if len(aliases) != len(set(aliases)):
            raise ContractError(f"withheld artifact {artifact} repeats a public alias")
        if set(aliases) != expected_aliases:
            raise ContractError(
                f"withheld artifact {artifact} aliases drifted: "
                f"stored={sorted(aliases)}, expected={sorted(expected_aliases)}"
            )
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
            if canonical != expected_alias:
                raise ContractError(
                    f"withheld alias {alias} canonicalizes to {canonical}, not {expected_alias} "
                    f"for {artifact}"
                )
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
        aliases = _artifact_delivery_aliases(artifact)
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
        "membership_hashes": membership_hashes,
        "counts": counts,
        "unclassified": sorted(categories["unclassified"]),
    }


def compute_claim_disposition(root: Path) -> dict[str, Any]:
    source = load_json(root / CLAIM_SOURCE)
    rows = require_list(source.get("open"), "claim-status open rows", [])
    if any(not isinstance(row, dict) for row in rows):
        raise ContractError("claim-status open rows must be objects")
    ids = [str(row.get("id")) for row in rows]
    if len(set(ids)) != len(ids) or "None" in ids:
        raise ContractError("claim-status open rows have duplicate or missing ids")
    statuses = {str(row["id"]): str(row.get("status")) for row in rows}

    reopened = require_list(source.get("reopened"), "claim-status reopened rows", [])
    if any(not isinstance(row, dict) for row in reopened):
        raise ContractError("claim-status reopened rows must be objects")
    reopened_ids = [str(row.get("id")) for row in reopened]
    if len(set(reopened_ids)) != len(reopened_ids) or "None" in reopened_ids:
        raise ContractError("claim-status reopened rows have duplicate or missing ids")
    required_rq_fields = {"parent", "question", "discriminator", "kill", "survivor"}
    all_source_ids = {
        str(row.get("id"))
        for value in source.values()
        if isinstance(value, list)
        for row in value
        if isinstance(row, dict) and row.get("id") is not None
    }
    for row in reopened:
        missing = required_rq_fields - set(row)
        if missing:
            raise ContractError(
                f"{row.get('id')} lost reopened-question fields: {', '.join(sorted(missing))}"
            )
        if row.get("parent") not in all_source_ids:
            raise ContractError(
                f"{row.get('id')} names absent source parent {row.get('parent')!r}"
            )

    df04 = None
    for value in source.values():
        if not isinstance(value, list):
            continue
        for row in value:
            if isinstance(row, dict) and row.get("id") == "DF-04":
                df04 = row
                break
    if df04 is None:
        raise ContractError("claim-status source lost the DF-04 owner-reopening row")
    live_statuses = set(require_list(source.get("live_statuses"), "live_statuses", []))
    live_w_rows = sum(status in live_statuses for status in statuses.values())
    return {
        "w_scope": {
            "rows": len(rows),
            "live_status_rows": live_w_rows,
            "terminal_status_rows": len(rows) - live_w_rows,
            "status_counts": dict(Counter(statuses.values())),
            "ids": ids,
            "statuses": statuses,
        },
        "reopened_scope": {"rows": len(reopened), "ids": reopened_ids},
        "owner_rows_total": len(rows) + len(reopened),
        "live_investigation_rows": live_w_rows + len(reopened),
        "df04": df04,
    }


def compute_owner_debts(root: Path) -> set[str]:
    profile = load_json(root / COHERENCE_SOURCE)
    axes = require_mapping(profile.get("axes"), "coherence axes", [])
    routing = require_mapping(axes.get("routing"), "coherence routing axis", [])
    debt_ids = require_list(routing.get("debt_ids"), "routing debt_ids", [])
    if any(not isinstance(item, str) for item in debt_ids) or len(set(debt_ids)) != len(
        debt_ids
    ):
        raise ContractError("coherence routing debt_ids must be unique strings")
    return set(debt_ids)


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
    if "All 97 reused prefixes remain unsafe" not in bare_boundary or "proves no target" not in bare_boundary:
        errors.append("bare_numeric_boundary must not present the legacy 91 heuristic as safe")
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
    }
    if set(item for item in public_sources if isinstance(item, str)) != expected_public_sources:
        errors.append("public_lifecycle.sources must name all four machine owners exactly")
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
            "known_matcher_drift",
        },
        "deploy_ignore_contract",
        errors,
    )
    if "at any depth" not in str(ignore_state.get("semantics", "")):
        errors.append("deploy-ignore semantics must pin unanchored directory matching at any depth")
    matcher_drift = require_mapping(
        ignore_state.get("known_matcher_drift"), "known_matcher_drift", errors
    )
    exact_keys(
        matcher_drift,
        {"state", "pattern", "excluded_artifact", "evidence"},
        "known_matcher_drift",
        errors,
    )
    if matcher_drift.get("state") != "OPEN_INTERNAL_DRIFT" or matcher_drift.get("pattern") != "_archive/":
        errors.append("known matcher drift must remain open on the _archive/ rule")
    if matcher_drift.get("excluded_artifact") != "compass/_archive/index_2026_07_12_pre_restructure.html":
        errors.append("known matcher drift lost the nested compass archive artifact")
    for index, evidence in enumerate(
        require_list(matcher_drift.get("evidence"), "known_matcher_drift.evidence", errors)
    ):
        repo_file(root, evidence, f"known_matcher_drift.evidence[{index}]", errors)

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
            "owner_rows_total",
            "live_investigation_rows",
            "w_scope",
            "reopened_scope",
            "w3_guard",
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
        if overlap_contract != EXPECTED_RAW_OVERLAPS:
            errors.append("raw lifecycle overlap allowlist changed without a new ratchet contract")
        if withheld_alias_contract != public["withheld_alias_contract"]:
            errors.append(
                f"withheld public-alias contract drifted: stored={withheld_alias_contract}, "
                f"actual={public['withheld_alias_contract']}"
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

    claims = computed.get("claim_disposition")
    w_state = require_mapping(claim_state.get("w_scope"), "claim_disposition.w_scope", errors)
    exact_keys(
        w_state,
        {
            "rows",
            "live_status_rows",
            "terminal_status_rows",
            "status_counts",
            "id_status",
            "contact_gated",
            "internal_disposition",
        },
        "claim_disposition.w_scope",
        errors,
    )
    reopened_state = require_mapping(
        claim_state.get("reopened_scope"), "claim_disposition.reopened_scope", errors
    )
    exact_keys(
        reopened_state,
        {"rows", "disposition", "ids", "required_source_fields"},
        "claim_disposition.reopened_scope",
        errors,
    )
    contact = require_list(w_state.get("contact_gated"), "w_scope.contact_gated", errors)
    internal = require_list(
        w_state.get("internal_disposition"), "w_scope.internal_disposition", errors
    )
    if tuple(contact) != EXPECTED_CONTACT:
        errors.append("contact_gated mapping changed without a new ratchet contract")
    if tuple(internal) != EXPECTED_INTERNAL:
        errors.append("internal_disposition mapping changed without a new ratchet contract")
    if len(set(contact)) != len(contact) or len(set(internal)) != len(internal):
        errors.append("claim lifecycle lists contain duplicate ids")
    overlap = set(contact) & set(internal)
    if overlap:
        errors.append("claims have two lifecycle classes: " + ", ".join(sorted(overlap)))
    rq_ids = require_list(reopened_state.get("ids"), "reopened_scope.ids", errors)
    if tuple(rq_ids) != EXPECTED_RQ:
        errors.append("reopened RQ inventory changed without a new ratchet contract")
    if reopened_state.get("disposition") != "UNADJUDICATED_REOPENED_RESEARCH_QUESTIONS":
        errors.append("reopened RQ rows must remain explicitly unadjudicated")
    if tuple(
        require_list(
            reopened_state.get("required_source_fields"),
            "reopened_scope.required_source_fields",
            errors,
        )
    ) != ("parent", "question", "discriminator", "kill", "survivor"):
        errors.append("reopened RQ source-field contract drifted")
    if claims is not None:
        computed_w = claims["w_scope"]
        for key in ("rows", "live_status_rows", "terminal_status_rows", "status_counts"):
            if w_state.get(key) != computed_w[key]:
                errors.append(
                    f"stale W-scope {key}: stored={w_state.get(key)}, actual={computed_w[key]}"
                )
        if w_state.get("id_status") != computed_w["statuses"]:
            errors.append(
                f"per-ID W status map drifted: stored={w_state.get('id_status')}, "
                f"actual={computed_w['statuses']}"
            )
        if set(contact) | set(internal) != set(computed_w["ids"]):
            errors.append("W disposition does not cover every and only W-scope id")
        computed_rq = claims["reopened_scope"]
        if reopened_state.get("rows") != computed_rq["rows"] or rq_ids != computed_rq["ids"]:
            errors.append(
                f"reopened RQ inventory drifted: stored={rq_ids}, actual={computed_rq['ids']}"
            )
        if claim_state.get("owner_rows_total") != claims["owner_rows_total"]:
            errors.append(
                f"stale claim owner-row total: stored={claim_state.get('owner_rows_total')}, "
                f"actual={claims['owner_rows_total']}"
            )
        if claim_state.get("live_investigation_rows") != claims["live_investigation_rows"]:
            errors.append(
                "stale live-investigation count: "
                f"stored={claim_state.get('live_investigation_rows')}, "
                f"actual={claims['live_investigation_rows']}"
            )
        if computed_w["statuses"].get("W3") != "OPEN-EMPIRICAL":
            errors.append("W3 machine-owner row must not be silently resolved")
        df04 = claims["df04"]
        repair_path = str(df04.get("repair_path", ""))
        if df04.get("successor") != "W3" or "cannot be prosecuted" not in repair_path:
            errors.append("DF-04 no longer carries the W3 source-reconciliation conflict")

    w3 = require_mapping(claim_state.get("w3_guard"), "w3_guard", errors)
    exact_keys(
        w3,
        {
            "id",
            "state",
            "requires_source_reconciliation",
            "receipt_ref",
            "evidence",
            "does_not_claim",
        },
        "w3_guard",
        errors,
    )
    if w3.get("id") != "W3" or w3.get("state") != "INTERNAL_DISPOSITION_PENDING_SOURCE_RECONCILIATION":
        errors.append("w3_guard lost its pending internal-disposition state")
    if w3.get("requires_source_reconciliation") is not True:
        errors.append("w3_guard must require source reconciliation")
    if w3.get("receipt_ref") != str(W3_RECEIPT):
        errors.append("w3_guard must retain the Receipt 184 ruling path")
    receipt_ref(root, w3.get("receipt_ref"), "w3_guard.receipt_ref", errors)
    w3_evidence = require_list(w3.get("evidence"), "w3_guard.evidence", errors)
    for index, evidence in enumerate(w3_evidence):
        repo_file(root, evidence, f"w3_guard.evidence[{index}]", errors)
    does_not_claim = str(w3.get("does_not_claim", ""))
    if "does not close" not in does_not_claim or "OPEN-EMPIRICAL" not in does_not_claim:
        errors.append("w3_guard must state that routing neither closes W3 nor changes its status")

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
        if debt.get("id") == "OWNER_GATE_HELD_PUBLIC_DOCS":
            if not PUBLIC_DOC_EVIDENCE <= evidence_set:
                errors.append("public-doc owner debt lost one of its duplicate evidence paths")
            else:
                left, right = sorted(PUBLIC_DOC_EVIDENCE)
                if (root / left).read_bytes() != (root / right).read_bytes():
                    errors.append("public-doc debt evidence is no longer byte-identical")
        if debt.get("id") == "OWNER_GATE_OPEN_TOPOLOGY" and not TOPOLOGY_EVIDENCE <= evidence_set:
            errors.append("topology owner debt lost one of its conflicting evidence paths")

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
            "w_rows": claims["w_scope"]["rows"],
            "contact_gated": len(contact),
            "internal_disposition": len(internal),
            "reopened_rows": claims["reopened_scope"]["rows"],
            "owner_rows_total": claims["owner_rows_total"],
            "live_investigation_rows": claims["live_investigation_rows"],
        },
        "owner_held": len(debt_rows),
        "world_contact": world,
    }


def check(root: Path = ROOT) -> dict[str, Any]:
    return validate_state(load_json(root / STATE_PATH), root)


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
        "matcher-drift=1; "
        f"claims=W{claims['w_rows']} [{claims['contact_gated']} contact/"
        f"{claims['internal_disposition']} internal] + RQ{claims['reopened_rows']} unadjudicated "
        f"[{claims['owner_rows_total']} owner rows/{claims['live_investigation_rows']} live]; "
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

#!/usr/bin/env python3
"""Build deterministic Emergentism file and folder registers from the Git index.

The index, rather than the mutable worktree, is the source of truth. This makes
the result reproducible from a clean checkout and prevents unrelated unstaged
work from entering a signing surface.

The file register represents itself with sha256=SELF. Its byte count is solved
after rendering. The signing manifest must likewise use SELF for generated
register rows, which avoids an otherwise impossible cryptographic cycle.

The inbound_references field counts distinct indexed source files that contain
a resolvable Markdown link, HTML href/src, or declared target/successor/absorber.
It is a deterministic structured-link census, not a claim that every prose
mention has been semantically interpreted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


FILE_REGISTER = (
    "00_META/05_MAGNUM_OPUS_FILE_DISPOSITION_MANIFEST_"
    "PENDING_SIGNATURE_2026_07_19.csv"
)
FOLDER_REGISTER = (
    "00_META/06_MAGNUM_OPUS_FOLDER_DISPOSITION_MANIFEST_"
    "PENDING_SIGNATURE_2026_07_19.csv"
)
SIGNING_MANIFEST = (
    "00_META/07_RECEIPT_139_SIGNING_MANIFEST_PENDING_SIGNATURE_2026_07_19.csv"
)

FILE_FIELDS = [
    "path",
    "sha256",
    "bytes",
    "owner_lane",
    "artifact_class",
    "authority_status",
    "evidence_tier",
    "k_relation",
    "public_projection",
    "disposition",
    "destination",
    "absorber",
    "inbound_references",
    "gate",
    "review_state",
]

FOLDER_FIELDS = [
    "path",
    "type",
    "nearest_front_door",
    "front_door_requirement",
    "owns",
    "must_not_own",
    "status",
    "tracked_file_count",
    "disposition",
    "gate",
    "review_state",
]

ROUTE_NAMES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "ROSETTA.md",
    "VMOSK_A.md",
    "AGENT_README.md",
    "00_INDEX.md",
    "INDEX.md",
    "TOMBSTONE.md",
    "ARCHIVE_SURFACES_INDEX.md",
}
FRONT_DOOR_PRIORITY = [
    "README.md",
    "00_INDEX.md",
    "INDEX.md",
    "AGENTS.md",
    "CLAUDE.md",
    "ROSETTA.md",
    "VMOSK_A.md",
    "TOMBSTONE.md",
    "ARCHIVE_SURFACES_INDEX.md",
]
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".csv",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".sh",
}
CODE_SUFFIXES = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".sh",
    ".rb",
    ".rs",
    ".go",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
}
DATA_SUFFIXES = {".csv", ".json", ".yaml", ".yml", ".toml", ".xml"}
ASSET_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    ".pdf",
    ".woff",
    ".woff2",
    ".ttf",
    ".mp3",
    ".mp4",
}

REQUIRED_FRONT_DOORS = {
    ".",
    "00_CONTROL/10_OPEN_CANON_FOUNDATION",
    "00_CONTROL/PRIMETIME_AUDIT",
    "00_META/worldview_consolidation_2026_06_12",
    "06_ONTOLOGY/ruminations",
    "10_SEED/01_THE_SEED_LADDER",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
}

DISPUTED_PATHS = {
    "00_META/00_K5_THE_REFUSALS.md",
    "02_EPISTEMOLOGY/03_MEMETICS/00_ROSETTA_VALIDATION.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "08_FRAMEWORK_SUPPORT/05_SYNTHESIS/00_THE_DISTILLED_DOCTRINE.md",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/139_THE_SIGNING_SITTING_SIGNED_2026_07_19.md",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/141_SOVEREIGN_EXECUTION_2026_07_19.md",
}

REFERENCE_EXCLUDED = {FILE_REGISTER, FOLDER_REGISTER}
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"'#]+)["']""", re.IGNORECASE)
TARGET_RE = re.compile(
    r"""(?:canonical_target|target|successor|absorber)\s*:\s*["']?([^"'\s]+)""",
    re.IGNORECASE,
)
EVIDENCE_RE = re.compile(
    r"""^evidence_tier:\s*(?:"([^"]*)"|'([^']*)'|([^\n]+))""",
    re.MULTILINE,
)
STATUS_RE = re.compile(
    r"""^status:\s*(?:"([^"]*)"|'([^']*)'|([^\n]+))""",
    re.MULTILINE,
)


@dataclass(frozen=True)
class IndexEntry:
    mode: str
    oid: str
    path: str


def run_git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout


def find_repo(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).resolve()
    else:
        candidate = Path(__file__).resolve().parents[2]
    root = Path(
        run_git(candidate, "rev-parse", "--show-toplevel")
        .decode("utf-8")
        .strip()
    ).resolve()
    if root != candidate:
        raise RuntimeError(f"expected repository root {candidate}, got {root}")
    return root


def read_index(repo: Path) -> list[IndexEntry]:
    raw = run_git(repo, "ls-files", "-s", "-z")
    entries: list[IndexEntry] = []
    seen: set[str] = set()
    for item in raw.split(b"\0"):
        if not item:
            continue
        meta, encoded_path = item.split(b"\t", 1)
        mode, oid, stage = meta.decode("ascii").split()
        if stage != "0":
            raise RuntimeError(
                f"unmerged index entry at {encoded_path.decode('utf-8', 'replace')}"
            )
        path = encoded_path.decode("utf-8", "surrogateescape")
        if path in seen:
            raise RuntimeError(f"duplicate tracked path: {path}")
        seen.add(path)
        entries.append(IndexEntry(mode=mode, oid=oid, path=path))
    entries.sort(key=lambda item: item.path)
    return entries


def load_blob_metadata(
    repo: Path, entries: list[IndexEntry]
) -> tuple[dict[str, tuple[int, str]], dict[str, str]]:
    paths_by_oid: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        paths_by_oid[entry.oid].append(entry.path)

    metadata: dict[str, tuple[int, str]] = {}
    text_by_oid: dict[str, str] = {}
    process = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None

    try:
        for oid in sorted(paths_by_oid):
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline()
            if not header:
                raise RuntimeError(f"missing cat-file response for {oid}")
            parts = header.decode("ascii", "replace").strip().split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header: {header!r}")
            size = int(parts[2])
            data = process.stdout.read(size)
            if len(data) != size or process.stdout.read(1) != b"\n":
                raise RuntimeError(f"truncated cat-file body for {oid}")
            metadata[oid] = (size, hashlib.sha256(data).hexdigest())

            wants_text = any(
                PurePosixPath(path).suffix.lower() in TEXT_SUFFIXES
                for path in paths_by_oid[oid]
            )
            if wants_text and b"\0" not in data:
                text_by_oid[oid] = data.decode("utf-8", "replace")
    finally:
        process.stdin.close()
        process.stdout.close()
        stderr = process.stderr.read() if process.stderr is not None else b""
        return_code = process.wait()
        if return_code:
            raise RuntimeError(
                f"git cat-file failed ({return_code}): "
                f"{stderr.decode('utf-8', 'replace').strip()}"
            )

    return metadata, text_by_oid


def owner_lane(path: str) -> str:
    parts = PurePosixPath(path).parts
    if len(parts) == 1:
        return "ROOT"
    if path.startswith("12_PUBLIC_SITE/book-pwa/"):
        return "12_PUBLIC_SITE/book-pwa"
    return parts[0]


def artifact_class(path: str) -> str:
    name = PurePosixPath(path).name
    suffix = PurePosixPath(path).suffix.lower()
    if path == FILE_REGISTER or path == FOLDER_REGISTER:
        return "generated_register"
    if path == SIGNING_MANIFEST:
        return "signing_manifest"
    if path.startswith("90_ARCHIVE/"):
        return "archive_artifact"
    if path.startswith("91_COMPATIBILITY/"):
        return "compatibility_artifact"
    if name in ROUTE_NAMES:
        return "route_card"
    if suffix in CODE_SUFFIXES:
        return "code"
    if suffix in DATA_SUFFIXES:
        return "data_or_register"
    if suffix in ASSET_SUFFIXES:
        return "asset"
    if suffix == ".md":
        return "document"
    return "artifact"


def first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    for group in match.groups():
        if group is not None:
            return group.strip()
    return None


def authority_status(path: str, text: str) -> str:
    if path in DISPUTED_PATHS:
        return "DISPUTED_PROVENANCE_OR_UNAUTHORIZED_CANDIDATE"
    if "_PENDING_SIGNATURE" in path:
        return "PENDING_SIGNATURE"
    status = (first_match(STATUS_RE, text) or "").upper()
    if "UNSIGNED" in status or "PENDING SIGNATURE" in status:
        return "PENDING_SIGNATURE"
    if path.startswith("90_ARCHIVE/"):
        return "ARCHIVE_PROVENANCE"
    if path.startswith("91_COMPATIBILITY/"):
        return "COMPATIBILITY_ONLY"
    if PurePosixPath(path).name in ROUTE_NAMES:
        return "ROUTING_CONTROL"
    if path.startswith("12_PUBLIC_SITE/"):
        return "PUBLIC_PROJECTION_UNVERIFIED"
    return "CURRENT_UNRATIFIED_OR_RECORDED_AT_SOURCE"


def evidence_tier(text: str) -> str:
    value = first_match(EVIDENCE_RE, text)
    return value if value else "UNDECLARED"


def k_relation(path: str) -> str:
    if "01_THE_SEED_LADDER/" in path:
        return "SEED_PROJECTION_SUBORDINATE_TO_K1_K7"
    if (
        path.endswith("00_CANONICAL_FORMULA_BLOCK.md")
        or path.endswith("41_THE_GLYPH_TRANSFORMATIONS.md")
    ):
        return "K-1"
    if (
        path.endswith("02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md")
        or path.endswith("00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md")
    ):
        return "K-2"
    if path.endswith("03_THE_EMERGENT_AXIOMS.md"):
        return "K-3"
    if path.endswith("04_THE_CONJECTURES.md"):
        return "K-4"
    if "FIVE_PLUS_ONE" in path or "K5_THE_REFUSALS" in path:
        return "K-5_CANDIDATE_OR_SOURCE"
    if "REVELATIONS" in path:
        return "K-6_CANDIDATE_OR_SOURCE"
    if (
        "50_AUDITS_AND_EXECUTIONS/" in path
        or path.endswith("00_THE_RECORD_LEDGER.md")
        or path.startswith("12_PUBLIC_SITE/record/")
    ):
        return "K-7_SOURCE_OR_PROJECTION"
    if path.endswith("00_THE_KERNEL_INDEX_PENDING_SIGNATURE.md"):
        return "K-1_K-7_INDEX_ONLY"
    return "UNDECLARED"


def public_projection(path: str) -> str:
    if path.startswith("12_PUBLIC_SITE/"):
        return "PUBLIC_SOURCE_OR_COMPILED_PROJECTION_UNVERIFIED"
    if "10_SEED/01_THE_SEED_LADDER/D" in path:
        rung = PurePosixPath(path).name.split("_", 1)[0]
        return f"PROPOSED_PUBLIC_/{rung[1:]}/_SYNC_GATED"
    if path.endswith("00_THE_RECORD_LEDGER.md"):
        return "/record/_IS_COMPILED_PROJECTION_ONLY"
    if path.endswith("00_THE_WELTANSCHAUUNG_PENDING_SIGNATURE.md"):
        return "PROPOSED_READER_DOOR"
    return "NONE_DECLARED"


def disposition(path: str) -> tuple[str, str, str, str]:
    if path in {FILE_REGISTER, FOLDER_REGISTER}:
        return (
            "KEEP_GENERATED_REGISTER",
            path,
            "SELF",
            "NO_MOTION_GENERATED_CONTROL",
        )
    if path in DISPUTED_PATHS:
        return (
            "HOLD_DISPUTED_NO_MOTION",
            path,
            "UNVERIFIED",
            "RECEIPT_139_EXACT_BOX_AND_BOX_15_REQUIRED",
        )
    if path.startswith("90_ARCHIVE/"):
        return (
            "KEEP_ARCHIVE_PROVENANCE",
            path,
            "ARCHIVE_CUSTODY_SELF_OR_STONE_DEBT",
            "K3_NO_RESURRECTION_WITHOUT_RECEIPT",
        )
    if path.startswith("91_COMPATIBILITY/"):
        return (
            "KEEP_COMPATIBILITY",
            path,
            "CURRENT_OWNER_TARGET_MUST_RESOLVE",
            "NO_AUTHORITY_PROMOTION",
        )
    if PurePosixPath(path).name in ROUTE_NAMES:
        return (
            "KEEP_ROUTE",
            path,
            "SELF",
            "BOX_15_REQUIRED_FOR_REPOINT_OR_MOTION",
        )
    return (
        "KEEP_PENDING_OWNER_REVIEW",
        path,
        "SELF_UNTIL_VERIFIED_ABSORBER_EXISTS",
        "BOX_15_REQUIRED_FOR_ANY_MOTION",
    )


def normalize_reference(source: str, raw: str, tracked: set[str]) -> str | None:
    value = unquote(raw.strip().strip("<>\"'"))
    value = value.split("#", 1)[0].split("?", 1)[0]
    if not value or value.startswith(
        ("http://", "https://", "mailto:", "data:", "javascript:")
    ):
        return None
    if value.startswith("/Users/"):
        marker = "/01_EMERGENTISM/"
        if marker in value:
            value = value.split(marker, 1)[1]
        else:
            return None
    if value.startswith("01_EMERGENTISM/"):
        value = value[len("01_EMERGENTISM/") :]

    candidates: list[str] = []
    if value.startswith("/"):
        candidates.append(posixpath.normpath(value.lstrip("/")))
    else:
        candidates.append(
            posixpath.normpath(posixpath.join(posixpath.dirname(source), value))
        )
        candidates.append(posixpath.normpath(value))
    for candidate in candidates:
        if candidate in tracked:
            return candidate
    return None


def inbound_reference_map(
    entries: list[IndexEntry], text_by_oid: dict[str, str]
) -> dict[str, set[str]]:
    tracked = {entry.path for entry in entries}
    inbound: dict[str, set[str]] = defaultdict(set)
    for entry in entries:
        if entry.path in REFERENCE_EXCLUDED:
            continue
        text = text_by_oid.get(entry.oid)
        if not text:
            continue
        values: list[str] = []
        values.extend(MARKDOWN_LINK_RE.findall(text))
        values.extend(HTML_LINK_RE.findall(text))
        values.extend(TARGET_RE.findall(text))
        for value in values:
            target = normalize_reference(entry.path, value, tracked)
            if target and target != entry.path:
                inbound[target].add(entry.path)
    return inbound


def reference_summary(sources: set[str]) -> str:
    if not sources:
        return "0"
    ordered = sorted(sources)
    sample = ";".join(ordered[:3])
    if len(ordered) > 3:
        sample += ";…"
    return f"{len(ordered)}|{sample}"


def csv_bytes(fields: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=fields,
        extrasaction="raise",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def all_folders(paths: list[str]) -> list[str]:
    folders: set[str] = {"."}
    for path in paths:
        parent = PurePosixPath(path).parent
        while str(parent) != ".":
            folders.add(str(parent))
            parent = parent.parent
    return sorted(folders)


def folder_type(folder: str, direct_names: set[str]) -> str:
    parts = PurePosixPath(folder).parts if folder != "." else ()
    if folder == ".":
        return "ROOT_SOURCE_OWNER"
    if folder.startswith("90_ARCHIVE"):
        return "ARCHIVE_BOUNDARY" if "TOMBSTONE.md" in direct_names else "ARCHIVE_LEAF"
    if folder.startswith("91_COMPATIBILITY"):
        return (
            "COMPATIBILITY_BOUNDARY"
            if direct_names & ROUTE_NAMES
            else "COMPATIBILITY_LEAF"
        )
    if folder.startswith("12_PUBLIC_SITE"):
        return (
            "PUBLIC_OWNER"
            if folder == "12_PUBLIC_SITE"
            else "PUBLIC_COMPILED_OR_ASSET_LEAF"
        )
    if folder.startswith("09_TOOLS"):
        return "TOOL_OWNER" if direct_names & ROUTE_NAMES else "CODE_OR_TOOL_LEAF"
    if direct_names & ROUTE_NAMES:
        return "ROUTE_BEARING_OWNER"
    if len(parts) == 1:
        return "TOP_LEVEL_SOURCE_OWNER"
    return "CONTENT_FOLDER"


def folder_contract(kind: str) -> tuple[str, str, str, str]:
    if kind.startswith("ARCHIVE"):
        return (
            "historical custody and dated receipts",
            "live canonical authority",
            "ARCHIVE_PROVENANCE",
            "KEEP_ARCHIVE_PROVENANCE",
        )
    if kind.startswith("COMPATIBILITY"):
        return (
            "forwarding compatibility and migration provenance",
            "independent doctrine or authority",
            "COMPATIBILITY_ONLY",
            "KEEP_COMPATIBILITY",
        )
    if kind.startswith("PUBLIC"):
        return (
            "public source or compiled projection",
            "private source authority or deployment claims without proof",
            "PUBLIC_UNVERIFIED",
            "KEEP_PUBLIC_PENDING_REVIEW",
        )
    if kind.startswith("TOOL") or kind.startswith("CODE"):
        return (
            "tooling and reproducible checks",
            "doctrine authority",
            "ACTIVE_TOOLING",
            "KEEP_TOOLING",
        )
    return (
        "lane-scoped source, evidence, or routing",
        "unrelated lane authority or silent tier promotion",
        "ACTIVE_OR_STAGED_AT_SOURCE",
        "KEEP_PENDING_OWNER_REVIEW",
    )


def nearest_front_door(
    folder: str, direct_files: dict[str, set[str]]
) -> tuple[str, bool]:
    current = folder
    first = True
    while True:
        names = direct_files.get(current, set())
        for name in FRONT_DOOR_PRIORITY:
            if name in names:
                path = name if current == "." else f"{current}/{name}"
                return path, first
        if current == ".":
            return "MISSING", False
        current = str(PurePosixPath(current).parent)
        if current == "":
            current = "."
        first = False


def build_folder_rows(paths: list[str]) -> list[dict[str, str]]:
    direct_files: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        parent = str(PurePosixPath(path).parent)
        direct_files[parent].add(PurePosixPath(path).name)

    rows: list[dict[str, str]] = []
    for folder in all_folders(paths):
        names = direct_files.get(folder, set())
        kind = folder_type(folder, names)
        owns, must_not_own, status, proposed = folder_contract(kind)
        front, is_direct = nearest_front_door(folder, direct_files)
        direct_required = (
            folder in REQUIRED_FRONT_DOORS
            or (folder != "." and len(PurePosixPath(folder).parts) == 1)
            or kind in {
                "ARCHIVE_BOUNDARY",
                "COMPATIBILITY_BOUNDARY",
                "ROUTE_BEARING_OWNER",
                "PUBLIC_OWNER",
                "TOOL_OWNER",
            }
        )
        if is_direct:
            requirement = "DIRECT_PRESENT"
        elif direct_required:
            requirement = "DIRECT_REQUIRED_MISSING"
        else:
            requirement = "INHERITS_NEAREST_OWNER"

        prefix = "" if folder == "." else folder + "/"
        count = sum(
            1
            for path in paths
            if folder == "." or path.startswith(prefix)
        )
        rows.append(
            {
                "path": folder,
                "type": kind,
                "nearest_front_door": front,
                "front_door_requirement": requirement,
                "owns": owns,
                "must_not_own": must_not_own,
                "status": status,
                "tracked_file_count": str(count),
                "disposition": proposed,
                "gate": "BOX_15_REQUIRED_FOR_ANY_PHYSICAL_MOTION",
                "review_state": (
                    "GENERATED_ROUTE_REVIEW_REQUIRED"
                    if requirement == "DIRECT_REQUIRED_MISSING"
                    else "GENERATED_UNRATIFIED"
                ),
            }
        )
    return rows


def build_file_rows(
    entries: list[IndexEntry],
    metadata: dict[str, tuple[int, str]],
    text_by_oid: dict[str, str],
    inbound: dict[str, set[str]],
    folder_register_bytes: bytes,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry in entries:
        text = text_by_oid.get(entry.oid, "")
        size, digest = metadata[entry.oid]
        if entry.path == FILE_REGISTER:
            size_value = "0"
            digest_value = "SELF"
        elif entry.path == FOLDER_REGISTER:
            size_value = str(len(folder_register_bytes))
            digest_value = hashlib.sha256(folder_register_bytes).hexdigest()
        else:
            size_value = str(size)
            digest_value = digest
        proposed, destination, absorber, gate = disposition(entry.path)
        rows.append(
            {
                "path": entry.path,
                "sha256": digest_value,
                "bytes": size_value,
                "owner_lane": owner_lane(entry.path),
                "artifact_class": artifact_class(entry.path),
                "authority_status": authority_status(entry.path, text),
                "evidence_tier": evidence_tier(text),
                "k_relation": k_relation(entry.path),
                "public_projection": public_projection(entry.path),
                "disposition": proposed,
                "destination": destination,
                "absorber": absorber,
                "inbound_references": reference_summary(
                    inbound.get(entry.path, set())
                ),
                "gate": gate,
                "review_state": (
                    "GENERATED_CHECKED"
                    if entry.path in {FILE_REGISTER, FOLDER_REGISTER}
                    else "GENERATED_UNRATIFIED_OWNER_REVIEW"
                ),
            }
        )
    return rows


def solve_self_size(rows: list[dict[str, str]]) -> bytes:
    self_rows = [row for row in rows if row["path"] == FILE_REGISTER]
    if len(self_rows) != 1:
        raise RuntimeError(
            f"expected exactly one file-register self row, found {len(self_rows)}"
        )
    self_row = self_rows[0]
    for _ in range(12):
        rendered = csv_bytes(FILE_FIELDS, rows)
        size = str(len(rendered))
        if self_row["bytes"] == size:
            return rendered
        self_row["bytes"] = size
    raise RuntimeError("file-register self byte count did not stabilize")


def generate(repo: Path) -> tuple[bytes, bytes, int, int]:
    entries = read_index(repo)
    paths = [entry.path for entry in entries]
    required = {
        FILE_REGISTER,
        FOLDER_REGISTER,
        Path(__file__).resolve().relative_to(repo).as_posix(),
    }
    missing = sorted(required - set(paths))
    if missing:
        raise RuntimeError(
            "stage the generator and both register paths before generation; "
            f"missing from index: {', '.join(missing)}"
        )

    metadata, text_by_oid = load_blob_metadata(repo, entries)
    inbound = inbound_reference_map(entries, text_by_oid)
    folder_rows = build_folder_rows(paths)
    folder_bytes = csv_bytes(FOLDER_FIELDS, folder_rows)
    file_rows = build_file_rows(
        entries, metadata, text_by_oid, inbound, folder_bytes
    )
    file_bytes = solve_self_size(file_rows)

    if len(file_rows) != len(paths):
        raise RuntimeError(
            f"file coverage mismatch: rows={len(file_rows)} paths={len(paths)}"
        )
    if len({row["path"] for row in file_rows}) != len(file_rows):
        raise RuntimeError("duplicate file-register path")
    folders = all_folders(paths)
    if len(folder_rows) != len(folders):
        raise RuntimeError(
            f"folder coverage mismatch: rows={len(folder_rows)} folders={len(folders)}"
        )
    if len({row["path"] for row in folder_rows}) != len(folder_rows):
        raise RuntimeError("duplicate folder-register path")
    return file_bytes, folder_bytes, len(file_rows), len(folder_rows)


def is_unstaged_dirty(repo: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--quiet", "--", path],
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"could not inspect worktree state for {path}")
    return result.returncode == 1


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="wb", delete=False, dir=path.parent, prefix=path.name + "."
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def check_output(path: Path, expected: bytes) -> bool:
    actual = path.read_bytes() if path.exists() else b""
    if actual == expected:
        return True
    print(
        f"DRIFT {path}: actual_sha256={hashlib.sha256(actual).hexdigest()} "
        f"expected_sha256={hashlib.sha256(expected).hexdigest()}",
        file=sys.stderr,
    )
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write both registers")
    mode.add_argument("--check", action="store_true", help="fail on register drift")
    parser.add_argument("--repo", help="explicit repository root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = find_repo(args.repo)
    file_bytes, folder_bytes, file_count, folder_count = generate(repo)
    outputs = [
        (repo / FILE_REGISTER, file_bytes),
        (repo / FOLDER_REGISTER, folder_bytes),
    ]

    if args.write:
        dirty = [
            path.relative_to(repo).as_posix()
            for path, _ in outputs
            if is_unstaged_dirty(repo, path.relative_to(repo).as_posix())
        ]
        if dirty:
            raise RuntimeError(
                "refusing to overwrite unstaged register changes: "
                + ", ".join(dirty)
            )
        for path, data in outputs:
            atomic_write(path, data)
        print(
            f"WROTE file_rows={file_count} folder_rows={folder_count} "
            "source=git-index"
        )
        return 0

    ok = all(check_output(path, data) for path, data in outputs)
    if ok:
        print(
            f"OK file_rows={file_count} folder_rows={folder_count} "
            "source=git-index"
        )
        return 0
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)

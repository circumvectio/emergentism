#!/usr/bin/env python3
"""Validate the bounded Receipt-126 Kintsugi propagation manifest.

This tool checks reproducible repository facts and registered semantic
regressions.  It deliberately cannot promote an evidence tier or pronounce a
worldview true.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = (
    ROOT
    / "03_METHODOLOGY/01_THE_DERIVATION/03_RECEIPT_126_PROPAGATION_MANIFEST.json"
)
TEXT_SUFFIXES = {".html", ".json", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}


class ManifestError(ValueError):
    """Raised when the declared propagation evidence does not reproduce."""


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout


def _commit_paths(commit: str) -> tuple[str, ...]:
    output = _git("show", "--pretty=format:", "--name-only", commit)
    return tuple(sorted({line for line in output.splitlines() if line.strip()}))


def _path_set_hash(paths: Sequence[str]) -> str:
    payload = ("\n".join(sorted(set(paths))) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_semantic_module() -> ModuleType:
    path = ROOT / "09_TOOLS/02_COMPILERS/test_emergentist_compass_semantics.py"
    spec = importlib.util.spec_from_file_location("receipt126_semantics", path)
    if spec is None or spec.loader is None:
        raise ManifestError(f"cannot load semantic fixture module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _tracked_text_paths(excluded_prefixes: Sequence[str]) -> tuple[Path, ...]:
    tracked = _git("ls-files").splitlines()
    return tuple(
        ROOT / relative
        for relative in tracked
        if Path(relative).suffix.lower() in TEXT_SUFFIXES
        and not any(relative.startswith(prefix) for prefix in excluded_prefixes)
    )


def _validate_archived_custody_path(relative: str, errors: list[str]) -> None:
    """Require an in-repository, symlink-free regular file under 90_ARCHIVE."""

    if (
        "\x00" in relative
        or "\\" in relative
        or PurePosixPath(relative).is_absolute()
        or re.match(r"^[A-Za-z]:", relative)
    ):
        errors.append(
            "ownerRepair currentPath must be a repository-relative POSIX path "
            f"under 90_ARCHIVE: {relative}"
        )
        return

    lexical = PurePosixPath(relative)
    if ".." in lexical.parts:
        errors.append(
            f"ownerRepair currentPath must not contain '..' traversal: {relative}"
        )
        return
    if not lexical.parts or lexical.parts[0] != "90_ARCHIVE":
        errors.append(
            "ownerRepair archived custody must remain lexically under "
            f"90_ARCHIVE: {relative}"
        )
        return

    candidate = ROOT.joinpath(*lexical.parts)
    archive_root = ROOT / "90_ARCHIVE"
    cursor = ROOT
    symlink_found = False
    for part in lexical.parts:
        cursor /= part
        try:
            if cursor.is_symlink():
                symlink_found = True
                break
        except OSError:
            # The regular-file and strict-resolution checks below fail closed.
            break
    if symlink_found:
        errors.append(
            "ownerRepair currentPath must not contain direct or ancestor "
            f"symlinks: {relative}"
        )

    try:
        resolved_archive = archive_root.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        errors.append(
            f"ownerRepair moved custody path must resolve to an existing file: {relative}"
        )
        return
    try:
        resolved_candidate.relative_to(resolved_archive)
    except ValueError:
        errors.append(
            f"ownerRepair currentPath resolves outside 90_ARCHIVE: {relative}"
        )

    try:
        mode = candidate.lstat().st_mode
    except (OSError, ValueError):
        errors.append(
            f"ownerRepair moved custody path must be an existing regular file: {relative}"
        )
        return
    if not stat.S_ISREG(mode):
        errors.append(
            f"ownerRepair moved custody path must be an existing regular file: {relative}"
        )


def validate_manifest(manifest: Mapping[str, object]) -> dict[str, object]:
    errors: list[str] = []
    if manifest.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")
    if manifest.get("status") != "closed_for_registered_contract":
        errors.append("status must remain closed_for_registered_contract")
    if "does not authorize publication" not in str(manifest.get("authorityBoundary", "")):
        errors.append("authority boundary must deny publication authority")

    required_files = (manifest.get("sourceReceipt"), manifest.get("releaseDoctrine"))
    for relative in required_files:
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            errors.append(f"required file is absent: {relative!r}")

    frozen = tuple(str(item) for item in manifest.get("frozenPrefixes", []))
    expected_frozen = {
        "11_UPLINK/60_SESSION_PACKETS/",
        "12_PUBLIC_SITE/",
        "90_ARCHIVE/",
        "91_COMPATIBILITY/",
    }
    if set(frozen) != expected_frozen:
        errors.append("frozenPrefixes does not match the bounded contract")

    for record in manifest.get("implementationCommits", []):
        if not isinstance(record, Mapping):
            errors.append("implementation commit record must be an object")
            continue
        commit = str(record.get("commit", ""))
        try:
            paths = _commit_paths(commit)
        except subprocess.CalledProcessError:
            errors.append(f"implementation commit is not reproducible: {commit}")
            continue
        violations = [path for path in paths if any(path.startswith(prefix) for prefix in frozen)]
        if violations:
            errors.append(f"implementation commit {commit} touches frozen paths: {violations}")

    owner_record = manifest.get("ownerRepair", {})
    if not isinstance(owner_record, Mapping):
        errors.append("ownerRepair must be an object")
        owner_record = {}
    owner_paths = tuple(str(path) for path in owner_record.get("paths", []))
    if len(owner_paths) != len(set(owner_paths)):
        errors.append("ownerRepair paths must be unique")
    if len(owner_paths) != owner_record.get("pathCount"):
        errors.append("ownerRepair pathCount does not match its explicit path list")
    move_records = owner_record.get("currentPathMoves", [])
    if not isinstance(move_records, list):
        errors.append("ownerRepair currentPathMoves must be a list")
        move_records = []
    current_path_moves: dict[str, str] = {}
    current_targets: set[str] = set()
    for record in move_records:
        if not isinstance(record, Mapping):
            errors.append("ownerRepair move record must be an object")
            continue
        historical = str(record.get("historicalPath", ""))
        current = str(record.get("currentPath", ""))
        if not historical or historical in current_path_moves:
            errors.append("ownerRepair move historical paths must be non-empty and unique")
            continue
        if not current or current in current_targets:
            errors.append("ownerRepair move current paths must be non-empty and unique")
            continue
        current_path_moves[historical] = current
        current_targets.add(current)
        if historical not in owner_paths:
            errors.append(f"ownerRepair move source is not in the historical path set: {historical}")
        if (ROOT / historical).exists():
            errors.append(f"ownerRepair move source unexpectedly exists again: {historical}")
        _validate_archived_custody_path(current, errors)
        if record.get("custody") != "archived_provenance":
            errors.append(f"ownerRepair move custody must remain archived_provenance: {historical}")
        if record.get("semanticAuthority") != "none":
            errors.append(f"ownerRepair move must deny semantic authority: {historical}")
    absent_historical_paths = {
        relative for relative in owner_paths if not (ROOT / relative).is_file()
    }
    if set(current_path_moves) != absent_historical_paths:
        errors.append(
            "ownerRepair currentPathMoves must map exactly the absent historical owner paths"
        )
    try:
        recorded_owner_paths = _commit_paths(str(owner_record.get("commit", "")))
    except subprocess.CalledProcessError:
        recorded_owner_paths = ()
        errors.append("ownerRepair commit is not reproducible")
    if recorded_owner_paths != tuple(sorted(owner_paths)):
        errors.append("ownerRepair explicit path list differs from its Git object")
    if _path_set_hash(recorded_owner_paths) != owner_record.get("sortedPathSetSha256"):
        errors.append("ownerRepair sorted path-set hash differs")

    propagation = manifest.get("derivedPropagation", {})
    if not isinstance(propagation, Mapping):
        errors.append("derivedPropagation must be an object")
        propagation = {}
    try:
        propagation_paths = _commit_paths(str(propagation.get("commit", "")))
    except subprocess.CalledProcessError:
        propagation_paths = ()
        errors.append("derivedPropagation commit is not reproducible")
    if len(propagation_paths) != propagation.get("pathCount"):
        errors.append("derivedPropagation pathCount differs from its Git object")
    if _path_set_hash(propagation_paths) != propagation.get("sortedPathSetSha256"):
        errors.append("derivedPropagation sorted path-set hash differs")

    semantic_module = _load_semantic_module()
    specs = tuple(semantic_module.MUTATIONS)
    manifest_mutations = manifest.get("mutations", [])
    if not isinstance(manifest_mutations, list):
        errors.append("mutations must be a list")
        manifest_mutations = []
    mutation_count = manifest.get("mutationCount")
    if mutation_count != len(specs):
        errors.append("mutationCount differs from the executable mutation inventory")
    registered = {
        str(item.get("id")): str(item.get("owner"))
        for item in manifest_mutations
        if isinstance(item, Mapping)
    }
    expected = {spec.mutation_id: spec.owner for spec in specs}
    if (
        len(manifest_mutations) != mutation_count
        or len(registered) != len(manifest_mutations)
        or registered != expected
    ):
        errors.append("manifest must bind exactly the current executable mutations")

    boundary_validator = semantic_module.ClaimBoundaryValidator(specs)
    for spec in specs:
        owner = ROOT / spec.owner
        if not owner.is_file():
            errors.append(f"mutation owner is absent: {spec.owner}")
            continue
        text = owner.read_text(encoding="utf-8")
        if spec.repair_marker not in text:
            errors.append(f"repair marker is absent for {spec.mutation_id}")
        if spec.mutation_id in boundary_validator.violations(text):
            errors.append(f"registered fallacy is live in owner: {spec.mutation_id}")

    derived_seams = manifest.get("derivedSeams", [])
    if not isinstance(derived_seams, list) or len(derived_seams) != 6:
        errors.append("derivedSeams must contain the six registered review seams")
        derived_seams = []
    derived_ids: list[str] = []
    for seam in derived_seams:
        if not isinstance(seam, Mapping):
            errors.append("derived seam record must be an object")
            continue
        seam_id = str(seam.get("id", ""))
        derived_ids.append(seam_id)
        relative = str(seam.get("path", ""))
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"derived seam path is absent: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in seam.get("requiredMarkers", []):
            if str(marker) not in text:
                errors.append(f"derived seam marker is absent: {seam_id}: {marker}")
        for pattern in seam.get("forbiddenPatterns", []):
            if re.search(str(pattern), text, flags=re.IGNORECASE | re.DOTALL):
                errors.append(f"derived seam regression is live: {seam_id}: {pattern}")
    if len(derived_ids) != len(set(derived_ids)):
        errors.append("derived seam IDs must be unique")

    negative = manifest.get("negativeScan", {})
    if not isinstance(negative, Mapping):
        errors.append("negativeScan must be an object")
        negative = {}
    evidence_exclusions = tuple(str(item) for item in negative.get("excludedPrefixes", []))
    scan_exclusions = frozen + evidence_exclusions
    active_violations: list[tuple[str, str]] = []
    for path in _tracked_text_paths(scan_exclusions):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for mutation_id in sorted(boundary_validator.violations(text)):
            active_violations.append((str(path.relative_to(ROOT)), mutation_id))
    if active_violations:
        errors.append(f"active registered fallacy mutations remain: {active_violations}")

    if errors:
        raise ManifestError("; ".join(errors))
    return {
        "status": "ok",
        "owners": len(owner_paths),
        "movedOwners": len(current_path_moves),
        "mutations": len(specs),
        "derivedSeams": len(derived_seams),
        "propagationPaths": len(propagation_paths),
        "activeMutationHits": 0,
        "frozenScope": "clean",
        "authority": "staged-only",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", action="store_true", help="emit canonical JSON")
    args = parser.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    try:
        result = validate_manifest(manifest)
    except (ManifestError, subprocess.CalledProcessError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, sort_keys=True))
        else:
            print(f"PROP-126-FAIL {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(
            "PROP-126-OK "
            f"owners={result['owners']} "
            f"movedOwners={result['movedOwners']} "
            f"mutations={result['mutations']} "
            f"derivedSeams={result['derivedSeams']} "
            f"propagationPaths={result['propagationPaths']} "
            "activeMutationHits=0 frozen=clean authority=staged-only"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

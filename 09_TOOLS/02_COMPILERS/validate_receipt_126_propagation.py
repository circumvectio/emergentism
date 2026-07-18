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
import subprocess
import sys
from pathlib import Path
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


def validate_manifest(manifest: Mapping[str, object]) -> dict[str, object]:
    errors: list[str] = []
    if manifest.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")
    if manifest.get("status") != "closed_on_isolated_branch":
        errors.append("status must remain closed_on_isolated_branch")
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
    for relative in owner_paths:
        if not (ROOT / relative).is_file():
            errors.append(f"owner path is absent: {relative}")
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
    registered = {
        str(item.get("id")): str(item.get("owner"))
        for item in manifest_mutations
        if isinstance(item, Mapping)
    }
    expected = {spec.mutation_id: spec.owner for spec in specs}
    if len(manifest_mutations) != 14 or registered != expected:
        errors.append("manifest must bind exactly the fourteen executable mutations")

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
        "mutations": len(specs),
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
            f"mutations={result['mutations']} "
            f"propagationPaths={result['propagationPaths']} "
            "activeMutationHits=0 frozen=clean authority=staged-only"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

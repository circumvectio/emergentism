#!/usr/bin/env python3
"""Validate the bounded Receipt-126 propagation contract.

The validator reproduces declared file, marker, regex, fixture, and Git-scope
facts.  A pass means only that this registered contract reproduces.  It does
not assess substantive truth, empirical calibration, novelty, or authority.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import unittest
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from types import ModuleType


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = (
    ROOT
    / "03_METHODOLOGY/01_THE_DERIVATION/03_RECEIPT_126_PROPAGATION_MANIFEST.json"
)
EXPECTED_BASE = "614227e402abfb42c442d4637246691660857f75"
EXPECTED_EVIDENCE_TIER = (
    "[B] reproducible path/test facts; "
    "[I] sufficiency only for registered contract"
)
EXPECTED_FROZEN_PREFIXES = (
    "11_UPLINK/60_SESSION_PACKETS/",
    "12_PUBLIC_SITE/",
    "90_ARCHIVE/",
    "91_COMPATIBILITY/",
)
EXPECTED_REQUIREMENT_IDS = {
    "fixed-d4-d5-modality",
    "six-mu-and-non-mu-r6",
    "selected-titans",
    "selected-nonunique-product",
    "removable-quantum-correspondence",
    "bearer-complete-justice",
    "accountable-authorization-envelope",
    "canonical-egregoreotype",
    "positive-result-recovery",
    "rosetta-real-algebra-no-forced-seven",
}
TOP_LEVEL_KEYS = {
    "schemaVersion",
    "manifestId",
    "status",
    "date",
    "evidenceTier",
    "scopeStatement",
    "authorityBoundary",
    "sourceReceipt",
    "releaseDoctrine",
    "baseCommit",
    "frozenPrefixes",
    "mutationFixture",
    "mutations",
    "surfaces",
    "semanticRequirements",
    "closureCriteria",
    "knownLimits",
}
MUTATION_FIXTURE_KEYS = {
    "path",
    "specSymbol",
    "validatorSymbol",
    "testCase",
    "expectedCount",
}
MUTATION_KEYS = {"id", "owner", "repairMarker"}
SURFACE_KEYS = {
    "id",
    "category",
    "path",
    "requiredMarkers",
    "forbiddenPatterns",
}
REQUIREMENT_KEYS = {"id", "surfaceIds"}
SURFACE_CATEGORIES = {"owner", "front_door", "derived", "recovery"}


class ManifestError(ValueError):
    """The registered propagation evidence failed closed."""


class GitUnavailable(RuntimeError):
    """Git is not installed, so the optional frozen-scope probe cannot run."""


FrozenProbe = Callable[[Path, str, Sequence[str]], tuple[str, ...]]


def _run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _path_in_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(prefix)


def _frozen_touches(
    root: Path, base_commit: str, frozen_prefixes: Sequence[str]
) -> tuple[str, ...]:
    """Return tracked or untracked frozen paths changed since ``base_commit``."""

    if shutil.which("git") is None:
        raise GitUnavailable("git executable is unavailable")

    top = _run_git(root, "rev-parse", "--show-toplevel")
    if Path(top.stdout.strip()).resolve() != root.resolve():
        raise ManifestError("validator root is not the active Git worktree root")

    _run_git(root, "cat-file", "-e", f"{base_commit}^{{commit}}")
    ancestor = _run_git(
        root, "merge-base", "--is-ancestor", base_commit, "HEAD", check=False
    )
    if ancestor.returncode != 0:
        raise ManifestError("baseCommit is not an ancestor of HEAD")

    changed = _run_git(
        root, "diff", "--name-only", "--no-ext-diff", "--no-renames", base_commit, "--"
    ).stdout.splitlines()
    untracked = _run_git(
        root, "ls-files", "--others", "--exclude-standard"
    ).stdout.splitlines()
    touches = {
        path
        for path in (*changed, *untracked)
        if any(_path_in_prefix(path, prefix) for prefix in frozen_prefixes)
    }
    return tuple(sorted(touches))


def _safe_relative_path(value: object, label: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a nonempty relative POSIX path")
        return ""
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        errors.append(f"{label} must not escape the repository: {value!r}")
        return ""
    return value


def _exact_keys(
    value: object, expected: set[str], label: str, errors: list[str]
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        errors.append(f"{label} must be an object")
        return {}
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        errors.append(f"{label} keys differ; missing={missing}, unknown={unknown}")
    return value


def _string_list(value: object, label: str, errors: list[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        errors.append(f"{label} must be a nonempty list")
        return ()
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{label}[{index}] must be a nonempty string")
        else:
            result.append(item)
    if len(result) != len(set(result)):
        errors.append(f"{label} must not contain duplicates")
    return tuple(result)


def _load_module(path: Path) -> ModuleType:
    module_name = "_receipt126_compass_semantic_fixture"
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ManifestError(f"cannot load mutation fixture: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _run_bound_test(module: ModuleType, test_case: str) -> tuple[str, ...]:
    suite = unittest.defaultTestLoader.loadTestsFromName(test_case, module)
    if suite.countTestCases() != 1:
        return (f"bound mutation test must resolve to one case: {test_case}",)
    result = unittest.TestResult()
    suite.run(result)
    messages = [
        f"bound mutation test failure: {test.id()}: {detail}"
        for test, detail in (*result.failures, *result.errors)
    ]
    if result.skipped:
        messages.append("bound mutation test must not be skipped")
    return tuple(messages)


def _read_utf8(path: Path, label: str, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"{label} is absent: {path}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        errors.append(f"{label} is not readable UTF-8: {path}: {exc}")
        return ""


def validate_manifest(
    manifest: Mapping[str, object],
    *,
    root: Path = ROOT,
    frozen_probe: FrozenProbe | None = _frozen_touches,
) -> dict[str, object]:
    """Validate only the manifest's registered, bounded contract."""

    errors: list[str] = []
    top = _exact_keys(manifest, TOP_LEVEL_KEYS, "manifest", errors)

    if top.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")
    if top.get("manifestId") != "RECEIPT-126-PROPAGATION-CONTRACT-2026-07-19":
        errors.append("manifestId must name the locked Receipt-126 contract")
    if top.get("date") != "2026-07-19":
        errors.append("date must be the locked contract date")
    if top.get("status") != "closed_for_registered_contract":
        errors.append("status must be closed_for_registered_contract")
    if top.get("evidenceTier") != EXPECTED_EVIDENCE_TIER:
        errors.append("evidenceTier must retain the bounded B/I wording")
    if top.get("baseCommit") != EXPECTED_BASE:
        errors.append("baseCommit must be the locked 614227e lineage base")
    if "not corpus-wide semantic closure" not in str(top.get("scopeStatement", "")):
        errors.append("scopeStatement must deny corpus-wide semantic closure")
    if "does not authorize publication" not in str(top.get("authorityBoundary", "")):
        errors.append("authorityBoundary must deny publication authority")

    frozen_prefixes = _string_list(
        top.get("frozenPrefixes"), "frozenPrefixes", errors
    )
    if frozen_prefixes != EXPECTED_FROZEN_PREFIXES:
        errors.append("frozenPrefixes must match the locked four-prefix contract")

    for field in ("sourceReceipt", "releaseDoctrine"):
        relative = _safe_relative_path(top.get(field), field, errors)
        if relative:
            _read_utf8(root / relative, field, errors)

    fixture = _exact_keys(
        top.get("mutationFixture"), MUTATION_FIXTURE_KEYS, "mutationFixture", errors
    )
    fixture_path = _safe_relative_path(
        fixture.get("path"), "mutationFixture.path", errors
    )
    if fixture.get("expectedCount") != 14:
        errors.append("mutationFixture.expectedCount must be 14")
    for field in ("specSymbol", "validatorSymbol", "testCase"):
        if not isinstance(fixture.get(field), str) or not fixture.get(field):
            errors.append(f"mutationFixture.{field} must be a nonempty string")

    module: ModuleType | None = None
    specs: tuple[object, ...] = ()
    if fixture_path:
        path = root / fixture_path
        if not path.is_file():
            errors.append(f"mutation fixture is absent: {fixture_path}")
        else:
            try:
                module = _load_module(path)
                specs = tuple(getattr(module, str(fixture.get("specSymbol"))))
                if len(specs) != 14:
                    errors.append("mutation fixture must expose exactly fourteen specs")
                validator_type = getattr(module, str(fixture.get("validatorSymbol")))
                if not callable(validator_type):
                    errors.append("mutation validator symbol is not callable")
            except (AttributeError, ImportError, OSError, TypeError) as exc:
                errors.append(f"cannot load mutation fixture contract: {exc}")
                module = None

    mutation_value = top.get("mutations")
    if not isinstance(mutation_value, list):
        errors.append("mutations must be a list")
        mutation_value = []
    mutation_records: list[Mapping[str, object]] = []
    mutation_ids: list[str] = []
    for index, raw in enumerate(mutation_value):
        record = _exact_keys(raw, MUTATION_KEYS, f"mutations[{index}]", errors)
        mutation_records.append(record)
        mutation_id = record.get("id")
        if not isinstance(mutation_id, str) or not mutation_id:
            errors.append(f"mutations[{index}].id must be a nonempty string")
        else:
            mutation_ids.append(mutation_id)
        _safe_relative_path(record.get("owner"), f"mutations[{index}].owner", errors)
        if not isinstance(record.get("repairMarker"), str) or not record.get(
            "repairMarker"
        ):
            errors.append(f"mutations[{index}].repairMarker must be nonempty")
    if len(mutation_ids) != len(set(mutation_ids)):
        errors.append("mutation IDs must be unique")
    if len(mutation_records) != 14:
        errors.append("mutations must contain exactly fourteen records")

    if specs:
        expected_mutations = [
            {
                "id": spec.mutation_id,
                "owner": spec.owner,
                "repairMarker": spec.repair_marker,
            }
            for spec in specs
        ]
        normalized_mutations = [dict(record) for record in mutation_records]
        if normalized_mutations != expected_mutations:
            errors.append(
                "mutations must exactly bind the fixture IDs, owners, markers, and order"
            )
        try:
            boundary_validator = getattr(
                module, str(fixture.get("validatorSymbol"))
            )(specs)
            for spec in specs:
                owner_path = root / spec.owner
                owner_text = _read_utf8(owner_path, f"mutation owner {spec.mutation_id}", errors)
                if spec.repair_marker not in owner_text:
                    errors.append(
                        f"mutation repair marker is absent: {spec.mutation_id}"
                    )
                if spec.mutation_id in boundary_validator.violations(owner_text):
                    errors.append(f"registered mutation is live: {spec.mutation_id}")
        except (AttributeError, TypeError) as exc:
            errors.append(f"cannot execute mutation boundary validator: {exc}")
        if module is not None:
            errors.extend(_run_bound_test(module, str(fixture.get("testCase"))))

    surfaces_value = top.get("surfaces")
    if not isinstance(surfaces_value, list) or not surfaces_value:
        errors.append("surfaces must be a nonempty list")
        surfaces_value = []
    surface_ids: list[str] = []
    for index, raw in enumerate(surfaces_value):
        surface = _exact_keys(raw, SURFACE_KEYS, f"surfaces[{index}]", errors)
        surface_id = surface.get("id")
        if not isinstance(surface_id, str) or not surface_id:
            errors.append(f"surfaces[{index}].id must be a nonempty string")
            surface_id = f"invalid-{index}"
        else:
            surface_ids.append(surface_id)
        if surface.get("category") not in SURFACE_CATEGORIES:
            errors.append(f"surfaces[{index}].category is invalid")
        relative = _safe_relative_path(
            surface.get("path"), f"surfaces[{index}].path", errors
        )
        markers = _string_list(
            surface.get("requiredMarkers"),
            f"surfaces[{index}].requiredMarkers",
            errors,
        )
        patterns = _string_list(
            surface.get("forbiddenPatterns"),
            f"surfaces[{index}].forbiddenPatterns",
            errors,
        )
        text = _read_utf8(root / relative, f"surface {surface_id}", errors) if relative else ""
        for marker in markers:
            if marker not in text:
                errors.append(f"required marker is absent: {surface_id}: {marker}")
        for pattern in patterns:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL)
            except re.error as exc:
                errors.append(f"forbidden regex is invalid: {surface_id}: {exc}")
                continue
            if compiled.search(text):
                errors.append(f"forbidden regex matched: {surface_id}: {pattern}")
    if len(surface_ids) != len(set(surface_ids)):
        errors.append("surface IDs must be unique")

    requirements_value = top.get("semanticRequirements")
    if not isinstance(requirements_value, list):
        errors.append("semanticRequirements must be a list")
        requirements_value = []
    requirement_ids: list[str] = []
    known_surface_ids = set(surface_ids)
    for index, raw in enumerate(requirements_value):
        requirement = _exact_keys(
            raw, REQUIREMENT_KEYS, f"semanticRequirements[{index}]", errors
        )
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or not requirement_id:
            errors.append(f"semanticRequirements[{index}].id must be nonempty")
        else:
            requirement_ids.append(requirement_id)
        references = _string_list(
            requirement.get("surfaceIds"),
            f"semanticRequirements[{index}].surfaceIds",
            errors,
        )
        unknown = sorted(set(references) - known_surface_ids)
        if unknown:
            errors.append(
                f"semanticRequirements[{index}] references unknown surfaces: {unknown}"
            )
    if len(requirement_ids) != len(set(requirement_ids)):
        errors.append("semantic requirement IDs must be unique")
    if set(requirement_ids) != EXPECTED_REQUIREMENT_IDS:
        errors.append("semanticRequirements must bind the locked ten requirements")

    for field in ("closureCriteria", "knownLimits"):
        _string_list(top.get(field), field, errors)
    limits_text = " ".join(
        item for item in top.get("knownLimits", []) if isinstance(item, str)
    )
    if "not a semantic theorem prover" not in limits_text:
        errors.append("knownLimits must deny semantic-theorem-prover status")
    if "does not establish novelty" not in limits_text:
        errors.append("knownLimits must deny novelty and external authority")

    frozen_scope = "not_checked_no_git"
    if frozen_probe is not None and frozen_prefixes:
        try:
            touches = frozen_probe(root, str(top.get("baseCommit", "")), frozen_prefixes)
        except GitUnavailable:
            touches = ()
        except (ManifestError, OSError, subprocess.SubprocessError) as exc:
            errors.append(f"frozen-prefix Git probe failed: {exc}")
            touches = ()
        else:
            frozen_scope = "clean"
            if touches:
                errors.append(f"frozen prefixes changed since baseCommit: {list(touches)}")

    if errors:
        raise ManifestError("; ".join(errors))

    return {
        "status": "registered_contract_pass",
        "substantiveTruth": "not_assessed",
        "registeredSurfaces": len(surface_ids),
        "semanticRequirements": len(requirement_ids),
        "mutations": len(mutation_records),
        "frozenScope": frozen_scope,
        "scope": "registered_paths_and_tests_only",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", action="store_true", help="emit canonical JSON")
    args = parser.parse_args(argv)

    try:
        loaded = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(loaded, Mapping):
            raise ManifestError("manifest root must be an object")
        result = validate_manifest(loaded)
    except (json.JSONDecodeError, OSError, ManifestError) as exc:
        if args.json:
            print(
                json.dumps(
                    {
                        "error": str(exc),
                        "status": "registered_contract_fail",
                        "substantiveTruth": "not_assessed",
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
        else:
            print(f"PROP-126-FAIL {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    else:
        print(
            "PROP-126-REGISTERED-CONTRACT-PASS "
            f"surfaces={result['registeredSurfaces']} "
            f"requirements={result['semanticRequirements']} "
            f"mutations={result['mutations']} "
            f"frozen={result['frozenScope']} "
            "substantive-truth=not-assessed"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

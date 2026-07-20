#!/usr/bin/env python3
"""Fail-closed verifier for the Formal Reap Lean project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "FormalReap"
LEDGER_ROW_BY_THEOREM = {
    "reciprocal_seam": "R1.1",
    "positive_inversion_fixed_point": "R1.3",
    "inversion_fixed_points": "R1.2",
    "reciprocal_amgm": "R1.4",
    "reciprocal_amgm_eq_iff": "R1.4",
    "normalized_balance_le_one": "R1.5",
    "normalized_balance_eq_one_iff": "R1.5",
    "multiplication_need_both": "R3.1",
    "minimum_need_both": "R3.2",
    "zero_boundary_does_not_force_multiplication": "R3.2",
    "effective_power_zero_iff": "R5.2",
    "effective_power_positive": "R5.3",
    "effective_power_unit_interval": "R5.3a",
    "ladder_inheritance": "R1.6",
    "inheritance_requires_preservation": "R1.7",
    "forecast_changes_outcome": "R5.4",
    "not_every_forecast_is_reflexive": "R5.5",
    "typed_boundary_composition": "R0.2",
    "extended_zero_times_infinity_is_not_one": "R0.3",
    "operator_mask_does_not_determine_valence": "RC.2",
    "return_matches_floor_in_role": "R6.1",
    "finite_horizon_host_collapse": "R5.12",
    "gated_universal_collapse_certificate": "R5.12",
    "positive_extraction_can_persist": "R5.13",
    "non_extraction_does_not_imply_justice_or_ascent": "R5.14",
    "no_universal_is_ought": "R5.15",
    "ought_from_declared_bridge": "R5.15",
    "bool_action_has_utility_maximizer": "R5.9",
    "action_need_not_maximize_utility": "R5.10",
    "cone_and_horizon_do_not_determine_justice": "R5.11",
    "dyadic_gate_implies_nonnegative_aggregate": "R5.11b",
    "positive_aggregate_does_not_imply_dyadic_gate": "R5.11b",
    "mass_shell_iff_normalized": "R4.1",
    "null_product_iff_mass_shell": "R4.1",
    "rest_energy_of_mass_shell": "R4.2",
    "rest_ratio_le_one": "R4.3",
}
EXPECTED = set(LEDGER_ROW_BY_THEOREM)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEAN_NAME_TOKEN = r"(«[^»]+»|[^\s({:]+)"
THEOREM_DECLARATION = re.compile(rf"\b(?:theorem|lemma)\s+{LEAN_NAME_TOKEN}")
FORBIDDEN_DECLARATION = re.compile(rf"\b(?:axiom|constant)\s+{LEAN_NAME_TOKEN}")
VOLATILE_RECEIPT_FIELDS = {
    "generated_at_utc",
    "git_head_at_start",
    "git_head_at_end",
    "git_head_changed_during_run",
    "git_worktree_clean_before_receipt_write",
    "stored_receipt_matches_current_core",
}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{Path.home()}/.elan/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_probe(
    command: list[str], cwd: Path = ROOT
) -> subprocess.CompletedProcess[str]:
    """Run a metadata probe with stderr separated from machine-readable stdout."""
    env = os.environ.copy()
    env["PATH"] = f"{Path.home()}/.elan/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def strip_lean_comments(text: str) -> str:
    """Remove nested Lean block comments and line comments for token scanning."""
    out: list[str] = []
    i = 0
    depth = 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith("--", i):
            newline = text.find("\n", i)
            if newline == -1:
                break
            out.append("\n")
            i = newline + 1
        else:
            out.append(text[i])
            i += 1
    if depth:
        raise ValueError("unterminated Lean block comment")
    return "".join(out)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def snapshot(paths: list[Path]) -> dict[str, str]:
    """Hash verification inputs, retaining missing paths as fail-closed evidence."""
    return {
        str(path.resolve()): sha256(path) if path.is_file() else "<missing>"
        for path in paths
    }


def parse_ledger_certificate_cells(text: str) -> tuple[dict[str, str], list[str]]:
    """Return claim-ID to certificate-cell mappings and duplicate claim IDs."""
    rows: dict[str, str] = {}
    duplicates: list[str] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 6 or not cells[1].startswith("R"):
            continue
        claim_id = cells[1]
        if claim_id in rows:
            duplicates.append(claim_id)
        rows[claim_id] = cells[4]
    return rows, sorted(set(duplicates))


def receipt_core(receipt: dict[str, object]) -> dict[str, object]:
    """Remove intentionally volatile provenance fields for stored-receipt checks."""
    return {
        key: value
        for key, value in receipt.items()
        if key not in VOLATILE_RECEIPT_FIELDS
    }


def dependency_snapshot(
    manifest: dict[str, object],
) -> tuple[dict[str, dict[str, object]], list[str]]:
    """Attest that every manifest dependency is at its pinned, clean Git tree."""
    attestations: dict[str, dict[str, object]] = {}
    errors: list[str] = []
    packages = manifest.get("packages")
    if not isinstance(packages, list):
        return {}, ["lake manifest has no package list"]

    for package in packages:
        if not isinstance(package, dict):
            errors.append("lake manifest contains a non-object package entry")
            continue
        name = package.get("name")
        expected_revision = package.get("rev")
        if not isinstance(name, str) or not isinstance(expected_revision, str):
            errors.append("lake manifest package lacks name or revision")
            continue
        package_dir = ROOT / ".lake" / "packages" / name
        if not package_dir.is_dir():
            errors.append(f"dependency checkout missing: {name}")
            continue

        head_probe = run_probe(["/usr/bin/git", "rev-parse", "HEAD"], package_dir)
        tree_probe = run_probe(["/usr/bin/git", "rev-parse", "HEAD^{tree}"], package_dir)
        status_probe = run_probe(
            ["/usr/bin/git", "status", "--porcelain=v1", "--untracked-files=all"],
            package_dir,
        )
        probes = {
            "HEAD": head_probe,
            "tree": tree_probe,
            "status": status_probe,
        }
        for label, probe in probes.items():
            if probe.returncode != 0:
                errors.append(f"dependency {name} {label} probe failed")

        actual_revision = head_probe.stdout.strip()
        tree = tree_probe.stdout.strip()
        clean = status_probe.returncode == 0 and not status_probe.stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40,64}", actual_revision):
            errors.append(f"dependency {name} returned an invalid HEAD")
        if not re.fullmatch(r"[0-9a-f]{40,64}", tree):
            errors.append(f"dependency {name} returned an invalid tree hash")
        if actual_revision != expected_revision:
            errors.append(f"dependency {name} is not at its manifest revision")
        if not clean:
            errors.append(f"dependency {name} checkout is dirty")

        attestations[name] = {
            "expected_revision": expected_revision,
            "actual_revision": actual_revision,
            "tree": tree,
            "clean": clean,
        }

    return dict(sorted(attestations.items())), sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()

    sources = sorted([ROOT / "FormalReap.lean", *LEAN_ROOT.rglob("*.lean")])
    project_inputs = [
        ROOT / "lean-toolchain",
        ROOT / "lakefile.toml",
        ROOT / "lake-manifest.json",
    ]
    support_artifacts = [ROOT / "README.md", ROOT / "PROOF_LEDGER.md", ROOT / "verify.py"]
    source_under_test = (ROOT / "../../../10_SEED/02_THE_REAP.md").resolve()
    verification_inputs = [*sources, *project_inputs, *support_artifacts, source_under_test]
    input_snapshot_before = snapshot(verification_inputs)
    manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    dependency_state_before, dependency_errors_before = dependency_snapshot(manifest)
    git_head_before_probe = run_probe(["/usr/bin/git", "rev-parse", "HEAD"])
    probe_errors: list[str] = []
    if git_head_before_probe.returncode != 0:
        probe_errors.append("initial Git HEAD probe failed")
    git_head_before = git_head_before_probe.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", git_head_before):
        probe_errors.append("initial Git HEAD probe returned invalid output")
    forbidden: list[str] = []
    theorem_names: set[str] = set()
    for source in sources:
        stripped = strip_lean_comments(source.read_text(encoding="utf-8"))
        for token in ("sorry", "admit"):
            if re.search(rf"\b{token}\b", stripped):
                forbidden.append(f"{source.relative_to(ROOT)}: token {token}")
        for name in FORBIDDEN_DECLARATION.findall(stripped):
            forbidden.append(
                f"{source.relative_to(ROOT)}: custom axiom/constant declaration {name}"
            )
        theorem_names.update(THEOREM_DECLARATION.findall(stripped))

    missing = sorted(EXPECTED - theorem_names)
    unexpected_theorems = sorted(theorem_names - EXPECTED)
    ledger_text = (ROOT / "PROOF_LEDGER.md").read_text(encoding="utf-8")
    ledger_rows, duplicate_ledger_rows = parse_ledger_certificate_cells(ledger_text)
    unledgered_theorems = sorted(
        name
        for name, claim_id in LEDGER_ROW_BY_THEOREM.items()
        if f"`{name}`" not in ledger_rows.get(claim_id, "")
    )
    audit_source = (LEAN_ROOT / "Audit.lean").read_text(encoding="utf-8")
    audited_names = set(re.findall(
        r"(?m)^#print axioms FormalReap\.[A-Za-z0-9_']+\.([A-Za-z0-9_']+)$",
        audit_source,
    ))
    missing_audits = sorted(theorem_names - audited_names)
    orphan_audits = sorted(audited_names - theorem_names)
    build = run([str(Path.home() / ".elan/bin/lake"), "build"])
    audit = run([
        str(Path.home() / ".elan/bin/lake"),
        "env",
        "lean",
        "FormalReap/Audit.lean",
    ])

    reported_axioms: set[str] = set()
    for match in re.finditer(r"depends on axioms: \[([^\]]*)\]", audit.stdout, re.DOTALL):
        reported_axioms.update(item.strip() for item in match.group(1).split(",") if item.strip())
    audit_output_names = set(re.findall(
        r"'FormalReap\.[A-Za-z0-9_']+\.([A-Za-z0-9_']+)' "
        r"(?:depends on axioms:|does not depend on any axioms)",
        audit.stdout,
    ))
    missing_audit_outputs = sorted(EXPECTED - audit_output_names)
    unexpected_audit_outputs = sorted(audit_output_names - EXPECTED)
    unexpected_axioms = sorted(reported_axioms - ALLOWED_AXIOMS)

    lean_version_probe = run_probe([str(Path.home() / ".elan/bin/lean"), "--version"])
    lake_version_probe = run_probe([str(Path.home() / ".elan/bin/lake"), "--version"])
    if lean_version_probe.returncode != 0:
        probe_errors.append("Lean version probe failed")
    if lake_version_probe.returncode != 0:
        probe_errors.append("Lake version probe failed")
    lean_version = lean_version_probe.stdout.strip()
    lake_version = lake_version_probe.stdout.strip()
    mathlib_package = next(
        package for package in manifest["packages"] if package["name"] == "mathlib"
    )
    dependency_state_after, dependency_errors_after = dependency_snapshot(manifest)
    dependency_errors = sorted(
        set(dependency_errors_before) | set(dependency_errors_after)
    )
    dependency_checkouts_changed = dependency_state_before != dependency_state_after
    git_head_after_probe = run_probe(["/usr/bin/git", "rev-parse", "HEAD"])
    git_status_probe = run_probe(["/usr/bin/git", "status", "--porcelain"])
    if git_head_after_probe.returncode != 0:
        probe_errors.append("final Git HEAD probe failed")
    if git_status_probe.returncode != 0:
        probe_errors.append("Git status probe failed")
    git_head_after = git_head_after_probe.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", git_head_after):
        probe_errors.append("final Git HEAD probe returned invalid output")
    git_head_changed = git_head_before != git_head_after
    git_status = git_status_probe.stdout
    sources_after = sorted([ROOT / "FormalReap.lean", *LEAN_ROOT.rglob("*.lean")])
    verification_inputs_after = [
        *sources_after,
        *project_inputs,
        *support_artifacts,
        source_under_test,
    ]
    input_snapshot_after = snapshot(verification_inputs_after)
    def verified_hash(path: Path) -> str:
        return input_snapshot_after[str(path.resolve())]

    changed_inputs = sorted(
        path
        for path in set(input_snapshot_before) | set(input_snapshot_after)
        if input_snapshot_before.get(path) != input_snapshot_after.get(path)
    )

    status = "PASS"
    failures: list[str] = []
    if build.returncode != 0:
        status = "FAIL"
        failures.append("lake build failed")
    if audit.returncode != 0:
        status = "FAIL"
        failures.append("axiom audit failed")
    if forbidden:
        status = "FAIL"
        failures.extend(forbidden)
    if missing:
        status = "FAIL"
        failures.append(f"missing expected theorems: {', '.join(missing)}")
    if unexpected_theorems:
        status = "FAIL"
        failures.append(f"unregistered theorems: {', '.join(unexpected_theorems)}")
    if unledgered_theorems:
        status = "FAIL"
        failures.append(f"theorems missing from proof ledger: {', '.join(unledgered_theorems)}")
    if duplicate_ledger_rows:
        status = "FAIL"
        failures.append(f"duplicate proof-ledger rows: {', '.join(duplicate_ledger_rows)}")
    if missing_audits:
        status = "FAIL"
        failures.append(f"missing axiom audits: {', '.join(missing_audits)}")
    if orphan_audits:
        status = "FAIL"
        failures.append(f"orphan axiom audits: {', '.join(orphan_audits)}")
    if missing_audit_outputs:
        status = "FAIL"
        failures.append(f"missing parsed audit outputs: {', '.join(missing_audit_outputs)}")
    if unexpected_audit_outputs:
        status = "FAIL"
        failures.append(f"unexpected parsed audit outputs: {', '.join(unexpected_audit_outputs)}")
    if unexpected_axioms:
        status = "FAIL"
        failures.append(f"unexpected axioms: {', '.join(unexpected_axioms)}")
    if changed_inputs:
        status = "FAIL"
        failures.append("verification inputs changed during run")
    if probe_errors:
        status = "FAIL"
        failures.extend(sorted(set(probe_errors)))
    if dependency_errors:
        status = "FAIL"
        failures.extend(dependency_errors)
    if dependency_checkouts_changed:
        status = "FAIL"
        failures.append("dependency checkouts changed during run")
    receipt = {
        "schema": "formal-reap-verification-v2",
        "status": status,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "local machine-checked theorem and countermodel kernel; no doctrine promotion",
        "source_under_test": "10_SEED/02_THE_REAP.md",
        "source_under_test_sha256": verified_hash(source_under_test),
        "git_head_at_start": git_head_before,
        "git_head_at_end": git_head_after,
        "git_head_changed_during_run": git_head_changed,
        "git_worktree_clean_before_receipt_write": not bool(git_status.strip()),
        "lean_version": lean_version,
        "lake_version": lake_version,
        "mathlib_input_revision": mathlib_package["inputRev"],
        "mathlib_resolved_revision": mathlib_package["rev"],
        "source_count": len(sources),
        "theorem_count": len(theorem_names),
        "expected_theorem_count": len(EXPECTED),
        "missing_expected_theorems": missing,
        "unregistered_theorems": unexpected_theorems,
        "theorems_missing_from_ledger": unledgered_theorems,
        "duplicate_proof_ledger_rows": duplicate_ledger_rows,
        "ledger_row_by_theorem": LEDGER_ROW_BY_THEOREM,
        "audited_theorem_count": len(audited_names),
        "missing_axiom_audits": missing_audits,
        "orphan_axiom_audits": orphan_audits,
        "parsed_audit_output_count": len(audit_output_names),
        "missing_parsed_audit_outputs": missing_audit_outputs,
        "unexpected_parsed_audit_outputs": unexpected_audit_outputs,
        "forbidden_declarations": forbidden,
        "reported_axioms": sorted(reported_axioms),
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "unexpected_axioms": unexpected_axioms,
        "metadata_probe_errors": sorted(set(probe_errors)),
        "dependency_checkout_errors": dependency_errors,
        "dependency_checkouts_changed_during_run": dependency_checkouts_changed,
        "dependency_checkouts": dependency_state_after,
        "verification_input_changes": changed_inputs,
        "source_sha256": {
            str(path.relative_to(ROOT)): verified_hash(path) for path in sources
        },
        "project_input_sha256": {
            str(path.relative_to(ROOT)): verified_hash(path) for path in project_inputs
        },
        "support_artifact_sha256": {
            str(path.relative_to(ROOT)): verified_hash(path) for path in support_artifacts
        },
        "failures": failures,
    }

    receipt_path = ROOT / "verification_receipt.json"
    if args.write_receipt:
        receipt["stored_receipt_matches_current_core"] = True
        serialized_receipt = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        temporary_receipt = receipt_path.with_suffix(".json.tmp")
        temporary_receipt.write_text(serialized_receipt, encoding="utf-8")
        os.replace(temporary_receipt, receipt_path)
    else:
        stored_receipt_matches = False
        try:
            stored_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            stored_receipt_matches = (
                isinstance(stored_receipt, dict)
                and receipt_core(stored_receipt) == receipt_core(receipt)
            )
        except (FileNotFoundError, json.JSONDecodeError):
            stored_receipt_matches = False
        if not stored_receipt_matches:
            status = "FAIL"
            failures.append("stored verification receipt does not match current core")
            receipt["status"] = status
        receipt["stored_receipt_matches_current_core"] = stored_receipt_matches

    print(json.dumps(receipt, indent=2, sort_keys=True))
    if build.returncode != 0:
        print("\n--- lake build output ---\n" + build.stdout, file=sys.stderr)
    if audit.returncode != 0 or unexpected_axioms:
        print("\n--- axiom audit output ---\n" + audit.stdout, file=sys.stderr)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

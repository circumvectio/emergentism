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
EXPECTED = {
    "reciprocal_seam",
    "positive_inversion_fixed_point",
    "inversion_fixed_points",
    "reciprocal_amgm",
    "reciprocal_amgm_eq_iff",
    "normalized_balance_le_one",
    "normalized_balance_eq_one_iff",
    "multiplication_need_both",
    "minimum_need_both",
    "zero_boundary_does_not_force_multiplication",
    "effective_power_zero_iff",
    "effective_power_positive",
    "effective_power_unit_interval",
    "ladder_inheritance",
    "inheritance_requires_preservation",
    "forecast_changes_outcome",
    "not_every_forecast_is_reflexive",
    "typed_boundary_composition",
    "extended_zero_times_infinity_is_not_one",
    "operator_mask_does_not_determine_valence",
    "return_matches_floor_in_role",
    "finite_horizon_host_collapse",
    "gated_universal_collapse_certificate",
    "positive_extraction_can_persist",
    "non_extraction_does_not_imply_justice_or_ascent",
    "no_universal_is_ought",
    "ought_from_declared_bridge",
    "bool_action_has_utility_maximizer",
    "action_need_not_maximize_utility",
    "cone_and_horizon_do_not_determine_justice",
    "dyadic_gate_implies_nonnegative_aggregate",
    "positive_aggregate_does_not_imply_dyadic_gate",
    "mass_shell_iff_normalized",
    "null_product_iff_mass_shell",
    "rest_energy_of_mass_shell",
    "rest_ratio_le_one",
}
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


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
    forbidden: list[str] = []
    theorem_names: set[str] = set()
    for source in sources:
        stripped = strip_lean_comments(source.read_text(encoding="utf-8"))
        for token in ("sorry", "admit"):
            if re.search(rf"\b{token}\b", stripped):
                forbidden.append(f"{source.relative_to(ROOT)}: token {token}")
        if re.search(r"(?m)^\s*(?:axiom|constant)\s+", stripped):
            forbidden.append(f"{source.relative_to(ROOT)}: custom axiom/constant declaration")
        theorem_names.update(
            re.findall(r"(?m)^(?:theorem|lemma)\s+([A-Za-z0-9_']+)", stripped)
        )

    missing = sorted(EXPECTED - theorem_names)
    unexpected_theorems = sorted(theorem_names - EXPECTED)
    ledger_text = (ROOT / "PROOF_LEDGER.md").read_text(encoding="utf-8")
    unledgered_theorems = sorted(name for name in EXPECTED if f"`{name}`" not in ledger_text)
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

    lean_version = run([str(Path.home() / ".elan/bin/lean"), "--version"]).stdout.strip()
    lake_version = run([str(Path.home() / ".elan/bin/lake"), "--version"]).stdout.strip()
    manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_package = next(
        package for package in manifest["packages"] if package["name"] == "mathlib"
    )
    git_head = run(["/usr/bin/git", "rev-parse", "HEAD"]).stdout.strip()
    git_status = run(["/usr/bin/git", "status", "--porcelain"]).stdout
    sources_after = sorted([ROOT / "FormalReap.lean", *LEAN_ROOT.rglob("*.lean")])
    verification_inputs_after = [
        *sources_after,
        *project_inputs,
        *support_artifacts,
        source_under_test,
    ]
    input_snapshot_after = snapshot(verification_inputs_after)
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

    receipt = {
        "schema": "formal-reap-verification-v1",
        "status": status,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "local machine-checked theorem and countermodel kernel; no doctrine promotion",
        "source_under_test": "10_SEED/02_THE_REAP.md",
        "source_under_test_sha256": sha256(source_under_test),
        "git_head": git_head,
        "git_worktree_clean": not bool(git_status.strip()),
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
        "verification_input_changes": changed_inputs,
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in sources
        },
        "project_input_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in project_inputs
        },
        "support_artifact_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in support_artifacts
        },
        "failures": failures,
    }

    if args.write_receipt:
        (ROOT / "verification_receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(receipt, indent=2, sort_keys=True))
    if build.returncode != 0:
        print("\n--- lake build output ---\n" + build.stdout, file=sys.stderr)
    if audit.returncode != 0 or unexpected_axioms:
        print("\n--- axiom audit output ---\n" + audit.stdout, file=sys.stderr)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Kintsugi A0 Foundations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the deterministic, no-K2 foundation for Kintsugi: freeze the execution base, preserve the repository's known test state as data, and add a standard-library validator shell with canonical hashing, safe paths, exact baseline comparison, stable diagnostics, and a truthful CLI.

**Architecture:** This is the first executable slice of the approved Kintsugi design. One read-only Python module owns canonical bytes, hash domains, safe repository paths, diagnostics, pytest collection/failure parsing, and the baseline command. Its contract is a checked-in JSON file. It does not yet create the Kintsugi schema, manifest, seam graph, owner repairs, `REC-A-108`, or review bundle; those receive separate plans after this slice passes.

**Tech Stack:** Python 3.11 standard library, `unittest`, pytest as the existing repository test runner, Git.

**Read first:** `docs/superpowers/specs/2026-07-11-kintsugi-formal-logic-design.md`, especially §§3, 14, and 16.

---

## Fixed boundary

- Expected canonical base: `454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22` on `main`.
- This plan modifies exactly four paths:
  - `09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json`
  - `09_TOOLS/02_COMPILERS/validate_kintsugi.py`
  - `09_TOOLS/02_COMPILERS/test_validate_kintsugi.py`
  - `09_TOOLS/02_COMPILERS/README.md`
- Do not modify `12_PUBLIC_SITE/`, any `90_ARCHIVE` subtree, or `91_COMPATIBILITY/`.
- Preserve the canonical checkout's pre-existing untracked public file at raw SHA-256 `db794ac3e1d91b9c4d9e92ef121ef016f128a3fb518df86d11b5dc0f5a8eec1c`.
- Preserve `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md` at raw SHA-256 `9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c`; it is historical provenance only.
- Preserve `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md` at raw SHA-256 `3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629`. It is immutable external/pre-program support and provenance only: not a Kintsugi phase receipt, claim owner, dependency, or authority. Its historical `PENDING_K2` lifecycle creates no K2 gate for Kintsugi.
- The frozen proof audit's human number does not identify the future Phase B receipt. That receipt is only typed ID `REC-B-109` at exact path `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md`; bare `109` has no authority. Phase B must add the design's exact two-row README route, mirroring the existing 108 compatibility rule.
- `/Users/Yves/.codex/attachments/ec649130-9018-4d89-a0f1-99b9e82f34b5/pasted-text.txt` is potential A0B support only at raw SHA-256 `2937faf077f58a49e3c5953d33c3413ea3108350f82c8166eaf54818cdb5ad73`. It is `[B/D]` external support, every finding starts `ALLEGED`, and its claimed counts are not proof. A0B may hash-pin and deduplicate it before `MAN-A-001` freezes; it is not an A0 input or A0 scope path.
- The Kintsugi program has no K2 approval, countersign, checkpoint, or veto gate.
- These plan/spec amendments are pre-rebase planning changes and are outside the A0 implementation diff. The A0 implementation scope remains exactly the four paths above, with a baseline of 19 collected nodes and five allowed failures.
- The validator is read-only and uses only the standard library.
- Use `apply_patch` for hand-authored files. Stage only the four paths above.
- If canonical `main` moves or a protected hash changes, stop before rebasing and write a concurrency addendum.

## Handoff sequence

This plan ends when the baseline CLI is green and committed. Then, one after the other:

1. `docs/superpowers/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md` will implement the complete JSON Schema, graph, ledger, manifest, renderer, and mutation engine.
2. `docs/superpowers/plans/2026-07-12-kintsugi-a1-owner-repairs-implementation.md` will freeze `MAN-A-001`, atomize the actual owner claims, and make owner-first repairs.
3. `docs/superpowers/plans/2026-07-12-kintsugi-a2-review-closure-implementation.md` will run independent reviews, mechanical closure, the immutable bundle, and receipt verification.

Those are not executable tasks here; their exact plans depend on artifacts produced by the preceding slice.
No handoff adds an extra K2 pause; the slices continue one after the other.

---

### Task 1: Freeze Canonical Concurrency and Reconfirm the Baseline

**Files:** Read-only verification.

- [ ] **Step 1: Verify canonical HEAD, branch, dirt, and protected bytes**

```bash
set -euo pipefail
CANON=/Users/Yves/Documents/01_EMERGENTISM
WT=/Users/Yves/Documents/.codex-worktrees/emergentism-kintsugi-formal-logic
EXPECTED=454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22

test "$(git -C "$CANON" rev-parse --abbrev-ref HEAD)" = main
test "$(git -C "$CANON" rev-parse HEAD)" = "$EXPECTED"
test "$(git -C "$CANON" status --porcelain=v1 --untracked-files=all)" = \
  "?? 12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md"
test "$(shasum -a 256 "$CANON/12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md" | awk '{print $1}')" = \
  db794ac3e1d91b9c4d9e92ef121ef016f128a3fb518df86d11b5dc0f5a8eec1c
test "$(shasum -a 256 "$CANON/11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md" | awk '{print $1}')" = \
  9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c
test "$(shasum -a 256 "$CANON/11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md" | awk '{print $1}')" = \
  3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629
```

Expected: exit 0 and no output.

- [ ] **Step 2: Rebase only after this plan/spec commit exists**

```bash
set -euo pipefail
WT=/Users/Yves/Documents/.codex-worktrees/emergentism-kintsugi-formal-logic
EXPECTED=454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22
git -C "$WT" rebase "$EXPECTED"
git -C "$WT" merge-base --is-ancestor "$EXPECTED" HEAD
test -z "$(git -C "$WT" show-ref --verify --hash refs/codex/kintsugi-a0-start 2>/dev/null)"
git -C "$WT" update-ref refs/codex/kintsugi-a0-start HEAD
```

Expected: every command exits 0 and the private ref freezes the exact post-rebase,
pre-implementation commit. On conflict, run `git -C "$WT" rebase --abort` and
stop; do not auto-resolve doctrine.

- [ ] **Step 3: Reconfirm the observed repository state**

```bash
WT=/Users/Yves/Documents/.codex-worktrees/emergentism-kintsugi-formal-logic
cd "$WT"
python3 -m pytest --collect-only -q
python3 -m pytest -q --tb=short
```

Expected: 19 collected nodes; the execution returns exactly five failures, 14 passes, and one warning. The five failing node IDs and signatures must equal the JSON contract in Task 2. If they differ, stop without writing the allowlist.

---

### Task 2: Add the Exact Baseline Contract and Failing Tests

**Files:**
- Create: `09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json`
- Create: `09_TOOLS/02_COMPILERS/test_validate_kintsugi.py`

- [ ] **Step 1: Add the immutable baseline JSON as canonical bytes**

The object below is shown pretty-printed for review. The file itself must be the
single-line canonical serialization plus one LF, with raw hash
`sha256:92bc13d84b0cee317f648af6b1589f507e23a227afb40da2d66fb94282017957`.
The tests reject the pretty form, any key/order substitution, or any alternate
command array.

```json
{
  "schemaVersion": "1.0.0",
  "baseCommit": "454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22",
  "command": ["python3", "-m", "pytest", "-q", "--tb=short"],
  "collectCommand": ["python3", "-m", "pytest", "--collect-only", "-q"],
  "collectedAtBaseline": 19,
  "baselineNodeIds": [
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_constrained_kernel_preserves_lower_law_support",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_default_run_has_perturbable_positive_costed_witness",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_export_is_deterministic_json",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_records_hashes_and_frozen_objects",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_negative_controls_reject_false_macro_constraint_witnesses",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_report_export_is_tier_honest_json",
    "09_TOOLS/01_SCRIPTS/test_cross_entity_receipt_traversal.py::test_traversal",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_strict_flags_unresolved_warnings",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_listings_have_titles",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_parse_index",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_passes",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_missing_file",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_hash_mismatch",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_flags_unindexed_file"
  ],
  "allowedFailures": [
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog",
      "exceptionType": "AssertionError",
      "requiredSignature": "discipline check failed:"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog",
      "exceptionType": "AssertionError",
      "requiredSignature": "assert 1 == 0"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings",
      "exceptionType": "AssertionError",
      "requiredSignature": "assert 1 == 0"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve",
      "exceptionType": "AssertionError",
      "requiredSignature": "00_SKYZAI_COM_PRODUCT_MANIFEST.md"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes",
      "exceptionType": "AssertionError",
      "requiredSignature": "09_K2_ROUTE_READINESS_RECEIPT.jsonld"
    }
  ]
}
```

Apply this exact one-line file content (followed by one LF):

```json
{"allowedFailures":[{"exceptionType":"AssertionError","nodeId":"09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog","requiredSignature":"discipline check failed:"},{"exceptionType":"AssertionError","nodeId":"09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog","requiredSignature":"assert 1 == 0"},{"exceptionType":"AssertionError","nodeId":"09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings","requiredSignature":"assert 1 == 0"},{"exceptionType":"AssertionError","nodeId":"09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve","requiredSignature":"00_SKYZAI_COM_PRODUCT_MANIFEST.md"},{"exceptionType":"AssertionError","nodeId":"09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes","requiredSignature":"09_K2_ROUTE_READINESS_RECEIPT.jsonld"}],"baseCommit":"454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22","baselineNodeIds":["03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_constrained_kernel_preserves_lower_law_support","03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_default_run_has_perturbable_positive_costed_witness","03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_export_is_deterministic_json","03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_records_hashes_and_frozen_objects","03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_negative_controls_reject_false_macro_constraint_witnesses","03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_report_export_is_tier_honest_json","09_TOOLS/01_SCRIPTS/test_cross_entity_receipt_traversal.py::test_traversal","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_strict_flags_unresolved_warnings","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_listings_have_titles","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve","09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes","09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_parse_index","09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_passes","09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_missing_file","09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_hash_mismatch","09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_flags_unindexed_file"],"collectCommand":["python3","-m","pytest","--collect-only","-q"],"collectedAtBaseline":19,"command":["python3","-m","pytest","-q","--tb=short"],"schemaVersion":"1.0.0"}
```

- [ ] **Step 2: Add the complete test module**

```python
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_kintsugi as v

ROOT = Path(__file__).resolve().parents[2]
COMPILER = Path(__file__).resolve().parent
CONTRACT_PATH = COMPILER / "kintsugi_baseline_failures.json"
ZERO = "0" * 40

EXPECTED_FAILURES = {
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog": ("AssertionError", "discipline check failed:"),
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog": ("AssertionError", "assert 1 == 0"),
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings": ("AssertionError", "assert 1 == 0"),
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve": ("AssertionError", "00_SKYZAI_COM_PRODUCT_MANIFEST.md"),
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes": ("AssertionError", "09_K2_ROUTE_READINESS_RECEIPT.jsonld"),
}
EXPECTED_CONTRACT_HASH = "sha256:92bc13d84b0cee317f648af6b1589f507e23a227afb40da2d66fb94282017957"

class PrimitiveTests(unittest.TestCase):
    def test_canonical_json_and_hash_domains(self):
        self.assertEqual(v.canonical_json_bytes({"b": 1, "a": "é"}), b'{"a":"\xc3\xa9","b":1}\n')
        self.assertEqual(v.raw_hash(b"x"), "sha256:" + hashlib.sha256(b"x").hexdigest())
        self.assertEqual(v.text_hash("a\r\nb\r"), v.text_hash("a\nb\n"))

    def test_safe_repo_path_accepts_relative_and_rejects_escape(self):
        self.assertEqual(v.safe_repo_path(ROOT, "09_TOOLS"), ROOT / "09_TOOLS")
        for bad in ("../escape", "/absolute", "a/../../escape", ""):
            with self.subTest(bad=bad), self.assertRaises(v.KintsugiError) as caught:
                v.safe_repo_path(ROOT, bad)
            self.assertEqual(caught.exception.code, "KIN-E-PATH")

class ParserTests(unittest.TestCase):
    def test_collect_parser_ignores_summary(self):
        text = "a/test_x.py::test_one\nb/test_y.py::T::test_two\n\n2 tests collected in 0.01s\n"
        self.assertEqual(v.parse_collected_nodes(text), {
            "a/test_x.py::test_one", "b/test_y.py::T::test_two",
        })

    def test_failure_parser_reads_short_summary(self):
        text = (
            "================ short test summary info ================\n"
            "FAILED a/test_x.py::test_one - AssertionError: boom\n"
            "FAILED b/test_y.py::test_two - ValueError: bad\n"
        )
        self.assertEqual(v.parse_pytest_failures(text), {
            "a/test_x.py::test_one": "AssertionError",
            "b/test_y.py::test_two": "ValueError",
        })

    def test_error_summary_is_not_treated_as_green(self):
        self.assertEqual(v.parse_pytest_errors("ERROR a/test_x.py::test_one - RuntimeError\n"), {
            "a/test_x.py::test_one",
        })

class ContractTests(unittest.TestCase):
    def test_checked_in_contract_is_exact(self):
        contract = v.load_contract(CONTRACT_PATH)
        self.assertEqual(contract["schemaVersion"], "1.0.0")
        self.assertEqual(contract["baseCommit"], "454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22")
        self.assertEqual(contract["collectedAtBaseline"], 19)
        self.assertEqual(contract["command"], ["python3", "-m", "pytest", "-q", "--tb=short"])
        self.assertEqual(contract["collectCommand"], ["python3", "-m", "pytest", "--collect-only", "-q"])
        self.assertEqual(len(contract["baselineNodeIds"]), 19)
        self.assertEqual(len(set(contract["baselineNodeIds"])), 19)
        self.assertEqual(CONTRACT_PATH.read_bytes(), v.canonical_json_bytes(contract))
        self.assertEqual(v.raw_hash(CONTRACT_PATH.read_bytes()), EXPECTED_CONTRACT_HASH)
        actual = {
            item["nodeId"]: (item["exceptionType"], item["requiredSignature"])
            for item in contract["allowedFailures"]
        }
        self.assertEqual(actual, EXPECTED_FAILURES)

    def test_contract_rejects_unknown_keys_and_duplicate_nodes(self):
        contract = tiny_contract()
        contract["extra"] = True
        with self.assertRaises(v.KintsugiError) as caught:
            v.validate_contract(contract)
        self.assertEqual(caught.exception.code, "KIN-E-BASELINE")
        contract = tiny_contract()
        contract["baselineNodeIds"].append("suite.py::test_one")
        with self.assertRaises(v.KintsugiError):
            v.validate_contract(contract)

    def test_contract_rejects_executable_command_substitution(self):
        contract = tiny_contract()
        contract["command"] = ["touch", "/tmp/should-not-run"]
        with self.assertRaises(v.KintsugiError) as caught:
            v.validate_contract(contract)
        self.assertEqual(caught.exception.code, "KIN-E-BASELINE")

class ComparisonTests(unittest.TestCase):
    def test_missing_node_new_failure_type_and_signature_drift_fail(self):
        contract = tiny_contract()
        issues = v.compare_baseline(contract, set(), {}, {})
        self.assertIn("KIN-E-BASELINE", {item.code for item in issues})
        issues = v.compare_baseline(
            contract,
            {"suite.py::test_one"},
            {"suite.py::test_new": "AssertionError"},
            {"suite.py::test_new": "boom"},
        )
        self.assertIn("KIN-E-BASELINE", {item.code for item in issues})
        issues = v.compare_baseline(
            contract,
            {"suite.py::test_one"},
            {"suite.py::test_one": "ValueError"},
            {"suite.py::test_one": "different"},
        )
        self.assertEqual([item.code for item in issues], ["KIN-E-BASELINE", "KIN-E-BASELINE"])

    def test_passing_old_failure_is_allowed(self):
        self.assertEqual(v.compare_baseline(
            tiny_contract(), {"suite.py::test_one"}, {}, {},
        ), [])

class RunnerTests(unittest.TestCase):
    @mock.patch.object(v.subprocess, "run")
    def test_runner_uses_collect_full_and_isolated_commands(self, run):
        run.side_effect = [
            subprocess.CompletedProcess([], 0, "suite.py::test_one\n1 test collected\n", ""),
            subprocess.CompletedProcess([], 1, "FAILED suite.py::test_one - AssertionError: expected\n", ""),
            subprocess.CompletedProcess([], 1, "E   AssertionError: expected\n", ""),
        ]
        result = v.run_baseline(ROOT, tiny_contract())
        self.assertEqual(result, v.BaselineResult(1, 1, ()))
        self.assertEqual(run.call_count, 3)
        self.assertEqual(run.call_args_list[2].args[0][-1], "suite.py::test_one")

    @mock.patch.object(v.subprocess, "run")
    def test_runtime_error_cannot_pass_as_green(self, run):
        run.side_effect = [
            subprocess.CompletedProcess([], 0, "suite.py::test_one\n1 test collected\n", ""),
            subprocess.CompletedProcess([], 1, "ERROR suite.py::test_one - RuntimeError\n", ""),
        ]
        result = v.run_baseline(ROOT, tiny_contract())
        self.assertEqual([issue.code for issue in result.issues], ["KIN-E-BASELINE"])
        self.assertEqual(run.call_count, 2)

class CliTests(unittest.TestCase):
    def test_bad_json_has_stable_failure_without_traceback(self):
        with tempfile.NamedTemporaryFile("w", dir=COMPILER, suffix=".json", delete=False) as handle:
            handle.write("{")
            path = Path(handle.name)
        relative = path.relative_to(ROOT).as_posix()
        try:
            observed = []
            for _ in range(2):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    code = v.main(["--check-baseline", "--contract", relative])
                observed.append((code, stdout.getvalue(), stderr.getvalue()))
            self.assertEqual(observed[0], observed[1])
            code, stdout, stderr = observed[0]
            self.assertEqual(code, 1)
            self.assertEqual(stdout, "")
            self.assertIn(f"KIN-ERROR {path} KIN-E-JSON:", stderr)
            self.assertNotIn("Traceback", stderr)
        finally:
            path.unlink()

    def test_argument_error_uses_exit_two_and_stable_format(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = v.main(["--unknown"])
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("KIN-ERROR CLI KIN-E-CLI:", stderr.getvalue())
        self.assertNotIn("usage:", stderr.getvalue())

    def test_unreadable_contract_uses_exit_two(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = v.main(["--check-baseline", "--contract", "09_TOOLS/02_COMPILERS/absent-kintsugi-contract.json"])
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("KIN-ERROR CLI KIN-E-IO:", stderr.getvalue())

def tiny_contract():
    return {
        "schemaVersion": "1.0.0",
        "baseCommit": ZERO,
        "command": ["python3", "-m", "pytest", "-q", "--tb=short"],
        "collectCommand": ["python3", "-m", "pytest", "--collect-only", "-q"],
        "collectedAtBaseline": 1,
        "baselineNodeIds": ["suite.py::test_one"],
        "allowedFailures": [{
            "nodeId": "suite.py::test_one",
            "exceptionType": "AssertionError",
            "requiredSignature": "expected",
        }],
    }

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests and observe the intended failure**

```bash
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
```

Expected: FAIL at import with `ModuleNotFoundError: No module named 'validate_kintsugi'`.

---

### Task 3: Implement the Complete Read-Only Foundation

**Files:**
- Create: `09_TOOLS/02_COMPILERS/validate_kintsugi.py`

- [ ] **Step 1: Add the complete validator module**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = "09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
FAILED_RE = re.compile(r"^FAILED (?P<node>\S+)(?: - (?P<detail>.*))?$")
ERROR_RE = re.compile(r"^ERROR (?P<node>\S+)(?: - .*)?$")
EXCEPTION_RE = re.compile(r"^E\s+(?P<exception>[A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception))(?::|$)")
BASELINE_COMMAND = ["python3", "-m", "pytest", "-q", "--tb=short"]
COLLECT_COMMAND = ["python3", "-m", "pytest", "--collect-only", "-q"]
EXIT_TWO_CODES = {"KIN-E-CLI", "KIN-E-IO"}

@dataclass(frozen=True, order=True)
class Issue:
    path: str
    code: str
    message: str

@dataclass(frozen=True)
class BaselineResult:
    collected: int
    failures: int
    issues: tuple[Issue, ...]

class KintsugiError(Exception):
    def __init__(self, code: str, path: str, message: str):
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message

def canonical_json_bytes(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise KintsugiError("KIN-E-CANONICAL", "json", str(exc)) from None
    return (rendered + "\n").encode("utf-8")

def raw_hash(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()

def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def text_hash(text: str) -> str:
    return "sha256-text-lf:" + hashlib.sha256(normalize_lf(text).encode("utf-8")).hexdigest()

def safe_repo_path(root: Path, relative: str) -> Path:
    if not relative or relative.startswith("/") or "\\" in relative:
        raise KintsugiError("KIN-E-PATH", relative or "<empty>", "path must be non-empty repository-relative POSIX")
    pure = PurePosixPath(relative)
    if any(part in ("", ".", "..") for part in pure.parts):
        raise KintsugiError("KIN-E-PATH", relative, "path contains a forbidden segment")
    candidate = (root / Path(*pure.parts)).resolve(strict=False)
    try:
        candidate.relative_to(root.resolve(strict=True))
    except ValueError:
        raise KintsugiError("KIN-E-PATH", relative, "path escapes repository root") from None
    return candidate

def load_contract(path: Path) -> dict[str, Any]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise KintsugiError("KIN-E-IO", str(path), str(exc)) from None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        if isinstance(exc, json.JSONDecodeError):
            detail = f"line {exc.lineno} column {exc.colno}: {exc.msg}"
        else:
            detail = str(exc)
        raise KintsugiError("KIN-E-JSON", str(path), detail) from None
    if payload != canonical_json_bytes(value):
        raise KintsugiError("KIN-E-CANONICAL", str(path), "JSON bytes are not canonical")
    validate_contract(value)
    return value

def validate_contract(value: Any) -> None:
    required = {
        "schemaVersion", "baseCommit", "command", "collectCommand",
        "collectedAtBaseline", "baselineNodeIds", "allowedFailures",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise KintsugiError("KIN-E-BASELINE", "contract", "contract keys differ from the fixed schema")
    if value["schemaVersion"] != "1.0.0" or not isinstance(value["baseCommit"], str) or not HASH_RE.fullmatch(value["baseCommit"]):
        raise KintsugiError("KIN-E-BASELINE", "contract", "invalid version or base commit")
    if value["command"] != BASELINE_COMMAND or value["collectCommand"] != COLLECT_COMMAND:
        raise KintsugiError("KIN-E-BASELINE", "commands", "baseline commands differ from fixed internal commands")
    nodes = value["baselineNodeIds"]
    if not isinstance(nodes, list) or not nodes or not all(isinstance(item, str) and "::" in item for item in nodes) or len(nodes) != len(set(nodes)):
        raise KintsugiError("KIN-E-BASELINE", "baselineNodeIds", "node IDs must be unique pytest node strings")
    if type(value["collectedAtBaseline"]) is not int or value["collectedAtBaseline"] != len(nodes):
        raise KintsugiError("KIN-E-BASELINE", "collectedAtBaseline", "count must equal baselineNodeIds length")
    failures = value["allowedFailures"]
    if not isinstance(failures, list):
        raise KintsugiError("KIN-E-BASELINE", "allowedFailures", "must be an array")
    failure_keys = {"nodeId", "exceptionType", "requiredSignature"}
    seen: set[str] = set()
    for index, item in enumerate(failures):
        if not isinstance(item, dict) or set(item) != failure_keys:
            raise KintsugiError("KIN-E-BASELINE", f"allowedFailures[{index}]", "invalid failure record")
        if item["nodeId"] not in nodes or item["nodeId"] in seen:
            raise KintsugiError("KIN-E-BASELINE", item["nodeId"], "failure node is absent or duplicated")
        if not all(isinstance(item[field], str) and item[field] for field in failure_keys):
            raise KintsugiError("KIN-E-BASELINE", item["nodeId"], "failure fields must be non-empty strings")
        seen.add(item["nodeId"])

def run_process(command: Sequence[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)

def parse_collected_nodes(output: str) -> set[str]:
    return {
        line.strip() for line in output.splitlines()
        if "::" in line and not line.startswith(("FAILED ", "ERROR "))
    }

def parse_failed_nodes(output: str) -> list[str]:
    nodes: list[str] = []
    for line in output.splitlines():
        match = FAILED_RE.match(line.strip())
        if match and match.group("node") not in nodes:
            nodes.append(match.group("node"))
    return nodes

def infer_exception(output: str) -> str:
    for line in output.splitlines():
        match = EXCEPTION_RE.match(line)
        if match:
            return match.group("exception").split(".")[-1]
    if any(line.startswith("E   assert") for line in output.splitlines()):
        return "AssertionError"
    return "UNKNOWN"

def parse_pytest_failures(output: str) -> dict[str, str]:
    failures: dict[str, str] = {}
    for line in output.splitlines():
        match = FAILED_RE.match(line.strip())
        if not match:
            continue
        detail = match.group("detail") or ""
        token = detail.split(":", 1)[0].split(" ", 1)[0]
        failures[match.group("node")] = token if token.endswith(("Error", "Exception")) else "UNKNOWN"
    return failures

def parse_pytest_errors(output: str) -> set[str]:
    return {
        match.group("node")
        for line in output.splitlines()
        if (match := ERROR_RE.match(line.strip()))
    }

def compare_baseline(contract: dict[str, Any], collected: set[str],
                     failures: dict[str, str], isolated_outputs: dict[str, str]) -> list[Issue]:
    issues: list[Issue] = []
    baseline = set(contract["baselineNodeIds"])
    allowed = {item["nodeId"]: item for item in contract["allowedFailures"]}
    for node in sorted(baseline - collected):
        issues.append(Issue(node, "KIN-E-BASELINE", "baseline node is missing or renamed"))
    for node, exception in sorted(failures.items()):
        record = allowed.get(node)
        if record is None:
            issues.append(Issue(node, "KIN-E-BASELINE", "new failing node is not allowlisted"))
            continue
        if exception != record["exceptionType"]:
            issues.append(Issue(node, "KIN-E-BASELINE", f"exception drift: {exception} != {record['exceptionType']}"))
        if record["requiredSignature"] not in isolated_outputs.get(node, ""):
            issues.append(Issue(node, "KIN-E-BASELINE", "required failure signature is absent"))
    return sorted(issues)

def run_baseline(root: Path, contract: dict[str, Any]) -> BaselineResult:
    collection = run_process(COLLECT_COMMAND, root)
    if collection.returncode != 0:
        issue = Issue("collectCommand", "KIN-E-BASELINE", "pytest collection command failed")
        return BaselineResult(0, 0, (issue,))
    collected = parse_collected_nodes(collection.stdout + collection.stderr)
    execution = run_process(BASELINE_COMMAND, root)
    combined = execution.stdout + execution.stderr
    failed_nodes = parse_failed_nodes(combined)
    error_nodes = parse_pytest_errors(combined)
    if execution.returncode not in (0, 1):
        issue = Issue("command", "KIN-E-BASELINE", f"pytest returned unexpected exit {execution.returncode}")
        return BaselineResult(len(collected), len(failed_nodes), (issue,))
    if error_nodes:
        issues = tuple(Issue(node, "KIN-E-BASELINE", "pytest runtime/collection error") for node in sorted(error_nodes))
        return BaselineResult(len(collected), len(failed_nodes), issues)
    if (execution.returncode == 0) != (not failed_nodes):
        issue = Issue("command", "KIN-E-BASELINE", "pytest exit code and failure summary disagree")
        return BaselineResult(len(collected), len(failed_nodes), (issue,))
    isolated: dict[str, str] = {}
    failures: dict[str, str] = {}
    for node in sorted(failed_nodes):
        probe = run_process(["python3", "-m", "pytest", "-q", "--tb=short", node], root)
        isolated[node] = probe.stdout + probe.stderr
        failures[node] = infer_exception(isolated[node])
    issues = compare_baseline(contract, collected, failures, isolated)
    return BaselineResult(len(collected), len(failures), tuple(issues))

class KintsugiArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise KintsugiError("KIN-E-CLI", "CLI", message)

def build_parser() -> argparse.ArgumentParser:
    parser = KintsugiArgumentParser(prog="validate_kintsugi.py", add_help=False)
    parser.add_argument("--check-baseline", action="store_true")
    parser.add_argument("--contract", default=DEFAULT_CONTRACT)
    parser.add_argument("--canonical-root", type=Path, default=ROOT)
    return parser

def emit_error(error: KintsugiError) -> None:
    print(f"KIN-ERROR {error.path} {error.code}: {error.message}", file=sys.stderr)

def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if not args.check_baseline:
            raise KintsugiError("KIN-E-CLI", "arguments", "--check-baseline is required in A0")
        contract_path = safe_repo_path(ROOT, args.contract)
        contract = load_contract(contract_path)
        root = args.canonical_root.resolve(strict=True)
        if not (root / ".git").exists():
            raise KintsugiError("KIN-E-PATH", str(root), "canonical root is not a Git checkout")
        result = run_baseline(root, contract)
        if result.issues:
            for issue in result.issues:
                emit_error(KintsugiError(issue.code, issue.path, issue.message))
            return 1
        print(f"KIN-OK baseline collected={result.collected} failures={result.failures}")
        return 0
    except KintsugiError as exc:
        if exc.code in EXIT_TWO_CODES:
            emit_error(KintsugiError(exc.code, "CLI", f"{exc.path}: {exc.message}"))
            return 2
        emit_error(exc)
        return 1
    except (OSError, subprocess.SubprocessError) as exc:
        emit_error(KintsugiError("KIN-E-IO", "CLI", str(exc)))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run focused tests**

```bash
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
```

Expected: all tests pass.

- [ ] **Step 3: Run syntax and deterministic-output checks**

```bash
python3 -m py_compile 09_TOOLS/02_COMPILERS/validate_kintsugi.py 09_TOOLS/02_COMPILERS/test_validate_kintsugi.py
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
```

Expected: exit 0. Deterministic failure bytes are asserted directly by
`test_bad_json_has_stable_failure_without_traceback`; unittest's variable
elapsed-time footer is not compared.

- [ ] **Step 4: Commit the foundation implementation**

```bash
git add 09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json 09_TOOLS/02_COMPILERS/validate_kintsugi.py 09_TOOLS/02_COMPILERS/test_validate_kintsugi.py
git diff --cached --check
git commit -m "feat(kintsugi): establish deterministic audit foundation"
```

---

### Task 4: Document, Exercise, and Freeze the A0 Handoff

**Files:**
- Modify: `09_TOOLS/02_COMPILERS/README.md`

- [ ] **Step 1: Add this exact README section**

~~~~markdown
## Kintsugi audit foundation

The read-only A0 validator freezes the known repository test state without treating existing failures as new truth:

```bash
set -euo pipefail
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

`kintsugi_baseline_failures.json` records 19 baseline node IDs and five exact failure signatures at `main@454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`. A previously failing node may turn green; a removed node, new failure, exception drift, or signature drift fails. The validator never writes files and has no K2 approval gate.
~~~~

Apply the block exactly; the outer tildes preserve the literal inner Bash fence.

- [ ] **Step 2: Run the real baseline CLI**

```bash
set -euo pipefail
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

Expected exact stdout:

```text
KIN-OK baseline collected=19 failures=5
```

Expected exit: 0. Stderr: empty.

- [ ] **Step 3: Verify scope and protected surfaces**

```bash
set -euo pipefail
CANON=/Users/Yves/Documents/01_EMERGENTISM
EXPECTED=454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22
PROTECTED=(
  00_META/90_ARCHIVE
  01_TELEOLOGY/90_ARCHIVE
  03_METHODOLOGY/90_ARCHIVE
  04_AXIOLOGY/90_ARCHIVE
  08_FRAMEWORK_SUPPORT/01_GOVERNANCE/90_ARCHIVE
  09_TOOLS/90_ARCHIVE
  11_UPLINK/90_ARCHIVE
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md
  12_PUBLIC_SITE
  90_ARCHIVE
  91_COMPATIBILITY
  91_COMPATIBILITY/01_FOUNDATIONS/02_THE_DERIVATION/90_ARCHIVE
)
test -z "$(git diff --name-only 454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22..HEAD -- "${PROTECTED[@]}")"
test -z "$(git status --porcelain=v1 --untracked-files=all -- "${PROTECTED[@]}")"
test "$(git -C "$CANON" rev-parse HEAD)" = "$EXPECTED"
test "$(git -C "$CANON" status --porcelain=v1 --untracked-files=all)" = \
  "?? 12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md"
test "$(shasum -a 256 "$CANON/12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md" | awk '{print $1}')" = \
  db794ac3e1d91b9c4d9e92ef121ef016f128a3fb518df86d11b5dc0f5a8eec1c
test "$(shasum -a 256 "$CANON/11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md" | awk '{print $1}')" = \
  9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c
test "$(shasum -a 256 "$CANON/11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md" | awk '{print $1}')" = \
  3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629
test "$(shasum -a 256 11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md | awk '{print $1}')" = \
  9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c
test "$(shasum -a 256 11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md | awk '{print $1}')" = \
  3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629
git diff --check
```

Expected: no protected diff and no whitespace errors.

- [ ] **Step 4: Commit documentation and run final verification**

```bash
set -euo pipefail
git add 09_TOOLS/02_COMPILERS/README.md
git diff --cached --check
git commit -m "docs(kintsugi): document the A0 baseline gate"

python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check-baseline --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -B - <<'PY'
import subprocess

expected = [
    "09_TOOLS/02_COMPILERS/README.md",
    "09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json",
    "09_TOOLS/02_COMPILERS/test_validate_kintsugi.py",
    "09_TOOLS/02_COMPILERS/validate_kintsugi.py",
]
actual = sorted(subprocess.run(
    ["git", "diff", "--name-only", "refs/codex/kintsugi-a0-start..HEAD"],
    check=True, text=True, capture_output=True,
).stdout.splitlines())
if actual != expected:
    raise SystemExit(f"A0 scope mismatch: {actual!r}")
print("A0-SCOPE-OK paths=4")
PY
git update-ref -d refs/codex/kintsugi-a0-start
test -z "$(git status --short)"
```

Expected: tests pass; CLI prints `KIN-OK baseline collected=19 failures=5`; status contains no uncommitted implementation paths.

---

## A0 Acceptance Checklist

- [ ] Execution branch descends from exact canonical `main@454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`.
- [ ] Protected public, predecessor-receipt 108, and pre-program proof-audit 109 bytes are unchanged.
- [ ] The baseline contract deep-equals the approved 19-node/five-failure data.
- [ ] Canonical JSON, raw hash, normalized text hash, and safe path tests pass.
- [ ] Missing nodes, new failures, exception drift, and signature drift fail deterministically.
- [ ] Old allowlisted failures may turn green without becoming required failures.
- [ ] Failure output is sorted, stderr-only, and contains no traceback.
- [ ] Real baseline returns `KIN-OK baseline collected=19 failures=5`.
- [ ] Exactly the four declared A0 paths changed.
- [ ] The pre-rebase plan/spec amendment commit is excluded from the four-path A0 implementation diff.
- [ ] No K2 gate was introduced.

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

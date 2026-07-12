from __future__ import annotations

import contextlib
import hashlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kintsugi_kernel as kernel
import validate_kintsugi as facade


ROOT = Path(__file__).resolve().parents[2]
COMPILER = Path(__file__).resolve().parent
TEST_VALIDATE_HASH = "9ca7f87ba8f37f7648bea7ac961e0cea1dcc85441ad4fde16a7ef457c296738a"
BASELINE_CONTRACT_HASH = "74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b"


class CompatibilityExtractionTests(unittest.TestCase):
    def test_frozen_a0_inputs_remain_byte_identical(self):
        expected = {
            "test_validate_kintsugi.py": TEST_VALIDATE_HASH,
            "kintsugi_baseline_failures.json": BASELINE_CONTRACT_HASH,
        }
        actual = {
            name: hashlib.sha256((COMPILER / name).read_bytes()).hexdigest()
            for name in expected
        }
        self.assertEqual(actual, expected)

    def test_package_and_facade_share_the_a0_compatibility_surface(self):
        names = (
            "Issue",
            "BaselineResult",
            "KintsugiError",
            "ROOT",
            "DEFAULT_CONTRACT",
            "HASH_RE",
            "FAILED_RE",
            "ERROR_RE",
            "EXCEPTION_RE",
            "BASELINE_COMMAND",
            "COLLECT_COMMAND",
            "EXIT_TWO_CODES",
            "PYTEST_ENV",
            "canonical_json_bytes",
            "raw_hash",
            "normalize_lf",
            "text_hash",
            "safe_repo_path",
            "load_contract",
            "validate_contract",
            "run_process",
            "parse_collected_nodes",
            "parse_failed_nodes",
            "parse_failed_node_lines",
            "parse_pytest_evidence",
            "infer_exception",
            "parse_pytest_failures",
            "parse_pytest_errors",
            "compare_baseline",
            "run_baseline",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertIs(getattr(facade, name), getattr(kernel, name))

    def test_facade_parser_retains_a0_flags_and_defaults(self):
        args = facade.build_parser().parse_args(["--check-baseline"])
        self.assertTrue(args.check_baseline)
        self.assertEqual(args.contract, facade.DEFAULT_CONTRACT)
        self.assertEqual(args.canonical_root, facade.ROOT)

    def test_facade_main_retains_a0_success_output_and_exit(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        result = facade.BaselineResult(19, 5, ())
        with mock.patch.object(facade, "run_baseline", return_value=result):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = facade.main([
                    "--check-baseline",
                    "--canonical-root",
                    str(ROOT),
                ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "KIN-OK baseline collected=19 failures=5\n")
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()

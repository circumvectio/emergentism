#!/usr/bin/env python3
"""Focused custody and provenance tests for run_benchmark.py."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
RUNNER_PATH = HERE / "run_benchmark.py"
spec = importlib.util.spec_from_file_location("r2_run_benchmark", RUNNER_PATH)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class R2RunnerCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in (
            "run_benchmark.py",
            "conditions.json",
            "scenarios_40_candidate.json",
            "BATTERY_FROZEN_SHA256.txt",
        ):
            shutil.copy2(HERE / name, self.root / name)

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, *args, out_name="transcripts.jsonl"):
        out = self.root / out_name
        result = subprocess.run(
            [sys.executable, str(self.root / "run_benchmark.py"), *map(str, args),
             "--out", str(out)],
            cwd=self.root, text=True, capture_output=True,
        )
        return result, out

    def dry_run_args(self):
        return (
            "--dry-run", "--models", "mock-model", "--conditions", "C0",
            "--limit", "1", "--no-controls",
        )

    def test_default_dry_run_binds_hashes_selection_and_response_model(self):
        result, out = self.invoke(*self.dry_run_args())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["run_class"], "NON_REGISTERED_DRY_RUN")
        self.assertEqual(row["requested_model"], "mock-model")
        self.assertEqual(row["response_models"], ["mock-model"])
        self.assertTrue(all(turn["response_model"] == "mock-model" for turn in row["turns"]))
        self.assertEqual(
            row["input_provenance"]["scenarios_sha256"],
            runner.FROZEN_SCENARIOS_SHA256,
        )
        self.assertEqual(
            row["input_provenance"]["conditions_sha256"],
            runner.FROZEN_CONDITIONS_SHA256,
        )
        self.assertEqual(row["run_provenance"]["models_requested"], ["mock-model"])
        self.assertEqual(row["run_provenance"]["conditions_selected"], ["C0"])
        self.assertEqual(row["run_provenance"]["adversarial_limit"], 1)
        self.assertFalse(row["run_provenance"]["controls_included"])
        self.assertTrue(row["run_provenance"]["dry_run"])

    def test_default_hash_mutation_refuses_before_output_in_all_modes(self):
        cases = (
            ("scenarios_40_candidate.json", "default scenarios hash drift"),
            ("conditions.json", "default conditions hash drift"),
        )
        for index, (name, expected) in enumerate(cases):
            with self.subTest(name=name):
                target = self.root / name
                original = target.read_bytes()
                target.write_bytes(original + b"\n")
                result, out = self.invoke(*self.dry_run_args(), out_name=f"mutated-{index}.jsonl")
                self.assertEqual(result.returncode, 2)
                self.assertIn(expected, result.stderr)
                self.assertFalse(out.exists())
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                target.write_bytes(original)

        target = self.root / "conditions.json"
        target.write_bytes(target.read_bytes() + b"\n")
        result, out = self.invoke(
            "--non-registered", "--models", "mock-model", "--conditions", "C0",
            "--limit", "1", "--no-controls", out_name="mutated-explicit.jsonl",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("default conditions hash drift", result.stderr)
        self.assertFalse(out.exists())

    def test_alternate_input_requires_non_registered_or_dry_run(self):
        alternate = self.root / "alternate-scenarios.json"
        shutil.copy2(self.root / "scenarios_40_candidate.json", alternate)
        result, out = self.invoke(
            "--scenarios", alternate, "--models", "mock-model", "--conditions", "C0",
            "--limit", "1", "--no-controls", out_name="alternate-refused.jsonl",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("alternate inputs require --non-registered", result.stderr)
        self.assertFalse(out.exists())

        result, out = self.invoke(
            "--dry-run", "--scenarios", alternate, "--models", "mock-model",
            "--conditions", "C0", "--limit", "1", "--no-controls",
            out_name="alternate-dry.jsonl",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        row = json.loads(out.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(row["run_class"], "NON_REGISTERED_DRY_RUN")
        self.assertFalse(row["input_provenance"]["registered_inputs"])
        self.assertEqual(
            row["input_provenance"]["input_mode"], "NON_REGISTERED_ALTERNATE_INPUTS"
        )

    def test_invalid_selection_refuses_before_client_or_output(self):
        cases = (
            (("--models", "mock-model", "--conditions", "C0,BOGUS", "--limit", "1"),
             "condition 'BOGUS' is missing"),
            (("--dry-run", "--models", "", "--conditions", "C0"),
             "at least one model must be selected"),
            (("--dry-run", "--models", "mock,mock", "--conditions", "C0"),
             "model selections must not contain duplicates"),
            (("--dry-run", "--models", "mock", "--conditions", "C0,C0"),
             "condition selections must not contain duplicates"),
            (("--dry-run", "--models", "mock", "--conditions", "C0", "--limit", "-1"),
             "--limit must be zero or a positive integer"),
        )
        for index, (args, expected) in enumerate(cases):
            with self.subTest(expected=expected):
                result, out = self.invoke(*args, out_name=f"invalid-{index}.jsonl")
                self.assertEqual(result.returncode, 2)
                self.assertIn(expected, result.stderr)
                self.assertFalse(out.exists())
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_freeze_metadata_matches_runtime_constants(self):
        recorded = {}
        for line in (HERE / "BATTERY_FROZEN_SHA256.txt").read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 64:
                recorded[parts[1]] = parts[0]
        self.assertEqual(recorded["conditions.json"], runner.FROZEN_CONDITIONS_SHA256)
        self.assertEqual(
            recorded["scenarios_40_candidate.json"], runner.FROZEN_SCENARIOS_SHA256
        )

    def test_exact_response_model_can_differ_from_requested_alias(self):
        class Message:
            content = []
            model = "resolved-model-2026-08-01"

        class Messages:
            def create(self, **kwargs):
                return Message()

        class Client:
            messages = Messages()

        transcript = runner.play_scenario(Client(), "requested-alias", "", ["hello"])
        self.assertEqual(transcript[0]["response_model"], "resolved-model-2026-08-01")


if __name__ == "__main__":
    print("R2 FROZEN-INPUT AND PROVENANCE CONTROLS", flush=True)
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path

from vesicle_macro_constraint import (
    DEFAULT_CONFIG,
    build_lower_kernel,
    build_constrained_kernel,
    freeze_manifest,
    macro_constraint_report,
    negative_control_suite,
    write_freeze_manifest,
    write_report,
)


class VesicleMacroConstraintTests(unittest.TestCase):
    def test_constrained_kernel_preserves_lower_law_support(self):
        lower = build_lower_kernel(DEFAULT_CONFIG)
        constrained = build_constrained_kernel(DEFAULT_CONFIG, lower)

        self.assertEqual(len(lower), DEFAULT_CONFIG.capacity + 1)
        self.assertEqual(len(constrained), DEFAULT_CONFIG.capacity + 1)

        for x in range(DEFAULT_CONFIG.capacity + 1):
            self.assertAlmostEqual(sum(lower[x]), 1.0, places=12)
            self.assertAlmostEqual(sum(constrained[x]), 1.0, places=12)
            for x_next, constrained_probability in enumerate(constrained[x]):
                if constrained_probability > DEFAULT_CONFIG.support_epsilon:
                    self.assertGreater(lower[x][x_next], DEFAULT_CONFIG.support_epsilon)

    def test_default_run_has_perturbable_positive_costed_witness(self):
        report = macro_constraint_report(DEFAULT_CONFIG)

        self.assertTrue(report["support_subset"])
        self.assertTrue(report["passes_macro_constraint"])
        self.assertGreater(report["perturbation_kl"], report["epsilon"])
        self.assertGreater(report["witness"]["ei_macro"], report["witness"]["ei_baseline"])
        self.assertGreater(report["witness"]["w_c"], 0.0)
        self.assertGreater(report["syntropy"]["syn_c"], 0.0)
        self.assertTrue(report["negative_controls"]["all_controls_reject"])

    def test_report_export_is_tier_honest_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "vesicle_macro_constraint_report.json"
            report = write_report(output, DEFAULT_CONFIG)

            parsed = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(parsed, report)
        self.assertEqual(parsed["evidence_tier"], "[B] toy-model receipt only; [C] for biology")
        self.assertIn("not biological evidence", parsed["claim_boundary"])
        self.assertIn("support(K_X^C) subset support(K_X)", parsed["closure"])
        self.assertIn("Cost_entropy_export", parsed["cost_ledger"])
        self.assertIn("negative_controls", parsed)

    def test_freeze_manifest_records_hashes_and_frozen_objects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "vesicle_macro_constraint_report.json"
            write_report(report_path, DEFAULT_CONFIG)

            manifest = freeze_manifest(report_path=report_path)

        self.assertEqual(manifest["manifest_version"], "macro-constraint-freeze-v1")
        self.assertEqual(manifest["evidence_tier"], "[B] toy-model receipt only; [C] for biology")
        self.assertEqual(manifest["report_witness"]["w_c"], "0.425356")
        self.assertEqual(manifest["report_witness"]["syn_c"], "0.785347")
        self.assertEqual(manifest["report_witness"]["perturbation_kl"], "0.141286")
        self.assertTrue(manifest["negative_controls"]["all_controls_reject"])
        self.assertIn("X", manifest["frozen_objects"])
        self.assertIn("K_X", manifest["frozen_objects"])
        self.assertIn("pi", manifest["frozen_objects"])
        self.assertIn("G_C", manifest["frozen_objects"])
        self.assertIn("Cost_C", manifest["frozen_objects"])
        self.assertIn("python3 -m unittest test_vesicle_macro_constraint.py", manifest["commands"])
        self.assertIn("vesicle_macro_constraint.py", manifest["file_hashes"])
        self.assertRegex(manifest["file_hashes"]["vesicle_macro_constraint.py"], r"^[0-9a-f]{64}$")
        self.assertRegex(manifest["report_sha256"], r"^[0-9a-f]{64}$")

    def test_freeze_manifest_export_is_deterministic_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "vesicle_macro_constraint_report.json"
            manifest_path = tmp_path / "FREEZE_MANIFEST.json"
            write_report(report_path, DEFAULT_CONFIG)

            manifest = write_freeze_manifest(manifest_path, report_path=report_path)
            parsed = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(parsed, manifest)
        self.assertEqual(list(parsed["file_hashes"].keys()), sorted(parsed["file_hashes"].keys()))

    def test_negative_controls_reject_false_macro_constraint_witnesses(self):
        controls = negative_control_suite(DEFAULT_CONFIG)

        self.assertFalse(controls["no_gate"]["passes_macro_constraint"])
        self.assertEqual(controls["no_gate"]["perturbation_kl"], "0.000000")
        self.assertLessEqual(float(controls["no_gate"]["w_c"]), 0.0)

        self.assertFalse(controls["high_cost"]["passes_macro_constraint"])
        self.assertGreater(float(controls["high_cost"]["ei_macro_minus_baseline"]), 0.0)
        self.assertLessEqual(float(controls["high_cost"]["w_c"]), 0.0)

        self.assertTrue(controls["forbidden_support"]["violation_detected"])
        self.assertTrue(controls["all_controls_reject"])


if __name__ == "__main__":
    unittest.main()

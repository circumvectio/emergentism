import json
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import asdict, replace
from io import StringIO
from pathlib import Path

from vesicle_macro_constraint import (
    COST_GATE_ALGORITHM_FIXTURE,
    DEFAULT_CONFIG,
    FreezeVerificationError,
    build_lower_kernel,
    build_constrained_kernel,
    freeze_manifest,
    main,
    macro_constraint_report,
    mutual_information_bits,
    negative_control_suite,
    verify_freeze_manifest,
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

    def test_default_run_reports_negative_fair_micro_witness(self):
        report = macro_constraint_report(DEFAULT_CONFIG)
        witness = report["witness"]

        self.assertTrue(report["support_subset"])
        self.assertFalse(report["passes_macro_constraint"])
        self.assertGreater(report["perturbation_kl"], report["epsilon"])
        self.assertAlmostEqual(witness["ei_macro"], 1.2350368019243483)
        self.assertAlmostEqual(witness["ei_micro_lower"], 1.341697164269043)
        self.assertAlmostEqual(witness["ei_micro_constrained"], 1.5915907712418638)
        self.assertEqual(witness["ei_micro_fair"], witness["ei_micro_constrained"])
        self.assertEqual(witness["ei_baseline"], witness["ei_micro_fair"])
        self.assertLess(witness["ei_macro"], witness["ei_baseline"])
        self.assertLess(report["syntropy"]["delta_effective_information"], 0.0)
        self.assertAlmostEqual(witness["w_c"], -0.4265539693175155)
        self.assertFalse(report["syntropy"]["gate"]["passes"])
        self.assertEqual(report["result"]["classification"], "negative")
        self.assertEqual(report["result"]["macro_claim_status"], "fails_and_contracts")
        self.assertFalse(report["result"]["derived_from"]["macro_constraint_gate"])
        self.assertFalse(report["result"]["derived_from"]["syntropy_gate"])
        self.assertTrue(report["negative_controls"]["all_controls_reject"])

    def test_mutual_information_algorithm_is_not_a_constant(self):
        identity = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        uninformative = [[0.2, 0.3, 0.5], [0.2, 0.3, 0.5], [0.2, 0.3, 0.5]]
        asymmetric = [[0.8, 0.2], [0.1, 0.9]]

        self.assertAlmostEqual(mutual_information_bits(identity), 1.584962500721156)
        self.assertAlmostEqual(mutual_information_bits(uninformative), 0.0)
        self.assertAlmostEqual(mutual_information_bits(asymmetric), 0.3973126097494865)

    def test_nondefault_positive_delta_fixture_isolates_cost_gate(self):
        low_cost_config = COST_GATE_ALGORITHM_FIXTURE
        high_cost_config = replace(low_cost_config, penalty_bits_model=0.5)
        low_report = macro_constraint_report(low_cost_config)
        high_report = macro_constraint_report(high_cost_config)

        low_config_without_model_cost = asdict(low_cost_config)
        high_config_without_model_cost = asdict(high_cost_config)
        low_config_without_model_cost.pop("penalty_bits_model")
        high_config_without_model_cost.pop("penalty_bits_model")
        self.assertEqual(low_config_without_model_cost, high_config_without_model_cost)

        for name in (
            "ei_macro",
            "ei_micro_lower",
            "ei_micro_constrained",
            "ei_micro_fair",
            "ei_baseline",
        ):
            self.assertEqual(low_report["witness"][name], high_report["witness"][name])

        delta_ei = low_report["syntropy"]["delta_effective_information"]
        self.assertAlmostEqual(low_report["witness"]["ei_macro"], 1.5617307289349305)
        self.assertAlmostEqual(low_report["witness"]["ei_micro_fair"], 1.371635499056061)
        self.assertAlmostEqual(delta_ei, 0.1900952298788694)
        self.assertEqual(delta_ei, high_report["syntropy"]["delta_effective_information"])

        self.assertAlmostEqual(low_report["witness"]["penalty_bits_c"], 0.035)
        self.assertAlmostEqual(high_report["witness"]["penalty_bits_c"], 0.53)
        self.assertAlmostEqual(low_report["witness"]["w_c"], 0.1550952298788694)
        self.assertAlmostEqual(high_report["witness"]["w_c"], -0.33990477012113063)
        for report in (low_report, high_report):
            self.assertAlmostEqual(
                report["witness"]["w_c"],
                report["syntropy"]["delta_effective_information"]
                - report["witness"]["penalty_bits_c"],
            )

        self.assertTrue(low_report["passes_macro_constraint"])
        self.assertTrue(low_report["syntropy"]["gate"]["passes"])
        self.assertEqual(low_report["result"]["classification"], "positive")
        self.assertEqual(low_report["result"]["macro_claim_status"], "passes_toy_witness")
        self.assertTrue(low_report["result"]["derived_from"]["macro_constraint_gate"])
        self.assertTrue(low_report["result"]["derived_from"]["syntropy_gate"])

        self.assertFalse(high_report["passes_macro_constraint"])
        self.assertFalse(high_report["syntropy"]["gate"]["passes"])
        self.assertEqual(high_report["result"]["classification"], "negative")
        self.assertEqual(high_report["result"]["macro_claim_status"], "fails_and_contracts")
        failed_macro_gates = {
            name
            for name, passes in high_report["macro_constraint_gate"].items()
            if name != "passes" and not passes
        }
        self.assertEqual(
            failed_macro_gates,
            {"penalty_within_budget", "w_c_positive"},
        )

    def test_report_export_is_tier_honest_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "vesicle_macro_constraint_report.json"
            report = write_report(output, DEFAULT_CONFIG)

            parsed = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(parsed, report)
        self.assertEqual(parsed["evidence_tier"], "[B] toy-model receipt only; [C] for biology")
        self.assertEqual(parsed["bundle_kind"], "post_result_reproducibility_bundle")
        self.assertEqual(parsed["preregistration_status"], "not_prospectively_preregistered")
        self.assertIn("post-result", parsed["claim_boundary"])
        self.assertIn("not biological evidence", parsed["claim_boundary"])
        self.assertIn("support(K_X^C) subset support(K_X)", parsed["closure"])
        self.assertEqual(parsed["cost_ledger"]["unit"], "bit_equivalent_penalty")
        self.assertEqual(
            parsed["cost_ledger"]["declaration_status"],
            "declared_post_result_toy_parameters",
        )
        self.assertIn("post-result toy bit penalties", parsed["cost_ledger"]["conversion_status"])
        self.assertIn("labor", parsed["cost_ledger"]["penalty_bits_by_component"])
        self.assertIn("entropy_export", parsed["cost_ledger"]["penalty_bits_by_component"])
        self.assertIn("negative_controls", parsed)

    def test_freeze_manifest_records_hashes_and_frozen_objects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "vesicle_macro_constraint_report.json"
            write_report(report_path, DEFAULT_CONFIG)

            manifest = freeze_manifest(report_path=report_path)

        self.assertEqual(manifest["manifest_version"], "macro-constraint-reproducibility-v3")
        self.assertEqual(manifest["bundle_kind"], "post_result_reproducibility_bundle")
        self.assertFalse(manifest["prospective_preregistration"])
        self.assertEqual(manifest["evidence_tier"], "[B] toy-model receipt only; [C] for biology")
        self.assertEqual(manifest["report_witness"]["ei_micro_lower"], "1.341697")
        self.assertEqual(manifest["report_witness"]["ei_micro_constrained"], "1.591591")
        self.assertEqual(manifest["report_witness"]["ei_micro_fair"], "1.591591")
        self.assertEqual(manifest["report_witness"]["delta_ei_c"], "-0.356554")
        self.assertEqual(manifest["report_witness"]["w_c"], "-0.426554")
        self.assertFalse(manifest["report_witness"]["syntropy_gate"])
        self.assertFalse(manifest["report_witness"]["passes_macro_constraint"])
        self.assertEqual(manifest["report_witness"]["classification"], "negative")
        self.assertEqual(manifest["report_witness"]["macro_claim_status"], "fails_and_contracts")
        self.assertEqual(manifest["report_witness"]["perturbation_kl"], "0.141286")
        self.assertTrue(manifest["negative_controls"]["all_controls_reject"])
        self.assertIn("X", manifest["frozen_objects"])
        self.assertIn("K_X", manifest["frozen_objects"])
        self.assertIn("pi", manifest["frozen_objects"])
        self.assertIn("G_C", manifest["frozen_objects"])
        self.assertIn("CostPenaltyBits_C", manifest["frozen_objects"])
        self.assertIn("python3 -m unittest test_vesicle_macro_constraint.py", manifest["commands"])
        self.assertIn("python3 vesicle_macro_constraint.py --check", manifest["commands"])
        self.assertIn("vesicle_macro_constraint.py", manifest["file_hashes"])
        self.assertRegex(manifest["file_hashes"]["vesicle_macro_constraint.py"], r"^[0-9a-f]{64}$")
        self.assertRegex(manifest["report_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            manifest["bindings"]["model"]["sha256"],
            manifest["file_hashes"]["vesicle_macro_constraint.py"],
        )
        self.assertRegex(manifest["bindings"]["config"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["bindings"]["report"]["sha256"], manifest["report_sha256"])

    def test_freeze_manifest_export_is_deterministic_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "vesicle_macro_constraint_report.json"
            manifest_path = tmp_path / "FREEZE_MANIFEST.json"
            write_report(report_path, DEFAULT_CONFIG)

            manifest = write_freeze_manifest(manifest_path, report_path=report_path)
            first_export = manifest_path.read_bytes()
            repeated_manifest = write_freeze_manifest(
                manifest_path,
                report_path=report_path,
            )
            second_export = manifest_path.read_bytes()
            parsed = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(parsed, manifest)
        self.assertEqual(repeated_manifest, manifest)
        self.assertEqual(second_export, first_export)
        self.assertEqual(list(parsed["file_hashes"].keys()), sorted(parsed["file_hashes"].keys()))

    def test_freeze_manifest_rejects_report_config_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "vesicle_macro_constraint_report.json"
            write_report(report_path, DEFAULT_CONFIG)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["config"]["capacity"] += 1
            report_path.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(FreezeVerificationError, "report/config mismatch"):
                freeze_manifest(report_path=report_path)

    def test_verification_api_rejects_manifest_tampering(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report_path = tmp_path / "vesicle_macro_constraint_report.json"
            manifest_path = tmp_path / "FREEZE_MANIFEST.json"
            write_report(report_path, DEFAULT_CONFIG)
            write_freeze_manifest(manifest_path, report_path=report_path)

            verification = verify_freeze_manifest(
                manifest_path=manifest_path,
                report_path=report_path,
            )
            self.assertTrue(verification["valid"])
            self.assertEqual(verification["macro_claim_status"], "fails_and_contracts")
            with redirect_stdout(StringIO()):
                check_status = main(
                    [
                        "--check",
                        "--report",
                        str(report_path),
                        "--manifest",
                        str(manifest_path),
                    ]
                )
            self.assertEqual(check_status, 0)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["bindings"]["config"]["sha256"] = "0" * 64
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(FreezeVerificationError, "manifest mismatch"):
                verify_freeze_manifest(
                    manifest_path=manifest_path,
                    report_path=report_path,
                )

    def test_negative_controls_reject_false_macro_constraint_witnesses(self):
        controls = negative_control_suite(DEFAULT_CONFIG)

        self.assertFalse(controls["no_gate"]["passes_macro_constraint"])
        self.assertEqual(controls["no_gate"]["perturbation_kl"], "0.000000")
        self.assertLessEqual(float(controls["no_gate"]["w_c"]), 0.0)

        self.assertFalse(controls["high_cost"]["passes_macro_constraint"])
        self.assertTrue(controls["high_cost"]["information_metrics_match"])
        self.assertTrue(controls["high_cost"]["isolates_cost_gate"])
        self.assertGreater(float(controls["high_cost"]["delta_ei_c"]), 0.0)
        self.assertTrue(controls["high_cost"]["low_cost"]["passes_macro_constraint"])
        self.assertEqual(controls["high_cost"]["low_cost"]["penalty_bits_c"], "0.035000")
        self.assertEqual(controls["high_cost"]["low_cost"]["w_c"], "0.155095")
        self.assertFalse(controls["high_cost"]["high_cost"]["passes_macro_constraint"])
        self.assertEqual(controls["high_cost"]["high_cost"]["penalty_bits_c"], "0.530000")
        self.assertEqual(controls["high_cost"]["high_cost"]["w_c"], "-0.339905")

        self.assertTrue(controls["forbidden_support"]["violation_detected"])
        self.assertTrue(controls["all_controls_reject"])


if __name__ == "__main__":
    unittest.main()

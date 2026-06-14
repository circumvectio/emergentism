import json
import tempfile
import unittest
from pathlib import Path

from vesicle_macro_constraint import (
    DEFAULT_CONFIG,
    build_lower_kernel,
    build_constrained_kernel,
    macro_constraint_report,
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
        self.assertGreater(report["perturbation_kl"], report["epsilon"])
        self.assertGreater(report["witness"]["ei_macro"], report["witness"]["ei_baseline"])
        self.assertGreater(report["witness"]["w_c"], 0.0)
        self.assertGreater(report["syntropy"]["syn_c"], 0.0)

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


if __name__ == "__main__":
    unittest.main()

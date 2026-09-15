"""Synthetic contract regressions; no empirical or execution validation."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import validate as v


class ExergyContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = v.load(v.HERE / "contract.json")
        self.record = v.load(v.HERE / "example.json")

    def check(self, record=None, previous=None):
        return v.validate(record or self.record, self.contract, previous)

    def reject(self, message, change):
        bad = copy.deepcopy(self.record)
        change(bad)
        with self.assertRaisesRegex(v.ContractError, message):
            self.check(bad)

    def product(self, left=0.8, right=0.5):
        self.record["assessment"] = {
            "mode": "experimental_product",
            "calibration": {
                "id": "synthetic-calibration", "version": "1",
                "context_sha256": v.digest(self.record["context"]),
                "bundle_sha256": v.bundle_digest(self.record),
                "scale": "cardinal", "units": "dimensionless",
                "evaluator_vmo": "Synthetic evaluator, not validated",
                "evaluator_ska": "Synthetic evaluator, not validated",
                "zeros": "Declared absence of capability under this toy model",
                "transformations": "Identity only for this toy calculation",
                "uncertainty": "No empirical calibration; numbers invented",
                "comparison_domain": "This synthetic example only",
                "evidence": ["synthetic-flow"]
            },
            "factors": {
                "VMO": {"value": left, "evidence": ["synthetic-flow"] if left is not None else []},
                "SKA": {"value": right, "evidence": ["synthetic-flow"] if right is not None else []}
            }
        }

    def test_example_preserves_unknown_and_failed(self):
        result = self.check()
        self.assertIsNone(result["experimental_candidate"])
        self.assertEqual(result["disposition"], "HOLD")
        self.assertFalse(result["may_execute"])
        self.assertFalse(result["empirical_validation"])
        self.assertIn("KPI flow: failed.", result["findings"])
        self.assertIn("KPI water-safety: unknown.", result["findings"])

    def test_source_pins_match(self):
        v.source_check(self.contract)

    def test_source_drift_fails(self):
        self.contract["source_pins"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(v.ContractError, "source drift"):
            v.source_check(self.contract)

    def test_source_pin_cannot_escape_repo(self):
        self.contract["source_pins"][0]["path"] = "../AGENTS.md"
        with self.assertRaisesRegex(v.ContractError, "escapes repository"):
            v.source_check(self.contract)

    def test_contract_version_rejected(self):
        self.contract["schema_version"] = "future-version"
        with self.assertRaisesRegex(v.ContractError, "unsupported contract version"):
            v.source_check(self.contract)

    def test_record_version_rejected(self):
        self.reject("unsupported record version", lambda r: r.update(schema_version="v2"))

    def test_unknown_fields_at_each_object_depth(self):
        def objects(node):
            if isinstance(node, dict):
                yield node
                for child in list(node.values()):
                    yield from objects(child)
            elif isinstance(node, list):
                for child in node:
                    yield from objects(child)
        for index in range(len(list(objects(self.record)))):
            bad = copy.deepcopy(self.record)
            list(objects(bad))[index]["may_execute"] = True
            with self.subTest(object=index), self.assertRaisesRegex(v.ContractError, "unknown fields"):
                self.check(bad)

    def test_default_mode_rejects_scalar(self):
        self.reject("no scalar operands", lambda r: r["assessment"].update(factors={"VMO": 1, "SKA": 1}))

    def test_product_is_bounded_arithmetic_not_permission(self):
        self.product()
        result = self.check()
        self.assertAlmostEqual(result["experimental_candidate"], 0.4)
        self.assertEqual(result["disposition"], "HOLD")
        self.assertFalse(result["may_execute"])
        self.assertFalse(result["empirical_validation"])

    def test_unknown_times_zero_stays_unknown(self):
        self.product(None, 0)
        self.assertIsNone(self.check()["experimental_candidate"])

    def test_known_zero_is_a_toy_model_zero(self):
        self.product(0, 0.8)
        self.assertEqual(self.check()["experimental_candidate"], 0)

    def test_product_rejects_ordinal_scale(self):
        self.product()
        self.reject("cardinal dimensionless", lambda r: r["assessment"]["calibration"].update(scale="ordinal"))

    def test_product_rejects_joules(self):
        self.product()
        self.reject("never joules", lambda r: r["assessment"]["calibration"].update(units="J"))

    def test_product_requires_calibration_evidence(self):
        self.product()
        self.reject("empty array", lambda r: r["assessment"]["calibration"].update(evidence=[]))

    def test_product_cannot_reuse_different_context(self):
        self.product()
        self.reject("context mismatch", lambda r: r["context"].update(horizon_end="2027-01-01T00:00:00Z"))

    def test_changed_strategy_invalidates_product_factors(self):
        self.product()
        self.reject("bundle mismatch", lambda r: r["ska"]["strategies"][0].update(policy="Replace instead of inspect."))

    def test_boolean_nan_infinity_and_out_of_domain(self):
        for value in (True, float("nan"), float("inf"), -0.1, 1.1, "0.5"):
            self.product(value, 0.5)
            with self.subTest(value=value), self.assertRaises(v.ContractError):
                self.check()

    def test_ordinal_recoding_counterexample_still_reverses_product(self):
        a, b = (0.9, 0.2), (0.4, 0.4)
        f = {0.2: 0.01, 0.4: 0.5, 0.9: 0.9}
        self.assertGreater(a[0] * a[1], b[0] * b[1])
        self.assertLess(f[a[0]] * f[a[1]], f[b[0]] * f[b[1]])
        self.assertLess(min(a), min(b))
        self.assertLess(min(map(f.get, a)), min(map(f.get, b)))

    def test_min_is_not_invariant_under_independent_recodings(self):
        a, b = (0.9, 0.2), (0.4, 0.4)
        f_left = {0.4: 0.01, 0.9: 0.9}
        self.assertLess(min(a), min(b))
        self.assertGreater(min(f_left[a[0]], a[1]), min(f_left[b[0]], b[1]))

    def test_vision_cannot_claim_physical_cone(self):
        self.reject("not a physical light cone", lambda r: r["vmo"]["vision"].update(cone_type="physical_light_cone"))

    def test_supported_trajectory_needs_evidence(self):
        self.reject("empty array", lambda r: r["vmo"]["mission"]["trajectories"][0].update(status="supported"))

    def test_supported_dependency_needs_evidence(self):
        self.reject("empty array", lambda r: r["ska"]["strategies"][0]["dependencies"][0].update(status="supported"))

    def test_unknown_reference_rejected(self):
        self.reject("unresolved evidence", lambda r: r["ska"]["kpis"][0].update(evidence=["missing"]))

    def test_duplicate_ids_do_not_enlarge_option_space(self):
        self.reject("duplicate object id", lambda r: r["vmo"]["mission"]["trajectories"].append(copy.deepcopy(r["vmo"]["mission"]["trajectories"][0])))

    def test_more_descriptions_produce_no_default_score(self):
        self.record["vmo"]["mission"]["trajectories"].append({
            "id": "repair-reworded", "description": "Another wording of repair",
            "status": "imagined", "evidence": []})
        self.assertIsNone(self.check()["experimental_candidate"])

    def test_unknown_agent_and_unpaired_objective_rejected(self):
        self.reject("unknown agent", lambda r: r["ska"]["strategies"][0].update(agent_ids=["ghost"]))
        self.reject("strategy mapping", lambda r: r["vmo"]["objectives"].append({
            "id": "orphan", "trajectory_id": "replace", "description": "No implementation", "kpi_ids": ["flow"]}))

    def test_boolean_measurement_rejected(self):
        self.reject("finite number", lambda r: r["ska"]["kpis"][0].update(value=True))

    def test_huge_integer_is_bounded_failure(self):
        self.reject("supported range", lambda r: r["ska"]["kpis"][0].update(threshold=10 ** 1000))

    def test_unknown_is_not_zero_or_success(self):
        self.reject("masquerade", lambda r: r["ska"]["kpis"][1].update(value=0))
        self.reject("contradicts threshold", lambda r: r["ska"]["kpis"][0].update(status="met"))

    def test_stale_and_future_kpis_rejected(self):
        self.reject("future-dated or stale", lambda r: r["ska"]["kpis"][0].update(expires_at="2026-09-15T10:00:00Z"))
        self.reject("future-dated or stale", lambda r: r["ska"]["kpis"][0].update(observed_at="2026-09-16T10:00:00Z"))

    def test_horizon_order_and_timezone(self):
        self.reject("review horizon", lambda r: r["context"].update(review_at="2026-11-01T00:00:00Z"))
        self.reject("timezone required", lambda r: r["context"].update(as_of="2026-09-15T10:00:00"))

    def test_missing_bearer_and_combined_ledgers_rejected(self):
        self.reject("missing bearer", lambda r: r["guardrails"]["bearers"].pop())
        self.reject("unknown fields", lambda r: r["guardrails"]["ledgers"].update(entropy=0))

    def test_declared_permission_still_never_executes(self):
        g = self.record["guardrails"]
        g.update(authorization="documented", authorization_evidence=["synthetic-flow"],
                 justice="reviewed", justice_evidence=["synthetic-flow"])
        result = self.check()
        self.assertEqual(result["disposition"], "REVIEW_ONLY")
        self.assertFalse(result["may_execute"])
        self.reject("no signing", lambda r: r["ska"]["agents"][0].update(may_authorize=True))

    def test_failed_kpi_can_revise_strategy_without_erasing_observation(self):
        previous = copy.deepcopy(self.record)
        self.record["id"] = "synthetic-clinic-r2"
        self.record["ska"]["strategies"][0]["policy"] = "Propose leak inspection before pump replacement."
        self.record["revision"] = {"parent_id": previous["id"], "changed_fields": ["strategies"],
                                   "reason": "Flow fell below the predeclared waypoint.", "evidence": ["synthetic-flow"]}
        self.assertTrue(self.check(previous=previous)["revision_link_checked"])
        self.assertEqual(self.record["ska"]["kpis"], previous["ska"]["kpis"])
        self.record["vmo"]["vision"]["statement"] = "Only volume matters now."
        with self.assertRaisesRegex(v.ContractError, "changes mismatch"):
            self.check(previous=previous)

    def test_missing_parent_and_evidence_rewrite_rejected(self):
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["strategies"],
                                   "reason": "Test", "evidence": ["synthetic-flow"]}
        with self.assertRaisesRegex(v.ContractError, "requires exactly"):
            self.check()
        self.record["evidence"][0]["limitations"] = "Pretend this was independently observed."
        with self.assertRaisesRegex(v.ContractError, "rewrote prior evidence"):
            self.check(previous=old)

    def test_lowering_target_cannot_turn_old_failure_into_new_success(self):
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["ska"]["kpis"][0].update(threshold=50, status="met")
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["kpis"],
                                   "reason": "Lower proposed future target", "evidence": ["synthetic-flow"]}
        with self.assertRaisesRegex(v.ContractError, "fresh observation or unknown"):
            self.check(previous=old)
        self.record["ska"]["kpis"][0].update(value=None, status="unknown", observed_at=None, expires_at=None)
        self.assertTrue(self.check(previous=old)["revision_link_checked"])

    def test_renaming_kpi_does_not_launder_same_observation(self):
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["ska"]["kpis"][0].update(id="flow-new", threshold=50, status="met")
        self.record["vmo"]["objectives"][0]["kpi_ids"][0] = "flow-new"
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["kpis", "objectives"],
                                   "reason": "Rename and lower criterion", "evidence": ["synthetic-flow"]}
        with self.assertRaisesRegex(v.ContractError, "fresh observation or unknown"):
            self.check(previous=old)

    def test_shared_observation_with_unchanged_upper_lower_bounds(self):
        upper = copy.deepcopy(self.record["ska"]["kpis"][0])
        upper.update(id="flow-upper", threshold=200, comparator="le", status="met")
        self.record["ska"]["kpis"].append(upper)
        self.record["vmo"]["objectives"][0]["kpi_ids"].append("flow-upper")
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["ska"]["strategies"][0]["policy"] = "Propose leak inspection."
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["strategies"],
                                   "reason": "Lower bound failed; upper bound still holds.", "evidence": ["synthetic-flow"]}
        self.assertTrue(self.check(previous=old)["revision_link_checked"])

    def test_rename_only_with_shared_observation_is_valid(self):
        upper = copy.deepcopy(self.record["ska"]["kpis"][0])
        upper.update(id="flow-upper", threshold=200, comparator="le", status="met")
        self.record["ska"]["kpis"].append(upper)
        self.record["vmo"]["objectives"][0]["kpi_ids"].append("flow-upper")
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["ska"]["kpis"][0]["id"] = "flow-lower-bound"
        self.record["vmo"]["objectives"][0]["kpi_ids"][0] = "flow-lower-bound"
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["kpis", "objectives"],
                                   "reason": "Clarify KPI label; criterion and observation unchanged.", "evidence": ["synthetic-flow"]}
        self.assertTrue(self.check(previous=old)["revision_link_checked"])

    def test_reused_observation_cannot_change_value_silently(self):
        old = copy.deepcopy(self.record)
        self.record["id"] = "r2"
        self.record["ska"]["kpis"][0].update(value=120, status="met")
        self.record["revision"] = {"parent_id": old["id"], "changed_fields": ["kpis"],
                                   "reason": "Pretend failure became success.", "evidence": ["synthetic-flow"]}
        with self.assertRaisesRegex(v.ContractError, "same observation"):
            self.check(previous=old)

    def test_error_cli_also_declares_no_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            self.record["ska"]["kpis"][0]["threshold"] = 10 ** 1000
            path.write_text(json.dumps(self.record))
            result = subprocess.run([sys.executable, "-B", str(v.HERE / "validate.py"), str(path)],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stderr, "")
            output = json.loads(result.stdout)
            self.assertFalse(output["empirical_validation"])
            self.assertFalse(output["may_execute"])

    def test_duplicate_json_keys_and_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            for raw in ('{"id":1,"id":2}', '{"value":NaN}', '{"value":Infinity}'):
                path.write_text(raw)
                with self.subTest(raw=raw), self.assertRaises(v.ContractError):
                    v.load(path)

    def test_validation_does_not_write_or_network(self):
        with patch("builtins.open", side_effect=AssertionError("no writes")), patch("socket.socket", side_effect=AssertionError("no network")):
            self.check()

    def test_cli_repeated_checks_deterministic(self):
        command = [sys.executable, "-B", str(v.HERE / "validate.py"), "--check"]
        first = subprocess.run(command, capture_output=True, text=True, check=True)
        second = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertFalse(json.loads(first.stdout)["may_execute"])


if __name__ == "__main__":
    unittest.main()

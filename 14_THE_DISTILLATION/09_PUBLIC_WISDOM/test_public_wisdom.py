from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("public_wisdom_builder", HERE / "build_public_wisdom.py")
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class PublicWisdomContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {name: BUILDER.load_json(path) for name, path in BUILDER.SCHEMAS.items()}
        cls.manifest = BUILDER.load_json(BUILDER.PATHS["manifest"])
        cls.stack = BUILDER.load_json(BUILDER.PATHS["stack"])
        cls.record_set = BUILDER.load_json(BUILDER.PATHS["records"])
        cls.card_set = BUILDER.load_json(BUILDER.PATHS["cards"])
        cls.ledger = BUILDER.load_json(BUILDER.PATHS["ledger"])
        cls.source_ids = BUILDER.validate_source_manifest(cls.manifest, verify_git=True)

    def test_complete_packet_validates_and_compiles(self) -> None:
        bundle = BUILDER.load_and_validate(verify_git=True)
        compiled = BUILDER.compile_corpus(bundle)
        self.assertEqual(compiled["supported_wisdom"], 0)
        self.assertEqual(compiled["supported_count_is_derived"], 0)
        self.assertFalse(compiled["public_is_truth_rung"])
        self.assertEqual(compiled["external_states"]["product_adoptions"], 0)

    def test_generation_is_deterministic(self) -> None:
        bundle = BUILDER.load_and_validate(verify_git=False)
        first = BUILDER.pretty(BUILDER.compile_corpus(bundle))
        second = BUILDER.pretty(BUILDER.compile_corpus(bundle))
        self.assertEqual(first, second)

    def test_public_cannot_become_a_stage(self) -> None:
        stack = deepcopy(self.stack)
        stack["stages"][-1]["name"] = "Public"
        with self.assertRaisesRegex(BUILDER.ContractError, "outside enum|stage order|projection"):
            BUILDER.validate_stack(stack, self.schemas["stack"])

    def test_non_adjacent_promotion_is_rejected(self) -> None:
        stack = deepcopy(self.stack)
        stack["promotions"][0]["to"] = "ES-3"
        with self.assertRaisesRegex(BUILDER.ContractError, "adjacent"):
            BUILDER.validate_stack(stack, self.schemas["stack"])

    def test_supported_without_independent_outcome_is_rejected(self) -> None:
        records = deepcopy(self.record_set)
        records["records"][0]["maturity"] = "SUPPORTED"
        with self.assertRaisesRegex(BUILDER.ContractError, "not integrated support"):
            BUILDER.validate_records(records, self.schemas["record"], self.source_ids)

    def test_receipt_or_agent_agreement_is_not_an_outcome(self) -> None:
        for kind in ("EXECUTION_RECEIPT", "AGENT_AGREEMENT"):
            records = deepcopy(self.record_set)
            row = records["records"][0]
            row["maturity"] = "SUPPORTED"
            row["supported_by_outcome_count"] = 1
            row["outcomes"] = [{
                "outcome_id": "OUT-1",
                "kind": kind,
                "independent_provenance": "self report",
                "metric": "none",
                "result": "claimed pass",
                "source_id": "SRC-EM-METHOD"
            }]
            with self.assertRaisesRegex(BUILDER.ContractError, "not outcomes"):
                BUILDER.validate_records(records, self.schemas["record"], self.source_ids)

    def test_lighting_does_not_promote_maturity(self) -> None:
        records = deepcopy(self.record_set)
        records["records"][0]["projection"] = "LIT"
        validated = BUILDER.validate_records(records, self.schemas["record"], self.source_ids)
        self.assertEqual(validated[0]["maturity"], "PROVISIONAL")

    def test_status_container_value_is_not_a_status(self) -> None:
        records = deepcopy(self.record_set)
        records["records"][0]["maturity"] = "STATUS=SUPPORTED"
        with self.assertRaisesRegex(BUILDER.ContractError, "outside enum"):
            BUILDER.validate_records(records, self.schemas["record"], self.source_ids)

    def test_correction_cannot_overwrite_or_resurrect_itself(self) -> None:
        records = deepcopy(self.record_set)
        row = records["records"][0]
        row["projection"] = "CORRECTED"
        row["corrections"] = [{"note": "silent mutation"}]
        row["lineage"]["correction_of"] = row["stable_id"]
        with self.assertRaisesRegex(BUILDER.ContractError, "cannot point to itself"):
            BUILDER.validate_records(records, self.schemas["record"], self.source_ids)

    def test_product_candidate_cannot_adopt_itself(self) -> None:
        cards = deepcopy(self.card_set)
        cards["cards"][1]["adoption_state"] = "ADOPTED_IN_EMERGENTISM"
        with self.assertRaisesRegex(BUILDER.ContractError, "cannot promote or adopt itself"):
            BUILDER.validate_cards(cards, self.schemas["card"], self.source_ids)

    def test_uncommitted_or_wrong_hash_source_is_rejected(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(BUILDER.ContractError, "committed source digest drift"):
            BUILDER.validate_source_manifest(manifest, verify_git=True)

    def test_worktree_carrier_is_rejected_as_source(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["sources"][0]["path"] = ".codex-worktrees/replay/source.md"
        with self.assertRaisesRegex(BUILDER.ContractError, "not custody"):
            BUILDER.validate_source_manifest(manifest, verify_git=False)

    def test_coverage_counts_and_zero_unclassified_are_exact(self) -> None:
        cards = BUILDER.validate_cards(self.card_set, self.schemas["card"], self.source_ids)
        ledger = deepcopy(self.ledger)
        ledger["counts"]["CANDIDATE_ONLY"] += 1
        with self.assertRaisesRegex(BUILDER.ContractError, "coverage counts drift"):
            BUILDER.validate_ledger(ledger, self.schemas["ledger"], self.source_ids, cards)


if __name__ == "__main__":
    unittest.main()

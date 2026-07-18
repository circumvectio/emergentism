from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path


COMPILER = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(COMPILER))

from kintsugi_kernel.baseline import (  # noqa: E402
    COLLECT_COMMAND,
    load_contract,
    parse_collected_nodes,
    run_process,
)


CONTRACT = COMPILER / "kintsugi_lineage_baseline_failures.json"
LEGACY_CONTRACT = COMPILER / "kintsugi_baseline_failures.json"
BASE_COMMIT = "bb9a4fc84854d00df5ac5a67dcfa83adca59fc78"
CONTRACT_SHA256 = "a97641705e8156b1a0f62a26ff01908a49548b69f794124275383b36aab13160"
LEGACY_SHA256 = "74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b"
BASELINE_PATHS = (
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py",
    "09_TOOLS/01_SCRIPTS/test_cross_entity_receipt_traversal.py",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py",
)


class LineageBaselineContractTests(unittest.TestCase):
    def test_contract_is_canonical_and_preserves_the_immutable_a0_contract(self):
        contract = load_contract(CONTRACT)

        self.assertEqual(contract["baseCommit"], BASE_COMMIT)
        self.assertEqual(contract["collectedAtBaseline"], 23)
        self.assertEqual(len(contract["baselineNodeIds"]), 23)
        self.assertEqual(len(contract["allowedFailures"]), 5)
        self.assertEqual(hashlib.sha256(CONTRACT.read_bytes()).hexdigest(), CONTRACT_SHA256)
        self.assertEqual(
            hashlib.sha256(LEGACY_CONTRACT.read_bytes()).hexdigest(),
            LEGACY_SHA256,
        )

    def test_frozen_paths_match_the_declared_lineage_commit(self):
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_COMMIT, "HEAD"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(ancestor.returncode, 0)

        drift = subprocess.run(
            ["git", "diff", "--quiet", BASE_COMMIT, "--", *BASELINE_PATHS],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(drift.returncode, 0)

    def test_contract_nodes_equal_the_selected_lineage_collection(self):
        contract = load_contract(CONTRACT)
        collection = run_process([*COLLECT_COMMAND, *BASELINE_PATHS], ROOT)

        self.assertEqual(collection.returncode, 0, collection.stderr)
        self.assertEqual(
            parse_collected_nodes(collection.stdout + collection.stderr),
            set(contract["baselineNodeIds"]),
        )


if __name__ == "__main__":
    unittest.main()

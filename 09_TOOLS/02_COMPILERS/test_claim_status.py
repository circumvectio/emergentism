from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_claim_status.py"
SPEC = importlib.util.spec_from_file_location("check_claim_status", MODULE_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ClaimStatusContractTests(unittest.TestCase):
    def make_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "corpus"
        for rel in (
            CHECKER.STATUS_PATH,
            CHECKER.HUMAN_OWNER,
            CHECKER.CONJECTURES,
            CHECKER.RECORD_LEDGER,
            Path(CHECKER.EXPECTED_AUTHORIZATION),
        ):
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, target)
        return temp, root

    def mutate(self, root: Path, fn) -> None:
        path = root / CHECKER.STATUS_PATH
        document = json.loads(path.read_text(encoding="utf-8"))
        fn(document)
        path.write_text(json.dumps(document), encoding="utf-8")

    def test_corrected_baseline_passes(self) -> None:
        self.assertEqual(CHECKER.check(ROOT), [])

    def test_no_live_status_can_thaw_a_grave(self) -> None:
        for status in ("OWNER-REOPENED", "NARROWED", "OPEN-FORMAL"):
            with self.subTest(status=status):
                temp, root = self.make_fixture()
                try:
                    self.mutate(root, lambda d: d["graves"][0].update(status=status))
                    errors = CHECKER.check(root)
                    self.assertTrue(any("must retain a terminal status" in e for e in errors), errors)
                finally:
                    temp.cleanup()

    def test_pinned_terminal_status_cannot_be_relabelled(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["graves"][0].update(status="CATEGORY-ERROR"))
        self.assertTrue(any("terminal status drifted" in e for e in CHECKER.check(root)))

    def test_df14_is_terminal_with_separate_narrowed_disposition(self) -> None:
        document = json.loads((ROOT / CHECKER.STATUS_PATH).read_text(encoding="utf-8"))
        row = next(row for row in document["graves"] if row["id"] == "DF-14")
        self.assertEqual(row["status"], "FORMALLY-REFUTED")
        self.assertEqual(row["disposition"], "NARROWED")

    def test_open_investigation_requires_complete_new_row(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["investigations"][0].pop("discriminator"))
        self.assertTrue(any("RQ-01.discriminator" in e for e in CHECKER.check(root)))

    def test_investigation_parent_and_successor_must_agree(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["graves"][5].update(successor="RQ-02"))
        self.assertTrue(any("does not name it as successor" in e for e in CHECKER.check(root)))

    def test_authorization_cannot_change_parent_status(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["graves"][4].update(status="OWNER-REOPENED"))
        errors = CHECKER.check(root)
        self.assertTrue(any("must retain a terminal status" in e for e in errors), errors)

    def test_future_contiguous_grave_is_allowed(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def add_grave(document):
            row = copy.deepcopy(document["graves"][-1])
            row.update(
                id="DF-23", status="NOT-WELL-POSED", form="new bounded dead form",
                counterexample="The proposed statement has no declared truth conditions or discriminator.",
                successor=None, successor_kind="closed_no_successor",
            )
            document["graves"].append(row)
        self.mutate(root, add_grave)
        self.assertEqual(CHECKER.check(root), [])

    def test_baseline_grave_deletion_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["graves"].pop(0))
        errors = CHECKER.check(root)
        self.assertTrue(any("baseline graves may not disappear" in e for e in errors), errors)

    def test_rq10_and_rq11_leave_parents_terminal(self) -> None:
        document = json.loads((ROOT / CHECKER.STATUS_PATH).read_text(encoding="utf-8"))
        investigations = {row["id"]: row for row in document["investigations"]}
        graves = {row["id"]: row for row in document["graves"]}
        self.assertEqual(investigations["RQ-10"]["parent"], "DF-05")
        self.assertEqual(investigations["RQ-11"]["parent"], "DF-21")
        self.assertIn(graves["DF-05"]["status"], CHECKER.TERMINAL)
        self.assertIn(graves["DF-21"]["status"], CHECKER.TERMINAL)

    def test_titan_survivor_cannot_be_restored_as_formally_valid(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate(root, lambda d: d["typed_survivors"][0].update(status="FORMALLY-VALID"))
        self.assertTrue(any("must carry NARROWED" in e for e in CHECKER.check(root)))


if __name__ == "__main__":
    unittest.main()

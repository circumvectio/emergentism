"""Local succession/regression checks; not official programme conformance."""
import hashlib
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "09_TOOLS/01_SCRIPTS"))
import check_emergentism_purity as purity

CURRENT = Path("VMOSK_A_v3_2026_09_07.md")
PREDECESSORS = {
    "VMOSK_A_v1_2026_07_28.md": "9d410ad6ecb369e67dad8084f9bd58554ba82596aa0c92cfce9e968e0aa637ea",  # sha256
    "VMOSK_A_v2_2026_07_31.md": "70353a27c79009f318e69128d1aaef93a42a7ffe64e2ea24810bb5af259db2e2",  # sha256
}
REQUIRED = {
    "may_sign": "false", "may_authorize": "false",
    "authority_effect": "none", "semantic_authority": '"none"',
}


def authority_fields_valid(text):
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0]:
        return False
    for key, value in REQUIRED.items():
        if re.findall(rf"^{key}:\s*(.*?)$", parts[1], re.M) != [value]:
            return False
    return True


class SuccessionTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / CURRENT).read_text()

    def fixture(self, root, path=CURRENT, text=None):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.text if text is None else text)
        return target

    def test_predecessors_byte_preserved(self):
        for name, expected in PREDECESSORS.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)

    def test_six_sections_and_authority_fields(self):
        self.assertEqual(re.findall(r"^## ([VMOSKA]) —", self.text, re.M), list("VMOSKA"))
        self.assertTrue(authority_fields_valid(self.text))
        self.assertTrue(authority_fields_valid((ROOT / "VMOSK_A.md").read_text()))

    def test_authority_escalations_and_duplicates_rejected(self):
        for key, value in REQUIRED.items():
            with self.subTest(key=key):
                self.assertFalse(authority_fields_valid(self.text.replace(f"{key}: {value}", f"{key}: true")))
                self.assertFalse(authority_fields_valid(self.text.replace(f"{key}: {value}", f"{key}: {value}\n{key}: true")))

    def test_pointer_and_history_remain_distinct(self):
        pointer = (ROOT / "VMOSK_A.md").read_text()
        self.assertIn(f"**Current work programme:** [`{CURRENT}`]({CURRENT})", pointer)
        self.assertIn("O1–O14 remain", self.text)
        self.assertIn("unsigned successor", self.text)
        self.assertIn("comparative trial not run", self.text)

    def test_source_and_markdown_targets_exist(self):
        source_block = self.text.split("sources:\n", 1)[1].split("---", 1)[0]
        refs = re.findall(r"^  - (.+)$", source_block, re.M)
        refs += re.findall(r"\]\(([^)]+)\)", self.text)
        for ref in refs:
            with self.subTest(ref=ref):
                target = ROOT / ref.split("#", 1)[0]
                self.assertTrue(target.exists(), ref)
                self.assertIsNone(purity.first_symlink_component(target))

    def test_scoped_files_and_sensitive_inventories_pass(self):
        paths = (*purity.CONTROL_PROJECTION_PATHS, Path("README.md"), Path("AGENTS.md"), purity.SELF_VALIDATED_TOOLING_PATH)
        for rel in paths:
            with self.subTest(path=rel):
                self.assertEqual(purity.scan_file(ROOT / rel, receipt_target_names=()), [])
        for rel, expected in purity.CONTROL_PROJECTION_UNIT_SHA256.items():
            self.assertTrue(purity.semantic_unit_inventory_matches(ROOT / rel, expected))
        self.assertTrue(purity.semantic_unit_inventory_matches(ROOT / purity.SELF_VALIDATED_TOOLING_PATH, purity.SELF_CHECKER_UNIT_SHA256))

    def test_control_inventory_matches_paths(self):
        self.assertEqual(set(purity.CONTROL_PROJECTION_UNIT_SHA256), set(purity.CONTROL_PROJECTION_PATHS))
        self.assertNotIn(Path("VMOSK_A_v1_2026_07_28.md"), purity.CONTROL_PROJECTION_PATHS)

    def test_changed_sensitive_line_rejected(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(purity, "ROOT", Path(folder)):
            path = self.fixture(Path(folder), text=self.text.replace("VMOSK-A — Emergentism:", "VMOSK-A — Certified authority:"))
            self.assertTrue(purity.scan_file(path, receipt_target_names=()))
            self.assertFalse(purity.semantic_unit_inventory_matches(path, purity.CONTROL_PROJECTION_UNIT_SHA256[CURRENT]))

    def test_duplicate_sensitive_line_rejected_by_inventory(self):
        title = next(line for line in self.text.splitlines() if line.startswith("title:"))
        with tempfile.TemporaryDirectory() as folder:
            path = self.fixture(Path(folder), text=self.text + "\n" + title)
            self.assertFalse(purity.semantic_unit_inventory_matches(path, purity.CONTROL_PROJECTION_UNIT_SHA256[CURRENT]))

    def test_sibling_copy_not_exempt(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(purity, "ROOT", Path(folder)):
            path = self.fixture(Path(folder), Path("copy.md"))
            self.assertTrue(purity.scan_file(path, receipt_target_names=()))

    def test_missing_and_symlink_targets_rejected(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(purity, "ROOT", Path(folder)):
            root = Path(folder)
            self.assertIsNotNone(purity.scoped_file_problem(CURRENT, "control projection"))
            self.assertTrue(purity.scan_file(root / CURRENT, receipt_target_names=()))
            source = self.fixture(root, Path("source.md"))
            (root / CURRENT).symlink_to(source)
            self.assertIn("symlink", purity.scoped_file_problem(CURRENT, "control projection"))
            self.assertTrue(purity.scan_file(root / CURRENT, receipt_target_names=()))

    def test_reference_labels_targets_and_authority_additions(self):
        good = f"[VMOSK-A v3]({CURRENT}) — non-semantic work programme"
        bad = [
            good.replace("v3]", "v99]"),
            good.replace(str(CURRENT), "wrong.md"),
            good.replace("non-semantic", "sovereign"),
            good + "; Skyzai authorizes every act",
        ]
        with tempfile.TemporaryDirectory() as folder, patch.object(purity, "ROOT", Path(folder)):
            self.assertEqual(purity.scan_file(self.fixture(Path(folder), Path("README.md"), good), receipt_target_names=()), [])
            for text in bad:
                with self.subTest(text=text):
                    self.assertTrue(purity.scan_file(self.fixture(Path(folder), Path("README.md"), text), receipt_target_names=()))


if __name__ == "__main__":
    unittest.main(verbosity=2)

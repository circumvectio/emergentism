#!/usr/bin/env python3
"""Focused fail-closed tests for build_magnum_opus_register.py."""

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE_BUILDER = Path(__file__).with_name("build_magnum_opus_register.py")
BUILDER_REL = Path("09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py")
FILE_REG_REL = Path("00_META/registers/FILE_REGISTER.json")
FOLDER_REG_REL = Path("00_META/registers/FOLDER_REGISTER.json")
README_REL = Path("00_META/registers/README.md")


class RegisterBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        builder = self.root / BUILDER_REL
        builder.parent.mkdir(parents=True)
        shutil.copy2(SOURCE_BUILDER, builder)
        (self.root / "alpha.md").write_text("# Alpha\n", encoding="utf-8")
        for rel in (FILE_REG_REL, FOLDER_REG_REL):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        (self.root / README_REL).write_text("placeholder\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "register-test@example.invalid")
        self.git("config", "user.name", "Register Test")
        self.git("add", BUILDER_REL.as_posix(), "alpha.md", FILE_REG_REL.as_posix(),
                 FOLDER_REG_REL.as_posix(), README_REL.as_posix())
        self.git("commit", "-qm", "fixture source")

        first = self.builder("--write")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.git("add", FILE_REG_REL.as_posix(), FOLDER_REG_REL.as_posix(), README_REL.as_posix())
        self.git("commit", "-qm", "settle generated outputs")
        self.assert_clean()

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", *map(str, args)], cwd=self.root, check=True,
            text=True, capture_output=True,
        )

    def builder(self, mode):
        return subprocess.run(
            [sys.executable, str(self.root / BUILDER_REL), mode],
            cwd=self.root, text=True, capture_output=True,
        )

    def load_file_register(self):
        return json.loads((self.root / FILE_REG_REL).read_text(encoding="utf-8"))

    def assert_clean(self):
        result = self.builder("--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_tracked_path_blocks_both_modes_until_staged_deletion(self):
        (self.root / "alpha.md").unlink()
        before = {
            rel: (self.root / rel).read_bytes()
            for rel in (FILE_REG_REL, FOLDER_REG_REL, README_REL)
        }
        for mode in ("--check", "--write"):
            result = self.builder(mode)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("index-tracked path(s) are missing", result.stdout)
            self.assertIn("missing alpha.md", result.stdout)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertEqual(
            before,
            {rel: (self.root / rel).read_bytes() for rel in before},
            "--write changed generated outputs despite a missing tracked source",
        )

        self.git("add", "-u", "--", "alpha.md")
        written = self.builder("--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assert_clean()
        paths = {entry["path"] for entry in self.load_file_register()["entries"]}
        self.assertNotIn("alpha.md", paths)

    def test_staged_add_is_drift_until_regenerated(self):
        (self.root / "new.md").write_text("# New\n", encoding="utf-8")
        self.git("add", "new.md")
        check = self.builder("--check")
        self.assertNotEqual(check.returncode, 0)
        self.assertIn("added   new.md", check.stdout)
        written = self.builder("--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assert_clean()
        paths = {entry["path"] for entry in self.load_file_register()["entries"]}
        self.assertIn("new.md", paths)

    def test_duplicate_and_corrupt_documents_fail_structural_validation(self):
        register_path = self.root / FILE_REG_REL
        original = register_path.read_bytes()
        base = json.loads(original)
        cases = []

        duplicate = copy.deepcopy(base)
        duplicate["entries"].append(copy.deepcopy(duplicate["entries"][0]))
        duplicate["entry_count"] += 1
        cases.append((duplicate, "duplicate entry paths"))

        wrong_schema = copy.deepcopy(base)
        wrong_schema["schema"] = "wrong/schema"
        cases.append((wrong_schema, "schema must be"))

        wrong_generator = copy.deepcopy(base)
        wrong_generator["generator"] = "wrong.py"
        cases.append((wrong_generator, "generator must be"))

        wrong_source = copy.deepcopy(base)
        wrong_source["source"] = "mutable source"
        cases.append((wrong_source, "source must be"))

        wrong_count = copy.deepcopy(base)
        wrong_count["entry_count"] += 1
        cases.append((wrong_count, "entry_count="))

        wrong_shape = copy.deepcopy(base)
        wrong_shape["entries"] = {"not": "a list"}
        cases.append((wrong_shape, "entries must be a list"))

        extra_metadata = copy.deepcopy(base)
        extra_metadata["unchecked"] = True
        cases.append((extra_metadata, "top-level keys differ"))

        reordered = copy.deepcopy(base)
        reordered["entries"] = list(reversed(reordered["entries"]))
        cases.append((reordered, "document ordering or non-entry metadata differs"))

        for document, expected in cases:
            with self.subTest(expected=expected):
                register_path.write_text(json.dumps(document) + "\n", encoding="utf-8")
                result = self.builder("--check")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                register_path.write_bytes(original)
        self.assert_clean()

    def test_readme_is_exact_and_only_generated_jsons_use_self(self):
        expected_readme = (self.root / README_REL).read_bytes()
        readme_text = expected_readme.decode("utf-8")
        for name in (
            "FILE_REGISTER", "FOLDER_REGISTER", "CLAIM_CARD_REGISTER",
            "CLAIM_GRAPH", "CLAIM_LIFECYCLE_INVENTORY",
        ):
            self.assertIn(name, readme_text)
        self.assertIn("compile_claim_cards.py --write", readme_text)
        self.assertIn("compile_claim_cards.py --check", readme_text)
        self.assertIn("deterministic derived artifacts", readme_text)
        entries = {entry["path"]: entry for entry in self.load_file_register()["entries"]}
        self.assertEqual(
            {path for path, entry in entries.items() if entry["sha256"] == "SELF"},
            {FILE_REG_REL.as_posix(), FOLDER_REG_REL.as_posix()},
        )
        self.assertEqual(entries[FILE_REG_REL.as_posix()]["sha256"], "SELF")
        self.assertEqual(entries[FOLDER_REG_REL.as_posix()]["sha256"], "SELF")
        self.assertEqual(
            entries[README_REL.as_posix()]["sha256"],
            hashlib.sha256(expected_readme).hexdigest(),
        )
        self.assertNotEqual(entries[README_REL.as_posix()]["sha256"], "SELF")

        (self.root / README_REL).write_text("mutated\n", encoding="utf-8")
        mutated = self.builder("--check")
        self.assertNotEqual(mutated.returncode, 0)
        self.assertIn("content differs from exact generated README_BODY", mutated.stdout)
        restored = self.builder("--write")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertEqual((self.root / README_REL).read_bytes(), expected_readme)
        self.assert_clean()

        (self.root / README_REL).unlink()
        missing = self.builder("--check")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("missing 00_META/registers/README.md", missing.stdout)
        restored = self.builder("--write")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertEqual((self.root / README_REL).read_bytes(), expected_readme)
        self.assert_clean()

    def test_staged_generated_output_deletion_is_not_silently_recreated(self):
        self.git("rm", "-q", "--", README_REL.as_posix())
        result = self.builder("--write")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("declared generated output(s) are absent from the git index", result.stdout)
        self.assertIn(f"untracked-output {README_REL.as_posix()}", result.stdout)
        self.assertFalse((self.root / README_REL).exists())
        self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    print("REGISTER BUILDER NEGATIVE CONTROLS", flush=True)
    unittest.main()

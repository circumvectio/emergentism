#!/usr/bin/env python3
"""Tests for the Git-index-backed FILE/FOLDER register compiler."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "build_magnum_opus_register.py"
SPEC = importlib.util.spec_from_file_location("build_magnum_opus_register", SCRIPT)
register = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = register
SPEC.loader.exec_module(register)


def run_git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
    ).stdout


def write(repo, relative, content):
    path = Path(repo) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        content = content.encode("utf-8")
    path.write_bytes(content)


def initialize_repo(root):
    run_git(root, "init", "-q")
    run_git(root, "config", "user.name", "Register Test")
    run_git(root, "config", "user.email", "register@example.invalid")
    write(root, "README.md", "# Root\n\nIndex-owned corpus.\n")
    write(
        root,
        "notes.md",
        "---\nstatus: SIGNED\nevidence_tier: '[S]'\n---\n# Notes\nREADME.md\n",
    )
    write(root, register.FILE_REG_REL, "{}\n")
    write(root, register.FOLDER_REG_REL, "{}\n")
    write(
        root,
        register.FILE_MANIFEST_REL,
        "path,disposition\nnotes.md,ABSORB\n",
    )
    write(
        root,
        register.FOLDER_MANIFEST_REL,
        "folder,disposition\n.,KEEP\n",
    )
    run_git(root, "add", ".")
    run_git(root, "commit", "-qm", "fixture")


class IndexRecordTests(unittest.TestCase):
    def test_parse_index_records_supports_tabs_and_sorts_paths(self):
        oid_a = "a" * 40
        oid_b = "b" * 40
        raw = (
            f"100644 {oid_b} 0\tz.md\0".encode()
            + f"100644 {oid_a} 0\ta\tname.md\0".encode()
        )
        entries = register.parse_index_records(raw)
        self.assertEqual([entry.path for entry in entries], ["a\tname.md", "z.md"])
        self.assertEqual(entries[0].oid, oid_a)

    def test_parse_index_records_rejects_duplicate_path(self):
        oid = "a" * 40
        raw = (
            f"100644 {oid} 0\tduplicate.md\0".encode()
            + f"100644 {oid} 0\tduplicate.md\0".encode()
        )
        with self.assertRaisesRegex(register.RegisterError, "duplicate path"):
            register.parse_index_records(raw)

    def test_parse_index_records_rejects_unmerged_stage(self):
        raw = f"100644 {'a' * 40} 2\tconflict.md\0".encode()
        with self.assertRaisesRegex(register.RegisterError, "unmerged index entry"):
            register.parse_index_records(raw)

    def test_parse_cat_file_batch_preserves_exact_binary_bytes(self):
        oid_a = "a" * 40
        oid_b = "b" * 40
        payload_a = b"line one\nline two\0tail"
        payload_b = b"\xff\x00\n"
        raw = (
            f"{oid_a} blob {len(payload_a)}\n".encode() + payload_a + b"\n"
            + f"{oid_b} blob {len(payload_b)}\n".encode() + payload_b + b"\n"
        )
        parsed = register.parse_cat_file_batch(raw, [oid_a, oid_b])
        self.assertEqual(parsed, {oid_a: payload_a, oid_b: payload_b})

    def test_parse_cat_file_batch_rejects_non_blob(self):
        oid = "a" * 40
        raw = f"{oid} commit 0\n\n".encode()
        with self.assertRaisesRegex(register.RegisterError, "not blob"):
            register.parse_cat_file_batch(raw, [oid])


class RegisterDerivationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        initialize_repo(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def test_derive_reads_index_not_unstaged_working_tree(self):
        before = register.derive(str(self.repo))
        write(self.repo, "notes.md", "UNSTAGED AND FALSE\n")
        after_unstaged = register.derive(str(self.repo))
        self.assertEqual(before, after_unstaged)

        run_git(self.repo, "add", "notes.md")
        after_staged = register.derive(str(self.repo))
        self.assertNotEqual(before, after_staged)
        staged_entry = next(
            entry for entry in after_staged[0]["entries"] if entry["path"] == "notes.md"
        )
        self.assertEqual(
            staged_entry["sha256"],
            hashlib.sha256(b"UNSTAGED AND FALSE\n").hexdigest(),
        )

    def test_file_register_has_one_self_row_and_no_duplicate_paths(self):
        file_doc, folder_doc = register.derive(str(self.repo))
        self_rows = [
            entry for entry in file_doc["entries"]
            if entry["path"] == register.SELF_PATH
        ]
        self.assertEqual(len(self_rows), 1)
        self.assertEqual(self_rows[0]["sha256"], "SELF")
        self.assertEqual(self_rows[0]["bytes"], 0)
        paths = [entry["path"] for entry in file_doc["entries"]]
        self.assertEqual(file_doc["entry_count"], len(paths))
        self.assertEqual(len(paths), len(set(paths)))
        register.validate_register(file_doc, "file")
        register.validate_register(folder_doc, "folder")

        folder_register = next(
            entry for entry in file_doc["entries"]
            if entry["path"] == register.FOLDER_REG_REL
        )
        self.assertEqual(
            folder_register["sha256"], hashlib.sha256(b"{}\n").hexdigest()
        )

    def test_derivation_and_serialization_are_byte_deterministic(self):
        first = register.derive(str(self.repo))
        second = register.derive(str(self.repo))
        self.assertEqual(first, second)
        self.assertEqual(register.serialized(first[0]), register.serialized(second[0]))
        self.assertNotIn(b"generated_at", register.serialized(first[0]))
        self.assertFalse(
            any(
                "timestamp" in key.lower() or key.lower().endswith("_at")
                for key in first[0]
            )
        )

    def test_index_manifest_bytes_control_disposition(self):
        file_doc, folder_doc = register.derive(str(self.repo))
        notes = next(entry for entry in file_doc["entries"] if entry["path"] == "notes.md")
        root = next(entry for entry in folder_doc["entries"] if entry["path"] == ".")
        self.assertEqual(notes["disposition"], "staged")
        self.assertEqual(root["disposition"], "keep")

    def test_write_guard_rejects_unstaged_non_register_change(self):
        write(self.repo, "notes.md", "unstaged\n")
        with self.assertRaisesRegex(register.RegisterError, "notes.md"):
            register.assert_write_safe(str(self.repo))
        run_git(self.repo, "add", "notes.md")
        register.assert_write_safe(str(self.repo))

    def test_write_guard_allows_dirty_generated_outputs_only(self):
        write(self.repo, register.FILE_REG_REL, "dirty generated output\n")
        write(self.repo, register.FOLDER_REG_REL, "dirty generated output\n")
        register.assert_write_safe(str(self.repo))

    def test_write_guard_rejects_untracked_non_register_file(self):
        write(self.repo, "scratch.txt", "not staged\n")
        with self.assertRaisesRegex(register.RegisterError, "scratch.txt"):
            register.assert_write_safe(str(self.repo))


class ValidationAndWriteTests(unittest.TestCase):
    @staticmethod
    def valid_doc(paths=()):
        entries = [{"path": path} for path in paths]
        return {"entry_count": len(entries), "entries": entries}

    def test_validate_register_rejects_count_mismatch(self):
        doc = {"entry_count": 2, "entries": [{"path": "one"}]}
        with self.assertRaisesRegex(register.RegisterError, "entry_count"):
            register.validate_register(doc, "fixture")

    def test_validate_register_rejects_duplicate_paths(self):
        doc = self.valid_doc(["same", "same"])
        with self.assertRaisesRegex(register.RegisterError, "duplicate"):
            register.validate_register(doc, "fixture")

    def test_diff_detects_top_level_metadata_drift(self):
        derived = {
            "schema": "current",
            "source": "Git index blob bytes",
            **self.valid_doc(["one"]),
        }
        stale = {
            "schema": "current",
            "source": "working-tree bytes",
            **self.valid_doc(["one"]),
        }
        added, removed, changed = register.diff_docs(derived, stale)
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertEqual(changed, [("<register metadata>", ["source"])])

    def test_write_registers_preserves_all_dated_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dated = {
                "00_META/registers/03_FILE_REGISTER_2026_07_19.json": b"file evidence\n",
                "00_META/registers/04_FOLDER_REGISTER_2026_07_19.json": b"folder evidence\n",
                register.FILE_MANIFEST_REL: b"file manifest\n",
                register.FOLDER_MANIFEST_REL: b"folder manifest\n",
            }
            for path, raw in dated.items():
                write(root, path, raw)
            register.write_registers(self.valid_doc(), self.valid_doc(), str(root))
            for path, raw in dated.items():
                self.assertEqual((root / path).read_bytes(), raw)
            self.assertEqual(
                json.loads((root / register.FILE_REG_REL).read_text()), self.valid_doc()
            )
            self.assertEqual(
                json.loads((root / register.FOLDER_REG_REL).read_text()), self.valid_doc()
            )


if __name__ == "__main__":
    unittest.main()

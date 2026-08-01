#!/usr/bin/env python3
"""Mutation controls for review-bundle readiness projection."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_review_bundle.py"
SPEC = importlib.util.spec_from_file_location("check_review_bundle", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
BUNDLE_DIR = ROOT / "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice"
MANIFEST_PATH = BUNDLE_DIR / "REVIEW_BUNDLE_v3.json"
PACKET_PATH = BUNDLE_DIR / "REVIEW_BUNDLE_v3.md"


class ReviewBundleStatusTests(unittest.TestCase):
    def test_live_packet_matches_blocked_registry(self) -> None:
        state = CHECKER.review_execution_state()
        packet = PACKET_PATH.read_text(encoding="utf-8")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        registry, gate = CHECKER.review_gate_data()
        self.assertEqual(state, "blocked")
        self.assertEqual(CHECKER.document_status_errors(packet, state), [])
        packet_relative = PACKET_PATH.relative_to(ROOT).as_posix()
        self.assertEqual(
            manifest["files"].get(packet_relative), "sha256:" + CHECKER.sha256(PACKET_PATH)
        )
        self.assertEqual(
            CHECKER.acyclic_binding_errors(MANIFEST_PATH, manifest, registry, gate, 3),
            [],
        )

    def test_projection_excludes_runtime_but_tracks_static_contract(self) -> None:
        registry, _ = CHECKER.review_gate_data()
        runtime_mutation = copy.deepcopy(registry)
        runtime_mutation["external_state"]["reviewers_engaged"]["state"] = "present"
        runtime_mutation["gates"][1]["execution"]["prerequisites"]["bundle_manifest"]["sha256"] = "0" * 64
        self.assertEqual(
            CHECKER.review_registry_projection(runtime_mutation),
            CHECKER.review_registry_projection(registry),
        )
        static_mutation = copy.deepcopy(registry)
        static_mutation["gates"][1]["execution"]["ready_when"] += " changed"
        self.assertNotEqual(
            CHECKER.review_registry_projection(static_mutation),
            CHECKER.review_registry_projection(registry),
        )

    def test_mutable_self_binding_files_are_rejected(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        forbidden = (
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/GATE_REGISTRY.json",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v3.json",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v3_BINDING_RECEIPT.json",
        )
        for path in forbidden:
            with self.subTest(path=path):
                mutated = copy.deepcopy(manifest)
                mutated["files"][path] = "sha256:" + "0" * 64
                errors = CHECKER.acyclic_binding_errors(
                    MANIFEST_PATH, mutated, registry, gate, 3
                )
                self.assertTrue(
                    any("must not hash mutable/self-binding" in error for error in errors),
                    errors,
                )

    def test_wrong_binding_digest_and_human_prerequisites_fail_closed(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        bad_registry = copy.deepcopy(registry)
        bad_gate = bad_registry["gates"][1]
        bad_gate["execution"]["prerequisites"]["bundle_manifest"]["sha256"] = "0" * 64
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, manifest, bad_registry, bad_gate, 3
        )
        self.assertTrue(any("artifact digest drifted" in error for error in errors), errors)

        prerequisites = gate["execution"]["prerequisites"]
        self.assertEqual(prerequisites["bundle_manifest"]["state"], "satisfied")
        remaining = set(prerequisites) - {"bundle_manifest"}
        self.assertEqual(remaining, CHECKER.REMAINING_REVIEW_PREREQUISITES)
        self.assertTrue(all(prerequisites[name]["state"] == "missing" for name in remaining))
        self.assertEqual(gate["execution"]["state"], "blocked")

    def test_ready_to_send_cannot_hide_inside_blocked_packet(self) -> None:
        claims = (
            "READY TO SEND",
            "ready-to-send",
            "contact ready",
            "may now be sent",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                packet = (
                    f"{claim}. not sent. review received: no. "
                    "The reviewer does not work here. CONTACT BLOCKED."
                )
                errors = CHECKER.document_status_errors(packet, "blocked")
                self.assertTrue(
                    any("contact readiness" in error for error in errors), errors
                )

    def test_blocked_packet_requires_explicit_boundary_phrases(self) -> None:
        errors = CHECKER.document_status_errors("CONTACT BLOCKED", "blocked")
        self.assertTrue(any("not sent" in error for error in errors), errors)
        self.assertTrue(any("review received" in error for error in errors), errors)
        self.assertTrue(any("does not work here" in error for error in errors), errors)

    def test_manifest_file_paths_cannot_escape_the_corpus(self) -> None:
        for relative in ("/tmp/outside", "../outside", "./not-canonical", "a/../../outside", "x\x00y"):
            with self.subTest(relative=relative):
                path, error = CHECKER.contained_manifest_file(relative)
                self.assertIsNone(path)
                self.assertIn("safe and repository-relative", error)

        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            corpus = temporary_root / "corpus"
            corpus.mkdir()
            outside = temporary_root / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            (corpus / "escape").symlink_to(outside)
            with mock.patch.object(CHECKER, "ROOT", corpus):
                path, error = CHECKER.contained_manifest_file("escape")
            self.assertIsNone(path)
            self.assertIn("resolves outside the repository", error)

            bundle_dir = corpus / "finity"
            bundle_dir.mkdir()
            (bundle_dir / "REVIEW_BUNDLE_v1.json").write_text(
                json.dumps(
                    {
                        "bundleVersion": "v1",
                        "frozen": "test",
                        "files": {"/tmp/outside": "sha256:" + "0" * 64},
                    }
                ),
                encoding="utf-8",
            )
            (bundle_dir / "REVIEW_BUNDLE_v1.md").write_text(
                "not sent; review received: no; does not work here; CONTACT BLOCKED.",
                encoding="utf-8",
            )
            output = io.StringIO()
            with (
                mock.patch.object(CHECKER, "ROOT", corpus),
                mock.patch.object(CHECKER, "DIR", bundle_dir),
                mock.patch.object(CHECKER, "review_gate_data", return_value=({}, {})),
                mock.patch.object(CHECKER, "review_execution_state", return_value="blocked"),
                redirect_stdout(output),
            ):
                self.assertEqual(CHECKER.main(), 1)
            self.assertIn("safe and repository-relative", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)

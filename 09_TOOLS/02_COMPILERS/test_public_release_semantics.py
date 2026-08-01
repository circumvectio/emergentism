#!/usr/bin/env python3
"""Mutation checks for the dimension-first public release projection."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "12_PUBLIC_SITE"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parity = load("public_semantic_parity", SITE / "check_public_semantic_parity.py")
frozen = load("frozen_library_boundary", SITE / "apply_frozen_library_boundary.py")
renderer = load("dimension_renderer", SITE / "render_dimension_site.py")
rag_builder = load("book_rag_builder", SITE / "build_rag_index.py")


class PublicReleaseSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))

    def test_exact_typed_sequence(self) -> None:
        self.assertEqual(self.data["sequence"], parity.EXPECTED_SEQUENCE)
        self.assertEqual([x["id"] for x in self.data["levels"]], [f"D{i}" for i in range(7)])
        transitions = [x["transition"]["id"] for x in self.data["levels"] if "transition" in x]
        self.assertEqual(transitions, ["mu0", "mu1", "mu2", "mu3", "mu4", "b6"])
        self.assertEqual(self.data["levels"][4]["modality"], "actual")
        self.assertEqual(self.data["levels"][5]["modality"], "possible")

    def test_claim_card_projection_contract_is_current(self) -> None:
        self.assertEqual(self.data["schemaVersion"], 2)
        contract = self.data["claimCardContract"]
        source = ROOT / contract["source"]
        self.assertEqual(
            contract["sourceRevision"],
            "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        register = json.loads((ROOT / contract["register"]).read_text(encoding="utf-8"))
        known = {card["card_id"] for card in register["cards"]}
        for level in self.data["levels"]:
            self.assertTrue(level["claimCardIds"])
            self.assertTrue(set(level["claimCardIds"]) <= known)
            self.assertEqual(level["sourceRevision"], contract["sourceRevision"])
            self.assertEqual(level["lifecycle"], "reader_synthesis")
            self.assertEqual(level["publicDisposition"], "bounded_current")

    def test_forbidden_claim_mutations_are_caught(self) -> None:
        mutations = {
            "literal D6 identity": "D6 ≡ D0",
            "extra mu crossing": "μ5 opens",
            "invalid scalar sampling": "Sample[∫|ψ|²]",
            "physical cone inflation": "the physical light cone widens",
            "quantum dimensional stacking": "Everett is a five-dimensional realm",
            "quantum-gravity solution inflation": "we solved quantum gravity",
            "zero-momentum D3 inflation": "D3 has no momentum",
            "application authority leakage": "Sky" + "zai governs this claim",
        }
        for name, text in mutations.items():
            with self.subTest(name=name):
                self.assertRegex(text, parity.FORBIDDEN[name])

    def test_provisional_surfaces_are_inside_parity_prohibition_scope(self) -> None:
        audited = set(parity.parity_audit_surfaces(self.data))
        provisional = set(self.data["declaredProvisional"]["routes"])
        self.assertTrue(provisional)
        self.assertTrue(provisional <= audited)
        self.assertTrue(set(self.data["currentSurfaces"]) <= audited)
        self.assertTrue(
            set(self.data["infrastructureRoutes"]["routes"]).isdisjoint(audited)
        )

    def test_d3_preserves_momentum_and_open_physics(self) -> None:
        d3 = self.data["levels"][3]
        joined = " ".join(str(value) for value in d3.values())
        self.assertIn("momentum distributions", joined)
        self.assertIn("noncommuting observables", joined)
        self.assertIn("does not solve measurement, quantum gravity", joined)

    def test_renderer_is_deterministic_and_instrument_is_wired(self) -> None:
        first = renderer.render()
        second = renderer.render()
        self.assertEqual(first, second)
        for path, body in first.items():
            if path.parent.name == "dimensions":
                continue
            self.assertIn('class="diagram visual-panel"', body)
            self.assertIn('type="importmap"', body)
            self.assertIn('type="module" src="../dimensions/dimensions.js"', body)

    def test_frozen_boundary_is_idempotent(self) -> None:
        sample = "<html><body><main>old claim</main></body></html>"
        once = frozen.desired(sample)
        self.assertIn(frozen.MARKER, once)
        self.assertEqual(frozen.desired(once), once)

    def test_rag_excludes_frozen_library(self) -> None:
        rag = json.loads((SITE / "book/rag_index.json").read_text(encoding="utf-8"))
        prefixes = tuple(f"{root}:" for root in self.data["frozenLibraryRoots"])
        self.assertTrue(rag["passages"])
        self.assertFalse(any(str(item.get("id", "")).startswith(prefixes) for item in rag["passages"]))

    def test_release_checker_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SITE / "check_public_semantic_parity.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_book_manifest_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SITE / "build_book.py"), "--check"],
            cwd=SITE,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest = json.loads((SITE / "book/build-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "emergentism/public-book-build/v2")
        self.assertEqual(manifest["work_id"], "BK-ONE-SITTING")

        # v2 is deliberately narrower than the retired 29-source projection:
        # one current reader source, with exact byte custody, and no inherited
        # Reciprocal chapters silently entering either output or retrieval.
        self.assertEqual(len(manifest["sources"]), 1)
        source = manifest["sources"][0]
        self.assertEqual(source["path"], "00_THE_WELTANSCHAUUNG_ONE_SITTING.md")
        self.assertEqual(source["lifecycle"], "reader_synthesis")
        self.assertIs(source["public_eligible"], True)
        self.assertEqual(manifest["ordered_source_paths"], [source["path"]])
        self.assertEqual(
            source["sha256"],
            hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest(),
        )

        catalog = manifest["catalog_contract"]
        self.assertEqual(catalog["schema"], "emergentism/book-manifest/v1")
        self.assertEqual(catalog["path"], "13_BOOKS/book-manifest.json")
        self.assertEqual(catalog["release_state"], "source_active_current_public_reader")
        self.assertEqual(catalog["public_route"], "../12_PUBLIC_SITE/book/index.html")
        self.assertEqual(
            catalog["sha256"],
            hashlib.sha256((ROOT / catalog["path"]).read_bytes()).hexdigest(),
        )

        output = manifest["output"]
        self.assertEqual(output["path"], "book/index.html")
        self.assertEqual(
            output["sha256"],
            hashlib.sha256((SITE / output["path"]).read_bytes()).hexdigest(),
        )
        coverage = manifest["claim_card_contract"]["coverage"]
        self.assertEqual(coverage["claim_card_count"], 26)
        self.assertEqual(len(coverage["rendered_source_chapter_order"]), 12)
        self.assertEqual(coverage["public_states"], ["bounded_current", "candidate"])
        self.assertEqual(coverage["review_states"], ["implemented", "l3_audited"])

        withheld = manifest["withheld_provenance"]
        self.assertEqual(withheld["path"], "13_BOOKS/the_reciprocal/")
        self.assertEqual(withheld["lifecycle"], "withheld_staged_provenance")
        self.assertIs(withheld["included_in_output"], False)
        self.assertIs(withheld["included_in_rag"], False)

    def test_rag_source_integrity_negative_controls(self) -> None:
        # The generator's permanent controls must reject both loss of the
        # declared source and byte drift against its v2 SHA-256 receipt.
        rag_builder.source_negative_controls()


if __name__ == "__main__":
    unittest.main()

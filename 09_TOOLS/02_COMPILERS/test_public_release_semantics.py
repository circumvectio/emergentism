#!/usr/bin/env python3
"""Mutation checks for the dimension-first public release projection."""

from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main()

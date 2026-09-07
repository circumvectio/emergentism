#!/usr/bin/env python3
"""Point-in-time checks for two reviewed projections; not semantic validation.

Later deliberate source revisions may fail the frozen-byte check. Preserve this
receipt rather than silently updating its digests to make a new state pass.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "09_TOOLS/01_SCRIPTS"))
from check_all_citations import INLINE, fm_paths, frontmatter
from check_emergentism_purity import scan_file
from foundation_type_firewall import titan_arithmetic_matches

GUIDE = "07_THEOLOGY/01_SYMBOL_DESIGN_AND_PUBLIC_TRANSLATION.md"
SEED = "10_SEED/00_THE_SEED.md"
SHA256 = {
    GUIDE: "0f8f352429de8dbfc1dfc37c529def78a0f7c2c8cbeaa820a2ca5cb2e520d1de",  # SHA-256
    SEED: "6a49c93cbd4b429bd4dc371ba882cf9401f09de54423de9794aa687c05c50682",  # SHA-256
}


class ProjectionReview(unittest.TestCase):
    def test_reviewed_bytes(self):
        for rel, digest in SHA256.items():
            with self.subTest(path=rel):
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest)

    def test_local_citation_targets(self):
        paths = [ROOT / rel for rel in SHA256] + [Path(__file__).with_name("README.md")]
        count = 0
        for path in paths:
            text = path.read_text(encoding="utf-8")
            refs = INLINE.findall(text) + [value for _, value in fm_paths(frontmatter(text))]
            for href in refs:
                with self.subTest(path=path.name, href=href):
                    self.assertFalse(re.match(r"^(https?:|mailto:|data:)", href))
                    self.assertTrue((path.parent / href).resolve().exists())
                count += 1
        self.assertGreater(count, 0)

    def test_existing_type_firewall(self):
        for rel in SHA256:
            with self.subTest(path=rel):
                self.assertEqual(titan_arithmetic_matches((ROOT / rel).read_text()), [])

    def test_existing_scoped_purity(self):
        for rel in SHA256:
            with self.subTest(path=rel):
                self.assertEqual(scan_file(ROOT / rel), [])

    def test_named_seed_repair_sentinels(self):
        text = (ROOT / SEED).read_text()
        rows = [line for line in text.splitlines() if re.match(r"^\| D[0-6] \|", line)]
        self.assertEqual(len(rows), 7)
        self.assertEqual(len({line.split("|")[1].strip() for line in rows}), 7)
        self.assertIn("an actual preparation or assignment act is D4", rows[3])
        self.assertIn("merely possible content", rows[5])
        self.assertIn("a recognition or withdrawal act is D4", rows[6])
        self.assertNotIn("| Modality |", text)
        self.assertIn("preserve", text.lower())

    def test_named_guide_repair_sentinels(self):
        text = (ROOT / GUIDE).read_text()
        for retired in ("access φ directly", "reaches Layer 1 directly", "20-40 minutes",
                        "Coherence-viability trade-off", "Zero-Sum Resolution Equation"):
            self.assertNotIn(retired, text)
        flat = " ".join(text.split())
        for required in ("Anyone may *discard* the symbol at any time", "θ∈(0,π)",
                         "L7 counsel first returns to L4", "omitted remainder",
                         "Comparative benefit remains untested", "what survives failure"):
            self.assertIn(required, flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)

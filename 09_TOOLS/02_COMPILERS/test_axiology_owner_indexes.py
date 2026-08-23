#!/usr/bin/env python3
"""Regression checks for the active Axiology owner indexes."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AXIOLOGY = ROOT / "04_AXIOLOGY"
AXIOLOGY_INDEX = AXIOLOGY / "README.md"
VALUE_THEORY = AXIOLOGY / "02_VALUE_THEORY"
VALUE_THEORY_INDEX = VALUE_THEORY / "README.md"


def markdown_targets(text: str) -> set[str]:
    """Return local Markdown link targets from the supplied index section."""
    return set(re.findall(r"\[[^]]+\]\(([^)#]+\.md)\)", text))


class AxiologyOwnerIndexTests(unittest.TestCase):
    def test_lane_source_owner_index_is_complete_and_resolvable(self) -> None:
        text = AXIOLOGY_INDEX.read_text(encoding="utf-8")
        section = text.split("## Source owners\n", 1)[1].split(
            "\nApplication-specific economic", 1
        )[0]
        expected = {
            "02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
            "02_VALUE_THEORY/01_RIGHTS_DUTIES_AND_DUE_PROCESS.md",
            "02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md",
            "02_VALUE_THEORY/01_TRANSCENDENTALS.md",
            "02_VALUE_THEORY/02_OBJECTIVE_ETHICS_BRIDGE_DOCKET.md",
            "02_VALUE_THEORY/03_RECIPROCAL_CO_AGENCY_BRIDGE_RCAB_01.md",
            "02_VALUE_THEORY/04_GUARDIANSHIP_EXTENSION_GEX_01.md",
            "00_BRIDGE_LAWS_BETWEEN_LEVELS.md",
            "00_THE_EXTRACTION_LAW.md",
            "00_COMMANDMENT_VS_GEOMETRY.md",
            "00_ANMUT_AND_DEMUT.md",
            "01_THEURGY/00_THEURGY_AND_F5_FORCE_MAP.md",
        }
        actual = markdown_targets(section)
        self.assertEqual(actual, expected)
        for target in actual:
            self.assertTrue((AXIOLOGY / target).is_file(), target)

    def test_value_theory_index_includes_its_a4_docket(self) -> None:
        text = VALUE_THEORY_INDEX.read_text(encoding="utf-8")
        section = text.split("This directory contains the pure Emergentist value owners:\n", 1)[1].split(
            "\nThe formal discipline", 1
        )[0]
        expected = {
            "00_OBJECTIVE_MORALS_AND_ETHICS.md",
            "00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md",
            "01_RIGHTS_DUTIES_AND_DUE_PROCESS.md",
            "01_TRANSCENDENTALS.md",
            "02_OBJECTIVE_ETHICS_BRIDGE_DOCKET.md",
            "03_RECIPROCAL_CO_AGENCY_BRIDGE_RCAB_01.md",
            "04_GUARDIANSHIP_EXTENSION_GEX_01.md",
        }
        actual = markdown_targets(section)
        self.assertEqual(actual, expected)
        for target in actual:
            self.assertTrue((VALUE_THEORY / target).is_file(), target)

        docket = (VALUE_THEORY / "02_OBJECTIVE_ETHICS_BRIDGE_DOCKET.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("adequacy_docket: A4", docket)
        self.assertIn("EVIDENCE-OPEN", docket)


if __name__ == "__main__":
    print("AXIOLOGY OWNER INDEXES", flush=True)
    unittest.main()

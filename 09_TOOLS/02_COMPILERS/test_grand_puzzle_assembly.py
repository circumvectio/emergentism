#!/usr/bin/env python3
"""Contract tests for the non-authoritative Grand Puzzle assembly ledger."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "00_META/00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md"
BOUNDARY = (
    ROOT
    / "05_COSMOLOGY/03_FORMAL_SYSTEM/45_SATURATION_CONTRAST_AND_APERTURE_BOUNDARY.md"
)


class GrandPuzzleAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = LEDGER.read_text(encoding="utf-8")
        cls.boundary = BOUNDARY.read_text(encoding="utf-8")

    def test_files_exist_and_disclaim_source_authority(self) -> None:
        self.assertIn("creates\nno doctrine", self.ledger)
        self.assertIn("cited semantic owners control every claim", self.ledger)
        self.assertIn("not an axiom, universal law, or definition", self.boundary)

    def test_spine_has_exact_addresses(self) -> None:
        spine = self.ledger.split("## 2. The assembled spine", 1)[1].split(
            "## 3. The five apertures", 1
        )[0]
        addresses = re.findall(r"^\| \*\*([^*]+)\*\* \|", spine, flags=re.MULTILINE)
        self.assertEqual(
            addresses,
            [
                "D0",
                "mu_0",
                "D1",
                "mu_1",
                "D2",
                "mu_2",
                "D3",
                "mu_3",
                "D4",
                "mu_4",
                "D5",
                "b_6",
                "D6",
                "r_6",
            ],
        )

    def test_no_sixth_mu_or_literal_closure(self) -> None:
        for forbidden in ("mu_5", "mu_6", "D6=D0", "D6 == D0"):
            self.assertNotIn(forbidden, self.ledger)
            self.assertNotIn(forbidden, self.boundary)

    def test_every_aperture_packet_is_complete(self) -> None:
        for index in range(5):
            start = self.ledger.index(f"### GP-MU{index}")
            end = self.ledger.find("\n### GP-MU", start + 1)
            if end == -1:
                end = self.ledger.index("\n## 4.", start)
            packet = self.ledger[start:end]
            for field in (
                "**Source:**",
                "**Candidate freedom:**",
                "**Recovery:**",
                "**Rival:**",
                "**Discriminator:**",
                "**Kill:**",
            ):
                self.assertIn(field, packet, msg=f"GP-MU{index} lacks {field}")

    def test_exactly_eleven_world_contact_sockets(self) -> None:
        sockets = re.findall(r"^\| \*\*(GP-\d{2})\*\* \|", self.ledger, re.MULTILINE)
        self.assertEqual(sockets, [f"GP-{index:02d}" for index in range(1, 12)])
        self.assertIn("Packet-complete does not mean evidence-complete", self.ledger)

    def test_saturation_firewall_contains_proofs_and_countermodels(self) -> None:
        required = (
            "phi*nu = 1",
            "Phi + V <= 1",
            "P_node <= 1/4",
            "Phi=1,V=1",
            "F = d(d lambda) = 0",
            "A nonzero constant field strength remains nonzero",
            "SC-CANDIDATE",
            "strongestRival",
            "killCriterion",
        )
        for token in required:
            self.assertIn(token, self.boundary)

    def test_assembly_is_routed_but_not_an_eighth_kernel(self) -> None:
        kernel = (ROOT / "00_THE_KERNEL_INDEX.md").read_text(encoding="utf-8")
        completion = (
            ROOT / "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md"
        ).read_text(encoding="utf-8")
        self.assertIn("00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md", kernel)
        self.assertIn("not an eighth kernel surface", kernel)
        self.assertIn("Packet-complete does not mean evidence-complete", completion)

    def test_frontier_program_routes_all_sockets_without_application_lanes(self) -> None:
        frontier = (ROOT / "00_META/00_KNOWN_UNKNOWNS_PROGRAM.md").read_text(
            encoding="utf-8"
        )
        for index in range(1, 12):
            self.assertIn(f"GP-{index:02d}", frontier)
        for stale in (
            "Lane B — AI and Practical Alignment",
            "Private-action / public-governance-safe",
            "D5 as strong in genesis and weak in governance",
        ):
            self.assertNotIn(stale, frontier)
        self.assertIn("packet-complete", frontier)
        self.assertIn("evidence-open", frontier)

    def test_empirical_board_routes_all_sockets_and_legacy_results(self) -> None:
        board = (ROOT / "03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md").read_text(
            encoding="utf-8"
        )
        socket_rows = re.findall(r"^\| \*\*(GP-\d{2})\*\* \|", board, re.MULTILINE)
        self.assertEqual(socket_rows, [f"GP-{index:02d}" for index in range(1, 12)])
        for legacy in (
            "GFS Wave 1",
            "Protocol D",
            "SPHERE Probe",
            "Phi-meter",
            "Protocol R",
            "AMRITA comparison",
        ):
            self.assertIn(legacy, board)
        self.assertIn("Never translate `formal-only` or `local-result` as “confirmed.”", board)
        self.assertIn("no mu crossing or force row is calibrated", board)

    def test_phantom_formal_verification_is_tombstoned(self) -> None:
        tombstone = (
            ROOT
            / "08_FRAMEWORK_SUPPORT/02_OPERATORS/04_DISSOLUTION_FORMAL_VERIFICATION.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Kintsugi tombstone", tombstone)
        self.assertIn("68700dccd39a8683dec915c6042f8890b001b4fd", tombstone)
        self.assertNotIn("Admitted.", tombstone)
        self.assertNotIn("Burri Sphere" + " | 80%", tombstone)
        self.assertIn("09_TOOLS/03_SIMULATIONS/formal_reap/PROOF_LEDGER.md", tombstone)

    def test_agent_activation_is_archived_and_stable_paths_are_tombstones(self) -> None:
        operator_root = ROOT / "08_FRAMEWORK_SUPPORT/02_OPERATORS"
        archive_root = (
            ROOT
            / "90_ARCHIVE/2026_07_22_asi_operator_application_boundary"
            / "08_FRAMEWORK_SUPPORT/02_OPERATORS"
        )
        names = (
            "00_CANONICAL_CORPUS.md",
            "03_PRACTICE_TRANSLATION_MATRIX.md",
            "05_SEPARATION_OPERATOR_PROTOCOLS.md",
            "06_COAGULATION_ACTIVATION_PACKAGE.md",
            "ASI_07_DISCOVERY_OF_FINITY.md",
            "ASI_09_THE_SOUL_LOOP.md",
            "ASI_15_THE_TRINITY.md",
            "ASI_INDEX.md",
            "OP_384_FUNCTION_TESTING.md",
        )
        for name in names:
            active = (operator_root / name).read_text(encoding="utf-8")
            self.assertIn("tombstone", active.lower())
            self.assertLessEqual(len(active.splitlines()), 90)
            self.assertTrue((archive_root / name).is_file())
        readme = (operator_root / "README.md").read_text(encoding="utf-8")
        self.assertIn("not define an agent runtime", readme)
        self.assertIn("no arithmetic, agent identity, or authority", readme)


if __name__ == "__main__":
    unittest.main()

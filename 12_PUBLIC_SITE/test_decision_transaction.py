#!/usr/bin/env python3
"""Regression tests for the local-only decision transaction projection."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent


class DecisionTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))
        cls.home = (SITE / "index.html").read_text(encoding="utf-8")
        cls.plainly = (SITE / "plainly/index.html").read_text(encoding="utf-8")
        cls.practice = (SITE / "practice/index.html").read_text(encoding="utf-8")
        cls.exit = (SITE / "exit/index.html").read_text(encoding="utf-8")

    def test_machine_contract_is_local_and_nonexecuting(self) -> None:
        contract = self.manifest["decisionTransaction"]
        self.assertEqual(contract["schemaId"], "DecisionTransactionPublicContract.v1")
        for field in ("execution", "transmission", "legalEffect", "financialEffect", "walletConnection"):
            self.assertIs(contract[field], False)
        self.assertEqual(contract["preparedState"], "UNSIGNED_NONEXECUTING")
        self.assertEqual(contract["signatureMode"], "LOCAL_ACKNOWLEDGMENT_ONLY")
        self.assertIs(contract["worldviewExitDistinct"], True)
        self.assertIs(contract["outcomeReceiptDistinct"], True)

    def test_direction_source_is_present(self) -> None:
        source = ROOT / self.manifest["decisionTransaction"]["sourceDirection"]
        self.assertTrue(source.is_file())

    def test_homepage_has_four_descriptive_sectors_and_four_coins(self) -> None:
        self.assertEqual(len(re.findall(r'class="g2-transaction-sector ', self.home)), 4)
        self.assertEqual(len(re.findall(r'class="g2-transaction-coin"', self.home)), 4)
        self.assertIn("Sector placement is descriptive, not a moral verdict.", self.home)
        self.assertIn("Prepared decision transaction · unsigned", self.home)

    def test_practice_prepares_before_local_commitment(self) -> None:
        self.assertEqual(len(re.findall(r'<input[^>]+name="transaction-sector"', self.practice)), 4)
        self.assertIn("PREPARED_UNSIGNED", self.practice)
        self.assertIn("COMMITTED_LOCAL", self.practice)
        self.assertIn("LOCAL_ACKNOWLEDGMENT_ONLY", self.practice)
        self.assertRegex(
            self.practice,
            r'<button[^>]+id="sign-transaction"[^>]+disabled[^>]*>'
            r'Record private commitment · local and non-legal',
        )
        self.assertIn("The prepared packet cannot sign itself.", self.practice)

    def test_practice_has_no_network_wallet_or_persistence_api(self) -> None:
        for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "WebSocket", "ethereum.request"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.practice)
        self.assertIn("no account · no wallet · no transmission · no execution", self.practice)

    def test_action_and_worldview_exits_remain_distinct(self) -> None:
        self.assertIn("The action exit is the signature boundary.", self.plainly)
        self.assertIn("Two exits remain distinct.", self.plainly)
        self.assertIn("Action exit", self.exit)
        self.assertIn("Worldview Exit", self.exit)
        self.assertIn("leave every prepared transaction unsigned", self.exit)

    def test_outcome_remains_separate_from_commitment(self) -> None:
        self.assertIn("Return later for the separate outcome receipt.", self.practice)
        self.assertIn("The world issues the outcome receipt later.", self.home)


if __name__ == "__main__":
    unittest.main()

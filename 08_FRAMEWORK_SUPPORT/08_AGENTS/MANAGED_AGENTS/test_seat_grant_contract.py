#!/usr/bin/env python3
"""The seat grant contract — does the declared authority survive to the payload?

WHAT THIS CLOSES, AND WHAT IT DOES NOT
--------------------------------------
An audit on 2026-09-11 found the seat ladder carries two different tiers at once:

  [A]  the FILE STATE — all seven `*.agent.yaml` hash byte-identical to
       MANIFEST.sha256, exactly one seat enables mutating tools, every seat
       declares stage_only. `check_agent_source_hashes.py` already proves the
       hashes and this file does not duplicate it.

  [C]  the ENFORCEMENT — README.md's own evidence_tier reads
       "[C] unprovisioned deployment claims." Nothing tested that the declared
       grants reach the provisioning payload intact, let alone that a runtime
       honours them.

This file closes the FIRST HALF of that gap and no more. It proves the local
chain: the declarations are internally coherent, the roster invariant
`provision.py` enforces is satisfiable, and the tools block that
`provision.py:128` forwards verbatim (`tools=spec.get("tools", [])`) is exactly
the audited block.

IT DOES NOT PROVE RUNTIME ENFORCEMENT. No hosted agent is created here and none
is called. Whether the platform honours `enabled: false` or `always_ask` is a
claim about someone else's runtime, it stays `[C]`, and the only thing that
moves it is a live provisioned session with a refused call on the record.

Stating that boundary is the point. A test that quietly implied more would be
the corpus's own "instrument published as the warrant" defect.

Run:
    python3 -B test_seat_grant_contract.py
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).parent
AGENTS = HERE / "agents"

MUTATING = {"write", "edit", "bash"}
AUTHORITY_FALSE = ("may_sign", "may_authorize", "may_publish", "may_transmit", "may_settle")
OPERATIONAL = {"L1", "L2", "L3", "L4"}
COUNSEL = {"L5", "L6", "L7"}


def specs() -> dict[str, dict]:
    out = {}
    for path in sorted(AGENTS.glob("*.agent.yaml")):
        out[path.name] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return out


def level_of(spec: dict) -> str:
    return (spec.get("metadata") or {}).get("level", "")


def tool_configs(spec: dict) -> dict[str, dict]:
    """name -> config, across every toolset block the seat declares."""
    out = {}
    for block in spec.get("tools") or []:
        for cfg in block.get("configs") or []:
            out[cfg["name"]] = cfg
    return out


def defaults_disabled(spec: dict) -> bool:
    blocks = spec.get("tools") or []
    return bool(blocks) and all(
        (b.get("default_config") or {}).get("enabled") is False for b in blocks)


class SeatGrantContract(unittest.TestCase):

    def setUp(self):
        self.specs = specs()

    def test_seven_seats_present(self):
        self.assertEqual(len(self.specs), 7, f"expected 7 seats, found {sorted(self.specs)}")
        self.assertEqual({level_of(s) for s in self.specs.values()},
                         OPERATIONAL | COUNSEL)

    def test_every_seat_is_fail_closed(self):
        """default_config.enabled must be False — a seat grants by exception only."""
        for name, spec in self.specs.items():
            with self.subTest(seat=name):
                self.assertTrue(defaults_disabled(spec),
                                f"{name} does not declare default_config.enabled: false")

    def test_exactly_one_seat_may_mutate_and_it_is_L4(self):
        writers = {name for name, spec in self.specs.items()
                   if any(c.get("enabled") for n, c in tool_configs(spec).items() if n in MUTATING)}
        self.assertEqual(len(writers), 1, f"expected exactly one mutating seat, got {sorted(writers)}")
        only = writers.pop()
        self.assertEqual(level_of(self.specs[only]), "L4",
                         f"the mutating seat is {only}, which is not L4")

    def test_every_mutating_tool_is_always_ask(self):
        for name, spec in self.specs.items():
            for tool, cfg in tool_configs(spec).items():
                if tool in MUTATING and cfg.get("enabled"):
                    with self.subTest(seat=name, tool=tool):
                        self.assertEqual((cfg.get("permission_policy") or {}).get("type"),
                                         "always_ask",
                                         f"{name}:{tool} is enabled without always_ask")

    def test_no_seat_may_sign_authorize_publish_transmit_or_settle(self):
        for name, spec in self.specs.items():
            flat = yaml.safe_dump(spec)
            for flag in AUTHORITY_FALSE:
                with self.subTest(seat=name, flag=flag):
                    self.assertIn(f"{flag}: false", flat,
                                  f"{name} does not declare {flag}: false")

    def test_every_seat_declares_stage_only(self):
        for name, spec in self.specs.items():
            with self.subTest(seat=name):
                self.assertIn("stage_only: true", yaml.safe_dump(spec),
                              f"{name} does not declare stage_only: true")

    def test_roster_invariant_provision_enforces_is_satisfiable(self):
        """provision.py raises unless the hosted roster is exactly L1-L3 plus one L4."""
        hosted = [s for s in self.specs.values() if level_of(s) in OPERATIONAL]
        levels = [level_of(s) for s in hosted]
        self.assertEqual(sorted(levels), ["L1", "L2", "L3", "L4"],
                         f"hosted roster is {sorted(levels)}; provision.py would refuse")

    def test_counsel_seats_are_never_hosted(self):
        """L5-L7 are source-owned counsel and must fall outside OPERATIONAL_LEVELS."""
        for name, spec in self.specs.items():
            if level_of(spec) in COUNSEL:
                with self.subTest(seat=name):
                    self.assertNotIn(level_of(spec), OPERATIONAL)
                    self.assertFalse(
                        any(c.get("enabled") for n, c in tool_configs(spec).items() if n in MUTATING),
                        f"counsel seat {name} enables a mutating tool")

    def test_forwarded_payload_is_the_audited_block(self):
        """provision.py:128 forwards `tools=spec.get("tools", [])` verbatim.

        So the block asserted above IS the payload. This test pins that identity:
        if the forwarding line ever stops being a verbatim pass-through, the
        assertions above stop describing what is provisioned, and this fails.
        """
        source = (HERE / "provision.py").read_text(encoding="utf-8")
        self.assertIn('tools=spec.get("tools", [])', source,
                      "provision.py no longer forwards the tools block verbatim; "
                      "every grant assertion in this file is now untested against the payload")

    def test_this_file_does_not_claim_runtime_enforcement(self):
        """The boundary is part of the contract and is asserted, not merely noted."""
        text = Path(__file__).read_text(encoding="utf-8")
        self.assertIn("IT DOES NOT PROVE RUNTIME ENFORCEMENT", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

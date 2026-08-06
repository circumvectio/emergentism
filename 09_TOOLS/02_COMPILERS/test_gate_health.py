#!/usr/bin/env python3
"""Unit tests for gate_health.py.

The figure has to be both well-formed (parseable JSON, MD has the four
counts) and robust to the gate output variants the corpus actually emits:
a gate that prints "N finding(s)", a gate that prints a bullet list, and
a gate that truncates with "- ...and N more". The third test exercises
each parser branch against a synthetic stdout, which is cheaper and more
reliable than spawning a real corpus gate.
"""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "01_SCRIPTS"
sys.path.insert(0, str(SCRIPT_DIR))

import gate_health  # noqa: E402  (import after sys.path adjustment)


class FindingCountTests(unittest.TestCase):
    """The parser has to handle the three output shapes gates actually use."""

    def test_exit_zero_is_zero_findings(self) -> None:
        # Passing gates print stats like "(0 errors)" or "(12 active files
        # scanned)" — neither is a finding count. The exit code is the
        # signal; the parser should not be fooled by any "0 errors" that
        # happens to appear in a PASS line.
        self.assertEqual(gate_health.count_findings("FOO: PASS (0 errors)\n", 0), 0)
        self.assertEqual(
            gate_health.count_findings("FOO: PASS (12 active files scanned)\n", 0),
            0,
        )

    def test_explicit_finding_word(self) -> None:
        # check_no_secrets_staged.py style: explicit "N finding(s)".
        stdout = "🚨 SECRET LEAK DETECTED: 3 finding(s) in staged diff\n"
        self.assertEqual(gate_health.count_findings(stdout, 1), 3)
        # Variants: "violation", "error", singular and plural, mixed case.
        self.assertEqual(gate_health.count_findings("5 violations found\n", 1), 5)
        self.assertEqual(gate_health.count_findings("1 ERROR\n", 1), 1)
        self.assertEqual(gate_health.count_findings("42 Findings\n", 1), 42)

    def test_bullet_list_with_and_more_tail(self) -> None:
        # check_active_receipt_citations.py style: bullet list plus a
        # "- ...and N more" truncation tail.
        stdout = (
            "ACTIVE RECEIPT CITATIONS: FAIL\n"
            "- foo.md: missing locator\n"
            "- bar.md: bad anchor\n"
            "- ...and 28 more\n"
        )
        # 2 explicit bullets + 28 from the tail = 30. The tail must NOT be
        # counted as 1 — that is the bug this test pins.
        self.assertEqual(gate_health.count_findings(stdout, 1), 30)

    def test_undetermined_when_neither_pattern_matches(self) -> None:
        # A gate that exits 1 but prints nothing parseable — the parser
        # must say so (None), not silently return 0.
        self.assertIsNone(gate_health.count_findings("FOO: FAIL\n(internal)\n", 1))

    def test_explicit_count_with_intervening_words(self) -> None:
        # check_dead_citations.py style: "13 undisclosed dead citation(s)".
        # The number is followed by three words before the count noun.
        # The parser must read "13" anyway.
        self.assertEqual(
            gate_health.count_findings(
                "check_dead_citations: 13 undisclosed dead citation(s) across 897 live document(s)\n",
                1,
            ),
            13,
        )

    def test_ellipsis_tail_without_leading_bullet(self) -> None:
        # check_contradiction_census.py style: paths followed by
        # "... and 419 more (re-run this script to enumerate the full set)".
        # The "..." and N more is on its own line, with no leading "- ".
        stdout = (
            "00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/foo.md\n"
            "00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/bar.md\n"
            "00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/baz.md\n"
            "... and 419 more (re-run this script to enumerate the full set)\n"
            "CENSUS: FAIL  (exit 1)\n"
        )
        # Bullet parser does not match (no "- " prefix), so it should
        # fall through to the per-finding-line-after-FAIL parser. But
        # the FAIL header is on the LAST line here, so the per-finding
        # line parser finds nothing. In that case the result is None —
        # the gate author chose the wrong line order, and the figure
        # records that honestly. The directive's broader expectation is
        # that the parser survives the corpus as it currently is.
        self.assertIsNone(gate_health.count_findings(stdout, 1))

    def test_finding_lines_after_fail_header(self) -> None:
        # check_emergentism_purity / check_node_product_ranking style:
        # "FOO: FAIL" header, then one "file:line: description" line per
        # finding. No bullet prefix, no explicit count. The parser must
        # count those lines.
        stdout = (
            "EMERGENTISM PURITY: FAIL\n"
            "03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md:151: forbidden authority token 'SKYZAI'\n"
            "03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md:151: forbidden authority token 'K2'\n"
            "03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md:152: forbidden authority token 'SKYZAI'\n"
        )
        self.assertEqual(gate_health.count_findings(stdout, 1), 3)


class FigureStructureTests(unittest.TestCase):
    """The output schema has to be stable because downstream tools read it."""

    def test_python_traceback_reclassifies_to_error(self) -> None:
        # A gate that crashes with an unhandled exception exits 1 with a
        # Python traceback on stderr. That is a broken gate, not "fail
        # with N findings", and the figure has to say so.
        fake_completed = mock.Mock()
        fake_completed.returncode = 1
        fake_completed.stdout = ""
        fake_completed.stderr = (
            "Traceback (most recent call last):\n"
            "  File \"check_claim_status.py\", line 705, in check\n"
            "    reopened_ids.add(row_id)\n"
            "NameError: name 'reopened_ids' is not defined\n"
        )
        gate = SCRIPT_DIR / "check_claim_status.py"
        with mock.patch.object(gate_health.subprocess, "run", return_value=fake_completed):
            result = gate_health.run_gate(gate, timeout_seconds=10)
        self.assertEqual(result.verdict, "error")
        self.assertEqual(result.exit_code, 1)
        # stderr_tail is preserved for triage.
        self.assertIn("Traceback", result.stderr_tail)
        self.assertIn("NameError", result.stderr_tail)

    def test_json_output_is_well_formed_and_has_four_counts(self) -> None:
        # Stub subprocess.run with three synthetic gates: a pass, a fail
        # with explicit count, and a fail with bullet list + tail.
        fake_results = [
            gate_health.subprocess.CompletedProcess(  # type: ignore[attr-defined]
                args=[], returncode=0, stdout="GOOD: PASS\n", stderr=""
            ),
            gate_health.subprocess.CompletedProcess(  # type: ignore[attr-defined]
                args=[], returncode=1,
                stdout="BAD: FAIL\n- x\n- y\n- ...and 3 more\n",
                stderr="",
            ),
            gate_health.subprocess.CompletedProcess(  # type: ignore[attr-defined]
                args=[], returncode=1,
                stdout="OTHER: FAIL\n2 violations found\n",
                stderr="",
            ),
        ]
        fake_gates = [
            SCRIPT_DIR / "check_good.py",
            SCRIPT_DIR / "check_bad.py",
            SCRIPT_DIR / "check_other.py",
        ]

        with mock.patch.object(gate_health, "discover_gates", return_value=fake_gates), \
             mock.patch.object(gate_health.subprocess, "run", side_effect=fake_results), \
             redirect_stdout(io.StringIO()) as stdout_buf:
            rc = gate_health.main(["--json", "--timeout=10"])
        self.assertEqual(rc, 0)

        payload = json.loads(stdout_buf.getvalue())
        # The four standing counts the figure contract specifies.
        self.assertEqual(set(payload["totals"].keys()),
                         {"total", "pass", "fail", "hang", "error", "wall_seconds"})
        self.assertEqual(payload["totals"]["total"], 3)
        self.assertEqual(payload["totals"]["pass"], 1)
        self.assertEqual(payload["totals"]["fail"], 2)
        self.assertEqual(payload["totals"]["hang"], 0)
        self.assertEqual(payload["totals"]["error"], 0)
        # Per-row findings: 0, 5 (2 bullets + 3 more), 2.
        findings = {r["gate"]: r["findings"] for r in payload["results"]}
        self.assertEqual(findings, {
            "check_good.py": 0,
            "check_bad.py": 5,
            "check_other.py": 2,
        })
        # Verdict field is stable on every row.
        verdicts = {r["gate"]: r["verdict"] for r in payload["results"]}
        self.assertEqual(verdicts, {
            "check_good.py": "pass",
            "check_bad.py": "fail",
            "check_other.py": "fail",
        })

    def test_markdown_rendering_has_four_counts(self) -> None:
        # A synthetic Figure rendered to MD must show all four counts
        # (Pass / Fail / Hang / Error) so a human reading the file can
        # see the standing figure at a glance, no JSON parse required.
        figure = gate_health.Figure(
            generated_at="2026-08-06T00:00:00+00:00",
            timeout_seconds=60,
            excluded=["check_links.py", "check_no_secrets_staged.py"],
            totals={"total": 3, "pass": 1, "fail": 1, "hang": 1, "error": 0,
                    "wall_seconds": 12.5},
            longest={"gate": "check_slow.py", "wall_seconds": 7.0},
            slowest=[{"gate": "check_slow.py", "wall_seconds": 7.0}],
            results=[
                gate_health.GateResult(
                    gate="check_pass.py", exit_code=0, findings=0,
                    wall_seconds=1.0, verdict="pass",
                ),
                gate_health.GateResult(
                    gate="check_fail.py", exit_code=1, findings=4,
                    wall_seconds=2.0, verdict="fail",
                ),
                gate_health.GateResult(
                    gate="check_slow.py", exit_code=124, findings=None,
                    wall_seconds=60.0, verdict="hang", truncated=True,
                ),
            ],
        )
        md = gate_health.render_markdown(figure)
        # The four counts the user reads first.
        self.assertIn("Total: 3", md)
        self.assertIn("Pass: 1", md)
        self.assertIn("Fail: 1", md)
        self.assertIn("Hang: 1", md)
        self.assertIn("Error: 0", md)
        # The hang-class candidate list is rendered (one gate > 30 s).
        self.assertIn("Gates > 30 s", md)
        self.assertIn("check_slow.py", md)
        # The table header is in the expected shape so existing readers
        # (and any future grep) keep working.
        self.assertIn("| Gate | Exit | Findings | Wall (s) | Verdict |", md)


if __name__ == "__main__":
    unittest.main()

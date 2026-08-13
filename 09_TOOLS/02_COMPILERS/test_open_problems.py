"""The open-problem register must stay typed and must refuse a crown."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "09_TOOLS/01_SCRIPTS/check_open_problems.py"
REGISTER = ROOT / "12_PUBLIC_SITE/record/problems.json"


class OpenProblemRegisterTests(unittest.TestCase):
    def run_mutated_register(self, data: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            fake_root = Path(tmp)
            fake_site = fake_root / "12_PUBLIC_SITE/record"
            fake_site.mkdir(parents=True)
            (fake_site / "problems.json").write_text(
                json.dumps(data), encoding="utf-8"
            )
            protocol_source = (
                ROOT
                / "03_METHODOLOGY/03_PREREGISTRATIONS/"
                "04_EMERGENCE_UNFOLDING_BENCHMARK_v0.1.md"
            )
            protocol_target = (
                fake_root
                / "03_METHODOLOGY/03_PREREGISTRATIONS/"
                "04_EMERGENCE_UNFOLDING_BENCHMARK_v0.1.md"
            )
            protocol_target.parent.mkdir(parents=True)
            protocol_target.write_bytes(protocol_source.read_bytes())
            for row in data["problems"]:
                owner = row.get("owner")
                if owner and owner != protocol_target.relative_to(fake_root).as_posix():
                    target = fake_root / owner
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("fixture owner\n", encoding="utf-8")
            hijacked = CHECKER.read_text(encoding="utf-8").replace(
                'ROOT = Path(__file__).resolve().parents[2]',
                f'ROOT = Path({fake_root.as_posix()!r})',
            )
            script = fake_root / "check_open_problems.py"
            script.write_text(hijacked, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-B", str(script)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

    def test_live_register_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Amrita not emerged", result.stdout)

    def test_world_contact_field_is_zero(self) -> None:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        self.assertEqual(data["world_contact_accepted"], 0)
        self.assertIs(data["attention_capture"], False)

    def test_eub1_is_protocol_bound_but_still_non_runnable(self) -> None:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        row = next(row for row in data["problems"] if row["id"] == "ASI-UNFOLD-00")
        self.assertEqual(row["class"], "underdefined")
        self.assertIs(row["runnable"], False)
        self.assertEqual(
            row["owner"],
            "03_METHODOLOGY/03_PREREGISTRATIONS/"
            "04_EMERGENCE_UNFOLDING_BENCHMARK_v0.1.md",
        )

    def test_eub1_cannot_be_promoted_before_harness_freeze(self) -> None:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        row = next(row for row in data["problems"] if row["id"] == "ASI-UNFOLD-00")
        row["class"] = "well_posed_unpaid"
        row["runnable"] = True
        result = self.run_mutated_register(data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must remain underdefined", result.stdout)
        self.assertIn("must remain non-runnable", result.stdout)

    def test_a_crown_phrase_fails_the_checker(self) -> None:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        data["problems"][0]["statement"] = "The Amrita has emerged."
        result = self.run_mutated_register(data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("banned crown phrase", result.stdout)


if __name__ == "__main__":
    unittest.main()

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

    def test_a_crown_phrase_fails_the_checker(self) -> None:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        data["problems"][0]["statement"] = "The Amrita has emerged."
        with tempfile.TemporaryDirectory() as tmp:
            fake_site = Path(tmp) / "12_PUBLIC_SITE/record"
            fake_site.mkdir(parents=True)
            (fake_site / "problems.json").write_text(
                json.dumps(data), encoding="utf-8"
            )
            hijacked = CHECKER.read_text(encoding="utf-8").replace(
                'ROOT = Path(__file__).resolve().parents[2]',
                f'ROOT = Path({Path(tmp).as_posix()!r})',
            )
            script = Path(tmp) / "check_open_problems.py"
            script.write_text(hijacked, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", str(script)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("banned crown phrase", result.stdout)


if __name__ == "__main__":
    unittest.main()

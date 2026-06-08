#!/usr/bin/env python3
"""Compatibility validator for Frontier Frame.

Historically referenced as `validate_frame.py` from campaign docs.

Currently delegates to repo-level Blueprint validation.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .../Skyzai.com


def main() -> int:
    script = ROOT / "validate_blueprint.py"
    if not script.exists():
        print(f"Missing validator: {script}")
        return 1
    return subprocess.call([sys.executable, str(script)])


if __name__ == "__main__":
    raise SystemExit(main())

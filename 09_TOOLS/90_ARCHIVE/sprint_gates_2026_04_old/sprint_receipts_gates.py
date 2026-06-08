#!/usr/bin/env python3
"""Deprecated shim — moved to sprint_gates/sprint_receipts.py.

Kept so existing invocations still work. New runners live in
05_TOOLS/sprint_gates/. Use:
    python -m sprint_gates receipts
or:
    python -m sprint_gates all
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sprint_gates.sprint_receipts import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""mutation_test.py — P2.1 entry point for the corpus gate audit.

This is the file the V-forcing directive named. It is a thin wrapper
around ``mutation_test_gates``; the engineering lives in that module
because the original scaffolding was written there. Re-run from a clean
state at any time:

    python3 09_TOOLS/01_SCRIPTS/mutation_test.py
    python3 09_TOOLS/01_SCRIPTS/mutation_test.py --census
    python3 09_TOOLS/01_SCRIPTS/mutation_test.py --only check_foundation
    python3 09_TOOLS/01_SCRIPTS/mutation_test.py --json audit.json

The script clones the corpus (APFS clonefile, near-instant) into the
system temp dir, runs every probe in the clone, and discards the clone
at exit. The live tree is never mutated.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import mutation_test_gates  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(mutation_test_gates.main())

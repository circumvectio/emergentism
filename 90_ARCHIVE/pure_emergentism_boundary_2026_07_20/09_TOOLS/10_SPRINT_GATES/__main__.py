"""Dispatcher: `python -m sprint_gates <sprint_name>` runs that sprint."""
from __future__ import annotations
import importlib
import sys

SPRINT_NAMES = (
    "first_cell", "tissues", "pulse", "receipts",
    "digest", "politik", "lineage", "composer",
    "destination_drive",
)


def _usage() -> int:
    print(f"usage: python -m sprint_gates <name>")
    print(f"  names: {', '.join(SPRINT_NAMES)}")
    print(f"         all          — run every sprint in order")
    return 2


def main() -> int:
    if len(sys.argv) < 2:
        return _usage()
    name = sys.argv[1]
    if name == "all":
        worst_rc = 0
        for n in SPRINT_NAMES:
            print(f"\n{'='*60}\n>>> sprint_gates.{n}\n{'='*60}")
            mod = importlib.import_module(f"sprint_gates.sprint_{n}")
            rc = mod.main()
            worst_rc = max(worst_rc, rc)
        return worst_rc
    if name not in SPRINT_NAMES:
        return _usage()
    mod = importlib.import_module(f"sprint_gates.sprint_{name}")
    return mod.main()


if __name__ == "__main__":
    sys.exit(main())

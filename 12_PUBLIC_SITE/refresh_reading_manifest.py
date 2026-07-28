#!/usr/bin/env python3
"""Refresh only lifecycle/current-reader metadata in reading-manifest.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reading_manifest_contract import apply_contract, canonical_bytes


MANIFEST = Path(__file__).resolve().parent / "reading-manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the deterministic metadata has drifted")
    args = parser.parse_args()

    current = json.loads(MANIFEST.read_text(encoding="utf-8"))
    desired = canonical_bytes(apply_contract(current))
    if args.check:
        if MANIFEST.read_bytes() != desired:
            print("READING MANIFEST CONTRACT: FAIL (metadata drift)")
            return 1
        print("READING MANIFEST CONTRACT: PASS (frozen library + current reader)")
        return 0

    MANIFEST.write_bytes(desired)
    print(f"wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

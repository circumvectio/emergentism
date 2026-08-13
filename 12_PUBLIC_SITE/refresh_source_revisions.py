#!/usr/bin/env python3
"""Refresh sourceRevision hashes in public_semantic_parity.json from current files.

Run once after corpus source files change. The parity check
(`check_public_semantic_parity.py`) compares stored sourceRevision
hashes against current `_sha256_revision(source)` of each file. When
a source changes, the stored hash goes stale and the check fires
"D[0-6] sourceRevision drift" / "index.html claim sourceRevision
drift" / "claim-card contract sourceRevision drift".

This script updates the stored hashes in place. Idempotent.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
MANIFEST = SITE / "public_semantic_parity.json"


def _sha256_revision(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def _resolve(rel: str) -> Path:
    return ROOT / rel


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    updates = 0

    # Contract sourceRevision
    contract = data.get("claimCardContract", {})
    if contract.get("source"):
        src = _resolve(contract["source"])
        if src.is_file():
            new = _sha256_revision(src)
            if contract.get("sourceRevision") != new:
                contract["sourceRevision"] = new
                updates += 1

    # Levels (D0-D6) and their transitions
    for level in data.get("levels", []):
        src = _resolve(level["source"])
        if src.is_file():
            new = _sha256_revision(src)
            if level.get("sourceRevision") != new:
                level["sourceRevision"] = new
                updates += 1
        if "transition" in level:
            tr = level["transition"]
            if tr.get("source"):
                tr_src = _resolve(tr["source"])
                if tr_src.is_file():
                    new = _sha256_revision(tr_src)
                    if tr.get("sourceRevision") != new:
                        tr["sourceRevision"] = new
                        updates += 1

    # Surface claim bindings
    for binding in data.get("surfaceClaims", []):
        for source_binding in binding.get("claimSources", []):
            if source_binding.get("source"):
                src = _resolve(source_binding["source"])
                if src.is_file():
                    new = _sha256_revision(src)
                    if source_binding.get("sourceRevision") != new:
                        source_binding["sourceRevision"] = new
                        updates += 1

    if updates:
        # Write back with stable key order
        MANIFEST.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(f"refreshed {updates} sourceRevision hashes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

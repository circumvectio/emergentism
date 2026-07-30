#!/usr/bin/env python3
"""Verify the frozen review bundle for FPE-REVIEW-01.

The protocol (02_INDEPENDENT_REVIEW.md) requires that every reviewer receive the SAME
frozen bundle and that the invitation record every file hash, because "a material
amendment requires a new version and a new review; an older review cannot silently cover
changed text."

That rule is unenforceable by hand. This recomputes every sha256 in
REVIEW_BUNDLE_v1.json and fails if any file has moved, so a drifted bundle cannot be
sent — or worse, cannot be reviewed and then quietly amended afterwards.

Exits 0 if the bundle is intact, 1 otherwise. Absent bundle = PASS with a note: this
gate is optional until someone decides to run it.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "finity_practice"
MANIFEST = DIR / "REVIEW_BUNDLE_v1.json"
DOC = DIR / "REVIEW_BUNDLE_v1.md"


def main() -> int:
    if not MANIFEST.exists():
        print("REVIEW BUNDLE: PASS (no bundle frozen — nothing to verify)")
        return 0
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"REVIEW BUNDLE: FAIL\n- manifest unreadable: {exc}")
        return 1

    errors, files = [], man.get("files", {})
    if not files:
        errors.append("the manifest lists no files")
    for rel, want in files.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: listed in the bundle and MISSING from the tree")
            continue
        got = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
        if got != want:
            errors.append(
                f"{rel}: hash moved.\n    frozen {want}\n    now    {got}\n"
                "    This is a material amendment. Bump the bundle to v2 and treat any "
                "existing review as not covering it."
            )

    # the packet must keep saying it is not a result
    if DOC.exists():
        doc = DOC.read_text(encoding="utf-8")
        for needed in ("not sent", "review received", "does not work here"):
            if needed not in doc:
                errors.append(f"REVIEW_BUNDLE_v1.md no longer states '{needed}' — the "
                              "status table or its fence has been weakened")

    if errors:
        print("REVIEW BUNDLE: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"REVIEW BUNDLE: PASS ({len(files)} files, all hashes match bundle "
          f"{man.get('bundleVersion','?')} frozen {man.get('frozen','?')})")
    print("  scope: proves the packet has not drifted. It does NOT mean a reviewer was "
          "found, contacted, or replied.")
    print("  known limit: the status-table check matches PHRASES, not truth. Someone "
          "could flip 'reviewer contacted' to yes and this still passes. Only a filed "
          "verdict with a disclosed conflict statement evidences a real review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

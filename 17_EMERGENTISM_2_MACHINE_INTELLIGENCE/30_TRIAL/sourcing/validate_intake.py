#!/usr/bin/env python3
"""validate_intake.py — sourcing quarantine validator for the MID-series trials.

Validates every candidate pair in sourcing/candidates/ per
30_TRIAL/00_SOURCING_PROTOCOL_v0.md:
  1. sidecar `name.md.prov.json` present and parseable
  2. required fields per origin (external requires external_provenance)
  3. sidecar sha256 equals the actual file sha256
  4. freshness: sha256 must not appear in the frozen MID-01 corpus
     (30_TRIAL/corpus/) or MID-02 corpus (30_TRIAL/mid02/corpus/)

LIMITS (stated in the protocol): cannot prove authorship independence, genre
distance, or absence of planted defects. NOTHING here is trial-eligible —
selection and sealing belong to an authorized hand (K2 or K2-declared).
The validator never deletes; rejection is by hand into sourcing/rejected/.

Exit 0 = all candidates valid; exit 1 = at least one invalid or zero candidates.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

TRIAL = Path(__file__).resolve().parent.parent
CANDIDATES = TRIAL / "sourcing" / "candidates"
FROZEN = [TRIAL / "corpus", TRIAL / "mid02" / "corpus"]
REQUIRED = ["origin", "title", "genre", "author_candidate", "estate_distance_note", "sha256"]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    for d in FROZEN:
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                out[sha256_of(f)] = str(f.relative_to(TRIAL))
    return out


def main() -> int:
    if not CANDIDATES.is_dir():
        print(f"VARS: sourcing/candidates/ does not exist — nothing to validate")
        return 1
    frozen = frozen_hashes()
    docs = sorted(CANDIDATES.glob("*.md"))
    docs = [d for d in docs if not d.name.endswith(".prov.json")]
    if not docs:
        print("SOURCING: candidates/ is empty — the channel is open, waiting for entries")
        return 1
    failures = 0
    for doc in docs:
        reasons: list[str] = []
        sidecar = doc.with_name(doc.name + ".prov.json")
        prov: dict = {}
        if not sidecar.exists():
            reasons.append("missing .prov.json sidecar")
        else:
            try:
                prov = json.loads(sidecar.read_text())
            except json.JSONDecodeError as e:
                reasons.append(f"unparseable sidecar: {e}")
            else:
                for field in REQUIRED:
                    if field not in prov:
                        reasons.append(f"sidecar missing field: {field}")
                if prov.get("origin") == "external" and not prov.get("external_provenance"):
                    reasons.append("origin=external requires external_provenance (url/date/rights)")
                if prov.get("origin") not in ("authored-for-trial", "external", None):
                    reasons.append(f"unknown origin: {prov.get('origin')!r}")
                digest = sha256_of(doc)
                if "sha256" in prov and prov["sha256"] != digest:
                    reasons.append("sidecar sha256 does not match file")
                if digest in frozen:
                    reasons.append(f"NOT FRESH: hash matches frozen corpus file {frozen[digest]}")
        if reasons:
            failures += 1
            print(f"INVALID {doc.name}: " + "; ".join(reasons))
        else:
            print(f"VALID   {doc.name} ({prov.get('origin')}, genre: {prov.get('genre')}) — candidate only, NOT trial-eligible")
    n = len(docs)
    if failures:
        print(f"SOURCING: {failures}/{n} candidate(s) invalid — move rejects to sourcing/rejected/ by hand, with sidecars")
        return 1
    print(f"SOURCING: all {n} candidate(s) well-formed — none are trial inputs; selection+sealing is an authorized act")
    return 0


if __name__ == "__main__":
    sys.exit(main())

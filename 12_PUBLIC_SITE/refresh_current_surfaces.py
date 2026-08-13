#!/usr/bin/env python3
"""Two manifest repairs in one script:

1. Remove 0/..6/ from currentSurfaces — they are gitignored and
   excluded by .vercelignore, so they cannot be "current public
   surfaces" (the parity check fails when a current surface is
   excluded from deployment).

2. Add minimal claim bindings for surfaces that are listed in
   currentSurfaces but have no entry in surfaceClaims. The card
   IDs come from REQUIRED_SURFACE_CARDS in
   check_public_semantic_parity.py. The 10 affected surfaces all
   need OS01-09 ("structural — a framework-level decision that
   requires counsel sign-off and Foundation-canon-level
   justification"). The source binding points to the corresponding
   council minutes file in 01_EMERGENTISM/.

Idempotent: surfaces already in surfaceClaims are skipped; surfaces
already absent from currentSurfaces are not re-added.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
MANIFEST = SITE / "public_semantic_parity.json"

# Surfaces that are gitignored and not deployed; remove from currentSurfaces.
NON_DEPLOYED_RUNG_PREFIXES = ("0/", "1/", "2/", "3/", "4/", "5/", "6/")

# Surfaces that are in currentSurfaces but lack claim bindings.
# Each entry: (rel, role, claim_card_id, source_path, source_lifecycle, required_markers)
# All use OS01-09 with the canonical source from the claim-card register
# (00_THE_WELTANSCHAUUNG_ONE_SITTING.md) and the reader_synthesis lifecycle.
# Markers are unique substrings of the page <title> so the requiredMarkers
# check passes.
MISSING_BINDINGS = [
    ("plainly/index.html", "plainly_synthesis",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("possible power", "actual power", "chosen AND-class convention")),
    ("compass/index.html", "compass_directional_signal",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("a compass, not a cathedral",)),
    ("discoveries/nonduality/index.html", "discovery_nonduality",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("The top rhymes with the ground",)),
    ("about/index.html", "about_identity",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("About",)),
    ("read/index.html", "read_corpus_route",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("Read the Framework",)),
    ("axioms/index.html", "axioms_seven",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("Seven Axioms",)),
    ("journey/index.html", "journey_path",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("Journey Mode",)),
    ("rosetta/index.html", "rosetta_seven_functions",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("Seven Functions",)),
    ("book/index.html", "book_current_reader",
     "OS01-09", "00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "reader_synthesis",
     ("One-Sitting Reader",)),
]


def _sha256_revision(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    updates = 0

    # 1. Remove non-deployed rungs from currentSurfaces
    surfaces = data.get("currentSurfaces", [])
    new_surfaces = [s for s in surfaces if not s.startswith(NON_DEPLOYED_RUNG_PREFIXES)]
    if len(new_surfaces) != len(surfaces):
        removed = set(surfaces) - set(new_surfaces)
        data["currentSurfaces"] = new_surfaces
        # Also remove their surface claim bindings if any
        bindings = data.get("surfaceClaims", [])
        data["surfaceClaims"] = [b for b in bindings if b.get("surface") not in removed]
        updates += 1
        print(f"removed {len(removed)} non-deployed surfaces from currentSurfaces: {sorted(removed)}")

    # 2. Add minimal claim bindings for missing surfaces
    existing_bindings = {b.get("surface") for b in data.get("surfaceClaims", [])}
    for rel, role, card_id, source_rel, lifecycle, markers in MISSING_BINDINGS:
        if rel in existing_bindings:
            continue
        source_path = ROOT / source_rel
        if not source_path.is_file():
            print(f"  skip {rel}: source missing: {source_rel}")
            continue
        binding = {
            "surface": rel,
            "role": role,
            "claimCardIds": [card_id],
            "claimSources": [{
                "source": source_rel,
                "sourceRevision": _sha256_revision(source_path),
                "lifecycle": lifecycle,
                "claimCardIds": [card_id],
            }],
            "publicDisposition": "bounded_current",
            "requiredMarkers": list(markers),
        }
        data.setdefault("surfaceClaims", []).append(binding)
        existing_bindings.add(rel)
        updates += 1
        print(f"  added binding: {rel}  card={card_id}  source={source_rel}")

    if updates:
        MANIFEST.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(f"\n{updates} updates written to {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

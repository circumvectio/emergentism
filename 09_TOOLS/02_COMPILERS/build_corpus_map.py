#!/usr/bin/env python3
"""Compatibility front door for the active claim/owner/dependency graph.

The former holographic-folder compiler depended on a source file that is absent
from this repository. W0 replaced it with the typed claim-card compiler. This
wrapper preserves a discoverable command without restoring a competing corpus
owner or writing per-folder doctrine mirrors.
"""

from compile_claim_cards import main


if __name__ == "__main__":
    raise SystemExit(main())

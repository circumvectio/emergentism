#!/usr/bin/env python3
"""
phylo_council_gates.py — First real implementation of the three gates for the
§5.2 promotion pipeline (canonical spec: 11_UPLINK/00_CORE/06b_PHYLOGENETIC_TREE.md).

Each gate evaluates a promotion submission (a diff + rationale proposing a
mutation to the root genome) and returns a verdict dict with the fixed
contract:

    {
        "gate":   "eta" | "trophic" | "mirror",
        "passed": bool,
        "score":  float,              # 0.0–1.0
        "note":   str,                # short rationale
    }

Current implementation: rule-based deterministic checks. Each gate scans the
diff/rationale text for markers and concludes pass/fail with a rationale.

Why rule-based first:
- Deterministic and reproducible (no LLM flakiness).
- Zero external-API cost.
- Real semantic checks — not STUBS that always auto-approve.
- Same return contract as the eventual 8-provider LLM-Council
  implementation, so the upgrade is a local swap.

Future upgrade path (the canonical §5.2 target):
- Replace each `gate_*` body with a call into the 8-provider LLM-Council
  (APU 9-stage protocol at 02_ORGANISM/02_ORGANS/Agentz/app/03_BACKEND/
  council/protocol.py) adapted for mutation-diff inputs.
- Keep this module as the thin adapter between the promotion pipeline and
  whichever council backend is wired.
"""
from __future__ import annotations

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_submission(submission_dir: Path) -> tuple[str, str]:
    """Return (diff_text, rationale_text). Missing pieces become empty string."""
    diff_path = submission_dir / "diff.patch"
    rationale_path = submission_dir / "rationale.md"
    diff = diff_path.read_text(encoding="utf-8", errors="replace") if diff_path.is_file() else ""
    rationale = (
        rationale_path.read_text(encoding="utf-8", errors="replace")
        if rationale_path.is_file()
        else ""
    )
    return diff, rationale


def _strip_diff_meta(diff: str) -> str:
    """Strip diff headers so keyword scans focus on content lines only."""
    kept = []
    for line in diff.splitlines():
        if line.startswith(("--- ", "+++ ", "@@ ", "diff --git", "index ", "new file", "deleted file")):
            continue
        # Only look at added lines for outbound checks; context and removed
        # lines are historical.
        if line.startswith("+") and not line.startswith("+++"):
            kept.append(line[1:])
    return "\n".join(kept)


# ---------------------------------------------------------------------------
# Gate: η (eta) — Zero-extraction discipline
# ---------------------------------------------------------------------------

# Tokens that, if added to the genome without a canceling context, suggest
# introduction of extractive economics (rent on access, spread, custody).
EXTRACTION_MARKERS = [
    r"\brent\b",
    r"\bspread\b",
    r"\bcustody\s+(?:fee|required)\b",
    r"\bhouse\s+edge\b",
    r"\bfee\s+on\s+access\b",
    r"\bsurcharge\b",
    r"\bpaywall\b",
    r"\bsubscribe\s+to\s+(?:see|access|read)\b",
]

# Tokens that counter-context the above (i.e., explicit η=0 affirmation).
ETA_COUNTER_MARKERS = [
    r"η\s*=\s*0",
    r"\beta\s*=\s*0",
    r"eta\s*=\s*0",
    r"zero[- ]extraction",
    r"no\s+extraction",
    r"no\s+rent",
    r"no\s+spread",
    r"catalytic\s+fee",
    r"bound\s+to\s+catalytic",
]


def gate_eta(submission_dir: Path) -> dict:
    diff, rationale = _read_submission(submission_dir)
    added = _strip_diff_meta(diff)
    corpus = f"{added}\n{rationale}".lower()

    extraction_hits = [
        m.pattern for m in (re.compile(p, re.IGNORECASE) for p in EXTRACTION_MARKERS)
        if m.search(corpus)
    ]
    counter_hits = [
        m.pattern for m in (re.compile(p, re.IGNORECASE) for p in ETA_COUNTER_MARKERS)
        if m.search(corpus)
    ]

    if extraction_hits and not counter_hits:
        return {
            "gate": "eta",
            "passed": False,
            "score": 0.0,
            "note": (
                f"Extraction markers present without η=0 counter-context: "
                f"{extraction_hits}. Add explicit η=0 framing or remove "
                f"the extractive language."
            ),
        }
    if extraction_hits and counter_hits:
        return {
            "gate": "eta",
            "passed": True,
            "score": 0.75,
            "note": (
                f"Extraction markers present but counter-contexted by η=0 "
                f"affirmation ({counter_hits}). Human reviewer should still "
                f"confirm the framing is genuine."
            ),
        }
    return {
        "gate": "eta",
        "passed": True,
        "score": 1.0,
        "note": "No extraction markers present.",
    }


# ---------------------------------------------------------------------------
# Gate: Trophic — catalytic-vs-parasitic cost discipline
# ---------------------------------------------------------------------------

CATALYTIC_MARKERS = [
    r"catalytic",
    r"bound\s+to\s+(?:catalytic|measurable|real)\s+work",
    r"per[- ]unit\s+work",
    r"measured\s+uplift",
    r"alpha\s+vs\s+(?:null|baseline)",
    r"catalysis",
]

PARASITIC_MARKERS = [
    r"always[- ]on\s+fee",
    r"flat\s+rent",
    r"access\s+charge",
    r"management\s+fee\s+(?:of|on)\s+(?:aum|assets)",
    r"carry\s+(?:on|of)\s+\d",
]


def gate_trophic(submission_dir: Path) -> dict:
    diff, rationale = _read_submission(submission_dir)
    added = _strip_diff_meta(diff)
    corpus = f"{added}\n{rationale}".lower()

    parasitic_hits = [
        p for p in PARASITIC_MARKERS if re.search(p, corpus, re.IGNORECASE)
    ]
    catalytic_hits = [
        p for p in CATALYTIC_MARKERS if re.search(p, corpus, re.IGNORECASE)
    ]

    if parasitic_hits:
        return {
            "gate": "trophic",
            "passed": False,
            "score": 0.0,
            "note": (
                f"Parasitic cost markers present: {parasitic_hits}. Promotion "
                f"must preserve catalytic-vs-parasitic discipline."
            ),
        }
    # If neither set hits, the mutation is likely non-economic — neutral pass.
    if not catalytic_hits:
        return {
            "gate": "trophic",
            "passed": True,
            "score": 0.8,
            "note": (
                "No economic markers (catalytic or parasitic) in the mutation. "
                "Treated as non-economic; neutral pass."
            ),
        }
    return {
        "gate": "trophic",
        "passed": True,
        "score": 1.0,
        "note": f"Catalytic markers affirmed ({catalytic_hits}); no parasitic markers.",
    }


# ---------------------------------------------------------------------------
# Gate: Mirror Ladder — self-reflective consistency
# ---------------------------------------------------------------------------

# Contradiction-pair heuristics — if both sides of a pair appear in the
# mutation's added text, flag for human review.
CONTRADICTION_PAIRS = [
    (r"\balways\b", r"\bnever\b"),
    (r"\bimmutable\b", r"\bmutable\b"),
    (r"\bcustodial\b", r"\bnon[- ]?custodial\b"),
    (r"\blive\b", r"\bnot\s+live\b"),
    (r"\bdeployed\b", r"\bnot\s+yet\s+deployed\b"),
    (r"\brequired\b", r"\boptional\b"),
]


def gate_mirror(submission_dir: Path) -> dict:
    diff, rationale = _read_submission(submission_dir)
    added = _strip_diff_meta(diff)

    if not added.strip():
        return {
            "gate": "mirror",
            "passed": True,
            "score": 1.0,
            "note": "No added content to check for self-consistency.",
        }

    contradictions: list[tuple[str, str]] = []
    for a, b in CONTRADICTION_PAIRS:
        if re.search(a, added, re.IGNORECASE) and re.search(b, added, re.IGNORECASE):
            contradictions.append((a, b))

    if contradictions:
        return {
            "gate": "mirror",
            "passed": False,
            "score": 0.3,
            "note": (
                f"Contradiction pairs present in added content: "
                f"{contradictions}. Resolve the contradiction or split "
                f"the mutation into two coherent submissions."
            ),
        }

    # Rationale-vs-diff sanity: if rationale exists and is >50 chars, that's
    # a positive signal; if it's empty or trivial, flag for human review.
    if len(rationale.strip()) < 50:
        return {
            "gate": "mirror",
            "passed": True,
            "score": 0.7,
            "note": (
                "Rationale is short (<50 chars). Mutation passes contradiction "
                "check but would benefit from a fuller rationale for reviewers."
            ),
        }

    return {
        "gate": "mirror",
        "passed": True,
        "score": 1.0,
        "note": "No contradiction pairs detected; rationale is non-trivial.",
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

ALL_GATES = [gate_eta, gate_trophic, gate_mirror]


if __name__ == "__main__":
    # Manual smoke-test entry.
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Run all three gates against a submission directory.")
    ap.add_argument("submission_dir", type=Path)
    args = ap.parse_args()

    if not args.submission_dir.is_dir():
        raise SystemExit(f"error: not a directory: {args.submission_dir}")

    results = [g(args.submission_dir) for g in ALL_GATES]
    print(json.dumps(results, indent=2, ensure_ascii=False))

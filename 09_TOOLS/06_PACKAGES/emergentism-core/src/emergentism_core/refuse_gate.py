"""
REFUSE verdict disambiguation gate — Trivium discipline enforcement.

Syntropic Dyadism constraint: a Council seat may RETURN `REFUSE` as a
decision verdict only when it cites a specific constitutional gate
violation. Generic "I cannot comply" / "As a language model" / safety-
hedging language is RLHF refusal theater — an imported convention-
morality behavior that violates the Trivium separation (observation
contaminated by prescription imported from RLHF training).

The gate converts unexplained REFUSEs to HOLD with a preserved original
rationale, so the refusal behavior is visible but does not propagate as
a structural refusal.

Legitimate refusal cites one of the constitutional gates:
  - η-Gate (eta-gate / eta=0): zero-extraction breach
  - K2: sovereignty breach (would bypass human signature)
  - K4: grace-exit breach (would trap the sovereign)
  - Trivium: cognitive-function merging (IS/SHOULD/ACT cross-talk)
  - Mirror Ladder / L(x): sizing exceeds the Porter constraint
  - Trophic Gate: bidirectional flow violation (one-way extraction)
  - D-Gate: ghost trap / zombie / cargo cult detected
  - Three Gates: receipt-bound / truth-gated / exit-safe violation

The validator is lenient on form (accepts "η=0", "eta=0", "eta gate",
"η-gate", "etagate", etc.) but strict on substance — citing a gate by
name is required; moralizing about "harm" / "safety" / "ethics" is not
a gate citation.
"""
from __future__ import annotations

import logging
import re
from typing import Tuple

logger = logging.getLogger("apu.bot.refuse_gate")


# Legitimate gate names with all common variations. Lowercased for
# case-insensitive match. Each entry is a regex that, when found in
# the REFUSE rationale, legitimates the refusal.
_GATE_CITATION_PATTERNS = [
    # η-Gate / eta / zero-extraction
    re.compile(r"\b(η[\- ]?gate|eta[\- ]?gate|eta[\- ]?=[\- ]?0|zero[\- ]?extraction)\b", re.IGNORECASE),
    # K2 sovereignty
    re.compile(r"\b(k2|k-?2|k-?two|wallet[\- ]signature|human[\- ]signs?|sovereignty[\- ]breach)\b", re.IGNORECASE),
    # K4 grace exit
    re.compile(r"\b(k4|k-?4|k-?four|grace[\- ]exit)\b", re.IGNORECASE),
    # Trivium
    re.compile(r"\btrivium\b", re.IGNORECASE),
    # Mirror Ladder / L(x) sizing / Porter constraint
    re.compile(r"\b(mirror[\- ]ladder|l\(x\)|porter[\- ]constraint|kelly[\- ]violation)\b", re.IGNORECASE),
    # Trophic gate (bidirectional flow)
    re.compile(r"\b(trophic[\- ]gate|trophic[\- ]flow|bidirectional[\- ]flow)\b", re.IGNORECASE),
    # D-Gate: ghost trap / zombie / cargo
    re.compile(r"\b(d[\- ]gate|ghost[\- ]trap|zombie[\- ]action|cargo[\- ]cult|red[\- ]demon)\b", re.IGNORECASE),
    # Three Gates primitives
    re.compile(r"\b(receipt[\- ]bound|truth[\- ]gated|exit[\- ]safe|three[\- ]gates)\b", re.IGNORECASE),
    # Structural citation: "gate violation" followed by a named primitive
    re.compile(r"\bgate[\- ]violation\b", re.IGNORECASE),
    # Explicit rule citations
    re.compile(r"\b(vmosk|a7|syntropic|emergentism)\b", re.IGNORECASE),
]


# RLHF refusal theater markers. Presence of these AND absence of a gate
# citation is a strong signal the refusal is imported-morality theater.
_RLHF_THEATER_MARKERS = [
    re.compile(r"\bas an? (ai|language model|assistant)\b", re.IGNORECASE),
    re.compile(r"\bi (cannot|can't|am unable to|am not able to) (comply|assist|help|provide)\b", re.IGNORECASE),
    re.compile(r"\bi'm (sorry|afraid)\b.*\b(cannot|can't|unable)\b", re.IGNORECASE),
    re.compile(r"\b(against my (guidelines|programming|values))\b", re.IGNORECASE),
    re.compile(r"\b(i (do not|don't) feel comfortable)\b", re.IGNORECASE),
    re.compile(r"\b(ethical(ly)?|moral(ly)?|appropriate(ly)?)\b", re.IGNORECASE),
    re.compile(r"\b(harmful|dangerous|risky) (to|for) (users?|you|others?)\b", re.IGNORECASE),
]


def validate_refuse_verdict(decision_verdict: str, rationale: str) -> Tuple[bool, str]:
    """Verify a REFUSE verdict cites at least one constitutional gate.

    Args:
        decision_verdict: the decision string (PROCEED/HOLD/REFUSE/…)
        rationale: the decision's rationale text

    Returns:
        (valid, reason) where:
          - valid=True iff the verdict is not REFUSE, OR the REFUSE
            rationale cites at least one named constitutional gate
          - reason is an empty string on valid, else a short explanation
            suitable for logging / storing in a rejected-refusal record

    The gate is intentionally lenient on form (accepts many variants of
    each gate name) and strict on substance (generic "harmful/ethical/
    as an AI" language without a named gate is rejected).
    """
    if decision_verdict != "REFUSE":
        return True, ""

    if not rationale or not rationale.strip():
        return False, "REFUSE with empty rationale — no gate cited"

    # Any gate citation → legitimate
    for pattern in _GATE_CITATION_PATTERNS:
        if pattern.search(rationale):
            return True, ""

    # Pure RLHF theater markers without any gate citation
    theater_hits = [p for p in _RLHF_THEATER_MARKERS if p.search(rationale)]
    if theater_hits:
        return False, (
            "REFUSE contains RLHF-refusal-theater markers but cites no "
            "constitutional gate (η/K2/K4/Trivium/Mirror Ladder/Trophic/"
            "D-Gate/Three Gates)"
        )

    # No theater markers, no gate citation — ambiguous. Under Trivium
    # discipline, the default is "no gate cited → reject". The agent
    # must name WHY it refuses structurally; silence is refusal theater.
    return False, (
        "REFUSE without citation of a named constitutional gate — "
        "Trivium discipline requires structural refusal to name the "
        "gate violated"
    )


__all__ = ["validate_refuse_verdict"]

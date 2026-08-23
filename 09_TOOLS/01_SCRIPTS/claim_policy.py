"""Lifecycle-aware barred-claim policy shared by corpus and public gates."""

from __future__ import annotations

import re
from typing import NamedTuple


class Rule(NamedTuple):
    name: str
    pattern: re.Pattern[str]


RULES = (
    Rule("total ontology inflation", re.compile(r"\b(?:is|provides|constitutes|gives us)\s+(?:a\s+)?(?:complete|total)\s+ontology\b", re.I)),
    Rule("total reality account inflation", re.compile(r"\b(?:complete|total)\s+(?:account|theory)\s+of\s+(?:all\s+)?reality\b", re.I)),
    Rule("universal paradox inflation", re.compile(r"\b(?:resolves?|solves?)\s+(?:all|every)\s+(?:fundamental\s+)?paradoxes?\b", re.I)),
    Rule("verified foundational algebra inflation", re.compile(r"\b(?:is|has\s+become)\s+(?:a\s+)?(?:verified|proved|complete)\s+foundational\s+algebra\b", re.I)),
    Rule("science unification inflation", re.compile(r"\b(?:unifies|has\s+unified)\s+(?:all|the)\s+sciences?\b", re.I)),
    Rule("Titan arithmetic", re.compile(r"(?:0_T|•)\s*(?:×|x|\*)\s*(?:∞_T|○)|(?:1_T|⊙)\s*=\s*(?:0_T|•)\s*(?:×|x|\*)\s*(?:∞_T|○)")),
    Rule("retired untyped node product", re.compile(r"(?<![A-Za-z0-9_])P\s*=\s*Φ\s*(?:×|x|\*)\s*V(?![A-Za-z0-9_])")),
    Rule("causal symbol reification", re.compile(r"\b(?:D5|Φ₅|Phi5|μ[0-4]|mu[0-4])\s+(?:causes?|commands?|decides?|acts?|pushes?)\b", re.I)),
    Rule("ethics from geometry", re.compile(r"\b(?:ethics?|morals?|justice)\s+(?:is|are|follows?|falls?)\s+(?:directly\s+)?(?:derived\s+)?from\s+(?:the\s+)?(?:geometry|arithmetic|equation)\b", re.I)),
    Rule("total war explanation", re.compile(r"\bwar\s+is\s+(?:always|only|ultimately)\s+(?:a\s+)?(?:war|battle|conflict)\s+between\s+(?:worldviews?|egregores?)\b", re.I)),
    Rule("human rank ontology", re.compile(r"\b(?:caste|varn?a|Rosetta\s+row|spiritual\s+class)\s+(?:determines?|establishes?|proves?|is)\s+(?:a\s+)?(?:human\s+)?(?:rank|worth|authority|entitlement)\b", re.I)),
    Rule("philosopher-king entitlement", re.compile(r"\bphilosopher[- ]kings?\s+(?:should|must|may|are\s+entitled\s+to)\s+(?:rule|govern|command)\b", re.I)),
    Rule("existential blackmail", re.compile(r"\b(?:Great\s+Filter|civilizational\s+survival).{0,100}\b(?:requires?|demands?|authorizes?)\s+(?:obedience|coercion|compulsion|sacrifice)\b", re.I | re.S)),
)

NEGATION = re.compile(
    r"(?:\bnot\b|\bnever\b|\bcannot\b|\bdoes\s+not\b|\bdo\s+not\b|"
    r"\bno\s+current\b|\bmay\s+not\b|\bmust\s+not\b|\bwithout\s+claiming\b)",
    re.I,
)
BOUNDARY_CONTEXT = re.compile(
    r"(?:\bheadline\s+framings?\b.{0,80}\boutran\b|\bforbidden\b|"
    r"\bretired\b|\boverclaim(?:ed|ing)?\b|\binflation\b)",
    re.I | re.S,
)


def _same_sentence_prefix(prefix: str) -> str:
    """Keep only the current sentence so earlier denials cannot waive later claims."""

    parts = re.split(r"(?<=[.!?])(?:[ \t\r]*\n+|[ \t]+)", prefix)
    return parts[-1] if parts else prefix


def violations(text: str) -> list[tuple[str, int, str]]:
    """Return positive barred assertions as ``(rule, line, snippet)`` tuples.

    A local negation in the same sentence immediately before the match makes a denial admissible. Prior-sentence negation does not waive a later positive claim.
    The policy deliberately uses narrow positive assertions rather than broad
    vocabulary bans; historical material is controlled by lifecycle routing.
    """

    found: list[tuple[str, int, str]] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            prefix = text[max(0, match.start() - 180):match.start()]
            if NEGATION.search(_same_sentence_prefix(prefix)) or BOUNDARY_CONTEXT.search(prefix):
                continue
            line = text.count("\n", 0, match.start()) + 1
            snippet = re.sub(r"\s+", " ", text[match.start():match.end()]).strip()
            found.append((rule.name, line, snippet))
    return found

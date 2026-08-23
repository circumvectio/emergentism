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
    Rule("unbounded philosophy majority", re.compile(r"\b(?:Emergentism|Finity|the\s+framework)\s+(?:resolves?|answers?|settles?)\s+most\s+(?:philosophical\s+)?(?:questions?|problems?|paradoxes?)\b", re.I)),
    Rule("objective morality proof inflation", re.compile(r"\b(?:Emergentism|Finity|the\s+framework|the\s+(?:geometry|equation|balance))\s+(?:proves?|establishes?|derives?)\s+(?:an?\s+)?objective\s+(?:morality|morals?|ethics?|teleology)\b", re.I)),
    Rule("Hume gap closure inflation", re.compile(r"\b(?:Emergentism|Finity|the\s+framework|RCAB-01)\s+(?:closes?|solves?|bridges?)\s+(?:Hume(?:'s)?\s+)?(?:the\s+)?is[–-]ought\s+gap\b", re.I)),
    Rule("value identity inflation", re.compile(r"\b(?:potential|balance|entropy|emergence|evolution)\s+(?:is|proves?|establishes?|defines?)\s+(?:the\s+)?Good\b", re.I)),
    Rule("co-agency authority inflation", re.compile(r"\bco[ -]?agency\s+(?:creates?|merges?|establishes?|implies?)\s+(?:shared\s+)?(?:personhood|consent|will|authority)\b", re.I)),
    Rule("guardian domination inflation", re.compile(r"\b(?:a\s+)?guardian\s+(?:owns?|rules?|overrides?|commands?|replaces?)\s+(?:the\s+)?bearer\b", re.I)),
    Rule("protection coercion authority", re.compile(r"\bprotection\s+authorizes?\s+coercion\b", re.I)),
    Rule("guardianship co-agency collapse", re.compile(r"\bguardianship\s+(?:is|equals?|=|≡)\s+co[ -]?agency\b", re.I)),
    Rule("AI guardian authority", re.compile(r"\b(?:an?\s+)?AI\s+guardian\s+(?:may|can|is\s+authorized\s+to)\s+(?:sign|authorize)\b", re.I)),
    Rule("construction validates worldview", re.compile(r"\b(?:benchmark\s+construction|publication|cross[ -]?(?:agent|model)\s+agreement|AI\s+agreement)\s+(?:validates?|proves?|confirms?)\s+(?:the\s+)?(?:worldview|Emergentism)\b", re.I)),
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

CLAUSE_BOUNDARY = re.compile(r"[.!?;\n]")


def _local_prefix(text: str, start: int) -> str:
    """Return only the unfinished clause immediately preceding a match.

    A denial in a previous sentence cannot launder a later affirmative claim.
    The 180-character cap remains a defense against pathological unpunctuated
    input while sentence, semicolon, and newline boundaries control scope.
    """

    prefix = text[max(0, start - 180):start]
    boundaries = list(CLAUSE_BOUNDARY.finditer(prefix))
    return prefix[boundaries[-1].end():] if boundaries else prefix


def violations(text: str) -> list[tuple[str, int, str]]:
    """Return positive barred assertions as ``(rule, line, snippet)`` tuples.

    A local negation immediately before the match makes a denial admissible.
    The policy deliberately uses narrow positive assertions rather than broad
    vocabulary bans; historical material is controlled by lifecycle routing.
    """

    found: list[tuple[str, int, str]] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            prefix = _local_prefix(text, match.start())
            if NEGATION.search(prefix) or BOUNDARY_CONTEXT.search(prefix):
                continue
            line = text.count("\n", 0, match.start()) + 1
            snippet = re.sub(r"\s+", " ", text[match.start():match.end()]).strip()
            found.append((rule.name, line, snippet))
    return found

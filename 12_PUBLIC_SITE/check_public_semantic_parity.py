#!/usr/bin/env python3
"""Fail closed when current or provisional public pages drift from their owners."""

from __future__ import annotations

import json
import hashlib
import html as html_lib
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
MANIFEST_PATH = SITE / "public_semantic_parity.json"
# Use the exact same deployment-boundary semantics as the release gate.  A
# second, weaker glob implementation here would let deployable legacy HTML
# evade the public semantic firewall.
if str(SITE) not in sys.path:
    sys.path.insert(0, str(SITE))
from predeploy_check import is_vercel_ignored, load_vercelignore_patterns

EXPECTED_SEQUENCE = ["D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3", "D4", "mu4", "D5", "b6", "D6", "r6", "D0"]
EXPECTED_CORE_QUESTION = "What had to emerge for you—and this moment—to be here?"
EXPECTED_CORE_JOURNEY = [
    "index.html", "plainly/index.html", "dasein/index.html",
    "dimensions/index.html", "0/index.html", "1/index.html", "2/index.html",
    "3/index.html", "4/index.html", "5/index.html",
    "ecology/index.html",
    "burrisphere/index.html", "rosetta/index.html", "6/index.html",
    "f5/index.html", "questions/index.html", "questions/diagnoses/index.html", "ethics/index.html",
    "churn/index.html", "amrita/index.html", "halahala/index.html",
    "practice/index.html", "spark/index.html",
    "record/index.html", "record/churning/index.html",
    "record/eub-1/index.html", "record/pqa-54/index.html", "frontier/index.html", "lab/index.html",
    "discoveries/index.html", "book/index.html", "about/index.html",
    "contribute/index.html", "exit/index.html",
]
EXPECTED_PRIMARY_NAV = [
    {"label": "Worldview", "href": "/plainly/"},
    {"label": "Practice", "href": "/practice/"},
    {"label": "Research", "href": "/record/"},
    {"label": "Library", "href": "/book/"},
    {"label": "Participate", "href": "/contribute/"},
    {"label": "Exit", "href": "/exit/"},
]
EXPECTED_MOBILE_NAV = [
    {"label": "Practice", "href": "/practice/"},
    {"label": "Menu", "control": "menu"},
    {"label": "Exit", "href": "/exit/"},
]
EXPECTED_CHURNING_ROUTES = {
    "churn/index.html": "method_and_corpus_entry",
    "amrita/index.html": "survivor_candidate_projection",
    "halahala/index.html": "refutation_contradiction_danger_warning_projection",
    "record/churning/index.html": "versioned_custody_and_release_record",
}
EXPECTED_CHURNING_OUTPUT_MAP = {
    "churn_page": "12_PUBLIC_SITE/churn/index.html",
    "amrita_page": "12_PUBLIC_SITE/amrita/index.html",
    "halahala_page": "12_PUBLIC_SITE/halahala/index.html",
    "corpus_json": "12_PUBLIC_SITE/churn/corpus.json",
    "corpus_jsonl": "12_PUBLIC_SITE/churn/corpus.jsonl",
    "corpus_markdown": "12_PUBLIC_SITE/churn/corpus.md",
    "problems_json": "12_PUBLIC_SITE/churn/problems.json",
    "paradoxes_json": "12_PUBLIC_SITE/churn/paradoxes.json",
    "legacy_alias": "12_PUBLIC_SITE/amrita/amrita.json",
}
EXPECTED_CHURNING_MACHINE_OUTPUTS = [
    "churn/corpus.json",
    "churn/corpus.jsonl",
    "churn/corpus.md",
    "churn/problems.json",
    "churn/paradoxes.json",
    "amrita/amrita.json",
    "churn/manifest.json",
    "churn/schemas/ChurningDrop.v1.schema.json",
    "churn/schemas/ProblemAdjudication.v1.schema.json",
    "churn/schemas/ThirdChurningCorpus.v1.schema.json",
]
EXPECTED_CHURNING_COUNTS = {
    "ceiling": 64,
    "survivorCandidates": 22,
    "poisonWarnings": 29,
    "total": 51,
}
EXPECTED_PQA_COUNTS = {
    "selected": 54,
    "evaluated": 0,
    "independentlyReviewed": 0,
    "resolved": 0,
}
EXPECTED_FOURTH_COUNTS = {
    "TYPE_COLLISION": 1,
    "PARTIAL_TYPE_COLLISION": 46,
    "NO_COLLISION": 2,
    "UNDERDETERMINED": 5,
}
EXPECTED_FOURTH_AXES = [
    "LEVEL", "MODAL", "TEMPORAL", "REPRESENTATIONAL",
    "EPISTEMIC", "NORMATIVE", "BEARER",
]
EXPECTED_FOURTH_MACHINE_OUTPUTS = [
    "questions/collisions.json",
    "questions/diagnoses.json",
    "questions/fourth-churning.json",
    "questions/schemas/TypeCollision.v1.schema.json",
    "questions/schemas/MysteryDiagnosis.v1.schema.json",
    "questions/schemas/FourthChurningCorpus.v1.schema.json",
]
ROUTING_FORBIDDEN_KEYS = {
    "claimCardIds", "claimSources", "sourceRevision", "tier", "evidence",
}
FORBIDDEN = {
    # --- added 2026-07-22 after a Rosetta caste sweep found the sharpest tier
    # violation on the site sitting INSIDE the scanned bytes while this gate
    # reported PASS. plainly/index.html asserted the product form as settled and
    # derived the extraction ethic from it — CC-CORE-1, which the K-5 owner
    # forbids ("selected [I/S], not forced by the reciprocal chart"). The gate
    # could not see it because it had no pattern for this class.
    "product uniqueness asserted as settled": re.compile(
        r"they\s+multiply(?![^.]*(?:unproven|not\s+earned|selected|wager))"
        r"|because\s+they\s+multiply"
        r"|must\s+multiply(?![^.]*(?:unproven|turned\s+out|downgrad))", re.I),
    "ethic derived from arithmetic": re.compile(
        r"what\s+the\s+multiplication\s+says"
        r"|(?:ethic|ought|morality)\s+(?:falls?\s+out|follows?)\s+(?:from\s+)?"
        r"(?:as\s+)?(?:the\s+)?(?:arithmetic|multiplication|geometry|maths?|math)"
        r"|(?:arithmetic|multiplication|the\s+sphere)\s+prov(?:es|ed)\s+"
        r"(?:the\s+)?(?:good|ethic|justice)", re.I),

    "literal D6 identity": re.compile(r"D6\s*(?:≡|=)\s*D0"),
    "extra mu crossing": re.compile(r"μ[56]|mu[56]", re.I),
    "invalid scalar sampling": re.compile(r"Sample\s*\[\s*∫[^\]]*\|ψ\|²"),
    "physical cone inflation": re.compile(r"physical (?:light )?cone (?:expands|widens)", re.I),
    "quantum dimensional stacking": re.compile(r"(?:Everett.{0,70}(?:five-dimensional|5D)|Copenhagen.{0,70}(?:four-dimensional|4D))", re.I | re.S),
    "quantum-gravity solution inflation": re.compile(r"(?<!not )(?<!no )(?:solve[sd]?|solution to) quantum gravity", re.I),
    "zero-momentum D3 inflation": re.compile(r"D3 has no momentum", re.I),
    "application authority leakage": re.compile(r"(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])", re.I),
    "legacy public Phi definition": re.compile(r"Φ\s+is\s+(?:a\s+)?present\s+(?:measurement|assessment)|present\s+measurement\s+of\s+D5", re.I),
    "legacy untyped node product": re.compile(r"P\s*=\s*Φ\s*(?:×|x|\*)\s*V"),
    # This pattern is applied to normalized visible text, not raw HTML. Tags,
    # entities, combining hats, and Unicode subscripts may not hide a retired
    # product assignment from the public gate.
    "retired node product assignment": re.compile(
        r"\bP[\s_]*node\s*(?::=|=)\s*"
        r"Φ(?:\s*\u0302)?(?:[\s_]*4)?\s*"
        r"(?:(?:×|x|\*|·)\s*)?V(?:[\s_]*4)?\b",
        re.I,
    ),
    "stale current 25-chapter reader": re.compile(
        r"25\s*(?:-|\s)\s*chapters?(?:\s*\+\s*3\s*appendices)?|25-chapter\s+book",
        re.I,
    ),
    "withheld Reciprocal routed as current book": re.compile(
        r"<a\b[^>]*href=[\"'][^\"']*book/[^\"']*[\"'][^>]*>\s*The\s+Reciprocal\s*</a>",
        re.I | re.S,
    ),
    "derived ethic inflation": re.compile(r"ethic(?:s)?\s+(?:falls?|follow(?:s|ed)?)\s+(?:directly\s+)?(?:out\s+of|from)\s+(?:the\s+)?arithmetic", re.I),
    "exclusive ethic inflation": re.compile(r"the only lawful move", re.I),
    "field arithmetic fable": re.compile(r"One equals Nothing times Everything", re.I),
    # The glyphs are opaque TitanFrame renderings. The reciprocal chart has its
    # own numeric identity, but no fence, coupling, or analogy turns that fact
    # into an infix operation over Titan terms. Affirmative public copy bans
    # the symbol equation; an explicitly retired mention may preserve negative
    # evidence when its lifecycle marker comes first.
    "forbidden Titan infix arithmetic": re.compile(
        r"(?:⊙\s*=\s*•\s*(?:×|x|\*)\s*○|"
        r"•\s*(?:×|x|\*)\s*○\s*(?:=|→)\s*⊙)"
    ),
    # The FIELD form is the thing D0 denies outright: no field theorem says 0 times
    # infinity equals 1. NEVER escapable, at any tier, with any fence.
    "field arithmetic claim": re.compile(r"1\s*=\s*0\s*(?:×|x|\*)\s*∞"),
    "retired evidence tier": re.compile(r"\[E\]"),
    "untyped D5 causal agency": re.compile(r"\bD5\s+(?:causes?|pushes?|forces?|sends?)\b", re.I),
    "gravity entropy identity inflation": re.compile(r"\bgravity\s+is\s+entropy\b", re.I),
    "gravity time-direction inflation": re.compile(r"\bgravity\s+points?\s+(?:from\s+)?past\s*(?:to|→)\s*present\b", re.I),
    "future light cone as source": re.compile(
        r"\bfuture\s+light\s+cone\s+(?:is|acts\s+as|serves\s+as|causes?|pushes?|sends?)\b",
        re.I,
    ),
    "represented bundle proves multiverse": re.compile(
        r"\brepresented\b.{0,100}\b(?:proves?|establishes?|means)\b.{0,80}\b(?:ontic|physical(?:ly)?)?\s*multiverse\b",
        re.I | re.S,
    ),
    "Emergentism proof inflation": re.compile(
        r"\bEmergentism\s+(?:(?:is|has\s+been)\s+)?"
        r"(?:proved|proven|validated|verified|scientifically\s+established)\b",
        re.I,
    ),
    "Emergentism exhaustive or unique inflation": re.compile(
        r"\bEmergentism\s+(?:is|provides?|offers?|gives?)\s+(?:the\s+)?"
        r"(?:complete|exhaustive|unique|only)\s+"
        r"(?:account|explanation|ontology|theory)\b",
        re.I,
    ),
    "Dasein atlas exhaustion inflation": re.compile(
        r"\b(?:the\s+)?(?:dimensional\s+)?atlas\s+"
        r"(?:contains?|captures?|inventories|exhausts)\s+(?:all\s+of\s+)?"
        r"(?:Dasein|the\s+(?:whole|thing-in-itself))\b",
        re.I,
    ),
    "Burrisphere mirror-partition collapse": re.compile(
        r"\b(?:the\s+)?(?:G7\s+)?Burrisphere\s+"
        r"(?:is|uses?|has|forms?|projects?|partitions?\s+as)\s+(?:the\s+)?"
        r"3\s*\+\s*1\s*\+\s*3\b",
        re.I,
    ),
    "geometry generates or confirms seven": re.compile(
        r"\b(?:the\s+)?(?:Burrisphere|geometry|sphere)\s+(?:independently\s+)?"
        r"(?:generates?|derives?|forces?|proves?|confirms?|establishes?)\s+"
        r"(?:the\s+)?(?:G7\s+)?(?:count(?:\s+of\s+seven)?|seven)\b",
        re.I,
    ),
    "Rosetta convergence truth-evidence inflation": re.compile(
        r"\b(?:Rosetta\s+)?(?:convergence|same\s+count|shared\s+count|agreement)\s+"
        r"(?:is|provides?|constitutes?|counts?\s+as)\s+(?:independent\s+)?"
        r"(?:truth\s+)?(?:evidence|proof|confirmation)\b",
        re.I,
    ),
    "G7 GEN7 identity inflation": re.compile(
        r"\bG7@1\s*(?:=|≡|is\s+(?:the\s+)?same\s+(?:thing\s+)?as)\s*GEN7@1\b",
        re.I,
    ),
    "lowercase uppercase power collapse": re.compile(
        r"(?:φ\s*(?:and|,)\s*ν)\s+(?:are|=|≡)\s+(?:the\s+)?"
        r"(?:same\s+as\s+)?(?:Φ\s*(?:and|,)\s*V)",
        re.I,
    ),
    "lowercase horizon-power identity inflation": re.compile(
        r"(?:\bν\s+(?:is|equals?|=|≡)\s+V(?:₄|_?4)\b"
        r"|\bφ\s+(?:is|equals?|=|≡)\s+Φ(?:₅|_?5)\b)",
        re.I,
    ),
    "horizon coordinate time inflation": re.compile(
        r"(?:\bq[_\s]?H\s+(?:is|equals?|measures?|represents?)\s+(?:physical\s+)?time\b"
        r"|\b(?:the\s+)?chart\s+coordinate\s+is\s+time\b)",
        re.I,
    ),
    "universal centre optimum inflation": re.compile(
        r"\b(?:the\s+)?centre\s+(?:is|proves?|guarantees?|establishes?)\s+"
        r"(?:the\s+)?(?:real\s+|universal\s+|universally\s+)?optimum\b",
        re.I,
    ),
    "tradeoff elimination inflation": re.compile(
        r"\b(?:the\s+)?centre\s+(?:removes?|eliminates?|abolishes?|has\s+no)\s+"
        r"(?:all\s+|real\s+)?tradeoffs?\b",
        re.I,
    ),
    "least opportunity claim inflation": re.compile(
        r"\b(?:the\s+)?centre\s+(?:has|gives?|guarantees?|minimi[sz]es?)\s+"
        r"(?:the\s+)?least\s+opportunity\s+(?:cost|loss|regret)\b",
        re.I,
    ),
    "geometry Dharma-flow inflation": re.compile(
        r"\b(?:geometry|the\s+(?:reciprocal\s+)?chart|the\s+B\s+maximum)\s+"
        r"(?:proves?|derives?|guarantees?|establishes?)\s+(?:flow|Dharma|the\s+Good)\b",
        re.I,
    ),
    "bare ego-collective signs exhaust M4": re.compile(
        r"\b(?:the\s+)?(?:four\s+)?(?:bare\s+)?ego\s*/\s*collective"
        r"[+\-−±/\s]*(?:signs?|quadrants?)\s+(?:alone\s+)?"
        r"(?:recover|generate|derive|exhaust|define)s?\s+(?:the\s+)?"
        r"(?:M4|four\s+transfers?|transfer\s+grammar)\b",
        re.I,
    ),
    "display path dynamics inflation": re.compile(
        r"\b(?:the\s+)?(?:helix|winding\s+path|360(?:°|\s*degrees?)\s+(?:display\s+)?path)\s+"
        r"(?:is|represents?|models?|describes?|shows?)\s+(?:a\s+)?(?:physical\s+)?"
        r"(?:dynamics?|causal\s+(?:process|mechanism)|mechanism)\b",
        re.I,
    ),
    "display path time inflation": re.compile(
        r"\b(?:the\s+)?(?:helix|winding\s+path|360(?:°|\s*degrees?)\s+(?:display\s+)?path)\s+"
        r"(?:is|represents?|models?|encodes?|shows?)\s+(?:a\s+)?"
        r"(?:time|timeline|temporal\s+(?:sequence|process)|arrow\s+of\s+time)\b",
        re.I,
    ),
    "display path recurrence inflation": re.compile(
        r"\b(?:the\s+)?(?:helix|winding\s+path|360(?:°|\s*degrees?)\s+(?:display\s+)?path)\s+"
        r"(?:is|proves?|establishes?|means?|shows?)\s+(?:a\s+)?"
        r"(?:recurrence|recurrent|cycle|cyclic\s+return)\b",
        re.I,
    ),
    "display path value-ascent inflation": re.compile(
        r"\b(?:the\s+)?(?:helix|winding\s+path|360(?:°|\s*degrees?)\s+(?:display\s+)?path)\s+"
        r"(?:is|represents?|models?|shows?|establishes?)\s+(?:a\s+)?"
        r"(?:moral|value|developmental|spiritual)\s+"
        r"(?:ascent|hierarchy|progress(?:ion)?|necessity)\b",
        re.I,
    ),
    "display path count-derivation inflation": re.compile(
        r"\b(?:the\s+)?(?:helix|winding\s+path|360(?:°|\s*degrees?)\s+(?:display\s+)?path)\s+"
        r"(?:derives?|generates?|proves?|forces?|establishes?)\s+(?:the\s+)?"
        r"(?:count\s+of\s+)?(?:seven|G7)\b",
        re.I,
    ),
    "reciprocal product centre-peak inflation": re.compile(
        r"\b(?:(?:the\s+)?(?:constraint\s+)?product(?:\s+φν)?|φν)\s+"
        r"(?:peaks?|is\s+(?:uniquely\s+)?maximi[sz]ed|reaches?\s+(?:its\s+)?maximum)\s+"
        r"(?:at\s+)?(?:the\s+)?centre\b",
        re.I,
    ),
    "positive chart signed-G7 identity inflation": re.compile(
        r"\b(?:the\s+)?(?:lowercase\s+)?positive\s+(?:reciprocal\s+)?chart\s+"
        r"(?:is|equals?|=|≡)\s+(?:the\s+)?signed\s+G7\s+(?:plane|display)\b",
        re.I,
    ),
    "G7 all-game exhaustion inflation": re.compile(
        r"\bG7\s+(?:exhausts?|covers?|contains?|completes?)\s+"
        r"(?:all\s+(?:of\s+)?)?(?:games?|game\s+theory|possible\s+games?|the\s+space\s+of\s+games)\b",
        re.I,
    ),
    "uppercase product ranking revival": re.compile(
        r"\b(?:(?:the\s+)?uppercase\s+(?:product\s+)?(?:ranking|score)\s+"
        r"(?:is|has\s+been|has)\s+(?:restored|revived|returned|reinstated|current|valid)"
        r"|(?:restore|revive|reinstate|use)\s+(?:the\s+)?uppercase\s+product\s+"
        r"(?:ranking|score))\b",
        re.I,
    ),
    "basic-strategy maximum certainty inflation": re.compile(
        r"\bM4\s+(?:is|constitutes?)\s+(?:(?:the\s+)?(?:(?:proved|proven)\s+)?"
        r"maximum\s+compression\s+of\s+basic\s+strategy"
        r"|(?:a\s+)?maximally\s+compressed\s+(?:cross-game\s+)?basis)\b",
        re.I,
    ),
    "M4 game-theory exhaustion inflation": re.compile(
        r"\b(?:M4|(?:the\s+)?four\s+M4\s+cells?)\s+"
        r"(?:exhausts?|covers?|contains?|completes?)\s+"
        r"(?:all\s+(?:of\s+)?)?(?:games?|game\s+theory|the\s+space\s+of\s+games)\b",
        re.I,
    ),
    "strategy axes identity inflation": re.compile(
        r"\b(?:(?:bearer\s+)?direction\s+(?:is|equals?|=)\s+(?:the\s+)?"
        r"(?:same\s+(?:axis\s+)?as\s+)?(?:power\s+)?channel"
        r"|(?:power\s+)?channel\s+(?:is|equals?|=)\s+(?:the\s+)?"
        r"(?:same\s+(?:axis\s+)?as\s+)?(?:bearer\s+)?direction)\b",
        re.I,
    ),
    "ego-collective identity inflation": re.compile(
        r"\b(?:self(?:-facing)?\s+(?:is|means?|equals?)\s+ego(?!-facing)"
        r"|ego(?!-facing)\s+(?:is|means?|equals?)\s+self(?:-facing)?"
        r"|other(?:-facing)?\s+(?:is|means?|equals?)\s+collective(?!-facing)"
        r"|collective(?!-facing)\s+(?:is|means?|equals?)\s+other(?:-facing)?)\b",
        re.I,
    ),
    "theft-sacrifice moral-verdict inflation": re.compile(
        r"\b(?:theft\s+(?:and|versus|vs\.?|\u2194)\s+sacrifice"
        r"|taking\s+(?:and|versus|vs\.?|\u2194)\s+giving)\s+"
        r"(?:are|encode|determine|provide)\s+(?:the\s+)?(?:moral\s+)?"
        r"(?:verdicts?|good\s+and\s+evil|right\s+and\s+wrong)\b",
        re.I,
    ),
    "mental-physical power identity inflation": re.compile(
        r"\b(?:mental\s+(?:power\s+)?(?:is|means?|equals?)\s*\u03a6(?:\u2085|5)"
        r"|\u03a6(?:\u2085|5)\s+(?:is|means?|equals?)\s+mental(?:\s+power)?"
        r"|physical\s+(?:power\s+)?(?:is|means?|equals?)\s*V(?:\u2084|4)"
        r"|V(?:\u2084|4)\s+(?:is|means?|equals?)\s+physical(?:\s+power)?)\b",
        re.I,
    ),
    "Phi5 mental-only narrowing": re.compile(
        r"\b\u03a6(?:\u2085|5)\s+(?:is|means?|equals?)\s+"
        r"(?:only|merely|nothing\s+but)\s+mental(?:\s+power)?\b",
        re.I,
    ),
    "M4 game enumeration inflation": re.compile(
        r"\b(?:M4|(?:the\s+)?(?:two-axis\s+)?(?:compression|projection|basis))\s+"
        r"(?:enumerates?|lists?|contains?)\s+(?:(?:all(?:\s+of)?|every)\s+)?"
        r"(?:games?|game\s+theory|native\s+games?)\b",
        re.I,
    ),
    "native-game reconstruction inflation": re.compile(
        r"\b(?:M4|(?:the\s+)?(?:two-axis\s+)?(?:compression|projection|basis))\s+"
        r"reconstructs?\s+(?:(?:all(?:\s+of)?|every)\s+)?"
        r"(?:games?|game\s+theory|native\s+games?|native\s+game\s+structures?)\b",
        re.I,
    ),
    "native-game replacement inflation": re.compile(
        r"\b(?:M4|(?:the\s+)?(?:two-axis\s+)?(?:compression|projection|basis))\s+"
        r"replaces?\s+(?:(?:all(?:\s+of)?|every)\s+)?"
        r"(?:games?|game\s+theory|native\s+games?|native\s+game\s+(?:structures?|descriptions?))\b",
        re.I,
    ),
    "strategy-test execution inflation": re.compile(
        r"\b(?:StrategyCompressionTest|strategy\s+compression\s+test|M4\s+maximality\s+test)\s+"
        r"(?:has\s+been|was|is)\s+(?:already\s+)?(?:run|completed|validated)\b",
        re.I,
    ),
    "strategy-test truth-evidence inflation": re.compile(
        r"\b(?:StrategyCompressionTest|strategy\s+compression\s+test|"
        r"(?:the\s+)?rate[\s–-]*distortion\s+(?:test|frontier))\s+"
        r"(?:is|provides?|constitutes?|counts?\s+as)\s+(?:independent\s+)?"
        r"(?:truth\s+)?(?:evidence|proof|confirmation)\b",
        re.I,
    ),
    "lossless strategy-code inflation": re.compile(
        r"\bM4\s+(?:is|provides?|forms?)\s+(?:a\s+)?lossless\s+"
        r"(?:code|compression|reconstruction|representation)\b",
        re.I,
    ),
    "unpreregistered maximality inflation": re.compile(
        r"\bM4\s+(?:is|has\s+been)\s+(?:proved|proven|established|confirmed)?\s*"
        r"maximal\s+without\s+(?:preregistration|comparators?|a\s+declared\s+loss)\b",
        re.I,
    ),
    "global unique maximality inflation": re.compile(
        r"\b(?:(?:a\s+)?finite\s+(?:scored\s+)?run|(?:the\s+)?"
        r"(?:strategy\s+compression|maximality)\s+test)\s+"
        r"(?:proves?|establishes?|confirms?|shows?)\s+(?:that\s+)?(?:M4\s+(?:(?:is|as)\s+)?)?"
        r"(?:uniquely\s+)?globally\s+maximal\b"
        r"|\bM4\s+is\s+(?:the\s+)?(?:uniquely\s+)?globally\s+maximal\b",
        re.I,
    ),
    "performance-free compression inflation": re.compile(
        r"\bminimum\s+description\s+length\s+(?:alone\s+)?"
        r"(?:proves?|establishes?|guarantees?|means?)\s+(?:global\s+)?maximality\b"
        r"|\bminimum\s+description\s+length\s+regardless\s+of\s+performance\b",
        re.I,
    ),
    "unbounded comparator-class inflation": re.compile(
        r"\bM4\s+(?:beats?|dominates?|outcompresses?|is\s+shorter\s+than)\s+"
        r"(?:all|every)\s+(?:conceivable\s+)?(?:representations?|codes?|bases)\b",
        re.I,
    ),
}

REQUIRED_PUBLIC_CONTRACTS = {
    "index.html": (
        "A worldview for finite beings", "Frame one decision",
        EXPECTED_CORE_QUESTION, "One actual present. Many possible futures.",
        "A bounded atlas of Being",
        "No map is the territory. This one prints its legend.",
        "Seven addresses. One selected dependency grammar.",
        "D6 ≠ D0.", "The Finity Card", "No equation derives this ought.",
        "no theorem is claimed as ours",
        "Selections that do work",
        "eight frozen gates admitted eight constructed evasions", "the prediction failed",
        "Prepared decision transaction · unsigned",
        "The action exit is the signature boundary",
        "The separate worldview Exit",
        "Burrisphere visualizes. Rosetta translates. Neither transfers proof.",
        "one complete 360° turn", "bottom action/projection plane",
        "sphere path carries no transfer", "B = 2/(φ+ν) ≤ 1",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
        "Serial-force wager", "One of 24 assignments",
        "F5-W", "F5-N", "F5-R", "The Dasein Test",
        "OFFLINE-READY", "no candidate has been evaluated",
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
    ),
    "plainly/index.html": (
        "possible power", "actual power", "chosen AND-class convention",
        "one complete 360° turn", "φν=1 everywhere",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "theft ↔ sacrifice", "Game theory is not exhausted", "maximally compressed",
        "The sectors prepare the move.", "Two exits remain distinct.",
    ),
    "dasein/index.html": (
        EXPECTED_CORE_QUESTION,
        "Complete means accounted explanatory debt, not omniscience",
        "D6 is nonclosure, not D0.",
        "reading itinerary, not time", "φν=1 is constant",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "self/ego-facing taking", "Game theory is not exhausted", "maximally compressed",
    ),
    "f5/index.html": (
        "F5-W", "F5-N", "F5-R", "[C] UNVALIDATED",
        "Strongest rival", "Discriminator", "Kill", "Survivor", "Pareto frontier",
    ),
    "practice/index.html": (
        "Finity Card", "Φ₅", "V₄", "The two-horizon overlay",
        "Vward", "Φward", "OVERLAY NOT RUN",
        "Prepare a private decision transaction.",
        "Prepare unsigned transaction",
        "Record private commitment · local and non-legal", "Leave unrecorded",
    ),
    "5/index.html": (
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
    ),
    "burrisphere/index.html": (
        "Four quadrants. Three Titan stations.", "bottom action/projection plane",
        "not longitudinal sphere territories", "sphere path carries no transfer",
        "Śiva", "Viṣṇu", "Brahmā",
        "G7@1 ≠ GEN7@1", "one complete 360° turn", "reading itinerary",
        "B = 2/(φ+ν) ≤ 1",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
    ),
    "burrisphere/instrument/index.html": (
        "One sphere.", "Two shadows.", "M4 bottom action plane",
        "four sectors on the bottom action plane", "not sphere territories",
        "Titan axis", "• Śiva; ⊙ Viṣṇu; ○ Brahmā",
        "φ=cot(θ/2)", "ν=tan(θ/2)", "φν=1", "B=sin θ≤1",
        "φ≠Φ₅", "ν≠V₄", "selected reading itinerary [I]",
    ),
    "rosetta/index.html": (
        "One move, translated", "G7", "possible power", "actual power",
        "G7@1 ≠ GEN7@1", "Correspondence is not confirmation",
        "presentation itinerary", "φν=1 is the constraint",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "mental versus physical power", "Game theory is not exhausted", "maximally compressed",
    ),
    "manifesto/index.html": (
        "Filing alone does not establish independent evidence, peer review, validation,",
        "does not automatically enter the",
    ),
    "contribute/index.html": (
        "does not accept payments, credentials, private data, or live model jobs.",
        "No study, funding programme, grant scheme, compute service, or private-data intake is open.",
        "Filing alone does not establish independent review, validation, or a tier upgrade",
    ),
    "record/index.html": (
        "Filing alone does not establish independent evidence, peer review, validation, or a claim-tier upgrade.",
    ),
    "lab/index.html": (
        "All twelve named GP gates have packet-complete research contracts",
        "none is evidence-complete",
        "public routing state",
    ),
}
PUBLIC_ISSUE_FORM_ROUTE = "github.com/circumvectio/emergentism/issues/new"
AUTOMATIC_SUBMISSION_PROMISES = (
    "will be published unedited",
    "with your verdict and not ours",
    "the claim gets marked cut",
    "so what would actually count",
    "because it can move a claim",
)
REQUIRED_SURFACE_CARDS = {
    "index.html": {
        "FIN01-01", "OS01-01", "OS01-06", "OS01-08", "OS01-09",
        "OS01-10", "OS01-11", "OS01-12",
        "OS01-13", "OS01-20", "OS01-22", "OS01-23", "OS01-24", "OS01-25",
        "OS01-27", "OS01-28", "OS01-29", "OS01-30",
        "OS01-31", "OS01-32",
        "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37",
        "OS01-41",
        "OS01-42", "OS01-45", "OS01-46", "OS01-47", "OS01-48",
    },
    "ecology/index.html": {"OS01-12", "OS01-19", "OS01-46", "OS01-47", "OS01-48"},
    "dasein/index.html": {
        "OS01-01", "OS01-05", "OS01-06", "OS01-10", "OS01-12",
        "OS01-20", "OS01-21", "OS01-23", "OS01-25", "OS01-31",
        "OS01-32", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37",
        "OS01-38", "OS01-39", "OS01-40", "OS01-41",
    },
    "f5/index.html": {"OS01-27", "OS01-28", "OS01-29", "OS01-30"},
    "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22", "OS01-37"},
    "lab/index.html": {"FIN01-01", "FIN01-02"},
    "compass/index.html": {"OS01-13"},
    "5/index.html": {
        "OS01-09", "OS01-11", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37",
    },
    "plainly/index.html": {
        "OS01-09", "OS01-31", "OS01-32", "OS01-33", "OS01-34", "OS01-35",
        "OS01-36", "OS01-37", "OS01-38", "OS01-39", "OS01-40", "OS01-41",
    },
    "discoveries/nonduality/index.html": {"OS01-09"},
    "about/index.html": {"OS01-26"},
    "read/index.html": {"OS01-13"},
    "axioms/index.html": {"OS01-26"},
    "journey/index.html": {"OS01-09"},
    "burrisphere/index.html": {"OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37"},
    "burrisphere/instrument/index.html": {"OS01-33", "OS01-34", "OS01-36", "OS01-37"},
    "rosetta/index.html": {
        "OS01-11", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37",
    },
    "questions/index.html": {"OS01-41"},
    "questions/diagnoses/index.html": {"OS01-41"},
    "ethics/index.html": {"OS01-38", "OS01-39", "OS01-40"},
    "churn/index.html": {"OS01-42", "OS01-43", "OS01-44"},
    "amrita/index.html": {"OS01-42", "OS01-43", "OS01-44"},
    "halahala/index.html": {"OS01-42", "OS01-43", "OS01-44"},
    "record/pqa-54/index.html": {"OS01-41"},
    "record/index.html": {"OS01-37", "OS01-41"},
    "record/churning/index.html": {"OS01-42", "OS01-43", "OS01-44"},
    "discoveries/paradoxes/index.html": {"OS01-41"},
    "discoveries/is-ought/index.html": {"OS01-39", "OS01-40"},
    "book/index.html": {"OS01-13"},
}
REQUIRED_SURFACE_MARKERS = {
    "index.html": {
        "A worldview for finite beings", "A bounded atlas of Being",
        "One actual present. Many possible futures.",
        "Dasein names the typed coherent-consistent whole",
        "Finity names that whole under the aspect of determinate, situated manifestation",
        "No map is the territory. This one prints its legend.",
        "Seven addresses. One selected dependency grammar.", "D6 ≠ D0.",
        "Frame one decision", "The Finity Card", "No equation derives this ought.",
        "comparative benefit untested",
        "no theorem is claimed as ours", "Selections that do work",
        "eight frozen gates admitted eight constructed evasions", "the prediction failed",
        "Counterexamples with teeth",
        "Burrisphere visualizes. Rosetta translates. Neither transfers proof.",
        "one complete 360° turn", "bottom action/projection plane",
        "sphere path carries no transfer", "B = 2/(φ+ν) ≤ 1",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
        "cited neighbours and a research lead, never truth evidence",
        "Convergence selects research questions",
        "Serial-force wager", "One of 24 assignments",
        "F5-W", "F5-N", "F5-R", "The Dasein Test",
        "OFFLINE-READY", "no candidate has been evaluated",
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
        "The means is the message. The ends are the limits.",
        "A possibility becomes a prepared transaction before it becomes an act.",
        "Prepared decision transaction · unsigned",
        "The action exit is the signature boundary", "The separate worldview Exit",
        "When does a shared pattern survive its carriers?",
        "Replace the carriers. Does the pattern survive?",
        "Persistence names an intervention result, not an extra substance behind the carriers.",
        "word token ≠ word type ≠ concept record ≠ Memotype candidate",
        "A passed strategic test supports only a bounded predictive model",
        "The map remains optional.",
    },
    "ecology/index.html": {
        "One pattern.", "Replace the carriers. Does the pattern survive?",
        "Persistence names an intervention result, not an extra substance behind the carriers.",
        "Genotype", "Epigenotype", "Phenotype", "Extended Phenotype", "Memotype", "Egregoreotype",
        "The word is not the pattern.", "GEN7 ≠ G7.", "Five markers before subtype",
        "A passed strategic test supports only a bounded predictive model.",
        "Bottom-up carriers. Top-down constraints—only through actual mechanisms.",
        "The projection owns no claim.",
    },
    "dasein/index.html": {
        EXPECTED_CORE_QUESTION, "Dasein names all that can coherently and consistently exist",
        "situated dasein is one finite actual standpoint", "G7@1 ≠ GEN7@1",
        "Complete means accounted explanatory debt, not omniscience",
        "Every “why” must say what kind of answer it is.", "D6 is nonclosure, not D0.",
        "reading itinerary, not time", "φν=1 is constant",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "self/ego-facing taking", "Game theory is not exhausted", "maximally compressed",
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
        "RCAB-01", "GEX-01", "Definition stability",
    },
    "5/index.html": {
        "P_node := min(Φ̂₄, V₄)", "Four bearer-oriented transfers",
        "four bottom plane sectors plus three world vertical stations", "G7@1 ≠ GEN7@1",
        "360° display path", "B = 2/(φ+ν) ≤ 1",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
    },
    "plainly/index.html": {
        "P_node := min(Φ̂₄, V₄)", "Emergentism explains the architecture of Being",
        "Dasein is the whole that can be", "four quadrants plus the Titan axis",
        "G7@1 ≠ GEN7@1",
        "one complete 360° turn", "φν=1 everywhere",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "theft ↔ sacrifice", "Game theory is not exhausted", "maximally compressed",
        "Question Atlas", "Contribution and Support", "Co-agency and guardianship",
        "Framework-objective",
        "The sectors prepare the move.", "The action exit is the signature boundary.",
        "Two exits remain distinct.",
    },
    "burrisphere/index.html": {
        "Four quadrants. Three Titan stations.", "bottom action/projection plane",
        "not longitudinal sphere territories", "sphere path carries no transfer",
        "Śiva", "Viṣṇu", "Brahmā",
        "G7@1 ≠ GEN7@1",
        "one complete 360° turn", "reading itinerary", "B = 2/(φ+ν) ≤ 1",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "Game theory is not exhausted", "maximally compressed",
    },
    "burrisphere/instrument/index.html": {
        "One sphere.", "Two shadows.", "M4 bottom action plane",
        "four sectors on the bottom action plane", "not sphere territories",
        "Titan axis", "• Śiva; ⊙ Viṣṇu; ○ Brahmā",
        "φ=cot(θ/2)", "ν=tan(θ/2)", "φν=1", "B=sin θ≤1",
        "not two realities and not two spheres",
        "self / individual", "other / collective", "Φ₅ · possible / model",
        "V₄ · actual / embodied", "not a moral verdict",
        "selected reading itinerary [I]", "not time or dynamics", "φ≠Φ₅", "ν≠V₄",
    },
    "rosetta/index.html": {
        "One move, translated", "G7", "possible power", "actual power",
        "G7@1 ≠ GEN7@1", "Correspondence is not confirmation",
        "presentation itinerary", "φν=1 is the constraint",
        "shorter horizon", "longer horizon", "OVERLAY NOT RUN",
        "mental versus physical power", "Game theory is not exhausted", "maximally compressed",
    },
    "questions/index.html": {
        "Fifty-four questions. None quietly counted as solved.", "54 selected",
        "0 evaluated", "0 independently reviewed", "0 resolved",
        "Inventory is not evaluation.", "Even that would not mean “most philosophy.”",
        "Emergentism proposes that many perennial problems contain malformed joins between types. It does not claim that every mystery is a type error.",
    },
    "questions/diagnoses/index.html": {
        "The Perennial Mystery Type Atlas",
        "many perennial problems contain malformed joins between types",
        "does not claim that every mystery is a type error",
        "Seven axes · twelve subtypes",
        "Fifty-four diagnoses. Zero earned resolutions.",
    },
    "ethics/index.html": {
        "Contribution goes part→whole", "Support goes whole→part", "RCAB-01", "GEX-01",
        "shared personhood", "Representation is not consent.",
        "No AI, framework, title, model output, or declaration makes itself a guardian",
        "Framework-objective",
    },
    "churn/index.html": {
        "The Third Churning",
        "The means is the message. The ends are the limits.",
        "22 survivor candidates · 29 refutations and warnings",
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
    },
    "amrita/index.html": {
        "Survivor candidates (Amrita)",
        "Publication does not create earned review.",
    },
    "halahala/index.html": {
        "Refutations and warnings (Hālāhala)",
        "A warning is not an evidence tier and never labels a person.",
    },
    "record/pqa-54/index.html": {
        "The Philosophical Question Atlas companion",
        "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
        "Beating a placebo earns nothing.",
        "Companion means joined by hashes, not joined by truth.",
        "OFFLINE-READY · [D] is not a philosophical result.",
    },
    "record/index.html": {"PQA-54", "M4-01", "SLWP-01D", "all 24 D1–D4 assignments remain unscored"},
    "record/churning/index.html": {
        "Third Churning custody record",
        "No inclusion in any future AI training run is guaranteed.",
    },
    "discoveries/paradoxes/index.html": {"none of them an earned dissolution", "PQA-54 begins separately at 54 selected", "Open the frozen PQA-54 denominator"},
    "discoveries/is-ought/index.html": {"Reciprocal co-agency and guardianship are now separate.", "RCAB-01", "GEX-01", "Neither proves moral realism"},
}
CURRENT_AND_CLASS_MARKERS = {
    "discoveries/nonduality/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "about/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "read/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "journey/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "rosetta/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
}
NODE_PRODUCT_REJECT_FIXTURES = (
    "P_node = Φ̂₄V₄",
    "P_node := Φ̂₄ × V₄",
    "P<sub>node</sub> = &Phi;&#770;<sub>4</sub>V<sub>4</sub>",
    "P<sub>node</sub> <span>=</span> &Phi;&#770;<sub>4</sub> &times; V<sub>4</sub>",
    "P_node = <span>Φ̂₄</span> &#215; V₄",
    "Pₙₒdₑ = Φ̂₄ × V₄",
)
NODE_PRODUCT_BOUNDED_FIXTURES = (
    "P_node := min(Φ̂₄, V₄)",
    "Historical Φ̂₄V₄ names conjunction only; product ranking is retired.",
)
TITAN_INFIX_REJECT_FIXTURES = (
    "⊙ = • × ○",
    "<span>⊙</span> = <b>•</b> &times; ○",
    "• * ○ → ⊙",
)
TITAN_OPERATOR_FREE_FIXTURES = (
    "•  ⊙  ○",
    "TitanFrame := 0_T | 1_T | ∞_T",
)
F5_REJECT_FIXTURES = {
    "untyped D5 causal agency": "D5 pushes physical events into the present.",
    "gravity entropy identity inflation": "Gravity is entropy.",
    "gravity time-direction inflation": "Gravity points past to present.",
    "future light cone as source": "The future light cone is a causal source for present choice.",
    "represented bundle proves multiverse": "A represented history bundle proves a physical multiverse.",
}
V21_REJECT_FIXTURES = (
    ("Emergentism proof inflation", "Emergentism has been scientifically established."),
    ("Emergentism exhaustive or unique inflation", "Emergentism provides the unique explanation of Being."),
    ("Dasein atlas exhaustion inflation", "The dimensional atlas exhausts Dasein."),
    ("Burrisphere mirror-partition collapse", "The G7 Burrisphere is 3+1+3."),
    ("geometry generates or confirms seven", "The Burrisphere independently generates seven."),
    ("Rosetta convergence truth-evidence inflation", "Rosetta convergence is truth evidence."),
    ("G7 GEN7 identity inflation", "G7@1 = GEN7@1."),
    ("lowercase uppercase power collapse", "φ and ν are the same as Φ and V."),
    ("lowercase horizon-power identity inflation", "ν is V₄."),
    ("lowercase horizon-power identity inflation", "φ is Φ₅."),
    ("horizon coordinate time inflation", "q_H represents physical time."),
    ("universal centre optimum inflation", "The centre is the universal optimum."),
    ("tradeoff elimination inflation", "The centre eliminates real tradeoffs."),
    ("least opportunity claim inflation", "The centre gives the least opportunity cost."),
    ("geometry Dharma-flow inflation", "The reciprocal chart proves Dharma."),
    ("geometry Dharma-flow inflation", "Geometry guarantees flow."),
    ("bare ego-collective signs exhaust M4", "Bare ego/collective signs exhaust M4."),
    ("display path dynamics inflation", "The helix represents physical dynamics."),
    ("display path time inflation", "The winding path encodes time."),
    ("display path recurrence inflation", "The 360° display path proves a cycle."),
    ("display path value-ascent inflation", "The helix represents moral ascent."),
    ("display path count-derivation inflation", "The winding path derives seven."),
    ("reciprocal product centre-peak inflation", "φν peaks at the centre."),
    (
        "positive chart signed-G7 identity inflation",
        "The lowercase positive reciprocal chart is the signed G7 plane.",
    ),
    ("G7 all-game exhaustion inflation", "G7 exhausts all of game theory."),
    ("uppercase product ranking revival", "The uppercase product ranking has returned."),
    (
        "basic-strategy maximum certainty inflation",
        "M4 is the maximum compression of basic strategy.",
    ),
    (
        "basic-strategy maximum certainty inflation",
        "M4 is a maximally compressed cross-game basis.",
    ),
    ("M4 game-theory exhaustion inflation", "M4 exhausts all of game theory."),
    ("strategy axes identity inflation", "Direction is the same axis as power channel."),
    ("ego-collective identity inflation", "Self-facing means ego."),
    (
        "theft-sacrifice moral-verdict inflation",
        "Theft and sacrifice are moral verdicts.",
    ),
    ("mental-physical power identity inflation", "Mental power is Φ₅."),
    ("Phi5 mental-only narrowing", "Φ₅ is only mental power."),
    ("M4 game enumeration inflation", "M4 enumerates every game."),
    ("native-game reconstruction inflation", "M4 reconstructs native games."),
    ("native-game replacement inflation", "M4 replaces native game descriptions."),
    ("strategy-test execution inflation", "The M4 maximality test has been run."),
    (
        "strategy-test truth-evidence inflation",
        "The rate-distortion frontier provides truth evidence.",
    ),
    ("lossless strategy-code inflation", "M4 is a lossless code for native games."),
    ("unpreregistered maximality inflation", "M4 is proven maximal without preregistration."),
    (
        "global unique maximality inflation",
        "A finite scored run establishes M4 as uniquely globally maximal.",
    ),
    (
        "performance-free compression inflation",
        "Minimum description length alone establishes maximality.",
    ),
    (
        "unbounded comparator-class inflation",
        "M4 beats every conceivable representation.",
    ),
)
V21_BOUNDED_FIXTURES = (
    ("Emergentism proof inflation", "Emergentism is not proved or externally validated."),
    ("Emergentism exhaustive or unique inflation", "Emergentism is not an exhaustive or uniquely established explanation."),
    ("Dasein atlas exhaustion inflation", "The dimensional atlas does not exhaust Dasein."),
    ("Burrisphere mirror-partition collapse", "The G7 Burrisphere is not the separate 3+1+3 mirror ladder."),
    ("geometry generates or confirms seven", "The Burrisphere does not independently generate or confirm seven."),
    ("Rosetta convergence truth-evidence inflation", "Rosetta convergence is not truth evidence."),
    ("G7 GEN7 identity inflation", "G7@1 ≠ GEN7@1."),
    ("lowercase uppercase power collapse", "φ and ν are not Φ and V."),
    ("lowercase horizon-power identity inflation", "ν≠V₄ and φ≠Φ₅."),
    ("horizon coordinate time inflation", "q_H is not time."),
    ("universal centre optimum inflation", "The centre is not a universal optimum."),
    ("tradeoff elimination inflation", "The centre does not eliminate real tradeoffs."),
    ("least opportunity claim inflation", "Least opportunity regret is only a conditional candidate."),
    ("geometry Dharma-flow inflation", "Geometry does not derive Dharma or guarantee flow."),
    ("bare ego-collective signs exhaust M4", "Bare ego/collective signs do not recover M4."),
    ("display path dynamics inflation", "The helix is not physical dynamics."),
    ("display path time inflation", "The winding path is not time."),
    ("display path recurrence inflation", "The 360° display path is not recurrence."),
    ("display path value-ascent inflation", "The helix is not moral ascent."),
    ("display path count-derivation inflation", "The winding path does not derive seven."),
    (
        "reciprocal product centre-peak inflation",
        "φν is constant and does not peak at the centre.",
    ),
    (
        "positive chart signed-G7 identity inflation",
        "The positive reciprocal chart is not the signed G7 plane.",
    ),
    ("G7 all-game exhaustion inflation", "G7 does not exhaust all game theory."),
    (
        "uppercase product ranking revival",
        "The retired uppercase product ranking has not returned.",
    ),
    (
        "basic-strategy maximum certainty inflation",
        "M4 is a candidate maximum compression of basic strategy.",
    ),
    (
        "basic-strategy maximum certainty inflation",
        "M4 is conjectured to be a maximally compressed cross-game basis.",
    ),
    ("M4 game-theory exhaustion inflation", "M4 does not exhaust game theory."),
    ("strategy axes identity inflation", "Direction and channel are distinct declared axes."),
    ("ego-collective identity inflation", "Self-facing is glossed as ego-facing, not identity."),
    (
        "theft-sacrifice moral-verdict inflation",
        "Theft and sacrifice are mnemonics, not moral verdicts.",
    ),
    (
        "mental-physical power identity inflation",
        "Mental and physical power are mnemonics, not identities with Φ₅ and V₄.",
    ),
    ("Phi5 mental-only narrowing", "Φ₅ is wider than mental power."),
    ("M4 game enumeration inflation", "M4 does not enumerate native games."),
    ("native-game reconstruction inflation", "M4 does not reconstruct native games."),
    ("native-game replacement inflation", "M4 does not replace native game descriptions."),
    (
        "strategy-test execution inflation",
        "The M4 maximality test requires preregistration and has not been run.",
    ),
    (
        "strategy-test truth-evidence inflation",
        "The rate-distortion test is not truth evidence.",
    ),
    (
        "lossless strategy-code inflation",
        "M4 is a lossy coding hypothesis and does not reconstruct native games.",
    ),
    (
        "unpreregistered maximality inflation",
        "M4 maximality is conjectural until preregistered comparator tests are run.",
    ),
    (
        "global unique maximality inflation",
        "A finite run cannot establish unique global maximality.",
    ),
    (
        "performance-free compression inflation",
        "Maximal means minimum description length at fixed acceptable performance.",
    ),
    (
        "unbounded comparator-class inflation",
        "M4 is compared only within the preregistered comparator class.",
    ),
)
NORMALIZED_FORBIDDEN = {name for name, _fixture in V21_REJECT_FIXTURES}
LIFECYCLE_AWARE_FORBIDDEN = {
    "literal D6 identity",
    "legacy untyped node product",
    "retired node product assignment",
}
# A repair/retirement marker must precede the quoted form in the same sentence.
# A later disclaimer cannot launder an affirmative formula.
LIFECYCLE_PREFIX = re.compile(
    r"(?:\b(?:retired|withdrawn|refuted|struck|killed|banned|ill-typed|ill typed)\b"
    r"[^.;:!?]{0,80}|\bno\s+(?:literal\s+)?identity\b[^.;:!?]{0,80})$",
    re.I,
)
LIFECYCLE_FIXTURES = {
    "literal D6 identity": "D6 ≡ D0",
    "legacy untyped node product": "P = Φ × V",
    "retired node product assignment": "P_node := Φ̂₄ × V₄",
}
CURRENT_BOOK_MARKERS = {
    "book/index.html": (
        "Only a declared common strictly increasing reparameterization applied to both factors is assumed here:",
        "independently reparameterized factor scales do not license an invariant cross-factor scalar ranking",
        "GP-03 remains open.",
    ),
    "manifesto/index.html": (
        "The One-Sitting Reader",
        "readable now &mdash; 12 chapters",
        "withheld, not current",
        "not the current <code>/book/</code> source",
    ),
    "read/index.html": (
        "Frozen generated-library records remain preserved with provenance",
        "current twelve-chapter One-Sitting Reader",
    ),
}
HIDDEN_ROBOTS_META = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\'][^"\']*\b(?:noindex|none)\b)[^>]*>',
    re.IGNORECASE,
)
FROZEN_LIBRARY_BOUNDARY_MARKER = "data-frozen-library-boundary"


def normalize_visible_text(text: str) -> str:
    """Return semantic text so routine HTML cannot bypass claim guards."""
    unescaped = html_lib.unescape(text)
    without_tags = re.sub(r"<[^>]*>", " ", unescaped)
    normalized = unicodedata.normalize("NFKC", without_tags)
    return re.sub(r"\s+", " ", normalized).strip()


def has_retired_node_product(text: str) -> bool:
    return bool(
        FORBIDDEN["retired node product assignment"].search(
            normalize_visible_text(text)
        )
    )


def has_titan_infix(text: str) -> bool:
    return bool(
        FORBIDDEN["forbidden Titan infix arithmetic"].search(
            normalize_visible_text(text)
        )
    )


def record_has_only_historical_k2(text: str) -> bool:
    """Allow the existing provenance label, not a blanket record-page waiver."""

    if "data-historical-authority-boundary" not in text:
        return False
    matches = list(FORBIDDEN["application authority leakage"].finditer(text))
    return bool(matches) and all(match.group(0).casefold() == "k2" for match in matches)


STATUS_SOURCE_CONTRACTS = {
    "00_THE_KERNEL_INDEX.md": "[I]",
    "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md": "[S/B]",
    "03_METHODOLOGY/03_PREREGISTRATIONS/06_THE_DASEIN_TEST_EUB1_v1.0.md": "[D]",
    "03_METHODOLOGY/03_PREREGISTRATIONS/07_PQA_54_COMPANION_v1.0.md": "[D]",
}


def parity_audit_surfaces(data: dict) -> list[str]:
    """Return every current/provisional surface subject to prohibition scans."""
    current = data.get("currentSurfaces")
    machine = data.get("machineSurfaces")
    provisional_block = data.get("declaredProvisional")
    if not isinstance(current, list) or not all(
        isinstance(item, str) for item in current
    ):
        raise ValueError("currentSurfaces must be a list of paths")
    if not isinstance(machine, list) or not all(
        isinstance(item, str) for item in machine
    ):
        raise ValueError("machineSurfaces must be a list of paths")
    if not isinstance(provisional_block, dict) or not isinstance(
        provisional_block.get("routes"), list
    ) or not all(isinstance(item, str) for item in provisional_block["routes"]):
        raise ValueError("declaredProvisional.routes must be a list of paths")
    combined = current + machine + provisional_block["routes"]
    if len(combined) != len(set(combined)):
        raise ValueError("current, machine, and provisional public surfaces must be disjoint")
    return combined

NEGATIVE_PRODUCT_RECORDS = {"axioms/index.html", "record/index.html"}

EXPECTED_G7_POWERS = {
    "possible": {"symbol": "Φ₅", "type": "D5 possible power", "causalByItself": False},
    "actual": {"symbol": "V₄", "type": "D4 actual power"},
    "presentEvaluation": {"symbol": "Φ̂₄", "type": "D4 evaluation of Φ₅"},
    "tier": "[S/I]",
}
EXPECTED_D5_CARD_IDS = [
    "OS01-09", "OS01-10", "OS01-11", "OS01-12", "OS01-33", "OS01-34", "OS01-35",
    "OS01-36", "OS01-37",
]
EXPECTED_EGO_COLLECTIVE_GLOSS = {
    "self": "ego-facing",
    "other": "collective-facing",
    "identity": False,
    "bareSignsRecoverM4": False,
    "tier": "[I]",
}
EXPECTED_G7_PLANE_AXES = {
    "bearerDirection": "self-facing to other-facing",
    "powerChannel": "raised Phi5 channel to raised V4 channel",
    "planePosition": "bottom action/projection plane",
    "tier": "[I]",
}
EXPECTED_G7_COUNT_SOURCE = {
    "id": "G7@1",
    "partition": [4, 3],
    "tier": "[S]",
    "derivation": "four bearer-oriented mixed-sign transfers plus three Titan-frame classes inside the selected vocabulary",
}
EXPECTED_G7_TRANSFERS = (
    {
        "id": "taking-a", "plain": "Taking-A", "alias": "Kali",
        "signature": "+Φ₅,self; −V₄,other", "quadrant": "top-left",
        "channelPair": "Φ₅,self ↔ V₄,other",
        "egoCollectiveSigns": "ego +Φ₅; collective −V₄",
    },
    {
        "id": "taking-b", "plain": "Taking-B", "alias": "Kālī",
        "signature": "+V₄,self; −Φ₅,other", "quadrant": "bottom-left",
        "channelPair": "V₄,self ↔ Φ₅,other",
        "egoCollectiveSigns": "ego +V₄; collective −Φ₅",
    },
    {
        "id": "giving-a", "plain": "Giving-A", "alias": "Kṛṣṇa",
        "signature": "−Φ₅,self; +V₄,other", "quadrant": "bottom-right",
        "channelPair": "Φ₅,self ↔ V₄,other",
        "egoCollectiveSigns": "ego −Φ₅; collective +V₄",
    },
    {
        "id": "giving-b", "plain": "Giving-B", "alias": "Arjuna",
        "signature": "−V₄,self; +Φ₅,other", "quadrant": "top-right",
        "channelPair": "V₄,self ↔ Φ₅,other",
        "egoCollectiveSigns": "ego −V₄; collective +Φ₅",
    },
)
EXPECTED_G7_FRAMES = (
    {"id": "shiva-dissolve", "plain": "dissolution", "alias": "Śiva", "glyph": "•", "axisPosition": "bottom", "signature": "−Φ₅; −V₄"},
    {
        "id": "vishnu-preserve", "plain": "preservation", "alias": "Viṣṇu",
        "glyph": "⊙",
        "glyphMeaning": "finite-realm glyph used for the preservation-frame projection",
        "axisPosition": "centre", "valueMarker": "1_T",
        "valueMarkerMeaning": "selected centre-unit marker",
        "glyphEqualsValueMarker": False,
        "signature": "ΔΦ₅≈0; ΔV₄≈0",
    },
    {"id": "brahma-create", "plain": "creation", "alias": "Brahmā", "glyph": "○", "axisPosition": "top", "signature": "+Φ₅; +V₄"},
)
EXPECTED_BURRISPHERE_G7 = {
    "layout": "four-bottom-plane-sectors-plus-three-world-vertical-stations",
    "actionPlanePosition": "bottom-projection-plane",
    "titanAxisPosition": "world-vertical",
    "transfersOnSphereSurface": False,
    "coLocatedWithLowerChart": True,
    "identicalToLowerChart": False,
    "tier": "[I]",
    "generatesCount": False,
    "meaningWithoutColor": True,
}
EXPECTED_G7_DISPLAY_PATH = {
    "schema": "emergentism/G7DisplayPath.v2",
    "geometry": "one-selected-turn-around-stationary-axis",
    "turns": 1,
    "degrees": 360,
    "verticalDirection": "bottom-to-top",
    "startFrame": "shiva-dissolve",
    "centreLatitude": "vishnu-preserve",
    "endFrame": "brahma-create",
    "traversesAxisPoint": False,
    "phaseOrder": ["taking-a", "taking-b", "giving-a", "giving-b"],
    "phaseOrderTier": "[I]",
    "phaseCarrier": "bottom-action-plane-trace",
    "bottomPlaneTraceTraversesM4": True,
    "spherePathCarriesTransfers": False,
    "semantics": "presentation-itinerary-only",
    "makesContinuousG7State": False,
    "dynamics": False,
    "causal": False,
    "temporal": False,
    "recurrent": False,
    "moralRanking": False,
    "derivesCount": False,
    "tier": "[I]",
}
EXPECTED_HORIZON_BALANCE_OVERLAY = {
    "schema": "emergentism/HorizonBalanceOverlay.v1",
    "status": "candidate-not-run",
    "sourceObject": "emergentism/ReciprocalSpectrum.v1",
    "chartWeights": {
        "short": "w_S:=ν/(φ+ν)",
        "long": "w_L:=φ/(φ+ν)",
        "tilt": "q_H:=w_L−w_S=(φ−ν)/(φ+ν)",
        "identities": [
            "w_S+w_L=1",
            "B=2sqrt(w_S*w_L)=sqrt(1−q_H^2)",
        ],
        "tier": "[A]",
    },
    "interpretation": {
        "negativeTilt": "short-horizon/present-enactment-facing (Vward)",
        "centre": "equal normalized chart weights",
        "positiveTilt": "long-horizon/represented-future-facing (Phiward)",
        "tier": "[I]",
    },
    "firewalls": {
        "lowercaseEqualsUppercase": False,
        "coordinateIsTime": False,
        "centreMeansShortClockEqualsLongClock": False,
        "futureContentActsByItself": False,
        "displayPathBecomesTemporal": False,
        "centreIsUniversalOptimum": False,
        "eliminatesTradeoffs": False,
        "derivesDharma": False,
    },
    "transfer": {
        "tier": "[C]",
        "requires": [
            "named-decision-domain",
            "named-short-and-long-horizons",
            "native-cardinal-calibration-or-explicit-ordinal-alternative",
            "feasible-set-or-budget",
            "complement-or-substitute-declaration",
            "prices-storage-and-asymmetry",
            "named-affected-bearers",
            "Justice-consent-and-Exit",
            "held-out-target-null-and-rivals",
        ],
    },
    "opportunityRegret": {
        "mode": "bearer-wise-Pareto-vector",
        "scalarAggregationDefault": False,
        "centreMinimizes": "candidate-only-under-declared-symmetric-premises",
        "tier": "[I/C]",
    },
    "normativePhenomenology": {
        "justiceFirst": True,
        "exitRequired": True,
        "dharmaDerivedFromChart": False,
        "flowRequiresIndependentOperationalization": True,
        "tier": "[S/I/C]",
    },
    "test": {
        "status": "not-run",
        "comparators": [
            "centre-policy", "Vward-policy", "Phiward-policy",
            "timescale-matched-policy", "native-domain-baseline",
        ],
        "kills": [
            "robust-off-centre-or-native-winner",
            "hidden-delayed-cost-or-harmed-bearer",
            "decorative-Exit",
            "no-independent-flow-relation",
        ],
        "survivor": [
            "reciprocal-chart-identities", "two-clock-practice",
            "bearer-complete-Justice", "lawful-context-specific-tilts",
        ],
        "truthEvidence": False,
        "tier": "[C]",
    },
    "truthEvidence": False,
    "tier": "[A/I/C]",
}
EXPECTED_RECIPROCAL_SPECTRUM = {
    "schema": "emergentism/ReciprocalSpectrum.v1",
    "domain": "positive reciprocal chart",
    "from": "ν→∞, φ→0",
    "centre": "φ=ν=1",
    "to": "φ→∞, ν→0",
    "constraint": "φν=1 everywhere",
    "constraintSelectsCentre": False,
    "balance": "B=2/(φ+ν)≤1",
    "uniqueMaximum": {"value": 1, "at": "φ=ν=1", "tier": "[A]"},
    "sameAsSignedG7Plane": False,
    "sameAsUppercasePowerModel": False,
    "revivesProductRanking": False,
    "g7ExhaustsAllGames": False,
    "horizonBalanceOverlay": EXPECTED_HORIZON_BALANCE_OVERLAY,
    "tier": "[A/S/I]",
}
EXPECTED_BASIC_STRATEGY_COMPRESSION = {
    "schema": "emergentism/BasicStrategyCompression.v1",
    "axes": {
        "direction": ["self-facing taking", "other-facing giving"],
        "channel": ["Φ₅ possible/model power", "V₄ actual/embodied power"],
    },
    "cells": 4,
    "scopedExhaustion": "selected M4 two-axis vocabulary",
    "compressionMode": "intensional-not-extensional",
    "compressionTarget": (
        "cross-game self/other direction and possible/actual power-channel orientation"
    ),
    "maximumCompressionCandidate": True,
    "exhaustsGameTheory": False,
    "reconstructsNativeGames": False,
    "nativeStructurePreserved": [
        "players",
        "coalitions",
        "information",
        "timing",
        "payoffs",
        "repetition",
        "stochasticity",
        "institutions",
        "learning",
        "equilibrium concepts",
    ],
    "maximalityTest": {
        "schema": "emergentism/StrategyCompressionTest.v1",
        "status": "preregistration-required-not-run",
        "coding": "lossy",
        "corpus": "declared cross-game corpus",
        "fixedBeforeCoding": [
            "native-game-descriptions",
            "bearer-indexed-option-capability-changes",
            "held-out-prediction-or-intervention-targets",
            "loss-function",
            "description-length-measure",
            "material-improvement-threshold",
            "acceptable-distortion-ceiling-or-target-utility-floor",
        ],
        "comparators": [
            "native-game-baseline",
            "coarser-one-axis-code",
            "added-axis-rival",
        ],
        "criterion": "declared rate-distortion frontier",
        "maximalDefinition": (
            "minimum-description-length-at-fixed-acceptable-performance-"
            "within-preregistered-comparator-class"
        ),
        "globalUniqueEstablished": False,
        "kills": [
            "richer-rival-clears-threshold-after-complexity-cost",
            "necessary-orientation-distinctions-collapse",
            "third-universal-channel-or-bearer-orientation",
        ],
        "truthEvidence": False,
        "tier": "[C]",
    },
    "mnemonics": {
        "egoCollective": {"tier": "[I]", "identity": False},
        "theftSacrifice": {"tier": "[I]", "moralVerdict": False},
        "mentalPhysical": {
            "tier": "[I]",
            "identity": False,
            "phi5WiderThanMental": True,
        },
    },
    "kills": [
        "third-power-channel",
        "additional-bearer-orientation",
        "unrecoverable-strategy-effect",
    ],
    "tier": "[S/I/C]",
}
EXPECTED_GEN7_MIRROR_LADDER = {
    "id": "GEN7@1",
    "partition": [3, 1, 3],
    "values": ["0", "1/2", "sqrt(3)/2", "1", "sqrt(3)/2", "1/2", "0"],
    "selectionTier": "[S]",
    "analyticGivenSelectionTier": "[A]",
    "projectionTier": "[I]",
    "isG7Burrisphere": False,
    "generatesCount": False,
}
EXPECTED_G7_GEN7_RELATION = {
    "g7NotGen7": True,
    "sameCount": True,
    "sameStructure": False,
    "geometryForcesSeven": False,
    "convergenceIsTruthEvidence": False,
    "lowercaseEqualsUppercase": False,
}
EXPECTED_G7_SOURCE_TIERS = {
    "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md": "[S/I/C]",
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md": "[A/I/C]",
    "05_COSMOLOGY/00_THE_BURRISPHERE.md": "[S] routing only",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/35_THE_LADDER_AND_THE_TWO_PARTITIONS_2026_08_05.md": "[A/S/I]",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md": "[S/I]",
    "00_HANDOFF/EMERGENTISM_ORG_V2_1_OWNER_DIRECTION_2026_08_23.md": "[B] direction",
    "00_HANDOFF/EMERGENTISM_HORIZON_BALANCE_OWNER_DIRECTION_2026_08_23.md": "[B] direction",
    "00_HANDOFF/EMERGENTISM_BURRISPHERE_BOTTOM_PLANE_OWNER_DIRECTION_2026_08_24.md": "[B] direction",
}


def _sha256_revision(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_projection_rows(
    label: str,
    rows: object,
    expected: tuple[dict, ...],
    errors: list[str],
) -> None:
    """Validate an ordered, ID-addressable part of G7Projection.v2."""

    if not isinstance(rows, list):
        errors.append(f"G7Projection.v2 {label} must be a list")
        return
    expected_ids = [row["id"] for row in expected]
    actual_ids = [row.get("id") if isinstance(row, dict) else None for row in rows]
    if actual_ids != expected_ids:
        errors.append(
            f"G7Projection.v2 {label} order/IDs drift: "
            f"expected {expected_ids}, got {actual_ids}"
        )
    for index, expected_row in enumerate(expected):
        if index >= len(rows):
            break
        if rows[index] != expected_row:
            errors.append(
                f"G7Projection.v2 {label} row drift: {expected_row['id']}"
            )
    if len(rows) != len(expected):
        errors.append(
            f"G7Projection.v2 {label} cardinality must be {len(expected)}, got {len(rows)}"
        )


def validate_g7_projection(levels: object, errors: list[str]) -> None:
    """Validate the corrected operational G7 and its two distinct projections."""

    if not isinstance(levels, list):
        errors.append("levels must be a list before validating G7Projection.v2")
        return
    d5_rows = [row for row in levels if isinstance(row, dict) and row.get("id") == "D5"]
    if len(d5_rows) != 1:
        errors.append("G7Projection.v2 requires exactly one D5 level")
        return
    d5 = d5_rows[0]
    if d5.get("claimCardIds") != EXPECTED_D5_CARD_IDS:
        errors.append(
            "D5 claimCardIds drift: "
            f"expected {EXPECTED_D5_CARD_IDS}, got {d5.get('claimCardIds')}"
        )
    stone = d5.get("stone")
    if not isinstance(stone, dict):
        errors.append("D5 stone must be an object")
        return
    projection = stone.get("projection")
    if not isinstance(projection, dict):
        errors.append("D5 stone.projection must be an object")
        return
    expected_keys = {
        "schema", "powers", "bearerIndices", "egoCollectiveGlossTier",
        "egoCollectiveGloss", "planeAxes", "countSource", "transfers", "frames",
        "burrisphereG7", "displayPath", "reciprocalSpectrum",
        "strategyCompression",
        "separateMirrorLadder", "relation", "sources",
    }
    if set(projection) != expected_keys:
        errors.append(
            "G7Projection.v2 field set drift: "
            f"expected {sorted(expected_keys)}, got {sorted(projection)}"
        )
    if projection.get("schema") != "emergentism/G7Projection.v2":
        errors.append("D5 stone.projection schema must be emergentism/G7Projection.v2")
    for key, expected in (
        ("powers", EXPECTED_G7_POWERS),
        ("bearerIndices", ["self", "other"]),
        ("egoCollectiveGlossTier", "[I]"),
        ("egoCollectiveGloss", EXPECTED_EGO_COLLECTIVE_GLOSS),
        ("planeAxes", EXPECTED_G7_PLANE_AXES),
        ("countSource", EXPECTED_G7_COUNT_SOURCE),
        ("burrisphereG7", EXPECTED_BURRISPHERE_G7),
        ("displayPath", EXPECTED_G7_DISPLAY_PATH),
        ("reciprocalSpectrum", EXPECTED_RECIPROCAL_SPECTRUM),
        ("strategyCompression", EXPECTED_BASIC_STRATEGY_COMPRESSION),
        ("separateMirrorLadder", EXPECTED_GEN7_MIRROR_LADDER),
        ("relation", EXPECTED_G7_GEN7_RELATION),
    ):
        if projection.get(key) != expected:
            errors.append(f"G7Projection.v2 {key} contract drift")
    _validate_projection_rows(
        "transfers", projection.get("transfers"), EXPECTED_G7_TRANSFERS, errors
    )
    _validate_projection_rows(
        "frames", projection.get("frames"), EXPECTED_G7_FRAMES, errors
    )

    sources = projection.get("sources")
    if not isinstance(sources, list):
        errors.append("G7Projection.v2 sources must be a list")
        return
    rows_by_path: dict[str, dict] = {}
    for row in sources:
        if not isinstance(row, dict):
            errors.append("G7Projection.v2 source row must be an object")
            continue
        source_rel = row.get("path")
        if not isinstance(source_rel, str) or not source_rel:
            errors.append("G7Projection.v2 source row missing path")
            continue
        if source_rel in rows_by_path:
            errors.append(f"G7Projection.v2 repeats source {source_rel}")
            continue
        rows_by_path[source_rel] = row
    if set(rows_by_path) != set(EXPECTED_G7_SOURCE_TIERS):
        errors.append(
            "G7Projection.v2 source set drift: "
            f"expected {sorted(EXPECTED_G7_SOURCE_TIERS)}, got {sorted(rows_by_path)}"
        )
    for source_rel, expected_tier in EXPECTED_G7_SOURCE_TIERS.items():
        row = rows_by_path.get(source_rel)
        if row is None:
            continue
        if set(row) != {"path", "sha256", "tier"}:
            errors.append(f"G7Projection.v2 source field set drift: {source_rel}")
        if row.get("tier") != expected_tier:
            errors.append(f"G7Projection.v2 source tier drift: {source_rel}")
        source_path = ROOT / source_rel
        try:
            source_path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"G7Projection.v2 source escapes corpus: {source_rel}")
            continue
        if not source_path.is_file():
            errors.append(f"G7Projection.v2 source missing: {source_rel}")
            continue
        actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if row.get("sha256") != actual_hash:
            errors.append(f"G7Projection.v2 source hash drift: {source_rel}")


def deployable_html_surfaces() -> list[str]:
    """Return every HTML artifact Vercel may receive under .vercelignore."""

    patterns = load_vercelignore_patterns()
    if patterns is None:
        raise ValueError(".vercelignore is required to determine deployable HTML")
    surfaces: list[str] = []
    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
            continue
        rel = path.relative_to(SITE).as_posix()
        if not is_vercel_ignored(rel, patterns):
            surfaces.append(rel)
    return sorted(surfaces)


def withheld_public_routes() -> set[str]:
    """Read the exact withheld-route policy for RAG custody checks."""

    registry_path = SITE / "withheld-routes.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read withheld-route registry: {exc}") from exc
    artifacts = registry.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("withheld-route registry artifacts must be a list")
    routes: set[str] = set()
    for item in artifacts:
        item_routes = item.get("publicRoutes") if isinstance(item, dict) else None
        if not isinstance(item_routes, list) or not all(
            isinstance(route, str) for route in item_routes
        ):
            raise ValueError("withheld-route registry has an invalid publicRoutes entry")
        routes.update(item_routes)
    return routes


def has_unretired_forbidden_match(text: str, name: str) -> bool:
    """True when a lifecycle-aware retired form is used rather than mentioned."""

    if name not in LIFECYCLE_AWARE_FORBIDDEN:
        raise ValueError(f"{name} is not a lifecycle-aware public prohibition")
    candidate = normalize_visible_text(text)
    pattern = FORBIDDEN[name]
    for match in pattern.finditer(candidate):
        prefix = candidate[max(0, match.start() - 180):match.start()]
        if not LIFECYCLE_PREFIX.search(prefix):
            return True
    return False


def validate_status_source_claims(data: dict, errors: list[str]) -> None:
    """Bind narrow owner-status copy without promoting it to a claim card.

    This extension is deliberately local to this corpus: it can attest that a
    public page accurately reports an editorial or record status, but it cannot
    add a doctrine claim, import an application source, or raise an evidence
    tier. Claim-bearing public language remains governed by ``surfaceClaims``.
    """

    bindings = data.get("statusSourceClaims", [])
    if not isinstance(bindings, list):
        errors.append("statusSourceClaims must be a list")
        return
    seen_ids: set[str] = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            errors.append("status source binding must be an object")
            continue
        binding_id = binding.get("id")
        if not isinstance(binding_id, str) or not binding_id:
            errors.append("status source binding missing id")
            continue
        if binding_id in seen_ids:
            errors.append(f"duplicate status source binding: {binding_id}")
            continue
        seen_ids.add(binding_id)
        for key in ("surface", "role", "source", "sourceRevision", "tier", "requiredMarkers", "scope"):
            if not binding.get(key):
                errors.append(f"{binding_id} status source binding missing {key}")
        if binding.get("scope") != "editorial_or_record_status_only":
            errors.append(f"{binding_id} status source binding has invalid scope")
        tier = binding.get("tier")
        if binding.get("surface") not in data.get("currentSurfaces", []):
            errors.append(f"{binding_id} status binding is not a current surface")
        markers = binding.get("requiredMarkers")
        if not isinstance(markers, list) or not all(isinstance(marker, str) and marker for marker in markers):
            errors.append(f"{binding_id} status binding requiredMarkers must be non-empty strings")
            markers = []
        source_rel = binding.get("source")
        if not isinstance(source_rel, str) or not source_rel:
            continue
        expected_tier = STATUS_SOURCE_CONTRACTS.get(source_rel)
        if expected_tier is None:
            errors.append(f"{binding_id} status source is not an approved owner-status source")
            continue
        if tier != expected_tier:
            errors.append(f"{binding_id} status source tier must remain {expected_tier}")
        source_path = ROOT / source_rel
        try:
            source_path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{binding_id} status source escapes the Emergentism corpus")
            continue
        if not source_path.is_file():
            errors.append(f"{binding_id} status source is missing: {source_rel}")
        elif binding.get("sourceRevision") != _sha256_revision(source_path):
            errors.append(f"{binding_id} status sourceRevision drift: {source_rel}")
        surface = binding.get("surface")
        page = SITE / surface if isinstance(surface, str) else None
        rendered = page.read_text(encoding="utf-8", errors="replace") if page and page.is_file() else ""
        visible = normalize_visible_text(rendered)
        for marker in markers:
            if marker not in visible:
                errors.append(f"{binding_id} missing bound public marker {marker!r}")
        if "claimCardIds" in binding or "publicDisposition" in binding:
            errors.append(f"{binding_id} status binding may not act as a claim-card binding")


def _routing_semantic_keys(value: object, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in ROUTING_FORBIDDEN_KEYS:
                errors.append(child_path)
            errors.extend(_routing_semantic_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_routing_semantic_keys(child, f"{path}[{index}]"))
    return errors


def validate_core_routing(data: dict, errors: list[str]) -> None:
    """Keep presentation routing exact and separate from semantic ownership."""

    journey = data.get("coreJourney")
    navigation = data.get("navigation")
    if not isinstance(journey, dict):
        errors.append("coreJourney must be an object")
        return
    if not isinstance(navigation, dict):
        errors.append("navigation must be an object")
        return
    if journey.get("question") != EXPECTED_CORE_QUESTION:
        errors.append("coreJourney question drift")
    surfaces = journey.get("surfaces")
    if surfaces != EXPECTED_CORE_JOURNEY:
        errors.append("coreJourney surfaces must match the exact ordered v6 journey")
    elif len(surfaces) != len(set(surfaces)):
        errors.append("coreJourney surfaces repeat an artifact")
    current = set(data.get("currentSurfaces", []))
    for surface in EXPECTED_CORE_JOURNEY:
        if surface not in current:
            errors.append(f"coreJourney surface is not current: {surface}")
    if navigation.get("primary") != EXPECTED_PRIMARY_NAV:
        errors.append("primary navigation contract drift")
    if navigation.get("mobilePersistent") != EXPECTED_MOBILE_NAV:
        errors.append("mobile persistent navigation contract drift")
    for path in _routing_semantic_keys({"coreJourney": journey, "navigation": navigation}):
        errors.append(f"routing block may not own semantics: {path}")


def f5_typing_errors(text: str) -> list[str]:
    """Reject F5/entropy shorthand that hides required types and bearers."""

    visible = normalize_visible_text(text)
    folded = visible.casefold()
    errors: list[str] = []
    if "least entropy" in folded:
        required = (
            "thermodynamic entropy", "entropy production", "path", "empowerment",
        )
        if any(marker not in folded for marker in required):
            errors.append("least entropy lacks the four-ledger separation")
    if re.search(r"\bagent (?:potential|options)\b", folded):
        required = ("affected", "consent", "justice", "exit")
        if any(marker not in folded for marker in required):
            errors.append("agent potential hides affected bearers or safeguards")
    if "strange attractor" in folded:
        required = ("state space", "flow", "invariant set", "attraction test")
        if any(marker not in folded for marker in required):
            errors.append("strange attractor lacks declared dynamics")
    return errors


def validate_v5_churning(data: dict, errors: list[str]) -> None:
    """Fail closed on the Third Churning's public lifecycle projection."""

    contract = data.get("churning")
    if not isinstance(contract, dict):
        errors.append("churning must be an object")
        return
    expected_keys = {
        "schemaId", "releaseId", "frozenSourceCommit", "sourcePacket",
        "sourcePacketRevision", "dropCounts", "pqaCounts", "routeRoles",
        "machineOutputs", "plainLabelsBeforeAliases",
        "classificationIsEvidenceTier", "publicationCreatesEarnedReview",
        "trainingInclusionGuaranteed", "requiredDropFields", "boundary",
    }
    if set(contract) != expected_keys:
        errors.append(
            "churning field set drift: "
            f"expected {sorted(expected_keys)}, got {sorted(contract)}"
        )
    if contract.get("schemaId") != "ThirdChurningPublicContract.v1":
        errors.append("churning schema identity drift")
    if contract.get("releaseId") != "THIRD-CHURNING-2026-08-23":
        errors.append("churning release identity drift")
    if contract.get("frozenSourceCommit") != "8b07e00c563f338923b1928d3469c862d44c1e07":
        errors.append("churning frozen source commit drift")
    if contract.get("dropCounts") != EXPECTED_CHURNING_COUNTS:
        errors.append("churning drop counts must remain 22/29 within ceiling 64")
    if contract.get("pqaCounts") != EXPECTED_PQA_COUNTS:
        errors.append("churning PQA counts must remain 54/0/0/0")
    if contract.get("routeRoles") != EXPECTED_CHURNING_ROUTES:
        errors.append("churning route-role contract drift")
    if contract.get("machineOutputs") != EXPECTED_CHURNING_MACHINE_OUTPUTS:
        errors.append("churning machine-output contract drift")
    machine_surfaces = data.get("machineSurfaces", [])
    if not isinstance(machine_surfaces, list) or any(
        rel not in machine_surfaces for rel in EXPECTED_CHURNING_MACHINE_OUTPUTS
    ):
        errors.append("churning machine outputs are not all registered machine surfaces")
    if contract.get("plainLabelsBeforeAliases") is not True:
        errors.append("churning plain labels must precede aliases")
    if contract.get("classificationIsEvidenceTier") is not False:
        errors.append("churning classification must remain distinct from evidence tier")
    if contract.get("publicationCreatesEarnedReview") is not False:
        errors.append("churning publication cannot create earned review")
    if contract.get("trainingInclusionGuaranteed") is not False:
        errors.append("churning cannot guarantee future AI training inclusion")

    required_drop_fields = [
        "source_refs", "evidence_tier", "strongest_rival", "kill_criterion",
        "residual_debt", "survivor_if_killed", "means_message", "ends_limits",
    ]
    if contract.get("requiredDropFields") != required_drop_fields:
        errors.append("churning proposition-level evidence field contract drift")

    source_rel = contract.get("sourcePacket")
    if not isinstance(source_rel, str) or not source_rel:
        errors.append("churning sourcePacket is missing")
        return
    source_path = (ROOT / source_rel).resolve()
    try:
        source_path.relative_to(ROOT.resolve())
    except ValueError:
        errors.append("churning sourcePacket escapes the corpus")
        return
    if not source_path.is_file():
        errors.append(f"churning sourcePacket is missing: {source_rel}")
        return
    if contract.get("sourcePacketRevision") != _sha256_revision(source_path):
        errors.append("churning sourcePacketRevision drift")
    try:
        packet = json.loads(source_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append("churning sourcePacket is malformed JSON")
        return
    if not isinstance(packet, dict):
        errors.append("churning sourcePacket must contain an object")
        return
    if packet.get("schema_id") != "emergentism/ThirdChurningCorpus.v1":
        errors.append("Third Churning source packet schema drift")
    if packet.get("release_id") != contract.get("releaseId"):
        errors.append("Third Churning source packet release drift")
    if packet.get("frozen_source_commit") != contract.get("frozenSourceCommit"):
        errors.append("Third Churning source packet frozen commit drift")
    if packet.get("drop_ceiling") != EXPECTED_CHURNING_COUNTS["ceiling"]:
        errors.append("Third Churning source packet drop ceiling drift")
    if packet.get("output_map") != EXPECTED_CHURNING_OUTPUT_MAP:
        errors.append("Third Churning source packet output map drift")
    if packet.get("pqa_launch_counts") != {
        "selected": 54,
        "evaluated": 0,
        "independently_reviewed": 0,
        "resolved": 0,
    }:
        errors.append("Third Churning source packet PQA state drift")
    external_states = packet.get("external_states")
    if not isinstance(external_states, dict) or external_states.get(
        "training_inclusion_guaranteed"
    ) is not False:
        errors.append("Third Churning source packet training boundary drift")

    expected_schema_paths = {
        "drop": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ChurningDrop.v1.schema.json",
        "problem": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ProblemAdjudication.v1.schema.json",
        "corpus": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ThirdChurningCorpus.v1.schema.json",
    }
    if packet.get("schema_paths") != expected_schema_paths:
        errors.append("Third Churning source schema-path contract drift")
    for label, rel in expected_schema_paths.items():
        if not (ROOT / rel).is_file():
            errors.append(f"Third Churning {label} source schema is missing: {rel}")

    packet_paths = packet.get("source_pathset")
    packet_hash_rows = packet.get("source_hashes")
    if not isinstance(packet_paths, list) or not all(
        isinstance(rel, str) and rel for rel in packet_paths
    ):
        errors.append("Third Churning source pathset is malformed")
        packet_paths = []
    if not isinstance(packet_hash_rows, list):
        errors.append("Third Churning source hashes are malformed")
        packet_hash_rows = []
    packet_hashes: dict[str, str] = {}
    for row in packet_hash_rows:
        if not isinstance(row, dict):
            errors.append("Third Churning source hash row must be an object")
            continue
        rel = row.get("path")
        digest = row.get("sha256")
        if not isinstance(rel, str) or not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            errors.append("Third Churning source hash row is malformed")
            continue
        if rel in packet_hashes:
            errors.append(f"Third Churning source hash repeats path: {rel}")
        packet_hashes[rel] = str(digest)
        source = ROOT / rel
        if not source.is_file():
            errors.append(f"Third Churning named source is missing: {rel}")
    if packet_paths != list(packet_hashes):
        errors.append("Third Churning source pathset/hash order drift")

    data_dir = source_path.parent / "data"
    source_data = {
        "drops": data_dir / "churning_drops.v1.json",
        "problems": data_dir / "problem_adjudications.v1.json",
        "paradoxes": data_dir / "paradox_inventory.v1.json",
    }
    parsed: dict[str, object] = {}
    for label, path in source_data.items():
        if not path.is_file():
            errors.append(f"Third Churning {label} source is missing: {path.relative_to(ROOT)}")
            continue
        try:
            parsed[label] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append(f"Third Churning {label} source is malformed JSON")

    drops = parsed.get("drops")
    if isinstance(drops, list):
        classifications = Counter()
        seen_drop_ids: set[str] = set()
        alias_by_class = {
            "SURVIVOR_CANDIDATE": "AMRITA",
            "POISON_WARNING": "HALAHALA",
        }
        for index, drop in enumerate(drops):
            if not isinstance(drop, dict):
                errors.append(f"Third Churning drop {index} must be an object")
                continue
            drop_id = drop.get("drop_id")
            if not isinstance(drop_id, str) or not drop_id:
                errors.append(f"Third Churning drop {index} is missing drop_id")
            elif drop_id in seen_drop_ids:
                errors.append(f"Third Churning repeats drop_id: {drop_id}")
            else:
                seen_drop_ids.add(drop_id)
            classification = drop.get("classification")
            classifications[classification] += 1
            if classification not in alias_by_class:
                errors.append(f"{drop_id or index} has invalid public classification")
            elif drop.get("mythic_alias") != alias_by_class[classification]:
                errors.append(f"{drop_id or index} classification/alias drift")
            if not isinstance(drop.get("plain_name"), str) or not drop["plain_name"].strip():
                errors.append(f"{drop_id or index} is missing its plain-first name")
            for field in required_drop_fields:
                if not drop.get(field):
                    errors.append(f"{drop_id or index} missing proposition field {field}")
            tier = drop.get("evidence_tier")
            if not isinstance(tier, str) or not re.fullmatch(r"\[[A-Z/]+\]", tier):
                errors.append(f"{drop_id or index} evidence tier is malformed")
            if classification == tier:
                errors.append(f"{drop_id or index} collapses classification into tier")
            source_refs = drop.get("source_refs")
            if isinstance(source_refs, list):
                for source_ref in source_refs:
                    if not isinstance(source_ref, dict):
                        errors.append(f"{drop_id or index} source reference must be an object")
                        continue
                    rel = source_ref.get("path")
                    if rel not in packet_hashes:
                        errors.append(f"{drop_id or index} source is outside the source packet: {rel}")
                    elif source_ref.get("sha256") != packet_hashes[rel]:
                        errors.append(f"{drop_id or index} source hash drifts from packet: {rel}")
            means = drop.get("means_message")
            if not isinstance(means, dict) or any(
                not means.get(key) for key in ("bearers", "short_horizon", "long_horizon")
            ):
                errors.append(f"{drop_id or index} bearer-horizon ledger is incomplete")
            limits = drop.get("ends_limits")
            if not isinstance(limits, dict) or any(
                not limits.get(key) for key in ("hard_limit", "residue", "exit", "uncertainty")
            ):
                errors.append(f"{drop_id or index} ends-limit ledger is incomplete")
            if drop.get("earned_review") != {
                "state": "UNREVIEWED",
                "independent_review_count": 0,
                "receipts": [],
            }:
                errors.append(f"{drop_id or index} publication/review boundary drift")
        if len(drops) != EXPECTED_CHURNING_COUNTS["total"]:
            errors.append(f"Third Churning must contain exactly 51 drops, got {len(drops)}")
        if classifications != Counter({"SURVIVOR_CANDIDATE": 22, "POISON_WARNING": 29}):
            errors.append(f"Third Churning classification counts drift: {dict(classifications)}")
        if packet.get("drop_order") != [
            drop.get("drop_id") for drop in drops if isinstance(drop, dict)
        ]:
            errors.append("Third Churning packet/drop source order drift")
    elif "drops" in parsed:
        errors.append("Third Churning drops source must contain a list")

    problems = parsed.get("problems")
    if isinstance(problems, list):
        problem_ids = [
            row.get("problem_id") if isinstance(row, dict) else None for row in problems
        ]
        if len(problems) != 54 or problem_ids != packet.get("problem_order"):
            errors.append("Third Churning problem source must preserve the exact ordered PQA-54 denominator")
        for index, row in enumerate(problems):
            if not isinstance(row, dict):
                errors.append(f"Third Churning problem {index} must be an object")
                continue
            if row.get("result_state") != "SELECTED":
                errors.append(f"{row.get('problem_id', index)} is not merely selected")
            if row.get("earned_effect") != "NO_INCREMENT":
                errors.append(f"{row.get('problem_id', index)} claims an earned effect")
            if row.get("native_reviews") != []:
                errors.append(f"{row.get('problem_id', index)} claims native review")
    elif "problems" in parsed:
        errors.append("Third Churning problems source must contain a list")
    paradoxes = parsed.get("paradoxes")
    if isinstance(paradoxes, dict):
        expected_paradox_counts = {
            "formal": 9,
            "legacy": 21,
            "synthesis": 4,
            "legacy_dissolved": 0,
        }
        rows = paradoxes.get("rows")
        if paradoxes.get("schema_id") != "emergentism/ParadoxInventory.v1":
            errors.append("Third Churning paradox source schema drift")
        if paradoxes.get("frozen_source_commit") != contract.get("frozenSourceCommit"):
            errors.append("Third Churning paradox source frozen commit drift")
        if paradoxes.get("counts") != expected_paradox_counts:
            errors.append("Third Churning paradox inventory count drift")
        if not isinstance(rows, list) or len(rows) != sum(
            value for key, value in expected_paradox_counts.items()
            if key != "legacy_dissolved"
        ):
            errors.append("Third Churning paradox inventory row count drift")
        elif any(
            not isinstance(row, dict) or not row.get("residual") for row in rows
        ):
            errors.append("Third Churning paradox inventory drops residual debt")
        elif Counter(row.get("earned_state") for row in rows) != Counter({
            "NOT_INDEPENDENTLY_REVIEWED": 9,
            "0_OF_21_DISSOLVED": 21,
            "SELECTED": 2,
            "UNREVIEWED": 2,
        }):
            errors.append("Third Churning paradox earned-state inventory drift")
    elif "paradoxes" in parsed:
        errors.append("Third Churning paradox source must contain an object")


def validate_v6_fourth_churning(data: dict, errors: list[str]) -> None:
    """Fail closed on the additive Fourth Churning diagnosis sidecar."""

    contract = data.get("fourthChurning")
    if not isinstance(contract, dict):
        errors.append("fourthChurning must be an object")
        return
    expected_keys = {
        "schemaId", "releaseId", "sourcePacket", "candidateCounts", "axes",
        "subtypeCount", "earnedEffects", "heldOutIntegrity",
        "globalPhilosophyClaimAllowed", "machineOutputs", "boundary",
    }
    if set(contract) != expected_keys:
        errors.append("fourthChurning field set drift")
    if contract.get("schemaId") != "FourthChurningPublicContract.v1":
        errors.append("fourthChurning schema identity drift")
    if contract.get("releaseId") != "FOURTH-CHURNING-2026-08-24":
        errors.append("fourthChurning release identity drift")
    if contract.get("candidateCounts") != EXPECTED_FOURTH_COUNTS:
        errors.append("fourthChurning candidate counts must remain 1/46/2/5")
    if contract.get("axes") != EXPECTED_FOURTH_AXES or contract.get("subtypeCount") != 12:
        errors.append("fourthChurning grammar must remain seven axes and twelve subtypes")
    if contract.get("earnedEffects") != 0:
        errors.append("fourthChurning cannot pre-earn effects")
    if contract.get("heldOutIntegrity") != "CONTAMINATED_FOR_FOURTH_USE":
        errors.append("fourthChurning may not launder the exposed PQA split")
    if contract.get("globalPhilosophyClaimAllowed") is not False:
        errors.append("fourthChurning cannot claim to solve most philosophy")
    if contract.get("machineOutputs") != EXPECTED_FOURTH_MACHINE_OUTPUTS:
        errors.append("fourthChurning machine-output contract drift")
    machine = data.get("machineSurfaces", [])
    if not isinstance(machine, list) or any(rel not in machine for rel in EXPECTED_FOURTH_MACHINE_OUTPUTS):
        errors.append("fourthChurning machine outputs are not all registered")

    source_rel = contract.get("sourcePacket")
    if not isinstance(source_rel, str):
        errors.append("fourthChurning sourcePacket is missing")
        return
    source = (ROOT / source_rel).resolve()
    try:
        source.relative_to(ROOT.resolve())
    except ValueError:
        errors.append("fourthChurning sourcePacket escapes the corpus")
        return
    if not source.is_file():
        errors.append(f"fourthChurning sourcePacket is missing: {source_rel}")
        return
    try:
        corpus = json.loads(source.read_text(encoding="utf-8"))
        collisions = json.loads((SITE / "questions/collisions.json").read_text(encoding="utf-8"))
        diagnoses = json.loads((SITE / "questions/diagnoses.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"fourthChurning public projection malformed: {exc}")
        return
    if corpus.get("schema_id") != "emergentism/FourthChurningCorpus.v1":
        errors.append("Fourth Churning source packet schema drift")
    if corpus.get("candidate_counts") != EXPECTED_FOURTH_COUNTS:
        errors.append("Fourth Churning source candidate-count drift")
    if corpus.get("pqa_state") != {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}:
        errors.append("Fourth Churning changed the PQA null state")
    if len(collisions) != 12 or len(diagnoses) != 54:
        errors.append("Fourth Churning public denominator drift")
    if any(row.get("earned_effect") != "NO_INCREMENT" for row in diagnoses):
        errors.append("Fourth Churning public diagnosis claims an earned effect")
    if any(row.get("split_integrity") != "CONTAMINATED_FOR_FOURTH_USE" for row in diagnoses):
        errors.append("Fourth Churning public diagnosis launders held-out status")

    schema_pairs = (
        ("TypeCollision.v1.schema.json", "collision"),
        ("MysteryDiagnosis.v1.schema.json", "diagnosis"),
        ("FourthChurningCorpus.v1.schema.json", "corpus"),
    )
    for name, key in schema_pairs:
        source_schema = ROOT / corpus.get("schema_paths", {}).get(key, "__missing__")
        public_schema = SITE / "questions" / "schemas" / name
        if not source_schema.is_file() or not public_schema.is_file() or source_schema.read_bytes() != public_schema.read_bytes():
            errors.append(f"Fourth Churning schema-copy drift: {name}")


def validate_v7_decision_transaction(data: dict, errors: list[str]) -> None:
    """Fail closed on the local-only decision-transaction interaction."""

    contract = data.get("decisionTransaction")
    if not isinstance(contract, dict):
        errors.append("decisionTransaction must be an object")
        return
    expected = {
        "schemaId": "DecisionTransactionPublicContract.v1",
        "sourceDirection": "00_HANDOFF/EMERGENTISM_DECISION_TRANSACTION_SITE_DIRECTION_2026_08_24.md",
        "surfaces": ["index.html", "plainly/index.html", "practice/index.html", "exit/index.html"],
        "stages": ["MODEL", "CLASSIFY", "PREPARE", "HUMAN_COMMIT_OR_REFUSE", "OUTCOME", "REVISE"],
        "sectorRole": "DESCRIPTIVE_ORIENTATION_NOT_MORAL_VERDICT",
        "preparedState": "UNSIGNED_NONEXECUTING",
        "signatureMode": "LOCAL_ACKNOWLEDGMENT_ONLY",
        "execution": False,
        "transmission": False,
        "legalEffect": False,
        "financialEffect": False,
        "walletConnection": False,
        "worldviewExitDistinct": True,
        "outcomeReceiptDistinct": True,
        "boundary": (
            "The action exit leaves represented possibility for an authorized actual commitment. "
            "The worldview Exit permits refusal, an unsigned packet, or leaving Emergentism entirely."
        ),
    }
    if contract != expected:
        errors.append("decisionTransaction contract drift")

    source = (ROOT / expected["sourceDirection"]).resolve()
    try:
        source.relative_to(ROOT.resolve())
    except ValueError:
        errors.append("decisionTransaction source direction escapes the corpus")
    else:
        if not source.is_file():
            errors.append("decisionTransaction source direction is missing")

    markers = {
        "index.html": (
            "A possibility becomes a prepared transaction before it becomes an act.",
            "Prepared decision transaction · unsigned",
            "The action exit is the signature boundary",
            "The separate worldview Exit",
        ),
        "plainly/index.html": (
            "The sectors prepare the move.",
            "The action exit is the signature boundary.",
            "Two exits remain distinct.",
        ),
        "practice/index.html": (
            'id="receipt-builder"',
            'name="transaction-sector"',
            "Prepare unsigned transaction",
            "Record private commitment · local and non-legal",
            "Leave unrecorded",
            "PREPARED_UNSIGNED",
            "COMMITTED_LOCAL",
            "LOCAL_ACKNOWLEDGMENT_ONLY",
            "The prepared packet cannot sign itself.",
        ),
        "exit/index.html": (
            "Two exits, two different types",
            "Action exit",
            "Worldview Exit",
            "leave every prepared transaction unsigned",
        ),
    }
    for rel, required in markers.items():
        path = SITE / rel
        if not path.is_file():
            errors.append(f"decisionTransaction surface is missing: {rel}")
            continue
        source_text = path.read_text(encoding="utf-8")
        for marker in required:
            if marker not in source_text:
                errors.append(f"decisionTransaction marker missing from {rel}: {marker}")

    practice = SITE / "practice/index.html"
    if practice.is_file():
        text = practice.read_text(encoding="utf-8")
        for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "WebSocket", "ethereum.request"):
            if forbidden in text:
                errors.append(f"decisionTransaction practice must remain local-only: {forbidden}")
        local_boundary = (
            "Local only · no account · no wallet · no transmission · "
            "no execution · no recommendation"
        )
        if local_boundary not in text:
            errors.append("decisionTransaction practice boundary is not explicit")
        if not re.search(
            r'<button[^>]+id="sign-transaction"[^>]+disabled[^>]*>\s*'
            r'Record private commitment · local and non-legal',
            text,
        ):
            errors.append("decisionTransaction local commitment must begin disabled")


def validate_v4_contracts(data: dict, errors: list[str]) -> None:
    """Validate the v2.2 question, normative, and companion firewalls."""

    atlas_contract = data.get("questionAtlas")
    bridge = data.get("normativeBridge")
    companions = data.get("researchCompanions")
    if not isinstance(atlas_contract, dict):
        errors.append("questionAtlas must be an object")
        return
    if not isinstance(bridge, dict):
        errors.append("normativeBridge must be an object")
        return
    if not isinstance(companions, dict):
        errors.append("researchCompanions must be an object")
        return

    expected_counts = {
        "selected": 54,
        "evaluated": 0,
        "independentlyReviewed": 0,
        "resolved": 0,
    }
    if atlas_contract.get("schemaId") != "PQAAtlasManifest.v1":
        errors.append("questionAtlas schema identity drift")
    if atlas_contract.get("counts") != expected_counts:
        errors.append("questionAtlas launch counts must remain 54/0/0/0")
    if (
        atlas_contract.get("majorityThreshold") != 28
        or atlas_contract.get("perDomainMinimum") != 3
        or atlas_contract.get("globalPhilosophyClaimAllowed") is not False
    ):
        errors.append("questionAtlas bounded-majority contract drift")
    source_fields = ("protocol", "atlas", "publicProjection")
    sources: dict[str, Path] = {}
    for field in source_fields:
        rel = atlas_contract.get(field)
        if not isinstance(rel, str) or not rel:
            errors.append(f"questionAtlas.{field} is missing")
            continue
        path = (ROOT / rel).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"questionAtlas.{field} escapes the corpus")
            continue
        if not path.is_file():
            errors.append(f"questionAtlas.{field} is missing: {rel}")
            continue
        sources[field] = path
    if "atlas" in sources:
        try:
            atlas = json.loads(sources["atlas"].read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("questionAtlas source is malformed JSON")
        else:
            domains = atlas.get("domains", [])
            rows = [row for domain in domains if isinstance(domain, dict) for row in domain.get("questions", [])]
            if len(domains) != 9 or any(len(domain.get("questions", [])) != 6 for domain in domains if isinstance(domain, dict)) or len(rows) != 54:
                errors.append("questionAtlas source must preserve the exact 9x6 denominator")
            if atlas.get("launch_counts") != {
                "selected": 54,
                "evaluated": 0,
                "independently_reviewed": 0,
                "resolved": 0,
            }:
                errors.append("questionAtlas source launch state drift")
    if "publicProjection" in sources:
        try:
            projection = json.loads(sources["publicProjection"].read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("questionAtlas public projection is malformed JSON")
        else:
            if projection.get("counts") != {
                "selected": 54,
                "evaluated": 0,
                "independently_reviewed": 0,
                "resolved": 0,
            }:
                errors.append("questionAtlas public projection count drift")
            if projection.get("external_validation") is not False or projection.get("deployed") is not False:
                errors.append("questionAtlas offline projection cannot claim validation or deployment")

    if {
        bridge.get("directionCard"),
        bridge.get("coAgencyCard"),
        bridge.get("guardianshipCard"),
    } != {"OS01-38", "OS01-39", "OS01-40"}:
        errors.append("normativeBridge card ownership drift")
    for field in (
        "sharedPersonhoodInferred",
        "sharedConsentInferred",
        "authorityCreated",
        "moralRealismEstablished",
    ):
        if bridge.get(field) is not False:
            errors.append(f"normativeBridge.{field} must be false")
    if bridge.get("coAgencyAndGuardianshipAreDistinct") is not True:
        errors.append("normativeBridge must keep co-agency and guardianship distinct")
    if bridge.get("objectivityLevels") != [
        "DEFINITION_STABLE",
        "PROCEDURALLY_REPRODUCIBLE",
        "EMPIRICALLY_ADEQUATE",
        "STANCE_INDEPENDENT",
    ]:
        errors.append("normativeBridge objectivity-level order drift")

    if companions.get("truthTransfer") is not False or companions.get("scoreTransfer") is not False:
        errors.append("researchCompanions cannot transfer score or truth")
    eub = companions.get("eub1")
    pqa = companions.get("pqa54")
    if not isinstance(eub, dict) or eub.get("frozen") is not True or eub.get("candidateResults") != 0:
        errors.append("researchCompanions EUB-1 freeze/result boundary drift")
    if not isinstance(pqa, dict) or pqa.get("companionOnly") is not True or pqa.get("candidateResults") != 0:
        errors.append("researchCompanions PQA-54 boundary drift")


def validate_frontier_protocol(data: dict, errors: list[str]) -> None:
    """Keep the AI-facing Frontier a source-bound, launch-null projection."""

    contract = data.get("frontierProtocol")
    if not isinstance(contract, dict):
        errors.append("frontierProtocol must be an object")
        return
    expected_keys = {
        "schemaId", "protocolVersion", "semanticOwner", "publicPage", "catalog",
        "schema", "gapOutputPrefix", "launchCounts", "sourceInputs",
        "completenessClaim", "worldContactAccepted", "liveService",
        "modelAgreementIsTruthEvidence", "paymentCanBuyStanding", "boundary",
    }
    if set(contract) != expected_keys:
        errors.append("frontierProtocol field set drift")
    if contract.get("schemaId") != "FrontierGraph.v1" or contract.get("protocolVersion") != "1.0.0":
        errors.append("frontierProtocol identity drift")
    owner_rel = "03_METHODOLOGY/03_PREREGISTRATIONS/frontier_protocol/README.md"
    if contract.get("semanticOwner") != owner_rel or not (ROOT / owner_rel).is_file():
        errors.append("frontierProtocol semantic owner drift")
    if contract.get("launchCounts") != {
        "gaps": 12,
        "candidates": 0,
        "frozenTests": 0,
        "worldReceipts": 0,
        "revisions": 0,
    }:
        errors.append("frontierProtocol launch counts must remain 12/0/0/0/0")
    for field, expected in (
        ("completenessClaim", False),
        ("worldContactAccepted", 0),
        ("liveService", False),
        ("modelAgreementIsTruthEvidence", False),
        ("paymentCanBuyStanding", False),
    ):
        if contract.get(field) != expected:
            errors.append(f"frontierProtocol.{field} boundary drift")

    expected_sources = {
        "03_METHODOLOGY/00_W7_SCIENCE_INTEGRATION_EXECUTION_REGISTER.yaml": "canonical_gap_owner",
        "12_PUBLIC_SITE/living-map.json": "public_routing_overlay",
    }
    sources = contract.get("sourceInputs")
    if not isinstance(sources, list) or len(sources) != 2:
        errors.append("frontierProtocol must bind exactly two source inputs")
        sources = []
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"path", "sha256", "role"}:
            errors.append("frontierProtocol source-input shape drift")
            continue
        rel = source.get("path")
        seen.add(str(rel))
        if expected_sources.get(rel) != source.get("role"):
            errors.append(f"frontierProtocol source role drift: {rel}")
        path = ROOT / str(rel)
        if not path.is_file():
            errors.append(f"frontierProtocol source missing: {rel}")
        elif source.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
            errors.append(f"frontierProtocol source hash drift: {rel}")
    if seen != set(expected_sources):
        errors.append("frontierProtocol source set drift")

    page_rel = contract.get("publicPage")
    catalog_rel = contract.get("catalog")
    schema_rel = contract.get("schema")
    for rel in (page_rel, catalog_rel, schema_rel):
        if not isinstance(rel, str) or not (SITE / rel).is_file():
            errors.append(f"frontierProtocol output missing: {rel}")
    if page_rel not in data.get("currentSurfaces", []):
        errors.append("frontierProtocol public page is not a current surface")
    machine = set(data.get("machineSurfaces", []))
    gap_outputs = {f"frontier/v1/gaps/GP-{index:02d}.json" for index in range(1, 13)}
    expected_machine = {str(catalog_rel), str(schema_rel), *gap_outputs}
    if not expected_machine.issubset(machine):
        errors.append("frontierProtocol machine outputs are not all registered")
    if isinstance(catalog_rel, str) and (SITE / catalog_rel).is_file():
        catalog = json.loads((SITE / catalog_rel).read_text(encoding="utf-8"))
        if catalog.get("schema_id") != "FrontierGraph.v1":
            errors.append("frontier catalog schema drift")
        if catalog.get("counts") != {
            "gaps": 12,
            "candidates": 0,
            "frozen_tests": 0,
            "world_receipts": 0,
            "revisions": 0,
        }:
            errors.append("frontier catalog launch counts drift")
        if catalog.get("completeness_claim") is not False or catalog.get("world_contact_accepted") != 0:
            errors.append("frontier catalog result boundary drift")
        gaps = catalog.get("gaps")
        if not isinstance(gaps, list) or len(gaps) != 12:
            errors.append("frontier catalog must contain twelve gaps")
        elif len({row.get("gap_id") for row in gaps if isinstance(row, dict)}) != 12:
            errors.append("frontier catalog gap IDs are not unique")
    if isinstance(schema_rel, str) and (SITE / schema_rel).is_file():
        source_schema = ROOT / "03_METHODOLOGY/03_PREREGISTRATIONS/frontier_protocol/FrontierGraph.v1.schema.json"
        if not source_schema.is_file() or (SITE / schema_rel).read_bytes() != source_schema.read_bytes():
            errors.append("frontier public schema differs from its source sidecar")
    if isinstance(page_rel, str) and (SITE / page_rel).is_file():
        page = (SITE / page_rel).read_text(encoding="utf-8")
        for marker in (
            "Every intelligence", "OFFLINE-READY · [D]", "The Socket Rack",
            "No model is connected", "Fund the search.", "Never purchase standing.",
        ):
            if marker not in page:
                errors.append(f"frontier page missing boundary marker: {marker}")
        if page.count('class="fr-socket"') != 12:
            errors.append("frontier page must render twelve static sockets")

    atlas_path = SITE / "atlas/site_index.json"
    if atlas_path.is_file():
        atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
        atlas_hrefs = {
            page.get("href")
            for section in atlas.get("tree", [])
            if isinstance(section, dict)
            for page in section.get("pages", [])
            if isinstance(page, dict)
        }
        if "/frontier/" not in atlas_hrefs:
            errors.append("frontier page is absent from the public Atlas index")

    rag_path = SITE / "book/rag_index.json"
    if rag_path.is_file():
        rag = json.loads(rag_path.read_text(encoding="utf-8"))
        if not any(
            isinstance(row, dict) and row.get("href") == "/frontier/"
            for row in rag.get("passages", [])
        ):
            errors.append("frontier page is absent from the current RAG index")


def main() -> int:
    errors: list[str] = []
    for fixture in NODE_PRODUCT_REJECT_FIXTURES:
        if not has_retired_node_product(fixture):
            errors.append(f"retired node product negative-control escaped: {fixture}")
    for fixture in NODE_PRODUCT_BOUNDED_FIXTURES:
        if has_retired_node_product(fixture):
            errors.append(f"retired node product rule overmatched bounded wording: {fixture}")
    for fixture in TITAN_INFIX_REJECT_FIXTURES:
        if not has_titan_infix(fixture):
            errors.append(f"Titan infix negative-control escaped: {fixture}")
    for fixture in TITAN_OPERATOR_FREE_FIXTURES:
        if has_titan_infix(fixture):
            errors.append(f"Titan infix rule overmatched operator-free wording: {fixture}")
    for name, fixture in F5_REJECT_FIXTURES.items():
        if not FORBIDDEN[name].search(fixture):
            errors.append(f"F5 negative-control escaped: {name}")
    for name, fixture in V21_REJECT_FIXTURES:
        if not FORBIDDEN[name].search(normalize_visible_text(fixture)):
            errors.append(f"v2.1 negative-control escaped: {name}")
    for name, fixture in V21_BOUNDED_FIXTURES:
        if FORBIDDEN[name].search(normalize_visible_text(fixture)):
            errors.append(f"v2.1 rule overmatched bounded wording: {name}")
    for fixture, expected in (
        ("Choose the least entropy future.", "least entropy lacks the four-ledger separation"),
        ("Maximize agent options.", "agent potential hides affected bearers or safeguards"),
        ("Potential is a strange attractor.", "strange attractor lacks declared dynamics"),
    ):
        if expected not in f5_typing_errors(fixture):
            errors.append(f"F5 typed-ledger negative-control escaped: {expected}")
    for name, fixture in LIFECYCLE_FIXTURES.items():
        if not has_unretired_forbidden_match(fixture, name):
            errors.append(f"lifecycle-aware prohibition escaped: {name}")
        if has_unretired_forbidden_match(f"Retired {fixture}", name):
            errors.append(f"lifecycle-aware prohibition overmatched retired mention: {name}")
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    try:
        audited_surfaces = parity_audit_surfaces(data)
    except ValueError as exc:
        errors.append(str(exc))
        audited_surfaces = []
    try:
        deployable_html = deployable_html_surfaces()
    except ValueError as exc:
        errors.append(str(exc))
        deployable_html = []
    deployment_patterns = load_vercelignore_patterns() or []
    for rel in audited_surfaces:
        path = SITE / rel
        if not path.is_file():
            errors.append(f"missing current/provisional public surface: {rel}")
        elif is_vercel_ignored(rel, deployment_patterns):
            errors.append(f"current/provisional public surface is excluded from deployment: {rel}")
    try:
        excluded_routes = withheld_public_routes()
    except ValueError as exc:
        errors.append(str(exc))
        excluded_routes = set()
    if data.get("schemaVersion") != 7:
        errors.append("public semantic parity schemaVersion must be 7")
    validate_core_routing(data, errors)
    validate_v4_contracts(data, errors)
    validate_v5_churning(data, errors)
    validate_v6_fourth_churning(data, errors)
    validate_v7_decision_transaction(data, errors)
    validate_frontier_protocol(data, errors)
    contract = data.get("claimCardContract", {})
    required_contract = ("ledger", "register", "graph", "source", "sourceRevision", "lifecycle", "publicDisposition")
    for key in required_contract:
        if not contract.get(key):
            errors.append(f"claim-card contract missing {key}")
    claim_ids: set[str] = set()
    card_lookup: dict[str, dict] = {}
    ledger_path = ROOT / contract.get("ledger", "__missing__")
    if ledger_path.is_file():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        for card in ledger.get("cards", []):
            card_id = card.get("card_id")
            if card_id in card_lookup:
                errors.append(f"duplicate claim-card ID in public ledger: {card_id}")
            elif card_id:
                card_lookup[card_id] = card
                claim_ids.add(card_id)
    else:
        errors.append(f"missing claim-card ledger: {contract.get('ledger')}")
    register_lookup: dict[str, dict] = {}
    for key in ("register", "graph"):
        path = ROOT / contract.get(key, "__missing__")
        if not path.is_file():
            errors.append(f"missing claim-card {key}: {contract.get(key)}")
            continue
        if key == "register":
            register = json.loads(path.read_text(encoding="utf-8"))
            for row in register.get("cards", []):
                card_id = row.get("card_id")
                if not card_id:
                    errors.append("claim-card register contains a row without card_id")
                elif card_id in register_lookup:
                    errors.append(f"duplicate claim-card ID in derived register: {card_id}")
                else:
                    register_lookup[card_id] = row
    source_path = ROOT / contract.get("source", "__missing__")
    if source_path.is_file():
        actual_revision = _sha256_revision(source_path)
        if contract.get("sourceRevision") != actual_revision:
            errors.append("claim-card contract sourceRevision drift")
    else:
        errors.append(f"missing claim-card source: {contract.get('source')}")
    if contract.get("lifecycle") != "reader_synthesis":
        errors.append("public claim-card lifecycle must remain reader_synthesis")
    if contract.get("publicDisposition") != "bounded_current":
        errors.append("public claim-card disposition must remain bounded_current")
    if data.get("sequence") != EXPECTED_SEQUENCE:
        errors.append("dimension sequence is not the canonical D0/mu0...D6/r6 order")
    levels = data.get("levels", [])
    if [x.get("id") for x in levels] != [f"D{i}" for i in range(7)]:
        errors.append("levels must be exactly D0 through D6")
    crossings = [x.get("transition", {}).get("id") for x in levels if "transition" in x]
    if crossings != ["mu0", "mu1", "mu2", "mu3", "mu4", "b6"]:
        errors.append("transitions must be exactly mu0..mu4 plus b6")
    if levels[4].get("modality") != "actual" or levels[5].get("modality") != "possible":
        errors.append("D4 must be actual and D5 possible")
    validate_g7_projection(levels, errors)
    for item in levels:
        for key in ("claimCardIds", "sourceRevision", "lifecycle", "publicDisposition"):
            if not item.get(key):
                errors.append(f"{item.get('id', '?')} missing claim-card parity field {key}")
        if item.get("lifecycle") != contract.get("lifecycle"):
            errors.append(f"{item.get('id', '?')} claim-card lifecycle drift")
        if item.get("publicDisposition") != contract.get("publicDisposition"):
            errors.append(f"{item.get('id', '?')} public disposition drift")
        for card_id in item.get("claimCardIds", []):
            if card_id not in claim_ids:
                errors.append(f"{item.get('id', '?')} binds unknown claim-card {card_id}")
                continue
            state = card_lookup[card_id].get("public", {}).get("state")
            if state not in {"bounded_current", "candidate"}:
                errors.append(f"{item.get('id', '?')} binds non-current claim-card {card_id} ({state})")
        source = ROOT / item["source"]
        if source.is_file():
            if item.get("sourceRevision") != _sha256_revision(source):
                errors.append(f"{item.get('id', '?')} sourceRevision drift: {item['source']}")
        else:
            errors.append(f"missing source owner: {item['source']}")
        if "transition" in item:
            tr = item["transition"]
            for key in ("source", "sourceRevision", "saturation", "capability", "recovery", "evidence", "prediction", "alternatives", "kill"):
                if not tr.get(key):
                    errors.append(f"{tr.get('id', '?')} missing {key}")
            transition_source = ROOT / tr["source"]
            if transition_source.is_file():
                if tr.get("sourceRevision") != _sha256_revision(transition_source):
                    errors.append(f"{tr.get('id', '?')} sourceRevision drift: {tr['source']}")
            else:
                errors.append(f"missing crossing owner: {tr['source']}")
        rendered_path = SITE / item["id"][1:] / "index.html"
        if not rendered_path.is_file():
            errors.append(f"{item['id']} missing rendered dimension surface")
            continue
        rendered = rendered_path.read_text(encoding="utf-8", errors="replace")
        for needle, label in (
            ('class="diagram visual-panel"', "instrument visual hook"),
            ('type="importmap"', "local Three.js import map"),
            ('type="module" src="../dimensions/dimensions.js"', "module instrument loader"),
            ('data-core-shell="v2"', "shared v2 navigation"),
        ):
            if needle not in rendered:
                errors.append(f"{item['id']} missing {label}")

    surface_claims = data.get("surfaceClaims", [])
    validate_status_source_claims(data, errors)
    surface_lookup: dict[str, dict] = {}
    for binding in surface_claims:
        surface = binding.get("surface")
        if not surface:
            errors.append("surface claim binding missing surface")
            continue
        if surface in surface_lookup:
            errors.append(f"duplicate surface claim binding: {surface}")
            continue
        surface_lookup[surface] = binding
        for key in (
            "role", "claimCardIds", "claimSources", "publicDisposition",
            "requiredMarkers",
        ):
            if not binding.get(key):
                errors.append(f"{surface} surface claim binding missing {key}")
        if surface not in data.get("currentSurfaces", []):
            errors.append(f"surface claim binding is not a current surface: {surface}")
        if binding.get("publicDisposition") != "bounded_current":
            errors.append(f"{surface} surface disposition must remain bounded_current")
        page = SITE / surface
        rendered = page.read_text(encoding="utf-8", errors="replace") if page.is_file() else ""
        for marker in binding.get("requiredMarkers", []):
            if marker not in rendered:
                errors.append(f"{surface} missing bound public marker {marker!r}")
        if len(binding.get("claimCardIds", [])) != len(set(binding.get("claimCardIds", []))):
            errors.append(f"{surface} repeats a claim-card ID")
        source_bound_cards: set[str] = set()
        source_paths: set[str] = set()
        for source_binding in binding.get("claimSources", []):
            for key in ("source", "sourceRevision", "lifecycle", "claimCardIds"):
                if not source_binding.get(key):
                    errors.append(f"{surface} claim source binding missing {key}")
            source_rel = source_binding.get("source", "__missing__")
            if source_rel in source_paths:
                errors.append(f"{surface} repeats claim source {source_rel}")
            source_paths.add(source_rel)
            source = ROOT / source_rel
            if source.is_file():
                actual_revision = _sha256_revision(source)
                if source_binding.get("sourceRevision") != actual_revision:
                    errors.append(f"{surface} claim sourceRevision drift: {source_rel}")
            else:
                errors.append(f"{surface} claim source is missing: {source_rel}")
            for card_id in source_binding.get("claimCardIds", []):
                if card_id in source_bound_cards:
                    errors.append(f"{surface} binds {card_id} to more than one source")
                source_bound_cards.add(card_id)
                row = register_lookup.get(card_id)
                if row is None:
                    continue
                if row.get("source_path") != source_rel:
                    errors.append(
                        f"{surface} source mismatch for {card_id}: "
                        f"{source_rel} != {row.get('source_path')}"
                    )
                if row.get("source_lifecycle") != source_binding.get("lifecycle"):
                    errors.append(f"{surface} lifecycle mismatch for {card_id}")
        if source_bound_cards != set(binding.get("claimCardIds", [])):
            errors.append(
                f"{surface} claimSources do not cover the declared claim-card set"
            )
        for card_id in binding.get("claimCardIds", []):
            row = register_lookup.get(card_id)
            if row is None:
                errors.append(f"{surface} binds unknown registered claim-card {card_id}")
                continue
            if row.get("public_state") not in {"bounded_current", "candidate"}:
                errors.append(
                    f"{surface} binds non-current registered claim-card {card_id} "
                    f"({row.get('public_state')})"
                )
            source_path = ROOT / row.get("source_path", "__missing__")
            if not source_path.is_file():
                errors.append(f"{surface} claim-card source is missing for {card_id}")
    for surface, expected_cards in REQUIRED_SURFACE_CARDS.items():
        binding = surface_lookup.get(surface)
        if binding is None:
            errors.append(f"missing required surface claim binding: {surface}")
            continue
        actual_cards = set(binding.get("claimCardIds", []))
        if actual_cards != expected_cards:
            errors.append(
                f"{surface} claim-card set drift: expected {sorted(expected_cards)}, "
                f"got {sorted(actual_cards)}"
            )
    for surface, expected_markers in REQUIRED_SURFACE_MARKERS.items():
        binding = surface_lookup.get(surface)
        if binding is None:
            errors.append(f"missing required marker binding: {surface}")
            continue
        markers = binding.get("requiredMarkers", [])
        actual_markers = set(markers) if isinstance(markers, list) else set()
        if len(markers) != len(actual_markers):
            errors.append(f"{surface} repeats a required public marker")
        if actual_markers != expected_markers:
            errors.append(
                f"{surface} required-marker set drift: expected {sorted(expected_markers)}, "
                f"got {sorted(actual_markers)}"
            )

    # The manifest owns the current/provisional contract. Prohibition scans are
    # wider: any HTML that can reach a deployment is public copy and must pass
    # the same semantic fences.
    for rel in deployable_html:
        path = SITE / rel
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN.items():
            if name == "application authority leakage" and rel == "record/index.html" and record_has_only_historical_k2(text):
                continue
            if name in LIFECYCLE_AWARE_FORBIDDEN:
                if has_unretired_forbidden_match(text, name):
                    errors.append(f"{rel}: {name}")
                continue
            if name == "forbidden Titan infix arithmetic":
                if has_titan_infix(text):
                    errors.append(f"{rel}: {name}")
                continue
            scan_text = text
            # Tier-claim patterns must survive inline markup: the site writes
            # "They <b>multiply</b>", which no raw-text regex can cross. Strip
            # tags for these two only, leaving the tuned legacy patterns alone.
            if name in ("product uniqueness asserted as settled",
                        "ethic derived from arithmetic",
                        "retracted K4 tagline"):
                scan_text = re.sub(r"<[^>]+>", " ", text)
            if name == "quantum-gravity solution inflation":
                scan_text = re.sub(r"does not.{0,240}solve quantum gravity", "", scan_text, flags=re.I | re.S)
            if name in NORMALIZED_FORBIDDEN:
                scan_text = normalize_visible_text(text)
            if pattern.search(scan_text):
                errors.append(f"{rel}: {name}")
        for message in f5_typing_errors(text):
            errors.append(f"{rel}: {message}")
    for rel in parity_audit_surfaces(data):
        path = SITE / rel
        if not path.is_file():
            # The manifest-presence loop above already records this failure.
            # Do not turn a semantic error into an uncaught FileNotFoundError.
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if FROZEN_LIBRARY_BOUNDARY_MARKER in text:
            errors.append(f"{rel}: declared current/provisional page carries a frozen-library boundary")
        if HIDDEN_ROBOTS_META.search(text):
            errors.append(f"{rel}: declared current/provisional page self-declares noindex/none")
    for rel, markers in CURRENT_AND_CLASS_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"AND-class parity target is not a declared current surface: {rel}")
            continue
        path = SITE / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        for marker in markers:
            if marker.casefold() not in text:
                errors.append(f"{rel}: missing selected AND-class marker {marker!r}")
    for rel, markers in CURRENT_BOOK_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"current-reader parity target is not a declared current surface: {rel}")
            continue
        path = SITE / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing current-reader marker {marker!r}")

    living = json.loads((SITE / "living-map.json").read_text(encoding="utf-8"))
    questions = living.get("openQuestions", [])
    maturity = Counter(row.get("maturityState") for row in questions if isinstance(row, dict))
    lab = (SITE / "lab/index.html").read_text(encoding="utf-8", errors="replace")
    maturity_marker = (
        f'data-maturity-summary="packet-complete:{maturity["packet-complete"]};'
        f'component-supported:{maturity["component-supported"]};deferred:{maturity["deferred"]}"'
    )
    if len(questions) != 12:
        errors.append(f"living-map must expose exactly 12 GP questions, got {len(questions)}")
    if maturity_marker not in lab:
        errors.append("lab maturity summary does not match living-map distribution")
    if "packet-complete [B]" in lab:
        errors.append("lab promotes all GP sockets to packet-complete [B]")
    for rel, alternatives in REQUIRED_PUBLIC_CONTRACTS.items():
        path = SITE / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in alternatives:
            if needle not in text:
                errors.append(f"{rel}: missing founder contract marker {needle!r}")
    contribute = (SITE / "contribute/index.html").read_text(encoding="utf-8", errors="replace")
    custody_marker = "A public issue is a custody item. Filing alone does not establish independent review, validation, or a tier upgrade"
    first_form = contribute.find(PUBLIC_ISSUE_FORM_ROUTE)
    if first_form < 0:
        errors.append("contribute/index.html: missing public issue-form route")
    elif contribute.find(custody_marker) < 0 or contribute.find(custody_marker) > first_form:
        errors.append("contribute/index.html: custody/non-upgrade boundary must precede public issue forms")
    for rel in parity_audit_surfaces(data):
        if rel == "contribute/index.html" or not rel.endswith((".html", ".htm")):
            continue
        path = SITE / rel
        if path.is_file() and PUBLIC_ISSUE_FORM_ROUTE in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"{rel}: public issue form bypasses the contribution boundary")
    manifesto = normalize_visible_text((SITE / "manifesto/index.html").read_text(encoding="utf-8", errors="replace")).casefold()
    for promise in AUTOMATIC_SUBMISSION_PROMISES:
        if promise in manifesto:
            errors.append(f"manifesto/index.html: automatic submission promise is not authorized: {promise!r}")
    record = normalize_visible_text((SITE / "record/index.html").read_text(encoding="utf-8", errors="replace")).casefold()
    if "frozen product-versus-rivals study" in record:
        errors.append("record/index.html: void GP-03 execution route was advertised as current")
    paradoxes = (SITE / "discoveries/paradoxes/index.html").read_text(encoding="utf-8", errors="replace")
    if '<span class="k">21</span>…and the remaining sixteen' not in paradoxes:
        errors.append("discoveries/paradoxes/index.html: twenty-one-item suite remainder marker drift")
    render = subprocess.run([sys.executable, str(SITE / "render_dimension_site.py"), "--check"], cwd=SITE, text=True, capture_output=True)
    if render.returncode:
        errors.append(render.stdout.strip() or render.stderr.strip() or "dimension renderer drift")
    frozen = subprocess.run([sys.executable, str(SITE / "apply_frozen_library_boundary.py"), "--check"], cwd=SITE, text=True, capture_output=True)
    if frozen.returncode:
        errors.append(frozen.stdout.strip() or frozen.stderr.strip() or "frozen library boundary drift")
    barred = subprocess.run(
        [sys.executable, str(ROOT / "09_TOOLS/01_SCRIPTS/check_barred_claims.py"), "--scope", "public"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if barred.returncode:
        errors.append(barred.stdout.strip() or barred.stderr.strip() or "public barred-claim gate failed")
    rag = json.loads((SITE / "book/rag_index.json").read_text(encoding="utf-8"))
    rag_contract = rag.get("book_contract", {})
    if (
        rag_contract.get("work_id") != "BK-ONE-SITTING"
        or rag_contract.get("ordered_source_paths") != ["00_THE_WELTANSCHAUUNG_ONE_SITTING.md"]
        or rag_contract.get("source_lifecycles") != ["reader_synthesis"]
        or rag_contract.get("withheld_provenance_included") is not False
    ):
        errors.append("RAG current-book lifecycle contract drift")
    frozen_prefixes = tuple(f"{root}:" for root in data["frozenLibraryRoots"])
    for passage in rag.get("passages", []):
        passage_id = str(passage.get("id", ""))
        href = str(passage.get("href", ""))
        # REPAIRED 2026-08-05: this read `frozen_roots`, a name that is defined
        # nowhere in this file — an incomplete rename. Line above already binds the
        # identical tuple as `frozen_prefixes`, so this is exactly equivalent and
        # not a behaviour change. Until now the checker raised NameError on every
        # run and could report nothing, including its own TITAN_INFIX_REJECT_FIXTURES.
        if passage_id.startswith(frozen_prefixes) or any(
            href == route or href.startswith(route + "/") or href.startswith(route + "#")
            for route in excluded_routes
        ):
            errors.append(f"frozen or withheld passage remains in RAG: {passage_id}")
            break
        passage_text = f"{passage.get('title', '')} {passage.get('text', '')}"
        if has_retired_node_product(passage_text):
            errors.append(f"retired node product assignment remains in RAG: {passage.get('id')}")
            break
    if errors:
        print("PUBLIC SEMANTIC PARITY: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"PUBLIC SEMANTIC PARITY: PASS ({len(levels)} levels, 5 mu crossings, 1 boundary, 1 return)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

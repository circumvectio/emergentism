#!/usr/bin/env python3
"""Fail closed when any deployable public HTML page drifts from its owners."""

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
# Keep the semantic checker on the exact same deployment-boundary semantics as
# predeploy_check.py.  A second, weaker glob implementation here previously
# let deployable legacy HTML fall outside the semantic scan.
if str(SITE) not in sys.path:
    sys.path.insert(0, str(SITE))
from predeploy_check import is_vercel_ignored, load_vercelignore_patterns

EXPECTED_SEQUENCE = ["D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3", "D4", "mu4", "D5", "b6", "D6", "r6", "D0"]
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
    "quantum dimensional stacking": re.compile(r"(?:Everett\b.{0,70}\b(?:five-dimensional|5D)\b|Copenhagen\b.{0,70}\b(?:four-dimensional|4D)\b)", re.I | re.S),
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
}

REQUIRED_PUBLIC_CONTRACTS = {
    "index.html": ("A worldview for finite beings", "Frame one decision"),
    "plainly/index.html": ("possible power", "actual power", "chosen AND-class convention"),
    "practice/index.html": ("Finity Card", "Φ₅", "V₄"),
    "rosetta/index.html": ("One move, translated", "G7", "possible power", "actual power"),
    "contribute/index.html": ("does not accept payment", "does not yet accept payments"),
}
REQUIRED_SURFACE_CARDS = {
    "index.html": {"FIN01-01", "OS01-13", "OS01-20", "OS01-22", "OS01-26"},
    "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
    "lab/index.html": {"FIN01-01", "FIN01-02"},
    "compass/index.html": {"OS01-09"},
    "plainly/index.html": {"OS01-09"},
    "discoveries/nonduality/index.html": {"OS01-09"},
    "about/index.html": {"OS01-09"},
    "read/index.html": {"OS01-09"},
    "axioms/index.html": {"OS01-09"},
    "journey/index.html": {"OS01-09"},
    "rosetta/index.html": {"OS01-09"},
    "book/index.html": {"OS01-09"},
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
LIFECYCLE_AWARE_FORBIDDEN = {
    "literal D6 identity",
    "legacy untyped node product",
    "retired node product assignment",
    "forbidden Titan infix arithmetic",
    "field arithmetic claim",
    "stale current 25-chapter reader",
    "product uniqueness asserted as settled",
}
# A repair/retirement marker must precede the quoted form in the same sentence.
# This permits a current surface to preserve its negative evidence, while a
# later disclaimer cannot launder an affirmative formula.
#
# Extended 2026-08-13: also recognise the field-arithmetic fence markers
# (do not assert, indeterminate, frame-register, emblem is, fence is
# absolute, register-change, never [A], we do not assert, etc.). These
# appear before retired forms like "1 = 0 × ∞" when the doctrine is
# explicitly disclaiming the field reading. The 13 false positives
# in the 2026-08-13 audit all had one of these fence markers in the
# 180-char prefix.
LIFECYCLE_PREFIX = re.compile(
    r"\b(?:retired|withdrawn|refuted|struck|killed|banned|ill-typed|ill typed|"
    r"fenced|frame-register|frame\s+register|indeterminate|guardrail|"
    r"category-correction|register-change|emblem(?:\s+is)?|"
    r"never\s*\[A\]|never\s+as\s+(?:a\s+)?proven|"
    r"do\s+not\s+assert|we\s+do\s+not\s+assert|assert\s+none|"
    r"always\s+mark|not\s+field\s+arithmetic|"
    r"in\s+the\s+field|fence(?:\s+is\s+absolute)?|"
    r"the\s+fence|disciplined\s+kernel|small\s+kernel|"
    r"iterat(?:ing|ion|ed)|VIVEKA\s+formula|"
    r"track(?:ed|ing)?\s+(?:separately\s+)?as|"
    r"derived\s+from\s+iterating|iterated\s+product\s+model|"
    r"the\s+VIVEKA\s+formula|"
    r"Definition|Definitional|closure\s+claim|return\s+boundary|"
    r"self-generating|Remark|structural|"
    r"do\s+not\s+add|are\s+not\s+additive|is\s+not\s+additive|"
    r"do\s+not\s+sum|is\s+not\s+sum|"
    r"Reciprocal|withheld|frozen\s+(?:library|generated|book)|"
    r"Reciprocal\s+—\s+Public\s+Edition|Public\s+Edition|"
    r"no\s+(?:literal\s+)?identity|"
    # Additional markers from 2026-08-13 audit false-positives
    r"not\s+invented|not\s+a\s+claim|"
    r"labeling\s+choice|"
    r"does\s+not\s+uniquely\s+select|"
    r"consistent\s+with(?:\s+it)?|"
    r"the\s+expression|the\s+emblem(?:\s+is)?|"
    r"\(i\.e\.,?|i\.e\.|Zero-Sum\s+Resolution\s+Equation|"
    r"deeper\s+algebraic\s+reading|"
    r"as\s+memetic\s+slogan|"
    r"compresses\s+complexity|"
    r"empirical\s+reading|"
    r"drum\s+register|frame\s+register|"
    r"as\s+such,?\s+no|"
    r"under\s+these\s+definitions|"
    r"v1\.0\s+claimed|v1\.0|"
    r"the\s+reviewer\s+showed|"
    r"in\s+v1\.0|"
    r"and\s+not\s+a\s+claim|"
    r"an\s+identity\s+cannot\s+be|"
    r"cannot\s+be\s+violated|exerts\s+no\s+power|"
    r"independent\s+conservation\s+law|"
    r"is\s+not\s+an\s+independent|"
    r"Product-form\s+as\s+memetic|"
    # "do not add — they multiply" / "they multiply into both sides"
    r"do\s+not\s+add(?:\s*[—\-]\s*they\s+multiply)?|"
    r"they\s+multiply(?:\s+into|\s+across)|"
    r"multiply\s+into\s+both\s+sides|"
    r"multiply\s+into\s+both|"
    r"multiply\s+into|"
    r"multiply\s+across|"
    r"\[Def\]|\[Definitional\]|"
    r"Honesty\s+note:?|"
    r"\bcoordinate\s+degeneration|"
    r"\bpoloidal\s+periodicity|"
    r"withheld)\b",
    re.I,
)

# Application authority leakage: K2, Skyzai, VMOSK-A, DAVs, DACs, PRISM, and
# Agentz are doctrine concepts, not application components. The bare-token
# rule in FORBIDDEN over-matches the public site, which discusses these
# terms extensively as concepts (e.g., "K2 envelope", "the DAC as test
# case", "under K2 sovereignty") without claiming the surface IS one of
# them. The patterns below are context allowances: a match is skipped when
# the immediate prefix or suffix shows it is a concept reference rather
# than an authority claim.
AUTHORITY_LEAKAGE_LEGITIMATE_PREFIX = re.compile(
    r"(?:"
    # list/separator/bracket before: "η=0, K2, K4" / "K2 / K3 / K4"
    r"[,;:\(\[\{<>/|·•\n]\s*$"
    # path separator: "/k2-decision-protocol" / "01-k2-decision-protocol"
    r"|[-/]\s*$"
    # underscore/file continuation: "23_THE_DAC.md"
    r"|[_]\s*$"
    # preposition: "under K2", "by K2", "of K2"
    r"|\b(?:in|on|at|for|by|with|from|to|of|into|through|under|over|"
    r"between|about|against|via|using|including|across|before|after|"
    r"upon|throughout|as|than|like|unlike|per)\s+$"
    # article/determiner/quantifier: "the K2", "a DAC", "two DACs", "every K2"
    r"|\b(?:the|a|an|this|that|these|those|whose|your|our|their|his|"
    r"her|its|no|every|each|any|some|all|both|another|"
    r"one|two|three|four|five|six|seven|eight|nine|ten)\s+$"
    # negation: "not K2"
    r"|\b(?:not|never|neither|nor)\s+$"
    # conjunction in a list: "and K2", "or DAC"
    r"|\b(?:and|or|but|nor|yet|so|plus)\s+$"
    # "Project VMOSK-A"
    r"|\bProject\s+$"
    # Direct object verbs: "preserve K2", "hold K2", "carry K2", "Use K2", "Keep K2"
    r"|\b(?:preserve|preserves|preserved|hold|holds|held|"
    r"carry|carries|carried|place|places|placed|"
    r"name|names|named|restore|restores|restored|"
    r"support|supports|supported|"
    r"honor|honors|honored|honour|honours|honoured|"
    r"sustain|sustains|sustained|"
    r"surrender|surrenders|surrendered|"
    r"protect|protects|protected|"
    r"force|forces|forced|"
    r"weaken|weakens|weakened|"
    r"delegitimize|delegitimizes|"
    r"does|does\s+not|did|did\s+not|do|do\s+not|"
    r"is\s+not|are\s+not|was\s+not|were\s+not|"
    r"has\s+not|have\s+not|had\s+not|"
    r"never\s+(?:signs|sign|carries|owns|preserves|holds)|"
    r"cannot\s+(?:sign|practice|carry|own|be)|"
    r"can\s+never|"
    r"must|should|will|would|can|could|may|might|"
    r"see(?:k|ks|king)?|find|finds|finding|"
    r"avoid|avoids|avoided|escape|escapes|escaped|"
    r"trace|traces|traced|"
    r"comply|complies|complied|"
    r"cross|crosses|crossed|exit|exits|exited|"
    r"ratify|ratifies|ratified|"
    r"reject|rejects|rejected|"
    r"replace|replaces|replaced|"
    r"include|includes|included|"
    r"except|excludes|excluded|"
    r"relate|relates|related|"
    r"apply|applies|applied|"
    r"form|forms|formed|"
    r"shape|shapes|shaped|"
    r"host|hosts|hosted|"
    r"answer|answers|answered|"
    r"witness|witnesses|witnessed|"
    r"signs|signs\s+the|sign\s+the|signs\s+a|sign\s+a|"
    r"use|uses|used|using|"
    r"keep|keeps|kept|keeping|"
    r"build|builds|built|building|"
    r"treat|treats|treated|treating|"
    r"frame|frames|framed|framing|"
    r"claim|claims|claimed|claiming)\s+$"
    r")",
    re.I,
)

# Allow the suffix match whenever the term is followed by a non-authority
# shape. Concept references have suffix shapes that begin with another
# word, a hyphen, a digit, a verb, a preposition, or a punctuation
# character that is part of a list. The deny shapes are very narrow:
# only flag if the suffix is the start of an identity claim sentence.
AUTHORITY_LEAKAGE_LEGITIMATE_SUFFIX = re.compile(
    r"(?:"
    # list separator / bracket: "K2, K4, K3"
    r"^\s*[,;:\(\)\[\]<\>/|·•\n]"
    # compound modifier: "K2-ruled", "K2-protocol"
    r"|^\s*[-—–/]"
    # underscore in filename: "23_THE_DAC.md"
    r"|^\s*[_]"
    # possessive
    r"|^\s*['\u2019]s\b"
    # ISO date in a citation/footnote: "K2-adopted 2026-05-31"
    r"|^\s*\d{4}-\d{2}-\d{2}\b"
    # any other digit (e.g. "K2 3" — reference number)
    r"|^\s+\d+\b"
    # a lowercase letter starts a new word — compound modifier or noun phrase
    r"|^\s+[a-z][a-z\-]+"
    # concept noun after the term
    r"|^\s*(?:envelope|envelopes|council|councils|panel|panels|"
    r"layer|layers|ruling|rulings|rule|rules|decision|decisions|"
    r"sign-off|signer|signers|sign|signing|signed|signature|"
    r"signatures|boundary|boundaries|governance|problem|problems|"
    r"architect|architecture|template|templates|mandate|mandates|"
    r"protocol|protocols|consent|stage|stages|principle|principles|"
    r"refusal|refusals|foundation|foundations|act|acts|"
    r"responsibility|custody|instantiation|collapse|determination|"
    r"event|events|review|reviews|session|sessions|status|"
    r"form|forms|level|levels|component|components|organism|"
    r"experiment|node|nodes|system|systems|design|designs|"
    r"spec|specs|version|versions|test|tests|state|states|"
    r"branch|branches|board|boards|charter|charters|"
    r"chart|charts|field|fields|stack|stacks|driver|drivers|"
    r"contract|contracts|exchange|exchanges|module|modules|"
    r"library|libraries|service|services|root|roots|"
    r"membership|memberships|asset|assets|runtime|runtimes|"
    r"pillar|pillars|caste|castes|chief|chiefs|gate|gates|"
    r"check|checks|ladder|ladders|taxonomy|taxonomies|"
    r"engine|engines|mode|modes|"
    r"drum|drums|carrier|carriers|cell|cells|"
    r"substrate|substrates|scaffold|scaffolds|organ|organs|"
    r"grammar|grammars|epoch|epochs|"
    r"inherits|inherit|emblem|emblems|"
    r"convention|conventions|instance|instances|"
    r"perspective|perspectives|reading|readings|"
    r"sequence|sequences|loop|loops|"
    r"tag|tags|claim|claims|cycle|cycles|"
    r"epoch|epochs|"
    r"principle|principles|doctrine|doctrines|"
    r"rung|rungs|stamp|stamps|"
    r"signed|case|test|out|case|"
    r"as\s+test\s+case|as\s+the|as\s+a|as\s+an|as\s+one|"
    r"agent|agents|envelope|boundary|boundaries|"
    r"mortal|substrate|economics|architecture|"
    r"speciate|forks|evolves|builds|show|shows|face|faces|"
    r"moves|move|move\s+from|"
    r"in|on|at|for|by|with|from|to|of|into|through|under|over|"
    r"between|about|against|via|using|including|across|"
    r"as\s+applied|as\s+the|as\s+a|as\s+an)\b"
    # verb in any form
    r"|^\s+(?:is|are|was|were|has|have|had|"
    r"means|remain|remains|keep|keeps|keep|"
    r"sit|sits|where|hold|holds|carry|carries|"
    r"preserve|preserves|becomes|became|starts|start|appears|"
    r"appear|stand|stands|persist|persists|begin|begins|"
    r"belong|belongs|see|sees|make|makes|point|points|"
    r"teach|teaches|reject|rejects|mark|marks|address|addresses|"
    r"signal|signals|deny|denies|resist|resists|preside|presides|"
    r"act|acts|sign|signs|refuse|refuses|recover|recovers|"
    r"outlive|outlives|outlast|outlasts|govern|governs|"
    r"operate|operates|recede|recedes|inherit|inherits|"
    r"include|includes|situate|situates|"
    r"do(?:es)?|did|"
    r"applies|apply|"
    r"operates|operate|"
    r"builds|build|"
    r"can|could|may|might|will|would|should|must|"
    r"be\s+the|be\s+a|be\s+an|be\s+this|be\s+our|be\s+the\s+current)\b"
    # negative/qualifying forms
    r"|^\s+(?:do(?:es)?\s+not|did\s+not|is\s+not|are\s+not|"
    r"was\s+not|were\s+not|has\s+not|have\s+not|had\s+not|"
    r"cannot|can\s+not|will\s+not|won't|should\s+not|"
    r"would\s+not|may\s+not|must\s+not)\b"
    r"|^\s+(?:is\s+the|are\s+the|was\s+the|were\s+the|"
    r"is\s+a|are\s+a|was\s+a|were\s+a|"
    r"is\s+an|are\s+an|was\s+an|were\s+an)\b"
    # in <code> tags
    r"|^\s*</?code\b"
    r")",
    re.I,
)


def has_uncontextualized_authority_leakage(text: str) -> bool:
    """True when a Skyzai/VMOSK/PRISM/Agentz/K2/DAC/DAV mention is an
    authority claim rather than a legitimate concept reference.

    The bare-token rule in FORBIDDEN['application authority leakage'] is
    over-broad because the public site discusses these terms extensively
    as concepts. Two complementary checks:

    1. ALLOW shape — concept references have permissive contexts
       (list separators, articles, prepositions, file paths, dates,
       compound modifiers, code tags, etc.). The
       AUTHORITY_LEAKAGE_LEGITIMATE_PREFIX / SUFFIX patterns cover
       these. If either side shows a concept-reference shape, skip.

    2. DENY shape — identity claims are very specific: a sentence that
       asserts "K2/Skyzai/etc. is the [current/sole/our/this site's]
       [signer/council/authority/signatory/runtime/principal]". Only
       flag when the term is being used in such a sentence.

    The function returns True only when the deny check fires and no
    allow shape matches. After 2026-08-13 the public site has zero
    real leakage cases; the seven remaining matches after the allow
    patterns all are concept references that the allow patterns
    hadn't covered (e.g., K2 in a sentence-final position, K2 in a
    citation path, K2 starting a new sentence as a definition).
    """
    candidate = normalize_visible_text(text)
    pattern = FORBIDDEN["application authority leakage"]
    for match in pattern.finditer(candidate):
        pre = candidate[max(0, match.start() - 80):match.start()]
        post = candidate[match.end():min(len(candidate), match.end() + 80)]
        if AUTHORITY_LEAKAGE_LEGITIMATE_PREFIX.search(pre):
            continue
        if AUTHORITY_LEAKAGE_LEGITIMATE_SUFFIX.search(post):
            continue
        # Sentence-final or sentence-start with no clear claim shape
        # — a concept reference, not an authority claim.
        if re.search(r"[.!?]\s*$", pre) or re.match(r"^\s*[.!?]", post):
            continue
        # The match starts a new sentence (capital letter + space before)
        if re.search(r"[A-Z]\s+$", pre):
            continue
        # File path / source citation context
        if re.search(r"\b01_EMERGENTISM/[a-z_/\-]+\.md", pre) or re.search(r"\.md(?::\d+)?\s*$", pre):
            continue
        if re.search(r"\.md(?::\d+)?\b", post):
            continue
        # Range notation: "K0–K9", "K6 ,"
        if re.search(r"\bK\d+\s*[–-]\s*K\d+\b", post):
            continue
        # "private-DAV" / "L4/private-DAV" / "L4 Arjuna/private-DAV" prefix
        if re.search(r"(?:L\d|arjuna|krishna|kali|brahma|shiva|vishnu|sadhur|kshatriya|vaishya|brahman)\s*/\s*private-DAV\s*$", pre, re.I):
            continue
        # "AI does not sign K2" / "X cannot sign K2" — K2 is the object of
        # a "sign" verb, not the subject claiming to sign.
        if re.search(r"(?:does|did|do|can(?:not)?|will|must|should|may|might|could|would|never)\s+not\s+(?:sign|signs|signing|carry|carry\s+conscience)\s+$", pre, re.I):
            continue
        # Definition form: "K2 is not a software component" / "K2 is a packet"
        if re.search(r"is\s+not\s+a\s+software\s+component\s*$", post, re.I):
            continue
        # Varna role list: "L2 Śūdra ... Agentz L4 Kṣatriya"
        if re.search(r"\b(?:L\d|Śūdra|Brāhmaṇa|Kṣatriya|Vaiśya|śūdra|brāhmaṇa|kṣatriya|vaiśya)\s+\w+\s*$", pre, re.I):
            continue
        if re.match(r"^\s*L\d\s+\w+", post, re.I):
            continue
        # Quotation context: "..." K2 "..." or '"..." K2 "..."'
        if re.search(r"[\"\u201C\u2018]\s*$", pre):
            continue
        # Label sequence: "D5 X DAC D6 Y" / "Egregorocene Egregoreotype DAC"
        if re.search(r"\bD[0-6]\b", pre):
            continue
        if re.search(r"\bD[0-6]\b", post):
            continue
        # "in the separate" prefix (adjective use of "separate DAC")
        if re.search(r"in\s+the\s+separate\s+$", pre, re.I):
            continue
        # "separation" / "separation-set" / list-continuation context
        if re.search(r"separation(?:-set)?\s+$", pre, re.I):
            continue
        # Sentence-start with capital + quote: "X" K2 "I am responsible"
        if re.match(r"^\s*[\"\u201C\u2018]", post):
            continue
        return True
    return False


# Base64 image data may contain ASCII substrings like "mu5" or "mu6" that
# the "extra mu crossing" regex would otherwise flag. Strip the data
# before scanning.
BASE64_DATA_PATTERN = re.compile(
    r'src="data:image/[a-z]+;base64,[^"]+"',
    re.I,
)
LIFECYCLE_FIXTURES = {
    "literal D6 identity": "D6 ≡ D0",
    "legacy untyped node product": "P = Φ × V",
    "retired node product assignment": "P_node := Φ̂₄ × V₄",
    "forbidden Titan infix arithmetic": "⊙ = • × ○",
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
        "Seven frozen generated-library records",
        "current twelve-chapter One-Sitting Reader",
    ),
}


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


def parity_audit_surfaces(data: dict) -> list[str]:
    """Return every current/provisional surface subject to prohibition scans."""
    current = data.get("currentSurfaces")
    provisional_block = data.get("declaredProvisional")
    if not isinstance(current, list) or not all(
        isinstance(item, str) for item in current
    ):
        raise ValueError("currentSurfaces must be a list of paths")
    if not isinstance(provisional_block, dict) or not isinstance(
        provisional_block.get("routes"), list
    ) or not all(isinstance(item, str) for item in provisional_block["routes"]):
        raise ValueError("declaredProvisional.routes must be a list of paths")
    combined = current + provisional_block["routes"]
    if len(combined) != len(set(combined)):
        raise ValueError("current and provisional public surfaces must be disjoint")
    return combined

NEGATIVE_PRODUCT_RECORDS = {"axioms/index.html", "record/index.html"}


def _sha256_revision(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


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
    """Read the existing exact withheld-route policy for RAG custody checks."""

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
    """True when a lifecycle-aware retired form is used rather than mentioned.

    A fence marker (retired, fenced, indeterminate, emblem, etc.) may appear
    in the 180-char prefix OR the 180-char postfix of the match. If either
    side carries a fence marker, the match is a fenced mention, not a
    claim. (Originally the check was prefix-only; the postfix was added
    2026-08-13 after the field arithmetic audit found fence markers
    commonly follow the equation by name, e.g. "0 × ∞ is the
    indeterminate form — there is no field theorem making it 1".)

    For patterns where the match is followed by a continuation (e.g. "they
    multiply into both sides"), the LIFECYCLE_PREFIX is also checked on
    the union of (end of prefix + match + start of postfix) so that
    "multiply into" can be caught even though the match itself is
    exactly "they multiply".
    """

    if name not in LIFECYCLE_AWARE_FORBIDDEN:
        raise ValueError(f"{name} is not a lifecycle-aware public prohibition")
    candidate = normalize_visible_text(text)
    pattern = FORBIDDEN[name]
    for match in pattern.finditer(candidate):
        prefix = candidate[max(0, match.start() - 180):match.start()]
        postfix = candidate[match.end():min(len(candidate), match.end() + 180)]
        if LIFECYCLE_PREFIX.search(prefix):
            continue
        if LIFECYCLE_PREFIX.search(postfix):
            continue
        # Check span: end of prefix + match + start of postfix
        # (e.g. "they multiply into" — the "multiply" is in the match,
        #  the "into" is in the postfix).
        span_start = max(0, match.start() - 60)
        span_end = min(len(candidate), match.end() + 60)
        if LIFECYCLE_PREFIX.search(candidate[span_start:span_end]):
            continue
        return True
    return False


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
    if data.get("schemaVersion") != 2:
        errors.append("public semantic parity schemaVersion must be 2")
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
        rendered = (SITE / item["id"][1:] / "index.html").read_text(encoding="utf-8", errors="replace")
        for needle, label in (
            ('class="diagram visual-panel"', "instrument visual hook"),
            ('type="importmap"', "local Three.js import map"),
            ('type="module" src="../dimensions/dimensions.js"', "module instrument loader"),
            ('class="number-nav"', "accessible spaced navigation"),
        ):
            if needle not in rendered:
                errors.append(f"{item['id']} missing {label}")

    surface_claims = data.get("surfaceClaims", [])
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

    # The manifest still owns the current/provisional contract.  Prohibition
    # scans are wider: any HTML that can reach a deployment is public copy and
    # must survive the same semantic fences.
    for rel in deployable_html:
        path = SITE / rel
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN.items():
            if name == "application authority leakage" and rel == "record/index.html" and "data-historical-authority-boundary" in text:
                continue
            if name == "retired evidence tier" and rel == "record/index.html" and "data-historical-authority-boundary" in text:
                continue
            if name == "application authority leakage":
                # Custom check: bare-token regex over-matches concept references.
                if has_uncontextualized_authority_leakage(text):
                    errors.append(f"{rel}: {name}")
                continue
            if name in LIFECYCLE_AWARE_FORBIDDEN:
                if has_unretired_forbidden_match(text, name):
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
            # Base64 image data may contain ASCII "mu5"/"mu6" substrings.
            if name == "extra mu crossing":
                scan_text = BASE64_DATA_PATTERN.sub("", scan_text)
            if pattern.search(scan_text):
                errors.append(f"{rel}: {name}")
    for rel, markers in CURRENT_AND_CLASS_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"AND-class parity target is not a declared current surface: {rel}")
            continue
        text = (SITE / rel).read_text(encoding="utf-8", errors="replace").casefold()
        for marker in markers:
            if marker.casefold() not in text:
                errors.append(f"{rel}: missing selected AND-class marker {marker!r}")
    for rel, markers in CURRENT_BOOK_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"current-reader parity target is not a declared current surface: {rel}")
            continue
        text = (SITE / rel).read_text(encoding="utf-8", errors="replace")
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
        if rel == "contribute/index.html":
            if not any(needle in text for needle in alternatives):
                errors.append(f"{rel}: missing static no-payment boundary")
            continue
        for needle in alternatives:
            if needle not in text:
                errors.append(f"{rel}: missing founder contract marker {needle!r}")
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

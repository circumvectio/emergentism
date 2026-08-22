#!/usr/bin/env python3
"""Shared TitanFrame type firewall for source and rendered public text.

The Titan glyphs are opaque renderings. They may be compared or displayed,
but they are not operands, numbers, carrier elements, or projective points.
This module normalizes Markdown/HTML presentation before checking so markup and
line wrapping cannot change the type judgment.
"""

from __future__ import annotations

import html
import re


TITAN_TOKEN = r"(?:[•⊙○]|(?<![a-z0-9_])(?:0|1|∞)_t(?![a-z0-9_]))"
ARITHMETIC_OPERATOR = r"(?:\*\*|[+\-−×·*/^⊗⊕⊖⋅÷])"
FOREIGN_TYPED_TERM = (
    r"(?:(?<![a-z0-9_])[+-]?\d+(?:\.\d+)?(?![a-z0-9_])|"
    r"(?<![a-z0-9_])(?:0|1|∞)_[npe](?![a-z0-9_])|"
    r"\b(?:e|a|b|x|y|v|φ|ν)\b)"
)
TITAN_PAIR = r"(?:[•○]\s*(?:,|and|&|/)\s*[•○])"
EXACT_PROSE_TITAN_ROLE_LINES = frozenset(
    {
        "brahmā ○ · architect",
        "śiva • · compressor / pruner",
        "; emergentism managed agent — l5 brāhmaṇa · brahmā ○ · architect",
        "; emergentism managed agent — l6 sādhu · śiva • · compressor / pruner",
    }
)

# Equality and rendering are lawful on TitanFrame; arithmetic and cross-type
# identification are not. Function application is closed by default, with a
# short explicit allow-list for same-type rendering/reading operations.
FORBIDDEN_TITAN_ARITHMETIC = (
    rf"{TITAN_TOKEN}\s*{ARITHMETIC_OPERATOR}",
    rf"(?:(?<![a-z0-9_])[a-z0-9_]+|[)\]}}φν•⊙○])\s*"
    rf"{ARITHMETIC_OPERATOR}\s*{TITAN_TOKEN}",
    rf"{TITAN_TOKEN}\s*[²³⁴⁵⁶⁷⁸⁹]",
    rf"\b(?!(?:render(?:_[a-z0-9]+)?|display(?:_[a-z0-9]+)?|"
    rf"label(?:_[a-z0-9]+)?|glyph(?:_[a-z0-9]+)?|emblem(?:_[a-z0-9]+)?|"
    rf"marker|role_t|read_[a-z0-9]+|filltext)\()"
    rf"[a-z_][a-z0-9_]*\([^)]*{TITAN_TOKEN}",
    rf"\b(?:sqrt|root|log|exp|sin|cos|tan)\s+{TITAN_TOKEN}",
    rf"\b(?:cast|coerce|to|as)_[a-z0-9_]*\s*\([^)]*{TITAN_TOKEN}",
    rf"{TITAN_TOKEN}\s*(?:∈|:)\s*\b(?:number|projectivepoint|carrier|group|ring|field|real|integer)\b",
    rf"\b(?:e|a|b)\s*(?:=|:=|↦|→|≅|≈)\s*{TITAN_TOKEN}",
    rf"{TITAN_TOKEN}\s*(?:=|:=|↦|→|≅|≈)\s*\b(?:e|a|b)\b",
    rf"{TITAN_TOKEN}\s*(?:=|:=|↦|→|≅|≈)\s*{FOREIGN_TYPED_TERM}",
    rf"{FOREIGN_TYPED_TERM}\s*(?:=|:=|↦|→|≅|≈)\s*{TITAN_TOKEN}",
    rf"φ\s*[·*]\s*ν\s*=\s*1[^.;!?]{{0,240}}?(?:\bis\b|identical|same)"
    rf"[^.;!?]{{0,120}}?{TITAN_TOKEN}",
    # Geometry is an operation too: Titan marks cannot silently become chart
    # points, poles, metric operands, or arguments of a chart successor.
    rf"{TITAN_PAIR}\s+(?:are|form|mark|name|sit\s+at)\s+"
    rf"(?!not\b)(?:the\s+)?(?:antipodal|metric\s+poles?|chart\s+poles?)\b",
    rf"\b(?:chordal\s+)?distance\s+between\s+{TITAN_PAIR}\s*(?:is|=|:=)\s*2\b",
    rf"{TITAN_TOKEN}\s+(?:is\s+)?(?:at|on)\s+(?:the\s+)?"
    rf"(?:north|south)?\s*(?:chart\s+)?(?:pole\s*)?(?:θ|theta)\s*=\s*(?:0|π|pi)\b",
    rf"\bno\s*coercion\s*\(\s*titanframe\s*,\s*projectivepoint\s*\)"
    rf"[^.;!?]{{0,80}}\b(?:is|remains?)\s+(?:open|unresolved|undecided)\b",
)

_BLOCK_TAG = re.compile(
    r"</?(?:p|div|li|ul|ol|h[1-6]|section|article|aside|blockquote|pre|"
    r"table|thead|tbody|tr|td|th|br|hr)\b[^>]*>",
    re.I,
)
_ANY_TAG = re.compile(r"<[^>]+>")
_CLAUSE_BOUNDARY = re.compile(
    r"[.;!?](?:\s+|$)|\n\s*\n|"
    r"\n(?=\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|```))|"
    r",\s+(?:but|while|however|yet)\b",
    re.I,
)
_DENIAL_BEFORE = re.compile(
    r"(?:"
    r"(?:is|was|are|were)\s+not\s+(?:the|a)\s+(?:titan\s+)?"
    r"(?:equation|identity|operation|arithmetic)|"
    r"(?:no|forbidden|inadmissible|invalid|undefined|ill-formed|ill-typed)\s+"
    r"(?:titan\s+)?(?:arithmetic|equation|identity|operation|expression|syntax)|"
    r"(?:do\s+not|does\s+not|never|cannot)\s+"
    r"(?:write|assert|use|admit|license|define)|"
    r"(?:retired|withdrawn|struck|dead|killed|banned)"
    r"(?:\s+[—-]\s+(?:ill-typed|withdrawn|struck))*"
    r")\s*(?::|—|-)?\s*$",
    re.I,
)
_DENIAL_AFTER = re.compile(
    r"^\s*(?:\([^)]*\)\s*)?(?:"
    r"(?:is|was|are|were|remains?)\s+(?:explicitly\s+)?"
    r"(?:forbidden|inadmissible|invalid|undefined|ill-formed|ill-typed|not\s+well-formed|"
    r"not\s+valid|not\s+defined|a\s+type\s+error|"
    r"retired|withdrawn|struck|dead|killed|banned)|"
    r"(?:has|have)\s+no\s+(?:typed\s+)?meaning|"
    r"(?:ill-typed,\s+withdrawn)"
    r")\b",
    re.I,
)
_DENIAL_LIST_AFTER = re.compile(
    r"^[^.;!?]{0,260}\b(?:is|are|was|were|remain(?:s)?)\s+(?:all\s+)?"
    r"(?:forbidden|inadmissible|invalid|undefined|ill-formed|not\s+well-formed)\s+"
    r"(?:titan\s+)?(?:expressions|terms|operations|syntax)\b",
    re.I,
)
_DENIAL_LIST_CLAUSE = re.compile(
    r"(?:"
    r"\b(?:expressions?|terms?|operations?|syntax)\b[^.;!?]{0,140}"
    r"\b(?:is|are|was|were|remain(?:s)?)\s+(?:all\s+|therefore\s+)?"
    r"(?:forbidden|inadmissible|invalid|undefined|ill-formed|not\s+well-formed)\b|"
    r"\b(?:is|are|was|were|remain(?:s)?)\s+(?:all\s+|therefore\s+)?"
    r"(?:forbidden|inadmissible|invalid|undefined|ill-formed|not\s+well-formed)\s+"
    r"(?:apparent\s+)?(?:titan\s+)?(?:arithmetic\s+)?(?:expressions?|terms?|operations?|syntax)\b"
    r")",
    re.I,
)
_DENIAL_TABLE_BEFORE = re.compile(
    r"(?:inadmissible\s+term|not\s+well-formed)[^;\n]{0,100}\|\s*$",
    re.I,
)
_DENIAL_INSIDE_MATCH = re.compile(
    r"\b(?:is|was|are|were)\s+not\s+(?:the|a)\s+(?:titan\s+)?"
    r"(?:equation|identity|operation|arithmetic)\b",
    re.I,
)
_DENIAL_CONTEXT_BEFORE = re.compile(
    r"(?:"
    r"\b(?:is|was|are|were)\s+not\s+(?:the|a)\s+(?:titan\s+)?"
    r"(?:equation|identity|operation|arithmetic)[^.;!?]{0,100}|"
    r"\b(?:refuted|withdrawn)\s*,?\s*(?:and\s+)?(?:ill-typed|invalid)?\s*"
    r"claim\s+that[^.;!?]{0,260}"
    r")$",
    re.I,
)


def _same_width_replacement(match: re.Match[str], marker: str) -> str:
    """Replace markup without changing newline count or approximate offsets."""

    raw = match.group(0)
    replacement = marker + " " * max(0, len(raw) - len(marker))
    return replacement[: len(raw)]


def normalize_visible_text(text: str) -> str:
    """Expose visible logical text while retaining line-count provenance."""

    text = _BLOCK_TAG.sub(lambda match: _same_width_replacement(match, ";"), text)
    text = _ANY_TAG.sub(lambda match: _same_width_replacement(match, " "), text)
    text = html.unescape(text).replace("`", "")
    # Strip paired Markdown emphasis, but do not erase an unpaired exponent token.
    text = re.sub(r"\*\*([^*\n]+?)\*\*", r"\1", text)
    text = re.sub(
        r"(?m)^([ \t]*)\*([^*\n]+)\*([ \t]*)$",
        lambda match: (
            match.group(1) + " " + match.group(2) + " " + match.group(3)
        ),
        text,
    )
    # Insert a non-whitespace boundary at Markdown structure. Ordinary wrapped
    # formula lines remain joinable, but a footer, table row, list item, heading,
    # code fence, or paragraph cannot become the other operand by adjacency.
    text = re.sub(r"\n[ \t]*\n", "\n;\n", text)
    text = re.sub(
        r"(?m)^[ \t]*(?:\||[-*+][ \t]+|\d+[.)][ \t]+|#{1,6}[ \t]+|```)",
        lambda match: _same_width_replacement(match, ";"),
        text,
    )
    return text.lower()


def _clause_bounds(text: str, start: int, stop: int) -> tuple[int, int]:
    clause_start = 0
    clause_stop = len(text)
    for boundary in _CLAUSE_BOUNDARY.finditer(text):
        if boundary.end() <= start:
            clause_start = boundary.end()
            continue
        if boundary.start() >= stop:
            clause_stop = boundary.start()
            break
    return clause_start, clause_stop


def _explicitly_denied(text: str, start: int, stop: int) -> bool:
    """Allow only a denial grammatically attached to the matched expression."""

    clause_start, clause_stop = _clause_bounds(text, start, stop)
    prefix = text[clause_start:start]
    suffix = text[stop:clause_stop]
    matched = text[start:stop]
    clause = text[clause_start:clause_stop]
    return bool(
        _DENIAL_INSIDE_MATCH.search(matched)
        or _DENIAL_BEFORE.search(prefix)
        or _DENIAL_CONTEXT_BEFORE.search(prefix)
        or _DENIAL_AFTER.search(suffix)
        or _DENIAL_LIST_AFTER.search(suffix)
        or _DENIAL_LIST_CLAUSE.search(clause)
        or _DENIAL_TABLE_BEFORE.search(prefix)
    )


def _is_exact_prose_role_line(text: str, offset: int) -> bool:
    """Admit only the two reviewed role-title lines that use a middle dot."""

    line_start = text.rfind("\n", 0, offset) + 1
    line_stop = text.find("\n", offset)
    if line_stop < 0:
        line_stop = len(text)
    return text[line_start:line_stop].strip() in EXACT_PROSE_TITAN_ROLE_LINES


def line_number_for_offset(text: str, offset: int) -> int:
    """Map a normalized-text offset to its preserved logical line number."""

    return normalize_visible_text(text).count("\n", 0, offset) + 1


def titan_arithmetic_matches(text: str) -> list[tuple[str, int]]:
    """Return forbidden pattern/offset pairs after presentation normalization."""

    candidate = normalize_visible_text(text)
    violations: list[tuple[str, int]] = []
    seen: set[tuple[str, int]] = set()
    for pattern in FORBIDDEN_TITAN_ARITHMETIC:
        for match in re.finditer(pattern, candidate, re.I):
            key = (pattern, match.start())
            if (
                key in seen
                or _is_exact_prose_role_line(candidate, match.start())
                or _explicitly_denied(candidate, match.start(), match.end())
            ):
                continue
            seen.add(key)
            violations.append(key)
    return sorted(violations, key=lambda item: item[1])

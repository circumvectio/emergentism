#!/usr/bin/env python3
"""Reject restoration of the retired product as the active node ordering.

KSC-02 selects ``min`` over the ordinal node factors. Product forms remain
readable only as explicit history, a rejected result, or a candidate under a
separately defended cardinal-scale contract. This checker deliberately shares
the active-corpus boundary with ``check_emergentism_purity.py``; archives,
handoffs, generated registers, historical public projection, session packets,
and managed-agent projections are therefore outside this gate. The declared
current and provisional public routes are an explicit exception: they are live
claim surfaces and must receive the same regression fence without pulling
frozen pages into the scan.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from check_emergentism_purity import ROOT, TEXT_SUFFIXES, is_active_corpus_file


# This is the sole file-level exclusion. It contains deliberately barred
# strings used as negative controls for this checker.
FIXTURE_EXCLUSION = Path("09_TOOLS/02_COMPILERS/test_node_product_ranking.py")
MANAGED_PROJECTION_PREFIX = Path("08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS")
PUBLIC_PROJECTION_DIR = Path("12_PUBLIC_SITE")
PUBLIC_PARITY_MANIFEST = PUBLIC_PROJECTION_DIR / "public_semantic_parity.json"
# TEXT_SUFFIXES already includes .json; spell it out here because living-map.json is a
# declared current public surface and must remain visibly inside this projection fence.
PUBLIC_TEXT_SUFFIXES = TEXT_SUFFIXES | {".css", ".html", ".js", ".json"}

# Uppercase node-product spellings. Implicit multiplication is accepted only
# for the established compact forms (PhiV and hatted/subscripted factors); a
# bare Phi followed later by V is intentionally not enough.
PRODUCT_FORM = re.compile(
    r"(?:"
    r"Φ̂(?:₄|4)\s*(?:[×·*]\s*)?V(?:₄|4)"
    r"|Φ\s*[×·*]\s*V"
    r"|ΦV"
    r"|Phi(?:_?hat)?_?4\s*(?:[x×·*]\s*)?V_?4"
    r"|Phi\s*[x×·*]\s*V"
    r"|PhiV"
    r"|\\widehat\{\\Phi\}_\{?4\}?\s*(?:\\times\s*|\\cdot\s*|\*\s*)?V_\{?4\}?"
    r"|\\hat\{\\Phi\}_\{?4\}?\s*(?:\\times\s*|\\cdot\s*|\*\s*)?V_\{?4\}?"
    r"|\\Phi\s*(?:\\times|\\cdot|\*)\s*V"
    r")",
    re.IGNORECASE,
)

SELECTED_NODE_PRODUCT = re.compile(r"\bselected\s+node[- ]product\b", re.IGNORECASE)

# Lowercase reciprocal coordinates may satisfy phi*nu = 1 analytically. Only
# an explicit multiplication sign is scanned, and only in ordering/objective
# context, so the identity itself remains outside the node-score prohibition.
LOWER_PRODUCT_FORM = re.compile(
    r"(?:φ\s*[×*]\s*ν|phi\s*[x×*]\s*nu)", re.IGNORECASE
)

NODE_PRODUCT_ASSIGNMENT = re.compile(
    r"(?:P(?:_?\{?node\}?|_node|ₙₒdₑ)?|U(?:_eff)?|utility)\s*(?::=|=)\s*"
    + PRODUCT_FORM.pattern,
    re.IGNORECASE,
)

RANKING_LANGUAGE = re.compile(
    r"\b(?:rank(?:s|ed|ing)?|order(?:s|ed|ing)?|score(?:s|d|ing)?|"
    r"select(?:s|ed|ing)?|working|current|default|objective|"
    r"maximi[sz](?:e|es|ed|ing|ation)?|compar(?:e|es|ed|ing|ison)|"
    r"sort(?:s|ed|ing)?|fitness|payoff|utility|flourish(?:ing|ment)?|"
    r"predict(?:s|ed|ing|ion)?|model)\b",
    re.IGNORECASE,
)

LIFECYCLE_LANGUAGE = re.compile(
    r"\b(?:historical(?:ly)?|retired|former|legacy|provenance|superseded|"
    r"retracted|refuted|tombstone|frozen|dated|then-current|then-selected|"
    r"older|prior)\b",
    re.IGNORECASE,
)

CANDIDATE_LANGUAGE = re.compile(
    r"\b(?:candidate|conjecture|hypothesis|wager|pre-?register(?:ed|ation)?|"
    r"experimental|exploratory|test(?:able|ed|ing)?|trial|rival|open-empirical)\b|"
    r"separately\s+(?:declared\s+and\s+)?defended\s+cardinal|"
    r"cardinal[- ]scale\s+contract|cardinal\s+(?:proxy|proxies|scale|scales)",
    re.IGNORECASE,
)

NEGATION_LANGUAGE = re.compile(
    r"(?:does\s+not|doesn't|cannot|can't|may\s+not|must\s+not|no\s+longer|"
    r"never)[^.!?;\n]{0,180}(?:rank|score|select|order|compare|maximi[sz]e|"
    r"serve\s+as|restore|ground|derive|support)|"
    r"not\s+(?:the\s+)?(?:current|selected|working|default)\b|"
    r"(?:not\s+derived\s+from|do\s+not\s+entail|no\s+physical\s+force\s+follows|"
    r"being\s+heard\s+as)|"
    r"(?:not\s+supported|decisively\s+rejected|rejected|falsified|"
    r"kill\s+criterion\s+fired|ranks\s+nothing)",
    re.IGNORECASE,
)

DATED_EXPERIMENT = re.compile(r"^11_UPLINK/25_EXPERIMENTS/20\d\d-\d\d-\d\d_[^/]+/")

# One complete metalinguistic warning, not permission to define or rank nodes
# by the brand formula. Full-context equality admits only whitespace wrapping;
# adjacent assertions and weakened conditions do not inherit this exception.
BRAND_COLLISION_WARNING = (
    r"If this \(P\) co-appears with brand \(P=\Phi\times V\), "  # Not the current node ranking: warning literal.
    r"a projection note is required (name collision)."
)


def _starts_markdown_unit(line: str) -> bool:
    stripped = line.lstrip()
    return bool(
        re.match(r"(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|```|~~~|\|)", stripped)
    )


def _inside_code_fence(lines: list[str], index: int) -> bool:
    fences = sum(
        1 for line in lines[: index + 1] if re.match(r"^\s*(?:```|~~~)", line)
    )
    return fences % 2 == 1


def _clause_context(lines: list[str], index: int) -> str:
    """Return only the sentence/clause governing the occurrence's line.

    Markdown prose is commonly hard-wrapped, so a newline alone is not a
    boundary. Sentence punctuation, blank lines, and new Markdown units are.
    This intentionally prevents an unrelated adjacent denial from shielding a
    live assertion while still recognizing a qualifier wrapped across lines.
    """

    if _inside_code_fence(lines, index):
        return lines[index]

    start = index
    while start > 0:
        previous = lines[start - 1].strip()
        current = lines[start].strip()
        if not previous or re.search(r"[.!?;]\s*$", previous):
            break
        if _starts_markdown_unit(current):
            break
        start -= 1

    end = index
    while end + 1 < len(lines):
        current = lines[end].strip()
        following = lines[end + 1].strip()
        if not following or re.search(r"[.!?;]\s*$", current):
            break
        if _starts_markdown_unit(following):
            break
        end += 1
    return "\n".join(lines[start : end + 1])


def _direct_governing_label(lines: list[str], index: int) -> str:
    """Return an immediately preceding candidate/history label, if present."""

    cursor = index - 1
    while cursor >= 0 and not lines[cursor].strip():
        cursor -= 1
    if cursor < 0:
        return ""
    label = lines[cursor].strip()
    if not (
        label.endswith(":")
        or re.match(r"^(?:#{1,6}\s|[-*+]\s|>\s*\*\*)", label)
    ):
        return ""
    return label


def _file_wide_provenance_fence(text: str, rel: Path) -> bool:
    """Return true only for an explicit whole-file provenance/candidate fence."""

    rel_posix = rel.as_posix()
    if DATED_EXPERIMENT.match(rel_posix):
        return True

    head = "\n".join(text.splitlines()[:120])
    head_lower = head.lower()

    if (
        "historical peer-review artifact" in head_lower
        and "quoted axiom language is genealogy only" in head_lower
    ):
        return True
    if (
        re.search(r"(?:intake\s+)?status.{0,40}(?:superseded|retracted|refuted|frozen)", head, re.I | re.S)
        and re.search(r"(?:do\s+not\s+route|provenance|precursor|quoted|historical)", head, re.I)
    ):
        return True
    if (
        "result landed" in head_lower
        and "product-only" in head_lower
        and "not supported" in head_lower
        and "proposal below" in head_lower
    ):
        return True
    if (
        re.search(r"every\s+product\s+formula\s+in\s+this\s+paper.{0,180}candidate", head, re.I | re.S)
        and re.search(r"nothing\s+below\s+restores", head, re.I)
    ):
        return True
    if (
        re.search(r"every\s+multiplicative\s+curve\s+below.{0,120}candidate", head, re.I | re.S)
        and re.search(r"not\s+the\s+current\s+node\s+ranking", head, re.I)
    ):
        return True
    if (
        "quoted and proposed product-scoring" in head_lower
        and "not the current" in head_lower
        and "retired as a node ranking" in head_lower
    ):
        return True
    if (
        "[c] conjecture" in head_lower
        and "exploratory proof-of-concept" in head_lower
        and "canon-upgrade route" in head_lower
    ):
        return True
    if (
        re.search(r"every\s+product\s+expression\s+in\s+this\s+experiment.{0,160}candidate", head, re.I | re.S)
        and re.search(r"does\s+not\s+select\s+the\s+current\s+node\s+ranking", head, re.I)
    ):
        return True
    return False


def violations_in_text(text: str, rel: Path = Path("fixture.md")) -> list[tuple[int, str]]:
    """Return ``(line_number, line)`` for unfenced current product rankings."""

    if _file_wide_provenance_fence(text, rel):
        return []

    lines = text.splitlines()
    violations: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        upper_match = PRODUCT_FORM.search(line)
        selected_node_product = SELECTED_NODE_PRODUCT.search(line)
        lower_match = LOWER_PRODUCT_FORM.search(line)
        if not upper_match and not lower_match and not selected_node_product:
            continue

        # The lowercase reciprocal identity is analytic rather than a node
        # product. An explicit equality to one remains admissible even when the
        # surrounding prose discusses selection or fitness.
        if lower_match and re.match(r"\s*=\s*1(?:\b|-)", line[lower_match.end() :]):
            lower_match = None
            if not upper_match and not selected_node_product:
                continue

        context = _clause_context(lines, index)
        if " ".join(context.split()) == BRAND_COLLISION_WARNING:
            continue
        governing_label = _direct_governing_label(lines, index)
        qualified_context = "\n".join(part for part in (governing_label, context) if part)
        qualified_plain = re.sub(r"[`*_]", "", qualified_context)
        assignment = bool(NODE_PRODUCT_ASSIGNMENT.search(line))
        ranking_context = bool(RANKING_LANGUAGE.search(context))
        if not assignment and not ranking_context:
            continue

        # A qualifier must govern this occurrence locally. Generic uncertainty
        # (for example "not uniquely derived") is deliberately insufficient.
        if LIFECYCLE_LANGUAGE.search(qualified_plain):
            continue
        if CANDIDATE_LANGUAGE.search(qualified_plain):
            continue
        if NEGATION_LANGUAGE.search(qualified_plain):
            continue

        violations.append((index + 1, line.strip()))
    return violations


def is_node_ranking_scoped(path: Path, root: Path = ROOT) -> bool:
    rel = path.relative_to(root)
    if is_active_corpus_file(path):
        return True
    return (
        rel.is_relative_to(MANAGED_PROJECTION_PREFIX)
        and not any(part.startswith(".") for part in rel.parts)
        and path.suffix.lower() in TEXT_SUFFIXES
    )


def active_paths(root: Path = ROOT) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or not is_node_ranking_scoped(path, root):
            continue
        if path.relative_to(root) == FIXTURE_EXCLUSION:
            continue
        paths.append(path)
    return sorted(paths)


def declared_public_paths(root: Path = ROOT) -> list[Path]:
    """Return only public routes explicitly declared current or provisional.

    The manifest's frozen roots, withheld artifacts, infrastructure routes, and every
    arbitrary path below ``12_PUBLIC_SITE`` stay outside this semantic scan. This is a
    narrow projection extension, not a reclassification of historical public bytes.
    """

    site = (root / PUBLIC_PROJECTION_DIR).resolve()
    manifest_path = root / PUBLIC_PARITY_MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    current = manifest.get("currentSurfaces")
    provisional = manifest.get("declaredProvisional", {}).get("routes")
    if not isinstance(current, list) or not isinstance(provisional, list):
        raise ValueError("public lifecycle manifest must provide current and provisional path lists")

    paths: list[Path] = []
    for rel in current + provisional:
        if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
            raise ValueError(f"invalid declared public route: {rel!r}")
        path = (site / rel).resolve()
        try:
            path.relative_to(site)
        except ValueError as exc:
            raise ValueError(f"declared public route escapes 12_PUBLIC_SITE: {rel!r}") from exc
        if path.suffix.lower() in PUBLIC_TEXT_SUFFIXES:
            paths.append(path)
    return sorted(set(paths))


def scanned_paths(root: Path = ROOT) -> list[Path]:
    """Union active corpus paths with declared current/provisional public routes."""

    return sorted(set(active_paths(root)) | set(declared_public_paths(root)))


def check_active_corpus(root: Path = ROOT) -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        paths = scanned_paths(root)
    except (OSError, ValueError) as exc:
        return [f"public projection scope is unreadable: {exc}"], 0
    for path in paths:
        rel = path.relative_to(root)
        if not path.is_file():
            errors.append(f"{rel}: declared current/provisional public route is missing")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{rel}: unreadable declared current/provisional public route: {exc}")
            continue
        for line_no, line in violations_in_text(text, rel):
            errors.append(
                f"{rel}:{line_no}: retired node-product used as a current ordering: {line}"
            )
    return errors, len(paths)


def main() -> int:
    errors, count = check_active_corpus()
    if errors:
        print("NODE PRODUCT RANKING: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    print(f"NODE PRODUCT RANKING: PASS ({count} active files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

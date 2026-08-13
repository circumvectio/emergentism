#!/usr/bin/env python3
"""Deterministically assemble the staged full Emergentist Manifesto book.

The book is a projection-only reader artifact.  It composes source-mapped
chapter modules and appends a lifecycle-aware atlas of the claim cards that
support or bound the manuscript.  It deliberately does not create a new claim
owner or promote research, historical, or frozen material.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "13_BOOKS"
MANIFESTO = BOOKS / "manifesto"
CONTRACT = MANIFESTO / "FULL_BOOK_1_CONTRACT.json"
PREAMBLE_CONTRACT = MANIFESTO / "manifesto-contract.json"
OUTPUT = MANIFESTO / "MANIFESTO_BOOK_1.md"
BUILD = MANIFESTO / "MANIFESTO_BOOK_1_BUILD.json"
LEDGER = MANIFESTO / "MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"
DOCKETS = ROOT / "00_META/ADEQUACY_DOCKETS.yaml"
CARD_DIR = ROOT / "00_META/claim_cards"
BOOK_MANIFEST = BOOKS / "book-manifest.json"

MODULES = [
    ("preamble", MANIFESTO / "MANIFESTO_DRAFT_0.md"),
    ("part_i", MANIFESTO / "chapters/PART_I_THE_FINITE_CONDITION.md"),
    ("part_ii_iii", MANIFESTO / "chapters/PART_II_AND_III_CURRENT_CORE.md"),
    ("part_iv_v", MANIFESTO / "chapters/PART_IV_V_RESEARCH_GENEALOGY.md"),
    ("appendices", MANIFESTO / "chapters/APPENDICES_AND_WORKSHEETS.md"),
]


class ContractError(ValueError):
    """Raised when the staged book cannot be assembled safely."""


CARD_ID_RE = re.compile(r"\b[A-Z]+\d{2}-\d{2}\b")
FULLBOOK_MARKER_RE = re.compile(r"<!-- FULLBOOK-P: ([a-z0-9_-]+) -->")
PREAMBLE_MARKER_RE = re.compile(r"<!-- MANIFESTO-P: ([a-z0-9_]+) -->")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON-subset YAML {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S).strip()


def projection_owner_schema_errors(path: Path, card: dict[str, Any]) -> list[str]:
    """Return ownership-contract errors before a projection can dereference a card.

    The full-book assembler intentionally consumes the cards as a projection
    input rather than recompiling their complete corpus contract.  It still
    must not turn an incomplete or legacy ownership declaration into a
    ``KeyError`` or silently choose an owner.  The canonical claim-card
    compiler remains responsible for the wider source, locator, and registry
    checks.
    """
    card_id = card.get("card_id", "<unknown>")
    prefix = f"{path.relative_to(ROOT)}:{card_id}"
    if "owner_ids" in card:
        return [
            f"{prefix}: legacy owner_ids cannot enter a projection; declare "
            "semantic_owner_id and supporting_owner_ids"
        ]
    semantic_owner = card.get("semantic_owner_id")
    if not isinstance(semantic_owner, str) or not semantic_owner:
        return [f"{prefix}: missing semantic_owner_id"]
    supporting_owners = card.get("supporting_owner_ids")
    if not isinstance(supporting_owners, list) or any(
        not isinstance(owner, str) or not owner for owner in supporting_owners
    ):
        return [f"{prefix}: supporting_owner_ids must be a list of non-empty strings"]
    if semantic_owner in supporting_owners or len(set(supporting_owners)) != len(supporting_owners):
        return [f"{prefix}: supporting_owner_ids must be unique and exclude semantic_owner_id"]
    return []


def load_cards() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    cards: dict[str, dict[str, Any]] = {}
    sets: list[dict[str, Any]] = []
    ownership_errors: list[str] = []
    for path in sorted(CARD_DIR.glob("*.yaml")):
        payload = read_json(path)
        work_id = payload.get("work_id")
        if not isinstance(work_id, str):
            raise ContractError(f"claim-card set lacks work_id: {path.relative_to(ROOT)}")
        source = payload.get("source")
        if not isinstance(source, dict):
            raise ContractError(f"claim-card set lacks source: {path.relative_to(ROOT)}")
        sets.append({
            "work_id": work_id,
            "path": path.relative_to(ROOT).as_posix(),
            "source": source,
        })
        raw_cards = payload.get("cards")
        if not isinstance(raw_cards, list):
            raise ContractError(f"claim-card set cards must be a list: {path.relative_to(ROOT)}")
        for card in raw_cards:
            if not isinstance(card, dict) or not isinstance(card.get("card_id"), str):
                raise ContractError(f"invalid card in {path.relative_to(ROOT)}")
            card_id = card["card_id"]
            if card_id in cards:
                raise ContractError(f"duplicate card id: {card_id}")
            ownership_errors.extend(projection_owner_schema_errors(path, card))
            cards[card_id] = {**card, "_work_id": work_id, "_card_set": path.relative_to(ROOT).as_posix(), "_source": source}
    if ownership_errors:
        raise ContractError(
            "claim-card ownership contract invalid:\n"
            + "\n".join(f"- {error}" for error in ownership_errors)
        )
    return cards, sets


def preamble_for_full_book(body: str) -> str:
    """Project only the current Preamble out of its older standalone draft.

    The short draft includes its own research-map pages, which would duplicate
    and blur the lifecycle-bound Part IV/V chapters in the full reader.  The
    full book keeps the compression ladder, the current core, the refusal list,
    and the release note; its research material is supplied by the dedicated
    source-mapped chapters later in the manuscript.
    """
    body = re.sub(
        r"\n## Research record — not part of the current claim body.*?(?=\n## The close:)",
        "\n",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\n## One corpus, differentiated jobs.*?(?=\n## What this manifesto refuses)",
        "\n",
        body,
        flags=re.S,
    )
    preamble_contract = read_json(PREAMBLE_CONTRACT)
    records = {entry["id"]: entry for entry in preamble_contract["paragraphs"]}
    matches = list(PREAMBLE_MARKER_RE.finditer(body))
    if not matches:
        raise ContractError("Preamble has no MANIFESTO-P coverage markers")
    rendered: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        marker_id = match.group(1)
        if marker_id not in records:
            raise ContractError(f"Preamble marker lacks source-contract record: {marker_id}")
        rendered.append(body[cursor:match.start()])
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        unit = body[match.end():next_start]
        record = records[marker_id]
        source_lines = re.findall(r"(?m)Source cards: .+$", unit)
        if len(source_lines) > 1:
            raise ContractError(f"Preamble marker has multiple source lines: {marker_id}")
        if not source_lines:
            card_ids = record["claim_card_ids"]
            source = ", ".join(card_ids) if card_ids else "none — editorial control"
            insert = f"\nSource cards: {source}.\n"
            # Do not attach a source line to the next heading.  If a heading
            # appears after the unit, place the receipt immediately before it.
            heading = re.search(r"(?m)^#{1,6}\s", unit)
            if heading:
                unit = unit[:heading.start()].rstrip() + insert + unit[heading.start():]
            else:
                unit = unit.rstrip() + insert
        else:
            rendered_cards = source_cards_from_line(source_lines[0])
            expected_cards = record["claim_card_ids"]
            if rendered_cards != expected_cards:
                raise ContractError(
                    f"Preamble marker {marker_id} receipt does not match its source-contract card list"
                )
        rendered.append(f"<!-- FULLBOOK-P: preamble_{marker_id} -->")
        rendered.append(unit)
        cursor = next_start
    return "".join(rendered).strip()


def source_body(kind: str, path: Path) -> str:
    if not path.is_file():
        raise ContractError(f"missing book module: {path.relative_to(ROOT)}")
    body = strip_frontmatter(path.read_text(encoding="utf-8"))
    if kind == "preamble":
        body = re.sub(r"\A# The Emergentist Manifesto\s*\n", "", body, count=1)
        body = preamble_for_full_book(body)
    # Some reader modules keep their receipt at the end of a prose line.  The
    # assembled book gives every substantive unit a distinct, machine-readable
    # source line without rewriting the source module or its semantic owner.
    body = re.sub(r"(?<!\n)(?<=\S) Source cards: ", "\n\nSource cards: ", body)
    return body.strip()


def marker(card_id: str) -> str:
    return card_id.lower().replace("-", "_")


def bullet(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def atlas_entry(card: dict[str, Any]) -> str:
    card_id = card["card_id"]
    public = card["public"]
    state = public["state"]
    evidence = "; ".join(f"[{row['tier']}] {row['scope']}" for row in card["evidence"])
    source = card["_source"]
    if state == "frozen":
        return "\n".join([
            f"<!-- FULLBOOK-P: atlas_{marker(card_id)} -->",
            f"### {card_id} — frozen custody record",
            "This card is frozen historical provenance. The full book preserves its identifier, "
            "owner route, and custody boundary but does not regenerate its claim, rival, or "
            "explanatory prose.",
            f"- **Work:** `{card['_work_id']}`; **owner:** `{card['semantic_owner_id']}`.",
            f"- **Public state:** `{state}`; **disposition:** `{card['disposition']}`.",
            f"- **Source custody:** `{source['path']}` at reviewed SHA-256 `{source['reviewed_source_sha256']}`.",
            f"Source cards: `{card_id}`.",
        ])

    consequence = card.get("consequence", {})
    consequence_text = "not applicable"
    if consequence.get("applicable"):
        consequence_text = (
            f"bearers: {bullet(consequence.get('bearers', []))}; consent: {consequence.get('consent')}; "
            f"reversibility: {consequence.get('reversibility')}; exit: {consequence.get('exit')}"
        )
    return "\n".join([
        f"<!-- FULLBOOK-P: atlas_{marker(card_id)} -->",
        f"### {card_id} — {card['plain_claim']}",
        f"- **Work / owner:** `{card['_work_id']}` / `{card['semantic_owner_id']}`.",
        f"- **Classification:** `{card['claim_type']}`; **evidence:** {evidence}.",
        f"- **Lifecycle and public ceiling:** source `{source['lifecycle']}`; public `{state}` — {public['wording']}",
        f"- **Type boundary:** {bullet(card.get('type_boundaries', []))}.",
        f"- **Strongest rival:** {card['strongest_rival']}",
        f"- **Discriminator:** {card['discriminator']}",
        f"- **Kill or narrowing route:** {card['kill_criterion']}",
        f"- **Survivor if killed:** {card['survivor_if_killed']}",
        f"- **Consequence / exit:** {consequence_text}.",
        f"- **Source revision:** `{source['path']}` at reviewed SHA-256 `{source['reviewed_source_sha256']}`.",
        f"Source cards: `{card_id}`.",
    ])


def claim_card_atlas(cards: dict[str, dict[str, Any]]) -> str:
    order = [
        "BK-ONE-SITTING",
        "BK-FINITY-PRACTICE",
        "BK-TITANS",
        "BK-DHARMA",
        "BK-EVOLUTIONARY-NETWORK",
        "BK-SELF-EATING",
        "BK-SIX-LENSES",
        "BK-SARPASYA",
        "BK-RECIPROCAL-INFINITE-PLAY",
    ]
    grouped: dict[str, list[dict[str, Any]]] = {work_id: [] for work_id in order}
    for card in cards.values():
        grouped.setdefault(card["_work_id"], []).append(card)
    sections = [
        "# Appendix B — Claim-Card Atlas",
        "",
        "<!-- FULLBOOK-P: appendix_atlas_intro -->",
        "This atlas is a transparency layer, not a second doctrine. Each entry preserves the "
        "card's owner, evidence tier, lifecycle, public ceiling, strongest rival, discriminator, "
        "and kill route. `bounded_current` means only that an explicitly bounded wording is "
        "available for review; it does not mean the whole worldview, a book, a product, or a "
        "group has been validated. Source-only and historical cards remain visibly non-current. "
        "Frozen cards receive custody metadata only.",
        "Source cards: none — editorial control.",
    ]
    for work_id in order:
        entries = sorted(grouped.get(work_id, []), key=lambda row: row["card_id"])
        if not entries:
            continue
        sections.extend(["", f"## {work_id}", ""])
        sections.extend(atlas_entry(card) for card in entries)
    return "\n\n".join(sections)


def docket_atlas(dockets: dict[str, Any]) -> str:
    rows = [
        "# Appendix C — Adequacy Dockets",
        "",
        "<!-- FULLBOOK-P: appendix_docket_intro -->",
        "The dockets are maturity records, not truth labels. A stronger result in one row does "
        "not validate the worldview as a whole; publication, adoption, and agreement are not "
        "evidence. The entries below state the unpaid gate and the narrowing route for each "
        "ambition.",
        "Source cards: none — editorial control.",
    ]
    for docket in dockets["dockets"]:
        rows.extend([
            "",
            f"<!-- FULLBOOK-P: docket_{docket['docket_id'].lower()} -->",
            f"## {docket['docket_id']} — {docket['title']}",
            f"- **Maturity:** `{docket['status']}`; **owners:** {', '.join(docket['owner_ids'])}.",
            f"- **Gate:** {docket['gate']}",
            f"- **Narrow or kill route:** {docket['kill_or_narrow']}",
            f"- **Depends on:** {', '.join(docket['depends_on']) or 'none'}.",
            "Source record: `00_META/ADEQUACY_DOCKETS.yaml`.",
            "Source cards: none — adequacy-docket metadata.",
        ])
    return "\n".join(rows)


def custody_note() -> str:
    """Render custody metadata only for the frozen Reciprocal source."""
    manifest = read_json(BOOK_MANIFEST)
    work = next(
        (row for row in manifest.get("works", []) if row.get("work_id") == "BK-RECIPROCAL-INFINITE-PLAY"),
        None,
    )
    if not isinstance(work, dict):
        raise ContractError("book manifest lacks BK-RECIPROCAL-INFINITE-PLAY custody work")
    historical_sources = work.get("historical_sources")
    if not isinstance(historical_sources, list) or not historical_sources:
        raise ContractError("frozen Reciprocal custody work lacks historical sources")
    provenance = work.get("build_provenance")
    if not isinstance(provenance, dict):
        raise ContractError("frozen Reciprocal custody work lacks critical-edition provenance")
    routes = manifest.get("editorial_architecture", {}).get("nonbook_claim_routes", [])
    route = next(
        (row for row in routes if row.get("work_id") == work["work_id"]),
        None,
    )
    if not isinstance(route, dict):
        raise ContractError("frozen Reciprocal custody work lacks custody route")
    source_rows = []
    for source in historical_sources:
        if not isinstance(source, dict):
            raise ContractError("frozen Reciprocal custody source is malformed")
        source_rows.append(
            f"- **Historical source:** `{source['path']}`; **lifecycle:** `{source['lifecycle']}`; "
            f"**reviewed SHA-256:** `{source['reviewed_source_sha256']}`."
        )
    return "\n".join([
        "# Appendix D — Frozen Reciprocal / Infinite Play Custody Note",
        "",
        "<!-- FULLBOOK-P: appendix_reciprocal_custody -->",
        f"- **Work ID:** `{work['work_id']}`.",
        "- **Frozen lifecycle:** `frozen`.",
        "- **Preservation reason:** retain historical provenance without regenerating any claim prose.",
        *source_rows,
        f"- **Critical-edition projection:** `{provenance['path']}`; **SHA-256:** `{provenance['sha256']}`.",
        "- **Debrief route:** `13_BOOKS/reciprocal_infinite_play/DEBRIEF.md`.",
        f"- **Custody route:** `{route['route_id']}`; **primary home:** `{route['primary_home']}`.",
        "Source cards: none — custody metadata.",
    ])


def source_cards_from_line(line: str) -> list[str]:
    return CARD_ID_RE.findall(line)


RESEARCH_RECORD_PREFIXES = ("p4-12-", "p4-13-", "p4-14-", "p4-15-")
RESEARCH_RECORD_LABELS = (
    "Research status:",
    "Strongest rival:",
    "Discriminator:",
    "Narrow or kill condition:",
    "Public disposition:",
)


def research_record_fields(card_ids: list[str], cards: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Derive the five G4 fields from a unit's declared primary source card."""
    if not card_ids:
        raise ContractError("research-record unit has no source-card receipt")
    primary = cards[card_ids[0]]
    tier_summary = "; ".join(
        f"[{row['tier']}] {row['scope']}" for row in primary["evidence"]
    )
    source_states = ", ".join(
        f"`{card_id}` `{cards[card_id]['public']['state']}`" for card_id in card_ids
    )
    return {
        "primary_card_id": primary["card_id"],
        "record_basis": "derived_from_primary_card",
        "research_status": (
            f"primary card `{primary['card_id']}` — {tier_summary}; this remains a private "
            "research record rather than a result."
        ),
        "strongest_rival": primary["strongest_rival"],
        "discriminator": primary["discriminator"],
        "narrow_or_kill_condition": primary["kill_criterion"],
        "public_disposition": (
            "`private_research_record_only`; source-card ceilings remain " + source_states + "."
        ),
    }


def research_record_metadata(card_ids: list[str], cards: dict[str, dict[str, Any]], unit: str) -> str:
    """Supply any missing G4 labels without changing the source chapter prose.

    The source-mapped reader modules carry the argument.  This projection-level
    metadata makes each private research unit legible beside that argument by
    using the first listed source card as the unit's primary record.  All
    remaining cards stay visible in the unit receipt and the Claim-Card Atlas.
    """
    fields = research_record_fields(card_ids, cards)
    fields = {
        "Research status:": fields["research_status"],
        "Strongest rival:": fields["strongest_rival"],
        "Discriminator:": fields["discriminator"],
        "Narrow or kill condition:": fields["narrow_or_kill_condition"],
        "Public disposition:": fields["public_disposition"],
    }
    missing = [label for label in RESEARCH_RECORD_LABELS if label not in unit]
    return "\n".join(f"**{label}** {fields[label]}" for label in missing)


def annotate_research_records(body: str, cards: dict[str, dict[str, Any]]) -> str:
    """Make G4's five labels adjacent to every research unit in Chapters 12–15."""
    matches = list(FULLBOOK_MARKER_RE.finditer(body))
    if not matches:
        return body
    rendered: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        marker_id = match.group(1)
        rendered.append(body[cursor:match.end()])
        unit = body[match.end():stop]
        if marker_id.startswith(RESEARCH_RECORD_PREFIXES):
            source_lines = re.findall(r"(?m)^Source cards: .+$", unit)
            if len(source_lines) != 1:
                raise ContractError(
                    f"research-record marker {marker_id} needs exactly one standalone Source cards receipt"
                )
            source_line = source_lines[0]
            card_ids = source_cards_from_line(source_line)
            metadata = research_record_metadata(card_ids, cards, unit)
            if metadata:
                position = unit.index(source_line)
                unit = unit[:position].rstrip() + "\n\n" + metadata + "\n\n" + unit[position:]
        rendered.append(unit)
        cursor = stop
    return "".join(rendered)


def chapter_metadata(contract: dict[str, Any], marker_id: str, unit: str, preceding: str) -> dict[str, str]:
    """Classify a marker without allowing the projection to invent an owner."""
    chapters = {item["id"]: item for item in contract["chapters"]}
    if marker_id.startswith("book_"):
        return {
            "chapter_id": "book_editorial_scope",
            "lifecycle_class": "editorial_control",
            "public_disposition": "not_a_body_claim",
    }
    if marker_id.startswith("preamble_"):
        record_id = marker_id.removeprefix("preamble_")
        records = {entry["id"]: entry for entry in read_json(PREAMBLE_CONTRACT)["paragraphs"]}
        if record_id not in records:
            raise ContractError(f"unknown Preamble marker: {record_id}")
        record = records[record_id]
        return {
            "chapter_id": "preamble_quickstart",
            "lifecycle_class": "current_body" if record["lifecycle"] == "current_body" else "editorial_control",
            "public_disposition": "bounded_current_only_after_full_chapter_and_public_gates" if record["lifecycle"] == "current_body" else "not_a_body_claim",
        }
    if marker_id in {"p1-001"} or marker_id.startswith(("p2-boundary", "p4-boundary")):
        return {
            "chapter_id": "editorial_part_boundary",
            "lifecycle_class": "editorial_control",
            "public_disposition": "not_a_body_claim",
        }
    numbered = re.findall(r"(?m)^## ([1-9]|1[0-7])\. ", preceding)
    if numbered and marker_id.startswith(("p1-", "p2-")):
        chapter_id = {
            "1": "ch01_finite_predicament",
            "2": "ch02_frames_not_furniture",
            "3": "ch03_record_and_possibility",
            "4": "ch04_soul_loop",
            "5": "ch05_finity_card",
            "6": "ch06_justice_chosen",
            "7": "ch07_conflict_and_residue",
            "8": "ch08_social_loop",
            "9": "ch09_thin_coordination",
            "10": "ch10_institutions_can_end",
            "11": "ch11_competition_without_war",
        }[numbered[-1]]
        chapter = chapters[chapter_id]
        return {
            "chapter_id": chapter_id,
            "lifecycle_class": chapter["lifecycle_class"],
            "public_disposition": chapter["public_disposition"],
        }
    direct = (
        ("p2-05-", "ch05_finity_card"),
        ("p2-06-", "ch06_justice_chosen"),
        ("p2-07-", "ch07_conflict_and_residue"),
        ("p2-08-", "ch08_social_loop"),
        ("p2-09-", "ch09_thin_coordination"),
        ("p2-10-", "ch10_institutions_can_end"),
        ("p2-11-", "ch11_competition_without_war"),
        ("p4-12-", "ch12_titans_research"),
        ("p4-13-", "ch13_world_contact"),
        ("p4-14-", "ch14_action_and_institution_research"),
        ("p4-15-", "ch15_lenses_and_immune_protocol"),
        ("p5-16-", "ch16_corrections_kept"),
        ("p5-17-", "ch17_right_to_leave"),
    )
    for prefix, chapter_id in direct:
        if marker_id.startswith(prefix):
            chapter = chapters[chapter_id]
            return {
                "chapter_id": chapter_id,
                "lifecycle_class": chapter["lifecycle_class"],
                "public_disposition": chapter["public_disposition"],
            }
    if marker_id.startswith("app_b_"):
        return {
            "chapter_id": "appendix_finity_comparison",
            "lifecycle_class": "research_record",
            "public_disposition": "private_research_record_only",
        }
    if marker_id.startswith(("app_a_", "app_c_", "app_d_", "app_e_", "app_f_", "app_g_", "app_h_")):
        return {
            "chapter_id": "appendix_finity_card_or_reader_tools",
            "lifecycle_class": "current_body",
            "public_disposition": "bounded_current_only_after_full_chapter_and_public_gates",
        }
    if marker_id.startswith("app_status_"):
        return {
            "chapter_id": "appendix_editorial_boundary",
            "lifecycle_class": "editorial_control",
            "public_disposition": "not_a_body_claim",
        }
    if marker_id.startswith("atlas_"):
        return {
            "chapter_id": "appendix_claim_card_atlas",
            "lifecycle_class": "editorial_control",
            "public_disposition": "not_a_body_claim",
        }
    if marker_id.startswith("docket_") or marker_id in {"appendix_docket_intro", "appendix_atlas_intro"}:
        return {
            "chapter_id": "appendix_adequacy_dockets_or_atlas",
            "lifecycle_class": "editorial_control",
            "public_disposition": "not_a_body_claim",
        }
    if marker_id == "appendix_reciprocal_custody":
        return {
            "chapter_id": "appendix_reciprocal_custody",
            "lifecycle_class": "custody_only",
            "public_disposition": "no_regenerated_prose",
        }
    raise ContractError(f"unrouted full-book marker: {marker_id}")


def parse_marker_units(text: str, contract: dict[str, Any], cards: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    matches = list(FULLBOOK_MARKER_RE.finditer(text))
    if not matches:
        raise ContractError("assembled manuscript has no FULLBOOK-P markers")
    ids = [match.group(1) for match in matches]
    if len(ids) != len(set(ids)):
        duplicate = next(item for item in ids if ids.count(item) > 1)
        raise ContractError(f"duplicate full-book marker: {duplicate}")
    units: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        marker_id = match.group(1)
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        unit = text[match.end():stop]
        source_lines = re.findall(r"(?m)^Source cards: .+$", unit)
        if len(source_lines) != 1:
            raise ContractError(f"marker {marker_id} needs exactly one standalone Source cards receipt")
        source_line = source_lines[0]
        source_match = re.search(r"(?m)^Source cards: .+$", unit)
        assert source_match is not None
        heading = re.search(r"(?m)^#{1,6}\s", unit[:source_match.start()])
        if heading:
            allowed_heading_scope = marker_id.startswith(("atlas_", "docket_"))
            if not allowed_heading_scope or unit[:heading.start()].strip():
                raise ContractError(
                    f"marker {marker_id} has an unpermitted heading before its source receipt"
                )
        card_ids = source_cards_from_line(source_line)
        if not card_ids and "none" not in source_line.lower():
            raise ContractError(f"marker {marker_id} has no known cards and is not editorial/custody metadata")
        for card_id in card_ids:
            if card_id not in cards:
                raise ContractError(f"marker {marker_id} references unknown card {card_id}")
        meta = chapter_metadata(contract, marker_id, unit, text[:match.start()])
        non_current = [card_id for card_id in card_ids if cards[card_id]["public"]["state"] != "bounded_current"]
        if marker_id.startswith("atlas_") and card_ids and all(
            cards[card_id]["public"]["state"] == "frozen" for card_id in card_ids
        ):
            meta = {
                "chapter_id": "appendix_reciprocal_custody",
                "lifecycle_class": "custody_only",
                "public_disposition": "no_regenerated_prose",
            }
        # The appendix is a reader tool with a visibly private comparison
        # layer.  A marker in that source module becomes a research record as
        # soon as it actually names a non-current card; it never promotes the
        # card merely because the surrounding appendix is otherwise current.
        if non_current and marker_id.startswith("app_") and meta["lifecycle_class"] == "current_body":
            meta = {
                "chapter_id": "appendix_research_boundary",
                "lifecycle_class": "research_record",
                "public_disposition": "private_research_record_only",
            }
        if meta["lifecycle_class"] == "current_body":
            if not card_ids:
                raise ContractError(f"current-body marker {marker_id} has no card coverage")
            if non_current:
                raise ContractError(f"current-body marker {marker_id} uses non-current cards: {', '.join(non_current)}")
        work_ids = sorted({cards[card_id]["_work_id"] for card_id in card_ids})
        source_revision_rows: dict[tuple[str, str, str], dict[str, Any]] = {}
        for card_id in card_ids:
            card = cards[card_id]
            source = card["_source"]
            key = (
                card["_work_id"],
                source["path"],
                source["reviewed_source_sha256"],
            )
            row = source_revision_rows.setdefault(key, {
                "work_id": card["_work_id"],
                "source_path": source["path"],
                "reviewed_source_sha256": source["reviewed_source_sha256"],
                "claim_card_ids": [],
            })
            row["claim_card_ids"].append(card_id)
        source_revisions = [
            source_revision_rows[key]
            for key in sorted(source_revision_rows)
        ]
        evidence_tiers = sorted({row["tier"] for card_id in card_ids for row in cards[card_id]["evidence"]})
        owner_ids = sorted({owner for card_id in card_ids for owner in [cards[card_id]["semantic_owner_id"], *cards[card_id].get("supporting_owner_ids", [])]})
        research_record = None
        if marker_id.startswith(RESEARCH_RECORD_PREFIXES):
            missing_labels = [label for label in RESEARCH_RECORD_LABELS if label not in unit]
            if missing_labels:
                raise ContractError(
                    f"research-record marker {marker_id} lacks G4 labels: {', '.join(missing_labels)}"
                )
            research_record = research_record_fields(card_ids, cards)
        entry = {
            "id": marker_id,
            **meta,
            "line_range": [text.count("\n", 0, match.start()) + 1, text.count("\n", 0, match.end() + source_match.end()) + 1],
            "claim_card_ids": card_ids,
            "source_work_ids": work_ids,
            "source_revisions": source_revisions,
            "semantic_owner_ids": owner_ids,
            "evidence_tiers": evidence_tiers,
            "card_public_states": sorted({cards[card_id]["public"]["state"] for card_id in card_ids}),
            "source_receipt": source_line,
        }
        if research_record is not None:
            entry["research_record"] = research_record
        units.append(entry)
    return units


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def render() -> tuple[str, dict[str, Any], dict[str, Any]]:
    contract = read_json(CONTRACT)
    if contract.get("status") != "staged_full_book_build_not_public":
        raise ContractError("full-book contract must remain staged and not public")
    cards, card_sets = load_cards()
    dockets = read_json(DOCKETS)
    modules: list[tuple[str, str]] = []
    source_hashes: list[dict[str, str]] = []
    for kind, path in MODULES:
        body = source_body(kind, path)
        if kind == "part_iv_v":
            body = annotate_research_records(body, cards)
        modules.append((kind, body))
        source_hashes.append({"role": kind, "path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path.read_bytes())})

    frontmatter = "\n".join([
        "---",
        'title: "The Emergentist Manifesto: A Worldview for Finite Beings"',
        'status: "STAGED PRIVATE FULL-BOOK MANUSCRIPT — evidence-mapped; not public or deployed"',
        'authority: "projection only; K-1 through K-7 retain semantic ownership"',
        'source_contract: "FULL_BOOK_1_CONTRACT.json"',
        'build_provenance: "09_TOOLS/02_COMPILERS/assemble_manifesto_book.py"',
        "---",
        "",
    ])
    introduction = "\n".join([
        "# The Emergentist Manifesto",
        "",
        "## A worldview for finite beings",
        "",
        "<!-- FULLBOOK-P: book_private_scope -->",
        "This is a staged private full-reader manuscript. It is a projection of reviewed source "
        "cards and preserves their evidence tiers and lifecycle boundaries. It is not a completed "
        "ontology, a public release, a membership test, a political programme, or proof of its own "
        "truth. A reader may use a part, test it, criticize it, fork it, or put it down.",
        "",
        "Source cards: OS01-13, OS01-25, OS01-26.",
        "",
        "<!-- FULLBOOK-P: book_layer_scope -->",
        "The book separates four layers: current-body prose grounded only in `bounded_current` "
        "cards; research records that retain their rivals and kill routes; critical genealogy that "
        "does not revive legacy authority; and frozen custody that does not regenerate claims. "
        "Its claim atlas is part of the reader: an argument is not made stronger by being hidden "
        "from its rival or its failure condition.",
        "",
        "Source cards: OS01-13, OS01-26.",
        "",
    ])
    body_parts = [frontmatter + introduction]
    for _, body in modules:
        body_parts.append(body)
    body_parts.extend([claim_card_atlas(cards), docket_atlas(dockets), custody_note()])
    rendered = "\n\n---\n\n".join(body_parts).strip() + "\n"
    words = word_count(rendered)
    lower = contract["target_word_range"]["minimum"]
    upper = contract["target_word_range"]["maximum"]
    if words < lower or words > upper:
        raise ContractError(f"full-book word count {words} falls outside declared target {lower}–{upper}")
    paragraphs = parse_marker_units(rendered, contract, cards)
    ledger = {
        "schema": "emergentism/full-book-paragraph-ledger/v1",
        "authority": "generated coverage receipt; source cards retain semantic ownership",
        "contract": CONTRACT.relative_to(ROOT).as_posix(),
        "manuscript": {
            "path": OUTPUT.relative_to(ROOT).as_posix(),
            "sha256": sha256(rendered.encode("utf-8")),
            "word_count": words,
        },
        "paragraphs": paragraphs,
    }
    build = {
        "schema": "emergentism/full-book-build/v1",
        "authority": "deterministic projection receipt; source owners retain semantics",
        "contract": CONTRACT.relative_to(ROOT).as_posix(),
        "contract_sha256": sha256(CONTRACT.read_bytes()),
        "output": {"path": OUTPUT.relative_to(ROOT).as_posix(), "sha256": sha256(rendered.encode("utf-8")), "word_count": words},
        "modules": source_hashes,
        "metadata_sources": [
            {"role": "preamble_contract", "path": PREAMBLE_CONTRACT.relative_to(ROOT).as_posix(), "sha256": sha256(PREAMBLE_CONTRACT.read_bytes())},
            {"role": "book_manifest_custody", "path": BOOK_MANIFEST.relative_to(ROOT).as_posix(), "sha256": sha256(BOOK_MANIFEST.read_bytes())},
        ],
        "paragraph_ledger": {
            "path": LEDGER.relative_to(ROOT).as_posix(),
            "sha256": sha256(canonical_json(ledger)),
            "count": len(paragraphs),
        },
        "claim_card_sets": [
            {
                "work_id": value["work_id"],
                "path": value["path"],
                "source": value["source"]["path"],
                "reviewed_source_sha256": value["source"]["reviewed_source_sha256"],
            }
            for value in sorted(card_sets, key=lambda row: (row["work_id"], row["path"]))
        ],
        "adequacy_dockets": {"path": DOCKETS.relative_to(ROOT).as_posix(), "sha256": sha256(DOCKETS.read_bytes())},
        "public_disposition": "not_a_public_route",
    }
    return rendered, build, ledger


def canonical_json(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the assembled manuscript and deterministic build receipt")
    mode.add_argument("--check", action="store_true", help="verify the assembled manuscript and receipt")
    args = parser.parse_args(argv)
    try:
        manuscript, build, ledger = render()
    except ContractError as exc:
        print(f"FULL BOOK BUILD: FAIL\n- {exc}")
        return 1
    expected_build = canonical_json(build)
    expected_ledger = canonical_json(ledger)
    if args.check:
        errors = []
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != manuscript.encode("utf-8"):
            errors.append(f"{OUTPUT.relative_to(ROOT)} drift")
        if not BUILD.is_file() or BUILD.read_bytes() != expected_build:
            errors.append(f"{BUILD.relative_to(ROOT)} drift")
        if not LEDGER.is_file() or LEDGER.read_bytes() != expected_ledger:
            errors.append(f"{LEDGER.relative_to(ROOT)} drift")
        if errors:
            print("FULL BOOK BUILD: FAIL")
            print("\n".join(f"- {item}" for item in errors))
            return 1
        print(f"FULL BOOK BUILD: PASS ({build['output']['word_count']:,} words, {len(build['modules'])} narrative modules, {build['paragraph_ledger']['count']} source-mapped units, {len(build['claim_card_sets'])} card sets)")
        return 0
    OUTPUT.write_text(manuscript, encoding="utf-8")
    BUILD.write_bytes(expected_build)
    LEDGER.write_bytes(expected_ledger)
    print(f"FULL BOOK BUILD: WROTE {build['output']['word_count']:,} words and {build['paragraph_ledger']['count']} source-mapped units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

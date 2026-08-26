#!/usr/bin/env python3
"""Build every public Third Churning projection from its source packet.

The source packet owns propositions, problem adjudications, paradox inventory,
schemas, ordering, and custody.  This file is the sole writer of the public
routes and machine projections listed in ``build_outputs``.  ``--check`` is
strictly read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

from build_core_shell import render_page, surface_for


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PACKET = ROOT / "14_THE_DISTILLATION" / "07_THE_THIRD_CHURNING_2026_08_23"
DROP_SOURCE = PACKET / "data" / "churning_drops.v1.json"
PROBLEM_SOURCE = PACKET / "data" / "problem_adjudications.v1.json"
PARADOX_SOURCE = PACKET / "data" / "paradox_inventory.v1.json"
ENVELOPE_SOURCE = PACKET / "ThirdChurningCorpus.v1.json"

SCHEMA_SOURCES = {
    "ChurningDrop.v1.schema.json": PACKET / "contracts" / "ChurningDrop.v1.schema.json",
    "ProblemAdjudication.v1.schema.json": PACKET
    / "contracts"
    / "ProblemAdjudication.v1.schema.json",
    "ThirdChurningCorpus.v1.schema.json": PACKET
    / "contracts"
    / "ThirdChurningCorpus.v1.schema.json",
}

FROZEN_COMMIT = "8b07e00c563f338923b1928d3469c862d44c1e07"
PQA_COUNTS = {
    "selected": 54,
    "evaluated": 0,
    "independently_reviewed": 0,
    "resolved": 0,
}
PQA_STATUS = (
    "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved"
)
MAXIM = "The means is the message. The ends are the limits."
SCRIPT_TAG = '<script defer src="/assets/js/gestalt-v2.js"></script>'

SOURCE_OUTPUT_MAP = {
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

DROP_KEYS = {
    "schema_id",
    "drop_id",
    "plain_name",
    "mythic_alias",
    "classification",
    "lifecycle",
    "evidence_tier",
    "proposition",
    "scope",
    "assumptions",
    "source_refs",
    "strongest_rival",
    "discriminator",
    "kill_criterion",
    "cheapest_next_test",
    "survivor_if_killed",
    "residual_debt",
    "means_message",
    "ends_limits",
    "linked_problem_ids",
    "earned_review",
    "revision_history",
}
PROBLEM_KEYS = {
    "schema_id",
    "problem_id",
    "canonical_problem_id",
    "aliases",
    "domain",
    "family",
    "native_problem",
    "native_reference",
    "proposed_answer",
    "proposed_effect",
    "earned_effect",
    "result_state",
    "assumptions",
    "strongest_rival",
    "native_frame_control",
    "generic_decomposition_control",
    "discriminator",
    "kill_criterion",
    "remaining_debt",
    "survivor_if_killed",
    "linked_drop_ids",
    "native_reviews",
}
MEANS_KEYS = {
    "bearers",
    "short_horizon",
    "long_horizon",
    "carrier",
    "cost",
    "consent_or_mandate",
    "authority",
    "reversibility",
    "externalities",
}
ENDS_KEYS = {
    "target",
    "hard_limit",
    "option_change",
    "residue",
    "exit",
    "uncertainty",
}
EVIDENCE_TIERS = {
    "[A]",
    "[B]",
    "[S]",
    "[I]",
    "[D]",
    "[C]",
    "[A/S]",
    "[I/C]",
    "[D/C]",
    "[S/I/C]",
}
PROPOSED_EFFECTS = {
    "INVENTORY",
    "CLARIFICATION",
    "FORMAL_CORRECTION",
    "TYPE_DISSOLUTION",
    "CONDITIONAL_RESOLUTION",
    "REFRAME",
    "OPEN",
}


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value


def require_text_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{label} must be a{' non-empty' if not allow_empty else ''} list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label} must contain only non-empty text")
    return value


def safe_relative_path(value: Any, label: str) -> str:
    """Accept only a repository-relative, non-traversing POSIX path."""

    text = require_text(value, label)
    path = Path(text)
    if path.is_absolute() or ".." in path.parts or "\\" in text:
        raise ValueError(f"{label} must be a safe repository-relative path")
    if path.as_posix() != text or text.startswith("./"):
        raise ValueError(f"{label} must use canonical POSIX spelling")
    return text


def esc(value: object) -> str:
    """Escape every source-derived string before it enters HTML."""

    return html.escape(str(value), quote=True)


def md_esc(value: object) -> str:
    """Keep source strings inert in the generated Markdown projection."""

    text = " ".join(str(value).splitlines())
    return re.sub(r"([\\`*_{}\[\]()#+.!|>])", r"\\\1", text)


def pretty_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate_inputs(
    envelope: Any,
    drops: Any,
    problems: Any,
    paradoxes: Any,
    schemas: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    if not isinstance(envelope, dict):
        raise ValueError("ThirdChurningCorpus.v1 must be an object")
    if envelope.get("schema_id") != "emergentism/ThirdChurningCorpus.v1":
        raise ValueError("wrong ThirdChurningCorpus schema ID")
    if envelope.get("release_id") != "THIRD-CHURNING-2026-08-23":
        raise ValueError("wrong Third Churning release ID")
    if envelope.get("frozen_source_commit") != FROZEN_COMMIT:
        raise ValueError("Third Churning frozen commit drift")
    if envelope.get("drop_ceiling") != 64:
        raise ValueError("Third Churning drop ceiling must remain 64")
    if envelope.get("pqa_launch_counts") != PQA_COUNTS:
        raise ValueError("PQA launch state must remain 54/0/0/0")
    if envelope.get("output_map") != SOURCE_OUTPUT_MAP:
        raise ValueError("Third Churning source output map drift")
    if envelope.get("predecessor_receipt") != (
        "90_ARCHIVE/2026_08_23_third_churning_predecessors/SUPERSESSION_RECEIPT.md"
    ):
        raise ValueError("Third Churning predecessor receipt drift")
    predecessor = ROOT / envelope["predecessor_receipt"]
    if not predecessor.is_file():
        raise ValueError("Third Churning predecessor receipt is missing")
    if envelope.get("license") != "CC BY-SA 4.0":
        raise ValueError("Third Churning license drift")
    if envelope.get("authorship") != "Yves R. Burri":
        raise ValueError("Third Churning authorship drift")
    require_text(envelope.get("ai_assistance"), "AI-assistance disclosure")
    states = envelope.get("external_states")
    if not isinstance(states, dict) or set(states) != {
        "deployed",
        "doi_archive",
        "github_release",
        "training_inclusion_guaranteed",
    }:
        raise ValueError("Third Churning external-state contract drift")
    if states["training_inclusion_guaranteed"] is not False:
        raise ValueError("training inclusion may never be guaranteed")
    if any(not isinstance(states[key], bool) for key in states):
        raise ValueError("external states must be booleans")

    schema_paths = envelope.get("schema_paths")
    expected_schema_paths = {
        "drop": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ChurningDrop.v1.schema.json",
        "problem": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ProblemAdjudication.v1.schema.json",
        "corpus": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ThirdChurningCorpus.v1.schema.json",
    }
    if schema_paths != expected_schema_paths:
        raise ValueError("Third Churning schema path bindings drift")
    expected_schema_ids = {
        "ChurningDrop.v1.schema.json": "https://emergentism.org/schemas/ChurningDrop.v1.schema.json",
        "ProblemAdjudication.v1.schema.json": "https://emergentism.org/schemas/ProblemAdjudication.v1.schema.json",
        "ThirdChurningCorpus.v1.schema.json": "https://emergentism.org/schemas/ThirdChurningCorpus.v1.schema.json",
    }
    for name, schema in schemas.items():
        if not isinstance(schema, dict) or schema.get("$id") != expected_schema_ids[name]:
            raise ValueError(f"schema identity drift: {name}")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"schema draft drift: {name}")

    if not isinstance(drops, list) or len(drops) != 51:
        raise ValueError("Third Churning must contain exactly 51 drop objects")
    drop_ids: list[str] = []
    class_counts = {"SURVIVOR_CANDIDATE": 0, "POISON_WARNING": 0}
    source_hash_rows = envelope.get("source_hashes")
    if not isinstance(source_hash_rows, list) or not source_hash_rows:
        raise ValueError("source hashes must be a non-empty list")
    manifest_hashes: dict[str, str] = {}
    for index, row in enumerate(source_hash_rows, start=1):
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "_sha256_scan"}:
            raise ValueError(f"source hash row {index} has invalid fields")
        path = safe_relative_path(row.get("path"), f"source hash row {index} path")
        digest = require_text(row.get("sha256"), f"source hash row {index} digest")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"source hash row {index} digest is malformed")
        if row.get("_sha256_scan") != "# pragma: allow-secret":
            raise ValueError(f"source hash row {index} checksum marker drift")
        if path in manifest_hashes:
            raise ValueError("source hash paths must be unique")
        manifest_hashes[path] = digest
    source_pathset = envelope.get("source_pathset")
    if not isinstance(source_pathset, list) or source_pathset != sorted(manifest_hashes):
        raise ValueError("source pathset and source hashes must agree exactly")
    for index, drop in enumerate(drops):
        if not isinstance(drop, dict) or set(drop) != DROP_KEYS:
            raise ValueError(f"drop {index + 1} does not match ChurningDrop.v1 fields")
        drop_id = require_text(drop.get("drop_id"), f"drop {index + 1} ID")
        if not re.fullmatch(r"TC-(AMR|HAL)-[0-9]{3}", drop_id):
            raise ValueError(f"invalid drop ID: {drop_id}")
        if drop.get("schema_id") != "emergentism/ChurningDrop.v1":
            raise ValueError(f"{drop_id}: wrong schema ID")
        require_text(drop.get("plain_name"), f"{drop_id} plain name")
        require_text(drop.get("proposition"), f"{drop_id} proposition")
        require_text(drop.get("scope"), f"{drop_id} scope")
        for field in (
            "strongest_rival",
            "discriminator",
            "kill_criterion",
            "cheapest_next_test",
            "survivor_if_killed",
            "residual_debt",
        ):
            require_text(drop.get(field), f"{drop_id} {field}")
        require_text_list(drop.get("assumptions"), f"{drop_id} assumptions")
        require_text_list(
            drop.get("linked_problem_ids"),
            f"{drop_id} linked problems",
            allow_empty=True,
        )
        classification = drop.get("classification")
        expected_alias = {
            "SURVIVOR_CANDIDATE": "AMRITA",
            "POISON_WARNING": "HALAHALA",
        }.get(classification)
        if expected_alias is None or drop.get("mythic_alias") != expected_alias:
            raise ValueError(f"{drop_id}: classification and mythic alias disagree")
        class_counts[classification] += 1
        if drop.get("evidence_tier") not in EVIDENCE_TIERS:
            raise ValueError(f"{drop_id}: unknown evidence tier")
        if drop.get("evidence_tier") in {"AMRITA", "HALAHALA"}:
            raise ValueError(f"{drop_id}: mythic alias cannot be an evidence tier")
        if drop.get("lifecycle") != "SOURCE_BOUND":
            raise ValueError(f"{drop_id}: launch lifecycle must remain SOURCE_BOUND")
        if not isinstance(drop.get("means_message"), dict) or set(drop["means_message"]) != MEANS_KEYS:
            raise ValueError(f"{drop_id}: means-message ledger drift")
        require_text_list(drop["means_message"].get("bearers"), f"{drop_id} bearers")
        for key in MEANS_KEYS - {"bearers"}:
            require_text(drop["means_message"].get(key), f"{drop_id} means {key}")
        if not isinstance(drop.get("ends_limits"), dict) or set(drop["ends_limits"]) != ENDS_KEYS:
            raise ValueError(f"{drop_id}: ends-limits ledger drift")
        for key in ENDS_KEYS:
            require_text(drop["ends_limits"].get(key), f"{drop_id} ends {key}")
        review = drop.get("earned_review")
        if review != {"state": "UNREVIEWED", "independent_review_count": 0, "receipts": []}:
            raise ValueError(f"{drop_id}: publication cannot create earned review")
        if not isinstance(drop.get("revision_history"), list) or not drop["revision_history"]:
            raise ValueError(f"{drop_id}: revision history is required")
        refs = drop.get("source_refs")
        if not isinstance(refs, list) or not refs:
            raise ValueError(f"{drop_id}: at least one source reference is required")
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError(f"{drop_id}: source references must be objects")
            path = safe_relative_path(ref.get("path"), f"{drop_id} source path")
            digest = require_text(ref.get("sha256"), f"{drop_id} source hash")
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError(f"{drop_id}: malformed source hash")
            if manifest_hashes.get(path) != digest:
                raise ValueError(f"{drop_id}: source reference is not envelope-bound")
            if ref.get("_sha256_scan") != "# pragma: allow-secret":
                raise ValueError(f"{drop_id}: source checksum marker drift")
            if ref.get("frozen_commit") not in {FROZEN_COMMIT, "POST_FREEZE_OWNER_DIRECTION"}:
                raise ValueError(f"{drop_id}: source commit binding drift")
            if ref.get("frozen_commit") == "POST_FREEZE_OWNER_DIRECTION":
                owner_path = ROOT / path
                actual = hashlib.sha256(owner_path.read_bytes()).hexdigest()
                if actual != digest:
                    raise ValueError(f"{drop_id}: post-freeze owner direction hash drift")
        drop_ids.append(drop_id)

    if len(set(drop_ids)) != 51 or envelope.get("drop_order") != drop_ids:
        raise ValueError("drop IDs must be unique and match the envelope order")
    if class_counts != {"SURVIVOR_CANDIDATE": 22, "POISON_WARNING": 29}:
        raise ValueError("classification counts must remain exactly 22/29")

    if not isinstance(problems, list) or len(problems) != 54:
        raise ValueError("Third Churning must contain exactly 54 problem objects")
    problem_ids: list[str] = []
    for index, problem in enumerate(problems):
        if not isinstance(problem, dict) or set(problem) != PROBLEM_KEYS:
            raise ValueError(f"problem {index + 1} does not match ProblemAdjudication.v1 fields")
        problem_id = require_text(problem.get("problem_id"), f"problem {index + 1} ID")
        if problem.get("schema_id") != "emergentism/ProblemAdjudication.v1":
            raise ValueError(f"{problem_id}: wrong problem schema ID")
        if problem.get("canonical_problem_id") != problem_id:
            raise ValueError(f"{problem_id}: canonical problem ID drift")
        if problem.get("proposed_effect") not in PROPOSED_EFFECTS:
            raise ValueError(f"{problem_id}: unknown proposed effect")
        if problem.get("earned_effect") != "NO_INCREMENT":
            raise ValueError(f"{problem_id}: earned effect must remain NO_INCREMENT")
        if problem.get("result_state") != "SELECTED":
            raise ValueError(f"{problem_id}: result state must remain SELECTED")
        if problem.get("native_reviews") != []:
            raise ValueError(f"{problem_id}: native reviews must remain empty")
        for field in (
            "domain",
            "family",
            "native_problem",
            "native_reference",
            "proposed_answer",
            "strongest_rival",
            "native_frame_control",
            "generic_decomposition_control",
            "discriminator",
            "kill_criterion",
            "remaining_debt",
            "survivor_if_killed",
        ):
            require_text(problem.get(field), f"{problem_id} {field}")
        require_text_list(problem.get("assumptions"), f"{problem_id} assumptions")
        require_text_list(problem.get("aliases"), f"{problem_id} aliases", allow_empty=True)
        require_text_list(
            problem.get("linked_drop_ids"),
            f"{problem_id} linked drops",
            allow_empty=True,
        )
        problem_ids.append(problem_id)
    if len(set(problem_ids)) != 54 or envelope.get("problem_order") != problem_ids:
        raise ValueError("problem IDs must be unique and match the envelope order")

    if not isinstance(paradoxes, dict) or paradoxes.get("schema_id") != "emergentism/ParadoxInventory.v1":
        raise ValueError("wrong ParadoxInventory schema ID")
    if paradoxes.get("frozen_source_commit") != FROZEN_COMMIT:
        raise ValueError("paradox inventory frozen commit drift")
    expected_paradox_counts = {
        "formal": 9,
        "legacy": 21,
        "synthesis": 4,
        "legacy_dissolved": 0,
    }
    if paradoxes.get("counts") != expected_paradox_counts:
        raise ValueError("paradox inventory counts drift")
    rows = paradoxes.get("rows")
    if not isinstance(rows, list) or len(rows) != 34:
        raise ValueError("paradox inventory must contain exactly 34 rows")
    inventory_ids: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"paradox row {index + 1} must be an object")
        for field in (
            "inventory_id",
            "kind",
            "title",
            "canonical_problem_id",
            "proposed_state",
            "earned_state",
            "residual",
            "source_path",
        ):
            require_text(row.get(field), f"paradox row {index + 1} {field}")
        inventory_ids.append(row["inventory_id"])
    if len(set(inventory_ids)) != 34:
        raise ValueError("paradox inventory IDs must be unique")
    require_text(paradoxes.get("boundary"), "paradox inventory boundary")

    return drops, problems, paradoxes, envelope


def html_list(values: list[object], *, empty: str = "None declared.") -> str:
    if not values:
        return f"<p>{esc(empty)}</p>"
    return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def html_mapping(mapping: dict[str, Any]) -> str:
    parts = ["<dl class=\"g2-definition-list\">"]
    for key, value in mapping.items():
        label = key.replace("_", " ").capitalize()
        if isinstance(value, list):
            rendered = html_list(value)
        elif isinstance(value, bool) or value is None:
            rendered = f"<code>{esc(json.dumps(value))}</code>"
        else:
            rendered = esc(value)
        parts.append(f"<dt>{esc(label)}</dt><dd>{rendered}</dd>")
    parts.append("</dl>")
    return "".join(parts)


def source_refs_html(refs: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for ref in refs:
        claims = ref.get("claim_ids", [])
        claims_html = f"<br /><strong>Claim IDs:</strong> {esc(', '.join(claims))}" if claims else ""
        rows.append(
            "<li>"
            f"<strong>Path:</strong> <code>{esc(ref['path'])}</code><br />"
            f"<strong>SHA-256:</strong> <code>{esc(ref['sha256'])}</code><br />"
            f"<strong>Source state:</strong> <code>{esc(ref['frozen_commit'])}</code>"
            f"{claims_html}</li>"
        )
    return "<ul>" + "".join(rows) + "</ul>"


def drop_card(drop: dict[str, Any], *, heading: str = "h2") -> str:
    survivor = drop["classification"] == "SURVIVOR_CANDIDATE"
    variant = "survivor" if survivor else "poison"
    plain_class = "Survivor candidate" if survivor else "Refutation or warning"
    alias = "Amrita" if survivor else "Hālāhala"
    review = drop["earned_review"]
    revisions = [f"{row['date']} — {row['event']}" for row in drop["revision_history"]]
    return f'''<article class="g2-drop g2-drop--{variant}" id="{esc(drop['drop_id'].lower())}" data-classification="{esc(drop['classification'])}">
  <p class="g2-drop__meta">{esc(drop['drop_id'])} · {esc(plain_class)} · Evidence tier {esc(drop['evidence_tier'])} · {esc(drop['lifecycle'])}</p>
  <{heading}>{esc(drop['plain_name'])}</{heading}>
  <p>{esc(drop['proposition'])}</p>
  <div class="g2-drop__grid">
    <p><strong>Plain classification:</strong> {esc(plain_class)}<br /><strong>Optional mythic alias:</strong> {esc(alias)}</p>
    <p><strong>Earned review:</strong> {esc(review['state'])}<br /><strong>Independent reviews:</strong> {esc(review['independent_review_count'])}</p>
    <p><strong>Scope:</strong> {esc(drop['scope'])}</p>
    <p><strong>Linked problems:</strong> {esc(', '.join(drop['linked_problem_ids']) or 'None declared')}</p>
  </div>
  <details>
    <summary>Sources, rival, kill, residual, bearers, horizons, and revision</summary>
    <h3>Assumptions</h3>{html_list(drop['assumptions'])}
    <h3>Source custody</h3>{source_refs_html(drop['source_refs'])}
    <h3>Adversarial account</h3>
    <p><strong>Strongest rival:</strong> {esc(drop['strongest_rival'])}</p>
    <p><strong>Discriminator:</strong> {esc(drop['discriminator'])}</p>
    <p><strong>Kill criterion:</strong> {esc(drop['kill_criterion'])}</p>
    <p><strong>Cheapest next test:</strong> {esc(drop['cheapest_next_test'])}</p>
    <p><strong>What survives if killed:</strong> {esc(drop['survivor_if_killed'])}</p>
    <p><strong>Residual debt:</strong> {esc(drop['residual_debt'])}</p>
    <h3>The means is the message</h3>{html_mapping(drop['means_message'])}
    <h3>The ends are the limits</h3>{html_mapping(drop['ends_limits'])}
    <h3>Revision history</h3>{html_list(revisions)}
  </details>
</article>'''


def problem_card(problem: dict[str, Any]) -> str:
    return f'''<article class="g2-drop" id="{esc(problem['problem_id'].lower())}">
  <p class="g2-drop__meta">{esc(problem['problem_id'])} · {esc(problem['domain'])} · {esc(problem['family'])}</p>
  <h3>{esc(problem['native_problem'])}</h3>
  <p><strong>Native reference:</strong> {esc(problem['native_reference'])}</p>
  <div class="g2-drop__grid">
    <p><strong>Proposed effect:</strong> <code>{esc(problem['proposed_effect'])}</code><br /><strong>Proposed answer:</strong> {esc(problem['proposed_answer'])}</p>
    <p><strong>Earned effect:</strong> <code>{esc(problem['earned_effect'])}</code><br /><strong>Result state:</strong> <code>{esc(problem['result_state'])}</code><br /><strong>Native reviews:</strong> 0</p>
    <p><strong>Remaining debt:</strong> {esc(problem['remaining_debt'])}</p>
    <p><strong>What survives if killed:</strong> {esc(problem['survivor_if_killed'])}</p>
  </div>
  <details>
    <summary>Assumptions, controls, rival, discriminator, and kill</summary>
    <h4>Assumptions</h4>{html_list(problem['assumptions'])}
    <p><strong>Aliases:</strong> {esc(', '.join(problem['aliases']) or 'None declared')}</p>
    <p><strong>Strongest rival:</strong> {esc(problem['strongest_rival'])}</p>
    <p><strong>Native-frame control:</strong> {esc(problem['native_frame_control'])}</p>
    <p><strong>Generic-decomposition control:</strong> {esc(problem['generic_decomposition_control'])}</p>
    <p><strong>Discriminator:</strong> {esc(problem['discriminator'])}</p>
    <p><strong>Kill criterion:</strong> {esc(problem['kill_criterion'])}</p>
    <p><strong>Linked drops:</strong> {esc(', '.join(problem['linked_drop_ids']) or 'None declared')}</p>
  </details>
</article>'''


def paradox_card(row: dict[str, Any]) -> str:
    return f'''<article class="g2-panel">
  <p class="g2-drop__meta">{esc(row['inventory_id'])} · {esc(row['kind'])}</p>
  <h3>{esc(row['title'])}</h3>
  <p><strong>Canonical target:</strong> {esc(row['canonical_problem_id'])}</p>
  <p><strong>Proposed state:</strong> <code>{esc(row['proposed_state'])}</code></p>
  <p><strong>Earned state:</strong> <code>{esc(row['earned_state'])}</code></p>
  <p><strong>Residual:</strong> {esc(row['residual'])}</p>
  <p><strong>Source:</strong> <code>{esc(row['source_path'])}</code></p>
</article>'''


def churning_seam() -> str:
    steps = (
        ("Freeze", "one Git state"),
        ("Source", "path and hash"),
        ("Tier", "warrant retained"),
        ("Rival", "serious alternative"),
        ("Kill", "failure condition"),
        ("Residual", "debt survives"),
        ("Bearers", "means and horizon"),
    )
    track = "".join(
        f'<li class="g2-churn-step" data-step="{index:02d}"><strong>{esc(name)}</strong><span>{esc(note)}</span></li>'
        for index, (name, note) in enumerate(steps, start=1)
    )
    return f'''<figure class="g2-churn-seam" aria-labelledby="churn-seam-title churn-seam-desc">
  <figcaption><strong id="churn-seam-title">The audit seam</strong><span id="churn-seam-desc">One source-bound method; two provisional branches.</span></figcaption>
  <ol class="g2-churn-seam__track">{track}</ol>
  <div class="g2-churn-branch">
    <article class="g2-churn-branch--survivor"><span>Plain classification first</span><h3>Survivor candidates</h3><p><strong>Amrita</strong> is the optional mythic alias. Twenty-two propositions survived this source, tier, rival, kill, and residual pass. They are not eternal truths or earned independent results.</p></article>
    <article class="g2-churn-branch--poison"><span>Plain classification first</span><h3>Refutations and warnings</h3><p><strong>Hālāhala</strong> is the optional mythic alias. Twenty-nine reusable warnings preserve failure, danger, survivor, and repair paths. A warning is not an evidence tier and never labels a person.</p></article>
  </div>
</figure>'''


def page_document(
    *,
    title: str,
    description: str,
    canonical: str,
    active: str,
    main: str,
    robots: str | None = None,
    q4_status: str | None = None,
) -> str:
    robots_meta = (
        f'  <meta name="robots" content="{esc(robots)}" />\n' if robots else ""
    )
    q4_meta = (
        f'  <meta name="emergentism:status" content="{esc(q4_status.lower())}; '
        'not warranted; ruling Q4 2026-07-31" />\n'
        if q4_status
        else ""
    )
    q4_declaration = (
        '<aside class="q4decl g2-note" aria-label="Publication declaration">'
        f'<strong>{esc(q4_status)}</strong> — this page is reachable, indexable and '
        'registered. The corpus does not warrant what it claims; a coherence test is '
        'not a capability test. Ruling Q4, signed 2026-07-31.'
        '</aside>\n'
        if q4_status
        else ""
    )
    base = f'''<!doctype html>
<html lang="en" data-gestalt="v2">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="theme-color" content="#07090f" />
{robots_meta}{q4_meta}  <link rel="canonical" href="{esc(canonical)}" />
  <link rel="stylesheet" href="/assets/css/gestalt-v2.css" />
<!--OG:AUTO-->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:url" content="{esc(canonical)}" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<!--/OG:AUTO-->
</head>
<body class="g2-page">
{q4_declaration}<main id="main" class="g2-main" tabindex="-1">
{main}
</main>
</body>
</html>
'''
    rendered = render_page(
        base,
        active,
        surface=surface_for("churn/index.html"),
    ).replace(SCRIPT_TAG, "")
    if re.search(r"<script\b", rendered, flags=re.IGNORECASE):
        raise ValueError(f"static no-JavaScript contract failed for {canonical}")
    return rendered


def drop_ledger(drops: list[dict[str, Any]], *, heading: str = "h2") -> str:
    return '<div class="g2-drop-ledger">' + "\n".join(
        drop_card(drop, heading=heading) for drop in drops
    ) + "</div>"


def churn_main(drops: list[dict[str, Any]]) -> str:
    return f'''  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">Research ledger · frozen 2026-08-23</p>
    <h1>The Third Churning</h1>
    <p class="g2-page-hero__lede">What survives a disciplined attempt to refute it? Every atomic proposition keeps its source, evidence tier, serious rival, discriminator, kill criterion, residual debt, affected bearers, and responsible horizons.</p>
    <div class="g2-page-meta"><span>22 survivor candidates</span><span>29 refutations and warnings</span><span>{esc(PQA_STATUS)}</span></div>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="#ledger">Read all 51 drops</a><a class="g2-button" href="/record/churning/">Audit custody</a><a class="g2-button" href="/churn/corpus.json">JSON corpus</a><a class="g2-button" href="/churn/corpus.md">Markdown corpus</a></div>
  </header>

  <section class="g2-shell g2-section" aria-labelledby="churn-method-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">01 · One method</p><h2 id="churn-method-title">Freeze, attack, preserve.</h2></div><p class="g2-section__intro">Classification is provisional. Publication does not create earned review.</p></div>
    {churning_seam()}
    <blockquote class="g2-churn-maxim"><p>{esc(MAXIM)}</p><footer>OS01-42 · selected methodological and ethical maxim [D], not a theorem or permission</footer></blockquote>
    <p class="g2-note"><strong>Reading rule:</strong> “survivor candidate” and “refutation or warning” are proposed classifications at one source snapshot. They are not evidence tiers. Amrita and Hālāhala are optional aliases, never truth grades or labels for people.</p>
  </section>

  <section class="g2-shell g2-section" id="ledger" aria-labelledby="churn-ledger-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">02 · Full atomic ledger</p><h2 id="churn-ledger-title">22 survivor candidates · 29 refutations and warnings</h2></div><p class="g2-section__intro">All 51 source-bound records are present in the static page.</p></div>
    {drop_ledger(drops)}
  </section>

  <section class="g2-shell g2-section" aria-labelledby="churn-contact-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">03 · World contact</p><h2 id="churn-contact-title">The public denominator can make the framework lose.</h2></div><p class="g2-section__intro">{esc(PQA_STATUS)}.</p></div>
    <p>No philosophical result is earned until the native problem and premises survive, serious controls are tested, the kill remains unfired, and two independent native-domain reviewers agree. Public availability cannot guarantee crawling, indexing, citation, or inclusion in any future AI training run.</p>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="/questions/">Open PQA-54</a><a class="g2-button" href="/amrita/">Survivor candidates</a><a class="g2-button" href="/halahala/">Refutations and warnings</a><a class="g2-button" href="/exit/">Exit</a></div>
  </section>'''


def branch_main(drops: list[dict[str, Any]], *, survivor: bool) -> str:
    if survivor:
        title = "Survivor candidates (Amrita)"
        kicker = "What survived scrutiny · source-bound candidates"
        lede = (
            "Amrita is the optional mythic alias for a survivor candidate. Each proposition "
            "remained coherent after this release’s source, tier, rival, kill, residual, "
            "bearer, and horizon checks."
        )
        note = (
            "Survival here does not mean proven forever, independently reviewed, "
            "scientifically validated, or safe in every domain. Publication does not "
            "create earned review."
        )
    else:
        title = "Refutations and warnings (Hālāhala)"
        kicker = "What failed or remains dangerous · preserved, not erased"
        lede = (
            "Hālāhala is the optional mythic alias for a refutation or reusable warning. "
            "These records preserve type collisions, overclaims, smuggled mechanisms, "
            "hidden bearers, false closure, and their repair paths."
        )
        note = (
            "A warning is not an evidence tier and never labels a person. Each warning "
            "retains a rival, discriminator, kill criterion, survivor, and residual debt."
        )
    return f'''  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">{esc(kicker)}</p>
    <h1>{esc(title)}</h1>
    <p class="g2-page-hero__lede">{esc(lede)}</p>
    <div class="g2-page-meta"><span>{len(drops)} records</span><span>SOURCE_BOUND</span><span>0 independent reviews</span></div>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="#ledger">Read every record</a><a class="g2-button" href="/churn/">Full Churning</a><a class="g2-button" href="/record/churning/">Audit custody</a></div>
  </header>

  <section class="g2-shell g2-section" aria-labelledby="branch-rule-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Reading rule</p><h2 id="branch-rule-title">Plain function before mythic alias.</h2></div><p class="g2-section__intro">Evidence tiers remain attached and separate.</p></div>
    <p class="g2-note">{esc(note)}</p>
    <blockquote class="g2-churn-maxim"><p>{esc(MAXIM)}</p><footer>OS01-42 · chosen maxim [D]; never an analytic or empirical proof</footer></blockquote>
  </section>

  <section class="g2-shell g2-section" id="ledger" aria-labelledby="branch-ledger-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Full source-bound ledger</p><h2 id="branch-ledger-title">{esc(title)}</h2></div><p class="g2-section__intro">All source strings are statically rendered; JavaScript is not required.</p></div>
    {drop_ledger(drops)}
  </section>

  <section class="g2-shell g2-section" aria-labelledby="branch-exit-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Challenge and Exit</p><h2 id="branch-exit-title">Every classification remains revisable.</h2></div><p class="g2-section__intro">A killed claim leaves its named survivor and native domain intact.</p></div>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="/contribute/">Submit a challenge</a><a class="g2-button" href="/churn/corpus.json">Download JSON</a><a class="g2-button" href="/exit/">Exit</a></div>
  </section>'''


def record_main(
    envelope: dict[str, Any],
    problems: list[dict[str, Any]],
    paradoxes: dict[str, Any],
) -> str:
    source_rows = "".join(
        f'''<li><code>{esc(row['path'])}</code><br /><strong>SHA-256:</strong> <code>{esc(row['sha256'])}</code></li>'''
        for row in envelope["source_hashes"]
    )
    output_rows = "".join(
        f"<dt>{esc(key.replace('_', ' ').capitalize())}</dt><dd><code>{esc(value)}</code></dd>"
        for key, value in envelope["output_map"].items()
    )
    problem_rows = "\n".join(problem_card(problem) for problem in problems)
    paradox_rows = "\n".join(paradox_card(row) for row in paradoxes["rows"])
    schema_links = "".join(
        f'<a class="g2-button" href="/churn/schemas/{esc(name)}">{esc(name)}</a>'
        for name in SCHEMA_SOURCES
    )
    states = envelope["external_states"]
    return f'''  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">Custody · method · null-state record</p>
    <h1>Third Churning custody record</h1>
    <p class="g2-page-hero__lede">This record binds the frozen source state, exact ordering, schemas, predecessor receipt, proposed classifications, unresolved PQA denominator, and public projections without promoting any proposition.</p>
    <div class="g2-page-meta"><span>{esc(envelope['release_id'])}</span><span>Record boundary [D] · conjectures [C]</span><span>22 survivor candidates</span><span>29 refutations and warnings</span><span>{esc(PQA_STATUS)}</span></div>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="#custody">Inspect custody</a><a class="g2-button" href="/churn/">Read the ledger</a><a class="g2-button" href="/churn/manifest.json">Machine manifest</a></div>
  </header>

  <section class="g2-shell g2-section" id="custody" aria-labelledby="custody-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">01 · Non-semantic envelope</p><h2 id="custody-title">Custody binds bytes. It does not make propositions true.</h2></div><p class="g2-section__intro">Frozen source commit <code>{esc(envelope['frozen_source_commit'])}</code>.</p></div>
    <div class="g2-practice-grid"><article class="g2-panel"><span class="g2-claim-id">Authorship</span><h3>{esc(envelope['authorship'])}</h3><p>{esc(envelope['ai_assistance'])}</p></article><article class="g2-panel"><span class="g2-claim-id">License</span><h3>{esc(envelope['license'])}</h3><p>Release date: {esc(envelope['date'])}. Drop ceiling: {esc(envelope['drop_ceiling'])}.</p></article><article class="g2-panel"><span class="g2-claim-id">Predecessor receipt</span><h3>Preserved before promotion</h3><p><code>{esc(envelope['predecessor_receipt'])}</code></p></article></div>
    <h3>Source pathset and SHA-256 bindings</h3><ol>{source_rows}</ol>
    <h3>Canonical public output map</h3><dl class="g2-definition-list">{output_rows}</dl>
    <h3>Byte-identical schema copies</h3><div class="g2-corpus-actions">{schema_links}</div>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="states-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">02 · External-state boundary</p><h2 id="states-title">A local build does not create an external fact.</h2></div><p class="g2-section__intro">No inclusion in any future AI training run is guaranteed.</p></div>
    {html_mapping(states)}
    <p class="g2-note">The envelope records <code>training_inclusion_guaranteed=false</code>. This is not evidence about an external crawler, index, citation graph, model corpus, DOI archive, release host, or deployment. OS01-44 keeps that negative boundary visible.</p>
  </section>

  <section class="g2-shell g2-section" id="pqa" aria-labelledby="pqa-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">03 · Problem adjudication ledger</p><h2 id="pqa-title">{esc(PQA_STATUS)}</h2></div><p class="g2-section__intro">A proposed answer and proposed effect are not earned resolution.</p></div>
    <p class="g2-note">All 54 records remain <code>SELECTED</code> with earned effect <code>NO_INCREMENT</code> and zero native reviews. OS01-43 forbids selection, clarification, reframing, or publication from silently incrementing the result.</p>
    <div class="g2-drop-ledger">{problem_rows}</div>
  </section>

  <section class="g2-shell g2-section" id="paradoxes" aria-labelledby="paradoxes-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">04 · Paradox inventory</p><h2 id="paradoxes-title">Inventory and proposed effects are not earned dissolution.</h2></div><p class="g2-section__intro">9 formal · 21 legacy · 4 synthesis · 0 of 21 legacy dissolutions earned.</p></div>
    <p>{esc(paradoxes['boundary'])}</p>
    <div class="g2-practice-grid">{paradox_rows}</div>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="exports-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">05 · Deterministic exports</p><h2 id="exports-title">One source packet, inspectable projections.</h2></div><p class="g2-section__intro">JSONL contains 51 typed drops, 54 typed problem records, one typed paradox inventory, and one typed custody envelope.</p></div>
    <div class="g2-corpus-actions"><a class="g2-button g2-button--primary" href="/churn/corpus.json">Drop corpus JSON</a><a class="g2-button" href="/churn/corpus.jsonl">All records JSONL</a><a class="g2-button" href="/churn/problems.json">Problems JSON</a><a class="g2-button" href="/churn/paradoxes.json">Paradoxes JSON</a><a class="g2-button" href="/churn/corpus.md">Markdown</a><a class="g2-button" href="/exit/">Exit</a></div>
  </section>'''


def corpus_markdown(drops: list[dict[str, Any]], envelope: dict[str, Any]) -> str:
    lines = [
        "# The Third Churning — atomic corpus",
        "",
        f"- Release: `{md_esc(envelope['release_id'])}`",
        f"- Frozen source commit: `{md_esc(envelope['frozen_source_commit'])}`",
        "- Counts: **22 survivor candidates · 29 refutations and warnings**",
        f"- PQA: **{md_esc(PQA_STATUS)}**",
        "- Earned review: **none at launch**",
        "",
        f"> {md_esc(MAXIM)}",
        "",
        "Survivor candidate and refutation or warning are provisional classifications, not evidence tiers. Amrita and Hālāhala are optional aliases. Publication does not create earned review. No inclusion in any future AI training run is guaranteed.",
        "",
    ]
    for drop in drops:
        survivor = drop["classification"] == "SURVIVOR_CANDIDATE"
        plain_class = "Survivor candidate" if survivor else "Refutation or warning"
        alias = "Amrita" if survivor else "Hālāhala"
        lines.extend(
            [
                f"## {md_esc(drop['drop_id'])} — {md_esc(drop['plain_name'])}",
                "",
                f"- Plain classification: **{md_esc(plain_class)}**",
                f"- Optional mythic alias: {md_esc(alias)}",
                f"- Evidence tier: `{md_esc(drop['evidence_tier'])}`",
                f"- Lifecycle: `{md_esc(drop['lifecycle'])}`",
                f"- Scope: {md_esc(drop['scope'])}",
                f"- Proposition: {md_esc(drop['proposition'])}",
                f"- Assumptions: {'; '.join(md_esc(value) for value in drop['assumptions'])}",
                f"- Strongest rival: {md_esc(drop['strongest_rival'])}",
                f"- Discriminator: {md_esc(drop['discriminator'])}",
                f"- Kill criterion: {md_esc(drop['kill_criterion'])}",
                f"- Cheapest next test: {md_esc(drop['cheapest_next_test'])}",
                f"- What survives if killed: {md_esc(drop['survivor_if_killed'])}",
                f"- Residual debt: {md_esc(drop['residual_debt'])}",
                f"- Linked problems: {', '.join(md_esc(value) for value in drop['linked_problem_ids']) or 'None declared'}",
                f"- Earned review: `{md_esc(drop['earned_review']['state'])}`; 0 independent reviews; no receipts",
                "",
                "### Sources",
                "",
            ]
        )
        for ref in drop["source_refs"]:
            claims = ", ".join(md_esc(value) for value in ref.get("claim_ids", []))
            suffix = f"; claims {claims}" if claims else ""
            lines.append(
                f"- `{md_esc(ref['path'])}` — SHA-256 `{md_esc(ref['sha256'])}` — source state `{md_esc(ref['frozen_commit'])}`{suffix}"
            )
        lines.extend(["", "### The means is the message", ""])
        for key, value in drop["means_message"].items():
            rendered = "; ".join(md_esc(item) for item in value) if isinstance(value, list) else md_esc(value)
            lines.append(f"- {md_esc(key.replace('_', ' ').capitalize())}: {rendered}")
        lines.extend(["", "### The ends are the limits", ""])
        for key, value in drop["ends_limits"].items():
            lines.append(f"- {md_esc(key.replace('_', ' ').capitalize())}: {md_esc(value)}")
        lines.extend(["", "### Revision history", ""])
        for row in drop["revision_history"]:
            lines.append(f"- {md_esc(row['date'])}: {md_esc(row['event'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def compatibility_alias(drops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Preserve the old array carrier without preserving its tier conflation."""

    rows: list[dict[str, Any]] = []
    for drop in drops:
        survivor = drop["classification"] == "SURVIVOR_CANDIDATE"
        rows.append(
            {
                "id": drop["drop_id"],
                "classification": drop["classification"],
                "group": "nectar" if survivor else "halahala",
                "tier": drop["evidence_tier"],
                "title": drop["plain_name"],
                "body": drop["proposition"],
                "source": drop["source_refs"][0]["path"],
                "route": "churn",
                "mythic_alias": drop["mythic_alias"],
                "earned_review": drop["earned_review"]["state"],
            }
        )
    return rows


def jsonl_projection(
    drops: list[dict[str, Any]],
    problems: list[dict[str, Any]],
    paradoxes: dict[str, Any],
    envelope: dict[str, Any],
) -> bytes:
    records: list[object] = [*drops, *problems, paradoxes, envelope]
    return (
        "\n".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for record in records
        )
        + "\n"
    ).encode("utf-8")


def build_outputs() -> dict[Path, bytes]:
    source_bytes = {
        "drops": DROP_SOURCE.read_bytes(),
        "problems": PROBLEM_SOURCE.read_bytes(),
        "paradoxes": PARADOX_SOURCE.read_bytes(),
        "envelope": ENVELOPE_SOURCE.read_bytes(),
    }
    drops_raw = load_json(DROP_SOURCE)
    problems_raw = load_json(PROBLEM_SOURCE)
    paradoxes_raw = load_json(PARADOX_SOURCE)
    envelope_raw = load_json(ENVELOPE_SOURCE)
    schema_bytes = {name: path.read_bytes() for name, path in SCHEMA_SOURCES.items()}
    schemas = {name: load_json(path) for name, path in SCHEMA_SOURCES.items()}
    drops, problems, paradoxes, envelope = validate_inputs(
        envelope_raw, drops_raw, problems_raw, paradoxes_raw, schemas
    )
    survivors = [drop for drop in drops if drop["classification"] == "SURVIVOR_CANDIDATE"]
    warnings = [drop for drop in drops if drop["classification"] == "POISON_WARNING"]

    outputs: dict[Path, bytes] = {
        SITE / "churn" / "index.html": page_document(
            title="The Third Churning — proposition by proposition",
            description="A source-bound ledger of 22 survivor candidates, 29 refutations and warnings, their rivals, kills, residuals, bearers, and horizons.",
            canonical="https://emergentism.org/churn/",
            active="research",
            main=churn_main(drops),
        ).encode("utf-8"),
        SITE / "amrita" / "index.html": page_document(
            title="Survivor candidates (Amrita) — The Third Churning",
            description="Twenty-two source-bound survivor candidates with evidence tiers, rivals, kill criteria, residual debt, bearers, and horizons.",
            canonical="https://emergentism.org/amrita/",
            active="research",
            main=branch_main(survivors, survivor=True),
            robots="index, follow",
            q4_status="DECLARED-PROVISIONAL",
        ).encode("utf-8"),
        SITE / "halahala" / "index.html": page_document(
            title="Refutations and warnings (Hālāhala) — The Third Churning",
            description="Twenty-nine source-bound refutations and reusable warnings with repair routes and named survivors.",
            canonical="https://emergentism.org/halahala/",
            active="research",
            main=branch_main(warnings, survivor=False),
        ).encode("utf-8"),
        SITE / "record" / "churning" / "index.html": page_document(
            title="Third Churning custody record",
            description="The frozen sources, exact 22/29 classifications, PQA 54/0/0/0 null state, schemas, problems, paradoxes, and external-state boundary.",
            canonical="https://emergentism.org/record/churning/",
            active="research",
            main=record_main(envelope, problems, paradoxes),
        ).encode("utf-8"),
        SITE / "churn" / "corpus.json": source_bytes["drops"],
        SITE / "churn" / "corpus.jsonl": jsonl_projection(
            drops, problems, paradoxes, envelope
        ),
        SITE / "churn" / "corpus.md": corpus_markdown(drops, envelope).encode("utf-8"),
        SITE / "churn" / "problems.json": source_bytes["problems"],
        SITE / "churn" / "paradoxes.json": source_bytes["paradoxes"],
        SITE / "churn" / "manifest.json": source_bytes["envelope"],
        SITE / "amrita" / "amrita.json": pretty_json(compatibility_alias(survivors)),
    }
    for name, payload in schema_bytes.items():
        outputs[SITE / "churn" / "schemas" / name] = payload

    expected = {
        SITE / "churn" / "index.html",
        SITE / "amrita" / "index.html",
        SITE / "halahala" / "index.html",
        SITE / "record" / "churning" / "index.html",
        SITE / "churn" / "corpus.json",
        SITE / "churn" / "corpus.jsonl",
        SITE / "churn" / "corpus.md",
        SITE / "churn" / "problems.json",
        SITE / "churn" / "paradoxes.json",
        SITE / "churn" / "manifest.json",
        SITE / "churn" / "schemas" / "ChurningDrop.v1.schema.json",
        SITE / "churn" / "schemas" / "ProblemAdjudication.v1.schema.json",
        SITE / "churn" / "schemas" / "ThirdChurningCorpus.v1.schema.json",
        SITE / "amrita" / "amrita.json",
    }
    if set(outputs) != expected:
        raise ValueError("public Third Churning output ownership drift")
    if len(outputs) != 14:
        raise ValueError("public Third Churning output count must remain 14")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify all outputs without writing")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"THIRD CHURNING PUBLIC: FAIL\n- {exc}")
        return 1

    drift: list[str] = []
    for path, payload in outputs.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                drift.append(path.relative_to(SITE).as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.read_bytes() != payload:
            path.write_bytes(payload)

    if drift:
        print("THIRD CHURNING PUBLIC: FAIL")
        for relative in drift:
            print(f"- deterministic drift: {relative}")
        return 1
    mode = "clean" if args.check else "rendered"
    print(
        "THIRD CHURNING PUBLIC: PASS · 22 survivor candidates · "
        f"29 refutations and warnings · 54/0/0/0 · 14 outputs · {mode}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

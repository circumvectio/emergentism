#!/usr/bin/env python3
"""Deterministically render the typed Burri Rules proof plate and emblem.

The JSON topology is a non-authoritative, machine-readable mirror of the
Markdown owners.  This renderer deliberately uses only the Python standard
library and emits self-contained SVG: no clocks, scripts, animation, external
fonts, or external assets.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TOPOLOGY = REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_TOPOLOGY.json"

RULE_IDS = {f"BR-{number}" for number in range(1, 7)}
REGISTERS = {f"D{number}" for number in range(7)}
KINDS = {"state", "frame", "crossing", "commitment", "receipt", "trace"}
MODALITIES = {"actual", "possible"}
ROLES = {"forward", "feedback", "coupling"}
TIERS = {"A", "B", "S", "I", "D", "C"}
FROZEN_SOURCE_PARTS = {"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"}


def load_topology(path: Path | str = DEFAULT_TOPOLOGY) -> dict[str, Any]:
    """Load a topology object without mutating it."""

    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("topology root must be an object")
    return value


def topology_sha256(path: Path | str = DEFAULT_TOPOLOGY) -> str:
    """Return the SHA-256 of the exact topology bytes embedded in each SVG."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _schema(topology: Mapping[str, Any], schema_id: str) -> Mapping[str, Any]:
    for schema in topology.get("schemas", []):
        if schema.get("id") == schema_id:
            return schema
    return {}


def validate_topology(
    topology: Mapping[str, Any], repo_root: Path | str = REPO_ROOT
) -> list[str]:
    """Return every deterministic contract violation found in ``topology``."""

    errors: list[str] = []
    root = Path(repo_root)
    required = {"schemaVersion", "rules", "sources", "nodes", "edges", "views"}
    missing = sorted(required - set(topology))
    if missing:
        errors.append(f"missing top-level keys: {', '.join(missing)}")

    rules = topology.get("rules", [])
    rule_ids = [item.get("id") for item in rules if isinstance(item, Mapping)]
    if set(rule_ids) != RULE_IDS or len(rule_ids) != len(RULE_IDS):
        errors.append("rules must be exactly BR-1 through BR-6")

    sources = topology.get("sources", [])
    source_ids = [item.get("id") for item in sources if isinstance(item, Mapping)]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source ids must be unique")
    for source in sources:
        if not isinstance(source, Mapping):
            errors.append("each source must be an object")
            continue
        if source.get("tier") not in TIERS:
            errors.append(f"source {source.get('id')} has invalid tier")
        if "path" in source:
            path = Path(str(source["path"]))
            if path.is_absolute():
                errors.append(f"source {source.get('id')} path must be relative")
            if FROZEN_SOURCE_PARTS & set(path.parts):
                errors.append(f"source {source.get('id')} uses a frozen tree")
            if not (root / path).is_file():
                errors.append(f"source {source.get('id')} does not exist: {path}")
        elif not str(source.get("url", "")).startswith("https://"):
            errors.append(f"source {source.get('id')} needs a local path or HTTPS URL")

    nodes = topology.get("nodes", [])
    edges = topology.get("edges", [])
    elements = [*nodes, *edges]
    element_ids = [item.get("id") for item in elements if isinstance(item, Mapping)]
    if len(element_ids) != len(set(element_ids)):
        errors.append("graph element ids must be globally unique")
    node_ids = {item.get("id") for item in nodes if isinstance(item, Mapping)}
    source_id_set = set(source_ids)

    for node in nodes:
        node_id = node.get("id", "<missing>")
        if node.get("kind") not in KINDS:
            errors.append(f"node {node_id} has invalid kind")
        if node.get("dRegister") not in REGISTERS:
            errors.append(f"node {node_id} has invalid dRegister")
        if node.get("modality") not in MODALITIES:
            errors.append(f"node {node_id} has invalid modality")
        if node.get("role") not in ROLES:
            errors.append(f"node {node_id} has invalid role")
        if node.get("tier") not in TIERS:
            errors.append(f"node {node_id} has invalid tier")
        if not node.get("ruleIds") or not set(node.get("ruleIds", [])) <= RULE_IDS:
            errors.append(f"node {node_id} has invalid ruleIds")
        if not node.get("sourceIds") or not set(node.get("sourceIds", [])) <= source_id_set:
            errors.append(f"node {node_id} has invalid sourceIds")
        if not isinstance(node.get("x"), (int, float)) or not isinstance(
            node.get("y"), (int, float)
        ):
            errors.append(f"node {node_id} needs numeric geometry")
        register = node.get("dRegister")
        modality = node.get("modality")
        if register == "D4" and modality != "actual":
            errors.append(f"node {node_id}: every D4 element must be actual")
        if register == "D5" and modality != "possible":
            errors.append(f"node {node_id}: every D5 element must be possible")

    for edge in edges:
        edge_id = edge.get("id", "<missing>")
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            errors.append(f"edge {edge_id} has an unknown endpoint")
        if edge.get("dRegister") not in REGISTERS:
            errors.append(f"edge {edge_id} has invalid dRegister")
        if edge.get("modality") not in MODALITIES:
            errors.append(f"edge {edge_id} has invalid modality")
        if edge.get("role") not in ROLES:
            errors.append(f"edge {edge_id} has invalid role")
        if edge.get("tier") not in TIERS:
            errors.append(f"edge {edge_id} has invalid tier")
        if not edge.get("ruleIds") or not set(edge.get("ruleIds", [])) <= RULE_IDS:
            errors.append(f"edge {edge_id} has invalid ruleIds")
        if not edge.get("sourceIds") or not set(edge.get("sourceIds", [])) <= source_id_set:
            errors.append(f"edge {edge_id} has invalid sourceIds")
        if edge.get("dRegister") == "D4" and edge.get("modality") != "actual":
            errors.append(f"edge {edge_id}: every D4 element must be actual")
        if edge.get("dRegister") == "D5" and edge.get("modality") != "possible":
            errors.append(f"edge {edge_id}: every D5 element must be possible")

    state_ids = {item.get("id") for item in nodes if item.get("kind") == "state"}
    if not {f"d{number}" for number in range(7)} <= state_ids:
        errors.append("state spine must contain exactly named d0 through d6 nodes")
    crossings = {item.get("id") for item in nodes if item.get("kind") == "crossing"}
    if crossings != {f"mu-{number}" for number in range(6)}:
        errors.append("crossings must be exactly mu-0 through mu-5; mu-6 is forbidden")
    for number in range(6):
        crossing = next((n for n in nodes if n.get("id") == f"mu-{number}"), {})
        if crossing.get("source") != f"D{number}" or crossing.get("target") != f"D{number + 1}":
            errors.append(f"mu-{number} must connect D{number} to D{number + 1}")
        for field in (
            "saturatedRegister",
            "evidenceStatus",
            "newFreedomOrBoundaryResult",
            "lowerRegisterRecovery",
            "reductionStatus",
            "prediction",
            "killCriterion",
        ):
            if not crossing.get(field):
                errors.append(f"mu-{number} is missing {field}")
        evidence = crossing.get("saturationEvidence")
        evidence_status = crossing.get("evidenceStatus")
        if not isinstance(evidence, list):
            errors.append(f"mu-{number} saturationEvidence must be a list")
        elif evidence_status == "supplied" and not evidence:
            errors.append(f"mu-{number}: supplied evidence status requires evidence")
        elif evidence_status == "not_yet_supplied" and evidence:
            errors.append(f"mu-{number}: not_yet_supplied requires an empty evidence list")
        elif evidence_status not in {"supplied", "not_yet_supplied"}:
            errors.append(f"mu-{number} has invalid evidenceStatus")
        if crossing.get("reductionStatus") not in {
            "reduced",
            "currently_unreduced",
            "candidate_strong",
        }:
            errors.append(f"mu-{number} has invalid reductionStatus")

    closures = [edge for edge in edges if edge.get("edgeType") == "closure"]
    if len(closures) != 1:
        errors.append("topology needs exactly one closure edge")
    elif (
        closures[0].get("id") != "r6"
        or closures[0].get("from") != "d6"
        or closures[0].get("to") != "d0"
        or closures[0].get("closure") is not True
    ):
        errors.append("the sole closure must be non-mu r6: d6 to d0")

    receipts = [node for node in nodes if node.get("kind") == "receipt"]
    if {node.get("receiptType") for node in receipts} != {"commitment", "outcome"}:
        errors.append("receipt nodes must separate commitment and outcome")
    if len(receipts) != 2:
        errors.append("topology must contain exactly two receipt nodes")

    by_id = {node.get("id"): node for node in nodes}
    for actual_id in ("d4-model-token", "d4-rank-event", "d4-selector-token"):
        node = by_id.get(actual_id, {})
        if (node.get("dRegister"), node.get("modality")) != ("D4", "actual"):
            errors.append(f"{actual_id} must be a present D4 actual token")
    for content_id in ("d5-option-a", "d5-option-b"):
        node = by_id.get(content_id, {})
        if (node.get("dRegister"), node.get("modality")) != ("D5", "possible"):
            errors.append(f"{content_id} must be merely-possible D5 content")
    represented_content = next(
        (edge for edge in edges if edge.get("id") == "e-d5-model-content"), {}
    )
    if (
        represented_content.get("from") != "d4-model-token"
        or represented_content.get("to") != "d5"
        or represented_content.get("edgeType") != "represented-content"
        or represented_content.get("modality") != "possible"
    ):
        errors.append(
            "e-d5-model-content must run from the present D4 model token to D5 possible content"
        )

    selector_inputs = [
        edge
        for edge in edges
        if edge.get("from") == "d4-selector-token" and edge.get("to") == "chi"
    ]
    selector_returns = [
        edge
        for edge in edges
        if edge.get("from") == "outcome-receipt"
        and edge.get("to") == "d4-selector-token"
        and edge.get("loadBearing") is True
    ]
    if not selector_inputs or not selector_returns:
        errors.append("G_t must be load-bearing both into chi and back from receipt")
    if "physical-availability" not in by_id or "authorization" not in by_id:
        errors.append("physical availability and authorization need distinct nodes")
    if by_id.get("physical-availability", {}).get("status") == by_id.get(
        "authorization", {}
    ).get("status"):
        errors.append("physical availability and authorization statuses must be distinct")

    assessment = _schema(topology, "AuthorizationAssessment")
    variants = assessment.get("variants", {})
    if set(variants) != {"valid", "invalid", "absent", "not_required"}:
        errors.append("AuthorizationAssessment must inhabit all four tagged variants")
    else:
        if "complete non-null" not in str(variants["valid"].get("envelope", "")):
            errors.append("valid authorization requires a complete non-null envelope")
        if "Partial<AuthorizationEnvelope>" not in str(variants["invalid"].get("envelope", "")) or "NonEmpty" not in str(variants["invalid"].get("reasons", "")):
            errors.append("invalid authorization requires a partial envelope plus reasons")
        if variants["absent"].get("envelope") != "null" or "NonEmpty" not in str(variants["absent"].get("reasons", "")):
            errors.append("absent authorization requires null envelope plus reasons")
        if (
            variants["not_required"].get("envelope") != "null"
            or variants["not_required"].get("reasons") != "[]"
            or variants["not_required"].get("scope") != "NonConsequentialScope"
        ):
            errors.append("not_required authorization requires empty reasons and NonConsequentialScope")
    envelope_schema = _schema(topology, "AuthorizationEnvelope")
    if "NonEmpty Unique[BearerId]" not in str(envelope_schema.get("invariant", "")):
        errors.append("AuthorizationEnvelope consequence bearers must be nonempty and unique")
    evaluation_schema = _schema(topology, "EvaluationContract")
    if evaluation_schema.get("fields", {}).get("bearerIds") != "[BearerId]" or "NonEmpty Unique[BearerId]" not in str(
        evaluation_schema.get("invariant", "")
    ):
        errors.append("EvaluationContract bearerIds must be nonempty and unique")
    commitment_schema = _schema(topology, "CommitmentReceipt")
    commitment_fields = commitment_schema.get("fields", {})
    if "validated authorization.status" not in str(
        commitment_fields.get("authorizationStatusDerivedFrom", "")
    ):
        errors.append("commitment authorization status must derive from validated assessment")
    if not commitment_schema.get("statusDerivation"):
        errors.append("CommitmentReceipt needs a closed status derivation")
    if "nonconsequential_attempt" not in str(commitment_fields.get("status", "")) or "not_required" not in str(commitment_schema.get("statusDerivation", "")):
        errors.append("not_required must derive only to nonconsequential_attempt")
    if commitment_fields.get("expectedOutcome") != "String?":
        errors.append("CommitmentReceipt expectedOutcome must be nullable")
    commitment_invariant = str(commitment_schema.get("invariant", ""))
    for fragment in (
        "keys(expectedBearerDeltas)=set(evaluation.bearerIds)",
        "authorization.envelope.consequenceBearerIds, payerIds, and beneficiaryIds is a subset of evaluation.bearerIds",
        "status in {refused,unavailable} requires attemptedActionId=null and expectedOutcome=null",
    ):
        if fragment not in commitment_invariant:
            errors.append(f"CommitmentReceipt bearer invariant missing: {fragment}")
    outcome_schema = _schema(topology, "OutcomeReceipt")
    outcome_fields = outcome_schema.get("fields", {})
    if outcome_fields.get("receiptCause") != "action_attempt | ambient_observation":
        errors.append("OutcomeReceipt must discriminate action_attempt from ambient_observation")
    if outcome_fields.get("attemptedActionId") != "String?" or outcome_fields.get("performedActionId") != "String?":
        errors.append("OutcomeReceipt action identifiers must be nullable under the cause invariant")
    outcome_invariant = str(outcome_schema.get("invariant", ""))
    for fragment in (
        "action_attempt requires attemptedActionId non-null",
        "ambient_observation requires attemptedActionId=null and performedActionId=null",
        "consequenceBearerIds is NonEmpty Unique[BearerId]",
        "set(bearerObservations.bearerId)=set(consequenceBearerIds)",
        "evaluationRef=q.evaluation.id and set(consequenceBearerIds)=set(q.evaluation.bearerIds)",
    ):
        if fragment not in outcome_invariant:
            errors.append(f"OutcomeReceipt invariant missing: {fragment}")
    receipt_boundary = topology.get("receiptBoundary", {})
    if "never an action-attributed outcome" not in str(receipt_boundary.get("nullActionCase", "")):
        errors.append("null action must exclude action OutcomeReceipt")
    if by_id.get("outcome-receipt", {}).get("receiptCause") != "action_attempt":
        errors.append("rendered outcome receipt must be action-caused")

    candidate_fields = _schema(topology, "EgregoreotypeCandidate").get("fields", {})
    for field in (
        "affectedBearerIds",
        "etaObserved",
        "payerIds",
        "beneficiaryIds",
    ):
        if field not in candidate_fields:
            errors.append(f"EgregoreotypeCandidate is missing {field}")
    if "eta" in candidate_fields:
        errors.append("descriptive Egregoreotype candidacy must not fix eta")
    justice_fields = (
        topology.get("boundaries", [{}])[0].get("fields", {})
        if topology.get("boundaries")
        else {}
    )
    if str(justice_fields.get("eta", "")).lower().find("0") < 0:
        errors.append("Justice boundary alone must fix eta at zero")
    for field in ("affectedBearerIds", "payerIds", "beneficiaryIds"):
        if field not in justice_fields:
            errors.append(f"Justice boundary is missing {field}")

    overlay = topology.get("quantumOverlay", {})
    if overlay.get("removable") is not True:
        errors.append("quantum overlay must be removable")
    overlay_ids = set(overlay.get("nodeIds", [])) | set(overlay.get("edgeIds", []))
    if overlay_ids & set(topology.get("operationalCore", [])):
        errors.append("quantum overlay must not enter the operational core")
    if not overlay_ids <= set(element_ids):
        errors.append("quantum overlay references unknown graph elements")

    for view_id, view in topology.get("views", {}).items():
        output = Path(str(view.get("output", "")))
        if not output.parts or output.is_absolute():
            errors.append(f"view {view_id} needs a relative output path")
        if FROZEN_SOURCE_PARTS & set(output.parts):
            errors.append(f"view {view_id} targets a frozen tree")
        if not isinstance(view.get("width"), int) or not isinstance(view.get("height"), int):
            errors.append(f"view {view_id} needs integer dimensions")

    return errors


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _fmt(value: float | int) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.3f}".rstrip("0").rstrip(".")


def _attrs(**attributes: Any) -> str:
    rendered = []
    for key in sorted(attributes):
        value = attributes[key]
        if value is None:
            continue
        rendered.append(f'{key.replace("_", "-")}="{_esc(value)}"')
    return " ".join(rendered)


class _Svg:
    """Small deterministic SVG string builder."""

    def __init__(self, width: int, height: int, title: str, view: str, digest: str):
        self.lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg {_attrs(**{"data-topology-sha256": digest, "height": height, "role": "img", "viewBox": f"0 0 {width} {height}", "width": width, "xmlns": "http://www.w3.org/2000/svg"})}>',
            f"  <title>{_esc(title)}</title>",
            f'  <metadata id="topology-sha256">sha256:{_esc(digest)};view:{_esc(view)}</metadata>',
            "  <defs>",
            '    <marker id="arrow-actual" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M 0 0 L 8 4 L 0 8 Z" fill="#332d29"/></marker>',
            '    <marker id="arrow-possible" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M 0 0 L 8 4 L 0 8 Z" fill="#526879"/></marker>',
            '    <marker id="arrow-light" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M 0 0 L 8 4 L 0 8 Z" fill="#e7dcc2"/></marker>',
            "  </defs>",
        ]

    def add(self, tag: str, content: str = "", indent: int = 1, **attributes: Any) -> None:
        pad = "  " * indent
        attribute_text = _attrs(**attributes)
        spacer = " " if attribute_text else ""
        if content:
            self.lines.append(f"{pad}<{tag}{spacer}{attribute_text}>{content}</{tag}>")
        else:
            self.lines.append(f"{pad}<{tag}{spacer}{attribute_text}/>")

    def open(self, tag: str, indent: int = 1, **attributes: Any) -> None:
        attribute_text = _attrs(**attributes)
        spacer = " " if attribute_text else ""
        self.lines.append(f'{"  " * indent}<{tag}{spacer}{attribute_text}>')

    def close(self, tag: str, indent: int = 1) -> None:
        self.lines.append(f'{"  " * indent}</{tag}>')

    def text(
        self,
        x: float,
        y: float,
        value: str,
        *,
        size: int = 14,
        fill: str = "#332d29",
        weight: int = 400,
        anchor: str = "start",
        letter_spacing: float | None = None,
        italic: bool = False,
        id: str | None = None,
    ) -> None:
        self.add(
            "text",
            _esc(value),
            x=_fmt(x),
            y=_fmt(y),
            fill=fill,
            id=id,
            **{
                "font-family": "sans-serif",
                "font-size": size,
                "font-style": "italic" if italic else None,
                "font-weight": weight,
                "letter-spacing": _fmt(letter_spacing) if letter_spacing is not None else None,
                "text-anchor": anchor,
            },
        )

    def multiline(
        self,
        x: float,
        y: float,
        lines: Sequence[str],
        *,
        size: int = 13,
        fill: str = "#332d29",
        weight: int = 400,
        anchor: str = "middle",
        leading: int = 17,
        id: str | None = None,
    ) -> None:
        self.open(
            "text",
            x=_fmt(x),
            y=_fmt(y),
            fill=fill,
            id=id,
            **{
                "font-family": "sans-serif",
                "font-size": size,
                "font-weight": weight,
                "text-anchor": anchor,
            },
        )
        for index, line in enumerate(lines):
            self.add(
                "tspan",
                _esc(line),
                indent=2,
                x=_fmt(x),
                dy="0" if index == 0 else str(leading),
            )
        self.close("text")

    def finish(self) -> str:
        return "\n".join([*self.lines, "</svg>", ""])


def _line(
    svg: _Svg,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str,
    width: float = 2,
    dash: str | None = None,
    marker: str | None = None,
    id: str | None = None,
) -> None:
    svg.add(
        "line",
        x1=_fmt(x1),
        y1=_fmt(y1),
        x2=_fmt(x2),
        y2=_fmt(y2),
        stroke=color,
        **{
            "stroke-width": _fmt(width),
            "stroke-dasharray": dash,
            "marker-end": f"url(#{marker})" if marker else None,
            "id": id,
        },
    )


def _path(
    svg: _Svg,
    d: str,
    *,
    color: str,
    width: float = 2,
    dash: str | None = None,
    marker: str | None = None,
    fill: str = "none",
    id: str | None = None,
) -> None:
    svg.add(
        "path",
        d=d,
        fill=fill,
        stroke=color,
        **{
            "stroke-width": _fmt(width),
            "stroke-dasharray": dash,
            "marker-end": f"url(#{marker})" if marker else None,
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "id": id,
        },
    )


def _edge_dash(
    edges_by_id: Mapping[str, Mapping[str, Any]], edge_id: str
) -> str | None:
    """Derive graph-edge dash solely from the topology modality."""

    edge = edges_by_id[edge_id]
    return "6 5" if edge["modality"] == "possible" else None


def _state_node(
    svg: _Svg,
    node: Mapping[str, Any],
    lines: Sequence[str],
    *,
    width: int = 154,
    height: int = 54,
    possible: bool = False,
) -> None:
    x, y = float(node["x"]), float(node["y"])
    svg.open("g", id=node["id"], **{"data-kind": node["kind"], "data-modality": node["modality"]})
    svg.add(
        "rect",
        x=_fmt(x - width / 2),
        y=_fmt(y - height / 2),
        width=width,
        height=height,
        rx=13,
        fill="#eef3f4" if possible else "#fffdf6",
        stroke="#526879" if possible else "#332d29",
        **{
            "stroke-width": 2,
            "stroke-dasharray": "6 5" if possible else None,
        },
    )
    svg.multiline(x, y - (len(lines) - 1) * 8 + 5, lines, size=12, weight=600)
    svg.close("g")


def _receipt_node(
    svg: _Svg,
    node: Mapping[str, Any],
    lines: Sequence[str],
    *,
    dark: bool = False,
) -> None:
    x, y = float(node["x"]), float(node["y"])
    fill = "#1b242c" if dark else "#fff8df"
    stroke = "#e8c96b" if dark else "#7b5f18"
    text_fill = "#f7f0dc" if dark else "#332d29"
    points = (
        f"{_fmt(x-70)},{_fmt(y-31)} {_fmt(x+49)},{_fmt(y-31)} "
        f"{_fmt(x+70)},{_fmt(y-10)} {_fmt(x+70)},{_fmt(y+31)} "
        f"{_fmt(x-70)},{_fmt(y+31)}"
    )
    svg.open("g", id=node["id"], **{"data-kind": "receipt", "data-receipt-type": node["receiptType"]})
    svg.add("polygon", points=points, fill=fill, stroke=stroke, **{"stroke-width": 2})
    _line(svg, x + 49, y - 31, x + 49, y - 10, color=stroke, width=1.5)
    _line(svg, x + 49, y - 10, x + 70, y - 10, color=stroke, width=1.5)
    svg.multiline(x, y - (len(lines) - 1) * 8 + 4, lines, size=11, fill=text_fill, weight=700)
    svg.close("g")


def _render_spine(svg: _Svg, topology: Mapping[str, Any], dark: bool = False) -> None:
    by_id = {node["id"]: node for node in topology["nodes"]}
    edges_by_id = {edge["id"]: edge for edge in topology["edges"]}
    ink = "#e7dcc2" if dark else "#332d29"
    muted = "#9fb4bf" if dark else "#526879"
    fill = "#171d22" if dark else "#fffdf6"
    candidate_fill = "#2a2212" if dark else "#fff1c7"
    y = 175 if dark else 170
    state_xs = [70 + 240 * number for number in range(7)]
    crossing_xs = [190 + 240 * number for number in range(6)]

    def spine_edge(
        edge_id: str, x1: float, y1: float, x2: float, y2: float
    ) -> None:
        edge = edges_by_id[edge_id]
        is_possible = edge["modality"] == "possible"
        _line(
            svg,
            x1,
            y1,
            x2,
            y2,
            color=muted if is_possible else ink,
            dash=_edge_dash(edges_by_id, edge_id),
            marker=(
                "arrow-light"
                if dark
                else ("arrow-possible" if is_possible else "arrow-actual")
            ),
            id=edge_id,
        )

    svg.open("g", id="d-register-spine", **{"data-primitive": "mu-crossing"})
    for number, x in enumerate(state_xs):
        node = by_id[f"d{number}"]
        if number < 6:
            spine_edge(
                f"e-d{number}-mu{number}",
                x + 42,
                y,
                crossing_xs[number] - 27,
                y,
            )
            spine_edge(
                f"e-mu{number}-d{number + 1}",
                crossing_xs[number] + 27,
                y,
                state_xs[number + 1] - 42,
                y,
            )
        svg.open("g", id=f"d{number}", **{"data-register": f"D{number}"})
        svg.add("rect", x=x - 42, y=y - 25, width=84, height=50, rx=12, fill=fill, stroke=ink, **{"stroke-width": 2})
        svg.text(x, y - 2, f"D{number}", size=17, fill=ink, weight=700, anchor="middle")
        descriptors = ["ground", "distinction", "configuration", "change", "actual", "possible", "closure"]
        svg.text(x, y + 17, descriptors[number], size=10, fill=muted, weight=600, anchor="middle")
        svg.close("g")
    for number, x in enumerate(crossing_xs):
        node = by_id[f"mu-{number}"]
        points = f"{x},{y-27} {x+27},{y} {x},{y+27} {x-27},{y}"
        svg.open("g", id=node["id"], **{"data-kind": "crossing", "data-reduction-status": node["reductionStatus"]})
        svg.add("polygon", points=points, fill=candidate_fill, stroke="#c99a2e" if dark else "#7b5f18", **{"stroke-width": 2})
        svg.text(x, y + 5, f"mu{number}", size=12, fill=ink, weight=700, anchor="middle")
        svg.text(x, y + 42, "evidence: empty", size=8, fill=muted, weight=600, anchor="middle")
        svg.close("g")
    closure_y = y + 76
    _path(
        svg,
        f"M {state_xs[-1]} {y+27} C {state_xs[-1]} {closure_y}, {state_xs[0]} {closure_y}, {state_xs[0]} {y+27}",
        color=muted,
        width=2,
        dash=_edge_dash(edges_by_id, "r6"),
        marker="arrow-light" if dark else "arrow-actual",
        id="r6",
    )
    svg.add(
        "rect",
        x=610,
        y=closure_y - 22,
        width=360,
        height=18,
        rx=9,
        fill="#171d22" if dark else "#fbf7eb",
    )
    svg.text(790, closure_y - 7, "r6 interpretive return · not identity · not mu6", size=11, fill=muted, weight=600, anchor="middle")
    svg.close("g")


def _render_proof(topology: Mapping[str, Any], digest: str) -> str:
    view = topology["views"]["proof"]
    svg = _Svg(view["width"], view["height"], view["title"], "proof", digest)
    svg.add("rect", x=0, y=0, width=view["width"], height=view["height"], fill="#f7f0dc")
    svg.text(60, 52, "THE BURRI RULES", size=28, weight=800, letter_spacing=2.2)
    svg.text(60, 79, "Ivory proof plate · typed emergence, commitment, receipt, and composition", size=13, fill="#5b534c", weight=600)
    svg.text(1540, 52, "COMPASS / NOT COMMAND", size=11, fill="#5b534c", weight=700, anchor="end", letter_spacing=1.2)
    svg.text(1540, 76, f"topology sha256 {digest[:16]}…", size=10, fill="#5b534c", anchor="end")

    svg.add("rect", x=45, y=104, width=1510, height=160, rx=20, fill="#fbf7eb", stroke="#b8a98e", **{"stroke-width": 1.5})
    svg.text(65, 128, "BR-2 · SIX CANDIDATE CROSSINGS + ONE NON-mu CLOSURE", size=11, fill="#5b534c", weight=700, letter_spacing=1)
    _render_spine(svg, topology)

    by_id = {node["id"]: node for node in topology["nodes"]}
    edges_by_id = {edge["id"]: edge for edge in topology["edges"]}
    actual = "#332d29"
    possible = "#526879"
    gold = "#7b5f18"

    svg.open("g", id="physical-cone", **{"data-primitive": "boundary-envelope"})
    svg.add("rect", x=70, y=300, width=1460, height=430, rx=34, fill="#fbf7eb", stroke=actual, **{"stroke-width": 2.4})
    svg.text(95, 328, "J+ · c-BOUNDED PHYSICAL CAUSAL ENVELOPE", size=12, fill=actual, weight=800, letter_spacing=1)
    svg.text(1505, 328, "modeling changes reachable choices, not c", size=11, fill="#5b534c", anchor="end")
    svg.close("g")

    svg.open("g", id="option-cone", **{"data-primitive": "boundary-envelope"})
    svg.add("rect", x=250, y=350, width=590, height=220, rx=25, fill="#eef3f4", stroke=possible, **{"stroke-width": 2, "stroke-dasharray": "8 6"})
    svg.text(270, 376, "Omega · AGENT-RELATIVE OPTION FIELD", size=11, fill=possible, weight=800, letter_spacing=0.8)
    svg.text(815, 376, "authorized histories are a separate subset", size=10, fill=possible, anchor="end")
    svg.close("g")

    # Actual present carriers and merely-possible represented contents.
    _line(svg, 417, 405, 458, 405, color=actual, dash=_edge_dash(edges_by_id, "e-model-rank"), marker="arrow-actual", id="e-model-rank")
    _line(svg, 612, 405, 653, 405, color=actual, dash=_edge_dash(edges_by_id, "e-rank-selector"), marker="arrow-actual", id="e-rank-selector")
    _path(svg, "M 340 432 C 340 478, 395 490, 430 506", color=possible, dash=_edge_dash(edges_by_id, "e-model-option-a"), marker="arrow-possible", id="e-model-option-a")
    _path(svg, "M 340 432 C 420 470, 575 485, 650 506", color=possible, dash=_edge_dash(edges_by_id, "e-model-option-b"), marker="arrow-possible", id="e-model-option-b")
    _path(svg, "M 535 432 C 515 478, 465 490, 430 506", color=possible, dash=_edge_dash(edges_by_id, "e-rank-option-a"), marker="arrow-possible", id="e-rank-option-a")
    _path(svg, "M 535 432 C 560 475, 620 488, 650 506", color=possible, dash=_edge_dash(edges_by_id, "e-rank-option-b"), marker="arrow-possible", id="e-rank-option-b")
    _state_node(svg, by_id["d4-model-token"], ["M_t actual token", "represents D5 future"])
    _state_node(svg, by_id["d4-rank-event"], ["actual rank event", "orders D5 contents"])
    _state_node(svg, by_id["d4-selector-token"], ["G_t actual selector", "next-cycle policy"])
    _state_node(svg, by_id["d5-option-a"], ["D5 option A", "merely possible"], possible=True)
    _state_node(svg, by_id["d5-option-b"], ["D5 option B", "merely possible"], possible=True)

    # Means and the independent physical / authorization assessments.
    _line(svg, 507, 655, 533, 655, color=actual, dash=_edge_dash(edges_by_id, "e-means-availability"), marker="arrow-actual", id="e-means-availability")
    _path(svg, "M 687 655 C 750 650, 790 624, 814 605", color=actual, dash=_edge_dash(edges_by_id, "e-availability-chi"), marker="arrow-actual", id="e-availability-chi")
    _path(svg, "M 687 705 C 770 705, 800 650, 830 611", color=gold, dash=_edge_dash(edges_by_id, "e-authorization-chi"), marker="arrow-actual", id="e-authorization-chi")
    _path(svg, "M 730 432 C 750 490, 810 520, 842 556", color=actual, dash=_edge_dash(edges_by_id, "e-selector-chi"), marker="arrow-actual", id="e-selector-chi")
    _path(svg, "M 650 562 C 715 585, 765 588, 822 586", color=possible, dash=_edge_dash(edges_by_id, "e-option-a-chi"), marker="arrow-possible", id="e-option-a-chi")
    _state_node(svg, by_id["d4-means"], ["V_t embodied means", "actual resources"], width=154)
    _state_node(svg, by_id["physical-availability"], ["PHYSICAL", "available / unavailable"], width=154)
    _state_node(svg, by_id["authorization"], ["AUTHORIZATION", "valid / invalid / absent"], width=154)

    # Commitment, two receipts, environment, and both feedback targets.
    _line(svg, 925, 585, 980, 585, color=actual, width=2.7, dash=_edge_dash(edges_by_id, "e-chi-commitment"), marker="arrow-actual", id="e-chi-commitment")
    _line(svg, 1120, 585, 1150, 585, color=actual, width=2.7, dash=_edge_dash(edges_by_id, "e-commitment-action"), marker="arrow-actual", id="e-commitment-action")
    _line(svg, 1292, 585, 1320, 585, color=actual, width=2.7, dash=_edge_dash(edges_by_id, "e-action-outcome"), marker="arrow-actual", id="e-action-outcome")
    svg.open("g", id="chi", **{"data-primitive": "commitment"})
    svg.add("polygon", points="875,540 927,585 875,630 823,585", fill="#ffe7a3", stroke=gold, **{"stroke-width": 2.5})
    svg.text(875, 580, "chi", size=19, fill=actual, weight=800, anchor="middle")
    svg.text(875, 600, "commit", size=10, fill=actual, weight=700, anchor="middle")
    svg.close("g")
    _receipt_node(svg, by_id["commitment-receipt"], ["q_t COMMITMENT", "attempt / refusal"])
    _state_node(svg, by_id["d4-action"], ["a_t attempted", "D4 action"], width=145)
    _receipt_node(svg, by_id["outcome-receipt"], ["r_t+1 OUTCOME", "world-issued"])
    svg.text(1215, 635, "K_t may transform, veto, or distribute consequence", size=10, fill="#5b534c", anchor="middle")
    svg.add("rect", x=875, y=643, width=350, height=21, rx=10, fill="#fbf7eb")
    svg.text(1050, 657, "a_t = bottom -> null or ambient OutcomeReceipt (distinct cause)", size=9, fill="#5b534c", anchor="middle")

    _path(svg, "M 1390 552 C 1390 280, 395 280, 340 376", color=actual, width=2.2, dash=_edge_dash(edges_by_id, "e-outcome-model-feedback"), marker="arrow-actual", id="e-outcome-model-feedback")
    _path(svg, "M 1390 617 C 1350 680, 950 710, 730 434", color=gold, width=2.2, dash=_edge_dash(edges_by_id, "e-outcome-selector-feedback"), marker="arrow-actual", id="e-outcome-selector-feedback")
    svg.text(1045, 292, "Loop(M_t, G_t, q_t, r_t+1) revises M", size=10, fill="#5b534c", weight=600)
    svg.text(900, 690, "receipt also revises G · not optional", size=10, fill=gold, weight=700)

    # Titan boundary frame.
    svg.open("g", id="titan-frame", **{"data-primitive": "titan-frame"})
    svg.add("rect", x=95, y=605, width=238, height=102, rx=18, fill="#f7f0dc", stroke="#b8a98e", **{"stroke-width": 1.5})
    svg.text(112, 627, "BR-1 · SELECTED FRAME", size=10, fill="#5b534c", weight=800, letter_spacing=0.8)
    for x, symbol, label in ((140, "0", "ground"), (215, "1", "finite"), (290, "∞", "horizon")):
        svg.add("circle", cx=x, cy=661, r=20, fill="#fffdf6", stroke=actual, **{"stroke-width": 2})
        svg.text(x, 667, symbol, size=18, fill=actual, weight=700, anchor="middle")
        svg.text(x, 695, label, size=9, fill="#5b534c", anchor="middle")
    svg.close("g")

    # Reflexive bridge and removable correspondence.
    if view.get("showQuantumInset") and topology.get("quantumOverlay", {}).get("nodeIds"):
        svg.open("g", id="quantum-inset", **{"data-overlay": "quantum", "data-removable": "true"})
        svg.add("rect", x=60, y=760, width=505, height=155, rx=20, fill="#eef3f4", stroke=possible, **{"stroke-width": 1.5, "stroke-dasharray": "7 5"})
        svg.text(80, 785, "OPTIONAL QUANTUM CORRESPONDENCE [C] · REMOVABLE", size=10, fill=possible, weight=800, letter_spacing=0.6)
        svg.add("rect", x=90, y=815, width=175, height=48, rx=12, fill="#fffdf6", stroke=possible, **{"stroke-width": 1.5, "stroke-dasharray": "5 4"})
        svg.add("rect", x=350, y=815, width=175, height=48, rx=12, fill="#fffdf6", stroke=actual, **{"stroke-width": 1.5})
        svg.text(177.5, 836, "D5 structured", size=11, fill=possible, weight=700, anchor="middle")
        svg.text(177.5, 851, "alternatives", size=11, fill=possible, anchor="middle")
        svg.text(437.5, 836, "D4 observer-relative", size=11, fill=actual, weight=700, anchor="middle")
        svg.text(437.5, 851, "factual record", size=11, fill=actual, anchor="middle")
        _line(svg, 265, 839, 350, 839, color=possible, dash=_edge_dash(edges_by_id, "e-quantum-correspondence"), marker="arrow-possible", id="e-quantum-correspondence")
        svg.text(312, 879, "no extra dimension · no mu/chi measurement identity", size=9, fill="#5b534c", anchor="middle")
        svg.close("g")

    svg.open("g", id="reflexive-bridge")
    svg.add("rect", x=590, y=760, width=430, height=155, rx=20, fill="#fbf7eb", stroke="#b8a98e", **{"stroke-width": 1.5})
    svg.text(610, 785, "BR-5 · THREE INSPECTABLE GAPS", size=10, fill="#5b534c", weight=800, letter_spacing=0.8)
    gaps = [
        ("COGNITIVE", "territory vs prediction"),
        ("EXECUTION", "intended vs performed"),
        ("OUTCOME", "expected vs observed"),
    ]
    for index, (name, detail) in enumerate(gaps):
        y = 817 + 34 * index
        svg.text(615, y, name, size=10, fill=gold, weight=800)
        svg.text(720, y, detail, size=11, fill=actual)
    svg.text(997, 900, "feedback sign is dynamical, not moral", size=9, fill="#5b534c", anchor="end", italic=True)
    svg.close("g")

    # Descriptive candidate is inside a separately drawn normative boundary.
    svg.open("g", id="justice-boundary", **{"data-primitive": "boundary-envelope", "data-eta": "0"})
    svg.add("rect", x=1045, y=750, width=475, height=165, rx=26, fill="#fff8df", stroke=gold, **{"stroke-width": 2.5})
    svg.add("rect", x=1052, y=757, width=461, height=151, rx=21, fill="none", stroke=gold, **{"stroke-width": 1})
    svg.text(1070, 779, "JUSTICE CLASSIFICATION · eta = 0", size=10, fill=gold, weight=800, letter_spacing=0.8)
    svg.text(1495, 779, "separate from candidacy", size=9, fill="#5b534c", anchor="end")
    svg.close("g")
    svg.open("g", id="shared-trace", **{"data-primitive": "trace-field", "data-eta-observed": "number-or-unknown"})
    svg.add("ellipse", cx=1280, cy=835, rx=78, ry=45, fill="#f7f0dc", stroke=actual, **{"stroke-width": 2})
    svg.add("ellipse", cx=1280, cy=835, rx=55, ry=30, fill="none", stroke=possible, **{"stroke-width": 1.5, "stroke-dasharray": "5 4"})
    svg.text(1280, 831, "EGREGOREOTYPE", size=11, fill=actual, weight=800, anchor="middle")
    svg.text(1280, 849, "etaObserved = n | ?", size=9, fill=possible, weight=600, anchor="middle")
    svg.close("g")
    _path(svg, "M 1390 617 C 1410 700, 1360 760, 1330 795", color=actual, dash=_edge_dash(edges_by_id, "e-outcome-trace"), marker="arrow-actual", id="e-outcome-trace")
    _path(svg, "M 1215 835 C 1070 825, 890 720, 748 434", color=gold, dash=_edge_dash(edges_by_id, "e-trace-selector"), marker="arrow-actual", id="e-trace-selector")
    svg.multiline(1390, 816, ["affected bearer set", "payerIds / beneficiaryIds", "custody · consent · exit"], size=9, fill="#5b534c", anchor="middle", leading=14)
    svg.text(1280, 895, "five trace tests · no consciousness or personhood presumed", size=9, fill="#5b534c", anchor="middle")

    # Modality legend and bounded footer.
    _line(svg, 65, 949, 125, 949, color=actual, width=2.5, marker="arrow-actual")
    svg.text(138, 953, "D4 actual / enacted", size=10, fill=actual)
    _line(svg, 310, 949, 370, 949, color=possible, width=2, dash="5 5", marker="arrow-possible")
    svg.text(383, 953, "D5 merely possible / represented", size=10, fill=possible)
    _path(svg, "M 600 954 C 620 930, 660 930, 680 954", color=gold, marker="arrow-actual")
    svg.text(696, 953, "feedback / return", size=10, fill=gold)
    svg.text(1540, 953, "Map != territory · receipt > self-certification", size=11, fill=actual, weight=700, anchor="end")
    svg.text(60, 981, "[I] externally uncalibrated translation grammar · empirical crossings and universal-fit claims remain [C]", size=10, fill="#5b534c")
    svg.text(1540, 981, "JSON mirrors owners; it cannot introduce doctrine or upgrade evidence", size=10, fill="#5b534c", anchor="end")
    return svg.finish()


def _render_emblem(topology: Mapping[str, Any], digest: str) -> str:
    view = topology["views"]["emblem"]
    svg = _Svg(view["width"], view["height"], view["title"], "emblem", digest)
    bg = "#0f1418"
    ivory = "#e7dcc2"
    pale = "#9fb4bf"
    gold = "#e8c96b"
    panel = "#171d22"
    edges_by_id = {edge["id"]: edge for edge in topology["edges"]}

    svg.add("rect", x=0, y=0, width=view["width"], height=view["height"], fill=bg)
    svg.text(60, 58, "THE BURRI RULES", size=28, fill=ivory, weight=800, letter_spacing=2.2)
    svg.text(60, 84, "Obsidian emblem · derived compression", size=13, fill=pale, weight=600)
    svg.text(1540, 58, "FRAME · CROSS · COMMIT · RECEIVE · RETURN · COMPOSE", size=11, fill=gold, weight=700, anchor="end", letter_spacing=1)
    svg.text(1540, 82, f"sha256 {digest[:16]}…", size=10, fill=pale, anchor="end")
    _render_spine(svg, topology, dark=True)

    svg.open("g", id="master-emblem-geometry")
    svg.add("circle", cx=800, cy=585, r=310, fill=panel, stroke=ivory, **{"stroke-width": 2.5})
    svg.add("circle", cx=800, cy=585, r=274, fill="none", stroke=pale, **{"stroke-width": 1.5, "stroke-dasharray": "10 8"})
    svg.text(800, 315, "J+ PHYSICAL ENVELOPE · c-BOUNDED", size=11, fill=ivory, weight=800, anchor="middle", letter_spacing=1)
    svg.text(800, 345, "Omega option field lies inside · authorization remains separately typed", size=10, fill=pale, anchor="middle")

    # Core loop around an unforced Titan frame.
    positions = {
        "model": (560, 475),
        "option": (760, 410),
        "commit": (1000, 475),
        "action": (1090, 650),
        "receipt": (800, 805),
        "trace": (510, 680),
    }
    _path(
        svg,
        "M 620 458 C 665 425, 700 414, 716 412",
        color=pale,
        dash=_edge_dash(edges_by_id, "e-model-option-a"),
        marker="arrow-possible",
        id="e-model-option-a",
    )
    _path(
        svg,
        "M 805 414 C 875 415, 930 440, 960 466",
        color=pale,
        dash=_edge_dash(edges_by_id, "e-option-a-chi"),
        marker="arrow-possible",
        id="e-option-a-chi",
    )
    _path(
        svg,
        "M 1026 505 C 1075 540, 1095 585, 1093 614",
        color=ivory,
        dash=_edge_dash(edges_by_id, "e-commitment-action"),
        marker="arrow-light",
        id="e-commitment-action",
    )
    _path(
        svg,
        "M 1065 683 C 1010 745, 900 790, 845 801",
        color=ivory,
        dash=_edge_dash(edges_by_id, "e-action-outcome"),
        marker="arrow-light",
        id="e-action-outcome",
    )
    _path(
        svg,
        "M 747 804 C 650 785, 570 735, 538 707",
        color=gold,
        dash=_edge_dash(edges_by_id, "e-outcome-trace"),
        marker="arrow-light",
        id="e-outcome-trace",
    )
    _path(
        svg,
        "M 495 645 C 475 570, 500 515, 535 493",
        color=gold,
        dash=_edge_dash(edges_by_id, "e-trace-selector"),
        marker="arrow-light",
        id="e-trace-selector",
    )
    _path(
        svg,
        "M 800 775 C 765 690, 660 565, 590 495",
        color=gold,
        dash=_edge_dash(edges_by_id, "e-outcome-model-feedback"),
        marker="arrow-light",
        id="e-outcome-model-feedback",
    )

    def dark_box(identifier: str, x: float, y: float, lines: Sequence[str], *, dotted: bool = False) -> None:
        svg.open("g", id=identifier)
        svg.add("rect", x=x - 72, y=y - 30, width=144, height=60, rx=15, fill=bg, stroke=pale if dotted else ivory, **{"stroke-width": 2, "stroke-dasharray": "6 5" if dotted else None})
        svg.multiline(x, y - (len(lines) - 1) * 8 + 4, lines, size=11, fill=ivory, weight=700)
        svg.close("g")

    dark_box("emblem-model", *positions["model"], ["D4 MODEL TOKEN", "future content"])
    dark_box("emblem-option", *positions["option"], ["D5 OPTIONS", "merely possible"], dotted=True)
    svg.open("g", id="emblem-commitment")
    svg.add("polygon", points="1000,430 1045,475 1000,520 955,475", fill="#2a2212", stroke=gold, **{"stroke-width": 2.5})
    svg.text(1000, 470, "chi", size=18, fill=gold, weight=800, anchor="middle")
    svg.text(1000, 490, "COMMIT", size=9, fill=ivory, weight=700, anchor="middle")
    svg.close("g")
    dark_box("emblem-action", *positions["action"], ["D4 ACTION", "attempted"])
    _receipt_node(svg, {"id": "emblem-outcome", "x": 800, "y": 805, "receiptType": "outcome"}, ["WORLD RECEIPT", "revises M + G"], dark=True)
    svg.open("g", id="emblem-trace")
    svg.add("ellipse", cx=510, cy=680, rx=76, ry=44, fill=bg, stroke=gold, **{"stroke-width": 2})
    svg.add("ellipse", cx=510, cy=680, rx=52, ry=27, fill="none", stroke=pale, **{"stroke-width": 1.5, "stroke-dasharray": "5 4"})
    svg.text(510, 676, "SHARED TRACE", size=10, fill=ivory, weight=800, anchor="middle")
    svg.text(510, 694, "etaObserved = n | ?", size=9, fill=pale, anchor="middle")
    svg.close("g")

    svg.open("g", id="emblem-titan-frame", **{"data-primitive": "titan-frame"})
    for x, symbol in ((735, "0"), (800, "1"), (865, "∞")):
        svg.add("circle", cx=x, cy=590, r=27, fill=bg, stroke=gold, **{"stroke-width": 2})
        svg.text(x, 597, symbol, size=19, fill=ivory, weight=700, anchor="middle")
    svg.text(800, 642, "selected frame · not forced ontology", size=10, fill=pale, anchor="middle")
    svg.close("g")

    svg.open("g", id="emblem-justice", **{"data-eta": "0"})
    svg.add("rect", x=1170, y=390, width=300, height=210, rx=25, fill=panel, stroke=gold, **{"stroke-width": 2.5})
    svg.text(1200, 422, "JUSTICE · eta = 0", size=12, fill=gold, weight=800, letter_spacing=0.8)
    svg.multiline(1320, 462, ["affected bearer set", "payerIds / beneficiaryIds", "custody · consent", "reversibility · exit", "contestable authorization"], size=11, fill=ivory, weight=600, leading=23)
    svg.text(1320, 576, "normative test, not candidacy", size=9, fill=pale, anchor="middle", italic=True)
    svg.close("g")

    svg.open("g", id="emblem-receipts")
    svg.add("rect", x=120, y=405, width=285, height=270, rx=25, fill=panel, stroke=pale, **{"stroke-width": 1.5})
    svg.text(150, 438, "TWO RECEIPTS", size=12, fill=ivory, weight=800, letter_spacing=1)
    svg.multiline(262, 480, ["q_t commitment", "intention · means", "physical status", "authorization status"], size=11, fill=pale, weight=600, leading=20)
    _line(svg, 165, 562, 360, 562, color=pale, dash="5 5")
    svg.multiline(262, 594, ["r_t+1 outcome", "world-issued consequence", "full bearer observations"], size=11, fill=ivory, weight=600, leading=20)
    svg.close("g")
    svg.close("g")

    svg.text(800, 930, "A PRESENT MODEL OF A POSSIBLE FUTURE CAN REWEIGHT PRESENT ACTION", size=15, fill=gold, weight=800, anchor="middle", letter_spacing=1.1)
    svg.text(800, 957, "No realized future signal is required · the returned world revises both map and mapper", size=11, fill=ivory, anchor="middle")
    svg.text(60, 985, "[I] compass grammar · [C] where empirical crossings or universal fit are claimed", size=10, fill=pale)
    svg.text(1540, 985, "quantum inset removed without changing the operational core", size=10, fill=pale, anchor="end")
    return svg.finish()


def render_view(topology: Mapping[str, Any], view_id: str, digest: str) -> str:
    """Render one configured view as deterministic SVG text."""

    if view_id not in topology.get("views", {}):
        raise KeyError(f"unknown view: {view_id}")
    if view_id == "proof":
        return _render_proof(topology, digest)
    if view_id == "emblem":
        return _render_emblem(topology, digest)
    raise KeyError(f"unsupported view renderer: {view_id}")


def _rendered_outputs(
    topology: Mapping[str, Any], topology_path: Path, repo_root: Path
) -> dict[Path, str]:
    digest = topology_sha256(topology_path)
    return {
        repo_root / view["output"]: render_view(topology, view_id, digest)
        for view_id, view in sorted(topology["views"].items())
    }


def write_outputs(
    topology_path: Path | str = DEFAULT_TOPOLOGY,
    repo_root: Path | str = REPO_ROOT,
) -> list[Path]:
    """Validate and write both configured artifacts; return written paths."""

    path = Path(topology_path)
    root = Path(repo_root)
    topology = load_topology(path)
    errors = validate_topology(topology, root)
    if errors:
        raise ValueError("invalid Burri topology:\n- " + "\n- ".join(errors))
    rendered = _rendered_outputs(topology, path, root)
    for output_path, content in rendered.items():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8", newline="\n")
    return sorted(rendered)


def check_outputs(
    topology_path: Path | str = DEFAULT_TOPOLOGY,
    repo_root: Path | str = REPO_ROOT,
) -> list[str]:
    """Return validation, absence, or byte-drift errors without writing."""

    path = Path(topology_path)
    root = Path(repo_root)
    topology = load_topology(path)
    errors = validate_topology(topology, root)
    if errors:
        return errors
    for output_path, expected in _rendered_outputs(topology, path, root).items():
        if not output_path.is_file():
            errors.append(f"missing generated artifact: {output_path.relative_to(root)}")
        elif output_path.read_bytes() != expected.encode("utf-8"):
            errors.append(f"generated artifact is stale: {output_path.relative_to(root)}")
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topology", type=Path, default=DEFAULT_TOPOLOGY)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--check", action="store_true", help="verify exact generated bytes")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.check:
            errors = check_outputs(args.topology, args.repo_root)
            if errors:
                for error in errors:
                    print(f"BURRI-ERROR {error}", file=sys.stderr)
                return 1
            print("BURRI-OK topology valid; generated SVG bytes are current")
            return 0
        outputs = write_outputs(args.topology, args.repo_root)
        digest = topology_sha256(args.topology)
        for output in outputs:
            print(f"BURRI-WROTE {output.relative_to(args.repo_root)} sha256={hashlib.sha256(output.read_bytes()).hexdigest()}")
        print(f"BURRI-TOPOLOGY sha256={digest}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"BURRI-ERROR {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

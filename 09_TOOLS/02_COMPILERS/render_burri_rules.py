#!/usr/bin/env python3
"""Validate and deterministically render the Burri Rules topology.

The Markdown rulebook owns semantics. This compiler accepts only geometry and
source references, then produces two deterministic, accessible SVG views.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from urllib.parse import urlparse
from xml.sax.saxutils import escape, quoteattr


RENDERER_VERSION = "1.0.0"
SCHEMA_VERSION = "0.1"
RULE_IDS = {f"BR-{number}" for number in range(1, 7)}
ALLOWED_KINDS = {"state", "frame", "crossing", "commitment", "receipt", "trace"}
ALLOWED_REGISTERS = {f"D{number}" for number in range(7)}
ALLOWED_MODALITIES = {"actual", "possible"}
ALLOWED_ROLES = {"forward", "feedback", "coupling"}
ALLOWED_TIERS = {"A", "B", "S", "I", "D", "C"}
FORBIDDEN_SOURCE_PARTS = {"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"}
EXPECTED_OUTPUTS = {
    "proof": "05_COSMOLOGY/00_BURRI_RULES_PLATE.svg",
    "emblem": "05_COSMOLOGY/00_BURRI_RULES_EMBLEM.svg",
}
TRACE_CRITERIA = {
    "carrier-turnover-persistence",
    "later-selection-reweighting",
    "objective-like-bias",
    "continuing-substrate-input-cost",
}
BOUNDARY_FIELDS = {
    "individual",
    "whole",
    "eta",
    "custody",
    "consent",
    "reversibility",
    "exit",
}
FULL_TEXT_EQUIVALENT = (
    "The Titans frame possibility; a finite agent forms a fallible D5 option field, "
    "commits through D4 means and authorization, receives D4 consequences, and "
    "recursively corrects both world-model and selector."
)


def load_topology(path: Path) -> dict:
    """Load a topology JSON object from path."""
    with Path(path).open("r", encoding="utf-8") as handle:
        topology = json.load(handle)
    if not isinstance(topology, dict):
        raise ValueError(f"topology root must be an object: {path}")
    return topology


def topology_sha256(path: Path) -> str:
    """Return the SHA-256 of the topology's exact bytes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _refs_are_valid(
    element: dict,
    element_name: str,
    source_ids: set[str],
    errors: list[str],
) -> None:
    rule_ids = element.get("ruleIds")
    if not isinstance(rule_ids, list) or not rule_ids:
        errors.append(f"{element_name}: ruleIds must be a non-empty list")
    elif not set(rule_ids) <= RULE_IDS:
        errors.append(f"{element_name}: unknown rule reference")
    source_refs = element.get("sourceIds")
    if not isinstance(source_refs, list) or not source_refs:
        errors.append(f"{element_name}: sourceIds must be a non-empty list")
    elif not set(source_refs) <= source_ids:
        errors.append(f"{element_name}: unknown source reference")


def _inside_repo(path: Path, repo_root: Path) -> bool:
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except ValueError:
        return False


def validate_topology(topology: dict, repo_root: Path) -> list[str]:
    """Return deterministic validation errors; an empty list means valid."""
    errors: list[str] = []
    if not isinstance(topology, dict):
        return ["topology root must be an object"]

    required_top = {"schemaVersion", "rules", "sources", "nodes", "edges", "views"}
    missing_top = sorted(required_top - set(topology))
    if missing_top:
        errors.append(f"missing top-level keys: {', '.join(missing_top)}")
    if topology.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"schemaVersion must be {SCHEMA_VERSION}")

    rules = topology.get("rules", [])
    if not isinstance(rules, list):
        errors.append("rules must be a list")
        rules = []
    rule_ids = [rule.get("id") for rule in rules if isinstance(rule, dict)]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate rule id")
    if set(rule_ids) != RULE_IDS or len(rule_ids) != 6:
        errors.append("rules must contain exactly BR-1 through BR-6")

    sources = topology.get("sources", [])
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    source_ids_list = [source.get("id") for source in sources if isinstance(source, dict)]
    if len(source_ids_list) != len(set(source_ids_list)):
        errors.append("duplicate source id")
    source_ids = {source_id for source_id in source_ids_list if _is_nonempty_string(source_id)}
    remote_sources = []
    root = Path(repo_root)
    for index, source in enumerate(sources):
        name = f"source[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{name}: must be an object")
            continue
        source_id = source.get("id")
        if not _is_nonempty_string(source_id):
            errors.append(f"{name}: id must be non-empty")
        has_path = "path" in source
        has_url = "url" in source
        if has_path == has_url:
            errors.append(f"{name}: provide exactly one of path or url")
            continue
        if source.get("tier") not in ALLOWED_TIERS:
            errors.append(f"{name}: invalid tier")
        if has_path:
            value = source.get("path")
            if not _is_nonempty_string(value):
                errors.append(f"{name}: path must be non-empty")
                continue
            local = Path(value)
            if local.is_absolute() or not _inside_repo(root / local, root):
                errors.append(f"{name}: source path must stay relative to repo root")
            if FORBIDDEN_SOURCE_PARTS & set(local.parts):
                errors.append(f"{name}: disallowed source path: {value}")
            if not (root / local).is_file():
                errors.append(f"{name}: missing local source path: {value}")
        else:
            value = source.get("url")
            parsed = urlparse(value if isinstance(value, str) else "")
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{name}: remote source must be HTTPS")
            remote_sources.append(source)
    if len(remote_sources) != 1:
        errors.append("sources must contain exactly one HTTPS primary source")
    elif remote_sources[0].get("tier") != "B" or remote_sources[0].get("crosswalkTier") != "I":
        errors.append("Soros source must be attribution B with crosswalk I")

    nodes = topology.get("nodes", [])
    edges = topology.get("edges", [])
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        edges = []
    all_elements = [item for item in nodes + edges if isinstance(item, dict)]
    element_ids = [element.get("id") for element in all_elements]
    seen: set[str] = set()
    for element_id in element_ids:
        if not _is_nonempty_string(element_id):
            errors.append("element id must be a non-empty string")
        elif element_id in seen:
            errors.append(f"duplicate element id: {element_id}")
        else:
            seen.add(element_id)

    node_ids = {node.get("id") for node in nodes if isinstance(node, dict)}
    for index, node in enumerate(nodes):
        name = f"node[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{name}: must be an object")
            continue
        node_id = node.get("id", name)
        name = f"node {node_id}"
        if node.get("kind") not in ALLOWED_KINDS:
            errors.append(f"{name}: invalid kind")
        if node.get("dRegister") not in ALLOWED_REGISTERS:
            errors.append(f"{name}: invalid dRegister")
        if node.get("modality") not in ALLOWED_MODALITIES:
            errors.append(f"{name}: invalid modality")
        if node.get("role") not in ALLOWED_ROLES:
            errors.append(f"{name}: invalid role")
        if node.get("tier") not in ALLOWED_TIERS:
            errors.append(f"{name}: invalid tier")
        if not _is_nonempty_string(node.get("label")):
            errors.append(f"{name}: label must be non-empty")
        for coordinate in ("x", "y"):
            value = node.get(coordinate)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{name}: {coordinate} must be numeric")
        _refs_are_valid(node, name, source_ids, errors)

    for index, edge in enumerate(edges):
        name = f"edge[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{name}: must be an object")
            continue
        edge_id = edge.get("id", name)
        name = f"edge {edge_id}"
        if edge.get("from") not in node_ids:
            errors.append(f"{name}: invalid from endpoint")
        if edge.get("to") not in node_ids:
            errors.append(f"{name}: invalid to endpoint")
        if edge.get("dRegister") not in ALLOWED_REGISTERS:
            errors.append(f"{name}: invalid dRegister")
        if edge.get("modality") not in ALLOWED_MODALITIES:
            errors.append(f"{name}: invalid modality")
        if edge.get("role") not in ALLOWED_ROLES:
            errors.append(f"{name}: invalid role")
        if edge.get("tier") not in ALLOWED_TIERS:
            errors.append(f"{name}: invalid tier")
        _refs_are_valid(edge, name, source_ids, errors)

    required_states = {f"d{number}" for number in range(7)}
    if not required_states <= node_ids:
        errors.append("nodes must include complete d0 through d6 spine")
    crossing_nodes = {
        node.get("id") for node in nodes if isinstance(node, dict) and node.get("kind") == "crossing"
    }
    expected_crossings = {f"mu-{number}" for number in range(6)}
    if crossing_nodes != expected_crossings or "mu-6" in node_ids:
        errors.append("crossing nodes must be exactly mu-0 through mu-5")
    edge_pairs = {(edge.get("from"), edge.get("to")) for edge in edges if isinstance(edge, dict)}
    for number in range(6):
        if (f"d{number}", f"mu-{number}") not in edge_pairs:
            errors.append(f"missing crossing ingress d{number} -> mu-{number}")
        if (f"mu-{number}", f"d{number + 1}") not in edge_pairs:
            errors.append(f"missing crossing egress mu-{number} -> d{number + 1}")
    closures = [edge for edge in edges if isinstance(edge, dict) and edge.get("closure") is True]
    if len(closures) != 1 or (closures[0].get("from"), closures[0].get("to")) != ("d6", "d0"):
        errors.append("exactly one D6 -> D0 closure edge is required")

    frames = [node for node in nodes if isinstance(node, dict) and node.get("kind") == "frame"]
    if len(frames) != 1:
        errors.append("exactly one Titan frame node is required")
    elif (
        set(frames[0].get("marks", {})) != {"bullet", "finity", "horizon"}
        or frames[0].get("acting") is not False
        or frames[0].get("displayLociOnly") is not True
    ):
        errors.append("Titan frame must be nonacting display loci bullet/finity/horizon")

    boundaries = topology.get("boundaries", [])
    if not isinstance(boundaries, list) or len(boundaries) != 1:
        errors.append("exactly one collective boundary is required")
    else:
        fields = boundaries[0].get("fields", {}) if isinstance(boundaries[0], dict) else {}
        if not isinstance(fields, dict) or not BOUNDARY_FIELDS <= set(fields):
            errors.append("collective boundary is missing required fields")

    traces = [node for node in nodes if isinstance(node, dict) and node.get("kind") == "trace"]
    if len(traces) != 1:
        errors.append("exactly one shared trace node is required")
    else:
        if set(traces[0].get("criteria", [])) != TRACE_CRITERIA:
            errors.append("shared trace must declare all four Egregoreotype criteria")
        if "no consciousness claim" not in str(traces[0].get("claimBoundary", "")).lower():
            errors.append("shared trace must carry the no consciousness claim boundary")

    bridge = topology.get("reflexiveBridge", {})
    slippages = bridge.get("slippages", []) if isinstance(bridge, dict) else []
    if {item.get("id") for item in slippages if isinstance(item, dict)} != {
        "cognitive-gap",
        "execution-gap",
        "outcome-gap",
    }:
        errors.append("Reflexive Bridge must name cognitive, execution, and outcome gaps")
    signs = {
        item.get("id"): str(item.get("label", "")).lower()
        for item in bridge.get("feedbackSigns", [])
        if isinstance(item, dict)
    } if isinstance(bridge, dict) else {}
    if "corrective" not in signs.get("negative", "") or "amplifying" not in signs.get("positive", ""):
        errors.append("Reflexive Bridge must label negative/corrective and positive/amplifying")
    if "not moral" not in str(bridge.get("signBoundary", "")).lower():
        errors.append("Reflexive Bridge feedback signs must be dynamical, not moral")

    receipts = [node for node in nodes if isinstance(node, dict) and node.get("kind") == "receipt"]
    if len(receipts) != 1:
        errors.append("exactly one receipt node is required")
    else:
        feedback = [
            edge for edge in edges
            if isinstance(edge, dict)
            and edge.get("role") == "feedback"
            and edge.get("from") == receipts[0].get("id")
        ]
        if len(feedback) != 1 or feedback[0].get("updatePolicy") != "changed or explicit null-with-reason":
            errors.append("receipt feedback requires changed or explicit null-with-reason policy")

    cones = topology.get("cones", {})
    physical = cones.get("physical", {}) if isinstance(cones, dict) else {}
    option = cones.get("option", {}) if isinstance(cones, dict) else {}
    if physical.get("label") != "J+" or "c-bounded" not in str(physical.get("boundary", "")):
        errors.append("physical cone must be J+ with c-bounded boundary")
    if option.get("label") != "Omega" or "inside" not in str(option.get("boundary", "")):
        errors.append("option cone must be Omega inside the physical cone")
    rosetta = topology.get("rosettaProjection", {})
    if not isinstance(rosetta, dict) or rosetta.get("label") != "rho_domain" or "no proof transfer" not in str(rosetta.get("boundary", "")):
        errors.append("Rosetta projection must be rho_domain with no proof transfer")
    if topology.get("fullTextEquivalent") != FULL_TEXT_EQUIVALENT:
        errors.append("master emblem fullTextEquivalent does not match the rulebook")

    views = topology.get("views", {})
    if not isinstance(views, dict) or set(views) != {"proof", "emblem"}:
        errors.append("views must contain exactly proof and emblem")
    else:
        for view_id, expected_output in EXPECTED_OUTPUTS.items():
            view = views.get(view_id, {})
            if view.get("output") != expected_output:
                errors.append(f"view {view_id}: output must be {expected_output}")
            if view.get("width") != 1600 or view.get("height") != 1000:
                errors.append(f"view {view_id}: dimensions must be 1600x1000")

    operational_core = topology.get("operationalCore", [])
    if not isinstance(operational_core, list) or not operational_core:
        errors.append("operationalCore must be a non-empty node-id list")
    else:
        core = set(operational_core)
        if not core <= node_ids:
            errors.append("operationalCore references missing nodes")
        quantum_nodes = {
            node.get("id") for node in nodes
            if isinstance(node, dict) and node.get("overlay") == "quantum"
        }
        if core & quantum_nodes:
            errors.append("operationalCore may not depend on quantum overlay nodes")
        adjacency = {node_id: set() for node_id in core}
        for edge in edges:
            if not isinstance(edge, dict) or edge.get("overlay") == "quantum":
                continue
            start, end = edge.get("from"), edge.get("to")
            if start in core and end in core:
                adjacency[start].add(end)
                adjacency[end].add(start)
        if core:
            seen_core: set[str] = set()
            frontier = [sorted(core)[0]]
            while frontier:
                current = frontier.pop()
                if current in seen_core:
                    continue
                seen_core.add(current)
                frontier.extend(sorted(adjacency[current] - seen_core))
            if seen_core != core:
                errors.append("operationalCore must stay connected without quantum overlays")

    for element in all_elements:
        if element.get("overlay") == "quantum" and element.get("tier") != "C":
            errors.append(f"quantum overlay element {element.get('id')} must remain tier C")

    return errors


def _attrs(values: dict[str, Any]) -> str:
    return "".join(
        f" {key}={quoteattr(str(value))}"
        for key, value in values.items()
        if value is not None
    )


def _text(x: float, y: float, value: str, **attrs: Any) -> str:
    base = {"x": x, "y": y}
    base.update(attrs)
    return f"<text{_attrs(base)}>{escape(value)}</text>"


def _wrap_words(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and len(candidate) > width:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def _multiline_text(
    x: float,
    y: float,
    text: str,
    width: int,
    line_height: int,
    **attrs: Any,
) -> str:
    lines = _wrap_words(text, width)
    base = {"x": x, "y": y}
    base.update(attrs)
    spans = []
    for index, line in enumerate(lines):
        spans.append(
            f"<tspan{_attrs({'x': x, 'dy': 0 if index == 0 else line_height})}>{escape(line)}</tspan>"
        )
    return f"<text{_attrs(base)}>{''.join(spans)}</text>"


def _palette(view_id: str) -> dict[str, str]:
    if view_id == "proof":
        return {
            "background": "#F4ECDD",
            "ink": "#1C211E",
            "muted": "#6D7068",
            "line": "#303A34",
            "possible": "#657D70",
            "accent": "#A56A3A",
            "gold": "#B28A45",
            "panel": "#FBF7EE",
            "panel2": "#E8DFCF",
            "danger": "#8F4D44",
        }
    return {
        "background": "#101211",
        "ink": "#F3EBDD",
        "muted": "#B8AE9E",
        "line": "#E8DEC9",
        "possible": "#C8A96B",
        "accent": "#C8A96B",
        "gold": "#D7B66F",
        "panel": "#171A18",
        "panel2": "#24241F",
        "danger": "#D08773",
    }


def _node_position(node: dict, view_id: str) -> tuple[float, float]:
    if view_id == "emblem":
        emblem_positions = {
            "d5-model": (420, 350),
            "d5-option-a": (560, 270),
            "d5-option-b": (560, 350),
            "d5-option-c": (560, 430),
            "d4-means": (420, 590),
            "chi": (760, 500),
            "d4-action": (980, 500),
            "receipt": (1200, 500),
            "shared-trace": (1200, 700),
            "titan-frame": (760, 500),
        }
        if node.get("id") in emblem_positions:
            return emblem_positions[node["id"]]
    return float(node.get("x", 0)), float(node.get("y", 0))


def _edge_svg(edge: dict, node_map: dict[str, dict], view_id: str, colors: dict[str, str]) -> str:
    start_node = node_map[edge["from"]]
    end_node = node_map[edge["to"]]
    x1, y1 = _node_position(start_node, view_id)
    x2, y2 = _node_position(end_node, view_id)
    color = colors["possible"] if edge.get("modality") == "possible" else colors["line"]
    dash = "7 10" if edge.get("modality") == "possible" else None
    if edge.get("role") == "coupling":
        dash = "3 7"
    common = {
        "id": edge["id"],
        "fill": "none",
        "stroke": color,
        "stroke-width": 2.2 if view_id == "proof" else 3,
        "stroke-dasharray": dash,
        "stroke-linecap": "round",
        "marker-end": f"url(#arrow-{view_id})",
        "opacity": 0.9,
    }
    if edge.get("role") == "feedback":
        lift = 130 if view_id == "proof" else 210
        control1 = (x1, min(y1, y2) - lift)
        control2 = (x2, min(y1, y2) - lift)
        path = f"M {x1:.1f} {y1:.1f} C {control1[0]:.1f} {control1[1]:.1f}, {control2[0]:.1f} {control2[1]:.1f}, {x2:.1f} {y2:.1f}"
        return f"<path{_attrs({**common, 'd': path})}/>"
    return f"<line{_attrs({**common, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})}/>"


def _node_svg(node: dict, view_id: str, colors: dict[str, str]) -> str:
    x, y = _node_position(node, view_id)
    node_id = node["id"]
    kind = node["kind"]
    tier = node["tier"]
    label = node["label"]
    fill = colors["panel"]
    stroke = colors["possible"] if node.get("modality") == "possible" else colors["line"]
    stroke_dash = "6 7" if node.get("modality") == "possible" else None
    parts = [f"<g{_attrs({'id': node_id, 'data-kind': kind, 'data-tier': tier})}>"]
    if kind == "commitment":
        points = f"{x:.1f},{y - 46:.1f} {x + 58:.1f},{y:.1f} {x:.1f},{y + 46:.1f} {x - 58:.1f},{y:.1f}"
        parts.append(f"<polygon{_attrs({'points': points, 'fill': colors['accent'], 'stroke': stroke, 'stroke-width': 2.5})}/>")
    elif kind == "receipt":
        parts.append(f"<rect{_attrs({'x': x - 68, 'y': y - 40, 'width': 136, 'height': 80, 'rx': 6, 'fill': fill, 'stroke': colors['accent'], 'stroke-width': 3})}/>")
        parts.append(f"<path{_attrs({'d': f'M {x - 48:.1f} {y - 14:.1f} H {x + 48:.1f} M {x - 48:.1f} {y + 8:.1f} H {x + 30:.1f}', 'fill': 'none', 'stroke': colors['accent'], 'stroke-width': 1.5})}/>")
    elif kind == "trace":
        parts.append(f"<rect{_attrs({'x': x - 82, 'y': y - 42, 'width': 164, 'height': 84, 'rx': 22, 'fill': fill, 'stroke': colors['gold'], 'stroke-width': 3})}/>")
        parts.append(f"<ellipse{_attrs({'cx': x, 'cy': y - 26, 'rx': 62, 'ry': 11, 'fill': 'none', 'stroke': colors['gold'], 'stroke-width': 1.5})}/>")
    elif kind == "crossing":
        points = f"{x:.1f},{y - 15:.1f} {x + 15:.1f},{y:.1f} {x:.1f},{y + 15:.1f} {x - 15:.1f},{y:.1f}"
        parts.append(f"<polygon{_attrs({'points': points, 'fill': colors['accent'], 'stroke': stroke, 'stroke-width': 1.5})}/>")
    else:
        radius = 31 if node_id.startswith("d") and node_id[1:].isdigit() else 42
        parts.append(f"<circle{_attrs({'cx': x, 'cy': y, 'r': radius, 'fill': fill, 'stroke': stroke, 'stroke-width': 2.5, 'stroke-dasharray': stroke_dash})}/>")
    font_size = 12 if kind == "crossing" else 14
    text_color = colors["background"] if kind == "commitment" else colors["ink"]
    parts.append(_text(x, y + (4 if kind != "receipt" else 29), label, fill=text_color, **{"font-family": "sans-serif", "font-size": font_size, "font-weight": 700, "text-anchor": "middle"}))
    if kind not in {"crossing", "commitment"}:
        parts.append(_text(x + 30, y - 29, f"[{tier}]", fill=colors["accent"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def _titan_frame_svg(frame: dict, view_id: str, colors: dict[str, str]) -> str:
    if view_id == "proof":
        x, top, bottom = 785, 150, 655
    else:
        x, top, bottom = 760, 135, 790
    marks = frame["markLabels"]
    loci = [
        ("horizon", top, "∞", marks["horizon"]),
        ("finity", (top + bottom) / 2, "1", marks["finity"]),
        ("bullet", bottom, "0", marks["bullet"]),
    ]
    parts = [f"<g{_attrs({'id': frame['id'], 'data-acting': 'false', 'data-display-loci-only': 'true'})}>"]
    parts.append(f"<line{_attrs({'x1': x, 'y1': top, 'x2': x, 'y2': bottom, 'stroke': colors['gold'], 'stroke-width': 3})}/>")
    for name, y, symbol, label in loci:
        parts.append(f"<circle{_attrs({'id': f'titan-{name}', 'cx': x, 'cy': y, 'r': 15 if name == 'finity' else 11, 'fill': colors['background'] if name != 'finity' else colors['gold'], 'stroke': colors['gold'], 'stroke-width': 3})}/>")
        parts.append(_text(x - 28, y + 6, symbol, fill=colors["ink"], **{"font-family": "serif", "font-size": 23, "font-weight": 700, "text-anchor": "end"}))
        parts.append(_text(x + 28, y + 5, label, fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 12, "font-weight": 700}))
    parts.append(_text(x, bottom + 34, "BOUNDARY FRAME · NEVER AN ACTOR", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700, "letter-spacing": 1.4, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def _proof_extras(topology: dict, colors: dict[str, str]) -> str:
    parts: list[str] = []
    cones = topology["cones"]
    parts.append(f"<g{_attrs({'id': cones['physical']['id']})}>")
    parts.append(f"<path{_attrs({'d': 'M 355 650 L 785 403 L 1215 650', 'fill': 'none', 'stroke': colors['muted'], 'stroke-width': 2})}/>")
    parts.append(_text(365, 638, "J+ · c-BOUNDED PHYSICAL ENVELOPE [A]", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700, "letter-spacing": 0.8}))
    parts.append("</g>")
    parts.append(f"<g{_attrs({'id': cones['option']['id']})}>")
    for target_y in (270, 345, 420):
        parts.append(f"<line{_attrs({'x1': 620, 'y1': 400, 'x2': 470, 'y2': target_y, 'stroke': colors['possible'], 'stroke-width': 2, 'stroke-dasharray': '6 8'})}/>")
    parts.append(_text(365, 250, "Ω · MODELED / SELECTABLE / REACHABLE", fill=colors["possible"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700, "letter-spacing": 0.8}))
    parts.append("</g>")

    bridge = topology["reflexiveBridge"]
    parts.append(f"<g{_attrs({'id': 'reflexive-bridge-panel'})}>")
    parts.append(f"<rect{_attrs({'x': 1225, 'y': 130, 'width': 325, 'height': 270, 'rx': 14, 'fill': colors['panel'], 'stroke': colors['panel2'], 'stroke-width': 2})}/>")
    parts.append(_text(1250, 163, "REFLEXIVE BRIDGE", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 15, "font-weight": 800, "letter-spacing": 1.2}))
    for index, gap in enumerate(bridge["slippages"]):
        parts.append(_text(1250, 198 + index * 38, f"0{index + 1}  {gap['label']}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 12, "font-weight": 700}))
    signs = {item["id"]: item["label"] for item in bridge["feedbackSigns"]}
    parts.append(_text(1250, 324, f"−  {signs['negative']}", fill=colors["possible"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700}))
    parts.append(_text(1250, 349, f"+  {signs['positive']}", fill=colors["accent"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700}))
    parts.append(_text(1250, 378, bridge["signBoundary"].upper(), fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 700, "letter-spacing": 0.8}))
    parts.append("</g>")

    boundary = topology["boundaries"][0]
    trace = next(node for node in topology["nodes"] if node["kind"] == "trace")
    parts.append(f"<g{_attrs({'id': 'egregoreotype-inset'})}>")
    parts.append(f"<rect{_attrs({'x': 1160, 'y': 430, 'width': 390, 'height': 290, 'rx': 14, 'fill': colors['panel'], 'stroke': colors['gold'], 'stroke-width': 2})}/>")
    parts.append(_text(1185, 463, "CANDIDATE EGREGOREOTYPE · SHARED TRACE [I]", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 13, "font-weight": 800, "letter-spacing": 0.7}))
    for index, criterion in enumerate(trace["criteria"]):
        parts.append(_text(1185, 494 + index * 26, f"• {criterion.replace('-', ' ')}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 11}))
    fields = " · ".join(boundary["fields"].keys())
    parts.append(_multiline_text(1185, 608, fields, 48, 18, fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700}))
    parts.append(_text(1185, 691, trace["claimBoundary"].upper(), fill=colors["danger"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.6}))
    parts.append("</g>")

    quantum_nodes = [node for node in topology["nodes"] if node.get("overlay") == "quantum"]
    if quantum_nodes:
        parts.append(f"<g{_attrs({'id': 'quantum-inset', 'data-overlay': 'quantum'})}>")
        parts.append(f"<rect{_attrs({'x': 55, 'y': 535, 'width': 275, 'height': 185, 'rx': 12, 'fill': colors['panel'], 'stroke': colors['danger'], 'stroke-width': 2, 'stroke-dasharray': '5 6'})}/>")
        parts.append(_text(78, 568, "QUARANTINED QUANTUM INSET [C]", fill=colors["danger"], **{"font-family": "sans-serif", "font-size": 12, "font-weight": 800, "letter-spacing": 0.7}))
        for index, node in enumerate(quantum_nodes):
            parts.append(_text(78, 600 + index * 25, f"• {node['label']}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 10}))
        parts.append(_text(78, 690, "REMOVABLE · CORE MUST STILL RENDER", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 700}))
        parts.append("</g>")

    projection = topology["rosettaProjection"]
    parts.append(f"<g{_attrs({'id': 'rosetta-projection-label'})}>")
    parts.append(_text(80, 760, f"{projection['label']}  →  {projection['boundary'].upper()}", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700, "letter-spacing": 0.8}))
    parts.append("</g>")
    return "".join(parts)


def _emblem_extras(topology: dict, colors: dict[str, str]) -> str:
    parts = [f"<g{_attrs({'id': 'master-emblem-geometry'})}>"]
    parts.append(f"<path{_attrs({'d': 'M 270 770 L 760 455 L 1250 770', 'fill': 'none', 'stroke': colors['muted'], 'stroke-width': 2, 'opacity': 0.55})}/>")
    for y in (270, 350, 430):
        parts.append(f"<line{_attrs({'x1': 560, 'y1': 350, 'x2': 690, 'y2': y, 'stroke': colors['gold'], 'stroke-width': 2, 'stroke-dasharray': '5 9', 'opacity': 0.8})}/>")
    parts.append(_text(270, 792, "J+ · PHYSICAL ENVELOPE", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700, "letter-spacing": 1.0}))
    parts.append(_text(390, 230, "Ω · FALLIBLE OPTION FIELD", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700, "letter-spacing": 1.2}))
    parts.append("</g>")
    parts.append(f"<g{_attrs({'id': 'emblem-legend'})}>")
    parts.append(_multiline_text(800, 865, topology["fullTextEquivalent"], 105, 24, fill=colors["ink"], **{"font-family": "serif", "font-size": 17, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def render_view(topology: dict, view_id: str, topology_hash: str) -> str:
    """Render one deterministic SVG view entirely in memory."""
    if view_id not in {"proof", "emblem"}:
        raise ValueError(f"unknown view id: {view_id}")
    if not isinstance(topology_hash, str) or len(topology_hash) != 64:
        raise ValueError("topology_hash must be a 64-character SHA-256 hex string")
    view = topology.get("views", {}).get(view_id)
    if not isinstance(view, dict):
        raise ValueError(f"topology does not define view: {view_id}")
    width = int(view["width"])
    height = int(view["height"])
    colors = _palette(view_id)
    node_map = {node["id"]: node for node in topology["nodes"]}
    frame = next(node for node in topology["nodes"] if node["kind"] == "frame")

    if view_id == "proof":
        visible_nodes = [node for node in topology["nodes"] if node["kind"] != "frame"]
        visible_ids = {node["id"] for node in visible_nodes}
        visible_edges = [
            edge for edge in topology["edges"]
            if edge["from"] in visible_ids and edge["to"] in visible_ids
        ]
        title = "Burri Rules v0.1 — Canonical Proof Plate"
        desc = "Ivory proof plate showing the typed D0-D6 spine, Titan boundary frame, D5 option field, D4 commitment and receipt, reflexive return, collective trace boundary, and removable quantum correspondence."
    else:
        core = set(topology["operationalCore"])
        visible_nodes = [node for node in topology["nodes"] if node["id"] in core]
        visible_ids = {node["id"] for node in visible_nodes}
        visible_edges = [
            edge for edge in topology["edges"]
            if edge["from"] in visible_ids
            and edge["to"] in visible_ids
            and edge.get("overlay") != "quantum"
        ]
        title = "Burri Rules v0.1 — Master Emblem"
        desc = "Obsidian emblem of the nonacting Titan frame, fallible option field, finite commitment through D4 means, act, receipt, trace, and recursive return."

    lines = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        f"<svg{_attrs({'role': 'img', 'width': width, 'height': height, 'viewBox': f'0 0 {width} {height}', 'aria-labelledby': f'{view_id}-title {view_id}-desc'})}>",
        f"<title{_attrs({'id': f'{view_id}-title'})}>{escape(title)}</title>",
        f"<desc{_attrs({'id': f'{view_id}-desc'})}>{escape(desc)}</desc>",
        f"<metadata>rendererVersion={RENDERER_VERSION};topologySha256={escape(topology_hash)}</metadata>",
        f"<rect{_attrs({'x': 0, 'y': 0, 'width': width, 'height': height, 'fill': colors['background']})}/>",
        f"<defs><marker{_attrs({'id': f'arrow-{view_id}', 'viewBox': '0 0 10 10', 'refX': 9, 'refY': 5, 'markerWidth': 7, 'markerHeight': 7, 'orient': 'auto-start-reverse'})}><path{_attrs({'d': 'M 0 0 L 10 5 L 0 10 z', 'fill': colors['line']})}/></marker></defs>",
    ]
    if view_id == "proof":
        lines.extend(
            [
                _text(55, 58, "BURRI RULES · v0.1", fill=colors["accent"], **{"font-family": "sans-serif", "font-size": 14, "font-weight": 800, "letter-spacing": 2.2}),
                _text(55, 98, "THE CONSEQUENCE COMPILER", fill=colors["ink"], **{"font-family": "serif", "font-size": 30, "font-weight": 700, "letter-spacing": 1.1}),
                _text(1545, 58, "DRAFT [D] · SEMANTICS: 00_THE_BURRI_RULES.md", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 700, "letter-spacing": 0.9, "text-anchor": "end"}),
                _proof_extras(topology, colors),
            ]
        )
    else:
        lines.extend(
            [
                _text(800, 62, "BURRI RULES", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 13, "font-weight": 800, "letter-spacing": 4.5, "text-anchor": "middle"}),
                _text(800, 104, "THE MASTER EMBLEM", fill=colors["ink"], **{"font-family": "serif", "font-size": 31, "font-weight": 700, "letter-spacing": 1.5, "text-anchor": "middle"}),
                _emblem_extras(topology, colors),
            ]
        )

    lines.append(f"<g{_attrs({'id': 'edges'})}>")
    for edge in visible_edges:
        lines.append(_edge_svg(edge, node_map, view_id, colors))
    lines.append("</g>")
    lines.append(_titan_frame_svg(frame, view_id, colors))
    lines.append(f"<g{_attrs({'id': 'nodes'})}>")
    for node in visible_nodes:
        lines.append(_node_svg(node, view_id, colors))
    lines.append("</g>")

    if view_id == "proof":
        lines.append(_multiline_text(55, 936, topology["fullTextEquivalent"], 175, 21, fill=colors["ink"], **{"font-family": "serif", "font-size": 13}))
        lines.append(_text(1545, 966, f"TOPOLOGY SHA-256 · {topology_hash}", fill=colors["muted"], **{"font-family": "monospace", "font-size": 9, "text-anchor": "end"}))
    else:
        lines.append(_text(800, 970, f"RENDERER {RENDERER_VERSION} · TOPOLOGY {topology_hash[:16]}… · DRAFT [D]", fill=colors["muted"], **{"font-family": "monospace", "font-size": 9, "letter-spacing": 0.8, "text-anchor": "middle"}))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _validated_renderings(topology_path: Path, repo_root: Path) -> tuple[dict[Path, bytes], list[str]]:
    topology = load_topology(topology_path)
    validation_errors = validate_topology(topology, repo_root)
    if validation_errors:
        return {}, [f"topology: {error}" for error in validation_errors]
    digest = topology_sha256(topology_path)
    rendered: dict[Path, bytes] = {}
    for view_id in ("proof", "emblem"):
        output = Path(repo_root) / topology["views"][view_id]["output"]
        rendered[output] = render_view(topology, view_id, digest).encode("utf-8")
    return rendered, []


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_outputs(topology_path: Path, repo_root: Path) -> list[Path]:
    """Validate and atomically write both generated SVG outputs."""
    rendered, errors = _validated_renderings(Path(topology_path), Path(repo_root))
    if errors:
        raise ValueError("\n".join(errors))
    paths = list(rendered)
    for path in paths:
        _atomic_write(path, rendered[path])
    return paths


def check_outputs(topology_path: Path, repo_root: Path) -> list[str]:
    """Return path-specific missing/drift errors for generated outputs."""
    rendered, errors = _validated_renderings(Path(topology_path), Path(repo_root))
    if errors:
        return errors
    root = Path(repo_root).resolve()
    for path, expected in rendered.items():
        relative = path.resolve().relative_to(root).as_posix()
        if not path.exists():
            errors.append(f"{relative}: missing generated output; run --write")
        elif path.read_bytes() != expected:
            errors.append(f"{relative}: generated output drift; run --write")
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and render the Burri Rules topology into deterministic SVGs."
    )
    parser.add_argument("--write", action="store_true", help="atomically write both SVG outputs")
    parser.add_argument("--check", action="store_true", help="check tracked SVG bytes for drift")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the renderer CLI."""
    parser = _parser()
    args = parser.parse_args(argv)
    if int(args.write) + int(args.check) != 1:
        parser.error("exactly one of --write or --check is required")
    repo_root = Path(__file__).resolve().parents[2]
    topology_path = repo_root / "05_COSMOLOGY" / "00_BURRI_RULES_TOPOLOGY.json"
    if args.write:
        try:
            written = write_outputs(topology_path, repo_root)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(str(error), file=os.sys.stderr)
            return 2
        for path in written:
            print(f"wrote {path.relative_to(repo_root).as_posix()}")
        print(f"topology sha256 {topology_sha256(topology_path)}")
        return 0
    try:
        errors = check_outputs(topology_path, repo_root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=os.sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(error, file=os.sys.stderr)
        return 1
    print(f"Burri Rules outputs match topology {topology_sha256(topology_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

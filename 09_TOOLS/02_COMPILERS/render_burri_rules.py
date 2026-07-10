#!/usr/bin/env python3
"""Validate and deterministically render the Burri Rules topology.

The Markdown rulebook owns semantics. This compiler accepts only geometry and
source references, then produces two deterministic, accessible SVG views.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
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
SOROS_SOURCE_ID = "src-soros"
SOROS_URL = (
    "https://www.opensocietyfoundations.org/uploads/"
    "9ae17912-2262-4646-8ffc-d01afc934c36/"
    "george-soros-general-theory-of-reflexivity-transcript.pdf"
)
REQUIRED_NODE_TYPES = {
    "d5-model": ("state", "D5", "possible", "forward", "S"),
    "d5-selector": ("state", "D5", "possible", "forward", "S"),
    "d5-option-a": ("state", "D5", "possible", "forward", "I"),
    "d5-option-b": ("state", "D5", "possible", "forward", "I"),
    "d4-means": ("state", "D4", "actual", "forward", "S"),
    "signature": ("state", "D4", "actual", "coupling", "S"),
    "chi": ("commitment", "D4", "actual", "forward", "S"),
    "d4-action": ("state", "D4", "actual", "forward", "S"),
    "receipt": ("receipt", "D4", "actual", "feedback", "S"),
    "shared-trace": ("trace", "D4", "actual", "coupling", "I"),
}
REQUIRED_EDGE_TYPES = {
    "e-d5-model": ("d5", "d5-model", "D5", "possible", "forward"),
    "e-d5-selector": ("d5", "d5-selector", "D5", "possible", "forward"),
    "e-model-option-a": ("d5-model", "d5-option-a", "D5", "possible", "forward"),
    "e-model-option-b": ("d5-model", "d5-option-b", "D5", "possible", "forward"),
    "e-selector-option-a": ("d5-selector", "d5-option-a", "D5", "possible", "coupling"),
    "e-selector-option-b": ("d5-selector", "d5-option-b", "D5", "possible", "coupling"),
    "e-model-chi": ("d5-model", "chi", "D5", "possible", "coupling"),
    "e-selector-chi": ("d5-selector", "chi", "D5", "possible", "coupling"),
    "e-option-a-chi": ("d5-option-a", "chi", "D5", "possible", "coupling"),
    "e-d4-means": ("d4", "d4-means", "D4", "actual", "forward"),
    "e-d4-signature": ("d4", "signature", "D4", "actual", "coupling"),
    "e-means-chi": ("d4-means", "chi", "D4", "actual", "forward"),
    "e-signature-chi": ("signature", "chi", "D4", "actual", "coupling"),
    "e-chi-action": ("chi", "d4-action", "D4", "actual", "forward"),
    "e-action-receipt": ("d4-action", "receipt", "D4", "actual", "forward"),
    "e-receipt-model-feedback": ("receipt", "d5-model", "D5", "actual", "feedback"),
    "e-receipt-trace": ("receipt", "shared-trace", "D4", "actual", "coupling"),
    "e-trace-selector": ("shared-trace", "d5-selector", "D5", "possible", "coupling"),
}
FULL_TEXT_EQUIVALENT = (
    "The Titans frame possibility; a finite agent forms a fallible D5 option field, "
    "commits through D4 means and authorization, receives D4 consequences, and "
    "recursively corrects both world-model and selector."
)

SPINE_IDS = tuple(
    item
    for number in range(7)
    for item in ((f"d{number}", f"mu-{number}") if number < 6 else (f"d{number}",))
)
SPINE_STATE_LABELS = {
    "d0": "Ground-limit",
    "d1": "Distinction",
    "d2": "Configuration",
    "d3": "Transform / persist",
    "d4": "Causal actuality",
    "d5": "Counterfactuals",
    "d6": "Apophatic closure",
}
SPINE_CROSSING_LABELS = {
    "mu-0": "distinction",
    "mu-1": "configuration",
    "mu-2": "transformation",
    "mu-3": "actuality",
    "mu-4": "counterfactuals",
    "mu-5": "closure",
}
PROOF_POSITIONS = {
    "d5-model": (730, 415),
    "d5-selector": (730, 505),
    "d5-option-a": (925, 415),
    "d5-option-b": (925, 505),
    "d4-means": (630, 650),
    "signature": (630, 760),
    "chi": (790, 650),
    "d4-action": (950, 650),
    "receipt": (1070, 650),
    "shared-trace": (1335, 610),
    "quantum-state": (1215, 855),
    "quantum-record": (1450, 855),
}
EMBLEM_POSITIONS = {
    "d5-model": (520, 405),
    "d5-selector": (520, 505),
    "d5-option-a": (705, 405),
    "d5-option-b": (705, 505),
    "d4-means": (520, 650),
    "signature": (665, 755),
    "chi": (820, 630),
    "d4-action": (1010, 630),
    "receipt": (1210, 630),
    "shared-trace": (1210, 760),
}
PROOF_DISPLAY_LABELS = {
    "d5-model": "world-model",
    "d5-selector": "selector",
    "d5-option-a": "selected option",
    "d5-option-b": "retained option",
    "d4-means": "finite means",
    "signature": "authorization",
    "chi": "commitment",
    "d4-action": "enacted action",
    "receipt": "consequence receipt",
    "shared-trace": "shared trace",
    "quantum-state": "D5 alternatives",
    "quantum-record": "D4 record",
}
EMBLEM_DISPLAY_LABELS = {
    "d5-model": "M_t model",
    "d5-selector": "V_t selector",
    "d5-option-a": "A selected",
    "d5-option-b": "B possible",
    "d4-means": "D4 means",
    "signature": "authorization",
    "chi": "chi commit",
    "d4-action": "a_t action",
    "receipt": "R_t+1 receipt",
    "shared-trace": "shared trace",
}
NODE_SYMBOLS = {
    "d5-model": "M",
    "d5-selector": "V",
    "d5-option-a": "A",
    "d5-option-b": "B",
    "d4-means": "D4",
    "signature": "SIG",
    "chi": "χ",
    "d4-action": "a",
    "receipt": "R",
    "shared-trace": "TRACE",
    "quantum-state": "D5",
    "quantum-record": "D4",
}


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


def _is_allowed(value: Any, allowed: set[str]) -> bool:
    """Return membership without hashing malformed JSON containers."""
    return isinstance(value, str) and value in allowed


def _refs_are_valid(
    element: dict,
    element_name: str,
    source_ids: set[str],
    errors: list[str],
) -> None:
    rule_ids = element.get("ruleIds")
    if not isinstance(rule_ids, list) or not rule_ids:
        errors.append(f"{element_name}: ruleIds must be a non-empty list")
    elif not all(_is_nonempty_string(value) for value in rule_ids):
        errors.append(f"{element_name}: ruleIds must contain non-empty strings")
    elif not set(rule_ids) <= RULE_IDS:
        errors.append(f"{element_name}: unknown rule reference")
    source_refs = element.get("sourceIds")
    if not isinstance(source_refs, list) or not source_refs:
        errors.append(f"{element_name}: sourceIds must be a non-empty list")
    elif not all(_is_nonempty_string(value) for value in source_refs):
        errors.append(f"{element_name}: sourceIds must contain non-empty strings")
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
    rule_ids: list[str] = []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"rule[{index}]: must be an object")
            continue
        rule_id = rule.get("id")
        if not _is_nonempty_string(rule_id):
            errors.append(f"rule[{index}]: id must be a non-empty string")
            continue
        rule_ids.append(rule_id)
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate rule id")
    if set(rule_ids) != RULE_IDS or len(rule_ids) != 6:
        errors.append("rules must contain exactly BR-1 through BR-6")

    sources = topology.get("sources", [])
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    source_ids_list: list[str] = []
    for source in sources:
        if isinstance(source, dict) and _is_nonempty_string(source.get("id")):
            source_ids_list.append(source["id"])
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
        if not _is_allowed(source.get("tier"), ALLOWED_TIERS):
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
    else:
        soros = remote_sources[0]
        if (
            soros.get("id") != SOROS_SOURCE_ID
            or soros.get("url") != SOROS_URL
            or soros.get("tier") != "B"
            or soros.get("crosswalkTier") != "I"
        ):
            errors.append("Soros source must retain its stable id, approved URL, B attribution, and I crosswalk")

    nodes = topology.get("nodes", [])
    edges = topology.get("edges", [])
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        edges = []
    all_elements = [item for item in nodes + edges if isinstance(item, dict)]
    seen: set[str] = set()
    for element in all_elements:
        element_id = element.get("id")
        if not _is_nonempty_string(element_id):
            errors.append("element id must be a non-empty string")
        elif element_id in seen:
            errors.append(f"duplicate element id: {element_id}")
        else:
            seen.add(element_id)

    node_ids = {
        node.get("id")
        for node in nodes
        if isinstance(node, dict) and _is_nonempty_string(node.get("id"))
    }
    for index, node in enumerate(nodes):
        name = f"node[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{name}: must be an object")
            continue
        node_id = node.get("id", name)
        name = f"node {node_id}"
        if not _is_allowed(node.get("kind"), ALLOWED_KINDS):
            errors.append(f"{name}: invalid kind")
        if not _is_allowed(node.get("dRegister"), ALLOWED_REGISTERS):
            errors.append(f"{name}: invalid dRegister")
        if not _is_allowed(node.get("modality"), ALLOWED_MODALITIES):
            errors.append(f"{name}: invalid modality")
        if not _is_allowed(node.get("role"), ALLOWED_ROLES):
            errors.append(f"{name}: invalid role")
        if not _is_allowed(node.get("tier"), ALLOWED_TIERS):
            errors.append(f"{name}: invalid tier")
        if not _is_nonempty_string(node.get("label")):
            errors.append(f"{name}: label must be non-empty")
        for coordinate in ("x", "y"):
            value = node.get(coordinate)
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
            ):
                errors.append(f"{name}: {coordinate} must be finite numeric geometry")
        _refs_are_valid(node, name, source_ids, errors)

    for index, edge in enumerate(edges):
        name = f"edge[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{name}: must be an object")
            continue
        edge_id = edge.get("id", name)
        name = f"edge {edge_id}"
        if not _is_nonempty_string(edge.get("from")) or edge.get("from") not in node_ids:
            errors.append(f"{name}: invalid from endpoint")
        if not _is_nonempty_string(edge.get("to")) or edge.get("to") not in node_ids:
            errors.append(f"{name}: invalid to endpoint")
        if not _is_allowed(edge.get("dRegister"), ALLOWED_REGISTERS):
            errors.append(f"{name}: invalid dRegister")
        if not _is_allowed(edge.get("modality"), ALLOWED_MODALITIES):
            errors.append(f"{name}: invalid modality")
        if not _is_allowed(edge.get("role"), ALLOWED_ROLES):
            errors.append(f"{name}: invalid role")
        if not _is_allowed(edge.get("tier"), ALLOWED_TIERS):
            errors.append(f"{name}: invalid tier")
        _refs_are_valid(edge, name, source_ids, errors)

    node_by_id = {
        node["id"]: node
        for node in nodes
        if isinstance(node, dict) and _is_nonempty_string(node.get("id"))
    }
    for node_id, expected in REQUIRED_NODE_TYPES.items():
        node = node_by_id.get(node_id)
        if node is None:
            errors.append(f"missing load-bearing node: {node_id}")
            continue
        actual = tuple(node.get(field) for field in ("kind", "dRegister", "modality", "role", "tier"))
        if actual != expected:
            errors.append(f"load-bearing node {node_id} must retain kind/register/modality/role/tier")

    edge_by_id = {
        edge["id"]: edge
        for edge in edges
        if isinstance(edge, dict) and _is_nonempty_string(edge.get("id"))
    }
    for edge_id, expected in REQUIRED_EDGE_TYPES.items():
        edge = edge_by_id.get(edge_id)
        if edge is None:
            errors.append(f"missing load-bearing edge: {edge_id}")
            continue
        actual = tuple(edge.get(field) for field in ("from", "to", "dRegister", "modality", "role"))
        if actual != expected:
            errors.append(f"load-bearing edge {edge_id} must retain endpoints/register/modality/role")
    feedback_edge = edge_by_id.get("e-receipt-model-feedback")
    if feedback_edge is not None and feedback_edge.get("updatePolicy") != "changed or explicit null-with-reason":
        errors.append("receipt feedback must retain changed or explicit null-with-reason policy")

    required_states = {f"d{number}" for number in range(7)}
    if not required_states <= node_ids:
        errors.append("nodes must include complete d0 through d6 spine")
    crossing_nodes = {
        node.get("id")
        for node in nodes
        if isinstance(node, dict)
        and node.get("kind") == "crossing"
        and _is_nonempty_string(node.get("id"))
    }
    expected_crossings = {f"mu-{number}" for number in range(6)}
    if crossing_nodes != expected_crossings or "mu-6" in node_ids:
        errors.append("crossing nodes must be exactly mu-0 through mu-5")
    edge_pairs = {
        (edge.get("from"), edge.get("to"))
        for edge in edges
        if isinstance(edge, dict)
        and _is_nonempty_string(edge.get("from"))
        and _is_nonempty_string(edge.get("to"))
    }
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
    else:
        marks = frames[0].get("marks")
        if (
            not isinstance(marks, dict)
            or set(marks) != {"bullet", "finity", "horizon"}
            or frames[0].get("acting") is not False
            or frames[0].get("displayLociOnly") is not True
        ):
            errors.append("Titan frame must be nonacting display loci bullet/finity/horizon")

    boundaries = topology.get("boundaries", [])
    if not isinstance(boundaries, list) or len(boundaries) != 1:
        errors.append("exactly one collective boundary is required")
    else:
        if not isinstance(boundaries[0], dict):
            errors.append("collective boundary must be an object")
        fields = boundaries[0].get("fields", {}) if isinstance(boundaries[0], dict) else {}
        if not isinstance(fields, dict) or not BOUNDARY_FIELDS <= set(fields):
            errors.append("collective boundary is missing required fields")

    traces = [node for node in nodes if isinstance(node, dict) and node.get("kind") == "trace"]
    if len(traces) != 1:
        errors.append("exactly one shared trace node is required")
    else:
        criteria = traces[0].get("criteria")
        if (
            not isinstance(criteria, list)
            or not all(_is_nonempty_string(value) for value in criteria)
            or set(criteria) != TRACE_CRITERIA
        ):
            errors.append("shared trace must declare all four Egregoreotype criteria")
        if "no consciousness claim" not in str(traces[0].get("claimBoundary", "")).lower():
            errors.append("shared trace must carry the no consciousness claim boundary")

    bridge = topology.get("reflexiveBridge", {})
    if not isinstance(bridge, dict):
        errors.append("Reflexive Bridge must be an object")
        bridge = {}
    slippages = bridge.get("slippages", [])
    if not isinstance(slippages, list):
        errors.append("Reflexive Bridge slippages must be a list")
        slippages = []
    slippage_ids = {
        item.get("id")
        for item in slippages
        if isinstance(item, dict) and _is_nonempty_string(item.get("id"))
    }
    if slippage_ids != {
        "cognitive-gap",
        "execution-gap",
        "outcome-gap",
    }:
        errors.append("Reflexive Bridge must name cognitive, execution, and outcome gaps")
    feedback_signs = bridge.get("feedbackSigns", [])
    if not isinstance(feedback_signs, list):
        errors.append("Reflexive Bridge feedbackSigns must be a list")
        feedback_signs = []
    signs = {
        item.get("id"): str(item.get("label", "")).lower()
        for item in feedback_signs
        if isinstance(item, dict) and _is_nonempty_string(item.get("id"))
    }
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
    if not isinstance(cones, dict):
        errors.append("cones must be an object")
        cones = {}
    physical = cones.get("physical", {})
    option = cones.get("option", {})
    if not isinstance(physical, dict):
        errors.append("physical cone must be an object")
        physical = {}
    if not isinstance(option, dict):
        errors.append("option cone must be an object")
        option = {}
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
            if not isinstance(view, dict):
                errors.append(f"view {view_id}: must be an object")
                continue
            if view.get("output") != expected_output:
                errors.append(f"view {view_id}: output must be {expected_output}")
            if view.get("width") != 1600 or view.get("height") != 1000:
                errors.append(f"view {view_id}: dimensions must be 1600x1000")

    operational_core = topology.get("operationalCore", [])
    if (
        not isinstance(operational_core, list)
        or not operational_core
        or not all(_is_nonempty_string(value) for value in operational_core)
    ):
        errors.append("operationalCore must be a non-empty node-id list")
    else:
        core = set(operational_core)
        if not core <= node_ids:
            errors.append("operationalCore references missing nodes")
        quantum_nodes = {
            node.get("id") for node in nodes
            if isinstance(node, dict)
            and node.get("overlay") == "quantum"
            and _is_nonempty_string(node.get("id"))
        }
        if core & quantum_nodes:
            errors.append("operationalCore may not depend on quantum overlay nodes")
        adjacency = {node_id: set() for node_id in core}
        for edge in edges:
            if not isinstance(edge, dict) or edge.get("overlay") == "quantum":
                continue
            start, end = edge.get("from"), edge.get("to")
            if (
                _is_nonempty_string(start)
                and _is_nonempty_string(end)
                and start in core
                and end in core
            ):
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
    node_id = node.get("id")
    if node_id in SPINE_IDS:
        start, step = (70, 84) if view_id == "proof" else (180, 70)
        return float(start + SPINE_IDS.index(node_id) * step), 180.0
    positions = PROOF_POSITIONS if view_id == "proof" else EMBLEM_POSITIONS
    if node_id in positions:
        x, y = positions[node_id]
        return float(x), float(y)
    return float(node.get("x", 0)), float(node.get("y", 0))


def _edge_svg(edge: dict, node_map: dict[str, dict], view_id: str, colors: dict[str, str]) -> str:
    start_node = node_map[edge["from"]]
    end_node = node_map[edge["to"]]
    x1, y1 = _node_position(start_node, view_id)
    x2, y2 = _node_position(end_node, view_id)
    color = colors["possible"] if edge.get("modality") == "possible" else colors["line"]
    dash = "7 9" if edge.get("modality") == "possible" else None
    common = {
        "id": edge["id"],
        "data-modality": edge.get("modality"),
        "data-role": edge.get("role"),
        "data-tier": edge.get("tier"),
        "fill": "none",
        "stroke": color,
        "stroke-width": 2.1 if view_id == "proof" else 2.6,
        "stroke-dasharray": dash,
        "stroke-linecap": "round",
        "marker-end": f"url(#arrow-{view_id})",
        "opacity": 0.88,
    }
    custom_paths: dict[str, str] = {}
    if view_id == "proof":
        custom_paths = {
            "e-d5-model": f"M {x1:.1f} {y1:.1f} C {x1:.1f} 300, 820 335, {x2:.1f} {y2:.1f}",
            "e-d5-selector": f"M {x1:.1f} {y1:.1f} C 890 315, 805 390, {x2:.1f} {y2:.1f}",
            "e-d4-means": f"M {x1:.1f} {y1:.1f} C 600 330, 555 500, {x2:.1f} {y2:.1f}",
            "e-d4-signature": f"M {x1:.1f} {y1:.1f} C 500 370, 520 625, {x2:.1f} {y2:.1f}",
            "e-model-option-b": f"M {x1:.1f} {y1:.1f} C 780 370, 985 355, {x2:.1f} {y2:.1f}",
            "e-selector-option-a": f"M {x1:.1f} {y1:.1f} C 780 550, 985 565, {x2:.1f} {y2:.1f}",
            "e-model-chi": f"M {x1:.1f} {y1:.1f} C 650 440, 650 600, {x2:.1f} {y2:.1f}",
            "e-receipt-model-feedback": f"M {x1:.1f} {y1:.1f} C 1110 330, 920 315, {x2:.1f} {y2:.1f}",
            "e-receipt-trace": f"M {x1:.1f} {y1:.1f} C 1140 650, 1210 610, {x2:.1f} {y2:.1f}",
            "e-trace-selector": f"M {x1:.1f} {y1:.1f} C 1260 815, 900 850, {x2:.1f} {y2:.1f}",
        }
    else:
        custom_paths = {
            "e-model-option-b": f"M {x1:.1f} {y1:.1f} C 570 355, 760 345, {x2:.1f} {y2:.1f}",
            "e-selector-option-a": f"M {x1:.1f} {y1:.1f} C 570 555, 760 565, {x2:.1f} {y2:.1f}",
            "e-receipt-model-feedback": f"M {x1:.1f} {y1:.1f} C 1210 300, 820 285, {x2:.1f} {y2:.1f}",
            "e-trace-selector": f"M {x1:.1f} {y1:.1f} C 1080 850, 690 850, {x2:.1f} {y2:.1f}",
        }
    if edge["id"] in custom_paths:
        return f"<path{_attrs({**common, 'd': custom_paths[edge['id']]})}/>"
    if edge.get("role") == "feedback":
        lift = 150 if view_id == "proof" else 230
        path = (
            f"M {x1:.1f} {y1:.1f} C {x1:.1f} {min(y1, y2) - lift:.1f}, "
            f"{x2:.1f} {min(y1, y2) - lift:.1f}, {x2:.1f} {y2:.1f}"
        )
        return f"<path{_attrs({**common, 'd': path})}/>"
    return f"<line{_attrs({**common, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})}/>"


def _node_svg(node: dict, view_id: str, colors: dict[str, str]) -> str:
    x, y = _node_position(node, view_id)
    node_id = node["id"]
    kind = node["kind"]
    tier = node["tier"]
    label_map = PROOF_DISPLAY_LABELS if view_id == "proof" else EMBLEM_DISPLAY_LABELS
    label = label_map.get(node_id, node["label"])
    symbol = NODE_SYMBOLS.get(node_id, label)
    fill = colors["panel"]
    stroke = colors["possible"] if node.get("modality") == "possible" else colors["line"]
    stroke_dash = "6 7" if node.get("modality") == "possible" else None
    group_attrs = {
        "id": node_id,
        "data-kind": kind,
        "data-tier": tier,
        "data-modality": node.get("modality"),
        "data-role": node.get("role"),
        "data-display-label": label,
        "aria-label": f"{node['label']} [{tier}]",
    }
    parts = [f"<g{_attrs(group_attrs)}>"]
    parts.append(f"<title>{escape(node['label'])} [{escape(tier)}]</title>")
    if kind == "commitment":
        points = f"{x:.1f},{y - 44:.1f} {x + 48:.1f},{y:.1f} {x:.1f},{y + 44:.1f} {x - 48:.1f},{y:.1f}"
        parts.append(f"<polygon{_attrs({'points': points, 'fill': colors['accent'], 'stroke': stroke, 'stroke-width': 2.5})}/>")
    elif kind == "receipt":
        parts.append(f"<rect{_attrs({'x': x - 62, 'y': y - 34, 'width': 124, 'height': 68, 'rx': 7, 'fill': fill, 'stroke': colors['accent'], 'stroke-width': 3})}/>")
        parts.append(f"<path{_attrs({'d': f'M {x - 42:.1f} {y + 12:.1f} H {x + 42:.1f}', 'fill': 'none', 'stroke': colors['accent'], 'stroke-width': 1.5})}/>")
    elif kind == "trace":
        parts.append(f"<rect{_attrs({'x': x - 74, 'y': y - 33, 'width': 148, 'height': 66, 'rx': 20, 'fill': fill, 'stroke': colors['gold'], 'stroke-width': 3})}/>")
        parts.append(f"<ellipse{_attrs({'cx': x, 'cy': y - 19, 'rx': 55, 'ry': 8, 'fill': 'none', 'stroke': colors['gold'], 'stroke-width': 1.4})}/>")
    elif kind == "crossing":
        points = f"{x:.1f},{y - 15:.1f} {x + 15:.1f},{y:.1f} {x:.1f},{y + 15:.1f} {x - 15:.1f},{y:.1f}"
        parts.append(f"<polygon{_attrs({'points': points, 'fill': colors['accent'], 'stroke': stroke, 'stroke-width': 1.5})}/>")
    else:
        radius = 28 if node.get("overlay") == "quantum" else 34
        parts.append(f"<circle{_attrs({'cx': x, 'cy': y, 'r': radius, 'fill': fill, 'stroke': stroke, 'stroke-width': 2.5, 'stroke-dasharray': stroke_dash})}/>")
    font_size = 12 if kind == "crossing" else 15
    text_color = colors["background"] if kind == "commitment" else colors["ink"]
    parts.append(_text(x, y + 5, symbol, fill=text_color, **{"font-family": "sans-serif", "font-size": font_size, "font-weight": 800, "text-anchor": "middle"}))
    label_y = y + (55 if kind not in {"receipt", "trace"} else 54)
    parts.append(_text(x, label_y, label, fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 11 if view_id == "proof" else 12, "font-weight": 700, "text-anchor": "middle"}))
    if view_id == "proof":
        parts.append(_text(x, label_y + 14, f"[{tier}]", fill=colors["accent"], **{"class": "tier-badge", "font-family": "sans-serif", "font-size": 9, "font-weight": 800, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def _titan_frame_svg(frame: dict, view_id: str, colors: dict[str, str]) -> str:
    if view_id == "proof":
        x, top, bottom = 190, 410, 755
    else:
        x, top, bottom = 130, 375, 735
    marks = frame["markLabels"] if view_id == "proof" else {
        "horizon": "open horizon",
        "finity": "finite boundary",
        "bullet": "Ground-limit",
    }
    loci = [
        ("horizon", top, "∞", marks["horizon"]),
        ("finity", (top + bottom) / 2, "1", marks["finity"]),
        ("bullet", bottom, "0", marks["bullet"]),
    ]
    parts = [f"<g{_attrs({'id': frame['id'], 'data-acting': 'false', 'data-display-loci-only': 'true', 'data-display-label': 'Titan frame', 'aria-label': frame['label']})}>"]
    parts.append(f"<title>{escape(frame['label'])}</title>")
    parts.append(f"<line{_attrs({'x1': x, 'y1': top, 'x2': x, 'y2': bottom, 'stroke': colors['gold'], 'stroke-width': 3})}/>")
    for name, y, symbol, label in loci:
        parts.append(f"<circle{_attrs({'id': f'titan-{name}', 'cx': x, 'cy': y, 'r': 15 if name == 'finity' else 11, 'fill': colors['background'] if name != 'finity' else colors['gold'], 'stroke': colors['gold'], 'stroke-width': 3})}/>")
        parts.append(_text(x - 28, y + 6, symbol, fill=colors["ink"], **{"font-family": "serif", "font-size": 23, "font-weight": 700, "text-anchor": "end"}))
        parts.append(_text(x + 28, y + 5, label, fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 700}))
    parts.append(_text(x, bottom + 31, "NONACTING BOUNDARY FRAME", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 1.2, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def _proof_extras(topology: dict, colors: dict[str, str]) -> str:
    parts: list[str] = []
    parts.append(_text(55, 333, "SOUL LOOP · D5 OPTIONS → χ → D4 RECEIPT → RETURN", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 14, "font-weight": 800, "letter-spacing": 1.1}))
    parts.append(f"<g{_attrs({'id': 'physical-cone'})}>")
    parts.append(f"<path{_attrs({'d': 'M 500 815 L 790 318 L 1110 815', 'fill': 'none', 'stroke': colors['muted'], 'stroke-width': 2.2})}/>")
    parts.append(_text(720, 792, "J+ · PHYSICAL LIGHT CONE · c-BOUNDED [A]", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 800, "letter-spacing": 0.7}))
    parts.append("</g>")
    parts.append(f"<g{_attrs({'id': 'option-cone'})}>")
    parts.append(f"<rect{_attrs({'x': 665, 'y': 365, 'width': 330, 'height': 205, 'rx': 24, 'fill': colors['panel'], 'fill-opacity': 0.62, 'stroke': colors['possible'], 'stroke-width': 2, 'stroke-dasharray': '7 9'})}/>")
    parts.append("</g>")
    parts.append(_text(55, 362, "SOLID = D4 ACTUAL · DOTTED = D5 POSSIBLE · CURVE = REFLEXIVE RETURN", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.6}))
    parts.append(f"<g{_attrs({'id': 'proof-annotations', 'data-box': '55 800 615 122'})}>")
    parts.append(f"<rect{_attrs({'x': 55, 'y': 800, 'width': 615, 'height': 122, 'rx': 10, 'fill': colors['panel'], 'stroke': colors['panel2'], 'stroke-width': 1.5})}/>")
    parts.append(_text(72, 823, "LOAD-BEARING PROOF ANNOTATIONS", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 10, "font-weight": 800, "letter-spacing": 0.8}))
    proof_lines = (
        "D5 [S/I] · M_t fallible world-model · V_t declared selector / value state",
        "BR-4 [S] · chi_t finite authorized commitment",
        "D4 [S] · a_t D4 enacted action → R_(t+1) consequence receipt",
        "BR-5 [I] · changed or explicit null-with-reason",
        "rho_domain [I] · type and tier preserved; no proof transfer",
    )
    for index, line in enumerate(proof_lines):
        parts.append(_text(72, 843 + index * 15, line, fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 700}))
    parts.append("</g>")
    return "".join(parts)


def _proof_overlay_annotations(colors: dict[str, str]) -> str:
    """Paint semantic edge labels last so paths cannot strike through them."""
    parts = [f"<g{_attrs({'id': 'proof-edge-annotations'})}>"]
    labels = (
        (680, 332, 350, 22, 855, 347, "RETURN [I] · receipt updates M,V or declares a reasoned null", colors["accent"], 9),
        (675, 368, 315, 23, 686, 384, "Ω OPTION CONE [I] · MODELED / RANKED / REACHABLE INSIDE J+", colors["possible"], 8.5),
        (675, 586, 230, 22, 790, 601, "χ_t(Ω_t, M_t, V_t, D4 means, signature)", colors["muted"], 8.5),
        (824, 617, 102, 20, 875, 631, "AUTHORIZED [S]", colors["accent"], 7.5),
        (964, 617, 100, 20, 1014, 631, "CONSEQUENCE [S]", colors["accent"], 7.5),
    )
    for x, y, width, height, tx, ty, label, color, size in labels:
        parts.append(f"<rect{_attrs({'x': x, 'y': y, 'width': width, 'height': height, 'rx': 5, 'fill': colors['background'], 'fill-opacity': 0.94})}/>")
        anchor = "middle" if tx != x + 11 else "start"
        parts.append(_text(tx, ty, label, fill=color, **{"class": "edge-annotation", "font-family": "sans-serif", "font-size": size, "font-weight": 800, "text-anchor": anchor}))
    parts.append("</g>")
    return "".join(parts)


def _emblem_extras(topology: dict, colors: dict[str, str]) -> str:
    parts = [f"<g{_attrs({'id': 'master-emblem-geometry'})}>"]
    parts.append(f"<path{_attrs({'d': 'M 350 820 L 820 300 L 1450 820', 'fill': 'none', 'stroke': colors['muted'], 'stroke-width': 2.1, 'opacity': 0.65})}/>")
    parts.append(f"<rect{_attrs({'x': 445, 'y': 345, 'width': 340, 'height': 225, 'rx': 28, 'fill': colors['panel'], 'fill-opacity': 0.5, 'stroke': colors['possible'], 'stroke-width': 2, 'stroke-dasharray': '7 9'})}/>")
    parts.append(_text(350, 842, "J+ · c-BOUNDED PHYSICAL ENVELOPE", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.9}))
    parts.append("</g>")
    parts.append(f"<g{_attrs({'id': 'emblem-legend'})}>")
    parts.append(_multiline_text(800, 880, topology["fullTextEquivalent"], 112, 21, fill=colors["ink"], **{"font-family": "serif", "font-size": 15, "text-anchor": "middle"}))
    parts.append(_text(800, 944, "SOLID D4 ACTUAL · DOTTED D5 POSSIBLE · CURVED RETURN · [S] STRUCTURE / [I] CROSSWALK", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.8, "text-anchor": "middle"}))
    parts.append("</g>")
    return "".join(parts)


def _dimension_spine_svg(topology: dict, view_id: str, colors: dict[str, str]) -> str:
    """Render the complete D0..D6 / mu-0..mu-5 scaffold as a clean band."""
    node_map = {node["id"]: node for node in topology["nodes"]}
    if view_id == "proof":
        box = (50, 118, 1050, 198)
    else:
        box = (155, 132, 895, 145)
    x, y, width, height = box
    parts = [f"<g{_attrs({'id': 'dimension-spine', 'data-box': f'{x} {y} {width} {height}'})}>"]
    parts.append(f"<rect{_attrs({'x': x, 'y': y, 'width': width, 'height': height, 'rx': 14, 'fill': colors['panel'], 'fill-opacity': 0.72, 'stroke': colors['panel2'], 'stroke-width': 1.5})}/>")
    if view_id == "proof":
        parts.append(_text(70, 143, "D0 → μ₀ → … → D6 · STRUCTURAL / INTERPRETIVE SCAFFOLD [S]", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.65}))

    spine_edges = [
        edge
        for edge in topology["edges"]
        if edge["from"] in SPINE_IDS
        and edge["to"] in SPINE_IDS
        and not edge.get("closure")
    ]
    for edge in spine_edges:
        parts.append(_edge_svg(edge, node_map, view_id, colors))

    closure = next(edge for edge in topology["edges"] if edge.get("closure") is True)
    d6x, d6y = _node_position(node_map["d6"], view_id)
    d0x, d0y = _node_position(node_map["d0"], view_id)
    curve_y = 296 if view_id == "proof" else 252
    closure_attrs = {
        "id": closure["id"],
        "data-modality": closure["modality"],
        "data-role": closure["role"],
        "data-tier": closure["tier"],
        "d": f"M {d6x:.1f} {d6y:.1f} C {d6x:.1f} {curve_y:.1f}, {d0x:.1f} {curve_y:.1f}, {d0x:.1f} {d0y:.1f}",
        "fill": "none",
        "stroke": colors["possible"],
        "stroke-width": 1.8 if view_id == "proof" else 2.2,
        "stroke-dasharray": "7 9",
        "marker-end": f"url(#arrow-{view_id})",
    }
    parts.append(f"<path{_attrs(closure_attrs)}/>")
    parts.append(_text((d0x + d6x) / 2, curve_y - 5, "D6 ≡ D0 · DECLARED CLOSURE · NO μ₆", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 8 if view_id == "proof" else 9, "font-weight": 800, "letter-spacing": 0.55, "text-anchor": "middle"}))

    for node_id in SPINE_IDS:
        node = node_map[node_id]
        nx, ny = _node_position(node, view_id)
        possible = node.get("modality") == "possible"
        stroke = colors["possible"] if possible else colors["line"]
        dash = "5 6" if possible else None
        if node_id.startswith("d"):
            symbol = node_id.upper()
            display = symbol if view_id == "emblem" else f"{symbol} {SPINE_STATE_LABELS[node_id]}"
        else:
            number = node_id.split("-", 1)[1]
            symbol = f"μ{number}"
            display = symbol if view_id == "emblem" else f"{symbol} {SPINE_CROSSING_LABELS[node_id]}"
        group_attrs = {
            "id": node_id,
            "data-kind": node["kind"],
            "data-tier": node["tier"],
            "data-modality": node["modality"],
            "data-role": node["role"],
            "data-display-label": display,
            "aria-label": f"{node['label']} [{node['tier']}]",
        }
        parts.append(f"<g{_attrs(group_attrs)}><title>{escape(node['label'])} [{escape(node['tier'])}]</title>")
        if node_id.startswith("d"):
            radius = 22 if view_id == "proof" else 18
            parts.append(f"<circle{_attrs({'cx': nx, 'cy': ny, 'r': radius, 'fill': colors['panel'], 'stroke': stroke, 'stroke-width': 2, 'stroke-dasharray': dash})}/>")
        else:
            radius = 12 if view_id == "proof" else 10
            points = f"{nx:.1f},{ny - radius:.1f} {nx + radius:.1f},{ny:.1f} {nx:.1f},{ny + radius:.1f} {nx - radius:.1f},{ny:.1f}"
            parts.append(f"<polygon{_attrs({'points': points, 'fill': colors['accent'], 'stroke': stroke, 'stroke-width': 1.4, 'stroke-dasharray': dash})}/>")
        parts.append(_text(nx, ny + 4, symbol, fill=colors["ink"] if node_id.startswith("d") else colors["background"], **{"font-family": "sans-serif", "font-size": 10 if view_id == "proof" else 9, "font-weight": 800, "text-anchor": "middle"}))
        if view_id == "proof":
            description = (
                SPINE_STATE_LABELS[node_id]
                if node_id in SPINE_STATE_LABELS
                else f"opens {SPINE_CROSSING_LABELS[node_id]}"
            )
            label_y = 220 if node_id in SPINE_STATE_LABELS else 251
            parts.append(_text(nx, label_y, description, fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700, "text-anchor": "middle"}))
            parts.append(_text(nx, label_y + 13, f"[{node['tier']}]", fill=colors["accent"], **{"class": "tier-badge", "font-family": "sans-serif", "font-size": 8, "font-weight": 800, "text-anchor": "middle"}))
        parts.append("</g>")
    parts.append("</g>")
    return "".join(parts)


def _proof_insets_svg(topology: dict, colors: dict[str, str]) -> str:
    """Render three isolated proof insets; quantum content occurs only here."""
    node_map = {node["id"]: node for node in topology["nodes"]}
    bridge = topology["reflexiveBridge"]
    boundary = topology["boundaries"][0]
    trace = node_map["shared-trace"]
    parts = [f"<g{_attrs({'id': 'proof-insets'})}>"]

    parts.append(f"<g{_attrs({'id': 'reflexive-bridge-panel', 'data-box': '1130 315 420 210'})}>")
    parts.append(f"<rect{_attrs({'x': 1130, 'y': 315, 'width': 420, 'height': 210, 'rx': 14, 'fill': colors['panel'], 'stroke': colors['panel2'], 'stroke-width': 2})}/>")
    parts.append(_text(1152, 344, "REFLEXIVE BRIDGE · THREE INSPECTABLE GAPS [I]", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 12, "font-weight": 800, "letter-spacing": 0.7}))
    for index, gap in enumerate(bridge["slippages"]):
        parts.append(_text(1152, 375 + index * 31, f"0{index + 1} · {gap['label']}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700}))
    signs = {item["id"]: item["label"] for item in bridge["feedbackSigns"]}
    parts.append(_text(1152, 472, f"− {signs['negative']}", fill=colors["possible"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 800}))
    parts.append(_text(1152, 492, f"+ {signs['positive']}", fill=colors["accent"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 800}))
    parts.append(_text(1152, 513, "DYNAMICAL SIGNS, NOT MORAL VERDICTS · SOROS [B] / CROSSWALK [I]", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 7.5, "font-weight": 800, "letter-spacing": 0.4}))
    parts.append("</g>")

    parts.append(f"<g{_attrs({'id': 'egregoreotype-inset', 'data-box': '1130 540 420 230'})}>")
    parts.append(f"<rect{_attrs({'x': 1130, 'y': 540, 'width': 420, 'height': 230, 'rx': 14, 'fill': colors['panel'], 'stroke': colors['gold'], 'stroke-width': 2})}/>")
    parts.append(_text(1152, 566, "CANDIDATE EGREGOREOTYPE · PERSISTENT SHARED TRACE [I]", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 800, "letter-spacing": 0.55}))
    parts.append(_node_svg(trace, "proof", colors))
    criteria = [criterion.replace("-", " ") for criterion in trace["criteria"]]
    parts.append(_text(1152, 704, f"• {criteria[0]}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700}))
    parts.append(_text(1350, 704, f"• {criteria[1]}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700}))
    parts.append(_text(1152, 722, f"• {criteria[2]}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700}))
    parts.append(_text(1350, 722, f"• {criteria[3]}", fill=colors["ink"], **{"font-family": "sans-serif", "font-size": 8.5, "font-weight": 700}))
    fields = " · ".join(boundary["fields"])
    parts.append(_text(1152, 744, fields, fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 8, "font-weight": 800}))
    parts.append(_text(1152, 761, "NO CONSCIOUSNESS OR SOVEREIGN SUPER-AGENT CLAIM", fill=colors["danger"], **{"font-family": "sans-serif", "font-size": 8, "font-weight": 800, "letter-spacing": 0.4}))
    parts.append("</g>")

    if "quantum-state" in node_map and "quantum-record" in node_map:
        quantum_state = node_map["quantum-state"]
        quantum_record = node_map["quantum-record"]
        qedge = next(
            edge
            for edge in topology["edges"]
            if edge["id"] == "e-quantum-correspondence"
        )
        parts.append(f"<g{_attrs({'id': 'quantum-inset', 'data-overlay': 'quantum', 'data-box': '1130 785 420 165'})}>")
        parts.append(f"<rect{_attrs({'x': 1130, 'y': 785, 'width': 420, 'height': 165, 'rx': 14, 'fill': colors['panel'], 'stroke': colors['danger'], 'stroke-width': 2, 'stroke-dasharray': '5 6'})}/>")
        parts.append(_text(1152, 813, "QUARANTINED BURRI CORRESPONDENCE [C]", fill=colors["danger"], **{"font-family": "sans-serif", "font-size": 11, "font-weight": 800, "letter-spacing": 0.65}))
        parts.append(_text(1332, 834, "CORRESPONDENCE, NEVER IDENTITY", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 8, "font-weight": 800, "text-anchor": "middle"}))
        qx1, qy1 = _node_position(quantum_state, "proof")
        qx2, qy2 = _node_position(quantum_record, "proof")
        parts.append(f"<line{_attrs({'id': qedge['id'], 'data-modality': qedge['modality'], 'data-role': qedge['role'], 'data-tier': qedge['tier'], 'x1': qx1 + 30, 'y1': qy1, 'x2': qx2 - 30, 'y2': qy2, 'stroke': colors['possible'], 'stroke-width': 1.8, 'stroke-dasharray': '7 9', 'marker-end': 'url(#arrow-proof)'})}/>")
        parts.append(_node_svg(quantum_state, "proof", colors))
        parts.append(_node_svg(quantum_record, "proof", colors))
        parts.append(_text(1152, 941, "REMOVABLE · NO EXTRA SPACETIME DIMENSION · OPERATIONAL CORE INDEPENDENT", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 7.5, "font-weight": 800, "letter-spacing": 0.35}))
        parts.append("</g>")
    parts.append("</g>")
    return "".join(parts)


def render_view(topology: dict, view_id: str, topology_hash: str) -> str:
    """Render one deterministic SVG view entirely in memory."""
    if view_id not in {"proof", "emblem"}:
        raise ValueError(f"unknown view id: {view_id}")
    if not isinstance(topology_hash, str) or re.fullmatch(r"[0-9a-fA-F]{64}", topology_hash) is None:
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
        central_nodes = [
            node
            for node in topology["nodes"]
            if node["id"] not in SPINE_IDS
            and node["kind"] != "frame"
            and node["id"] != "shared-trace"
            and node.get("overlay") != "quantum"
        ]
        title = "Burri Rules v0.1 — Canonical Proof Plate"
        desc = "Ivory proof plate showing the typed D0-D6 spine, Titan boundary frame, D5 option field, D4 commitment and receipt, reflexive return, collective trace boundary, and removable quantum correspondence."
    else:
        core = set(topology["operationalCore"])
        central_nodes = [
            node for node in topology["nodes"]
            if node["id"] in core and node["id"] not in SPINE_IDS
        ]
        title = "Burri Rules v0.1 — Master Emblem"
        desc = "Obsidian emblem of the nonacting Titan frame, fallible option field, finite commitment through D4 means, act, receipt, trace, and recursive return."

    soul_edge_ids = {
        edge["id"]
        for edge in topology["edges"]
        if edge.get("overlay") != "quantum"
        and not edge.get("closure")
        and not (edge["from"] in SPINE_IDS and edge["to"] in SPINE_IDS)
    }
    omitted_for_clarity = {
        "e-selector-chi",
    }
    if view_id == "emblem":
        omitted_for_clarity |= {
            "e-d5-selector",
            "e-d4-signature",
            "e-model-chi",
        }
    soul_edge_ids -= omitted_for_clarity
    soul_edges = [edge for edge in topology["edges"] if edge["id"] in soul_edge_ids]

    lines = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        f"<svg{_attrs({'xmlns': 'http://www.w3.org/2000/svg', 'role': 'img', 'width': width, 'height': height, 'viewBox': f'0 0 {width} {height}', 'data-view': view_id, 'data-layout': 'banded-v2', 'aria-labelledby': f'{view_id}-title {view_id}-desc'})}>",
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
            ]
        )
    else:
        lines.extend(
            [
                _text(800, 62, "BURRI RULES", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 13, "font-weight": 800, "letter-spacing": 4.5, "text-anchor": "middle"}),
                _text(800, 104, "THE MASTER EMBLEM", fill=colors["ink"], **{"font-family": "serif", "font-size": 31, "font-weight": 700, "letter-spacing": 1.5, "text-anchor": "middle"}),
            ]
        )

    lines.append(_dimension_spine_svg(topology, view_id, colors))
    lines.append(f"<g{_attrs({'id': 'soul-loop'})}>")
    lines.append(_proof_extras(topology, colors) if view_id == "proof" else _emblem_extras(topology, colors))
    lines.append(f"<g{_attrs({'id': 'edges'})}>")
    for edge in soul_edges:
        lines.append(_edge_svg(edge, node_map, view_id, colors))
    lines.append("</g>")
    lines.append(_titan_frame_svg(frame, view_id, colors))
    lines.append(f"<g{_attrs({'id': 'nodes'})}>")
    for node in central_nodes:
        lines.append(_node_svg(node, view_id, colors))
    lines.append("</g>")
    if view_id == "proof":
        lines.append(_proof_overlay_annotations(colors))
    else:
        lines.append(f"<g{_attrs({'id': 'emblem-overlay'})}>")
        lines.append(f"<rect{_attrs({'x': 455, 'y': 350, 'width': 245, 'height': 22, 'rx': 5, 'fill': colors['background'], 'fill-opacity': 0.94})}/>")
        lines.append(_text(465, 366, "Ω · OPTION CONE WITHIN J+", fill=colors["gold"], **{"font-family": "sans-serif", "font-size": 9, "font-weight": 800, "letter-spacing": 0.9}))
        lines.append("</g>")
    lines.append("</g>")

    if view_id == "proof":
        lines.append(_proof_insets_svg(topology, colors))
        lines.append(_text(55, 978, "IVORY PROOF · DRAFT [D] · REMOVE THE QUANTUM INSET AND THE OPERATIONAL CALCULUS REMAINS", fill=colors["muted"], **{"font-family": "sans-serif", "font-size": 8, "font-weight": 800, "letter-spacing": 0.5}))
        lines.append(_text(1545, 978, f"TOPOLOGY SHA-256 · {topology_hash}", fill=colors["muted"], **{"font-family": "monospace", "font-size": 8, "text-anchor": "end"}))
    else:
        lines.append(_text(800, 978, f"RENDERER {RENDERER_VERSION} · TOPOLOGY {topology_hash[:16]}… · DRAFT [D]", fill=colors["muted"], **{"font-family": "monospace", "font-size": 8, "letter-spacing": 0.8, "text-anchor": "middle"}))
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
            os.fchmod(handle.fileno(), 0o644)
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

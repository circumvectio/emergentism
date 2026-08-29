#!/usr/bin/env python3
"""Deterministic, offline Emergentism Frontier reference graph and projection."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "12_PUBLIC_SITE"
W7_REL = "03_METHODOLOGY/00_W7_SCIENCE_INTEGRATION_EXECUTION_REGISTER.yaml"
ROUTING_REL = "12_PUBLIC_SITE/living-map.json"
PROTOCOL_REL = "03_METHODOLOGY/03_PREREGISTRATIONS/frontier_protocol/README.md"
SCHEMA = HERE / "FrontierGraph.v1.schema.json"
TEMPLATE = HERE / "templates" / "frontier.html"
PUBLIC_DIR = SITE / "frontier"
PUBLIC_V1 = PUBLIC_DIR / "v1"

GRAPH_KEYS = {
    "schema_id", "protocol_version", "projection_state", "semantic_owner",
    "source_authority", "source_inputs", "role_firewall", "lifecycle",
    "gaps", "candidate_records", "frozen_test_records", "world_receipt_refs",
    "revision_records", "counts", "completeness_claim",
    "world_contact_accepted", "live_service",
}
GAP_KEYS = {
    "schema_id", "gap_id", "source_gap_id", "title", "tier",
    "maturity_state", "execution_requirement", "public_routing_state",
    "question", "native_objects", "native_equations",
    "accepted_domain_recovery", "permutation_challenge",
    "held_out_incremental_prediction", "independent_replication",
    "no_placement_rival", "kill_criterion", "survivor", "source_refs",
    "candidate_ids", "test_ids", "receipt_ids", "revision_ids", "public_href",
}
LAUNCH_COUNTS = {
    "gaps": 12,
    "candidates": 0,
    "frozen_tests": 0,
    "world_receipts": 0,
    "revisions": 0,
}
ROLE_FIREWALL = {
    "model": "CANDIDATE_CONTRIBUTOR_NO_AUTHORITY",
    "sensor": "OBSERVATION_CARRIER_NOT_INDEPENDENT_WITNESS",
    "principal": "EXTERNAL_MANDATE_AND_AUTHORIZATION_BEARER",
    "evidence_custodian": "INDEPENDENT_PROVENANCE_AND_RESULT_REFERENCE",
    "emergentism": "TYPING_VERSIONING_CUSTODY_AND_EXIT_PROTOCOL",
}
LIVE_SERVICE_NULL = {
    "enabled": False,
    "accepts_submissions": False,
    "accepts_payment": False,
    "accepts_credentials": False,
    "accepts_private_data": False,
    "sensor_ingestion": False,
    "model_execution": False,
    "may_sign": False,
    "may_authorize": False,
}


def canonical_bytes(value: Any) -> bytes:
    """Stable public JSON: sorted keys, finite values, one trailing newline."""

    return (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def load_json(path: str | Path) -> Any:
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON value: {value}")
        ),
    )


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def typed_sha256(path: str | Path) -> str:
    return "sha256:" + sha256_file(path)


def _source_paths(root: Path = ROOT) -> tuple[Path, Path]:
    return root / W7_REL, root / ROUTING_REL


def build_graph(root: Path = ROOT) -> dict[str, Any]:
    """Compose the reference graph without allowing the projection to own truth."""

    w7_path, routing_path = _source_paths(root)
    w7 = load_json(w7_path)
    routing = load_json(routing_path)
    w7_rows = w7.get("rows")
    route_rows = routing.get("openQuestions")
    order = w7.get("execution_order")
    if not isinstance(w7_rows, list) or not isinstance(route_rows, list):
        raise ValueError("Frontier sources must expose rows and openQuestions arrays")
    if not isinstance(order, list) or len(order) != 12 or len(set(order)) != 12:
        raise ValueError("W7 execution_order must contain twelve unique gap IDs")

    w7_by_id = {row.get("id"): (index, row) for index, row in enumerate(w7_rows)}
    route_by_id = {
        row.get("id"): (index, row) for index, row in enumerate(route_rows)
    }
    if set(w7_by_id) != set(order) or set(route_by_id) != set(order):
        raise ValueError("W7 and public routing must contain the same twelve GP IDs")

    w7_hash = typed_sha256(w7_path)
    routing_hash = typed_sha256(routing_path)
    gaps: list[dict[str, Any]] = []
    for source_id in order:
        w7_index, row = w7_by_id[source_id]
        route_index, route = route_by_id[source_id]
        gaps.append(
            {
                "schema_id": "FrontierGap.v1",
                "gap_id": f"frontier-gap:{source_id}",
                "source_gap_id": source_id,
                "title": row["title"],
                "tier": route["tier"],
                "maturity_state": row["maturity_state"],
                "execution_requirement": row["execution_state"],
                "public_routing_state": {
                    "maturity": route["maturityState"],
                    "execution": route["executionState"],
                    "program": route["programState"],
                },
                "question": route["question"],
                "native_objects": row["native_objects"],
                "native_equations": row["native_equations"],
                "accepted_domain_recovery": row["accepted_domain_recovery"],
                "permutation_challenge": row["permutation_challenge"],
                "held_out_incremental_prediction": row[
                    "held_out_incremental_prediction"
                ],
                "independent_replication": row["independent_replication"],
                "no_placement_rival": row["no_placement_rival"],
                "kill_criterion": row["kill_criterion"],
                "survivor": row["survivor"],
                "source_refs": [
                    {
                        "path": W7_REL,
                        "json_pointer": f"/rows/{w7_index}",
                        "sha256": w7_hash,
                        "authority": "canonical_gap_owner",
                    },
                    {
                        "path": ROUTING_REL,
                        "json_pointer": f"/openQuestions/{route_index}",
                        "sha256": routing_hash,
                        "authority": "public_routing_overlay",
                    },
                ],
                "candidate_ids": [],
                "test_ids": [],
                "receipt_ids": [],
                "revision_ids": [],
                "public_href": f"/frontier/v1/gaps/{source_id}.json",
            }
        )

    graph = {
        "schema_id": "FrontierGraph.v1",
        "protocol_version": "1.0.0",
        "projection_state": "OFFLINE_READY_DRAFT",
        "semantic_owner": PROTOCOL_REL,
        "source_authority": (
            "The W7 register owns canonical gap contracts; living-map.json owns "
            "public routing only; this graph is a deterministic reference projection."
        ),
        "source_inputs": [
            {
                "path": W7_REL,
                "sha256": w7_hash,
                "role": "canonical_gap_owner",
            },
            {
                "path": ROUTING_REL,
                "sha256": routing_hash,
                "role": "public_routing_overlay",
            },
        ],
        "role_firewall": ROLE_FIREWALL,
        "lifecycle": [
            "FrontierGap.v1",
            "FrontierCandidate.v1",
            "FrontierFrozenTest.v1",
            "FrontierWorldReceiptRef.v1",
            "FrontierRevision.v1",
        ],
        "gaps": gaps,
        "candidate_records": [],
        "frozen_test_records": [],
        "world_receipt_refs": [],
        "revision_records": [],
        "counts": LAUNCH_COUNTS,
        "completeness_claim": False,
        "world_contact_accepted": 0,
        "live_service": LIVE_SERVICE_NULL,
    }
    errors = validate_graph(graph, root=root)
    if errors:
        raise ValueError("; ".join(errors))
    return graph


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_graph(value: Any, *, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["FrontierGraph.v1 must be an object"]
    if set(value) != GRAPH_KEYS:
        errors.append("FrontierGraph.v1 field set drift")
    if value.get("schema_id") != "FrontierGraph.v1":
        errors.append("schema_id must be FrontierGraph.v1")
    if value.get("protocol_version") != "1.0.0":
        errors.append("protocol_version must be 1.0.0")
    if value.get("projection_state") != "OFFLINE_READY_DRAFT":
        errors.append("projection_state must remain OFFLINE_READY_DRAFT")
    if value.get("semantic_owner") != PROTOCOL_REL:
        errors.append("semantic owner drift")
    if value.get("role_firewall") != ROLE_FIREWALL:
        errors.append("role firewall drift")
    if value.get("live_service") != LIVE_SERVICE_NULL:
        errors.append("live service boundary drift")
    if value.get("completeness_claim") is not False:
        errors.append("Frontier cannot make a completeness claim")
    if value.get("world_contact_accepted") != 0:
        errors.append("launch graph cannot accept world contact")
    if value.get("lifecycle") != [
        "FrontierGap.v1",
        "FrontierCandidate.v1",
        "FrontierFrozenTest.v1",
        "FrontierWorldReceiptRef.v1",
        "FrontierRevision.v1",
    ]:
        errors.append("lifecycle order drift")

    source_inputs = value.get("source_inputs")
    if not isinstance(source_inputs, list) or len(source_inputs) != 2:
        errors.append("source_inputs must bind exactly W7 and the routing overlay")
        source_inputs = []
    expected_sources = {
        W7_REL: "canonical_gap_owner",
        ROUTING_REL: "public_routing_overlay",
    }
    seen_sources: set[str] = set()
    for source in source_inputs:
        if not isinstance(source, dict) or set(source) != {"path", "sha256", "role"}:
            errors.append("source input shape drift")
            continue
        rel = source.get("path")
        if rel in seen_sources:
            errors.append(f"duplicate source input: {rel}")
        seen_sources.add(rel)
        if expected_sources.get(rel) != source.get("role"):
            errors.append(f"source role drift: {rel}")
        path = root / str(rel)
        if not path.is_file():
            errors.append(f"source input missing: {rel}")
        elif source.get("sha256") != typed_sha256(path):
            errors.append(f"source hash drift: {rel}")
    if seen_sources != set(expected_sources):
        errors.append("source input set drift")

    gaps = value.get("gaps")
    if not isinstance(gaps, list) or len(gaps) != 12:
        errors.append("launch graph must contain twelve gaps")
        gaps = []
    gap_ids: set[str] = set()
    source_ids: set[str] = set()
    for gap in gaps:
        if not isinstance(gap, dict):
            errors.append("gap must be an object")
            continue
        if set(gap) != GAP_KEYS:
            errors.append(f"gap field set drift: {gap.get('gap_id')}")
        gap_id = gap.get("gap_id")
        source_id = gap.get("source_gap_id")
        if gap.get("schema_id") != "FrontierGap.v1":
            errors.append(f"gap schema drift: {gap_id}")
        if not isinstance(gap_id, str) or gap_id != f"frontier-gap:{source_id}":
            errors.append(f"gap identity mismatch: {gap_id}")
        if gap_id in gap_ids or source_id in source_ids:
            errors.append(f"duplicate gap identity: {gap_id}")
        gap_ids.add(str(gap_id))
        source_ids.add(str(source_id))
        for field in (
            "title", "tier", "maturity_state", "execution_requirement",
            "question", "native_objects", "native_equations",
            "accepted_domain_recovery", "permutation_challenge",
            "held_out_incremental_prediction", "independent_replication",
            "no_placement_rival", "kill_criterion", "survivor", "public_href",
        ):
            if not _nonempty_text(gap.get(field)):
                errors.append(f"{gap_id}.{field} must be non-empty text")
        routing = gap.get("public_routing_state")
        if not isinstance(routing, dict) or set(routing) != {
            "maturity", "execution", "program"
        } or any(not _nonempty_text(routing.get(key)) for key in routing):
            errors.append(f"{gap_id}.public_routing_state is invalid")
        for ids_field in ("candidate_ids", "test_ids", "receipt_ids", "revision_ids"):
            if gap.get(ids_field) != []:
                errors.append(f"{gap_id}.{ids_field} must be empty at v1 launch")
        refs = gap.get("source_refs")
        if not isinstance(refs, list) or len(refs) != 2:
            errors.append(f"{gap_id}.source_refs must contain two refs")
        elif {ref.get("authority") for ref in refs if isinstance(ref, dict)} != {
            "canonical_gap_owner", "public_routing_overlay"
        }:
            errors.append(f"{gap_id}.source_refs authority drift")

    for field in (
        "candidate_records", "frozen_test_records", "world_receipt_refs",
        "revision_records",
    ):
        if value.get(field) != []:
            errors.append(f"{field} must remain empty at v1 launch")
    if value.get("counts") != LAUNCH_COUNTS:
        errors.append("launch counts must remain 12/0/0/0/0")
    return errors


def validate_world_receipt(value: Any) -> list[str]:
    """Focused semantic guard beyond JSON shape for later receipt admission."""

    if not isinstance(value, dict):
        return ["world receipt must be an object"]
    errors: list[str] = []
    if value.get("schema_id") != "FrontierWorldReceiptRef.v1":
        errors.append("world receipt schema mismatch")
    if value.get("custodian_independent_of_test_actor") is not True:
        errors.append("test actor cannot certify its own independent world receipt")
    if value.get("custodian") == value.get("test_actor"):
        errors.append("world receipt custodian must differ from test actor")
    if value.get("adjudicates_claim") is not False:
        errors.append("world receipt cannot adjudicate its own claim")
    return errors


def _nav() -> str:
    nav = (SITE / "partials" / "core-nav.html").read_text(encoding="utf-8").strip()
    return nav.replace(
        'data-section="research"',
        'data-section="research" data-current-section="true"',
    )


def _footer() -> str:
    return (SITE / "partials" / "core-footer.html").read_text(encoding="utf-8").strip()


def _socket_html(gap: dict[str, Any], index: int) -> str:
    esc = lambda value: html.escape(str(value), quote=True)
    open_attr = " open" if index == 0 else ""
    source_id = esc(gap["source_gap_id"])
    route = gap["public_routing_state"]
    endpoint = gap["public_href"]
    return f'''<details class="fr-socket" id="{source_id}"{open_attr}>
  <summary>
    <span class="fr-socket__number">{index + 1:02d}</span>
    <span class="fr-socket__identity"><b>{source_id}</b><em>{esc(gap["title"])}</em></span>
    <span class="fr-socket__state">{esc(gap["tier"])} · {esc(gap["maturity_state"])}</span>
    <span class="fr-socket__open">Open object</span>
  </summary>
  <div class="fr-envelope">
    <div class="fr-envelope__question">
      <p class="fr-kicker">The gap</p>
      <h3>{esc(gap["question"])}</h3>
      <p class="fr-endpoint"><span>GET</span> <a href="{esc(endpoint)}">{esc(endpoint)}</a></p>
    </div>
    <dl class="fr-state-pair">
      <div><dt>Canonical execution requirement</dt><dd>{esc(gap["execution_requirement"])}</dd></div>
      <div><dt>Public routing only</dt><dd>{esc(route["maturity"])} · {esc(route["execution"])} · {esc(route["program"])}</dd></div>
    </dl>
    <div class="fr-triad" aria-label="Native recovery, no-placement rival, and discriminator">
      <article><p class="fr-kicker">Recover first</p><p>{esc(gap["accepted_domain_recovery"])}</p></article>
      <article><p class="fr-kicker">No-placement rival</p><p>{esc(gap["no_placement_rival"])}</p></article>
      <article class="fr-triad__decider"><p class="fr-kicker">Discriminator</p><p>{esc(gap["held_out_incremental_prediction"])}</p></article>
    </div>
    <div class="fr-decision-line">
      <article><p class="fr-kicker">Kill</p><p>{esc(gap["kill_criterion"])}</p></article>
      <article><p class="fr-kicker">Survivor</p><p>{esc(gap["survivor"])}</p></article>
      <article class="fr-empty-receipt"><p class="fr-kicker">World receipt</p><p>None in the Frontier v1 namespace.</p></article>
    </div>
    <details class="fr-machine-record">
      <summary>Read the machine-object fields</summary>
      <dl>
        <div><dt>schema_id</dt><dd>FrontierGap.v1</dd></div>
        <div><dt>gap_id</dt><dd>{esc(gap["gap_id"])}</dd></div>
        <div><dt>source owner</dt><dd>{esc(gap["source_refs"][0]["path"])}</dd></div>
        <div><dt>source hash</dt><dd>{esc(gap["source_refs"][0]["sha256"])}</dd></div>
      </dl>
    </details>
  </div>
</details>'''


def render_html(graph: dict[str, Any]) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    tokens = {
        "@@NAV@@": _nav(),
        "@@FOOTER@@": _footer(),
        "@@SOCKETS@@": "\n".join(
            _socket_html(gap, index) for index, gap in enumerate(graph["gaps"])
        ),
        "@@W7_HASH@@": graph["source_inputs"][0]["sha256"],
        "@@ROUTING_HASH@@": graph["source_inputs"][1]["sha256"],
    }
    for token, replacement in tokens.items():
        if template.count(token) != 1:
            raise ValueError(f"frontier template token count drift: {token}")
        template = template.replace(token, replacement)
    if "@@" in template:
        raise ValueError("frontier template contains an unresolved token")
    return template


def output_payloads(root: Path = ROOT) -> dict[Path, bytes]:
    graph = build_graph(root)
    outputs: dict[Path, bytes] = {
        PUBLIC_DIR / "index.html": render_html(graph).encode("utf-8"),
        PUBLIC_V1 / "catalog.json": canonical_bytes(graph),
        PUBLIC_V1 / "schema.json": SCHEMA.read_bytes(),
    }
    for gap in graph["gaps"]:
        outputs[
            PUBLIC_V1 / "gaps" / f"{gap['source_gap_id']}.json"
        ] = canonical_bytes(gap)
    return outputs


def generate(*, check: bool = False, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path, payload in output_payloads(root).items():
        if check:
            if not path.is_file():
                errors.append(f"missing generated output: {path.relative_to(root)}")
            elif path.read_bytes() != payload:
                errors.append(f"generated output drift: {path.relative_to(root)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    return errors

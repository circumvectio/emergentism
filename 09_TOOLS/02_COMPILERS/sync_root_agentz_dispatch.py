#!/usr/bin/env python3
"""Deterministically compile Rosetta source YAMLs into a side-output runtime view."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment boundary
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


SCRIPT = Path(__file__).resolve()
DOCUMENTS = SCRIPT.parents[3]
SOURCE_DIR = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents"
MANIFEST = SOURCE_DIR / "MANIFEST.sha256"
LOCAL_RUNTIME = (DOCUMENTS / ".codex/agents").resolve()
STONE_ROW = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"
GENERATIVE_TABLE = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/00_GENERATIVE_TABLE.md"
MASTER_STONE = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md"

ROW_FILES = {
    "L1": "rows/01_L1_candala_firewall.toml",
    "L2": "rows/02_L2_sudra_explorer.toml",
    "L3": "rows/03_L3_vaisya_auditor.toml",
    "L4": "rows/04_L4_ksatriya_executor.toml",
    "L5": "rows/05_L5_brahmana_architect.toml",
    "L6": "rows/06_L6_sadhu_compressor.toml",
    "L7": "rows/07_L7_rsi_constitution.toml",
}
EXPECTED_ROLE = {**{f"L{i}": "operational" for i in range(1, 5)}, **{f"L{i}": "boundary" for i in range(5, 8)}}
MUTATING = {"write", "edit", "bash"}
AUTH_FALSE = ("may_sign", "may_authorize", "may_publish", "may_transmit", "may_settle")
STOP_CONDITIONS = {
    "L1": "ambiguity_exceeds_direct_evidence",
    "L2": "candidates_ready_for_ranking",
    "L3": "ranked_options_with_uncertainty_and_risks",
    "L4": "action_committed_or_refused_or_escalated",
    "L5": "alternatives_risks_owners_and_kill_criteria_complete",
    "L6": "paths_successors_risks_and_reversibility_complete",
    "L7": "invariant_reason_scope_risks_downgrade_and_return_complete",
}
MISSION_MISROUTE_ACTION = "move_to_the_station_whose_pramana_and_stop_condition_can_close_it_or_split_into_independently_closable_missions; do_not_retry_unchanged"
LEGACY_FIELDS = {
    "input_type", "output_type", "evaluation_contract",
    "budget_source", "budget_required_fields", "full_closure_positions",
    "operator_tier", "balance_coordinate", "equation_domain", "d4_d5_contract",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects duplicate mapping keys."""


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest() -> list[tuple[str, str]]:
    pattern = re.compile(r"^([0-9a-f]{64})\s+\*?(.+?)\s*$")
    entries = []
    for lineno, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line)
        if not match:
            raise ValueError(f"{MANIFEST}:{lineno}: invalid manifest line")
        entries.append((match.group(2), match.group(1)))
    if len(entries) != 7 or len({name for name, _ in entries}) != 7:
        raise ValueError("manifest must list exactly seven unique YAML files")
    disk = {p.name for p in SOURCE_DIR.glob("*.agent.yaml")}
    listed = {name for name, _ in entries}
    if disk != listed:
        raise ValueError(f"manifest/disk set mismatch: listed={sorted(listed)} disk={sorted(disk)}")
    for name, pinned in entries:
        actual = sha256(SOURCE_DIR / name)
        if actual != pinned:
            raise ValueError(f"manifest hash mismatch for {name}: pinned={pinned} actual={actual}")
    return sorted(entries)


def load_yaml(path: Path) -> dict:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return data


def enabled_tools(spec: dict) -> tuple[list[str], list[str], bool]:
    enabled = []
    mutating = []
    all_ask = True
    for toolset in spec.get("tools", []):
        for item in toolset.get("configs", []):
            if item.get("enabled") is True:
                name = item.get("name")
                if not isinstance(name, str):
                    raise ValueError("enabled tool has no string name")
                enabled.append(name)
                if name in MUTATING:
                    mutating.append(name)
                    all_ask = all_ask and item.get("permission_policy", {}).get("type") == "always_ask"
    return sorted(set(enabled)), sorted(set(mutating)), all_ask


def permissions(enabled: list[str], mutating: list[str]) -> str:
    if mutating:
        return "mutating_tools_always_ask_task_scoped"
    if any(name.startswith("web_") for name in enabled):
        return "read_web_only"
    return "read_only"


def markdown_plain(value: str) -> str:
    """Remove the small Markdown vocabulary used inside the canonical row tables."""
    value = value.replace("**", "").replace("`", "").replace("*", "")
    return " ".join(value.strip().split())


def analogy_key(value: str) -> str:
    """Compare case/hyphen variants without weakening non-analogy fields."""
    return re.sub(r"[^0-9a-z]+", "", value.casefold())


def parse_canonical_rows() -> dict[str, dict[str, str]]:
    """Parse the two active Stone-owned seven-row tables; fail on shape drift."""
    stone_text = STONE_ROW.read_text(encoding="utf-8")
    required_fences = (
        "The geometry is `[A]`, given the selection.",
        "The count is `[S]` — selected, not derived.",
        "Every cross-domain cell is `[I]`",
        "`GEN7 ≠ G7`",
        "the seats approach them and never identify",
    )
    for fence in required_fences:
        if fence not in stone_text:
            raise ValueError(f"{STONE_ROW}: canonical fence missing: {fence}")
    stone_rows: dict[str, dict[str, str]] = {}
    for raw in stone_text.splitlines():
        if not re.match(r"^\| \*\*L[1-7]\*\* \|", raw):
            continue
        cells = [markdown_plain(cell) for cell in raw.strip().split("|")[1:-1]]
        if len(cells) != 12:
            raise ValueError(f"{STONE_ROW}: expected 12 cells, got {len(cells)}: {raw}")
        level = cells[0]
        stone_rows[level] = dict(zip(
            ("level", "caste", "operator", "g7", "pramana", "rep6", "vmosk", "balance", "reasoning", "ology", "regime", "deploy"),
            cells,
        ))
    generative_text = GENERATIVE_TABLE.read_text(encoding="utf-8")
    generative_rows: dict[str, dict[str, str]] = {}
    for raw in generative_text.splitlines():
        if not re.match(r"^\| `GEN7@1:L[1-7]` \|", raw):
            continue
        cells = [markdown_plain(cell) for cell in raw.strip().split("|")[1:-1]]
        if len(cells) != 6:
            raise ValueError(f"{GENERATIVE_TABLE}: expected 6 cells, got {len(cells)}: {raw}")
        level = cells[0].rsplit(":", 1)[-1]
        generative_rows[level] = dict(zip(
            ("stable_id", "projected", "caste", "analogy", "mathematical_note", "standing"),
            cells,
        ))
    expected = {f"L{i}" for i in range(1, 8)}
    if set(stone_rows) != expected or set(generative_rows) != expected:
        raise ValueError("canonical Stone tables must each contain exactly L1 through L7")
    return {level: {**stone_rows[level], **{f"generative_{key}": value for key, value in generative_rows[level].items()}} for level in sorted(expected)}


def validate_canonical_row(metadata: dict, projection: dict, canonical: dict, path: Path) -> None:
    level = metadata["level"]
    comparisons = {
        "caste": (metadata.get("caste"), canonical["caste"]),
        "operator": (metadata.get("operator"), canonical["operator"]),
        "g7_cell": (projection.get("g7_cell"), f"G7@1:{canonical['g7']}"),
        "rep6": (projection.get("rep6"), canonical["rep6"].removeprefix("— ")),
    }
    balance = {"→0 (limiting)": "B→0 (limiting)", "½": "B=1/2", "√3⁄2": "B=√3/2", "1": "B=1"}.get(canonical["balance"])
    comparisons["balance"] = (projection.get("balance"), balance)
    for key, (actual, expected) in comparisons.items():
        if actual != expected:
            raise ValueError(f"{path}: {level} differs from canonical Stone {key}: {actual!r} != {expected!r}")
    if canonical["pramana"] not in str(metadata.get("pramana", "")):
        raise ValueError(f"{path}: {level} pramana no longer carries canonical {canonical['pramana']!r}")
    if not str(projection.get("vmosk_a", "")).startswith(f"[I/C] {canonical['vmosk']}"):
        raise ValueError(f"{path}: {level} VMOSK-A no longer carries the canonical qualified cell")
    for key in ("reasoning", "ology", "regime"):
        if analogy_key(str(metadata.get(key, ""))) != analogy_key(canonical[key]):
            raise ValueError(f"{path}: {level} differs from canonical Stone {key}")
    expected_operational = canonical["deploy"] == "✓"
    if (canonical["deploy"] not in {"✓", "✗"} or projection.get("operational_move") is not expected_operational):
        raise ValueError(f"{path}: {level} deployability differs from canonical Stone")
    if canonical["generative_projected"] != f"{projection['g7_cell']} · {metadata['operator']}":
        raise ValueError(f"{path}: {level} G7/operator pair differs from Generative Table")
    if canonical["generative_caste"] != metadata["caste"]:
        raise ValueError(f"{path}: {level} caste differs from Generative Table")
    analogy = [analogy_key(part) for part in canonical["generative_analogy"].split("/")]
    current = [analogy_key(str(metadata[key])) for key in ("reasoning", "ology", "regime")]
    if analogy != current:
        raise ValueError(f"{path}: {level} analogy triple differs from Generative Table")
    if markdown_plain(str(projection.get("mathematical_note", ""))) != canonical["generative_mathematical_note"]:
        raise ValueError(f"{path}: {level} mathematical note differs from Generative Table")
    if level in {"L1", "L7"} and "approaches, never identifies" not in str(path.read_text(encoding="utf-8")):
        raise ValueError(f"{path}: {level} nonmember-pole fence missing")


def validate_spec(spec: dict, path: Path, canonical_rows: dict[str, dict[str, str]]) -> dict:
    if "model" in spec:
        raise ValueError(f"{path}: model assignment must be registry-bound, not pinned")
    metadata = spec.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: metadata mapping required")
    level = metadata.get("level")
    if level not in ROW_FILES:
        raise ValueError(f"{path}: invalid level {level!r}")
    projection = metadata.get("runtime_projection")
    if not isinstance(projection, dict):
        raise ValueError(f"{path}: metadata.runtime_projection required")
    if projection.get("schema_version") != "root-agentz-dispatch-v3":
        raise ValueError(f"{path}: projection schema must be root-agentz-dispatch-v3")
    if projection.get("role_class") != EXPECTED_ROLE[level]:
        raise ValueError(f"{path}: role class conflicts with level")
    if projection.get("operational_move") is not (level in {"L1", "L2", "L3", "L4"}):
        raise ValueError(f"{path}: operational_move conflicts with level")
    if projection.get("gen7_not_g7") is not True:
        raise ValueError(f"{path}: GEN7 != G7 fence missing")
    for key in ("route_stage", "g7_cell", "rep6", "vmosk_a", "balance", "mathematical_note", "geometry_tier", "count_tier", "cross_domain_tier", "stop_condition"):
        if not isinstance(projection.get(key), str) or not projection[key]:
            raise ValueError(f"{path}: runtime_projection.{key} required")
    if projection.get("stop_condition") != STOP_CONDITIONS[level]:
        raise ValueError(f"{path}: stop condition conflicts with the {level} dispatch contract")
    if projection.get("mission_must_be_closable_by_stop_condition") is not True:
        raise ValueError(f"{path}: mission closability gate must be true")
    if projection.get("misroute_action") != MISSION_MISROUTE_ACTION:
        raise ValueError(f"{path}: misroute action must preserve move-or-split and no unchanged retry")
    authority = metadata.get("authority")
    if not isinstance(authority, dict) or authority.get("stage_only") is not True:
        raise ValueError(f"{path}: authority.stage_only=true required")
    for key in AUTH_FALSE:
        if authority.get(key) is not False:
            raise ValueError(f"{path}: authority.{key}=false required")
    enabled, mutating, all_ask = enabled_tools(spec)
    if mutating and level != "L4":
        raise ValueError(f"{path}: only L4 may expose enabled mutating tools")
    if level == "L4" and set(mutating) != MUTATING:
        raise ValueError(f"{path}: L4 must expose exactly write/edit/bash")
    if mutating and not all_ask:
        raise ValueError(f"{path}: every mutating tool must use always_ask")
    for key in LEGACY_FIELDS:
        if key in metadata or key in projection:
            raise ValueError(f"{path}: unsourced legacy field forbidden: {key}")
    validate_canonical_row(metadata, projection, canonical_rows[level], path)
    return {"metadata": metadata, "projection": projection, "authority": authority, "enabled": enabled, "mutating": mutating, "all_ask": all_ask}


def toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    raise TypeError(f"unsupported TOML value: {type(value).__name__}")


def table(name: str, items: list[tuple[str, object]]) -> str:
    lines = [f"[{name}]"]
    lines.extend(f"{key} = {toml_value(value)}" for key, value in items)
    return "\n".join(lines) + "\n"


def bundle_digest(records: list[tuple[str, str]]) -> str:
    payload = "".join(f"{path}\0{digest}\n" for path, digest in sorted(records))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compile_outputs() -> dict[str, str]:
    manifest = parse_manifest()
    canonical_rows = parse_canonical_rows()
    canonical_records = [
        (path.relative_to(DOCUMENTS).as_posix(), sha256(path))
        for path in (STONE_ROW, GENERATIVE_TABLE, MASTER_STONE)
    ]
    canonical_bundle = bundle_digest(canonical_records)
    records = []
    agents = []
    for filename, pinned in manifest:
        path = SOURCE_DIR / filename
        spec = load_yaml(path)
        level = (spec.get("metadata") or {}).get("level")
        if level not in canonical_rows:
            raise ValueError(f"{path}: invalid canonical level {level!r}")
        checked = validate_spec(spec, path, canonical_rows)
        level = checked["metadata"]["level"]
        source_rel = path.relative_to(DOCUMENTS).as_posix()
        records.append((source_rel, pinned))
        agents.append((level, spec, checked, source_rel, pinned))
    agents.sort(key=lambda item: int(item[0][1:]))
    if [item[0] for item in agents] != [f"L{i}" for i in range(1, 8)]:
        raise ValueError("source bundle must contain exactly L1 through L7")
    bundle = bundle_digest(records)
    outputs = {}
    for level, spec, checked, source_rel, pin in agents:
        md = checked["metadata"]
        rp = checked["projection"]
        auth = checked["authority"]
        parts = [
            "# GENERATED FILE. DO NOT EDIT DIRECTLY.\n"
            f"# Source: {source_rel}\n"
            "# Generator: 01_EMERGENTISM/09_TOOLS/02_COMPILERS/sync_root_agentz_dispatch.py\n",
            table("meta", [
                ("schema_version", "root-agentz-dispatch-v3"),
                ("name", spec["name"]), ("description", spec.get("description", "")),
                ("level", level), ("caste", md["caste"]), ("operator", md["operator"]),
                ("operator_id", md["operator_id"]), ("role_class", rp["role_class"]),
                ("operational_move", rp["operational_move"]),
                ("permissions", permissions(checked["enabled"], checked["mutating"])),
                ("source_spec", source_rel), ("source_sha256", pin),
                ("source_bundle_sha256", bundle),
                ("canonical_stone_spec", canonical_records[0][0]),
                ("canonical_stone_sha256", canonical_records[0][1]),
                ("canonical_generative_spec", canonical_records[1][0]),
                ("canonical_generative_sha256", canonical_records[1][1]),
                ("canonical_master_spec", canonical_records[2][0]),
                ("canonical_master_sha256", canonical_records[2][1]),
                ("canonical_bundle_sha256", canonical_bundle),
            ]),
            table("rosetta", [
                ("pramana", md["pramana"]), ("reasoning", md["reasoning"]),
                ("ology", md["ology"]), ("regime", md["regime"]),
                ("equation", md["equation"]), ("axis", md["axis"]),
                ("deployability", md["deployability"]), ("route_stage", rp["route_stage"]),
                ("g7_cell", rp["g7_cell"]), ("g7_projection", md["g7_projection"]),
                ("rep6", rp["rep6"]), ("vmosk_a", rp["vmosk_a"]),
                ("balance", rp["balance"]), ("mathematical_note", rp["mathematical_note"]),
                ("geometry_tier", rp["geometry_tier"]), ("count_tier", rp["count_tier"]),
                ("cross_domain_tier", rp["cross_domain_tier"]),
                ("gen7_not_g7", rp["gen7_not_g7"]),
                ("involution_mirror", md["involution_mirror"]),
                ("virtue", md["virtue"]), ("vice", md["vice"]),
                ("dispatch_one_liner", md["dispatch_one_liner"]),
                ("stone_brief_ref", md["stone_brief_ref"]),
                ("master_rosetta_ref", md["master_rosetta_ref"]),
            ]),
            table("agentz", [
                ("trunk", md["agentz_trunk"]),
                ("disposition", md["agentz_disp"]),
                ("a3_closeout_ref", md["a3_closeout_ref"]),
            ]),
            table("dispatch_contract", [
                ("stop_condition", rp["stop_condition"]),
                ("mission_must_be_closable_by_stop_condition", rp["mission_must_be_closable_by_stop_condition"]),
                ("misroute_action", rp["misroute_action"]),
            ]),
            table("authority", [
                ("stage_only", auth["stage_only"]),
                *[(key, auth[key]) for key in AUTH_FALSE],
                ("disposer_class", auth["disposer_class"]),
                ("boundary", md["authority_boundary"]),
            ]),
            table("fences", [("names", md["fences"]), ("ref", md["fences_ref"]), ("alignment", md["alignment_fence"])]),
            table("tools", [("enabled", checked["enabled"]), ("mutating", checked["mutating"]), ("all_mutating_always_ask", checked["all_ask"])]),
        ]
        outputs[ROW_FILES[level]] = "\n".join(parts).rstrip() + "\n"

    outputs["rosetta_dispatch_schema.toml"] = render_schema(agents, bundle, canonical_records, canonical_bundle)
    outputs.update(render_docs(agents, bundle, canonical_bundle))
    outputs["DEPLOYMENT_MANIFEST.md"] = render_deployment_manifest(outputs, bundle, canonical_records, canonical_bundle)
    return outputs


def render_schema(agents, bundle: str, canonical_records: list[tuple[str, str]], canonical_bundle: str) -> str:
    text = "# GENERATED FILE. DO NOT EDIT DIRECTLY.\n# Source: seven manifest-listed managed-agent YAMLs\n\n"
    text += table("meta", [
        ("schema_version", "root-agentz-dispatch-v3"),
        ("source_authority", "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents"),
        ("source_bundle_sha256", bundle),
        ("canonical_stone_spec", canonical_records[0][0]),
        ("canonical_stone_sha256", canonical_records[0][1]),
        ("canonical_generative_spec", canonical_records[1][0]),
        ("canonical_generative_sha256", canonical_records[1][1]),
        ("canonical_master_spec", canonical_records[2][0]),
        ("canonical_master_sha256", canonical_records[2][1]),
        ("canonical_bundle_sha256", canonical_bundle),
        ("status", "derived_local_runtime_projection"),
    ]) + "\n"
    text += table("dispatch", [
        ("sequence", ["PARSE", "ROUTE_SELECT", "DRAFT", "LINT", "GROUND"]),
        ("operational_levels", ["L1", "L2", "L3", "L4"]),
        ("boundary_levels", ["L5", "L6", "L7"]),
        ("mutation_level", "L4_only"), ("hard_problem_route", "Soul Loop / Ultracode"),
        ("mission_must_be_closable_by_stop_condition", True),
        ("misroute_action", MISSION_MISROUTE_ACTION),
    ]) + "\n"
    text += table("evidence", [
        ("geometry", "[A] given the selected chart"),
        ("count", "[S] seven selected; 3, 5, or 9 satisfy the same symmetry"),
        ("cross_domain", "[I]"), ("gen7_not_g7", True),
    ]) + "\n"
    text += table("authority", [
        ("ai_stage_only", True), ("ai_may_sign", False), ("ai_may_authorize", False),
        ("prism", "verifies_only"), ("public_dav_bind", "at_least_two_natural_persons"),
    ])
    for level, _spec, checked, _source, _pin in agents:
        md = checked["metadata"]
        rp = checked["projection"]
        text += "\n[[agents]]\n"
        for key, value in [
            ("level", level), ("caste", md["caste"]), ("operator", md["operator"]),
            ("operator_id", md["operator_id"]), ("row", ROW_FILES[level]),
            ("route_stage", rp["route_stage"]), ("role_class", rp["role_class"]),
            ("operational_move", rp["operational_move"]),
            ("stop_condition", rp["stop_condition"]),
            ("permissions", permissions(checked["enabled"], checked["mutating"])),
        ]:
            text += f"{key} = {toml_value(value)}\n"
    return text


def render_docs(agents, bundle: str, canonical_bundle: str) -> dict[str, str]:
    rows = []
    stops = []
    for level, _spec, checked, _source, _pin in agents:
        md, rp = checked["metadata"], checked["projection"]
        rows.append(f"| {level} | {md['caste']} | {md['operator']} | {md['pramana']} | {md['reasoning']} | {md['ology']} | {md['regime']} | {rp['role_class']} | {rp['route_stage']} |")
        stops.append(f"| {level} | `{rp['stop_condition']}` |")
    table_md = "\n".join(rows)
    stop_table_md = "\n".join(stops)
    fence = "1. Geometry is `[A]`, given the selected chart.\n2. Seven seats are `[S]`, selected; 3, 5, or 9 satisfy the same symmetry.\n3. Every cross-domain cell is `[I]`.\n"
    readme = f"""# Rosetta agents — generated local projection

Managed-agent bundle: `{bundle}`. Canonical Stone bundle: `{canonical_bundle}`.
Edit the owning Stone/YAML sources, never this directory.

{fence}
`GEN7 ≠ G7`. Models are registry-bound and absent from this projection.

| Seat | Varṇa | Operator | Pramāṇa | Inference | -ology | Regime | Class | Route |
|---|---|---|---|---|---|---|---|---|
{table_md}

Only L4 may mutate local files, within the user's scoped task. Every seat has
`may_sign=false` and `may_authorize=false`; PRISM verifies only.
"""
    dispatch = f"""# Rosetta dispatch — generated runtime card

{fence}
## Hard problems: Soul Loop / Ultracode

Run L1 boundary, meaningfully independent L2 candidates/rivals, and L3 audit
before the single L4 mutator. Escalate through L5 architecture, L6 negative
boundary, and L7 constitutional witness only when warranted; all three return
non-authorizing counsel to L4. Feed verification and outcome evidence back to L1.

An eight-section ephemeral brief is mandatory: identity; authority and negative
space; house rules; dated tiered facts; verified paths and degradation; runtime
breakage; atomic mission with licence to refute; output contract with
`premise-refuted`.

## Mission sizing by stop condition

A mission that cannot be closed by the station's own stop condition is mis-routed.
Move it to the station whose pramāṇa and stop condition can close it, or split it
into independently closable missions; do not retry the unchanged mission. A
mismatch or resulting timeout is a briefing error, not a station failure.

L1 direct perception is bounded to one named source or artifact and contradictions
visible within it. When ambiguity exceeds that direct evidence, L1 stops and hands
off. Cross-source inference belongs to L3; it must not be smuggled into L1 as a
larger search budget.

| Seat | Exact stop condition |
|---|---|
{stop_table_md}

## Commit cadence

L4 ends a completed owned change in a local commit and does not ask the owner to
choose the cadence. On non-trivial, mixed-ownership, foreign-dirty, or inherited
surfaces: L1 maps direct dirty paths and write activity; L2 proposes independently
revertible groups; L3 ranks ownership, completeness, reversibility, and risk; L4
stages the selected group by explicit pathspec and inspects the staged diff. Never
use `git add -A`, and exclude active or unresolved foreign work. A commit is a local
record, not authority, deployment, publication, settlement, or permission to push.

Model consensus creates no authority. PRISM verifies only.
"""
    managed = f"""# Managed agents — generated pointer

The seven canonical YAMLs are source-owned in Emergentism. This local projection
does not prove hosted provisioning or deployment. Model routing is registry-bound.

{fence}
Use `DISPATCH.md` for the Soul Loop and Ultracode hard-problem route.
"""
    boundary = f"""# Rosetta boundary and consequence predicates — generated card

God/demon words, where retained in historical material, are retrospective
consequence predicates, never identities, person-ranks, permissions, or authority.

{fence}
L1–L4 are operational work seats. L5–L7 are non-deployable counsel. L4 is the
sole local mutator. No Rosetta seat signs, authorizes, publishes, transmits, or
settles consequence; PRISM verifies only.
"""
    return {"README.md": readme, "DISPATCH.md": dispatch, "MANAGED_AGENTS.md": managed, "ROOT_AND_GOD_DEPLOYMENT.md": boundary}


def render_deployment_manifest(
    outputs: dict[str, str],
    bundle: str,
    canonical_records: list[tuple[str, str]],
    canonical_bundle: str,
) -> str:
    if "DEPLOYMENT_MANIFEST.md" in outputs:
        raise ValueError("deployment manifest must exclude itself from its hash table")
    lines = [
        "# Deployment manifest — generated Rosetta runtime projection",
        "",
        "- Schema: `root-agentz-dispatch-v3`",
        "- Source: seven manifest-listed managed-agent YAMLs",
        f"- Source bundle SHA-256: `{bundle}`",
        f"- Canonical Stone: `{canonical_records[0][0]}` @ `{canonical_records[0][1]}`",
        f"- Canonical Generative Table: `{canonical_records[1][0]}` @ `{canonical_records[1][1]}`",
        f"- Canonical Master Rosetta: `{canonical_records[2][0]}` @ `{canonical_records[2][1]}`",
        f"- Canonical Stone bundle SHA-256: `{canonical_bundle}`",
        "- Scope: exactly 12 payload files plus this manifest (13 generated files total).",
        "- Exclusion: `rows/cx_suite/` is preserved and is not loaded, hashed, or modified.",
        "- Determinism: UTF-8, LF-only, timestamp-free.",
        "",
        "| Path | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for rel, content in sorted(outputs.items()):
        encoded = content.encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        lines.append(f"| `{rel}` | {len(encoded)} | `{digest}` |")
    lines.extend([
        "",
        "This manifest proves local byte custody only. It grants no authority and",
        "does not prove provisioning, deployment, publication, or a world outcome.",
        "",
    ])
    return "\n".join(lines)


def emit(outputs: dict[str, str], out: Path) -> None:
    resolved = out.resolve()
    if resolved == LOCAL_RUNTIME or LOCAL_RUNTIME in resolved.parents:
        raise ValueError("compiler emits side proposals only; direct local-runtime emission is forbidden")
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"output directory must be absent or empty: {out}")
    out.mkdir(parents=True, exist_ok=True)
    for rel, content in sorted(outputs.items()):
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def check(outputs: dict[str, str], target: Path) -> int:
    mismatches = []
    for rel, expected in sorted(outputs.items()):
        path = target / rel
        if not path.is_file():
            mismatches.append(f"MISSING {rel}")
        elif path.read_text(encoding="utf-8") != expected:
            mismatches.append(f"STALE {rel}")
    if mismatches:
        print("\n".join(mismatches))
        return 1
    print(f"ROSETTA-PROJECTION OK target={target} files={len(outputs)}")
    return 0


def self_test() -> int:
    outputs = compile_outputs()
    joined = "\n".join(outputs.values())
    forbidden = ["model =", "Data Science", "∂P_node", "log P_node", "E_node", "PRISM signs"]
    if any(token in joined for token in forbidden):
        print("SELF-TEST FAIL forbidden semantic token survived")
        return 1
    try:
        yaml.load("a: 1\na: 2\n", Loader=UniqueKeyLoader)
    except ValueError:
        pass
    else:
        print("SELF-TEST FAIL duplicate YAML key accepted")
        return 1
    canonical = parse_canonical_rows()
    mutated = {level: dict(row) for level, row in canonical.items()}
    mutated["L1"]["operator"] = "deliberate-self-test-drift"
    l1_path = SOURCE_DIR / "01_candala_firewall.agent.yaml"
    try:
        validate_spec(load_yaml(l1_path), l1_path, mutated)
    except ValueError:
        pass
    else:
        print("SELF-TEST FAIL canonical Stone drift was accepted")
        return 1
    stop_mutated = copy.deepcopy(load_yaml(l1_path))
    stop_mutated["metadata"]["runtime_projection"]["stop_condition"] = "deliberate-self-test-drift"
    try:
        validate_spec(stop_mutated, l1_path, canonical)
    except ValueError:
        pass
    else:
        print("SELF-TEST FAIL stop-condition drift was accepted")
        return 1
    action_mutated = copy.deepcopy(load_yaml(l1_path))
    action_mutated["metadata"]["runtime_projection"]["misroute_action"] = "deliberate-self-test-drift"
    try:
        validate_spec(action_mutated, l1_path, canonical)
    except ValueError:
        pass
    else:
        print("SELF-TEST FAIL misroute-action drift was accepted")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        first, second = Path(tmp) / "a", Path(tmp) / "b"
        emit(outputs, first)
        emit(compile_outputs(), second)
        a = {p.relative_to(first): p.read_bytes() for p in first.rglob("*") if p.is_file()}
        b = {p.relative_to(second): p.read_bytes() for p in second.rglob("*") if p.is_file()}
        if a != b:
            print("SELF-TEST FAIL output is not deterministic")
            return 1
    print(f"SELF-TEST PASS files={len(outputs)} canonical_drift=fail-closed stop_condition=fail-closed misroute_action=fail-closed")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--emit-proposal", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--target", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return self_test()
        outputs = compile_outputs()
        if args.emit_proposal:
            if args.out is None:
                parser.error("--emit-proposal requires --out")
            emit(outputs, args.out)
            print(f"ROSETTA-PROPOSAL OK out={args.out} files={len(outputs)}")
            return 0
        if args.target is None:
            parser.error("--check requires --target")
        return check(outputs, args.target)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ROSETTA-PROJECTION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

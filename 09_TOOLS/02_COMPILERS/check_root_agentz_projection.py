#!/usr/bin/env python3
"""Independent semantic checker for the generated root Rosetta projection."""

from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
import tomllib
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment boundary
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


SCRIPT = Path(__file__).resolve()
DOCUMENTS = SCRIPT.parents[3]
SOURCE = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents"
SOURCE_MANIFEST = SOURCE / "MANIFEST.sha256"
STONE_ROW = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"
GENERATIVE_TABLE = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/00_GENERATIVE_TABLE.md"
MASTER_STONE = DOCUMENTS / "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md"
ROWS = {
    "L1": ("01_L1_candala_firewall.toml", "Caṇḍāla", "Kali 🎲", "G7@1:kali_take_phi", "Pratyakṣa (Direct Perception)", "Dialectical", "Objective Function", "Tyranny", "operational", "PARSE", "B→0 (limiting)"),
    "L2": ("02_L2_sudra_explorer.toml", "Śūdra", "Kālī 💀", "G7@1:kali_take_v", "Upamāna (Analogy)", "Inductive", "Epistemology", "Democracy", "operational", "ROUTE_SELECT", "B=1/2"),
    "L3": ("03_L3_vaisya_auditor.toml", "Vaiśya", "Kṛṣṇa ◇", "G7@1:krishna_give_v", "Anumāna (Inference)", "Deductive", "Methodology", "Oligarchy", "operational", "ROUTE_SELECT", "B=√3/2"),
    "L4": ("04_L4_ksatriya_executor.toml", "Kṣatriya", "Arjuna ⚔", "G7@1:arjuna_give_phi", "Arthāpatti (Postulation)", "Abductive", "Axiology", "Timocracy", "operational", "DRAFT", "B=1"),
    "L5": ("05_L5_brahmana_architect.toml", "Brāhmaṇa", "Brahmā ○", "G7@1:brahma_create", "Śabda (Testimony)", "Systematic", "Ontology", "Aristocracy", "boundary", "LINT", "B=√3/2"),
    "L6": ("06_L6_sadhu_compressor.toml", "Sādhu", "Śiva •", "G7@1:shiva_dissolve", "Anupalabdhi (Non-Apprehension)", "Apophatic", "Metaphysics", "Anarchy", "boundary", "LINT", "B=1/2"),
    "L7": ("07_L7_rsi_constitution.toml", "Ṛṣi", "Viṣṇu ⊙", "G7@1:vishnu_preserve", "[D staged, not ratified] Pratibhā (framework-added seventh; no school's separate seventh)", "Transcendental", "Teleology", "Theocracy", "boundary", "GROUND", "B→0 (limiting)"),
}
SOURCE_FILES = {
    "L1": "01_candala_firewall.agent.yaml", "L2": "02_sudra_explorer.agent.yaml",
    "L3": "03_vaisya_auditor.agent.yaml", "L4": "04_ksatriya_executor.agent.yaml",
    "L5": "05_brahmana_architect.agent.yaml", "L6": "06_sadhu_compressor.agent.yaml",
    "L7": "07_rsi_constitution.agent.yaml",
}
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
LEGACY = {"model", "input_type", "output_type", "evaluation_contract", "budget_source", "budget_required_fields", "full_closure_positions", "operator_tier", "balance_coordinate", "equation_domain", "d4_d5_contract"}
FORBIDDEN_TEXT = ("Data Science", "Auditing", "System Architecture", "Core State", "Institutional Narrative", "∂P_node", "log P_node", "E_node", "dΦ/Φ", "PRISM signs", "Mavis signs", "K2-of-the-time")
AUTH_FALSE = ("may_sign", "may_authorize", "may_publish", "may_transmit", "may_settle")
MUTATING = {"write", "edit", "bash"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Independent duplicate-key-rejecting loader."""


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return data


def source_manifest() -> dict[str, str]:
    pattern = re.compile(r"^([0-9a-f]{64})\s+\*?(.+?)\s*$")
    entries = {}
    for lineno, raw in enumerate(SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line)
        if not match:
            raise ValueError(f"{SOURCE_MANIFEST}:{lineno}: invalid line")
        if match.group(2) in entries:
            raise ValueError(f"duplicate manifest name: {match.group(2)}")
        entries[match.group(2)] = match.group(1)
    return entries


def bundle_digest(records: list[tuple[str, str]]) -> str:
    payload = "".join(f"{path}\0{digest}\n" for path, digest in sorted(records))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def source_tools(spec: dict) -> tuple[list[str], list[str], bool]:
    enabled, mutating, all_ask = [], [], True
    for toolset in spec.get("tools", []):
        for item in toolset.get("configs", []):
            if item.get("enabled") is True:
                name = item.get("name")
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


def plain_cell(value: str) -> str:
    value = value.replace("**", "").replace("`", "").replace("*", "")
    return " ".join(value.strip().split())


def analogy_key(value: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", value.casefold())


def canonical_tables() -> dict[str, dict[str, str]]:
    """Independently parse the active Stone tables instead of trusting generator output."""
    stone_text = STONE_ROW.read_text(encoding="utf-8")
    for required in (
        "The geometry is `[A]`, given the selection.",
        "The count is `[S]` — selected, not derived.",
        "Every cross-domain cell is `[I]`",
        "`GEN7 ≠ G7`",
        "the seats approach them and never identify",
    ):
        if required not in stone_text:
            raise ValueError(f"canonical Stone fence missing: {required}")
    stone = {}
    for raw in stone_text.splitlines():
        if re.match(r"^\| \*\*L[1-7]\*\* \|", raw):
            cells = [plain_cell(cell) for cell in raw.strip().split("|")[1:-1]]
            if len(cells) != 12:
                raise ValueError(f"canonical Stone row has {len(cells)} cells")
            stone[cells[0]] = dict(zip(
                ("level", "caste", "operator", "g7", "pramana", "rep6", "vmosk", "balance", "reasoning", "ology", "regime", "deploy"), cells
            ))
    generated = {}
    for raw in GENERATIVE_TABLE.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| `GEN7@1:L[1-7]` \|", raw):
            cells = [plain_cell(cell) for cell in raw.strip().split("|")[1:-1]]
            if len(cells) != 6:
                raise ValueError(f"Generative Table row has {len(cells)} cells")
            level = cells[0].rsplit(":", 1)[-1]
            generated[level] = dict(zip(("stable_id", "projected", "caste", "analogy", "mathematical_note", "standing"), cells))
    expected = set(ROWS)
    if set(stone) != expected or set(generated) != expected:
        raise ValueError("canonical tables must each contain exactly L1 through L7")
    return {level: {**stone[level], **{f"generative_{key}": value for key, value in generated[level].items()}} for level in ROWS}


def canonical_source_errors(level: str, spec: dict, canonical: dict) -> list[str]:
    """Return Stone-to-YAML semantic drift; used by the live gate and negative self-test."""
    errors = []
    md = spec.get("metadata", {})
    rp = md.get("runtime_projection", {})
    exact = {
        "caste": (md.get("caste"), canonical["caste"]),
        "operator": (md.get("operator"), canonical["operator"]),
        "g7_cell": (rp.get("g7_cell"), f"G7@1:{canonical['g7']}"),
        "rep6": (rp.get("rep6"), canonical["rep6"].removeprefix("— ")),
        "projected pair": (canonical["generative_projected"], f"{rp.get('g7_cell')} · {md.get('operator')}"),
        "generative caste": (canonical["generative_caste"], md.get("caste")),
        "mathematical note": (plain_cell(str(rp.get("mathematical_note", ""))), canonical["generative_mathematical_note"]),
    }
    balances = {"→0 (limiting)": "B→0 (limiting)", "½": "B=1/2", "√3⁄2": "B=√3/2", "1": "B=1"}
    exact["balance"] = (rp.get("balance"), balances.get(canonical["balance"]))
    for label, (actual, wanted) in exact.items():
        if actual != wanted:
            errors.append(f"{level}: canonical {label}={actual!r}, expected {wanted!r}")
    if canonical["pramana"] not in str(md.get("pramana", "")):
        errors.append(f"{level}: canonical pramana {canonical['pramana']!r} missing")
    if not str(rp.get("vmosk_a", "")).startswith(f"[I/C] {canonical['vmosk']}"):
        errors.append(f"{level}: canonical qualified VMOSK-A cell missing")
    for field in ("reasoning", "ology", "regime"):
        if analogy_key(str(md.get(field, ""))) != analogy_key(canonical[field]):
            errors.append(f"{level}: canonical {field} mismatch")
    analogy = [analogy_key(part) for part in canonical["generative_analogy"].split("/")]
    current = [analogy_key(str(md.get(field, ""))) for field in ("reasoning", "ology", "regime")]
    if analogy != current:
        errors.append(f"{level}: Generative Table analogy triple mismatch")
    expected_operational = canonical["deploy"] == "✓"
    if canonical["deploy"] not in {"✓", "✗"} or rp.get("operational_move") is not expected_operational:
        errors.append(f"{level}: canonical deployability mismatch")
    if level in {"L1", "L7"} and "approaches, never identifies" not in str(spec.get("description", "")):
        errors.append(f"{level}: nonmember-pole fence missing")
    return errors


def stop_condition_errors(level: str, spec: dict) -> list[str]:
    projection = (spec.get("metadata") or {}).get("runtime_projection") or {}
    errors = []
    if projection.get("stop_condition") != STOP_CONDITIONS[level]:
        errors.append(f"{level}: source stop condition conflicts with the dispatch contract")
    if projection.get("mission_must_be_closable_by_stop_condition") is not True:
        errors.append(f"{level}: source mission closability gate must be true")
    if projection.get("misroute_action") != MISSION_MISROUTE_ACTION:
        errors.append(f"{level}: source misroute action loses move-or-split or no-retry semantics")
    return errors


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def check(target: Path) -> list[str]:
    errors = []
    try:
        manifest = source_manifest()
        canonical = canonical_tables()
    except Exception as exc:
        return [f"canonical/source intake failed: {exc}"]
    canonical_records = [
        (path.relative_to(DOCUMENTS).as_posix(), sha256(path))
        for path in (STONE_ROW, GENERATIVE_TABLE, MASTER_STONE)
    ]
    canonical_bundle = bundle_digest(canonical_records)
    if set(manifest) != set(SOURCE_FILES.values()):
        errors.append("source manifest must name exactly the seven canonical YAMLs")
    records = []
    sources = {}
    for level, filename in SOURCE_FILES.items():
        path = SOURCE / filename
        try:
            spec = load_yaml(path)
        except Exception as exc:
            errors.append(f"{level}: source YAML parse failed: {exc}")
            continue
        source_meta = spec.get("metadata", {})
        source_projection = source_meta.get("runtime_projection", {})
        source_authority = source_meta.get("authority", {})
        if "model" in set(walk_keys(spec)):
            errors.append(f"{level}: source YAML pins a model instead of registry-bound dispatch")
        if source_meta.get("level") != level:
            errors.append(f"{level}: source metadata.level={source_meta.get('level')!r}")
        if source_projection.get("schema_version") != "root-agentz-dispatch-v3":
            errors.append(f"{level}: source projection schema is not v3")
        expected_operational = level in {"L1", "L2", "L3", "L4"}
        if source_projection.get("operational_move") is not expected_operational:
            errors.append(f"{level}: source operational_move conflicts with the L1-L4 boundary")
        if source_projection.get("gen7_not_g7") is not True:
            errors.append(f"{level}: source GEN7 != G7 fence missing")
        errors.extend(stop_condition_errors(level, spec))
        if source_authority.get("stage_only") is not True:
            errors.append(f"{level}: source authority.stage_only must be true")
        for key in AUTH_FALSE:
            if source_authority.get(key) is not False:
                errors.append(f"{level}: source authority.{key} must be false")
        errors.extend(canonical_source_errors(level, spec, canonical[level]))
        live = sha256(path)
        if manifest.get(filename) != live:
            errors.append(f"{level}: source manifest pin mismatch")
        source_rel = path.relative_to(DOCUMENTS).as_posix()
        records.append((source_rel, live))
        sources[level] = (spec, source_rel, live)
    expected_bundle = bundle_digest(records) if len(records) == 7 else None

    for level, expected in ROWS.items():
        filename, caste, operator, g7, pramana, reasoning, ology, regime, role, route, balance = expected
        path = target / "rows" / filename
        if not path.is_file():
            errors.append(f"{level}: missing {path}")
            continue
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{level}: TOML parse failed: {exc}")
            continue
        if level not in sources:
            continue
        spec, source_rel, source_pin = sources[level]
        smd = spec.get("metadata", {})
        srp = smd.get("runtime_projection", {})
        sauth = smd.get("authority", {})
        enabled, mutating_source, all_ask_source = source_tools(spec)
        meta, row = data.get("meta", {}), data.get("rosetta", {})
        agentz, dispatch_contract = data.get("agentz", {}), data.get("dispatch_contract", {})
        auth = data.get("authority", {})
        fences, tools = data.get("fences", {}), data.get("tools", {})
        checks = {
            "meta.schema_version": (meta.get("schema_version"), "root-agentz-dispatch-v3"),
            "meta.name": (meta.get("name"), spec.get("name")), "meta.description": (meta.get("description"), spec.get("description", "")),
            "meta.level": (meta.get("level"), level), "meta.caste": (meta.get("caste"), smd.get("caste")),
            "meta.operator": (meta.get("operator"), smd.get("operator")), "meta.operator_id": (meta.get("operator_id"), smd.get("operator_id")),
            "meta.role_class": (meta.get("role_class"), srp.get("role_class")),
            "meta.operational_move": (meta.get("operational_move"), srp.get("operational_move")),
            "meta.permissions": (meta.get("permissions"), permissions(enabled, mutating_source)),
            "meta.source_spec": (meta.get("source_spec"), source_rel), "meta.source_sha256": (meta.get("source_sha256"), source_pin),
            "meta.source_bundle_sha256": (meta.get("source_bundle_sha256"), expected_bundle),
            "meta.canonical_stone_spec": (meta.get("canonical_stone_spec"), canonical_records[0][0]),
            "meta.canonical_stone_sha256": (meta.get("canonical_stone_sha256"), canonical_records[0][1]),
            "meta.canonical_generative_spec": (meta.get("canonical_generative_spec"), canonical_records[1][0]),
            "meta.canonical_generative_sha256": (meta.get("canonical_generative_sha256"), canonical_records[1][1]),
            "meta.canonical_master_spec": (meta.get("canonical_master_spec"), canonical_records[2][0]),
            "meta.canonical_master_sha256": (meta.get("canonical_master_sha256"), canonical_records[2][1]),
            "meta.canonical_bundle_sha256": (meta.get("canonical_bundle_sha256"), canonical_bundle),
            "rosetta.pramana": (row.get("pramana"), smd.get("pramana")), "rosetta.reasoning": (row.get("reasoning"), smd.get("reasoning")),
            "rosetta.ology": (row.get("ology"), smd.get("ology")), "rosetta.regime": (row.get("regime"), smd.get("regime")),
            "rosetta.equation": (row.get("equation"), smd.get("equation")), "rosetta.axis": (row.get("axis"), smd.get("axis")),
            "rosetta.deployability": (row.get("deployability"), smd.get("deployability")),
            "rosetta.route_stage": (row.get("route_stage"), srp.get("route_stage")), "rosetta.g7_cell": (row.get("g7_cell"), srp.get("g7_cell")),
            "rosetta.g7_projection": (row.get("g7_projection"), smd.get("g7_projection")),
            "rosetta.rep6": (row.get("rep6"), srp.get("rep6")), "rosetta.vmosk_a": (row.get("vmosk_a"), srp.get("vmosk_a")),
            "rosetta.balance": (row.get("balance"), srp.get("balance")),
            "rosetta.mathematical_note": (row.get("mathematical_note"), srp.get("mathematical_note")),
            "rosetta.geometry_tier": (row.get("geometry_tier"), srp.get("geometry_tier")),
            "rosetta.count_tier": (row.get("count_tier"), srp.get("count_tier")),
            "rosetta.cross_domain_tier": (row.get("cross_domain_tier"), srp.get("cross_domain_tier")),
            "rosetta.gen7_not_g7": (row.get("gen7_not_g7"), srp.get("gen7_not_g7")),
            "rosetta.involution_mirror": (row.get("involution_mirror"), smd.get("involution_mirror")),
            "rosetta.virtue": (row.get("virtue"), smd.get("virtue")), "rosetta.vice": (row.get("vice"), smd.get("vice")),
            "rosetta.dispatch_one_liner": (row.get("dispatch_one_liner"), smd.get("dispatch_one_liner")),
            "rosetta.stone_brief_ref": (row.get("stone_brief_ref"), smd.get("stone_brief_ref")),
            "rosetta.master_rosetta_ref": (row.get("master_rosetta_ref"), smd.get("master_rosetta_ref")),
            "agentz.trunk": (agentz.get("trunk"), smd.get("agentz_trunk")),
            "agentz.disposition": (agentz.get("disposition"), smd.get("agentz_disp")),
            "agentz.a3_closeout_ref": (agentz.get("a3_closeout_ref"), smd.get("a3_closeout_ref")),
            "dispatch_contract.stop_condition": (dispatch_contract.get("stop_condition"), srp.get("stop_condition")),
            "dispatch_contract.mission_must_be_closable_by_stop_condition": (dispatch_contract.get("mission_must_be_closable_by_stop_condition"), srp.get("mission_must_be_closable_by_stop_condition")),
            "dispatch_contract.misroute_action": (dispatch_contract.get("misroute_action"), srp.get("misroute_action")),
            "authority.stage_only": (auth.get("stage_only"), sauth.get("stage_only")),
            "authority.disposer_class": (auth.get("disposer_class"), sauth.get("disposer_class")),
            "authority.boundary": (auth.get("boundary"), smd.get("authority_boundary")),
            "fences.names": (fences.get("names"), smd.get("fences")), "fences.ref": (fences.get("ref"), smd.get("fences_ref")),
            "fences.alignment": (fences.get("alignment"), smd.get("alignment_fence")),
            "tools.enabled": (tools.get("enabled"), enabled), "tools.mutating": (tools.get("mutating"), mutating_source),
            "tools.all_mutating_always_ask": (tools.get("all_mutating_always_ask"), all_ask_source),
        }
        for key in AUTH_FALSE:
            checks[f"authority.{key}"] = (auth.get(key), sauth.get(key))
        for label, (actual, wanted) in checks.items():
            if actual != wanted:
                errors.append(f"{level}: {label}={actual!r}, expected {wanted!r}")
        canonical = {
            "meta.caste": (meta.get("caste"), caste), "meta.operator": (meta.get("operator"), operator),
            "meta.role_class": (meta.get("role_class"), role), "rosetta.g7_cell": (row.get("g7_cell"), g7),
            "rosetta.pramana": (row.get("pramana"), pramana), "rosetta.reasoning": (row.get("reasoning"), reasoning),
            "rosetta.ology": (row.get("ology"), ology), "rosetta.regime": (row.get("regime"), regime),
            "rosetta.route_stage": (row.get("route_stage"), route), "rosetta.balance": (row.get("balance"), balance),
            "rosetta.cross_domain_tier": (row.get("cross_domain_tier"), "[I]"), "rosetta.gen7_not_g7": (row.get("gen7_not_g7"), True),
        }
        for label, (actual, wanted) in canonical.items():
            if actual != wanted:
                errors.append(f"{level}: canonical {label}={actual!r}, expected {wanted!r}")
        if not str(row.get("vmosk_a", "")).startswith("[I/C]"):
            errors.append(f"{level}: VMOSK-A qualifier [I/C] did not travel")
        legacy = LEGACY.intersection(walk_keys(data))
        if legacy:
            errors.append(f"{level}: unsourced legacy fields {sorted(legacy)}")
        mutating = set(tools.get("mutating", []))
        if level == "L4":
            if mutating != {"bash", "edit", "write"} or tools.get("all_mutating_always_ask") is not True:
                errors.append("L4: mutating tools must be exactly bash/edit/write with always_ask")
        elif mutating:
            errors.append(f"{level}: non-L4 row exposes mutating tools {sorted(mutating)}")
    required = {"rosetta_dispatch_schema.toml", "README.md", "DISPATCH.md", "MANAGED_AGENTS.md", "ROOT_AND_GOD_DEPLOYMENT.md", "DEPLOYMENT_MANIFEST.md"}
    required.update(f"rows/{value[0]}" for value in ROWS.values())
    for name in sorted(required):
        path = target / name
        if not path.is_file():
            errors.append(f"missing generated surface {name}")
    actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file() and "cx_suite" not in p.parts}
    unexpected = actual - required
    if unexpected:
        errors.append(f"unexpected active generated files: {sorted(unexpected)}")
    schema_path = target / "rosetta_dispatch_schema.toml"
    if schema_path.is_file():
        try:
            schema = tomllib.loads(schema_path.read_text(encoding="utf-8"))
            if schema.get("meta", {}).get("source_bundle_sha256") != expected_bundle:
                errors.append("schema source bundle digest is not live")
            schema_meta = schema.get("meta", {})
            canonical_schema = {
                "canonical_stone_spec": canonical_records[0][0],
                "canonical_stone_sha256": canonical_records[0][1],
                "canonical_generative_spec": canonical_records[1][0],
                "canonical_generative_sha256": canonical_records[1][1],
                "canonical_master_spec": canonical_records[2][0],
                "canonical_master_sha256": canonical_records[2][1],
                "canonical_bundle_sha256": canonical_bundle,
            }
            for key, wanted in canonical_schema.items():
                if schema_meta.get(key) != wanted:
                    errors.append(f"schema {key} is not live")
            schema_dispatch = schema.get("dispatch", {})
            if schema_dispatch.get("mission_must_be_closable_by_stop_condition") is not True:
                errors.append("schema mission-closability gate is missing")
            if schema_dispatch.get("misroute_action") != MISSION_MISROUTE_ACTION:
                errors.append("schema misroute action is not exact")
            schema_agents = schema.get("agents", [])
            if [a.get("level") for a in schema_agents] != list(ROWS):
                errors.append("schema agent sequence is not exactly L1 through L7")
            for agent in schema_agents:
                level = agent.get("level")
                if level in STOP_CONDITIONS and agent.get("stop_condition") != STOP_CONDITIONS[level]:
                    errors.append(f"schema {level} stop condition is not exact")
        except Exception as exc:
            errors.append(f"schema TOML parse failed: {exc}")
    text = "\n".join(p.read_text(encoding="utf-8") for p in target.rglob("*") if p.is_file() and (p.suffix in {".toml", ".md"}) and "cx_suite" not in p.parts)
    for token in FORBIDDEN_TEXT:
        if token in text:
            errors.append(f"forbidden stale token survived: {token}")
    dispatch = target / "DISPATCH.md"
    if dispatch.is_file():
        dispatch_text = dispatch.read_text(encoding="utf-8")
        required_dispatch_text = (
            "Ultracode",
            "eight-section",
            "A mission that cannot be closed by the station's own stop condition is mis-routed.",
            "do not retry",
            "the unchanged mission",
            "Cross-source inference belongs to L3",
            "## Commit cadence",
            "does not ask the owner",
            "explicit pathspec",
            "`git add -A`",
            "permission to push",
        )
        if any(token not in dispatch_text for token in required_dispatch_text):
            errors.append("DISPATCH.md lacks the Ultracode, brief, or mission-closability contract")
    readme = target / "README.md"
    if readme.is_file():
        lines = readme.read_text(encoding="utf-8").splitlines()
        for level, expected in ROWS.items():
            row_line = next((line for line in lines if line.startswith(f"| {level} |")), "")
            for value in (expected[1], expected[2], expected[4], expected[5], expected[6], expected[7], expected[8], expected[9]):
                if value not in row_line:
                    errors.append(f"README {level} row omits {value!r}")
    deployment = target / "DEPLOYMENT_MANIFEST.md"
    if deployment.is_file():
        deployment_text = deployment.read_text(encoding="utf-8")
        entry_re = re.compile(r"^\| `([^`]+)` \| ([0-9]+) \| `([0-9a-f]{64})` \|$", re.M)
        raw_entries = entry_re.findall(deployment_text)
        table_lines = [line for line in deployment_text.splitlines() if line.startswith("|")]
        header = "| Path | Bytes | SHA-256 |"
        separator = "|---|---:|---|"
        malformed = [line for line in table_lines if line not in {header, separator} and entry_re.fullmatch(line) is None]
        if table_lines.count(header) != 1 or table_lines.count(separator) != 1 or malformed:
            errors.append(f"deployment manifest contains malformed table rows: {malformed}")
        raw_paths = [path for path, _size, _digest in raw_entries]
        if len(raw_paths) != len(set(raw_paths)):
            errors.append("deployment manifest contains duplicate payload paths")
        entries = {path: (int(size), digest) for path, size, digest in raw_entries}
        payload = required - {"DEPLOYMENT_MANIFEST.md"}
        if set(entries) != payload:
            errors.append(f"deployment manifest payload set mismatch: {sorted(set(entries) ^ payload)}")
        for rel in sorted(payload.intersection(entries)):
            path = target / rel
            if path.is_file() and entries[rel] != (len(path.read_bytes()), sha256(path)):
                errors.append(f"deployment manifest hash/size mismatch: {rel}")
        canonical_manifest_tokens = [
            canonical_records[0][0], canonical_records[0][1],
            canonical_records[1][0], canonical_records[1][1],
            canonical_records[2][0], canonical_records[2][1],
            canonical_bundle,
        ]
        if (
            not expected_bundle
            or expected_bundle not in deployment_text
            or any(token not in deployment_text for token in canonical_manifest_tokens)
            or "12 payload files plus this manifest" not in deployment_text
        ):
            errors.append("deployment manifest lacks live source/canonical bundle or scope contract")
    return errors


def self_test() -> int:
    try:
        canonical = canonical_tables()
        spec = load_yaml(SOURCE / SOURCE_FILES["L1"])
        if canonical_source_errors("L1", spec, canonical["L1"]):
            print("SELF-TEST FAIL live L1 does not match canonical tables")
            return 1
        mutated = dict(canonical["L1"])
        mutated["operator"] = "deliberate-self-test-drift"
        if not canonical_source_errors("L1", spec, mutated):
            print("SELF-TEST FAIL canonical-row drift was accepted")
            return 1
        stop_mutated = copy.deepcopy(spec)
        stop_mutated["metadata"]["runtime_projection"]["stop_condition"] = "deliberate-self-test-drift"
        if not stop_condition_errors("L1", stop_mutated):
            print("SELF-TEST FAIL stop-condition drift was accepted")
            return 1
        action_mutated = copy.deepcopy(spec)
        action_mutated["metadata"]["runtime_projection"]["misroute_action"] = "deliberate-self-test-drift"
        if not stop_condition_errors("L1", action_mutated):
            print("SELF-TEST FAIL misroute-action drift was accepted")
            return 1
    except Exception as exc:
        print(f"SELF-TEST FAIL {exc}")
        return 1
    print("SELF-TEST PASS canonical Stone, stop-condition, and misroute-action drift are fail-closed")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--target", type=Path)
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    errors = check(args.target)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"ROSETTA-SEMANTICS OK target={args.target} rows=7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

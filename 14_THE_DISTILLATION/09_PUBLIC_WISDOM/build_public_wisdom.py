#!/usr/bin/env python3
"""Validate and compile the Public Wisdom Instrument source packet.

The compiler is deterministic and standard-library only. It reads exact Git
blobs named by ``source_manifest.v1.json``; working-tree changes never enter
through convenience. ``--check`` performs no writes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
EMERGENTISM_ROOT = HERE.parents[1]
FEDERATION_ROOT = EMERGENTISM_ROOT.parent
DATA = HERE / "data"
OUTPUT = HERE / "PublicWisdomCorpus.v1.json"

PATHS = {
    "manifest": DATA / "source_manifest.v1.json",
    "stack": DATA / "emergence_stack.v1.json",
    "records": DATA / "public_wisdom_records.v1.json",
    "cards": DATA / "estate_application_cards.v1.json",
    "ledger": DATA / "estate_coverage_ledger.v1.json",
}

SCHEMAS = {
    "stack": HERE / "contracts" / "EmergenceStack.v1.schema.json",
    "record": HERE / "contracts" / "PublicWisdomRecord.v1.schema.json",
    "card": HERE / "contracts" / "EstateApplicationCard.v1.schema.json",
    "ledger": HERE / "contracts" / "EstateCoverageLedger.v1.schema.json",
}

KINDS = ("PUBLIC_KNOWLEDGE", "POLICY_CANDIDATE", "WISDOM_POLICY")
MATURITIES = ("N/A", "PROVISIONAL", "SUPPORTED", "CONTESTED", "SUPERSEDED")
PROJECTIONS = ("DRAFT", "AUTHORIZED_NOT_LIT", "LIT", "CORRECTED", "RETRACTED")
COVERAGE_STATES = (
    "ADMITTED_APPLICATION",
    "CANDIDATE_ONLY",
    "NO_ADMISSIBLE_RECORD",
    "EXCLUDED_PRIVATE",
    "HELD_CUSTODY",
    "HISTORICAL",
)
FORBIDDEN_PATH_PARTS = {".codex-worktrees", ".git"}


class ContractError(ValueError):
    """Raised when a Public Wisdom contract fails closed."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
    }.get(expected, False)


def validate_schema_subset(value: Any, schema: dict[str, Any], label: str) -> None:
    """Validate the JSON-Schema subset used by the four public contracts."""
    expected = schema.get("type")
    if expected is not None:
        allowed = [expected] if isinstance(expected, str) else expected
        if not any(_type_matches(value, kind) for kind in allowed):
            raise ContractError(f"{label}: expected type {allowed}, got {type(value).__name__}")
    if "const" in schema and value != schema["const"]:
        raise ContractError(f"{label}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractError(f"{label}: value {value!r} is outside enum")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ContractError(f"{label}: string shorter than minLength")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            raise ContractError(f"{label}: string does not match {pattern}")

    if isinstance(value, int) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            raise ContractError(f"{label}: number below minimum")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ContractError(f"{label}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ContractError(f"{label}: too many items")
        if schema.get("uniqueItems"):
            frozen = [json.dumps(item, sort_keys=True) for item in value]
            if len(frozen) != len(set(frozen)):
                raise ContractError(f"{label}: duplicate items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_schema_subset(item, item_schema, f"{label}[{index}]")

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        missing = required - set(value)
        if missing:
            raise ContractError(f"{label}: missing fields {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise ContractError(f"{label}: extra fields {sorted(extra)}")
        additional = schema.get("additionalProperties")
        for key, item in value.items():
            if key in properties:
                validate_schema_subset(item, properties[key], f"{label}.{key}")
            elif isinstance(additional, dict):
                validate_schema_subset(item, additional, f"{label}.{key}")


def _git_blob(repo: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        diagnostic = result.stderr.decode("utf-8", errors="replace").strip()
        raise ContractError(f"source blob unavailable {repo}/{path}@{commit}: {diagnostic}")
    return result.stdout


def validate_source_manifest(manifest: dict[str, Any], verify_git: bool = True) -> set[str]:
    required = {
        "schema_id", "manifest_id", "date", "federation_root_name",
        "source_policy", "claim_compiler_environment", "repositories",
        "sources", "excluded_inputs",
    }
    if set(manifest) != required:
        raise ContractError(
            f"source manifest closed contract failure missing={sorted(required - set(manifest))} "
            f"extra={sorted(set(manifest) - required)}"
        )
    if manifest["schema_id"] != "emergentism/PublicWisdomSourceManifest.v1":
        raise ContractError("source manifest schema_id drift")
    if manifest["manifest_id"] != "PUBLIC-WISDOM-SOURCES@1":
        raise ContractError("source manifest ID drift")
    if manifest["date"] != "2026-09-01":
        raise ContractError("source manifest date drift")
    environment = manifest["claim_compiler_environment"]
    if environment.get("variable") != "EMERGENTISM_PRIMARY_CHECKOUT_ROOT":
        raise ContractError("explicit federation environment is missing")
    if set(environment.get("excluded_carriers", [])) != {".codex-worktrees", ".claude/worktrees", ".git"}:
        raise ContractError("source carrier exclusion set drift")

    repositories: dict[str, dict[str, str]] = {}
    for row in manifest["repositories"]:
        if set(row) != {"repo_id", "root", "commit"}:
            raise ContractError(f"repository row is not closed: {row.get('repo_id')}")
        repo_id = row["repo_id"]
        if repo_id in repositories:
            raise ContractError(f"duplicate repository ID: {repo_id}")
        if not re.fullmatch(r"[0-9a-f]{40}", row["commit"]):
            raise ContractError(f"{repo_id}: invalid commit")
        root = Path(row["root"])
        if root.is_absolute() or ".." in root.parts:
            raise ContractError(f"{repo_id}: repository root escapes federation")
        repositories[repo_id] = row

    source_ids: set[str] = set()
    for row in manifest["sources"]:
        if set(row) != {"source_id", "repo_id", "path", "sha256", "role"}:
            raise ContractError(f"source row is not closed: {row.get('source_id')}")
        source_id = row["source_id"]
        if not re.fullmatch(r"SRC-[A-Z0-9-]+", source_id):
            raise ContractError(f"invalid source ID: {source_id}")
        if source_id in source_ids:
            raise ContractError(f"duplicate source ID: {source_id}")
        source_ids.add(source_id)
        if row["repo_id"] not in repositories:
            raise ContractError(f"{source_id}: unknown repository")
        if row["role"] not in {"SEMANTIC_INPUT", "APPLICATION_CONTEXT", "COVERAGE_REGISTRY", "DESIGN_CRAFT_INPUT", "HISTORICAL_CUSTODY"}:
            raise ContractError(f"{source_id}: unknown source role")
        path = Path(row["path"])
        if path.is_absolute() or ".." in path.parts:
            raise ContractError(f"{source_id}: source path escapes repository")
        if any(part in FORBIDDEN_PATH_PARTS for part in path.parts) or (
            ".claude" in path.parts and "worktrees" in path.parts
        ):
            raise ContractError(f"{source_id}: worktree or Git carrier is not custody")
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ContractError(f"{source_id}: invalid SHA-256")
        if verify_git:
            repo = repositories[row["repo_id"]]
            repo_root = (FEDERATION_ROOT / repo["root"]).resolve()
            if not repo_root.is_relative_to(FEDERATION_ROOT.resolve()):
                raise ContractError(f"{source_id}: resolved repository escapes federation")
            actual = digest_bytes(_git_blob(repo_root, repo["commit"], row["path"]))
            if actual != row["sha256"]:
                raise ContractError(
                    f"{source_id}: committed source digest drift; expected {row['sha256']}, got {actual}"
                )

    for row in manifest["excluded_inputs"]:
        if set(row) != {"path", "reason"} or not row["path"] or not row["reason"]:
            raise ContractError("excluded source rows require path and reason")
    return source_ids


def validate_stack(stack: dict[str, Any], schema: dict[str, Any]) -> None:
    validate_schema_subset(stack, schema, "EmergenceStack.v1")
    expected_names = ["Signal", "Data", "Information", "Knowledge", "Judgment", "Wisdom"]
    names = [row["name"] for row in stack["stages"]]
    ordinals = [row["ordinal"] for row in stack["stages"]]
    ids = [row["stage_id"] for row in stack["stages"]]
    if names != expected_names or ordinals != list(range(1, 7)) or ids != [f"ES-{n}" for n in range(1, 7)]:
        raise ContractError("Emergence Stack stage order drift")
    expected_edges = [(f"ES-{n}", f"ES-{n + 1}") for n in range(1, 6)]
    actual_edges = [(row["from"], row["to"]) for row in stack["promotions"]]
    if actual_edges != expected_edges:
        raise ContractError("promotion edges must be adjacent and complete; skips are forbidden")
    if any(stage["name"] == "Public" for stage in stack["stages"]):
        raise ContractError("Public is a projection, not a higher truth stage")


def _validate_outcomes(record: dict[str, Any]) -> None:
    for index, outcome in enumerate(record["outcomes"]):
        required = {"outcome_id", "kind", "independent_provenance", "metric", "result", "source_id"}
        if set(outcome) != required:
            raise ContractError(f"{record['stable_id']}.outcomes[{index}]: outcome contract is not closed")
        if outcome["kind"] != "INDEPENDENT_OUTCOME":
            raise ContractError(f"{record['stable_id']}: receipts or agent agreement are not outcomes")
        if not outcome["independent_provenance"]:
            raise ContractError(f"{record['stable_id']}: outcome lacks independent provenance")


def validate_records(
    record_set: dict[str, Any], schema: dict[str, Any], source_ids: set[str]
) -> list[dict[str, Any]]:
    if set(record_set) != {"schema_id", "record_order", "records"}:
        raise ContractError("PublicWisdomRecordSet.v1 is not closed")
    if record_set["schema_id"] != "emergentism/PublicWisdomRecordSet.v1":
        raise ContractError("record-set schema drift")
    records = record_set["records"]
    ids = [record["stable_id"] for record in records]
    if ids != record_set["record_order"] or len(ids) != len(set(ids)):
        raise ContractError("wisdom record order or stable IDs are invalid")
    by_id = {record["stable_id"]: record for record in records}
    for record in records:
        validate_schema_subset(record, schema, record["stable_id"])
        unknown = set(record["source_ids"]) - source_ids
        if unknown:
            raise ContractError(f"{record['stable_id']}: dangling source IDs {sorted(unknown)}")
        _validate_outcomes(record)
        if record["supported_by_outcome_count"] != len(record["outcomes"]):
            raise ContractError(f"{record['stable_id']}: outcome count drift")
        if record["maturity"] == "SUPPORTED" and not record["outcomes"]:
            raise ContractError(f"{record['stable_id']}: component support or publication is not integrated support")
        if record["maturity"] != "SUPPORTED" and record["supported_by_outcome_count"]:
            raise ContractError(f"{record['stable_id']}: outcomes require an explicit maturity adjudication")
        lineage = record["lineage"]
        for relation in ("predecessor_id", "successor_id", "correction_of"):
            target = lineage[relation]
            if target is not None:
                if target == record["stable_id"]:
                    raise ContractError(f"{record['stable_id']}: lineage cannot point to itself")
                if target not in by_id:
                    raise ContractError(f"{record['stable_id']}: dangling {relation} {target}")
        if record["projection"] in {"CORRECTED", "RETRACTED"} and not record["corrections"]:
            raise ContractError(f"{record['stable_id']}: corrected or retracted projection needs a correction ledger")
        if record["corrections"] and not lineage["correction_of"]:
            raise ContractError(f"{record['stable_id']}: grave resurrection requires a new successor with correction_of")
    return records


def validate_cards(
    card_set: dict[str, Any], schema: dict[str, Any], source_ids: set[str]
) -> list[dict[str, Any]]:
    if set(card_set) != {"schema_id", "card_order", "cards"}:
        raise ContractError("EstateApplicationCardSet.v1 is not closed")
    if card_set["schema_id"] != "emergentism/EstateApplicationCardSet.v1":
        raise ContractError("application-card set schema drift")
    cards = card_set["cards"]
    ids = [card["stable_id"] for card in cards]
    if ids != card_set["card_order"] or len(ids) != len(set(ids)):
        raise ContractError("application-card order or stable IDs are invalid")
    for card in cards:
        validate_schema_subset(card, schema, card["stable_id"])
        unknown = set(card["source_ids"]) - source_ids
        if unknown:
            raise ContractError(f"{card['stable_id']}: dangling source IDs {sorted(unknown)}")
        if card["coverage_state"] == "CANDIDATE_ONLY" and card["adoption_state"] != "NOT_ADOPTED_BY_PRODUCT":
            raise ContractError(f"{card['stable_id']}: a product candidate cannot promote or adopt itself")
        if card["coverage_state"] == "ADMITTED_APPLICATION":
            if card["stable_id"] != "EAC-EMERGENTISM@1" or card["adoption_state"] != "ADOPTED_IN_EMERGENTISM":
                raise ContractError("only Emergentism may admit this doctrine application")
        if card["source_owner"] != "01_EMERGENTISM" and "defines Emergentism doctrine" in card["candidate_application"]:
            raise ContractError(f"{card['stable_id']}: product may not define Emergentism doctrine")
    return cards


def validate_ledger(
    ledger: dict[str, Any], schema: dict[str, Any], source_ids: set[str], cards: list[dict[str, Any]]
) -> None:
    validate_schema_subset(ledger, schema, "EstateCoverageLedger.v1")
    card_ids = {card["stable_id"] for card in cards}
    seen_lanes: set[str] = set()
    referenced_cards: set[str] = set()
    for row in ledger["entries"]:
        if row["lane_id"] in seen_lanes:
            raise ContractError(f"duplicate coverage lane: {row['lane_id']}")
        seen_lanes.add(row["lane_id"])
        unknown = set(row["source_ids"]) - source_ids
        if unknown:
            raise ContractError(f"{row['lane_id']}: dangling source IDs {sorted(unknown)}")
        card_id = row["application_card_id"]
        if row["coverage_state"] in {"ADMITTED_APPLICATION", "CANDIDATE_ONLY"}:
            if card_id not in card_ids:
                raise ContractError(f"{row['lane_id']}: application state requires a valid card")
            referenced_cards.add(card_id)
        elif card_id is not None:
            raise ContractError(f"{row['lane_id']}: non-application coverage cannot cite an application card")
    if referenced_cards != card_ids:
        raise ContractError(f"coverage ledger does not classify every card: {sorted(card_ids - referenced_cards)}")
    actual = Counter(row["coverage_state"] for row in ledger["entries"])
    expected = {state: actual.get(state, 0) for state in COVERAGE_STATES}
    if ledger["counts"] != expected:
        raise ContractError(f"coverage counts drift: expected {expected}")
    if not ledger["zero_unclassified"]:
        raise ContractError("coverage ledger contains an unclassified lane")


def load_and_validate(verify_git: bool = True) -> dict[str, Any]:
    schemas = {name: load_json(path) for name, path in SCHEMAS.items()}
    manifest = load_json(PATHS["manifest"])
    stack = load_json(PATHS["stack"])
    record_set = load_json(PATHS["records"])
    card_set = load_json(PATHS["cards"])
    ledger = load_json(PATHS["ledger"])

    source_ids = validate_source_manifest(manifest, verify_git=verify_git)
    validate_stack(stack, schemas["stack"])
    records = validate_records(record_set, schemas["record"], source_ids)
    cards = validate_cards(card_set, schemas["card"], source_ids)
    validate_ledger(ledger, schemas["ledger"], source_ids, cards)
    return {
        "manifest": manifest,
        "stack": stack,
        "record_set": record_set,
        "records": records,
        "card_set": card_set,
        "cards": cards,
        "ledger": ledger,
    }


def compile_corpus(bundle: dict[str, Any]) -> dict[str, Any]:
    records = bundle["records"]
    cards = bundle["cards"]
    ledger = bundle["ledger"]
    kind_counts = Counter(record["kind"] for record in records)
    maturity_counts = Counter(record["maturity"] for record in records)
    projection_counts = Counter(record["projection"] for record in records)
    return {
        "schema_id": "emergentism/PublicWisdomCorpus.v1",
        "release_id": "PUBLIC-WISDOM-2026-09-01",
        "date": "2026-09-01",
        "authorship": "Yves R. Burri",
        "ai_assistance": "AI assistance disclosed; no AI coauthor, authority bearer, or independent outcome source.",
        "license": "CC BY-SA 4.0",
        "source_manifest_sha256": digest_path(PATHS["manifest"]),
        "input_hashes": {f"{name}_sha256": digest_path(path) for name, path in PATHS.items()},
        "schema_hashes": {f"{name}_sha256": digest_path(path) for name, path in SCHEMAS.items()},
        "record_order": bundle["record_set"]["record_order"],
        "application_card_order": bundle["card_set"]["card_order"],
        "counts": {
            "kind": {name: kind_counts.get(name, 0) for name in KINDS},
            "maturity": {name: maturity_counts.get(name, 0) for name in MATURITIES},
            "projection": {name: projection_counts.get(name, 0) for name in PROJECTIONS},
            "coverage": deepcopy(ledger["counts"]),
        },
        "supported_wisdom": 0,
        "supported_count_is_derived": maturity_counts.get("SUPPORTED", 0),
        "zero_unclassified_lanes": ledger["zero_unclassified"],
        "public_is_truth_rung": False,
        "external_states": {
            "site_published": False,
            "site_deployed": False,
            "product_adoptions": 0,
            "independent_outcomes": sum(len(record["outcomes"]) for record in records),
            "external_validation": False,
        },
        "notes": [
            "Formal validity, survival, publication, agent agreement, and polish cannot promote a record to Supported Wisdom.",
            "Estate applications are source-owned candidates unless the coverage ledger says ADMITTED_APPLICATION.",
            "Public projection changes visibility only and begins another correction loop."
        ],
    }


def run(mode: str) -> int:
    bundle = load_and_validate(verify_git=True)
    compiled = compile_corpus(bundle)
    rendered = pretty(compiled)
    if mode == "write":
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"WROTE {OUTPUT.relative_to(EMERGENTISM_ROOT)}")
        return 0
    if not OUTPUT.is_file():
        raise ContractError(f"missing generated corpus: {OUTPUT}")
    actual = OUTPUT.read_text(encoding="utf-8")
    if actual != rendered:
        raise ContractError("PublicWisdomCorpus.v1.json drift; run build_public_wisdom.py --write")
    print("PUBLIC WISDOM CONTRACT: PASS")
    print(f"- records: {len(bundle['records'])}")
    print(f"- supported: {compiled['supported_wisdom']}")
    print(f"- application cards: {len(bundle['cards'])}")
    print(f"- coverage lanes: {sum(compiled['counts']['coverage'].values())}")
    print("- public is a projection: yes")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="write deterministic compiled output")
    group.add_argument("--check", action="store_true", help="validate and require byte-identical output")
    args = parser.parse_args()
    try:
        return run("write" if args.write else "check")
    except (ContractError, json.JSONDecodeError) as exc:
        print(f"PUBLIC WISDOM CONTRACT: FAIL\n- {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

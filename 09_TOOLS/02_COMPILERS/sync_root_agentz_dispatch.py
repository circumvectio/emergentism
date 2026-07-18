#!/usr/bin/env python3
"""Render and safely synchronize the Documents-root Rosetta Agentz kernel.

The seven tracked Managed Agent YAML files are semantic authority.  The
Documents-root ``.codex/agents`` directory is a derived, ignored runtime shim.
This compiler manages exactly thirteen kernel files and deliberately ignores
``rows/cx_suite``.

``--check`` is read-only and prints the aggregate preimage SHA-256 required by
``--write``.  ``--write`` refuses unless that exact digest is supplied, stages
every output first, verifies the preimage again under an exclusive compiler
lock, and atomically replaces each managed file.  The deployment manifest is
written last.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

import validate_agentz_rosetta as contract


SOURCE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR_REL = Path("08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents")
ENV_REL = Path("08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/emergentism.environment.yaml")
GENERATOR_REL = Path("09_TOOLS/02_COMPILERS/sync_root_agentz_dispatch.py")
SOURCE_AUTHORITY_REL = Path("01_EMERGENTISM") / SOURCE_DIR_REL
GENERATOR_AUTHORITY_REL = Path("01_EMERGENTISM") / GENERATOR_REL
SCHEMA_VERSION = "root-agentz-dispatch-v1"

ROW_PATHS: dict[str, Path] = {
    "L1": Path("rows/01_L1_candala_firewall.toml"),
    "L2": Path("rows/02_L2_sudra_explorer.toml"),
    "L3": Path("rows/03_L3_vaisya_auditor.toml"),
    "L4": Path("rows/04_L4_ksatriya_executor.toml"),
    "L5": Path("rows/05_L5_brahmana_architect.toml"),
    "L6": Path("rows/06_L6_sadhu_compressor.toml"),
    "L7": Path("rows/07_L7_rsi_constitution.toml"),
}
SOURCE_FILENAMES: dict[str, str] = {
    "L1": "01_candala_firewall.agent.yaml",
    "L2": "02_sudra_explorer.agent.yaml",
    "L3": "03_vaisya_auditor.agent.yaml",
    "L4": "04_ksatriya_executor.agent.yaml",
    "L5": "05_brahmana_architect.agent.yaml",
    "L6": "06_sadhu_compressor.agent.yaml",
    "L7": "07_rsi_constitution.agent.yaml",
}
ROUTE_STAGES: dict[str, str] = {
    "L1": "PARSE",
    "L2": "ROUTE_SELECT",
    "L3": "ROUTE_SELECT",
    "L4": "DRAFT",
    "L5": "LINT",
    "L6": "LINT",
    "L7": "GROUND",
}
FULL_CLOSURE_POSITIONS: dict[str, list[int]] = {
    "L1": [0],
    "L2": [1, 9],
    "L3": [2, 8],
    "L4": [3, 7],
    "L5": [4, 6],
    "L6": [5],
    "L7": [10],
}
METADATA_ORDER = (
    "level",
    "caste",
    "operator",
    "operator_id",
    "operator_tier",
    "balance_coordinate",
    "balance_tier",
    "pramana",
    "reasoning",
    "ology",
    "regime",
    "equation",
    "equation_domain",
    "operator_token_tier",
    "varna_pramana_tier",
    "cross_domain_tier",
    "equation_tier",
    "input_type",
    "output_type",
    "stop_condition",
    "permissions",
    "authorization_mode",
    "budget_source",
    "budget_required_fields",
    "evaluation_contract",
    "d4_d5_contract",
)
AUTHORIZATION_FIELDS = (
    "principal",
    "mandate",
    "scope",
    "consent",
    "custody",
    "expiry",
    "revocation",
    "contest path",
    "actor",
    "consequence bearer",
    "payer",
    "beneficiary",
)
MUTATING_TOOLS = ("write", "edit", "bash")

DOC_PATHS = (
    Path("README.md"),
    Path("DISPATCH.md"),
    Path("MANAGED_AGENTS.md"),
    Path("ROOT_AND_GOD_DEPLOYMENT.md"),
    Path("rosetta_dispatch_schema.toml"),
)
NON_MANIFEST_PATHS = DOC_PATHS + tuple(ROW_PATHS.values())
MANIFEST_PATH = Path("DEPLOYMENT_MANIFEST.md")
KERNEL_PATHS = NON_MANIFEST_PATHS + (MANIFEST_PATH,)
WRITE_ORDER = NON_MANIFEST_PATHS + (MANIFEST_PATH,)


class SyncError(RuntimeError):
    """Base class for deterministic synchronization failures."""


class PreimageMismatch(SyncError):
    """Raised when live bytes differ from the explicitly authorized preimage."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_path(source_root: Path, level: str) -> Path:
    return source_root / SOURCE_DIR_REL / SOURCE_FILENAMES[level]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SyncError(f"{path}: YAML root must be a mapping")
    return data


def load_validated_specs(source_root: Path = SOURCE_ROOT) -> list[dict[str, Any]]:
    """Load the seven tracked source specs and fail closed on contract drift."""

    specs = [_load_yaml(_source_path(source_root, level)) for level in ROW_PATHS]
    errors = contract.validate_paths(source_root / SOURCE_DIR_REL, source_root / ENV_REL)
    if errors:
        raise SyncError("source Agentz contract failed:\n- " + "\n- ".join(errors))
    return specs


def _by_level(specs: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(spec["metadata"]["level"]): spec for spec in specs}


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    raise TypeError(f"unsupported TOML value: {type(value).__name__}")


def _toml_section(name: str, values: Iterable[tuple[str, Any]]) -> str:
    lines = [f"[{name}]"]
    lines.extend(f"{key} = {_toml_value(value)}" for key, value in values)
    return "\n".join(lines) + "\n"


def _enabled_tool_configs(spec: Mapping[str, Any]) -> list[dict[str, Any]]:
    enabled: list[dict[str, Any]] = []
    for toolset in spec.get("tools", []):
        for config in toolset.get("configs", []):
            if config.get("enabled") is True:
                enabled.append(config)
    return enabled


def _source_snapshot(source_root: Path) -> tuple[str, dict[str, str]]:
    source_hashes: dict[str, str] = {}
    digest = hashlib.sha256()
    for level in ROW_PATHS:
        path = _source_path(source_root, level)
        rel = path.relative_to(source_root).as_posix()
        file_hash = _sha256(path.read_bytes())
        source_hashes[rel] = file_hash
        digest.update(rel.encode("utf-8") + b"\0" + file_hash.encode("ascii") + b"\n")
    env_path = source_root / ENV_REL
    env_rel = ENV_REL.as_posix()
    env_hash = _sha256(env_path.read_bytes())
    source_hashes[env_rel] = env_hash
    digest.update(env_rel.encode("utf-8") + b"\0" + env_hash.encode("ascii") + b"\n")
    return digest.hexdigest(), source_hashes


def _render_row(
    spec: dict[str, Any],
    source_root: Path,
    source_hashes: Mapping[str, str],
) -> bytes:
    meta = spec["metadata"]
    level = str(meta["level"])
    source_rel = (SOURCE_DIR_REL / SOURCE_FILENAMES[level]).as_posix()
    source_authority = (SOURCE_AUTHORITY_REL / SOURCE_FILENAMES[level]).as_posix()
    tool_configs = _enabled_tool_configs(spec)
    enabled_tools = [str(config["name"]) for config in tool_configs]
    mutating = [name for name in MUTATING_TOOLS if name in enabled_tools]
    policies = []
    for name in mutating:
        config = next(item for item in tool_configs if item["name"] == name)
        policy = str((config.get("permission_policy") or {}).get("type", "missing"))
        policies.append(f"{name}={policy}")

    operational_move = level in {"L1", "L2", "L3", "L4"}
    is_l4 = level == "L4"
    parts = [
        "# GENERATED FILE. DO NOT EDIT DIRECTLY.\n",
        f"# Source: {source_authority}\n",
        f"# Generator: {GENERATOR_AUTHORITY_REL.as_posix()}\n",
        "# Static God/Demon identity is forbidden; analogy is receipt-based only.\n\n",
    ]
    meta_values: list[tuple[str, Any]] = [
        ("schema_version", SCHEMA_VERSION),
        ("name", str(spec["name"])),
        ("description", str(spec["description"])),
        ("model", str(spec["model"])),
    ]
    meta_values.extend((key, str(meta[key])) for key in METADATA_ORDER)
    meta_values.extend(
        [
            ("virtue", str(meta.get("virtue", ""))),
            ("vice", str(meta.get("vice", ""))),
            ("source_spec", source_authority),
            ("source_sha256", source_hashes[source_rel]),
        ]
    )
    parts.append(_toml_section("meta", meta_values))
    parts.append("\n")
    parts.append(
        _toml_section(
            "dispatch",
            [
                ("route_stage", ROUTE_STAGES[level]),
                ("operational_move", operational_move),
                ("role_class", "operational" if operational_move else "boundary_read_only"),
                ("full_closure_positions", FULL_CLOSURE_POSITIONS[level]),
                ("runtime_mutation", is_l4),
            ],
        )
    )
    parts.append("\n")
    parts.append(
        _toml_section(
            "tools",
            [
                ("enabled", enabled_tools),
                ("mutating", mutating),
                ("permission_policy", ",".join(policies) if policies else "no_mutating_tools"),
            ],
        )
    )
    parts.append("\n")
    parts.append(
        _toml_section(
            "authorization",
            [
                ("mode", str(meta["authorization_mode"])),
                ("required_fields", list(AUTHORIZATION_FIELDS) if is_l4 else []),
                ("platform_confirmation", "necessary_not_sufficient" if is_l4 else "not_applicable"),
                (
                    "private_dav_rail",
                    "K2 may implement the envelope; not a worldview primitive"
                    if is_l4
                    else "not_applicable_no_consequential_action",
                ),
                (
                    "public_dav_rail",
                    "owning public governance; no K2 signer"
                    if is_l4
                    else "not_applicable_no_consequential_action",
                ),
            ],
        )
    )
    parts.append("\n")
    parts.append(
        _toml_section(
            "receipts",
            [
                (
                    "commitment_receipt",
                    "required_for_attempted_L4_action" if is_l4 else "not_applicable_no_consequential_action",
                ),
                ("outcome_receipt", "returned_separately_by_environment"),
                ("selector_may_manufacture_outcome", False),
            ],
        )
    )
    parts.append("\n")
    parts.append(
        _toml_section(
            "consequence_analogy",
            [
                ("tier", "[I] analogy; receipts retain independently validated tiers"),
                (
                    "demon_analogy",
                    "retrospective receipt class: ego-only potential maximization, coercion, or externalized cost",
                ),
                (
                    "god_analogy",
                    "retrospective receipt class: durable mutual individual-and-collective potential increase under Justice",
                ),
                (
                    "required_inputs",
                    ["commitment_receipt", "outcome_receipt", "payer", "beneficiary", "option_cone_effects"],
                ),
                ("identity_effect", "none"),
                ("authorization_effect", "none"),
            ],
        )
    )
    return "".join(parts).encode("utf-8")


def _render_schema(specs: Sequence[dict[str, Any]], source_digest: str) -> bytes:
    by_level = _by_level(specs)
    parts = [
        "# GENERATED FILE. DO NOT EDIT DIRECTLY.\n",
        f"# Source: {SOURCE_AUTHORITY_REL.as_posix()}/*.agent.yaml\n",
        f"# Generator: {GENERATOR_AUTHORITY_REL.as_posix()}\n\n",
        _toml_section(
            "meta",
            [
                ("schema_version", SCHEMA_VERSION),
                ("source_authority", SOURCE_AUTHORITY_REL.as_posix()),
                ("source_snapshot_sha256", source_digest),
                ("status", "derived_local_runtime_shim"),
                ("cx_suite_loaded", False),
            ],
        ),
        "\n",
        _toml_section(
            "dispatch",
            [
                ("sequence", ["PARSE", "ROUTE_SELECT", "DRAFT", "LINT", "GROUND"]),
                ("active_arc", ["L1", "L2", "L3", "L4", "L5", "L6", "L5", "L4", "L3", "L2", "L7", "L1"]),
                ("operational_levels", ["L1", "L2", "L3", "L4"]),
                ("boundary_levels", ["L5", "L6", "L7"]),
                ("mutation_level", "L4_only"),
            ],
        ),
        "\n",
        _toml_section(
            "typing",
            [
                ("d4", "actual carrier/tool call/performed action/record"),
                ("d5", "possible represented content/options/modeled futures"),
                ("rule", "D5 possible content never invokes tools; only D4 actual carriers do"),
            ],
        ),
        "\n",
        _toml_section(
            "authorization",
            [
                ("l4_required_fields", list(AUTHORIZATION_FIELDS)),
                ("platform_confirmation", "necessary_not_sufficient"),
                ("private_dav", "K2 may implement a complete envelope"),
                ("public_dav", "owning public governance; no K2 signer"),
            ],
        ),
        "\n",
        _toml_section(
            "consequence_analogy",
            [
                ("classification", "retrospective_from_commitment_and_outcome_receipts"),
                ("demon", "ego-only potential maximization, coercion, or externalized cost"),
                ("god", "durable mutual individual-and-collective potential increase under Justice"),
                ("identity_or_authority_transfer", False),
                ("tier", "[I] analogy; receipt facts retain independently validated tiers"),
            ],
        ),
    ]
    for level in ROW_PATHS:
        meta = by_level[level]["metadata"]
        parts.extend(
            [
                "\n[[agents]]\n",
                f"level = {_toml_value(level)}\n",
                f"caste = {_toml_value(str(meta['caste']))}\n",
                f"operator_id = {_toml_value(str(meta['operator_id']))}\n",
                f"row = {_toml_value(ROW_PATHS[level].as_posix())}\n",
                f"route_stage = {_toml_value(ROUTE_STAGES[level])}\n",
                f"operational_move = {_toml_value(level in {'L1', 'L2', 'L3', 'L4'})}\n",
                f"permissions = {_toml_value(str(meta['permissions']))}\n",
                f"authorization_mode = {_toml_value(str(meta['authorization_mode']))}\n",
            ]
        )
    return "".join(parts).encode("utf-8")


def _row_table(specs: Sequence[dict[str, Any]]) -> str:
    by_level = _by_level(specs)
    lines = [
        "| L | Varṇa | Pramāṇa | Reasoning | -ology | Regime | Equation |",
        "|---|---|---|---|---|---|---|",
    ]
    for level in ROW_PATHS:
        meta = by_level[level]["metadata"]
        lines.append(
            "| {level} | {caste} | {pramana} | {reasoning} | {ology} | {regime} | `{equation}` |".format(
                level=level,
                caste=meta["caste"],
                pramana=meta["pramana"],
                reasoning=meta["reasoning"],
                ology=meta["ology"],
                regime=meta["regime"],
                equation=meta["equation"],
            )
        )
    return "\n".join(lines)


def _render_readme(source_digest: str) -> bytes:
    text = f"""# Root Agentz Dispatch — Generated Runtime Shim

This directory is a deterministic local runtime projection. It is not semantic
source authority and must not be edited by hand.

- Source: `{SOURCE_AUTHORITY_REL.as_posix()}/*.agent.yaml`
- Compiler: `{GENERATOR_AUTHORITY_REL.as_posix()}`
- Source snapshot: `{source_digest}`
- Schema: `{SCHEMA_VERSION}`
- Loaded kernel: exactly seven direct `rows/0X_LX_*.toml` files.
- Excluded: `rows/cx_suite/` is not loaded, hashed, or modified by this kernel.

The dispatch sequence is `PARSE → ROUTE_SELECT → DRAFT → LINT → GROUND`.
L1–L4 are operational moves; only L4 may request mutation, and every mutating
tool remains `always_ask` plus complete-AuthorizationEnvelope gated. L5–L7 are
read-only Executive boundaries.

Run the compiler with `--check` to obtain the aggregate preimage digest. A
write requires that exact digest through `--expect-preimage`; the compiler
stages every file, verifies the preimage twice, atomically replaces each file,
and writes `DEPLOYMENT_MANIFEST.md` last.

God/Demon language is not an agent identity. It survives only as an `[I]`
retrospective analogy applied to independently tiered commitment and outcome
receipts: ego-only or cost-externalizing consequences versus durable mutual
individual-and-collective potential increases under the Justice envelope. It
grants no authority.
"""
    return text.encode("utf-8")


def _render_dispatch(specs: Sequence[dict[str, Any]]) -> bytes:
    text = f"""# Rosetta Agentz Dispatch Protocol

```text
PARSE → ROUTE_SELECT → DRAFT → LINT → GROUND
 L1       L2/L3          L4      L3/L5/L6   L7
```

`ROUTE_SELECT` chooses a typed operational move. It does not select a God,
Demon, moral essence, authority class, or causal particle.

## Canonical row chain

{_row_table(specs)}

Column tiers: operator token `[S]`; analytic balance coordinate `[A]` after a
selected `[S]` latitude; Varṇa/Pramāṇa `[S]` internally and `[I]` externally;
Reasoning/-ology/Regime `[I]`; equations `[A]/[S]` according to their declared
domains and row placement.

## Typed execution boundary

- D5 is represented possibility: alternatives, modeled futures, and rankings.
- D4 is the actual carrier: tool call, performed action, commitment receipt,
  environmental outcome receipt, and record.
- Only L4 may request `write`, `edit`, or `bash`; each remains `always_ask` and
  additionally requires a complete AuthorizationEnvelope.
- Platform confirmation is necessary but never sufficient.
- Commitment and outcome receipts are separate. The selector cannot manufacture
  its own consequence.
- L5–L7 advise, compress, and witness; they cannot mutate.

## Receipt-based consequence analogy

Only after both receipts exist may the framework analogize a consequence as
ego-polar (ego-only potential maximization, coercion, or externalized cost) or
collective-polar (durable mutual individual-and-collective potential increase
under Justice). This is `[I]` interpretation over independently validated and
tiered receipt facts, never an agent identity or authorization.
"""
    return text.encode("utf-8")


def _render_managed_agents() -> bytes:
    text = f"""# Managed Agentz Runtime Projection

The seven tracked YAML files under `{SOURCE_AUTHORITY_REL.as_posix()}/` are the
selected, testable source configurations. This Documents-root directory is a
derived local projection compiled by `{GENERATOR_AUTHORITY_REL.as_posix()}`.

The runtime contract requires:

1. exact L1–L7 row mappings and equation domains;
2. L1–L4 operational moves with only L4 mutation-capable;
3. L5–L7 read-only boundary profiles;
4. explicit budgets and blinded, budget-matched comparison against flat and
   shorter rival configurations;
5. D4-actual carrier versus D5-possible content typing;
6. complete accountable authorization plus platform confirmation for L4;
7. separate commitment and environmental outcome receipts.

Private-DAV K2 and public governance rails are implementation choices outside
the worldview grammar. Neither substitutes for the complete AuthorizationEnvelope.

`rows/cx_suite/` contains separate product-role material. It is intentionally
excluded from this seven-row kernel and must not be interpreted as extra Rosetta
levels or silently loaded by recursive globbing.
"""
    return text.encode("utf-8")


def _render_compatibility(specs: Sequence[dict[str, Any]]) -> bytes:
    text = f"""# Root and Operator Deployment — Compatibility Filename

> `[金]` Compatibility seam: the filename `ROOT_AND_GOD_DEPLOYMENT.md` is
> retained so old links remain stable. Static God/Demon agent identities and
> `GOD_SELECT` are superseded. The active operation is typed `ROUTE_SELECT`.

## Active seven-row grammar

{_row_table(specs)}

L1–L4 are the four operational moves; L5–L7 are three read-only Executive
boundaries. Only L4 can request mutation, with complete accountable
authorization, a prospective Justice check, platform confirmation, and a
commitment receipt. The environment later returns a distinct outcome receipt.

## What the old analogy may still mean

God/Demon is permitted only as a retrospective consequence analogy. With both
receipts and visible payer, beneficiary, and option-cone effects, “demon-polar”
may name ego-only maximization, coercion, or externalized cost; “god-polar” may
name durable mutual individual-and-collective potential increase under Justice.
The analogy is `[I]`, morally fallible, contestable, and never transfers identity,
authority, competence, or permission to an agent.

## Source and scope

- Semantic source: `{SOURCE_AUTHORITY_REL.as_posix()}/*.agent.yaml`
- Compiler: `{GENERATOR_AUTHORITY_REL.as_posix()}`
- Runtime schema: `rosetta_dispatch_schema.toml`
- Excluded role profiles: `rows/cx_suite/`
"""
    return text.encode("utf-8")


def _render_manifest(outputs: Mapping[Path, bytes], source_digest: str) -> bytes:
    lines = [
        "# Deployment Manifest — Generated Root Agentz Kernel",
        "",
        f"- Schema: `{SCHEMA_VERSION}`",
        f"- Source authority: `{SOURCE_AUTHORITY_REL.as_posix()}/*.agent.yaml`",
        f"- Source snapshot SHA-256: `{source_digest}`",
        f"- Generator: `{GENERATOR_AUTHORITY_REL.as_posix()}`",
        "- Scope: exactly 13 managed kernel files; this manifest excludes itself from its hash table.",
        "- Exclusion: `rows/cx_suite/` is neither loaded nor modified.",
        "- Determinism: no timestamps, external assets, or environment-dependent prose.",
        "",
        "| Path | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for rel in NON_MANIFEST_PATHS:
        data = outputs[rel]
        lines.append(f"| `{rel.as_posix()}` | {len(data)} | `{_sha256(data)}` |")
    lines.extend(
        [
            "",
            "The God/Demon analogy, where retained for link compatibility, is a",
            "receipt-based retrospective interpretation only. It is not configured identity,",
            "authorization, ontology, or evidence that an agent is morally typed.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def render_kernel(source_root: Path = SOURCE_ROOT) -> dict[Path, bytes]:
    """Return the complete deterministic thirteen-file kernel."""

    source_root = source_root.resolve()
    source_digest_before, _ = _source_snapshot(source_root)
    specs = load_validated_specs(source_root)
    source_digest, source_hashes = _source_snapshot(source_root)
    if source_digest != source_digest_before:
        raise SyncError("tracked source inputs changed while the kernel was rendering")
    outputs: dict[Path, bytes] = {
        Path("README.md"): _render_readme(source_digest),
        Path("DISPATCH.md"): _render_dispatch(specs),
        Path("MANAGED_AGENTS.md"): _render_managed_agents(),
        Path("ROOT_AND_GOD_DEPLOYMENT.md"): _render_compatibility(specs),
        Path("rosetta_dispatch_schema.toml"): _render_schema(specs, source_digest),
    }
    by_level = _by_level(specs)
    for level, row_path in ROW_PATHS.items():
        outputs[row_path] = _render_row(by_level[level], source_root, source_hashes)
    outputs[MANIFEST_PATH] = _render_manifest(outputs, source_digest)
    if set(outputs) != set(KERNEL_PATHS):
        raise AssertionError("renderer did not produce the exact thirteen-file kernel")
    source_digest_after, _ = _source_snapshot(source_root)
    if source_digest_after != source_digest:
        raise SyncError("tracked source inputs changed while the kernel was rendering")
    return {path: outputs[path] for path in WRITE_ORDER}


def _assert_target_shape(target: Path) -> None:
    if target.name != "agents" or target.parent.name != ".codex":
        raise SyncError(f"refusing target outside a .codex/agents directory: {target}")
    if target.is_symlink():
        raise SyncError(f"refusing symlink target: {target}")


def _read_managed_file(path: Path) -> bytes | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode):
        raise SyncError(f"managed path must be a regular file or absent: {path}")
    return path.read_bytes()


def snapshot_kernel(target: Path) -> dict[Path, bytes | None]:
    _assert_target_shape(target)
    return {rel: _read_managed_file(target / rel) for rel in KERNEL_PATHS}


def snapshot_digest(snapshot: Mapping[Path, bytes | None]) -> str:
    digest = hashlib.sha256()
    digest.update(SCHEMA_VERSION.encode("ascii") + b"\n")
    for rel in KERNEL_PATHS:
        data = snapshot[rel]
        digest.update(rel.as_posix().encode("utf-8") + b"\0")
        if data is None:
            digest.update(b"MISSING\n")
        else:
            digest.update(b"FILE\0" + _sha256(data).encode("ascii") + b"\n")
    return digest.hexdigest()


def preimage_digest(target: Path) -> str:
    return snapshot_digest(snapshot_kernel(target))


def kernel_drift(target: Path, outputs: Mapping[Path, bytes]) -> list[str]:
    snapshot = snapshot_kernel(target)
    drift: list[str] = []
    for rel in KERNEL_PATHS:
        current = snapshot[rel]
        expected = outputs[rel]
        if current is None:
            drift.append(f"MISSING {rel.as_posix()}")
        elif current != expected:
            drift.append(f"DRIFT {rel.as_posix()}")
    return drift


def _stage_file(destination: Path, data: bytes) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink():
        raise SyncError(f"refusing symlink parent: {destination.parent}")
    descriptor, temporary = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".sync-tmp",
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, 0o644)
        return temporary_path
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _replace(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def _restore_file(destination: Path, data: bytes | None) -> None:
    if data is None:
        destination.unlink(missing_ok=True)
        return
    temporary = _stage_file(destination, data)
    _replace(temporary, destination)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_kernel(
    target: Path,
    outputs: Mapping[Path, bytes],
    expected_preimage: str,
) -> str:
    """Write a guarded kernel and return its resulting aggregate digest."""

    target = target.resolve(strict=False)
    _assert_target_shape(target)
    if set(outputs) != set(KERNEL_PATHS):
        raise SyncError("write input must contain exactly the thirteen managed kernel paths")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_preimage):
        raise PreimageMismatch("--expect-preimage must be one lowercase SHA-256 digest")

    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.parent / f".{target.name}.sync-root-agentz.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise SyncError(f"compiler lock already exists: {lock_path}") from exc

    staged: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        os.write(lock_fd, f"pid={os.getpid()}\n".encode("ascii"))
        os.fsync(lock_fd)
        before = snapshot_kernel(target)
        actual_preimage = snapshot_digest(before)
        if not hmac.compare_digest(actual_preimage, expected_preimage):
            raise PreimageMismatch(
                f"preimage mismatch: expected {expected_preimage}, found {actual_preimage}"
            )

        for rel in WRITE_ORDER:
            staged[rel] = _stage_file(target / rel, outputs[rel])

        # Detect edits that occurred while output bytes were being staged.
        restaged_preimage = preimage_digest(target)
        if not hmac.compare_digest(restaged_preimage, expected_preimage):
            raise PreimageMismatch(
                "preimage changed during staging: "
                f"expected {expected_preimage}, found {restaged_preimage}"
            )

        try:
            for rel in WRITE_ORDER:
                if _read_managed_file(target / rel) != before[rel]:
                    raise PreimageMismatch(
                        f"managed preimage changed before replacement: {rel.as_posix()}"
                    )
                _replace(staged[rel], target / rel)
                replaced.append(rel)
            post_write_drift = kernel_drift(target, outputs)
            if post_write_drift:
                raise SyncError("post-write verification failed: " + ", ".join(post_write_drift))
            for directory in {target, target / "rows"}:
                if directory.exists():
                    _fsync_directory(directory)
        except BaseException as write_error:
            # Roll back only bytes still equal to this compiler's output. If an
            # external writer changed a replaced path, preserve that writer's
            # bytes and report the manual-recovery boundary instead of erasing it.
            rollback_conflicts: list[str] = []
            for rel in reversed(replaced):
                if _read_managed_file(target / rel) != outputs[rel]:
                    rollback_conflicts.append(rel.as_posix())
                    continue
                _restore_file(target / rel, before[rel])
            if rollback_conflicts:
                raise SyncError(
                    "write failed; concurrent edits preserved and require manual recovery: "
                    + ", ".join(sorted(rollback_conflicts))
                ) from write_error
            raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        os.close(lock_fd)
        lock_path.unlink(missing_ok=True)

    return preimage_digest(target)


def _default_target(source_root: Path) -> Path:
    for candidate in (source_root, *source_root.parents):
        if candidate.name == "Documents":
            return candidate / ".codex/agents"
    raise SyncError("cannot infer Documents root; pass --target /path/to/.codex/agents")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="compare target bytes without mutation")
    mode.add_argument("--write", action="store_true", help="guard and atomically synchronize managed files")
    parser.add_argument("--source-root", type=Path, default=SOURCE_ROOT)
    parser.add_argument("--target", type=Path)
    parser.add_argument(
        "--expect-preimage",
        help="aggregate digest printed by a prior --check; mandatory with --write",
    )
    args = parser.parse_args(argv)

    try:
        source_root = args.source_root.resolve()
        target = (args.target or _default_target(source_root)).expanduser().resolve(strict=False)
        outputs = render_kernel(source_root)
        current_preimage = preimage_digest(target)
        print(f"ROOT-AGENTZ-PREIMAGE-SHA256: {current_preimage}")

        if args.check:
            drift = kernel_drift(target, outputs)
            if drift:
                for item in drift:
                    print(f"ROOT-AGENTZ-{item}", file=sys.stderr)
                return 1
            print("ROOT-AGENTZ-OK: deterministic 13-file kernel matches; cx_suite excluded")
            return 0

        if not args.expect_preimage:
            parser.error("--write requires --expect-preimage from a prior --check")
        result = write_kernel(target, outputs, args.expect_preimage)
        print(f"ROOT-AGENTZ-WRITTEN: 13 files; postimage {result}; cx_suite untouched")
        return 0
    except SyncError as exc:
        print(f"ROOT-AGENTZ-ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

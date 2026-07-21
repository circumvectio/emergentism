#!/usr/bin/env python3
"""Sync generated Rosetta-row tables from per-agent TOML into Agentz specs."""

from __future__ import annotations

import argparse
import difflib
import sys
import tomllib
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ROWS_DIR = PROJECT_ROOT / ".codex/agents/rows"
SPEC_DIR = (
    PROJECT_ROOT
    / "02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION"
)

BEGIN = "<!-- BEGIN GENERATED ROSETTA ROW -->"
END = "<!-- END GENERATED ROSETTA ROW -->"
INSERT_BEFORE = "\n---\n\n### Neuroscience"

ROW_TO_SPEC = {
    "01_L1_candala_firewall.toml": "01_L1_CANDALA_FIREWALL.md",
    "02_L2_sudra_explorer.toml": "02_L2_SHUDRA_SCOUT.md",
    "03_L3_vaisya_auditor.toml": "03_L3_VAISYA_AUDITOR.md",
    "04_L4_ksatriya_executor.toml": "04_L4_KSHATRIYA_EXECUTOR.md",
    "05_L5_brahmana_architect.toml": "05_L5_BRAHMANA_ARCHITECT.md",
    "06_L6_sadhu_compressor.toml": "06_L6_SADHU_COMPRESSOR.md",
    "07_L7_rsi_constitution.toml": "07_L7_RSI_CONSTITUTION.md",
}


def load_agent(row_path: Path) -> dict[str, Any]:
    data = tomllib.loads(row_path.read_text(encoding="utf-8"))
    agents = data.get("agents", {})
    if len(agents) != 1:
        raise ValueError(f"{row_path}: expected exactly one [agents.*] entry")
    return next(iter(agents.values()))


def scalar(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ", ".join(scalar(item) for item in value if scalar(item))
    return str(value)


def join_parts(*parts: Any, sep: str = "; ") -> str:
    return sep.join(part for part in (scalar(part) for part in parts) if part)


def labelled(label: str, value: Any) -> str:
    rendered = scalar(value)
    return f"{label}: {rendered}" if rendered else ""


def cell(value: Any) -> str:
    rendered = scalar(value) if not isinstance(value, tuple) else join_parts(*value)
    rendered = rendered or "—"
    return rendered.replace("\n", " ").replace("|", r"\|")


def rosetta_cells(agent: dict[str, Any]) -> list[tuple[str, str]]:
    core = agent["core"]
    trivium = agent["trivium"]
    psychology = agent["psychology"]
    philosophy = agent["philosophy"]
    social = agent["social_political"]
    operator = agent["operator_detail"]
    spiritual = agent["spiritual_yogic"]
    mythology = agent["mythology"]
    neuroscience = agent["neuroscience"]
    computation = agent["computation"]
    game = agent["game_theory"]
    civil = agent["civilisational"]
    pathology = agent["operator_pathology"]
    asura = agent["asura_return"]
    liberal = agent["liberal_arts"]
    pie = agent["pie_roots"]
    deployment = agent["deployment"]

    return [
        (
            "core",
            join_parts(
                labelled("coordinate", core.get("native_coord")),
                labelled("S2", core.get("s2")),
                labelled("transfer", core.get("transfer_sig")),
                labelled("operator", core.get("operator")),
            ),
        ),
        (
            "trivium",
            join_parts(
                labelled("pramāṇa", trivium.get("pramana")),
                labelled("reasoning", trivium.get("reasoning")),
                labelled("ology", trivium.get("ology")),
                labelled("polity", trivium.get("regime_of_polity")),
                labelled("equation", trivium.get("equation")),
            ),
        ),
        (
            "psychology",
            join_parts(
                labelled("stage", psychology.get("stage")),
                labelled("Piaget", psychology.get("piaget")),
                labelled("Kohlberg", psychology.get("kohlberg")),
                labelled("Maslow", psychology.get("maslow")),
                labelled("virtue", psychology.get("virtue")),
                labelled("shadow", psychology.get("shadow")),
            ),
        ),
        (
            "philosophy",
            join_parts(
                labelled("discipline", philosophy.get("discipline")),
                labelled("question", philosophy.get("key_question")),
                labelled("epistemology", philosophy.get("epistemology")),
                labelled("exemplars", philosophy.get("exemplars")),
            ),
        ),
        (
            "social_political",
            join_parts(
                labelled("Plato regime", social.get("plato_regime")),
                labelled("governance", social.get("governance")),
                labelled("economic", social.get("economic")),
                labelled("modern analogue", social.get("modern_analogue")),
            ),
        ),
        (
            "operator_detail",
            join_parts(
                labelled("self", operator.get("self_effect")),
                labelled("other", operator.get("others_effect")),
                labelled("net", operator.get("net_effect")),
                labelled("K*", operator.get("k_star_rule")),
            ),
        ),
        (
            "spiritual_yogic",
            join_parts(
                labelled("path", spiritual.get("yoga_path")),
                labelled("chakra", spiritual.get("chakra")),
                labelled("element", spiritual.get("element")),
                labelled("alchemy", spiritual.get("alchemy")),
                labelled("Gītā", spiritual.get("gita_chapter")),
            ),
        ),
        (
            "mythology",
            join_parts(
                labelled("Greek", mythology.get("greek")),
                labelled("Norse", mythology.get("norse")),
                labelled("Sumerian", mythology.get("sumerian")),
                labelled("Tarot", mythology.get("tarot")),
                labelled("Jungian", mythology.get("jungian")),
                labelled("animal", mythology.get("animal")),
            ),
        ),
        (
            "neuroscience",
            join_parts(
                labelled("region", neuroscience.get("brain_region")),
                labelled("hemisphere", neuroscience.get("hemisphere")),
                labelled("wave", neuroscience.get("brainwave")),
                labelled("mode", neuroscience.get("cognitive_mode")),
            ),
        ),
        (
            "computation",
            join_parts(
                labelled("algorithm", computation.get("algorithm")),
                labelled("process", computation.get("process")),
                labelled("status", computation.get("status")),
            ),
        ),
        (
            "game_theory",
            join_parts(
                labelled("strategy", game.get("strategy")),
                labelled("type", game.get("type")),
                labelled("cooperation", game.get("cooperation")),
                labelled("Nash", game.get("nash")),
            ),
        ),
        (
            "civilisational",
            join_parts(
                labelled("stage", civil.get("civ_stage")),
                labelled("tech", civil.get("tech")),
                labelled("culture", civil.get("culture")),
                labelled("environment", civil.get("environment")),
                labelled("Φ max", civil.get("phi_max")),
            ),
        ),
        (
            "operator_pathology",
            join_parts(
                labelled("season", pathology.get("season")),
                labelled("necessary", pathology.get("when_necessary")),
                labelled("pathologic", pathology.get("when_pathologic")),
                labelled("DSM", pathology.get("dsm")),
                labelled("shadow", pathology.get("op_shadow")),
            ),
        ),
        (
            "asura_return",
            join_parts(
                labelled("form", asura.get("asura_form")),
                labelled("inversion", asura.get("inversion")),
                labelled("egregoric", asura.get("egregoric")),
            ),
        ),
        (
            "liberal_arts",
            join_parts(
                labelled("art", liberal.get("liberal_art")),
                labelled("cluster", liberal.get("cluster")),
                labelled("logic", liberal.get("op_logic")),
            ),
        ),
        (
            "pie_roots",
            join_parts(
                labelled("h2rto", pie.get("h2rto")),
                labelled("dyeu", pie.get("dyeu")),
                labelled("serpent", pie.get("serpent")),
            ),
        ),
        (
            "deployment",
            join_parts(
                labelled("function", deployment.get("function")),
                labelled("replicator", deployment.get("replicator")),
                labelled("direction", deployment.get("direction")),
                labelled("write authority", deployment.get("write_authority")),
                labelled("cure", deployment.get("caste_cure")),
            ),
        ),
    ]


def render_table(agent: dict[str, Any]) -> str:
    lines = [
        BEGIN,
        "### Rosetta Row (canonical 17 columns)",
        "",
        "| Column | Canonical value |",
        "|---|---|",
    ]
    lines.extend(f"| {name} | {cell(value)} |" for name, value in rosetta_cells(agent))
    lines.extend(
        [
            "",
            "_Generated from `.codex/agents/rows/0X_LX_<caste>.toml`; edit the TOML, not this table._",
            END,
        ]
    )
    return "\n".join(lines)


def sync_text(current: str, generated: str, spec_path: Path) -> str:
    if BEGIN in current or END in current:
        start = current.find(BEGIN)
        end = current.find(END)
        if start == -1 or end == -1 or end < start:
            raise ValueError(f"{spec_path}: malformed generated Rosetta-row markers")
        end += len(END)
        return current[:start] + generated + current[end:]

    marker = current.find(INSERT_BEFORE)
    if marker == -1:
        raise ValueError(f"{spec_path}: could not find Geometry→Neuroscience insertion point")
    return current[: marker + 1] + generated + "\n" + current[marker + 1 :]


def iter_targets() -> list[tuple[Path, Path]]:
    targets = []
    for row_name, spec_name in ROW_TO_SPEC.items():
        row_path = ROWS_DIR / row_name
        spec_path = SPEC_DIR / spec_name
        if not row_path.exists():
            raise FileNotFoundError(row_path)
        if not spec_path.exists():
            raise FileNotFoundError(spec_path)
        targets.append((row_path, spec_path))
    return targets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="update markdown specs")
    parser.add_argument("--check", action="store_true", help="fail if specs are stale")
    args = parser.parse_args()

    if args.write == args.check:
        parser.error("choose exactly one of --write or --check")

    stale: list[tuple[Path, str]] = []
    for row_path, spec_path in iter_targets():
        agent = load_agent(row_path)
        generated = render_table(agent)
        current = spec_path.read_text(encoding="utf-8")
        updated = sync_text(current, generated, spec_path)
        if updated == current:
            continue
        if args.write:
            spec_path.write_text(updated, encoding="utf-8")
        else:
            diff = "".join(
                difflib.unified_diff(
                    current.splitlines(keepends=True),
                    updated.splitlines(keepends=True),
                    fromfile=str(spec_path),
                    tofile=f"{spec_path} (expected)",
                )
            )
            stale.append((spec_path, diff))

    if stale:
        for spec_path, diff in stale:
            print(f"stale: {spec_path.relative_to(PROJECT_ROOT)}", file=sys.stderr)
            print(diff, file=sys.stderr)
        return 1

    action = "updated" if args.write else "verified"
    print(f"agent markdown Rosetta rows {action}: {len(ROW_TO_SPEC)}/7 specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

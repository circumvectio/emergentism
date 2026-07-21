#!/usr/bin/env python3
"""
agent_goose_sync.py — propagate canonical Agentz doctrine into the Goose runtime.

Goose is the **applied framework runtime** — the place where Agentz doctrine
becomes operational agent grammar. Per the 2026-05-07 doctrinal settlement:

  Repo .codex/agents/rows/                    = constitutional source (one TOML per agent)
  Repo 02_INFRASTRUCTURE/Cascade/03_RUNTIME_DISPATCH/  = Agentz phenotype specs
  Repo …VMOSK/CONFIG/L<N>.toml                = Agentz phenotype TOMLs
  Goose ~/.config/goose/L<N>.toml             = runtime layer (this script syncs here)

This script is the bridge from the repo canonical layer to the Goose runtime
layer. Same pattern as agent_markdown_rosetta_row_sync.py — sync canonical →
derived, with --check mode to detect drift without writing.

Files synced (repo → Goose):
  - 02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/03_RUNTIME_DISPATCH/VMOSK/CONFIG/L<N>.toml
        → ~/.config/goose/L<N>.toml         (× 7 castes + L_MASTER)
  - TOM.md, MY_SOUL.md, SYSTEM_INSTRUCTIONS.md, ROUTER_CONFIG.yaml
        → ~/.config/goose/<same name>
  - ROSETTA_SOUL_LOOP.md, DELEGATION_GRAMMAR.md
        → ~/.config/goose/<same name>
  - agent_router.py, tom_router.py, agentz_status.py, gooseR, recipes/*
        → ~/.config/goose/<same name>
  - legacy runtime-only TOM shards (L*_TOM.md, AGENT_ROUTER_V2.md)
        → compatibility notices pointing at AGENTZ_ROUTED_TOM.md

Usage:
  python3 agent_goose_sync.py --check    # report drift, no writes, continuous exit
  python3 agent_goose_sync.py --check --strict
                                        # report drift, exit 1 on drift
  python3 agent_goose_sync.py --apply    # write Goose runtime
  python3 agent_goose_sync.py            # alias for --check

Exit 0 = in sync (or apply succeeded).
Exit 1 = drift detected only with --strict; use --apply to write.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VMOSK_CONFIG = (
    PROJECT_ROOT
    / "02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/03_RUNTIME_DISPATCH/VMOSK/CONFIG"
)
GOOSE_DIR = Path.home() / ".config" / "goose"

LEVELS = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L_MASTER"]

RUNTIME_FILES = {f"{lvl}.toml": f"{lvl}.toml" for lvl in LEVELS}
RUNTIME_FILES.update(
    {
        "TOM.md": "TOM.md",
        "MY_SOUL.md": "MY_SOUL.md",
        "SYSTEM_INSTRUCTIONS.md": "SYSTEM_INSTRUCTIONS.md",
        "ROUTER_CONFIG.yaml": "ROUTER_CONFIG.yaml",
        "ROSETTA_SOUL_LOOP.md": "ROSETTA_SOUL_LOOP.md",
        "DELEGATION_GRAMMAR.md": "DELEGATION_GRAMMAR.md",
        "agent_router.py": "agent_router.py",
        "tom_router.py": "tom_router.py",
        "agentz_status.py": "agentz_status.py",
        "agentz_k2.py": "agentz_k2.py",
        "gooseR": "gooseR",
        "recipes/release-the-agents/recipe.yaml": "recipes/release-the-agents/recipe.yaml",
        "recipes/agentz-status/recipe.yaml": "recipes/agentz-status/recipe.yaml",
        "recipes/L1_candala_firewall/recipe.yaml": "recipes/L1_candala_firewall/recipe.yaml",
        "recipes/L2_sudra_explorer/recipe.yaml": "recipes/L2_sudra_explorer/recipe.yaml",
        "recipes/L3_vaisya_auditor/recipe.yaml": "recipes/L3_vaisya_auditor/recipe.yaml",
        "recipes/L4_ksatriya_executor/recipe.yaml": "recipes/L4_ksatriya_executor/recipe.yaml",
        "recipes/L5_brahmana_architect/recipe.yaml": "recipes/L5_brahmana_architect/recipe.yaml",
        "recipes/L6_sadhu_compressor/recipe.yaml": "recipes/L6_sadhu_compressor/recipe.yaml",
        "recipes/L7_rsi_constitution/recipe.yaml": "recipes/L7_rsi_constitution/recipe.yaml",
    }
)

LEGACY_RUNTIME_FILES = [
    "L1_TOM.md",
    "L2_TOM.md",
    "L3_TOM.md",
    "L4_TOM.md",
    "L5_TOM.md",
    "L6_TOM.md",
    "L7_TOM.md",
    "AGENT_ROUTER_V2.md",
]


def _legacy_notice(name: str) -> str:
    return f"""# {name} — compatibility notice

This Goose runtime file is a legacy TOM/router shard. It is kept only so older
Goose references do not resolve to stale doctrine.

Canonical runtime context is generated per prompt at:

`~/.config/goose/AGENTZ_ROUTED_TOM.md`

Canonical source files are:

- `~/.config/goose/ROSETTA_SOUL_LOOP.md`
- `~/.config/goose/DELEGATION_GRAMMAR.md`
- `~/.config/goose/SYSTEM_INSTRUCTIONS.md`
- `~/.config/goose/MY_SOUL.md`
- `~/.config/goose/TOM.md`
- `~/.config/goose/tom_router.py`

Runtime law:

1. The prompt is the Objective (`O`).
2. Goose first derives Strategies (`S`) and KPIs (`K`).
3. Strategy/KPI packets are delegated to routed Agentz castes.
4. Goose stops only when Mission is achieved or Mission conflicts with Vision.
5. K2 is REQUIRED for irreversible/public/external acts; it is never removed.

Do not use this file as source canon.
"""


def _read_canonical_deity(toml_path: Path, level: int) -> str:
    """Extract the canonical deity (operator) from the [meta] section."""
    if not toml_path.exists():
        return ""
    data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    return data.get("meta", {}).get("operator", "")


def _k2_status(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("k2_status:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def _file_label(name: str) -> str:
    if name.endswith(".toml") and name[:-5] in LEVELS:
        return name[:-5]
    return name


def _check(*, strict: bool = False) -> int:
    """Report drift without writing.

    Default is continuous runtime mode: drift is visible but does not stop
    Goose. Use strict=True for CI-style failure.
    """
    drift_count = 0
    print(f"=== Goose runtime sync check (canonical: {VMOSK_CONFIG.relative_to(PROJECT_ROOT)}) ===\n")

    if not GOOSE_DIR.exists():
        print(f"  Goose dir not found: {GOOSE_DIR}")
        print("  Skipping check — Goose is not installed or has not been initialized.")
        return 0

    for src_name, dst_name in RUNTIME_FILES.items():
        canon = VMOSK_CONFIG / src_name
        runtime = GOOSE_DIR / dst_name
        label = _file_label(dst_name)
        if not canon.exists():
            print(f"  ✗ {label}: canonical missing at {canon}")
            drift_count += 1
            continue
        if not runtime.exists():
            print(f"  ⚠ {label}: Goose runtime missing — would create from canonical")
            drift_count += 1
            continue
        if canon.read_bytes() == runtime.read_bytes():
            if label in LEVELS:
                deity = _read_canonical_deity(canon, 0)
                print(f"  ✓ {label}: in sync (operator={deity})")
            else:
                print(f"  ✓ {label}: in sync")
        else:
            if label in LEVELS:
                canon_deity = _read_canonical_deity(canon, 0)
                runtime_deity = _read_canonical_deity(runtime, 0)
                marker = "✗" if canon_deity != runtime_deity else "⚠"
                extra = ""
                if canon_deity != runtime_deity:
                    extra = f" [DOCTRINE DRIFT: canon={canon_deity}, runtime={runtime_deity}]"
                print(f"  {marker} {label}: drift{extra}")
            else:
                print(f"  ⚠ {label}: drift")
            drift_count += 1

    for name in LEGACY_RUNTIME_FILES:
        runtime = GOOSE_DIR / name
        expected = _legacy_notice(name).encode("utf-8")
        if not runtime.exists():
            print(f"  ⚠ {name}: legacy notice missing — would create compatibility stub")
            drift_count += 1
        elif runtime.read_bytes() == expected:
            print(f"  ✓ {name}: legacy notice in sync")
        else:
            print(f"  ⚠ {name}: stale legacy runtime shard — would replace with compatibility notice")
            drift_count += 1

    print()
    canon_k2 = _k2_status(VMOSK_CONFIG / "ROUTER_CONFIG.yaml")
    runtime_k2 = _k2_status(GOOSE_DIR / "ROUTER_CONFIG.yaml")
    if canon_k2 != "REQUIRED":
        print(f"  ✗ ROUTER_CONFIG.yaml: canonical k2_status is {canon_k2!r}, expected 'REQUIRED'")
        drift_count += 1
    elif runtime_k2 != "REQUIRED":
        print(f"  ✗ ROUTER_CONFIG.yaml: Goose k2_status is {runtime_k2!r}, expected 'REQUIRED'")
        drift_count += 1
    else:
        print("  ✓ K2 boundary: REQUIRED")

    print()
    if drift_count == 0:
        print("✓ Goose runtime is fully in sync with repo canonical Agentz doctrine.")
        return 0
    print(f"✗ {drift_count} drift items detected.")
    print("  Continuous mode: returning 0 so Goose keeps working.")
    print("  Next non-destructive repair: run `make goose-sync` to refresh the derived runtime.")
    if strict:
        print("  Strict mode requested: returning 1.")
        return 1
    return 0


def _apply() -> int:
    """Write canonical → Goose runtime. Exit 0 on success."""
    if not GOOSE_DIR.exists():
        print(f"Goose dir not found: {GOOSE_DIR}", file=sys.stderr)
        print("Goose is not installed or initialized. Skipping.", file=sys.stderr)
        return 0

    print(f"=== Applying canonical Agentz doctrine to Goose runtime ({GOOSE_DIR}) ===\n")

    for src_name, dst_name in RUNTIME_FILES.items():
        canon = VMOSK_CONFIG / src_name
        runtime = GOOSE_DIR / dst_name
        label = _file_label(dst_name)
        if not canon.exists():
            print(f"  ✗ {label}: canonical missing at {canon}")
            continue
        if runtime.exists() and canon.read_bytes() == runtime.read_bytes():
            print(f"  ✓ {label}: already in sync")
            continue
        runtime.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canon, runtime)
        if dst_name in {"gooseR", "agentz_status.py"}:
            runtime.chmod(0o755)
        if label in LEVELS:
            deity = _read_canonical_deity(canon, 0)
            print(f"  → {label}: synced (operator={deity})")
        else:
            print(f"  → {label}: synced")

    for name in LEGACY_RUNTIME_FILES:
        runtime = GOOSE_DIR / name
        expected = _legacy_notice(name)
        if runtime.exists() and runtime.read_text(encoding="utf-8") == expected:
            print(f"  ✓ {name}: legacy notice already in sync")
            continue
        runtime.write_text(expected, encoding="utf-8")
        print(f"  → {name}: replaced stale legacy shard with compatibility notice")

    print()
    print("✓ Goose runtime now reads canonical Agentz doctrine.")
    print("  K2 boundary is REQUIRED. Goose remains runtime, not source canon.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="Report drift without writing (default)")
    parser.add_argument("--apply", action="store_true", help="Write canonical → Goose runtime")
    parser.add_argument("--strict", action="store_true", help="With --check, exit 1 when drift is detected")
    args = parser.parse_args()
    if args.apply:
        return _apply()
    return _check(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())

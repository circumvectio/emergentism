#!/usr/bin/env python3
"""Generate Agentz lane deployment receipts for Emergentism folders."""

from __future__ import annotations

import argparse
import csv
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


DATE = "2026-06-04"
FILE_STAMP = DATE.replace("-", "_")
ORG_ROOT = Path("01_EMERGENTISM")
META_ROOT = ORG_ROOT / "00_META"
FIELDS = [
    "path",
    "kind",
    "zone",
    "mutability",
    "lead_agentz",
    "support_agentz",
    "agentz_passes",
    "status",
    "last_checked",
    "route",
    "receipt",
]

SKIP_PHYSICAL_DIR_NAMES = {
    ".git",
    ".next",
    ".pytest_cache",
    ".turbo",
    ".vercel",
    "__pycache__",
    "node_modules",
}


@dataclass(frozen=True)
class LaneConfig:
    lane: str
    title: str
    lead: str
    support: str
    zone: str
    mutability: str
    route: str
    status: str
    archive_status: str
    archive_route: str
    notes: tuple[str, ...]


LANES = {
    "08_FRAMEWORK_SUPPORT": LaneConfig(
        lane="08_FRAMEWORK_SUPPORT",
        title="08_FRAMEWORK_SUPPORT Agentz Deployment Receipt",
        lead="L5 Brahmana",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L4 Ksatriya; L6 Sadhu; L7 Rsi",
        zone="framework-support",
        mutability="active-support-library",
        route="Support library for governance, operators, evidence, synthesis, and agent grammar; source-owner lanes outrank it.",
        status="SUPPORT_LIBRARY_COVERED",
        archive_status="ARCHIVE_ONLY_COVERED",
        archive_route="Historical support-library memory; not current source authority unless owner-lane surfaces cite it.",
        notes=(
            "Legacy [T] markers remain in support material as bounded structural or technical aliases unless a source-owner document promotes them.",
            "Framework-support prose supports the seven source roots and must not silently replace them.",
        ),
    ),
    "09_TOOLS": LaneConfig(
        lane="09_TOOLS",
        title="09_TOOLS Agentz Deployment Receipt",
        lead="L5 Brahmana",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L4 Ksatriya; L6 Sadhu; L7 Rsi",
        zone="tools",
        mutability="active-tooling",
        route="Tooling layer for scripts, compilers, simulations, pipelines, deploy helpers, packages, agent ops, audit artifacts, and sprint gates.",
        status="TOOL_SURFACE_COVERED",
        archive_status="ARCHIVE_ONLY_COVERED",
        archive_route="Cold tooling memory; not the active command surface.",
        notes=(
            "Tool outputs are receipts or generated summaries, not doctrine authority.",
            "Runnable scripts require fresh command receipts before being cited as current runtime truth.",
        ),
    ),
    "11_UPLINK": LaneConfig(
        lane="11_UPLINK",
        title="11_UPLINK Agentz Deployment Receipt",
        lead="L4 Ksatriya",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L5 Brahmana; L6 Sadhu; L7 Rsi",
        zone="uplink",
        mutability="compressed-routing",
        route="Compressed routing and packet memory for agent orientation; owner-lane source files outrank summaries.",
        status="COMPRESSED_ROUTE_COVERED",
        archive_status="ARCHIVE_ONLY_COVERED",
        archive_route="Archived Uplink packet memory; not current routing authority.",
        notes=(
            "Session packets can preserve old [T] product targets; current public or build claims still require [B] receipts or [D]/[C] labels.",
            "Uplink should route readers down into source-owner folders before revising doctrine.",
        ),
    ),
    "12_PUBLIC_SITE": LaneConfig(
        lane="12_PUBLIC_SITE",
        title="12_PUBLIC_SITE Agentz Deployment Receipt",
        lead="L5 Brahmana",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L4 Ksatriya; L6 Sadhu; L7 Rsi",
        zone="public-site",
        mutability="source-preserved-frozen",
        route="Public narrative prototypes plus frozen book-pwa source pending AIA migration envelope completion.",
        status="PUBLIC_SITE_COVERED",
        archive_status="SOURCE_PRESERVED_COVERED",
        archive_route="Frozen app source for migration/tombstone/public-claim repair only; not a live product feature lane.",
        notes=(
            "Historical 10_PUBLIC_SITE strings are signature provenance only; 12_PUBLIC_SITE is the current physical path.",
            "No new book-pwa feature work belongs here while the 02_SKYZAI/02_AIA/app migration envelope is open.",
        ),
    ),
    "90_ARCHIVE": LaneConfig(
        lane="90_ARCHIVE",
        title="90_ARCHIVE Agentz Deployment Receipt",
        lead="L6 Sadhu",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L4 Ksatriya; L5 Brahmana; L7 Rsi",
        zone="archive",
        mutability="archive-only-provenance",
        route="Historical Emergentism archive; preserved under K3 and non-authoritative unless active owner lanes cite it.",
        status="ARCHIVE_ONLY_COVERED",
        archive_status="ARCHIVE_ONLY_COVERED",
        archive_route="Historical Emergentism archive; preserved under K3 and non-authoritative unless active owner lanes cite it.",
        notes=(
            "Former 999_ARCHIVE references are bounded by the 90_ARCHIVE front door and should not recreate the old folder.",
            "Archive files are preserved for provenance; repair only indexing, tombstones, or misleading route cards.",
        ),
    ),
    "91_COMPATIBILITY": LaneConfig(
        lane="91_COMPATIBILITY",
        title="91_COMPATIBILITY Agentz Deployment Receipt",
        lead="L6 Sadhu",
        support="L1 Candala; L2 Sudra; L3 Vaisya; L4 Ksatriya; L5 Brahmana; L7 Rsi",
        zone="compatibility",
        mutability="compatibility-only",
        route="Legacy path stubs and migration notes; redirects must not fork or revive doctrine.",
        status="COMPATIBILITY_STUB_COVERED",
        archive_status="ARCHIVE_ONLY_COVERED",
        archive_route="Historical compatibility evidence; not active doctrine.",
        notes=(
            "Compatibility paths preserve old references but are not source authority.",
            "Real repairs should happen in active owner lanes before compatibility stubs are updated.",
        ),
    ),
}


def git_visible_files(path: Path) -> set[str]:
    output = subprocess.check_output(
        ["git", "-c", "core.quotePath=false", "ls-files", "-co", "--exclude-standard", str(path)],
        text=True,
    )
    return set(output.splitlines())


def physical_folders(path: Path) -> set[str]:
    folders = {str(path)}
    for folder in path.rglob("*"):
        if not folder.is_dir():
            continue
        rel_parts = folder.relative_to(path).parts
        if any(part in SKIP_PHYSICAL_DIR_NAMES for part in rel_parts):
            continue
        folders.add(str(folder))
    return folders


def classify_kind(path: str, is_folder: bool) -> str:
    if is_folder:
        return "folder"
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    if name in {"AGENTS.md", "CLAUDE.md", "README.md", "ROUTE_CARD.md"}:
        return "markdown-front-door"
    if suffix == ".md":
        return "markdown-document"
    if suffix == ".py":
        return "python-script"
    if suffix in {".sh", ""}:
        return "executable-or-shell"
    if suffix in {".json", ".jsonl", ".yaml", ".yml", ".toml", ".csv", ".sql", ".prisma"}:
        return "structured-data-or-config"
    if suffix in {".html", ".css", ".js", ".ts", ".tsx", ".mjs"}:
        return "web-source"
    if suffix in {".png", ".svg", ".ico", ".pdf", ".docx", ".xlsx"}:
        return "asset-or-document"
    return "source-visible-file"


def row_for(config: LaneConfig, path: str, is_folder: bool) -> dict[str, str]:
    in_archive = "/90_ARCHIVE" in path or config.lane in {"90_ARCHIVE", "91_COMPATIBILITY"}
    in_public_app = config.lane == "12_PUBLIC_SITE" and "/book-pwa" in path
    kind = classify_kind(path, is_folder)
    route = config.archive_route if in_archive or in_public_app else config.route
    status = config.archive_status if in_archive or in_public_app else config.status
    mutability = "archive-only-provenance" if in_archive else config.mutability
    if in_public_app:
        mutability = "source-preserved-frozen"
    return {
        "path": path,
        "kind": kind,
        "zone": config.zone,
        "mutability": mutability,
        "lead_agentz": config.lead,
        "support_agentz": config.support,
        "agentz_passes": "L1+L2+L3+L4+L5+L6+L7",
        "status": status,
        "last_checked": DATE,
        "route": route,
        "receipt": f"03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.md",
    }


def generate_lane(config: LaneConfig) -> tuple[Path, Path, list[dict[str, str]], Counter[str], int, int]:
    lane_root = ORG_ROOT / config.lane
    if not lane_root.exists():
        raise FileNotFoundError(lane_root)

    files = git_visible_files(lane_root)
    folders = physical_folders(lane_root)
    rows = [row_for(config, path, True) for path in sorted(folders)]
    rows.extend(row_for(config, path, False) for path in sorted(files))

    csv_path = META_ROOT / f"03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv"
    md_path = META_ROOT / f"03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.md"

    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    suffix_counts = Counter(Path(f).suffix or "[no suffix]" for f in files)
    frontdoors = sum(1 for f in files if Path(f).name in {"AGENTS.md", "CLAUDE.md", "README.md", "ROUTE_CARD.md"})
    archive_rows = sum(1 for r in rows if "ARCHIVE" in r["status"] or r["mutability"].startswith("archive"))
    app_rows = sum(1 for r in rows if r["status"] == "SOURCE_PRESERVED_COVERED")

    notes = "\n".join(f"- {note}" for note in config.notes)
    suffix_table = "\n".join(
        f"| `{suffix}` | {count} |" for suffix, count in sorted(suffix_counts.items())
    )
    md_path.write_text(
        f"""---\nrosetta:\n  primary_level: {config.lead.split()[0]}\n  primary_column: Agentz Deployment Control\n  register: \"[B/I]\"\n  canonical_phrase: \"{config.title}\"\n---\n\n# {config.title}\n\n**Date:** {DATE}\n**Scope:** `01_EMERGENTISM_ORG/{config.lane}/`\n**Status:** Complete for source-visible folders and files in this lane.\n\nThis receipt records an Agentz L1-L7 deployment over `{config.lane}`. It is a\nrouting and control receipt, not a doctrine rewrite. Existing lane front doors\nremain the active route surfaces; this pass adds exact per-folder/per-file\ncoverage so future agents can see what has already been traversed.\n\n## Coverage\n\n| Surface | Count | Control |\n|---|---:|---|\n| Source-visible folders | {len(folders)} | Physical folders under this lane |\n| Source-visible files | {len(files)} | Git source-visible tracked/unignored files |\n| Deployment manifest rows | {len(rows)} | One row per folder and source-visible file |\n| Route-card/front-door files | {frontdoors} | `AGENTS.md`, `CLAUDE.md`, `README.md`, or route-card surfaces |\n| Archive/provenance rows | {archive_rows} | Bounded as non-authority |\n| Frozen app-source rows | {app_rows} | Source-preserved only, where applicable |\n\nManifest: [`03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv`](03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv)\n\n## File-Type Profile\n\n| Suffix | Count |\n|---|---:|\n{suffix_table}\n\n## Agentz Pass Order\n\n| Pass | Duty in this lane |\n|---|---|\n| L1 Candala | Detect contradictions, path drift, broken maps, and objective pressure. |\n| L2 Sudra | Check disclosure, public-safety, and candidate interpretations before strengthening claims. |\n| L3 Vaisya | Audit receipts, evidence tiers, route cards, links, and generated ledgers. |\n| L4 Ksatriya | Execute only bounded repairs and block irreversible moves without K2/owner route. |\n| L5 Brahmana | Preserve topology, owner boundaries, and source architecture. |\n| L6 Sadhu | Bound archives, compatibility shims, generated output, and overgrown summaries. |\n| L7 Rsi | Compress only source-confirmed truth into narrative or witness form. |\n\n## Lane Decisions\n\n{notes}\n- No broad file moves, deletions, or doctrine upgrades were performed by this receipt generator.\n- Any future rename or restructure should cite this manifest and then update the owning front door.\n\n## Verification Commands\n\n```bash\npython3 - <<'PY'\nfrom pathlib import Path\nimport csv, subprocess\nlane = '01_EMERGENTISM_ORG/{config.lane}'\nmanifest = Path('01_EMERGENTISM_ORG/00_META/03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv')\nrows = list(csv.DictReader(manifest.open()))\npaths = {{r['path'] for r in rows}}\nfiles = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', lane], text=True).splitlines())\nroot = Path(lane)\nfolders = {{str(root)}} | {{str(p) for p in root.rglob('*') if p.is_dir()}}\nactual = files | folders\nprint('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))\nif actual != paths or len(rows) != len(paths):\n    raise SystemExit(1)\nPY\ngit diff --check -- 01_EMERGENTISM_ORG/00_META/03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv 01_EMERGENTISM_ORG/00_META/03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.md\n```\n""",
        encoding="utf-8",
    )

    return csv_path, md_path, rows, suffix_counts, len(files), len(folders)


def verify_lane(config: LaneConfig) -> None:
    lane_root = ORG_ROOT / config.lane
    manifest = META_ROOT / f"03_AGENTZ_DEPLOYMENT_{config.lane}_{FILE_STAMP}.csv"
    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    paths = {r["path"] for r in rows}
    actual = git_visible_files(lane_root) | physical_folders(lane_root)
    blank = {
        field: sum(1 for row in rows if not row[field].strip())
        for field in FIELDS
    }
    print(
        config.lane,
        "rows",
        len(rows),
        "unique",
        len(paths),
        "actual",
        len(actual),
        "missing",
        len(actual - paths),
        "extra",
        len(paths - actual),
        "dupes",
        len(rows) - len(paths),
        "blank",
        sum(blank.values()),
    )
    if len(rows) != len(paths) or actual != paths or any(blank.values()):
        raise SystemExit(f"coverage verification failed for {config.lane}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lanes", nargs="*")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    lanes = args.lanes or sorted(LANES)
    unknown = sorted(set(lanes) - set(LANES))
    if unknown:
        raise SystemExit(
            f"unknown lane(s): {', '.join(unknown)}; choose from {', '.join(sorted(LANES))}"
        )

    for lane in lanes:
        config = LANES[lane]
        if args.verify:
            verify_lane(config)
        else:
            csv_path, md_path, rows, suffix_counts, file_count, folder_count = generate_lane(config)
            print(
                "wrote",
                csv_path,
                "and",
                md_path,
                "rows",
                len(rows),
                "files",
                file_count,
                "folders",
                folder_count,
                "suffixes",
                dict(sorted(suffix_counts.items())),
            )


if __name__ == "__main__":
    main()

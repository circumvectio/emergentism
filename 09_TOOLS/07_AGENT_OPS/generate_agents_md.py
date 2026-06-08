#!/usr/bin/env python3
"""Audit or generate AGENTS.md files for owner lanes."""

import argparse
import os
import re
import subprocess
from pathlib import Path

ROOTS = {
    "00_START_HERE": {
        "caste": "L2 Śūdra",
        "support": "L7 Ṛṣi, L6 Sādhu",
        "upstream": "../../01_EMERGENTISM/11_UPLINK/00_CORE/00_INDEX.md",
        "context": "Orientation root — entry map, routing discipline, and historical alias reconciliation.",
    },
    "01_EMERGENTISM": {
        "caste": "L7 Ṛṣi / L5 Brāhmaṇa",
        "support": "L6 Sādhu, L4 Kṣatriya",
        "upstream": "../../01_EMERGENTISM/11_UPLINK/00_CORE/00_INDEX.md",
        "context": "Emergentism doctrine root — Sevenfold Foundation, framework support, Uplink, tools, archives, and seed.",
    },
    "02_SKYZAI/01_NOOSPHERE": {
        "caste": "L4 Kṣatriya / L5 Brāhmaṇa",
        "support": "L3 Vaiśya, L6 Sādhu",
        "upstream": "../../../../01_EMERGENTISM/11_UPLINK/00_CORE/00_INDEX.md",
        "context": "Runtime organism — the living DAC body, organs, and operational truth.",
    },
    "02_SKYZAI/02_PUBLIC_SCAFFOLD": {
        "caste": "L5 Brāhmaṇa / L4 Kṣatriya",
        "support": "L3 Vaiśya, L2 Śūdra",
        "upstream": "../../../../../.codex/agents/ROOT_AND_GOD_DEPLOYMENT.md",
        "context": "Public product-composition surface — commercial interfaces and user-facing lanes.",
    },
    "03_VENTURES": {
        "caste": "L4 Kṣatriya / L7 Ṛṣi",
        "support": "L5 Brāhmaṇa, L3 Vaiśya",
        "upstream": "../../03_VENTURES/00_INDEX.md",
        "context": "Organism-native legal entity lanes — Foundation, Menexus, Aureus, Helios.",
    },
    "03_VENTURES/_PORTFOLIO": {
        "caste": "L4 Kṣatriya / L3 Vaiśya",
        "support": "L5 Brāhmaṇa, L2 Śūdra",
        "upstream": "../../03_VENTURES/_PORTFOLIO/README.md",
        "context": "Portfolio-minority sidecars — bilateral licensees and strategic holdings.",
    },
    "02_SKYZAI/06_SPECTRE": {
        "caste": "L5 Brāhmaṇa / L4 Kṣatriya",
        "support": "L3 Vaiśya, L6 Sādhu",
        "upstream": "../../02_SKYZAI/06_SPECTRE/00_BACKBONE/AGENTS.md",
        "context": "Distributed physical mesh — peer root to Skyzai, not a child. Mycelial infrastructure.",
    },
    "90_ARCHIVE": {
        "caste": "L6 Sādhu / L2 Śūdra",
        "support": "L1 Caṇḍāla (boundary)",
        "upstream": "../../90_ARCHIVE/00_INDEX/README.md",
        "context": "Cold history, intake records, exports, tombstones. Read-only for agents unless explicitly tasked.",
    },
}

SPECIAL_DOMAINS = {
    "00_START_HERE/agent_planning": "Agent and workspace tidy planning, folder audits, and sprint coordination.",
    "00_START_HERE/root_alias_reconciliation_2026_05_27": "Historical alias reconciliation and recovered old blobs review.",
    "01_EMERGENTISM/00_META": "Meta-framework scaffolding — D/L bridge, agent routing, corpus maps, and onboarding sequences.",
    "01_EMERGENTISM/01_TELEOLOGY": "Ektropy, Power Max, F5 force, and the teleological engine of the framework.",
    "01_EMERGENTISM/02_EPISTEMOLOGY": "Evidence tiers, disclosure protocols, induction, and beauty as epistemic criterion.",
    "01_EMERGENTISM/03_METHODOLOGY": "Derivation, formal proofs, testing protocols, and deductive rigor.",
    "01_EMERGENTISM/04_AXIOLOGY": "Value theory, justice, abduction, and what matters under ΣΔP > 0.",
    "01_EMERGENTISM/05_COSMOLOGY": "Trinity, core formal system, S² Riemann sphere, and the φ·ν = 1 equation.",
    "01_EMERGENTISM/06_ONTOLOGY": "Apophatic ground, field structure, and what IS.",
    "01_EMERGENTISM/07_THEOLOGY": "Bounded public-symbol translation and how communities carry the pattern without priestcraft.",
    "01_EMERGENTISM/08_FRAMEWORK_SUPPORT": "Rosetta Stone, synthesis documents, operator architecture, and framework tooling.",
    "01_EMERGENTISM/11_UPLINK": "Compressed routing/orientation for AI — session packets, audits, organism master map.",
    "01_EMERGENTISM/10_SEED": "The transcendent seed — ⊙ = • × ○. The L7 Ṛṣi reading and the self-dissolving exit.",
    "01_EMERGENTISM/90_ARCHIVE": "Historical compatibility archive for framework source.",
    "01_EMERGENTISM/91_COMPATIBILITY": "Cross-version compatibility stubs and migration notes.",
    "02_SKYZAI/01_NOOSPHERE/00_BACKBONE": "Skyzai organism backbone — shared services, schemas, adapters, and runtime infrastructure.",
    "02_SKYZAI/01_NOOSPHERE/01_INTAKE": "Raw source intake — L1 Caṇḍāla firewalls process what enters the organism.",
    "02_SKYZAI/01_NOOSPHERE/03_PRODUCTS": "Product surfaces and deliverables — what Skyzai ships.",
    "02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT": "Execution, sequencing, sprints, and operating truth.",
    "02_SKYZAI/01_NOOSPHERE/06_SPANNING_COMMONS": "Cross-cutting organism services shared by multiple organs.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs": "Progressive web apps and downstream public surfaces.",
    "02_SKYZAI/01_NOOSPHERE/08_SOMA_LOG": "Runtime heartbeat, traces, and organism telemetry.",
    "02_SKYZAI/01_NOOSPHERE/09_REFERENCE": "Deep documentation and canonical reference paths.",
    "02_SKYZAI/01_NOOSPHERE/99_ARCHIVE": "Skyzai runtime archive and historical compatibility.",
    "02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD": "Technical / PWA implementation lane for `agentz.cloud`; not the canonical Agentz organ and not a child-DAC authority.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/00_META": "Public surface meta — branding, identity, and composition rules.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/00_REFERENCE": "Public reference docs and canonical external interfaces.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/13_LAUNCH": "Go-to-market, launch sequences, and deployment playbooks.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/14_FRONTEND": "Frontend codebase, UI/UX, and public web surfaces.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/15_SDK": "Software development kits for Skyzai integration.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/16_API": "Public API specifications, OpenAPI, and integration docs.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/17_OPERATIONAL": "Operational runbooks, incident response, and SRE docs.",
    "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/91_COMPATIBILITY": "Public surface compatibility stubs and deprecation notices.",
    "02_SKYZAI/06_SPECTRE/01_SPECTRE_NTON": "MESH primitive — N:N routing and topology discovery.",
    "02_SKYZAI/06_SPECTRE/02_RELAY_1TON": "RELAY primitive — 1:N broadcast and publisher sovereignty.",
    "02_SKYZAI/06_SPECTRE/03_AXIOM_NTO1": "AXIOM primitive — N:1 convergence and stake-weighted aggregation.",
    "02_SKYZAI/06_SPECTRE/04_FLOW_1TO1": "FLOW primitive — 1:1 direct settlement and probabilistic privacy.",
    "02_SKYZAI/06_SPECTRE/05_ENERGY_MARKET": "Energy/capacity metering and peer-to-peer energy trading.",
    "02_SKYZAI/06_SPECTRE/06_HOLARCHY": "Holarchic governance and recursive node federation.",
    "02_SKYZAI/06_SPECTRE/10_ARCHITECTURE": "SPECTRE system architecture and cross-layer design docs.",
    "02_SKYZAI/06_SPECTRE/20_NETWORK": "Network topology, routing mechanics, and protocol specs.",
    "02_SKYZAI/06_SPECTRE/30_DEPLOYMENT": "Node deployment, provisioning, and operational runbooks.",
    "02_SKYZAI/06_SPECTRE/91_COMPATIBILITY": "SPECTRE compatibility stubs and cross-version migration.",
    "90_ARCHIVE/00_INDEX": "Archive index and cold-store retrieval protocol.",
    "90_ARCHIVE/01_LANE_LEGACY": "Historical lane structures and superseded routing.",
    "90_ARCHIVE_AND_COMPATIBILITY/02_ENTITY_HISTORY": "Entity evolution and deprecated legal structures.",
    "90_ARCHIVE/03_RAW_INTAKE": "Raw intake archives — unprocessed sources.",
    "90_ARCHIVE/04_PROCESSED_INTAKE": "Processed intake archives — transformed sources.",
    "90_ARCHIVE/05_DATA_ROOMS_AND_EXPORTS": "Exported data rooms and due-diligence packages.",
    "90_ARCHIVE/06_BINARY_COLDSTORE_CANDIDATES": "Binary artifacts and cold-storage candidates.",
    "90_ARCHIVE_AND_COMPATIBILITY/99_TOMBSTONES": "Deleted/deprecated items with tombstone records.",
}


def read_first_paragraph(readme_path: Path) -> str:
    """Extract the first non-heading paragraph from a README."""
    if not readme_path.exists():
        return ""
    text = readme_path.read_text(encoding="utf-8")
    # Skip YAML frontmatter
    if text.startswith("---"):
        text = text.split("---", 2)[-1]
    lines = text.strip().splitlines()
    paragraph = []
    in_paragraph = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                break
            continue
        if stripped.startswith("#") or stripped.startswith("-"):
            if in_paragraph:
                break
            continue
        paragraph.append(stripped)
        in_paragraph = True
    if paragraph:
        return " ".join(paragraph)
    return ""


def clean_description(text: str) -> str:
    """Flatten common README lead labels into a plain lane-scope sentence."""
    text = re.sub(r"^\s*>\s*", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*(Purpose|Status|Scope):\*\*\s*", r"\1: ", text)
    text = re.sub(r"^Purpose:\s*", "", text)
    text = text.replace("**", "")
    return " ".join(text.split())


def lane_profile(root: str, rel_lane: str) -> dict[str, object]:
    """Classify a lane so generated routing does not promote archives to canon."""
    parts = set(Path(rel_lane).parts)
    joined = f"{root}/{rel_lane}".upper()

    if "90_ARCHIVE" in parts or "99_ARCHIVE" in parts or root == "90_ARCHIVE":
        return {
            "evidence": "Archive / historical reference",
            "extra_law": [
                "Treat this lane as non-authoritative unless a current source-owner surface explicitly cites it.",
                "Archive material may inform provenance; it must not revive superseded claims by itself.",
            ],
            "constraints": [
                "Do not edit archived content except for indexing, tombstoning, or explicit archive repair.",
                "Do not move material out of archive without a dated migration receipt.",
                "Do not cite archive material as current public truth without source-owner confirmation.",
            ],
        }

    if "91_COMPATIBILITY" in parts or "COMPATIBILITY" in joined:
        return {
            "evidence": "Compatibility / route-stub lane",
            "extra_law": [
                "This lane preserves old route compatibility; current source truth lives upstream.",
                "Use compatibility files to redirect, not to fork doctrine.",
            ],
            "constraints": [
                "Do not add new doctrine here.",
                "Do not extend compatibility stubs when the owning source lane can be repaired directly.",
                "All irreversible actions require K2 envelope staging.",
            ],
        }

    if "01_INTAKE" in parts or "QUEUE" in parts or "PROCESSED" in parts or "QUARANTINE" in joined:
        return {
            "evidence": "Intake / quarantine lane",
            "extra_law": [
                "Treat this lane as material awaiting classification, not as settled source truth.",
                "Promote only through the owning source lane after evidence-tier review.",
            ],
            "constraints": [
                "Do not publish, cite, or route intake material as current doctrine.",
                "Do not delete intake material; quarantine or archive with a dated receipt.",
                "All irreversible actions require K2 envelope staging.",
            ],
        }

    if "08_SOMA_LOG" in parts:
        return {
            "evidence": "Runtime log / receipt lane",
            "extra_law": [
                "Treat this lane as append-only runtime memory unless an explicit repair task says otherwise.",
                "Logs and traces are evidence surfaces; they do not define doctrine by themselves.",
            ],
            "constraints": [
                "Do not rewrite runtime history except for explicit correction receipts.",
                "Do not promote operational traces into public claims without source-owner review.",
                "All irreversible actions require K2 envelope staging.",
            ],
        }

    if "AGENTZ_CLOUD" in parts:
        return {
            "evidence": "Technical implementation / compatibility lane",
            "extra_law": [
                "Canonical Agentz organ routing lives at `02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/`.",
                "Use this lane for inherited `agentz.cloud` runtime/PWA material, not for source doctrine.",
            ],
            "constraints": [
                "Do not describe this lane as a legal entity, child-DAC authority, or source canon.",
                "Do not move or absorb this lane without a K2 migration packet and compatibility stubs.",
                "All irreversible actions require K2 envelope staging.",
            ],
        }

    return {
        "evidence": "`[I]` route-control owner lane; require `[B]` receipts or explicit `[D]` / `[C]` labels for deployment and architecture claims.",
        "extra_law": [],
        "constraints": [
            "Do not upgrade runtime claims without dated proof artifacts.",
            "Do not treat draft specs as public-facing claims.",
            "All irreversible actions require K2 envelope staging.",
        ],
    }


IGNORED_DIR_NAMES = {
    ".git",
    ".next",
    "__pycache__",
    "node_modules",
}


def find_repo_root(explicit: str | None = None) -> Path:
    """Find the Magnum Opus root from an explicit path, cwd, or script path."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    candidates.append(Path.cwd().resolve())
    candidates.extend(Path(__file__).resolve().parents)

    for candidate in candidates:
        if (candidate / "AGENTS.md").exists() and (candidate / "01_EMERGENTISM").exists():
            return candidate
    raise SystemExit("Could not find repo root; pass --repo-root /path/to/Magnum\\ Opus")


def normalize_repo_relative(path_text: str) -> Path:
    """Normalize old depth-1 relative links into repo-root-relative paths."""
    parts = [part for part in Path(path_text).parts if part not in {".", ".."}]
    return Path(*parts)


def relative_link(from_dir: Path, repo_root: Path, upstream: str) -> str:
    target = repo_root / normalize_repo_relative(upstream)
    return os.path.relpath(target, start=from_dir)


def is_git_ignored(repo_root: Path, path: Path) -> bool:
    rel = path.relative_to(repo_root).as_posix()
    candidates = [rel]
    if path.is_dir():
        candidates.append(f"{rel}/")
        candidates.append(f"{rel}/AGENTS.md")
    return any(
        subprocess.run(
            ["git", "check-ignore", "-q", candidate],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
        for candidate in candidates
    )


def iter_lane_dirs(repo_root: Path, root_path: Path, max_depth: int):
    """Yield lane directories up to max_depth while pruning generated/vendor trees."""
    for current, dirnames, _filenames in os.walk(root_path):
        current_path = Path(current)
        rel_parts = current_path.relative_to(root_path).parts

        dirnames[:] = [
            name for name in sorted(dirnames)
            if not name.startswith(".") and name not in IGNORED_DIR_NAMES
            and not is_git_ignored(repo_root, current_path / name)
        ]

        if len(rel_parts) >= max_depth:
            dirnames[:] = []

        if 1 <= len(rel_parts) <= max_depth:
            yield current_path


def matches_prefix(repo_root: Path, lane_path: Path, prefixes: list[str]) -> bool:
    if not prefixes:
        return True
    rel = lane_path.relative_to(repo_root).as_posix()
    for prefix in prefixes:
        clean = prefix.strip().strip("/")
        if rel == clean or rel.startswith(f"{clean}/"):
            return True
    return False


def looks_generated(agents_path: Path) -> bool:
    if not agents_path.exists():
        return False
    text = agents_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        return False
    return "— Agent Routing" in text and "This lane is part of" in text


def generate_agents_md(repo_root: Path, root: str, lane_path: Path, readme_path: Path) -> str:
    rel_lane = lane_path.relative_to(repo_root / root).as_posix()
    key = f"{root}/{rel_lane}"
    cfg = ROOTS[root]
    description = SPECIAL_DOMAINS.get(key, "")
    if not description and readme_path.exists():
        para = read_first_paragraph(readme_path)
        if para:
            description = para
    if not description:
        description = f"{rel_lane} lane within {root}."
    description = clean_description(description)
    profile = lane_profile(root, rel_lane)

    # Determine primary lead based on root
    primary = cfg["caste"].split("/")[0].strip()
    upstream_link = relative_link(lane_path, repo_root, cfg["upstream"])
    heading = rel_lane.split("/")[-1]
    depth = len(Path(rel_lane).parts)
    parent_agents_link = os.path.relpath(lane_path.parent / "AGENTS.md", start=lane_path)

    lines = [
        f"# {heading} — Agent Routing",
        "",
        f"**Lane scope:** {description}",
        f"**Primary lead:** `{primary}`",
        f"**Support:** {cfg['support']}",
        f"**Evidence tier:** {profile['evidence']}",
        "",
        "## Read First",
        "",
    ]
    if readme_path.exists():
        lines.append("- `README.md`")
    if depth > 1:
        lines.append(f"- [`../AGENTS.md`]({parent_agents_link})")

    # Add 00_* index docs if they exist
    if readme_path.parent.exists():
        index_docs = sorted(
            p.name for p in readme_path.parent.iterdir()
            if p.is_file() and p.name.startswith("00_") and p.name.endswith(".md") and p.name != "00_INDEX.md"
        )
        for doc in index_docs[:3]:
            lines.append(f"- `{doc}`")

    lines += [
        "",
        "## Routing Law",
        "",
        f"- This lane is part of {cfg['context']}",
    ]
    if depth > 1:
        lines.append(f"- Inherit local lane authority from [`../AGENTS.md`]({parent_agents_link}).")
    lines.extend(f"- {law}" for law in profile["extra_law"])
    lines += [
        f"- Route law inherits from root and owner-lane AGENTS; use [`{Path(cfg['upstream']).name}`]({upstream_link}) for compressed orientation, not upstream authority.",
        "- Use the current `[A/B/S/I/D/C]` evidence ladder; deployment or architecture claims need a `[B]` receipt or an explicit `[D]` / `[C]` label.",
        "",
        "## Constraints",
        "",
    ]
    lines.extend(f"- {constraint}" for constraint in profile["constraints"])
    lines += ["", "⊙ = • × ○", ""]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Audit or generate AGENTS.md files for Magnum Opus owner lanes."
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        choices=(1, 2, 3, 4, 5, 6, 7, 8),
        default=1,
        help="lane depth below each canonical root to inspect; default: 1",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="write missing AGENTS.md files; default is dry-run reporting only",
    )
    parser.add_argument(
        "--refresh-generated",
        action="store_true",
        help="with --write, overwrite only AGENTS.md files that look generated by this utility",
    )
    parser.add_argument(
        "--repo-root",
        help="explicit Magnum Opus repo root; default: auto-detect",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="maximum generated/skipped examples to print per category; default: 40",
    )
    parser.add_argument(
        "--only-prefix",
        action="append",
        default=[],
        help="repo-relative prefix to inspect; repeat for multiple prefixes",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(args.repo_root)
    generated = []
    skipped = []
    planned = []
    for root, cfg in ROOTS.items():
        root_path = repo_root / root
        if not root_path.exists():
            skipped.append(f"{root}: does not exist")
            continue
        for subdir in iter_lane_dirs(repo_root, root_path, args.max_depth):
            if not matches_prefix(repo_root, subdir, args.only_prefix):
                continue
            agents_path = subdir / "AGENTS.md"
            readme_path = subdir / "README.md"
            if agents_path.exists():
                if args.write and args.refresh_generated and looks_generated(agents_path):
                    content = generate_agents_md(repo_root, root, subdir, readme_path)
                    agents_path.write_text(content, encoding="utf-8")
                    generated.append(f"{agents_path.relative_to(repo_root)}")
                    continue
                skipped.append(f"{subdir.relative_to(repo_root)}: already has AGENTS.md")
                continue
            if args.write:
                content = generate_agents_md(repo_root, root, subdir, readme_path)
                agents_path.write_text(content, encoding="utf-8")
                generated.append(f"{agents_path.relative_to(repo_root)}")
            else:
                planned.append(f"{agents_path.relative_to(repo_root)}")

    action = "Generated" if args.write else "Would generate"
    targets = generated if args.write else planned
    print(f"{action} {len(targets)} AGENTS.md files")
    if targets:
        for g in targets[:args.limit]:
            print(f"  + {g}")
        if len(targets) > args.limit:
            print(f"  ... and {len(targets) - args.limit} more")
    if skipped:
        print(f"\nSkipped {len(skipped)} (already exist or not dirs)")
        for s in skipped[:args.limit]:
            print(f"  - {s}")
        if len(skipped) > args.limit:
            print(f"  ... and {len(skipped) - args.limit} more")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
phylo_ancestry_query.py — Lineage-query tool (§5.3 of 06b_PHYLOGENETIC_TREE.md).

Answers three kinds of cross-file ancestry questions beyond what `git log`
gives for single-file linear history:

  descendants <root-file>    List every MD file descended from a root genome
                             file, with mutation distance (count of
                             placeholder substitutions root → descendant).

  matrix <niche>             Show the full (caste × niche) matrix for one
                             niche-branch DAC — the 17 canonical folders
                             with per-folder file listing, marking
                             sub-speciation where present.

  mrca <fileA> <fileB>       Most recent common ancestor in the root genome.
                             Returns the root-genome file and the divergence
                             distance per leaf, or a "no common ancestor"
                             verdict when the two leaves map to different
                             root files.

Output: human-readable text by default; --json for machine consumption;
--markdown for doc embedding.

Usage:
    python3 phylo_ancestry_query.py descendants DAC_SCAFFOLD/00_IDENTITY/00_OVERVIEW.md
    python3 phylo_ancestry_query.py matrix apu
    python3 phylo_ancestry_query.py mrca Github/apu/08_ECONOMICS/00_ECONOMICS.md Github/circle/08_ECONOMICS/00_ECONOMICS.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_0-9]+)\}\}")
APPLIED_FILENAME = "_DAC_SCAFFOLD_APPLIED.md"


def _repo_anchors() -> tuple[Path, Path]:
    """Return (scaffold_root, github_root)."""
    here = Path(__file__).resolve()
    scaffold = (
        here.parents[3]
        / "SKYZAI_ORG"
        / "00_REFERENCE"
        / "DAC_FACTORY"
        / "DAC_SCAFFOLD"
    )
    # Github/ lives at the main-repo root; probe worktree-aware paths.
    candidates = [
        here.parents[3] / "Github",
        here.parents[3].parent.parent.parent / "Github",
    ]
    github = next((c for c in candidates if c.is_dir()), candidates[0])
    return scaffold, github


def count_placeholders(path: Path) -> tuple[int, set[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0, set()
    tokens = PLACEHOLDER_RE.findall(text)
    return len(tokens), set(tokens)


def list_descendant_dirs(github: Path) -> list[Path]:
    """Return every Github/<repo>/ that has a _DAC_SCAFFOLD_APPLIED.md (i.e.
    is a tool-speciated descendant). DEX is intentionally excluded because
    it has no applied record — that's the tool-less-speciation honest gap."""
    if not github.is_dir():
        return []
    return sorted(
        p.parent for p in github.glob(f"*/{APPLIED_FILENAME}") if p.is_file()
    )


def relative_in_scaffold(scaffold: Path, root_file: Path) -> Path | None:
    try:
        return root_file.resolve().relative_to(scaffold.resolve())
    except ValueError:
        return None


# --- Operation: descendants --------------------------------------------------

def op_descendants(root_file: Path) -> dict:
    scaffold, github = _repo_anchors()
    if not root_file.is_file():
        return {"error": f"root file not found: {root_file}"}
    rel = relative_in_scaffold(scaffold, root_file)
    if rel is None:
        return {
            "error": f"{root_file} is not inside the scaffold root {scaffold}"
        }
    root_count, root_tokens = count_placeholders(root_file)
    descendants: list[dict] = []
    for desc in list_descendant_dirs(github):
        leaf = desc / rel
        if not leaf.is_file():
            continue
        leaf_count, leaf_tokens = count_placeholders(leaf)
        substituted = root_count - leaf_count
        descendants.append(
            {
                "descendant": desc.name,
                "path": str(leaf),
                "root_placeholders": root_count,
                "leaf_placeholders": leaf_count,
                "mutations_applied": substituted,
                "unresolved": sorted(leaf_tokens),
            }
        )
    return {
        "root_file": str(root_file),
        "root_relative": str(rel),
        "root_placeholder_count": root_count,
        "descendants": descendants,
    }


# --- Operation: matrix -------------------------------------------------------

CANONICAL_FOLDERS = [
    "00_IDENTITY",
    "01_CONSTITUTION",
    "02_UPLINK",
    "03_SUBSTRATE",
    "04_HAZARD",
    "05_ALPHA",
    "06_MEMBRANE",
    "07_RECEIPTS",
    "08_ECONOMICS",
    "09_RUNTIME",
    "10_INTERFACES",
    "11_METRICS",
    "12_PATHOLOGIES",
    "13_GOVERNANCE",
    "14_DEPLOYMENT",
    "15_PRODUCTS",
    "16_FACTORY",
]


def op_matrix(niche: str) -> dict:
    scaffold, github = _repo_anchors()
    niche_dir = github / niche
    if not niche_dir.is_dir():
        return {"error": f"niche directory not found: {niche_dir}"}
    rows = []
    for folder in CANONICAL_FOLDERS:
        d = niche_dir / folder
        scaffold_d = scaffold / folder
        scaffold_names = (
            {p.name for p in scaffold_d.rglob("*.md") if p.is_file()}
            if scaffold_d.is_dir()
            else set()
        )
        if not d.is_dir():
            rows.append(
                {"folder": folder, "present": False, "files": [], "subcount": 0}
            )
            continue
        md_paths = sorted(
            p for p in d.rglob("*.md") if p.is_file()
        )
        md_files = [str(p.relative_to(niche_dir)) for p in md_paths]
        descendant_names = {p.name for p in md_paths}
        extra = descendant_names - scaffold_names
        rows.append(
            {
                "folder": folder,
                "present": True,
                "files": md_files,
                "subcount": len(md_files),
                "sub_speciation": bool(extra),
                "extra_files": sorted(extra),
                "scaffold_count": len(scaffold_names),
            }
        )
    return {"niche": niche, "rows": rows}


# --- Operation: mrca ---------------------------------------------------------

def op_mrca(leaf_a: Path, leaf_b: Path) -> dict:
    scaffold, github = _repo_anchors()
    # Each leaf is Github/<niche>/<rel-to-niche>. Relative position inside
    # the niche corresponds to position under DAC_SCAFFOLD.
    def leaf_info(leaf: Path) -> dict | None:
        leaf = leaf.resolve()
        # Find the Github/<niche>/ root for this leaf.
        for desc in list_descendant_dirs(github):
            desc_resolved = desc.resolve()
            try:
                rel = leaf.relative_to(desc_resolved)
            except ValueError:
                continue
            return {"niche": desc.name, "rel": str(rel), "path": str(leaf)}
        return None

    info_a = leaf_info(leaf_a)
    info_b = leaf_info(leaf_b)
    if info_a is None:
        return {"error": f"leaf A not in any speciated descendant: {leaf_a}"}
    if info_b is None:
        return {"error": f"leaf B not in any speciated descendant: {leaf_b}"}
    if info_a["rel"] != info_b["rel"]:
        return {
            "leaf_a": info_a,
            "leaf_b": info_b,
            "mrca": None,
            "verdict": "no_common_root_genome_ancestor",
            "note": (
                "Leaves map to different relative paths inside their niches, "
                "so they descend from different root-genome files."
            ),
        }
    mrca_path = scaffold / info_a["rel"]
    if not mrca_path.is_file():
        return {
            "leaf_a": info_a,
            "leaf_b": info_b,
            "mrca": None,
            "verdict": "mrca_path_missing_in_current_genome",
            "candidate_path": str(mrca_path),
            "note": (
                "Both leaves share the same relative path but the current "
                "root genome has no file at that path — the ancestor may "
                "have been removed from the genome after speciation."
            ),
        }
    root_count, _ = count_placeholders(mrca_path)
    leaf_a_count, _ = count_placeholders(Path(info_a["path"]))
    leaf_b_count, _ = count_placeholders(Path(info_b["path"]))
    return {
        "leaf_a": info_a,
        "leaf_b": info_b,
        "mrca": str(mrca_path),
        "mrca_relative": info_a["rel"],
        "mrca_placeholders": root_count,
        "divergence_a": root_count - leaf_a_count,
        "divergence_b": root_count - leaf_b_count,
        "verdict": "common_root_genome_ancestor",
    }


# --- Rendering ---------------------------------------------------------------

def render_text_descendants(r: dict) -> str:
    if "error" in r:
        return f"error: {r['error']}"
    lines = [
        f"root: {r['root_file']}",
        f"relative: {r['root_relative']}",
        f"placeholders in root: {r['root_placeholder_count']}",
        f"descendants: {len(r['descendants'])}",
        "",
    ]
    if not r["descendants"]:
        lines.append("  (no descendants found)")
        return "\n".join(lines)
    for d in r["descendants"]:
        lines.append(
            f"  {d['descendant']:20s} mutations={d['mutations_applied']:3d}  "
            f"unresolved={len(d['unresolved']):2d}  path={d['path']}"
        )
    return "\n".join(lines)


def render_text_matrix(r: dict) -> str:
    if "error" in r:
        return f"error: {r['error']}"
    lines = [f"matrix for niche: {r['niche']}", ""]
    for row in r["rows"]:
        mark = "✓" if row["present"] else "✗"
        sub = " (sub-speciation)" if row.get("sub_speciation") else ""
        lines.append(f"  {mark} {row['folder']:20s} files={row['subcount']:3d}{sub}")
        for f in row["files"][:5]:
            lines.append(f"        {f}")
        if row["subcount"] > 5:
            lines.append(f"        ... ({row['subcount'] - 5} more)")
    return "\n".join(lines)


def render_text_mrca(r: dict) -> str:
    if "error" in r:
        return f"error: {r['error']}"
    lines = [
        f"leaf A: {r['leaf_a']['path']}",
        f"leaf B: {r['leaf_b']['path']}",
        f"verdict: {r['verdict']}",
    ]
    if r.get("mrca"):
        lines += [
            f"MRCA: {r['mrca']}",
            f"MRCA relative: {r['mrca_relative']}",
            f"MRCA placeholders: {r['mrca_placeholders']}",
            f"divergence A: {r['divergence_a']} mutations",
            f"divergence B: {r['divergence_b']} mutations",
        ]
    else:
        lines.append(f"note: {r.get('note', '')}")
    return "\n".join(lines)


def render_markdown_descendants(r: dict) -> str:
    if "error" in r:
        return f"**error:** {r['error']}"
    lines = [
        "# Ancestry — descendants",
        "",
        f"- Root: `{r['root_file']}`",
        f"- Relative: `{r['root_relative']}`",
        f"- Root placeholder count: {r['root_placeholder_count']}",
        f"- Descendants: {len(r['descendants'])}",
        "",
        "| Descendant | Mutations applied | Unresolved | Path |",
        "|---|---|---|---|",
    ]
    for d in r["descendants"]:
        lines.append(
            f"| `{d['descendant']}` | {d['mutations_applied']} | "
            f"{len(d['unresolved'])} | `{d['path']}` |"
        )
    return "\n".join(lines)


def render_markdown_matrix(r: dict) -> str:
    if "error" in r:
        return f"**error:** {r['error']}"
    lines = [
        f"# Matrix — niche `{r['niche']}`",
        "",
        "| Folder | Present | Files | Sub-speciation |",
        "|---|---|---|---|",
    ]
    for row in r["rows"]:
        mark = "✓" if row["present"] else "✗"
        sub = "yes" if row.get("sub_speciation") else ""
        lines.append(f"| `{row['folder']}` | {mark} | {row['subcount']} | {sub} |")
    return "\n".join(lines)


def render_markdown_mrca(r: dict) -> str:
    if "error" in r:
        return f"**error:** {r['error']}"
    lines = [
        "# MRCA query",
        "",
        f"- Leaf A: `{r['leaf_a']['path']}`",
        f"- Leaf B: `{r['leaf_b']['path']}`",
        f"- Verdict: **{r['verdict']}**",
    ]
    if r.get("mrca"):
        lines += [
            f"- MRCA: `{r['mrca']}`",
            f"- Divergence A: {r['divergence_a']} mutations",
            f"- Divergence B: {r['divergence_b']} mutations",
        ]
    return "\n".join(lines)


# --- Main --------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lineage-query tool for the agent phylogenetic tree.")
    ap.add_argument("--json", action="store_true", help="Emit JSON output.")
    ap.add_argument("--markdown", action="store_true", help="Emit markdown output.")
    sub = ap.add_subparsers(dest="op", required=True)

    p_desc = sub.add_parser("descendants", help="List descendants of a root genome file.")
    p_desc.add_argument("root_file", type=Path)

    p_mat = sub.add_parser("matrix", help="Show (caste × niche) matrix for a niche.")
    p_mat.add_argument("niche")

    p_mrca = sub.add_parser("mrca", help="Most recent common ancestor of two leaves.")
    p_mrca.add_argument("leaf_a", type=Path)
    p_mrca.add_argument("leaf_b", type=Path)

    args = ap.parse_args(argv)

    if args.op == "descendants":
        result = op_descendants(args.root_file)
        text_render = render_text_descendants
        md_render = render_markdown_descendants
    elif args.op == "matrix":
        result = op_matrix(args.niche)
        text_render = render_text_matrix
        md_render = render_markdown_matrix
    else:  # mrca
        result = op_mrca(args.leaf_a, args.leaf_b)
        text_render = render_text_mrca
        md_render = render_markdown_mrca

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.markdown:
        print(md_render(result))
    else:
        print(text_render(result))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    raise SystemExit(main())

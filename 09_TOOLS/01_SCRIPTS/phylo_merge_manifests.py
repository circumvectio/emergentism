#!/usr/bin/env python3
"""
phylo_merge_manifests.py — Merge operator for hyperagents (§5.4 of 06b_PHYLOGENETIC_TREE.md).

Composes two or more parent manifests into a single merged manifest that can
be consumed by the standard speciation operator (apply_dac_scaffold.py).

Accepts a merge manifest that specifies collision-resolution rules:

    {
      "name": "hyperagent-name",
      "precedence": ["parent_a.json", "parent_b.json"],
      "explicit_overrides": {
        "DAC_NAME": "HYPER-X",
        "NICHE": "cross-domain-synthesis"
      },
      "llm_council_keys": ["DISPUTED_HAZARD", "DISPUTED_ALPHA"]
    }

Collision resolution order:
  1. If all parents agree, use the agreed value.
  2. If key is in `explicit_overrides`, use the override.
  3. If key is in `llm_council_keys`, emit a sentinel value
     {{LLM_COUNCIL_PENDING:<KEY>}} — requires external council run.
  4. Otherwise, use the parent that appears first in `precedence`.

Emits:
  - `<out>` — the merged manifest JSON.
  - `<out>.MERGE_MANIFEST.md` — human-readable record of parentage,
    collisions, and resolutions.

DAG acyclicity: enforced by refusing to merge if `<out>` path equals any
parent path. Transitive cycles are prevented by the same rule applied at
each merge level (tool is stateless; chain discipline is git-enforced).

Usage:
    python3 phylo_merge_manifests.py \\
        --parent 05_TOOLS/scripts/dac_scaffold_manifests/apu.json \\
        --parent 05_TOOLS/scripts/dac_scaffold_manifests/circle.json \\
        --merge  merge_apu_circle.json \\
        --out    05_TOOLS/scripts/dac_scaffold_manifests/apu_circle_hyper.json

Exit codes:
  0 — merge successful (possibly with LLM_COUNCIL_PENDING sentinels)
  1 — unresolvable collision (no rule matched)
  2 — input error (missing file, cycle, bad merge manifest)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


LLM_COUNCIL_SENTINEL = "{{LLM_COUNCIL_PENDING:{key}}}"


def load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: manifest not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"error: bad JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def normalize_key(k: str) -> str:
    return k.upper()


def merge(parents: list[tuple[Path, dict]], merge_spec: dict) -> tuple[dict, list[dict]]:
    """Return (merged_manifest, collisions_report)."""
    precedence = [normalize_key(p) for p in merge_spec.get("precedence", [])]
    explicit = {
        normalize_key(k): v for k, v in merge_spec.get("explicit_overrides", {}).items()
    }
    council_keys = {normalize_key(k) for k in merge_spec.get("llm_council_keys", [])}

    # Build parent_name → manifest lookup.
    parent_by_name: dict[str, dict] = {}
    for path, m in parents:
        name = normalize_key(path.name)
        parent_by_name[name] = m

    # Union of all keys.
    all_keys: set[str] = set()
    for _, m in parents:
        all_keys.update(normalize_key(k) for k in m.keys())

    merged: dict = {}
    collisions: list[dict] = []

    for key in sorted(all_keys):
        values_by_parent: dict[str, object] = {}
        for path, m in parents:
            # Tolerate both uppercase and mixed-case keys in inputs.
            for k, v in m.items():
                if normalize_key(k) == key:
                    values_by_parent[path.name] = v
                    break

        # Only one parent has the key.
        if len(values_by_parent) == 1:
            merged[key] = next(iter(values_by_parent.values()))
            continue

        # All agree.
        unique_values = {json.dumps(v, sort_keys=True, ensure_ascii=False) for v in values_by_parent.values()}
        if len(unique_values) == 1:
            merged[key] = next(iter(values_by_parent.values()))
            continue

        # Disagreement — resolve.
        if key in explicit:
            merged[key] = explicit[key]
            collisions.append(
                {
                    "key": key,
                    "resolution": "explicit_override",
                    "chosen_value": explicit[key],
                    "parent_values": values_by_parent,
                }
            )
            continue

        if key in council_keys:
            merged[key] = LLM_COUNCIL_SENTINEL.format(key=key)
            collisions.append(
                {
                    "key": key,
                    "resolution": "llm_council_pending",
                    "chosen_value": merged[key],
                    "parent_values": values_by_parent,
                }
            )
            continue

        if precedence:
            chosen_parent = None
            for pref in precedence:
                if pref in {normalize_key(name) for name in values_by_parent}:
                    for name in values_by_parent:
                        if normalize_key(name) == pref:
                            chosen_parent = name
                            break
                    break
            if chosen_parent is not None:
                merged[key] = values_by_parent[chosen_parent]
                collisions.append(
                    {
                        "key": key,
                        "resolution": "precedence",
                        "chosen_parent": chosen_parent,
                        "chosen_value": merged[key],
                        "parent_values": values_by_parent,
                    }
                )
                continue

        # Unresolvable.
        collisions.append(
            {
                "key": key,
                "resolution": "UNRESOLVED",
                "parent_values": values_by_parent,
            }
        )
    return merged, collisions


def render_record(
    parents: list[tuple[Path, dict]],
    merge_spec_path: Path,
    merged_path: Path,
    collisions: list[dict],
) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    unresolved = [c for c in collisions if c["resolution"] == "UNRESOLVED"]
    council = [c for c in collisions if c["resolution"] == "llm_council_pending"]
    precedence_resolved = [c for c in collisions if c["resolution"] == "precedence"]
    explicit_resolved = [c for c in collisions if c["resolution"] == "explicit_override"]
    lines = [
        f"# MERGE_MANIFEST — `{merged_path.name}`",
        "",
        f"- Generated: {ts}",
        f"- Merge spec: `{merge_spec_path}`",
        f"- Merged output: `{merged_path}`",
        "",
        "## Parentage",
        "",
    ]
    for path, _ in parents:
        lines.append(f"- `{path}`")
    lines += [
        "",
        f"## Resolution summary",
        "",
        f"- Explicit overrides: {len(explicit_resolved)}",
        f"- Precedence-resolved: {len(precedence_resolved)}",
        f"- LLM-Council pending: {len(council)}",
        f"- Unresolved (ERROR): {len(unresolved)}",
        "",
    ]
    if explicit_resolved:
        lines.append("### Explicit overrides applied\n")
        for c in explicit_resolved:
            lines.append(f"- `{c['key']}` → `{c['chosen_value']!r}`")
        lines.append("")
    if precedence_resolved:
        lines.append("### Precedence-resolved\n")
        for c in precedence_resolved:
            lines.append(
                f"- `{c['key']}` from `{c['chosen_parent']}` "
                f"(alternatives: {', '.join(n for n in c['parent_values'] if n != c['chosen_parent'])})"
            )
        lines.append("")
    if council:
        lines.append("### LLM-Council pending\n")
        for c in council:
            lines.append(f"- `{c['key']}` → sentinel `{c['chosen_value']}`")
            lines.append(f"  - parent values: {list(c['parent_values'].values())!r}")
        lines.append(
            "\n**Action required:** run the LLM-Council arbitration for each key "
            "above and replace the sentinel in the merged manifest.\n"
        )
    if unresolved:
        lines.append("### Unresolved (merge FAILED)\n")
        for c in unresolved:
            lines.append(f"- `{c['key']}`: values {list(c['parent_values'].values())!r}")
        lines.append("")
    lines.append("---\n")
    lines.append("*⊙ = • × ○*")
    return "\n".join(lines) + "\n"


def check_acyclicity(parents: list[Path], out: Path) -> None:
    out_resolved = out.resolve()
    for p in parents:
        if p.resolve() == out_resolved:
            print(
                f"error: DAG acyclicity violation — output path "
                f"{out} equals parent path {p}",
                file=sys.stderr,
            )
            sys.exit(2)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Merge parent manifests into a hyperagent manifest.")
    ap.add_argument("--parent", action="append", required=True, type=Path, help="Parent manifest JSON. Specify 2+ times.")
    ap.add_argument("--merge", required=True, type=Path, help="Merge-spec JSON.")
    ap.add_argument("--out", required=True, type=Path, help="Output merged-manifest path.")
    ap.add_argument("--output-record", type=Path, help="Path for MERGE_MANIFEST.md (default: <out>.MERGE_MANIFEST.md)")
    args = ap.parse_args(argv)

    if len(args.parent) < 2:
        print("error: at least two --parent manifests are required", file=sys.stderr)
        return 2

    check_acyclicity(args.parent, args.out)

    merge_spec = load_manifest(args.merge)
    parents = [(p, load_manifest(p)) for p in args.parent]

    merged, collisions = merge(parents, merge_spec)

    unresolved = [c for c in collisions if c["resolution"] == "UNRESOLVED"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    record_path = args.output_record or args.out.with_suffix(args.out.suffix + ".MERGE_MANIFEST.md")
    record_path.write_text(
        render_record(parents, args.merge, args.out, collisions),
        encoding="utf-8",
    )

    print(f"✓ merged manifest written: {args.out}")
    print(f"  record:                    {record_path}")
    print(f"  collisions: "
          f"explicit={sum(1 for c in collisions if c['resolution']=='explicit_override')}, "
          f"precedence={sum(1 for c in collisions if c['resolution']=='precedence')}, "
          f"council={sum(1 for c in collisions if c['resolution']=='llm_council_pending')}, "
          f"unresolved={len(unresolved)}")

    if unresolved:
        print("error: unresolved collisions — see MERGE_MANIFEST.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

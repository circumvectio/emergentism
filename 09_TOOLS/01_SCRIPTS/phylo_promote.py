#!/usr/bin/env python3
"""
phylo_promote.py — Promotion pipeline (§5.2 of 06b_PHYLOGENETIC_TREE.md).

Moves a prompt improvement from a niche leaf toward the root genome, under
LLM-Council review + three-gate validation + back-propagation to all
existing niche branches so the genome and its descendants stay in sync.

Four subcommands:

  submit   Create a new promotion submission from a niche.
           Inputs: source niche, target root file, diff, rationale.
           Output: promote/submissions/<id>/ with meta + diff + rationale.

  list     List pending submissions with status.

  review   Run the review pipeline on a submission. Today this calls
           STUB gate implementations (η-Gate, Trophic Gate, Mirror
           Ladder) that auto-pass with a note. Real 8-provider
           LLM-Council integration is the follow-up work that will
           replace the stubs. Emits promote/submissions/<id>/review.json.

  apply    Apply an approved submission. Two steps:
           (1) patch the root genome with the submission's diff
               (requires review.status == "approved");
           (2) back-propagate: for every tool-speciated descendant
               visible to the ancestry audit, re-run
               apply_dac_scaffold.py --overwrite so the descendant's
               SNP-marker realigns to the new genome tree-hash.
           After apply, the submission moves to promote/archive/<id>/.

Usage:
    python3 phylo_promote.py submit --from apu --target <root-file> \\
        --diff <diff.patch> --rationale <rationale.md>
    python3 phylo_promote.py list
    python3 phylo_promote.py review <submission-id>
    python3 phylo_promote.py apply <submission-id>

Exit codes:
    0 — operation succeeded
    1 — operation failed (gate rejection, unresolved collision, patch fail)
    2 — input/environment error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve()
WORKTREE_ROOT = HERE.parents[3]
PROMOTE_ROOT = (
    WORKTREE_ROOT / "SKYZAI_ORG" / "00_REFERENCE" / "DAC_FACTORY" / "promote"
)
SUBMISSIONS_DIR = PROMOTE_ROOT / "submissions"
ARCHIVE_DIR = PROMOTE_ROOT / "archive"
SCAFFOLD_DIR = (
    WORKTREE_ROOT / "SKYZAI_ORG" / "00_REFERENCE" / "DAC_FACTORY" / "DAC_SCAFFOLD"
)
APPLY_SCAFFOLD = HERE.parent / "apply_dac_scaffold.py"
MANIFESTS_DIR = HERE.parent / "dac_scaffold_manifests"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _submission_id(source_niche: str, target: str) -> str:
    h = hashlib.sha256(f"{source_niche}:{target}:{_now()}".encode()).hexdigest()[:8]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"{stamp}-{h}-{source_niche}"


# --- Gate implementations ----------------------------------------------------
# Delegates to phylo_council_gates.py for the real (rule-based) gate logic.
# That module's gate_eta / gate_trophic / gate_mirror functions follow the
# same return contract that the eventual 8-provider LLM-Council integration
# will honour, so future upgrade is a local swap inside that module.

import importlib
_gates = importlib.import_module("phylo_council_gates")
ALL_GATES = _gates.ALL_GATES


# --- Subcommand: submit ------------------------------------------------------

def cmd_submit(args: argparse.Namespace) -> int:
    source = args.source_niche
    target = args.target
    diff = args.diff
    rationale = args.rationale

    if not diff.is_file():
        print(f"error: diff file not found: {diff}", file=sys.stderr)
        return 2
    if not rationale.is_file():
        print(f"error: rationale file not found: {rationale}", file=sys.stderr)
        return 2

    sub_id = _submission_id(source, target)
    sub_dir = SUBMISSIONS_DIR / sub_id
    sub_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "submission_id": sub_id,
        "source_niche": source,
        "target_root_file": target,
        "submitter": args.submitter or "unknown",
        "submitted_at": _now(),
        "status": "pending_review",
    }
    (sub_dir / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    shutil.copy2(diff, sub_dir / "diff.patch")
    shutil.copy2(rationale, sub_dir / "rationale.md")

    print(f"✓ submission created: {sub_id}")
    print(f"  dir: {sub_dir}")
    return 0


# --- Subcommand: list --------------------------------------------------------

def cmd_list(_args: argparse.Namespace) -> int:
    if not SUBMISSIONS_DIR.is_dir():
        print("no submissions")
        return 0
    subs = sorted(p for p in SUBMISSIONS_DIR.iterdir() if p.is_dir())
    if not subs:
        print("no submissions")
        return 0
    print(f"pending submissions: {len(subs)}")
    for s in subs:
        meta_path = s / "meta.json"
        if not meta_path.is_file():
            print(f"  {s.name}  (meta.json missing)")
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        print(
            f"  {meta['submission_id']:55s} "
            f"status={meta.get('status', '?'):20s} "
            f"from={meta.get('source_niche', '?')}"
        )
    return 0


# --- Subcommand: review ------------------------------------------------------

def cmd_review(args: argparse.Namespace) -> int:
    sub_dir = SUBMISSIONS_DIR / args.submission_id
    if not sub_dir.is_dir():
        print(f"error: submission not found: {args.submission_id}", file=sys.stderr)
        return 2
    meta_path = sub_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    gate_results = [gate(sub_dir) for gate in ALL_GATES]
    all_passed = all(g["passed"] for g in gate_results)
    status = "approved" if all_passed else "rejected"

    review = {
        "submission_id": meta["submission_id"],
        "reviewed_at": _now(),
        "status": status,
        "all_gates_passed": all_passed,
        "gates": gate_results,
        "council": {
            "note": "STUB — real 8-provider LLM-Council consensus not yet wired. "
                    "Gate results above are deterministic stub outputs.",
        },
    }
    (sub_dir / "review.json").write_text(
        json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    meta["status"] = status
    meta["reviewed_at"] = review["reviewed_at"]
    meta_path.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"✓ review complete: {status}")
    for g in gate_results:
        mark = "✓" if g["passed"] else "✗"
        print(f"  {mark} {g['gate']:10s} score={g['score']:.2f}  {g['note']}")
    return 0


# --- Subcommand: apply -------------------------------------------------------

def _run(cmd: list[str]) -> int:
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=WORKTREE_ROOT)
    return result.returncode


def _back_propagate() -> int:
    """Re-apply the scaffold to every tool-speciated descendant so their
    SNP markers realign to the new genome tree-hash."""
    from_ref = list(MANIFESTS_DIR.glob("*.json"))
    # Skip the manifests-dir README and any non-manifest files.
    manifests = [p for p in from_ref if p.stem not in {"README"}]
    if not manifests:
        print("  (no manifests to back-propagate)")
        return 0

    # Probe github-root location (same logic as ancestry_query).
    candidates = [
        WORKTREE_ROOT / "Github",
        WORKTREE_ROOT.parent.parent.parent / "Github",
    ]
    github_root = next((c for c in candidates if c.is_dir()), None)
    if github_root is None:
        print("  error: Github/ root not found; back-propagation skipped", file=sys.stderr)
        return 2

    failures = 0
    for manifest in manifests:
        repo_name = manifest.stem
        target = github_root / repo_name
        applied_record = target / "_DAC_SCAFFOLD_APPLIED.md"
        if not applied_record.is_file():
            print(f"  skip {repo_name} (no SNP record; tool-less scaffold or entry-spine tier)")
            continue
        rc = _run(
            [
                sys.executable,
                str(APPLY_SCAFFOLD),
                "--manifest",
                str(manifest),
                "--target",
                str(target),
                "--overwrite",
            ]
        )
        if rc != 0:
            failures += 1
            print(f"  ✗ back-propagation failed for {repo_name}", file=sys.stderr)
        else:
            print(f"  ✓ back-propagated {repo_name}")
    return 1 if failures else 0


def cmd_apply(args: argparse.Namespace) -> int:
    sub_dir = SUBMISSIONS_DIR / args.submission_id
    if not sub_dir.is_dir():
        print(f"error: submission not found: {args.submission_id}", file=sys.stderr)
        return 2
    review_path = sub_dir / "review.json"
    if not review_path.is_file():
        print("error: no review.json; run `review` first", file=sys.stderr)
        return 2
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("status") != "approved":
        print(f"error: submission not approved (status={review.get('status')})", file=sys.stderr)
        return 1
    meta = json.loads((sub_dir / "meta.json").read_text(encoding="utf-8"))
    target = Path(meta["target_root_file"])
    target_abs = target if target.is_absolute() else WORKTREE_ROOT / target
    if not target_abs.is_file():
        print(f"error: target root file not found: {target_abs}", file=sys.stderr)
        return 2

    diff_path = sub_dir / "diff.patch"
    print(f"applying diff to root genome: {target_abs}")
    rc = _run(["git", "apply", "--unsafe-paths", str(diff_path)])
    if rc != 0:
        print("error: git apply failed; submission marked apply_failed", file=sys.stderr)
        meta["status"] = "apply_failed"
        (sub_dir / "meta.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return 1

    print("back-propagating to all tool-speciated descendants:")
    bp_rc = _back_propagate()
    if bp_rc != 0:
        print("warning: one or more descendants failed back-propagation", file=sys.stderr)

    # Archive submission.
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archived = ARCHIVE_DIR / sub_dir.name
    shutil.move(str(sub_dir), str(archived))
    meta["status"] = "applied"
    meta["applied_at"] = _now()
    (archived / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"✓ submission archived: {archived}")
    return bp_rc


# --- Main --------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Promotion pipeline for the agent phylogenetic tree.")
    sub = ap.add_subparsers(dest="op", required=True)

    p_submit = sub.add_parser("submit", help="Create a new promotion submission.")
    p_submit.add_argument("--from", dest="source_niche", required=True, help="Source niche name (e.g. apu).")
    p_submit.add_argument("--target", required=True, help="Path to the root-genome file being mutated.")
    p_submit.add_argument("--diff", type=Path, required=True, help="Path to the unified-diff patch.")
    p_submit.add_argument("--rationale", type=Path, required=True, help="Path to the rationale markdown.")
    p_submit.add_argument("--submitter", help="Human or automated submitter identifier.")
    p_submit.set_defaults(func=cmd_submit)

    p_list = sub.add_parser("list", help="List pending submissions.")
    p_list.set_defaults(func=cmd_list)

    p_review = sub.add_parser("review", help="Run the review pipeline on a submission.")
    p_review.add_argument("submission_id")
    p_review.set_defaults(func=cmd_review)

    p_apply = sub.add_parser("apply", help="Apply an approved submission + back-propagate.")
    p_apply.add_argument("submission_id")
    p_apply.set_defaults(func=cmd_apply)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

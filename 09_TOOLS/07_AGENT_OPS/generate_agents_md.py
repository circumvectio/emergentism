#!/usr/bin/env python3
"""Generate pure-Emergentism AGENTS.md and CLAUDE.md route cards.

This utility is deliberately pillar-local.  It never imports product,
venture, company, runtime, or external-governance instructions into the
Emergentism worldview.  Consequential action uses a complete, scoped,
contestable AuthorizationEnvelope; ordinary repository work follows the
user's scoped request, repository permissions, provenance, and tests.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


CARD_NAMES = ("AGENTS.md", "CLAUDE.md")
FROZEN_PARTS = {"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"}
SESSION_PREFIX = ("11_UPLINK", "60_SESSION_PACKETS")
CUSTOM_ROUTE_CARDS = {
    "00_CONTROL/AGENTS.md",
    "00_CONTROL/CLAUDE.md",
    "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AGENTS.md",
    "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AXIOM_PAPERS/AGENTS.md",
    "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/R2_HARNESS/AGENTS.md",
    "06_ONTOLOGY/ruminations/AGENTS.md",
}


def repository_root(explicit: str | None = None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    candidates.extend((Path.cwd().resolve(), Path(__file__).resolve()))
    for candidate in candidates:
        for parent in (candidate, *candidate.parents):
            if (parent / "00_THE_WELTANSCHAUUNG.md").exists() and (
                parent / "00_THE_KERNEL_INDEX.md"
            ).exists():
                return parent
    raise SystemExit("could not locate the Emergentism repository root")


def active(relative: Path) -> bool:
    if any(part in FROZEN_PARTS for part in relative.parts):
        return False
    if relative.parts[:2] == SESSION_PREFIX:
        return False
    return True


def relative_link(source_dir: Path, target: Path) -> str:
    return os.path.relpath(target, start=source_dir).replace(os.sep, "/")


def lane_title(directory: Path, root: Path) -> str:
    if directory == root:
        return "Emergentism"
    return directory.name.replace("_", " ").strip().title()


def render_card(path: Path, root: Path) -> str:
    directory = path.parent
    relative_directory = directory.relative_to(root)
    root_agents = relative_link(directory, root / "AGENTS.md")
    kernel = relative_link(directory, root / "00_THE_KERNEL_INDEX.md")
    registry = relative_link(directory, root / "00_META/00_SETTLED_CANON_REGISTRY.md")
    completion = relative_link(
        directory,
        root / "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md",
    )
    local_readme = directory / "README.md"
    local_agents = directory / "AGENTS.md"
    heading = lane_title(directory, root)
    route_kind = "Claude compatibility route" if path.name == "CLAUDE.md" else "Agent route"

    read_first = [
        f"- [Emergentism root route]({root_agents})",
        f"- [Kernel Index]({kernel})",
        f"- [Settled Canon Registry]({registry})",
        f"- [Internal completion register]({completion})",
    ]
    if local_readme.exists():
        read_first.insert(0, "- [Local README](README.md)")
    if path.name == "CLAUDE.md" and local_agents.exists():
        read_first.insert(0, "- [Local agent route](AGENTS.md)")

    lane = "." if directory == root else relative_directory.as_posix()
    return "\n".join(
        [
            "---",
            "type: emergentism-agent-route",
            f'title: "{heading} — {route_kind}"',
            'status: "ACTIVE — pure Emergentism route, 2026-07-20"',
            'evidence_tier: "[S] routing discipline; content retains owner-declared tiers."',
            "---",
            "",
            f"# {heading} — {route_kind}",
            "",
            f"**Lane:** `{lane}`",
            "",
            "## Read first",
            "",
            *read_first,
            "",
            "## Pure-worldview boundary",
            "",
            "- Emergentism stands on its own axioms, wagers, methods, and receipts.",
            "- Product, venture, company, runtime, and external-governance systems are neither premises nor authorities here.",
            "- AI and repository work follows the user's scoped request, repository permissions, provenance, reversibility, and tests; no private person's financial or contractual signature is an AI-work gate.",
            "- Consequential action requires a complete, scoped, contestable authorization represented by `AuthorizationEnvelope = principal + mandate + scope + consent + custody + expiry/revocation + contest path + actor + consequence bearer`.",
            "",
            "## Epistemic contract",
            "",
            "- Preserve `[A]/[B]/[S]/[I]/[D]/[C]`; never promote a claim silently.",
            "- Distinguish analytic identity, selected model, interpretation, conjecture, receipt, test, and world outcome.",
            "- Repair source truth before mirrors. Keep counterexamples, alternatives, predictions, and kill criteria visible.",
            "- Archive or tombstone superseded work; do not erase provenance or make an archive a competing owner.",
            "- The physical light cone remains bounded by spacetime and `c`; model-mediated option cones are a different type.",
            "- D4 is actual; D5 is possible. Five typed interfaces are `μ₀…μ₄`; each emergence reading is tiered separately, while `b₆` and `r₆` are non-μ interpretive edges.",
            "",
            "## Rosetta dispatch",
            "",
            "Use the seven roles as a work vocabulary, never as identities or ranks of worth:",
            "",
            "- L1 isolates boundaries and contradictions.",
            "- L2 expands alternatives and counterexamples.",
            "- L3 audits logic, evidence, sources, and routes.",
            "- L4 executes the smallest authorized, testable change.",
            "- L5 designs schemas and owner maps.",
            "- L6 compresses, archives, and removes false necessity.",
            "- L7 witnesses and translates without overriding source truth.",
            "",
            "## Lane discipline",
            "",
            "- Stay inside this lane unless the scoped task requires a named owner elsewhere.",
            "- Preserve concurrent work and inspect Git state before edits.",
            "- A commit, test, receipt, preview, deployment, domain, and independent replication are different claims.",
            "- If a local instruction conflicts with the root route or Settled Canon Registry, repair or escalate the conflict; do not silently choose the grander claim.",
            "",
            "•   ⊙   ○ — sovereign frames; no arithmetic or coercion.",
            "",
        ]
    )


def tracked_route_cards(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "**/AGENTS.md", "**/CLAUDE.md", "CLAUDE.md"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    cards: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = Path(raw.decode("utf-8"))
        if (
            relative == Path("AGENTS.md")
            or relative.as_posix() in CUSTOM_ROUTE_CARDS
            or not active(relative)
        ):
            continue
        path = root / relative
        # `git ls-files` can still expose a path that has been relocated in the
        # working tree but not yet staged.  A deleted route is not an active
        # instruction surface and must never be recreated by this generator.
        if not path.is_file():
            continue
        cards.append(path)
    return sorted(cards)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Emergentism repository root")
    parser.add_argument("--write", action="store_true", help="rewrite active route cards")
    parser.add_argument("--check", action="store_true", help="fail when a generated card differs")
    args = parser.parse_args()
    if args.write and args.check:
        parser.error("choose either --write or --check")

    root = repository_root(args.repo)
    cards = tracked_route_cards(root)
    drift: list[str] = []
    for path in cards:
        expected = render_card(path, root)
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == expected:
            continue
        drift.append(path.relative_to(root).as_posix())
        if args.write:
            path.write_text(expected, encoding="utf-8")

    action = "rewrote" if args.write else "would rewrite"
    print(f"{action} {len(drift)} of {len(cards)} active route cards")
    for item in drift[:40]:
        print(f"  {item}")
    if len(drift) > 40:
        print(f"  ... and {len(drift) - 40} more")

    if args.check and drift:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

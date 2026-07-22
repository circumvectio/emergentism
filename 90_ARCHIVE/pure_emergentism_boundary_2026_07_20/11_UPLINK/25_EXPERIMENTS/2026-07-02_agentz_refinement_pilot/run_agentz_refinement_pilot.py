#!/usr/bin/env python3
"""Run the bounded Agentz refinement pilot.

This script does not call models. It mechanizes the parts that should be
reproducible: scope loading, claim extraction, reviewer report collation, and
K2 packet assembly.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
ROOT = PACKET_DIR.parents[2]
REPORTS_DIR = PACKET_DIR / "reports"
OUTPUTS_DIR = PACKET_DIR / "outputs"
SCOPE_PATH = PACKET_DIR / "scope.json"


@dataclass
class Claim:
    claim_id: str
    source_path: str
    line: int
    kind: str
    text: str
    asserted_tiers: list[str]


def load_scope() -> dict[str, Any]:
    return json.loads(SCOPE_PATH.read_text())


def tiers(text: str) -> list[str]:
    return sorted(set(re.findall(r"\[[A-Z][0-9]?\]|\[[A-Z]/[A-Z/]+\]", text)))


def strip_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^\s*[-*]\s+", "", text)
    text = text.strip("`*_ ")
    return text


def should_capture(line: str) -> tuple[bool, str]:
    raw = line.strip()
    if not raw:
        return False, ""
    if raw.startswith(">"):
        return True, "blockquote"
    if raw.startswith("## ") and not raw.startswith("###"):
        return True, "heading"
    if "**" in raw and len(raw) > 30:
        return True, "bold_claim"
    if "kill criterion" in raw.lower() or re.match(r"^\d+\.\s+\*\*.*dies", raw):
        return True, "kill_criterion"
    if raw.startswith("|") or raw.startswith("---") or raw.startswith("```"):
        return False, ""
    return False, ""


def extract_claims(scope: dict[str, Any]) -> list[Claim]:
    claims: list[Claim] = []
    counter = 1
    for rel in scope["inputs"]:
        if rel.endswith(".json"):
            continue
        path = ROOT / rel
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            capture, kind = should_capture(line)
            if not capture:
                continue
            text = strip_markdown(line.lstrip("> "))
            if len(text) < 12:
                continue
            claims.append(
                Claim(
                    claim_id=f"C{counter:03d}",
                    source_path=rel,
                    line=line_no,
                    kind=kind,
                    text=text,
                    asserted_tiers=tiers(text),
                )
            )
            counter += 1
    return claims


def write_claim_outputs(claims: list[Claim]) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / "claims.json").write_text(
        json.dumps([asdict(c) for c in claims], indent=2, sort_keys=True) + "\n"
    )

    lines = [
        "# Extracted Claims",
        "",
        "Mechanical extraction only. No inference; false positives are expected and should be cut downstream.",
        "",
        "| ID | Source | Line | Kind | Claim | Tiers |",
        "|---|---|---:|---|---|---|",
    ]
    for c in claims:
        claim_text = c.text.replace("|", "\\|")
        lines.append(
            f"| {c.claim_id} | `{c.source_path}` | {c.line} | {c.kind} | {claim_text} | {', '.join(c.asserted_tiers) or '-'} |"
        )
    (OUTPUTS_DIR / "claims.md").write_text("\n".join(lines) + "\n")


def read_reports() -> dict[str, str]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    reports: dict[str, str] = {}
    for path in sorted(REPORTS_DIR.glob("*.md")):
        reports[path.name] = path.read_text(errors="replace").strip()
    return reports


def read_empirical_result(scope: dict[str, Any]) -> dict[str, Any]:
    result_rel = next(path for path in scope["inputs"] if path.endswith("results.json"))
    return json.loads((ROOT / result_rel).read_text())


def proposed_patch_note(empirical: dict[str, Any]) -> str:
    verdict = empirical["verdict"]
    metrics = empirical["metrics"]
    comparison = empirical["comparisons"]
    return (
        "2026-07-02 empirical pilot note: in the Ciampaglia-Lozano-Helbing public "
        "Generalized Ultimatum Game dataset, the bounded fairness/coherence proxy beat "
        "payoff-only (`payoff_plus_fairness` log_loss "
        f"{metrics['payoff_plus_fairness']['log_loss_mean']:.6f} vs payoff_only "
        f"{metrics['payoff_only']['log_loss_mean']:.6f}; win rate "
        f"{comparison['payoff_plus_fairness']['log_loss_win_rate_vs_payoff_only']:.3f}), "
        "while the product-only proxy was not supported "
        f"(`{verdict['multiplicative_single_score_proxy']}`). Treat this as evidence "
        "for a justice/fairness gate and against product-only overcompression at node scale."
    )


def assemble_k2_packet(scope: dict[str, Any], claims: list[Claim], reports: dict[str, str]) -> str:
    empirical = read_empirical_result(scope)
    patch_note = proposed_patch_note(empirical)
    report_lines: list[str] = []
    if reports:
        for name, content in reports.items():
            report_lines.extend([f"### {name}", "", content, ""])
    else:
        report_lines.append("_No reviewer reports present yet._")

    source_counts: dict[str, int] = {}
    for c in claims:
        source_counts[c.source_path] = source_counts.get(c.source_path, 0) + 1

    packet = [
        "---",
        'title: "K2 Packet - Agentz Refinement Pilot"',
        "date: 2026-07-02",
        'status: "STAGED FOR K2; NOT CANON"',
        'evidence_tier: "[B] local extraction/collation; [D] staged recommendations"',
        "---",
        "",
        "# K2 Packet - Agentz Refinement Pilot",
        "",
        "## 1. Scope",
        "",
        f"Packet: `{scope['packet']}`",
        "",
        "Inputs:",
        "",
    ]
    packet.extend(f"- `{path}`" for path in scope["inputs"])
    packet.extend(
        [
            "",
            "## 2. Guardrails",
            "",
            "- May cut, test-specify, archive-candidate, and stage only.",
            "- May not write canon, amend the registry, or self-ratify.",
            "- K2/PRISM remains outside the workflow.",
            "- Archive candidates require read-before-flagging and K3 tombstones.",
            "- All doctrine edits remain `[D]` until K2 signs.",
            "",
            "## 3. Extracted Claims",
            "",
            f"Mechanical claims extracted: {len(claims)}",
            "",
        ]
    )
    for source, count in sorted(source_counts.items()):
        packet.append(f"- `{source}`: {count}")
    packet.extend(
        [
            "",
            "See `outputs/claims.md` and `outputs/claims.json`.",
            "",
            "## 4. Reviewer Reports",
            "",
            *report_lines,
            "## 5. Proposed Cuts",
            "",
            "- Cut any product-only behavioral overclaim. The empirical result does not support `material_score * fairness_score` as the standalone best predictor in the tested domain.",
            "- Cut any wording that treats a single bounded ultimatum-game run as proof of the full Extraction Law.",
            "- Cut any workflow output that presents itself as canon rather than staged advice.",
            "",
            "## 6. Proposed Tests",
            "",
            "- Repeat the extraction/coherence test on a larger ultimatum-game meta dataset.",
            "- Run a repeated trust/prisoner's-dilemma test for whether repeated lawful exchange reduces coordination-cost proxies over time.",
            "- Once Skyzai receipts exist, measure dispute/reversal/reverification rates before and after repeated `eta=0` exchange loops.",
            "",
            "## 7. Archive Candidates",
            "",
            "- No canonical archive action authorized by this packet.",
            "- Candidate only: preserve `90_ARCHIVE/2026_07_02_PRE_PRUNE/` as K3 pre-prune provenance.",
            "",
            "## 8. Draft Patches To Stage",
            "",
            "Patch note to add to affected `[D]` drafts:",
            "",
            f"> {patch_note}",
            "",
            "Default patch targets:",
            "",
            "- `04_AXIOLOGY/00_THE_EXTRACTION_LAW.md`",
            "- `05_COSMOLOGY/00_D5_THE_MUTUALISM_LIMIT.md`",
            "",
            "Default non-target:",
            "",
            "- `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md` unless a reviewer identifies a direct overclaim. The current pilot result bears on behavioral/product proxy claims, not PSL(2,C) algebra.",
            "",
            "## 9. Stop Conditions",
            "",
            "- Stop before registry edits.",
            "- Stop before constitutional wording changes.",
            "- Stop before archival moves outside already-read pilot files.",
            "- Stop before any claim that the pilot proves Emergentism.",
            "",
        ]
    )
    return "\n".join(packet)


def write_receipts(scope: dict[str, Any], claims: list[Claim], reports: dict[str, str]) -> None:
    receipt = {
        "packet": scope["packet"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope_inputs": scope["inputs"],
        "claims_extracted": len(claims),
        "reports_collated": sorted(reports),
        "outputs": [
            "outputs/claims.json",
            "outputs/claims.md",
            "outputs/k2_packet.md",
            "outputs/run_receipt.json",
            "RUN_RECEIPT.md",
        ],
        "canon_change": False,
        "k2_required_for_canon_change": True,
    }
    (OUTPUTS_DIR / "run_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )
    lines = [
        "---",
        'title: "Run Receipt - Agentz Refinement Pilot"',
        "date: 2026-07-02",
        'status: "RUN COMPLETE"',
        'evidence_tier: "[B] local script run; [D] staged recommendations"',
        "---",
        "",
        "# Run Receipt - Agentz Refinement Pilot",
        "",
        f"- Claims extracted: {len(claims)}",
        f"- Reports collated: {len(reports)}",
        "- Canon changed by script: no",
        "- K2 required for canon change: yes",
        "",
        "Outputs:",
        "",
    ]
    lines.extend(f"- `{item}`" for item in receipt["outputs"])
    (PACKET_DIR / "RUN_RECEIPT.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    scope = load_scope()
    for rel in scope["inputs"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing scoped input: {rel}")

    claims = extract_claims(scope)
    reports = read_reports()
    write_claim_outputs(claims)
    k2_packet = assemble_k2_packet(scope, claims, reports)
    (OUTPUTS_DIR / "k2_packet.md").write_text(k2_packet + "\n")
    write_receipts(scope, claims, reports)
    print(f"claims={len(claims)} reports={len(reports)}")
    print(f"k2_packet={OUTPUTS_DIR / 'k2_packet.md'}")


if __name__ == "__main__":
    main()


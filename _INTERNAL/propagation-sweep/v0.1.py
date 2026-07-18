#!/usr/bin/env python3
"""
Propagation Sweep v0.1 — finds high-confidence contradictions between doc
bodies in the canon and the Settled Canon Registry.

Read-mostly. K3 (archive-first) honored. K2 disposes per fix.

Scope: all .md files under the canon sections (root 00_*, 00_META, 01-11).
Excludes: _INTERNAL/, 90_ARCHIVE/, 91_COMPATIBILITY/, 09_TOOLS/06_PACKAGES/,
and the report itself.

Patterns checked (high-confidence only):
  - Forbidden imports: R* ≈ 1.5, ABM-verified, 85-92% syntropy,
    Kolmogorov complexity zero, 25% tipping point
  - Retracted items (receipt 126): D6≡D0 literal identity, 4-force
    bijection, "Dn problem needs Dn+1 tools"
  - AI-as-evidence: "an AI confirmed/proved/verified X"
  - Specific KSC violations: KSC-04 (Titans forced), KSC-06
    (K2 primitive), KSC-08 (whole Compass calibrated), emblem
    arithmetic

Patterns NOT checked (semantic, out of scope for v0.1):
  - "Still flag if" cells that require context understanding
  - Per-claim tier promotions (requires reading the claim)
  - Bearer laundering, type-seam violations, μ-irreducibility
    inferences, etc.

Output: 00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md
"""

import re
import sys
from pathlib import Path

WORKTREE = Path("/Users/Yves/Documents/.codex-worktrees/emergentist-compass-kintsugi")
REPORT_PATH = WORKTREE / "00_META" / "00_PROPAGATION_SWEEP_REPORT_v0.1.md"

# In-scope canon sections
CANON_SECTIONS = [
    WORKTREE,  # root for 00_*.md
    WORKTREE / "00_META",
    WORKTREE / "01_TELEOLOGY",
    WORKTREE / "02_EPISTEMOLOGY",
    WORKTREE / "03_METHODOLOGY",
    WORKTREE / "04_AXIOLOGY",
    WORKTREE / "05_COSMOLOGY",
    WORKTREE / "06_ONTOLOGY",
    WORKTREE / "07_THEOLOGY",
    WORKTREE / "08_FRAMEWORK_SUPPORT",
    WORKTREE / "10_SEED",
    WORKTREE / "11_UPLINK",
]

# Out-of-scope paths (excluded)
EXCLUDE_PATTERNS = [
    "/_INTERNAL/",
    "/90_ARCHIVE/",
    "/91_COMPATIBILITY/",
    "/09_TOOLS/06_PACKAGES/",
    "/12_PUBLIC_SITE/",  # generated HTML; out of scope for v0.1
    "/node_modules/",
]

# High-confidence forbidden imports (regex, description)
FORBIDDEN_IMPORTS = [
    (r"R\*\s*[≈~=]\s*1\.5", "R* ≈ 1.5 (retracted; live is η_c ≈ 0.58 [C])"),
    (r"\bABM[- ]verified\b", '"ABM-verified" (retracted)'),
    (r"85\s*[-–—]\s*92\s*%\s*syntropy", '"85–92% syntropy" (retracted)'),
    (r"\bKolmogorov complexity zero\b", '"Kolmogorov complexity zero" (retracted)'),
    (r"\b25\s*%\s*tipping point\b", '"25% tipping point" (retracted)'),
]

# Retracted items from receipt 126
RETRACTED_126 = [
    (r"\bD6\s*≡\s*D0\b", "D6≡D0 literal identity (retracted; KSC-03)"),
    (r"\bfour[- ]force bijection\b", "4-force bijection (retracted; electroweak unifies D2/D3)"),
    (r"\bD[ₙn]\s*problem\s*needs\s*D[ₙn][+＋]\s*tools?\b", '"Dₙ problem needs Dₙ₊₁ tools" (retracted; Presburger/RCF complete+decidable)'),
]

# AI-as-evidence pattern
AI_AS_EVIDENCE = re.compile(
    r"\b(?:an?\s+)?AI\s+(?:confirmed|proved|verified|attested|showed|demonstrated|attests)\s+",
    re.IGNORECASE,
)

# Specific KSC violations
KSC_PATTERNS = [
    (
        re.compile(
            r"\b(?:forced|uniquely\s+forced|derived|proved|proven)\b[^.\n]{0,80}\b(?:triad|three\s+Titans|\{0,1,∞\}|Titans)\b",
            re.IGNORECASE,
        ),
        "KSC-04: Titans presented as forced/derived (selected symbolic roles only)",
    ),
    (
        re.compile(
            r"\b(?:K2|founder|mortal\s+signer)\b[^.\n]{0,80}\b(?:primitive\s+of|necessary\s+for|universal|ground\s+of)\b[^.\n]{0,40}\b(?:reality|agency|truth|ethic)\b",
            re.IGNORECASE,
        ),
        "KSC-06: K2 presented as primitive of reality/agency/ethic",
    ),
    (
        re.compile(
            r"\b(?:whole\s+Compass|Compass\s+as\s+a\s+whole|the\s+framework\s+as\s+a\s+whole)\b[^.\n]{0,80}\b(?:calibrated|validated|replicated|proven)\b",
            re.IGNORECASE,
        ),
        "KSC-08: Whole Compass presented as calibrated/validated (only claim-level is)",
    ),
    (
        re.compile(r"\b1\s*=\s*0\s*×\s*∞\b"),
        "Emblem used as arithmetic identity (must be explicitly non-arithmetic)",
    ),
    (
        re.compile(
            r"\bη\s*=\s*0\b[^.\n]{0,80}\b(?:alone|sufficient|decisive|by\s+itself)\b",
            re.IGNORECASE,
        ),
        "η=0 presented as morally decisive alone (KSC: η is necessary, not sufficient)",
    ),
]

# Pre-compile forbidden imports and retracted items
COMPILED_FORBIDDEN = [(re.compile(p, re.IGNORECASE), d) for p, d in FORBIDDEN_IMPORTS]
COMPILED_RETRACTED = [(re.compile(p, re.IGNORECASE), d) for p, d in RETRACTED_126]


def in_scope(path: Path) -> bool:
    """Check if path is in a canon section and not excluded."""
    pstr = str(path)
    for ex in EXCLUDE_PATTERNS:
        if ex in pstr:
            return False
    # Must be under at least one canon section
    for section in CANON_SECTIONS:
        try:
            path.relative_to(section)
            return True
        except ValueError:
            continue
    return False


def scan_doc(path: Path):
    """Scan a doc for forbidden patterns. Returns list of (line_no, category, snippet)."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (IOError, OSError):
        return findings

    for lineno, line in enumerate(text.splitlines(), 1):
        # Skip pure YAML frontmatter block lines
        if line.strip() == "---":
            continue
        # Skip lines inside the report template itself if encountered (none expected)

        for pattern, desc in COMPILED_FORBIDDEN:
            if pattern.search(line):
                findings.append((lineno, "FORBIDDEN_IMPORT", desc, line.strip()[:140]))

        for pattern, desc in COMPILED_RETRACTED:
            if pattern.search(line):
                findings.append((lineno, "RETRACTED_126", desc, line.strip()[:140]))

        if AI_AS_EVIDENCE.search(line):
            findings.append(
                (lineno, "AI_AS_EVIDENCE", "AI-as-evidence (a live AI confirmation cited as proof)", line.strip()[:140])
            )

        for pattern, desc in KSC_PATTERNS:
            if pattern.search(line):
                findings.append((lineno, "KSC_VIOLATION", desc, line.strip()[:140]))

    return findings


def main():
    findings_by_doc = {}
    scanned_count = 0
    seen = set()  # dedupe: walk once, iterate all canon sections together
    for section in CANON_SECTIONS:
        if not section.exists():
            continue
        for md in section.rglob("*.md"):
            if not md.is_file():
                continue
            if md == REPORT_PATH:
                continue
            # Dedupe by absolute path (CANON_SECTIONS is nested)
            apath = md.resolve()
            if apath in seen:
                continue
            seen.add(apath)
            if not in_scope(md):
                continue
            scanned_count += 1
            findings = scan_doc(md)
            if findings:
                findings_by_doc[md.relative_to(WORKTREE)] = findings

    total_findings = sum(len(v) for v in findings_by_doc.values())

    # Group findings by category
    by_category = {}
    for findings in findings_by_doc.values():
        for _, cat, desc, _ in findings:
            by_category.setdefault(cat, {}).setdefault(desc, 0)
            by_category[cat][desc] += 1

    # Build report
    lines = []
    lines.append("# Propagation Sweep Report v0.1")
    lines.append("")
    lines.append("> **Status:** `[D]` draft. Single V-forcer per the Release Doctrine Phase 0 #1.")
    lines.append("> **Method:** high-confidence regex scan of all in-scope `.md` files against the Settled Canon Registry.")
    lines.append(f"> **Total findings:** {total_findings} across {len(findings_by_doc)} docs ({scanned_count} scanned).")
    lines.append("> **Out of scope:** semantic patterns requiring manual review (per-row 'Still flag if' matches that need context).")
    lines.append("")
    lines.append("## 1. Scope")
    lines.append("")
    lines.append("**In scope (canon sections):**")
    for s in CANON_SECTIONS:
        rel = s.relative_to(WORKTREE) if s != WORKTREE else "."
        lines.append(f"- `{rel}/`")
    lines.append("")
    lines.append("**Excluded:**")
    for ex in EXCLUDE_PATTERNS:
        lines.append(f"- `{ex}`")
    lines.append("")
    lines.append("**Patterns checked (high-confidence only):**")
    lines.append("- Forbidden imports: R* ≈ 1.5, ABM-verified, 85–92% syntropy, Kolmogorov complexity zero, 25% tipping point")
    lines.append("- Retracted items (receipt 126): D6≡D0 literal, 4-force bijection, 'Dₙ problem needs Dₙ₊₁ tools'")
    lines.append("- AI-as-evidence: 'an AI confirmed/proved/verified/attested/showed/demonstrated X'")
    lines.append("- KSC-04: Titans presented as forced/derived")
    lines.append("- KSC-06: K2 presented as primitive of reality/agency/ethic")
    lines.append("- KSC-08: Whole Compass presented as calibrated/validated")
    lines.append("- Emblem used as arithmetic identity")
    lines.append("- η=0 presented as morally decisive alone")
    lines.append("")
    lines.append("## 2. Findings by category")
    lines.append("")
    if by_category:
        for cat in sorted(by_category.keys()):
            lines.append(f"### {cat}")
            lines.append("")
            for desc, count in sorted(by_category[cat].items(), key=lambda x: -x[1]):
                lines.append(f"- ({count}×) {desc}")
            lines.append("")
    else:
        lines.append("_No high-confidence contradictions found._")
        lines.append("")

    lines.append("## 3. Per-doc findings")
    lines.append("")
    if findings_by_doc:
        for doc, findings in sorted(findings_by_doc.items()):
            lines.append(f"### `{doc}`")
            lines.append("")
            for lineno, cat, desc, snippet in findings:
                lines.append(f"- **Line {lineno}** [{cat}] {desc}")
                lines.append("  ```")
                lines.append(f"  {snippet}")
                lines.append("  ```")
            lines.append("")
    else:
        lines.append("_No docs with high-confidence contradictions._")
        lines.append("")

    lines.append("## 4. Out of scope (manual review needed)")
    lines.append("")
    lines.append("The following registry rows have 'Still flag if' patterns that require semantic understanding (not regex). Each row's authority doc should be reviewed against the row's ruling:")
    lines.append("")
    lines.append("**Authority docs to review (one per row):**")
    lines.append("")
    lines.append("| Row | Authority | Manual check needed for |")
    lines.append("|---|---|---|")
    lines.append("| The four mixed-sign operator slots | `05_COSMOLOGY/00_INTELLIGENCE_AND_THE_POTENTIAL_CONE.md` | archetype labels used as moral verdicts |")
    lines.append("| Kālī's status | `00_THE_COMPASS.md` | name itself makes the cut lawful |")
    lines.append("| F5 as an Emergentist teleology token | `05_COSMOLOGY/00_INTELLIGENCE_AND_THE_POTENTIAL_CONE.md` | F5-as-physics |")
    lines.append("| The reciprocal-chart identity | `05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md` | pole behavior, empirical use |")
    lines.append("| The non-extraction axis | `05_COSMOLOGY/00_THE_DYADIC_COUPLING_LAW.md` | η-alone-as-moral-decisive (also caught by regex) |")
    lines.append("| Viṣṇu's Möbius class | `08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_63_Mobius_Operators.md` | 'outside PSL(2,ℂ)' |")
    lines.append("| Finity (1) as the self-dual midpoint | `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md` | 'proved as new theorem' |")
    lines.append("| Burrisphere vs Bloch sphere | `…/01_THE_TRANSCENDENTAL_TRINITY/04_BIT_TO_QUBIT.md` | Bloch-sphere-only |")
    lines.append("| The two faces of number | `…/00_THE_TRANSCENDENTAL_TRINITY_CANON.md` | sphere-as-only-geometry |")
    lines.append("| Replicator Stack: six layers | `05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md` | '5 layers' or Epigenotype dropped |")
    lines.append("| Replicator ↔ varṇa correspondence | `08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md` | 'worth-by-birth' reading |")
    lines.append("| Titan Composition Law | `…/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md` | unconditional composition |")
    lines.append("| KSC-01 D4/D5 | `05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md` | type-seam violations |")
    lines.append("| KSC-02 μ-crossings | `05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md` | μ-irreducibility inference |")
    lines.append("| KSC-03 D6 closure | `…/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md` | D6-as-freedom |")
    lines.append("| KSC-05 quantum correspondence | `…/03_FORMAL_SYSTEM/38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md` | quantum-as-dimension |")
    lines.append("| KSC-06 authorization | `00_THE_COMPASS.md` | bearer laundering |")
    lines.append("| KSC-07 Justice | `04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md` | omitted bearer |")
    lines.append("| KSC-09 macro costs | `03_METHODOLOGY/03_PREREGISTRATIONS/02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md` | heterogeneous scalar cost |")
    lines.append("| KSC-10 Egregoreotype | `05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGORETYPE.md` | Egregoreotype-as-entity |")
    lines.append("")
    lines.append("## 5. Recommendation")
    lines.append("")
    lines.append("Per the Release Doctrine Phase 0 #1:")
    lines.append("")
    lines.append("1. **The findings in §3 are per-doc fixes with K2 sign-off.** They are NOT addressed by this V-forcer. Each fix is a future V-forcer once K2 reviews the list.")
    lines.append("2. **The manual-review list in §4 is parked.** Each authority doc should be re-read against its registry row, with semantic findings batched into a future V-forcer per row.")
    lines.append("3. **The script (`_INTERNAL/propagation-sweep/v0.1.py`) is archival.** Re-run only if the registry is updated; update the patterns first.")
    lines.append("4. **Do not flag doc-lag as live error** (per the registry's preamble: 'The doctrine does not change because a doc lagged it. Repair the lagging doc *to* the ruling; never re-open the ruling because a doc disagrees.').")
    lines.append("")
    lines.append(f"**Audited {scanned_count} files; found {total_findings} high-confidence contradictions in {len(findings_by_doc)} docs; flagged 20 rows for manual review.**")
    lines.append("")
    lines.append("—")
    lines.append("")
    lines.append("⊙ = • × ○")
    lines.append("")
    lines.append(f"v0.1 · generated by `_INTERNAL/propagation-sweep/v0.1.py` · K2-delegated 2026-07-18")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    # Also print a summary to stdout
    print(f"Report written: {REPORT_PATH}")
    print(f"Scanned: {scanned_count} files")
    print(f"Findings: {total_findings} across {len(findings_by_doc)} docs")
    print(f"Out-of-scope rows for manual review: 20")
    return 0 if total_findings == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

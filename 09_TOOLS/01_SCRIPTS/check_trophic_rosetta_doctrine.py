#!/usr/bin/env python3
"""Check the restored Trophic–Replicator–Rosetta doctrine.

The check is intentionally narrow: live source owners and their current reader
projection. Archives are provenance and may retain the wording this repair
rejects. Use ``--self-test`` to prove each negative control fires.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

LIVE_OWNERS = (
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
    "04_AXIOLOGY/00_THE_EXTRACTION_LAW.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/39_NEOTENY_AS_F5_DELAY_AND_CULTURAL_WOMB.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/12_EFR_EXTRACTION_COEFFICIENT.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/46_THE_ETA_CONVERSION_MAP.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md",
    "01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md",
    "00_META/00_SETTLED_CANON_REGISTRY.md",
)

PROJECTION_FILES = (
    "00_THE_KERNEL_INDEX.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "12_PUBLIC_SITE/ecology/index.html",
)

BARE_ETA_SCOPE = (
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
    "04_AXIOLOGY/00_THE_EXTRACTION_LAW.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/39_NEOTENY_AS_F5_DELAY_AND_CULTURAL_WOMB.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/12_EFR_EXTRACTION_COEFFICIENT.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md",
    "01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "00_META/00_SETTLED_CANON_REGISTRY.md",
)

FORBIDDEN = {
    "same-species-is-trophic": re.compile(
        r"same[ -]species\s*(?:=|is|means|/|as (?:a )?synonym for)\s*same trophic",
        re.IGNORECASE,
    ),
    "trophic-is-moral-rank": re.compile(
        r"higher trophic(?: position| level| stratum)?[^.\n]{0,90}"
        r"(?:higher worth|more worthy|morally superior|better people?)",
        re.IGNORECASE,
    ),
    "hereditary-rosetta": re.compile(
        r"(?:Rosetta (?:row|caste)|human caste)[^.\n]{0,80}"
        r"(?:assigned at birth|birth-based|must be hereditary|is hereditary)",
        re.IGNORECASE,
    ),
    "higher-caste-extraction": re.compile(
        r"higher (?:caste|Rosetta row)[^.\n]{0,100}extract[^.\n]{0,80}"
        r"lower (?:caste|Rosetta row)",
        re.IGNORECASE,
    ),
    "sexual-competition-general-license": re.compile(
        r"sexual (?:selection|competition)[^.\n]{0,100}"
        r"(?:general (?:social|economic|political) (?:licen[cs]e|rule)|"
        r"licen[cs]es (?:social|economic|political) predation)",
        re.IGNORECASE,
    ),
    "tantra-presented-as-empirical": re.compile(
        r"(?:Kundalini|Tantra|Vajrayana)[^.\n]{0,100}"
        r"(?:empirically|physiologically) (?:proven|established|confirmed)",
        re.IGNORECASE,
    ),
}

BARE_ETA = re.compile(r"(?<![\w_])η\s*(?:=|<|>|→|≈)")

REQUIRED = {
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md": (
        "same trophic stratum or functional guild",
        "obtain biomass and usable energy through the lower trophic strata",
        "Species, trophic position, replicator depth, and Rosetta row",
        "Human polyphenotypic cooperation",
    ),
    "05_COSMOLOGY/03_FORMAL_SYSTEM/46_THE_ETA_CONVERSION_MAP.md": (
        "η_ratio = 1",
        "η_move = 0",
        "η_domain",
        "payer",
        "beneficiary",
        "regenerative capacity",
    ),
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md": (
        "Selected cooperation corollary",
        "not force it",
        "bounded horizontal exception",
        "Strongest rivals",
        "Kill criterion",
    ),
    "05_COSMOLOGY/03_FORMAL_SYSTEM/12_EFR_EXTRACTION_COEFFICIENT.md": (
        "coexistence equilibrium is a center",
        "closed periodic orbits",
        "it does not converge",
    ),
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md": (
        "L1 is not a layer",
        "Genotype → Epigenotype → Phenotype → Extended Phenotype → Memotype → Egregoreotype",
        "specialized, changeable functions",
        "grants no higher row an extraction right",
    ),
    "01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md": (
        "symbolic vertical",
        "practice claim and testable hypothesis",
        "No physiological",
        "Strongest rivals",
    ),
}

LEDGER = (
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
    "168_TROPHIC_REPLICATOR_ROSETTA_RESTORATION_2026_07_23.md"
)

PUBLIC_OWNER_PATHS = (
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/46_THE_ETA_CONVERSION_MAP.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md",
    "01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md",
    LEDGER,
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def line_for(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def forbidden_findings(relative: str, text: str) -> list[str]:
    findings: list[str] = []
    for label, pattern in FORBIDDEN.items():
        for match in pattern.finditer(text):
            findings.append(f"{relative}:{line_for(text, match.start())}: {label}")
    return findings


def run_self_test() -> int:
    planted = {
        "same-species-is-trophic": "same species = same trophic level",
        "trophic-is-moral-rank": "higher trophic position means morally superior people",
        "hereditary-rosetta": "Rosetta caste is hereditary",
        "higher-caste-extraction": "higher caste may extract resources from lower caste",
        "sexual-competition-general-license": "sexual competition licenses economic predation",
        "tantra-presented-as-empirical": "Tantra is physiologically proven to create power",
    }
    failed: list[str] = []
    for expected, sample in planted.items():
        labels = {
            finding.rsplit(": ", 1)[-1]
            for finding in forbidden_findings("<planted>", sample)
        }
        if expected not in labels:
            failed.append(expected)

    safe = (
        "Species, trophic stratum, replicator layer, and Rosetta row are separate. "
        "Human functions are changeable. Sexual selection is bounded. "
        "Tantra remains an interpretive and testable hypothesis."
    )
    if forbidden_findings("<safe>", safe):
        failed.append("safe-control-false-positive")
    if not BARE_ETA.search("η = 0") or BARE_ETA.search("η_move = 0"):
        failed.append("bare-eta-control")

    if failed:
        print("trophic_rosetta_doctrine self-test FAILED: " + ", ".join(failed))
        return 1
    print("trophic_rosetta_doctrine self-test: all planted negatives detected")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()

    findings: list[str] = []
    paths = set(LIVE_OWNERS + PROJECTION_FILES + BARE_ETA_SCOPE + (LEDGER,))
    texts: dict[str, str] = {}
    for relative in sorted(paths):
        path = ROOT / relative
        if not path.is_file():
            findings.append(f"{relative}: missing required file")
            continue
        texts[relative] = path.read_text(encoding="utf-8")

    for relative in LIVE_OWNERS + PROJECTION_FILES:
        if relative in texts:
            findings.extend(forbidden_findings(relative, texts[relative]))

    for relative in BARE_ETA_SCOPE:
        text = texts.get(relative, "")
        for match in BARE_ETA.finditer(text):
            findings.append(
                f"{relative}:{line_for(text, match.start())}: bare ambiguous eta"
            )

    for relative, needles in REQUIRED.items():
        text = texts.get(relative, "")
        normalized = " ".join(text.split())
        for needle in needles:
            if " ".join(needle.split()) not in normalized:
                findings.append(f"{relative}: missing required doctrine: {needle!r}")

    ledger = texts.get(LEDGER, "")
    dispositions = (
        "RESTORE",
        "RESTORE_AND_RETIER",
        "LIVE_EQUIVALENT",
        "CONFLICT_REQUIRES_RULING",
        "ARCHIVE_ONLY",
    )
    for disposition in dispositions:
        if f"`{disposition}`" not in ledger:
            findings.append(f"{LEDGER}: missing disposition {disposition}")
    ids = [int(value) for value in re.findall(r"\| TRR-(\d{2}) \|", ledger)]
    if ids != list(range(1, 30)):
        findings.append(f"{LEDGER}: candidate sequence is {ids!r}, expected 1..29")

    public = texts.get("12_PUBLIC_SITE/ecology/index.html", "")
    for owner in PUBLIC_OWNER_PATHS:
        if owner not in public:
            findings.append(f"12_PUBLIC_SITE/ecology/index.html: missing owner {owner}")
        if not (ROOT / owner).is_file():
            findings.append(f"12_PUBLIC_SITE/ecology/index.html: owner is not live: {owner}")

    parity_path = ROOT / "12_PUBLIC_SITE/public_semantic_parity.json"
    try:
        parity = json.loads(parity_path.read_text(encoding="utf-8"))
        if "ecology/index.html" not in parity.get("currentSurfaces", []):
            findings.append(
                "12_PUBLIC_SITE/public_semantic_parity.json: ecology surface unregistered"
            )
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"12_PUBLIC_SITE/public_semantic_parity.json: {exc}")

    if findings:
        print("trophic_rosetta_doctrine: FAILED")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(
        "trophic_rosetta_doctrine: clean "
        f"({len(LIVE_OWNERS)} owners, {len(PROJECTION_FILES)} projections, "
        f"{len(ids)} ledger candidates)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

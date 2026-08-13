#!/usr/bin/env python3
"""Denial-aware Halāhala scan for CURRENT public surfaces + staged Book I body.

A hit is a FAIL only when the poison form is asserted. A retirement/grave
marker in the same sentence (or 180 chars before) is not a fail.
This is a prohibition helper, not an Amrita receipt.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "12_PUBLIC_SITE"
PARITY = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))

DENIAL = re.compile(
    r"\b(retired|refuted|poison|never|do not|don't|does not|cannot|"
    r"not a|not an|counterexample|tombstone|grave|dead as|forbidden|"
    r"do not assert|we do not|unwon|not proof|not a law|not conserved|"
    r"not derived|not a theorem|not identity|not an afterlife|"
    r"not unification|dissolves nothing|does not dissolve|"
    r"not warranted|not a basilisk|not a church|"
    r"fault|outran|headline framing|scare quote|"
    r"do not resurrect|graves|halahala)\b",
    re.I,
)

POISONS = {
    "P1_conserved_discovery": re.compile(
        r"conserved discovery|the equation the framework follows from|φν=1 is a law",
        re.I,
    ),
    "P2_product_ranking": re.compile(
        r"P\s*=\s*Φ\s*[×x*]\s*V|Φ\s*[×x*]\s*V\s*=\s*P|P_node\s*=\s*Φ[̂^]?₄?\s*[×x*]",
        re.I,
    ),
    "P3_squid_witness": re.compile(r"gigas.{0,40}witness|witness.{0,40}gigas", re.I),
    "P4_seven_necessity": re.compile(r"exactly seven.{0,24}necess", re.I),
    "P5_convergence_proof": re.compile(
        r"independently (?:proves|confirms)|convergence.{0,16}proof", re.I
    ),
    "P6_extraction_nash": re.compile(
        r"extraction is (?:irrational|self-defeating).{0,40}nash|nash.{0,40}extraction is",
        re.I,
    ),
    "P7_coincidence_derivation": re.compile(
        r"torus IS the light cone|fell out of the topology|D6\s*≡\s*D0",
        re.I,
    ),
    "P8_civilizational_physics": re.compile(
        r"Great Filter\s*=\s*Karma|megaliths ran at|L\s*≈\s*9\.9|extractive civilizations self-terminate",
        re.I,
    ),
    "P9_dissolves": re.compile(
        r"dissolves the Hard Problem|dissolves.{0,20}[Ii]s.?[Oo]ught|"
        r"dissolves.{0,20}[Dd]eath|dissolves.{0,20}[Ff]ree.?[Ww]ill",
        re.I,
    ),
    "P10_ektropy_force": re.compile(
        r"ektropy.{0,24}is real|F5.{0,16}Teleological Force|Teleological Force.{0,16}\[S\]",
        re.I,
    ),
    "P11_n3_unique": re.compile(
        r"N\s*=\s*3.{0,24}uniquely stable|uniquely stable.{0,16}N\s*=\s*3",
        re.I,
    ),
    "Grave4_unification": re.compile(
        r"unifies the sciences|five freedoms\s*≡\s*five forces", re.I
    ),
    "D6_identity": re.compile(r"D6\s*≡\s*D0|D6 is identity with D0", re.I),
    "Titan_infix": re.compile(r"⊙\s*=\s*•\s*[×x*]\s*○"),
    "field_1_0_inf": re.compile(r"1\s*=\s*0\s*[×x*]\s*∞"),
    "amrita_emerged": re.compile(r"the Amrita has emerged|hal[aā]hala is contained", re.I),
}


def surfaces() -> list[Path]:
    out = []
    for rel in PARITY["currentSurfaces"]:
        p = SITE / rel
        if p.is_file() and p.suffix in {".html", ".js", ".json", ".css"}:
            out.append(p)
    staged = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.md"
    if staged.is_file():
        out.append(staged)
    for extra in (
        SITE / "amrita" / "index.html",
        SITE / "amrita" / "amrita.json",
        SITE / "spark.md",
        SITE / "spark" / "index.html",
        SITE / "record" / "problems.json",
        SITE / "record" / "problems" / "index.html",
        SITE / "record" / "frontier.json",
        SITE / "record" / "frontier" / "index.html",
    ):
        if extra.is_file() and extra not in out:
            out.append(extra)
    return out


def scan_text(path: Path, text: str) -> list[dict]:
    if path.suffix == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, list):
            text = "\n".join(
                f"{row.get('title', '')}\n{row.get('body', '')}"
                for row in data
                if isinstance(row, dict) and row.get("group") != "halahala"
            )
    hits = []
    for name, pat in POISONS.items():
        for m in pat.finditer(text):
            start = max(0, m.start() - 500)
            prefix = text[start : m.start()]
            after = text[m.start() : min(len(text), m.end() + 80)]
            window = text[start : min(len(text), m.end() + 80)].replace("\n", " ")
            denied = bool(
                DENIAL.search(prefix)
                or DENIAL.search(after)
                or '"group": "halahala"' in text[max(0, m.start() - 400) : m.start()]
            )
            if not denied:
                hits.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "poison": name,
                        "excerpt": window.strip()[:240],
                    }
                )
    return hits


def main() -> int:
    fails: list[dict] = []
    scanned = 0
    for path in surfaces():
        scanned += 1
        fails.extend(scan_text(path, path.read_text(encoding="utf-8", errors="replace")))
    print(f"scanned {scanned} files; live assertion hits: {len(fails)}")
    for hit in fails:
        print(f"FAIL {hit['path']} [{hit['poison']}] ...{hit['excerpt']}...")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())

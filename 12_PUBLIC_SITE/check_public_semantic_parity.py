#!/usr/bin/env python3
"""Fail closed when current public pages drift from the pure dimension-first owners."""

from __future__ import annotations

import json
import hashlib
import fnmatch
import re
import subprocess
import sys
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
MANIFEST_PATH = SITE / "public_semantic_parity.json"
EXPECTED_SEQUENCE = ["D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3", "D4", "mu4", "D5", "b6", "D6", "r6", "D0"]
FORBIDDEN = {
    "literal D6 identity": re.compile(r"D6\s*(?:≡|=)\s*D0"),
    "extra mu crossing": re.compile(r"μ[56]|mu[56]", re.I),
    "invalid scalar sampling": re.compile(r"Sample\s*\[\s*∫[^\]]*\|ψ\|²"),
    "physical cone inflation": re.compile(r"physical (?:light )?cone (?:expands|widens)", re.I),
    "quantum dimensional stacking": re.compile(r"(?:Everett.{0,70}(?:five-dimensional|5D)|Copenhagen.{0,70}(?:four-dimensional|4D))", re.I | re.S),
    "quantum-gravity solution inflation": re.compile(r"(?<!not )(?<!no )(?:solve[sd]?|solution to) quantum gravity", re.I),
    "zero-momentum D3 inflation": re.compile(r"D3 has no momentum", re.I),
    "application authority leakage": re.compile(r"(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])", re.I),
    "legacy public Phi definition": re.compile(r"Φ\s+is\s+(?:a\s+)?present\s+(?:measurement|assessment)|present\s+measurement\s+of\s+D5", re.I),
    "legacy untyped node scalar": re.compile(r"P(?:_|<sub>)?node(?:</sub>)?(?:\s*,?\s*i)?", re.I),
    "raw uncalibrated Phi-V product": re.compile(r"(?:Φ|&Phi;)\s*(?:×|x|\*)\s*V\b", re.I),
    "legacy aggregate objective": re.compile(r"(?:Σ|sum)\s*Δ\s*P(?:_|<sub>)?node", re.I),
    "product-derived ethics": re.compile(
        r"(?:(?:P(?:_|<sub>)?node(?:</sub>)?|(?:Φ|&Phi;)\s*(?:×|x|\*)\s*V).{0,1400}"
        r"(?:objective|derived|structural)\s+(?:ethic|ethics|dharma)|"
        r"(?:objective|derived|structural)\s+(?:ethic|ethics|dharma).{0,1400}"
        r"(?:P(?:_|<sub>)?node(?:</sub>)?|(?:Φ|&Phi;)\s*(?:×|x|\*)\s*V))",
        re.I | re.S,
    ),
    "derived ethic inflation": re.compile(r"ethic(?:s)?\s+(?:falls?|follow(?:s|ed)?)\s+(?:directly\s+)?(?:out\s+of|from)\s+(?:the\s+)?arithmetic", re.I),
    "exclusive ethic inflation": re.compile(r"the only lawful move", re.I),
    "field arithmetic fable": re.compile(r"One equals Nothing times Everything", re.I),
    "forbidden Titan infix arithmetic": re.compile(
        r"(?:⊙\s*=\s*•\s*(?:×|x|\*)\s*○|"
        r"•\s*(?:×|x|\*)\s*○\s*(?:=|→)\s*⊙|"
        r"1\s*=\s*0\s*(?:×|x|\*)\s*∞)"
    ),
    "retired evidence tier": re.compile(r"\[E\]"),
}

REQUIRED_PUBLIC_CONTRACTS = {
    "index.html": ("A worldview for finite beings", "Frame one decision"),
    "plainly/index.html": ("possible power", "actual power", "componentwise Pareto", "calibration contract"),
    "practice/index.html": ("Finity Card", "Φ₅", "V₄"),
    "rosetta/index.html": ("One move, translated", "G7", "possible power", "actual power"),
    "contribute/index.html": ("does not accept payment", "does not yet accept payments"),
}
REQUIRED_SURFACE_CARDS = {
    "index.html": {"FIN01-01", "OS01-13", "OS01-20", "OS01-22", "OS01-26"},
    "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
    "lab/index.html": {"FIN01-01", "FIN01-02"},
    "compass/index.html": {"OS01-09"},
    "5/index.html": {"OS01-09"},
    "plainly/index.html": {"OS01-09"},
    "discoveries/nonduality/index.html": {"OS01-09"},
    "about/index.html": {"OS01-09"},
    "read/index.html": {"OS01-09"},
    "axioms/index.html": {"OS01-09"},
    "journey/index.html": {"OS01-09"},
    "rosetta/index.html": {"OS01-09"},
    "book/index.html": {"OS01-09"},
}

NEGATIVE_PRODUCT_RECORDS = {"axioms/index.html", "record/index.html"}


def _sha256_revision(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _vercelignore_patterns() -> list[str]:
    return [
        line.strip() for line in (SITE / ".vercelignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _ignored(rel: str, patterns: list[str]) -> bool:
    ignored = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw = pattern[1:] if negated else pattern
        if raw.endswith("/"):
            prefix = raw.rstrip("/")
            matched = rel == prefix or rel.startswith(prefix + "/")
        elif "/" not in raw:
            matched = fnmatch.fnmatch(Path(rel).name, raw) or fnmatch.fnmatch(rel, raw)
        else:
            matched = fnmatch.fnmatch(rel, raw.lstrip("/"))
        if matched:
            ignored = not negated
    return ignored


def main() -> int:
    errors: list[str] = []
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 2:
        errors.append("public semantic parity schemaVersion must be 2")
    contract = data.get("claimCardContract", {})
    required_contract = ("ledger", "register", "graph", "source", "sourceRevision", "lifecycle", "publicDisposition")
    for key in required_contract:
        if not contract.get(key):
            errors.append(f"claim-card contract missing {key}")
    claim_ids: set[str] = set()
    card_lookup: dict[str, dict] = {}
    ledger_path = ROOT / contract.get("ledger", "__missing__")
    if ledger_path.is_file():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        for card in ledger.get("cards", []):
            card_id = card.get("card_id")
            if card_id in card_lookup:
                errors.append(f"duplicate claim-card ID in public ledger: {card_id}")
            elif card_id:
                card_lookup[card_id] = card
                claim_ids.add(card_id)
    else:
        errors.append(f"missing claim-card ledger: {contract.get('ledger')}")
    register_lookup: dict[str, dict] = {}
    for key in ("register", "graph"):
        path = ROOT / contract.get(key, "__missing__")
        if not path.is_file():
            errors.append(f"missing claim-card {key}: {contract.get(key)}")
            continue
        if key == "register":
            register = json.loads(path.read_text(encoding="utf-8"))
            for row in register.get("cards", []):
                card_id = row.get("card_id")
                if not card_id:
                    errors.append("claim-card register contains a row without card_id")
                elif card_id in register_lookup:
                    errors.append(f"duplicate claim-card ID in derived register: {card_id}")
                else:
                    register_lookup[card_id] = row
    source_path = ROOT / contract.get("source", "__missing__")
    if source_path.is_file():
        actual_revision = _sha256_revision(source_path)
        if contract.get("sourceRevision") != actual_revision:
            errors.append("claim-card contract sourceRevision drift")
    else:
        errors.append(f"missing claim-card source: {contract.get('source')}")
    if contract.get("lifecycle") != "reader_synthesis":
        errors.append("public claim-card lifecycle must remain reader_synthesis")
    if contract.get("publicDisposition") != "bounded_current":
        errors.append("public claim-card disposition must remain bounded_current")
    if data.get("sequence") != EXPECTED_SEQUENCE:
        errors.append("dimension sequence is not the canonical D0/mu0...D6/r6 order")
    levels = data.get("levels", [])
    if [x.get("id") for x in levels] != [f"D{i}" for i in range(7)]:
        errors.append("levels must be exactly D0 through D6")
    crossings = [x.get("transition", {}).get("id") for x in levels if "transition" in x]
    if crossings != ["mu0", "mu1", "mu2", "mu3", "mu4", "b6"]:
        errors.append("transitions must be exactly mu0..mu4 plus b6")
    if levels[4].get("modality") != "actual" or levels[5].get("modality") != "possible":
        errors.append("D4 must be actual and D5 possible")
    for item in levels:
        for key in ("claimCardIds", "sourceRevision", "lifecycle", "publicDisposition"):
            if not item.get(key):
                errors.append(f"{item.get('id', '?')} missing claim-card parity field {key}")
        if item.get("lifecycle") != contract.get("lifecycle"):
            errors.append(f"{item.get('id', '?')} claim-card lifecycle drift")
        if item.get("publicDisposition") != contract.get("publicDisposition"):
            errors.append(f"{item.get('id', '?')} public disposition drift")
        for card_id in item.get("claimCardIds", []):
            if card_id not in claim_ids:
                errors.append(f"{item.get('id', '?')} binds unknown claim-card {card_id}")
                continue
            state = card_lookup[card_id].get("public", {}).get("state")
            if state not in {"bounded_current", "candidate"}:
                errors.append(f"{item.get('id', '?')} binds non-current claim-card {card_id} ({state})")
        source = ROOT / item["source"]
        if source.is_file():
            if item.get("sourceRevision") != _sha256_revision(source):
                errors.append(f"{item.get('id', '?')} sourceRevision drift: {item['source']}")
        else:
            errors.append(f"missing source owner: {item['source']}")
        if "transition" in item:
            tr = item["transition"]
            for key in ("source", "sourceRevision", "saturation", "capability", "recovery", "evidence", "prediction", "alternatives", "kill"):
                if not tr.get(key):
                    errors.append(f"{tr.get('id', '?')} missing {key}")
            transition_source = ROOT / tr["source"]
            if transition_source.is_file():
                if tr.get("sourceRevision") != _sha256_revision(transition_source):
                    errors.append(f"{tr.get('id', '?')} sourceRevision drift: {tr['source']}")
            else:
                errors.append(f"missing crossing owner: {tr['source']}")
        rendered = (SITE / item["id"][1:] / "index.html").read_text(encoding="utf-8", errors="replace")
        for needle, label in (
            ('class="diagram visual-panel"', "instrument visual hook"),
            ('type="importmap"', "local Three.js import map"),
            ('type="module" src="../dimensions/dimensions.js"', "module instrument loader"),
            ('class="number-nav"', "accessible spaced navigation"),
        ):
            if needle not in rendered:
                errors.append(f"{item['id']} missing {label}")

    surface_claims = data.get("surfaceClaims", [])
    surface_lookup: dict[str, dict] = {}
    for binding in surface_claims:
        surface = binding.get("surface")
        if not surface:
            errors.append("surface claim binding missing surface")
            continue
        if surface in surface_lookup:
            errors.append(f"duplicate surface claim binding: {surface}")
            continue
        surface_lookup[surface] = binding
        for key in (
            "role", "claimCardIds", "claimSources", "publicDisposition",
            "requiredMarkers",
        ):
            if not binding.get(key):
                errors.append(f"{surface} surface claim binding missing {key}")
        if surface not in data.get("currentSurfaces", []):
            errors.append(f"surface claim binding is not a current surface: {surface}")
        if binding.get("publicDisposition") != "bounded_current":
            errors.append(f"{surface} surface disposition must remain bounded_current")
        page = SITE / surface
        rendered = page.read_text(encoding="utf-8", errors="replace") if page.is_file() else ""
        for marker in binding.get("requiredMarkers", []):
            if marker not in rendered:
                errors.append(f"{surface} missing bound public marker {marker!r}")
        if len(binding.get("claimCardIds", [])) != len(set(binding.get("claimCardIds", []))):
            errors.append(f"{surface} repeats a claim-card ID")
        source_bound_cards: set[str] = set()
        source_paths: set[str] = set()
        for source_binding in binding.get("claimSources", []):
            for key in ("source", "sourceRevision", "lifecycle", "claimCardIds"):
                if not source_binding.get(key):
                    errors.append(f"{surface} claim source binding missing {key}")
            source_rel = source_binding.get("source", "__missing__")
            if source_rel in source_paths:
                errors.append(f"{surface} repeats claim source {source_rel}")
            source_paths.add(source_rel)
            source = ROOT / source_rel
            if source.is_file():
                actual_revision = _sha256_revision(source)
                if source_binding.get("sourceRevision") != actual_revision:
                    errors.append(f"{surface} claim sourceRevision drift: {source_rel}")
            else:
                errors.append(f"{surface} claim source is missing: {source_rel}")
            for card_id in source_binding.get("claimCardIds", []):
                if card_id in source_bound_cards:
                    errors.append(f"{surface} binds {card_id} to more than one source")
                source_bound_cards.add(card_id)
                row = register_lookup.get(card_id)
                if row is None:
                    continue
                if row.get("source_path") != source_rel:
                    errors.append(
                        f"{surface} source mismatch for {card_id}: "
                        f"{source_rel} != {row.get('source_path')}"
                    )
                if row.get("source_lifecycle") != source_binding.get("lifecycle"):
                    errors.append(f"{surface} lifecycle mismatch for {card_id}")
        if source_bound_cards != set(binding.get("claimCardIds", [])):
            errors.append(
                f"{surface} claimSources do not cover the declared claim-card set"
            )
        for card_id in binding.get("claimCardIds", []):
            row = register_lookup.get(card_id)
            if row is None:
                errors.append(f"{surface} binds unknown registered claim-card {card_id}")
                continue
            if row.get("public_state") not in {"bounded_current", "candidate"}:
                errors.append(
                    f"{surface} binds non-current registered claim-card {card_id} "
                    f"({row.get('public_state')})"
                )
            source_path = ROOT / row.get("source_path", "__missing__")
            if not source_path.is_file():
                errors.append(f"{surface} claim-card source is missing for {card_id}")
    for surface, expected_cards in REQUIRED_SURFACE_CARDS.items():
        binding = surface_lookup.get(surface)
        if binding is None:
            errors.append(f"missing required surface claim binding: {surface}")
            continue
        actual_cards = set(binding.get("claimCardIds", []))
        if actual_cards != expected_cards:
            errors.append(
                f"{surface} claim-card set drift: expected {sorted(expected_cards)}, "
                f"got {sorted(actual_cards)}"
            )

    current = set(data.get("currentSurfaces", []))
    infrastructure = set(data.get("currentInfrastructureSurfaces", []))
    frozen_legacy = set(data.get("frozenLegacySurfaces", []))
    frozen_roots = set(data.get("frozenLibraryRoots", []))
    withheld_data = json.loads((SITE / "withheld-routes.json").read_text(encoding="utf-8"))
    withheld = {row.get("artifact") for row in withheld_data.get("artifacts", [])}
    for label, values in (
        ("current surface", current),
        ("current infrastructure surface", infrastructure),
        ("frozen legacy surface", frozen_legacy),
        ("withheld surface", withheld),
    ):
        if None in values or len(values) != len(list(values)):
            errors.append(f"{label} registry contains an invalid entry")
        for rel in values:
            if not (SITE / rel).is_file():
                errors.append(f"missing declared {label}: {rel}")
    conflicting = (current | infrastructure) & (frozen_legacy | withheld)
    for rel in sorted(conflicting):
        errors.append(f"current surface also classified as frozen or withheld: {rel}")
    patterns = _vercelignore_patterns()
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE).as_posix()
        if rel in withheld:
            category = "withheld"
        elif _ignored(rel, patterns):
            continue
        elif rel in current:
            category = "current"
        elif rel in infrastructure:
            category = "infrastructure"
        elif rel in frozen_legacy or rel.split("/", 1)[0] in frozen_roots:
            category = "frozen"
        else:
            errors.append(f"unclassified deployable HTML route: {rel}")
            continue
        if category == "frozen":
            frozen_text = path.read_text(encoding="utf-8", errors="replace")
            if 'name="robots" content="noindex, follow"' not in frozen_text:
                errors.append(f"frozen route lacks explicit noindex marker: {rel}")
            if 'data-frozen-library-boundary="2026-07-22"' not in frozen_text:
                errors.append(f"frozen route lacks provenance boundary marker: {rel}")

    profile_surfaces = {
        rel for rel in current
        if rel.endswith(".html") and (SITE / rel).is_file()
        and "N_node" in (SITE / rel).read_text(encoding="utf-8", errors="replace")
    }
    missing_profile_bindings = sorted(profile_surfaces - set(REQUIRED_SURFACE_CARDS))
    for rel in missing_profile_bindings:
        errors.append(f"typed node-profile surface lacks an OS01-09 claim binding: {rel}")

    for rel in data.get("currentSurfaces", []):
        path = SITE / rel
        if not path.is_file():
            errors.append(f"missing current public surface: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN.items():
            if name == "application authority leakage" and rel == "record/index.html" and "data-historical-authority-boundary" in text:
                continue
            if name == "retired evidence tier" and rel == "record/index.html" and "data-historical-authority-boundary" in text:
                continue
            if name in {
                "legacy untyped node scalar",
                "raw uncalibrated Phi-V product",
                "legacy aggregate objective",
                "product-derived ethics",
            } and rel in NEGATIVE_PRODUCT_RECORDS:
                continue
            scan_text = text
            if name == "quantum-gravity solution inflation":
                scan_text = re.sub(r"does not.{0,240}solve quantum gravity", "", scan_text, flags=re.I | re.S)
            if pattern.search(scan_text):
                errors.append(f"{rel}: {name}")
    for rel, alternatives in REQUIRED_PUBLIC_CONTRACTS.items():
        path = SITE / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if rel == "contribute/index.html":
            if not any(needle in text for needle in alternatives):
                errors.append(f"{rel}: missing static no-payment boundary")
            continue
        for needle in alternatives:
            if needle not in text:
                errors.append(f"{rel}: missing founder contract marker {needle!r}")
    render = subprocess.run([sys.executable, str(SITE / "render_dimension_site.py"), "--check"], cwd=SITE, text=True, capture_output=True)
    if render.returncode:
        errors.append(render.stdout.strip() or render.stderr.strip() or "dimension renderer drift")
    frozen = subprocess.run([sys.executable, str(SITE / "apply_frozen_library_boundary.py"), "--check"], cwd=SITE, text=True, capture_output=True)
    if frozen.returncode:
        errors.append(frozen.stdout.strip() or frozen.stderr.strip() or "frozen library boundary drift")
    barred = subprocess.run(
        [sys.executable, str(ROOT / "09_TOOLS/01_SCRIPTS/check_barred_claims.py"), "--scope", "public"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if barred.returncode:
        errors.append(barred.stdout.strip() or barred.stderr.strip() or "public barred-claim gate failed")
    rag = json.loads((SITE / "book/rag_index.json").read_text(encoding="utf-8"))
    excluded_routes = {
        "/" + rel[:-10]
        for rel in frozen_legacy | withheld
        if rel.endswith("index.html")
    }
    for passage in rag.get("passages", []):
        passage_id = str(passage.get("id", ""))
        href = str(passage.get("href", ""))
        if passage_id.startswith(tuple(f"{root}:" for root in frozen_roots)) or any(
            href == route or href.startswith(route + "/") or href.startswith(route + "#")
            for route in excluded_routes
        ):
            errors.append(f"frozen or withheld passage remains in RAG: {passage_id}")
            break
    if errors:
        print("PUBLIC SEMANTIC PARITY: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"PUBLIC SEMANTIC PARITY: PASS ({len(levels)} levels, 5 mu crossings, 1 boundary, 1 return)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

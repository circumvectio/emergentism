#!/usr/bin/env python3
"""Fail closed when current or provisional public pages drift from their owners."""

from __future__ import annotations

import json
import hashlib
import html as html_lib
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
MANIFEST_PATH = SITE / "public_semantic_parity.json"
# Use the exact same deployment-boundary semantics as the release gate.  A
# second, weaker glob implementation here would let deployable legacy HTML
# evade the public semantic firewall.
if str(SITE) not in sys.path:
    sys.path.insert(0, str(SITE))
from predeploy_check import is_vercel_ignored, load_vercelignore_patterns

EXPECTED_SEQUENCE = ["D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3", "D4", "mu4", "D5", "b6", "D6", "r6", "D0"]
FORBIDDEN = {
    # --- added 2026-07-22 after a Rosetta caste sweep found the sharpest tier
    # violation on the site sitting INSIDE the scanned bytes while this gate
    # reported PASS. plainly/index.html asserted the product form as settled and
    # derived the extraction ethic from it — CC-CORE-1, which the K-5 owner
    # forbids ("selected [I/S], not forced by the reciprocal chart"). The gate
    # could not see it because it had no pattern for this class.
    "product uniqueness asserted as settled": re.compile(
        r"they\s+multiply(?![^.]*(?:unproven|not\s+earned|selected|wager))"
        r"|because\s+they\s+multiply"
        r"|must\s+multiply(?![^.]*(?:unproven|turned\s+out|downgrad))", re.I),
    "ethic derived from arithmetic": re.compile(
        r"what\s+the\s+multiplication\s+says"
        r"|(?:ethic|ought|morality)\s+(?:falls?\s+out|follows?)\s+(?:from\s+)?"
        r"(?:as\s+)?(?:the\s+)?(?:arithmetic|multiplication|geometry|maths?|math)"
        r"|(?:arithmetic|multiplication|the\s+sphere)\s+prov(?:es|ed)\s+"
        r"(?:the\s+)?(?:good|ethic|justice)", re.I),

    "literal D6 identity": re.compile(r"D6\s*(?:≡|=)\s*D0"),
    "extra mu crossing": re.compile(r"μ[56]|mu[56]", re.I),
    "invalid scalar sampling": re.compile(r"Sample\s*\[\s*∫[^\]]*\|ψ\|²"),
    "physical cone inflation": re.compile(r"physical (?:light )?cone (?:expands|widens)", re.I),
    "quantum dimensional stacking": re.compile(r"(?:Everett.{0,70}(?:five-dimensional|5D)|Copenhagen.{0,70}(?:four-dimensional|4D))", re.I | re.S),
    "quantum-gravity solution inflation": re.compile(r"(?<!not )(?<!no )(?:solve[sd]?|solution to) quantum gravity", re.I),
    "zero-momentum D3 inflation": re.compile(r"D3 has no momentum", re.I),
    "application authority leakage": re.compile(r"(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])", re.I),
    "legacy public Phi definition": re.compile(r"Φ\s+is\s+(?:a\s+)?present\s+(?:measurement|assessment)|present\s+measurement\s+of\s+D5", re.I),
    "legacy untyped node product": re.compile(r"P\s*=\s*Φ\s*(?:×|x|\*)\s*V"),
    # This pattern is applied to normalized visible text, not raw HTML. Tags,
    # entities, combining hats, and Unicode subscripts may not hide a retired
    # product assignment from the public gate.
    "retired node product assignment": re.compile(
        r"\bP[\s_]*node\s*(?::=|=)\s*"
        r"Φ(?:\s*\u0302)?(?:[\s_]*4)?\s*"
        r"(?:(?:×|x|\*|·)\s*)?V(?:[\s_]*4)?\b",
        re.I,
    ),
    "stale current 25-chapter reader": re.compile(
        r"25\s*(?:-|\s)\s*chapters?(?:\s*\+\s*3\s*appendices)?|25-chapter\s+book",
        re.I,
    ),
    "withheld Reciprocal routed as current book": re.compile(
        r"<a\b[^>]*href=[\"'][^\"']*book/[^\"']*[\"'][^>]*>\s*The\s+Reciprocal\s*</a>",
        re.I | re.S,
    ),
    "derived ethic inflation": re.compile(r"ethic(?:s)?\s+(?:falls?|follow(?:s|ed)?)\s+(?:directly\s+)?(?:out\s+of|from)\s+(?:the\s+)?arithmetic", re.I),
    "exclusive ethic inflation": re.compile(r"the only lawful move", re.I),
    "field arithmetic fable": re.compile(r"One equals Nothing times Everything", re.I),
    # The glyphs are opaque TitanFrame renderings. The reciprocal chart has its
    # own numeric identity, but no fence, coupling, or analogy turns that fact
    # into an infix operation over Titan terms. Affirmative public copy bans
    # the symbol equation; an explicitly retired mention may preserve negative
    # evidence when its lifecycle marker comes first.
    "forbidden Titan infix arithmetic": re.compile(
        r"(?:⊙\s*=\s*•\s*(?:×|x|\*)\s*○|"
        r"•\s*(?:×|x|\*)\s*○\s*(?:=|→)\s*⊙)"
    ),
    # The FIELD form is the thing D0 denies outright: no field theorem says 0 times
    # infinity equals 1. NEVER escapable, at any tier, with any fence.
    "field arithmetic claim": re.compile(r"1\s*=\s*0\s*(?:×|x|\*)\s*∞"),
    "retired evidence tier": re.compile(r"\[E\]"),
}

REQUIRED_PUBLIC_CONTRACTS = {
    "index.html": (
        "A worldview for finite beings",
        "Fluency is not emergence",
        "Enter the Spark",
        "Frame one decision",
        "A criterion on trial",
    ),
    "spark/index.html": (
        "Ontology-churn instrument",
        "Nothing promotes itself",
        "No model validates itself",
        "Current disposition · raised [C] → not-well-posed",
    ),
    "record/problems/index.html": (
        "VIS-00 publishing aim",
        "W10-SPARK mechanism under test",
        "W0-COMPLETE <strong>NOT-WELL-POSED</strong>",
    ),
    "record/frontier/index.html": (
        "W10-SPARK <span>open · OPEN-EMPIRICAL</span>",
        "W0-COMPLETE <span>open · NOT-WELL-POSED</span>",
    ),
    "plainly/index.html": ("possible power", "actual power", "chosen AND-class convention"),
    "practice/index.html": ("Finity Card", "Φ₅", "V₄"),
    "rosetta/index.html": ("One move, translated", "G7", "possible power", "actual power"),
    "manifesto/index.html": (
        "Filing alone does not establish independent evidence, peer review, validation,",
        "does not automatically enter the",
    ),
    "contribute/index.html": (
        "does not accept payments, credentials, private data, or live model jobs.",
        "No study, funding programme, grant scheme, compute service, or private-data intake is open.",
        "Filing alone does not establish independent review, validation, or a tier upgrade",
    ),
    "record/index.html": (
        "Filing alone does not establish independent evidence, peer review, validation, or a claim-tier upgrade.",
    ),
    "lab/index.html": (
        "All twelve named GP gates have packet-complete research contracts",
        "none is evidence-complete",
        "public routing state",
    ),
}
PUBLIC_ISSUE_FORM_ROUTE = "github.com/circumvectio/emergentism/issues/new"
AUTOMATIC_SUBMISSION_PROMISES = (
    "will be published unedited",
    "with your verdict and not ours",
    "the claim gets marked cut",
    "so what would actually count",
    "because it can move a claim",
)
REQUIRED_SURFACE_CARDS = {
    "index.html": {"FIN01-01", "OS01-02", "OS01-08", "OS01-13", "OS01-20", "OS01-22", "OS01-23", "OS01-26"},
    "spark/index.html": {"OS01-02", "OS01-08", "OS01-13", "OS01-23", "OS01-26"},
    "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
    "lab/index.html": {"FIN01-01", "FIN01-02"},
    "compass/index.html": {"OS01-13"},
    "5/index.html": {"OS01-09"},
    "plainly/index.html": {"OS01-09"},
    "discoveries/nonduality/index.html": {"OS01-09"},
    "about/index.html": {"OS01-26"},
    "read/index.html": {"OS01-13"},
    "axioms/index.html": {"OS01-26"},
    "journey/index.html": {"OS01-09"},
    "rosetta/index.html": {"OS01-11"},
    "book/index.html": {"OS01-13"},
}
CURRENT_AND_CLASS_MARKERS = {
    "discoveries/nonduality/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "about/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "read/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "journey/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
    "rosetta/index.html": ("P_node := min(Φ̂₄, V₄)", "historical product ranking is retired"),
}
NODE_PRODUCT_REJECT_FIXTURES = (
    "P_node = Φ̂₄V₄",
    "P_node := Φ̂₄ × V₄",
    "P<sub>node</sub> = &Phi;&#770;<sub>4</sub>V<sub>4</sub>",
    "P<sub>node</sub> <span>=</span> &Phi;&#770;<sub>4</sub> &times; V<sub>4</sub>",
    "P_node = <span>Φ̂₄</span> &#215; V₄",
    "Pₙₒdₑ = Φ̂₄ × V₄",
)
NODE_PRODUCT_BOUNDED_FIXTURES = (
    "P_node := min(Φ̂₄, V₄)",
    "Historical Φ̂₄V₄ names conjunction only; product ranking is retired.",
)
TITAN_INFIX_REJECT_FIXTURES = (
    "⊙ = • × ○",
    "<span>⊙</span> = <b>•</b> &times; ○",
    "• * ○ → ⊙",
)
TITAN_OPERATOR_FREE_FIXTURES = (
    "•  ⊙  ○",
    "TitanFrame := 0_T | 1_T | ∞_T",
)
LIFECYCLE_AWARE_FORBIDDEN = {
    "literal D6 identity",
    "legacy untyped node product",
    "retired node product assignment",
}
# A repair/retirement marker must precede the quoted form in the same sentence.
# A later disclaimer cannot launder an affirmative formula.
LIFECYCLE_PREFIX = re.compile(
    r"(?:\b(?:retired|withdrawn|refuted|struck|killed|banned|ill-typed|ill typed)\b"
    r"[^.;:!?]{0,80}|\bno\s+(?:literal\s+)?identity\b[^.;:!?]{0,80})$",
    re.I,
)
LIFECYCLE_FIXTURES = {
    "literal D6 identity": "D6 ≡ D0",
    "legacy untyped node product": "P = Φ × V",
    "retired node product assignment": "P_node := Φ̂₄ × V₄",
}
CURRENT_BOOK_MARKERS = {
    "book/index.html": (
        "Only a declared common strictly increasing reparameterization applied to both factors is assumed here:",
        "independently reparameterized factor scales do not license an invariant cross-factor scalar ranking",
        "GP-03 remains open.",
    ),
    "manifesto/index.html": (
        "The One-Sitting Reader",
        "readable now &mdash; 12 chapters",
        "withheld, not current",
        "not the current <code>/book/</code> source",
    ),
    "read/index.html": (
        "Frozen generated-library records remain preserved with provenance",
        "current twelve-chapter One-Sitting Reader",
    ),
}
HIDDEN_ROBOTS_META = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\'][^"\']*\b(?:noindex|none)\b)[^>]*>',
    re.IGNORECASE,
)
FROZEN_LIBRARY_BOUNDARY_MARKER = "data-frozen-library-boundary"


def normalize_visible_text(text: str) -> str:
    """Return semantic text so routine HTML cannot bypass claim guards."""
    unescaped = html_lib.unescape(text)
    without_tags = re.sub(r"<[^>]*>", " ", unescaped)
    normalized = unicodedata.normalize("NFKC", without_tags)
    return re.sub(r"\s+", " ", normalized).strip()


def has_retired_node_product(text: str) -> bool:
    return bool(
        FORBIDDEN["retired node product assignment"].search(
            normalize_visible_text(text)
        )
    )


def has_titan_infix(text: str) -> bool:
    return bool(
        FORBIDDEN["forbidden Titan infix arithmetic"].search(
            normalize_visible_text(text)
        )
    )


def record_has_only_historical_k2(text: str) -> bool:
    """Allow the existing provenance label, not a blanket record-page waiver."""

    if "data-historical-authority-boundary" not in text:
        return False
    matches = list(FORBIDDEN["application authority leakage"].finditer(text))
    return bool(matches) and all(match.group(0).casefold() == "k2" for match in matches)


STATUS_SOURCE_CONTRACTS = {
    "00_THE_KERNEL_INDEX.md": "[I]",
    "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md": "[S/B]",
    "00_META/ADJUDICATION_SPARK_AND_COMPLETENESS_2026_08_13.md": "[S]",
    "00_META/claim_status/CLAIM_STATUS.yaml": "[S]",
}
REQUIRED_STATUS_SOURCE_SURFACES = {
    "index.html",
    "about/index.html",
    "spark/index.html",
    "record/problems/index.html",
    "record/frontier/index.html",
}
REQUIRED_STATUS_SOURCE_BINDING_IDS = {
    "KERNEL-STATUS-HOME",
    "CONTACT-STATUS-HOME",
    "HOME-SPARK-ADJUDICATION",
    "KERNEL-STATUS-ABOUT",
    "CONTACT-STATUS-ABOUT",
    "SPARK-ADJUDICATION",
    "PROBLEMS-ADJUDICATION",
    "FRONTIER-CLAIM-STATUS",
}


def parity_audit_surfaces(data: dict) -> list[str]:
    """Return every current/provisional surface subject to prohibition scans."""
    current = data.get("currentSurfaces")
    provisional_block = data.get("declaredProvisional")
    if not isinstance(current, list) or not all(
        isinstance(item, str) for item in current
    ):
        raise ValueError("currentSurfaces must be a list of paths")
    if not isinstance(provisional_block, dict) or not isinstance(
        provisional_block.get("routes"), list
    ) or not all(isinstance(item, str) for item in provisional_block["routes"]):
        raise ValueError("declaredProvisional.routes must be a list of paths")
    combined = current + provisional_block["routes"]
    if len(combined) != len(set(combined)):
        raise ValueError("current and provisional public surfaces must be disjoint")
    return combined

NEGATIVE_PRODUCT_RECORDS = {"axioms/index.html", "record/index.html"}


def _sha256_revision(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def deployable_html_surfaces() -> list[str]:
    """Return every HTML artifact Vercel may receive under .vercelignore."""

    patterns = load_vercelignore_patterns()
    if patterns is None:
        raise ValueError(".vercelignore is required to determine deployable HTML")
    surfaces: list[str] = []
    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
            continue
        rel = path.relative_to(SITE).as_posix()
        if not is_vercel_ignored(rel, patterns):
            surfaces.append(rel)
    return sorted(surfaces)


def withheld_public_routes() -> set[str]:
    """Read the exact withheld-route policy for RAG custody checks."""

    registry_path = SITE / "withheld-routes.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read withheld-route registry: {exc}") from exc
    artifacts = registry.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("withheld-route registry artifacts must be a list")
    routes: set[str] = set()
    for item in artifacts:
        item_routes = item.get("publicRoutes") if isinstance(item, dict) else None
        if not isinstance(item_routes, list) or not all(
            isinstance(route, str) for route in item_routes
        ):
            raise ValueError("withheld-route registry has an invalid publicRoutes entry")
        routes.update(item_routes)
    return routes


def has_unretired_forbidden_match(text: str, name: str) -> bool:
    """True when a lifecycle-aware retired form is used rather than mentioned."""

    if name not in LIFECYCLE_AWARE_FORBIDDEN:
        raise ValueError(f"{name} is not a lifecycle-aware public prohibition")
    candidate = normalize_visible_text(text)
    pattern = FORBIDDEN[name]
    for match in pattern.finditer(candidate):
        prefix = candidate[max(0, match.start() - 180):match.start()]
        if not LIFECYCLE_PREFIX.search(prefix):
            return True
    return False


def validate_status_source_claims(data: dict, errors: list[str]) -> None:
    """Bind narrow owner-status copy without promoting it to a claim card.

    This extension is deliberately local to this corpus: it can attest that a
    public page accurately reports an editorial or record status, but it cannot
    add a doctrine claim, import an application source, or raise an evidence
    tier. Claim-bearing public language remains governed by ``surfaceClaims``.
    """

    bindings = data.get("statusSourceClaims", [])
    if not isinstance(bindings, list):
        errors.append("statusSourceClaims must be a list")
        return
    seen_ids: set[str] = set()
    seen_surfaces: set[str] = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            errors.append("status source binding must be an object")
            continue
        binding_id = binding.get("id")
        if not isinstance(binding_id, str) or not binding_id:
            errors.append("status source binding missing id")
            continue
        if binding_id in seen_ids:
            errors.append(f"duplicate status source binding: {binding_id}")
            continue
        seen_ids.add(binding_id)
        for key in ("surface", "role", "source", "sourceRevision", "tier", "requiredMarkers", "scope"):
            if not binding.get(key):
                errors.append(f"{binding_id} status source binding missing {key}")
        if binding.get("scope") != "editorial_or_record_status_only":
            errors.append(f"{binding_id} status source binding has invalid scope")
        tier = binding.get("tier")
        if binding.get("surface") not in data.get("currentSurfaces", []):
            errors.append(f"{binding_id} status binding is not a current surface")
        elif isinstance(binding.get("surface"), str):
            seen_surfaces.add(binding["surface"])
        markers = binding.get("requiredMarkers")
        if not isinstance(markers, list) or not all(isinstance(marker, str) and marker for marker in markers):
            errors.append(f"{binding_id} status binding requiredMarkers must be non-empty strings")
            markers = []
        source_rel = binding.get("source")
        if not isinstance(source_rel, str) or not source_rel:
            continue
        expected_tier = STATUS_SOURCE_CONTRACTS.get(source_rel)
        if expected_tier is None:
            errors.append(f"{binding_id} status source is not an approved owner-status source")
            continue
        if tier != expected_tier:
            errors.append(f"{binding_id} status source tier must remain {expected_tier}")
        source_path = ROOT / source_rel
        try:
            source_path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{binding_id} status source escapes the Emergentism corpus")
            continue
        if not source_path.is_file():
            errors.append(f"{binding_id} status source is missing: {source_rel}")
        elif binding.get("sourceRevision") != _sha256_revision(source_path):
            errors.append(f"{binding_id} status sourceRevision drift: {source_rel}")
        surface = binding.get("surface")
        page = SITE / surface if isinstance(surface, str) else None
        rendered = page.read_text(encoding="utf-8", errors="replace") if page and page.is_file() else ""
        visible = normalize_visible_text(rendered)
        for marker in markers:
            if marker not in visible:
                errors.append(f"{binding_id} missing bound public marker {marker!r}")
        if "claimCardIds" in binding or "publicDisposition" in binding:
            errors.append(f"{binding_id} status binding may not act as a claim-card binding")
    missing_surfaces = REQUIRED_STATUS_SOURCE_SURFACES - seen_surfaces
    for surface in sorted(missing_surfaces):
        errors.append(f"missing required status source binding: {surface}")
    missing_bindings = REQUIRED_STATUS_SOURCE_BINDING_IDS - seen_ids
    for binding_id in sorted(missing_bindings):
        errors.append(f"missing required status source binding id: {binding_id}")


def main() -> int:
    errors: list[str] = []
    for fixture in NODE_PRODUCT_REJECT_FIXTURES:
        if not has_retired_node_product(fixture):
            errors.append(f"retired node product negative-control escaped: {fixture}")
    for fixture in NODE_PRODUCT_BOUNDED_FIXTURES:
        if has_retired_node_product(fixture):
            errors.append(f"retired node product rule overmatched bounded wording: {fixture}")
    for fixture in TITAN_INFIX_REJECT_FIXTURES:
        if not has_titan_infix(fixture):
            errors.append(f"Titan infix negative-control escaped: {fixture}")
    for fixture in TITAN_OPERATOR_FREE_FIXTURES:
        if has_titan_infix(fixture):
            errors.append(f"Titan infix rule overmatched operator-free wording: {fixture}")
    for name, fixture in LIFECYCLE_FIXTURES.items():
        if not has_unretired_forbidden_match(fixture, name):
            errors.append(f"lifecycle-aware prohibition escaped: {name}")
        if has_unretired_forbidden_match(f"Retired {fixture}", name):
            errors.append(f"lifecycle-aware prohibition overmatched retired mention: {name}")
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    try:
        audited_surfaces = parity_audit_surfaces(data)
    except ValueError as exc:
        errors.append(str(exc))
        audited_surfaces = []
    try:
        deployable_html = deployable_html_surfaces()
    except ValueError as exc:
        errors.append(str(exc))
        deployable_html = []
    deployment_patterns = load_vercelignore_patterns() or []
    for rel in audited_surfaces:
        path = SITE / rel
        if not path.is_file():
            errors.append(f"missing current/provisional public surface: {rel}")
        elif is_vercel_ignored(rel, deployment_patterns):
            errors.append(f"current/provisional public surface is excluded from deployment: {rel}")
    try:
        excluded_routes = withheld_public_routes()
    except ValueError as exc:
        errors.append(str(exc))
        excluded_routes = set()
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
        rendered_path = SITE / item["id"][1:] / "index.html"
        if not rendered_path.is_file():
            errors.append(f"{item['id']} missing rendered dimension surface")
            continue
        rendered = rendered_path.read_text(encoding="utf-8", errors="replace")
        for needle, label in (
            ('class="diagram visual-panel"', "instrument visual hook"),
            ('type="importmap"', "local Three.js import map"),
            ('type="module" src="../dimensions/dimensions.js"', "module instrument loader"),
            ('class="number-nav"', "accessible spaced navigation"),
        ):
            if needle not in rendered:
                errors.append(f"{item['id']} missing {label}")

    surface_claims = data.get("surfaceClaims", [])
    validate_status_source_claims(data, errors)
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

    # The manifest owns the current/provisional contract. Prohibition scans are
    # wider: any HTML that can reach a deployment is public copy and must pass
    # the same semantic fences.
    for rel in deployable_html:
        path = SITE / rel
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN.items():
            if name == "application authority leakage" and rel == "record/index.html" and record_has_only_historical_k2(text):
                continue
            if name in LIFECYCLE_AWARE_FORBIDDEN:
                if has_unretired_forbidden_match(text, name):
                    errors.append(f"{rel}: {name}")
                continue
            if name == "forbidden Titan infix arithmetic":
                if has_titan_infix(text):
                    errors.append(f"{rel}: {name}")
                continue
            scan_text = text
            # Tier-claim patterns must survive inline markup: the site writes
            # "They <b>multiply</b>", which no raw-text regex can cross. Strip
            # tags for these two only, leaving the tuned legacy patterns alone.
            if name in ("product uniqueness asserted as settled",
                        "ethic derived from arithmetic",
                        "retracted K4 tagline"):
                scan_text = re.sub(r"<[^>]+>", " ", text)
            if name == "quantum-gravity solution inflation":
                scan_text = re.sub(r"does not.{0,240}solve quantum gravity", "", scan_text, flags=re.I | re.S)
            if pattern.search(scan_text):
                errors.append(f"{rel}: {name}")
    for rel in parity_audit_surfaces(data):
        text = (SITE / rel).read_text(encoding="utf-8", errors="replace")
        if FROZEN_LIBRARY_BOUNDARY_MARKER in text:
            errors.append(f"{rel}: declared current/provisional page carries a frozen-library boundary")
        if HIDDEN_ROBOTS_META.search(text):
            errors.append(f"{rel}: declared current/provisional page self-declares noindex/none")
    for rel, markers in CURRENT_AND_CLASS_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"AND-class parity target is not a declared current surface: {rel}")
            continue
        text = (SITE / rel).read_text(encoding="utf-8", errors="replace").casefold()
        for marker in markers:
            if marker.casefold() not in text:
                errors.append(f"{rel}: missing selected AND-class marker {marker!r}")
    for rel, markers in CURRENT_BOOK_MARKERS.items():
        if rel not in data.get("currentSurfaces", []):
            errors.append(f"current-reader parity target is not a declared current surface: {rel}")
            continue
        text = (SITE / rel).read_text(encoding="utf-8", errors="replace")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing current-reader marker {marker!r}")

    living = json.loads((SITE / "living-map.json").read_text(encoding="utf-8"))
    questions = living.get("openQuestions", [])
    maturity = Counter(row.get("maturityState") for row in questions if isinstance(row, dict))
    lab = (SITE / "lab/index.html").read_text(encoding="utf-8", errors="replace")
    maturity_marker = (
        f'data-maturity-summary="packet-complete:{maturity["packet-complete"]};'
        f'component-supported:{maturity["component-supported"]};deferred:{maturity["deferred"]}"'
    )
    if len(questions) != 12:
        errors.append(f"living-map must expose exactly 12 GP questions, got {len(questions)}")
    if maturity_marker not in lab:
        errors.append("lab maturity summary does not match living-map distribution")
    if "packet-complete [B]" in lab:
        errors.append("lab promotes all GP sockets to packet-complete [B]")
    for rel, alternatives in REQUIRED_PUBLIC_CONTRACTS.items():
        path = SITE / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in alternatives:
            if needle not in text:
                errors.append(f"{rel}: missing founder contract marker {needle!r}")
    contribute = (SITE / "contribute/index.html").read_text(encoding="utf-8", errors="replace")
    custody_marker = "A public issue is a custody item. Filing alone does not establish independent review, validation, or a tier upgrade"
    first_form = contribute.find(PUBLIC_ISSUE_FORM_ROUTE)
    if first_form < 0:
        errors.append("contribute/index.html: missing public issue-form route")
    elif contribute.find(custody_marker) < 0 or contribute.find(custody_marker) > first_form:
        errors.append("contribute/index.html: custody/non-upgrade boundary must precede public issue forms")
    for rel in parity_audit_surfaces(data):
        if rel == "contribute/index.html" or not rel.endswith((".html", ".htm")):
            continue
        path = SITE / rel
        if path.is_file() and PUBLIC_ISSUE_FORM_ROUTE in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"{rel}: public issue form bypasses the contribution boundary")
    manifesto = normalize_visible_text((SITE / "manifesto/index.html").read_text(encoding="utf-8", errors="replace")).casefold()
    for promise in AUTOMATIC_SUBMISSION_PROMISES:
        if promise in manifesto:
            errors.append(f"manifesto/index.html: automatic submission promise is not authorized: {promise!r}")
    record = normalize_visible_text((SITE / "record/index.html").read_text(encoding="utf-8", errors="replace")).casefold()
    if "frozen product-versus-rivals study" in record:
        errors.append("record/index.html: void GP-03 execution route was advertised as current")
    paradoxes = (SITE / "discoveries/paradoxes/index.html").read_text(encoding="utf-8", errors="replace")
    if '<span class="k">21</span>…and the remaining sixteen' not in paradoxes:
        errors.append("discoveries/paradoxes/index.html: twenty-one-item suite remainder marker drift")
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
    rag_contract = rag.get("book_contract", {})
    if (
        rag_contract.get("work_id") != "BK-ONE-SITTING"
        or rag_contract.get("ordered_source_paths") != ["00_THE_WELTANSCHAUUNG_ONE_SITTING.md"]
        or rag_contract.get("source_lifecycles") != ["reader_synthesis"]
        or rag_contract.get("withheld_provenance_included") is not False
    ):
        errors.append("RAG current-book lifecycle contract drift")
    frozen_prefixes = tuple(f"{root}:" for root in data["frozenLibraryRoots"])
    for passage in rag.get("passages", []):
        passage_id = str(passage.get("id", ""))
        href = str(passage.get("href", ""))
        # REPAIRED 2026-08-05: this read `frozen_roots`, a name that is defined
        # nowhere in this file — an incomplete rename. Line above already binds the
        # identical tuple as `frozen_prefixes`, so this is exactly equivalent and
        # not a behaviour change. Until now the checker raised NameError on every
        # run and could report nothing, including its own TITAN_INFIX_REJECT_FIXTURES.
        if passage_id.startswith(frozen_prefixes) or any(
            href == route or href.startswith(route + "/") or href.startswith(route + "#")
            for route in excluded_routes
        ):
            errors.append(f"frozen or withheld passage remains in RAG: {passage_id}")
            break
        passage_text = f"{passage.get('title', '')} {passage.get('text', '')}"
        if has_retired_node_product(passage_text):
            errors.append(f"retired node product assignment remains in RAG: {passage.get('id')}")
            break
    if errors:
        print("PUBLIC SEMANTIC PARITY: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"PUBLIC SEMANTIC PARITY: PASS ({len(levels)} levels, 5 mu crossings, 1 boundary, 1 return)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

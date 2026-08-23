#!/usr/bin/env python3
"""Build the exact public-withholding and frozen-route delivery boundary.

The JSON registry remains the release ledger. This deterministic reconciler
preserves curated entries, adds fail-closed entries for retired literal closure
or uncalibrated product-derived ethics, then derives Vercel exclusions,
redirects, and response headers from the resulting exact artifact set.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import re
from pathlib import Path

from check_public_semantic_parity import (
    FORBIDDEN,
    LIFECYCLE_AWARE_FORBIDDEN,
    has_unretired_forbidden_match,
    has_titan_infix,
    record_has_only_historical_k2,
)


SITE = Path(__file__).resolve().parent
REGISTRY = SITE / "withheld-routes.json"
PARITY = SITE / "public_semantic_parity.json"
READING = SITE / "reading-manifest.json"
VERCEL_IGNORE = SITE / ".vercelignore"
VERCEL = SITE / "vercel.json"

IGNORE_BEGIN = "# BEGIN GENERATED EXACT WITHHOLDING"
IGNORE_END = "# END GENERATED EXACT WITHHOLDING"

# These formerly active-looking routes are withheld even when a compact regex
# would miss the surrounding prose. They are historical custody, not current
# source owners.
FORCED_ARTIFACTS = {
    "axiology/index.html": "Historical axiology route selects an uncalibrated node product inside its ethical procedure.",
    "finity-papers/index.html": "Historical Finity overview presents an uncalibrated product constraint as a structural ethic.",
    "game/index.html": "Historical Game route scores lawful action through the retired uncalibrated node product.",
    "geometric-ontology/index.html": "Historical geometric-ontology route asserts literal D6/D0 identity and product-scored ethics.",
    "home/index.html": "Superseded alternate homepage carries the retired product-scored game rule.",
    "index_legacy_2026_07_19.html": "Superseded root homepage carries the retired product-scored game rule.",
    "soul-loop/index.html": "Historical Soul Loop route turns the retired node product into an objective-dharma test.",
    "synthesis/index.html": "Historical synthesis derives an objective ethic from an uncalibrated product.",
    "teleology/index.html": "Historical teleology route couples an uncalibrated product to an objective-dharma rule.",
}

# This policy inspects source artifacts that could be delivered by the static
# site. Local deployment output is neither source custody nor a public route:
# scanning it would manufacture routes such as
# `/.vercel/output/static/...` in the withholding ledger.
POLICY_SCAN_EXCLUDED_PREFIXES = (
    ".vercel/",
    ".git/",
    "node_modules/",
    "__pycache__/",
    "book-pwa/",
    "_archive/",
    "90_ARCHIVE/",
    "partials/",
    "_PLANS/",
)

LITERAL_D6 = re.compile(r"D6\s*(?:≡|=)\s*D0", re.I)
PRODUCT = (
    r"(?:P(?:_|<sub>)?node(?:</sub>)?\s*(?::?=)\s*(?:Φ|&Phi;)|"
    r"(?:empowerment\s*=\s*)?Φ\s*(?:×|x|\*)\s*V)"
)
ETHICAL = (
    r"(?:(?:objective|derived|structural)\s+(?:ethic|ethics|dharma)|"
    r"ethic(?:s)?\s+(?:emerges?|follows?|is\s+derived)|lawful\s+action)"
)
PRODUCT_DERIVED_ETHICS = re.compile(
    rf"(?:{PRODUCT}.{{0,1400}}{ETHICAL}|{ETHICAL}.{{0,1400}}{PRODUCT})",
    re.I | re.S,
)

# These two pages quote a failed expression inside an explicit correction
# boundary. Their negative evidence remains useful and is not an affirmative
# public claim.
PRODUCT_HISTORY_EXCEPTIONS = {"axioms/index.html", "record/index.html", "halahala/index.html"}

# The v2.3 Third Churning replaces the archived, policy-failing Hālāhala page
# with a generated warning ledger that passes the current semantic firewall.
# The predecessor remains byte-custodied under 90_ARCHIVE; only its curated
# public-withholding lifecycle ends here.
RETIRED_CURATED_ARTIFACTS = {"halahala/index.html"}


def _rule_id(name: str) -> str:
    """Stable custody rule identifier for a public semantic prohibition."""

    return "semantic-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


BASE_POLICY_RULE_IDS = (
    "retired-literal-d6-identity",
    "retired-product-derived-ethics",
    "explicit-legacy-route",
)
SEMANTIC_POLICY_RULE_IDS = tuple(sorted(_rule_id(name) for name in FORBIDDEN))
POLICY_RULE_IDS = (*BASE_POLICY_RULE_IDS, *SEMANTIC_POLICY_RULE_IDS)


def _semantic_policy_matches(artifact: str, text: str) -> tuple[list[str], list[str]]:
    """Return public-firewall violations for a source artifact.

    The semantic checker is the owner of the patterns. Reusing its exact
    lifecycle and historical-record exceptions keeps withholding fail-closed
    without inventing a second, weaker interpretation of public safety.
    """

    rule_ids: list[str] = []
    reasons: list[str] = []
    for name, pattern in FORBIDDEN.items():
        if name == "application authority leakage" and artifact == "record/index.html" and record_has_only_historical_k2(text):
            continue
        if name in LIFECYCLE_AWARE_FORBIDDEN:
            matched = has_unretired_forbidden_match(text, name)
        elif name == "forbidden Titan infix arithmetic":
            matched = has_titan_infix(text)
        else:
            scan_text = text
            if name in ("product uniqueness asserted as settled", "ethic derived from arithmetic"):
                scan_text = re.sub(r"<[^>]+>", " ", text)
            if name == "quantum-gravity solution inflation":
                scan_text = re.sub(
                    r"does not.{0,240}solve quantum gravity", "", scan_text,
                    flags=re.I | re.S,
                )
            matched = bool(pattern.search(scan_text))
        if matched:
            rule_ids.append(_rule_id(name))
            reasons.append(f"matches public semantic prohibition: {name}")
    return rule_ids, reasons


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _routes(artifact: str) -> list[str]:
    path = Path(artifact)
    if path.name == "index.html":
        base = "/" + path.parent.as_posix().strip("/")
        return [base, base + "/", "/" + artifact]
    # With clean URLs, ``foo.html`` and ``foo/index.html`` would both claim
    # ``/foo`` when they coexist.  The directory owns the clean alias; the
    # file remains an exact raw artifact route only.
    if (SITE / path.with_suffix("") / "index.html").is_file():
        return ["/" + artifact]
    base = "/" + path.with_suffix("").as_posix().strip("/")
    return [base, base + "/", "/" + artifact]


def _route_base(artifact: str) -> str:
    path = Path(artifact)
    if path.name == "index.html":
        return "/" + path.parent.as_posix().strip("/")
    if (SITE / path.with_suffix("") / "index.html").is_file():
        return "/" + artifact
    return "/" + path.with_suffix("").as_posix().strip("/")


def _manifest_lookup() -> dict[str, dict[str, str]]:
    manifest = json.loads(READING.read_text(encoding="utf-8"))
    return {
        row["href"]: {"section": row["section"], "href": row["href"]}
        for row in manifest.get("documents", [])
    }


def _manifest_document(artifact: str, lookup: dict[str, dict[str, str]]) -> dict[str, str] | None:
    path = Path(artifact)
    if path.name != "index.html":
        return None
    href = path.parent.as_posix().strip("/") + "/"
    return lookup.get(href)


def _policy_matches(current_surfaces: set[str]) -> dict[str, tuple[list[str], str]]:
    matches: dict[str, tuple[list[str], str]] = {}
    for path in sorted(SITE.rglob("*.html")):
        artifact = path.relative_to(SITE).as_posix()
        if artifact.startswith(POLICY_SCAN_EXCLUDED_PREFIXES):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rule_ids: list[str] = []
        reasons: list[str] = []
        if LITERAL_D6.search(text):
            rule_ids.append("retired-literal-d6-identity")
            reasons.append("asserts the retired literal D6/D0 identity")
        if artifact not in PRODUCT_HISTORY_EXCEPTIONS and PRODUCT_DERIVED_ETHICS.search(text):
            rule_ids.append("retired-product-derived-ethics")
            reasons.append("derives or scores ethics through an uncalibrated Phi/V product")
        if artifact in FORCED_ARTIFACTS:
            rule_ids.append("explicit-legacy-route")
            reasons.append(FORCED_ARTIFACTS[artifact])
        semantic_rules, semantic_reasons = _semantic_policy_matches(artifact, text)
        rule_ids.extend(semantic_rules)
        reasons.extend(semantic_reasons)
        if not rule_ids:
            continue
        if artifact in current_surfaces:
            raise ValueError(
                f"current surface matches retired withholding policy and must be repaired: {artifact} ({', '.join(rule_ids)})"
            )
        matches[artifact] = (
            sorted(set(rule_ids)),
            "; ".join(dict.fromkeys(reason.rstrip(".") for reason in reasons)) + ".",
        )
    missing = sorted(set(FORCED_ARTIFACTS) - set(matches))
    if missing:
        raise FileNotFoundError(f"forced withholding artifacts are missing: {missing}")
    return matches


def _build_registry() -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    parity = json.loads(PARITY.read_text(encoding="utf-8"))
    current = (
        set(parity.get("currentSurfaces", []))
        | set(parity.get("currentInfrastructureSurfaces", []))
        | set(parity.get("infrastructureRoutes", {}).get("routes", []))
        | set(parity.get("declaredProvisional", {}).get("routes", []))
    )
    present_retired = {
        artifact for artifact in RETIRED_CURATED_ARTIFACTS
        if (SITE / artifact).is_file()
    }
    if not present_retired.issubset(current):
        raise ValueError("retired curated artifacts must be declared current successors")
    policy_matches = _policy_matches(current)
    lookup = _manifest_lookup()

    prior_rows = {
        row["artifact"]: row for row in registry.get("artifacts", [])
    }
    curated_reasons: dict[str, str] = {}
    for artifact, row in prior_rows.items():
        declared = row.get("curatedReason")
        if isinstance(declared, str) and declared.strip():
            curated_reasons[artifact] = declared.strip()
            continue
        reason = str(row.get("reason", "")).strip()
        if not row.get("policyRuleIds") and reason:
            curated_reasons[artifact] = reason
            continue
        # Migration for a curated row that acquired a semantic policy match
        # before curatedReason was explicit. Auto-policy rows begin directly
        # with "matches" and therefore do not enter this branch.
        marker = "; matches public semantic prohibition:"
        if marker in reason:
            prefix = reason.split(marker, 1)[0].rstrip(".; ")
            if prefix:
                curated_reasons[artifact] = prefix + "."
    curated = {
        artifact: row
        for artifact, row in prior_rows.items()
        if artifact in curated_reasons and artifact not in RETIRED_CURATED_ARTIFACTS
    }
    prior_manifest_documents = {
        row["artifact"]: row["manifestDocument"]
        for row in registry.get("artifacts", [])
        if isinstance(row.get("manifestDocument"), dict)
    }
    rows: list[dict] = []
    for artifact in sorted(set(curated) | set(policy_matches)):
        path = SITE / artifact
        if not path.is_file():
            raise FileNotFoundError(f"withheld artifact is missing: {artifact}")
        if artifact in curated:
            row = dict(curated[artifact])
            curated_reason = curated_reasons[artifact].rstrip(".")
            row["curatedReason"] = curated_reason + "."
            row["sha256"] = _sha256(path)
            row["bytes"] = path.stat().st_size
            row["publicRoutes"] = _routes(artifact)
            if artifact in policy_matches:
                rule_ids, policy_reason = policy_matches[artifact]
                row["policyRuleIds"] = rule_ids
                row["reason"] = "; ".join(
                    part for part in (curated_reason, policy_reason.rstrip(".")) if part
                ) + "."
            else:
                row.pop("policyRuleIds", None)
                row["reason"] = curated_reason + "."
        else:
            rule_ids, reason = policy_matches[artifact]
            row = {
                "artifact": artifact,
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
                "publicRoutes": _routes(artifact),
                "reason": reason,
                "policyRuleIds": rule_ids,
            }
        manifest_document = _manifest_document(artifact, lookup) or prior_manifest_documents.get(artifact)
        if manifest_document:
            row["manifestDocument"] = manifest_document
        else:
            row.pop("manifestDocument", None)
        rows.append(row)

    result = dict(registry)
    result["schemaVersion"] = 2
    result["policy"] = {
        "mode": "exact-artifact fail-closed",
        "rules": list(POLICY_RULE_IDS),
        "boundary": "Affirmative literal D6/D0 identity, uncalibrated product-derived ethics, and every public-semantic-firewall violation are excluded from public delivery; negative correction records may remain only in their declared historical boundary.",
    }
    result["artifacts"] = rows
    route_owners: dict[str, list[str]] = {}
    for row in rows:
        for route in row["publicRoutes"]:
            route_owners.setdefault(route, []).append(row["artifact"])
    collisions = {
        route: owners for route, owners in route_owners.items() if len(owners) > 1
    }
    if collisions:
        rendered = "; ".join(
            f"{route}: {', '.join(owners)}" for route, owners in sorted(collisions.items())
        )
        raise ValueError(f"withheld public aliases must have one artifact owner: {rendered}")
    return result


def _build_ignore(artifacts: list[dict]) -> str:
    text = VERCEL_IGNORE.read_text(encoding="utf-8")
    start = text.index(IGNORE_BEGIN)
    end = text.index(IGNORE_END) + len(IGNORE_END)
    # Gitignore-style patterns are ordered: a later re-include such as
    # ``!build/**`` must never revive a withheld artifact. Keep the generated
    # exact block at EOF so the registry is the last applicable rule.
    without_generated = (text[:start] + text[end:]).rstrip()
    body = "\n".join(row["artifact"] for row in artifacts)
    return f"{without_generated}\n\n{IGNORE_BEGIN}\n{body}\n{IGNORE_END}\n"


def _is_single_frozen_header(row: dict) -> bool:
    headers = row.get("headers", [])
    return len(headers) == 1 and headers[0] == {"key": "X-Robots-Tag", "value": "noindex, follow"}


def _frozen_legacy_surfaces(parity: dict) -> list[str] | None:
    """Return an explicit legacy list, or None for older schema-v2 manifests.

    `frozenLegacySurfaces` appeared in one schema-v2 manifest revision and was
    absent in later valid schema-v2 manifests. Its absence therefore cannot
    silently authorize removing existing legacy noindex headers.
    """

    missing = object()
    value = parity.get("frozenLegacySurfaces", missing)
    if value is missing:
        return None
    if not isinstance(value, list) or any(
        not isinstance(artifact, str) or not artifact for artifact in value
    ):
        raise ValueError(
            "public_semantic_parity.json frozenLegacySurfaces must be a list of non-empty artifacts"
        )
    if len(value) != len(set(value)):
        raise ValueError(
            "public_semantic_parity.json frozenLegacySurfaces must not contain duplicates"
        )
    return value


def _is_frozen_root_header(row: dict, frozen_roots: list[str]) -> bool:
    return _is_single_frozen_header(row) and row.get("source") in {
        f"/{root}/(.*)" for root in frozen_roots
    }


def _is_current_surface_header(row: dict, current_surfaces: set[str]) -> bool:
    """Reject a retained legacy noindex header once its exact page is current."""

    if not _is_single_frozen_header(row):
        return False
    current_routes: set[str] = set()
    for artifact in current_surfaces:
        if not artifact.endswith(".html"):
            continue
        base = _route_base(artifact)
        if base != "/":
            # Historical configs also carried exact route headers (for
            # example ``/halahala``) beside subtree patterns. Once a surface
            # is current, neither form may retain the legacy noindex policy.
            current_routes.add(base.rstrip("/"))
        current_routes.add(base + "(.*)")
        if base != "/":
            current_routes.add(base.rstrip("/") + "/(.*)")
    return row.get("source") in current_routes


def _is_withheld_header(row: dict) -> bool:
    values = {item.get("value") for item in row.get("headers", []) if item.get("key") == "X-Robots-Tag"}
    return "noindex, noarchive, nosnippet, nofollow" in values and row.get("source") != "/historical-boundary/(.*)"


def _build_vercel(artifacts: list[dict]) -> dict:
    config = json.loads(VERCEL.read_text(encoding="utf-8"))
    withheld_routes = {
        route
        for item in artifacts
        for route in item["publicRoutes"]
    }
    config["redirects"] = [
        row for row in config.get("redirects", [])
        if row.get("destination") != "/historical-boundary/"
        and row.get("source") not in withheld_routes
    ]
    for item in artifacts:
        for route in item["publicRoutes"]:
            config["redirects"].append({
                "source": route,
                "destination": "/historical-boundary/",
                "permanent": False,
            })

    parity = json.loads(PARITY.read_text(encoding="utf-8"))
    frozen_roots = parity["frozenLibraryRoots"]
    current_surfaces = set(parity.get("currentSurfaces", [])) | set(
        parity.get("currentInfrastructureSurfaces", [])
    )
    frozen_legacy = _frozen_legacy_surfaces(parity)
    if frozen_legacy is None:
        # Compatibility mode: regenerate named frozen roots but retain existing
        # legacy headers. Treating omission as [] would change publication
        # policy merely because this generator ran.
        headers = [
            row for row in config.get("headers", [])
            if not _is_frozen_root_header(row, frozen_roots)
            and not _is_current_surface_header(row, current_surfaces)
            and not _is_withheld_header(row)
        ]
    else:
        headers = [
            row for row in config.get("headers", [])
            if not _is_single_frozen_header(row) and not _is_withheld_header(row)
        ]
    frozen_value = [{"key": "X-Robots-Tag", "value": "noindex, follow"}]
    for root in frozen_roots:
        headers.append({"source": f"/{root}/(.*)", "headers": frozen_value})
    if frozen_legacy is not None:
        for artifact in frozen_legacy:
            headers.append({"source": _route_base(artifact) + "(.*)", "headers": frozen_value})
    withheld_value = [
        {"key": "X-Robots-Tag", "value": "noindex, noarchive, nosnippet, nofollow"},
        {"key": "Cache-Control", "value": "no-store, max-age=0"},
        {"key": "CDN-Cache-Control", "value": "no-store"},
    ]
    for item in artifacts:
        headers.append({"source": _route_base(item["artifact"]) + "(.*)", "headers": withheld_value})
    config["headers"] = headers
    return config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated custody surfaces drift")
    args = parser.parse_args()
    registry = _build_registry()
    desired = {
        REGISTRY: json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        VERCEL_IGNORE: _build_ignore(registry["artifacts"]),
        VERCEL: json.dumps(_build_vercel(registry["artifacts"]), ensure_ascii=False, indent=2) + "\n",
    }
    if args.check:
        drift = [path.name for path, text in desired.items() if path.read_text(encoding="utf-8") != text]
        if drift:
            print("WITHHOLDING BOUNDARY: FAIL (drift: " + ", ".join(drift) + ")")
            return 1
        print(f"WITHHOLDING BOUNDARY: PASS ({len(registry['artifacts'])} exact artifacts)")
        return 0
    for path, text in desired.items():
        path.write_text(text, encoding="utf-8")
    print(f"withholding boundary: {len(registry['artifacts'])} exact artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

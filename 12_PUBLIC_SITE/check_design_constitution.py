#!/usr/bin/env python3
"""Fail closed when the public design grammar drifts from its source contract."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import sys
from pathlib import Path


SITE = Path(__file__).resolve().parent
CONTRACT_PATH = SITE / "emergentism-design.v2.json"
CONSTITUTION_PATH = SITE / "EMERGENTISM_DESIGN_CONSTITUTION.md"
PARITY_PATH = SITE / "public_semantic_parity.json"
CSS_PATH = SITE / "assets/css/gestalt-v2.css"
JS_PATH = SITE / "assets/js/gestalt-v2.js"


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name}: root must be an object")
    return payload


def load_shell():
    spec = importlib.util.spec_from_file_location(
        "emergentism_design_shell", SITE / "build_core_shell.py"
    )
    if not spec or not spec.loader:
        raise ValueError("cannot load build_core_shell.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def visible_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def check() -> list[str]:
    errors: list[str] = []
    try:
        contract = load_json(CONTRACT_PATH)
        parity = load_json(PARITY_PATH)
        shell = load_shell()
    except ValueError as exc:
        return [str(exc)]

    if contract.get("schema") != "emergentism/PublicDesignContract.v2":
        errors.append("contract schema is not emergentism/PublicDesignContract.v2")
    if contract.get("version") != "2.0.0":
        errors.append("contract version is not 2.0.0")
    if contract.get("owner") != CONSTITUTION_PATH.name:
        errors.append("contract owner does not name EMERGENTISM_DESIGN_CONSTITUTION.md")

    boundary = contract.get("boundary", {})
    for key in (
        "creates_doctrine",
        "creates_evidence",
        "creates_authority",
        "proves_comprehension",
        "proves_deployment",
    ):
        if boundary.get(key) is not False:
            errors.append(f"boundary.{key} must be false")
    if boundary.get("projection_only") is not True:
        errors.append("boundary.projection_only must be true")
    if boundary.get("public_changes_truth") is not False:
        errors.append("boundary.public_changes_truth must be false")

    supersedes = contract.get("supersedes", {})
    predecessor = SITE / str(supersedes.get("path", ""))
    if not predecessor.is_file():
        errors.append("archived v1 design predecessor is missing")
    else:
        actual = hashlib.sha256(predecessor.read_bytes()).hexdigest()
        if actual != supersedes.get("sha256"):
            errors.append("archived v1 design predecessor hash drift")

    try:
        constitution = CONSTITUTION_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read constitution: {exc}")
        constitution = ""
    for marker in (
        "The interface is part of the argument.",
        "Colour never carries a role alone.",
        "Motion signals state; it never supplies meaning",
        "A passing design gate proves bounded byte and structural agreement only.",
        "Public is a visibility state, not a truth state.",
    ):
        if marker not in constitution:
            errors.append(f"constitution missing marker: {marker}")

    roles = contract.get("semanticRoles", {})
    expected_roles = {
        "boundary": "--g2-bone-faint",
        "actual": "--g2-actual",
        "possible": "--g2-possible",
        "conjecture": "--g2-conjecture",
        "evidence": "--g2-evidence",
        "poison": "--g2-poison",
    }
    if set(roles) != set(expected_roles):
        errors.append("semanticRoles must contain exactly the six governed roles")

    css = CSS_PATH.read_text(encoding="utf-8")
    js = JS_PATH.read_text(encoding="utf-8")
    for role, token in expected_roles.items():
        if roles.get(role, {}).get("token") != token:
            errors.append(f"semantic role {role} does not bind {token}")
        if token not in css:
            errors.append(f"shared CSS does not define or consume {token}")
    for marker in (
        ".g2-footer__key-item--actual",
        ".g2-footer__key-item--possible",
        ".g2-footer__key-item--conjecture",
        ".g2-footer__key-item--evidence",
        "border-top-style: dashed",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
        "@media (prefers-color-scheme: dark)",
        ':root[data-theme="light"]',
        ':root[data-theme="dark"]',
        ".g2-promotion-rail",
        ".g2-public-lamp",
    ):
        if marker not in css:
            errors.append(f"shared CSS missing governed marker: {marker}")
    if re.search(r"(?:linear|radial|conic)-gradient\s*\(", css):
        errors.append("core atlas CSS reintroduced a decorative gradient")
    for foreign in ("#39ff14", "game-of-life", "skyzai-torus", "fire-sector"):
        if foreign in css.casefold():
            errors.append(f"core atlas CSS imports foreign Skyzai identity: {foreign}")

    motion = contract.get("motion", {})
    if motion.get("shared_default") != "static":
        errors.append("shared motion default must be static")
    if motion.get("continuous_shared_runtime") is not False:
        errors.append("continuous_shared_runtime must be false")
    if motion.get("shared_states") != ["static", "active", "reduced"]:
        errors.append("shared motion states must be static, active, reduced")
    for forbidden in ("requestAnimationFrame", "setInterval"):
        if forbidden in js:
            errors.append(f"shared reader runtime contains continuous mechanism: {forbidden}")
    for marker in (
        'root.dataset.gestaltMotion = "static"',
        'root.dataset.gestaltMotion = "active"',
        'root.dataset.gestaltMotion = "reduced"',
        "observer.unobserve(entry.target)",
        'const themeKey = "emergentism-theme"',
        'querySelectorAll("[data-g2-theme-toggle]")',
    ):
        if marker not in js:
            errors.append(f"shared reader runtime missing finite-state marker: {marker}")

    routes = contract.get("routes")
    if not isinstance(routes, list) or not routes:
        return errors + ["routes must be a non-empty list"]
    paths = [row.get("path") for row in routes if isinstance(row, dict)]
    if len(paths) != len(routes) or any(not isinstance(path, str) for path in paths):
        errors.append("every route must be an object with a string path")
        paths = [path for path in paths if isinstance(path, str)]
    if len(paths) != len(set(paths)):
        errors.append("route paths are not unique")

    parity_paths = parity.get("coreJourney", {}).get("surfaces", [])
    if paths != parity_paths:
        errors.append("design routes must exactly preserve semantic-parity coreJourney order")

    allowed_families = {
        "panorama", "narrative", "atlas", "dimension", "instrument",
        "practice", "research", "churning", "library", "accountability", "wisdom",
    }
    allowed_shells = {"core", "dimension", "diagnostic", "churning", "book"}
    core_rows = [row for row in routes if row.get("shell") == "core"]
    core_map = {row["path"]: row.get("navigationSection") for row in core_rows}
    family_map = {row["path"]: row.get("family") for row in core_rows}
    all_family_map = {row["path"]: row.get("family") for row in routes}
    if core_map != shell.CORE_PAGES:
        errors.append("build_core_shell CORE_PAGES drifted from the design contract")
    if family_map != shell.SURFACE_FAMILIES:
        errors.append("build_core_shell surface families drifted from the design contract")
    if all_family_map != shell.ALL_SURFACE_FAMILIES:
        errors.append("build_core_shell all-route families drifted from the design contract")

    required_key = contract.get("requiredVisibleKey", [])
    if not isinstance(required_key, list) or len(required_key) != 4:
        errors.append("requiredVisibleKey must contain the four public semantic readings")

    opted_in: set[str] = set()
    for row in routes:
        path = row.get("path")
        if not isinstance(path, str):
            continue
        if row.get("family") not in allowed_families:
            errors.append(f"{path}: unknown family {row.get('family')}")
        if row.get("shell") not in allowed_shells:
            errors.append(f"{path}: unknown shell {row.get('shell')}")
        page_path = SITE / path
        if not page_path.is_file():
            errors.append(f"missing current journey surface: {path}")
            continue
        text = page_path.read_text(encoding="utf-8")
        if "/assets/css/gestalt-v2.css" not in text:
            errors.append(f"{path}: shared atlas CSS is missing")
        if len(re.findall(r"<main\b", text, re.I)) != 1:
            errors.append(f"{path}: must contain exactly one main element")
        if 'href="/exit/"' not in text and "href='/exit/'" not in text:
            errors.append(f"{path}: current journey has no direct Exit link")
        if 'data-gestalt="v2"' not in text:
            errors.append(f"{path}: data-gestalt=v2 is missing")
        if "data-g2-reveal" in text or "data-g2-draw" in text:
            opted_in.add(path)
        if 'data-emergentism-design="v2"' not in text:
            errors.append(f"{path}: design contract version attribute is missing")
        expected_surface = f'data-emergentism-surface="{row.get("family")}"'
        if expected_surface not in text:
            errors.append(f"{path}: missing surface family attribute {expected_surface}")
        if text.count('data-g2-semantic-key="v2"') != 1:
            errors.append(f"{path}: must contain one visible semantic footer key")
        expected_theme_boot = 0 if row.get("shell") == "churning" else 1
        if text.count("data-g2-theme-boot") != expected_theme_boot:
            errors.append(
                f"{path}: expected {expected_theme_boot} prepaint theme boundaries"
            )
        page_visible = visible_text(text)
        for phrase in required_key:
            if phrase.replace(" · ", " ") not in page_visible.replace(" · ", " "):
                errors.append(f"{path}: semantic footer key missing {phrase}")

    if opted_in != set(motion.get("optInRoutes", [])):
        errors.append("finite motion opt-in routes drifted from rendered markup")

    exceptions = motion.get("instrumentExceptions", [])
    if len(exceptions) != 1 or exceptions[0].get("path") != "burrisphere/instrument/index.html":
        errors.append("Burrisphere must be the sole declared instrument motion exception")
    instrument = (SITE / "burrisphere/instrument/index.html").read_text(encoding="utf-8")
    instrument_js = (SITE / "assets/js/burrisphere-instrument.js").read_text(encoding="utf-8")
    for marker in (
        'id="motion-toggle"', 'id="centre-button"', 'id="polar-angle"',
        'id="axial-rotation"', 'id="motion-status"',
    ):
        if marker not in instrument:
            errors.append(f"Burrisphere motion exception missing control: {marker}")
    if "prefers-reduced-motion: reduce" not in instrument_js:
        errors.append("Burrisphere motion exception lacks reduced-motion handling")

    about = (SITE / "about/index.html").read_text(encoding="utf-8")
    for marker in (
        'id="interface-contract"',
        'href="/emergentism-design.v2.json"',
        "The medium carries <b>types, not truth</b>.",
    ):
        if marker not in about:
            errors.append(f"about page missing public design explanation: {marker}")

    adoption = contract.get("adoptionState", {})
    if adoption.get("reader_comprehension") != "untested":
        errors.append("reader comprehension must remain untested before contact")
    if adoption.get("independent_accessibility_review") != "not_run":
        errors.append("independent accessibility review must remain not_run before receipt")
    if adoption.get("production_deployment") != "separate_receipt_required":
        errors.append("production deployment must require a separate receipt")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("DESIGN CONSTITUTION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    contract = load_json(CONTRACT_PATH)
    print(
        "DESIGN CONSTITUTION: PASS "
        f"({len(contract['routes'])} current routes; 6 roles; finite shared motion)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

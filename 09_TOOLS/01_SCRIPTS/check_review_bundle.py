#!/usr/bin/env python3
"""Verify the frozen review bundle for FPE-REVIEW-01.

The protocol (02_INDEPENDENT_REVIEW.md) requires that every reviewer receive the SAME
frozen bundle and that the invitation record every file hash, because "a material
amendment requires a new version and a new review; an older review cannot silently cover
changed text."

That rule is unenforceable by hand. This locates the highest numbered complete
``REVIEW_BUNDLE_vN`` pair, checks that every earlier version still has both its
document and manifest, and recomputes every sha256 in the current manifest. A
drifted current bundle therefore cannot be sent — or worse, reviewed and then
quietly amended afterwards. Earlier manifests remain historical custody and are
not compared with the current tree after a declared version bump.

Exits 0 if the bundle is intact, 1 otherwise. Absent bundle = PASS with a note: this
gate is optional until someone decides to run it.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "finity_practice"
VERSIONED_BUNDLE = re.compile(r"^REVIEW_BUNDLE_v(?P<version>[1-9][0-9]*)\.(?P<kind>json|md)$")


def bundle_inventory() -> tuple[dict[int, Path], dict[int, Path]]:
    manifests: dict[int, Path] = {}
    documents: dict[int, Path] = {}
    for path in DIR.glob("REVIEW_BUNDLE_v*.*"):
        match = VERSIONED_BUNDLE.fullmatch(path.name)
        if not match:
            continue
        version = int(match.group("version"))
        target = manifests if match.group("kind") == "json" else documents
        target[version] = path
    return manifests, documents


def main() -> int:
    manifests, documents = bundle_inventory()
    versions = sorted(set(manifests) | set(documents))
    if not versions:
        print("REVIEW BUNDLE: PASS (no bundle document and no manifest — nothing frozen)")
        print("  scope: this is the genuinely-empty state. It does NOT mean a bundle was")
        print("  checked; it means none exists.")
        return 0

    errors: list[str] = []
    if versions != list(range(1, versions[-1] + 1)):
        errors.append(f"bundle version history is not contiguous: {versions}")
    for version in versions:
        if version not in manifests:
            errors.append(f"REVIEW_BUNDLE_v{version}.md has no matching JSON manifest")
        if version not in documents:
            errors.append(f"REVIEW_BUNDLE_v{version}.json has no matching Markdown document")
    if errors:
        print("REVIEW BUNDLE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    latest = versions[-1]
    manifest = manifests[latest]
    document = documents[latest]
    try:
        man = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"REVIEW BUNDLE: FAIL\n- manifest unreadable: {exc}")
        return 1

    if man.get("bundleVersion") != f"v{latest}":
        errors.append(
            f"{manifest.name}: bundleVersion must be v{latest}, got {man.get('bundleVersion')!r}"
        )
    files = man.get("files", {})
    if not files:
        errors.append("the manifest lists no files")
    for rel, want in files.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: listed in the bundle and MISSING from the tree")
            continue
        got = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
        if got != want:
            errors.append(
                f"{rel}: hash moved.\n    frozen {want}\n    now    {got}\n"
                f"    This is a material amendment. Bump the bundle to v{latest + 1} and treat any "
                "existing review as not covering it."
            )

    # the packet must keep saying it is not a result
    doc = document.read_text(encoding="utf-8")
    normalized_doc = " ".join(doc.split())
    for needed in ("not sent", "review received", "does not work here"):
        if needed not in normalized_doc:
            errors.append(
                f"{document.name} no longer states '{needed}' — the status table or its "
                "fence has been weakened"
            )

    if errors:
        print("REVIEW BUNDLE: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"REVIEW BUNDLE: PASS ({len(files)} files, {len(versions)} versions in custody; all hashes match bundle "
          f"{man.get('bundleVersion','?')} frozen {man.get('frozen','?')})")
    print("  scope: proves the packet has not drifted. It does NOT mean a reviewer was "
          "found, contacted, or replied.")
    print("  known limit: the status-table check matches PHRASES, not truth. Someone "
          "could flip 'reviewer contacted' to yes and this still passes. Only a filed "
          "verdict with a disclosed conflict statement evidences a real review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

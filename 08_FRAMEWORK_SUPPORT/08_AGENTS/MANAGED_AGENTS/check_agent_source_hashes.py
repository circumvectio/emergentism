#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_agent_source_hashes.py — ROSETTA-CASTE managed-agents hash gate.

Created 2026-08-19 (E3 manifest hand, runtime-DAV L4 execution lane).

[S] What it checks (stdlib only):
  1. MANIFEST CHECK — recomputes sha256 for every file listed in
     agents/MANIFEST.sha256 and compares against the pinned hash; also flags
     any *.agent.yaml on disk that the manifest does not list, and any listed
     file absent from disk. A diff between manifest and disk is a defect in
     the CHANGED file, never the manifest alone.
  2. GENERATED-ROW CHECK — reads /Users/Yves/Documents/.codex/agents/rows/*.toml
     for pinned source_sha256 keys (with their source_spec paths) and compares
     each pin against the live hash of its source YAML. Every divergence is
     reported as:
       GENERATED-ROW STALE (known compiler gap — sync_root_agentz_dispatch.py absent)
     so the silent divergence is a NAMED red, never silence.

Exit codes:
  0  manifest matches disk AND every pinned row matches its live YAML hash
  1  manifest-side defect (hash mismatch, listed-but-missing, unlisted-on-disk,
     or manifest absent/unparseable)
  2  manifest clean, but at least one generated row is stale or unreadable
     (the named red — known compiler gap)

--self-test:
  Copies the manifest to a temp file, corrupts exactly ONE hash, and verifies
  the manifest checker FAILS on exactly that file for exactly that reason
  (HASH MISMATCH; expected == the corrupted pin; actual == the live disk hash;
  no other divergence reported). Gates fail three ways — lie, never run, read
  the wrong file — so the self-test must fail for the RIGHT reason, not merely
  fail. Temp-only; nothing on disk is modified. Prints SELF-TEST PASS/FAIL.
"""

import hashlib
import re
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent          # .../MANAGED_AGENTS
AGENTS_DIR = SCRIPT_DIR / "agents"
MANIFEST_PATH = AGENTS_DIR / "MANIFEST.sha256"
DOCUMENTS_ROOT = SCRIPT_DIR.parents[3]                # .../Documents (source_spec paths are relative to this)
ROWS_DIR = Path("/Users/Yves/Documents/.codex/agents/rows")
STALE_LABEL = "GENERATED-ROW STALE (known compiler gap — sync_root_agentz_dispatch.py absent)"

_MANIFEST_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_manifest(path: Path) -> dict:
    """filename -> pinned sha256 (lowercase). Comment/blank lines skipped."""
    entries = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _MANIFEST_LINE.match(line)
        if not m:
            raise ValueError(f"{path}:{lineno}: unparseable manifest line: {line!r}")
        entries[m.group(2)] = m.group(1).lower()
    return entries


def check_manifest(manifest_path: Path, agents_dir: Path):
    """Returns (divergences, report_lines).

    divergences: list of (filename, kind, expected, actual) where kind is one of
    HASH MISMATCH / MISSING FROM DISK / UNLISTED ON DISK.
    """
    entries = parse_manifest(manifest_path)
    divergences = []
    lines = []
    for name, expected in entries.items():
        p = agents_dir / name
        if not p.is_file():
            divergences.append((name, "MISSING FROM DISK", expected, None))
            lines.append(f"  MISSING   {name} — listed in manifest, absent on disk")
            continue
        actual = sha256_of(p)
        if actual != expected:
            divergences.append((name, "HASH MISMATCH", expected, actual))
            lines.append(
                f"  MISMATCH  {name}\n"
                f"            manifest {expected}\n"
                f"            disk     {actual}"
            )
        else:
            lines.append(f"  OK        {name}")
    for p in sorted(agents_dir.glob("*.agent.yaml")):
        if p.name not in entries:
            divergences.append((p.name, "UNLISTED ON DISK", None, sha256_of(p)))
            lines.append(f"  UNLISTED  {p.name} — on disk, not in manifest")
    return divergences, lines


def _find_key(obj, key):
    """Recursive first-hit search for a key in nested dicts/lists (TOML tables)."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            hit = _find_key(v, key)
            if hit is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            hit = _find_key(v, key)
            if hit is not None:
                return hit
    return None


def parse_row(path: Path):
    """Returns (source_spec, source_sha256) — either may be None."""
    text = path.read_text(encoding="utf-8")
    spec = sha = None
    try:
        import tomllib
        data = tomllib.loads(text)
        spec = _find_key(data, "source_spec")
        sha = _find_key(data, "source_sha256")
    except Exception:
        pass  # fall through to regex
    if spec is None:
        m = re.search(r'^\s*source_spec\s*=\s*"([^"]+)"', text, re.M)
        spec = m.group(1) if m else None
    if sha is None:
        m = re.search(r'^\s*source_sha256\s*=\s*"([0-9a-fA-F]{64})"', text, re.M)
        sha = m.group(1) if m else None
    return spec, (sha.lower() if isinstance(sha, str) else None)


def check_rows():
    """Returns (reds, report_lines). reds = row filenames that are stale/unreadable."""
    lines = []
    reds = []
    if not ROWS_DIR.is_dir():
        lines.append(f"  (rows dir not found: {ROWS_DIR} — nothing to compare)")
        return reds, lines
    tomls = sorted(ROWS_DIR.glob("*.toml"))
    if not tomls:
        lines.append(f"  (no *.toml rows in {ROWS_DIR} — nothing to compare)")
        return reds, lines
    for t in tomls:
        try:
            spec, pin = parse_row(t)
        except Exception as e:
            reds.append(t.name)
            lines.append(f"  UNREADABLE {t.name} — {e}")
            continue
        if pin is None:
            lines.append(f"  NO PIN    {t.name} — no source_sha256 key; nothing to compare")
            continue
        if spec is None:
            reds.append(t.name)
            lines.append(f"  NO SPEC   {t.name} — source_sha256 pinned but no source_spec path; cannot locate source")
            continue
        yaml_path = (DOCUMENTS_ROOT / spec).resolve()
        if not yaml_path.is_file():
            reds.append(t.name)
            lines.append(f"  NO SOURCE {t.name} — source_spec not on disk: {spec}")
            continue
        live = sha256_of(yaml_path)
        if live != pin:
            reds.append(t.name)
            lines.append(
                f"  {STALE_LABEL}\n"
                f"            row      {t.name}\n"
                f"            pinned   {pin}\n"
                f"            live     {live}  ({yaml_path.name})"
            )
        else:
            lines.append(f"  OK        {t.name} — pin matches live {yaml_path.name}")
    return reds, lines


def self_test() -> int:
    """Corrupt ONE hash in a temp copy of the manifest; the checker must fail on
    exactly that file for exactly that reason. Temp-only; disk untouched."""
    print("SELF-TEST: corrupt-one-hash drill against a temp copy of the manifest")
    try:
        entries = parse_manifest(MANIFEST_PATH)
    except Exception as e:
        print(f"  cannot parse real manifest: {e}")
        print("SELF-TEST FAIL")
        return 1
    if not entries:
        print("  real manifest lists no files")
        print("SELF-TEST FAIL")
        return 1
    target = sorted(entries)[0]
    good = entries[target]
    bad = good[:-1] + ("0" if good[-1] != "0" else "1")
    manifest_text = MANIFEST_PATH.read_text(encoding="utf-8")
    corrupted_text = manifest_text.replace(good, bad, 1)
    if corrupted_text == manifest_text:
        print(f"  could not corrupt hash for {target}")
        print("SELF-TEST FAIL")
        return 1
    with tempfile.TemporaryDirectory() as td:
        tmp_manifest = Path(td) / "MANIFEST.sha256"
        tmp_manifest.write_text(corrupted_text, encoding="utf-8")
        try:
            divergences, _ = check_manifest(tmp_manifest, AGENTS_DIR)
        except Exception as e:
            print(f"  checker crashed instead of reporting: {e}")
            print("SELF-TEST FAIL")
            return 1
    print(f"  corrupted entry : {target}")
    print(f"  pinned (bad)    : {bad}")
    print(f"  expected actual : {good}")
    print(f"  divergences     : {[(d[0], d[1]) for d in divergences]}")
    # Must fail on exactly that file, for exactly that reason.
    if len(divergences) != 1:
        print(f"  WRONG: expected exactly 1 divergence, got {len(divergences)}")
        print("SELF-TEST FAIL")
        return 1
    name, kind, expected, actual = divergences[0]
    if name != target:
        print(f"  WRONG FILE: failed on {name}, corrupted {target}")
        print("SELF-TEST FAIL")
        return 1
    if kind != "HASH MISMATCH":
        print(f"  WRONG REASON: {kind} instead of HASH MISMATCH")
        print("SELF-TEST FAIL")
        return 1
    if expected != bad or actual != good:
        print("  WRONG HASHES: reported expected/actual do not match the drill")
        print("SELF-TEST FAIL")
        return 1
    print("  checker failed on exactly the corrupted file, for exactly the corrupted-hash reason")
    print("SELF-TEST PASS")
    return 0


def main(argv) -> int:
    if "--self-test" in argv:
        return self_test()

    print("check_agent_source_hashes — ROSETTA-CASTE managed-agents hash gate")
    print(f"manifest: {MANIFEST_PATH}")
    if not MANIFEST_PATH.is_file():
        print("  DEFECT: manifest absent — the gate cannot run (a gate that never ran proves nothing)")
        return 1
    try:
        manifest_divergences, manifest_lines = check_manifest(MANIFEST_PATH, AGENTS_DIR)
    except Exception as e:
        print(f"  DEFECT: manifest unparseable — {e}")
        return 1
    print("MANIFEST CHECK (agents/*.agent.yaml vs MANIFEST.sha256):")
    for line in manifest_lines:
        print(line)

    print(f"GENERATED-ROW CHECK ({ROWS_DIR}/*.toml pinned source_sha256 vs live YAML):")
    row_reds, row_lines = check_rows()
    for line in row_lines:
        print(line)

    if manifest_divergences:
        print(f"VERDICT: FAIL — {len(manifest_divergences)} manifest divergence(s); "
              f"the defect is in the CHANGED file, never the manifest alone (exit 1)")
        return 1
    if row_reds:
        print(f"VERDICT: MANIFEST OK; {len(row_reds)} generated row(s) RED — {STALE_LABEL} (exit 2)")
        return 2
    print("VERDICT: OK — manifest matches disk; all pinned rows match live hashes (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

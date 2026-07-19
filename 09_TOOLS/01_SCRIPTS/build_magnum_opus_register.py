#!/usr/bin/env python3
# rosetta:
#   primary_level: L3
#   primary_column: Meta
#   operator: "Kṛṣṇa ◇"
#   tier: "Executive"
#   regime: "Vaiśya"
#   register: "[S]"
#   canonical_phrase: "Canonical register builder — completion plan §2, additive-only"
# type: tool
# title: build_magnum_opus_register.py — FILE/FOLDER register generator + drift checker
# status: "ACTIVE 2026-07-19 — additive-only remediation wave (receipt 141A gate)"
# owner: 01_EMERGENTISM
"""Build the Magnum Opus canonical registers (completion plan §2).

Outputs (under 00_META/registers/):
  FILE_REGISTER.json   — one entry per TRACKED file (git ls-files, working tree)
  FOLDER_REGISTER.json — one entry per populated tracked directory
  README.md            — regeneration note (constant content)

Modes:
  --write  generate both registers (+ README.md if absent)
  --check  re-derive both registers and report drift;
           exit 1 on drift (changed/added/removed paths listed), exit 0 when clean

Deterministic: entries sorted by path; no timestamps; no HEAD hash.
Evidence tiers: [S] disk-read, [I] inference. Additive-only: this script never
moves, deletes, tombstones, or commits anything.

Derivation notes:
  * authority_status: frontmatter `status` (cheap first-block YAML scan) —
    STAGED/PENDING/[D]/DRAFT -> 'staged'; else SIGNED -> 'signed'; else 'unrated'.
  * evidence_tier: first [S]/[I]/[C]/[D]/[B]/[A] token in frontmatter
    `evidence_tier`, else null (spec: frontmatter evidence_tier else null).
  * k_relation: named kernel surfaces per
    00_META/00_THE_MAGNUM_OPUS_BLUEPRINT_PENDING_SIGNATURE.md §1.0 — exact file
    matches for K-1..K-6; K-7 = prefix surfaces 11_UPLINK/50_AUDITS_AND_EXECUTIONS/
    + 12_PUBLIC_SITE/record/ + the SYNTHETIC_GAP postures source (canonical path).
  * inbound_references: single-pass count of exact-basename token hits across all
    tracked .md/.html files (self-included, per spec's "grep hits for the
    basename"), capped at 999. Token-based; basenames with non-word characters
    (e.g. U+00D7) may undercount — documented approximation of git grep -o.
  * disposition: from 00_META/05/06 disposition manifests (current docs) —
    ARCHIVE/TOMBSTONE/STONE -> 'tombstone-candidate';
    ABSORB/REVISE/STAGED/ROUTE/SUCCESSION -> 'staged'; else 'keep'.
  * FILE_REGISTER represents itself with the stable marker entry
    path='00_META/registers/FILE_REGISTER.json', sha256='SELF'.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG_DIR_REL = "00_META/registers"
REG_DIR = os.path.join(REPO_ROOT, REG_DIR_REL)
FILE_REG_REL = REG_DIR_REL + "/FILE_REGISTER.json"
FOLDER_REG_REL = REG_DIR_REL + "/FOLDER_REGISTER.json"
README_REL = REG_DIR_REL + "/README.md"
SELF_PATH = FILE_REG_REL  # register represents itself at this path
REF_CAP = 999
FM_READ_BYTES = 16384

FILE_MANIFEST = os.path.join(REPO_ROOT, "00_META", "05_MAGNUM_OPUS_FILE_DISPOSITION_MANIFEST_PENDING_SIGNATURE_2026_07_19.csv")
FOLDER_MANIFEST = os.path.join(REPO_ROOT, "00_META", "06_MAGNUM_OPUS_FOLDER_DISPOSITION_MANIFEST_PENDING_SIGNATURE_2026_07_19.csv")

# Blueprint §1.0 named kernel surfaces (verified on disk 2026-07-19 [S]).
K_EXACT = {
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md": "K-1",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/41_THE_GLYPH_TRANSFORMATIONS.md": "K-1",
    "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md": "K-2",
    "06_ONTOLOGY/00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md": "K-2",
    "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md": "K-3",
    "06_ONTOLOGY/04_THE_CONJECTURES.md": "K-4",
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md": "K-5",
    "06_ONTOLOGY/06_THE_REVELATIONS.md": "K-6",
    "02_EPISTEMOLOGY/00_THE_SYNTHETIC_GAP_AND_FOUR_POSTURES_v0.1.md": "K-7",
}
K_PREFIX = (
    ("11_UPLINK/50_AUDITS_AND_EXECUTIONS/", "K-7"),
    ("12_PUBLIC_SITE/record/", "K-7"),
)

TIER_RE = re.compile(r"\[(S|I|C|D|B|A)\]")
TOKEN_RE = re.compile(r"[\w.\-]+", re.UNICODE)
CORPUS_EXTS = (".md", ".html")
CONFIG_NAMES = {".gitignore", ".gitattributes", ".gitmodules", "license", "makefile"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".lock"}

README_BODY = """# Registers — regeneration (completion plan §2)
Regenerate both registers: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write` (run from anywhere; repo root is derived from the script path).
Verify drift: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --check` — exit 0 clean, exit 1 lists changed/added/removed paths.
Source of truth: `git ls-files` (tracked files) + working-tree bytes; registers are derived artifacts — never hand-edit entries.
Additive-only gate (receipt 141A): these files are inventory/navigation only; they authorize no move, tombstone, promotion, or commit.
"""


def git_ls_files():
    out = subprocess.run(
        ["git", "-C", REPO_ROOT, "ls-files", "-z"],
        check=True, capture_output=True,
    ).stdout
    return sorted(p.decode("utf-8", "surrogateescape") for p in out.split(b"\0") if p)


def sha256_file(abs_path):
    h = hashlib.sha256()
    with open(abs_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_frontmatter(abs_path):
    """Cheap first-block YAML scan. Returns dict of top-level scalar fields found."""
    try:
        with open(abs_path, "rb") as fh:
            raw = fh.read(FM_READ_BYTES)
    except OSError:
        return {}
    text = raw.decode("utf-8", "replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    block = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        block.append(line)
    else:
        return {}
    fields = {}
    for line in block:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            val = m.group(2).strip().strip('"').strip("'")
            fields.setdefault(m.group(1), val)
    return fields


def authority_from_status(status):
    if not status:
        return "unrated"
    u = status.upper()
    if "STAGED" in u or "PENDING" in u or "[D]" in u or "DRAFT" in u:
        return "staged"
    if "SIGNED" in u:
        return "signed"
    return "unrated"


def evidence_tier_from(fields):
    val = fields.get("evidence_tier")
    if not val:
        return None
    m = TIER_RE.search(val)
    return m.group(0) if m else None


def artifact_class(path):
    top = path.split("/", 1)[0]
    if top in ("90_ARCHIVE", "91_COMPATIBILITY"):
        return "archive"
    if top == "12_PUBLIC_SITE":
        return "site"
    if top == "09_TOOLS":
        return "tool"
    base = path.rsplit("/", 1)[-1]
    low = base.lower()
    stem, ext = os.path.splitext(low)
    if "receipt" in low or "50_audits_and_executions" in path.lower():
        return "receipt"
    if low in CONFIG_NAMES or stem in CONFIG_NAMES or ext in CONFIG_EXTS:
        return "config"
    if ext in (".md", ".markdown"):
        return "doctrine"
    return "other"


def k_relation(path):
    if path in K_EXACT:
        return K_EXACT[path]
    for prefix, k in K_PREFIX:
        if path.startswith(prefix):
            return k
    return None


def map_disposition(raw):
    u = (raw or "").upper()
    if not u:
        return "keep"
    if "ARCHIVE" in u or "TOMBSTONE" in u or "STONE" in u:
        return "tombstone-candidate"
    if "ABSORB" in u or "REVISE" in u or "STAGED" in u or "ROUTE" in u or "SUCCESSION" in u:
        return "staged"
    return "keep"


def load_manifest_dispositions(path, key_col):
    table = {}
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                key = (row.get(key_col) or "").strip()
                if key:
                    table[key] = map_disposition(row.get("disposition"))
    except OSError:
        pass
    return table


def build_ref_index(tracked):
    """basename -> hit count across tracked .md/.html (single corpus pass)."""
    basenames = {p.rsplit("/", 1)[-1] for p in tracked}
    counts = Counter()
    for rel in tracked:
        if not rel.lower().endswith(CORPUS_EXTS):
            continue
        try:
            with open(os.path.join(REPO_ROOT, rel), "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        except OSError:
            continue
        for token, n in Counter(TOKEN_RE.findall(text)).items():
            if token in basenames:
                counts[token] += n
    return counts


def file_entry(rel, ref_counts, manifest_disp):
    if rel.startswith("00_META/registers/"):
        # Register-family artifacts are self-describing: hashing their bytes makes
        # FILE/FOLDER registers chase each other's hash on every pass (oscillation).
        # Per the completion plan's stable-SELF-marker rule, they carry SELF.
        e = self_entry()
        e["path"] = rel
        return e
    abs_path = os.path.join(REPO_ROOT, rel)
    digest = sha256_file(abs_path)
    size = os.path.getsize(abs_path)
    fields = read_frontmatter(abs_path) if rel.lower().endswith((".md", ".markdown")) else {}
    base = rel.rsplit("/", 1)[-1]
    top = rel.split("/", 1)[0]
    return {
        "path": rel,
        "sha256": digest,
        "bytes": size,
        "owner_lane": top if "/" in rel else "root",
        "artifact_class": artifact_class(rel),
        "authority_status": authority_from_status(fields.get("status")),
        "evidence_tier": evidence_tier_from(fields),
        "k_relation": k_relation(rel),
        "public_projection": rel if rel.startswith("12_PUBLIC_SITE/") else None,
        "disposition": manifest_disp.get(rel, "keep"),
        "destination": None,
        "absorber": None,
        "inbound_references": min(ref_counts.get(base, 0), REF_CAP),
        "gate": None,
        "review_state": "unreviewed",
    }


def self_entry():
    return {
        "path": SELF_PATH,
        "sha256": "SELF",
        "bytes": 0,
        "owner_lane": "00_META",
        "artifact_class": "config",
        "authority_status": "unrated",
        "evidence_tier": None,
        "k_relation": None,
        "public_projection": None,
        "disposition": "keep",
        "destination": None,
        "absorber": None,
        "inbound_references": 0,
        "gate": None,
        "review_state": "unreviewed",
    }


def folder_type(path):
    if path == ".":
        return "other"
    top = path.split("/", 1)[0]
    if top in ("00_META", "00_CONTROL"):
        return "meta"
    if top in ("90_ARCHIVE", "91_COMPATIBILITY"):
        return "archive"
    if top == "12_PUBLIC_SITE":
        return "site"
    if top == "09_TOOLS":
        return "tool"
    if top == "10_SEED":
        return "seed"
    if re.match(r"^(0[1-8]|11)_", top):
        return "lane"
    return "other"


def folder_scope_guess(door_abs):
    """One-line scope from the front door: canonical_phrase > title > description > first prose line."""
    if not door_abs:
        return None
    fields = read_frontmatter(door_abs)
    for key in ("canonical_phrase", "title", "description"):
        val = fields.get(key)
        if val:
            return val[:140]
    try:
        with open(door_abs, "rb") as fh:
            text = fh.read(FM_READ_BYTES).decode("utf-8", "replace")
    except OSError:
        return None
    in_fm = False
    for line in text.splitlines():
        s = line.strip()
        if s == "---":
            in_fm = not in_fm
            continue
        if in_fm or not s or s.startswith("#") or s.startswith("<!--"):
            continue
        return s[:140]
    return None


def build_folder_entries(tracked, manifest_disp):
    parents = {}
    for rel in tracked:
        d = rel.rsplit("/", 1)[0] if "/" in rel else "."
        parts = d.split("/") if d != "." else ["."]
        for i in range(len(parts)):
            parents.setdefault("/".join(parts[: i + 1]), 0)
        parents[d] += 1
    file_set = set(tracked)
    entries = []
    for folder in sorted(parents):
        prefix = "" if folder == "." else folder + "/"
        door = None
        for name in ("README.md", "AGENTS.md", "index.html"):
            cand = prefix + name
            if cand in file_set:
                door = cand
                break
        door_abs = os.path.join(REPO_ROOT, door) if door else None
        door_fields = read_frontmatter(door_abs) if door and door.lower().endswith(".md") else {}
        count = sum(1 for rel in tracked if rel.startswith(prefix)) if prefix else len(tracked)
        entries.append({
            "path": folder,
            "type": folder_type(folder),
            "nearest_front_door": door,
            "front_door_requirement": "present" if door else "missing",
            "owns": folder_scope_guess(door_abs),
            "must_not_own": None,
            "status": authority_from_status(door_fields.get("status")),
            "tracked_file_count": count,
            "disposition": manifest_disp.get(folder, "keep"),
            "gate": None,
            "review_state": "unreviewed",
        })
    return entries


def derive():
    tracked = git_ls_files()
    file_disp = load_manifest_dispositions(FILE_MANIFEST, "path")
    folder_disp = load_manifest_dispositions(FOLDER_MANIFEST, "folder")
    ref_counts = build_ref_index(tracked)
    file_entries = [file_entry(rel, ref_counts, file_disp) for rel in tracked]
    file_entries.append(self_entry())
    file_entries.sort(key=lambda e: e["path"])
    folder_entries = build_folder_entries(tracked, folder_disp)
    file_doc = {
        "schema": "magnum-opus/file-register/v1",
        "generator": "09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py",
        "source": "git ls-files + working-tree bytes (deterministic; no timestamps)",
        "entry_count": len(file_entries),
        "entries": file_entries,
    }
    folder_doc = {
        "schema": "magnum-opus/folder-register/v1",
        "generator": "09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py",
        "source": "git ls-files directory closure (deterministic; no timestamps)",
        "entry_count": len(folder_entries),
        "entries": folder_entries,
    }
    return file_doc, folder_doc


def dump(doc, abs_path):
    with open(abs_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def diff_docs(name, derived, on_disk):
    d_entries = {e["path"]: e for e in derived.get("entries", [])}
    o_entries = {e["path"]: e for e in on_disk.get("entries", [])}
    added = sorted(set(d_entries) - set(o_entries))
    removed = sorted(set(o_entries) - set(d_entries))
    changed = []
    for p in sorted(set(d_entries) & set(o_entries)):
        if d_entries[p] != o_entries[p]:
            fields = [k for k in d_entries[p] if d_entries[p].get(k) != o_entries[p].get(k)]
            changed.append((p, fields[:4]))
    return added, removed, changed


def main():
    ap = argparse.ArgumentParser(description="Build/check Magnum Opus canonical registers (completion plan §2).")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="generate FILE_REGISTER.json + FOLDER_REGISTER.json")
    mode.add_argument("--check", action="store_true", help="re-derive and report drift (exit 1 on drift)")
    args = ap.parse_args()

    file_doc, folder_doc = derive()

    if args.write:
        os.makedirs(REG_DIR, exist_ok=True)
        dump(file_doc, os.path.join(REG_DIR, "FILE_REGISTER.json"))
        dump(folder_doc, os.path.join(REG_DIR, "FOLDER_REGISTER.json"))
        readme_abs = os.path.join(REG_DIR, "README.md")
        if not os.path.exists(readme_abs):
            with open(readme_abs, "w", encoding="utf-8") as fh:
                fh.write(README_BODY)
        print(f"wrote {FILE_REG_REL} ({file_doc['entry_count']} entries)")
        print(f"wrote {FOLDER_REG_REL} ({folder_doc['entry_count']} entries)")
        print(f"ensured {README_REL}")
        return 0

    drift = False
    for rel, derived in ((FILE_REG_REL, file_doc), (FOLDER_REG_REL, folder_doc)):
        abs_path = os.path.join(REPO_ROOT, rel)
        try:
            with open(abs_path, encoding="utf-8") as fh:
                on_disk = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"DRIFT {rel}: unreadable on disk ({exc})")
            drift = True
            continue
        added, removed, changed = diff_docs(rel, derived, on_disk)
        if added or removed or changed:
            drift = True
            print(f"DRIFT {rel}: +{len(added)} added, -{len(removed)} removed, ~{len(changed)} changed")
            for p in added[:25]:
                print(f"  added   {p}")
            for p in removed[:25]:
                print(f"  removed {p}")
            for p, fields in changed[:25]:
                print(f"  changed {p} ({', '.join(fields)})")
        else:
            print(f"clean {rel} ({derived['entry_count']} entries)")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())

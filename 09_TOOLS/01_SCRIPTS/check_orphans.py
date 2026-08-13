#!/usr/bin/env python3
"""Gate the corpus's in-degree: how many live documents nothing points at.

WHY THIS EXISTS
---------------
The 2026-08-13 census (`00_HANDOFF/CENSUS_HANDOFF_2026_08_13.md` §2) recorded
"no orphan/reachability gate exists at all" as the one instrument defect with no
instrument behind it, and §3 measured a third of the live corpus with zero
inbound edge. The 2026-08-04 receipt `00_HANDOFF/0_REF_ORPHAN_VERIFICATION_2026_08_04.md`
named 7 candidates; nine days later all 7 were still at in-degree 0 and the
receipt that named them was itself an orphan. Unfindability reproduced on the
instrument built to catch it. Nothing was watching, so nothing moved.

This measures IN-DEGREE, not crawl-reachability from a root. A document with
in-degree 0 is one no other live document points at, by any of the three
channels below. That is the same quantity the census lens measured, so the two
numbers are comparable (see MEASUREMENT NOTE for why they are not equal).

WHAT COUNTS AS AN INBOUND EDGE
------------------------------
  1. A relative markdown link  `[text](target)`  from another live document.
  2. A frontmatter relation entry: parents / sources / depends_on / supersedes.
  3. A row in a HAND-CURATED register naming the document.

THE REGISTER CHANNEL IS NARROWER THAN IT LOOKS, AND THAT IS THE POINT
---------------------------------------------------------------------
Most files under `00_META/registers/` are GENERATED CENSUSES: deterministic
walks of the tree that list every tracked file. `00_META/registers/README.md`
declares this in the corpus's own words -- "deterministic derived artifacts ...
they do not become source authority or evidence by being present here" and
"inventory/navigation only; they authorize no move, tombstone, promotion, or
commit". `FILE_REGISTER.json` declares its own source as `git ls-files`.

Being enumerated by a census you were auto-added to is not being pointed at.
Counting those rows as edges builds a gate that CANNOT FAIL:

    MEASURED 2026-08-13 on this tree -- CORPUS_INDEX.jsonl alone names
    529 of the 529 orphans this gate finds. Admit it as an edge channel and
    the reported orphan count drops to 0 and stays there forever.

The census predicted exactly this failure and wrote it down before it happened
(reachability lens, finding on `00_META/registers/CORPUS_INDEX.jsonl`):
"If a future sweep counts generated-census rows as inbound edges it will report
~45 orphans instead of 432 and conclude the corpus is healthy."

So generated censuses are denied by name in GENERATED_CENSUSES, and a second,
structural guard denies ANY register whose coverage exceeds CENSUS_COVERAGE_MAX
of the live corpus -- because a new generated register dropped into that folder
must not be able to silently neuter this gate. The one hand-curated register the
census found, `00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json`, does count.

MEASUREMENT NOTE
----------------
This instrument finds MORE orphans than the census lens did (529 vs 432 on the
same 1,387-document denominator -- the walk agrees exactly). The census attributed
edges more generously: it counted raw frontmatter entries rather than entries that
resolve to a live document (it reported 713 `parents` edges where only 586 resolve,
41 `owner` where 3 resolve, 113 `sources` where 28 resolve), and it added a
unique-basename fallback worth ~12 documents. Neither number is wrong; they are
different instruments. Per the decay rule, both are true of a date and of a tree
state. Re-run before repairing anything on either one's basis.

This gate does not care which is "right". It is a RATCHET on a delta: stable
false positives cancel on both sides of a move, exactly as `check_all_citations.py`
argues for its own 2,043.

USAGE
-----
    python3 09_TOOLS/01_SCRIPTS/check_orphans.py \\
        --baseline 00_META/registers/ORPHAN_BASELINE.json --write-baseline
    python3 09_TOOLS/01_SCRIPTS/check_orphans.py \\
        --baseline 00_META/registers/ORPHAN_BASELINE.json

Exit 0 only when the orphan count is at or below --max-orphans (default 0), or
at or below the recorded baseline when --baseline names an existing file. The
count can go down and never up.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Walk rules copied from `build_corpus_index.py` (EXCLUDE_PARTS + its
# dot-directory rule) rather than invented here, so "live document" means the
# same thing to the index and to this gate. The dot-directory rule is what keeps
# the 41 vendored Lean/mathlib `.md` files under `09_TOOLS/03_SIMULATIONS/formal_reap/.lake/`
# out of the denominator -- the census warned that an orphan gate which fails to
# exclude them inflates its count by ~10%.
EXCLUDE_PARTS = {
    ".git", "90_ARCHIVE", "node_modules", "__pycache__",
    "vendor", "91_COMPATIBILITY",
}

INLINE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
NON_PATH_SCHEME = re.compile(r"^(https?:|mailto:|tel:|#|data:)")

# The four relation keys named in this gate's spec. Measured on this tree, they
# carry 698 of the 707 frontmatter edges that resolve to a live document
# (parents 586, depends_on 83, sources 28, supersedes 1). The deprecated spelling
# `depends` carries the other 9; widen this tuple with evidence if that spelling
# is ever re-canonicalised rather than migrated.
FM_RELATION_KEYS = ("parents", "sources", "depends_on", "supersedes")

# ---------------------------------------------------------------------------
# Register channel
# ---------------------------------------------------------------------------

REGISTER_DIR = ROOT / "00_META" / "registers"

# Hand-curated registers outside `registers/`. Someone chose to write each row.
CURATED_REGISTERS = (ROOT / "00_META" / "ACTIVE_RECEIPT_CITATION_REGISTRY.json",)

# Denied by name. Every one of these is regenerated by walking the tree or by
# `git ls-files`, per `00_META/registers/README.md`. A row here is proof-of-tracked,
# never proof-of-referenced.
GENERATED_CENSUSES = {
    "CORPUS_INDEX.jsonl",            # build_corpus_index.py -- walks every live .md
    "FILE_REGISTER.json",            # build_magnum_opus_register.py -- git ls-files
    "FOLDER_REGISTER.json",          # build_magnum_opus_register.py -- tracked-dir closure
    "CLAIM_CARD_REGISTER.json",      # compile_claim_cards.py --write
    "CLAIM_GRAPH.json",              # compile_claim_cards.py --write
    "CLAIM_LIFECYCLE_INVENTORY.json",  # compile_claim_cards.py --write
    "CITATION_BASELINE.json",        # check_all_citations.py --write-baseline
}

# Structural backstop for a generated register nobody thought to add above: a
# register that names more than this share of the live corpus is a census, not a
# citation. Denying it by measurement means the gate cannot be neutered by
# dropping a new inventory into the folder.
CENSUS_COVERAGE_MAX = 0.50

# ---------------------------------------------------------------------------
# The two hard-coded orphan exclusions
# ---------------------------------------------------------------------------
#
# Both are DECLARATION-GATED: a file earns the exemption only by saying so in its
# own frontmatter. That keeps the exemption from silently widening -- and it is
# why each is a predicate over a declaration, not a path pattern over a name.
# The measured membership of each class on 2026-08-13 is recorded beside it, so a
# future reader can see immediately if the class has grown.

def declares_itself_a_register(fm: str) -> bool:
    """Exclusion 1 -- a document that is ITSELF an index/register.

    WHY: a register is a ROOT of reachability. Its whole function is out-degree:
    it supplies inbound edges to other documents. Demanding that something point
    AT the index is circular -- it inverts the direction of the artifact. The
    corpus says so itself in `00_META/registers/README.md`: the registers are
    "navigation, audit, and routing views".

    Declaration channel: a frontmatter `type:` beginning `register` or `index`.
    MEASURED 2026-08-13: exactly 1 live document qualifies,
    `00_META/registers/README.md` (`type: register-front-door`), and it currently
    has an inbound edge -- so this exclusion changes the count by 0 today. It is a
    standing guard, not a discount: if the register front door ever loses its last
    inbound link, the gate must not report the map as lost cargo.
    """
    m = re.search(r"^type\s*:\s*[\"']?([A-Za-z0-9_-]+)", fm, re.M)
    return bool(m and re.match(r"(register|index)", m.group(1), re.I))


def declares_itself_a_tombstone(fm: str) -> bool:
    """Exclusion 2 -- a tombstone that exists to be pointed at, not to point.

    WHY: a destructive-act tombstone is the record left AT THE SITE of the act, so
    that whoever lands on that directory finds out what happened there. It is
    addressed by location, not by citation. Requiring an index to link it would
    move the record away from the place it documents, which is the one thing it
    must not do. It exists to be found in place.

    Declaration channel: a `tombstone:` BLOCK in frontmatter -- the custody record
    (date, actor, parent_act, receipt, recoverable, sha256_at_deletion).
    MEASURED 2026-08-13: exactly 1 live document qualifies,
    `12_PUBLIC_SITE/book-pwa/NODE_MODULES_TOMBSTONE.md`, and it IS an orphan --
    so this exclusion removes exactly 1 from the count.

    DELIBERATELY NOT WIDENED: 12 further orphans carry the word "tombstone" inside
    a free-text `status:` string (K3 TOMBSTONE / KINTSUGI TOMBSTONE / FORWARDING
    STUB). Exempting on a status substring would exempt anything whose prose
    happens to say the word, and several of those 12 are superseded doctrine a
    reader may still need to reach. They are reported as a diagnostic below and
    left in the count; widening this is an owner ruling, not a script's call.
    """
    return bool(re.search(r"^tombstone\s*:", fm, re.M))


# ---------------------------------------------------------------------------
# Corpus walk and parsing
# ---------------------------------------------------------------------------

def walk() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        parts = path.relative_to(ROOT).parts
        if EXCLUDE_PARTS & set(parts):
            continue
        if any(p.startswith(".") for p in parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def fm_relation_values(fm: str) -> list[str]:
    """Scalar and list values under the four relation keys.

    Same tolerant hand-rolled reader as `check_all_citations.py`: the corpus's
    frontmatter is hand-written and not schema-validated, so a strict YAML parse
    would drop real files.
    """
    out: list[str] = []
    key: str | None = None
    for raw in fm.splitlines():
        line = raw.rstrip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip("\"'")
            if key in FM_RELATION_KEYS and val and not val.startswith("#"):
                out.append(val)
            continue
        m = re.match(r"^\s+-\s+(.*)$", line)
        if m and key in FM_RELATION_KEYS:
            val = m.group(1).strip().strip("\"'").split(" #")[0].strip()
            if val:
                out.append(val)
    return out


def json_strings(node, sink: list[str]) -> None:
    if isinstance(node, str):
        sink.append(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            sink.append(k)
            json_strings(v, sink)
    elif isinstance(node, list):
        for v in node:
            json_strings(v, sink)


def register_strings(path: Path) -> list[str]:
    """Every string scalar in a .json or .jsonl register, keys included.

    Registers in this corpus disagree about shape -- some key rows BY path, some
    carry the path as a value. Harvesting every string is the only shape-agnostic
    read, and it errs toward finding an edge, which is the conservative direction
    for a gate that must not over-report orphans.
    """
    sink: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return sink
    if path.suffix == ".jsonl":
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                json_strings(json.loads(line), sink)
            except json.JSONDecodeError:
                continue
    else:
        try:
            json_strings(json.loads(text), sink)
        except json.JSONDecodeError:
            return sink
    return sink


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def scan() -> dict:
    live = walk()
    live_set = {p.resolve() for p in live}
    rel_of = {p.resolve(): p.relative_to(ROOT).as_posix() for p in live}

    by_basename: dict[str, list[Path]] = defaultdict(list)
    for p in live:
        by_basename[p.name].append(p.resolve())
    unique_basenames = {n: v[0] for n, v in by_basename.items() if len(v) == 1}

    def resolve(src: Path, href: str):
        if NON_PATH_SCHEME.match(href):
            return None
        href = href.split("#")[0].strip()
        if not href:
            return None
        for cand in ((src.parent / href), (ROOT / href.lstrip("/"))):
            try:
                target = cand.resolve()
            except OSError:
                continue
            if target in live_set:
                return target
        return None

    inbound: Counter = Counter()
    channels: dict[Path, set] = defaultdict(set)

    for src in live:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        here = src.resolve()

        for href in INLINE.findall(text):
            target = resolve(src, href)
            if target and target != here:          # a self-link is not an edge
                inbound[target] += 1
                channels[target].add("link")

        for value in fm_relation_values(frontmatter(text)):
            target = resolve(src, value)
            if target and target != here:
                inbound[target] += 1
                channels[target].add("frontmatter")

    # -- register channel ---------------------------------------------------
    candidates = [p for p in sorted(REGISTER_DIR.glob("*"))
                  if p.suffix in (".json", ".jsonl")]
    candidates += [p for p in CURATED_REGISTERS if p.exists()]

    all_rels = set(rel_of.values())
    resolved_of = {rel: resolved for resolved, rel in rel_of.items()}

    registers_counted, registers_denied = [], []
    for reg in candidates:
        strings = register_strings(reg)
        if not strings:
            continue
        covered = {s for s in strings if s in all_rels}
        named_bases = {Path(s).name for s in strings if s.endswith(".md")}
        for name in named_bases & unique_basenames.keys():
            covered.add(rel_of[unique_basenames[name]])
        share = len(covered) / len(live) if live else 0.0

        if reg.name in GENERATED_CENSUSES:
            registers_denied.append((reg.name, len(covered), share, "generated census (by name)"))
            continue
        if share > CENSUS_COVERAGE_MAX:
            registers_denied.append((reg.name, len(covered), share, "coverage guard -- a census, not a citation"))
            continue

        registers_counted.append((reg.name, len(covered), share))
        for rel in covered:
            resolved = resolved_of[rel]
            inbound[resolved] += 1
            channels[resolved].add("register")

    # -- orphans and exclusions --------------------------------------------
    orphans, excluded, loose_tombstones = [], [], []
    for p in live:
        if inbound.get(p.resolve()):
            continue
        rel = p.relative_to(ROOT).as_posix()
        try:
            fm = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            fm = ""
        if declares_itself_a_register(fm):
            excluded.append((rel, "declares itself an index/register"))
            continue
        if declares_itself_a_tombstone(fm):
            excluded.append((rel, "declares a tombstone: custody block"))
            continue
        status = re.search(r"^status\s*:\s*(.+)$", fm, re.M)
        if status and re.search(r"tombstone", status.group(1), re.I):
            loose_tombstones.append(rel)
        orphans.append(rel)

    return {
        "live": len(live),
        "orphans": sorted(orphans),
        "excluded": sorted(excluded),
        "loose_tombstones": sorted(loose_tombstones),
        "registers_counted": registers_counted,
        "registers_denied": registers_denied,
        "edges_by_channel": dict(Counter(
            c for s in channels.values() for c in s)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-orphans", type=int, default=0)
    ap.add_argument("--baseline", type=Path)
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    r = scan()
    orphans = r["orphans"]
    n = len(orphans)

    print(f"live documents scanned : {r['live']}")
    print(f"with an inbound edge   : {r['live'] - n - len(r['excluded'])}")
    print(f"ORPHANS (in-degree 0)  : {n}   ({100 * n / r['live']:.1f}%)")
    print(f"documents receiving each channel: {r['edges_by_channel']}")

    print("\nregister channel")
    for name, cov, share in r["registers_counted"]:
        print(f"    COUNTED  {name:38} names {cov:5d} live docs ({share:5.1%})")
    for name, cov, share, why in r["registers_denied"]:
        print(f"    DENIED   {name:38} names {cov:5d} live docs ({share:5.1%})  -- {why}")

    print("\nhard-coded exclusions (declaration-gated)")
    for rel, why in r["excluded"]:
        print(f"    {rel}  -- {why}")
    if r["loose_tombstones"]:
        print(f"\ndiagnostic: {len(r['loose_tombstones'])} orphans say \"tombstone\" in a free-text")
        print("    status: string. NOT excluded -- widening the exemption to a status")
        print("    substring is an owner ruling. Counted as orphans above.")

    lanes = Counter(o.split("/")[0] for o in orphans)
    print("\ntop orphan lanes")
    for lane, count in lanes.most_common(8):
        print(f"    {lane:36} {count:5d}")

    if args.json:
        args.json.write_text(json.dumps(r, indent=1), encoding="utf-8")

    limit = args.max_orphans
    if args.baseline and args.baseline.exists():
        limit = json.loads(args.baseline.read_text(encoding="utf-8"))["orphans"]
        print(f"\nbaseline               : {limit}")
    if args.write_baseline and args.baseline:
        args.baseline.write_text(
            json.dumps({"orphans": n, "live": r["live"]}), encoding="utf-8")
        print(f"baseline written       : {n}")
        return 0

    if n > limit:
        print(f"\nFAIL - {n} orphans exceeds {limit}.")
        for rel in orphans[:25]:
            print(f"   {rel}")
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

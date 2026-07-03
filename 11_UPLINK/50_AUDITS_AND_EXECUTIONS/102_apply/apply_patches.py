#!/usr/bin/env python3
"""
Idempotent, atomic apply-guard for the Burrisphere equator-optimum scope-clause patches.

Consumes manifest.json (a list of scope-clause insertions) and applies each SAFELY:
  * idempotent  — skips if the marker text is already present (never double-inserts)
  * anchored    — only inserts where the anchor substring occurs EXACTLY ONCE (else skips)
  * atomic      — writes a temp file + os.replace() (atomic rename); no partial writes
  * race-safe   — compare-and-swap on content hash: if a concurrent committer changed the
                  file between read and write, that patch aborts (reports 'raced') and is
                  left for a re-run — it never clobbers another writer. mtime-only touches
                  (the iCloud committer) do NOT trip it, since it compares CONTENT hash.

DEFAULT IS DRY-RUN. It writes nothing until you pass --apply. This tool is the mechanism;
applying canon still requires Yves's K2 signature (that is what invoking --apply attests).

Usage:
  python3 apply_patches.py                 # dry-run: report what WOULD change
  python3 apply_patches.py --apply         # apply (K2 signature attested by running this)
  python3 apply_patches.py --manifest X    # use a different manifest
  python3 apply_patches.py --root DIR      # override the EMERGENTISM root

Manifest entry schema (manifest.json = {"patches": [ ... ]}):
  {
    "id":       "unique id",
    "file":     "05_COSMOLOGY/00_EMERGENTISM.md",     # relative to --root
    "anchor":   "<exact substring that occurs once in the file>",
    "position": "after" | "before",                    # insert relative to the anchor's LINE
    "text":     "<the scope-clause block to insert>",  # inserted as its own paragraph
    "marker":   "<short substring of text; if already in file, SKIP as done>"
  }
"""
import argparse, hashlib, json, os, sys, tempfile

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def apply_one(root, p, do_apply):
    fid = p.get("id", "?")
    path = os.path.join(root, p["file"])
    if not os.path.isfile(path):
        return ("missing", fid, p["file"], "target file not found")
    with open(path, "r", encoding="utf-8") as fh:
        orig = fh.read()
    before_hash = sha(orig)

    marker = p.get("marker") or p["text"][:40]
    if marker in orig:
        return ("already", fid, p["file"], "marker present — already applied")

    anchor = p["anchor"]
    n = orig.count(anchor)
    if n == 0:
        return ("notfound", fid, p["file"], "anchor not found (file may have changed wording)")
    if n > 1:
        return ("ambiguous", fid, p["file"], f"anchor occurs {n}x — not unique, skipped")

    # locate the anchor's line and insert text as its own paragraph after/before that line
    idx = orig.index(anchor)
    line_start = orig.rfind("\n", 0, idx) + 1
    line_end = orig.find("\n", idx)
    if line_end == -1:
        line_end = len(orig)
    block = "\n\n" + p["text"].strip() + "\n"
    if p.get("position", "after") == "before":
        new = orig[:line_start] + p["text"].strip() + "\n\n" + orig[line_start:]
    else:
        new = orig[:line_end] + block + orig[line_end:]

    if not do_apply:
        return ("would", fid, p["file"], f"anchor ok, marker absent — would insert {len(p['text'])} chars")

    # compare-and-swap: re-read, verify unchanged since we computed, then atomic replace
    with open(path, "r", encoding="utf-8") as fh:
        current = fh.read()
    if sha(current) != before_hash:
        return ("raced", fid, p["file"], "file changed under us since read — skipped, re-run")
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".patch_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tf:
            tf.write(new)
        os.replace(tmp, path)   # atomic on POSIX
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return ("applied", fid, p["file"], f"inserted {len(p['text'])} chars")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry-run)")
    ap.add_argument("--manifest", default=os.path.join(os.path.dirname(__file__), "manifest.json"))
    ap.add_argument("--root", default="/Users/Yves/Documents/01_EMERGENTISM")
    args = ap.parse_args()

    with open(args.manifest, "r", encoding="utf-8") as fh:
        patches = json.load(fh)["patches"]

    print(f"{'APPLY' if args.apply else 'DRY-RUN'}  |  {len(patches)} patches  |  root={args.root}\n")
    tally = {}
    for p in patches:
        status, fid, f, msg = apply_one(args.root, p, args.apply)
        tally[status] = tally.get(status, 0) + 1
        sym = {"applied":"✓","would":"·","already":"=","notfound":"?","ambiguous":"!","raced":"~","missing":"x"}.get(status,"?")
        print(f"  {sym} [{status:9}] {fid:<28} {f}")
        if status in ("notfound","ambiguous","raced","missing"):
            print(f"      → {msg}")
    print("\nsummary:", ", ".join(f"{k}={v}" for k,v in sorted(tally.items())))
    if not args.apply:
        print("\n(dry-run — nothing written. Re-run with --apply to land the patches, K2-attested.)")
    # nonzero exit if anything needs attention in apply mode
    problems = sum(tally.get(k,0) for k in ("notfound","ambiguous","raced","missing"))
    sys.exit(1 if (args.apply and problems) else 0)

if __name__ == "__main__":
    main()

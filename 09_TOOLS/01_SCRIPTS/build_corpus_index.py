#!/usr/bin/env python3
"""Build the corpus findability index.

WHY THIS EXISTS
---------------
On 2026-08-05 a session produced five claims in a row that the corpus had
already settled, and no gate caught any of them. What caught them was grep on
a guessed substring. The corpus's failure mode is not falsity -- it is
UNFINDABILITY: the knowledge is written down, and being written down does not
stop the next reader from re-deriving it.

901 of 1661 live documents already carry a `rosetta:` frontmatter block with a
`canonical_phrase` -- a one-line statement of what that document claims.
Nothing aggregates them. This script does exactly that and nothing more.

DISCIPLINE
----------
This index HARVESTS. It does not infer, score, or classify.

  * Every field is copied from what a file DECLARES in its own frontmatter.
  * `d_register` is populated ONLY when the filename declares it (`*_D5_*`).
    A filename is a declaration. A guess is not. Everything else is null and
    stays null until a human assigns it.
  * Nothing is moved, renamed, or edited. This is read-only over the corpus.

A file's absence of metadata is reported as absence, never filled in.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXCLUDE_PARTS = {
    ".git", "90_ARCHIVE", "node_modules", "__pycache__",
    "vendor", "91_COMPATIBILITY",
}

# Flat frontmatter keys worth indexing. `canonical_phrase` is accepted at the
# top level too: minimal files (tombstones, stubs) carry no `rosetta:` block,
# and a tombstone's forwarding pointer is exactly the kind of thing a reader
# most needs to find.
FLAT_KEYS = ("title", "status", "evidence_tier", "owner", "date",
             "supersedes_blob", "canonical_phrase")
# Keys inside the nested `rosetta:` block.
ROSETTA_KEYS = ("primary_level", "primary_column", "operator", "tier",
                "regime", "register", "canonical_phrase")

# A filename that names its own dimensional register, e.g. 00_D5_THE_MUTUALISM_LIMIT.md
FILENAME_D = re.compile(r"(?:^|[_-])D([0-6])(?:[_-]|$)")
TIER_TOKEN = re.compile(r"\[([ABSICD](?:/[ABSICD])*)\]")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def parse_frontmatter(text: str) -> dict | None:
    """Minimal, dependency-free frontmatter reader.

    Deliberately tolerant: the corpus's frontmatter is hand-written and not
    schema-validated, so a strict YAML parse would drop real files. Only
    top-level scalars and the one-level-deep `rosetta:` block are read; lists
    and deeper nesting are skipped rather than guessed at.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]

    out: dict = {}
    in_rosetta = False
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        if indent == 0:
            in_rosetta = line.startswith("rosetta:")
            if in_rosetta:
                continue
            if ":" not in line or line.startswith("-"):
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            if key in FLAT_KEYS and value.strip():
                out[key] = unquote(value)
            continue

        # Indented: only the first level of the rosetta block is read. Deeper
        # nesting (the `secondary:` list) is intentionally skipped -- a
        # secondary binding is not the file's primary claim.
        if in_rosetta and indent <= 2 and ":" in line and not line.startswith("-"):
            key, _, value = line.partition(":")
            key = key.strip()
            if key in ROSETTA_KEYS and value.strip():
                out[key] = unquote(value)

    return out


def declared_d_register(path: Path) -> int | None:
    """A dimensional register ONLY where the filename declares one."""
    match = FILENAME_D.search(path.stem)
    return int(match.group(1)) if match else None


def tiers_in(value: str | None) -> list[str]:
    if not value:
        return []
    seen: list[str] = []
    for token in TIER_TOKEN.findall(value):
        for part in token.split("/"):
            if part not in seen:
                seen.append(part)
    return seen


def walk() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        parts = path.relative_to(ROOT).parts
        if EXCLUDE_PARTS & set(parts):
            continue
        # Any dot-directory is tool state, not corpus (.pytest_cache et al).
        if any(p.startswith(".") for p in parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def build() -> list[dict]:
    rows = []
    for path in walk():
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:                      # unreadable is data, not a crash
            rows.append({"path": rel, "error": str(exc)})
            continue

        fm = parse_frontmatter(text) or {}
        rows.append({
            "path": rel,
            "lane": rel.split("/")[0],
            "has_frontmatter": bool(fm),
            "title": fm.get("title"),
            "canonical_phrase": fm.get("canonical_phrase"),
            "status": fm.get("status"),
            "evidence_tier": fm.get("evidence_tier"),
            "tiers": tiers_in(fm.get("evidence_tier")) or tiers_in(fm.get("register")),
            "owner": fm.get("owner"),
            "date": fm.get("date"),
            "l_level": fm.get("primary_level"),
            "column": fm.get("primary_column"),
            "operator": fm.get("operator"),
            # null unless the file's own name declares it. Never guessed.
            "d_register": declared_d_register(path),
            "d_register_source": "filename" if declared_d_register(path) else None,
        })
    return rows


def summarise(rows: list[dict]) -> str:
    total = len(rows)
    with_fm = sum(1 for r in rows if r.get("has_frontmatter"))
    with_phrase = sum(1 for r in rows if r.get("canonical_phrase"))
    with_level = sum(1 for r in rows if r.get("l_level"))
    with_d = sum(1 for r in rows if r.get("d_register") is not None)
    with_tier = sum(1 for r in rows if r.get("tiers"))

    def pct(n: int) -> str:
        return f"{n:5d}  ({100*n/total:5.1f}%)" if total else "0"

    lines = [
        f"live documents indexed          {total:5d}",
        f"  with frontmatter              {pct(with_fm)}",
        f"  with canonical_phrase         {pct(with_phrase)}   <- the findability field",
        f"  with an L-level               {pct(with_level)}",
        f"  with an evidence tier         {pct(with_tier)}",
        f"  with a DECLARED D-register    {pct(with_d)}   <- the gap this index exposes",
        "",
        f"UNFINDABLE (no phrase, no tier) {sum(1 for r in rows if not r.get('canonical_phrase') and not r.get('tiers')):5d}",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = build()
    out_dir = ROOT / "00_META" / "registers"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "CORPUS_INDEX.jsonl"

    with out_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(summarise(rows))
    print(f"\nwritten: {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

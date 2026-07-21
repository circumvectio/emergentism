#!/usr/bin/env python3
"""check_no_alias_paths.py — guard against re-introducing retired root-alias paths.

The compatibility root-alias symlinks (1_EMERGENTISM_ORG, 2_/02_SKYZAI_ORG,
3_/03_SKYZAI_COM, 4_/04_ENTITIES, 5_PORTFOLIO_ORGS, 6_SPECTRE, root 999_ARCHIVE)
were retired 2026-05-29 and every reference canonicalized. This guard fails if a
new alias *path reference* (`alias/...`) appears in active source, so the repo
stays de-duplicated.

Exit 0 = clean. Exit 1 = alias path-refs found (printed file:line).

Intentionally NOT checked (historical / generated / archival — alias strings
there are point-in-time records, not live navigation):
  - 90_ARCHIVE/            (K3 archive root)
  - .../999_ARCHIVE/ , .../90_ARCHIVE/        (nested per-org archives)
  - 00_START_HERE/root_alias_reconciliation_2026_05_27/ (recovered old blobs)
  - **/08_SOMA_LOG/** , **/02_AUDITS/**       (dated receipts + audit snapshots)
  - generated data: *.csv *.jsonl content_graph.json content_chunks*
  - binaries (decode-failures are skipped)
"""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

# alias path-ref: numeric-prefix roots + zero-padded SKYZAI/ENTITIES aliases, each
# followed by '/'. 999_ARCHIVE only at root position (nested .../999_ARCHIVE/ is real).
ALIAS = re.compile(
    r"(?<![A-Za-z0-9_])(?:1_EMERGENTISM_ORG|0?2_SKYZAI_ORG|0?3_SKYZAI_COM|0?4_ENTITIES|5_PORTFOLIO_ORGS|6_SPECTRE)/"
)
# NB: the retired root `999_ARCHIVE` alias is intentionally NOT guarded — `999_ARCHIVE/`
# is also a real *nested* archive dir under several orgs (OFN, etc.), so document
# references are ambiguous root-vs-relative and produce false positives. The root
# archive canonical name is `90_ARCHIVE/`.
EXCL_PREFIX = (
    "90_ARCHIVE/",
    "00_START_HERE/root_alias_reconciliation_2026_05_27/",
)
EXCL_SEG = ("/08_SOMA_LOG/", "/02_AUDITS/", "/ARCHIVE/", "/90_ARCHIVE/", "/99_ARCHIVE/", "/999_ARCHIVE/")
EXCL_NAME = re.compile(
    r"\.(csv|jsonl)$|content_graph\.json$|content_chunks|\.lock$"
    # this guard's own definition files legitimately name the retired aliases:
    r"|check_no_alias_paths\.py$|alias_paths_guard\.yml$"
)

def tracked() -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z"],
                         capture_output=True, text=True).stdout
    return [f for f in out.split("\0") if f]

def main() -> int:
    violations: list[str] = []
    for f in tracked():
        if f.startswith(EXCL_PREFIX) or EXCL_NAME.search(f) or any(s in f"/{f}" for s in EXCL_SEG):
            continue
        try:
            text = (REPO / f).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if ALIAS.search(line):
                violations.append(f"{f}:{i}: {line.strip()[:120]}")
    if violations:
        print(f"❌ retired root-alias path refs found ({len(violations)}):")
        for v in violations[:200]:
            print("  " + v)
        print("\nUse canonical roots (01_EMERGENTISM, 03_VENTURES, "
              "03_VENTURES/_PORTFOLIO, 02_SKYZAI/06_SPECTRE, 90_ARCHIVE).")
        return 1
    print("✅ no retired root-alias path references in active source")
    return 0

if __name__ == "__main__":
    sys.exit(main())

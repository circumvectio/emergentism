#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_rule_tokens.py — the plain-language naming-law lint (2026-07-22).

Rejects BARE letter-number rule tokens in new or changed prose. The letter K
alone carried several namespaces in the historical corpus; the active
00_META/00_PLAIN_LANGUAGE_NAMING_LAW.md makes plain-language names canonical
and demoted letters to a read-only alias index. A voluntary convention already
failed once (K2_PRISM_BOUNDARY_2026_05_16.md:160) — hence a check, not a hope.

WHAT IT FLAGS (in .md / .html prose):
  - bare K0–K10, L0–L9 used as rule references (word-boundary, no register tag)
  - bare A1–A7 used as rule references
  - the retired token K* (in rule position)
  - the retracted slogan "leave with everything"

WHAT IT ALLOWS:
  - bracketed register tags:  [DAC-K]6, [KERNEL-L]4, [Axiom-A]7  (N-3)
  - plain names:              "zero extraction", "no silent erasure", R1–R5, D0–D9, P0–P9
  - alias-index / historical context: lines citing the alias table, receipts,
    quotations marked as verbatim, and anything inside 90_ARCHIVE / 91_COMPATIBILITY
  - code identifiers (checked files are prose: .md, .html; code is exempt)
  - K-1 … K-7 kernel-surface slots (hyphenated form is a different, unambiguous token)

USAGE:
  python3 lint_rule_tokens.py FILE [FILE ...]        # lint specific files
  python3 lint_rule_tokens.py --changed              # lint files changed vs HEAD (git)
  Exit 0 = clean · 1 = violations found · 2 = usage error

Scope note: this lint judges NEW text. Running it over the whole legacy corpus
will (correctly) report thousands of historical hits — that is the migration
backlog, not a reason to weaken the check. Wire it to changed files only.
"""

import re
import subprocess
import sys

# Paths never linted: archives are provenance (R3), compat stubs are frozen.
INLINE_CODE = re.compile(r"`[^`\n]*`")
BARE_PATH = re.compile(r"[\w./-]*[\w-]+\.(?:md|html|py|json|ya?ml)\b")
EXEMPT_PATH = re.compile(r"(90_ARCHIVE|91_COMPATIBILITY|\.codex-worktrees|node_modules|book-pwa|\.vercel)/")

# Lines that are quoting, aliasing, or explicitly historical.
EXEMPT_LINE = re.compile(
    r"(verbatim|alias|legacy|was local|historical|retired|"
    r"formerly|old name|provenance|tombstone|superseded|naming law|"
    r"naming law|register tag|FG-\d|receipt \d|№\d|Rosetta|caste|Directorate)",
    re.IGNORECASE,
)

RULES = [
    # (name, pattern, advice)
    ("bare-K", re.compile(r"(?<!\[)(?<![-\w])K(?:10|[0-9])(?![-\w\]])"),
     "bare K-number — use the plain name or a register tag ([DAC-K]n); see the alias index"),
    ("bare-L", re.compile(r"(?<!\[)(?<![-\w])L[0-9](?![-\w\]])(?!\s+(?:Sensor|Operations|Intelligence|Treasury|Chief|Legal|Rishi|Sadhu|Ṛṣi|Caṇḍāla|Śūdra|Vaiśya|Kṣatriya|Brāhmaṇa)\b)"),
     "bare L-number — protocol invariants are P0–P9 plain-named; L-levels of the Rosetta are exempt only in Rosetta context (add context or tag)"),
    ("bare-A", re.compile(r"(?<!\[)(?<![-\w])A[1-7](?![-\w\]])"),
     "bare A-number — 'no infallibility' (R5) or [Axiom-A]n; say which"),
    ("K-star", re.compile(r"K\*"),
     "retired token K* — use K_sel (index bits) or K_U (Kolmogorov); they are not interchangeable"),
    ("retracted-slogan", re.compile(r"leave with everything", re.IGNORECASE),
     "RETRACTED slogan (2026-06-10) — the guarantee is a pro-rata claim on redeemable assets (FG-3)"),
]

PROSE_EXT = (".md", ".html")


def lint_file(path):
    findings = []
    if EXEMPT_PATH.search(path.replace("\\", "/")):
        return findings
    if not path.endswith(PROSE_EXT):
        return findings
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError as exc:
        findings.append((path, 0, "io", f"unreadable: {exc}"))
        return findings
    in_code_fence = False
    in_frontmatter = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # YAML frontmatter carries Rosetta L-levels (primary_level: L5) —
        # structural metadata, not rule references. Skip the whole block.
        if stripped == "---":
            if i == 1:
                in_frontmatter = True
                continue
            if in_frontmatter:
                in_frontmatter = False
                continue
        if in_frontmatter:
            continue
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if EXEMPT_LINE.search(line):
            continue
        # A filename is not a rule reference. Inline code spans naming caste
        # reports (`L2.4_CLAIM_VS_EVIDENCE_....md`) or paths carry L/K tokens
        # as part of an identifier; flagging those asks the author to rename
        # a file that exists. Blank the spans, keep the offsets stable.
        line = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)
        line = BARE_PATH.sub(lambda m: " " * len(m.group(0)), line)
        for name, pat, advice in RULES:
            for m in pat.finditer(line):
                # kernel-surface hyphen form K-1..K-7 never matches bare-K
                # (lookahead already excludes '-'), kept as a comment for clarity
                findings.append((path, i, name, f"'{m.group(0)}' — {advice}"))
    return findings


def changed_files():
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"lint_rule_tokens: cannot list changed files ({exc})", file=sys.stderr)
        sys.exit(2)
    return [p for p in out.splitlines() if p.endswith(PROSE_EXT)]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    paths = changed_files() if argv[1] == "--changed" else argv[1:]
    all_findings = []
    for p in paths:
        all_findings.extend(lint_file(p))
    if not all_findings:
        print(f"lint_rule_tokens: clean ({len(paths)} file(s))")
        return 0
    for path, ln, kind, msg in all_findings:
        print(f"{path}:{ln}: [{kind}] {msg}")
    print(f"\nlint_rule_tokens: {len(all_findings)} violation(s) in {len(paths)} file(s)")
    print("Plain names are canonical; ambiguous aliases live in provenance only.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

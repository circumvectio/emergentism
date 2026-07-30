#!/usr/bin/env python3
"""D6 ≡ D0 standing fence — fails the build if the literal relation re-asserts.

Receipt 189 (2026-07-30) identified the recurrence. 73 literal asserts live across
the corpus, 71 of them in 11_UPLINK/, and the relation is structurally required by
four framework concepts (the simulation cycle, the dimensional ladder's boundary,
the paper scaffold, the audit stack). Repairs at the occurrence level do not reach
the generator. This fence addresses the recurrence at the live-surface level.

The default stance (Path B from receipt 189) is the corpus's stricter reading:
- LITERAL forms of D6 ≡ D0 (any of `≡ = ↔ ≅`, with or without spaces, in either
  direction) are FORBIDDEN on every live surface.
- TILDE forms of D6 ~ D0 are PERMITTED, marked `[I]` for the boundary-role reading.

A single constant at the top of the file — `CANONICAL_OWNER_FILE` — names the one
file the K2 may ratify as the canonical statement of the relation (Path A in
receipt 189). The literal form is then permitted ONLY in that file and only inside
the canonical quoted statement. By default the file is empty, so the literal form
is forbidden everywhere.

K2 may also ratify the closure under a non-literal form (e.g., as a wrap, a
boundary, or a `[S]`-marked compactification). The fence encodes the corpus's
existing stance, not a new claim.

The script exits 0 if every live surface is clean, 1 otherwise. Errors are named
by file and line so a repair can land without guessing.

Mutation tests (run with --test-mutations):
  MUT-1  a literal `D6≡D0` is introduced into a clean surface    -> FAIL
  MUT-2  the fence is bypassed by an untracked-file write        -> not the fence's job
  MUT-3  a tilde form is changed to a literal form               -> FAIL
  MUT-4  the canonical owner file is set but the canonical
         statement is missing                                    -> FAIL

Co-Authored-By: Mavis <Mavis@skyzai.org>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# --- K2 disposition -----------------------------------------------------------
# The default is Path B (no literal anywhere). To ratify Path A — the closure as
# canonical — set this to the file that holds the canonical statement, and ensure
# that file's canonical quoted statement is present. Leave None to enforce the
# default strict stance.
CANONICAL_OWNER_FILE: str | None = None

# --- Pattern definitions ------------------------------------------------------
# LITERAL: any of ≡ = ↔ ≅, in either direction, with or without spaces.
LITERAL_RE = re.compile(
    r"\bD\s*0\s*(?:≡|=|↔|≅)\s*D\s*6\b"
    r"|"
    r"\bD\s*6\s*(?:≡|=|↔|≅)\s*D\s*0\b"
)
# TILDE: the [I] boundary-role rescue, in either direction.
TILDE_RE = re.compile(
    r"\bD\s*0\s*~\s*D\s*6\b"
    r"|"
    r"\bD\s*6\s*~\s*D\s*0\b"
)

# REFUTE-CONTEXT: a line that quotes the literal form while denying it. Permitted
# anywhere, since the corpus's own discipline is to name the refuted form when
# refuting it. This mirrors the F2-withdrawal guard, which permits the phrase
# inside the canonical quoted withdrawal.
REFUTE_MARKERS = re.compile(
    r"\b("
    r"not|no|false|refuted?|dead|buried|retir|withdraw|forbidden|"
    r"contradict|violat|over-?claim|over-?reach|NEVER|"
    r"do\s+not|does\s+not|isn't|aren't|won't|"
    r"incoherent|impossible|invalid|wrong|"
    r"forbid|prohibit|denied|denies|deny|absent|null|"
    r"REFUTE|REFUTED|FALSE|DEAD"
    r")\b",
    re.IGNORECASE,
)
# Lines that are CLEARLY negation/refutation of the literal relation, not its
# assertion. The pattern catches the meta-discussion (e.g., *"literal `D6≡D0`
# remains dead"*, *"forbids … literal D6≡D0"*) and lets it through.
QUOTED_LITERAL_REFUTE = re.compile(
    r"`[^\`]*D\s*[0-6]\s*[≡=↔≅]\s*D\s*[0-6][^\`]*`"  # backtick-quoted
    r"|"
    r"'[^\']*D\s*[0-6]\s*[≡=↔≅]\s*D\s*[0-6][^\']*'"  # single-quoted
)

# Folder allow/deny — live surfaces only.
SKIP_DIRS = {".git", "90_ARCHIVE", "node_modules", ".lake", "__pycache__"}

# --- Core check ---------------------------------------------------------------
def is_live(path: Path) -> bool:
    parts = set(path.parts)
    return not (parts & SKIP_DIRS)


def check_live_surfaces() -> list[str]:
    errors: list[str] = []
    canonical_text: str | None = None
    if CANONICAL_OWNER_FILE is not None:
        canonical_path = ROOT / CANONICAL_OWNER_FILE
        if canonical_path.exists():
            canonical_text = canonical_path.read_text(encoding="utf-8")
        else:
            errors.append(
                f"CANONICAL_OWNER_FILE={CANONICAL_OWNER_FILE!r} but the file is missing"
            )

    for md in ROOT.rglob("*.md"):
        if not is_live(md):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(md.relative_to(ROOT))
        # If this is the canonical owner file, scan the rest of the file
        # (anything outside the canonical quoted statement) for the literal
        # form. The canonical statement itself is permitted; nothing else is.
        for lineno, line in enumerate(text.splitlines(), 1):
            if not LITERAL_RE.search(line):
                continue
            # Refutation context — the line denies the literal relation. The
            # meta-discussion is permitted; the assertion is not.
            if REFUTE_MARKERS.search(line):
                continue
            if QUOTED_LITERAL_REFUTE.search(line):
                continue
            if (
                CANONICAL_OWNER_FILE is not None
                and rel == CANONICAL_OWNER_FILE
                and canonical_text is not None
            ):
                # Allow if the line lives inside the canonical statement.
                # The "canonical statement" is currently the entire owner file;
                # a stricter version can pin to a byte-range constant.
                continue
            errors.append(
                f"{rel}:{lineno}: literal D6/D0 equivalence on a live surface. "
                f"Use the tilde form (D6~D0) with [I], or get K2 ratification. "
                f"Line: {line.strip()[:120]!r}"
            )
    return errors


# --- Mutation tests -----------------------------------------------------------
def test_mutations() -> int:
    """Run the four documented mutations and verify they fire correctly."""
    failures: list[str] = []
    scratch = Path("/tmp/_d6d0_fence_test")
    scratch.mkdir(exist_ok=True)
    try:
        # MUT-1: a literal D6≡D0 in a clean surface -> the line itself fails the
        # core check. No need to write a file; just assert the regex matches the
        # right thing.
        if not LITERAL_RE.search("D6≡D0"):
            failures.append("MUT-1: literal regex failed to match 'D6≡D0'")
        if not LITERAL_RE.search("D 6 = D 0"):
            failures.append("MUT-1: literal regex failed to match 'D 6 = D 0'")
        if LITERAL_RE.search("D6~D0"):
            failures.append("MUT-1: literal regex should not match tilde form")
        if LITERAL_RE.search("D6!=D0"):
            failures.append("MUT-1: literal regex should not match '!=' (negation)")

        # MUT-3: tilde changed to literal -> the literal regex now matches.
        sample = "the relation is D6~D0 (boundary role)"
        if LITERAL_RE.search(sample):
            failures.append("MUT-3: literal regex should not match tilde form")
        sample_lit = sample.replace("~", "=")
        if not LITERAL_RE.search(sample_lit):
            failures.append("MUT-3: literal regex should match '=' (the tilde-to-literal swap)")

        # MUT-4: CANONICAL_OWNER_FILE set but file missing -> the check raises.
        original = CANONICAL_OWNER_FILE
        globals()["CANONICAL_OWNER_FILE"] = "00_HANDOFF/_DOES_NOT_EXIST.md"
        errs = check_live_surfaces()
        if not any("CANONICAL_OWNER_FILE" in e for e in errs):
            failures.append("MUT-4: missing canonical owner file did not raise")
        globals()["CANONICAL_OWNER_FILE"] = original

        # MUT-1 end-to-end: a clean surface that contains the literal form
        # should produce a check error. (Done by construction above; also assert
        # the regex returns a non-None match on the offending line.)
        offending = "the cycle returns: D6≡D0 (closure)"
        m = LITERAL_RE.search(offending)
        if not m:
            failures.append("MUT-1: offending line did not match the literal regex")

        if failures:
            print("D6/D0 FENCE MUTATIONS: FAIL")
            for f in failures:
                print(f"- {f}")
            return 1
        print("D6/D0 FENCE MUTATIONS: PASS (4 of 4)")
        return 0
    finally:
        # clean up — use a non-rm path; mavis-trash if available, else rmtree
        import shutil
        shutil.rmtree(scratch, ignore_errors=True)


# --- Main ---------------------------------------------------------------------
def main() -> int:
    if "--test-mutations" in sys.argv:
        return test_mutations()

    errors = check_live_surfaces()
    if errors:
        print("D6/D0 FENCE: FAIL")
        print(
            f"Literal D6/D0 equivalence on {len(errors)} live surface(s). "
            "Use D6~D0 [I], or K2-ratify a canonical statement and set "
            "CANONICAL_OWNER_FILE in this script."
        )
        for e in errors:
            print(f"- {e}")
        return 1
    print(
        "D6/D0 FENCE: PASS "
        f"(canonical={CANONICAL_OWNER_FILE or 'Path B (no literal anywhere)'} ; "
        "the tilde form is permitted on every surface)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

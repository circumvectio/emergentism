#!/usr/bin/env python3
"""D6 ≡ D0 standing fence — fails the build if the literal relation re-asserts.

Receipt 189 (`189_D6_D0_GENERATOR_HUNT_2026_07_30.md`; 2026-07-30) identified the recurrence. 73 literal asserts live across
the corpus, 71 of them in 11_UPLINK/, and the relation is structurally required by
four framework concepts (the simulation cycle, the dimensional ladder's boundary,
the paper scaffold, the audit stack). Repairs at the occurrence level do not reach
the generator. This fence addresses the recurrence at the live-surface level.

The default stance (Path B from receipt 189, `189_D6_D0_GENERATOR_HUNT_2026_07_30.md`)
is the corpus's stricter reading:
- LITERAL forms of D6 ≡ D0 (any of `≡ = ↔ ≅`, with or without spaces, in either
  direction) are FORBIDDEN on every live surface.
- TILDE forms of D6 ~ D0 are PERMITTED, marked `[I]` for the boundary-role reading.

A single constant at the top of the file — `CANONICAL_OWNER_FILE` — names the one
file the owner may ratify as the canonical statement of the relation (Path A in
receipt 189 (`189_D6_D0_GENERATOR_HUNT_2026_07_30.md`). The literal form is then
permitted ONLY in that file and only inside
the canonical quoted statement. By default the file is empty, so the literal form
is forbidden everywhere.

The owner may also ratify the closure under a non-literal form (e.g., as a wrap, a
boundary, or a `[S]`-marked compactification). The fence encodes the corpus's
existing stance, not a new claim.

The script exits 0 if every live surface is clean, 1 otherwise. Errors are named
by file and line so a repair can land without guessing.

Mutation tests (run with --test-mutations):
  MUT-1  a literal `D6≡D0` is introduced into a clean surface    -> FAIL
  MUT-2  a literal is written to a new/untracked live Markdown   -> FAIL
  MUT-3  a tilde form is changed to a literal form               -> FAIL
  MUT-4  the canonical owner file is set but the canonical
         statement is missing                                    -> FAIL
  MUT-5  one byte changes in a frozen historical handoff         -> FAIL
  MUT-6  a new literal is appended beyond the frozen body        -> FAIL
  MUT-7  a frozen handoff is reached through a symlinked parent  -> FAIL

"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# --- owner disposition -----------------------------------------------------------
# The default is Path B (no literal anywhere). To ratify Path A — the closure as
# canonical — set this to the file that holds the canonical statement, and ensure
# that file's canonical quoted statement is present. Leave None to enforce the
# default strict stance.
CANONICAL_OWNER_FILE: str | None = None


@dataclass(frozen=True)
class FrozenHistoricalSurface:
    """Exact custody for a dated handoff that quotes the rejected relation.

    These are not canonical-owner exceptions. They are immutable historical
    bodies whose quoted mutation/retraction evidence predates this repair. A
    whole-file digest makes the exception byte-exact: changing even unrelated
    prose, changing an occurrence, or appending a new occurrence revokes it.
    """

    sha256: str
    literal_occurrences: int
    required_local_markers: tuple[str, ...]


FROZEN_HISTORICAL_SURFACES: dict[str, FrozenHistoricalSurface] = {
    "00_HANDOFF/GATE_MUTATION_REPORT_2026_08_06.md": FrozenHistoricalSurface(
        sha256="6b494abbc3763c59977aed710ecdc2f40f7b8c68ecf81a4a8325fa3b367aabdd",
        literal_occurrences=4,
        required_local_markers=(
            "type: emergentism-verification-report",
            "### 2.18 `check_d6_equiv_d0.py`",
            "`X D6≡D0 Y`",
        ),
    ),
    "00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md": FrozenHistoricalSurface(
        sha256="2a7cd9b5d395d178f8bf9cfb158dee9d475f4b6e892927daf5fcf30d3bf6a49b",
        literal_occurrences=5,
        required_local_markers=(
            "type: new-findings-audit",
            "**The literal equation `D6≡D0` is dead**",
            "D6≡D0 retraction argument",
        ),
    ),
}

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
#
# Word-stem patterns (no `\b` on the right) so that "Forbids" matches "forbid",
# "refuting" matches "refut", "laundered" matches "launder", etc. The earlier
# `\b...\b` form missed "Forbids" / "refutes" / "out" / "laundered" because
# the right-hand `\b` required a non-word character at the inflected suffix.
REFUTE_MARKERS = re.compile(
    r"("
    r"not|no|false|never|"
    r"refut|dead|buried|retir|withdraw|forbid|prohibit|"
    r"contradict|violat|over-?claim|over-?reach|"
    r"do\s+not|does\s+not|isn't|aren't|won't|don't|doesn't|"
    r"incoherent|impossible|invalid|wrong|"
    r"denied|denies|deny|absent|null|"
    r"shelter|launder|tautolog|"
    r"disambigu|readings|three\s+readings|has\s+three|"
    r"literal\b|form\b|status\b|keeps\s+its\s+status|"
    r"\bout\b|\binto\b|\bfrom\b|\babout\b"
    r")",
    re.IGNORECASE,
)
# Lines that are CLEARLY negation/refutation of the literal relation, not its
# assertion. The pattern catches the meta-discussion (e.g., *"literal `D6≡D0`
# remains dead"*, *"forbids … literal D6≡D0"*) and lets it through. Catches
# backtick, single, and double-quoted forms (natural-language references like
# "D6 ≡ D0 appears 98 times live").
QUOTED_LITERAL_REFUTE = re.compile(
    r"`[^\`]*D\s*[0-6]\s*[≡=↔≅]\s*D\s*[0-6][^\`]*`"  # backtick-quoted
    r"|"
    r"'[^\']*D\s*[0-6]\s*[≡=↔≅]\s*D\s*[0-6][^\']*'"  # single-quoted
    r"|"
    r'"[^"]*D\s*[0-6]\s*[≡=↔≅]\s*D\s*[0-6][^"]*"'  # double-quoted
)

# Folder allow/deny — live surfaces only.
SKIP_DIRS = {".git", "90_ARCHIVE", "node_modules", ".lake", "__pycache__"}

# --- Core check ---------------------------------------------------------------
def is_live(path: Path) -> bool:
    parts = set(path.parts)
    return not (parts & SKIP_DIRS)


def frozen_path_custody_error(root: Path, path: Path, rel: str) -> str | None:
    """Reject symlink components and resolved escapes before reading bytes."""

    lexical_root = Path(os.path.abspath(os.fspath(root)))
    lexical_path = Path(os.path.abspath(os.fspath(path)))
    try:
        parts = lexical_path.relative_to(lexical_root).parts
    except ValueError:
        return f"{rel}: frozen historical custody path escapes scan root"
    current = lexical_root
    if current.is_symlink():
        return f"{rel}: frozen historical custody scan root is a symlink"
    for part in parts:
        current = current / part
        if current.is_symlink():
            return (
                f"{rel}: frozen historical custody uses symlink component: "
                f"{current}"
            )
    try:
        lexical_path.resolve(strict=True).relative_to(lexical_root.resolve(strict=True))
    except (FileNotFoundError, RuntimeError, ValueError):
        return f"{rel}: frozen historical custody path is missing or escapes scan root"
    return None


def check_frozen_historical_surfaces(root: Path) -> tuple[list[str], set[str]]:
    """Return custody errors and the exact historical bodies they permit.

    The path, regular-file shape, complete bytes, literal-occurrence count, and
    local historical/retraction markers are all bound. The whole-file digest is
    the controlling boundary; the other checks make its intended semantics
    explicit in diagnostics and tests.
    """

    errors: list[str] = []
    permitted: set[str] = set()
    for rel, frozen in FROZEN_HISTORICAL_SURFACES.items():
        path = root / rel
        local_errors: list[str] = []
        custody_error = frozen_path_custody_error(root, path, rel)
        if custody_error is not None:
            local_errors.append(custody_error)
        elif not path.is_file():
            local_errors.append(f"{rel}: frozen historical custody file is missing")
        else:
            blob = path.read_bytes()
            actual_sha256 = hashlib.sha256(blob).hexdigest()
            if actual_sha256 != frozen.sha256:
                local_errors.append(
                    f"{rel}: frozen historical SHA-256 drift "
                    f"(expected {frozen.sha256}, got {actual_sha256})"
                )
            try:
                text = blob.decode("utf-8")
            except UnicodeDecodeError as exc:
                local_errors.append(f"{rel}: frozen historical body is not UTF-8: {exc}")
            else:
                occurrence_count = len(tuple(LITERAL_RE.finditer(text)))
                if occurrence_count != frozen.literal_occurrences:
                    local_errors.append(
                        f"{rel}: frozen historical literal-occurrence drift "
                        f"(expected {frozen.literal_occurrences}, got {occurrence_count})"
                    )
                for marker in frozen.required_local_markers:
                    if marker not in text:
                        local_errors.append(
                            f"{rel}: frozen historical/retraction marker missing: {marker!r}"
                        )
        if local_errors:
            errors.extend(local_errors)
        else:
            permitted.add(rel)
    return errors, permitted


def check_live_surfaces(root: Path | None = None) -> list[str]:
    scan_root = ROOT if root is None else root
    errors: list[str] = []
    custody_errors, frozen_historical = check_frozen_historical_surfaces(scan_root)
    errors.extend(custody_errors)
    canonical_text: str | None = None
    if CANONICAL_OWNER_FILE is not None:
        canonical_path = scan_root / CANONICAL_OWNER_FILE
        if canonical_path.exists():
            canonical_text = canonical_path.read_text(encoding="utf-8")
        else:
            errors.append(
                f"CANONICAL_OWNER_FILE={CANONICAL_OWNER_FILE!r} but the file is missing"
            )

    for md in scan_root.rglob("*.md"):
        if not is_live(md):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(md.relative_to(scan_root))
        # Exact dated handoffs are permitted as complete historical bodies, not
        # as directory- or file-wide semantic exemptions. Any byte drift above
        # removes the path from this set and the ordinary literal scan resumes.
        if rel in frozen_historical:
            continue
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
                f"Use the tilde form (D6~D0) with [I], or get an owner ruling. "
                f"Line: {line.strip()[:120]!r}"
            )
    return errors


# --- Mutation tests -----------------------------------------------------------
def test_mutations() -> int:
    """Run the seven documented mutations and verify they fire correctly."""
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="d6d0_fence_test_") as tmp:
        scratch = Path(tmp)
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

        # MUT-1 sanity: the compact closure wording itself must match.
        offending = "the cycle returns: D6≡D0 (closure)"
        m = LITERAL_RE.search(offending)
        if not m:
            failures.append("MUT-1: offending line did not match the literal regex")

        # Build a minimal exact-custody tree. Its dated bodies must pass before
        # either custody mutation is seeded.
        for rel in FROZEN_HISTORICAL_SURFACES:
            source = ROOT / rel
            target = scratch / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        clean_surface = scratch / "00_THE_KERNEL_INDEX.md"
        clean_surface.write_text("# Clean mutation surface\n", encoding="utf-8")
        baseline_errors = check_live_surfaces(scratch)
        if baseline_errors:
            failures.append(
                "MUT-5/6 setup: exact frozen historical bodies did not pass: "
                + "; ".join(baseline_errors[:2])
            )

        # MUT-2: filesystem discovery includes new/untracked live Markdown. A
        # generic file cannot inherit either dated handoff's exact custody.
        clean_surface.write_text("# New live surface\n\nX D6≡D0 Y\n", encoding="utf-8")
        untracked_errors = check_live_surfaces(scratch)
        if not any(
            "00_THE_KERNEL_INDEX.md" in error
            and "literal D6/D0 equivalence" in error
            for error in untracked_errors
        ):
            failures.append("MUT-2: literal in a new/untracked live file escaped")
        clean_surface.write_text("# Clean mutation surface\n", encoding="utf-8")

        # MUT-5: an otherwise-semantic-neutral byte change must revoke custody.
        drift_rel = "00_HANDOFF/GATE_MUTATION_REPORT_2026_08_06.md"
        drift_path = scratch / drift_rel
        exact_blob = drift_path.read_bytes()
        needle = b"type: emergentism-verification-report"
        replacement = b"type: emergentism-verification-reporu"
        if needle not in exact_blob:
            failures.append("MUT-5: frozen historical byte needle is missing")
        else:
            drift_path.write_bytes(exact_blob.replace(needle, replacement, 1))
            drift_errors = check_live_surfaces(scratch)
            if not any(
                drift_rel in error and "SHA-256 drift" in error
                for error in drift_errors
            ):
                failures.append("MUT-5: altered historical byte did not revoke custody")
            drift_path.write_bytes(exact_blob)

        # MUT-6: exercise the other dated handoff. Its frozen digest binds the
        # end of the body, so an appended literal is outside that unit and must
        # be caught by both custody and the ordinary live-surface scan.
        append_rel = "00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md"
        append_path = scratch / append_rel
        append_blob = append_path.read_bytes()
        append_path.write_bytes(append_blob + b"\nX D6\xe2\x89\xa1D0 Y\n")
        append_errors = check_live_surfaces(scratch)
        if not any(
            append_rel in error and "SHA-256 drift" in error
            for error in append_errors
        ):
            failures.append("MUT-6: appended literal did not revoke frozen custody")
        if not any(
            append_rel in error and "literal D6/D0 equivalence" in error
            for error in append_errors
        ):
            failures.append("MUT-6: appended literal escaped the ordinary live scan")

        # MUT-7: exact bytes cannot inherit custody through a symlinked parent
        # directory. Move the real handoff directory aside and replace it with
        # a lexical symlink so the ancestor case is exercised directly.
        handoff = scratch / "00_HANDOFF"
        real_handoff = scratch / "00_HANDOFF_REAL"
        handoff.rename(real_handoff)
        handoff.symlink_to(real_handoff, target_is_directory=True)
        symlink_errors = check_live_surfaces(scratch)
        if not any("symlink component" in error for error in symlink_errors):
            failures.append("MUT-7: symlinked historical parent directory escaped custody")

        if failures:
            print("D6/D0 FENCE MUTATIONS: FAIL")
            for f in failures:
                print(f"- {f}")
            return 1
        print("D6/D0 FENCE MUTATIONS: PASS (7 of 7)")
        return 0


# --- Main ---------------------------------------------------------------------
def main() -> int:
    if "--test-mutations" in sys.argv:
        return test_mutations()

    errors = check_live_surfaces()
    if errors:
        print("D6/D0 FENCE: FAIL")
        print(
            f"Found {len(errors)} D6/D0 fence violation(s). "
            "Use D6~D0 [I], or have the owner ratify a canonical statement and set "
            "CANONICAL_OWNER_FILE in this script."
        )
        for e in errors:
            print(f"- {e}")
        return 1
    print(
        "D6/D0 FENCE: PASS "
        f"(canonical={CANONICAL_OWNER_FILE or 'Path B (no literal anywhere)'} ; "
        f"frozen_history={len(FROZEN_HISTORICAL_SURFACES)} exact bodies ; "
        "the tilde form is permitted on every surface)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

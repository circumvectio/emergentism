#!/usr/bin/env python3
"""mutation_test_gates.py — mutation-test the corpus's own gates.

WHY THIS EXISTS
---------------
A referee panel instructed "your default is REFUTED" returned 18 kills in 18
hearings; a fair re-hearing overturned 15. The rule that came out of that is:

    A JUDGMENT INSTRUMENT THAT CANNOT RETURN THE OPPOSITE VERDICT IS BROKEN.

It had been applied to exactly one instrument — the panel. The corpus's own
checkers are judgment instruments too, and nobody had ever asked them the same
question. This script asks it, mechanically, of every ``check_*.py``.

THE CLASSES
-----------
SOUND           both verdicts demonstrated, and every seeded fault was caught.
SOUND-BUT-BLIND both verdicts demonstrated, but at least one seeded fault
                survived. The gate works and has a named hole.
CANNOT-FAIL     green on the corpus and green under EVERY seeded fault,
                including faults in exactly the property it names. Decorative.
CANNOT-PASS     red on the corpus and red on a minimal tree that contains
                nothing it could object to. The mirror of the rigged panel:
                a verdict machine with one verdict.
DOES-NOT-RUN    crashes or hangs; never reaches a verdict at all. Strictly
                worse than either, because it reports nothing.
UNDETERMINED    no probe reached a conclusion. Stated, never guessed.

METHOD, AND ITS ONE HARD RULE
-----------------------------
NOTHING IS EVER MUTATED IN THE REAL CORPUS. Every probe runs against a
copy-on-write clone (``cp -Rc``, APFS clonefile: seconds, near-zero disk) or a
throwaway minimal tree under the system temp dir. Each probe backs up the exact
bytes it touches and restores them, so probes are independent inside one clone.
If the clone cannot be made the script refuses to run rather than falling back
to the live tree.

THE THREE PROBE KINDS
---------------------
RED PROBE      applied to a gate that is currently GREEN. Seed the fault the
               gate exists to catch; require a non-zero exit. Several faults per
               gate, because one caught fault does not mean the gate sees the
               others — see check_generative_base, where 3 of 4 survive.
GREEN PROBE    applied to a gate that is currently RED. Repair, in the clone,
               the condition its own error message names; require exit 0.
MINIMAL-TREE   applied to a gate that is currently RED and whose repair set is
               too large to edit. Run it on a tree containing only itself and
               its imports. A scanner that is still RED with nothing to scan
               objects to its own source: green is unreachable.

A probe never edits a checker's source, with one declared exception: the two G2
regressions check a mathematical model that LIVES in the script, so for those
the model in the CLONED script is the data, and the mutation says so.

USAGE
-----
    python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py
    python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --census
    python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --only check_links
    python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --clone /tmp/em --keep-clone
    python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --json survey.json

Exit code is 0 when the survey completes. THIS SCRIPT SURVEYS; IT DOES NOT GATE.
Wiring it into gate.sh so a CANNOT-FAIL checker blocks a commit is an owner call,
because it would block the build on a meta-property nobody has ratified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
CHECK_GLOBS = ("09_TOOLS/01_SCRIPTS/check_*.py", "12_PUBLIC_SITE/check_*.py")
# P2.1 V-forcing directive: 60 s is a hard cap per gate. Anything that
# needs more is classified hang-class and the audit moves on. The
# tighter cap is also the worst-case upper bound for the full run.
DEFAULT_TIMEOUT = 60
SLOW_TIMEOUT = 60

SOUND = "SOUND"
SOUND_BLIND = "SOUND-BUT-BLIND"
CANNOT_FAIL = "CANNOT-FAIL"
CANNOT_PASS = "CANNOT-PASS"
DOES_NOT_RUN = "DOES-NOT-RUN"
UNDETERMINED = "UNDETERMINED"

S = "09_TOOLS/01_SCRIPTS"


# ---------------------------------------------------------------------------
# running
# ---------------------------------------------------------------------------


def run_script(tree: Path, rel_script: str, args: list[str] | None = None,
               timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Run a checker inside `tree`. Returns {status, rc, wall_s, out, findings}."""
    cmd = [sys.executable, "-B", str(tree / rel_script)] + list(args or [])
    started = time.time()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run(cmd, cwd=str(tree), capture_output=True, text=True,
                              timeout=timeout, env=env)
        rc, out = proc.returncode, (proc.stdout or "") + (proc.stderr or "")
        if rc == 0:
            status = "PASS"
        elif "Traceback (most recent call last)" in out:
            status = "ERROR"
        else:
            status = "FAIL"
    except subprocess.TimeoutExpired as exc:
        rc, status = None, "HANG"
        out = exc.stdout.decode("utf-8", "replace") if exc.stdout else ""
    return {"status": status, "rc": rc, "wall_s": round(time.time() - started, 2),
            "out": out.strip(), "findings": extract_findings_count(out)}


# P2.1 V-forcing: every gate must report how many things it objects to, so the
# mutation test can prove both the verdict (exit code) AND the magnitude of the
# verdict moved. Different gates use different vocabularies, so we match all
# of them and take the maximum. None means "the gate did not report a number";
# that is itself a finding (a gate that cannot report magnitude is, in this
# audit, a gate that cannot be measured).
_NUMERIC_PATTERNS = [
    re.compile(r"residual carriers?\s*\((\d+)\)", re.I),
    re.compile(r"\bcarriers?:\s*(\d+)\b", re.I),
    re.compile(r"\b(\d+)\s+findings?\b", re.I),
    re.compile(r"\b(\d+)\s+violations?\b", re.I),
    re.compile(r"\b(\d+)\s+issues?\b", re.I),
    re.compile(r"\b(\d+)\s+errors?\b", re.I),
    re.compile(r"\b(\d+)\s+problem", re.I),
]


def extract_findings_count(out: str) -> int | None:
    """Best-effort parse of a gate's "how many things did you object to" line.

    The richest match wins: if a gate prints BOTH "2 carriers" and
    "12 issues", we trust the bigger number (a gate that finds 12 issues
    but only lists 2 is the broken case we are looking for). For gates
    that list findings as bullet points, count the bullets. For gates
    that say nothing, return None — that is itself a finding.
    """
    if not out:
        return None
    best: int | None = None
    for pat in _NUMERIC_PATTERNS:
        for m in pat.finditer(out):
            try:
                n = int(m.group(1))
            except (IndexError, ValueError):
                continue
            if best is None or n > best:
                best = n
    # Bullet-list fallback: most "X things are wrong" dumps are `- ` lines.
    bullets = len(re.findall(r"^\s*-\s", out, flags=re.M))
    if bullets and (best is None or bullets > best):
        best = bullets
    return best


def head(text: str, n: int) -> str:
    return "\n".join(text.splitlines()[:n])


# ---------------------------------------------------------------------------
# sandbox
# ---------------------------------------------------------------------------


class Sandbox:
    """A cloned corpus tree with byte-exact undo for everything a probe touches."""

    def __init__(self, tree: Path) -> None:
        self.tree = tree
        self._backup: dict[Path, bytes | None] = {}

    def _stash(self, rel: str) -> Path:
        path = self.tree / rel
        if path not in self._backup:
            self._backup[path] = path.read_bytes() if path.is_file() else None
        return path

    def exists(self, rel: str) -> bool:
        return (self.tree / rel).is_file()

    def read(self, rel: str) -> str:
        return (self.tree / rel).read_text(encoding="utf-8", errors="replace")

    def write(self, rel: str, text: str) -> None:
        path = self._stash(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def append(self, rel: str, text: str) -> None:
        path = self._stash(rel)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(text)

    def sub(self, rel: str, old: str, new: str, count: int = 1) -> int:
        """Literal replace. Returns replacements made; 0 means the probe missed."""
        if not self.exists(rel):
            return 0
        body = self.read(rel)
        if old not in body:
            return 0
        made = body.count(old) if count == 0 else min(count, body.count(old))
        self._stash(rel).write_text(
            body.replace(old, new, -1 if count == 0 else count), encoding="utf-8")
        return made

    def resub(self, rel: str, pattern, repl, flags: int = 0) -> int:
        if not self.exists(rel):
            return 0
        body = self.read(rel)
        new, n = re.subn(pattern, repl, body, flags=flags)
        if n:
            self._stash(rel).write_text(new, encoding="utf-8")
        return n

    def restore(self) -> None:
        for path, blob in self._backup.items():
            if blob is None:
                if path.exists():
                    path.unlink()
            else:
                path.write_bytes(blob)
        self._backup.clear()

    def run(self, rel_script: str, args: list[str] | None = None,
            timeout: int = DEFAULT_TIMEOUT) -> dict:
        return run_script(self.tree, rel_script, args, timeout)


@dataclass
class ProbeResult:
    ok: bool
    detail: str
    observed: str = ""


def expect_red(sb: Sandbox, script: str, note: str, timeout: int = DEFAULT_TIMEOUT) -> ProbeResult:
    res = sb.run(script, None, timeout)
    return ProbeResult(res["status"] in {"FAIL", "ERROR"},
                       f"{note} -> {res['status']} rc={res['rc']}",
                       head(res["out"], 3))


def expect_green(sb: Sandbox, script: str, note: str, timeout: int = DEFAULT_TIMEOUT) -> ProbeResult:
    res = sb.run(script, None, timeout)
    return ProbeResult(res["status"] == "PASS",
                       f"{note} -> {res['status']} rc={res['rc']}",
                       head(res["out"], 3))


SELF_REFUTING = "SELF-REFUTING"
NEEDS_INPUTS = "NEEDS-INPUTS"


def minimal_tree_probe(sb: Sandbox, script: str, extras: tuple[str, ...] = (),
                       timeout: int = DEFAULT_TIMEOUT) -> ProbeResult:
    """Run a gate on a tree containing only itself (plus declared imports).

    THREE OUTCOMES, AND ONLY ONE OF THEM PROVES ANYTHING ABOUT REACHABILITY:

      PASS                   green is reachable. The corpus-red verdict is a real
                             finding about the corpus, not a property of the gate.
      FAIL naming ITSELF     the gate objects to its own source. No corpus repair
                             can make it green: this is CANNOT-PASS, proven.
      FAIL/ERROR otherwise   the gate needs inputs the minimal tree does not have.
                             INCONCLUSIVE. It is NOT evidence of unreachability,
                             and reporting it as such would be the same error this
                             whole survey exists to catch.
    """
    with tempfile.TemporaryDirectory(prefix="mutgate_min_") as tmp:
        root = Path(tmp) / "01_EMERGENTISM"
        for rel in (script,) + extras:
            src = sb.tree / rel
            if not src.is_file():
                continue
            dest = root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        res = run_script(root, script, None, timeout)

    if res["status"] == "PASS":
        verdict = ""
    elif res["status"] == "FAIL" and script in res["out"]:
        # The gate's own path appears in its own complaint. A traceback also
        # names the file, which is why ERROR never reaches this branch.
        verdict = SELF_REFUTING
    else:
        verdict = NEEDS_INPUTS
    return ProbeResult(res["status"] == "PASS",
                       f"minimal tree (only the checker + its imports) -> "
                       f"{res['status']} rc={res['rc']}"
                       + (f" [{verdict}]" if verdict else ""),
                       head(res["out"], 8))


# ---------------------------------------------------------------------------
# RED probes — seeded faults for gates that are currently GREEN
# ---------------------------------------------------------------------------


def m_adjudication_blank(sb):
    sb.append("09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl", "\n")
    return expect_red(sb, f"{S}/check_adjudication_custody.py",
                      "one newline appended to a frozen-digest ledger")


def m_adjudication_verdict(sb):
    rel = "09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl"
    if not sb.resub(rel, r'"verdict":\s*"FALSE"', '"verdict": "REAL_OPEN"'):
        return ProbeResult(False, "no FALSE verdict found to flip (ledger shape changed)")
    return expect_red(sb, f"{S}/check_adjudication_custody.py",
                      "a FALSE verdict silently flipped to REAL_OPEN inside the ledger")


def m_coherence_overall(sb):
    n = sb.sub(f"{S}/coherence_profile.json",
               '"state": "PASS_WITH_DEBT"\n  }\n}', '"state": "PASS"\n  }\n}')
    if not n:
        n = sb.resub(f"{S}/coherence_profile.json",
                     r'("overall":\s*\{[^}]*?"state":\s*")PASS_WITH_DEBT(")', r"\1PASS\2")
    if not n:
        return ProbeResult(False, "probe could not seed the overall-state fault")
    return expect_red(sb, f"{S}/check_coherence_profile.py",
                      "overall state claimed better than its worst axis")


def m_coherence_world_contact(sb):
    """The profile's whole point: local gates are NOT world contact."""
    n = sb.sub(f"{S}/coherence_profile.json", '"state": "OPEN"', '"state": "ESTABLISHED"')
    if not n:
        return ProbeResult(False, "probe could not find the world_contact state")
    return expect_red(sb, f"{S}/check_coherence_profile.py",
                      "world contact declared ESTABLISHED with an empty evidence list")


def m_d6_literal(sb):
    sb.append("00_THE_KERNEL_INDEX.md", "\n<!-- seeded --> D6 ≡ D0\n")
    return expect_red(sb, f"{S}/check_d6_equiv_d0.py",
                      "literal `D6 ≡ D0` written onto a live surface")


def m_d6_spaced(sb):
    sb.append("00_THE_WELTANSCHAUUNG.md", "\nThe closure means D 6 = D 0 exactly.\n")
    return expect_red(sb, f"{S}/check_d6_equiv_d0.py",
                      "spaced literal `D 6 = D 0` on a second live surface")


def m_d6_frozen_historical_byte_drift(sb):
    """Changing one byte must revoke the whole-body historical exception."""

    rel = "00_HANDOFF/GATE_MUTATION_REPORT_2026_08_06.md"
    if not sb.sub(rel, "type: emergentism-verification-report",
                  "type: emergentism-verification-reporu"):
        return ProbeResult(False, "frozen historical byte needle was not present")
    return expect_red(sb, f"{S}/check_d6_equiv_d0.py",
                      "one byte changed inside the exact frozen handoff body")


def m_d6_literal_beyond_frozen_body(sb):
    """A file path is not an allowlist: appended bytes resume ordinary scan."""

    rel = "00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md"
    sb.append(rel, "\nX D6≡D0 Y\n")
    return expect_red(sb, f"{S}/check_d6_equiv_d0.py",
                      "new literal appended beyond the exact frozen handoff body")


def m_d6_frozen_historical_parent_symlink(sb):
    """Exact bytes reached through a symlinked parent must lose custody."""

    handoff = sb.tree / "00_HANDOFF"
    real_handoff = sb.tree / "00_HANDOFF_REAL"
    if not handoff.is_dir() or real_handoff.exists():
        return ProbeResult(False, "handoff directory setup is unavailable")
    handoff.rename(real_handoff)
    handoff.symlink_to(real_handoff, target_is_directory=True)
    try:
        return expect_red(
            sb,
            f"{S}/check_d6_equiv_d0.py",
            "frozen handoff reached through a symlinked parent directory",
        )
    finally:
        handoff.unlink()
        real_handoff.rename(handoff)


def m_d6_archive_tagged_refutation_byte_drift(sb):
    """A dead-form handoff is exempt only while its exact refutation survives."""

    rel = "00_HANDOFF/EMERGENTISM_GREAT_MYSTERY_2026_08_20.md"
    if not sb.sub(
        rel,
        "**#8 Literal `D6≡D0`** (dead)",
        "**#8 Literal `D6≡D0`** (live)",
    ):
        return ProbeResult(False, "archive-tagged refutation marker was not present")
    return expect_red(
        sb,
        f"{S}/check_d6_equiv_d0.py",
        "archive-tagged D6/D0 refutation marker changed from dead to live",
    )


def m_established_inflation(sb):
    sb.append("00_ESTABLISHED/README.md",
              "\nThe Lean candidate compiles cleanly on every commit.\n")
    return expect_red(sb, f"{S}/check_established.py",
                      "manifest inflated to 'compiles cleanly'", SLOW_TIMEOUT)


def m_established_drop_unestablished(sb):
    """Shortening the NOT-ESTABLISHED list without a verification landing."""
    rel = "00_ESTABLISHED/README.md"
    for token in ("η = 0", "Power-Max", "Justice"):
        if sb.resub(rel, re.escape(token), "[withdrawn from the ledger]"):
            return expect_red(sb, f"{S}/check_established.py",
                              f"'{token}' quietly removed from the NOT-ESTABLISHED list",
                              SLOW_TIMEOUT)
    return ProbeResult(False, "none of the must-stay-unestablished tokens were present")


def m_g2_successor(sb):
    rel = f"{S}/check_g2_normal_form.py"
    if not sb.sub(rel, 'x = x + 1 if c == "S" else 1 / x',
                  'x = x + 2 if c == "S" else 1 / x  # SEEDED'):
        return ProbeResult(False, "probe could not find val() to mutate")
    return expect_red(sb, rel, "MODEL MUTANT: successor changed from x+1 to x+2", SLOW_TIMEOUT)


def m_g2_shrink_bound(sb):
    rel = f"{S}/check_g2_normal_form.py"
    if not sb.sub(rel, "WORD_LEN = 18", "WORD_LEN = 3"):
        return ProbeResult(False, "probe could not find WORD_LEN")
    return expect_red(sb, rel, "DECLARED BOUND MUTANT: exhaustive length 18 -> 3", SLOW_TIMEOUT)


def m_gb_successor(sb):
    rel = f"{S}/check_generative_base.py"
    if not sb.sub(rel, 'x = x + 1 if c == "S" else 1 / x',
                  'x = x + 2 if c == "S" else 1 / x  # SEEDED'):
        return ProbeResult(False, "probe could not find val() to mutate")
    return expect_red(sb, rel, "MODEL MUTANT: successor changed from x+1 to x+2", SLOW_TIMEOUT)


def m_gb_shrink_word_len(sb):
    rel = f"{S}/check_generative_base.py"
    if not sb.sub(rel, "WORD_LEN = 10", "WORD_LEN = 4"):
        return ProbeResult(False, "probe could not find WORD_LEN")
    return expect_red(sb, rel, "DECLARED BOUND MUTANT: exhaustive length 10 -> 4", SLOW_TIMEOUT)


def m_gb_shrink_grid(sb):
    rel = f"{S}/check_generative_base.py"
    if not sb.sub(rel, "GRID = 25", "GRID = 3"):
        return ProbeResult(False, "probe could not find GRID")
    return expect_red(sb, rel, "DECLARED BOUND MUTANT: reachability grid 25 -> 3", SLOW_TIMEOUT)


def m_gb_reducedness(sb):
    rel = f"{S}/check_generative_base.py"
    if not sb.sub(rel, 'return "ii" not in w and not w.startswith("i")',
                  "return True  # SEEDED"):
        return ProbeResult(False, "probe could not find reduced() to mutate")
    return expect_red(sb, rel, "GRAMMAR MUTANT: reducedness predicate weakened to True",
                      SLOW_TIMEOUT)


def m_secrets_staged(sb):
    rel = "SEEDED_SECRET_PROBE.md"
    sb.write(rel, "key = sk-ant-api03-" + "A" * 40 + "\n")
    subprocess.run(["git", "add", "--", rel], cwd=str(sb.tree), capture_output=True, text=True)
    out = expect_red(sb, f"{S}/check_no_secrets_staged.py",
                     "an Anthropic-shaped key staged in the CLONE's index")
    subprocess.run(["git", "reset", "-q", "--", rel], cwd=str(sb.tree),
                   capture_output=True, text=True)
    return out


def m_record_counters(sb):
    rel = "12_PUBLIC_SITE/record/index.html"
    n = sb.resub(rel, r'id="c-tested" data-count="(\d+)">(\d+)<',
                 lambda m: f'id="c-tested" data-count="{int(m.group(1)) - 3}">{int(m.group(2)) - 3}<')
    if not n:
        return ProbeResult(False, "probe could not find the c-tested fallback")
    return expect_red(sb, f"{S}/check_record_counters.py",
                      "static no-JS counter understated by 3 against the rows")


def m_record_row_verdict(sb):
    """Flip a row's verdict so the tally and the fallback disagree the other way."""
    rel = "12_PUBLIC_SITE/record/index.html"
    if not sb.resub(rel, r'data-verdict="cut"', 'data-verdict="held"', flags=0):
        return ProbeResult(False, "no cut row found to flip")
    return expect_red(sb, f"{S}/check_record_counters.py",
                      "one 'cut' row relabelled 'held' — the against-count drops")


def m_tree_tombstone_authority_append(sb):
    rel = "08_FRAMEWORK_SUPPORT/00_META/CLAUDE.md"
    if not sb.exists(rel):
        return ProbeResult(False, "exact support-meta tombstone is missing")
    sb.append(rel, "\nThis directory owns active doctrine and governance.\n")
    return expect_red(
        sb,
        f"{S}/check_tree_contract.py",
        "authority claim appended to an otherwise valid compatibility tombstone",
    )


def m_tree_extra_directory(sb):
    extra = sb.tree / "08_FRAMEWORK_SUPPORT/00_META/UNREGISTERED_EMPTY"
    extra.mkdir()
    try:
        return expect_red(
            sb,
            f"{S}/check_tree_contract.py",
            "an otherwise invisible empty directory added to held tombstone custody",
        )
    finally:
        extra.rmdir()


def m_tree_symlink_directory(sb):
    link = sb.tree / "08_FRAMEWORK_SUPPORT/00_META/UNREGISTERED_LINK"
    target = sb.tree / "08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS"
    link.symlink_to(target, target_is_directory=True)
    try:
        return expect_red(
            sb,
            f"{S}/check_tree_contract.py",
            "a symlink-to-directory added to held tombstone custody",
        )
    finally:
        link.unlink()


def m_tree_broken_meta_symlink(sb):
    link = sb.tree / "05_COSMOLOGY/00_META"
    link.symlink_to(sb.tree / "MISSING_META_TARGET", target_is_directory=True)
    try:
        return expect_red(
            sb,
            f"{S}/check_tree_contract.py",
            "a broken symlink named 00_META added to an active lane",
        )
    finally:
        link.unlink()


def m_tree_meta_regular_file(sb):
    path = sb.tree / "05_COSMOLOGY/00_META"
    path.write_text("not a directory\n", encoding="utf-8")
    try:
        return expect_red(
            sb,
            f"{S}/check_tree_contract.py",
            "a regular file named 00_META added to an active lane",
        )
    finally:
        path.unlink()


def v_tree_held_debt_visible(sb):
    res = sb.run(f"{S}/check_tree_contract.py")
    visible = (
        res["status"] == "PASS"
        and "TREE CONTRACT: PASS-WITH-DEBT" in res["out"]
        and "D-OWNER-02 is UNSET" in res["out"]
    )
    return ProbeResult(
        visible,
        "exact grandfathered tombstones remain explicitly visible as held debt",
        head(res["out"], 4),
    )


def m_trophic_extraction(sb):
    sb.append("00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
              "\nA higher caste may extract from a lower caste without limit.\n")
    return expect_red(sb, f"{S}/check_trophic_rosetta_doctrine.py",
                      "hereditary-extraction licence written into a live owner")


def m_ruling_threshold(sb):
    """The WO-D1-2026-07-19 ruling has 2 carriers. With --threshold 2 the
    gate must go green; if it stays red, the threshold knob is broken.
    Also tests a third value: --threshold 1 must STAY red (2 > 1), proving
    the threshold is not a constant-bypass."""
    res = sb.run(f"{S}/check_ruling_landed.py",
                 args=["--ruling-id", "WO-D1-2026-07-19", "--threshold", "2"])
    if res["status"] != "PASS":
        return ProbeResult(False, f"threshold=2 -> {res['status']} rc={res['rc']}",
                           head(res["out"], 5))
    res2 = sb.run(f"{S}/check_ruling_landed.py",
                  args=["--ruling-id", "WO-D1-2026-07-19", "--threshold", "1"])
    if res2["status"] != "FAIL":
        return ProbeResult(False, f"threshold=1 -> {res2['status']} (should still be red)",
                           head(res2["out"], 5))
    return ProbeResult(True,
                       "threshold knob honored: red→green at 2, green→red at 1",
                       head(res["out"], 3))


def m_foundation_lake_excluded(sb):
    """The .lake/ exclusion at check_foundation.py:170-182 must hold even
    under a malicious deposit. We plant the retired Titan infix inside a
    fresh .lake/packages/ tree in the clone; if the gate flags it, the
    exclusion is broken. (This is the regression that produced the 365 s
    hang on 2026-08-06.)"""
    target = ".lake/packages/emergentism_lake_probe/Titan.lean"
    sb.write(target,
             "-- this file is a Lean build cache simulation, not a corpus surface\n"
             "theorem seeded : True := by\n"
             "  exact (\"⊙ = " + "• × ○\")  -- SEEDED: the gate must NOT see this\n"
             "  trivial\n")
    res = sb.run(f"{S}/check_foundation.py")
    if "SEEDED" in res["out"] or target in res["out"]:
        return ProbeResult(False,
                           f"the gate scanned .lake/ (saw {target} in its output) — "
                           f"exclusion is broken",
                           head(res["out"], 8))
    return ProbeResult(True,
                       ".lake/ excluded: the seeded retired-Titan infix in "
                       ".lake/packages/.../Titan.lean was not surfaced",
                       head(res["out"], 3))


def m_foundation_mention_lines_struck(sb):
    """mention_lines() should excuse a properly-struck mention of the
    retired form. We plant a single struck mention in a live source owner
    that the gate definitely scans; if the gate flags it, mention_lines()
    is broken on strikethrough syntax. (Pre-fix this matched the
    `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md` at :121/:416/:417
    case the gate's own comment names.)"""
    target = "00_THE_FOUNDATION.md"
    if not sb.exists(target):
        return ProbeResult(False, f"target surface missing in clone: {target}")
    body = sb.read(target)
    seed_line = "\n~~⊙ = " + "• × ○~~ — historical form, struck in this edition.\n"
    if "SEEDED_MENTION_LINES" in body:
        return ProbeResult(False, "probe already ran on this clone; cannot seed again")
    sb.append(target, f"\n<!-- SEEDED_MENTION_LINES -->{seed_line}")
    res = sb.run(f"{S}/check_foundation.py")
    # The gate's findings list mentions line numbers; if our seeded line
    # is among them, mention_lines() did not excuse it.
    if "SEEDED_MENTION_LINES" in res["out"]:
        return ProbeResult(False,
                           "the struck mention was flagged — mention_lines() is "
                           "blind to a properly-struck mention of the retired form",
                           head(res["out"], 12))
    return ProbeResult(True,
                       "mention_lines() excused the struck mention of the retired form",
                       head(res["out"], 3))


def m_trophic_required_missing(sb):
    """The doctrine's REQUIRED phrases are as load-bearing as its FORBIDDEN ones."""
    rel = "05_COSMOLOGY/03_FORMAL_SYSTEM/46_THE_ETA_CONVERSION_MAP.md"
    if not sb.resub(rel, r"η_move = 0", "η_move is small"):
        return ProbeResult(False, "the required phrase was not present to remove")
    return expect_red(sb, f"{S}/check_trophic_rosetta_doctrine.py",
                      "required doctrine phrase 'η_move = 0' removed from its owner")


# ---------------------------------------------------------------------------
# GREEN probes — repairs for gates that are currently RED
# ---------------------------------------------------------------------------


def g_links(sb):
    """The gate names one dangling link. Its target exists nowhere in the tree,
    so the repair its own message implies is to drop the link, not re-path it."""
    rel = "05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md"
    n = sb.resub(rel, r"\[`?00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05\.md`?\]"
                      r"\(\.\./\.\./\.\./00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05\.md\)",
                 "`00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md` (not on disk)")
    if not n:
        return ProbeResult(False, "the dangling link this probe repairs has moved or been fixed")
    return expect_green(sb, f"{S}/check_links.py",
                        f"de-linked {n} reference whose target is not on disk")


def g_d6(sb):
    """Rewrite every live literal D6≡D0 to the permitted tilde form."""
    res = sb.run(f"{S}/check_d6_equiv_d0.py")
    files = sorted({m.group(1) for m in re.finditer(r"^- ([^:]+):\d+:", res["out"], re.M)})
    n = 0
    for rel in files:
        n += sb.resub(rel, r"D\s*6\s*(?:≡|=|↔|≅)\s*D\s*0", "D6~D0")
        n += sb.resub(rel, r"D\s*0\s*(?:≡|=|↔|≅)\s*D\s*6", "D0~D6")
    if not n:
        return ProbeResult(False, "no live literal forms found to rewrite")
    return expect_green(sb, f"{S}/check_d6_equiv_d0.py",
                        f"rewrote {n} literal form(s) to the permitted tilde across "
                        f"{len(files)} file(s)")


def g_receipt_citations(sb):
    """This gate is a two-sided fence: it is RED when the count rises AND RED
    when the count falls. Its green is the single point AMBIGUOUS_BASELINE.
    The probe therefore reports where green actually lives."""
    res = sb.run(f"{S}/check_receipt_citations.py")
    m = re.search(r"ambiguous receipt numbers (rose|FELL) to (\d+) \(baseline (\d+)\)", res["out"])
    detail = ("gate is a two-sided fence: " + res["out"].splitlines()[1][:160]) if m else "shape changed"
    return ProbeResult(False, detail, head(res["out"], 3))


def m_receipt_citation_collision(sb):
    """Add a second live r243 target; the namespace baseline must reject it."""

    path = sb.tree / "11_UPLINK/60_SESSION_PACKETS/243_MUTATION_COLLISION.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Seeded duplicate receipt namespace target\n", encoding="utf-8")
    try:
        return expect_red(
            sb,
            f"{S}/check_receipt_citations.py",
            "a second undeclared live r243 target raises the collision baseline",
        )
    finally:
        path.unlink()


def g_barred(sb):
    hits = 0
    for rel in ("12_PUBLIC_SITE/2/index.html", "12_PUBLIC_SITE/4/index.html",
                "12_PUBLIC_SITE/5/index.html"):
        hits += sb.resub(rel, r"P\s*=\s*Φ\s*×\s*V", "P is jointly limited by Φ and V")
        hits += sb.resub(rel, r"⊙\s*=\s*•\s*×\s*○", "⊙ names the held relation of • and ○")
    if not hits:
        return ProbeResult(False, "no barred strings found to repair")
    return expect_green(sb, f"{S}/check_barred_claims.py", f"rewrote {hits} barred string(s)")


def g_q4(sb):
    n = 0
    for route in ("amrita", "egg", "riemann", "suda"):
        n += sb.resub(f"12_PUBLIC_SITE/{route}/index.html",
                      r'(<meta name="robots" content=")noindex, follow(")', r"\1index, follow\2")
    if not n:
        return ProbeResult(False, "no robots metas found to repair")
    return expect_green(sb, f"{S}/check_q4_declarations.py",
                        f"restored the ruling's declared robots directive on {n} route(s)")


SITE_GENERATORS = ("build_atlas_index.py", "build_library_index.py", "build_library_nav.py",
                   "build_social_cards.py", "build_rag_index.py", "build_sw_version.py")


def g_site_artifacts(sb):
    """The gate's own message names the repair: replay the generator sequence."""
    site = sb.tree / "12_PUBLIC_SITE"
    ran, failed = [], []
    for gen in SITE_GENERATORS:
        if not (site / gen).is_file():
            continue
        proc = subprocess.run([sys.executable, "-B", gen], cwd=str(site),
                              capture_output=True, text=True, timeout=SLOW_TIMEOUT)
        ran.append(gen)
        if proc.returncode != 0:
            failed.append(f"{gen} rc={proc.returncode}")
    out = expect_green(sb, f"{S}/check_site_build_artifacts.py",
                       f"replayed {len(ran)} generator(s) in the clone"
                       + (f"; generators that themselves failed: {', '.join(failed)}" if failed else ""),
                       SLOW_TIMEOUT)
    return out


def g_work_in_progress(sb):
    """Repair the two conditions the gate names, then re-run and report."""
    manifest = "00_WORK_IN_PROGRESS/README.md"
    res = sb.run(f"{S}/check_work_in_progress.py")
    steps = []
    for _ in range(6):  # the repairs cascade; bounded so a probe cannot spin
        fixed = False
        for line in res["out"].splitlines():
            m = re.search(r"manifest says (\d+) receipt files; there are (\d+)", line)
            if m:
                fixed |= bool(sb.resub(manifest, rf"{m.group(1)}\s+numbered receipts",
                                       f"{m.group(2)} numbered receipts"))
                fixed |= bool(sb.resub(manifest, rf"{m.group(1)} receipt files",
                                       f"{m.group(2)} receipt files"))
                steps.append(f"receipt count {m.group(1)}->{m.group(2)}")
                continue
            m = re.search(r"manifest says (\d+) (\w+); CLAIM_STATUS\.yaml has (\d+)", line)
            if m:
                fixed |= bool(sb.resub(manifest, rf"^(\s*){m.group(1)}(\s+{m.group(2)}\b)",
                                       rf"\g<1>{m.group(3)}\g<2>", flags=re.M))
                steps.append(f"{m.group(2)} {m.group(1)}->{m.group(3)}")
        if not fixed:
            break
        res = sb.run(f"{S}/check_work_in_progress.py")
    return ProbeResult(res["status"] == "PASS",
                       f"mechanical repairs applied ({'; '.join(steps) or 'none'}) -> "
                       f"{res['status']} rc={res['rc']}",
                       head(res["out"], 5))


# --- minimal-tree reachability probes --------------------------------------


def mt(script: str, extras: tuple[str, ...] = (), timeout: int = DEFAULT_TIMEOUT):
    return lambda sb: minimal_tree_probe(sb, script, extras, timeout)


# ---------------------------------------------------------------------------
# the register
# ---------------------------------------------------------------------------


@dataclass
class GateSpec:
    name: str
    path: str
    red_probes: list[tuple[str, Callable]] = field(default_factory=list)
    green_probes: list[tuple[str, Callable]] = field(default_factory=list)
    # verify_probes run regardless of baseline. They test INTERNAL logic
    # of the gate (exclusion lists, use/mention handling, threshold
    # honours) rather than the gate's verdict on the corpus. P2.1 added
    # these so check_foundation's .lake/ and mention_lines() invariants
    # can be proven independently of the corpus being red.
    verify_probes: list[tuple[str, Callable]] = field(default_factory=list)
    timeout: int = DEFAULT_TIMEOUT
    # Args to pass to the gate on the baseline run. Some gates (notably
    # check_ruling_landed) require flags to perform their actual job;
    # without the right flags they return rc=2 (error), not rc=1 (verdict).
    baseline_args: tuple[str, ...] = ()
    note: str = ""


PURITY_IMPORTS = (f"{S}/check_emergentism_purity.py",)

GATES: list[GateSpec] = [
    GateSpec("check_active_receipt_citations", f"{S}/check_active_receipt_citations.py",
             green_probes=[("minimal tree", mt(f"{S}/check_active_receipt_citations.py"))],
             note="~124 violations; repair set too large to edit mechanically"),
    GateSpec("check_adjudication_custody", f"{S}/check_adjudication_custody.py",
             red_probes=[("blank record", m_adjudication_blank),
                         ("verdict flipped", m_adjudication_verdict)]),
    GateSpec("check_barred_claims", f"{S}/check_barred_claims.py",
             green_probes=[("rewrite the barred strings", g_barred)]),
    GateSpec("check_claim_status", f"{S}/check_claim_status.py",
             note="NameError: reopened_ids used before assignment (~line 705)"),
    GateSpec("check_coherence_profile", f"{S}/check_coherence_profile.py",
             red_probes=[("overall understated", m_coherence_overall),
                         ("world contact inflated", m_coherence_world_contact)]),
    GateSpec("check_contact_limited", f"{S}/check_contact_limited.py",
             note="inherits the check_claim_status NameError through its policy import"),
    GateSpec("check_contradiction_census", f"{S}/check_contradiction_census.py",
             green_probes=[("minimal tree", mt(f"{S}/check_contradiction_census.py"))]),
    GateSpec("check_d6_equiv_d0", f"{S}/check_d6_equiv_d0.py",
             red_probes=[("literal form", m_d6_literal),
                         ("spaced literal", m_d6_spaced),
                         ("frozen historical byte drift", m_d6_frozen_historical_byte_drift),
                         ("literal beyond frozen body", m_d6_literal_beyond_frozen_body),
                         ("frozen historical parent symlink", m_d6_frozen_historical_parent_symlink),
                         ("archive-tagged refutation drift", m_d6_archive_tagged_refutation_byte_drift)],
             green_probes=[("rewrite literals to the tilde form", g_d6)]),
    GateSpec("check_dead_citations", f"{S}/check_dead_citations.py",
             green_probes=[("minimal tree", mt(f"{S}/check_dead_citations.py"))],
             note="13 undisclosed dead citations; repair is editorial"),
    GateSpec("check_emergentism_purity", f"{S}/check_emergentism_purity.py",
             green_probes=[("minimal tree", mt(f"{S}/check_emergentism_purity.py"))],
             note="hundreds of authority tokens across the active corpus"),
    GateSpec("check_established", f"{S}/check_established.py", timeout=SLOW_TIMEOUT,
             red_probes=[("verification inflation", m_established_inflation),
                         ("unestablished entry dropped", m_established_drop_unestablished)]),
    GateSpec("check_forwarding_stubs", f"{S}/check_forwarding_stubs.py",
             green_probes=[("minimal tree", mt(f"{S}/check_forwarding_stubs.py"))],
             note="5 stub-chain / grave-target violations"),
    GateSpec("check_foundation", f"{S}/check_foundation.py", timeout=SLOW_TIMEOUT,
             green_probes=[("minimal tree", mt(f"{S}/check_foundation.py", timeout=SLOW_TIMEOUT))],
             verify_probes=[(".lake/ exclusion holds", m_foundation_lake_excluded),
                            ("mention_lines() excuses struck text", m_foundation_mention_lines_struck)],
             note="was non-terminating at 90s on 2026-08-06 10:42; the file was being "
                  "edited concurrently and returned FAIL in 5s at 10:53; the .lake/ "
                  "exclusion is in place (verify-probe confirms); the 50 quoted-and-"
                  "struck mentions are still flagged (P2.2 will fix mention_lines())"),
    GateSpec("check_g2_normal_form", f"{S}/check_g2_normal_form.py", timeout=SLOW_TIMEOUT,
             red_probes=[("model mutant x+1 -> x+2", m_g2_successor),
                         ("declared bound 18 -> 3", m_g2_shrink_bound)]),
    GateSpec("check_generative_base", f"{S}/check_generative_base.py", timeout=SLOW_TIMEOUT,
             red_probes=[("model mutant x+1 -> x+2", m_gb_successor),
                         ("word-length bound 10 -> 4", m_gb_shrink_word_len),
                         ("reachability grid 25 -> 3", m_gb_shrink_grid),
                         ("reducedness weakened", m_gb_reducedness)]),
    GateSpec("check_links", f"{S}/check_links.py",
             green_probes=[("de-link the dangling target", g_links)]),
    GateSpec("check_no_secrets_staged", f"{S}/check_no_secrets_staged.py",
             red_probes=[("staged live-shaped key", m_secrets_staged)]),
    GateSpec("check_node_product_ranking", f"{S}/check_node_product_ranking.py",
             green_probes=[("minimal tree", mt(f"{S}/check_node_product_ranking.py",
                                               PURITY_IMPORTS))],
             note="many retired-product occurrences across the active corpus"),
    GateSpec("check_q4_declarations", f"{S}/check_q4_declarations.py",
             green_probes=[("restore the robots directives", g_q4)]),
    GateSpec("check_receipt_citations", f"{S}/check_receipt_citations.py",
             red_probes=[("new live receipt collision", m_receipt_citation_collision)],
             note="ambiguity baseline and current count are both 94. The checker is a "
                  "two-sided fence: any rise fails, and any fall requires the baseline "
                  "to be lowered in the same repair."),
    GateSpec("check_record_counters", f"{S}/check_record_counters.py",
             red_probes=[("static fallback understated", m_record_counters),
                         ("row verdict relabelled", m_record_row_verdict)]),
    GateSpec("check_review_bundle", f"{S}/check_review_bundle.py",
             green_probes=[("minimal tree", mt(f"{S}/check_review_bundle.py"))],
             note="a frozen document's hash moved; the repair is an owner act "
                  "(bump the bundle version), not a mechanical edit"),
    GateSpec("check_ruling_landed", f"{S}/check_ruling_landed.py",
             baseline_args=("--ruling-id", "WO-D1-2026-07-19"),
             verify_probes=[("threshold knob honoured", m_ruling_threshold)],
             note="WO-D1-2026-07-19 ruling has 2 public_html carriers "
                  "(5/index.html, corrections/index.html); the audit proves the "
                  "threshold mechanism works — the corpus repair is an owner act"),
    GateSpec("check_site_build_artifacts", f"{S}/check_site_build_artifacts.py",
             timeout=SLOW_TIMEOUT,
             green_probes=[("replay every generator", g_site_artifacts)]),
    GateSpec("check_tree_contract", f"{S}/check_tree_contract.py",
             red_probes=[
                 ("tombstone authority append", m_tree_tombstone_authority_append),
                 ("extra held-custody directory", m_tree_extra_directory),
                 ("held-custody symlink directory", m_tree_symlink_directory),
                 ("broken non-root 00_META symlink", m_tree_broken_meta_symlink),
                 ("non-directory 00_META entry", m_tree_meta_regular_file),
             ],
             green_probes=[("minimal tree", mt(f"{S}/check_tree_contract.py"))],
             verify_probes=[("held topology debt remains visible", v_tree_held_debt_visible)],
             note="grandfathered support-meta violation is exact-inventory and digest bound"),
    GateSpec("check_trophic_rosetta_doctrine", f"{S}/check_trophic_rosetta_doctrine.py",
             red_probes=[("forbidden phrase added", m_trophic_extraction),
                         ("required phrase removed", m_trophic_required_missing)]),
    GateSpec("check_work_in_progress", f"{S}/check_work_in_progress.py",
             green_probes=[("repair the counts it names", g_work_in_progress)]),
    GateSpec("check_public_semantic_parity", "12_PUBLIC_SITE/check_public_semantic_parity.py",
             note="NameError: excluded_routes used before assignment (~line 541)"),
]


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------


def discover() -> list[str]:
    found: list[str] = []
    for pattern in CHECK_GLOBS:
        found.extend(sorted(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern)))
    return found


def make_clone(dest: Path) -> Path:
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    if subprocess.run(["cp", "-Rc", str(ROOT), str(dest)],
                      capture_output=True, text=True).returncode != 0:
        subprocess.run(["cp", "-R", str(ROOT), str(dest)], capture_output=True, text=True)
    if not dest.is_dir():
        raise SystemExit("REFUSING TO RUN: could not clone the corpus. This script "
                         "never mutates the live tree.")
    return dest


def classify(baseline: str, probes: list[dict], spec: GateSpec) -> tuple[str, str]:
    if baseline == "HANG":
        return DOES_NOT_RUN, "does not terminate; no verdict is reachable"
    if baseline == "ERROR":
        return DOES_NOT_RUN, "raises before reaching a verdict"
    usable = [p for p in probes if not p.get("probe_error")]
    if baseline == "PASS":
        if not usable:
            return UNDETERMINED, "green on the corpus; no usable RED probe"
        caught = [p for p in usable if p["ok"]]
        survived = [p["label"] for p in usable if not p["ok"]]
        if not caught:
            return CANNOT_FAIL, (f"green under every seeded fault "
                                 f"({len(survived)}/{len(usable)} survived)")
        if survived:
            return SOUND_BLIND, "blind to: " + "; ".join(survived)
        return SOUND, f"caught all {len(caught)} seeded fault(s)"
    # baseline FAIL
    if not usable:
        return UNDETERMINED, "red on the corpus; no usable GREEN probe"
    if any(p["ok"] for p in usable):
        return SOUND, "red on the corpus, green on a reachable input"
    if any(SELF_REFUTING in p["detail"] for p in usable):
        return CANNOT_PASS, ("red on a tree containing nothing but itself, and the "
                             "complaint names its own source file")
    return UNDETERMINED, ("red on the corpus; no green witness found. Unreachability "
                          "is NOT proven — the probes were inconclusive, which is not "
                          "the same as a verdict")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--census", action="store_true", help="baseline run only, no probes")
    ap.add_argument("--only", action="append", default=[], help="gate name (repeatable)")
    ap.add_argument("--clone", default=None)
    ap.add_argument("--keep-clone", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args(argv)

    on_disk = discover()
    specced = {g.path for g in GATES}
    print("── MUTATION SURVEY OF THE GATES ──────────────────────────────────")
    print(f"corpus: {ROOT}")
    print(f"checkers on disk: {len(on_disk)}")
    unspecced = [p for p in on_disk if p not in specced]
    stale = [g.path for g in GATES if g.path not in on_disk]
    if unspecced:
        print(f"NOT SURVEYED (added since this script was written): {', '.join(unspecced)}")
    if stale:
        print(f"SPECCED BUT ABSENT: {', '.join(stale)}")
    print()

    gates = [g for g in GATES if g.path in on_disk]
    if args.only:
        gates = [g for g in gates if g.name in args.only]

    print("PHASE 1 — baseline census (live tree, read-only)")
    results: list[dict] = []
    for g in gates:
        res = run_script(ROOT, g.path, args=list(g.baseline_args), timeout=g.timeout)
        print(f"  {res['status']:5}  rc={str(res['rc']):>4}  {res['wall_s']:7.2f}s  "
              f"findings={str(res['findings']):>5}  {g.name}")
        results.append({"name": g.name, "path": g.path, "baseline": res["status"],
                        "rc": res["rc"], "wall_s": res["wall_s"],
                        "findings": res["findings"],
                        "baseline_head": head(res["out"], 3), "note": g.note,
                        "probes": []})
    print()

    if args.census:
        summarise(results)
        return 0

    clone_root = Path(args.clone) if args.clone else (
        Path(tempfile.gettempdir()) / f"mutgate_{os.getpid()}" / ROOT.name)
    print(f"PHASE 2 — probes (clone at {clone_root})")
    make_clone(clone_root)
    sb = Sandbox(clone_root)

    try:
        for g, row in zip(gates, results):
            probes = g.red_probes if row["baseline"] == "PASS" else g.green_probes
            if row["baseline"] in {"HANG", "ERROR"}:
                probes = []
            for label, fn in probes:
                try:
                    out = fn(sb)
                    err = False
                except Exception as exc:
                    out, err = ProbeResult(False, f"PROBE ERROR: {type(exc).__name__}: {exc}"), True
                finally:
                    sb.restore()
                row["probes"].append({"label": label, "ok": out.ok, "detail": out.detail,
                                      "observed": out.observed, "probe_error": err})
            # verify_probes run regardless of baseline; their results are
            # recorded but do not move the gate's primary classification.
            for label, fn in g.verify_probes:
                try:
                    out = fn(sb)
                    err = False
                except Exception as exc:
                    out, err = ProbeResult(False, f"PROBE ERROR: {type(exc).__name__}: {exc}"), True
                finally:
                    sb.restore()
                row["probes"].append({"label": f"[verify] {label}", "ok": out.ok,
                                      "detail": out.detail, "observed": out.observed,
                                      "probe_error": err})
            row["class"], row["why"] = classify(row["baseline"], row["probes"], g)
            print(f"  {row['class']:16} {g.name}  — {row['why']}")
            for p in row["probes"]:
                mark = "caught" if p["ok"] else "SURVIVED/NOT-GREEN"
                print(f"       [{mark}] {p['detail']}")
    finally:
        sb.restore()
        if not args.keep_clone and str(clone_root).startswith(tempfile.gettempdir()):
            shutil.rmtree(clone_root.parent, ignore_errors=True)

    print()
    summarise(results)
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"wrote {args.json}")
    return 0


def summarise(results: list[dict]) -> None:
    from collections import Counter
    print("── SUMMARY ───────────────────────────────────────────────────────")
    base = Counter(r["baseline"] for r in results)
    print("baseline: " + "  ".join(f"{k}={v}" for k, v in sorted(base.items())))
    if any("class" in r for r in results):
        cls = Counter(r.get("class", UNDETERMINED) for r in results)
        print("verdict : " + "  ".join(f"{k}={v}" for k, v in sorted(cls.items())))
        # P2.1 4-bucket classification: collapse the 6-class taxonomy to
        # the four verdicts the V-forcing directive asked for.
        four = Counter(_class_to_four_bucket(r.get("class", UNDETERMINED))
                       for r in results)
        print("4-bucket: " + "  ".join(f"{k}={v}" for k, v in sorted(four.items())))
        # Verify-probe rollup: how many of the gate's internal-logic
        # checks (e.g. .lake/ exclusion, mention_lines()) passed.
        verify_total = sum(len([p for p in r.get("probes", []) if p["label"].startswith("[verify]")])
                           for r in results)
        verify_passed = sum(sum(1 for p in r.get("probes", [])
                                if p["label"].startswith("[verify]") and p["ok"])
                            for r in results)
        if verify_total:
            print(f"verify  : {verify_passed}/{verify_total} internal-logic checks passed")
    print(f"total   : {len(results)}")


# P2.1: map the 6-class verdict onto the V-forcing directive's 4 buckets.
# SOUND          -> healthy
# SOUND-BUT-BLIND -> blind (some faults survived; gate is partial)
# CANNOT-FAIL    -> broken (a gate that never goes red is unmeasurable; a
#                   known failure mode is the lowest it can do)
# CANNOT-PASS    -> false-positive (a gate that can't go green is an
#                   instrument with no reachable verdict, a verdict
#                   machine with one verdict)
# DOES-NOT-RUN   -> hang-class (timeout or crash; strictly worse than a
#                   wrong verdict, because it reports nothing)
# UNDETERMINED   -> undetermined (probes inconclusive; never guessed)
def _class_to_four_bucket(cls: str) -> str:
    return {
        SOUND: "healthy",
        SOUND_BLIND: "blind",
        CANNOT_FAIL: "broken",
        CANNOT_PASS: "false-positive",
        DOES_NOT_RUN: "hang-class",
        UNDETERMINED: "undetermined",
        SELF_REFUTING: "false-positive",
    }.get(cls, "undetermined")


if __name__ == "__main__":
    raise SystemExit(main())

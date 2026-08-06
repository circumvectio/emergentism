#!/usr/bin/env python3
"""Standing pass/fail/hang count for every check_*.py gate in this directory.

V-forcing directive (2026-08-06, P2.3): replace the user's hand-rolled
one-line survey with an instrument that auto-reruns. This script discovers
every `check_*.py` in the same directory (excluding the two non-orchestral
gates named below), runs each under a 60 s wall budget, and writes a JSON +
Markdown figure pair so the standing pass/fail/hang count is in the tree
and can be re-derived by `python3 gate_health.py`.

The script is read-only on the corpus. It only writes its own two output
files. It is idempotent: re-running it produces the same figures given the
same corpus state, with the only non-deterministic field being `generated_at`
(the ISO timestamp at the top of the figure).

Excluded gates:
  * check_links.py — pure local-Markdown link resolver; not part of the
    type-firewall/orchestral contract; CI owns it elsewhere.
  * check_no_secrets_staged.py — pre-commit guard, not an orchestral gate;
    inspects `git diff --cached` and would emit different findings on every
    run depending on what is staged. It is a different class of tool.

Exit-code semantics this script records:
  0    — pass
  1    — fail (one or more findings)
  124  — hang (subprocess.run timeout, the conventional bash `timeout` code)
  -1   — error (gate could not be invoked: not found, not executable, etc.)

Usage:
  python3 gate_health.py                 # write both figures next to this script
  python3 gate_health.py --json          # print JSON to stdout, do not write files
  python3 gate_health.py --timeout=30    # override the per-gate 60 s budget
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[2]  # 01_EMERGENTISM/

JSON_OUT = SCRIPT_DIR / "gate_health.json"
MD_OUT = SCRIPT_DIR / "gate_health.md"

DEFAULT_TIMEOUT = 60

# Gatest that are not part of the standing pass/fail/hang figure.
EXCLUDED_GATES = frozenset(
    {
        "check_links.py",  # pure local-Markdown link resolver (CI-owned)
        "check_no_secrets_staged.py",  # pre-commit diff guard, not orchestral
    }
)

# Verb markers the explicit-count parser looks for. First match wins. The
# count is allowed to be preceded by up to three intervening words so we
# catch both "3 finding(s)" and "13 undisclosed dead citation(s)" — the
# shape check_dead_citations.py actually prints.
_COUNT_WORD_RE = re.compile(
    r"(\d+)\s+(?:\w+\s+){0,3}?"
    r"(?:findings?|violations?|errors?|citations?|issues?|"
    r"discrepancies?|lapses?|infractions?|breaches?|defects?|"
    r"problems?|items?|instances?|rows?)\b",
    re.IGNORECASE,
)
# "...and N more" tail line that some gates print when truncating long
# failure lists (e.g. check_contradiction_census prints
# "... and 419 more (re-run this script to enumerate the full set)" with
# no leading bullet). Counted as N additional findings.
_AND_MORE_RE = re.compile(r"\.\.\.\s*and\s+(\d+)\s+more\b", re.IGNORECASE)
# Bullet line that begins a finding.
_BULLET_RE = re.compile(r"^\s*-\s+\S")
# "FAIL" header that some gates print before a long list of finding
# lines. The number of non-empty lines AFTER the header (minus the
# "...and N more" tail) is a strong proxy for the finding count when no
# explicit count is printed — used by check_emergentism_purity and
# check_node_product_ranking, which emit one "file:line: description"
# line per finding with no bullet prefix.
_FAIL_HEADER_RE = re.compile(r":\s*FAIL\b|\bFAIL\b\s*$")
# A line that looks like a per-finding entry: contains "path:line:" or
# "path:line " with a leading alphanumeric path segment.
_FINDING_LINE_RE = re.compile(r"^\S.*?:\d+:\s+\S")
# Python unhandled-exception traceback marker. When stderr carries this,
# the gate did not "fail with N findings" — it crashed. Reclassify to
# verdict="error" so the figure is honest about a broken gate.
_PYTHON_TRACEBACK_RE = re.compile(r"Traceback \(most recent call last\)")


@dataclass
class GateResult:
    """One row in the figure. Field names are stable (consumed by downstream tools)."""

    gate: str
    exit_code: int
    findings: int | None  # None = undetermined (parser could not read count)
    wall_seconds: float
    verdict: str  # pass | fail | hang | error
    truncated: bool = False  # True if subprocess.run timed out
    stdout_tail: str = ""  # last ~10 lines, for triage
    stderr_tail: str = ""  # last ~5 lines, for crash triage


@dataclass
class Figure:
    """The full figure. Field names are stable."""

    generated_at: str
    timeout_seconds: int
    excluded: list[str] = field(default_factory=list)
    totals: dict[str, int] = field(default_factory=dict)
    longest: dict[str, float] = field(default_factory=dict)
    slowest: list[dict[str, float]] = field(default_factory=list)
    results: list[GateResult] = field(default_factory=list)

    def to_jsonable(self) -> dict:
        return {
            "generated_at": self.generated_at,
            "timeout_seconds": self.timeout_seconds,
            "excluded": sorted(self.excluded),
            "totals": self.totals,
            "longest": self.longest,
            "slowest": self.slowest,
            "results": [asdict(r) for r in self.results],
        }


def discover_gates(script_dir: Path) -> list[Path]:
    """Return every check_*.py in script_dir, sorted, minus the excluded set."""

    gates = sorted(p for p in script_dir.glob("check_*.py") if p.is_file())
    return [p for p in gates if p.name not in EXCLUDED_GATES]


def count_findings(stdout: str, exit_code: int) -> int | None:
    """Best-effort count of findings/violations/errors in a gate's stdout.

    Returns None when no count can be read — this is the "undetermined"
    signal, distinct from 0. The figure marks it but the verdict still
    follows the exit code.

    Strategy (first hit wins):
      1. If exit_code == 0, return 0. A passing gate by definition has
         no findings, and any number it prints is a "scanned N" stat, not
         a count of findings.
      2. Look for an explicit "<N> findings/violations/errors/citations/
         issues/discrepancies/..." anywhere in stdout. The match allows
         up to three intervening words so we catch "13 undisclosed dead
         citation(s)" (check_dead_citations.py) as well as
         "3 finding(s)" (check_no_secrets_staged.py).
      3. Count bullet lines ("- error text"). For each "...and N more"
         truncation tail, add N to the count instead of counting it as 1.
         The ellipsis tail is matched without requiring a leading "- "
         so check_contradiction_census.py ("... and 419 more (re-run
         this script to enumerate the full set)") counts correctly.
      4. Count non-empty, finding-shaped lines after the first FAIL
         header. This is the "one-line-per-finding" shape that
         check_emergentism_purity and check_node_product_ranking use
         (lines like "FILE.md:NNN: description"). This is a stronger
         proxy than counting all lines, since FAIL headers are followed
         by exactly the finding list.
      5. If none of the above yields a count, return None.
    """

    if exit_code == 0:
        return 0

    # 2. explicit count
    for line in stdout.splitlines():
        match = _COUNT_WORD_RE.search(line)
        if match:
            return int(match.group(1))

    # 3. bullet list with "...and N more" tail
    total = 0
    counted_any = False
    for line in stdout.splitlines():
        if not _BULLET_RE.match(line):
            continue
        counted_any = True
        and_more = _AND_MORE_RE.search(line)
        if and_more:
            total += int(and_more.group(1))
        else:
            total += 1
    if counted_any:
        return total

    # 4. per-finding lines after a FAIL header
    after_fail = False
    finding_total = 0
    finding_counted = False
    for line in stdout.splitlines():
        if not after_fail and _FAIL_HEADER_RE.search(line):
            after_fail = True
            continue
        if not after_fail:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        # "...and N more" tail in the FAIL-body section also counts.
        and_more = _AND_MORE_RE.search(stripped)
        if and_more:
            finding_total += int(and_more.group(1))
            finding_counted = True
            continue
        if _FINDING_LINE_RE.match(stripped):
            finding_total += 1
            finding_counted = True
    if finding_counted:
        return finding_total

    # 5. undetermined
    return None


def tail(text: str, lines: int = 10) -> str:
    """Return the last `lines` non-empty lines of `text`, joined."""

    kept = [line for line in text.splitlines() if line.strip()]
    return "\n".join(kept[-lines:]) if kept else ""


def run_gate(gate: Path, timeout_seconds: int) -> GateResult:
    """Run a single gate, capture exit + findings + wall time."""

    start = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, str(gate)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        wall = time.monotonic() - start
        # 124 is the conventional `timeout` exit code; preserve the partial
        # stdout for triage (it usually contains a "Killed" or partial-findings
        # line that explains where the gate hung).
        partial_stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return GateResult(
            gate=gate.name,
            exit_code=124,
            findings=None,
            wall_seconds=round(wall, 3),
            verdict="hang",
            truncated=True,
            stdout_tail=tail(partial_stdout),
        )
    except FileNotFoundError:
        wall = time.monotonic() - start
        return GateResult(
            gate=gate.name,
            exit_code=-1,
            findings=None,
            wall_seconds=round(wall, 3),
            verdict="error",
            truncated=False,
            stdout_tail="",
        )
    except OSError as exc:
        wall = time.monotonic() - start
        return GateResult(
            gate=gate.name,
            exit_code=-1,
            findings=None,
            wall_seconds=round(wall, 3),
            verdict="error",
            truncated=False,
            stdout_tail=f"OSError: {exc}",
        )

    wall = time.monotonic() - start
    exit_code = completed.returncode
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""

    if exit_code == 0:
        verdict = "pass"
    elif exit_code == 124:
        verdict = "hang"
    elif exit_code == 1:
        # Python unhandled exceptions exit 1 with a traceback on stderr.
        # That is a broken gate, not a "fail with N findings" — the figure
        # has to say so, otherwise readers assume the corpus has open
        # findings when in fact the gate cannot run. Reclassify to
        # "error" but preserve the original exit_code for triage.
        if _PYTHON_TRACEBACK_RE.search(stderr):
            verdict = "error"
        else:
            verdict = "fail"
    else:
        # Some gates return 2 (e.g. check_contradiction_census) for usage
        # errors or empty inputs; record but do not classify as fail-with-findings
        # unless the stdout actually contains finding-shaped content.
        verdict = "fail" if stdout.strip() else "error"

    findings = count_findings(stdout, exit_code)
    return GateResult(
        gate=gate.name,
        exit_code=exit_code,
        findings=findings,
        wall_seconds=round(wall, 3),
        verdict=verdict,
        truncated=False,
        stdout_tail=tail(stdout),
        stderr_tail=tail(stderr, lines=5),
    )


def summarize(results: list[GateResult]) -> tuple[dict[str, int], dict, list]:
    """Compute totals, longest, slowest for the figure header."""

    totals = {
        "total": len(results),
        "pass": sum(1 for r in results if r.verdict == "pass"),
        "fail": sum(1 for r in results if r.verdict == "fail"),
        "hang": sum(1 for r in results if r.verdict == "hang"),
        "error": sum(1 for r in results if r.verdict == "error"),
    }
    wall_total = round(sum(r.wall_seconds for r in results), 3)
    totals["wall_seconds"] = wall_total

    if results:
        longest = max(results, key=lambda r: r.wall_seconds)
        longest_dict = {
            "gate": longest.gate,
            "wall_seconds": longest.wall_seconds,
        }
    else:
        longest_dict = {"gate": None, "wall_seconds": 0.0}

    slowest = sorted(results, key=lambda r: r.wall_seconds, reverse=True)[:3]
    slowest_list = [
        {"gate": r.gate, "wall_seconds": r.wall_seconds} for r in slowest
    ]

    return totals, longest_dict, slowest_list


def render_markdown(figure: Figure) -> str:
    """Render the human-readable figure."""

    totals = figure.totals
    longest = figure.longest
    slowest = figure.slowest
    lines: list[str] = []
    lines.append(f"# Gate Health — {figure.generated_at[:10]}")
    lines.append("")
    lines.append(f"Total: {totals['total']}")
    lines.append(f"Pass: {totals['pass']}")
    lines.append(f"Fail: {totals['fail']}")
    lines.append(f"Hang: {totals['hang']}")
    lines.append(f"Error: {totals['error']}")
    lines.append(
        f"Total wall time: {totals['wall_seconds']:.1f}s"
    )
    if longest.get("gate"):
        lines.append(
            f"Longest: {longest['gate']} ({longest['wall_seconds']:.2f}s)"
        )
    if slowest:
        slow_text = ", ".join(
            f"{s['gate']} ({s['wall_seconds']:.2f}s)" for s in slowest
        )
        lines.append(f"Slowest 3: {slow_text}")
    lines.append("")
    lines.append("| Gate | Exit | Findings | Wall (s) | Verdict |")
    lines.append("|------|------|----------|----------|---------|")
    # Sort by verdict (fail/hang/error first, then by wall desc) so a reader
    # scanning the table sees the actionable rows at the top.
    verdict_order = {"fail": 0, "hang": 1, "error": 2, "pass": 3}
    ordered = sorted(
        figure.results,
        key=lambda r: (verdict_order.get(r.verdict, 9), -r.wall_seconds, r.gate),
    )
    for r in ordered:
        findings = "?" if r.findings is None else str(r.findings)
        lines.append(
            f"| {r.gate} | {r.exit_code} | {findings} | "
            f"{r.wall_seconds:.2f} | {r.verdict} |"
        )
    lines.append("")
    # Hang-class candidates: any gate over 30 s. This is a soft signal — the
    # next run that crosses 30 s deserves a manual look, even if it did not
    # actually time out this run.
    hang_candidates = [r for r in figure.results if r.wall_seconds > 30.0]
    if hang_candidates:
        lines.append("## Gates > 30 s (hang-class candidates)")
        lines.append("")
        for r in hang_candidates:
            lines.append(
                f"- {r.gate}: {r.wall_seconds:.2f}s, verdict={r.verdict}"
            )
        lines.append("")
    lines.append(
        f"_Excluded (not part of the standing figure): "
        f"{', '.join(sorted(figure.excluded))}._"
    )
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Standing pass/fail/hang figure for check_*.py gates in this "
            "directory. Writes gate_health.json and gate_health.md by default."
        )
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"per-gate wall budget in seconds (default {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the JSON figure to stdout and do not write files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    if args.timeout <= 0:
        print(f"--timeout must be > 0 (got {args.timeout})", file=sys.stderr)
        return 2

    gates = discover_gates(SCRIPT_DIR)
    if not gates:
        print("no check_*.py gates discovered", file=sys.stderr)
        return 1

    results: list[GateResult] = []
    for gate in gates:
        result = run_gate(gate, args.timeout)
        results.append(result)
        # Live progress to stderr so a human watching the run sees the
        # numbers as they accumulate; the JSON/MD files are the durable
        # record.
        print(
            f"[{result.verdict:5s}] {result.gate:42s} "
            f"exit={result.exit_code:>4} findings={result.findings} "
            f"wall={result.wall_seconds:.2f}s",
            file=sys.stderr,
        )

    totals, longest, slowest = summarize(results)
    figure = Figure(
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        timeout_seconds=args.timeout,
        excluded=sorted(EXCLUDED_GATES),
        totals=totals,
        longest=longest,
        slowest=slowest,
        results=results,
    )
    payload = figure.to_jsonable()

    if args.json:
        json.dump(payload, sys.stdout, indent=2, sort_keys=False)
        sys.stdout.write("\n")
        return 0

    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    MD_OUT.write_text(render_markdown(figure), encoding="utf-8")
    print(
        f"\nwrote {JSON_OUT.relative_to(ROOT)} and {MD_OUT.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

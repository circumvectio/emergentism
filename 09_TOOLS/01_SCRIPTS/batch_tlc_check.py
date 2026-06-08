#!/usr/bin/env python3
"""
Guarded batch TLC checker for the Skyzai 300_Architecture TLA+ specs.

Default behavior is intentionally non-destructive:
- reports common scaffold fixes without changing source files;
- runs TLC against a temporary fixed copy;
- writes generated .cfg files only inside a temporary directory.

Pass --write-fixes to update source specs in place after reviewing the diff.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TLA_DIR = REPO_ROOT / (
    "03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/"
    "DAC_ARCHITECTURE/V3_CANONICAL/300_Architecture"
)
DEFAULT_TLC_JAR = Path.home() / ".local/tla/tla2tools.jar"
DEFAULT_SKIP = {
    "309_CHILD_DAC_TEMPLATE",
    "310_K2_RATIFICATION_WORKFLOW",
}
NON_INVARIANT_OPERATORS = {
    "Init",
    "Next",
    "Spec",
    "CanActivate",
    "CanArchive",
    "CanRatify",
    "CanRevoke",
    "NextChildId",
    "VerifySubstrate",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run guarded TLC checks over the Skyzai TLA+ architecture specs."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TLA_DIR,
        help="Directory containing .tla specs.",
    )
    parser.add_argument(
        "--tlc-jar",
        type=Path,
        default=DEFAULT_TLC_JAR,
        help="Path to tla2tools.jar.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Per-spec TLC timeout in seconds.",
    )
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        help="Module name to skip. Can be passed more than once.",
    )
    parser.add_argument(
        "--write-fixes",
        action="store_true",
        help="Write auto-fixes back to source specs. Default is dry-run only.",
    )
    parser.add_argument(
        "--no-tlc",
        action="store_true",
        help="Only report/apply auto-fixes; do not invoke TLC.",
    )
    return parser.parse_args()


def extract_module_name(content: str, fallback: str) -> str:
    match = re.search(r"^\s*-+\s*MODULE\s+(\w+)\s*-+\s*$", content, re.MULTILINE)
    return match.group(1) if match else fallback


def fix_spec_content(content: str) -> tuple[str, list[str]]:
    """Return fixed_content, changes without mutating the source file."""
    changes: list[str] = []

    lines = content.split("\n")
    if "Next ==" in content:
        next_block = content.split("Next ==", 1)[1].split("\n\n", 1)[0]
    else:
        next_block = ""

    in_next = False
    if r"\/" not in next_block:
        for i, line in enumerate(lines):
            if line.strip() == "Next ==":
                in_next = True
                continue
            if not in_next:
                continue
            if line.startswith(r"  /\ ("):
                lines[i] = line.replace(r"  /\ (", r"  \/ (", 1)
            elif line.startswith(r"  /\ "):
                lines[i] = line.replace(r"  /\ ", r"  \/ ", 1)
            elif line.strip() == "" or not line.startswith("  "):
                in_next = False

    fixed = "\n".join(lines)
    if fixed != content:
        changes.append(r"Next action choices: /\ -> \/")
        content = fixed

    next_section = content.split("Next ==", 1)[1] if "Next ==" in content else ""
    if "TimeBound" not in content and r"\E" in next_section and r"\in Nat" in next_section:
        content = content.replace("CONSTANTS\n", "CONSTANTS\n  TimeBound,\n", 1)
        before, after = content.split("Next ==", 1)
        after = after.replace(r"\in Nat", r"\in 0..TimeBound")
        content = "Next ==".join([before, after])
        changes.append(r"Next quantifiers: \in Nat -> \in 0..TimeBound")

    return content, changes


def extract_constants(content: str) -> list[str]:
    match = re.search(
        r"^CONSTANTS\s*\n(.*?)(?=^VARIABLES|\n\s*\n|\Z)",
        content,
        re.DOTALL | re.MULTILINE,
    )
    if not match:
        return []

    constants: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip().rstrip(",")
        if not line or line.startswith("("):
            continue
        for token in [part.strip() for part in line.split(",") if part.strip()]:
            constants.append(token)
    return constants


def constant_assignment(name: str) -> str | None:
    if name == "Nodes":
        return 'Nodes = {"n1", "n2", "n3"}'
    if name == "Archivers":
        return 'Archivers = {"a1"}'
    if name == "Layers":
        return 'Layers = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}'
    if name == "OQIds":
        return "OQIds = {1, 2}"
    if name == "OptionStrings":
        return 'OptionStrings = {"A", "B", "REVISION"}'
    if name == "ThetaDrift":
        return "ThetaDrift = 3"
    if name == "TauPathology":
        return "TauPathology = 5"
    if name == "MaxRound":
        return "MaxRound = 5"
    if name == "MaxCycles":
        return "MaxCycles = 10"
    if name == "MaxComputeBudget":
        return "MaxComputeBudget = 100"
    if name == "TimeBound":
        return "TimeBound = 10"
    if "Max" in name or "MAX" in name:
        return f"{name} = 5"
    if "Period" in name or "period" in name:
        return f"{name} = 2"
    if name == "N":
        return "N = 3"
    if name == "C":
        return "C = 2"
    return None


def build_cfg(content: str) -> str:
    """Generate a minimal TLC config as a string."""
    lines: list[str] = []
    assignments = [assignment for name in extract_constants(content) if (assignment := constant_assignment(name))]
    if assignments:
        lines.append("CONSTANTS")
        lines.extend(f"  {assignment}" for assignment in assignments)
        lines.append("")

    lines.extend(["INIT Init", "NEXT Next", "", "INVARIANTS"])

    for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*) ==\s*$", content, re.MULTILINE):
        name = match.group(1)
        if name not in NON_INVARIANT_OPERATORS:
            lines.append(f"  {name}")

    return "\n".join(lines) + "\n"


def run_tlc(
    source_spec_path: Path,
    module_name: str,
    content: str,
    tlc_jar: Path,
    timeout: int,
) -> dict[str, object]:
    """Run TLC against temporary spec/config files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / f"{module_name}.tla"
        tmp_cfg = Path(tmpdir) / f"{module_name}.cfg"
        tmp_path.write_text(content, encoding="utf-8")
        source_cfg = source_spec_path.with_suffix(".cfg")
        cfg_content = source_cfg.read_text(encoding="utf-8") if source_cfg.exists() else build_cfg(content)
        tmp_cfg.write_text(cfg_content, encoding="utf-8")

        try:
            result = subprocess.run(
                [
                    "java",
                    "-XX:+UseParallelGC",
                    "-cp",
                    str(tlc_jar),
                    "tlc2.TLC",
                    "-deadlock",
                    "-config",
                    str(tmp_cfg),
                    str(tmp_path),
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            partial_output = stdout + stderr
            return {
                "status": "TIMEOUT",
                "error": f"TLC timed out after {timeout}s",
                "output": partial_output,
                "source": str(source_spec_path),
            }

    output = result.stdout + result.stderr
    if "No error has been found" in output:
        states = re.search(r"(\d+) distinct states found", output)
        depth = re.search(r"depth of the complete state graph search is (\d+)", output)
        return {
            "status": "PASS",
            "states": int(states.group(1)) if states else 0,
            "depth": int(depth.group(1)) if depth else 0,
            "output": output,
        }

    if "Error:" in output:
        error = re.search(r"Error: (.+)", output)
        return {
            "status": "FAIL",
            "error": error.group(1) if error else "Unknown error",
            "output": output,
            "source": str(source_spec_path),
        }

    return {"status": "UNKNOWN", "output": output, "source": str(source_spec_path)}


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    skip_modules = DEFAULT_SKIP | set(args.skip)

    if not target.is_dir():
        print(f"Target directory not found: {target}", file=sys.stderr)
        return 2

    if not args.no_tlc and not args.tlc_jar.exists():
        print(f"TLC jar not found: {args.tlc_jar}", file=sys.stderr)
        print("Install tla2tools.jar or rerun with --no-tlc.", file=sys.stderr)
        return 2

    specs = sorted(target.glob("*.tla"))
    results: list[tuple[str, dict[str, object]]] = []
    seen_modules: set[str] = set()

    for spec_path in specs:
        original_content = spec_path.read_text(encoding="utf-8")
        module_name = extract_module_name(original_content, spec_path.stem)
        if spec_path.stem in skip_modules or module_name in skip_modules:
            continue
        if module_name in seen_modules:
            print(f"Skipping duplicate module artifact: {spec_path.relative_to(REPO_ROOT)}")
            continue
        seen_modules.add(module_name)

        print(f"\n{'=' * 60}")
        print(f"Checking {spec_path.relative_to(REPO_ROOT)} (module: {module_name})")

        fixed_content, changes = fix_spec_content(original_content)
        if changes:
            mode = "written" if args.write_fixes else "dry-run only; temp TLC copy uses fixes"
            print(f"  Auto-fixes ({mode}): {', '.join(changes)}")
            if args.write_fixes:
                spec_path.write_text(fixed_content, encoding="utf-8")

        if args.no_tlc:
            continue

        result = run_tlc(spec_path, module_name, fixed_content, args.tlc_jar, args.timeout)
        results.append((spec_path.name, result))

        if result["status"] == "PASS":
            print(f"  PASS - {result['states']} states, depth {result['depth']}")
        elif result["status"] == "FAIL":
            print(f"  FAIL - {result['error']}")
            for line in str(result["output"]).splitlines():
                if "Error:" in line or "line" in line.lower():
                    print(f"    {line}")
        elif result["status"] == "TIMEOUT":
            print(f"  TIMEOUT - {result['error']}")
        else:
            print("  UNKNOWN")
            print(str(result["output"])[:500])

    print(f"\n{'=' * 60}")
    print("TLC BATCH SUMMARY")
    print(f"{'=' * 60}")
    if args.no_tlc:
        print("  TLC execution skipped (--no-tlc).")
        return 0

    passes = sum(1 for _, result in results if result["status"] == "PASS")
    fails = sum(1 for _, result in results if result["status"] == "FAIL")
    unknown = sum(1 for _, result in results if result["status"] in {"UNKNOWN", "TIMEOUT"})
    print(f"  PASS:    {passes}")
    print(f"  FAIL:    {fails}")
    print(f"  UNKNOWN: {unknown}")
    print(f"  TOTAL:   {len(results)}")
    return 1 if fails or unknown else 0


if __name__ == "__main__":
    sys.exit(main())

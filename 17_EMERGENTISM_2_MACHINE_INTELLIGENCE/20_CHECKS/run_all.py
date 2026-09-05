#!/usr/bin/env python3
"""Run the entire Emergentism 2.0 instrument in one command.

Usage:
  python3 -B run_all.py          # human-readable (pipe-delimited)
  python3 -B run_all.py --json   # machine-parseable JSON

Exit 0 = all green. Exit 1 = any failure.
"""
import json, os, re, subprocess, sys

STACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKS = os.path.dirname(os.path.abspath(__file__))
os.chdir(CHECKS)

JSON_MODE = "--json" in sys.argv
results = []  # (name, ok, detail)

def check(name, ok, detail=""):
    results.append({"name": name, "pass": ok, "detail": detail})
    if not JSON_MODE:
        tag = "PASS" if ok else "FAIL"
        print(f"CHECK|{name}|{tag}" + (f"|{detail}" if detail and not ok else ""))

# 1 · Kernel JSON validity + structure
try:
    kernel = json.load(open(os.path.join(STACK, "10_KERNEL", "LENS.v0.json"), encoding="utf-8"))
    check("kernel_json_valid", True)
    nt = len(kernel.get("tenets", []))
    nd = len(kernel.get("defect_taxonomy", {}).get("defects", []))
    nk = len(kernel.get("kills", []))
    check("kernel_seven_tenets", nt == 7, f"got {nt}")
    check("kernel_ten_defects", nd == 10, f"got {nd}")
    check("kernel_kills_present", nk >= 5, f"got {nk}")
except Exception as e:
    check("kernel_json_valid", False, str(e))

# 2 · Test suite
r = subprocess.run([sys.executable, "-B", os.path.join(CHECKS, "test_adjudication.py")],
                   capture_output=True, text=True, cwd=CHECKS)
check("test_adjudication", r.returncode == 0,
      r.stderr[-200:] if r.returncode else "")

# 3 · All fixtures produce expected verdicts
expected = {
    "axis_mix.json": "AXIS_MIX",
    "constructionist.json": "KILLED",
    "credit_d5_ill_typed.json": "ILL_TYPED",
    "incomplete_mu.json": "INCOMPLETE",
    "l5_capital_axis_mix.json": "AXIS_MIX",
    "mind_d5_ill_typed.json": "ILL_TYPED",
    "noninvertible_as_strong.json": "KILLED",
    "slwp_reduced_wrap.json": "REDUCED",
}
for fname, want in sorted(expected.items()):
    path = os.path.join(CHECKS, "fixtures", fname)
    if not os.path.isfile(path):
        check(f"fixture_{fname}", False, "file missing")
        continue
    r = subprocess.run([sys.executable, "-B", os.path.join(CHECKS, "check_adjudication.py"),
                        "--check", path], capture_output=True, text=True)
    got = re.search(r"verdict=(\w+)", r.stdout)
    ok = bool(got and got.group(1) == want)
    check(f"fixture_{fname}", ok, f"expected {want}, got {got.group(1) if got else 'none'}")

# 4 · Ledger: exists, carries the founding kill
try:
    ledger = open(os.path.join(STACK, "00_ESTABLISHED.md"), encoding="utf-8").read()
    check("ledger_exists", True)
    check("ledger_founding_kill",
          "novel, positive, and ours" in ledger)
except Exception as e:
    check("ledger_exists", False, str(e))

# 5 · Direction fence in READ_FIRST
try:
    rf = open(os.path.join(STACK, "00_READ_FIRST.md"), encoding="utf-8").read()
    check("direction_fence",
          "never become evidence" in rf or "may never become evidence" in rf)
except Exception as e:
    check("direction_fence", False, str(e))

# Output
passed = sum(1 for r in results if r["pass"])
total = len(results)
if JSON_MODE:
    print(json.dumps({
        "instrument": "Emergentism 2.0",
        "version": "run_all v0",
        "passed": passed,
        "total": total,
        "all_green": passed == total,
        "checks": results,
    }, indent=2))
else:
    for r in results:
        tag = "PASS" if r["pass"] else "FAIL"
        line = f"CHECK|{r['name']}|{tag}"
        if r["detail"] and not r["pass"]:
            line += f"|{r['detail']}"
        print(line)
    print(f"\nINSTRUMENT|{passed}/{total}")

sys.exit(0 if passed == total else 1)

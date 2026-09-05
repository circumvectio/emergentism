#!/usr/bin/env python3
"""Run the entire Emergentism 2.0 instrument in one command.

Usage: python3 -B run_all.py
Exit 0 = all green. Exit 1 = any failure.
Machine-readable output: each check prints CHECK|name|PASS or CHECK|name|FAIL|detail.
"""
import json, os, re, subprocess, sys, glob

STACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKS = os.path.dirname(os.path.abspath(__file__))
os.chdir(CHECKS)
results = []

def check(name, ok, detail=""):
    results.append((name, ok, detail))
    tag = "PASS" if ok else "FAIL"
    print(f"CHECK|{name}|{tag}" + (f"|{detail}" if detail and not ok else ""))

# 1. Kernel JSON validity
try:
    kernel = json.load(open("../10_KERNEL/LENS.v0.json", encoding="utf-8"))
    check("kernel_json_valid", True)
    check("kernel_tenets", len(kernel.get("tenets", [])) == 7, f"got {len(kernel.get('tenets', []))}")
    check("kernel_defects", len(kernel.get("defect_taxonomy", {}).get("defects", [])) == 10,
          f"got {len(kernel.get('defect_taxonomy', {}).get('defects', []))}")
    check("kernel_kills", len(kernel.get("kills", [])) >= 5,
          f"got {len(kernel.get('kills', []))}")
except Exception as e:
    check("kernel_json_valid", False, str(e))

# 2. Test suite (absolute path — test_adjudication.py lives in CHECKS)
r = subprocess.run([sys.executable, "-B", os.path.join(CHECKS, "test_adjudication.py")],
                   capture_output=True, text=True, cwd=CHECKS)
check("test_adjudication", r.returncode == 0, r.stderr[-200:] if r.returncode else "")

# 3. All fixtures produce expected verdicts
fixture_dir = "fixtures"
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
    path = os.path.join(fixture_dir, fname)
    if not os.path.isfile(path):
        check(f"fixture_{fname}", False, "file missing")
        continue
    r = subprocess.run([sys.executable, "-B", "check_adjudication.py", "--check", os.path.abspath(path)],
                       capture_output=True, text=True)
    got = re.search(r"verdict=(\w+)", r.stdout)
    ok = got and got.group(1) == want
    check(f"fixture_{fname}", bool(ok), f"expected {want}, got {got.group(1) if got else 'none'}")

# 4. Ledger exists and carries the founding kill
ledger_path = "../00_ESTABLISHED.md"
try:
    ledger = open(ledger_path, encoding="utf-8").read()
    check("ledger_exists", True)
    check("ledger_kill",
          "novel, positive, and ours" in ledger and "dies if" in ledger.lower())
except Exception as e:
    check("ledger_exists", False, str(e))

# 5. Direction fence present in READ_FIRST
try:
    rf = open("../00_READ_FIRST.md", encoding="utf-8").read()
    check("direction_fence",
          "never become evidence" in rf or "may never become evidence" in rf)
except Exception as e:
    check("direction_fence", False, str(e))

# Summary
passed = sum(1 for _, ok, _ in results if ok)
total = len(results)
print(f"\nINSTRUMENT|{passed}/{total}")
sys.exit(0 if passed == total else 1)

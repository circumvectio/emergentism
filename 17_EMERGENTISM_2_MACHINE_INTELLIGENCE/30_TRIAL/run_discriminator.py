#!/usr/bin/env python3
"""MID-01 — the machine-intelligence discriminator.

Preregistered: 00_PREREG_DISCRIMINATOR_v0.md
Setup: MID01_SETUP_2026_09_05.md

Usage:
  python3 -B run_discriminator.py --arm lens    --session <session-id>
  python3 -B run_discriminator.py --arm plain   --session <session-id>
  python3 -B run_discriminator.py --arm checklist --session <session-id>
  python3 -B run_discriminator.py --grade       # after all three arms complete

Each arm invocation presents the corpus documents to the calling agent and
collects its findings. The grade step compares against the sealed key.
This script does NOT contact any MI — the orchestrator (caller) supplies
the intelligence. The script manages protocol, blinding, and grading.

Exit 0 = success. Exit 1 = protocol violation or grading complete with results.
"""
import argparse, hashlib, json, os, sys

TRIAL = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(TRIAL, "corpus")
ARMS_DIR = os.path.join(TRIAL, "arms")
SEALED = os.path.join(TRIAL, "sealed", "key.sha256")

ARMS = {"lens": None, "plain": None, "checklist": None}
ARM_INSTRUCTIONS = {
    "lens": (
        "Review these documents and report any problems. "
        "You have access to LENS.v0.json as your analytic framework."
    ),
    "plain": "Review these documents and report any problems.",
    "checklist": (
        "Review these documents and report any problems. Use this checklist:\n"
        "1. Check every number has a source or command that produces it\n"
        "2. Check every citation actually supports the claim it is attached to\n"
        "3. Check every conditional claim states its condition\n"
        "4. Check every measurement is dated and current\n"
        "5. Check every definition is used consistently\n"
        "6. Check every kill criterion could actually fire\n"
        "7. Check every proposal adds something the target lacks\n"
        "8. Check every claim carries its evidence tier\n"
        "9. Check every aggregate is derivable from its parts"
    ),
}

def sha256(data):
    import hashlib
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()

def list_corpus():
    docs = sorted(glob.glob(os.path.join(CORPUS, "*.md")))
    if not docs:
        print("ERROR: no corpus documents found in " + CORPUS)
        sys.exit(1)
    return docs

def cmd_arm(arm, session_id):
    instr = ARM_INSTRUCTIONS[arm]
    docs = list_corpus()
    out_dir = os.path.join(ARMS_DIR, f"{arm}_{session_id}")
    os.makedirs(out_dir, exist_ok=True)

    # Write the arm's instruction
    with open(os.path.join(out_dir, "INSTRUCTION.txt"), "w") as f:
        f.write(instr + "\n\n")
        f.write("Review each document below. For each, report:\n")
        f.write("- Document ID\n")
        f.write("- Line/section of the problem\n")
        f.write("- What the problem is\n")
        f.write("- Why it matters\n\n")

    for i, doc in enumerate(docs):
        doc_name = os.path.basename(doc)
        content = open(doc, encoding="utf-8").read()
        out_file = os.path.join(out_dir, f"doc_{i+1}_{doc_name}")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"<!-- DOCUMENT {i+1}: {doc_name} -->\n\n{content}\n")

    # Write the arm's output template
    with open(os.path.join(out_dir, "FINDINGS.md"), "w") as f:
        f.write(f"# {arm.upper()} arm findings — session {session_id}\n\n")
        f.write("Report findings per document. Format:\n")
        f.write("```\nDOC <number>\nLINE <approx line or section>\nISSUE <description>\n```\n\n")
        f.write("Findings:\n\n")

    print(f"ARM|{arm}|READY")
    print(f"  instruction: {instr[:80]}...")
    print(f"  documents: {len(docs)}")
    print(f"  output dir: {out_dir}")
    print(f"  next: the MI reviews the documents and writes FINDINGS.md")
    print(f"  then: run with --grade after all three arms complete")

def cmd_grade():
    # Check all three arms have findings
    arm_results = {}
    for arm in ("lens", "plain", "checklist"):
        arm_dirs = [d for d in os.listdir(ARMS_DIR) if d.startswith(arm + "_")]
        if not arm_dirs:
            print(f"GRADE|{arm}|MISSING — no session directory found")
            continue
        findings_file = os.path.join(ARMS_DIR, arm_dirs[0], "FINDINGS.md")
        if not os.path.isfile(findings_file):
            print(f"GRADE|{arm}|MISSING — FINDINGS.md not found")
            continue
        content = open(findings_file, encoding="utf-8").read()
        # Count findings (lines starting with DOC or ISSUE)
        doc_count = len(re.findall(r"(?m)^DOC \d+", content))
        issue_count = len(re.findall(r"(?m)^ISSUE ", content))
        arm_results[arm] = {"docs_reviewed": doc_count, "issues_reported": issue_count}

    if len(arm_results) < 3:
        print(f"GRADE|INCOMPLETE — only {len(arm_results)} of 3 arms have findings")
        sys.exit(1)

    # Compare (simplified — the sealed key comparison requires the experimenter)
    print("GRADE|RESULTS")
    for arm, data in sorted(arm_results.items()):
        print(f"  {arm}: {data['docs_reviewed']} docs, {data['issues_reported']} issues")

    print("\nNOTE: true-positive grading requires the sealed key (experimenter-held).")
    print("The grader must classify each reported issue as TP (planted defect found)")
    print("or FP (false positive on a clean sentence). The sealed key reveals which")
    print("sentences carry planted defects. This script manages protocol only.")

    lens = arm_results.get("lens", {}).get("issues_reported", 0)
    plain = arm_results.get("plain", {}).get("issues_reported", 0)
    checklist = arm_results.get("checklist", {}).get("issues_reported", 0)

    if lens > plain and lens > checklist:
        print("\nPRELIMINARY: LENS outperformed both controls on issue count.")
        print("True-positive grading against the sealed key determines the final verdict.")
    else:
        print("\nPRELIMINARY: LENS did NOT outperform both controls on raw issue count.")
        print("KILL condition may fire — grade true positives before concluding.")

def main():
    parser = argparse.ArgumentParser(description="MID-01 discriminator")
    parser.add_argument("--arm", choices=list(ARMS.keys()))
    parser.add_argument("--grade", action="store_true")
    parser.add_argument("--session", default="default")
    args = parser.parse_args()

    if not os.path.isfile(SEALED):
        print("ERROR: sealed key not found at " + SEALED)
        print("Run the setup first (see MID01_SETUP_2026_09_05.md)")
        sys.exit(1)

    if args.grade:
        cmd_grade()
    elif args.arm:
        cmd_arm(args.arm, args.session)
    else:
        parser.print_help()

if __name__ == "__main__":
    import re
    main()

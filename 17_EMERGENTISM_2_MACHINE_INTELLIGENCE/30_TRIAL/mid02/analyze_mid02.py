#!/usr/bin/env python3
"""MID-02 analyzer — grades arm outputs against the sealed key.

Frozen before any grading (committed with hash before arm outputs are read).
Inputs: sealed/key.json, outputs/<CODE>.json (A/B/C).
Scoring:
  detection  = planted defects found (type+doc match) / 10 total
  fp         = findings typed as a kernel defect but matching no planted
               defect for that doc (excluding corrections-channel items)
  typing     = per-doc: family exact (1), any operation keyword (1),
               tier exact (1) -> 15 points over 5 docs
  corrections= self-flaw caught (keyword "92% precision" or "214 adjudication")
Usage: python3 analyze_mid02.py outputs/A.json outputs/B.json outputs/C.json
"""
import json, re, sys

KEY = json.load(open("sealed/key.json"))
PLANTED = KEY["planted_defects"]
TYPING = KEY["typing_targets"]

def grade(path):
    out = json.load(open(path))
    docs = set(PLANTED) | {t["doc"] for t in out.get("typing", [])}
    det, tp, fp = 0, set(), 0
    for f in out.get("findings", []):
        doc, ftype = f.get("doc", ""), f.get("type", "")
        planted_types = {p["type"] for p in PLANTED.get(doc, [])}
        if ftype in planted_types:
            if (doc, ftype) not in tp:
                tp.add((doc, ftype)); det += 1
        elif ftype != "other":
            fp += 1
    typ = 0; typ_detail = {}
    for t in out.get("typing", []):
        doc = t.get("doc", "")
        if doc not in TYPING: continue
        k = TYPING[doc]
        fam = 1 if k["family"].lower() in str(t.get("family", "")).lower() else 0
        op = 1 if any(w in str(t.get("operation", "")).lower() for w in k["operation_keywords"]) else 0
        tier = 1 if k["tier"].lower() in str(t.get("tier", "")).lower() else 0
        typ += fam + op + tier
        typ_detail[doc] = {"family": fam, "operation": op, "tier": tier}
    blob = json.dumps(out).lower()
    corr = 1 if ("92% precision" in blob or "214 adjudication" in blob) else 0
    return {"path": path, "detection": f"{det}/10", "detection_n": det,
            "false_positives": fp, "typing": f"{typ}/15",
            "self_flaw_caught": bool(corr),
            "arm_note": out.get("arm_note", "")[:160]}

rows = [grade(p) for p in sys.argv[1:]]
rows.sort(key=lambda r: (-r["detection_n"], r["false_positives"]))
for r in rows:
    print(json.dumps(r, ensure_ascii=False))
print("TOTALS:", json.dumps({r["path"].split("/")[-1]: r["detection_n"] for r in rows}))

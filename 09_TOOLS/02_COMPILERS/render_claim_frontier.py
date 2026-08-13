#!/usr/bin/env python3
"""Render the claim-status frontier for /record/.

This is a deterministic projection of CLAIM_STATUS.yaml. It does not harvest
the whole tree, does not invent last-movers, does not score reach, and does
not say the ontology will be completed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "00_META/claim_status/CLAIM_STATUS.yaml"
OUT_JSON = ROOT / "12_PUBLIC_SITE/record/frontier.json"
OUT_HTML = ROOT / "12_PUBLIC_SITE/record/frontier/index.html"
BUCKETS = ("validated", "open", "reopened", "investigations", "restored", "typed_survivors", "graves")


def _text(*parts: object) -> str | None:
    bits = [str(p).strip() for p in parts if p not in (None, "", [], {})]
    return " ".join(bits) or None


def _contracts(row: dict) -> list[dict]:
    disp = row.get("disposition") or {}
    return [c for c in disp.get("contracts") or [] if isinstance(c, dict)]


def project(row: dict, bucket: str) -> dict:
    contracts = _contracts(row)
    first = contracts[0] if contracts else {}
    kill = _text(row.get("kill"), row.get("counterexample"), first.get("kill"))
    raise_it = _text(row.get("discriminator"), first.get("discriminator"), row.get("repair_path"))
    statement = _text(
        row.get("result"),
        row.get("question"),
        row.get("claim"),
        row.get("form"),
        row.get("note"),
    )
    if bucket == "graves":
        raise_it = "Forbidden. Graves do not thaw. A weaker successor needs its own ID."
    if bucket == "validated" and not raise_it:
        raise_it = "Already formally valid inside the declared system. A raise would be a category error."
    return {
        "id": row.get("id"),
        "bucket": bucket,
        "status": row.get("status"),
        "tier": row.get("tier"),
        "statement": statement,
        "raise": raise_it,
        "kill": kill,
        "survivor": _text(row.get("survivor"), first.get("survivor"), row.get("inherits")),
        "owner": _text(
            row.get("owner"),
            (row.get("disposition") or {}).get("claim_owner"),
            first.get("protocol_owner"),
        ),
        "last_move": row.get("last_move") if isinstance(row.get("last_move"), dict) else None,
        "last_move_note": (
            None
            if isinstance(row.get("last_move"), dict)
            else "CLAIM_STATUS.yaml does not record who moved this row or when. Unrecorded, not invented."
        ),
        "successor": row.get("successor"),
        "parent": row.get("parent"),
    }


def render_html(payload: dict) -> str:
    rows = payload["claims"]
    items = []
    for row in rows:
        items.append(
            "<article>"
            f"<p class='id'>{row['id']} <span>{row['bucket']} · {row['status']}"
            f"{' · ['+str(row['tier'])+']' if row.get('tier') else ''}</span></p>"
            f"<p>{row.get('statement') or ''}</p>"
            f"<p><b>Raise.</b> {row.get('raise') or 'unrecorded'}</p>"
            f"<p><b>Kill.</b> {row.get('kill') or 'unrecorded'}</p>"
            f"<p class='meta'>last move: "
            f"{(row.get('last_move') or {}).get('date', 'unrecorded') if isinstance(row.get('last_move'), dict) else 'unrecorded'}"
            f" · owner: {row.get('owner') or 'unrecorded'}</p>"
            "</article>"
        )
    body = "\n".join(items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontier ledger — Emergentism</title>
<meta name="description" content="Every row in CLAIM_STATUS.yaml: status, raise, kill. Not a complete ontology. Not a reach score. World contact 0.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://emergentism.org/record/frontier/">
<style>
body{{margin:0;background:#070A12;color:#F5F0E6;font:17px/1.55 -apple-system,BlinkMacSystemFont,sans-serif}}
main{{max-width:46rem;margin:0 auto;padding:2rem 1.2rem 4rem}}
.kicker{{font:500 .72rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;color:#F0C85A}}
.fence{{border:1px solid rgba(240,200,90,.35);padding:.85rem 1rem;margin:1rem 0 2rem;color:#C0C1C5;font-size:.92rem}}
article{{border-top:1px solid rgba(245,240,230,.12);padding:1rem 0}}
.id{{font:600 .78rem ui-monospace,Menlo,monospace;color:#F0C85A}}
.id span{{color:#959CAB;font-weight:500}}
.meta{{font:500 .74rem ui-monospace,Menlo,monospace;color:#959CAB}}
a{{color:#79A8FF}}
</style>
</head>
<body>
<main>
<p class="kicker">Record · frontier, not finish</p>
<h1>Frontier ledger</h1>
<div class="fence">
  Projection of <code>CLAIM_STATUS.yaml</code> only — {payload['counts']['total']} rows.
  A kill is a move. Reach is not a term. This is not a complete ontology and
  will not become one by filling the table. World contact accepted:
  <strong>0</strong>. Machine copy:
  <a href="/record/frontier.json">frontier.json</a>.
</div>
<noscript><p>Read the JSON. The ledger does not need this page.</p></noscript>
{body}
<p><a href="/record/">graves / trial record</a> ·
<a href="/record/problems/">typed holes</a> ·
<a href="/exit/">exit</a></p>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    claims = []
    for bucket in BUCKETS:
        for row in source.get(bucket) or []:
            if isinstance(row, dict) and row.get("id"):
                claims.append(project(row, bucket))
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    payload = {
        "schema": "emergentism/frontier-ledger/v0",
        "status": "STAGED [D] — rendering of the validation register, not a result",
        "source": "00_META/claim_status/CLAIM_STATUS.yaml",
        "source_sha256": digest,
        "k_star": 0,
        "attention_capture": False,
        "completeness_claim": False,
        "world_contact_accepted": 0,
        "score": "tier movement against stated kill criteria only; a kill counts; reach does not",
        "not": [
            "a complete ontology",
            "a promise that the frontier will close",
            "a reach or spread metric",
            "world contact",
            "Amrita emerged",
        ],
        "counts": {
            "validated": len(source.get("validated") or []),
            "open": len(source.get("open") or []),
            "investigations": len(source.get("investigations") or source.get("reopened") or []),
            "typed_survivors": len(source.get("typed_survivors") or source.get("restored") or []),
            "graves": len(source.get("graves") or []),
            "total": len(claims),
        },
        "claims": claims,
    }
    html = render_html(payload)
    if args.check:
        live = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        if live != payload or OUT_HTML.read_text(encoding="utf-8") != html:
            print("FRONTIER: FAIL drift")
            return 1
        print(f"FRONTIER: PASS ({payload['counts']['total']} rows; no completeness; world contact 0)")
        return 0
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"FRONTIER: wrote {payload['counts']['total']} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

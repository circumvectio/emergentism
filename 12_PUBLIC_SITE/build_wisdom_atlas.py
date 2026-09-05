#!/usr/bin/env python3
"""Build the source-bound Public Wisdom pages and machine atlas."""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
from typing import Any

from build_core_shell import render_page


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
SOURCE = ROOT / "14_THE_DISTILLATION" / "09_PUBLIC_WISDOM"
SOURCE_BUILDER = SOURCE / "build_public_wisdom.py"


def pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def load_source() -> tuple[dict[str, Any], dict[str, Any]]:
    spec = importlib.util.spec_from_file_location("emergentism_public_wisdom", SOURCE_BUILDER)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load Public Wisdom source compiler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bundle = module.load_and_validate(verify_git=True)
    compiled = module.compile_corpus(bundle)
    expected = module.pretty(compiled)
    actual = (SOURCE / "PublicWisdomCorpus.v1.json").read_text(encoding="utf-8")
    if actual != expected:
        raise ValueError("source PublicWisdomCorpus.v1.json is stale")
    return bundle, compiled


def page(title: str, description: str, body: str, *, active: str, href: str, surface: str) -> str:
    raw = f'''<!doctype html>
<html lang="en" data-gestalt="v2" data-emergentism-design="v2">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}" />
  <link rel="canonical" href="https://emergentism.org{href}" />
<!--OG:AUTO-->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:title" content="{html.escape(title, quote=True)}" />
<meta property="og:description" content="{html.escape(description, quote=True)}" />
<meta property="og:url" content="https://emergentism.org{href}" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<!--/OG:AUTO-->
</head>
<body class="g2-page" data-emergentism-surface="{html.escape(surface)}">
<main id="main" tabindex="-1">{body}</main>
</body>
</html>
'''
    return render_page(raw, active=active, current_href=href, surface=surface)


def stack_markup(stack: dict[str, Any], *, detailed: bool) -> str:
    items = []
    for stage in stack["stages"]:
        detail = stage["object_definition"] if detailed else stage["object_definition"].split(";")[0]
        items.append(
            f'<li><strong>{html.escape(stage["name"])}</strong>'
            f'<small>{html.escape(detail)}</small></li>'
        )
    return '<ol class="g2-promotion-rail" aria-label="Signal to Wisdom promotion ladder">' + "".join(items) + "</ol>"


def application_markup(cards: list[dict[str, Any]]) -> str:
    rows = []
    for card in cards:
        rows.append(f'''
<article class="g2-application-card" data-state="{html.escape(card['coverage_state'])}">
  <span class="g2-claim-id">{html.escape(card['coverage_state'].replace('_', ' '))} · {html.escape(card['evidence_tier'])}</span>
  <h3>{html.escape(card['name'])}</h3>
  <p>{html.escape(card['candidate_application'])}</p>
  <p><strong>Adoption:</strong> {html.escape(card['adoption_state'].replace('_', ' ').lower())}</p>
</article>''')
    return '<div class="g2-application-grid">' + "".join(rows) + "</div>"


def wisdom_index(bundle: dict[str, Any], compiled: dict[str, Any]) -> str:
    stack = bundle["stack"]
    cards = bundle["cards"]
    counts = compiled["counts"]
    body = f'''
<section class="g2-shell g2-wisdom-hero" aria-labelledby="wisdom-title">
  <div><p class="g2-kicker">The Public Wisdom Instrument · local candidate</p><h1 id="wisdom-title">Ideas do not become wisdom by being repeated.</h1><p class="g2-hero__lede">They climb by typed promotion, consequence, correction, and accountable policy. Publicity sits beside that ladder: it changes visibility, never truth.</p><div class="g2-actions"><a class="g2-button g2-button--primary" href="#promotion">Follow the promotion</a><a class="g2-action-link" href="/record/wisdom/">Inspect the source record</a></div></div>
  <aside class="g2-wisdom-hero__state" aria-label="Current Public Wisdom state"><span>current honest state</span><strong>0 supported</strong><small>1 Provisional · 1 AUTHORIZED_NOT_LIT · 0 independent outcomes</small></aside>
</section>
<section class="g2-shell g2-section" id="promotion" aria-labelledby="promotion-title">
  <div class="g2-section__head"><div><p class="g2-eyebrow">01 · Promotion</p><h2 id="promotion-title">Signal → Data → Information → Knowledge → Judgment → Wisdom</h2></div><p class="g2-section__intro">Each crossing creates a new addressable object or receipt. A label cannot perform the crossing.</p></div>
  <div class="g2-promotion-instrument">{stack_markup(stack, detailed=False)}<aside class="g2-public-lamp"><span>orthogonal projection</span><strong>Public</strong><p>Public is a separate lighting event, not a higher truth rung.</p></aside></div>
  <p class="g2-note"><strong>Nothing promotes itself.</strong> A commit, receipt, publication event, model consensus, or polished interface supplies no automatic maturity upgrade.</p>
</section>
<section class="g2-shell g2-section" id="compact" aria-labelledby="compact-title">
  <div class="g2-section__head"><div><p class="g2-eyebrow">02 · Compact</p><h2 id="compact-title">Four sentences for public reasoning.</h2></div><p class="g2-section__intro">A chosen Emergentism editorial policy `[D]`, not a law of nature or product mandate.</p></div>
  <div class="g2-compact-block"><blockquote>Keep possibility wide. Make commitment accountable. Nothing promotes itself. Reality retains the right to correct every map.</blockquote><dl class="g2-wisdom-ledger"><div><dt>Supported wisdom</dt><dd>{compiled['supported_wisdom']}</dd></div><div><dt>Provisional</dt><dd>{counts['maturity']['PROVISIONAL']}</dd></div><div><dt>Projection</dt><dd>AUTHORIZED_NOT_LIT</dd></div></dl></div>
  <div class="g2-actions"><a class="g2-button" href="/wisdom/EM-WISDOM-001@1/">Open all seven clauses</a><a class="g2-action-link" href="/record/wisdom/">Audit the denominator</a></div>
</section>
<section class="g2-shell g2-section" id="applications" aria-labelledby="applications-title">
  <div class="g2-section__head"><div><p class="g2-eyebrow">03 · Applications</p><h2 id="applications-title">One admitted local use. Seven source-owned candidates.</h2></div><p class="g2-section__intro">No product has adopted this Compact. Candidate readings create no product semantics, authority, runtime state, or outcome.</p></div>
  {application_markup(cards)}
  <p class="g2-note"><strong>Coverage:</strong> 17 estate lanes · 1 admitted Emergentism application · 7 candidate-only · 9 honest absences · zero unclassified.</p>
</section>
<section class="g2-shell g2-section g2-exit-band" aria-labelledby="return-title"><div><p class="g2-eyebrow">04 · Return</p><h2 id="return-title">Publication begins another correction loop.</h2><p>Reach is not truth. The source, rival, kill, correction path, and Exit remain visible after lighting.</p></div><div class="g2-actions"><a class="g2-button g2-button--primary" href="/record/wisdom/">Inspect the record</a><a class="g2-button" href="/contribute/">Contest or contribute</a><a class="g2-action-link" href="/exit/">Exit</a></div></section>
'''
    return page(
        "Public Wisdom Instrument — Emergentism",
        "A source-bound promotion ladder from Signal to Wisdom, with Public kept separate from truth.",
        body,
        active="wisdom",
        href="/wisdom/",
        surface="wisdom",
    )


def dossier(bundle: dict[str, Any], compiled: dict[str, Any]) -> str:
    record = bundle["records"][0]
    clauses = "".join(f"<li>{html.escape(clause)}</li>" for clause in record["clauses"])
    rivals = "".join(f"<li>{html.escape(item)}</li>" for item in record["rivals"])
    kills = "".join(f"<li>{html.escape(item)}</li>" for item in record["kill_criteria"])
    body = f'''
<section class="g2-shell g2-wisdom-hero" aria-labelledby="record-title"><div><p class="g2-kicker">{html.escape(record['stable_id'])} · {html.escape(record['evidence_tier'])}</p><h1 id="record-title">{html.escape(record['title'])}</h1><p class="g2-hero__lede">{html.escape(record['public_digest'])}</p></div><aside class="g2-wisdom-hero__state"><span>{html.escape(record['kind'])}</span><strong>{html.escape(record['maturity'])}</strong><small>{html.escape(record['projection'])} · independent outcomes {len(record['outcomes'])}</small></aside></section>
<section class="g2-shell g2-section" aria-labelledby="clauses-title"><div class="g2-section__head"><div><p class="g2-eyebrow">01 · Policy form</p><h2 id="clauses-title">Seven clauses. Every one remains correctable.</h2></div><p class="g2-section__intro">Scope: {html.escape(record['scope'])}.</p></div><ol class="g2-clause-list">{clauses}</ol></section>
<section class="g2-shell g2-section" aria-labelledby="debt-title"><div class="g2-section__head"><div><p class="g2-eyebrow">02 · Explanatory debt</p><h2 id="debt-title">A policy is useful only while its rivals and kills stay live.</h2></div></div><div class="g2-practice-grid"><article class="g2-panel g2-panel--possible"><h3>Strongest rivals</h3><ul>{rivals}</ul></article><article class="g2-panel g2-panel--conjecture"><h3>Kill criteria</h3><ul>{kills}</ul></article></div></section>
<section class="g2-shell g2-section" aria-labelledby="authority-title"><div class="g2-section__head"><div><p class="g2-eyebrow">03 · Authority</p><h2 id="authority-title">Local editorial scope only.</h2></div><p class="g2-section__intro">Bearer: {html.escape(record['authority']['bearer'])}. It may bind no product, sign nothing, and authorize no external act.</p></div><p class="g2-note"><strong>State:</strong> locally authorized for an Emergentism candidate; not lit, externally validated, product-adopted, or Supported.</p><div class="g2-actions"><a class="g2-button g2-button--primary" href="/record/wisdom/">Inspect source custody</a><a class="g2-action-link" href="/wisdom/">Return to the instrument</a></div></section>
'''
    return page(
        f"{record['title']} — Emergentism",
        record["public_digest"],
        body,
        active="wisdom",
        href=f"/wisdom/{record['stable_id']}/",
        surface="wisdom",
    )


def record_page(bundle: dict[str, Any], compiled: dict[str, Any], corpus_sha: str) -> str:
    coverage = compiled["counts"]["coverage"]
    body = f'''
<section class="g2-shell g2-wisdom-hero" aria-labelledby="record-title"><div><p class="g2-kicker">Source record · PUBLIC-WISDOM-2026-09-01 · [D]</p><h1 id="record-title">What the instrument can—and cannot—claim.</h1><p class="g2-hero__lede">This is a local deterministic projection of committed source bytes. It is not an outcome, external validation, deployment receipt, product adoption, or proof of Emergentism.</p></div><aside class="g2-wisdom-hero__state"><span>source package</span><strong>13 tests</strong><small>8 cards · 17 lanes · 0 Supported</small></aside></section>
<section class="g2-shell g2-section" aria-labelledby="state-title"><div class="g2-section__head"><div><p class="g2-eyebrow">01 · State vector</p><h2 id="state-title">The zeroes are part of the result.</h2></div></div><dl class="g2-wisdom-ledger"><div><dt>Supported</dt><dd>{compiled['supported_wisdom']}</dd></div><div><dt>Independent outcomes</dt><dd>{compiled['external_states']['independent_outcomes']}</dd></div><div><dt>Product adoptions</dt><dd>{compiled['external_states']['product_adoptions']}</dd></div></dl><p class="g2-note">Coverage: {coverage['ADMITTED_APPLICATION']} admitted · {coverage['CANDIDATE_ONLY']} candidate-only · {coverage['NO_ADMISSIBLE_RECORD']} no admissible record · zero unclassified.</p></section>
<section class="g2-shell g2-section" aria-labelledby="custody-title"><div class="g2-section__head"><div><p class="g2-eyebrow">02 · Custody</p><h2 id="custody-title">Exact source ancestry, machine-readable.</h2></div><p class="g2-section__intro">The source compiler accepts only named committed Git blobs and rejects working-tree, replay-carrier, and consensus substitutions.</p></div><p class="g2-source-digest">PublicWisdomCorpus.v1.json · sha256:{corpus_sha}<br />source manifest · sha256:{compiled['source_manifest_sha256']}<br />record · EM-WISDOM-001@1 · PROVISIONAL · AUTHORIZED_NOT_LIT</p><div class="g2-actions"><a class="g2-button g2-button--primary" href="/wisdom/atlas.json">Open atlas.json</a><a class="g2-button" href="/wisdom/atlas.jsonl">Open atlas.jsonl</a><a class="g2-button" href="/wisdom/rag.jsonl">Open retrieval chunks</a></div></section>
<section class="g2-shell g2-section" aria-labelledby="boundary-title"><div class="g2-section__head"><div><p class="g2-eyebrow">03 · Release boundary</p><h2 id="boundary-title">OFFLINE-READY is not public.</h2></div><p class="g2-section__intro">No push, deploy, DNS change, model evaluation, external adoption, independent outcome, or external validation is represented by these local bytes.</p></div><div class="g2-actions"><a class="g2-button" href="/wisdom/">Read the human projection</a><a class="g2-action-link" href="/record/">Return to the Trial Record</a></div></section>
'''
    return page(
        "Public Wisdom Record — Emergentism",
        "The source, counts, and release boundary behind the Public Wisdom Instrument.",
        body,
        active="research",
        href="/record/wisdom/",
        surface="research",
    )


def machine_outputs(bundle: dict[str, Any], compiled: dict[str, Any]) -> dict[Path, str]:
    # Metadata only: never copy private source bodies into a public projection.
    manifest = bundle["manifest"]
    repositories = {row["repo_id"]: row for row in manifest["repositories"]}
    sources = {row["source_id"]: row for row in manifest["sources"]}

    def provenance(source_ids: list[str], artifact: str, hash_key: str) -> dict[str, Any]:
        return {
            "source_manifest_sha256": compiled["source_manifest_sha256"],
            "source_artifact": {
                "path": (SOURCE / "data" / artifact).relative_to(ROOT).as_posix(),
                "sha256": compiled["input_hashes"][hash_key],
            },
            "source_ids": source_ids,
            "source_refs": [
                {**sources[source_id], "repository": repositories[sources[source_id]["repo_id"]]}
                for source_id in source_ids
            ],
        }

    atlas = {
        "schema_id": "emergentism/PublicWisdomAtlas.v1",
        "release_id": compiled["release_id"],
        "boundary": {
            "public_is_truth_rung": False,
            "public_changes_visibility_only": True,
            "nothing_promotes_itself": True,
        },
        "counts": compiled["counts"],
        "supported_wisdom": compiled["supported_wisdom"],
        "external_states": compiled["external_states"],
        "source_manifest": manifest,
        "source_manifest_sha256": compiled["source_manifest_sha256"],
        "input_hashes": compiled["input_hashes"],
        "stack": bundle["stack"],
        "records": bundle["records"],
        "application_cards": bundle["cards"],
        "coverage_ledger": bundle["ledger"],
    }
    rows: list[dict[str, Any]] = [{"kind": "atlas", "value": {k: atlas[k] for k in ("schema_id", "release_id", "boundary", "counts", "supported_wisdom", "external_states", "source_manifest", "source_manifest_sha256", "input_hashes")}}]
    rows += [{"kind": "stage", "value": row} for row in bundle["stack"]["stages"]]
    rows += [{"kind": "promotion", "value": row} for row in bundle["stack"]["promotions"]]
    rows += [{"kind": "wisdom_record", "value": row} for row in bundle["records"]]
    rows += [{"kind": "application_card", "value": row} for row in bundle["cards"]]
    rows += [{"kind": "coverage_lane", "value": row} for row in bundle["ledger"]["entries"]]
    jsonl = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    record = bundle["records"][0]
    rag_rows = [
        {
            "id": "PUBLIC-WISDOM-COMPACT", "record_id": record["stable_id"],
            "title": "The Public Wisdom Compact", "text": record["compression"],
            "route": f'/wisdom/{record["stable_id"]}/',
            **{key: record[key] for key in ("kind", "maturity", "projection", "evidence_tier", "scope", "authority")},
            **provenance(record["source_ids"], "public_wisdom_records.v1.json", "records_sha256"),
        },
        {
            "id": "PUBLIC-WISDOM-BOUNDARY", "kind": "stack_boundary",
            "title": "Public is orthogonal",
            "text": "Public is a separate lighting event, not a higher truth rung. Nothing promotes itself.",
            "route": "/wisdom/", "scope": bundle["stack"]["scope"],
            **provenance([], "emergence_stack.v1.json", "stack_sha256"),
        },
    ]
    rag_rows.extend({
        "id": card["stable_id"], "kind": "application_card",
        "title": card["name"], "text": card["candidate_application"], "route": "/wisdom/#applications",
        **{key: card[key] for key in ("coverage_state", "application_status", "adoption_state", "evidence_tier", "authority_effect", "may_sign", "may_authorize")},
        **provenance(card["source_ids"], "estate_application_cards.v1.json", "cards_sha256"),
    } for card in bundle["cards"])
    rag = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rag_rows)
    return {
        SITE / "wisdom" / "atlas.json": pretty(atlas),
        SITE / "wisdom" / "atlas.jsonl": jsonl,
        SITE / "wisdom" / "rag.jsonl": rag,
    }


def outputs() -> dict[Path, str]:
    bundle, compiled = load_source()
    source_bytes = (SOURCE / "PublicWisdomCorpus.v1.json").read_bytes()
    corpus_sha = hashlib.sha256(source_bytes).hexdigest()
    rendered = machine_outputs(bundle, compiled)
    rendered[SITE / "wisdom" / "index.html"] = wisdom_index(bundle, compiled)
    rendered[SITE / "wisdom" / "EM-WISDOM-001@1" / "index.html"] = dossier(bundle, compiled)
    rendered[SITE / "record" / "wisdom" / "index.html"] = record_page(bundle, compiled, corpus_sha)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on byte drift")
    args = parser.parse_args()
    try:
        rendered = outputs()
    except (OSError, ValueError) as exc:
        print(f"PUBLIC WISDOM ATLAS: FAIL\n- {exc}")
        return 1
    drift = []
    for path, content in rendered.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(SITE).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("PUBLIC WISDOM ATLAS: FAIL")
        for rel in drift:
            print(f"- drift: {rel}")
        return 1
    print(f"PUBLIC WISDOM ATLAS: PASS ({len(rendered)} artifacts; {'clean' if args.check else 'rendered'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

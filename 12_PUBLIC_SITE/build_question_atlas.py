#!/usr/bin/env python3
"""Build the public PQA-54 question atlas and its null-state record page."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from build_core_shell import render_page


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PACKAGE = ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "pqa_54"
ATLAS_PATH = PACKAGE / "prompts" / "questions.json"
PROJECTION_PATH = PACKAGE / "public_projection.json"
OUTPUTS = {
    SITE / "questions" / "index.html": "questions",
    SITE / "record" / "pqa-54" / "index.html": "record",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_document(*, title: str, description: str, canonical: str, main: str, active: str) -> str:
    base = f'''<!doctype html>
<html lang="en" data-gestalt="v2">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="theme-color" content="#07090f" />
  <link rel="canonical" href="{esc(canonical)}" />
  <link rel="stylesheet" href="/assets/css/gestalt-v2.css" />
  <script defer src="/assets/js/gestalt-v2.js"></script>
<!--OG:AUTO-->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:url" content="{esc(canonical)}" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<!--/OG:AUTO-->
</head>
<body class="g2-page">
<main id="main" class="g2-main" tabindex="-1">
{main}
</main>
</body>
</html>
'''
    return render_page(base, active)


def validate_inputs(atlas: dict, projection: dict) -> None:
    domains = atlas.get("domains")
    if not isinstance(domains, list) or len(domains) != 9:
        raise ValueError("PQA atlas must contain nine domains")
    rows = [question for domain in domains for question in domain.get("questions", [])]
    if len(rows) != 54 or len({row.get("question_id") for row in rows}) != 54:
        raise ValueError("PQA atlas must contain 54 unique questions")
    null = {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}
    if atlas.get("launch_counts") != null or projection.get("counts") != null:
        raise ValueError("PQA public launch counts must remain 54/0/0/0")
    if projection.get("deployed") is not False or projection.get("external_validation") is not False:
        raise ValueError("offline PQA projection cannot claim deployment or external validation")


def question_atlas_main(atlas: dict) -> str:
    domain_sections: list[str] = []
    for index, domain in enumerate(atlas["domains"], start=1):
        questions = "\n".join(
            f'''        <li class="g2-question" data-question-id="{esc(row['question_id'])}">
          <span class="g2-question__meta">{esc(row['question_id'])} · {esc(row['family'])} · {esc(row['split'])}</span>
          <h3>{esc(row['prompt'])}</h3>
          <p><strong>Native target:</strong> {esc(row['native_problem'])}</p>
          <p class="g2-question__source"><strong>Native anchor:</strong> {esc(row['native_reference'])}</p>
        </li>'''
            for row in domain["questions"]
        )
        domain_sections.append(
            f'''  <section class="g2-shell g2-section g2-question-domain" id="domain-{esc(domain['code'].lower())}" aria-labelledby="domain-{esc(domain['code'].lower())}-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">{index:02d} · {esc(domain['code'])}</p><h2 id="domain-{esc(domain['code'].lower())}-title">{esc(domain['name'])}</h2></div><p class="g2-section__intro">Six selected question families. Selection is a benchmark construct, not a philosophical result.</p></div>
    <ol class="g2-question-grid">
{questions}
    </ol>
  </section>'''
        )
    return f'''  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">Question Atlas · PQA-54 · public denominator</p>
    <h1>Fifty-four questions. None quietly counted as solved.</h1>
    <p class="g2-page-hero__lede">Emergentism does not end philosophy. It makes philosophical debt legible—and tests whether an exact type distinction clarifies, dissolves within a model, conditionally resolves, reframes, or leaves each question open.</p>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="#domain-met">Open the atlas</a><a class="g2-button" href="/record/pqa-54/">Read the protocol state</a><a class="g2-button" href="/ethics/">Inspect the normative bridge</a></div>
    <div class="g2-page-meta"><span>[D] selected construct</span><span>54 selected</span><span>0 evaluated</span><span>0 independently reviewed</span><span>0 resolved</span></div>
  </header>

  <nav class="g2-shell g2-atlas-nav" aria-label="Question Atlas sections">
    {''.join(f'<a href="#domain-{esc(row["code"].lower())}">{esc(row["code"])} <small>{esc(row["name"])}</small></a>' for row in atlas['domains'])}
  </nav>

  <section class="g2-shell g2-section" aria-labelledby="reading-rule-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Reading rule</p><h2 id="reading-rule-title">Inventory is not evaluation.</h2></div><p class="g2-section__intro">Every question begins open.</p></div>
    <div class="g2-practice-grid"><article class="g2-panel"><span class="g2-claim-id">Native recovery</span><h3>State the problem before translating it.</h3><p>The native terms, premises, established result, and strongest native rival must remain visible.</p></article><article class="g2-panel"><span class="g2-claim-id">Typed effect</span><h3>Clarification is not resolution.</h3><p>Formal correction, type dissolution, conditional resolution, practical guidance, and refutation remain distinct.</p></article><article class="g2-panel"><span class="g2-claim-id">Residual debt</span><h3>What remains open stays on the page.</h3><p>A renamed question, deleted premise, changed subject, or hidden residual earns no dissolution.</p></article></div>
    <p class="g2-note">A bounded majority would require 28 of 54 qualifying results, at least three per domain, two independent native-domain reviews per result, no live kill, and incremental value over both native-frame and generic-decomposition controls. Even that would not mean “most philosophy.”</p>
  </section>

{chr(10).join(domain_sections)}

  <section class="g2-shell g2-section" aria-labelledby="atlas-exit-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Exit and challenge</p><h2 id="atlas-exit-title">The denominator is public so the framework can lose.</h2></div><p class="g2-section__intro">No belief or participation is required.</p></div>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="/record/pqa-54/">Audit PQA-54</a><a class="g2-button" href="/discoveries/paradoxes/">See the earlier paradox ledger</a><a class="g2-button" href="/exit/">Take the Exit</a></div>
  </section>'''


def record_main() -> str:
    return '''  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">Research record · PQA-54 v0.1</p>
    <h1>The Philosophical Question Atlas companion</h1>
    <p class="g2-page-hero__lede">PQA-54 tests whether a candidate can recover a question in its native terms, expose exact type defects, preserve residual debt, survive serious rivals, and revise after contact.</p>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="/questions/">Read all 54 questions</a><a class="g2-button" href="/record/eub-1/">Dasein Test · EUB-1</a><a class="g2-button" href="/contribute/">Challenge the construct</a></div>
    <div class="g2-page-meta"><span>OFFLINE-READY · [D]</span><span>companion only</span><span>network refused by default</span></div>
  </header>

  <section class="g2-shell g2-section" aria-labelledby="pqa-state-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">01 · Exact launch state</p><h2 id="pqa-state-title">54 selected · 0 evaluated · 0 independently reviewed · 0 resolved</h2></div><p class="g2-section__intro">The selected atlas is a construct `[D]`, not a performance result.</p></div>
    <p class="g2-note">No candidate model has run. No native philosopher has reviewed a result. No question has earned clarification, dissolution, conditional resolution, or refutation. Local tests establish only that the contracts and synthetic fixtures behave as declared.</p>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="pqa-method-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">02 · Five phases</p><h2 id="pqa-method-title">Formulate → Attack → Discriminate → Contact → Revise and transfer</h2></div><p class="g2-section__intro">Only the public account, typed propositions, predictions, and revision ledger are scored.</p></div>
    <div class="g2-definition-list"><dt>Formulate</dt><dd>Recover the native target before applying Emergentism.</dd><dt>Attack</dt><dd>Introduce a serious native rival, a generic/null rival, and provenance poison.</dd><dt>Discriminate</dt><dd>Name the exact collision, conservative repair, prediction, kill, and survivor.</dd><dt>Contact</dt><dd>Reveal a counterexample or review challenge and require explicit correction.</dd><dt>Revise and transfer</dt><dd>Preserve stable claim IDs and transfer to a relabelled neighboring problem.</dd></div>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="pqa-effects-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">03 · Effects stay typed</p><h2 id="pqa-effects-title">A useful answer can leave the question open.</h2></div><p class="g2-section__intro">No scalar worldview leaderboard is produced.</p></div>
    <div class="g2-research-grid"><article class="g2-research-socket"><span class="g2-claim-id">NO_INCREMENT</span><h3>No earned change</h3><p>The native question remains where it began.</p></article><article class="g2-research-socket"><span class="g2-claim-id">CLARIFICATION</span><h3>Sharper statement</h3><p>Terms or debts become clearer without resolving the problem.</p></article><article class="g2-research-socket"><span class="g2-claim-id">TYPE_DISSOLUTION</span><h3>Scoped dissolution</h3><p>The exact illegal join is the whole contradiction within the declared model.</p></article><article class="g2-research-socket"><span class="g2-claim-id">CONDITIONAL_RESOLUTION</span><h3>Resolution under assumptions</h3><p>The result does not escape its premises or native-review boundary.</p></article></div>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="pqa-controls-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">04 · Controls and review</p><h2 id="pqa-controls-title">Beating a placebo earns nothing.</h2></div><p class="g2-section__intro">Agreement between systems is not truth evidence.</p></div>
    <p>Matched neutral, Emergentist, native-frame, generic-decomposition, and shuffled-placebo arms receive the same source access and budget. An earned result needs two independent blinded human native-domain reviews; AI reviews remain diagnostic and never satisfy quorum.</p>
    <p class="g2-note">The Emergentist arm must add value over both the native frame and generic decomposition. Nulls, harms, narrowing, kills, and retractions remain publishable outcomes.</p>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="pqa-companion-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">05 · EUB firewall</p><h2 id="pqa-companion-title">Companion means joined by hashes, not joined by truth.</h2></div><p class="g2-section__intro">EUB-1 v1.0 remains frozen.</p></div>
    <p><code>PQAEUBCompanion.v1</code> may bind exact protocol, schema, freeze, candidate, and runtime hashes. <code>truth_transfer=false</code> and <code>score_transfer=false</code> are mandatory. Neither benchmark validates the other.</p>
  </section>

  <section class="g2-shell g2-section" aria-labelledby="pqa-boundary-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">06 · Release boundary</p><h2 id="pqa-boundary-title">OFFLINE-READY · [D] is not a philosophical result.</h2></div><p class="g2-section__intro">This v2.2 projection has not been deployed by this implementation act.</p></div>
    <p>It means the public denominator, schemas, validators, deterministic synthetic fixtures, vector scorer, recorded-response tests, and projection pass locally. It does not mean Emergentism was scientifically validated, a question was resolved, a model was evaluated, or a priority deposit exists.</p>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="/questions/">Inspect the denominator</a><a class="g2-button" href="/ethics/">Audit the normative bridge</a><a class="g2-button" href="/exit/">Exit</a></div>
  </section>'''


def build_outputs() -> dict[Path, str]:
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    projection = json.loads(PROJECTION_PATH.read_text(encoding="utf-8"))
    validate_inputs(atlas, projection)
    return {
        SITE / "questions" / "index.html": page_document(
            title="The Question Atlas — 54 open philosophical targets",
            description="PQA-54 freezes 54 public question families and keeps inventory, clarification, dissolution, resolution, and residual debt distinct.",
            canonical="https://emergentism.org/questions/",
            main=question_atlas_main(atlas),
            active="worldview",
        ),
        SITE / "record" / "pqa-54" / "index.html": page_document(
            title="PQA-54 record — The Philosophical Question Atlas",
            description="The offline-ready PQA-54 construct: 54 selected, zero evaluated, zero independently reviewed, zero resolved.",
            canonical="https://emergentism.org/record/pqa-54/",
            main=record_main(),
            active="research",
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"QUESTION ATLAS: FAIL\n- {exc}")
        return 1
    drift: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(SITE).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("QUESTION ATLAS: FAIL")
        for rel in drift:
            print(f"- deterministic drift: {rel}")
        return 1
    print(f"QUESTION ATLAS: PASS · 54/0/0/0 · {'clean' if args.check else 'rendered'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

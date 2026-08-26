#!/usr/bin/env python3
"""Build disjoint public projections of the Fourth Churning Type Atlas."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any

from build_core_shell import render_page, surface_for


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PACKET = ROOT / "14_THE_DISTILLATION" / "08_THE_FOURTH_CHURNING_2026_08_24"
COLLISIONS = PACKET / "data" / "type_collisions.v1.json"
DIAGNOSES = PACKET / "data" / "mystery_diagnoses.v1.json"
CORPUS = PACKET / "FourthChurningCorpus.v1.json"
THIRD = ROOT / "14_THE_DISTILLATION" / "07_THE_THIRD_CHURNING_2026_08_23" / "ThirdChurningCorpus.v1.json"
SCHEMAS = {
    "TypeCollision.v1.schema.json": PACKET / "contracts" / "TypeCollision.v1.schema.json",
    "MysteryDiagnosis.v1.schema.json": PACKET / "contracts" / "MysteryDiagnosis.v1.schema.json",
    "FourthChurningCorpus.v1.schema.json": PACKET / "contracts" / "FourthChurningCorpus.v1.schema.json",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pretty(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def page_document(main: str) -> bytes:
    base = f'''<!doctype html>
<html lang="en" data-gestalt="v2">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>The Mystery Type Atlas — Fourth Churning</title>
  <meta name="description" content="A candidate seven-axis grammar diagnosing type collisions, partial collisions, non-collisions, and underdetermination across PQA-54." />
  <meta name="theme-color" content="#07090f" />
  <link rel="canonical" href="https://emergentism.org/questions/diagnoses/" />
  <link rel="stylesheet" href="/assets/css/gestalt-v2.css" />
  <script defer src="/assets/js/gestalt-v2.js"></script>
<!--OG:AUTO-->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:title" content="The Mystery Type Atlas — Fourth Churning" />
<meta property="og:description" content="A candidate seven-axis grammar diagnosing type collisions, partial collisions, non-collisions, and underdetermination across PQA-54." />
<meta property="og:url" content="https://emergentism.org/questions/diagnoses/" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<!--/OG:AUTO-->
</head>
<body class="g2-page"><main id="main" class="g2-main" tabindex="-1">{main}</main></body>
</html>'''
    return render_page(
        base,
        "worldview",
        surface=surface_for("questions/diagnoses/index.html"),
    ).encode("utf-8")


def validate_inputs(
    collisions: Any, diagnoses: Any, corpus: Any, third: Any
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if not isinstance(collisions, list) or len(collisions) != 12:
        raise ValueError("Fourth Churning requires 12 collision subtypes")
    if not isinstance(diagnoses, list) or len(diagnoses) != 54:
        raise ValueError("Fourth Churning requires 54 diagnoses")
    if not isinstance(corpus, dict) or corpus.get("schema_id") != "emergentism/FourthChurningCorpus.v1":
        raise ValueError("Fourth Churning corpus contract drift")
    if corpus.get("pqa_state") != {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}:
        raise ValueError("PQA state must remain 54/0/0/0")
    if corpus.get("held_out_integrity") != "CONTAMINATED_FOR_FOURTH_USE":
        raise ValueError("Fourth Churning may not claim fresh held-out status")
    if corpus.get("global_philosophy_claim_allowed") is not False:
        raise ValueError("global philosophy claims remain forbidden")
    if corpus.get("external_states") != {"deployed": False, "native_reviewed": False, "empirically_validated": False, "training_inclusion_guaranteed": False}:
        raise ValueError("external-state boundary drift")
    collision_ids = [row.get("collision_id") for row in collisions if isinstance(row, dict)]
    if collision_ids != corpus.get("collision_order") or len(set(collision_ids)) != 12:
        raise ValueError("collision order or identity drift")
    diagnosis_ids = [row.get("diagnosis_id") for row in diagnoses if isinstance(row, dict)]
    if diagnosis_ids != corpus.get("diagnosis_order") or len(set(diagnosis_ids)) != 54:
        raise ValueError("diagnosis order or identity drift")
    if any(row.get("earned_effect") != "NO_INCREMENT" or row.get("result_state") != "SELECTED_UNREVIEWED" for row in diagnoses):
        raise ValueError("candidate diagnosis attempts to award an earned result")
    if any(row.get("split_integrity") != "CONTAMINATED_FOR_FOURTH_USE" for row in diagnoses):
        raise ValueError("diagnosis split-integrity drift")
    refs = set(collision_ids)
    for row in diagnoses:
        linked = ([row["primary_collision_id"]] if row.get("primary_collision_id") else []) + row.get("secondary_collision_ids", [])
        if any(item not in refs for item in linked):
            raise ValueError(f"{row.get('diagnosis_id')}: dangling collision reference")
        if row.get("diagnosis_state") in {"NO_COLLISION", "UNDERDETERMINED"} and row.get("alleged_invalid_join") is not None:
            raise ValueError(f"{row.get('diagnosis_id')}: null diagnosis asserts a collision")
    input_hashes = corpus.get("input_hashes")
    if not isinstance(input_hashes, list):
        raise ValueError("input hash contract malformed")
    for row in input_hashes:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise ValueError(f"Fourth source hash drift: {row['path']}")
    third_outputs = set(third.get("output_map", {}).values())
    fourth_outputs = set(corpus.get("public_output_map", {}).values())
    if not third_outputs.isdisjoint(fourth_outputs):
        raise ValueError("Third and Fourth public writers overlap")
    return collisions, diagnoses, corpus


def render_main(collisions: list[dict[str, Any]], diagnoses: list[dict[str, Any]], corpus: dict[str, Any]) -> str:
    counts = corpus["candidate_counts"]
    collision_cards = "".join(
        f'''<article class="g2-panel" id="{esc(row['collision_id'].lower())}">
          <span class="g2-claim-id">{esc(row['collision_id'])} · {esc(row['axis'])} · [I/C]</span>
          <h3>{esc(row['plain_name'])}</h3>
          <p>{esc(row['forbidden_inference'])}</p>
          <details><summary>Question, repair, and kill</summary><p><strong>Ask:</strong> {esc(row['diagnostic_question'])}</p><p><strong>Repair:</strong> {esc(row['conservative_repair'])}</p><p><strong>Kill:</strong> {esc(row['kill_criterion'])}</p></details>
        </article>'''
        for row in collisions
    )
    diagnosis_cards = "".join(
        f'''<article class="g2-question" id="{esc(row['problem_id'])}" data-question-id="{esc(row['problem_id'])}">
          <span class="g2-question__meta">{esc(row['diagnosis_id'])} · {esc(row['diagnosis_state'])} · {esc(row['proposed_effect'])}</span>
          <h3>{esc(row['native_problem'])}</h3>
          <p><strong>Candidate diagnosis:</strong> {esc(row['diagnostic_claim'])}</p>
          <p><strong>Conservative repair:</strong> {esc(row['repaired_formulation'])}</p>
          <p><strong>Legitimate bridge:</strong> {esc(row['legitimate_bridge'])}</p>
          <p><strong>Emergentist answer:</strong> {esc(row['emergentist_answer'])}</p>
          <p><strong>Residual debt:</strong> {esc(row['residual_debt'])}</p>
          <details><summary>Rival, kill, and survivor</summary><p><strong>Native rival:</strong> {esc(row['strongest_native_rival'])}</p><p><strong>Generic control:</strong> {esc(row['generic_control'])}</p><p><strong>Kill:</strong> {esc(row['kill_criterion'])}</p><p><strong>Survivor:</strong> {esc(row['survivor_if_killed'])}</p></details>
        </article>'''
        for row in diagnoses
    )
    return f'''
  <header class="g2-shell g2-page-hero">
    <p class="g2-kicker">Fourth Churning · candidate Type Atlas · [D] [I] [C]</p>
    <h1>The Perennial Mystery Type Atlas</h1>
    <p>Where philosophical paradoxes break—and where they don’t.</p>
    <p class="g2-page-hero__lede">Emergentism proposes that many perennial problems contain malformed joins between types. It does not claim that every mystery is a type error.</p>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="#grammar">Inspect the grammar</a><a class="g2-button" href="#diagnoses">Read all 54 diagnoses</a><a class="g2-button" href="/questions/">Return to PQA-54</a></div>
    <div class="g2-page-meta"><span>54 selected</span><span>0 evaluated</span><span>0 independently reviewed</span><span>0 resolved</span></div>
  </header>
  <section class="g2-shell g2-section" aria-labelledby="outcomes-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Four honest outputs</p><h2 id="outcomes-title">The type checker is allowed to say no.</h2></div><p class="g2-section__intro">A distinction is not yet a collision.</p></div>
    <div class="g2-practice-grid"><article class="g2-panel"><span class="g2-claim-id">TYPE_COLLISION · {counts['TYPE_COLLISION']}</span><h3>Exact join proposed</h3><p>An invalid inference is stated, but no earned dissolution follows.</p></article><article class="g2-panel"><span class="g2-claim-id">PARTIAL · {counts['PARTIAL_TYPE_COLLISION']}</span><h3>Some debt is typed</h3><p>The distinction clarifies part of the problem while the native mystery survives.</p></article><article class="g2-panel"><span class="g2-claim-id">NO_COLLISION · {counts['NO_COLLISION']}</span><h3>Well-typed difficulty</h3><p>The problem remains substantive without any malformed join.</p></article><article class="g2-panel"><span class="g2-claim-id">UNDERDETERMINED · {counts['UNDERDETERMINED']}</span><h3>Not enough to classify</h3><p>The present sources do not expose a decisive collision.</p></article></div>
    <p class="g2-note">These are retrospective candidate labels over an exposed corpus. The old PQA split is contaminated for Fourth Churning use.</p>
  </section>
  <section class="g2-shell g2-section" id="grammar" aria-labelledby="grammar-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Seven axes · twelve subtypes</p><h2 id="grammar-title">A small algebra of philosophical failure.</h2></div><p class="g2-section__intro">Level · modal · temporal · representational · epistemic · normative · bearer.</p></div>
    <div class="g2-practice-grid">{collision_cards}</div>
  </section>
  <section class="g2-shell g2-section" id="diagnoses" aria-labelledby="diagnoses-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">PQA-54 sidecar</p><h2 id="diagnoses-title">Fifty-four diagnoses. Zero earned resolutions.</h2></div><p class="g2-section__intro">Every card preserves its native rival and residual debt.</p></div>
    <div class="g2-question-grid">{diagnosis_cards}</div>
  </section>
  <section class="g2-shell g2-section" aria-labelledby="boundary-title">
    <div class="g2-section__head"><div><p class="g2-eyebrow">Boundary</p><h2 id="boundary-title">A completed map is not a completed mystery.</h2></div><p class="g2-section__intro">Source hashes prove custody, not correctness.</p></div>
    <p>Russell, Tarski, Ryle, Carnap, Wittgenstein, Lawvere, and others own the underlying type, category, hierarchy, and dissolution moves. The candidate delta is their assembly into a machine-readable atlas with nulls, rivals, kills, and residuals. Novelty remains withheld.</p>
    <div class="g2-actions"><a class="g2-button g2-button--primary" href="/questions/diagnoses.json">Download diagnoses</a><a class="g2-button" href="/questions/collisions.json">Download the grammar</a><a class="g2-button" href="/exit/">Exit</a></div>
  </section>'''


def build_outputs() -> dict[Path, bytes]:
    collisions, diagnoses, corpus = validate_inputs(load(COLLISIONS), load(DIAGNOSES), load(CORPUS), load(THIRD))
    expected = {
        SITE / "questions" / "diagnoses" / "index.html": page_document(render_main(collisions, diagnoses, corpus)),
        SITE / "questions" / "collisions.json": pretty(collisions),
        SITE / "questions" / "diagnoses.json": pretty(diagnoses),
        SITE / "questions" / "fourth-churning.json": pretty(corpus),
    }
    for name, source in SCHEMAS.items():
        expected[SITE / "questions" / "schemas" / name] = source.read_bytes()
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"FOURTH PUBLIC: FAIL\n- {exc}")
        return 1
    drift: list[str] = []
    for path, payload in outputs.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                drift.append(path.relative_to(SITE).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    if drift:
        print("FOURTH PUBLIC: FAIL")
        for path in drift:
            print(f"- deterministic drift: {path}")
        return 1
    print(f"FOURTH PUBLIC: PASS · {len(outputs)} disjoint outputs · {'clean' if args.check else 'rendered'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

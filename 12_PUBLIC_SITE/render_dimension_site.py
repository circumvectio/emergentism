#!/usr/bin/env python3
"""Deterministically render the dimension-first public spine from its parity manifest."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from build_core_shell import head_assets, render_footer, render_nav


SITE = Path(__file__).resolve().parent
MANIFEST = SITE / "public_semantic_parity.json"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def pretty_id(value: str) -> str:
    return value.replace("mu", "μ")


def field(label: str, value: str) -> str:
    return f"<dt>{esc(label)}</dt><dd>{esc(value)}</dd>"


def require_g7_projection(stone: dict) -> dict:
    """Fail closed when the public D5 projection loses its typed safety fences."""
    projection = stone.get("projection")
    if not isinstance(projection, dict) or projection.get("schema") != "emergentism/G7Projection.v1":
        raise ValueError("D5 stone.projection must be emergentism/G7Projection.v1")

    transfers = projection.get("transfers")
    if not isinstance(transfers, list) or len(transfers) != 4:
        raise ValueError("G7Projection.v1 requires exactly four transfers")
    quadrants = {item.get("quadrant") for item in transfers}
    if quadrants != {"top-left", "top-right", "bottom-left", "bottom-right"}:
        raise ValueError("G7Projection.v1 transfers must occupy all four quadrants")
    expected_quadrants = {
        "taking-a": "top-left",
        "taking-b": "bottom-left",
        "giving-a": "bottom-right",
        "giving-b": "top-right",
    }
    if {item.get("id"): item.get("quadrant") for item in transfers} != expected_quadrants:
        raise ValueError("G7Projection.v1 transfer/quadrant assignment drift")
    if any(not item.get("signature") or not item.get("channelPair") or not item.get("egoCollectiveSigns") for item in transfers):
        raise ValueError("G7Projection.v1 transfers require bearer, channel, and ego/collective signs")

    plane_axes = projection.get("planeAxes", {})
    if plane_axes != {
        "horizontal": "self-facing to other-facing",
        "vertical": "raised Phi5 channel to raised V4 channel",
        "tier": "[I]",
    }:
        raise ValueError("G7Projection.v1 planeAxes contract drift")
    ego_collective_gloss = projection.get("egoCollectiveGloss", {})
    if ego_collective_gloss != {
        "self": "ego-facing",
        "other": "collective-facing",
        "identity": False,
        "bareSignsRecoverM4": False,
        "tier": "[I]",
    }:
        raise ValueError("G7Projection.v1 ego/collective gloss contract drift")

    frames = projection.get("frames")
    if not isinstance(frames, list) or len(frames) != 3:
        raise ValueError("G7Projection.v1 requires exactly three Titan frames")
    by_position = {item.get("axisPosition"): item for item in frames}
    if set(by_position) != {"bottom", "centre", "top"}:
        raise ValueError("G7Projection.v1 frames must occupy bottom, centre, and top")
    if by_position["centre"].get("alias") != "Viṣṇu" or by_position["centre"].get("valueMarker") != "1_T":
        raise ValueError("G7Projection.v1 centre must be Viṣṇu at 1_T")

    count_source = projection.get("countSource", {})
    mirror = projection.get("separateMirrorLadder", {})
    relation = projection.get("relation", {})
    burrisphere = projection.get("burrisphereG7", {})
    if count_source.get("partition") != [4, 3] or mirror.get("partition") != [3, 1, 3]:
        raise ValueError("G7@1 and GEN7@1 partitions must remain distinct")
    required_relations = {
        "g7NotGen7": True,
        "sameCount": True,
        "sameStructure": False,
        "geometryForcesSeven": False,
        "convergenceIsTruthEvidence": False,
        "lowercaseEqualsUppercase": False,
    }
    if any(relation.get(key) is not value for key, value in required_relations.items()):
        raise ValueError("G7Projection.v1 proof-transfer fences are missing or changed")
    if burrisphere.get("generatesCount") is not False or mirror.get("generatesCount") is not False:
        raise ValueError("neither Burrisphere projection may generate the selected count")

    display_path = projection.get("displayPath", {})
    expected_path = {
        "schema": "emergentism/G7DisplayPath.v1",
        "geometry": "one-selected-turn-around-stationary-axis",
        "turns": 1,
        "degrees": 360,
        "verticalDirection": "bottom-to-top",
        "startFrame": "shiva-dissolve",
        "centreLatitude": "vishnu-preserve",
        "endFrame": "brahma-create",
        "traversesAxisPoint": False,
        "phaseOrder": ["taking-a", "taking-b", "giving-a", "giving-b"],
        "phaseOrderTier": "[I]",
        "semantics": "presentation-itinerary-only",
        "makesContinuousG7State": False,
        "dynamics": False,
        "causal": False,
        "temporal": False,
        "recurrent": False,
        "moralRanking": False,
        "derivesCount": False,
        "tier": "[I]",
    }
    if display_path != expected_path:
        raise ValueError("G7DisplayPath.v1 contract drift")

    reciprocal = projection.get("reciprocalSpectrum", {})
    expected_reciprocal = {
        "schema": "emergentism/ReciprocalSpectrum.v1",
        "domain": "positive reciprocal chart",
        "from": "ν→∞, φ→0",
        "centre": "φ=ν=1",
        "to": "φ→∞, ν→0",
        "constraint": "φν=1 everywhere",
        "constraintSelectsCentre": False,
        "balance": "B=2/(φ+ν)≤1",
        "uniqueMaximum": {"value": 1, "at": "φ=ν=1", "tier": "[A]"},
        "sameAsSignedG7Plane": False,
        "sameAsUppercasePowerModel": False,
        "revivesProductRanking": False,
        "g7ExhaustsAllGames": False,
        "tier": "[A/S/I]",
    }
    if reciprocal != expected_reciprocal:
        raise ValueError("ReciprocalSpectrum.v1 contract drift")

    strategy = projection.get("strategyCompression", {})
    expected_strategy = {
        "schema": "emergentism/BasicStrategyCompression.v1",
        "axes": {
            "direction": ["self-facing taking", "other-facing giving"],
            "channel": ["Φ₅ possible/model power", "V₄ actual/embodied power"],
        },
        "cells": 4,
        "scopedExhaustion": "selected M4 two-axis vocabulary",
        "compressionMode": "intensional-not-extensional",
        "compressionTarget": "cross-game self/other direction and possible/actual power-channel orientation",
        "maximumCompressionCandidate": True,
        "exhaustsGameTheory": False,
        "reconstructsNativeGames": False,
        "nativeStructurePreserved": [
            "players",
            "coalitions",
            "information",
            "timing",
            "payoffs",
            "repetition",
            "stochasticity",
            "institutions",
            "learning",
            "equilibrium concepts",
        ],
        "mnemonics": {
            "egoCollective": {"tier": "[I]", "identity": False},
            "theftSacrifice": {"tier": "[I]", "moralVerdict": False},
            "mentalPhysical": {"tier": "[I]", "identity": False, "phi5WiderThanMental": True},
        },
        "kills": [
            "third-power-channel",
            "additional-bearer-orientation",
            "unrecoverable-strategy-effect",
        ],
        "maximalityTest": {
            "schema": "emergentism/StrategyCompressionTest.v1",
            "status": "preregistration-required-not-run",
            "coding": "lossy",
            "corpus": "declared cross-game corpus",
            "fixedBeforeCoding": [
                "native-game-descriptions",
                "bearer-indexed-option-capability-changes",
                "held-out-prediction-or-intervention-targets",
                "loss-function",
                "description-length-measure",
                "material-improvement-threshold",
                "acceptable-distortion-ceiling-or-target-utility-floor",
            ],
            "comparators": [
                "native-game-baseline",
                "coarser-one-axis-code",
                "added-axis-rival",
            ],
            "criterion": "declared rate-distortion frontier",
            "maximalDefinition": "minimum-description-length-at-fixed-acceptable-performance-within-preregistered-comparator-class",
            "globalUniqueEstablished": False,
            "kills": [
                "richer-rival-clears-threshold-after-complexity-cost",
                "necessary-orientation-distinctions-collapse",
                "third-universal-channel-or-bearer-orientation",
            ],
            "truthEvidence": False,
            "tier": "[C]",
        },
        "tier": "[S/I/C]",
    }
    if strategy != expected_strategy:
        raise ValueError("BasicStrategyCompression.v1 contract drift")
    return projection


def stone_section(stone: dict) -> tuple[str, str]:
    projection = require_g7_projection(stone)
    powers = projection["powers"]
    count_source = projection["countSource"]
    mirror = projection["separateMirrorLadder"]
    burrisphere = projection["burrisphereG7"]
    burrisphere_layout = burrisphere["layout"].replace("-", " ")
    plane_axes = projection["planeAxes"]
    ego_collective_gloss = projection["egoCollectiveGloss"]
    display_path = projection["displayPath"]
    reciprocal = projection["reciprocalSpectrum"]
    strategy = projection["strategyCompression"]
    balance_display = reciprocal["balance"].replace("=", " = ", 1).replace("≤", " ≤ ")

    power_card_parts: list[str] = []
    for key in ("possible", "presentEvaluation", "actual"):
        causal_note = (
            "  <p>Possible content is not causal by itself.</p>\n"
            if powers[key].get("causalByItself") is False
            else ""
        )
        power_card_parts.append(f"""<article>
  <p class="power-symbol">{esc(powers[key]['symbol'])}</p>
  <h4>{esc(powers[key]['type'])}</h4>
{causal_note}</article>""")
    power_cards = "".join(power_card_parts)

    transfers_by_quadrant = {item["quadrant"]: item for item in projection["transfers"]}
    transfer_cards = "".join(
        f"""<article class="g7-transfer g7-{esc(quadrant)}">
  <p class="quadrant-label">{esc(quadrant.replace('-', ' '))}</p>
  <h4>{esc(item['plain'])} <small>alias: {esc(item['alias'])}</small></h4>
  <p><b>Bearer signs:</b> <code>{esc(item['signature'])}</code></p>
  <p><b>Channel pair:</b> <code>{esc(item['channelPair'])}</code></p>
  <p><b>Ego/collective gloss {esc(projection['egoCollectiveGlossTier'])}:</b> <code>{esc(item['egoCollectiveSigns'])}</code></p>
</article>"""
        for quadrant in ("top-left", "top-right", "bottom-left", "bottom-right")
        for item in (transfers_by_quadrant[quadrant],)
    )

    frames_by_position = {item["axisPosition"]: item for item in projection["frames"]}
    frame_card_parts: list[str] = []
    for position in ("top", "centre", "bottom"):
        item = frames_by_position[position]
        value_marker = (
            f'  <p class="value-marker">{esc(item["valueMarker"])}</p>\n'
            if item.get("valueMarker")
            else ""
        )
        frame_card_parts.append(f"""<li class="titan-{esc(position)}">
  <p class="axis-position">{esc(position)}</p>
  <h4>{esc(item['plain'])} <small>alias: {esc(item['alias'])} {esc(item['glyph'])}</small></h4>
{value_marker}  <p class="signature">{esc(item['signature'])}</p>
</li>""")
    frame_cards = "".join(frame_card_parts)

    transfers_by_id = {item["id"]: item for item in projection["transfers"]}
    frames_by_id = {item["id"]: item for item in projection["frames"]}
    phase_cards = "".join(
        f"""<li>
  <p class="phase-id">{index} · {esc(item['id'])}</p>
  <h4>{esc(item['plain'])} <small>alias: {esc(item['alias'])}</small></h4>
  <p><code>{esc(item['signature'])}</code></p>
</li>"""
        for index, item_id in enumerate(display_path["phaseOrder"], start=1)
        for item in (transfers_by_id[item_id],)
    )
    start_frame = frames_by_id[display_path["startFrame"]]
    centre_frame = frames_by_id[display_path["centreLatitude"]]
    end_frame = frames_by_id[display_path["endFrame"]]
    strategy_kills = "".join(f"<li><code>{esc(kill)}</code></li>" for kill in strategy["kills"])
    native_structures = "".join(
        f"<li>{esc(structure)}</li>" for structure in strategy["nativeStructurePreserved"]
    )
    maximality_test = strategy["maximalityTest"]
    fixed_before_coding = "".join(
        f"<li><code>{esc(item)}</code></li>" for item in maximality_test["fixedBeforeCoding"]
    )
    strategy_comparators = "".join(
        f"<li><code>{esc(item)}</code></li>" for item in maximality_test["comparators"]
    )
    maximality_kills = "".join(
        f"<li><code>{esc(item)}</code></li>" for item in maximality_test["kills"]
    )

    bearer_indices = " · ".join(projection["bearerIndices"])
    html_output = f"""
<section class="stone" aria-labelledby="stone-title">
  <p class="eyebrow">D5 · {esc(count_source['id'])} · {esc(count_source['tier'])} selected vocabulary</p>
  <h2 id="stone-title">{esc(stone['title'])}</h2>
  <p>{esc(stone['summary'])}</p>
  <div id="d5-powers" class="d5-powers" aria-labelledby="d5-powers-title">
    <h3 id="d5-powers-title">Possible power, present evaluation, actual power</h3>
    <p class="stone-formula">{esc(stone['formula'])}</p>
    <p class="projection-tier">Projection tier: {esc(powers['tier'])} · bearer indices: {esc(bearer_indices)}</p>
    <div class="power-grid">{power_cards}</div>
  </div>
  <div id="g7-projection" class="g7-projection" aria-labelledby="g7-title">
    <p class="eyebrow">Four moves + three read-only frames</p>
    <h3 id="g7-title">G7, neutral functions first</h3>
    <p>{esc(count_source['derivation'])}. The mythic names are aliases; they do not decide moral standing.</p>
    <div class="plane-axes" aria-label="Selected signed G7 plane axes">
      <p><b>Horizontal axis · {esc(plane_axes['tier'])}:</b> {esc(plane_axes['horizontal'])}</p>
      <p><b>Vertical axis · {esc(plane_axes['tier'])}:</b> {esc(plane_axes['vertical'])}</p>
    </div>
    <p><b>Bearer gloss · {esc(ego_collective_gloss['tier'])}:</b> self is {esc(ego_collective_gloss['self'])}; other is {esc(ego_collective_gloss['other'])}. These are glosses, not identities, and bare signs do not recover M4.</p>
    <div class="g7-layout">
      <section aria-labelledby="transfer-title">
        <h4 id="transfer-title" class="map-title">Four bearer-oriented transfers</h4>
        <div class="g7-transfer-grid">{transfer_cards}</div>
      </section>
      <section aria-labelledby="titan-title">
        <h4 id="titan-title" class="map-title">Titan frame axis</h4>
        <ol class="titan-axis" aria-label="Titan frame axis from top through centre to bottom">{frame_cards}</ol>
      </section>
    </div>
  </div>
  <section id="strategy-compression" class="strategy-compression" aria-labelledby="strategy-title">
    <p class="eyebrow">{esc(strategy['schema'])} · {esc(strategy['tier'])}</p>
    <h3 id="strategy-title">Four cells as a scoped strategy compression</h3>
    <p><b>Game theory is not exhausted.</b> The broader [C] conjecture is that its basic strategic orientation is <b>maximally compressed</b> by these four cells—not that the cells reproduce every game.</p>
    <p><b>Compression target:</b> {esc(strategy['compressionTarget'])}. <b>Mode:</b> <code>{esc(strategy['compressionMode'])}</code>. Inside the <b>{esc(strategy['scopedExhaustion'])}</b>, the two declared axes close exactly {esc(strategy['cells'])} cells.</p>
    <div class="strategy-table-wrap"><table class="strategy-matrix">
      <caption>Selected M4 direction × channel vocabulary</caption>
      <thead><tr><th scope="col">Direction / channel</th><th scope="col">{esc(strategy['axes']['channel'][0])}</th><th scope="col">{esc(strategy['axes']['channel'][1])}</th></tr></thead>
      <tbody>
        <tr><th scope="row">{esc(strategy['axes']['direction'][0])}</th><td>{esc(transfers_by_id['taking-a']['plain'])}</td><td>{esc(transfers_by_id['taking-b']['plain'])}</td></tr>
        <tr><th scope="row">{esc(strategy['axes']['direction'][1])}</th><td>{esc(transfers_by_id['giving-a']['plain'])}</td><td>{esc(transfers_by_id['giving-b']['plain'])}</td></tr>
      </tbody>
    </table></div>
    <div class="strategy-mnemonics" aria-label="Bounded strategy mnemonics">
      <article><h4>Ego / collective · {esc(strategy['mnemonics']['egoCollective']['tier'])}</h4><p>A bounded facing gloss, not an identity.</p></article>
      <article><h4>Theft / sacrifice · {esc(strategy['mnemonics']['theftSacrifice']['tier'])}</h4><p>A mnemonic, not a moral verdict.</p></article>
      <article><h4>Mental / physical · {esc(strategy['mnemonics']['mentalPhysical']['tier'])}</h4><p>A mnemonic, not an identity. Φ₅ is wider than mentality.</p></article>
    </div>
    <h4>Native game structures are preserved, not reconstructed</h4>
    <p>This compression does not reconstruct native games. Their own structures remain explicit:</p>
    <ul class="native-structures">{native_structures}</ul>
    <h4>Exactly three registered kills</h4>
    <ul class="strategy-kills">{strategy_kills}</ul>
    <section class="maximality-test" aria-labelledby="maximality-test-title">
      <p class="eyebrow">{esc(maximality_test['schema'])} · {esc(maximality_test['tier'])}</p>
      <h4 id="maximality-test-title">Maximality test: preregistration required, not run</h4>
      <p><b>Status:</b> <code>{esc(maximality_test['status'])}</code>. <b>Coding:</b> <code>{esc(maximality_test['coding'])}</code>. <b>Corpus:</b> {esc(maximality_test['corpus'])}.</p>
      <p>The code is lossy. Preserving native game structure means keeping it in the evaluation baseline, not claiming that M4 reconstructs it.</p>
      <h5>Fixed-before-coding bundle</h5>
      <ul class="test-bundle">{fixed_before_coding}</ul>
      <h5>Three preregistered comparators</h5>
      <ul class="test-comparators">{strategy_comparators}</ul>
      <p><b>Rate–distortion criterion:</b> <code>{esc(maximality_test['criterion'])}</code>.</p>
      <p><b>Maximal definition:</b> <code>{esc(maximality_test['maximalDefinition'])}</code>.</p>
      <p><code>globalUniqueEstablished=false</code>. A finite run cannot prove unique global maximality.</p>
      <h5>Exactly three maximality-test kills</h5>
      <ul class="test-kills">{maximality_kills}</ul>
      <p class="itinerary-fence"><code>truthEvidence=false</code>. Even a compression win would not be truth evidence for the ontology.</p>
    </section>
  </section>
  <section id="g7-display-path" class="display-itinerary" aria-labelledby="display-path-title">
    <p class="eyebrow">{esc(display_path['schema'])} · {esc(display_path['tier'])} · {esc(display_path['semantics'])}</p>
    <h3 id="display-path-title">One selected {esc(display_path['degrees'])}° display path</h3>
    <p class="projection-tier">One selected {esc(display_path['degrees'])}° reading itinerary · geometry: <code>{esc(display_path['geometry'])}</code> · selected phase order: {esc(display_path['phaseOrderTier'])}</p>
    <p>One selected turn around a stationary axis, read {esc(display_path['verticalDirection'])}: begin at the {esc(start_frame['plain'])} latitude (alias: {esc(start_frame['alias'])} {esc(start_frame['glyph'])}), use {esc(centre_frame['plain'])} (alias: {esc(centre_frame['alias'])} {esc(centre_frame['glyph'])}, {esc(centre_frame['valueMarker'])}) as the centre latitude, and end at the {esc(end_frame['plain'])} latitude (alias: {esc(end_frame['alias'])} {esc(end_frame['glyph'])}). The itinerary turns around the axis and does not traverse an axis point.</p>
    <ol class="display-phases" aria-label="Selected four-phase G7 reading order">{phase_cards}</ol>
    <p class="itinerary-fence"><b>Display-path fence:</b> this is a presentation itinerary only—not time, dynamics, a causal path, recurrence, moral ranking or ascent, a continuous G7 state, or a source of the count seven.</p>
  </section>
  <section id="reciprocal-spectrum" class="reciprocal-spectrum" aria-labelledby="reciprocal-title">
    <p class="eyebrow">{esc(reciprocal['schema'])} · {esc(reciprocal['tier'])}</p>
    <h3 id="reciprocal-title">The lowercase reciprocal chart</h3>
    <p class="projection-tier">Domain: {esc(reciprocal['domain'])}</p>
    <div class="spectrum-points" aria-label="Positive reciprocal chart from one pole through the centre to the other pole">
      <p><b>From</b><code>{esc(reciprocal['from'])}</code></p>
      <p><b>Centre</b><code>{esc(reciprocal['centre'])}</code></p>
      <p><b>To</b><code>{esc(reciprocal['to'])}</code></p>
    </div>
    <p><code>{esc(reciprocal['constraint'])}</code>: the product is constant across the chart and therefore does not select the centre.</p>
    <p><code>{esc(balance_display)}</code>: B reaches its unique maximum <code>B={esc(reciprocal['uniqueMaximum']['value'])}</code> at <code>{esc(reciprocal['uniqueMaximum']['at'])}</code> {esc(reciprocal['uniqueMaximum']['tier'])}.</p>
    <h4>Signed G7 plane ≠ lowercase reciprocal chart ≠ uppercase node model</h4>
    <div class="model-distinction">
      <article><h5>Signed G7 plane</h5><p>Bearer-indexed <code>±Φ₅</code> and <code>±V₄</code> transfer signs in the selected G7 vocabulary.</p></article>
      <article><h5>Lowercase reciprocal chart</h5><p>Positive coordinates <code>φ,ν</code> constrained by <code>{esc(reciprocal['constraint'])}</code>.</p></article>
      <article><h5>Uppercase node model</h5><p>Present evaluation <code>Φ̂₄</code> and actual power <code>V₄</code>; <code>P_node := min(Φ̂₄, V₄)</code> is a separate selected AND-class convention.</p></article>
    </div>
    <p>The reciprocal chart is not the signed G7 plane or the uppercase power model. It does not revive product ranking, and G7 does not exhaust all games.</p>
  </section>
  <aside class="stone-boundary" aria-labelledby="namespace-title">
    <h3 id="namespace-title"><code>{esc(count_source['id'])} != {esc(mirror['id'])}</code> <small>({esc(count_source['id'])} ≠ {esc(mirror['id'])})</small></h3>
    <p>G7 uses the selected {esc(' + '.join(str(x) for x in count_source['partition']))} vocabulary. {esc(mirror['id'])} is the separate selected {esc(' + '.join(str(x) for x in mirror['partition']))} mirror ladder. Equal cardinality does not make them the same structure.</p>
    <p>The Burrisphere layout ({esc(burrisphere_layout)}, {esc(burrisphere['tier'])}) projects the vocabulary; geometry does not generate or force seven. Convergence is not truth evidence.</p>
    <p>{esc(stone['boundary'])}</p>
  </aside>
  <a class="next" href="../burrisphere/">See the selected Burrisphere geometry →</a>
</section>"""
    css_output = """
.stone{margin:2rem 0;padding:clamp(1.3rem,4vw,2rem);border:1px solid var(--gold);background:var(--surface)}
.stone h2{font-size:clamp(1.8rem,4vw,3rem);margin:.35rem 0}.stone h3{margin-top:2rem}.stone p,.stone li{color:var(--text-muted)}
.stone-formula,.signature,.power-symbol,.value-marker{font:700 .85rem/1.8 var(--font-mono);color:var(--gold)!important}.projection-tier,.quadrant-label,.axis-position,.phase-id{font:600 .7rem/1.5 var(--font-mono);text-transform:uppercase;letter-spacing:.08em;color:var(--text-dim)!important}
.power-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border)}.power-grid article{background:var(--bg);padding:1rem}.power-grid h4{margin:.2rem 0}.power-grid p{margin:.3rem 0}
.plane-axes{display:grid;grid-template-columns:1fr 1fr;gap:1px;margin:1rem 0;background:var(--border);border:1px solid var(--border)}.plane-axes p{margin:0;padding:.8rem;background:var(--bg)}
.g7-layout{display:grid;grid-template-columns:minmax(0,2fr) minmax(220px,1fr);gap:1.2rem;align-items:stretch}.map-title{margin:.5rem 0 1rem}
.g7-transfer-grid{display:grid;grid-template-areas:"top-left top-right" "bottom-left bottom-right";gap:1px;background:var(--border);border:1px solid var(--border)}
.g7-transfer{background:var(--bg);padding:1rem;min-width:0}.g7-transfer h4{margin:.2rem 0}.g7-transfer h4 small,.titan-axis h4 small,.display-phases h4 small{display:block;font:500 .72rem/1.5 var(--font-mono);color:var(--text-dim)}.g7-transfer p{overflow-wrap:anywhere}.g7-transfer code{color:var(--text-muted)}.g7-top-left{grid-area:top-left}.g7-top-right{grid-area:top-right}.g7-bottom-left{grid-area:bottom-left}.g7-bottom-right{grid-area:bottom-right}
.titan-axis{position:relative;display:grid;grid-template-rows:repeat(3,1fr);gap:1px;min-height:100%;margin:0;padding:0;list-style:none;background:var(--border);border:1px solid var(--border)}.titan-axis::before{content:"";position:absolute;top:1.5rem;bottom:1.5rem;left:.75rem;border-left:1px solid var(--gold)}.titan-axis li{position:relative;background:var(--bg);padding:.75rem .9rem .75rem 1.5rem}.titan-axis li::before{content:"";position:absolute;left:.5rem;top:50%;width:.5rem;border-top:1px solid var(--gold)}.titan-axis h4,.titan-axis p{margin:.2rem 0}.titan-top{grid-row:1}.titan-centre{grid-row:2;border:1px solid var(--gold)}.titan-bottom{grid-row:3}
.strategy-compression{margin-top:2rem;padding-top:.5rem;border-top:1px solid var(--border)}.strategy-table-wrap{overflow-x:auto}.strategy-matrix{width:100%;min-width:620px;border-collapse:collapse;margin:1rem 0}.strategy-matrix caption{text-align:left;padding:.6rem 0;font:600 .72rem/1.5 var(--font-mono);color:var(--text-dim)}.strategy-matrix th,.strategy-matrix td{padding:.8rem;border:1px solid var(--border);text-align:left}.strategy-matrix thead th{color:var(--gold);background:var(--bg)}.strategy-mnemonics{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border)}.strategy-mnemonics article{padding:1rem;background:var(--bg)}.strategy-mnemonics h4,.strategy-mnemonics p{margin:.2rem 0}.native-structures{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin:1rem 0;padding:0;list-style:none;background:var(--border);border:1px solid var(--border)}.native-structures li{padding:.7rem;background:var(--bg);text-align:center}.strategy-kills{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:1rem 0;padding:0;list-style:none;background:var(--border);border:1px solid var(--border)}.strategy-kills li{padding:1rem;background:var(--bg);overflow-wrap:anywhere}
.maximality-test{margin:1.5rem 0 0;padding:1rem;border:1px dashed var(--gold);background:var(--bg)}.maximality-test h4{margin:.35rem 0}.maximality-test h5{margin:1.2rem 0 .5rem}.test-bundle,.test-comparators,.test-kills{display:grid;gap:1px;margin:.5rem 0 1rem;padding:0;list-style:none;background:var(--border);border:1px solid var(--border)}.test-bundle{grid-template-columns:repeat(3,1fr)}.test-comparators,.test-kills{grid-template-columns:repeat(3,1fr)}.test-bundle li,.test-comparators li,.test-kills li{padding:.7rem;background:var(--surface);overflow-wrap:anywhere}
.display-itinerary,.reciprocal-spectrum{margin-top:2rem;padding-top:.5rem;border-top:1px solid var(--border)}.display-phases{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:1rem 0;padding:0;list-style:none;background:var(--border);border:1px solid var(--border)}.display-phases li{padding:.8rem;background:var(--bg)}.display-phases h4,.display-phases p{margin:.2rem 0}.itinerary-fence{border:1px dashed var(--gold);padding:1rem}
.spectrum-points,.model-distinction{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border)}.spectrum-points p,.model-distinction article{margin:0;padding:1rem;background:var(--bg)}.spectrum-points b,.spectrum-points code{display:block}.model-distinction h5{margin:.1rem 0 .5rem;font-size:.9rem}.model-distinction p{margin:0}.reciprocal-spectrum>p code{color:var(--gold)}
.stone-boundary{margin-top:1.5rem;border-left:2px solid var(--border);padding-left:1rem}.stone-boundary code{color:var(--gold)}
@media(max-width:700px){.power-grid,.plane-axes,.g7-layout,.g7-transfer-grid,.strategy-mnemonics,.native-structures,.strategy-kills,.test-bundle,.test-comparators,.test-kills,.display-phases,.spectrum-points,.model-distinction{display:grid;grid-template-columns:1fr;grid-template-areas:none}.g7-transfer{grid-area:auto}.native-structures li{text-align:left}}
"""
    return html_output, css_output


def transition_card(item: dict) -> str:
    if "transition" not in item:
        ret = item["return"]
        return f"""
<section class="transition" id="{esc(ret['id'])}">
  <p class="eyebrow">{esc(ret['id'])} · {esc(ret['tier'])} · non-causal interpretive edge</p>
  <h2>{esc(ret['label'])}</h2>
  <p>{esc(ret['meaning'])}</p>
  <a class="next" href="../0/">Return to D0 as a reader, not as an identity →</a>
</section>"""
    tr = item["transition"]
    next_index = int(item["id"][1:]) + 1
    next_href = f"../{next_index}/"
    if tr["id"] == "b6":
        next_href = "../6/"
    rows = "".join(
        field(label, tr[key])
        for label, key in (
            ("Saturation proposal", "saturation"),
            ("New capability", "capability"),
            ("Lower-level recovery", "recovery"),
            ("Evidence", "evidence"),
            ("Prediction", "prediction"),
            ("Alternatives", "alternatives"),
            ("Kill criterion", "kill"),
        )
    )
    # The label used to be derived from the ID STRING — every mu* got the identical
    # "candidate crossing", so no adjudication could ever reach the page. Two of the five
    # are adjudicated FAILED in doc 48 and the spine said "candidate" for all of them.
    # Now it comes from the data, and the source line travels with it.
    kind = tr.get("verdict") or ("candidate μ-crossing" if tr["id"].startswith("mu") else "non-μ boundary")
    verdict_source = (
        f'  <p class="source">Verdict source: {esc(tr["verdictSource"])}</p>\n'
        if tr.get("verdictSource")
        else ""
    )
    return f"""
<section class="transition" id="{esc(tr['id'])}">
  <p class="eyebrow">{esc(pretty_id(tr['id']))} · {kind}</p>
{verdict_source}  <h2>{esc(tr['label'])}</h2>
  <dl>{rows}</dl>
  <p class="source">Source owner: <code>{esc(tr['source'])}</code></p>
  <a class="next" href="{next_href}">Continue through {esc(pretty_id(tr['id']))} →</a>
</section>"""


def page(item: dict, prev_id: str | None, next_id: str | None) -> str:
    ident = item["id"]
    number = ident[1:]
    prev_link = f'<a href="../{prev_id[1:]}/">← {prev_id}</a>' if prev_id else '<a href="../dimensions/">← Spine</a>'
    next_link = f'<a href="../{next_id[1:]}/">{next_id} →</a>' if next_id else '<a href="../dimensions/">Spine →</a>'
    stone_html = ""
    stone_style = ""
    if stone := item.get("stone"):
        stone_html, stone_style = stone_section(stone)
    return f"""<!DOCTYPE html>
<html lang="en" data-gestalt="v2">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="color-scheme" content="dark" />
<title>/{number} — {esc(item['title'])} · Emergentism</title>
<meta name="description" content="{esc(item['summary'])}" />
<link rel="stylesheet" href="../assets/css/xai.css" />
<link rel="stylesheet" href="../dimensions/dimensions.css" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:title" content="/{number} — {esc(item['title'])} · Emergentism" />
<meta property="og:description" content="{esc(item['summary'])}" />
<meta property="og:url" content="https://emergentism.org/{number}/" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<script type="importmap">
{{"imports":{{"three":"../vendor/three-0.160.0/three.module.js","three/addons/":"../vendor/three-0.160.0/"}}}}
</script>
<style>
main{{max-width:920px;margin:0 auto;padding:110px 22px 72px}} .hero{{padding:2rem 0 3rem;border-bottom:1px solid var(--border)}}
.eyebrow,.tier,.source{{font:700 .74rem/1.6 var(--font-mono);color:var(--gold)}} h1{{font-size:clamp(2.5rem,7vw,5.8rem);line-height:.98;margin:.6rem 0 1.2rem}}
.lede{{font-size:1.15rem;color:var(--text-muted);max-width:68ch}} .grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border:1px solid var(--border);margin:2rem 0}}
.grid article{{background:var(--surface);padding:1.35rem}} .grid p{{color:var(--text-muted)}} .diagram{{min-height:300px;display:grid;place-items:center;border:1px solid var(--border);margin:2rem 0;overflow:hidden}}
.dimension-canvas{{width:100%;height:320px}} .transition{{margin:3rem 0;padding:1.5rem;border:1px solid var(--gold);border-radius:12px;background:var(--surface)}}
{stone_style}dl{{display:grid;grid-template-columns:minmax(150px,.35fr) 1fr;gap:0;border-top:1px solid var(--border)}} dt,dd{{margin:0;padding:.8rem;border-bottom:1px solid var(--border)}} dt{{font:700 .75rem/1.5 var(--font-mono);color:var(--text-dim)}} dd{{color:var(--text-muted)}}
.next{{display:inline-block;margin-top:1rem;color:var(--gold)}} .pager{{display:flex;justify-content:space-between;border-top:1px solid var(--border);padding-top:1rem}} code{{overflow-wrap:anywhere}}
html:not([data-gestalt-enhanced="true"]) .fallback{{display:flex}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}dl{{grid-template-columns:1fr}}dt{{padding-bottom:.2rem}}dd{{padding-top:.2rem}}}}
/* a11y-floor-2026-08-13 */
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px;border-radius:2px}}
@media (prefers-reduced-motion: reduce){{*,*::before,*::after{{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}}}}
</style>
{head_assets()}
</head>
<body class="g2-page g2-legacy g2-dimension">
{render_nav("worldview")}
<main id="main" tabindex="-1">
<section class="hero">
  <p class="eyebrow">{esc(ident)} · {esc(item['modality'])} · {esc(item['tier'])}</p>
  <h1>{esc(item['title'])}</h1>
  <p class="lede">{esc(item['subtitle'])}. {esc(item['summary'])}</p>
</section>
<section class="grid">
  <article><h2>Inherited structure</h2><p>{esc(item['inherited'])}</p></article>
  <article><h2>Claim boundary</h2><p>{esc(item['boundary'])}</p></article>
</section>{stone_html}
<section class="diagram visual-panel" aria-labelledby="diagram-title-{esc(number)}">
  <canvas class="dimension-canvas" aria-hidden="true"></canvas>
  <div class="fallback">
    <div class="fallback-inner">
      <p class="fallback-equation" id="diagram-title-{esc(number)}">{esc(ident)} · {esc(item['title'])}</p>
      <p>{esc(item['summary'])}</p>
      <p>This illustration carries no evidence beyond the typed text above.</p>
    </div>
  </div>
</section>
<p class="source">Semantic owner: <code>{esc(item['source'])}</code></p>
{transition_card(item)}
<nav class="pager">{prev_link}{next_link}</nav>
</main>
{render_footer()}
<script>window.DIMENSION_PAGE={{animationMode:{json.dumps(item['illustrationMode'])}}};</script>
<script type="module" src="../dimensions/dimensions.js"></script>
<script defer src="/assets/js/atlas-drawer.js"></script>
</body>
</html>
"""


def index_page(levels: list[dict], sequence: list[str], stone: dict) -> str:
    projection = require_g7_projection(stone)
    count_source = projection["countSource"]
    mirror = projection["separateMirrorLadder"]
    display_path = projection["displayPath"]
    reciprocal = projection["reciprocalSpectrum"]
    strategy = projection["strategyCompression"]
    maximality_test = strategy["maximalityTest"]
    balance_display = reciprocal["balance"].replace("=", " = ", 1).replace("≤", " ≤ ")
    native_structure_summary = ", ".join(strategy["nativeStructurePreserved"])
    rows: list[str] = []
    for item in levels:
        n = item["id"][1:]
        rows.append(f"<a class='rung' href='../{n}/'><b>{esc(item['id'])}</b><span>{esc(item['title'])}</span><small>{esc(item['tier'])} · {esc(item['modality'])}</small></a>")
        if "transition" in item:
            tr = item["transition"]
            rows.append(f"<div class='crossing'><b>{esc(pretty_id(tr['id']))}</b><span>{esc(tr['label'])}</span><small>{esc(tr.get('verdict') or ('candidate crossing' if tr['id'].startswith('mu') else 'non-μ boundary'))}</small></div>")
        else:
            ret = item["return"]
            rows.append(f"<div class='crossing'><b>{esc(ret['id'])}</b><span>{esc(ret['label'])}</span><small>interpretive edge only</small></div>")
    return f"""<!DOCTYPE html>
<html lang="en" data-gestalt="v2"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="color-scheme" content="dark" />
<title>The dimension-first spine · Emergentism</title><meta name="description" content="The complete typed Emergentist scaffold: D0 through D6 with five typed μ-interfaces — two standing, one owing a discriminator, two adjudicated failed — one exit boundary, and one interpretive return." />
<link rel="stylesheet" href="../assets/css/xai.css" /><style>
main{{max-width:900px;margin:0 auto;padding:120px 22px 80px}} h1{{font-size:clamp(2.6rem,7vw,5.5rem);line-height:1;margin:.5rem 0 1rem}} .lede{{color:var(--text-muted);max-width:64ch;font-size:1.1rem}}
.sequence{{font:700 .72rem/1.7 var(--font-mono);color:var(--gold);overflow-wrap:anywhere}} .spine{{margin:3rem 0;border-left:1px solid var(--gold);padding-left:1.2rem}}
.rung,.crossing{{display:grid;grid-template-columns:70px 1fr auto;gap:1rem;align-items:baseline;padding:1rem;border-bottom:1px solid var(--border);text-decoration:none}} .rung:hover{{background:var(--surface)}} .rung>*,.crossing>*{{min-width:0;overflow-wrap:anywhere}}
.rung b{{color:var(--gold)}} .crossing{{margin-left:1.5rem;color:var(--text-muted);font-style:italic}} .crossing b{{color:var(--text-dim)}} small{{font:600 .68rem/1.4 var(--font-mono);color:var(--text-dim)}}
.contract{{border:1px solid var(--border);padding:1.3rem;background:var(--surface)}} .contract li{{margin:.55rem 0;color:var(--text-muted);overflow-wrap:anywhere}}
.handoff{{margin:2rem 0;padding:1.3rem;border:1px solid var(--gold);background:var(--surface)}}.handoff p{{color:var(--text-muted)}}.handoff-route{{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}}.handoff-route a{{display:inline-flex;min-height:48px;align-items:center;padding:.55rem .75rem;border:1px solid var(--border);text-decoration:none}}.handoff-route span{{color:var(--gold)}}
@media(max-width:650px){{.rung,.crossing{{grid-template-columns:55px 1fr}}small{{grid-column:2}}.handoff-route{{display:grid;grid-template-columns:1fr}}.handoff-route span{{display:none}}}}
/* a11y-floor-2026-08-13 */
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px;border-radius:2px}}
@media (prefers-reduced-motion: reduce){{*,*::before,*::after{{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}}}}
</style>{head_assets()}<link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#070A12"><link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png"><script src="/assets/js/pwa.js" defer></script></head><body class="g2-page g2-legacy g2-dimensions-index">
{render_nav("worldview")}
<main id="main" tabindex="-1"><p class="sequence">{esc(' → '.join(pretty_id(x) for x in sequence))}</p><h1>The dimension-first spine</h1><p class="lede">A scaffold, not a census forced on nature. Each page separates inherited mathematics or science from Emergentist interpretation, and every crossing carries a prediction and a way to fail.</p>
<section class="contract"><h2>How to read it</h2><ul><li>D4 is actual; D5 is possible. An actual D4 model token may represent D5 possible content.</li><li>μ₀…μ₄ are candidate apertures. Empty evidence remains unassessed.</li><li>b₆ and r₆ are boundary relations, not additional μ-crossings.</li><li>The matter→bond→life→mind→choice story is an optional interpretation, not the owner of the formal registers.</li><li><b>The numbering is dependency priority, and nothing else.</b> Three orders must not collapse into it: <b>dependency priority</b> asks what rules and carriers a realization presupposes; <b>actuality</b> asks what causally occurred; <b>psychological salience</b> asks what is vivid or important to someone now. A higher number therefore implies <b>no</b> greater reality, vividness, moral worth, causal power, or standing of any person or thing placed near it. A ladder invites exactly that misreading, so it is refused here in writing.</li></ul></section>
<section class="handoff" aria-labelledby="handoff-title"><p class="eyebrow">One reading route · no proof transfer</p><h2 id="handoff-title">From the whole to its consequence</h2><p>Dasein asks for the whole account; the dimension pages type its dependencies. D5 then distinguishes possible and actual power before the selected {esc(count_source['id'])} vocabulary is projected into the Burrisphere, translated through Rosetta, and returned to practice by the Soul Loop. This sequence is a handoff, not a derivation: geometry does not force seven, {esc(count_source['id'])} != {esc(mirror['id'])} ({esc(count_source['id'])} ≠ {esc(mirror['id'])}), and convergence is not truth evidence.</p><p>The D5 display adds one selected {esc(display_path['degrees'])}° display path—a reading itinerary ({esc(display_path['semantics'])}), not time, dynamics, recurrence, moral ascent, or a count source. Its signed G7 plane remains distinct from the lowercase reciprocal chart and uppercase node model: <code>{esc(reciprocal['constraint'])}</code> is constant, while <code>{esc(balance_display)}</code> reaches its unique maximum <code>B={esc(reciprocal['uniqueMaximum']['value'])}</code> at <code>{esc(reciprocal['uniqueMaximum']['at'])}</code>.</p><p><b>Game theory is not exhausted.</b> A further [C] wager proposes that {esc(strategy['compressionTarget'])} is <b>maximally compressed</b> by the selected {esc(strategy['cells'])}-cell M4 vocabulary. This <code>{esc(strategy['compressionMode'])}</code> compression does not reconstruct native games; it preserves {esc(native_structure_summary)}. <a href="../5/#strategy-compression">Inspect that bounded compression →</a></p><p><b>Maximality test · {esc(maximality_test['tier'])}:</b> <code>{esc(maximality_test['status'])}</code>; <code>{esc(maximality_test['coding'])}</code> coding; {esc(len(maximality_test['fixedBeforeCoding']))} fields fixed before coding; {esc(len(maximality_test['comparators']))} comparators; criterion <code>{esc(maximality_test['criterion'])}</code>; definition <code>{esc(maximality_test['maximalDefinition'])}</code>; {esc(len(maximality_test['kills']))} kills; <code>globalUniqueEstablished=false</code>; <code>truthEvidence=false</code>. A finite run cannot prove unique global maximality.</p><nav class="handoff-route" aria-label="Dasein to Soul Loop reading route"><a href="../dasein/">Dasein whole</a><span aria-hidden="true">→</span><a href="../5/#d5-powers">Φ₅ / V₄ powers</a><span aria-hidden="true">→</span><a href="../5/#g7-projection">G7 transformations</a><span aria-hidden="true">→</span><a href="../burrisphere/">Burrisphere geometry</a><span aria-hidden="true">→</span><a href="../rosetta/">Rosetta translation</a><span aria-hidden="true">→</span><a href="../practice/">Soul Loop practice</a></nav></section>
<section class="spine">{''.join(rows)}</section><section class="contract"><h2>Related instruments and preserved visual studies</h2><p><a href="../suda/">Suda notes</a> · <a href="../egg/">The Egg</a> · <a href="../riemann/">Riemann view</a> · <a href="../journey/">Earlier journey view</a></p><p>These are supporting projections. The typed spine above governs where they conflict.</p></section><p><a href="../0/">Begin with D0 →</a></p></main><script defer src="/assets/js/atlas-drawer.js"></script>{render_footer()}</body></html>"""


def render() -> dict[Path, str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    levels = data["levels"]
    d5 = next((item for item in levels if item.get("id") == "D5"), None)
    if not d5 or "stone" not in d5:
        raise ValueError("public semantic parity must provide the D5 stone contract")
    outputs: dict[Path, str] = {
        SITE / "dimensions" / "index.html": index_page(levels, data["sequence"], d5["stone"])
    }
    for i, item in enumerate(levels):
        outputs[SITE / item["id"][1:] / "index.html"] = page(
            item,
            levels[i - 1]["id"] if i else None,
            levels[i + 1]["id"] if i + 1 < len(levels) else None,
        )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift: list[str] = []
    for path, content in render().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(str(path.relative_to(SITE)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("dimension render drift:")
        print("\n".join(drift))
        return 1
    print(f"dimension site: {'clean' if args.check else 'rendered'} ({len(render())} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

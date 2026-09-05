#!/usr/bin/env python3
"""Source-pinned G7 inspector projection; never updates doctrine or source pins.

Writes only atlas/burrisphere-operators.v1.json and a marked region of the
existing instrument. --check is read-only; source drift fails before writes.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PAGE = "burrisphere/instrument/index.html"
DATA = "atlas/burrisphere-operators.v1.json"
SCHEMA = "atlas/burrisphere-operators.v1.schema.json"
START = "<!-- burrisphere-operators:start -->"
END = "<!-- burrisphere-operators:end -->"
G7 = "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md"
ROWS = "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"
PINS = {
    G7: "a39a3e01255d208b852c158635507083127d46719e446ef88d2904b8a742a25c",  # pragma: allow-secret — verified public source SHA-256, not a credential
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md": "ba48ac8689d31032d3569b62c195bf992ba4b43bfe963e6162d5b77dac32d252",  # pragma: allow-secret — verified public source SHA-256, not a credential
    "05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md": "ebe6014b60c0b7d3f83f506a5d2a02dd70b241a055b69fb9fc089550ca81fbaa",  # pragma: allow-secret — verified public source SHA-256, not a credential
    ROWS: "dccca8c6c5a769fc1e3e25c9571bcbac3b71a876974b64e4081c32c8c67e6c8b",  # pragma: allow-secret — verified public source SHA-256, not a credential
}
RECORDS = [
    ("kali_take_phi", "Taking-A", "Kali 🎲", "+Φ₅,self, −V₄,other", "transfer", "top-left", "Raise own possible power while reducing another’s actual power.", [["Phi5", "self", "increase"], ["V4", "other", "decrease"]]),
    ("kali_take_v", "Taking-B", "Kālī 💀", "+V₄,self, −Φ₅,other", "transfer", "bottom-left", "Raise own actual power while cutting another’s represented possibility structure.", [["V4", "self", "increase"], ["Phi5", "other", "decrease"]]),
    ("krishna_give_v", "Giving-A", "Kṛṣṇa ◇", "−Φ₅,self, +V₄,other", "transfer", "bottom-right", "Spend own modeling or attention to build another’s actual power.", [["Phi5", "self", "decrease"], ["V4", "other", "increase"]]),
    ("arjuna_give_phi", "Giving-B", "Arjuna ⚔", "−V₄,self, +Φ₅,other", "transfer", "top-right", "Spend own actual power to improve another’s possible power.", [["V4", "self", "decrease"], ["Phi5", "other", "increase"]]),
    ("brahma_create", "Creation", "Brahmā ○", "+Φ₅,+V₄", "frame", "top", "Read joint growth of the two factors within a declared scope.", [["Phi5", "declared-scope", "increase"], ["V4", "declared-scope", "increase"]]),
    ("shiva_dissolve", "Dissolution", "Śiva •", "−Φ₅,−V₄", "frame", "bottom", "Read joint reduction of the two factors within a declared scope.", [["Phi5", "declared-scope", "decrease"], ["V4", "declared-scope", "decrease"]]),
    ("vishnu_preserve", "Preservation", "Viṣṇu ⊙", "ΔΦ₅≈0,ΔV₄≈0", "frame", "centre", "Read preservation, not maximization. The source leaves the meaning of approximate hold uncalibrated.", [["Phi5", "declared-scope", "hold-unresolved"], ["V4", "declared-scope", "hold-unresolved"]]),
]


def bound_rows(sources: dict) -> dict:
    """Join exact source rows by alias, not independent substring presence."""
    signatures = {}
    for line in sources[G7].splitlines():
        if line.startswith('| Taking-') or line.startswith('| Giving-'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            signatures[cells[1]] = (cells[0], cells[2].strip('`'), 'transfer')
        elif any(line.startswith('| '+name) for name in ('Brahmā ○', 'Śiva •', 'Viṣṇu ⊙')):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            signatures[cells[0]] = (cells[2].removesuffix(' frame').capitalize(), cells[1].strip('`'), 'frame')
    result = {}
    for line in sources[ROWS].splitlines():
        if not line.startswith('| **L'): continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        alias, key, seat = cells[2], cells[3].strip('`'), cells[0].strip('*')
        if alias in signatures:
            plain, signature, kind = signatures[alias]
            result[key] = (plain, alias, signature, kind, seat)
    if len(result) != 7: raise ValueError('Exactly seven joined source rows required')
    return result


def signature_clauses(signature: str, kind: str) -> list:
    """Parse only the seven reviewed directional shorthands; not arithmetic."""
    if signature == 'ΔΦ₅≈0,ΔV₄≈0' and kind == 'frame':
        return [['Phi5','declared-scope','hold-unresolved'], ['V4','declared-scope','hold-unresolved']]
    parts = [p.strip() for p in signature.split(',')]
    if len(parts) != (4 if kind == 'transfer' else 2): raise ValueError('Malformed source signature')
    pairs = [(parts[0],parts[1]),(parts[2],parts[3])] if kind == 'transfer' else [(p,'declared-scope') for p in parts]
    factors = {'Φ₅':'Phi5', 'V₄':'V4'}
    return [[factors[term[1:]], bearer, {'+':'increase','−':'decrease'}[term[0]]] for term,bearer in pairs]


def catalogue(root: Path = ROOT) -> dict:
    sources = {}
    for path, expected in PINS.items():
        raw = (root / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f"Source drift: {path}; review required, no automatic re-pin")
        sources[path] = raw.decode("utf-8")
    joined = bound_rows(sources)
    if len(RECORDS) != 7 or {r[0] for r in RECORDS} != set(joined):
        raise ValueError('Missing source signature or ID: exact seven-key set required')
    operators = []
    for key, plain, alias, signature, kind, location, explanation, clauses in RECORDS:
        source_plain, source_alias, source_signature, source_kind, seat = joined[key]
        if (plain,alias,signature,kind) != (source_plain,source_alias,source_signature,source_kind):
            raise ValueError(f'Source row binding mismatch: {key}')
        if clauses != signature_clauses(source_signature, source_kind):
            raise ValueError(f'Source clause binding mismatch: {key}')
        operators.append({
            "schema": "emergentism/OperatorEquation.v1", "id": f"G7@1:{key}",
            "plain": plain, "alias": alias, "kind": kind,
            "expressionKind": "source-direction-signature", "expression": signature,
            "tier": "[S] vocabulary / [I] interpretation", "status": "INTENDED_NOT_OBSERVED",
            "units": None, "magnitude": None, "outcomeEvidence": None,
            "clauses": [{"factor": f, "bearer": b, "direction": d} for f,b,d in clauses],
            "variables": {"Phi5": "possible power; modeled through a present Eval4 token", "V4": "actual usable capability"},
            "domain": "declared ordered domains; no cross-factor arithmetic",
            "requiredContext": ["bearer identities", "horizon", "model token", "comparison contract", "consent", "authority", "costs", "outcome receipt"],
            "missingContext": ["all instance-specific context"] + (["frame bearer scope"] if kind == "frame" else []) + (["hold comparison or defended tolerance"] if key == "vishnu_preserve" else []),
            "assumptions": ["signs indicate direction, not numeric deltas", "no conservation or exchange rate inferred", "a signature is not a moral verdict"],
            "gen7Projection": {"seat": f"GEN7@1:{seat}", "tier": "[I]", "identity": False, "chartSample": None},
            "displayProjection": {"location": location, "tier": "[I]", "selectingMovesCoordinates": False},
            "source": {"path": G7, "section": "3. Four transfers" if kind == "transfer" else "4. Three frames", "sha256": PINS[G7]},
            "idSource": {"path": ROWS, "section": "1. The row", "sha256": PINS[ROWS]},
            "explanation": explanation,
        })
    return {
        "schema": "emergentism/BurrisphereOperatorCatalogue.v1", "identity": "• < ⊙ > ○",
        "scope": "derived inspector, not an empirical evaluator or new doctrine",
        "sources": [{"path": p, "sha256": h} for p,h in PINS.items()],
        "partition": {"transfers": 4, "frames": 3, "countStatus": "conditional vocabulary construction", "orderStatus": "not derived", "strongEmergenceStatus": "not established"},
        "operators": operators,
    }


def render(data: dict) -> str:
    esc = html.escape
    blocks = [START, '<div class="bi-equation-list">']
    for row in data["operators"]:
        key = row["id"].split(":", 1)[1]
        scope = "self and other must be identified" if row["kind"] == "transfer" else "bearer scope must be declared; this is a frame, not an actor"
        blocks.extend([
            f'<details class="bi-equation" id="{key}" data-operator="{key}">',
            f'<summary><span>{esc(row["plain"])}</span><strong>{esc(row["alias"])}</strong></summary>',
            f'<div class="bi-equation__body"><p class="bi-equation__type">{esc(row["kind"])} · [S] vocabulary · [I] reading</p>',
            f'<p class="bi-equation__signature"><code>{esc(row["expression"])}</code></p>',
            f'<p>{esc(row["explanation"])}</p>',
            f'<p class="bi-equation__scope">{esc(scope)}. Signs describe intended direction, not measured deltas or an exchange rate.</p>',
            f'<p class="bi-equation__seat">{esc(row["id"])}<br>{esc(row["gen7Projection"]["seat"])} · interpretive correspondence, not identity or a sphere latitude.</p>',
            f'<p class="bi-equation__source">Source: G7 §{3 if row["kind"] == "transfer" else 4} · <a href="/{DATA}">source hashes and machine record</a></p>',
            '</div></details>',
        ])
    blocks.extend(['</div>', '<p class="bi-inspector__fence">No rule is a verdict about a person. Bearers, consent, authority, costs and observed outcomes remain separate. Titan glyphs are not arithmetic operands.</p>', END])
    return "\n".join(blocks)


def schema_document() -> dict:
    source = {"type":"object", "required":["path","section","sha256"], "additionalProperties":False,
              "properties":{"path":{"enum":[G7,ROWS]}, "section":{"type":"string"},
                            "sha256":{"type":"string","pattern":"^[0-9a-f]{64}$"}}}
    properties = {
        "schema":{"const":"emergentism/OperatorEquation.v1"},
        "id":{"enum":[f'G7@1:{r[0]}' for r in RECORDS]},
        "kind":{"enum":["transfer","frame"]},
        "expressionKind":{"const":"source-direction-signature"},
        "status":{"const":"INTENDED_NOT_OBSERVED"},
        **{key:{"type":"null"} for key in ("units","magnitude","outcomeEvidence")},
        **{key:{"type":"string","minLength":1} for key in ("plain","alias","expression","tier","domain","explanation")},
        **{key:{"type":"array","minItems":1,"items":{"type":"string"}} for key in ("requiredContext","missingContext","assumptions")},
        "clauses":{"type":"array","minItems":2,"maxItems":2,"items":{
            "type":"object","additionalProperties":False,"required":["factor","bearer","direction"],
            "properties":{"factor":{"enum":["Phi5","V4"]},"bearer":{"enum":["self","other","declared-scope"]},
                          "direction":{"enum":["increase","decrease","hold-unresolved"]}}}},
        "variables":{"type":"object","required":["Phi5","V4"],"additionalProperties":False,
                     "properties":{"Phi5":{"type":"string"},"V4":{"type":"string"}}},
        "gen7Projection":{"type":"object","required":["seat","tier","identity","chartSample"],"additionalProperties":False,
                          "properties":{"seat":{"type":"string","pattern":"^GEN7@1:L[1-7]$"},"tier":{"const":"[I]"},"identity":{"const":False},"chartSample":{"type":"null"}}},
        "displayProjection":{"type":"object","required":["location","tier","selectingMovesCoordinates"],"additionalProperties":False,
                             "properties":{"location":{"enum":["top-left","bottom-left","bottom-right","top-right","top","bottom","centre"]},"tier":{"const":"[I]"},"selectingMovesCoordinates":{"const":False}}},
        "source":source,"idSource":source,
    }
    return {"$schema":"https://json-schema.org/draft/2020-12/schema",
            "$id":"https://emergentism.org/"+SCHEMA,
            "title":"Burrisphere operator catalogue: syntax only; source-row binding is checked by the builder",
            "type":"object","additionalProperties":False,"required":["schema","identity","scope","sources","partition","operators"],
            "properties":{"schema":{"const":"emergentism/BurrisphereOperatorCatalogue.v1"},
                          "identity":{"const":"• < ⊙ > ○"},
                          "scope":{"const":"derived inspector, not an empirical evaluator or new doctrine"},
                          "sources":{"type":"array","minItems":4,"maxItems":4,"uniqueItems":True,
                                     "items":{"type":"object","additionalProperties":False,"required":["path","sha256"],
                                              "properties":{"path":{"enum":list(PINS)},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$"}}}},
                          "partition":{"type":"object","additionalProperties":False,
                                       "required":["transfers","frames","countStatus","orderStatus","strongEmergenceStatus"],
                                       "properties":{"transfers":{"const":4},"frames":{"const":3},
                                                     "countStatus":{"const":"conditional vocabulary construction"},
                                                     "orderStatus":{"const":"not derived"},"strongEmergenceStatus":{"const":"not established"}}},
                          "operators":{"type":"array","minItems":7,"maxItems":7,"items":{"$ref":"#/$defs/operator"}}},
            "$defs":{"operator":{"type":"object","additionalProperties":False,
                                 "required":list(properties),"properties":properties}}}


def build(*, check: bool = False, site: Path = SITE, root: Path = ROOT) -> None:
    data = catalogue(root)
    original = (site / PAGE).read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1 or original.index(END) < original.index(START):
        raise ValueError("Exactly one ordered inspector marker pair required")
    updated = original[:original.index(START)] + render(data) + original[original.index(END)+len(END):]
    outputs = {PAGE: updated, DATA: json.dumps(data, ensure_ascii=False, indent=2)+"\n",
               SCHEMA: json.dumps(schema_document(), ensure_ascii=False, indent=2)+"\n"}
    if check:
        for path, content in outputs.items():
            if not (site/path).is_file() or (site/path).read_text(encoding="utf-8") != content:
                raise ValueError(f"Generated inspector drift: {path}")
    else:
        for path, content in outputs.items():
            (site/path).parent.mkdir(parents=True, exist_ok=True)
            (site/path).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build(check=args.check)
    print("Burrisphere: seven source-pinned rules " + ("verified" if args.check else "generated"))

"""W7 D1–D4 force-assignment catalog and scoring lock (v2.2).

Worktree harness only. No candidate is scored as physics. Founder-prior
agreement is recorded and contributes zero points.
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
from typing import Any, Mapping

REGISTERS = ("D1", "D2", "D3", "D4")
FORCES = ("S", "E", "W", "G")
FOUNDER_PRIOR_TUPLE = ("S", "E", "W", "G")
FOUNDER_PRIOR_ID = "W7-4P-SEWG"

PACKET_GATES = (
    "native_recovery",
    "force_specific_physics",
    "held_out_observable",
    "permutation_contrast",
    "rival_comparison",
)

LEG_PHYSICS = {
    "S": (
        "QCD color",
        "non-Abelian SU(3)",
        "confinement or declared confinement-adjacent observable",
    ),
    "E": (
        "U(1) or Maxwell/QED structure",
        "charge/current coupling",
        "electromagnetic-specific observable",
    ),
    "W": (
        "chirality",
        "parity violation",
        "flavor change",
        "electroweak structure SU(2)_L x U(1)_Y",
    ),
    "G": (
        "general relativity in a declared domain",
        "valid low-energy quantum-gravity EFT where applicable",
    ),
}

INSUFFICIENT_FOR_WEAK = (
    "generic quantum state",
    "amplitude without chirality",
    "Hilbert space alone",
    "path integral alone",
    "superposition alone",
    "measurement context alone",
    "all forces are quantum",
)

RIVALS = (
    {
        "id": "R-NOMAP",
        "kind": "no-mapping",
        "statement": "Standard Model plus GR/EFT with no Emergentist D-placement.",
    },
    {
        "id": "R-M2M",
        "kind": "many-to-many",
        "statement": "Several D-type structures may be relevant to one interaction.",
    },
    {
        "id": "R-EWJ",
        "kind": "electroweak-joint",
        "statement": (
            "Low-energy E/W separation need not mean two serial D-stages; "
            "electromagnetic and weak legs may be jointly electroweak."
        ),
    },
)

F5_FORK = {
    "truth_bonus": 0,
    "arms": (
        {
            "id": "F5-W",
            "kind": "present modeled futures",
            "statement": (
                "Represented futures reweight present action through actual "
                "present models, signals, memories, institutions, and computations."
            ),
        },
        {
            "id": "F5-N",
            "kind": "D5 verification/controller null",
            "statement": (
                "No additional interaction couples to representation-as-such; "
                "selection, verification, correction, and revision service the "
                "D5 register."
            ),
        },
        {
            "id": "F5-R",
            "kind": "candidate future-boundary history law",
            "statement": (
                "An actual D4 history-selection law indexed by declared later "
                "boundary data and a D5 option functional may alter present "
                "transition probabilities."
            ),
        },
    ),
}


def assignment_id(mapping: tuple[str, str, str, str]) -> str:
    return "W7-4P-" + "".join(mapping)


def bijection_assignments() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mapping in permutations(FORCES):
        row = {
            "id": assignment_id(mapping),
            "kind": "bijection",
            "map": dict(zip(REGISTERS, mapping)),
            "tuple": mapping,
            "is_founder_prior": mapping == FOUNDER_PRIOR_TUPLE,
            "prior_status": "PRIOR_ONLY" if mapping == FOUNDER_PRIOR_TUPLE else None,
        }
        rows.append(row)
    return rows


def rival_universe() -> list[dict[str, Any]]:
    return [dict(item) for item in RIVALS]


def comparison_universe() -> list[dict[str, Any]]:
    return bijection_assignments() + rival_universe()


def founder_prior() -> dict[str, Any]:
    mapping = FOUNDER_PRIOR_TUPLE
    return {
        "id": FOUNDER_PRIOR_ID,
        "map": dict(zip(REGISTERS, mapping)),
        "tuple": mapping,
        "status": "PRIOR_ONLY",
        "agreement_score": 0,
    }


def weak_gate_requirements() -> dict[str, Any]:
    return {
        "required": list(LEG_PHYSICS["W"]),
        "insufficient": list(INSUFFICIENT_FOR_WEAK),
        "placement": "D3->W",
    }


def _gate_value(packet: Mapping[str, Any], gate: str) -> bool:
    value = packet.get(gate, False)
    return bool(value)


def score_packet(assignment: Mapping[str, str] | tuple[str, ...], packet: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Diagnostic tally from packet gates only.

    Matching the founder prior never increments the score. An
    ``agrees_with_founder`` flag is ignored. F5 preference never increments
    the score. ``truth_bonus`` is always 0.
    """
    packet = packet or {}
    if isinstance(assignment, Mapping):
        mapping = tuple(assignment[register] for register in REGISTERS)
    else:
        mapping = tuple(assignment)

    tally = 0
    earned: list[str] = []
    for gate in PACKET_GATES:
        if _gate_value(packet, gate):
            tally += 1
            earned.append(gate)

    founder_match = mapping == FOUNDER_PRIOR_TUPLE
    # Locked: these remain zero even if the packet claims them.
    founder_agreement_points = 0
    f5_truth_bonus = 0
    if packet.get("agrees_with_founder") or packet.get("founder_bonus"):
        founder_agreement_points = 0
    if packet.get("truth_bonus") or packet.get("f5_preferred"):
        f5_truth_bonus = 0

    return {
        "candidate_id": assignment_id(mapping) if set(mapping) == set(FORCES) and len(mapping) == 4 else "non-bijective",
        "score": tally,
        "earned_gates": earned,
        "founder_match": founder_match,
        "founder_agreement_points": founder_agreement_points,
        "truth_bonus": f5_truth_bonus,
        "prior_status": "PRIOR_ONLY" if founder_match else None,
    }


def protocol_corpus_paths() -> list[Path]:
    here = Path(__file__).resolve().parent
    prereg = here.parent / "05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md"
    paths = [prereg]
    for path in sorted(here.iterdir()):
        if not path.is_file():
            continue
        if path.name.startswith("test_"):
            continue
        if path.suffix in {".md", ".py", ".json"}:
            paths.append(path)
    return paths


def catalog_payload() -> dict[str, Any]:
    return {
        "schema": "emergentism/force_assignment_v22",
        "protocol_id": "W7-4P-PREREG-v2.2",
        "assignments": bijection_assignments(),
        "rivals": rival_universe(),
        "founder_prior": founder_prior(),
        "leg_physics": LEG_PHYSICS,
        "weak_gate": weak_gate_requirements(),
        "f5_fork": {
            "truth_bonus": F5_FORK["truth_bonus"],
            "arms": [dict(arm) for arm in F5_FORK["arms"]],
        },
    }


def write_catalog(path: Path | None = None) -> Path:
    target = path or Path(__file__).resolve().parent / "catalog.json"
    payload = {
        "schema": catalog_payload()["schema"],
        "protocol_id": catalog_payload()["protocol_id"],
        "founder_prior": {
            "id": FOUNDER_PRIOR_ID,
            "map": dict(zip(REGISTERS, FOUNDER_PRIOR_TUPLE)),
            "status": "PRIOR_ONLY",
            "agreement_score": 0,
        },
        "rivals": [{"id": r["id"], "kind": r["kind"]} for r in RIVALS],
        "f5_fork": {
            "truth_bonus": 0,
            "arms": [
                {"id": arm["id"], "kind": arm["kind"]} for arm in F5_FORK["arms"]
            ],
        },
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    rows = bijection_assignments()
    print(f"bijections={len(rows)} rivals={len(RIVALS)} f5_arms={len(F5_FORK['arms'])}")
    print(f"founder={FOUNDER_PRIOR_ID} prior_only=1 agreement_score=0")

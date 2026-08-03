from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

from .codec import text_hash
from .diagnostics import Issue


RECEIPT_IDENTITIES = {
    "A": (
        "REC-A-108",
        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md",
        (),
    ),
    "B": (
        "REC-B-109",
        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
        ("REC-A-108",),
    ),
    "C": (
        "REC-C-110",
        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md",
        ("REC-A-108", "REC-B-109"),
    ),
}
RECEIPT_PHASE = {identity[0]: phase for phase, identity in RECEIPT_IDENTITIES.items()}
PHASE_RANK = {"A": 0, "B": 1, "C": 2}
SOURCE_ROLE_MATRIX = {
    "OWNER": frozenset({"SEMANTIC_OWNER"}),
    "SUPPORT": frozenset({"EVIDENCE", "PROVENANCE"}),
    "COMPRESSION": frozenset({"DERIVATIVE"}),
    "PUBLIC": frozenset({"DERIVATIVE"}),
    "RECEIPT": frozenset({"PROVENANCE"}),
}
PHASE_A_REQUIREMENTS = {
    "REQ-A-PROTOCOL-SELF-TRIAL": (
        "00_META/00_THE_KINTSUGI_PROTOCOL.md",
        "# The Kintsugi Protocol",
        "sha256-text-lf:9fe68c734bce6c709c5879e0f7e40b552cdacb4cd14121302371509fb13f7cc9",
    ),
    "REQ-A-TRIADIC-UNIQUENESS": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/11_EFR_TRIADIC_STABILITY.md",
        "## The Uniqueness Theorem",
        "sha256-text-lf:438269d12273e6c169e2ba8bdb8c126dcb118378a1d28a55328aa4dbdaec17b8",
    ),
    "REQ-A-D6-AREA-DIRECTION": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
        "### 2.2 The Coordinate Collapse Theorem",
        "sha256-text-lf:75893a2cd097580c3ee44a8a62f940e9b02d3dc09e4d73a5d3796e70de7d8e26",
    ),
    "REQ-A-POWER-MAX-CIRCULARITY": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
        "## The Statement",
        "sha256-text-lf:8cb12ae6fb3b855cbe999d699041ae3a15c73d3c405362195f6bf58441019510",
    ),
    "REQ-A-D4-D5-REGISTER": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "## I. THE FUNDAMENTAL DISTINCTION",
        "sha256-text-lf:dee381fece54b4fe926b1af1145ab8676263091cc698460a3b37962c77a6cca2",
    ),
    "REQ-A-QUANTUM-MEASURE": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
        "## The Corrected Formula",
        "sha256-text-lf:41b8437a8e8715a7be6f8f7ddef46984b89757d9f9722494b554dc3e87d204fb",
    ),
    "REQ-A-OPTION-CONE": (
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "### Worldline and Light-Cone Corollary",
        "sha256-text-lf:6749c86499b1e5d1a04de8afcbc6df283403617f1d0e40bdf9dbe66073412527",
    ),
}


GLOBAL_COLLECTIONS = (
    "manifests",
    "sources",
    "claims",
    "trials",
    "seams",
    "antibodies",
    "discriminators",
    "fixtures",
    "propagations",
    "phaseReceipts",
    "reviewAttempts",
    "reviewAttestations",
    "reviewFindings",
    "reviewFindingDispositions",
)
CORE_RECORD_COLLECTIONS = GLOBAL_COLLECTIONS + ("reviewAttemptArtifacts",)


def malformed_core_issue() -> Issue:
    return issue(
        "core",
        "KIN-E-REF",
        "core record validation failed safely on malformed nested data",
    )


def core_record_shape_issues(core: Any) -> list[Issue]:
    if not isinstance(core, dict):
        return [issue("core", "KIN-E-REF", "core data must be an object")]
    result: list[Issue] = []
    if not isinstance(core.get("program"), dict):
        result.append(issue(
            "core.program",
            "KIN-E-REF",
            "program must be an object",
        ))
    for collection in CORE_RECORD_COLLECTIONS:
        value = core.get(collection)
        if not isinstance(value, list):
            result.append(issue(
                f"core.{collection}",
                "KIN-E-REF",
                f"{collection} must be a list of objects",
            ))
        elif any(not isinstance(record, dict) for record in value):
            result.append(issue(
                f"core.{collection}",
                "KIN-E-REF",
                f"{collection} must contain only objects",
            ))
    return ordered_issues(result)


def ordered_issues(issues: Iterable[Issue]) -> list[Issue]:
    return sorted(set(issues))


def issue(path: str, code: str, message: str) -> Issue:
    return Issue(path, code, message)


def items(core: dict[str, Any], name: str) -> list[dict[str, Any]]:
    value = core.get(name, [])
    if not isinstance(value, list):
        return []
    return [record for record in value if isinstance(record, dict)]


def valid_id(value: Any) -> bool:
    if not isinstance(value, str) or not value or not ("A" <= value[0] <= "Z"):
        return False
    return all(
        "A" <= character <= "Z"
        or "0" <= character <= "9"
        or character in "_-"
        for character in value
    )


def canonical_attempt(value: Any, phase: Any) -> bool:
    if not isinstance(value, str) or not isinstance(phase, str):
        return False
    parts = value.split("-")
    if len(parts) != 3 or parts[:2] != ["RVA", phase]:
        return False
    digits = parts[2]
    if not digits or any(character not in "0123456789" for character in digits):
        return False
    if len(digits) < 3 or not any(character != "0" for character in digits):
        return False
    return len(digits) == 3 or digits[0] != "0"


def attempt_paths(attempt_id: str) -> tuple[str, str, str, str]:
    return (
        f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/review_target.json",
        f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_LOGIC.md",
        f"11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{attempt_id}_BTJ.md",
        f"09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{attempt_id}/validation_bundle.json",
    )


def _index_global_ids(core: dict[str, Any]) -> tuple[dict[str, tuple[str, dict[str, Any]]], list[Issue]]:
    index: dict[str, tuple[str, dict[str, Any]]] = {}
    result: list[Issue] = []
    for collection in GLOBAL_COLLECTIONS:
        for position, record in enumerate(items(core, collection)):
            path = f"core.{collection}[{position}].id"
            record_id = record.get("id")
            if not valid_id(record_id):
                result.append(issue(path, "KIN-E-ID", "record ID is malformed"))
                continue
            if record_id == "LEDGER-PREAMBLE":
                result.append(issue(path, "KIN-E-ID", "LEDGER-PREAMBLE is reserved for the ledger preamble projection"))
            if record_id in index:
                prior_collection, _ = index[record_id]
                result.append(issue(path, "KIN-E-ID", f"global ID duplicates a {prior_collection} record: {record_id}"))
            else:
                index[record_id] = (collection, record)
    return index, result


def _collection_index(core: dict[str, Any], collection: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in items(core, collection):
        record_id = record.get("id")
        if isinstance(record_id, str) and record_id not in result:
            result[record_id] = record
    return result


def _require_ref(
    result: list[Issue], path: str, value: Any, index: dict[str, dict[str, Any]], kind: str
) -> dict[str, Any] | None:
    if not isinstance(value, str) or value not in index:
        result.append(issue(path, "KIN-E-REF", f"reference does not resolve to {kind}: {value!r}"))
        return None
    return index[value]


def _canonical_cycle(nodes: list[str]) -> tuple[str, ...]:
    ring = nodes[:-1]
    if not ring:
        return tuple(nodes)
    minimum_index = min(range(len(ring)), key=ring.__getitem__)
    chosen = tuple(ring[minimum_index:]) + tuple(ring[:minimum_index])
    return chosen + (chosen[0],)


def _graph_cycle_issues(graph: dict[str, set[str]]) -> list[Issue]:
    states: dict[str, int] = {}
    found: set[tuple[str, ...]] = set()
    result: list[Issue] = []
    for start in sorted(graph):
        if states.get(start, 0) != 0:
            continue
        states[start] = 1
        active = [start]
        positions = {start: 0}
        stack: list[tuple[str, Any]] = [
            (start, iter(sorted(graph.get(start, ()))))
        ]
        while stack:
            node, targets = stack[-1]
            try:
                target = next(targets)
            except StopIteration:
                stack.pop()
                states[node] = 2
                positions.pop(node, None)
                active.pop()
                continue
            if target not in graph:
                continue
            state = states.get(target, 0)
            if state == 0:
                states[target] = 1
                positions[target] = len(active)
                active.append(target)
                stack.append((target, iter(sorted(graph.get(target, ())))))
            elif state == 1:
                cycle = _canonical_cycle(active[positions[target]:] + [target])
                if cycle not in found:
                    found.add(cycle)
                    result.append(issue(
                        f"core.claims[{cycle[0]}]",
                        "KIN-E-CYCLE",
                        "claim dependency/support cycle: " + " -> ".join(cycle),
                    ))
    return result


def _validate_source_roles(core: dict[str, Any]) -> list[Issue]:
    result: list[Issue] = []
    canonical_receipt_paths = {
        identity[1] for identity in RECEIPT_IDENTITIES.values()
    }
    for index, source in enumerate(items(core, "sources")):
        allowed = SOURCE_ROLE_MATRIX.get(source.get("kind"), frozenset())
        if source.get("authorityRole") not in allowed:
            result.append(issue(
                f"core.sources[{index}].authorityRole",
                "KIN-E-REF",
                "source kind/authority role pairing is forbidden",
            ))
        if source.get("path") in canonical_receipt_paths:
            result.append(issue(
                f"core.sources[{index}].path",
                "KIN-E-REF",
                "source path aliases a canonical phase receipt",
            ))
    return result


def _validate_claim_graph(core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[Issue]:
    result: list[Issue] = []
    claims = indexes["claims"]
    sources = indexes["sources"]
    graph = {claim_id: set() for claim_id in claims}
    dependency_graph = {claim_id: set() for claim_id in claims}

    for position, claim in enumerate(items(core, "claims")):
        base = f"core.claims[{position}]"
        claim_id = claim.get("id")
        owner = _require_ref(result, f"{base}.ownerSourceId", claim.get("ownerSourceId"), sources, "source")
        if owner is not None and (
            owner.get("kind") != "OWNER" or owner.get("authorityRole") != "SEMANTIC_OWNER"
        ):
            result.append(issue(f"{base}.ownerSourceId", "KIN-E-REF", "claim owner must be OWNER/SEMANTIC_OWNER"))

        premise_ids: set[str] = set()
        for p_index, premise in enumerate(claim.get("premises", [])):
            if not isinstance(premise, dict):
                continue
            premise_id = premise.get("id")
            if premise_id in premise_ids:
                result.append(issue(f"{base}.premises[{p_index}].id", "KIN-E-ID", "premise ID is duplicated inside the claim"))
            elif isinstance(premise_id, str):
                premise_ids.add(premise_id)
            for s_index, source_id in enumerate(premise.get("sourceIds", [])):
                source = _require_ref(result, f"{base}.premises[{p_index}].sourceIds[{s_index}]", source_id, sources, "source")
                if source is not None and source.get("authorityRole") not in {"SEMANTIC_OWNER", "EVIDENCE"}:
                    result.append(issue(
                        f"{base}.premises[{p_index}].sourceIds[{s_index}]",
                        "KIN-E-REF",
                        "provenance or derivative source cannot serve as a premise warrant",
                    ))

        term_pairs: set[tuple[Any, Any]] = set()
        for t_index, term in enumerate(claim.get("typedTerms", [])):
            if not isinstance(term, dict):
                continue
            pair = (term.get("symbol"), term.get("semanticRegister"))
            if pair in term_pairs:
                result.append(issue(
                    f"{base}.typedTerms[{t_index}]",
                    "KIN-E-ID",
                    "typed term duplicates the semantic (symbol, register) pair",
                ))
            term_pairs.add(pair)

        dependencies = claim.get("dependencyClaimIds", [])
        dependency_set: set[str] = set()
        for d_index, dependency_id in enumerate(dependencies):
            dependency = _require_ref(result, f"{base}.dependencyClaimIds[{d_index}]", dependency_id, claims, "claim")
            if dependency is not None and isinstance(claim_id, str):
                dependency_set.add(dependency_id)
                graph[claim_id].add(dependency_id)
                dependency_graph[claim_id].add(dependency_id)

        link_ids: set[str] = set()
        support_targets: set[str] = set()
        for s_index, link in enumerate(claim.get("supportLinks", [])):
            if not isinstance(link, dict):
                continue
            link_id = link.get("id")
            target = link.get("supportingClaimId")
            if link_id in link_ids:
                result.append(issue(f"{base}.supportLinks[{s_index}].id", "KIN-E-ID", "support-link ID is duplicated inside the claim"))
            elif isinstance(link_id, str):
                link_ids.add(link_id)
            resolved = _require_ref(result, f"{base}.supportLinks[{s_index}].supportingClaimId", target, claims, "claim")
            if resolved is not None and isinstance(claim_id, str):
                if target == claim_id:
                    result.append(issue(f"{base}.supportLinks[{s_index}]", "KIN-E-REF", "self-support is forbidden"))
                if target in support_targets:
                    result.append(issue(f"{base}.supportLinks[{s_index}]", "KIN-E-REF", "duplicate support edge is forbidden"))
                if target in dependency_set:
                    result.append(issue(f"{base}.supportLinks[{s_index}]", "KIN-E-REF", "one claim cannot be both dependency and support endpoint"))
                support_targets.add(target)
                graph[claim_id].add(target)

        if isinstance(claim_id, str):
            for s_index, survivor in enumerate(claim.get("survivingIfKilled", {}).get("claimIds", [])):
                if _require_ref(result, f"{base}.survivingIfKilled.claimIds[{s_index}]", survivor, claims, "claim") is None:
                    continue
                if survivor == claim_id:
                    result.append(issue(f"{base}.survivingIfKilled.claimIds[{s_index}]", "KIN-E-CYCLE", "a claim cannot survive itself"))

    result.extend(_graph_cycle_issues(graph))

    for position, claim in enumerate(items(core, "claims")):
        killed = claim.get("id")
        if not isinstance(killed, str):
            continue
        for s_index, survivor in enumerate(claim.get("survivingIfKilled", {}).get("claimIds", [])):
            if survivor not in dependency_graph:
                continue
            pending = [survivor]
            seen: set[str] = set()
            while pending:
                current = pending.pop()
                if current in seen:
                    continue
                seen.add(current)
                if current == killed:
                    result.append(issue(
                        f"core.claims[{position}].survivingIfKilled.claimIds[{s_index}]",
                        "KIN-E-CYCLE",
                        "surviving claim transitively depends on the killed claim",
                    ))
                    break
                pending.extend(sorted(dependency_graph.get(current, ()), reverse=True))
    return result


def _validate_references(core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[Issue]:
    result: list[Issue] = []
    claims = indexes["claims"]
    manifests = indexes["manifests"]
    receipts = indexes["phaseReceipts"]
    seams = indexes["seams"]
    sources = indexes["sources"]
    discriminators = indexes["discriminators"]
    antibodies = indexes["antibodies"]
    fixtures = indexes["fixtures"]
    trials_by_seam: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trial in items(core, "trials"):
        seam_id = trial.get("seamId")
        if isinstance(seam_id, str):
            trials_by_seam[seam_id].append(trial)

    for position, trial in enumerate(items(core, "trials")):
        base = f"core.trials[{position}]"
        tried_quote = trial.get("triedQuote")
        tried_hash = trial.get("triedHash")
        if isinstance(tried_quote, str) and isinstance(tried_hash, str):
            try:
                computed_tried_hash = text_hash(tried_quote)
            except UnicodeError:
                computed_tried_hash = None
            if computed_tried_hash != tried_hash:
                result.append(issue(
                    f"{base}.triedHash",
                    "KIN-E-RECEIPT",
                    "tried quote does not recompute to its declared text hash",
                ))
        trial_claim = _require_ref(result, f"{base}.claimId", trial.get("claimId"), claims, "claim")
        trial_manifest = _require_ref(result, f"{base}.manifestId", trial.get("manifestId"), manifests, "manifest")
        trial_receipt = _require_ref(result, f"{base}.receiptId", trial.get("receiptId"), receipts, "phase receipt")
        if trial_receipt is not None and trial.get("id") not in trial_receipt.get("trialIds", []):
            result.append(issue(f"{base}.receiptId", "KIN-E-REF", "trial is absent from its owning receipt"))
        if trial_receipt is not None and trial_manifest is not None and (
            trial_receipt.get("manifestId") != trial.get("manifestId")
            or trial_receipt.get("phase") != trial_manifest.get("phase")
        ):
            result.append(issue(
                f"{base}.manifestId",
                "KIN-E-REF",
                "trial manifest and receipt must be the same-phase ownership tuple",
            ))
        if trial_receipt is not None and trial_claim is not None and (
            trial.get("claimId") not in trial_receipt.get("claimIds", [])
        ):
            result.append(issue(
                f"{base}.claimId",
                "KIN-E-REF",
                "trial claim is absent from its owning receipt",
            ))
        if trial_manifest is not None and trial_claim is not None:
            excluded_claim_ids = {
                exclusion.get("claimId")
                for exclusion in trial_manifest.get("excludedClaimIds", [])
                if isinstance(exclusion, dict)
            }
            if (
                trial.get("claimId") not in trial_manifest.get("harvestedClaimIds", [])
                or trial.get("claimId") not in trial_manifest.get("trialedClaimIds", [])
                or trial.get("claimId") in excluded_claim_ids
            ):
                result.append(issue(
                    f"{base}.claimId",
                    "KIN-E-REF",
                    "trial claim must be harvested, trialed, and not excluded by its manifest",
                ))
        seam_id = trial.get("seamId")
        if seam_id is not None:
            seam = _require_ref(result, f"{base}.seamId", seam_id, seams, "seam")
            if seam is not None and (
                seam.get("claimId") != trial.get("claimId")
                or seam.get("receiptId") != trial.get("receiptId")
            ):
                result.append(issue(
                    f"{base}.seamId",
                    "KIN-E-REF",
                    "trial seam must preserve the trial claim and receipt identity",
                ))
        for index, value in enumerate(trial.get("discriminatorIds", [])):
            _require_ref(result, f"{base}.discriminatorIds[{index}]", value, discriminators, "discriminator")

    for position, seam in enumerate(items(core, "seams")):
        base = f"core.seams[{position}]"
        seam_claim = _require_ref(result, f"{base}.claimId", seam.get("claimId"), claims, "claim")
        owner = _require_ref(result, f"{base}.ownerSource", seam.get("ownerSource"), sources, "source")
        if owner is not None and owner.get("authorityRole") != "SEMANTIC_OWNER":
            result.append(issue(f"{base}.ownerSource", "KIN-E-REF", "seam owner must be a semantic owner"))
        if seam_claim is not None and (
            seam.get("ownerSource") != seam_claim.get("ownerSourceId")
            or seam.get("ownerAnchor") != seam_claim.get("ownerAnchor")
        ):
            result.append(issue(
                f"{base}.ownerSource",
                "KIN-E-REF",
                "seam owner identity and anchor must match its tried claim",
            ))
        seam_id = seam.get("id")
        owning_trials = trials_by_seam.get(seam_id, []) if isinstance(seam_id, str) else []
        if len(owning_trials) != 1:
            result.append(issue(
                base,
                "KIN-E-REF",
                "seam must have exactly one owning trial",
            ))
        else:
            owning_trial = owning_trials[0]
            if (
                owning_trial.get("claimId") != seam.get("claimId")
                or owning_trial.get("receiptId") != seam.get("receiptId")
                or owning_trial.get("triedQuote") != seam.get("beforeQuote")
                or owning_trial.get("triedHash") != seam.get("beforeHash")
            ):
                result.append(issue(
                    base,
                    "KIN-E-REF",
                    "seam frozen quote and hash must match its owning trial/claim/receipt tuple",
                ))
        term_pairs: set[tuple[Any, Any]] = set()
        for index, term in enumerate(seam.get("typedTerms", [])):
            if not isinstance(term, dict):
                continue
            pair = (term.get("symbol"), term.get("semanticRegister"))
            if pair in term_pairs:
                result.append(issue(
                    f"{base}.typedTerms[{index}]",
                    "KIN-E-ID",
                    "seam typed term duplicates the semantic (symbol, register) pair",
                ))
            term_pairs.add(pair)
        for field, target_index, label in (
            ("sourceIds", sources, "source"),
            ("dependencyClaimIds", claims, "claim"),
            ("priorSeamIds", seams, "seam"),
            ("regressionFixtureIds", fixtures, "fixture"),
            ("discriminatorIds", discriminators, "discriminator"),
        ):
            for index, value in enumerate(seam.get(field, [])):
                resolved = _require_ref(result, f"{base}.{field}[{index}]", value, target_index, label)
                if field == "sourceIds" and resolved is not None and resolved.get("authorityRole") not in {"SEMANTIC_OWNER", "EVIDENCE"}:
                    result.append(issue(
                        f"{base}.{field}[{index}]", "KIN-E-REF",
                        "provenance or derivative source cannot serve as a seam warrant",
                    ))
                if (
                    field == "discriminatorIds"
                    and resolved is not None
                    and resolved.get("claimId") != seam.get("claimId")
                ):
                    result.append(issue(
                        f"{base}.{field}[{index}]",
                        "KIN-E-REF",
                        "seam discriminator belongs to another claim",
                    ))
        seam_receipt = _require_ref(result, f"{base}.receiptId", seam.get("receiptId"), receipts, "phase receipt")
        if seam_receipt is not None and seam.get("id") not in seam_receipt.get("seamIds", []):
            result.append(issue(f"{base}.receiptId", "KIN-E-REF", "seam is absent from its owning receipt"))
        for field in ("priorSupportLinks", "supportLinks"):
            link_ids: set[str] = set()
            for index, link in enumerate(seam.get(field, [])):
                if isinstance(link, dict):
                    link_id = link.get("id")
                    if isinstance(link_id, str):
                        if link_id in link_ids:
                            result.append(issue(
                                f"{base}.{field}[{index}].id",
                                "KIN-E-ID",
                                "support-link ID is duplicated inside the seam claim projection",
                            ))
                        link_ids.add(link_id)
                    _require_ref(result, f"{base}.{field}[{index}].supportingClaimId", link.get("supportingClaimId"), claims, "claim")
        for field in ("priorSurvivingIfKilled", "survivingIfKilled"):
            for index, value in enumerate(seam.get(field, {}).get("claimIds", [])):
                _require_ref(result, f"{base}.{field}.claimIds[{index}]", value, claims, "claim")
        containment = seam.get("containment")
        if isinstance(containment, dict):
            for index, value in enumerate(containment.get("antibodyIds", [])):
                _require_ref(result, f"{base}.containment.antibodyIds[{index}]", value, antibodies, "antibody")
            for index, value in enumerate(containment.get("blockedDependencyClaimIds", [])):
                _require_ref(result, f"{base}.containment.blockedDependencyClaimIds[{index}]", value, claims, "claim")

    for position, antibody in enumerate(items(core, "antibodies")):
        base = f"core.antibodies[{position}]"
        _require_ref(result, f"{base}.seamId", antibody.get("seamId"), seams, "seam")
        for field in ("positiveFixtureIds", "negativeFixtureIds", "quotationFixtureIds", "historicalFixtureIds"):
            for index, value in enumerate(antibody.get(field, [])):
                _require_ref(result, f"{base}.{field}[{index}]", value, fixtures, "fixture")

    for position, discriminator in enumerate(items(core, "discriminators")):
        _require_ref(result, f"core.discriminators[{position}].claimId", discriminator.get("claimId"), claims, "claim")

    for position, fixture in enumerate(items(core, "fixtures")):
        base = f"core.fixtures[{position}]"
        for index, value in enumerate(fixture.get("antibodyIds", [])):
            _require_ref(result, f"{base}.antibodyIds[{index}]", value, antibodies, "antibody")
        for index, value in enumerate(fixture.get("expectedAntibodyIds", [])):
            _require_ref(result, f"{base}.expectedAntibodyIds[{index}]", value, antibodies, "antibody")
        for index, value in enumerate(fixture.get("seamIds", [])):
            _require_ref(result, f"{base}.seamIds[{index}]", value, seams, "seam")

    for position, propagation in enumerate(items(core, "propagations")):
        base = f"core.propagations[{position}]"
        _require_ref(result, f"{base}.seamId", propagation.get("seamId"), seams, "seam")
        _require_ref(result, f"{base}.receiptId", propagation.get("receiptId"), receipts, "phase receipt")
        source = _require_ref(result, f"{base}.derivativeSourceId", propagation.get("derivativeSourceId"), sources, "source")
        if source is not None and source.get("authorityRole") != "DERIVATIVE":
            result.append(issue(f"{base}.derivativeSourceId", "KIN-E-REF", "propagation target must be a derivative source"))

    for position, manifest in enumerate(items(core, "manifests")):
        base = f"core.manifests[{position}]"
        for field in ("harvestedClaimIds", "trialedClaimIds"):
            for index, value in enumerate(manifest.get(field, [])):
                _require_ref(result, f"{base}.{field}[{index}]", value, claims, "claim")
        for index, exclusion in enumerate(manifest.get("excludedClaimIds", [])):
            if isinstance(exclusion, dict):
                _require_ref(result, f"{base}.excludedClaimIds[{index}].claimId", exclusion.get("claimId"), claims, "claim")

    return result


def _validate_bindings(core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[Issue]:
    result: list[Issue] = []
    claims = indexes["claims"]
    sources = indexes["sources"]
    receipts = indexes["phaseReceipts"]
    trials_by_claim: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trial in items(core, "trials"):
        if isinstance(trial.get("claimId"), str):
            trials_by_claim[trial["claimId"]].append(trial)

    for position, manifest in enumerate(items(core, "manifests")):
        phase = manifest.get("phase")
        bindings = manifest.get("requiredClaimBindings", [])
        base = f"core.manifests[{position}].requiredClaimBindings"
        if phase != "A":
            if bindings:
                result.append(issue(base, "KIN-E-RECEIPT", "Phase B/C required-claim bindings must be empty"))
            continue
        by_requirement = {binding.get("requirementId"): binding for binding in bindings if isinstance(binding, dict)}
        if set(by_requirement) != set(PHASE_A_REQUIREMENTS) or len(bindings) != len(PHASE_A_REQUIREMENTS):
            result.append(issue(base, "KIN-E-RECEIPT", "Phase A must bind each of the seven frozen requirements exactly once"))
        claim_ids = [binding.get("claimId") for binding in bindings if isinstance(binding, dict)]
        if len(claim_ids) != len(set(claim_ids)):
            result.append(issue(base, "KIN-E-RECEIPT", "Phase-A requirements must bind distinct claims"))
        harvested = set(manifest.get("harvestedClaimIds", []))
        excluded = {
            exclusion.get("claimId") for exclusion in manifest.get("excludedClaimIds", [])
            if isinstance(exclusion, dict)
        }
        trialed = set(manifest.get("trialedClaimIds", []))
        for index, binding in enumerate(bindings):
            if not isinstance(binding, dict):
                continue
            path = f"{base}[{index}]"
            expected = PHASE_A_REQUIREMENTS.get(binding.get("requirementId"))
            if expected is None:
                result.append(issue(path, "KIN-E-RECEIPT", "unknown Phase-A requirement binding"))
                continue
            claim_id = binding.get("claimId")
            claim = claims.get(claim_id)
            source = sources.get(binding.get("ownerSourceId"))
            expected_path, expected_anchor, expected_hash = expected
            if claim is None or source is None:
                result.append(issue(path, "KIN-E-RECEIPT", "binding claim or owner source does not resolve"))
                continue
            if claim_id not in harvested or claim_id in excluded:
                result.append(issue(path, "KIN-E-RECEIPT", "bound claim must be harvested and not excluded"))
            if manifest.get("id") and any(
                receipt.get("manifestId") == manifest.get("id")
                and receipt.get("status") in {"COMPLETE", "VERIFIED"}
                for receipt in items(core, "phaseReceipts")
            ) and claim_id not in trialed:
                result.append(issue(path, "KIN-E-RECEIPT", "terminal Phase-A binding must be trialed"))
            if (
                binding.get("ownerSourceId") != claim.get("ownerSourceId")
                or binding.get("ownerAnchor") != claim.get("ownerAnchor")
                or source.get("path") != expected_path
                or binding.get("ownerAnchor") != expected_anchor
                or binding.get("targetHash") != expected_hash
            ):
                result.append(issue(path, "KIN-E-RECEIPT", "binding does not match the frozen owner fingerprint"))
            if items(core, "trials"):
                canonical_receipt_id, canonical_path, canonical_dependencies = (
                    RECEIPT_IDENTITIES["A"]
                )
                canonical_receipt = receipts.get(canonical_receipt_id)
                canonical_trial_ids = set()
                if canonical_receipt is not None and (
                    canonical_receipt.get("path") == canonical_path
                    and tuple(canonical_receipt.get("dependsOnReceiptIds", []))
                    == canonical_dependencies
                    and canonical_receipt.get("manifestId") == manifest.get("id")
                    and canonical_receipt.get("phase") == "A"
                    and claim_id in canonical_receipt.get("claimIds", [])
                ):
                    canonical_trial_ids = set(canonical_receipt.get("trialIds", []))
                matching_trials = [
                    trial for trial in trials_by_claim.get(claim_id, [])
                    if trial.get("triedHash") == expected_hash
                    and trial.get("manifestId") == manifest.get("id")
                    and trial.get("receiptId") == canonical_receipt_id
                    and trial.get("id") in canonical_trial_ids
                ]
                if len(matching_trials) != 1:
                    result.append(issue(path, "KIN-E-RECEIPT", "binding requires one uniquely matching Phase-A-owned tried quote hash"))
    return result


def _validate_receipts_and_manifests(
    core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]], *, phase: str | None, bootstrap: bool
) -> list[Issue]:
    result: list[Issue] = []
    receipts = indexes["phaseReceipts"]
    manifests = indexes["manifests"]
    claims = indexes["claims"]
    trials = indexes["trials"]
    seams = indexes["seams"]
    propagations = indexes["propagations"]
    attempts = indexes["reviewAttempts"]
    artifacts = {
        record.get("attemptId"): record
        for record in items(core, "reviewAttemptArtifacts")
        if isinstance(record.get("attemptId"), str)
    }

    receipt_phases = [receipt.get("phase") for receipt in items(core, "phaseReceipts")]
    phase_values = [PHASE_RANK[value] for value in receipt_phases if value in PHASE_RANK]
    if phase_values != sorted(phase_values) or len(phase_values) != len(set(phase_values)):
        result.append(issue("core.phaseReceipts", "KIN-E-RECEIPT", "phase receipts must be unique and ordered A, B, C"))
    if phase is not None and phase not in PHASE_RANK:
        result.append(issue("phase", "KIN-E-RECEIPT", "selected phase is invalid"))
    if phase is not None and not any(receipt.get("phase") == phase for receipt in items(core, "phaseReceipts")):
        result.append(issue("phase", "KIN-E-RECEIPT", f"selected Phase {phase} has no receipt"))
    if bootstrap and phase != "A":
        result.append(issue("bootstrap", "KIN-E-RECEIPT", "bootstrap is legal only for Phase A"))

    attempts_by_phase: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for attempt in items(core, "reviewAttempts"):
        attempts_by_phase[attempt.get("phase")].append(attempt)

    for position, manifest in enumerate(items(core, "manifests")):
        base = f"core.manifests[{position}]"
        count_fields = (
            ("candidateFiles", "candidateFileCount"),
            ("finalFiles", "finalFileCount"),
            ("trialedClaimIds", "trialedClaimCount"),
        )
        for field, count_field in count_fields:
            if manifest.get(count_field) != len(manifest.get(field, [])):
                result.append(issue(f"{base}.{count_field}", "KIN-E-RECEIPT", f"{count_field} does not equal {field} length"))
        if manifest.get("eligibleClaimCount") != len(manifest.get("harvestedClaimIds", [])):
            result.append(issue(f"{base}.eligibleClaimCount", "KIN-E-RECEIPT", "eligible claim count does not match harvested claims"))
        manifest_attempts = attempts_by_phase.get(manifest.get("phase"), [])
        expected_closure = sorted({path for attempt in manifest_attempts for path in attempt_paths(str(attempt.get("id")))})
        actual_closure = sorted(manifest.get("closureOnlyPaths", []))
        if actual_closure != expected_closure:
            result.append(issue(f"{base}.closureOnlyPaths", "KIN-E-RECEIPT", "closureOnlyPaths is not the exact four-path attempt union"))
        if not set(actual_closure).issubset(set(manifest.get("allowedChangePaths", []))):
            result.append(issue(f"{base}.closureOnlyPaths", "KIN-E-RECEIPT", "closure-only paths must be allowed change paths"))

    for position, receipt in enumerate(items(core, "phaseReceipts")):
        base = f"core.phaseReceipts[{position}]"
        receipt_phase = receipt.get("phase")
        expected = RECEIPT_IDENTITIES.get(receipt_phase)
        if expected is None or (
            receipt.get("id"), receipt.get("path"), tuple(receipt.get("dependsOnReceiptIds", []))
        ) != expected:
            result.append(issue(base, "KIN-E-RECEIPT", "receipt identity, path, or dependency order is non-canonical"))
        manifest = manifests.get(receipt.get("manifestId"))
        if manifest is None or manifest.get("phase") != receipt_phase:
            result.append(issue(f"{base}.manifestId", "KIN-E-RECEIPT", "receipt manifest does not resolve in the same phase"))
        for dependency_id in receipt.get("dependsOnReceiptIds", []):
            dependency = receipts.get(dependency_id)
            if dependency is None:
                result.append(issue(f"{base}.dependsOnReceiptIds", "KIN-E-RECEIPT", f"dependency receipt is absent: {dependency_id}"))
            elif dependency.get("status") != "VERIFIED":
                result.append(issue(f"{base}.dependsOnReceiptIds", "KIN-E-RECEIPT", f"dependency receipt is not VERIFIED: {dependency_id}"))
        for field, target_index, label in (
            ("claimIds", claims, "claim"),
            ("trialIds", trials, "trial"),
            ("seamIds", seams, "seam"),
            ("propagationIds", propagations, "propagation"),
        ):
            for index, value in enumerate(receipt.get(field, [])):
                target = _require_ref(result, f"{base}.{field}[{index}]", value, target_index, label)
                if target is not None and target.get("receiptId", receipt.get("id")) != receipt.get("id"):
                    result.append(issue(f"{base}.{field}[{index}]", "KIN-E-RECEIPT", f"{label} belongs to another receipt"))

        current_attempt_id = receipt.get("reviewAttemptId")
        phase_attempts = attempts_by_phase.get(receipt_phase, [])
        if current_attempt_id is None:
            if receipt.get("status") != "DRAFT" or phase_attempts:
                result.append(issue(f"{base}.reviewAttemptId", "KIN-E-RECEIPT", "null attempt is legal exactly for a pre-review DRAFT"))
            if manifest is not None and (manifest.get("finalFiles") or manifest.get("finalFileCount") != 0):
                result.append(issue(f"{base}.reviewAttemptId", "KIN-E-RECEIPT", "pre-review DRAFT must have an empty final snapshot"))
        else:
            attempt = attempts.get(current_attempt_id)
            if attempt is None or attempt.get("receiptId") != receipt.get("id"):
                result.append(issue(f"{base}.reviewAttemptId", "KIN-E-RECEIPT", "receipt attempt pointer does not resolve to its chain"))
            if manifest is not None:
                final_paths = {record.get("path") for record in manifest.get("finalFiles", []) if isinstance(record, dict)}
                included_paths = {record.get("path") for record in manifest.get("includedFiles", []) if isinstance(record, dict)}
                if final_paths != included_paths or manifest.get("finalFileCount") != len(final_paths):
                    result.append(issue(f"{base}.reviewAttemptId", "KIN-E-RECEIPT", "allocated attempt requires exact included/final path coverage"))
            if receipt.get("status") == "DRAFT" and attempt is not None and attempt.get("status") == "PASSED":
                result.append(issue(
                    f"{base}.status",
                    "KIN-E-RECEIPT",
                    "DRAFT receipt cannot point to a PASSED attempt",
                ))
            if receipt.get("status") in {"COMPLETE", "VERIFIED"} and (
                attempt is None or attempt.get("status") != "PASSED"
            ):
                result.append(issue(f"{base}.status", "KIN-E-RECEIPT", "terminal receipt requires the current PASSED attempt"))
            if receipt.get("status") in {"COMPLETE", "VERIFIED"} and attempt is not None:
                artifact = artifacts.get(attempt.get("id"), {})
                expected_fields = {
                    "logicReviewPath": attempt.get("logicReviewPath"),
                    "btjReviewPath": attempt.get("btjReviewPath"),
                    "reviewTargetDigest": artifact.get("reviewTargetSha256"),
                }
                if any(receipt.get(field) != value for field, value in expected_fields.items()):
                    result.append(issue(
                        base,
                        "KIN-E-RECEIPT",
                        "terminal receipt paths and target digest do not bind the current attempt artifact",
                    ))
                if (
                    receipt.get("status") == "VERIFIED"
                    and receipt.get("validationBundlePath") != attempt.get("validationBundlePath")
                ):
                    result.append(issue(
                        f"{base}.validationBundlePath",
                        "KIN-E-RECEIPT",
                        "VERIFIED receipt bundle path does not bind the current attempt",
                    ))

        selected_bootstrap = (
            bootstrap and phase == "A" and receipt_phase == "A"
            and receipt.get("status") == "DRAFT"
        )
        exact_empty = (
            selected_bootstrap
            and not items(core, "trials")
            and manifest is not None
            and manifest.get("id") == "MAN-A-001"
            and manifest.get("trialedClaimIds") == []
            and manifest.get("trialedClaimCount") == 0
            and receipt.get("trialIds") == []
            and manifest.get("finalFiles") == []
            and manifest.get("finalFileCount") == 0
            and manifest.get("closureOnlyPaths") == []
            and bool(items(core, "claims"))
            and bool(manifest.get("requiredClaimBindings"))
        )
        owned_trials = [
            trials.get(trial_id)
            for trial_id in receipt.get("trialIds", [])
            if trial_id in trials
            and trials[trial_id].get("receiptId") == receipt.get("id")
            and trials[trial_id].get("manifestId") == receipt.get("manifestId")
            and trials[trial_id].get("claimId") in receipt.get("claimIds", [])
            and manifest is not None
            and trials[trial_id].get("claimId") in manifest.get("harvestedClaimIds", [])
            and trials[trial_id].get("claimId") in manifest.get("trialedClaimIds", [])
            and trials[trial_id].get("status") in {"ADJUDICATED", "CLOSED"}
        ]
        selected_for_coverage = (
            phase is None
            or phase == receipt_phase
            or receipt.get("status") in {"COMPLETE", "VERIFIED"}
        )
        if selected_for_coverage and not exact_empty and not owned_trials:
            coverage_context = (
                f"selected Phase-{receipt_phase} non-bootstrap"
                if phase == receipt_phase
                else f"Phase-{receipt_phase} terminal or bare non-bootstrap"
            )
            result.append(issue(
                f"{base}.trialIds",
                "KIN-E-RECEIPT",
                f"{coverage_context} receipt requires at least one owned trial",
            ))
    return result


def _validate_fixture_membership(core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[Issue]:
    result: list[Issue] = []
    fixtures = indexes["fixtures"]
    references: dict[str, list[tuple[str, str]]] = defaultdict(list)
    field_kind = {
        "positiveFixtureIds": "POSITIVE",
        "negativeFixtureIds": "NEGATIVE",
        "quotationFixtureIds": "QUOTATION",
        "historicalFixtureIds": "HISTORICAL",
    }
    for position, antibody in enumerate(items(core, "antibodies")):
        for field, expected_kind in field_kind.items():
            for fixture_id in antibody.get(field, []):
                references[fixture_id].append((antibody.get("id"), expected_kind))
                fixture = fixtures.get(fixture_id)
                if fixture is not None and fixture.get("kind") != expected_kind:
                    result.append(issue(
                        f"core.antibodies[{position}].{field}",
                        "KIN-E-FIXTURE",
                        "fixture is listed under the wrong execution context",
                    ))
    for position, fixture in enumerate(items(core, "fixtures")):
        if fixture.get("kind") == "MUTATION":
            continue
        fixture_id = fixture.get("id")
        declared = references.get(fixture_id, [])
        expected_antibodies = sorted(fixture.get("antibodyIds", []))
        actual_antibodies = sorted(value[0] for value in declared)
        if len(declared) != len(set(declared)) or actual_antibodies != expected_antibodies:
            result.append(issue(
                f"core.fixtures[{position}]",
                "KIN-E-FIXTURE",
                "fixture must execute exactly once in the matching list of each declared antibody",
            ))
        if not set(fixture.get("expectedAntibodyIds", [])).issubset(set(expected_antibodies)):
            result.append(issue(f"core.fixtures[{position}].expectedAntibodyIds", "KIN-E-FIXTURE", "expected triggers must be declared fixture antibodies"))
    for fixture_id in references:
        if fixture_id not in fixtures:
            result.append(issue("core.antibodies", "KIN-E-FIXTURE", f"declared fixture is missing: {fixture_id}"))
    return result


def _validate_review_history(core: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[Issue]:
    result: list[Issue] = []
    attempts_list = items(core, "reviewAttempts")
    attempts = indexes["reviewAttempts"]
    receipts = indexes["phaseReceipts"]
    manifests = indexes["manifests"]
    seams = indexes["seams"]
    claims = indexes["claims"]
    discriminators = indexes["discriminators"]
    artifacts_list = items(core, "reviewAttemptArtifacts")
    artifacts = {record.get("attemptId"): record for record in artifacts_list if isinstance(record.get("attemptId"), str)}
    if len(artifacts) != len(artifacts_list) or set(artifacts) != set(attempts):
        result.append(issue("core.reviewAttemptArtifacts", "KIN-E-REF", "attempt/artifact coverage must be an exact bijection"))
    if [record.get("attemptId") for record in artifacts_list] != [record.get("id") for record in attempts_list]:
        result.append(issue("core.reviewAttemptArtifacts", "KIN-E-REF", "attempt artifacts must follow root-to-leaf attempt order"))

    children: dict[str, list[str]] = defaultdict(list)
    attempt_positions = {attempt.get("id"): index for index, attempt in enumerate(attempts_list)}
    for position, attempt in enumerate(attempts_list):
        base = f"core.reviewAttempts[{position}]"
        attempt_id = attempt.get("id")
        phase = attempt.get("phase")
        if not canonical_attempt(attempt_id, phase):
            result.append(issue(f"{base}.id", "KIN-E-REF", "review attempt ID is not its canonical parse/render spelling"))
        if isinstance(attempt_id, str):
            expected_paths = attempt_paths(attempt_id)
            actual_paths = tuple(attempt.get(field) for field in (
                "reviewTargetPath", "logicReviewPath", "btjReviewPath", "validationBundlePath"
            ))
            if actual_paths != expected_paths:
                result.append(issue(base, "KIN-E-REF", "review attempt paths do not derive exactly from its ID"))
        receipt = receipts.get(attempt.get("receiptId"))
        if receipt is None or receipt.get("phase") != phase:
            result.append(issue(f"{base}.receiptId", "KIN-E-REF", "attempt phase and receipt do not agree"))
        parent_id = attempt.get("supersedesAttemptId")
        if parent_id is not None:
            parent = attempts.get(parent_id)
            if parent is None:
                result.append(issue(f"{base}.supersedesAttemptId", "KIN-E-REF", "superseded attempt does not resolve"))
            else:
                children[parent_id].append(attempt_id)
                if parent.get("phase") != phase or parent.get("receiptId") != attempt.get("receiptId"):
                    result.append(issue(f"{base}.supersedesAttemptId", "KIN-E-REF", "successor crosses a phase/receipt chain"))
                if parent.get("status") not in {"FAILED", "ABANDONED"}:
                    result.append(issue(f"{base}.supersedesAttemptId", "KIN-E-STATE", "only FAILED or ABANDONED attempts may be superseded"))
                if attempt_positions.get(parent_id, position) >= position:
                    result.append(issue(base, "KIN-E-REF", "attempt array is not root-to-leaf ordered"))
        artifact = artifacts.get(attempt_id)
        if artifact is None:
            continue
        logic_present = attempt.get("logicAttestationId") is not None
        btj_present = attempt.get("btjAttestationId") is not None
        if (artifact.get("logicReviewSha256") is not None) != logic_present:
            result.append(issue(base, "KIN-E-STATE", "LOGIC attestation and artifact hash must be jointly present or absent"))
        if (artifact.get("btjReviewSha256") is not None) != btj_present:
            result.append(issue(base, "KIN-E-STATE", "BTJ attestation and artifact hash must be jointly present or absent"))
        if (logic_present or btj_present or attempt.get("status") in {"FAILED", "PASSED"}) and artifact.get("reviewTargetSha256") is None:
            result.append(issue(base, "KIN-E-STATE", "reviewed or terminal attempt requires a target artifact hash"))

    # Attempt supersession cycles and one leaf per chain.
    supersession_graph = {
        attempt_id: ({attempt.get("supersedesAttemptId")} if attempt.get("supersedesAttemptId") else set())
        for attempt_id, attempt in attempts.items()
    }
    states: dict[str, int] = {}
    for start in sorted(supersession_graph):
        current = start
        lineage: list[str] = []
        positions: dict[str, int] = {}
        while current in supersession_graph and states.get(current, 0) == 0:
            states[current] = 1
            positions[current] = len(lineage)
            lineage.append(current)
            targets = supersession_graph[current]
            if not targets:
                break
            current = next(iter(targets))
            if states.get(current) == 1 and current in positions:
                cycle = _canonical_cycle(lineage[positions[current]:] + [current])
                result.append(issue("core.reviewAttempts", "KIN-E-CYCLE", "review supersession cycle: " + " -> ".join(cycle)))
                break
        for value in lineage:
            states[value] = 2
    chains: dict[tuple[Any, Any], list[str]] = defaultdict(list)
    for attempt_id, attempt in attempts.items():
        chains[(attempt.get("phase"), attempt.get("receiptId"))].append(attempt_id)
    for chain, attempt_ids in chains.items():
        roots = [attempt_id for attempt_id in attempt_ids if attempts[attempt_id].get("supersedesAttemptId") is None]
        leaves = [attempt_id for attempt_id in attempt_ids if not children.get(attempt_id)]
        if len(roots) != 1 or len(leaves) != 1:
            result.append(issue("core.reviewAttempts", "KIN-E-REF", f"review chain {chain} must have exactly one root and one leaf"))
        receipt = receipts.get(chain[1])
        if receipt is not None and leaves and receipt.get("reviewAttemptId") != leaves[0]:
            result.append(issue("core.phaseReceipts", "KIN-E-REF", "receipt must point to the unique current attempt leaf"))

    attestations = indexes["reviewAttestations"]
    findings = indexes["reviewFindings"]
    finding_ref_counts: Counter[str] = Counter()

    discriminator_ids_by_claim: dict[Any, set[Any]] = defaultdict(set)
    for discriminator_id, discriminator in discriminators.items():
        discriminator_ids_by_claim[discriminator.get("claimId")].add(discriminator_id)

    empty_review_subject = {
        "claimIds": set(), "seamIds": set(), "ledgerSectionIds": set(),
        "receiptIds": set(), "subjectPaths": set(), "discriminatorIds": set(),
    }
    review_subjects_by_receipt: dict[Any, dict[str, set[Any]]] = {}
    for receipt_id, receipt in receipts.items():
        manifest = manifests.get(receipt.get("manifestId"))
        if manifest is None:
            review_subjects_by_receipt[receipt_id] = empty_review_subject
            continue
        claim_ids = set(receipt.get("claimIds", [])) & set(manifest.get("harvestedClaimIds", []))
        seam_ids = {
            seam_id
            for seam_id in receipt.get("seamIds", [])
            if seam_id in seams
            and seams[seam_id].get("receiptId") == receipt.get("id")
            and seams[seam_id].get("claimId") in claim_ids
        }
        closure_paths = set(manifest.get("closureOnlyPaths", []))
        subject_paths = {
            record.get("path")
            for record in manifest.get("finalFiles", [])
            if isinstance(record, dict) and record.get("path") not in closure_paths
        }
        discriminator_ids: set[Any] = set()
        for claim_id in claim_ids:
            discriminator_ids.update(discriminator_ids_by_claim.get(claim_id, ()))
        review_subjects_by_receipt[receipt_id] = {
            "claimIds": claim_ids,
            "seamIds": seam_ids,
            "ledgerSectionIds": seam_ids | {"LEDGER-PREAMBLE"},
            "receiptIds": {receipt.get("id")},
            "subjectPaths": subject_paths,
            "discriminatorIds": discriminator_ids,
        }

    def review_subject(attempt: dict[str, Any] | None) -> dict[str, set[Any]]:
        if attempt is None:
            return empty_review_subject
        return review_subjects_by_receipt.get(
            attempt.get("receiptId"), empty_review_subject
        )

    for position, attempt in enumerate(attempts_list):
        base = f"core.reviewAttempts[{position}]"
        logic_id = attempt.get("logicAttestationId")
        btj_id = attempt.get("btjAttestationId")
        if logic_id is not None and logic_id == btj_id:
            result.append(issue(
                base,
                "KIN-E-STATE",
                "LOGIC and BTJ review slots require distinct attestations",
            ))
        for field, attestation_id, expected_kind in (
            ("logicAttestationId", logic_id, "LOGIC"),
            ("btjAttestationId", btj_id, "BTJ"),
        ):
            if attestation_id is None:
                continue
            attestation = attestations.get(attestation_id)
            if attestation is not None and (
                attestation.get("kind") != expected_kind
                or attestation.get("attemptId") != attempt.get("id")
            ):
                result.append(issue(
                    f"{base}.{field}",
                    "KIN-E-REF",
                    f"{field} must resolve to a {expected_kind} attestation for this attempt",
                ))

    for position, attestation in enumerate(items(core, "reviewAttestations")):
        base = f"core.reviewAttestations[{position}]"
        attempt = attempts.get(attestation.get("attemptId"))
        if attempt is None:
            result.append(issue(f"{base}.attemptId", "KIN-E-REF", "attestation attempt does not resolve"))
            continue
        kind = attestation.get("kind")
        field = "logicAttestationId" if kind == "LOGIC" else "btjAttestationId"
        expected_path = attempt.get("logicReviewPath" if kind == "LOGIC" else "btjReviewPath")
        if attempt.get(field) != attestation.get("id") or attestation.get("path") != expected_path:
            result.append(issue(base, "KIN-E-REF", "attestation is not exactly bound to its attempt kind/path"))
        artifact = artifacts.get(attempt.get("id"), {})
        if attestation.get("receiptId") != attempt.get("receiptId") or attestation.get("reviewTargetDigest") != artifact.get("reviewTargetSha256"):
            result.append(issue(base, "KIN-E-REF", "attestation receipt or target digest does not match its attempt"))
        named_findings: list[dict[str, Any]] = []
        for finding_id in attestation.get("findingIds", []):
            finding_ref_counts[finding_id] += 1
            finding = findings.get(finding_id)
            if finding is None or finding.get("attemptId") != attempt.get("id") or finding.get("reviewKind") != kind:
                result.append(issue(f"{base}.findingIds", "KIN-E-REF", "attestation finding does not resolve in the same attempt/kind"))
            else:
                named_findings.append(finding)
        severe = sorted(finding.get("id") for finding in named_findings if finding.get("severity") in {"CRITICAL", "MAJOR"})
        open_severe = sorted(attestation.get("openSevereFindingIds", []))
        if attestation.get("verdict") == "FAIL":
            if not named_findings or not severe or open_severe != severe:
                result.append(issue(base, "KIN-E-STATE", "FAIL must expose every open CRITICAL/MAJOR finding"))
        elif open_severe or any(finding.get("severity") != "MINOR" for finding in named_findings):
            result.append(issue(base, "KIN-E-STATE", "PASS may carry only MINOR findings and no open severe finding"))
        for field_name in ("approvedUpgradeSeamIds", "approvedGateSeamIds"):
            for value in attestation.get(field_name, []):
                if value not in seams:
                    result.append(issue(f"{base}.{field_name}", "KIN-E-REF", "approved seam does not resolve"))

    for finding_id in findings:
        if finding_ref_counts[finding_id] != 1:
            result.append(issue("core.reviewFindings", "KIN-E-REF", f"review finding must be resolved by exactly one attestation: {finding_id}"))

    for position, finding in enumerate(items(core, "reviewFindings")):
        base = f"core.reviewFindings[{position}]"
        subject = review_subject(attempts.get(finding.get("attemptId")))
        for field, target_index, label in (
            ("claimIds", claims, "claim"),
            ("seamIds", seams, "seam"),
            ("receiptIds", receipts, "receipt"),
        ):
            for value in finding.get(field, []):
                if value not in target_index:
                    result.append(issue(f"{base}.{field}", "KIN-E-REF", f"finding {label} endpoint does not resolve: {value}"))
                elif value not in subject[field]:
                    result.append(issue(f"{base}.{field}", "KIN-E-REF", f"finding {label} endpoint is outside its attempt subject: {value}"))
        for value in finding.get("ledgerSectionIds", []):
            if value != "LEDGER-PREAMBLE" and value not in seams:
                result.append(issue(f"{base}.ledgerSectionIds", "KIN-E-REF", f"finding ledger endpoint does not resolve: {value}"))
            elif value not in subject["ledgerSectionIds"]:
                result.append(issue(f"{base}.ledgerSectionIds", "KIN-E-REF", f"finding ledger endpoint is outside its attempt subject: {value}"))
        for value in finding.get("subjectPaths", []):
            if value not in subject["subjectPaths"]:
                result.append(issue(f"{base}.subjectPaths", "KIN-E-REF", f"finding subject path is outside its attempt final inventory: {value}"))

    dispositions = items(core, "reviewFindingDispositions")
    dispositions_by_pair: Counter[tuple[Any, Any]] = Counter()
    dispositions_by_successor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    predecessor_process_evidence_by_attempt: dict[
        Any, set[tuple[Any, Any]]
    ] = {}
    successor_process_evidence_by_manifest: dict[
        Any, set[tuple[Any, Any]]
    ] = {}
    for position, disposition in enumerate(dispositions):
        base = f"core.reviewFindingDispositions[{position}]"
        successor_attempt_id = disposition.get("successorAttemptId")
        if isinstance(successor_attempt_id, str):
            dispositions_by_successor[successor_attempt_id].append(disposition)
        finding = findings.get(disposition.get("findingId"))
        predecessor = attempts.get(disposition.get("fromAttemptId"))
        successor = attempts.get(successor_attempt_id)
        if finding is None or predecessor is None or successor is None:
            result.append(issue(base, "KIN-E-REF", "disposition finding/predecessor/successor does not resolve"))
            continue
        if finding.get("attemptId") != predecessor.get("id") or successor.get("supersedesAttemptId") != predecessor.get("id"):
            result.append(issue(base, "KIN-E-REF", "disposition does not join a finding to its direct successor"))
        dispositions_by_pair[(finding.get("id"), successor.get("id"))] += 1
        subject = review_subject(successor)
        for field, target_index, label in (
            ("claimIds", claims, "claim"),
            ("seamIds", seams, "seam"),
            ("receiptIds", receipts, "receipt"),
            ("discriminatorIds", discriminators, "discriminator"),
        ):
            for value in disposition.get(field, []):
                if value not in target_index:
                    result.append(issue(f"{base}.{field}", "KIN-E-REF", f"disposition {label} endpoint does not resolve: {value}"))
                elif value not in subject[field]:
                    result.append(issue(f"{base}.{field}", "KIN-E-REF", f"disposition {label} endpoint is outside the successor subject: {value}"))
        for value in disposition.get("ledgerSectionIds", []):
            if value != "LEDGER-PREAMBLE" and value not in seams:
                result.append(issue(f"{base}.ledgerSectionIds", "KIN-E-REF", f"disposition ledger endpoint does not resolve: {value}"))
            elif value not in subject["ledgerSectionIds"]:
                result.append(issue(f"{base}.ledgerSectionIds", "KIN-E-REF", f"disposition ledger endpoint is outside the successor subject: {value}"))
        for value in disposition.get("subjectPaths", []):
            if value not in subject["subjectPaths"]:
                result.append(issue(f"{base}.subjectPaths", "KIN-E-REF", f"disposition subject path is outside the successor final inventory: {value}"))
        kind = disposition.get("disposition")
        endpoints = sum(len(disposition.get(field, [])) for field in (
            "claimIds", "seamIds", "ledgerSectionIds", "receiptIds", "subjectPaths"
        ))
        if kind == "ADDRESSED" and (
            endpoints == 0 or disposition.get("discriminatorIds") or disposition.get("evidenceFiles")
        ):
            result.append(issue(base, "KIN-E-STATE", "ADDRESSED requires a semantic endpoint and no discriminator/process evidence"))
        if kind == "DISPUTED" and (
            not disposition.get("discriminatorIds") or disposition.get("evidenceFiles")
        ):
            result.append(issue(base, "KIN-E-STATE", "DISPUTED requires a discriminator and no process evidence"))
        if kind == "PROCESS_INVALID" and (
            not disposition.get("evidenceFiles")
            or endpoints or disposition.get("discriminatorIds")
        ):
            result.append(issue(base, "KIN-E-STATE", "PROCESS_INVALID requires only hash-bound process evidence"))
        if kind == "PROCESS_INVALID":
            predecessor_id = predecessor.get("id")
            predecessor_evidence = predecessor_process_evidence_by_attempt.get(
                predecessor_id
            )
            if predecessor_evidence is None:
                predecessor_evidence = set()
                predecessor_artifact = artifacts.get(predecessor_id, {})
                for path_field, hash_field in (
                    ("reviewTargetPath", "reviewTargetSha256"),
                    ("logicReviewPath", "logicReviewSha256"),
                    ("btjReviewPath", "btjReviewSha256"),
                ):
                    digest = predecessor_artifact.get(hash_field)
                    if digest is not None:
                        predecessor_evidence.add((predecessor.get(path_field), digest))
                predecessor_process_evidence_by_attempt[
                    predecessor_id
                ] = predecessor_evidence
            successor_receipt = receipts.get(successor.get("receiptId"))
            successor_manifest = (
                manifests.get(successor_receipt.get("manifestId"))
                if successor_receipt is not None else None
            )
            successor_evidence: set[tuple[Any, Any]] = set()
            if successor_manifest is not None:
                successor_manifest_id = successor_manifest.get("id")
                cached_successor_evidence = (
                    successor_process_evidence_by_manifest.get(successor_manifest_id)
                )
                if cached_successor_evidence is None:
                    cached_successor_evidence = set()
                    closure_paths = set(successor_manifest.get("closureOnlyPaths", []))
                    for file_record in successor_manifest.get("finalFiles", []):
                        if (
                            isinstance(file_record, dict)
                            and file_record.get("path") not in closure_paths
                        ):
                            cached_successor_evidence.add((
                                file_record.get("path"), file_record.get("sha256")
                            ))
                    successor_process_evidence_by_manifest[
                        successor_manifest_id
                    ] = cached_successor_evidence
                successor_evidence = cached_successor_evidence
            for evidence in disposition.get("evidenceFiles", []):
                evidence_key = (
                    (evidence.get("path"), evidence.get("sha256"))
                    if isinstance(evidence, dict) else None
                )
                if (
                    evidence_key is None
                    or (
                        evidence_key not in predecessor_evidence
                        and evidence_key not in successor_evidence
                    )
                ):
                    result.append(issue(f"{base}.evidenceFiles", "KIN-E-REF", "process evidence is not bound to an immutable predecessor artifact or successor final file"))

    findings_by_attempt: dict[str, list[str]] = defaultdict(list)
    for finding_id, finding in findings.items():
        finding_attempt_id = finding.get("attemptId")
        if isinstance(finding_attempt_id, str):
            findings_by_attempt[finding_attempt_id].append(finding_id)
    for finding_ids in findings_by_attempt.values():
        finding_ids.sort()
    for successor_dispositions in dispositions_by_successor.values():
        successor_dispositions.sort(key=lambda record: str(record.get("findingId")))

    for parent_id, child_ids in children.items():
        if len(child_ids) != 1:
            continue
        child_id = child_ids[0]
        predecessor_findings = findings_by_attempt.get(parent_id, ())
        if any(dispositions_by_pair[(finding_id, child_id)] != 1 for finding_id in predecessor_findings):
            result.append(issue("core.reviewFindingDispositions", "KIN-E-REF", "every predecessor finding requires exactly one successor disposition"))
        chain_dispositions = dispositions_by_successor.get(child_id, ())
        for ordinal, record in enumerate(chain_dispositions, start=1):
            expected_id = f"RFD-{child_id}-{ordinal:03d}"
            if record.get("id") != expected_id:
                result.append(issue("core.reviewFindingDispositions", "KIN-E-REF", "disposition ID/ordinal is non-canonical"))

    # Closed attempt state table.
    for position, attempt in enumerate(attempts_list):
        base = f"core.reviewAttempts[{position}]"
        ids = [attempt.get("logicAttestationId"), attempt.get("btjAttestationId")]
        present = [value for value in ids if value is not None]
        resolved = []
        for value, expected_kind in zip(ids, ("LOGIC", "BTJ")):
            record = attestations.get(value) if value is not None else None
            if (
                record is not None
                and record.get("kind") == expected_kind
                and record.get("attemptId") == attempt.get("id")
            ):
                resolved.append(record)
        for value in present:
            if value not in attestations:
                result.append(issue(base, "KIN-E-REF", f"attempt attestation does not resolve: {value}"))
        status = attempt.get("status")
        reason = attempt.get("abandonReason")
        if status == "PENDING" and (
            len(present) > 1 or reason is not None or any(record.get("verdict") != "PASS" for record in resolved)
        ):
            result.append(issue(base, "KIN-E-STATE", "PENDING permits at most one PASS attestation and no abandon reason"))
        elif status == "FAILED" and (
            not present or reason is not None or not any(record.get("verdict") == "FAIL" for record in resolved)
        ):
            result.append(issue(base, "KIN-E-STATE", "FAILED requires one or two attestations including FAIL"))
        elif status == "PASSED" and (
            len(present) != 2 or reason is not None or len(resolved) != 2
            or present[0] == present[1]
            or any(record.get("verdict") != "PASS" for record in resolved)
        ):
            result.append(issue(base, "KIN-E-STATE", "PASSED requires distinct role-bound LOGIC and BTJ PASS attestations"))
        elif status == "ABANDONED" and not isinstance(reason, str):
            result.append(issue(base, "KIN-E-STATE", "ABANDONED requires a non-null reason"))
    return result


def _validate_record_graph_unchecked(
    core: dict[str, Any], *, phase: str | None = None, bootstrap: bool = False
) -> list[Issue]:
    _, result = _index_global_ids(core)
    indexes = {collection: _collection_index(core, collection) for collection in GLOBAL_COLLECTIONS}
    result.extend(_validate_source_roles(core))
    result.extend(_validate_claim_graph(core, indexes))
    result.extend(_validate_references(core, indexes))
    result.extend(_validate_bindings(core, indexes))
    result.extend(_validate_receipts_and_manifests(core, indexes, phase=phase, bootstrap=bootstrap))
    result.extend(_validate_fixture_membership(core, indexes))
    result.extend(_validate_review_history(core, indexes))
    return ordered_issues(result)


def validate_record_graph(
    core: dict[str, Any], *, phase: str | None = None, bootstrap: bool = False
) -> list[Issue]:
    shape_issues = core_record_shape_issues(core)
    if shape_issues:
        return shape_issues
    try:
        return _validate_record_graph_unchecked(
            core,
            phase=phase,
            bootstrap=bootstrap,
        )
    except Exception:
        return [malformed_core_issue()]


__all__ = [
    "PHASE_A_REQUIREMENTS",
    "PHASE_RANK",
    "RECEIPT_IDENTITIES",
    "RECEIPT_PHASE",
    "SOURCE_ROLE_MATRIX",
    "attempt_paths",
    "canonical_attempt",
    "core_record_shape_issues",
    "malformed_core_issue",
    "ordered_issues",
    "validate_record_graph",
    "valid_id",
]

"""Offline record checks, not evidence adjudication or an execution engine [D/S]."""

import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MAX_BYTES = 1_048_576


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def obj(value, keys, path):
    require(type(value) is dict, f"{path}: expected object")
    require(set(value) == set(keys.split()), f"{path}: missing or unknown fields")
    return value


def text(value, path):
    require(type(value) is str and bool(value.strip()), f"{path}: expected nonempty text")
    return value


def seq(value, path, nonempty=True):
    require(type(value) is list, f"{path}: expected array")
    require(not nonempty or bool(value), f"{path}: empty array")
    return value


def words(value, path, nonempty=True):
    for item in seq(value, path, nonempty):
        text(item, path)
    require(len(set(value)) == len(value), f"{path}: duplicate values")
    return value


def number(value, path):
    require(type(value) in (int, float), f"{path}: expected finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    require(finite, f"{path}: expected finite number in supported range")
    return value


def stamp(value, path):
    text(value, path)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{path}: invalid timestamp") from exc
    require(parsed.tzinfo is not None, f"{path}: timezone required")
    return parsed


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def bundle_digest(record):
    return digest({key: record[key] for key in ("context", "vmo", "ska")})


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise ContractError(f"nonfinite JSON constant: {value}")

    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "record exceeds 1 MiB limit")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def source_check(contract, repo=REPO):
    require(contract.get("schema_version") == "emergentism/EmergentistExergyContract.v1",
            "unsupported contract version")
    root = repo.resolve()
    for pin in contract["source_pins"]:
        obj(pin, "path sha256", "source pin")
        path = (root / pin["path"]).resolve()
        require(path.is_relative_to(root), "source pin escapes repository")
        require(path.is_file(), f"missing source: {pin['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == pin["sha256"], f"source drift: {pin['path']}")


def _validate(record, contract):
    obj(record, "schema_version id tier context vmo ska evidence guardrails assessment revision", "record")
    require(record["schema_version"] == contract["record_version"], "unsupported record version")
    text(record["id"], "id")
    require(record["tier"] == "[D]", "prototype record tier must remain [D]")
    ctx = obj(record["context"], "id bearers system_boundary as_of review_at horizon_end", "context")
    text(ctx["id"], "context.id")
    text(ctx["system_boundary"], "system_boundary")
    bearers = set(words(ctx["bearers"], "bearers"))
    now = stamp(ctx["as_of"], "as_of")
    require(now < stamp(ctx["review_at"], "review_at") <= stamp(ctx["horizon_end"], "horizon_end"),
            "review horizon must be after as_of and within horizon_end")
    evidence = {}
    for e in seq(record["evidence"], "evidence", False):
        obj(e, "id kind source limitations", "evidence")
        for field in ("id", "source", "limitations"):
            text(e[field], f"evidence.{field}")
        require(e["id"] not in evidence, "duplicate evidence id")
        require(e["kind"] in contract["evidence_kinds"], "unknown evidence kind")
        evidence[e["id"]] = e

    def refs(items, path, needed=False):
        words(items, path, needed)
        require(set(items) <= set(evidence), f"{path}: unresolved evidence reference")

    ids = set()

    def identify(item, kind):
        name = text(item["id"], f"{kind}.id")
        require(name not in ids, "duplicate object id")
        ids.add(name)
        return name

    vmo = obj(record["vmo"], "vision mission objectives", "vmo")
    vision = obj(vmo["vision"], "statement cone_type exclusions", "vision")
    text(vision["statement"], "vision.statement")
    require(vision["cone_type"] == "imagined_option_cone", "vision is not a physical light cone")
    words(vision["exclusions"], "vision.exclusions")
    mission = obj(vmo["mission"], "statement constraints trajectories", "mission")
    text(mission["statement"], "mission.statement")
    words(mission["constraints"], "constraints")
    trajectories = {}
    for t in seq(mission["trajectories"], "trajectories"):
        obj(t, "id description status evidence", "trajectory")
        identify(t, "trajectory")
        text(t["description"], "trajectory.description")
        require(t["status"] in contract["trajectory_states"], "unknown trajectory status")
        refs(t["evidence"], "trajectory.evidence", t["status"] != "imagined")
        trajectories[t["id"]] = t
    objectives = {}
    for o in seq(vmo["objectives"], "objectives"):
        obj(o, "id trajectory_id description kpi_ids", "objective")
        identify(o, "objective")
        text(o["description"], "objective.description")
        require(o["trajectory_id"] in trajectories, "objective: unknown trajectory")
        words(o["kpi_ids"], "objective.kpi_ids")
        objectives[o["id"]] = o
    ska = obj(record["ska"], "strategies kpis agents", "ska")
    agents = set()
    for a in seq(ska["agents"], "agents"):
        obj(a, "id role capabilities scope may_sign may_authorize", "agent")
        agents.add(identify(a, "agent"))
        text(a["role"], "agent.role")
        words(a["capabilities"], "capabilities")
        words(a["scope"], "scope")
        require(a["may_sign"] is False and a["may_authorize"] is False,
                "record grants no signing or authorization")
    findings = ["External source authenticity, bearer completeness and outcomes are not verified."]
    covered = set()
    for s in seq(ska["strategies"], "strategies"):
        obj(s, "id objective_id agent_ids policy dependencies", "strategy")
        identify(s, "strategy")
        require(s["objective_id"] in objectives, "strategy: unknown objective")
        covered.add(s["objective_id"])
        require(set(words(s["agent_ids"], "strategy.agent_ids")) <= agents, "strategy: unknown agent")
        text(s["policy"], "strategy.policy")
        for d in seq(s["dependencies"], "dependencies"):
            obj(d, "id description status evidence", "dependency")
            identify(d, "dependency")
            text(d["description"], "dependency.description")
            require(d["status"] in contract["dependency_states"], "unknown dependency status")
            refs(d["evidence"], "dependency.evidence", d["status"] != "unknown")
            if d["status"] != "supported":
                findings.append(f"Dependency {d['id']}: {d['status']}; not demonstrated capability.")
    require(covered == set(objectives), "objective lacks strategy mapping")
    kpis = {}
    for k in seq(ska["kpis"], "kpis"):
        obj(k, "id objective_id metric unit threshold comparator value status observed_at expires_at evidence", "kpi")
        identify(k, "kpi")
        require(k["objective_id"] in objectives, "kpi: unknown objective")
        text(k["metric"], "metric")
        text(k["unit"], "unit")
        number(k["threshold"], "threshold")
        require(k["comparator"] in ("ge", "le"), "unknown comparator")
        require(k["status"] in contract["kpi_states"], "unknown kpi status")
        refs(k["evidence"], "kpi.evidence", k["status"] != "unknown")
        if k["status"] == "unknown":
            require(k["value"] is None and k["observed_at"] is None and k["expires_at"] is None,
                    "unknown KPI must not masquerade as a measurement")
        else:
            number(k["value"], "kpi.value")
            require(stamp(k["observed_at"], "observed_at") <= now < stamp(k["expires_at"], "expires_at"),
                    "KPI is future-dated or stale")
            met = k["value"] >= k["threshold"] if k["comparator"] == "ge" else k["value"] <= k["threshold"]
            require(k["status"] == ("met" if met else "failed"), "KPI status contradicts threshold")
        if k["status"] != "met":
            findings.append(f"KPI {k['id']}: {k['status']}.")
        kpis[k["id"]] = k
    for o in objectives.values():
        expected = {k["id"] for k in kpis.values() if k["objective_id"] == o["id"]}
        require(set(o["kpi_ids"]) == expected and bool(expected), "objective/KPI mapping mismatch")
    g = obj(record["guardrails"], "authorization authorization_evidence justice justice_evidence bearers ledgers", "guardrails")
    require(g["authorization"] in ("unassessed", "refused", "documented"), "unknown authorization state")
    require(g["justice"] in ("unassessed", "refused", "reviewed"), "unknown justice state")
    refs(g["authorization_evidence"], "authorization_evidence", g["authorization"] != "unassessed")
    refs(g["justice_evidence"], "justice_evidence", g["justice"] != "unassessed")
    reviewed = set()
    for b in seq(g["bearers"], "bearer reviews"):
        obj(b, "id option_effect consent costs repair_exit evidence", "bearer review")
        require(b["id"] in bearers and b["id"] not in reviewed, "missing, duplicate or unknown bearer")
        reviewed.add(b["id"])
        require(b["option_effect"] in ("unknown", "loss", "unchanged", "gain"), "unknown option effect")
        require(b["consent"] in ("unknown", "refused", "documented"), "unknown consent state")
        text(b["costs"], "bearer costs")
        text(b["repair_exit"], "repair_exit")
        refs(b["evidence"], "bearer.evidence", b["option_effect"] != "unknown" or b["consent"] != "unknown")
        if b["option_effect"] in ("unknown", "loss") or b["consent"] != "documented":
            findings.append(f"Bearer {b['id']}: effects/consent require review.")
    require(reviewed == bearers, "missing bearer review")
    ledgers = obj(g["ledgers"], "physical_exergy thermodynamic_entropy history_entropy viability", "ledgers")
    for name, ledger in ledgers.items():
        obj(ledger, "status evidence", f"ledger.{name}")
        require(ledger["status"] in ("unmeasured", "external_record"), "unknown ledger state")
        refs(ledger["evidence"], f"ledger.{name}.evidence", ledger["status"] == "external_record")
    assess = obj(record["assessment"], "mode calibration factors", "assessment")
    require(assess["mode"] in contract["modes"], "unknown assessment mode")
    candidate = None
    if assess["mode"] == "composition_only":
        require(assess["calibration"] is None and assess["factors"] is None,
                "composition_only has no scalar operands")
    else:
        cal = obj(assess["calibration"], "id version context_sha256 bundle_sha256 scale units evaluator_vmo evaluator_ska zeros transformations uncertainty comparison_domain evidence", "calibration")
        for key in ("id", "version", "evaluator_vmo", "evaluator_ska", "zeros", "transformations", "uncertainty", "comparison_domain"):
            text(cal[key], f"calibration.{key}")
        require(cal["context_sha256"] == digest(ctx), "calibration context mismatch")
        require(cal["bundle_sha256"] == bundle_digest(record), "calibration bundle mismatch; reassess changed VMO/SKA")
        require(cal["scale"] == "cardinal" and cal["units"] == "dimensionless", "product needs cardinal dimensionless factors, never joules")
        refs(cal["evidence"], "calibration.evidence", True)
        factors = obj(assess["factors"], "VMO SKA", "factors")
        values = []
        for name, f in factors.items():
            obj(f, "value evidence", f"factor.{name}")
            refs(f["evidence"], f"factor.{name}.evidence", f["value"] is not None)
            if f["value"] is not None:
                require(0 <= number(f["value"], name) <= 1, "factor outside declared [0,1] domain")
            values.append(f["value"])
        if all(v is not None for v in values):
            candidate = math.prod(values)
        findings.append("Experimental arithmetic only; calibration documentation is not validated calibration.")
    rev = obj(record["revision"], "parent_id changed_fields reason evidence", "revision")
    text(rev["reason"], "revision.reason")
    fields = words(rev["changed_fields"], "changed_fields", False)
    require(set(fields) <= set(contract["revision_fields"]), "unknown revision field")
    refs(rev["evidence"], "revision.evidence", rev["parent_id"] is not None)
    if rev["parent_id"] is None:
        require(not fields, "initial record cannot claim changed fields")
    else:
        text(rev["parent_id"], "parent_id")
        require(rev["parent_id"] != record["id"] and bool(fields), "revision must be new and declare changes")
    return {"contract_satisfied": True, "record_id": record["id"],
            "experimental_candidate": candidate, "units": "dimensionless" if candidate is not None else None,
            "disposition": "HOLD" if g["authorization"] != "documented" or g["justice"] != "reviewed" else "REVIEW_ONLY",
            "may_execute": False, "empirical_validation": False, "findings": findings}


def validate(record, contract, previous=None):
    result = _validate(record, contract)
    parent = record["revision"]["parent_id"]
    require((parent is None) == (previous is None), "linked revision requires exactly its previous record")
    if previous is not None:
        _validate(previous, contract)
        require(previous["id"] == parent, "wrong revision parent")
        require(stamp(record["context"]["as_of"], "as_of") >= stamp(previous["context"]["as_of"], "previous.as_of"), "revision time goes backwards")
        old_evidence = {e["id"]: e for e in previous["evidence"]}
        new_evidence = {e["id"]: e for e in record["evidence"]}
        require(all(new_evidence.get(key) == value for key, value in old_evidence.items()),
                "revision erased or rewrote prior evidence")
        # A changed target is a future criterion, not a new success on an old run.
        criteria = ("metric", "unit", "threshold", "comparator", "objective_id")
        old_kpis = previous["ska"]["kpis"]
        for new_kpi in record["ska"]["kpis"]:
            if new_kpi["status"] == "unknown":
                continue
            own_prior = next((k for k in old_kpis if k["id"] == new_kpi["id"]), None)
            if own_prior is None:
                own_prior = next((k for k in old_kpis
                                  if all(k[key] == new_kpi[key] for key in criteria)
                                  and set(k["evidence"]) & set(new_kpi["evidence"])), None)
            # Existing identity wins: distinct unchanged criteria can share an observation.
            # Only a new/renamed identity falls back to evidence reuse detection.
            for old_kpi in [own_prior] if own_prior is not None else old_kpis:
                same_id = new_kpi["id"] == old_kpi["id"]
                reused = bool(set(new_kpi["evidence"]) & set(old_kpi["evidence"]))
                changed = any(new_kpi[key] != old_kpi[key] for key in criteria)
                if reused and new_kpi["observed_at"] == old_kpi["observed_at"]:
                    require(new_kpi["value"] == old_kpi["value"],
                            "same observation cannot silently change measured value")
                if changed and (same_id or reused):
                    fresh = stamp(new_kpi["observed_at"], "observed_at") > stamp(previous["context"]["as_of"], "previous.as_of")
                    require(fresh and not reused,
                            "changed KPI criterion needs a fresh observation or unknown status; old failure is not new success")
        def fields(r):
            return {**r["vmo"], **r["ska"], **{k: r[k] for k in ("context", "guardrails", "assessment")}}
        old, new = fields(previous), fields(record)
        actual = {key for key in old if old[key] != new[key]}
        require(actual == set(record["revision"]["changed_fields"]), "declared revision changes mismatch")
    result["revision_link_checked"] = previous is not None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", nargs="?", type=Path, default=HERE / "example.json")
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--check", action="store_true", help="check source pins and synthetic example")
    args = parser.parse_args()
    try:
        contract = load(HERE / "contract.json")
        source_check(contract)
        result = validate(load(args.record), contract, load(args.previous) if args.previous else None)
        print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))
        return 0
    except (ContractError, OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        print(json.dumps({"contract_satisfied": False, "error": str(exc), "may_execute": False,
                          "empirical_validation": False}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

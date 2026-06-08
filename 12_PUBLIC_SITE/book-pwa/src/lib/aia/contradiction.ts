// ─────────────────────────────────────────────────────────────────────────
// AIA · Contradiction routing — the dialectical engine.
//
// Contradiction is a visible branch-state, not an error. This module is pure
// *routing*: given a new claim, the reader's lineage, and the expansion mode,
// it decides which lane the tension belongs to, how severe it is, and whether
// the UI should freeze or merely badge. The hard "do these two claims actually
// conflict?" question is delegated to an injected ConflictProbe (an LLM in
// production, a deterministic stub in tests) — so the routing stays testable.
// ─────────────────────────────────────────────────────────────────────────

import type {
  BranchMode,
  Claim,
  ClassificationContext,
  ConflictKind,
  ConflictProbe,
  Contradiction,
  ContradictionType,
  ExpansionMode,
  Friction,
  IdFactory,
  Severity,
} from "./types";

/** Which epistemic lane a private branch lands in for a given expansion mode. */
export function branchModeForExpansionMode(mode: ExpansionMode): BranchMode {
  if (mode === "challenge") return "antithesis";
  if (mode === "synthesize") return "synthesis";
  return "mainline";
}

export type ContradictionAction =
  | "revise"
  | "warn"
  | "tension"
  | "ask"
  | "antithesis"
  | "reconcile"
  | "soft_warn";

export interface Policy {
  onContradiction: ContradictionAction;
  friction: "high" | "medium" | "low" | "none";
}

/**
 * The dialectical matrix: how strict to be about contradiction per mode.
 * Simplify must stay coherent; challenge expects contradiction; synthesis
 * feeds on it.
 */
export function contradictionPolicy(mode: ExpansionMode): Policy {
  switch (mode) {
    case "simplify":
      return { onContradiction: "revise", friction: "high" };
    case "technical":
      return { onContradiction: "revise", friction: "high" };
    case "expand":
    case "go_deeper":
      return { onContradiction: "tension", friction: "medium" };
    case "apply":
      return { onContradiction: "ask", friction: "medium" };
    case "challenge":
      return { onContradiction: "antithesis", friction: "none" };
    case "synthesize":
      return { onContradiction: "reconcile", friction: "none" };
    case "creative":
      return { onContradiction: "soft_warn", friction: "low" };
  }
}

/**
 * What the UI should do about a contradiction. The rule from the spec:
 * never interrupt the reader unless a *canon* conflict threatens the *mainline*.
 * Everything else renders quietly as a badge the reader can ignore, fork, or
 * synthesize.
 */
export function frictionFor(type: ContradictionType, branchMode: BranchMode): Friction {
  if (type === "canon_conflict" && branchMode === "mainline") return "freeze";
  return "badge";
}

type Lane = "canon" | "ancestor" | "sibling";

interface LaneHit {
  prior: Claim;
  kind: Exclude<ConflictKind, "none">;
  lane: Lane;
}

function firstConflict(
  next: Claim,
  ctx: ClassificationContext,
  probe: ConflictProbe,
): LaneHit | null {
  // Priority order: canon outranks the reader's own lineage outranks siblings.
  const lanes: Array<[Lane, Claim[]]> = [
    ["canon", ctx.canonClaims],
    ["ancestor", [...ctx.ancestorClaims, ...ctx.mainlineCommitments]],
    ["sibling", ctx.siblingClaims],
  ];
  for (const [lane, claims] of lanes) {
    for (const prior of claims) {
      const kind = probe(next, prior);
      if (kind !== "none") return { prior, kind, lane };
    }
  }
  return null;
}

function severityFor(lane: Lane, kind: Exclude<ConflictKind, "none">): Severity {
  if (lane === "canon") return kind === "hard" ? "high" : "medium";
  if (lane === "ancestor") return kind === "hard" ? "medium" : "low";
  return "low"; // sibling tension is always low — productive pluralism
}

function typeFor(lane: Lane): ContradictionType {
  if (lane === "canon") return "canon_conflict";
  if (lane === "ancestor") return "ancestor_conflict";
  return "sibling_tension";
}

function explain(type: ContradictionType, next: Claim, prior: Claim | null): string {
  switch (type) {
    case "canon_conflict":
      return `New claim conflicts with the canonical commitment "${prior?.text ?? ""}".`;
    case "ancestor_conflict":
      return `New claim conflicts with your earlier commitment "${prior?.text ?? ""}".`;
    case "sibling_tension":
      return `This branch takes a different stance than a sibling branch on "${next.scope}".`;
    case "mode_intentional":
      return `Contradiction was explicitly requested for "${next.scope}".`;
  }
}

/**
 * Classify each new claim's tension (if any) against the reader's lineage.
 * Returns one Contradiction per conflicting claim, all `unresolved`.
 *
 * Invariants honoured:
 *  • #5 sludge boundary — sibling claims can only surface as `sibling_tension`,
 *    never get mistaken for the reader's own ancestor lineage.
 *  • #6 — `challenge`/antithesis expansions yield `mode_intentional`, never
 *    silent mainline drift.
 *  • purity — reads `ctx` only; never mutates it.
 */
export function classifyContradiction(
  newClaims: Claim[],
  ctx: ClassificationContext,
  probe: ConflictProbe,
  idFor: IdFactory,
): Contradiction[] {
  const branchMode = branchModeForExpansionMode(ctx.mode);
  const intentional = branchMode === "antithesis" || ctx.mode === "challenge";

  const out: Contradiction[] = [];
  for (const next of newClaims) {
    const hit = firstConflict(next, ctx, probe);
    if (!hit) continue;

    const type: ContradictionType = intentional ? "mode_intentional" : typeFor(hit.lane);
    const severity: Severity = intentional ? "low" : severityFor(hit.lane, hit.kind);

    out.push({
      id: idFor(`${next.id}:${hit.prior.id}`),
      type,
      severity,
      newClaimId: next.id,
      priorClaimId: hit.prior.id,
      explanation: explain(type, next, hit.prior),
      resolutionStatus: "unresolved",
    });
  }
  return out;
}

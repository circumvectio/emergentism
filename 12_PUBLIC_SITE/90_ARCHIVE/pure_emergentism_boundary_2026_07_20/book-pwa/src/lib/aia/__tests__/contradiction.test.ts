import { describe, it, expect } from "vitest";
import {
  branchModeForExpansionMode,
  contradictionPolicy,
  frictionFor,
  classifyContradiction,
} from "../contradiction";
import type { Claim, ClassificationContext, ConflictProbe } from "../types";

const claim = (over: Partial<Claim> & { id: string }): Claim => ({
  text: over.text ?? "a claim",
  scope: over.scope ?? "P_node_equals_phi_times_v",
  stance: over.stance ?? "asserted",
  sourceBranchId: over.sourceBranchId ?? "br_x",
  confidence: over.confidence ?? 0.9,
  ...over,
});

// Deterministic probe: two claims conflict iff their scope matches and one
// denies what the other asserts. No model, no randomness.
const stanceProbe: ConflictProbe = (next, prior) => {
  if (next.scope !== prior.scope) return "none";
  const opposed =
    (next.stance === "asserted" && prior.stance === "denied") ||
    (next.stance === "denied" && prior.stance === "asserted");
  if (opposed) return "hard";
  if (next.stance === "qualified" || prior.stance === "qualified") return "soft";
  return "none";
};

const idFor = (seed: string) => `c_${seed}`;

const baseCtx = (over: Partial<ClassificationContext> = {}): ClassificationContext => ({
  canonClaims: [],
  ancestorClaims: [],
  siblingClaims: [],
  mainlineCommitments: [],
  mode: "go_deeper",
  ...over,
});

describe("branchModeForExpansionMode", () => {
  it("routes challenge → antithesis", () => {
    expect(branchModeForExpansionMode("challenge")).toBe("antithesis");
  });
  it("routes synthesize → synthesis", () => {
    expect(branchModeForExpansionMode("synthesize")).toBe("synthesis");
  });
  it("routes ordinary expansion → mainline", () => {
    expect(branchModeForExpansionMode("go_deeper")).toBe("mainline");
    expect(branchModeForExpansionMode("simplify")).toBe("mainline");
  });
});

describe("contradictionPolicy (the dialectical matrix)", () => {
  it("makes simplify contradictions high-friction (likely invalid)", () => {
    expect(contradictionPolicy("simplify").friction).toBe("high");
  });
  it("treats challenge contradictions as expected (no friction)", () => {
    const p = contradictionPolicy("challenge");
    expect(p.friction).toBe("none");
    expect(p.onContradiction).toBe("antithesis");
  });
  it("treats synthesize contradictions as raw material", () => {
    expect(contradictionPolicy("synthesize").onContradiction).toBe("reconcile");
  });
});

describe("frictionFor — only freeze when a canon conflict threatens the mainline", () => {
  it("freezes a canon_conflict on a mainline branch", () => {
    expect(frictionFor("canon_conflict", "mainline")).toBe("freeze");
  });
  it("only badges a canon_conflict on an antithesis branch", () => {
    expect(frictionFor("canon_conflict", "antithesis")).toBe("badge");
  });
  it("never freezes ancestor/sibling/intentional tensions", () => {
    expect(frictionFor("ancestor_conflict", "mainline")).toBe("badge");
    expect(frictionFor("sibling_tension", "mainline")).toBe("badge");
    expect(frictionFor("mode_intentional", "antithesis")).toBe("badge");
  });
});

describe("classifyContradiction", () => {
  it("flags a hard conflict with canon as canon_conflict / high severity", () => {
    const next = claim({ id: "n1", scope: "ethics", stance: "asserted" });
    const ctx = baseCtx({
      canonClaims: [claim({ id: "k1", scope: "ethics", stance: "denied" })],
    });
    const out = classifyContradiction([next], ctx, stanceProbe, idFor);
    expect(out).toHaveLength(1);
    expect(out[0].type).toBe("canon_conflict");
    expect(out[0].severity).toBe("high");
    expect(out[0].newClaimId).toBe("n1");
    expect(out[0].priorClaimId).toBe("k1");
    expect(out[0].resolutionStatus).toBe("unresolved");
  });

  it("flags a conflict with the reader's own earlier branch as ancestor_conflict", () => {
    const next = claim({ id: "n1", scope: "value", stance: "asserted" });
    const ctx = baseCtx({
      ancestorClaims: [claim({ id: "a1", scope: "value", stance: "denied" })],
    });
    const out = classifyContradiction([next], ctx, stanceProbe, idFor);
    expect(out).toHaveLength(1);
    expect(out[0].type).toBe("ancestor_conflict");
  });

  // Invariant #6: challenge mode must produce an antithesis, never silent mainline drift.
  it("labels challenge-mode conflicts as mode_intentional, not canon/ancestor drift", () => {
    const next = claim({ id: "n1", scope: "ethics", stance: "denied" });
    const ctx = baseCtx({
      mode: "challenge",
      canonClaims: [claim({ id: "k1", scope: "ethics", stance: "asserted" })],
    });
    const out = classifyContradiction([next], ctx, stanceProbe, idFor);
    expect(out).toHaveLength(1);
    expect(out[0].type).toBe("mode_intentional");
    expect(out[0].severity).toBe("low");
  });

  // Invariant #5 (sludge boundary): a sibling's claim can only ever surface as
  // sibling_tension — never get mistaken for the reader's own ancestor lineage.
  it("keeps sibling disagreement in the sibling_tension lane (no cross-node bleed)", () => {
    const next = claim({ id: "n1", scope: "model", stance: "asserted" });
    const ctx = baseCtx({
      siblingClaims: [claim({ id: "s1", scope: "model", stance: "denied" })],
    });
    const out = classifyContradiction([next], ctx, stanceProbe, idFor);
    expect(out).toHaveLength(1);
    expect(out[0].type).toBe("sibling_tension");
    expect(out[0].severity).toBe("low");
  });

  it("returns nothing when the new claims are consistent", () => {
    const next = claim({ id: "n1", scope: "ethics", stance: "asserted" });
    const ctx = baseCtx({
      canonClaims: [claim({ id: "k1", scope: "ethics", stance: "asserted" })],
    });
    expect(classifyContradiction([next], ctx, stanceProbe, idFor)).toEqual([]);
  });

  it("is pure — does not mutate the context it is given", () => {
    const next = claim({ id: "n1", scope: "ethics", stance: "asserted" });
    const ctx = baseCtx({
      canonClaims: [claim({ id: "k1", scope: "ethics", stance: "denied" })],
    });
    const snapshot = JSON.stringify(ctx);
    classifyContradiction([next], ctx, stanceProbe, idFor);
    expect(JSON.stringify(ctx)).toBe(snapshot);
  });
});

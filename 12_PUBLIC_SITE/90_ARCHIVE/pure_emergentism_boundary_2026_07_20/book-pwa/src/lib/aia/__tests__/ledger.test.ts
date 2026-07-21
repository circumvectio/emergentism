import { describe, it, expect } from "vitest";
import { resolveContradiction, type LedgerState } from "../ledger";
import type { Claim, Contradiction } from "../types";

const claim = (id: string, scope: string): Claim => ({
  id,
  text: `claim ${id}`,
  scope,
  stance: "asserted",
  sourceBranchId: "br_x",
  confidence: 0.9,
});

const contradiction = (id: string): Contradiction => ({
  id,
  type: "ancestor_conflict",
  severity: "medium",
  newClaimId: "n1",
  priorClaimId: "a1",
  explanation: "tension",
  resolutionStatus: "unresolved",
});

const baseState = (): LedgerState => ({
  claimsById: { n1: claim("n1", "value"), a1: claim("a1", "value") },
  contradictionsById: { x1: contradiction("x1") },
});

describe("resolveContradiction", () => {
  it("marks keep_as_antithesis", () => {
    const next = resolveContradiction(baseState(), { contradictionId: "x1", action: "keep_as_antithesis" });
    expect(next.contradictionsById.x1.resolutionStatus).toBe("accepted_as_antithesis");
  });

  it("marks revise / fork / dismiss to their statuses", () => {
    const s = baseState();
    expect(resolveContradiction(s, { contradictionId: "x1", action: "revise" }).contradictionsById.x1.resolutionStatus).toBe("revised");
    expect(resolveContradiction(s, { contradictionId: "x1", action: "fork" }).contradictionsById.x1.resolutionStatus).toBe("forked");
    expect(resolveContradiction(s, { contradictionId: "x1", action: "dismiss" }).contradictionsById.x1.resolutionStatus).toBe("dismissed");
  });

  it("synthesize records a synthesis claim and marks synthesized", () => {
    const synthesis = claim("syn1", "value");
    const next = resolveContradiction(baseState(), {
      contradictionId: "x1",
      action: "synthesize",
      synthesisClaim: synthesis,
    });
    expect(next.contradictionsById.x1.resolutionStatus).toBe("synthesized");
    expect(next.claimsById.syn1).toEqual(synthesis);
  });

  it("does not mutate the input state", () => {
    const s = baseState();
    const snapshot = JSON.stringify(s);
    resolveContradiction(s, { contradictionId: "x1", action: "revise" });
    expect(JSON.stringify(s)).toBe(snapshot);
  });

  it("returns state unchanged for an unknown contradiction id", () => {
    const s = baseState();
    const next = resolveContradiction(s, { contradictionId: "nope", action: "revise" });
    expect(next).toEqual(s);
  });
});

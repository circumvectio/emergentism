import { describe, expect, it } from "vitest";
import {
  buildConsistencyReportPrompt,
  conflictProbeFromConsistencyReport,
  fallbackConsistencyReport,
  parseConsistencyReportText,
} from "../consistency";
import type { Claim, Contradiction } from "../types";

const claim = (over: Partial<Claim> & { id: string }): Claim => ({
  id: over.id,
  text: over.text ?? "AIA branches preserve reader commitments.",
  scope: over.scope ?? "aia_branch_constitution",
  stance: over.stance ?? "asserted",
  sourceBranchId: over.sourceBranchId ?? "branch-1",
  confidence: over.confidence ?? 0.9,
});

const contradiction = (over: Partial<Contradiction> = {}): Contradiction => ({
  id: over.id ?? "contradiction-1",
  type: over.type ?? "ancestor_conflict",
  severity: over.severity ?? "medium",
  newClaimId: over.newClaimId ?? "claim-1",
  priorClaimId: over.priorClaimId ?? "prior-1",
  explanation: over.explanation ?? "New claim conflicts with an earlier commitment.",
  resolutionStatus: over.resolutionStatus ?? "unresolved",
});

describe("AIA consistency report", () => {
  it("builds a bounded model prompt from claims, commitments, and contradictions", () => {
    const prompt = buildConsistencyReportPrompt({
      branchId: "branch-1",
      branchMode: "mainline",
      mode: "expand",
      generatedClaims: [claim({ id: "claim-1" })],
      commitments: [claim({ id: "prior-1", sourceBranchId: "main" })],
      openTensions: ["Whether stale branches should rebase is unresolved."],
      contradictions: [contradiction()],
    });

    expect(prompt).toContain("branchId: branch-1");
    expect(prompt).toContain("branchMode: mainline");
    expect(prompt).toContain("claim-1");
    expect(prompt).toContain("prior-1");
    expect(prompt).toContain("Whether stale branches should rebase is unresolved.");
    expect(prompt).toContain("Return only JSON");
  });

  it("parses model JSON into a normalized report", () => {
    const report = parseConsistencyReportText(
      JSON.stringify({
        status: "soft_tension",
        summary: "One tension needs review.",
        items: [
          {
            claimId: "claim-1",
            relation: "tension",
            priorClaimId: "prior-1",
            severity: "medium",
            explanation: "The branch qualifies an earlier commitment.",
          },
        ],
      }),
      [claim({ id: "claim-1" })]
    );

    expect(report).toEqual({
      reportSource: "model",
      status: "soft_tension",
      summary: "One tension needs review.",
      items: [
        {
          claimId: "claim-1",
          relation: "tension",
          priorClaimId: "prior-1",
          severity: "medium",
          explanation: "The branch qualifies an earlier commitment.",
        },
      ],
    });
  });

  it("falls back to a deterministic report when model JSON is unavailable", () => {
    expect(parseConsistencyReportText("not json", [claim({ id: "claim-1" })])).toBeNull();

    const report = fallbackConsistencyReport({
      generatedClaims: [claim({ id: "claim-1" })],
      contradictions: [contradiction({ severity: "high", type: "canon_conflict" })],
    });

    expect(report.status).toBe("canon_conflict");
    expect(report.reportSource).toBe("heuristic");
    expect(report.items[0]).toEqual(
      expect.objectContaining({
        claimId: "claim-1",
        relation: "conflict",
        severity: "high",
      })
    );
  });

  it("turns report relations into a conflict probe for classification", () => {
    const report = parseConsistencyReportText(
      JSON.stringify({
        status: "hard_contradiction",
        summary: "One claim conflicts with a commitment.",
        items: [
          {
            claimId: "claim-1",
            relation: "conflict",
            priorClaimId: "prior-1",
            severity: "high",
            explanation: "The report sees a semantic conflict.",
          },
          {
            claimId: "claim-2",
            relation: "tension",
            priorClaimId: "prior-2",
            severity: "medium",
            explanation: "The report sees a softer tension.",
          },
        ],
      }),
      [claim({ id: "claim-1" }), claim({ id: "claim-2" })]
    );

    expect(report).not.toBeNull();
    const probe = conflictProbeFromConsistencyReport(report!);

    expect(probe(claim({ id: "claim-1" }), claim({ id: "prior-1" }))).toBe("hard");
    expect(probe(claim({ id: "claim-2" }), claim({ id: "prior-2" }))).toBe("soft");
    expect(probe(claim({ id: "claim-1" }), claim({ id: "prior-2" }))).toBe("none");
  });
});

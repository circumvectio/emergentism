import { beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  branchFindMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      findMany: mocks.branchFindMany,
    },
  },
}));

describe("GET /api/branches", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.branchFindMany.mockResolvedValue([
      {
        id: "branch-1",
        sourceNodeId: "node-1",
        sourceVersionHash: "hash-1",
        depth: 1,
        outputMd: "Generated branch.",
        branchMode: "mainline",
        mode: "expand",
        visibility: "private",
        consistencyStatus: "soft_tension",
        consistencyReportJson: JSON.stringify({
          reportSource: "model",
          status: "soft_tension",
          summary: "One claim needs review.",
          items: [
            {
              claimId: "claim-1",
              relation: "tension",
              severity: "medium",
              explanation: "The branch qualifies an earlier commitment.",
            },
          ],
        }),
        contradictions: [
          {
            id: "contradiction-1",
            type: "ancestor_conflict",
            severity: "medium",
            explanation: "New claim conflicts with your earlier commitment.",
            resolutionStatus: "unresolved",
          },
        ],
        reviews: [
          {
            id: "review-1",
            decision: "revise",
            notes: "This branch needs a narrower claim before canon promotion.",
            createdAt: new Date("2026-05-31T00:00:00.000Z"),
          },
        ],
      },
    ]);
  });

  it("returns owned branches and contradiction summaries for requested nodes", async () => {
    const response = await GET(
      new Request("http://localhost/api/branches?nodeIds=node-1,node-2")
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).toHaveBeenCalledWith({
      where: {
        userId: "user-1",
        sourceNodeId: { in: ["node-1", "node-2"] },
      },
      include: {
        contradictions: {
          orderBy: { createdAt: "asc" },
        },
        reviews: {
          where: {
            decision: { in: ["reject", "revise"] },
          },
          orderBy: { createdAt: "desc" },
          take: 1,
        },
      },
      orderBy: { createdAt: "asc" },
    });
    await expect(response.json()).resolves.toEqual({
      branches: [
        expect.objectContaining({
          localId: "server:branch-1",
          serverId: "branch-1",
          sourceNodeId: "node-1",
          sourceVersionHash: "hash-1",
          status: "complete",
          visibility: "private",
          consistencyStatus: "soft_tension",
          reviewStatus: "revision_requested",
          reviewFeedback: "This branch needs a narrower claim before canon promotion.",
          consistencyReport: {
            reportSource: "model",
            status: "soft_tension",
            summary: "One claim needs review.",
            items: [
              {
                claimId: "claim-1",
                relation: "tension",
                severity: "medium",
                explanation: "The branch qualifies an earlier commitment.",
              },
            ],
          },
          contradictions: [
            expect.objectContaining({
              id: "contradiction-1",
              resolutionStatus: "unresolved",
            }),
          ],
        }),
      ],
    });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET(new Request("http://localhost/api/branches?nodeIds=node-1"));

    expect(response.status).toBe(401);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
  });

  it("returns unauthorized when Clerk auth cannot run locally", async () => {
    mocks.auth.mockRejectedValueOnce(new Error("missing middleware"));

    const response = await GET(new Request("http://localhost/api/branches?nodeIds=node-1"));

    expect(response.status).toBe(401);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
  });

  it("returns an empty list when no node ids are requested", async () => {
    const response = await GET(new Request("http://localhost/api/branches"));

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ branches: [] });
  });
});

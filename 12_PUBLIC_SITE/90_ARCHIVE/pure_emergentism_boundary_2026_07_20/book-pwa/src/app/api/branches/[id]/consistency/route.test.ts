import { beforeEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  anthropicCreate: vi.fn(),
  branchFindFirst: vi.fn(),
  branchUpdate: vi.fn(),
  branchConstitutionUpsert: vi.fn(),
  contradictionDeleteMany: vi.fn(),
  contradictionCreateMany: vi.fn(),
  userCreate: vi.fn(),
  userFindUnique: vi.fn(),
  userUpdate: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@anthropic-ai/sdk", () => ({
  default: vi.fn().mockImplementation(() => ({
    messages: {
      create: mocks.anthropicCreate,
    },
  })),
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      findFirst: mocks.branchFindFirst,
      update: mocks.branchUpdate,
    },
    branchConstitution: {
      upsert: mocks.branchConstitutionUpsert,
    },
    aIAContradiction: {
      deleteMany: mocks.contradictionDeleteMany,
      createMany: mocks.contradictionCreateMany,
    },
    user: {
      create: mocks.userCreate,
      findUnique: mocks.userFindUnique,
      update: mocks.userUpdate,
    },
  },
}));

function branch(overrides: Record<string, unknown> = {}) {
  return {
    id: "branch-1",
    userId: "user-1",
    sourceNodeId: "node-1",
    sourceVersionHash: "node-v1",
    outputMd: "- [asserted] aia_branch_constitution: AIA branches preserve reader commitments.",
    branchMode: "mainline",
    mode: "expand",
    depth: 1,
    visibility: "private",
    consistencyStatus: "unchecked",
    sourceNode: {
      currentVersion: {
        hash: "node-v1",
      },
    },
    ...overrides,
  };
}

describe("POST /api/branches/[id]/consistency", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.userFindUnique.mockResolvedValue({
      id: "user-1",
      plan: "Free",
      creditsRemaining: 3,
    });
    mocks.userCreate.mockResolvedValue({
      id: "user-1",
      plan: "Free",
      creditsRemaining: 3,
    });
    mocks.userUpdate.mockResolvedValue({
      id: "user-1",
      creditsRemaining: 2,
    });
    mocks.branchFindFirst.mockResolvedValue(branch());
    mocks.branchConstitutionUpsert.mockResolvedValue({
      branchId: "user:user-1:main",
      version: 3,
      acceptedCommitmentsJson: JSON.stringify([
        {
          id: "claim-existing",
          text: "AIA branches preserve reader commitments.",
          scope: "aia_branch_constitution",
          stance: "asserted",
          sourceBranchId: "user:user-1:main",
          confidence: 1,
        },
      ]),
      openTensionsJson: JSON.stringify([]),
      preferredStyle: "quiet-utility",
    });
    mocks.anthropicCreate.mockResolvedValue({
      content: [
        {
          type: "text",
          text: JSON.stringify({
            status: "consistent",
            summary: "Edited branch is compatible with the active constitution.",
            items: [
              {
                claimId: "claim:branch-1:1",
                relation: "supports",
                priorClaimId: "claim-existing",
                severity: "low",
                explanation: "The edited branch preserves the same commitment.",
              },
            ],
          }),
        },
      ],
    });
    mocks.branchUpdate.mockResolvedValue({ id: "branch-1" });
    mocks.contradictionDeleteMany.mockResolvedValue({ count: 1 });
    mocks.contradictionCreateMany.mockResolvedValue({ count: 0 });
  });

  it("refreshes an owned branch consistency report and clears stale contradiction rows", async () => {
    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindFirst).toHaveBeenCalledWith({
      where: {
        id: "branch-1",
        userId: "user-1",
      },
      include: {
        sourceNode: {
          include: {
            currentVersion: true,
          },
        },
      },
    });
    expect(mocks.anthropicCreate).toHaveBeenCalledWith(
      expect.objectContaining({
        system: expect.stringContaining("AIA consistency reviewer"),
        messages: [
          expect.objectContaining({
            content: expect.stringContaining("[GENERATED CLAIMS]"),
          }),
        ],
      })
    );
    expect(mocks.contradictionDeleteMany).toHaveBeenCalledWith({
      where: {
        branchId: "branch-1",
        userId: "user-1",
      },
    });
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: {
        consistencyStatus: "consistent",
        consistencyReportSource: "model",
        consistencySummary: "Edited branch is compatible with the active constitution.",
        consistencyReportJson: expect.stringContaining('"status":"consistent"'),
      },
    });
    expect(mocks.userUpdate).toHaveBeenCalledWith({
      where: { id: "user-1" },
      data: { creditsRemaining: 2 },
    });
    await expect(response.json()).resolves.toEqual({
      branch: {
        id: "branch-1",
        consistencyStatus: "consistent",
        consistencySummary: "Edited branch is compatible with the active constitution.",
      },
      consistencyReport: expect.objectContaining({
        status: "consistent",
        reportSource: "model",
      }),
      contradictions: [],
    });
  });

  it("falls back to a heuristic report when model JSON is malformed", async () => {
    mocks.anthropicCreate.mockResolvedValueOnce({
      content: [{ type: "text", text: "not-json" }],
    });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: expect.objectContaining({
        consistencyStatus: "consistent",
        consistencyReportSource: "heuristic",
      }),
    });
  });

  it("rejects stale-source branches before spending a consistency model call", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      branch({
        sourceVersionHash: "node-v1",
        sourceNode: {
          currentVersion: {
            hash: "node-v2",
          },
        },
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.anthropicCreate).not.toHaveBeenCalled();
    expect(mocks.branchUpdate).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "stale_source_version" });
  });

  it("rejects non-private branches before mutating consistency metadata", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(branch({ visibility: "proposed_canon" }));

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.anthropicCreate).not.toHaveBeenCalled();
    expect(mocks.contradictionDeleteMany).not.toHaveBeenCalled();
    expect(mocks.contradictionCreateMany).not.toHaveBeenCalled();
    expect(mocks.branchUpdate).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "branch_not_private" });
  });

  it("rejects free users without credits before spending a consistency model call", async () => {
    mocks.userFindUnique.mockResolvedValueOnce({
      id: "user-1",
      plan: "Free",
      creditsRemaining: 0,
    });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(403);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
    expect(mocks.anthropicCreate).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({
      error: "Out of credits. Please upgrade to Explorer.",
    });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
  });

  it("returns not found for branches outside the current user", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(null);

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/consistency", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(404);
    expect(mocks.branchUpdate).not.toHaveBeenCalled();
  });
});

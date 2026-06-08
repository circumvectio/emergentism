import { beforeEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  branchFindFirst: vi.fn(),
  branchUpdateMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      findFirst: mocks.branchFindFirst,
      updateMany: mocks.branchUpdateMany,
    },
  },
}));

function branch(overrides: Record<string, unknown> = {}) {
  return {
    id: "branch-1",
    userId: "user-1",
    sourceNodeId: "node-1",
    sourceVersionHash: "node-v1",
    visibility: "private",
    consistencyStatus: "consistent",
    sourceNode: {
      currentVersion: {
        hash: "node-v1",
      },
    },
    ...overrides,
  };
}

describe("POST /api/branches/[id]/proposal", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.branchFindFirst.mockResolvedValue(branch());
    mocks.branchUpdateMany.mockResolvedValue({ count: 1 });
  });

  it("marks an owned branch as proposed canon when pinned source version is current", async () => {
    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
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
    expect(mocks.branchUpdateMany).toHaveBeenCalledWith({
      where: {
        id: "branch-1",
        userId: "user-1",
        sourceVersionHash: "node-v1",
      },
      data: {
        visibility: "proposed_canon",
      },
    });
    await expect(response.json()).resolves.toEqual({
      branch: {
        id: "branch-1",
        visibility: "proposed_canon",
      },
    });
  });

  it("rejects canon proposal when the source node current version has moved", async () => {
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
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({
      error: "stale_source_version",
    });
  });

  it("rejects canon proposal when the branch has an unresolved canon conflict", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      branch({
        consistencyStatus: "canon_conflict",
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({
      error: "canon_conflict",
    });
  });

  it("rejects canon proposal when branch consistency is unchecked after revision", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      branch({
        consistencyStatus: "unchecked",
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({
      error: "consistency_unchecked",
    });
  });

  it("returns not found for branches outside the current user", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(null);

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(404);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });

  it("returns unauthorized when Clerk auth cannot run locally", async () => {
    mocks.auth.mockRejectedValueOnce(new Error("missing middleware"));

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/proposal", {
        method: "POST",
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });
});

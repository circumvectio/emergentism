import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  branchFindFirst: vi.fn(),
  transaction: vi.fn(),
  graphWriteLockUpsert: vi.fn(),
  nodeVersionCreate: vi.fn(),
  nodeUpdateMany: vi.fn(),
  canonReviewCreate: vi.fn(),
  branchUpdate: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      findFirst: mocks.branchFindFirst,
    },
    user: {
      findUnique: mocks.userFindUnique,
    },
    $transaction: mocks.transaction,
  },
}));

function proposedBranch(overrides: Record<string, unknown> = {}) {
  return {
    id: "branch-1",
    userId: "author-1",
    sourceNodeId: "node-1",
    sourceVersionHash: "node-v1",
    visibility: "proposed_canon",
    consistencyStatus: "consistent",
    outputMd: "Accepted canon text.",
    sourceNode: {
      id: "node-1",
      path: "root.node-1",
      currentVersion: {
        id: "version-1",
        hash: "node-v1",
      },
    },
    ...overrides,
  };
}

describe("POST /api/branches/[id]/review", () => {
  const originalReviewerIds = process.env.AIA_CANON_REVIEWER_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_CANON_REVIEWER_IDS = "reviewer-1";
    mocks.auth.mockResolvedValue({ userId: "reviewer-1" });
    mocks.userFindUnique.mockResolvedValue({ id: "reviewer-1", role: "reader" });
    mocks.branchFindFirst.mockResolvedValue(proposedBranch());
    mocks.nodeVersionCreate.mockResolvedValue({ id: "version-2", hash: "new-hash" });
    mocks.nodeUpdateMany.mockResolvedValue({ count: 1 });
    mocks.canonReviewCreate.mockResolvedValue({ id: "review-1" });
    mocks.branchUpdate.mockResolvedValue({ id: "branch-1" });
    mocks.transaction.mockImplementation(async (callback) =>
      callback({
        graphWriteLock: { upsert: mocks.graphWriteLockUpsert },
        nodeVersion: { create: mocks.nodeVersionCreate },
        node: { updateMany: mocks.nodeUpdateMany },
        canonReview: { create: mocks.canonReviewCreate },
        aIPBranch: { update: mocks.branchUpdate },
      })
    );
  });

  afterEach(() => {
    process.env.AIA_CANON_REVIEWER_IDS = originalReviewerIds;
  });

  it("accepts a proposed branch by minting a new canon node version under a version check", async () => {
    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept", notes: "Clean synthesis." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindFirst).toHaveBeenCalledWith({
      where: {
        id: "branch-1",
        visibility: "proposed_canon",
      },
      include: {
        sourceNode: {
          include: {
            currentVersion: true,
          },
        },
      },
    });
    expect(mocks.graphWriteLockUpsert).toHaveBeenCalledWith({
      where: { scope: "canon" },
      create: { scope: "canon" },
      update: {},
    });
    expect(mocks.nodeVersionCreate).toHaveBeenCalledWith({
      data: {
        hash: expect.stringMatching(/^[a-f0-9]{64}$/),
        nodeId: "node-1",
        contentMd: "Accepted canon text.",
        prevVersionId: "version-1",
        authorId: "reviewer-1",
      },
    });
    expect(mocks.nodeUpdateMany).toHaveBeenCalledWith({
      where: {
        id: "node-1",
        currentVersionId: "version-1",
      },
      data: {
        currentVersionId: "version-2",
      },
    });
    expect(mocks.canonReviewCreate).toHaveBeenCalledWith({
      data: {
        branchId: "branch-1",
        reviewerId: "reviewer-1",
        decision: "accept",
        notes: "Clean synthesis.",
      },
    });
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: { visibility: "accepted_canon" },
    });
    await expect(response.json()).resolves.toEqual({
      branch: {
        id: "branch-1",
        visibility: "accepted_canon",
      },
      review: {
        decision: "accept",
      },
      canon: {
        nodeId: "node-1",
        currentVersionId: "version-2",
      },
    });
  });

  it("rejects a proposed branch without changing canon", async () => {
    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "reject", notes: "Not canonical." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.nodeVersionCreate).not.toHaveBeenCalled();
    expect(mocks.nodeUpdateMany).not.toHaveBeenCalled();
    expect(mocks.canonReviewCreate).toHaveBeenCalledWith({
      data: {
        branchId: "branch-1",
        reviewerId: "reviewer-1",
        decision: "reject",
        notes: "Not canonical.",
      },
    });
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: { visibility: "private" },
    });
  });

  it("rejects accept when the source node current version has moved", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      proposedBranch({
        sourceVersionHash: "node-v1",
        sourceNode: {
          id: "node-1",
          path: "root.node-1",
          currentVersion: {
            id: "version-2",
            hash: "node-v2",
          },
        },
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.transaction).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "stale_source_version" });
  });

  it("rejects accept when the proposed branch has an unresolved canon conflict", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      proposedBranch({
        consistencyStatus: "canon_conflict",
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(409);
    expect(mocks.transaction).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "canon_conflict" });
  });

  it("still allows reviewers to reject canon-conflict proposals", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      proposedBranch({
        consistencyStatus: "canon_conflict",
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "reject" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.nodeVersionCreate).not.toHaveBeenCalled();
    expect(mocks.canonReviewCreate).toHaveBeenCalledWith({
      data: {
        branchId: "branch-1",
        reviewerId: "reviewer-1",
        decision: "reject",
        notes: undefined,
      },
    });
  });

  it("returns canon-conflict proposals for revision with the consistency summary attached", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(
      proposedBranch({
        consistencyStatus: "canon_conflict",
        consistencySummary: "This branch reverses a canon commitment.",
      })
    );

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "revise" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.nodeVersionCreate).not.toHaveBeenCalled();
    expect(mocks.canonReviewCreate).toHaveBeenCalledWith({
      data: {
        branchId: "branch-1",
        reviewerId: "reviewer-1",
        decision: "revise",
        notes: "This branch reverses a canon commitment.",
      },
    });
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: { visibility: "private" },
    });
    await expect(response.json()).resolves.toEqual({
      branch: {
        id: "branch-1",
        visibility: "private",
      },
      review: {
        decision: "revise",
        notes: "This branch reverses a canon commitment.",
      },
    });
  });

  it("returns not found when the branch is not proposed for canon", async () => {
    mocks.branchFindFirst.mockResolvedValueOnce(null);

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(404);
    expect(mocks.transaction).not.toHaveBeenCalled();
  });

  it("rejects unknown review decisions", async () => {
    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "publish" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(400);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
  });

  it("forbids authenticated users outside the canon reviewer policy", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ id: "reader-1", role: "reader" });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "accept" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(403);
    expect(mocks.userFindUnique).toHaveBeenCalledWith({
      where: { id: "reader-1" },
      select: { role: true },
    });
    expect(mocks.branchFindFirst).not.toHaveBeenCalled();
    expect(mocks.transaction).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "canon_reviewer_required" });
  });

  it("allows first-class canon reviewer users without the bootstrap allowlist", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reviewer-2" });
    mocks.userFindUnique.mockResolvedValueOnce({ id: "reviewer-2", role: "canon_reviewer" });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "reject" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.userFindUnique).toHaveBeenCalledWith({
      where: { id: "reviewer-2" },
      select: { role: true },
    });
    expect(mocks.branchFindFirst).toHaveBeenCalled();
  });

  it("allows first-class admin users to review canon", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "admin-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ id: "admin-1", role: "admin" });

    const response = await POST(
      new Request("http://localhost/api/branches/branch-1/review", {
        method: "POST",
        body: JSON.stringify({ decision: "reject" }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindFirst).toHaveBeenCalled();
  });
});

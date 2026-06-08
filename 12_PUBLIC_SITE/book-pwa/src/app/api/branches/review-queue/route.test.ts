import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  userFindMany: vi.fn(),
  branchFindMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    user: {
      findUnique: mocks.userFindUnique,
      findMany: mocks.userFindMany,
    },
    aIPBranch: {
      findMany: mocks.branchFindMany,
    },
  },
}));

describe("GET /api/branches/review-queue", () => {
  const originalReviewerIds = process.env.AIA_CANON_REVIEWER_IDS;
  const originalAdminIds = process.env.AIA_ADMIN_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_CANON_REVIEWER_IDS = "reviewer-1";
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValue({ userId: "reviewer-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
    mocks.userFindMany.mockResolvedValue([{ id: "author-1", email: "author@example.com" }]);
    mocks.branchFindMany.mockResolvedValue([
      {
        id: "branch-1",
        userId: "author-1",
        sourceNodeId: "node-1",
        sourceVersionHash: "hash-1",
        consistencyStatus: "soft_tension",
        consistencyReportSource: "model",
        consistencySummary: "One claim needs review.",
        outputMd: "Proposed canon text with enough words to preview.",
        createdAt: new Date("2026-05-31T00:00:00.000Z"),
        sourceNode: {
          title: "The Point",
          slug: "the-point-ylnsk",
          path: "root.the-point-ylnsk",
          currentVersion: {
            hash: "hash-1",
          },
        },
      },
    ]);
  });

  afterEach(() => {
    process.env.AIA_CANON_REVIEWER_IDS = originalReviewerIds;
    process.env.AIA_ADMIN_IDS = originalAdminIds;
  });

  it("returns pending proposed-canon branches for reviewers", async () => {
    const response = await GET(new Request("http://localhost/api/branches/review-queue"));

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).toHaveBeenCalledWith({
      where: { visibility: "proposed_canon" },
      orderBy: { createdAt: "desc" },
      take: 12,
      include: {
        sourceNode: {
          select: {
            title: true,
            slug: true,
            path: true,
            currentVersion: {
              select: { hash: true },
            },
          },
        },
      },
    });
    expect(mocks.userFindMany).toHaveBeenCalledWith({
      where: { id: { in: ["author-1"] } },
      select: { id: true, email: true },
    });
    await expect(response.json()).resolves.toEqual({
      branches: [
        {
          id: "branch-1",
          authorId: "author-1",
          authorEmail: "author@example.com",
          sourceNodeId: "node-1",
          sourceLabel: "The Point",
          sourceSlug: "the-point-ylnsk",
          sourceHref: "/book/the-point-ylnsk#node-node-1",
          sourceVersionHash: "hash-1",
          consistencyStatus: "soft_tension",
          consistencyReportSource: "model",
          consistencySummary: "One claim needs review.",
          currentVersionHash: "hash-1",
          isStaleSource: false,
          outputPreview: "Proposed canon text with enough words to preview.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });
  });

  it("supports pagination and marks stale-source proposals", async () => {
    mocks.branchFindMany.mockResolvedValueOnce([
      {
        id: "branch-2",
        userId: "author-2",
        sourceNodeId: "node-2",
        sourceVersionHash: "old-hash",
        consistencyStatus: "canon_conflict",
        consistencyReportSource: "heuristic",
        consistencySummary: "The local consistency router found unresolved tension in this branch.",
        outputMd: "Stale proposal",
        createdAt: new Date("2026-05-31T00:01:00.000Z"),
        sourceNode: {
          title: null,
          slug: "branch-source",
          path: "root.branch-source",
          currentVersion: {
            hash: "new-hash",
          },
        },
      },
    ]);
    mocks.userFindMany.mockResolvedValueOnce([]);

    const response = await GET(
      new Request("http://localhost/api/branches/review-queue?take=1&cursor=branch-1")
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).toHaveBeenCalledWith({
      where: { visibility: "proposed_canon" },
      orderBy: { createdAt: "desc" },
      take: 1,
      cursor: { id: "branch-1" },
      skip: 1,
      include: {
        sourceNode: {
          select: {
            title: true,
            slug: true,
            path: true,
            currentVersion: {
              select: { hash: true },
            },
          },
        },
      },
    });
    await expect(response.json()).resolves.toEqual({
      branches: [
        {
          id: "branch-2",
          authorId: "author-2",
          authorEmail: null,
          sourceNodeId: "node-2",
          sourceLabel: "branch-source",
          sourceSlug: "branch-source",
          sourceHref: "/book/branch-source#node-node-2",
          sourceVersionHash: "old-hash",
          consistencyStatus: "canon_conflict",
          consistencyReportSource: "heuristic",
          consistencySummary: "The local consistency router found unresolved tension in this branch.",
          currentVersionHash: "new-hash",
          isStaleSource: true,
          outputPreview: "Stale proposal",
          createdAt: "2026-05-31T00:01:00.000Z",
        },
      ],
      nextCursor: "branch-2",
    });
  });

  it("searches pending proposed-canon branches by source, branch, author, or output text", async () => {
    const response = await GET(new Request("http://localhost/api/branches/review-queue?q=presence"));

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).toHaveBeenCalledWith({
      where: {
        visibility: "proposed_canon",
        OR: [
          { id: { contains: "presence" } },
          { userId: { contains: "presence" } },
          { sourceNodeId: { contains: "presence" } },
          { outputMd: { contains: "presence" } },
          {
            sourceNode: {
              is: {
                OR: [
                  { title: { contains: "presence" } },
                  { slug: { contains: "presence" } },
                  { path: { contains: "presence" } },
                ],
              },
            },
          },
        ],
      },
      orderBy: { createdAt: "desc" },
      take: 12,
      include: {
        sourceNode: {
          select: {
            title: true,
            slug: true,
            path: true,
            currentVersion: {
              select: { hash: true },
            },
          },
        },
      },
    });
  });

  it("filters pending proposals by persisted consistency status", async () => {
    const response = await GET(
      new Request("http://localhost/api/branches/review-queue?consistency=canon_conflict")
    );

    expect(response.status).toBe(200);
    expect(mocks.branchFindMany).toHaveBeenCalledWith({
      where: {
        visibility: "proposed_canon",
        consistencyStatus: "canon_conflict",
      },
      orderBy: { createdAt: "desc" },
      take: 12,
      include: {
        sourceNode: {
          select: {
            title: true,
            slug: true,
            path: true,
            currentVersion: {
              select: { hash: true },
            },
          },
        },
      },
    });
  });

  it("rejects unknown consistency filters before reading the queue", async () => {
    const response = await GET(
      new Request("http://localhost/api/branches/review-queue?consistency=maybe")
    );

    expect(response.status).toBe(400);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "invalid_consistency_status" });
  });

  it("forbids ordinary readers before reading the queue", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "reader" });

    const response = await GET(new Request("http://localhost/api/branches/review-queue"));

    expect(response.status).toBe(403);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "canon_reviewer_required" });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET(new Request("http://localhost/api/branches/review-queue"));

    expect(response.status).toBe(401);
    expect(mocks.branchFindMany).not.toHaveBeenCalled();
  });
});

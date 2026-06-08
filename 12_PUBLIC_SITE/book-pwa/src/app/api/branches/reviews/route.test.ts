import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  userFindMany: vi.fn(),
  canonReviewFindMany: vi.fn(),
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
    canonReview: {
      findMany: mocks.canonReviewFindMany,
    },
  },
}));

describe("GET /api/branches/reviews", () => {
  const originalReviewerIds = process.env.AIA_CANON_REVIEWER_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_CANON_REVIEWER_IDS = "reviewer-1";
    mocks.auth.mockResolvedValue({ userId: "reviewer-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
    mocks.userFindMany.mockResolvedValue([
      { id: "reviewer-1", email: "reviewer@example.com" },
      { id: "reviewer-2", email: "second-reviewer@example.com" },
    ]);
    mocks.canonReviewFindMany.mockResolvedValue([
      {
        id: "review-1",
        branchId: "branch-1",
        reviewerId: "reviewer-1",
        decision: "accept",
        notes: "Clean synthesis.",
        createdAt: new Date("2026-05-31T00:00:00.000Z"),
        branch: {
          sourceNodeId: "node-1",
          sourceNode: {
            title: "The Point",
            slug: "the-point-ylnsk",
            path: "root.the-point-ylnsk",
          },
        },
      },
    ]);
  });

  afterEach(() => {
    process.env.AIA_CANON_REVIEWER_IDS = originalReviewerIds;
  });

  it("returns latest canon reviews for canon reviewers", async () => {
    const response = await GET();

    expect(response.status).toBe(200);
    expect(mocks.canonReviewFindMany).toHaveBeenCalledWith({
      orderBy: { createdAt: "desc" },
      take: 12,
      include: {
        branch: {
          select: {
            sourceNodeId: true,
            sourceNode: {
              select: {
                title: true,
                slug: true,
                path: true,
              },
            },
          },
        },
      },
    });
    expect(mocks.userFindMany).toHaveBeenCalledWith({
      where: { id: { in: ["reviewer-1"] } },
      select: { id: true, email: true },
    });
    await expect(response.json()).resolves.toEqual({
      reviews: [
        {
          id: "review-1",
          branchId: "branch-1",
          branchSourceNodeId: "node-1",
          branchSourceLabel: "The Point",
          branchSourceSlug: "the-point-ylnsk",
          branchSourceHref: "/book/the-point-ylnsk#node-node-1",
          reviewerId: "reviewer-1",
          reviewerEmail: "reviewer@example.com",
          decision: "accept",
          notes: "Clean synthesis.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });
  });

  it("filters and paginates canon review history", async () => {
    mocks.canonReviewFindMany.mockResolvedValueOnce([
      {
        id: "review-2",
        branchId: "branch-2",
        reviewerId: "reviewer-2",
        decision: "accept",
        notes: null,
        createdAt: new Date("2026-05-31T00:01:00.000Z"),
        branch: {
          sourceNodeId: "node-2",
          sourceNode: {
            title: null,
            slug: "branch-source",
            path: "root.branch-source",
          },
        },
      },
      {
        id: "review-3",
        branchId: "branch-2",
        reviewerId: "reviewer-2",
        decision: "accept",
        notes: "Ready.",
        createdAt: new Date("2026-05-31T00:00:00.000Z"),
        branch: {
          sourceNodeId: "node-2",
          sourceNode: {
            title: null,
            slug: "branch-source",
            path: "root.branch-source",
          },
        },
      },
    ]);

    const response = await GET(
      new Request(
        "http://localhost/api/branches/reviews?decision=accept&reviewerId=reviewer-2&branchId=branch-2&take=2&cursor=review-1"
      )
    );

    expect(response.status).toBe(200);
    expect(mocks.canonReviewFindMany).toHaveBeenCalledWith({
      where: {
        branchId: "branch-2",
        reviewerId: "reviewer-2",
        decision: "accept",
      },
      orderBy: { createdAt: "desc" },
      take: 2,
      cursor: { id: "review-1" },
      skip: 1,
      include: {
        branch: {
          select: {
            sourceNodeId: true,
            sourceNode: {
              select: {
                title: true,
                slug: true,
                path: true,
              },
            },
          },
        },
      },
    });
    await expect(response.json()).resolves.toEqual({
      reviews: [
        {
          id: "review-2",
          branchId: "branch-2",
          branchSourceNodeId: "node-2",
          branchSourceLabel: "branch-source",
          branchSourceSlug: "branch-source",
          branchSourceHref: "/book/branch-source#node-node-2",
          reviewerId: "reviewer-2",
          reviewerEmail: "second-reviewer@example.com",
          decision: "accept",
          notes: null,
          createdAt: "2026-05-31T00:01:00.000Z",
        },
        {
          id: "review-3",
          branchId: "branch-2",
          branchSourceNodeId: "node-2",
          branchSourceLabel: "branch-source",
          branchSourceSlug: "branch-source",
          branchSourceHref: "/book/branch-source#node-node-2",
          reviewerId: "reviewer-2",
          reviewerEmail: "second-reviewer@example.com",
          decision: "accept",
          notes: "Ready.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
      nextCursor: "review-3",
    });
  });

  it("searches review history by branch, source, reviewer, or notes text", async () => {
    const response = await GET(new Request("http://localhost/api/branches/reviews?q=syntropic"));

    expect(response.status).toBe(200);
    expect(mocks.canonReviewFindMany).toHaveBeenCalledWith({
      where: {
        OR: [
          { branchId: { contains: "syntropic" } },
          { reviewerId: { contains: "syntropic" } },
          { notes: { contains: "syntropic" } },
          {
            branch: {
              is: {
                OR: [
                  { id: { contains: "syntropic" } },
                  { userId: { contains: "syntropic" } },
                  { sourceNodeId: { contains: "syntropic" } },
                  { outputMd: { contains: "syntropic" } },
                  {
                    sourceNode: {
                      is: {
                        OR: [
                          { title: { contains: "syntropic" } },
                          { slug: { contains: "syntropic" } },
                          { path: { contains: "syntropic" } },
                        ],
                      },
                    },
                  },
                ],
              },
            },
          },
        ],
      },
      orderBy: { createdAt: "desc" },
      take: 12,
      include: {
        branch: {
          select: {
            sourceNodeId: true,
            sourceNode: {
              select: {
                title: true,
                slug: true,
                path: true,
              },
            },
          },
        },
      },
    });
  });

  it("rejects unknown canon review decisions before reading history", async () => {
    const response = await GET(new Request("http://localhost/api/branches/reviews?decision=publish"));

    expect(response.status).toBe(400);
    expect(mocks.canonReviewFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "invalid_decision" });
  });

  it("allows users with the persisted canon reviewer role", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reviewer-2" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "canon_reviewer" });

    const response = await GET();

    expect(response.status).toBe(200);
    expect(mocks.canonReviewFindMany).toHaveBeenCalledOnce();
  });

  it("forbids ordinary readers before reading review history", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "reader" });

    const response = await GET();

    expect(response.status).toBe(403);
    expect(mocks.canonReviewFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "canon_reviewer_required" });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET();

    expect(response.status).toBe(401);
    expect(mocks.canonReviewFindMany).not.toHaveBeenCalled();
  });
});

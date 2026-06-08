import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import type { Prisma } from "@prisma/client";
import { prisma } from "@/lib/prisma";

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

function allowlist(name: "AIA_CANON_REVIEWER_IDS" | "AIA_ADMIN_IDS"): string[] {
  return (process.env[name] ?? "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

async function canReadCanonReviews(userId: string): Promise<boolean> {
  if (allowlist("AIA_CANON_REVIEWER_IDS").includes(userId) || allowlist("AIA_ADMIN_IDS").includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "canon_reviewer" || user?.role === "admin";
}

type CanonReviewDecision = "accept" | "reject" | "revise";

function isCanonReviewDecision(value: string): value is CanonReviewDecision {
  return value === "accept" || value === "reject" || value === "revise";
}

function boundedTake(value: string | null): number {
  if (!value) return 12;
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return 12;
  return Math.min(50, Math.max(1, Math.trunc(parsed)));
}

function searchParams(req?: Request): URLSearchParams {
  return req ? new URL(req.url).searchParams : new URLSearchParams();
}

function branchSourceLabel(review: {
  branchId: string;
  branch?: {
    sourceNodeId?: string | null;
    sourceNode?: {
      title?: string | null;
      slug?: string | null;
      path?: string | null;
    } | null;
  } | null;
}): string {
  return (
    review.branch?.sourceNode?.title ||
    review.branch?.sourceNode?.slug ||
    review.branch?.sourceNode?.path ||
    review.branch?.sourceNodeId ||
    review.branchId
  );
}

function branchSourceSlug(review: {
  branch?: {
    sourceNode?: {
      slug?: string | null;
    } | null;
  } | null;
}): string | null {
  return review.branch?.sourceNode?.slug ?? null;
}

function sourceHref(slug: string | null | undefined, nodeId?: string | null): string | null {
  return slug && nodeId ? `/book/${encodeURIComponent(slug)}#node-${encodeURIComponent(nodeId)}` : null;
}

function reviewSearchPredicates(query: string): Prisma.CanonReviewWhereInput[] {
  return [
    { branchId: { contains: query } },
    { reviewerId: { contains: query } },
    { notes: { contains: query } },
    {
      branch: {
        is: {
          OR: [
            { id: { contains: query } },
            { userId: { contains: query } },
            { sourceNodeId: { contains: query } },
            { outputMd: { contains: query } },
            {
              sourceNode: {
                is: {
                  OR: [
                    { title: { contains: query } },
                    { slug: { contains: query } },
                    { path: { contains: query } },
                  ],
                },
              },
            },
          ],
        },
      },
    },
  ];
}

async function userEmailsById(ids: string[]): Promise<Map<string, string>> {
  const uniqueIds = Array.from(new Set(ids.filter(Boolean)));
  if (uniqueIds.length === 0) {
    return new Map();
  }

  const users = await prisma.user.findMany({
    where: { id: { in: uniqueIds } },
    select: { id: true, email: true },
  });

  return new Map(users.map((user) => [user.id, user.email]));
}

export async function GET(req?: Request) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  if (!(await canReadCanonReviews(userId))) {
    return NextResponse.json({ error: "canon_reviewer_required" }, { status: 403 });
  }

  const params = searchParams(req);
  const decision = params.get("decision")?.trim() ?? "";
  if (decision && !isCanonReviewDecision(decision)) {
    return NextResponse.json({ error: "invalid_decision" }, { status: 400 });
  }

  const where: Prisma.CanonReviewWhereInput = {};
  const branchId = params.get("branchId")?.trim();
  const reviewerId = params.get("reviewerId")?.trim();
  const searchQuery = params.get("q")?.trim();
  if (branchId) where.branchId = branchId;
  if (reviewerId) where.reviewerId = reviewerId;
  if (decision) where.decision = decision;
  if (searchQuery) where.OR = reviewSearchPredicates(searchQuery);

  const take = boundedTake(params.get("take"));
  const cursor = params.get("cursor")?.trim();
  const query = {
    orderBy: { createdAt: "desc" },
    take,
    ...(Object.keys(where).length > 0 ? { where } : {}),
    ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
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
  } satisfies Prisma.CanonReviewFindManyArgs;

  const reviews = await prisma.canonReview.findMany(query);
  const nextCursor = reviews.length === take ? reviews[reviews.length - 1]?.id : undefined;
  const userEmails = await userEmailsById(reviews.map((review) => review.reviewerId));

  return NextResponse.json({
    reviews: reviews.map((review) => {
      const sourceSlug = branchSourceSlug(review);
      const sourceNodeId = review.branch?.sourceNodeId ?? null;
      return {
        id: review.id,
        branchId: review.branchId,
        branchSourceNodeId: sourceNodeId,
        branchSourceLabel: branchSourceLabel(review),
        branchSourceSlug: sourceSlug,
        branchSourceHref: sourceHref(sourceSlug, sourceNodeId),
        reviewerId: review.reviewerId,
        reviewerEmail: userEmails.get(review.reviewerId) ?? null,
        decision: review.decision,
        notes: review.notes,
        createdAt: review.createdAt.toISOString(),
      };
    }),
    nextCursor,
  });
}

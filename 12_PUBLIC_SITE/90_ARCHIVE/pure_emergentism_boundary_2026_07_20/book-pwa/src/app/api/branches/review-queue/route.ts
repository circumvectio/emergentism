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

async function canReadReviewQueue(userId: string): Promise<boolean> {
  if (allowlist("AIA_CANON_REVIEWER_IDS").includes(userId) || allowlist("AIA_ADMIN_IDS").includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "canon_reviewer" || user?.role === "admin";
}

function boundedTake(value: string | null): number {
  if (!value) return 12;
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return 12;
  return Math.min(50, Math.max(1, Math.trunc(parsed)));
}

const CONSISTENCY_STATUSES = new Set([
  "unchecked",
  "consistent",
  "soft_tension",
  "hard_contradiction",
  "canon_conflict",
]);

function sourceLabel(branch: {
  id: string;
  sourceNodeId: string;
  sourceNode?: {
    title?: string | null;
    slug?: string | null;
    path?: string | null;
  } | null;
}): string {
  return branch.sourceNode?.title || branch.sourceNode?.slug || branch.sourceNode?.path || branch.sourceNodeId || branch.id;
}

function sourceHref(slug: string | null | undefined, nodeId: string): string | null {
  return slug ? `/book/${encodeURIComponent(slug)}#node-${encodeURIComponent(nodeId)}` : null;
}

function queueSearchPredicates(query: string): Prisma.AIPBranchWhereInput[] {
  return [
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
  ];
}

async function userEmailsById(ids: string[]): Promise<Map<string, string>> {
  const uniqueIds = Array.from(new Set(ids.filter(Boolean)));
  if (uniqueIds.length === 0) return new Map();

  const users = await prisma.user.findMany({
    where: { id: { in: uniqueIds } },
    select: { id: true, email: true },
  });

  return new Map(users.map((user) => [user.id, user.email]));
}

export async function GET(req: Request) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  if (!(await canReadReviewQueue(userId))) {
    return NextResponse.json({ error: "canon_reviewer_required" }, { status: 403 });
  }

  const params = new URL(req.url).searchParams;
  const take = boundedTake(params.get("take"));
  const cursor = params.get("cursor")?.trim();
  const searchQuery = params.get("q")?.trim();
  const consistencyStatus = params.get("consistency")?.trim();
  if (consistencyStatus && !CONSISTENCY_STATUSES.has(consistencyStatus)) {
    return NextResponse.json({ error: "invalid_consistency_status" }, { status: 400 });
  }

  const where: Prisma.AIPBranchWhereInput = { visibility: "proposed_canon" };
  if (searchQuery) {
    where.OR = queueSearchPredicates(searchQuery);
  }
  if (consistencyStatus) {
    where.consistencyStatus = consistencyStatus;
  }

  const query = {
    where,
    orderBy: { createdAt: "desc" },
    take,
    ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
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
  } satisfies Prisma.AIPBranchFindManyArgs;

  const branches = await prisma.aIPBranch.findMany(query);
  const nextCursor = branches.length === take ? branches[branches.length - 1]?.id : undefined;
  const userEmails = await userEmailsById(branches.map((branch) => branch.userId));

  return NextResponse.json({
    branches: branches.map((branch) => {
      const currentVersionHash = branch.sourceNode.currentVersion?.hash ?? null;
      return {
        id: branch.id,
        authorId: branch.userId,
        authorEmail: userEmails.get(branch.userId) ?? null,
        sourceNodeId: branch.sourceNodeId,
        sourceLabel: sourceLabel(branch),
        sourceSlug: branch.sourceNode.slug,
        sourceHref: sourceHref(branch.sourceNode.slug, branch.sourceNodeId),
        sourceVersionHash: branch.sourceVersionHash,
        consistencyStatus: branch.consistencyStatus,
        consistencyReportSource: branch.consistencyReportSource,
        consistencySummary: branch.consistencySummary,
        currentVersionHash,
        isStaleSource: Boolean(currentVersionHash && currentVersionHash !== branch.sourceVersionHash),
        outputPreview: branch.outputMd,
        createdAt: branch.createdAt.toISOString(),
      };
    }),
    nextCursor,
  });
}

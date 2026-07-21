import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import type { BranchConsistencyReport } from "@/lib/aia/consistency";
import { prisma } from "@/lib/prisma";

function parseNodeIds(url: string): string[] {
  const ids = new URL(url).searchParams.get("nodeIds");
  if (!ids) return [];

  return Array.from(
    new Set(
      ids
        .split(",")
        .map((id) => id.trim())
        .filter(Boolean)
    )
  );
}

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

function parseConsistencyReport(value: string | null): BranchConsistencyReport | undefined {
  if (!value) return undefined;
  try {
    const parsed = JSON.parse(value);
    if (!parsed || typeof parsed !== "object") return undefined;
    return parsed as BranchConsistencyReport;
  } catch {
    return undefined;
  }
}

function reviewStatusFromDecision(decision: string | undefined) {
  if (decision === "reject") return "rejected";
  if (decision === "revise") return "revision_requested";
  return undefined;
}

export async function GET(req: Request) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const nodeIds = parseNodeIds(req.url);
  if (nodeIds.length === 0) {
    return NextResponse.json({ branches: [] });
  }

  const branches = await prisma.aIPBranch.findMany({
    where: {
      userId,
      sourceNodeId: { in: nodeIds },
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

  return NextResponse.json({
    branches: branches.map((branch) => {
      const review = branch.reviews[0];
      return {
        localId: `server:${branch.id}`,
        serverId: branch.id,
        sourceNodeId: branch.sourceNodeId,
        sourceVersionHash: branch.sourceVersionHash,
        status: "complete",
        outputMd: branch.outputMd,
        depth: branch.depth,
        branchMode: branch.branchMode,
        mode: branch.mode,
        visibility: branch.visibility,
        consistencyStatus: branch.consistencyStatus,
        reviewStatus: reviewStatusFromDecision(review?.decision),
        reviewFeedback: review?.notes ?? undefined,
        consistencyReport: parseConsistencyReport(branch.consistencyReportJson),
        contradictions: branch.contradictions.map((contradiction) => ({
          id: contradiction.id,
          type: contradiction.type,
          severity: contradiction.severity,
          explanation: contradiction.explanation,
          resolutionStatus: contradiction.resolutionStatus,
        })),
      };
    }),
  });
}

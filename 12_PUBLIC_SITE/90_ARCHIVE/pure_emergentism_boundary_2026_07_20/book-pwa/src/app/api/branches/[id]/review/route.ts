import { createHash } from "node:crypto";
import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

type ReviewDecision = "accept" | "reject" | "revise";

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

function isReviewDecision(value: unknown): value is ReviewDecision {
  return value === "accept" || value === "reject" || value === "revise";
}

function canonReviewerIds(): string[] {
  return (process.env.AIA_CANON_REVIEWER_IDS ?? "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

async function canReviewCanon(userId: string): Promise<boolean> {
  const reviewerIds = canonReviewerIds();
  if (reviewerIds.includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "canon_reviewer" || user?.role === "admin";
}

function canonVersionHash(path: string, contentMd: string, branchId: string): string {
  return createHash("sha256")
    .update(`${path}\n${contentMd}\naccepted:${branchId}`)
    .digest("hex");
}

export async function POST(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const body = await req.json();
  if (!isReviewDecision(body.decision)) {
    return NextResponse.json({ error: "Invalid review decision" }, { status: 400 });
  }
  const requestedNotes = typeof body.notes === "string" ? body.notes : undefined;

  if (!(await canReviewCanon(userId))) {
    return NextResponse.json({ error: "canon_reviewer_required" }, { status: 403 });
  }

  const { id } = await params;
  const branch = await prisma.aIPBranch.findFirst({
    where: {
      id,
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

  if (!branch) {
    return NextResponse.json({ error: "Branch not found" }, { status: 404 });
  }

  const notes = body.decision === "revise"
    ? requestedNotes ?? branch.consistencySummary ?? undefined
    : requestedNotes;

  if (body.decision === "accept") {
    if (branch.consistencyStatus === "canon_conflict") {
      return NextResponse.json({ error: "canon_conflict" }, { status: 409 });
    }

    if (!branch.sourceNode.currentVersion || branch.sourceVersionHash !== branch.sourceNode.currentVersion.hash) {
      return NextResponse.json({ error: "stale_source_version" }, { status: 409 });
    }

    let accepted: { currentVersionId: string };
    try {
      accepted = await prisma.$transaction(async (tx) => {
        await tx.graphWriteLock.upsert({
          where: { scope: "canon" },
          create: { scope: "canon" },
          update: {},
        });

        const nextVersion = await tx.nodeVersion.create({
          data: {
            hash: canonVersionHash(branch.sourceNode.path, branch.outputMd, branch.id),
            nodeId: branch.sourceNodeId,
            contentMd: branch.outputMd,
            prevVersionId: branch.sourceNode.currentVersion!.id,
            authorId: userId,
          },
        });

        const nodeUpdate = await tx.node.updateMany({
          where: {
            id: branch.sourceNodeId,
            currentVersionId: branch.sourceNode.currentVersion!.id,
          },
          data: {
            currentVersionId: nextVersion.id,
          },
        });

        if (nodeUpdate.count === 0) {
          throw new Error("stale_source_version");
        }

        await tx.canonReview.create({
          data: {
            branchId: branch.id,
            reviewerId: userId,
            decision: body.decision,
            notes,
          },
        });

        await tx.aIPBranch.update({
          where: { id: branch.id },
          data: { visibility: "accepted_canon" },
        });

        return {
          currentVersionId: nextVersion.id,
        };
      });
    } catch (error) {
      if (error instanceof Error && error.message === "stale_source_version") {
        return NextResponse.json({ error: "stale_source_version" }, { status: 409 });
      }
      throw error;
    }

    return NextResponse.json({
      branch: {
        id: branch.id,
        visibility: "accepted_canon",
      },
      review: {
        decision: body.decision,
      },
      canon: {
        nodeId: branch.sourceNodeId,
        currentVersionId: accepted.currentVersionId,
      },
    });
  }

  await prisma.$transaction(async (tx) => {
    await tx.canonReview.create({
      data: {
        branchId: branch.id,
        reviewerId: userId,
        decision: body.decision,
        notes,
      },
    });

    await tx.aIPBranch.update({
      where: { id: branch.id },
      data: { visibility: "private" },
    });
  });

  return NextResponse.json({
    branch: {
      id: branch.id,
      visibility: "private",
    },
    review: {
      decision: body.decision,
      notes,
    },
  });
}

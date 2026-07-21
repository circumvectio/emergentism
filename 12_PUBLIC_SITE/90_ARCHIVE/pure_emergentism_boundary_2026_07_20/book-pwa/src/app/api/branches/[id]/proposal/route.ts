import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

export async function POST(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const { id } = await params;
  const branch = await prisma.aIPBranch.findFirst({
    where: {
      id,
      userId,
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

  if (branch.consistencyStatus === "canon_conflict") {
    return NextResponse.json({ error: "canon_conflict" }, { status: 409 });
  }

  if (branch.consistencyStatus === "unchecked") {
    return NextResponse.json({ error: "consistency_unchecked" }, { status: 409 });
  }

  if (!branch.sourceNode.currentVersion || branch.sourceVersionHash !== branch.sourceNode.currentVersion.hash) {
    return NextResponse.json({ error: "stale_source_version" }, { status: 409 });
  }

  const result = await prisma.aIPBranch.updateMany({
    where: {
      id,
      userId,
      sourceVersionHash: branch.sourceNode.currentVersion.hash,
    },
    data: {
      visibility: "proposed_canon",
    },
  });

  if (result.count === 0) {
    return NextResponse.json({ error: "Branch not found" }, { status: 404 });
  }

  return NextResponse.json({
    branch: {
      id,
      visibility: "proposed_canon",
    },
  });
}

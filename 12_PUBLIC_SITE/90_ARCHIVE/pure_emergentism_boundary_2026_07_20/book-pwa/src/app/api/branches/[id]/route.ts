import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

const STALE_CONSISTENCY_SUMMARY = "Branch output changed after its last consistency review.";

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const { id } = await params;
  const { outputMd } = await req.json();
  if (typeof outputMd !== "string" || outputMd.trim().length === 0) {
    return NextResponse.json({ error: "Branch output is required" }, { status: 400 });
  }

  const result = await prisma.aIPBranch.updateMany({
    where: {
      id,
      userId,
      visibility: "private",
    },
    data: {
      outputMd,
      visibility: "private",
      consistencyStatus: "unchecked",
      consistencyReportSource: null,
      consistencySummary: STALE_CONSISTENCY_SUMMARY,
      consistencyReportJson: null,
    },
  });

  if (result.count === 0) {
    return NextResponse.json({ error: "Branch not found" }, { status: 404 });
  }

  return NextResponse.json({
    branch: {
      id,
      outputMd,
      visibility: "private",
      consistencyStatus: "unchecked",
      consistencySummary: STALE_CONSISTENCY_SUMMARY,
    },
  });
}

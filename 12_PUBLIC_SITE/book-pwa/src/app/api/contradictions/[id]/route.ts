import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

const allowedResolutionStatuses = new Set([
  "accepted_as_antithesis",
  "forked",
  "revised",
  "synthesized",
  "dismissed",
]);

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
  const { resolutionStatus } = await req.json();
  if (typeof resolutionStatus !== "string" || !allowedResolutionStatuses.has(resolutionStatus)) {
    return NextResponse.json({ error: "Unsupported resolution status" }, { status: 400 });
  }

  const result = await prisma.aIAContradiction.updateMany({
    where: {
      id,
      userId,
    },
    data: {
      resolutionStatus,
    },
  });

  if (result.count === 0) {
    return NextResponse.json({ error: "Contradiction not found" }, { status: 404 });
  }

  return NextResponse.json({
    contradiction: {
      id,
      resolutionStatus,
    },
  });
}

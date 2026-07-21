import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

type UserRole = "reader" | "canon_reviewer" | "admin";

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

function idsFromEnv(name: string): string[] {
  return (process.env[name] ?? "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

function normaliseRole(role: string | null | undefined): UserRole {
  return role === "canon_reviewer" || role === "admin" ? role : "reader";
}

export async function GET() {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });
  const role = normaliseRole(user?.role);
  const bootstrapReviewer = idsFromEnv("AIA_CANON_REVIEWER_IDS").includes(userId);
  const bootstrapAdmin = idsFromEnv("AIA_ADMIN_IDS").includes(userId);
  const canAssignRoles = role === "admin" || bootstrapAdmin;
  const canReviewCanon = role === "canon_reviewer" || canAssignRoles || bootstrapReviewer;

  return NextResponse.json({
    user: {
      id: userId,
      role,
      canReviewCanon,
      canAssignRoles,
    },
  });
}

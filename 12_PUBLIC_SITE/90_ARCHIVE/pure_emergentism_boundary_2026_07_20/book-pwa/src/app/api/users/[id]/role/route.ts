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

function adminIds(): string[] {
  return (process.env.AIA_ADMIN_IDS ?? "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

function isUserRole(value: unknown): value is UserRole {
  return value === "reader" || value === "canon_reviewer" || value === "admin";
}

async function canAssignRoles(userId: string): Promise<boolean> {
  if (adminIds().includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "admin";
}

export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const body = await req.json();
  if (!isUserRole(body.role)) {
    return NextResponse.json({ error: "Invalid role" }, { status: 400 });
  }

  if (!(await canAssignRoles(userId))) {
    return NextResponse.json({ error: "admin_required" }, { status: 403 });
  }

  const { id } = await params;
  const targetUser = await prisma.user.findUnique({
    where: { id },
    select: { role: true },
  });

  if (!targetUser) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  const result = await prisma.$transaction(async (tx) => {
    const update = await tx.user.updateMany({
      where: { id },
      data: { role: body.role },
    });

    if (update.count === 0) {
      return update;
    }

    await tx.roleAssignmentAudit.create({
      data: {
        targetUserId: id,
        actorUserId: userId,
        fromRole: targetUser.role,
        toRole: body.role,
      },
    });

    return update;
  });

  if (result.count === 0) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  return NextResponse.json({
    user: {
      id,
      role: body.role,
    },
    audit: {
      recorded: true,
    },
  });
}

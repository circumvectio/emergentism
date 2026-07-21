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

function adminIds(): string[] {
  return (process.env.AIA_ADMIN_IDS ?? "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

async function canReadRoleAudits(userId: string): Promise<boolean> {
  if (adminIds().includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "admin";
}

function boundedTake(value: string | null): number {
  if (!value) return 12;
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return 12;
  return Math.min(50, Math.max(1, Math.trunc(parsed)));
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

  if (!(await canReadRoleAudits(userId))) {
    return NextResponse.json({ error: "admin_required" }, { status: 403 });
  }

  const params = req ? new URL(req.url).searchParams : new URLSearchParams();
  const targetUserId = params.get("targetUserId")?.trim();
  const actorUserId = params.get("actorUserId")?.trim();
  const where: Record<string, string> = {};
  if (targetUserId) where.targetUserId = targetUserId;
  if (actorUserId) where.actorUserId = actorUserId;

  const take = boundedTake(params.get("take"));
  const cursor = params.get("cursor")?.trim();
  const query: {
    where?: Record<string, string>;
    orderBy: { createdAt: "desc" };
    take: number;
    cursor?: { id: string };
    skip?: number;
  } = {
    orderBy: { createdAt: "desc" },
    take,
  };
  if (Object.keys(where).length > 0) query.where = where;
  if (cursor) {
    query.cursor = { id: cursor };
    query.skip = 1;
  }

  const audits = await prisma.roleAssignmentAudit.findMany(query);
  const nextCursor = audits.length === take ? audits[audits.length - 1]?.id : undefined;
  const userEmails = await userEmailsById(
    audits.flatMap((audit) => [audit.targetUserId, audit.actorUserId])
  );

  return NextResponse.json({
    audits: audits.map((audit) => ({
      id: audit.id,
      targetUserId: audit.targetUserId,
      targetUserEmail: userEmails.get(audit.targetUserId) ?? null,
      actorUserId: audit.actorUserId,
      actorUserEmail: userEmails.get(audit.actorUserId) ?? null,
      fromRole: audit.fromRole,
      toRole: audit.toRole,
      createdAt: audit.createdAt.toISOString(),
    })),
    nextCursor,
  });
}

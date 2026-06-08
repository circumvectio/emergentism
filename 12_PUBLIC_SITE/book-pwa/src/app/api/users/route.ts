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

async function canSearchUsers(userId: string): Promise<boolean> {
  if (adminIds().includes(userId)) {
    return true;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  return user?.role === "admin";
}

export async function GET(req: Request) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  if (!(await canSearchUsers(userId))) {
    return NextResponse.json({ error: "admin_required" }, { status: 403 });
  }

  const query = new URL(req.url).searchParams.get("query")?.trim() ?? "";
  if (!query) {
    return NextResponse.json({ users: [] });
  }

  const users = await prisma.user.findMany({
    where: {
      OR: [
        { id: { contains: query } },
        { email: { contains: query } },
      ],
    },
    select: {
      id: true,
      email: true,
      role: true,
    },
    orderBy: { email: "asc" },
    take: 8,
  });

  return NextResponse.json({ users });
}

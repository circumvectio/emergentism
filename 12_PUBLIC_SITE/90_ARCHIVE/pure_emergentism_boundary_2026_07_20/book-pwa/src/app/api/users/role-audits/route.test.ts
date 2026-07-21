import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  userFindMany: vi.fn(),
  roleAssignmentAuditFindMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    user: {
      findUnique: mocks.userFindUnique,
      findMany: mocks.userFindMany,
    },
    roleAssignmentAudit: {
      findMany: mocks.roleAssignmentAuditFindMany,
    },
  },
}));

describe("GET /api/users/role-audits", () => {
  const originalAdminIds = process.env.AIA_ADMIN_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_ADMIN_IDS = "admin-1";
    mocks.auth.mockResolvedValue({ userId: "admin-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
    mocks.userFindMany.mockResolvedValue([
      { id: "user-2", email: "target@example.com" },
      { id: "admin-1", email: "admin@example.com" },
      { id: "admin-2", email: "second-admin@example.com" },
    ]);
    mocks.roleAssignmentAuditFindMany.mockResolvedValue([
      {
        id: "audit-1",
        targetUserId: "user-2",
        actorUserId: "admin-1",
        fromRole: "reader",
        toRole: "canon_reviewer",
        createdAt: new Date("2026-05-31T00:00:00.000Z"),
      },
    ]);
  });

  afterEach(() => {
    process.env.AIA_ADMIN_IDS = originalAdminIds;
  });

  it("returns latest role assignment audits for admins", async () => {
    const response = await GET(new Request("http://localhost/api/users/role-audits"));

    expect(response.status).toBe(200);
    expect(mocks.roleAssignmentAuditFindMany).toHaveBeenCalledWith({
      orderBy: { createdAt: "desc" },
      take: 12,
    });
    expect(mocks.userFindMany).toHaveBeenCalledWith({
      where: { id: { in: ["user-2", "admin-1"] } },
      select: { id: true, email: true },
    });
    await expect(response.json()).resolves.toEqual({
      audits: [
        {
          id: "audit-1",
          targetUserId: "user-2",
          targetUserEmail: "target@example.com",
          actorUserId: "admin-1",
          actorUserEmail: "admin@example.com",
          fromRole: "reader",
          toRole: "canon_reviewer",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });
  });

  it("filters and paginates role assignment audit history", async () => {
    mocks.roleAssignmentAuditFindMany.mockResolvedValueOnce([
      {
        id: "audit-2",
        targetUserId: "user-2",
        actorUserId: "admin-2",
        fromRole: "canon_reviewer",
        toRole: "reader",
        createdAt: new Date("2026-05-31T00:01:00.000Z"),
      },
      {
        id: "audit-3",
        targetUserId: "user-2",
        actorUserId: "admin-2",
        fromRole: "reader",
        toRole: "canon_reviewer",
        createdAt: new Date("2026-05-31T00:00:00.000Z"),
      },
    ]);

    const response = await GET(
      new Request(
        "http://localhost/api/users/role-audits?targetUserId=user-2&actorUserId=admin-2&take=2&cursor=audit-1"
      )
    );

    expect(response.status).toBe(200);
    expect(mocks.roleAssignmentAuditFindMany).toHaveBeenCalledWith({
      where: {
        targetUserId: "user-2",
        actorUserId: "admin-2",
      },
      orderBy: { createdAt: "desc" },
      take: 2,
      cursor: { id: "audit-1" },
      skip: 1,
    });
    await expect(response.json()).resolves.toEqual({
      audits: [
        {
          id: "audit-2",
          targetUserId: "user-2",
          targetUserEmail: "target@example.com",
          actorUserId: "admin-2",
          actorUserEmail: "second-admin@example.com",
          fromRole: "canon_reviewer",
          toRole: "reader",
          createdAt: "2026-05-31T00:01:00.000Z",
        },
        {
          id: "audit-3",
          targetUserId: "user-2",
          targetUserEmail: "target@example.com",
          actorUserId: "admin-2",
          actorUserEmail: "second-admin@example.com",
          fromRole: "reader",
          toRole: "canon_reviewer",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
      nextCursor: "audit-3",
    });
  });

  it("forbids non-admin users before reading audit history", async () => {
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "reader" });

    const response = await GET(new Request("http://localhost/api/users/role-audits"));

    expect(response.status).toBe(403);
    expect(mocks.roleAssignmentAuditFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "admin_required" });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET(new Request("http://localhost/api/users/role-audits"));

    expect(response.status).toBe(401);
    expect(mocks.roleAssignmentAuditFindMany).not.toHaveBeenCalled();
  });
});

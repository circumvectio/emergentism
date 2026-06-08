import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { PATCH } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  userUpdateMany: vi.fn(),
  transaction: vi.fn(),
  roleAssignmentAuditCreate: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    user: {
      findUnique: mocks.userFindUnique,
    },
    $transaction: mocks.transaction,
  },
}));

describe("PATCH /api/users/[id]/role", () => {
  const originalAdminIds = process.env.AIA_ADMIN_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_ADMIN_IDS = "admin-1";
    mocks.auth.mockResolvedValue({ userId: "admin-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
    mocks.userUpdateMany.mockResolvedValue({ count: 1 });
    mocks.roleAssignmentAuditCreate.mockResolvedValue({ id: "audit-1" });
    mocks.transaction.mockImplementation(async (callback) =>
      callback({
        user: {
          updateMany: mocks.userUpdateMany,
        },
        roleAssignmentAudit: {
          create: mocks.roleAssignmentAuditCreate,
        },
      })
    );
  });

  afterEach(() => {
    process.env.AIA_ADMIN_IDS = originalAdminIds;
  });

  it("allows a bootstrap admin to assign canon reviewer role", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "canon_reviewer" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.userUpdateMany).toHaveBeenCalledWith({
      where: { id: "user-2" },
      data: { role: "canon_reviewer" },
    });
    expect(mocks.roleAssignmentAuditCreate).toHaveBeenCalledWith({
      data: {
        targetUserId: "user-2",
        actorUserId: "admin-1",
        fromRole: "reader",
        toRole: "canon_reviewer",
      },
    });
    await expect(response.json()).resolves.toEqual({
      user: {
        id: "user-2",
        role: "canon_reviewer",
      },
      audit: {
        recorded: true,
      },
    });
  });

  it("allows first-class admin users to assign reviewer roles", async () => {
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "admin-2" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "admin" });

    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "canon_reviewer" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.userFindUnique).toHaveBeenCalledWith({
      where: { id: "admin-2" },
      select: { role: true },
    });
    expect(mocks.userUpdateMany).toHaveBeenCalled();
  });

  it("forbids non-admin users before updating a role", async () => {
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "reader" });

    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "canon_reviewer" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(403);
    expect(mocks.userUpdateMany).not.toHaveBeenCalled();
    expect(mocks.roleAssignmentAuditCreate).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "admin_required" });
  });

  it("rejects unknown roles", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "owner" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(400);
    expect(mocks.userUpdateMany).not.toHaveBeenCalled();
    expect(mocks.roleAssignmentAuditCreate).not.toHaveBeenCalled();
  });

  it("returns not found when the target user does not exist", async () => {
    mocks.userUpdateMany.mockResolvedValueOnce({ count: 0 });

    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "canon_reviewer" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(404);
    expect(mocks.roleAssignmentAuditCreate).not.toHaveBeenCalled();
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await PATCH(
      new Request("http://localhost/api/users/user-2/role", {
        method: "PATCH",
        body: JSON.stringify({ role: "canon_reviewer" }),
      }),
      { params: Promise.resolve({ id: "user-2" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.userUpdateMany).not.toHaveBeenCalled();
    expect(mocks.roleAssignmentAuditCreate).not.toHaveBeenCalled();
  });
});

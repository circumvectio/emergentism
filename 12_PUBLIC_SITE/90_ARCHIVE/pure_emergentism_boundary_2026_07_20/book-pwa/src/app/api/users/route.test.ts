import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
  userFindMany: vi.fn(),
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
  },
}));

describe("GET /api/users", () => {
  const originalAdminIds = process.env.AIA_ADMIN_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_ADMIN_IDS = "admin-1";
    mocks.auth.mockResolvedValue({ userId: "admin-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
    mocks.userFindMany.mockResolvedValue([
      {
        id: "user-2",
        email: "reader@example.com",
        role: "reader",
      },
      {
        id: "reviewer-1",
        email: "reviewer@example.com",
        role: "canon_reviewer",
      },
    ]);
  });

  afterEach(() => {
    process.env.AIA_ADMIN_IDS = originalAdminIds;
  });

  it("lets bootstrap admins search users by id or email", async () => {
    const response = await GET(new Request("http://localhost/api/users?query=review"));

    expect(response.status).toBe(200);
    expect(mocks.userFindMany).toHaveBeenCalledWith({
      where: {
        OR: [
          { id: { contains: "review" } },
          { email: { contains: "review" } },
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
    await expect(response.json()).resolves.toEqual({
      users: [
        {
          id: "user-2",
          email: "reader@example.com",
          role: "reader",
        },
        {
          id: "reviewer-1",
          email: "reviewer@example.com",
          role: "canon_reviewer",
        },
      ],
    });
  });

  it("lets first-class admins search users without bootstrap allowlist", async () => {
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "admin-2" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "admin" });

    const response = await GET(new Request("http://localhost/api/users?query=reader"));

    expect(response.status).toBe(200);
    expect(mocks.userFindUnique).toHaveBeenCalledWith({
      where: { id: "admin-2" },
      select: { role: true },
    });
    expect(mocks.userFindMany).toHaveBeenCalled();
  });

  it("requires a non-empty query before searching", async () => {
    const response = await GET(new Request("http://localhost/api/users?query= "));

    expect(response.status).toBe(200);
    expect(mocks.userFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ users: [] });
  });

  it("forbids non-admin users before searching", async () => {
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValueOnce({ userId: "reader-1" });
    mocks.userFindUnique.mockResolvedValueOnce({ role: "reader" });

    const response = await GET(new Request("http://localhost/api/users?query=reader"));

    expect(response.status).toBe(403);
    expect(mocks.userFindMany).not.toHaveBeenCalled();
    await expect(response.json()).resolves.toEqual({ error: "admin_required" });
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET(new Request("http://localhost/api/users?query=reader"));

    expect(response.status).toBe(401);
    expect(mocks.userFindMany).not.toHaveBeenCalled();
  });
});

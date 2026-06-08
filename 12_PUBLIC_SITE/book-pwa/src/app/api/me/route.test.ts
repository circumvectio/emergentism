import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  userFindUnique: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    user: {
      findUnique: mocks.userFindUnique,
    },
  },
}));

describe("GET /api/me", () => {
  const originalReviewerIds = process.env.AIA_CANON_REVIEWER_IDS;
  const originalAdminIds = process.env.AIA_ADMIN_IDS;

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.AIA_CANON_REVIEWER_IDS = "";
    process.env.AIA_ADMIN_IDS = "";
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.userFindUnique.mockResolvedValue({ role: "reader" });
  });

  afterEach(() => {
    process.env.AIA_CANON_REVIEWER_IDS = originalReviewerIds;
    process.env.AIA_ADMIN_IDS = originalAdminIds;
  });

  it("returns reader permissions for ordinary users", async () => {
    const response = await GET();

    expect(response.status).toBe(200);
    expect(mocks.userFindUnique).toHaveBeenCalledWith({
      where: { id: "user-1" },
      select: { role: true },
    });
    await expect(response.json()).resolves.toEqual({
      user: {
        id: "user-1",
        role: "reader",
        canReviewCanon: false,
        canAssignRoles: false,
      },
    });
  });

  it("allows canon reviewers to review canon but not assign roles", async () => {
    mocks.userFindUnique.mockResolvedValueOnce({ role: "canon_reviewer" });

    const response = await GET();

    await expect(response.json()).resolves.toEqual({
      user: {
        id: "user-1",
        role: "canon_reviewer",
        canReviewCanon: true,
        canAssignRoles: false,
      },
    });
  });

  it("allows admins to review canon and assign roles", async () => {
    mocks.userFindUnique.mockResolvedValueOnce({ role: "admin" });

    const response = await GET();

    await expect(response.json()).resolves.toEqual({
      user: {
        id: "user-1",
        role: "admin",
        canReviewCanon: true,
        canAssignRoles: true,
      },
    });
  });

  it("honors bootstrap reviewer and admin allowlists", async () => {
    process.env.AIA_CANON_REVIEWER_IDS = "user-1";
    process.env.AIA_ADMIN_IDS = "user-1";

    const response = await GET();

    await expect(response.json()).resolves.toEqual({
      user: {
        id: "user-1",
        role: "reader",
        canReviewCanon: true,
        canAssignRoles: true,
      },
    });
  });

  it("returns unauthorized when no user is signed in", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await GET();

    expect(response.status).toBe(401);
    expect(mocks.userFindUnique).not.toHaveBeenCalled();
  });
});

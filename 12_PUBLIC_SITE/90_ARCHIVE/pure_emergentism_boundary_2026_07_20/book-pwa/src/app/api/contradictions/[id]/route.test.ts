import { beforeEach, describe, expect, it, vi } from "vitest";
import { PATCH } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  contradictionUpdateMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIAContradiction: {
      updateMany: mocks.contradictionUpdateMany,
    },
  },
}));

describe("PATCH /api/contradictions/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.contradictionUpdateMany.mockResolvedValue({ count: 1 });
  });

  it("updates an owned contradiction resolution status", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/contradictions/contradiction-1", {
        method: "PATCH",
        body: JSON.stringify({ resolutionStatus: "dismissed" }),
      }),
      { params: Promise.resolve({ id: "contradiction-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.contradictionUpdateMany).toHaveBeenCalledWith({
      where: {
        id: "contradiction-1",
        userId: "user-1",
      },
      data: {
        resolutionStatus: "dismissed",
      },
    });
    await expect(response.json()).resolves.toEqual({
      contradiction: {
        id: "contradiction-1",
        resolutionStatus: "dismissed",
      },
    });
  });

  it("rejects unsupported resolution statuses", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/contradictions/contradiction-1", {
        method: "PATCH",
        body: JSON.stringify({ resolutionStatus: "erase_history" }),
      }),
      { params: Promise.resolve({ id: "contradiction-1" }) }
    );

    expect(response.status).toBe(400);
    expect(mocks.contradictionUpdateMany).not.toHaveBeenCalled();
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await PATCH(
      new Request("http://localhost/api/contradictions/contradiction-1", {
        method: "PATCH",
        body: JSON.stringify({ resolutionStatus: "dismissed" }),
      }),
      { params: Promise.resolve({ id: "contradiction-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.contradictionUpdateMany).not.toHaveBeenCalled();
  });

  it("returns unauthorized when Clerk auth cannot run locally", async () => {
    mocks.auth.mockRejectedValueOnce(new Error("missing middleware"));

    const response = await PATCH(
      new Request("http://localhost/api/contradictions/contradiction-1", {
        method: "PATCH",
        body: JSON.stringify({ resolutionStatus: "dismissed" }),
      }),
      { params: Promise.resolve({ id: "contradiction-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.contradictionUpdateMany).not.toHaveBeenCalled();
  });
});

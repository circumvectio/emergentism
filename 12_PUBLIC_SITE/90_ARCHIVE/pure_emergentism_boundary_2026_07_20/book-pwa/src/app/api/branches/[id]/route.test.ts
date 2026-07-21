import { beforeEach, describe, expect, it, vi } from "vitest";
import { PATCH } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  branchUpdateMany: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      updateMany: mocks.branchUpdateMany,
    },
  },
}));

describe("PATCH /api/branches/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.branchUpdateMany.mockResolvedValue({ count: 1 });
  });

  it("updates only an owned private branch output", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/branches/branch-1", {
        method: "PATCH",
        body: JSON.stringify({ outputMd: "Edited branch output." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(200);
    expect(mocks.branchUpdateMany).toHaveBeenCalledWith({
      where: {
        id: "branch-1",
        userId: "user-1",
        visibility: "private",
      },
      data: {
        outputMd: "Edited branch output.",
        visibility: "private",
        consistencyStatus: "unchecked",
        consistencyReportSource: null,
        consistencySummary: "Branch output changed after its last consistency review.",
        consistencyReportJson: null,
      },
    });
    await expect(response.json()).resolves.toEqual({
      branch: {
        id: "branch-1",
        outputMd: "Edited branch output.",
        visibility: "private",
        consistencyStatus: "unchecked",
        consistencySummary: "Branch output changed after its last consistency review.",
      },
    });
  });

  it("returns not found when no owned private branch is editable", async () => {
    mocks.branchUpdateMany.mockResolvedValueOnce({ count: 0 });

    const response = await PATCH(
      new Request("http://localhost/api/branches/branch-1", {
        method: "PATCH",
        body: JSON.stringify({ outputMd: "Edited branch output." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(404);
    expect(mocks.branchUpdateMany).toHaveBeenCalledWith({
      where: {
        id: "branch-1",
        userId: "user-1",
        visibility: "private",
      },
      data: {
        outputMd: "Edited branch output.",
        visibility: "private",
        consistencyStatus: "unchecked",
        consistencyReportSource: null,
        consistencySummary: "Branch output changed after its last consistency review.",
        consistencyReportJson: null,
      },
    });
    await expect(response.json()).resolves.toEqual({ error: "Branch not found" });
  });

  it("rejects empty branch output", async () => {
    const response = await PATCH(
      new Request("http://localhost/api/branches/branch-1", {
        method: "PATCH",
        body: JSON.stringify({ outputMd: "   " }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(400);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });

  it("requires authentication", async () => {
    mocks.auth.mockResolvedValueOnce({ userId: null });

    const response = await PATCH(
      new Request("http://localhost/api/branches/branch-1", {
        method: "PATCH",
        body: JSON.stringify({ outputMd: "Edited branch output." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });

  it("returns unauthorized when Clerk auth cannot run locally", async () => {
    mocks.auth.mockRejectedValueOnce(new Error("missing middleware"));

    const response = await PATCH(
      new Request("http://localhost/api/branches/branch-1", {
        method: "PATCH",
        body: JSON.stringify({ outputMd: "Edited branch output." }),
      }),
      { params: Promise.resolve({ id: "branch-1" }) }
    );

    expect(response.status).toBe(401);
    expect(mocks.branchUpdateMany).not.toHaveBeenCalled();
  });
});

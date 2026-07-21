import { beforeEach, describe, expect, it, vi } from "vitest";
import { createMirrorLink, validateAcyclicMirror } from "./graph";
import { prisma } from "./prisma";

vi.mock("./prisma", () => {
  const tx = {
    graphWriteLock: { upsert: vi.fn() },
    node: { findUnique: vi.fn() },
    nodeLink: { create: vi.fn() },
    $queryRaw: vi.fn(),
  };

  return {
    prisma: {
      $queryRaw: vi.fn(),
      $transaction: vi.fn((callback) => callback(tx)),
      __tx: tx,
    },
  };
});

const mockedPrisma = prisma as unknown as {
  $queryRaw: ReturnType<typeof vi.fn>;
  $transaction: ReturnType<typeof vi.fn>;
  __tx: {
    graphWriteLock: { upsert: ReturnType<typeof vi.fn> };
    node: { findUnique: ReturnType<typeof vi.fn> };
    nodeLink: { create: ReturnType<typeof vi.fn> };
    $queryRaw: ReturnType<typeof vi.fn>;
  };
};

describe("validateAcyclicMirror", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("rejects a self-loop before querying", async () => {
    await expect(validateAcyclicMirror("A", "A")).rejects.toThrow(/source equals target/i);
    expect(mockedPrisma.$queryRaw).not.toHaveBeenCalled();
  });

  it("rejects a reverse path that would close a mirror cycle", async () => {
    mockedPrisma.$queryRaw.mockResolvedValueOnce([{ id: "A" }]);
    await expect(validateAcyclicMirror("A", "C")).rejects.toThrow(/target can already reach source/i);
  });

  it("allows an edge when target cannot reach source", async () => {
    mockedPrisma.$queryRaw.mockResolvedValueOnce([]);
    await expect(validateAcyclicMirror("A", "C")).resolves.toBe(true);
  });
});

describe("createMirrorLink", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedPrisma.__tx.graphWriteLock.upsert.mockResolvedValue({ scope: "mirror" });
    mockedPrisma.__tx.$queryRaw.mockResolvedValue([]);
    mockedPrisma.__tx.node.findUnique
      .mockResolvedValueOnce({ id: "A", currentVersion: { id: "A-v1" } })
      .mockResolvedValueOnce({ id: "B", currentVersion: { id: "B-v1" } });
    mockedPrisma.__tx.nodeLink.create.mockResolvedValue({
      id: "link-1",
      sourceNodeId: "A",
      sourceVersionId: "A-v1",
      targetNodeId: "B",
      targetVersionId: "B-v1",
      relationType: "mirror",
      status: "synced",
    });
  });

  it("locks the mirror graph before validating and creating a link", async () => {
    await createMirrorLink({ sourceNodeId: "A", targetNodeId: "B" });

    expect(mockedPrisma.__tx.graphWriteLock.upsert).toHaveBeenCalledWith({
      where: { scope: "mirror" },
      create: { scope: "mirror" },
      update: {},
    });
    expect(mockedPrisma.__tx.$queryRaw).toHaveBeenCalledTimes(1);
    expect(mockedPrisma.__tx.nodeLink.create).toHaveBeenCalledWith({
      data: {
        sourceNodeId: "A",
        sourceVersionId: "A-v1",
        targetNodeId: "B",
        targetVersionId: "B-v1",
        relationType: "mirror",
        status: "synced",
      },
    });
  });

  it("does not create a link when the transaction validator finds a cycle", async () => {
    mockedPrisma.__tx.$queryRaw.mockResolvedValueOnce([{ id: "A" }]);

    await expect(createMirrorLink({ sourceNodeId: "A", targetNodeId: "B" })).rejects.toThrow(
      /target can already reach source/i
    );
    expect(mockedPrisma.__tx.nodeLink.create).not.toHaveBeenCalled();
  });

  it("uses explicit version pins when supplied by the caller", async () => {
    await createMirrorLink({
      sourceNodeId: "A",
      sourceVersionId: "A-v0",
      targetNodeId: "B",
      targetVersionId: "B-v0",
    });

    expect(mockedPrisma.__tx.nodeLink.create).toHaveBeenCalledWith({
      data: expect.objectContaining({
        sourceVersionId: "A-v0",
        targetVersionId: "B-v0",
      }),
    });
  });
});

import type { NodeLink, Prisma } from "@prisma/client";
import { prisma } from "./prisma";

type PrismaGraphClient = Prisma.TransactionClient | typeof prisma;

type CreateMirrorLinkInput = {
  sourceNodeId: string;
  targetNodeId: string;
  sourceVersionId?: string | null;
  targetVersionId?: string | null;
};

async function mirrorCycleExists(
  client: PrismaGraphClient,
  sourceNodeId: string,
  targetNodeId: string
): Promise<boolean> {
  const reachabilityCheck = await client.$queryRaw<{ id: string }[]>`
    WITH RECURSIVE reachable(id) AS (
      SELECT targetNodeId
      FROM NodeLink
      WHERE sourceNodeId = ${targetNodeId} AND relationType = 'mirror'

      UNION

      SELECT e.targetNodeId
      FROM NodeLink e
      JOIN reachable r ON e.sourceNodeId = r.id
      WHERE e.relationType = 'mirror'
    )
    SELECT id
    FROM reachable
    WHERE id = ${sourceNodeId}
    LIMIT 1;
  `;

  return reachabilityCheck.length > 0;
}

export async function validateAcyclicMirror(
  sourceNodeId: string,
  targetNodeId: string,
  client: PrismaGraphClient = prisma
): Promise<boolean> {
  if (sourceNodeId === targetNodeId) {
    throw new Error("Cycle detected: source equals target");
  }

  if (await mirrorCycleExists(client, sourceNodeId, targetNodeId)) {
    throw new Error("Cycle detected in mirror node graph: target can already reach source");
  }

  return true;
}

export async function createMirrorLink(input: CreateMirrorLinkInput): Promise<NodeLink> {
  return prisma.$transaction(async (tx) => {
    await tx.graphWriteLock.upsert({
      where: { scope: "mirror" },
      create: { scope: "mirror" },
      update: {},
    });

    await validateAcyclicMirror(input.sourceNodeId, input.targetNodeId, tx);

    const [sourceNode, targetNode] = await Promise.all([
      tx.node.findUnique({
        where: { id: input.sourceNodeId },
        include: { currentVersion: true },
      }),
      tx.node.findUnique({
        where: { id: input.targetNodeId },
        include: { currentVersion: true },
      }),
    ]);

    if (!sourceNode?.currentVersion) {
      throw new Error(`Cannot create mirror link: source node ${input.sourceNodeId} has no current version`);
    }
    if (!targetNode?.currentVersion) {
      throw new Error(`Cannot create mirror link: target node ${input.targetNodeId} has no current version`);
    }

    return tx.nodeLink.create({
      data: {
        sourceNodeId: input.sourceNodeId,
        sourceVersionId: input.sourceVersionId || sourceNode.currentVersion.id,
        targetNodeId: input.targetNodeId,
        targetVersionId: input.targetVersionId || targetNode.currentVersion.id,
        relationType: "mirror",
        status: "synced",
      },
    });
  });
}

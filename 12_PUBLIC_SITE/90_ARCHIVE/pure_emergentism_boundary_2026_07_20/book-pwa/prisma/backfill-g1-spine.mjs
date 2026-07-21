import { PrismaClient } from "@prisma/client";
import crypto from "node:crypto";

const prisma = new PrismaClient();

function contentHash(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function fallbackNodeContent(node) {
  return node.title || node.summary || node.slug || node.path || node.id;
}

async function ensureNodeVersion(node) {
  if (node.currentVersionId && node.currentVersion) {
    return node.currentVersion;
  }

  const contentMd = fallbackNodeContent(node);
  const hash = contentHash(`${node.path}\n${contentMd}`);
  const existing = await prisma.nodeVersion.findUnique({ where: { hash } });

  const version =
    existing ||
    (await prisma.nodeVersion.create({
      data: {
        hash,
        nodeId: node.id,
        contentMd,
        authorId: "system",
      },
    }));

  await prisma.node.update({
    where: { id: node.id },
    data: { currentVersionId: version.id },
  });

  return version;
}

async function main() {
  const nodes = await prisma.node.findMany({ include: { currentVersion: true } });
  let nodeVersionsCreatedOrLinked = 0;

  for (const node of nodes) {
    const before = node.currentVersionId;
    await ensureNodeVersion(node);
    if (!before) nodeVersionsCreatedOrLinked += 1;
  }

  const branches = await prisma.aIPBranch.findMany({
    where: { sourceVersionId: null },
    include: { sourceNode: { include: { currentVersion: true } } },
  });
  let branchesPinned = 0;

  for (const branch of branches) {
    const versionByHash = await prisma.nodeVersion.findUnique({
      where: { hash: branch.sourceVersionHash },
    });
    const sourceVersion = versionByHash || branch.sourceNode.currentVersion;

    if (!sourceVersion) {
      throw new Error(`Cannot pin branch ${branch.id}: source node ${branch.sourceNodeId} has no current version`);
    }

    await prisma.aIPBranch.update({
      where: { id: branch.id },
      data: { sourceVersionId: sourceVersion.id },
    });
    branchesPinned += 1;
  }

  const links = await prisma.nodeLink.findMany({
    where: {
      OR: [{ sourceVersionId: null }, { targetVersionId: null }],
    },
    include: {
      sourceNode: { include: { currentVersion: true } },
      targetNode: { include: { currentVersion: true } },
    },
  });
  let linksPinned = 0;

  for (const link of links) {
    const sourceVersion = link.sourceNode.currentVersion;
    const targetVersion = link.targetNode.currentVersion;

    if (!sourceVersion || !targetVersion) {
      throw new Error(`Cannot pin link ${link.id}: source or target node has no current version`);
    }

    await prisma.nodeLink.update({
      where: { id: link.id },
      data: {
        sourceVersionId: link.sourceVersionId || sourceVersion.id,
        targetVersionId: link.targetVersionId || targetVersion.id,
      },
    });
    linksPinned += 1;
  }

  await prisma.graphWriteLock.upsert({
    where: { scope: "mirror" },
    create: { scope: "mirror" },
    update: {},
  });

  console.log(
    JSON.stringify(
      {
        nodesScanned: nodes.length,
        nodeVersionsCreatedOrLinked,
        branchesPinned,
        linksPinned,
        mirrorWriteLockReady: true,
      },
      null,
      2
    )
  );
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

import { prisma } from "@/lib/prisma";
import { buildTree } from "@/lib/tree";
import { GraphProvider } from "@/components/outliner/GraphProvider";
import { OutlineViewport } from "@/components/outliner/OutlineViewport";
import { loadWorldviewManifest } from "@/lib/aia/worldview";
import { notFound } from "next/navigation";

export async function generateStaticParams() {
  const chapters = await prisma.node.findMany({
    where: { depth: 1 },
    select: { slug: true }
  });
  return chapters.map((c) => ({ id: c.slug }));
}

export default async function ChapterPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  const rootNode = await prisma.node.findUnique({
    where: { slug: id },
    select: { path: true }
  });

  if (!rootNode) notFound();

  const flatNodes = await prisma.node.findMany({
    where: {
      path: { startsWith: rootNode.path }
    },
    include: {
      currentVersion: true
    }
  });

  const serializedNodes = flatNodes.map(n => ({
    id: n.id,
    parentId: n.parentId,
    path: n.path,
    depth: n.depth,
    orderIndex: n.orderIndex,
    title: n.title,
    slug: n.slug,
    canonicalTextMd: n.currentVersion?.contentMd || "",
    currentVersionHash: n.currentVersion?.hash,
  }));

  const chapterTree = buildTree(serializedNodes);
  const worldviewManifest = loadWorldviewManifest();
  const projectionLensOptions = Object.entries(worldviewManifest.projectionLenses ?? {}).map(
    ([id, lens]) => ({
      id,
      label: lens.label,
    })
  );

  return (
    <div className="min-h-screen bg-white font-sans selection:bg-[#b3d4fc] selection:text-black">
      <GraphProvider flatNodes={serializedNodes} rootNodeId={chapterTree.id}>
        <OutlineViewport rootNodeId={chapterTree.id} projectionLensOptions={projectionLensOptions} />
      </GraphProvider>
    </div>
  );
}

import { GraphProvider } from "@/components/outliner/GraphProvider";
import { OutlineViewport } from "@/components/outliner/OutlineViewport";
import { loadWorldviewManifest } from "@/lib/aia/worldview";
import { prisma } from "@/lib/prisma";

const ROOT_NODE_ID = "infinite-book-root";

export default async function Home() {
  const nodes = await prisma.node.findMany({
    orderBy: { orderIndex: "asc" },
    include: { currentVersion: true },
  });

  if (nodes.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white px-6 text-sm text-[#555]">
        No outline nodes found.
      </div>
    );
  }

  const serializedNodes = [
    {
      id: ROOT_NODE_ID,
      parentId: null,
      path: "the-infinite-book-of-emergence",
      depth: 0,
      orderIndex: -1,
      title: "The Infinite Book of Emergence",
      slug: "the-infinite-book-of-emergence",
      canonicalTextMd: "The Infinite Book of Emergence",
      currentVersionHash: ROOT_NODE_ID,
    },
    ...nodes.map((node) => ({
      id: node.id,
      parentId: node.parentId ?? ROOT_NODE_ID,
      path: node.path,
      depth: node.depth,
      orderIndex: node.orderIndex,
      title: node.title,
      slug: node.slug,
      canonicalTextMd: node.currentVersion?.contentMd || "",
      currentVersionHash: node.currentVersion?.hash,
    })),
  ];
  const worldviewManifest = loadWorldviewManifest();
  const projectionLensOptions = Object.entries(worldviewManifest.projectionLenses ?? {}).map(
    ([id, lens]) => ({
      id,
      label: lens.label,
    })
  );

  return (
    <div className="min-h-screen bg-white font-sans selection:bg-neutral-200 selection:text-neutral-950">
      <GraphProvider flatNodes={serializedNodes} rootNodeId={ROOT_NODE_ID}>
        <OutlineViewport rootNodeId={ROOT_NODE_ID} projectionLensOptions={projectionLensOptions} />
      </GraphProvider>
    </div>
  );
}

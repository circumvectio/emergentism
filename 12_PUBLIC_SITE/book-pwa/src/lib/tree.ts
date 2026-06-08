export type GraphNodeSource = {
  id: string;
  parentId: string | null;
  path: string;
  depth: number;
  orderIndex: number;
  title: string | null;
  slug: string;
  canonicalTextMd: string;
  currentVersionHash?: string;
};

export type TreeNode = GraphNodeSource & {
  children: TreeNode[];
  type: 'chapter' | 'section' | 'paragraph';
};

export function buildTree(flatNodes: GraphNodeSource[]): TreeNode {
  const nodeMap = new Map<string, TreeNode>();
  let rootNode: TreeNode | null = null;

  // Find the root (depth 1)
  const rootRaw = flatNodes.find(n => n.depth === 1);
  if (!rootRaw) throw new Error("No root node found in this branch");

  // Create all node objects
  for (const n of flatNodes) {
    nodeMap.set(n.id, {
      ...n,
      children: [],
      type: n.depth === 1 ? 'chapter' : n.title ? 'section' : 'paragraph'
    });
  }

  // Assign children
  for (const n of flatNodes) {
    if (n.parentId) {
      const parent = nodeMap.get(n.parentId);
      if (parent) {
        parent.children.push(nodeMap.get(n.id)!);
      }
    } else {
      rootNode = nodeMap.get(n.id)!;
    }
  }

  // Sort children by orderIndex
  for (const node of nodeMap.values()) {
    node.children.sort((a, b) => a.orderIndex - b.orderIndex);
  }

  return rootNode!;
}

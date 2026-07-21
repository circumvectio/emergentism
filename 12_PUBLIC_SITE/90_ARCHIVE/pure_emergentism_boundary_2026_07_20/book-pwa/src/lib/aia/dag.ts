// ─────────────────────────────────────────────────────────────────────────
// AIA · DAG integrity — the mirroring problem.
//
// Mirror edges let a concept appear in more than one place ("one recursive
// knowledge tree"), turning the strict tree into a Directed Acyclic Graph.
// The invariant: an edge may never close a cycle, or any traversal that reads
// the subtree loops forever. This is the pure, client-side mirror of the
// PostgreSQL BEFORE-INSERT cycle trigger described in the architecture spec —
// the proof is reachability, not trigger depth.
// ─────────────────────────────────────────────────────────────────────────

export interface Edge {
  source: string;
  target: string;
}

/**
 * Would adding `source → target` create a cycle?
 * A cycle forms iff `target` can already reach `source`. We DFS from `target`
 * over existing edges looking for `source`.
 */
export function wouldCreateCycle(edges: Edge[], source: string, target: string): boolean {
  if (source === target) return true;

  const adjacency = new Map<string, string[]>();
  for (const e of edges) {
    const outs = adjacency.get(e.source);
    if (outs) outs.push(e.target);
    else adjacency.set(e.source, [e.target]);
  }

  const seen = new Set<string>();
  const stack = [target];
  while (stack.length > 0) {
    const current = stack.pop()!;
    if (current === source) return true;
    if (seen.has(current)) continue;
    seen.add(current);
    for (const next of adjacency.get(current) ?? []) stack.push(next);
  }
  return false;
}

/** Append a mirror edge, refusing (by throwing) any edge that would cycle. */
export function addMirrorEdge(edges: Edge[], source: string, target: string): Edge[] {
  if (wouldCreateCycle(edges, source, target)) {
    throw new Error(`Refusing mirror edge ${source} → ${target}: would create a cycle.`);
  }
  return [...edges, { source, target }];
}

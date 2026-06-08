"use client";

import { useEffect, useRef, useState } from "react";
import { useGraphStore, NodeInstance } from "@/lib/store";
import type { GraphNodeSource } from "@/lib/tree";

interface GraphProviderProps {
  flatNodes: GraphNodeSource[];
  rootNodeId: string;
  children: React.ReactNode;
}

export function GraphProvider({ flatNodes, rootNodeId, children }: GraphProviderProps) {
  const hydrate = useGraphStore(state => state.hydrate);
  const dispatch = useGraphStore(state => state.dispatch);
  const hydrated = useRef(false);
  const branchesHydrated = useRef(false);
  const userHydrated = useRef(false);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    if (!hydrated.current) {
      const instances: NodeInstance[] = flatNodes.map(n => ({
        id: n.id,
        type: n.title ? (n.depth <= 1 ? 'chapter' : 'section') : 'paragraph',
        canonicalTextMd: n.canonicalTextMd,
        currentVersionHash: n.currentVersionHash,
        isExpanded: false,
        childrenIds: flatNodes
          .filter(child => child.parentId === n.id)
          .sort((a, b) => a.orderIndex - b.orderIndex)
          .map(child => child.id),
        branchIds: [],
        syncStatus: 'synced'
      }));

      hydrate(instances, rootNodeId);
      hydrated.current = true;
      setIsHydrated(true);
    }
  }, [flatNodes, hydrate, rootNodeId]);

  useEffect(() => {
    if (!isHydrated || userHydrated.current) return;

    const loadCurrentUser = async () => {
      userHydrated.current = true;
      try {
        const response = await fetch("/api/me");
        if (!response.ok) return;
        const data = await response.json();
        if (data.user) {
          dispatch({ type: "HYDRATE_CURRENT_USER", user: data.user });
        }
      } catch (error) {
        console.error("Failed to load current user capabilities", error);
      }
    };

    void loadCurrentUser();
  }, [dispatch, isHydrated]);

  useEffect(() => {
    if (!isHydrated || branchesHydrated.current || flatNodes.length === 0) return;

    const loadBranches = async () => {
      branchesHydrated.current = true;
      const nodeIds = encodeURIComponent(flatNodes.map((node) => node.id).join(","));
      try {
        const response = await fetch(`/api/branches?nodeIds=${nodeIds}`);
        if (!response.ok) return;
        const data = await response.json();
        if (Array.isArray(data.branches) && data.branches.length > 0) {
          dispatch({ type: "HYDRATE_SERVER_BRANCHES", branches: data.branches });
        }
      } catch (error) {
        console.error("Failed to load private branches", error);
      }
    };

    void loadBranches();
  }, [dispatch, flatNodes, isHydrated]);

  // Sync Queue Processor
  const syncQueue = useGraphStore(state => state.syncQueue);
  const processing = useRef(false);

  useEffect(() => {
    if (syncQueue.length > 0 && !processing.current) {
      const processQueue = async () => {
        processing.current = true;
        const op = syncQueue[0]; // grab first operation

        try {
          if (op.type === 'CREATE_AI_BRANCH') {
            const res = await fetch('/api/expand', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                nodeId: op.sourceNodeId,
                prompt: op.prompt ?? 'Expand on this concept',
                mode: op.mode,
                retrievalNodeIds: op.retrievalNodeIds,
                projectionLensId: op.projectionLensId,
              }),
            });

            if (res.status === 409 || res.status === 403) {
              // 409 Conflict or 403 Forbidden (no credits)
              const errorText = await res.text();
              dispatch({ type: 'SYNC_FAILED', localId: op.localId, error: errorText });
            } else if (res.ok) {
              const data = await res.json();
              if (data.branch) {
                dispatch({ type: 'BRANCH_GENERATION_CHUNK', localId: op.localId, chunk: data.branch.outputMd });
                dispatch({
                  type: 'BRANCH_GENERATION_COMPLETE',
                  localId: op.localId,
                  serverId: data.branch.id,
                  contradictions: data.contradictions ?? [],
                  consistencyReport: data.consistencyReport,
                });
              }
            } else {
               dispatch({ type: 'SYNC_FAILED', localId: op.localId, error: 'Server error' });
            }
          }
        } catch (e) {
          console.error("Sync op failed", e);
          dispatch({ type: 'SYNC_FAILED', localId: op.localId, error: 'Network error' });
        } finally {
          // Remove the processed op from queue
          useGraphStore.setState(s => ({ syncQueue: s.syncQueue.slice(1) }));
          processing.current = false;
        }
      };

      processQueue();
    }
  }, [syncQueue, dispatch]);

  if (!isHydrated) {
    return null;
  }

  return <>{children}</>;
}

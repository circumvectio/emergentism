import { create } from 'zustand';
import { openDB, IDBPDatabase } from 'idb';
import type { BranchConsistencyReport, ConsistencyReportStatus } from './aia/consistency';

export type NodeInstance = {
  id: string;
  type: string;
  canonicalTextMd: string;
  currentVersionHash?: string;
  isExpanded?: boolean;
  childrenIds?: string[];
  branchIds?: string[];
  syncStatus?: 'synced' | 'pending' | 'conflict';
};

export type PendingAIBranch = {
  localId: string;
  serverId?: string;
  sourceNodeId: string;
  /** The exact content hash of the canon version when this branch was created.
   *  This is the immutability moat: a branch is permanently pinned to the
   *  version it grew from, even if canon mutates later. */
  sourceVersionHash: string;
  status: "queued" | "generating" | "complete" | "failed";
  outputMd: string;
  depth: number;
  projectionLensId?: string;
  contradictions?: BranchContradictionSummary[];
  consistencyStatus?: ConsistencyReportStatus;
  consistencyReport?: BranchConsistencyReport;
  consistencyCheckStatus?: "checking" | "failed";
  consistencyCheckError?: string;
  revisionStatus?: "editing" | "saving" | "saved" | "failed";
  revisionDraftMd?: string;
  visibility?: "private" | "shared" | "proposed_canon" | "accepted_canon";
  proposalStatus?: "idle" | "submitted" | "conflict" | "failed";
  proposalError?: string;
  reviewStatus?: "accepted" | "rejected" | "revision_requested" | "failed";
  reviewFeedback?: string | null;
  reviewError?: string;
};

export type BranchContradictionSummary = {
  id: string;
  type: string;
  severity: "low" | "medium" | "high";
  explanation: string;
  resolutionStatus: string;
};

export type SyncOperation = {
  type: "CREATE_AI_BRANCH" | "RESOLVE_CONFLICT";
  localId: string;
  sourceNodeId: string;
  /** Pinned canon version at branch-creation time. */
  sourceVersionHash?: string;
  mode?: string;
  prompt?: string;
  retrievalNodeIds?: string[];
  projectionLensId?: string;
};

export type ThreadMessage = {
  id: string;
  role: "user" | "assistant";
  contentMd: string;
  status?: "streaming" | "complete";
};

export type ThreadState = {
  nodeId: string;
  messages: ThreadMessage[];
};

export type CurrentUserCapabilities = {
  id: string;
  role: "reader" | "canon_reviewer" | "admin";
  canReviewCanon: boolean;
  canAssignRoles: boolean;
};

type AssignableUserRole = CurrentUserCapabilities["role"];

export type RoleAssignmentCandidate = {
  id: string;
  email: string;
  role: AssignableUserRole;
};

export type RoleAssignmentAuditSummary = {
  id: string;
  targetUserId: string;
  targetUserEmail?: string | null;
  actorUserId: string;
  actorUserEmail?: string | null;
  fromRole: string;
  toRole: string;
  createdAt: string;
};

export type CanonReviewAuditSummary = {
  id: string;
  branchId: string;
  branchSourceNodeId?: string | null;
  branchSourceLabel?: string | null;
  branchSourceSlug?: string | null;
  branchSourceHref?: string | null;
  reviewerId: string;
  reviewerEmail?: string | null;
  decision: "accept" | "reject" | "revise";
  notes?: string | null;
  createdAt: string;
};

export type CanonReviewQueueItem = {
  id: string;
  authorId: string;
  authorEmail?: string | null;
  sourceNodeId: string;
  sourceLabel: string;
  sourceSlug?: string | null;
  sourceHref?: string | null;
  sourceVersionHash: string;
  consistencyStatus?: string;
  consistencyReportSource?: string | null;
  consistencySummary?: string | null;
  currentVersionHash?: string | null;
  isStaleSource: boolean;
  outputPreview: string;
  createdAt: string;
  actionStatus?: "failed";
  actionError?: string;
};

export type LocalGraphState = {
  nodesById: Record<string, NodeInstance>;
  branchesById: Record<string, PendingAIBranch>;
  focusStack: string[];
  syncQueue: SyncOperation[];
  selectedProjectionLensId?: string;
  currentUser?: CurrentUserCapabilities;
  roleAssignmentStatus?: "saved" | "failed";
  roleAssignmentError?: string;
  roleAssignmentCandidates?: RoleAssignmentCandidate[];
  userLookupStatus?: "loaded" | "failed";
  userLookupError?: string;
  roleAssignmentAudits?: RoleAssignmentAuditSummary[];
  roleAuditStatus?: "loaded" | "failed";
  roleAuditError?: string;
  roleAuditNextCursor?: string;
  canonReviewAudits?: CanonReviewAuditSummary[];
  canonReviewAuditStatus?: "loaded" | "failed";
  canonReviewAuditError?: string;
  canonReviewAuditNextCursor?: string;
  canonReviewQueue?: CanonReviewQueueItem[];
  canonReviewQueueStatus?: "loaded" | "failed";
  canonReviewQueueError?: string;
  canonReviewQueueNextCursor?: string;
  // SWIPE_LEFT_NODE ("swipe to speak") opens a chat thread anchored to a node.
  activeThreadNodeId?: string | null;
  threadsByNodeId: Record<string, ThreadState>;
};

interface GraphStore extends LocalGraphState {
  dispatch: (event: InteractionEvent) => void;
  hydrate: (nodes: NodeInstance[], rootNodeId?: string) => void;
}

export type InteractionEvent =
  | { type: "EXPAND_NODE"; nodeId: string }
  | { type: "COLLAPSE_NODE"; nodeId: string }
  | { type: "PUSH_FOCUS"; nodeId: string }
  | { type: "SET_FOCUS_STACK"; nodeIds: string[] }
  | { type: "SET_PROJECTION_LENS"; projectionLensId?: string }
  | { type: "LONG_PRESS_NODE"; nodeId: string }
  | { type: "HYDRATE_SERVER_BRANCHES"; branches: PendingAIBranch[] }
  | { type: "HYDRATE_CURRENT_USER"; user: CurrentUserCapabilities }
  | { type: "MARK_USER_ROLE_ASSIGNED"; userId: string; role: AssignableUserRole }
  | { type: "MARK_USER_ROLE_ASSIGNMENT_FAILED"; error: string }
  | { type: "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES"; users: RoleAssignmentCandidate[] }
  | { type: "MARK_USER_LOOKUP_FAILED"; error: string }
  | {
      type: "HYDRATE_ROLE_ASSIGNMENT_AUDITS";
      audits: RoleAssignmentAuditSummary[];
      append?: boolean;
      nextCursor?: string;
    }
  | { type: "MARK_ROLE_AUDIT_LOOKUP_FAILED"; error: string }
  | {
      type: "HYDRATE_CANON_REVIEW_AUDITS";
      reviews: CanonReviewAuditSummary[];
      append?: boolean;
      nextCursor?: string;
    }
  | { type: "MARK_CANON_REVIEW_AUDIT_LOOKUP_FAILED"; error: string }
  | {
      type: "HYDRATE_CANON_REVIEW_QUEUE";
      branches: CanonReviewQueueItem[];
      append?: boolean;
      nextCursor?: string;
    }
  | { type: "MARK_CANON_REVIEW_QUEUE_LOOKUP_FAILED"; error: string }
  | {
      type: "MARK_CANON_REVIEW_QUEUE_ITEM_REVIEWED";
      branchId: string;
      decision: "accept" | "reject" | "revise";
    }
  | { type: "MARK_CANON_REVIEW_QUEUE_ITEM_FAILED"; branchId: string; error: string }
  | { type: "SWIPE_LEFT_NODE"; nodeId: string }
  | { type: "SWIPE_RIGHT" }
  | { type: "BRANCH_GENERATION_CHUNK"; localId: string; chunk: string }
  | {
      type: "BRANCH_GENERATION_COMPLETE";
      localId: string;
      serverId?: string;
      contradictions?: BranchContradictionSummary[];
      consistencyReport?: BranchConsistencyReport;
    }
  | { type: "SYNC_FAILED"; localId: string; error: string }
  | { type: "RESOLVE_CONFLICT"; localId: string; action: 'keep_private' | 'discard' }
  | {
      type: "RESOLVE_BRANCH_CONTRADICTION";
      localId: string;
      contradictionId: string;
      resolutionStatus: string;
    }
  | { type: "START_BRANCH_REVISION"; localId: string }
  | { type: "UPDATE_BRANCH_REVISION_DRAFT"; localId: string; outputMd: string }
  | { type: "COMMIT_BRANCH_REVISION"; localId: string; outputMd: string }
  | { type: "CANCEL_BRANCH_REVISION"; localId: string }
  | { type: "MARK_BRANCH_CANON_PROPOSED"; localId: string }
  | { type: "MARK_BRANCH_CANON_PROPOSAL_FAILED"; localId: string; error: string }
  | { type: "MARK_BRANCH_CONSISTENCY_CHECKING"; localId: string }
  | {
      type: "MARK_BRANCH_CONSISTENCY_CHECKED";
      localId: string;
      consistencyReport: BranchConsistencyReport;
      contradictions?: BranchContradictionSummary[];
    }
  | { type: "MARK_BRANCH_CONSISTENCY_CHECK_FAILED"; localId: string; error: string }
  | {
      type: "MARK_BRANCH_CANON_REVIEWED";
      localId: string;
      decision: "accept" | "reject" | "revise";
      reviewFeedback?: string | null;
    }
  | { type: "MARK_BRANCH_CANON_REVIEW_FAILED"; localId: string; error: string }
  // Thread / chat events ("swipe to speak")
  | { type: "CLOSE_THREAD" }
  // Keyboard editing events ("the editing commands")
  | { type: "UPDATE_NODE_TEXT"; nodeId: string; text: string }
  | { type: "ENTER_SPLIT"; nodeId: string; cursorOffset: number }
  | { type: "TAB_INDENT"; nodeId: string }
  | { type: "SHIFT_TAB_OUTDENT"; nodeId: string }
  | { type: "BACKSPACE_MERGE"; nodeId: string };

// Initialize IndexedDB
let dbPromise: Promise<IDBPDatabase> | null = null;
if (typeof window !== 'undefined') {
  dbPromise = openDB('InfiniteBookDB', 2, {
    upgrade(db, oldVersion) {
      if (oldVersion < 1) {
        db.createObjectStore('nodes', { keyPath: 'id' });
        db.createObjectStore('branches', { keyPath: 'localId' });
        db.createObjectStore('ui_state'); // For focusStack
      }
      if (oldVersion < 2) {
        // Chat threads anchored to a node ("swipe to speak").
        db.createObjectStore('threads', { keyPath: 'nodeId' });
      }
    },
  });
}

// Stores touched by dispatch persistence. Keep in sync with the upgrade() above.
const IDB_STORES = ['nodes', 'branches', 'ui_state', 'threads'] as const;

export const useGraphStore = create<GraphStore>((set) => ({
  nodesById: {},
  branchesById: {},
  focusStack: ['root'],
  syncQueue: [],
  selectedProjectionLensId: undefined,
  currentUser: undefined,
  roleAssignmentStatus: undefined,
  roleAssignmentError: undefined,
  roleAssignmentCandidates: [],
  userLookupStatus: undefined,
  userLookupError: undefined,
  roleAssignmentAudits: [],
  roleAuditStatus: undefined,
  roleAuditError: undefined,
  roleAuditNextCursor: undefined,
  canonReviewAudits: [],
  canonReviewAuditStatus: undefined,
  canonReviewAuditError: undefined,
  canonReviewAuditNextCursor: undefined,
  canonReviewQueue: [],
  canonReviewQueueStatus: undefined,
  canonReviewQueueError: undefined,
  canonReviewQueueNextCursor: undefined,
  activeThreadNodeId: null,
  threadsByNodeId: {},

  hydrate: (nodes: NodeInstance[], rootNodeId?: string) => {
    const nodesById: Record<string, NodeInstance> = {};
    nodes.forEach(n => {
      nodesById[n.id] = { ...n, isExpanded: n.id === rootNodeId ? true : n.isExpanded ?? false };
    });
    set((state) => {
      const currentFocus = state.focusStack[state.focusStack.length - 1];
      const nextRoot = rootNodeId && nodesById[rootNodeId] ? rootNodeId : nodes[0]?.id;
      return {
        nodesById,
        focusStack: currentFocus && nodesById[currentFocus] && state.focusStack[0] === nextRoot
          ? state.focusStack.filter((id) => nodesById[id])
          : nextRoot
            ? [nextRoot]
            : state.focusStack,
      };
    });
  },

  dispatch: (event: InteractionEvent) => {
    set((state) => {
      const nextState = graphReducer(state, event);

      // Async persist to IDB (fire and forget to not block UI)
      if (dbPromise) {
        dbPromise.then(async (db) => {
          const tx = db.transaction(IDB_STORES as unknown as string[], 'readwrite');

          if (
            event.type === 'LONG_PRESS_NODE' ||
            event.type === 'BRANCH_GENERATION_CHUNK' ||
            event.type === 'BRANCH_GENERATION_COMPLETE' ||
            event.type === 'SYNC_FAILED' ||
            event.type === 'MARK_BRANCH_CANON_PROPOSED' ||
            event.type === 'MARK_BRANCH_CANON_PROPOSAL_FAILED' ||
            event.type === 'MARK_BRANCH_CONSISTENCY_CHECKING' ||
            event.type === 'MARK_BRANCH_CONSISTENCY_CHECKED' ||
            event.type === 'MARK_BRANCH_CONSISTENCY_CHECK_FAILED' ||
            event.type === 'MARK_BRANCH_CANON_REVIEWED' ||
            event.type === 'MARK_BRANCH_CANON_REVIEW_FAILED'
          ) {
            if ('localId' in event && nextState.branchesById[event.localId]) {
              await tx.objectStore('branches').put(nextState.branchesById[event.localId]);
            }
          }

          if (event.type === 'EXPAND_NODE' || event.type === 'COLLAPSE_NODE') {
             const node = nextState.nodesById[event.nodeId];
             if (node) await tx.objectStore('nodes').put(node);
          }

          if (event.type === 'PUSH_FOCUS' || event.type === 'SET_FOCUS_STACK' || event.type === 'SWIPE_RIGHT') {
             await tx.objectStore('ui_state').put(nextState.focusStack, 'focusStack');
          }

          // Persist node-structure edits (text, split, indent/outdent, merge).
          // childrenIds arrays are authoritative client-side, so we persist every
          // node the reducer may have touched, not just the targeted one.
          if (
            event.type === 'UPDATE_NODE_TEXT' ||
            event.type === 'ENTER_SPLIT' ||
            event.type === 'TAB_INDENT' ||
            event.type === 'SHIFT_TAB_OUTDENT' ||
            event.type === 'BACKSPACE_MERGE'
          ) {
            const nodeStore = tx.objectStore('nodes');
            for (const node of Object.values(nextState.nodesById)) {
              if (node) await nodeStore.put(node);
            }
          }

          // Persist thread state for "swipe to speak".
          if (event.type === 'SWIPE_LEFT_NODE') {
            const thread = nextState.threadsByNodeId[event.nodeId];
            if (thread) await tx.objectStore('threads').put(thread);
            await tx.objectStore('ui_state').put(nextState.activeThreadNodeId ?? null, 'activeThreadNodeId');
          }
          if (event.type === 'CLOSE_THREAD') {
            await tx.objectStore('ui_state').put(nextState.activeThreadNodeId ?? null, 'activeThreadNodeId');
          }

          await tx.done;
        });
      }

      return nextState;
    });
  },
}));

function findParentId(state: LocalGraphState, childId: string): string | null {
  for (const node of Object.values(state.nodesById)) {
    if (node.childrenIds?.includes(childId)) {
      return node.id;
    }
  }
  return null;
}

function makeSplitNodeId(nodeId: string): string {
  return `${nodeId}_split_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
}

function makeBranchId(): string {
  return `branch_${Date.now()}_${Math.random().toString(36).substring(7)}`;
}

// The Core State Machine Reducer
export function graphReducer(state: LocalGraphState, event: InteractionEvent): LocalGraphState {
  switch (event.type) {
    case "EXPAND_NODE": {
      const node = state.nodesById[event.nodeId];
      if (!node) return state;
      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: { ...node, isExpanded: true }
        }
      };
    }

    case "COLLAPSE_NODE": {
      const node = state.nodesById[event.nodeId];
      if (!node) return state;
      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: { ...node, isExpanded: false }
        }
      };
    }

    case "PUSH_FOCUS": {
      const node = state.nodesById[event.nodeId];
      if (!node) return state;
      const existingIndex = state.focusStack.indexOf(event.nodeId);
      if (existingIndex >= 0) {
        return {
          ...state,
          focusStack: state.focusStack.slice(0, existingIndex + 1),
        };
      }
      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: { ...node, isExpanded: true },
        },
        focusStack: [...state.focusStack, event.nodeId],
      };
    }

    case "SET_FOCUS_STACK": {
      const validPath = event.nodeIds.filter((nodeId) => state.nodesById[nodeId]);
      if (validPath.length === 0) return state;
      return {
        ...state,
        focusStack: validPath,
      };
    }

    case "SET_PROJECTION_LENS": {
      const projectionLensId = event.projectionLensId?.trim();
      return {
        ...state,
        selectedProjectionLensId: projectionLensId || undefined,
      };
    }

    case "LONG_PRESS_NODE": {
      const localId = makeBranchId();
      const sourceNode = state.nodesById[event.nodeId];
      const sourceVersionHash = sourceNode?.currentVersionHash ?? `local_${event.nodeId}`;
      const pending: PendingAIBranch = {
        localId,
        sourceNodeId: event.nodeId,
        sourceVersionHash,
        status: "queued",
        outputMd: "",
        depth: 1,
        projectionLensId: state.selectedProjectionLensId,
      };

      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [localId]: { ...pending, sourceVersionHash }
        },
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: {
            ...sourceNode,
            isExpanded: true,
            branchIds: [...(sourceNode?.branchIds || []), localId]
          }
        },
        syncQueue: [
          ...state.syncQueue,
          {
            type: "CREATE_AI_BRANCH",
            localId: localId,
            sourceNodeId: event.nodeId,
            sourceVersionHash,
            projectionLensId: state.selectedProjectionLensId,
          }
        ]
      };
    }

    case "HYDRATE_SERVER_BRANCHES": {
      const branchesById = { ...state.branchesById };
      const nodesById = { ...state.nodesById };

      for (const branch of event.branches) {
        const sourceNode = nodesById[branch.sourceNodeId];
        if (!sourceNode) continue;

        branchesById[branch.localId] = branch;
        const branchIds = sourceNode.branchIds ?? [];
        nodesById[branch.sourceNodeId] = {
          ...sourceNode,
          branchIds: branchIds.includes(branch.localId)
            ? branchIds
            : [...branchIds, branch.localId],
        };
      }

      return {
        ...state,
        branchesById,
        nodesById,
      };
    }

    case "HYDRATE_CURRENT_USER": {
      return {
        ...state,
        currentUser: event.user,
      };
    }

    case "MARK_USER_ROLE_ASSIGNED": {
      const canAssignRoles = event.role === "admin";
      const canReviewCanon = event.role === "admin" || event.role === "canon_reviewer";
      return {
        ...state,
        currentUser: state.currentUser?.id === event.userId
          ? {
              ...state.currentUser,
              role: event.role,
              canReviewCanon,
              canAssignRoles,
            }
          : state.currentUser,
        roleAssignmentStatus: "saved",
        roleAssignmentError: undefined,
      };
    }

    case "MARK_USER_ROLE_ASSIGNMENT_FAILED": {
      return {
        ...state,
        roleAssignmentStatus: "failed",
        roleAssignmentError: event.error,
      };
    }

    case "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES": {
      return {
        ...state,
        roleAssignmentCandidates: event.users,
        userLookupStatus: "loaded",
        userLookupError: undefined,
      };
    }

    case "MARK_USER_LOOKUP_FAILED": {
      return {
        ...state,
        userLookupStatus: "failed",
        userLookupError: event.error,
      };
    }

    case "HYDRATE_ROLE_ASSIGNMENT_AUDITS": {
      return {
        ...state,
        roleAssignmentAudits: event.append
          ? [...(state.roleAssignmentAudits ?? []), ...event.audits]
          : event.audits,
        roleAuditStatus: "loaded",
        roleAuditError: undefined,
        roleAuditNextCursor: event.nextCursor,
      };
    }

    case "MARK_ROLE_AUDIT_LOOKUP_FAILED": {
      return {
        ...state,
        roleAuditStatus: "failed",
        roleAuditError: event.error,
      };
    }

    case "HYDRATE_CANON_REVIEW_AUDITS": {
      return {
        ...state,
        canonReviewAudits: event.append
          ? [...(state.canonReviewAudits ?? []), ...event.reviews]
          : event.reviews,
        canonReviewAuditStatus: "loaded",
        canonReviewAuditError: undefined,
        canonReviewAuditNextCursor: event.nextCursor,
      };
    }

    case "MARK_CANON_REVIEW_AUDIT_LOOKUP_FAILED": {
      return {
        ...state,
        canonReviewAuditStatus: "failed",
        canonReviewAuditError: event.error,
      };
    }

    case "HYDRATE_CANON_REVIEW_QUEUE": {
      return {
        ...state,
        canonReviewQueue: event.append
          ? [...(state.canonReviewQueue ?? []), ...event.branches]
          : event.branches,
        canonReviewQueueStatus: "loaded",
        canonReviewQueueError: undefined,
        canonReviewQueueNextCursor: event.nextCursor,
      };
    }

    case "MARK_CANON_REVIEW_QUEUE_LOOKUP_FAILED": {
      return {
        ...state,
        canonReviewQueueStatus: "failed",
        canonReviewQueueError: event.error,
      };
    }

    case "MARK_CANON_REVIEW_QUEUE_ITEM_REVIEWED": {
      return {
        ...state,
        canonReviewQueue: (state.canonReviewQueue ?? []).filter((branch) => branch.id !== event.branchId),
      };
    }

    case "MARK_CANON_REVIEW_QUEUE_ITEM_FAILED": {
      return {
        ...state,
        canonReviewQueue: (state.canonReviewQueue ?? []).map((branch) =>
          branch.id === event.branchId
            ? {
                ...branch,
                actionStatus: "failed",
                actionError: event.error,
              }
            : branch
        ),
      };
    }

    case "BRANCH_GENERATION_CHUNK": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            status: "generating",
            outputMd: branch.outputMd + event.chunk
          }
        }
      };
    }

    case "BRANCH_GENERATION_COMPLETE": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            serverId: event.serverId ?? branch.serverId,
            status: "complete",
            contradictions: event.contradictions ?? branch.contradictions,
            consistencyReport: event.consistencyReport ?? branch.consistencyReport,
            consistencyStatus: event.consistencyReport?.status ?? branch.consistencyStatus,
          }
        }
      };
    }

    case "SYNC_FAILED": {
      // The crucial "Divergence" mutation
      // We mark the branch as failed/conflicted, preserving the local content
      // without breaking the UI flow.
      const branch = state.branchesById[event.localId];
      if (!branch) return state;

      const sourceNode = state.nodesById[branch.sourceNodeId];

      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            status: "failed" // Triggers the Divergence Badge in UI
          }
        },
        nodesById: {
          ...state.nodesById,
          [branch.sourceNodeId]: {
            ...sourceNode,
            syncStatus: "conflict"
          }
        }
      };
    }

    case "RESOLVE_CONFLICT": {
       if (event.action === 'discard') {
          // Remove branch locally
          const branch = state.branchesById[event.localId];
          const newBranches = { ...state.branchesById };
          delete newBranches[event.localId];

          const sourceNode = state.nodesById[branch.sourceNodeId];
          const newBranchIds = (sourceNode.branchIds || []).filter(id => id !== event.localId);

          return {
             ...state,
             branchesById: newBranches,
             nodesById: {
                ...state.nodesById,
                [branch.sourceNodeId]: {
                   ...sourceNode,
                   branchIds: newBranchIds,
                   syncStatus: "synced"
                }
             }
          };
       }
       // If keep_private, just remove the conflict flag but leave it in IDB
       const branch = state.branchesById[event.localId];
       const sourceNode = state.nodesById[branch.sourceNodeId];
       return {
          ...state,
          branchesById: {
             ...state.branchesById,
             [event.localId]: {
                ...branch,
                status: "complete"
             }
          },
          nodesById: {
             ...state.nodesById,
             [branch.sourceNodeId]: {
                ...sourceNode,
                syncStatus: "synced"
             }
          }
       };
    }

    case "RESOLVE_BRANCH_CONTRADICTION": {
      const branch = state.branchesById[event.localId];
      if (!branch?.contradictions) return state;
      const contradiction = branch.contradictions.find((item) => item.id === event.contradictionId);
      const sourceNode = state.nodesById[branch.sourceNodeId];
      const updatedBranch = {
        ...branch,
        revisionStatus: event.resolutionStatus === "revised" ? "editing" as const : branch.revisionStatus,
        revisionDraftMd: event.resolutionStatus === "revised" ? branch.outputMd : branch.revisionDraftMd,
        contradictions: branch.contradictions.map((item) =>
          item.id === event.contradictionId
            ? { ...item, resolutionStatus: event.resolutionStatus }
            : item
        ),
      };

      if (event.resolutionStatus === "synthesized" && contradiction && sourceNode) {
        const synthesisLocalId = makeBranchId();
        const sourceVersionHash = sourceNode.currentVersionHash ?? `local_${branch.sourceNodeId}`;
        const synthesisBranch: PendingAIBranch = {
          localId: synthesisLocalId,
          sourceNodeId: branch.sourceNodeId,
          sourceVersionHash,
          status: "queued",
          outputMd: "",
          depth: branch.depth + 1,
          projectionLensId: state.selectedProjectionLensId,
        };

        return {
          ...state,
          branchesById: {
            ...state.branchesById,
            [event.localId]: updatedBranch,
            [synthesisLocalId]: synthesisBranch,
          },
          nodesById: {
            ...state.nodesById,
            [branch.sourceNodeId]: {
              ...sourceNode,
              isExpanded: true,
              branchIds: [...(sourceNode.branchIds ?? []), synthesisLocalId],
            },
          },
          syncQueue: [
            ...state.syncQueue,
            {
              type: "CREATE_AI_BRANCH",
              localId: synthesisLocalId,
              sourceNodeId: branch.sourceNodeId,
              sourceVersionHash,
              mode: "synthesize",
              prompt: `Synthesize this unresolved contradiction: ${contradiction.explanation}`,
              retrievalNodeIds: [branch.sourceNodeId],
              projectionLensId: state.selectedProjectionLensId,
            },
          ],
        };
      }

      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: updatedBranch,
        },
      };
    }

    case "START_BRANCH_REVISION": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            revisionStatus: "editing",
            revisionDraftMd: branch.outputMd,
          },
        },
      };
    }

    case "UPDATE_BRANCH_REVISION_DRAFT": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            revisionStatus: "editing",
            revisionDraftMd: event.outputMd,
          },
        },
      };
    }

    case "COMMIT_BRANCH_REVISION": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const {
        consistencyReport: _consistencyReport,
        revisionDraftMd: _revisionDraftMd,
        reviewFeedback: _reviewFeedback,
        reviewStatus: _reviewStatus,
        ...branchWithoutDraft
      } = branch;
      void _consistencyReport;
      void _revisionDraftMd;
      void _reviewFeedback;
      void _reviewStatus;
      const reviewFields = branch.reviewStatus === "revision_requested"
        ? {}
        : {
            reviewStatus: branch.reviewStatus,
            reviewFeedback: branch.reviewFeedback,
          };
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branchWithoutDraft,
            ...reviewFields,
            outputMd: event.outputMd,
            revisionStatus: "saved",
            consistencyStatus: "unchecked",
          },
        },
      };
    }

    case "CANCEL_BRANCH_REVISION": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const { revisionDraftMd: _revisionDraftMd, revisionStatus: _revisionStatus, ...branchWithoutRevision } = branch;
      void _revisionDraftMd;
      void _revisionStatus;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: branchWithoutRevision,
        },
      };
    }

    case "MARK_BRANCH_CANON_PROPOSED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const { proposalError: _proposalError, ...branchWithoutProposalError } = branch;
      void _proposalError;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branchWithoutProposalError,
            visibility: "proposed_canon",
            proposalStatus: "submitted",
          },
        },
      };
    }

    case "MARK_BRANCH_CANON_PROPOSAL_FAILED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            proposalStatus: event.error === "stale_source_version" ? "conflict" : "failed",
            proposalError: event.error,
          },
        },
      };
    }

    case "MARK_BRANCH_CONSISTENCY_CHECKING": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const { consistencyCheckError: _consistencyCheckError, ...branchWithoutError } = branch;
      void _consistencyCheckError;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branchWithoutError,
            consistencyCheckStatus: "checking",
          },
        },
      };
    }

    case "MARK_BRANCH_CONSISTENCY_CHECKED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const {
        consistencyCheckError: _consistencyCheckError,
        consistencyCheckStatus: _consistencyCheckStatus,
        proposalError: _proposalError,
        ...branchWithoutEphemeral
      } = branch;
      void _consistencyCheckError;
      void _consistencyCheckStatus;
      void _proposalError;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branchWithoutEphemeral,
            consistencyStatus: event.consistencyReport.status,
            consistencyReport: event.consistencyReport,
            contradictions: event.contradictions ?? branch.contradictions,
            proposalStatus: branch.proposalStatus === "failed" ? "idle" : branch.proposalStatus,
          },
        },
      };
    }

    case "MARK_BRANCH_CONSISTENCY_CHECK_FAILED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            consistencyStatus: branch.consistencyStatus ?? "unchecked",
            consistencyCheckStatus: "failed",
            consistencyCheckError: event.error,
          },
        },
      };
    }

    case "MARK_BRANCH_CANON_REVIEWED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      const {
        proposalError: _proposalError,
        proposalStatus: _proposalStatus,
        reviewError: _reviewError,
        ...branchAfterReview
      } = branch;
      void _proposalError;
      void _proposalStatus;
      void _reviewError;
      const reviewStatus = event.decision === "accept"
        ? "accepted"
        : event.decision === "reject"
          ? "rejected"
          : "revision_requested";
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branchAfterReview,
            visibility: event.decision === "accept" ? "accepted_canon" : "private",
            reviewStatus,
            reviewFeedback: event.decision === "accept"
              ? undefined
              : event.reviewFeedback ?? branch.reviewFeedback,
          },
        },
      };
    }

    case "MARK_BRANCH_CANON_REVIEW_FAILED": {
      const branch = state.branchesById[event.localId];
      if (!branch) return state;
      return {
        ...state,
        branchesById: {
          ...state.branchesById,
          [event.localId]: {
            ...branch,
            reviewStatus: "failed",
            reviewError: event.error,
          },
        },
      };
    }

    case "SWIPE_RIGHT": {
      if (state.focusStack.length <= 1) return state;
      return {
        ...state,
        focusStack: state.focusStack.slice(0, -1)
      };
    }

    case "SWIPE_LEFT_NODE": {
      // Placeholder for thread UI
      return state;
    }

    case "UPDATE_NODE_TEXT": {
      const node = state.nodesById[event.nodeId];
      if (!node) return state;
      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: {
            ...node,
            canonicalTextMd: event.text,
            syncStatus: "pending",
          },
        },
      };
    }

    case "ENTER_SPLIT": {
      const node = state.nodesById[event.nodeId];
      const parentId = findParentId(state, event.nodeId);
      if (!node || !parentId) return state;

      const parent = state.nodesById[parentId];
      const siblings = parent.childrenIds ?? [];
      const nodeIndex = siblings.indexOf(event.nodeId);
      if (nodeIndex < 0) return state;

      const text = node.canonicalTextMd;
      const cursorOffset = Math.max(0, Math.min(event.cursorOffset, text.length));
      const newId = makeSplitNodeId(event.nodeId);
      const newNode: NodeInstance = {
        ...node,
        id: newId,
        canonicalTextMd: text.slice(cursorOffset),
        childrenIds: [],
        branchIds: [],
        syncStatus: "pending",
      };

      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [event.nodeId]: {
            ...node,
            canonicalTextMd: text.slice(0, cursorOffset),
            syncStatus: "pending",
          },
          [newId]: newNode,
          [parentId]: {
            ...parent,
            childrenIds: [
              ...siblings.slice(0, nodeIndex + 1),
              newId,
              ...siblings.slice(nodeIndex + 1),
            ],
          },
        },
      };
    }

    case "TAB_INDENT": {
      const parentId = findParentId(state, event.nodeId);
      if (!parentId) return state;

      const parent = state.nodesById[parentId];
      const siblings = parent.childrenIds ?? [];
      const nodeIndex = siblings.indexOf(event.nodeId);
      if (nodeIndex <= 0) return state;

      const previousSiblingId = siblings[nodeIndex - 1];
      const previousSibling = state.nodesById[previousSiblingId];
      if (!previousSibling) return state;

      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [parentId]: {
            ...parent,
            childrenIds: siblings.filter((id) => id !== event.nodeId),
          },
          [previousSiblingId]: {
            ...previousSibling,
            isExpanded: true,
            childrenIds: [...(previousSibling.childrenIds ?? []), event.nodeId],
            syncStatus: "pending",
          },
          [event.nodeId]: {
            ...state.nodesById[event.nodeId],
            syncStatus: "pending",
          },
        },
      };
    }

    case "SHIFT_TAB_OUTDENT": {
      const parentId = findParentId(state, event.nodeId);
      if (!parentId) return state;

      const grandParentId = findParentId(state, parentId);
      if (!grandParentId) return state;

      const parent = state.nodesById[parentId];
      const grandParent = state.nodesById[grandParentId];
      const parentChildren = parent.childrenIds ?? [];
      const grandSiblings = grandParent.childrenIds ?? [];
      const parentIndex = grandSiblings.indexOf(parentId);
      if (parentIndex < 0) return state;

      return {
        ...state,
        nodesById: {
          ...state.nodesById,
          [parentId]: {
            ...parent,
            childrenIds: parentChildren.filter((id) => id !== event.nodeId),
            syncStatus: "pending",
          },
          [grandParentId]: {
            ...grandParent,
            childrenIds: [
              ...grandSiblings.slice(0, parentIndex + 1),
              event.nodeId,
              ...grandSiblings.slice(parentIndex + 1),
            ],
          },
          [event.nodeId]: {
            ...state.nodesById[event.nodeId],
            syncStatus: "pending",
          },
        },
      };
    }

    case "BACKSPACE_MERGE": {
      const parentId = findParentId(state, event.nodeId);
      if (!parentId) return state;

      const parent = state.nodesById[parentId];
      const siblings = parent.childrenIds ?? [];
      const nodeIndex = siblings.indexOf(event.nodeId);
      if (nodeIndex <= 0) return state;

      const node = state.nodesById[event.nodeId];
      const previousSiblingId = siblings[nodeIndex - 1];
      const previousSibling = state.nodesById[previousSiblingId];
      if (!node || !previousSibling) return state;

      const nodesById = { ...state.nodesById };
      delete nodesById[event.nodeId];

      return {
        ...state,
        nodesById: {
          ...nodesById,
          [parentId]: {
            ...parent,
            childrenIds: siblings.filter((id) => id !== event.nodeId),
          },
          [previousSiblingId]: {
            ...previousSibling,
            canonicalTextMd: `${previousSibling.canonicalTextMd}${node.canonicalTextMd}`,
            childrenIds: [...(previousSibling.childrenIds ?? []), ...(node.childrenIds ?? [])],
            syncStatus: "pending",
          },
        },
      };
    }

    default:
      return state;
  }
}

import { describe, expect, it } from "vitest";
import { graphReducer, type LocalGraphState } from "../store";

function state(): LocalGraphState {
  return {
    nodesById: {
      root: {
        id: "root",
        type: "chapter",
        canonicalTextMd: "Root",
        isExpanded: true,
        childrenIds: ["a", "b", "c"],
        branchIds: [],
        syncStatus: "synced",
      },
      a: {
        id: "a",
        type: "paragraph",
        canonicalTextMd: "Alpha",
        childrenIds: [],
        branchIds: [],
        syncStatus: "synced",
      },
      b: {
        id: "b",
        type: "paragraph",
        canonicalTextMd: "Bravo",
        childrenIds: [],
        branchIds: [],
        syncStatus: "synced",
      },
      c: {
        id: "c",
        type: "paragraph",
        canonicalTextMd: "Charlie",
        childrenIds: [],
        branchIds: [],
        syncStatus: "synced",
      },
    },
    branchesById: {},
    focusStack: ["root"],
    syncQueue: [],
    activeThreadNodeId: null,
    threadsByNodeId: {},
  };
}

describe("graphReducer outline editing", () => {
  it("updates node text without changing the outline structure", () => {
    const next = graphReducer(state(), {
      type: "UPDATE_NODE_TEXT",
      nodeId: "b",
      text: "Bravo updated",
    });

    expect(next.nodesById.b.canonicalTextMd).toBe("Bravo updated");
    expect(next.nodesById.root.childrenIds).toEqual(["a", "b", "c"]);
  });

  it("splits a node at the cursor into a new next sibling", () => {
    const next = graphReducer(state(), {
      type: "ENTER_SPLIT",
      nodeId: "b",
      cursorOffset: 2,
    });

    const siblingIds = next.nodesById.root.childrenIds ?? [];
    const insertedId = siblingIds[2];

    expect(next.nodesById.b.canonicalTextMd).toBe("Br");
    expect(next.nodesById[insertedId].canonicalTextMd).toBe("avo");
    expect(siblingIds).toHaveLength(4);
    expect(siblingIds.slice(0, 4)).toEqual(["a", "b", insertedId, "c"]);
  });

  it("indents a node under its previous sibling", () => {
    const next = graphReducer(state(), {
      type: "TAB_INDENT",
      nodeId: "b",
    });

    expect(next.nodesById.root.childrenIds).toEqual(["a", "c"]);
    expect(next.nodesById.a.childrenIds).toEqual(["b"]);
    expect(next.nodesById.a.isExpanded).toBe(true);
  });

  it("outdents a node to sit after its parent", () => {
    const indented = graphReducer(state(), {
      type: "TAB_INDENT",
      nodeId: "b",
    });

    const next = graphReducer(indented, {
      type: "SHIFT_TAB_OUTDENT",
      nodeId: "b",
    });

    expect(next.nodesById.a.childrenIds).toEqual([]);
    expect(next.nodesById.root.childrenIds).toEqual(["a", "b", "c"]);
  });

  it("merges a node into its previous sibling and removes the empty outline item", () => {
    const next = graphReducer(state(), {
      type: "BACKSPACE_MERGE",
      nodeId: "b",
    });

    expect(next.nodesById.a.canonicalTextMd).toBe("AlphaBravo");
    expect(next.nodesById.root.childrenIds).toEqual(["a", "c"]);
    expect(next.nodesById.b).toBeUndefined();
  });

  it("pushes a node onto the focus stack for zoomed outline navigation", () => {
    const next = graphReducer(state(), {
      type: "PUSH_FOCUS",
      nodeId: "b",
    });

    expect(next.focusStack).toEqual(["root", "b"]);
  });

  it("queues the selected projection lens when growing a branch", () => {
    const withLens = graphReducer(state(), {
      type: "SET_PROJECTION_LENS",
      projectionLensId: "research",
    });

    const next = graphReducer(withLens, {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = next.nodesById.b.branchIds?.[0] ?? "";

    expect(next.selectedProjectionLensId).toBe("research");
    expect(next.branchesById[localId].projectionLensId).toBe("research");
    expect(next.syncQueue.at(-1)).toEqual(
      expect.objectContaining({
        type: "CREATE_AI_BRANCH",
        projectionLensId: "research",
      })
    );
  });

  it("clears the selected projection lens without affecting outline state", () => {
    const withLens: LocalGraphState = {
      ...state(),
      selectedProjectionLensId: "research",
    };

    const next = graphReducer(withLens, {
      type: "SET_PROJECTION_LENS",
      projectionLensId: "",
    });

    expect(next.selectedProjectionLensId).toBeUndefined();
    expect(next.nodesById.root.childrenIds).toEqual(["a", "b", "c"]);
  });

  it("attaches contradiction summaries to completed AI branches for reader badges", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";

    const next = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      serverId: "server-branch-1",
      contradictions: [
        {
          id: "contradiction-1",
          type: "ancestor_conflict",
          severity: "medium",
          explanation: "New claim conflicts with your earlier commitment.",
          resolutionStatus: "unresolved",
        },
      ],
    });

    expect(next.branchesById[localId].serverId).toBe("server-branch-1");
    expect(next.branchesById[localId].contradictions).toEqual([
      expect.objectContaining({
        type: "ancestor_conflict",
        severity: "medium",
      }),
    ]);
  });

  it("attaches a consistency report to completed AI branches for reader inspection", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";

    const next = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      serverId: "server-branch-1",
      consistencyReport: {
        reportSource: "model",
        status: "soft_tension",
        summary: "One claim needs review.",
        items: [
          {
            claimId: "claim-1",
            relation: "tension",
            priorClaimId: "prior-1",
            severity: "medium",
            explanation: "The branch qualifies an earlier commitment.",
          },
        ],
      },
    });

    expect(next.branchesById[localId].consistencyReport).toEqual({
      reportSource: "model",
      status: "soft_tension",
      summary: "One claim needs review.",
      items: [
        {
          claimId: "claim-1",
          relation: "tension",
          priorClaimId: "prior-1",
          severity: "medium",
          explanation: "The branch qualifies an earlier commitment.",
        },
      ],
    });
  });

  it("updates a branch contradiction resolution status locally", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const withContradiction = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      contradictions: [
        {
          id: "contradiction-1",
          type: "ancestor_conflict",
          severity: "medium",
          explanation: "New claim conflicts with your earlier commitment.",
          resolutionStatus: "unresolved",
        },
      ],
    });

    const next = graphReducer(withContradiction, {
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId: "contradiction-1",
      resolutionStatus: "dismissed",
    });

    expect(next.branchesById[localId].contradictions?.[0].resolutionStatus).toBe("dismissed");
  });

  it("queues a synthesize-mode branch when resolving a contradiction through synthesis", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const withContradiction = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      contradictions: [
        {
          id: "contradiction-1",
          type: "ancestor_conflict",
          severity: "medium",
          explanation: "New claim conflicts with your earlier commitment.",
          resolutionStatus: "unresolved",
        },
      ],
    });

    const next = graphReducer(withContradiction, {
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId: "contradiction-1",
      resolutionStatus: "synthesized",
    });
    const sourceBranchIds = next.nodesById.b.branchIds ?? [];
    const synthesisBranchId = sourceBranchIds.find((id) => id !== localId);

    expect(next.branchesById[localId].contradictions?.[0].resolutionStatus).toBe("synthesized");
    expect(synthesisBranchId).toBeTruthy();
    expect(next.branchesById[synthesisBranchId ?? ""].status).toBe("queued");
    expect(next.syncQueue.at(-1)).toEqual(
      expect.objectContaining({
        type: "CREATE_AI_BRANCH",
        localId: synthesisBranchId,
        sourceNodeId: "b",
        mode: "synthesize",
        prompt: expect.stringContaining("New claim conflicts"),
        retrievalNodeIds: ["b"],
      })
    );
  });

  it("records fork and revise statuses without queuing another branch", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const withContradiction = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      contradictions: [
        {
          id: "contradiction-1",
          type: "ancestor_conflict",
          severity: "medium",
          explanation: "New claim conflicts with your earlier commitment.",
          resolutionStatus: "unresolved",
        },
      ],
    });

    const forked = graphReducer(withContradiction, {
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId: "contradiction-1",
      resolutionStatus: "forked",
    });
    const revised = graphReducer(withContradiction, {
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId: "contradiction-1",
      resolutionStatus: "revised",
    });

    expect(forked.branchesById[localId].contradictions?.[0].resolutionStatus).toBe("forked");
    expect(revised.branchesById[localId].contradictions?.[0].resolutionStatus).toBe("revised");
    expect(forked.syncQueue).toHaveLength(withContradiction.syncQueue.length);
    expect(revised.syncQueue).toHaveLength(withContradiction.syncQueue.length);
  });

  it("opens a revision draft when a contradiction is marked revised", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const withOutput = graphReducer(withBranch, {
      type: "BRANCH_GENERATION_CHUNK",
      localId,
      chunk: "Original branch output.",
    });
    const withContradiction = graphReducer(withOutput, {
      type: "BRANCH_GENERATION_COMPLETE",
      localId,
      contradictions: [
        {
          id: "contradiction-1",
          type: "ancestor_conflict",
          severity: "medium",
          explanation: "New claim conflicts with your earlier commitment.",
          resolutionStatus: "unresolved",
        },
      ],
    });

    const next = graphReducer(withContradiction, {
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId: "contradiction-1",
      resolutionStatus: "revised",
    });

    expect(next.branchesById[localId].revisionStatus).toBe("editing");
    expect(next.branchesById[localId].revisionDraftMd).toBe("Original branch output.");
  });

  it("commits an inline branch revision into branch output", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const editing = graphReducer(withBranch, {
      type: "START_BRANCH_REVISION",
      localId,
    });
    const drafted = graphReducer(editing, {
      type: "UPDATE_BRANCH_REVISION_DRAFT",
      localId,
      outputMd: "Edited branch output.",
    });

    const next = graphReducer(drafted, {
      type: "COMMIT_BRANCH_REVISION",
      localId,
      outputMd: "Edited branch output.",
    });

    expect(next.branchesById[localId].outputMd).toBe("Edited branch output.");
    expect(next.branchesById[localId].revisionStatus).toBe("saved");
    expect(next.branchesById[localId].revisionDraftMd).toBeUndefined();
  });

  it("clears acted-on revision-request feedback after saving branch edits", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const revisionRequested = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_REVIEWED",
      localId,
      decision: "revise",
      reviewFeedback: "Narrow the branch claim before canon promotion.",
    });
    const editing = graphReducer(revisionRequested, {
      type: "START_BRANCH_REVISION",
      localId,
    });

    const next = graphReducer(editing, {
      type: "COMMIT_BRANCH_REVISION",
      localId,
      outputMd: "Edited branch output.",
    });

    expect(next.branchesById[localId].outputMd).toBe("Edited branch output.");
    expect(next.branchesById[localId].revisionStatus).toBe("saved");
    expect(next.branchesById[localId].reviewStatus).toBeUndefined();
    expect(next.branchesById[localId].reviewFeedback).toBeUndefined();
    expect(next.branchesById[localId].consistencyStatus).toBe("unchecked");
    expect(next.branchesById[localId].consistencyReport).toBeUndefined();
  });

  it("records refreshed branch consistency reports after an explicit recheck", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const unchecked = graphReducer(withBranch, {
      type: "COMMIT_BRANCH_REVISION",
      localId,
      outputMd: "- [asserted] scope: revised claim",
    });

    const next = graphReducer(unchecked, {
      type: "MARK_BRANCH_CONSISTENCY_CHECKED",
      localId,
      contradictions: [],
      consistencyReport: {
        reportSource: "model",
        status: "consistent",
        summary: "Edited branch is compatible with the active constitution.",
        items: [],
      },
    });

    expect(next.branchesById[localId].consistencyStatus).toBe("consistent");
    expect(next.branchesById[localId].consistencyReport).toEqual({
      reportSource: "model",
      status: "consistent",
      summary: "Edited branch is compatible with the active constitution.",
      items: [],
    });
    expect(next.branchesById[localId].contradictions).toEqual([]);
    expect(next.branchesById[localId].proposalError).toBeUndefined();
  });

  it("records consistency-check progress and failures on unchecked branches", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const unchecked = graphReducer(withBranch, {
      type: "COMMIT_BRANCH_REVISION",
      localId,
      outputMd: "- [asserted] scope: revised claim",
    });

    const checking = graphReducer(unchecked, {
      type: "MARK_BRANCH_CONSISTENCY_CHECKING",
      localId,
    });
    const failed = graphReducer(checking, {
      type: "MARK_BRANCH_CONSISTENCY_CHECK_FAILED",
      localId,
      error: "consistency_recheck_failed",
    });

    expect(checking.branchesById[localId].consistencyCheckStatus).toBe("checking");
    expect(checking.branchesById[localId].consistencyCheckError).toBeUndefined();
    expect(failed.branchesById[localId].consistencyStatus).toBe("unchecked");
    expect(failed.branchesById[localId].consistencyCheckStatus).toBe("failed");
    expect(failed.branchesById[localId].consistencyCheckError).toBe("consistency_recheck_failed");
  });

  it("marks a branch as proposed canon after server acceptance", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";

    const next = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_PROPOSED",
      localId,
    });

    expect(next.branchesById[localId].visibility).toBe("proposed_canon");
    expect(next.branchesById[localId].proposalStatus).toBe("submitted");
    expect(next.branchesById[localId].proposalError).toBeUndefined();
  });

  it("records stale-source canon proposal failures without mutating branch visibility", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";

    const next = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_PROPOSAL_FAILED",
      localId,
      error: "stale_source_version",
    });

    expect(next.branchesById[localId].visibility).toBeUndefined();
    expect(next.branchesById[localId].proposalStatus).toBe("conflict");
    expect(next.branchesById[localId].proposalError).toBe("stale_source_version");
  });

  it("records accepted canon reviews on proposed branches", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const proposed = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_PROPOSED",
      localId,
    });

    const next = graphReducer(proposed, {
      type: "MARK_BRANCH_CANON_REVIEWED",
      localId,
      decision: "accept",
    });

    expect(next.branchesById[localId].visibility).toBe("accepted_canon");
    expect(next.branchesById[localId].reviewStatus).toBe("accepted");
    expect(next.branchesById[localId].proposalStatus).toBeUndefined();
  });

  it("records rejected canon reviews without deleting the private branch", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const proposed = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_PROPOSED",
      localId,
    });

    const next = graphReducer(proposed, {
      type: "MARK_BRANCH_CANON_REVIEWED",
      localId,
      decision: "reject",
    });

    expect(next.branchesById[localId].visibility).toBe("private");
    expect(next.branchesById[localId].reviewStatus).toBe("rejected");
    expect(next.branchesById[localId].proposalStatus).toBeUndefined();
    expect(next.branchesById[localId].outputMd).toBe("");
  });

  it("records revision-requested canon reviews without leaving stale proposed state", () => {
    const withBranch = graphReducer(state(), {
      type: "LONG_PRESS_NODE",
      nodeId: "b",
    });
    const localId = withBranch.nodesById.b.branchIds?.[0] ?? "";
    const proposed = graphReducer(withBranch, {
      type: "MARK_BRANCH_CANON_PROPOSED",
      localId,
    });

    const next = graphReducer(proposed, {
      type: "MARK_BRANCH_CANON_REVIEWED",
      localId,
      decision: "revise",
      reviewFeedback: "Narrow the claim before proposing it again.",
    });

    expect(next.branchesById[localId].visibility).toBe("private");
    expect(next.branchesById[localId].reviewStatus).toBe("revision_requested");
    expect(next.branchesById[localId].reviewFeedback).toBe("Narrow the claim before proposing it again.");
    expect(next.branchesById[localId].proposalStatus).toBeUndefined();
  });

  it("hydrates server branches onto their source nodes without duplicating branch ids", () => {
    const next = graphReducer(state(), {
      type: "HYDRATE_SERVER_BRANCHES",
      branches: [
        {
          localId: "server:branch-1",
          serverId: "branch-1",
          sourceNodeId: "b",
          sourceVersionHash: "hash-1",
          status: "complete",
          outputMd: "Persisted branch.",
          depth: 1,
          reviewStatus: "revision_requested",
          reviewFeedback: "Tighten this branch before canon proposal.",
          contradictions: [
            {
              id: "contradiction-1",
              type: "ancestor_conflict",
              severity: "medium",
              explanation: "New claim conflicts with your earlier commitment.",
              resolutionStatus: "unresolved",
            },
          ],
        },
      ],
    });

    const again = graphReducer(next, {
      type: "HYDRATE_SERVER_BRANCHES",
      branches: [next.branchesById["server:branch-1"]],
    });

    expect(next.branchesById["server:branch-1"].outputMd).toBe("Persisted branch.");
    expect(next.branchesById["server:branch-1"].reviewStatus).toBe("revision_requested");
    expect(next.branchesById["server:branch-1"].reviewFeedback).toBe("Tighten this branch before canon proposal.");
    expect(next.nodesById.b.branchIds).toEqual(["server:branch-1"]);
    expect(again.nodesById.b.branchIds).toEqual(["server:branch-1"]);
  });

  it("sets the focus stack from a breadcrumb path", () => {
    const next = graphReducer(state(), {
      type: "SET_FOCUS_STACK",
      nodeIds: ["root", "a"],
    });

    expect(next.focusStack).toEqual(["root", "a"]);
  });

  it("hydrates current user permissions for capability-aware controls", () => {
    const next = graphReducer(state(), {
      type: "HYDRATE_CURRENT_USER",
      user: {
        id: "reviewer-1",
        role: "canon_reviewer",
        canReviewCanon: true,
        canAssignRoles: false,
      },
    });

    expect(next.currentUser).toEqual({
      id: "reviewer-1",
      role: "canon_reviewer",
      canReviewCanon: true,
      canAssignRoles: false,
    });
  });

  it("records successful role assignments and refreshes current user capabilities when self-assigned", () => {
    const withUser = graphReducer(state(), {
      type: "HYDRATE_CURRENT_USER",
      user: {
        id: "reviewer-1",
        role: "canon_reviewer",
        canReviewCanon: true,
        canAssignRoles: false,
      },
    });

    const next = graphReducer(withUser, {
      type: "MARK_USER_ROLE_ASSIGNED",
      userId: "reviewer-1",
      role: "admin",
    });

    expect(next.roleAssignmentStatus).toBe("saved");
    expect(next.roleAssignmentError).toBeUndefined();
    expect(next.currentUser).toEqual({
      id: "reviewer-1",
      role: "admin",
      canReviewCanon: true,
      canAssignRoles: true,
    });
  });

  it("records role assignment failures without changing current permissions", () => {
    const withUser = graphReducer(state(), {
      type: "HYDRATE_CURRENT_USER",
      user: {
        id: "admin-1",
        role: "admin",
        canReviewCanon: true,
        canAssignRoles: true,
      },
    });

    const next = graphReducer(withUser, {
      type: "MARK_USER_ROLE_ASSIGNMENT_FAILED",
      error: "admin_required",
    });

    expect(next.roleAssignmentStatus).toBe("failed");
    expect(next.roleAssignmentError).toBe("admin_required");
    expect(next.currentUser).toEqual(withUser.currentUser);
  });

  it("hydrates role assignment user candidates", () => {
    const next = graphReducer(state(), {
      type: "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES",
      users: [
        { id: "user-1", email: "reader@example.com", role: "reader" },
        { id: "reviewer-1", email: "reviewer@example.com", role: "canon_reviewer" },
      ],
    });

    expect(next.roleAssignmentCandidates).toEqual([
      { id: "user-1", email: "reader@example.com", role: "reader" },
      { id: "reviewer-1", email: "reviewer@example.com", role: "canon_reviewer" },
    ]);
    expect(next.userLookupStatus).toBe("loaded");
    expect(next.userLookupError).toBeUndefined();
  });

  it("records user lookup failures without clearing previous candidates", () => {
    const withCandidates = graphReducer(state(), {
      type: "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES",
      users: [
        { id: "user-1", email: "reader@example.com", role: "reader" },
      ],
    });

    const next = graphReducer(withCandidates, {
      type: "MARK_USER_LOOKUP_FAILED",
      error: "admin_required",
    });

    expect(next.roleAssignmentCandidates).toEqual(withCandidates.roleAssignmentCandidates);
    expect(next.userLookupStatus).toBe("failed");
    expect(next.userLookupError).toBe("admin_required");
  });

  it("hydrates role assignment audit history", () => {
    const next = graphReducer(state(), {
      type: "HYDRATE_ROLE_ASSIGNMENT_AUDITS",
      nextCursor: "audit-1",
      audits: [
        {
          id: "audit-1",
          targetUserId: "user-2",
          targetUserEmail: "target@example.com",
          actorUserId: "admin-1",
          actorUserEmail: "admin@example.com",
          fromRole: "reader",
          toRole: "canon_reviewer",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    expect(next.roleAssignmentAudits).toEqual([
      {
        id: "audit-1",
        targetUserId: "user-2",
        targetUserEmail: "target@example.com",
        actorUserId: "admin-1",
        actorUserEmail: "admin@example.com",
        fromRole: "reader",
        toRole: "canon_reviewer",
        createdAt: "2026-05-31T00:00:00.000Z",
      },
    ]);
    expect(next.roleAuditStatus).toBe("loaded");
    expect(next.roleAuditNextCursor).toBe("audit-1");
  });

  it("appends additional role assignment audit pages", () => {
    const firstPage = graphReducer(state(), {
      type: "HYDRATE_ROLE_ASSIGNMENT_AUDITS",
      nextCursor: "audit-1",
      audits: [
        {
          id: "audit-1",
          targetUserId: "user-2",
          actorUserId: "admin-1",
          fromRole: "reader",
          toRole: "canon_reviewer",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(firstPage, {
      type: "HYDRATE_ROLE_ASSIGNMENT_AUDITS",
      append: true,
      nextCursor: undefined,
      audits: [
        {
          id: "audit-2",
          targetUserId: "user-3",
          actorUserId: "admin-1",
          fromRole: "canon_reviewer",
          toRole: "reader",
          createdAt: "2026-05-30T00:00:00.000Z",
        },
      ],
    });

    expect(next.roleAssignmentAudits?.map((audit) => audit.id)).toEqual(["audit-1", "audit-2"]);
    expect(next.roleAuditNextCursor).toBeUndefined();
  });

  it("hydrates canon review audit history", () => {
    const next = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_AUDITS",
      nextCursor: "review-1",
      reviews: [
        {
          id: "review-1",
          branchId: "branch-1",
          branchSourceNodeId: "node-1",
          branchSourceLabel: "The Point",
          reviewerId: "reviewer-1",
          reviewerEmail: "reviewer@example.com",
          decision: "accept",
          notes: "Clean synthesis.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    expect(next.canonReviewAudits).toEqual([
      {
        id: "review-1",
        branchId: "branch-1",
        branchSourceNodeId: "node-1",
        branchSourceLabel: "The Point",
        reviewerId: "reviewer-1",
        reviewerEmail: "reviewer@example.com",
        decision: "accept",
        notes: "Clean synthesis.",
        createdAt: "2026-05-31T00:00:00.000Z",
      },
    ]);
    expect(next.canonReviewAuditStatus).toBe("loaded");
    expect(next.canonReviewAuditError).toBeUndefined();
    expect(next.canonReviewAuditNextCursor).toBe("review-1");
  });

  it("appends additional canon review audit pages", () => {
    const firstPage = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_AUDITS",
      nextCursor: "review-1",
      reviews: [
        {
          id: "review-1",
          branchId: "branch-1",
          reviewerId: "reviewer-1",
          decision: "accept",
          notes: null,
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(firstPage, {
      type: "HYDRATE_CANON_REVIEW_AUDITS",
      append: true,
      nextCursor: undefined,
      reviews: [
        {
          id: "review-2",
          branchId: "branch-2",
          reviewerId: "reviewer-1",
          decision: "revise",
          notes: "Needs narrower claim.",
          createdAt: "2026-05-30T00:00:00.000Z",
        },
      ],
    });

    expect(next.canonReviewAudits?.map((review) => review.id)).toEqual(["review-1", "review-2"]);
    expect(next.canonReviewAuditNextCursor).toBeUndefined();
  });

  it("hydrates pending canon review queue pages", () => {
    const firstPage = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_QUEUE",
      nextCursor: "branch-1",
      branches: [
        {
          id: "branch-1",
          authorId: "author-1",
          authorEmail: "author@example.com",
          sourceNodeId: "node-1",
          sourceLabel: "The Point",
          sourceVersionHash: "hash-1",
          currentVersionHash: "hash-1",
          isStaleSource: false,
          outputPreview: "Proposed canon text.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(firstPage, {
      type: "HYDRATE_CANON_REVIEW_QUEUE",
      append: true,
      nextCursor: undefined,
      branches: [
        {
          id: "branch-2",
          authorId: "author-2",
          authorEmail: null,
          sourceNodeId: "node-2",
          sourceLabel: "Another Point",
          sourceVersionHash: "old-hash",
          currentVersionHash: "new-hash",
          isStaleSource: true,
          outputPreview: "Stale proposal.",
          createdAt: "2026-05-30T00:00:00.000Z",
        },
      ],
    });

    expect(next.canonReviewQueue?.map((branch) => branch.id)).toEqual(["branch-1", "branch-2"]);
    expect(next.canonReviewQueueStatus).toBe("loaded");
    expect(next.canonReviewQueueNextCursor).toBeUndefined();
  });

  it("records pending review queue lookup failures without clearing previous queue items", () => {
    const withQueue = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_QUEUE",
      branches: [
        {
          id: "branch-1",
          authorId: "author-1",
          authorEmail: "author@example.com",
          sourceNodeId: "node-1",
          sourceLabel: "The Point",
          sourceVersionHash: "hash-1",
          currentVersionHash: "hash-1",
          isStaleSource: false,
          outputPreview: "Proposed canon text.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(withQueue, {
      type: "MARK_CANON_REVIEW_QUEUE_LOOKUP_FAILED",
      error: "canon_reviewer_required",
    });

    expect(next.canonReviewQueue).toEqual(withQueue.canonReviewQueue);
    expect(next.canonReviewQueueStatus).toBe("failed");
    expect(next.canonReviewQueueError).toBe("canon_reviewer_required");
  });

  it("removes a pending review queue item after a successful queue review action", () => {
    const withQueue = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_QUEUE",
      branches: [
        {
          id: "branch-1",
          authorId: "author-1",
          authorEmail: "author@example.com",
          sourceNodeId: "node-1",
          sourceLabel: "The Point",
          sourceVersionHash: "hash-1",
          currentVersionHash: "hash-1",
          isStaleSource: false,
          outputPreview: "Proposed canon text.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
        {
          id: "branch-2",
          authorId: "author-2",
          authorEmail: null,
          sourceNodeId: "node-2",
          sourceLabel: "Another Point",
          sourceVersionHash: "hash-2",
          currentVersionHash: "hash-2",
          isStaleSource: false,
          outputPreview: "Another proposal.",
          createdAt: "2026-05-31T00:01:00.000Z",
        },
      ],
    });

    const next = graphReducer(withQueue, {
      type: "MARK_CANON_REVIEW_QUEUE_ITEM_REVIEWED",
      branchId: "branch-1",
      decision: "accept",
    });

    expect(next.canonReviewQueue?.map((branch) => branch.id)).toEqual(["branch-2"]);
  });

  it("records pending review queue action failures without removing the item", () => {
    const withQueue = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_QUEUE",
      branches: [
        {
          id: "branch-1",
          authorId: "author-1",
          authorEmail: "author@example.com",
          sourceNodeId: "node-1",
          sourceLabel: "The Point",
          sourceVersionHash: "old-hash",
          currentVersionHash: "new-hash",
          isStaleSource: true,
          outputPreview: "Stale proposal.",
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(withQueue, {
      type: "MARK_CANON_REVIEW_QUEUE_ITEM_FAILED",
      branchId: "branch-1",
      error: "stale_source_version",
    });

    expect(next.canonReviewQueue).toEqual([
      {
        ...withQueue.canonReviewQueue?.[0],
        actionStatus: "failed",
        actionError: "stale_source_version",
      },
    ]);
  });

  it("records canon review audit lookup failures without clearing previous reviews", () => {
    const withReviews = graphReducer(state(), {
      type: "HYDRATE_CANON_REVIEW_AUDITS",
      reviews: [
        {
          id: "review-1",
          branchId: "branch-1",
          reviewerId: "reviewer-1",
          decision: "reject",
          notes: null,
          createdAt: "2026-05-31T00:00:00.000Z",
        },
      ],
    });

    const next = graphReducer(withReviews, {
      type: "MARK_CANON_REVIEW_AUDIT_LOOKUP_FAILED",
      error: "canon_reviewer_required",
    });

    expect(next.canonReviewAudits).toEqual(withReviews.canonReviewAudits);
    expect(next.canonReviewAuditStatus).toBe("failed");
    expect(next.canonReviewAuditError).toBe("canon_reviewer_required");
  });
});

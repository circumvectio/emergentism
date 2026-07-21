"use client";

import { useMemo, useState } from "react";
import { ChevronRight, Search, Share2, Star, UserCog } from "lucide-react";
import { OutlinerNode } from "./Node";
import { useGraphStore } from "@/lib/store";

interface OutlineViewportProps {
  rootNodeId: string;
  projectionLensOptions?: Array<{
    id: string;
    label: string;
  }>;
}

export function OutlineViewport({ rootNodeId, projectionLensOptions = [] }: OutlineViewportProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [rolesOpen, setRolesOpen] = useState(false);
  const [userLookupQuery, setUserLookupQuery] = useState("");
  const [targetUserId, setTargetUserId] = useState("");
  const [targetRole, setTargetRole] = useState<"reader" | "canon_reviewer" | "admin">("canon_reviewer");
  const [roleAuditTargetFilter, setRoleAuditTargetFilter] = useState("");
  const [roleAuditActorFilter, setRoleAuditActorFilter] = useState("");
  const [canonReviewQueueQueryFilter, setCanonReviewQueueQueryFilter] = useState("");
  const [canonReviewQueueConsistencyFilter, setCanonReviewQueueConsistencyFilter] = useState("");
  const [canonReviewQueryFilter, setCanonReviewQueryFilter] = useState("");
  const [canonReviewBranchFilter, setCanonReviewBranchFilter] = useState("");
  const [canonReviewReviewerFilter, setCanonReviewReviewerFilter] = useState("");
  const [canonReviewDecisionFilter, setCanonReviewDecisionFilter] = useState<
    "" | "accept" | "reject" | "revise"
  >("");
  const focusStack = useGraphStore((state) => state.focusStack);
  const nodesById = useGraphStore((state) => state.nodesById);
  const currentUser = useGraphStore((state) => state.currentUser);
  const roleAssignmentStatus = useGraphStore((state) => state.roleAssignmentStatus);
  const roleAssignmentError = useGraphStore((state) => state.roleAssignmentError);
  const roleAssignmentCandidates = useGraphStore((state) => state.roleAssignmentCandidates ?? []);
  const userLookupStatus = useGraphStore((state) => state.userLookupStatus);
  const userLookupError = useGraphStore((state) => state.userLookupError);
  const roleAssignmentAudits = useGraphStore((state) => state.roleAssignmentAudits ?? []);
  const roleAuditStatus = useGraphStore((state) => state.roleAuditStatus);
  const roleAuditError = useGraphStore((state) => state.roleAuditError);
  const roleAuditNextCursor = useGraphStore((state) => state.roleAuditNextCursor);
  const canonReviewAudits = useGraphStore((state) => state.canonReviewAudits ?? []);
  const canonReviewAuditStatus = useGraphStore((state) => state.canonReviewAuditStatus);
  const canonReviewAuditError = useGraphStore((state) => state.canonReviewAuditError);
  const canonReviewAuditNextCursor = useGraphStore((state) => state.canonReviewAuditNextCursor);
  const canonReviewQueue = useGraphStore((state) => state.canonReviewQueue ?? []);
  const canonReviewQueueStatus = useGraphStore((state) => state.canonReviewQueueStatus);
  const canonReviewQueueError = useGraphStore((state) => state.canonReviewQueueError);
  const canonReviewQueueNextCursor = useGraphStore((state) => state.canonReviewQueueNextCursor);
  const selectedProjectionLensId = useGraphStore((state) => state.selectedProjectionLensId ?? "");
  const dispatch = useGraphStore((state) => state.dispatch);
  const visibleFocusStack = useMemo(() => {
    // Drop the "root" sentinel + dupes; always anchor the trail at the chapter
    // root ("Home") so you can zoom back out via the breadcrumb, not only Alt-←.
    const path = focusStack.filter((id) => nodesById[id] && id !== rootNodeId);
    const rooted = nodesById[rootNodeId] ? [rootNodeId, ...path] : path;
    return rooted.length > 0 ? rooted : [rootNodeId].filter((id) => nodesById[id]);
  }, [focusStack, nodesById, rootNodeId]);
  const focusedNodeId = visibleFocusStack[visibleFocusStack.length - 1] ?? rootNodeId;
  const focusedNode = nodesById[focusedNodeId] ? focusedNodeId : rootNodeId;
  const bookRootNode = nodesById[rootNodeId];
  const sideNavItems = useMemo(
    () =>
      (nodesById[rootNodeId]?.childrenIds ?? [])
        .map((id) => nodesById[id])
        .filter(Boolean),
    [nodesById, rootNodeId]
  );
  const focusedRootChildId = visibleFocusStack.length > 1 ? visibleFocusStack[1] : null;
  const canAssignRoles = currentUser?.canAssignRoles ?? false;
  const canReviewCanon = currentUser?.canReviewCanon ?? false;
  const canOpenReviewPanel = canAssignRoles || canReviewCanon;

  const lookupUsers = async () => {
    const query = userLookupQuery.trim();
    if (!query) {
      dispatch({ type: "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES", users: [] });
      return;
    }

    const response = await fetch(`/api/users?query=${encodeURIComponent(query)}`);
    if (response.ok) {
      const payload = await response.json();
      dispatch({
        type: "HYDRATE_ROLE_ASSIGNMENT_CANDIDATES",
        users: Array.isArray(payload.users) ? payload.users : [],
      });
      return;
    }

    let error = "user_lookup_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({ type: "MARK_USER_LOOKUP_FAILED", error });
  };

  const assignRole = async () => {
    const userId = targetUserId.trim();
    if (!userId) return;

    const response = await fetch(`/api/users/${encodeURIComponent(userId)}/role`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: targetRole }),
    });
    if (response.ok) {
      dispatch({ type: "MARK_USER_ROLE_ASSIGNED", userId, role: targetRole });
      void loadRoleAudits();
      return;
    }

    let error = "role_assignment_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({ type: "MARK_USER_ROLE_ASSIGNMENT_FAILED", error });
  };

  const loadRoleAudits = async (append = false) => {
    const params = new URLSearchParams();
    const targetUserIdFilter = roleAuditTargetFilter.trim();
    const actorUserIdFilter = roleAuditActorFilter.trim();
    if (targetUserIdFilter) params.set("targetUserId", targetUserIdFilter);
    if (actorUserIdFilter) params.set("actorUserId", actorUserIdFilter);
    if (append && roleAuditNextCursor) params.set("cursor", roleAuditNextCursor);
    const query = params.toString();
    const response = await fetch(`/api/users/role-audits${query ? `?${query}` : ""}`);
    if (response.ok) {
      const payload = await response.json();
      dispatch({
        type: "HYDRATE_ROLE_ASSIGNMENT_AUDITS",
        audits: Array.isArray(payload.audits) ? payload.audits : [],
        append,
        nextCursor: typeof payload.nextCursor === "string" ? payload.nextCursor : undefined,
      });
      return;
    }

    let error = "role_audit_lookup_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({ type: "MARK_ROLE_AUDIT_LOOKUP_FAILED", error });
  };

  const loadCanonReviewAudits = async (append = false) => {
    const params = new URLSearchParams();
    const queryFilter = canonReviewQueryFilter.trim();
    const branchId = canonReviewBranchFilter.trim();
    const reviewerId = canonReviewReviewerFilter.trim();
    if (queryFilter) params.set("q", queryFilter);
    if (branchId) params.set("branchId", branchId);
    if (reviewerId) params.set("reviewerId", reviewerId);
    if (canonReviewDecisionFilter) params.set("decision", canonReviewDecisionFilter);
    if (append && canonReviewAuditNextCursor) params.set("cursor", canonReviewAuditNextCursor);
    const query = params.toString();
    const response = await fetch(`/api/branches/reviews${query ? `?${query}` : ""}`);
    if (response.ok) {
      const payload = await response.json();
      dispatch({
        type: "HYDRATE_CANON_REVIEW_AUDITS",
        reviews: Array.isArray(payload.reviews) ? payload.reviews : [],
        append,
        nextCursor: typeof payload.nextCursor === "string" ? payload.nextCursor : undefined,
      });
      return;
    }

    let error = "canon_review_audit_lookup_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({ type: "MARK_CANON_REVIEW_AUDIT_LOOKUP_FAILED", error });
  };

  const loadCanonReviewQueue = async (append = false) => {
    const params = new URLSearchParams();
    const queryFilter = canonReviewQueueQueryFilter.trim();
    if (canonReviewQueueConsistencyFilter) params.set("consistency", canonReviewQueueConsistencyFilter);
    if (queryFilter) params.set("q", queryFilter);
    if (append && canonReviewQueueNextCursor) params.set("cursor", canonReviewQueueNextCursor);
    const query = params.toString();
    const response = await fetch(`/api/branches/review-queue${query ? `?${query}` : ""}`);
    if (response.ok) {
      const payload = await response.json();
      dispatch({
        type: "HYDRATE_CANON_REVIEW_QUEUE",
        branches: Array.isArray(payload.branches) ? payload.branches : [],
        append,
        nextCursor: typeof payload.nextCursor === "string" ? payload.nextCursor : undefined,
      });
      return;
    }

    let error = "canon_review_queue_lookup_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({ type: "MARK_CANON_REVIEW_QUEUE_LOOKUP_FAILED", error });
  };

  const reviewQueuedBranch = async (
    branchId: string,
    decision: "accept" | "reject" | "revise"
  ) => {
    const response = await fetch(`/api/branches/${encodeURIComponent(branchId)}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision }),
    });

    if (response.ok) {
      dispatch({
        type: "MARK_CANON_REVIEW_QUEUE_ITEM_REVIEWED",
        branchId,
        decision,
      });
      void loadCanonReviewAudits();
      return;
    }

    let error = "review_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep generic failure state.
    }

    dispatch({
      type: "MARK_CANON_REVIEW_QUEUE_ITEM_FAILED",
      branchId,
      error,
    });
  };

  return (
    <section className="min-h-screen bg-white text-[#222]">
      <header className="sticky top-0 z-20 flex h-11 items-center gap-2 border-b border-[#e3e3e3] bg-white px-3 text-[13px] text-[#555]">
        <nav className="flex min-w-0 flex-1 items-center gap-1 overflow-hidden">
          {visibleFocusStack.map((id, index) => {
            const path = visibleFocusStack.slice(0, index + 1);
            const label = nodesById[id]?.canonicalTextMd || "Home";
            return (
              <div key={`${id}-${index}`} className="flex min-w-0 items-center gap-1">
                {index > 0 && <ChevronRight className="h-3.5 w-3.5 shrink-0 text-[#aaa]" />}
                <button
                  type="button"
                  className="max-w-[220px] truncate rounded-sm px-1.5 py-1 text-left hover:bg-[#f0f0f0] hover:text-[#111]"
                  onClick={() => dispatch({ type: "SET_FOCUS_STACK", nodeIds: path })}
                >
                  {label}
                </button>
              </div>
            );
          })}
        </nav>

        <label className="hidden h-7 w-56 items-center gap-2 rounded-sm border border-[#ddd] bg-[#fafafa] px-2 text-[#777] lg:flex">
          <Search className="h-3.5 w-3.5 shrink-0" />
          <input
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            className="min-w-0 flex-1 bg-transparent text-[13px] text-[#222] outline-none placeholder:text-[#999]"
            placeholder="Search"
          />
        </label>

        {projectionLensOptions.length > 0 ? (
          <select
            aria-label="Projection lens"
            value={selectedProjectionLensId}
            onChange={(event) =>
              dispatch({
                type: "SET_PROJECTION_LENS",
                projectionLensId: event.currentTarget.value,
              })
            }
            className="hidden h-7 max-w-36 rounded-sm border border-[#ddd] bg-white px-2 text-[12px] text-[#555] outline-none hover:border-[#bbb] focus:border-[#aaa] md:block"
          >
            <option value="">No lens</option>
            {projectionLensOptions.map((lens) => (
              <option key={lens.id} value={lens.id}>
                {lens.label}
              </option>
            ))}
          </select>
        ) : null}

        <button
          type="button"
          aria-label="Star"
          title="Star"
          className="flex h-7 w-7 items-center justify-center rounded-sm text-[#777] hover:bg-[#f0f0f0] hover:text-[#222]"
        >
          <Star className="h-3.5 w-3.5" />
        </button>
        <button
          type="button"
          className="flex h-7 items-center gap-1 rounded-sm border border-[#ddd] px-2 text-[#555] hover:border-[#bbb] hover:bg-[#f7f7f7] hover:text-[#222]"
        >
          <Share2 className="h-3.5 w-3.5" />
          Share
        </button>
        {canOpenReviewPanel ? (
          <div className="relative">
            <button
              type="button"
              className="flex h-7 items-center gap-1 rounded-sm border border-[#ddd] px-2 text-[#555] hover:border-[#bbb] hover:bg-[#f7f7f7] hover:text-[#222]"
              onClick={() => setRolesOpen((open) => !open)}
              onMouseDown={() => {
                if (!rolesOpen) {
                  if (canAssignRoles) void loadRoleAudits();
                  if (canReviewCanon) {
                    void loadCanonReviewQueue();
                    void loadCanonReviewAudits();
                  }
                }
              }}
            >
              <UserCog className="h-3.5 w-3.5" />
              {canAssignRoles ? "Roles" : "Reviews"}
            </button>
            {rolesOpen ? (
              <div className="absolute right-0 top-9 z-30 w-80 rounded-sm border border-[#ddd] bg-white p-3 text-[12px] shadow-sm">
                {canAssignRoles ? (
                  <>
                    <div className="mb-2 font-medium text-[#333]">Assign role</div>
                    <div className="mb-2 flex gap-2">
                      <input
                        value={userLookupQuery}
                        onChange={(event) => setUserLookupQuery(event.target.value)}
                        className="h-8 min-w-0 flex-1 rounded-sm border border-[#ddd] px-2 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Search users"
                      />
                      <button
                        type="button"
                        className="h-8 rounded-sm border border-[#ccc] px-2 text-[#333] hover:bg-[#f5f5f5]"
                        onClick={lookupUsers}
                      >
                        Find
                      </button>
                    </div>
                    {roleAssignmentCandidates.length > 0 ? (
                      <div className="mb-2 max-h-32 overflow-y-auto border-y border-[#eee] py-1">
                        {roleAssignmentCandidates.map((user) => (
                          <button
                            key={user.id}
                            type="button"
                            className="block w-full rounded-sm px-1.5 py-1 text-left hover:bg-[#f3f3f3]"
                            onClick={() => {
                              setTargetUserId(user.id);
                              setTargetRole(user.role);
                            }}
                          >
                            <span className="block truncate text-[#333]">{user.email}</span>
                            <span className="block truncate text-[11px] text-[#777]">
                              {user.id} · {user.role}
                            </span>
                          </button>
                        ))}
                      </div>
                    ) : null}
                    {userLookupStatus === "loaded" && roleAssignmentCandidates.length === 0 ? (
                      <div className="mb-2 text-[#777]">No users found</div>
                    ) : null}
                    {userLookupStatus === "failed" ? (
                      <div className="mb-2 text-red-700">{userLookupError ?? "User lookup failed"}</div>
                    ) : null}
                    <input
                      value={targetUserId}
                      onChange={(event) => setTargetUserId(event.target.value)}
                      className="mb-2 h-8 w-full rounded-sm border border-[#ddd] px-2 text-[#222] outline-none focus:border-[#aaa]"
                      placeholder="Clerk user ID"
                    />
                    <div className="flex gap-2">
                      <select
                        value={targetRole}
                        onChange={(event) =>
                          setTargetRole(event.target.value as "reader" | "canon_reviewer" | "admin")
                        }
                        className="h-8 min-w-0 flex-1 rounded-sm border border-[#ddd] bg-white px-2 text-[#222] outline-none focus:border-[#aaa]"
                      >
                        <option value="canon_reviewer">canon_reviewer</option>
                        <option value="reader">reader</option>
                        <option value="admin">admin</option>
                      </select>
                      <button
                        type="button"
                        className="h-8 rounded-sm border border-[#ccc] px-2 text-[#333] hover:bg-[#f5f5f5]"
                        onClick={assignRole}
                      >
                        Save
                      </button>
                    </div>
                    {roleAssignmentStatus === "saved" ? (
                      <div className="mt-2 text-[#4a7a4a]">Role saved</div>
                    ) : null}
                    {roleAssignmentStatus === "failed" ? (
                      <div className="mt-2 text-red-700">{roleAssignmentError ?? "Role assignment failed"}</div>
                    ) : null}
                  </>
                ) : null}
                {canAssignRoles ? (
                  <div className="mt-3 border-t border-[#eee] pt-2">
                    <div className="mb-1 flex items-center justify-between">
                      <span className="font-medium text-[#333]">Recent role changes</span>
                      <button
                        type="button"
                        className="rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadRoleAudits()}
                      >
                        Refresh
                      </button>
                    </div>
                    <div className="mb-2 grid grid-cols-2 gap-1.5">
                      <input
                        value={roleAuditTargetFilter}
                        onChange={(event) => setRoleAuditTargetFilter(event.target.value)}
                        className="h-7 rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Target user"
                      />
                      <input
                        value={roleAuditActorFilter}
                        onChange={(event) => setRoleAuditActorFilter(event.target.value)}
                        className="h-7 rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Actor user"
                      />
                    </div>
                    {roleAssignmentAudits.length > 0 ? (
                      <div className="max-h-32 overflow-y-auto">
                        {roleAssignmentAudits.map((audit) => (
                          <div key={audit.id} className="border-t border-[#f1f1f1] py-1 first:border-t-0">
                            <div className="truncate text-[#333]">
                              {audit.targetUserEmail ?? audit.targetUserId}
                            </div>
                            <div className="truncate text-[11px] text-[#777]">
                              {audit.fromRole} → {audit.toRole} by {audit.actorUserEmail ?? audit.actorUserId}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : roleAuditStatus === "loaded" ? (
                      <div className="text-[#777]">No role changes yet</div>
                    ) : null}
                    {roleAuditNextCursor ? (
                      <button
                        type="button"
                        className="mt-1 rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadRoleAudits(true)}
                      >
                        More
                      </button>
                    ) : null}
                    {roleAuditStatus === "failed" ? (
                      <div className="text-red-700">{roleAuditError ?? "Role history failed"}</div>
                    ) : null}
                  </div>
                ) : null}
                {canReviewCanon ? (
                  <div className="mt-3 border-t border-[#eee] pt-2">
                    <div className="mb-1 flex items-center justify-between">
                      <span className="font-medium text-[#333]">Pending canon review</span>
                      <button
                        type="button"
                        className="rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadCanonReviewQueue()}
                      >
                        Refresh
                      </button>
                    </div>
                    <input
                      value={canonReviewQueueQueryFilter}
                      onChange={(event) => setCanonReviewQueueQueryFilter(event.target.value)}
                      className="mb-2 h-7 w-full rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                      placeholder="Search pending proposals"
                    />
                    <select
                      value={canonReviewQueueConsistencyFilter}
                      onChange={(event) => setCanonReviewQueueConsistencyFilter(event.target.value)}
                      className="mb-2 h-7 w-full rounded-sm border border-[#ddd] bg-white px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                    >
                      <option value="">All consistency states</option>
                      <option value="consistent">consistent</option>
                      <option value="soft_tension">soft_tension</option>
                      <option value="hard_contradiction">hard_contradiction</option>
                      <option value="canon_conflict">canon_conflict</option>
                      <option value="unchecked">unchecked</option>
                    </select>
                    {canonReviewQueue.length > 0 ? (
                      <div className="mb-3 max-h-36 overflow-y-auto">
                        {canonReviewQueue.map((branch) => (
                          <div key={branch.id} className="border-t border-[#f1f1f1] py-1 first:border-t-0">
                            <div className="flex min-w-0 items-center gap-1">
                              <span className="truncate text-[#333]">{branch.sourceLabel}</span>
                              {branch.isStaleSource ? (
                                <span className="shrink-0 rounded-sm bg-[#fff4d6] px-1 text-[10px] text-[#8a5a00]">
                                  stale
                                </span>
                              ) : null}
                              {branch.consistencyStatus ? (
                                <span
                                  title={branch.consistencySummary ?? undefined}
                                  className="shrink-0 rounded-sm border border-[#e3e3e3] px-1 text-[10px] text-[#666]"
                                >
                                  {branch.consistencyStatus}
                                </span>
                              ) : null}
                            </div>
                            <div className="truncate text-[11px] text-[#777]">
                              by {branch.authorEmail ?? branch.authorId} · {branch.outputPreview}
                            </div>
                            <div className="mt-1 flex flex-wrap gap-1">
                              {branch.sourceHref ? (
                                <a
                                  className="rounded-sm border border-[#ddd] px-1.5 py-0.5 text-[11px] text-[#555] hover:bg-[#f5f5f5]"
                                  href={branch.sourceHref}
                                >
                                  Open
                                </a>
                              ) : null}
                              <button
                                type="button"
                                className="rounded-sm border border-[#ccc] px-1.5 py-0.5 text-[11px] text-[#333] hover:bg-[#f5f5f5] disabled:cursor-not-allowed disabled:border-[#e3e3e3] disabled:text-[#aaa]"
                                disabled={branch.isStaleSource || branch.consistencyStatus === "canon_conflict"}
                                title={
                                  branch.consistencyStatus === "canon_conflict"
                                    ? "Canon conflicts must be revised or rejected before acceptance."
                                    : undefined
                                }
                                onClick={() => reviewQueuedBranch(branch.id, "accept")}
                              >
                                Accept
                              </button>
                              <button
                                type="button"
                                className="rounded-sm border border-[#ddd] px-1.5 py-0.5 text-[11px] text-[#555] hover:bg-[#f5f5f5]"
                                onClick={() => reviewQueuedBranch(branch.id, "reject")}
                              >
                                Reject
                              </button>
                              <button
                                type="button"
                                className="rounded-sm border border-[#ddd] px-1.5 py-0.5 text-[11px] text-[#555] hover:bg-[#f5f5f5]"
                                onClick={() => reviewQueuedBranch(branch.id, "revise")}
                              >
                                Revise
                              </button>
                            </div>
                            {branch.actionStatus === "failed" ? (
                              <div className="mt-1 text-[11px] text-red-700">
                                {branch.actionError ?? "Review failed"}
                              </div>
                            ) : null}
                          </div>
                        ))}
                      </div>
                    ) : canonReviewQueueStatus === "loaded" ? (
                      <div className="mb-3 text-[#777]">No pending reviews</div>
                    ) : null}
                    {canonReviewQueueNextCursor ? (
                      <button
                        type="button"
                        className="mb-2 rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadCanonReviewQueue(true)}
                      >
                        More
                      </button>
                    ) : null}
                    {canonReviewQueueStatus === "failed" ? (
                      <div className="mb-3 text-red-700">
                        {canonReviewQueueError ?? "Review queue failed"}
                      </div>
                    ) : null}
                    <div className="mb-1 flex items-center justify-between">
                      <span className="font-medium text-[#333]">Recent canon reviews</span>
                      <button
                        type="button"
                        className="rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadCanonReviewAudits()}
                      >
                        Refresh
                      </button>
                    </div>
                    <div className="mb-2 grid grid-cols-2 gap-1.5">
                      <input
                        value={canonReviewQueryFilter}
                        onChange={(event) => setCanonReviewQueryFilter(event.target.value)}
                        className="col-span-2 h-7 rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Search review history"
                      />
                      <input
                        value={canonReviewBranchFilter}
                        onChange={(event) => setCanonReviewBranchFilter(event.target.value)}
                        className="h-7 rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Branch"
                      />
                      <input
                        value={canonReviewReviewerFilter}
                        onChange={(event) => setCanonReviewReviewerFilter(event.target.value)}
                        className="h-7 rounded-sm border border-[#ddd] px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                        placeholder="Reviewer"
                      />
                      <select
                        value={canonReviewDecisionFilter}
                        onChange={(event) =>
                          setCanonReviewDecisionFilter(event.target.value as "" | "accept" | "reject" | "revise")
                        }
                        className="col-span-2 h-7 rounded-sm border border-[#ddd] bg-white px-1.5 text-[#222] outline-none focus:border-[#aaa]"
                      >
                        <option value="">All decisions</option>
                        <option value="accept">accept</option>
                        <option value="reject">reject</option>
                        <option value="revise">revise</option>
                      </select>
                    </div>
                    {canonReviewAudits.length > 0 ? (
                      <div className="max-h-36 overflow-y-auto">
                        {canonReviewAudits.map((review) => (
                          <div key={review.id} className="border-t border-[#f1f1f1] py-1 first:border-t-0">
                            <div className="flex min-w-0 items-center gap-1">
                              <span className="truncate text-[#333]">
                                {review.decision} · {review.branchSourceLabel ?? review.branchId}
                              </span>
                              {review.branchSourceHref ? (
                                <a
                                  className="shrink-0 rounded-sm px-1 text-[11px] text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                                  href={review.branchSourceHref}
                                >
                                  Open
                                </a>
                              ) : null}
                            </div>
                            <div className="truncate text-[11px] text-[#777]">
                              by {review.reviewerEmail ?? review.reviewerId}
                              {review.notes ? ` · ${review.notes}` : ""}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : canonReviewAuditStatus === "loaded" ? (
                      <div className="text-[#777]">No canon reviews yet</div>
                    ) : null}
                    {canonReviewAuditNextCursor ? (
                      <button
                        type="button"
                        className="mt-1 rounded-sm px-1.5 py-0.5 text-[#666] hover:bg-[#f3f3f3] hover:text-[#222]"
                        onClick={() => loadCanonReviewAudits(true)}
                      >
                        More
                      </button>
                    ) : null}
                    {canonReviewAuditStatus === "failed" ? (
                      <div className="text-red-700">
                        {canonReviewAuditError ?? "Canon review history failed"}
                      </div>
                    ) : null}
                  </div>
                ) : null}
              </div>
            ) : null}
          </div>
        ) : null}
      </header>

      <aside
        data-aia-side-nav
        className="fixed bottom-0 left-0 top-11 z-10 hidden w-[280px] flex-col border-r border-[#e5e5e5] bg-[#fafafa] lg:flex"
      >
        <div className="border-b border-[#ededed] px-4 py-4">
          <div className="mb-2 text-[11px] font-medium uppercase tracking-[0.12em] text-[#999]">
            emergentism.org
          </div>
          <button
            type="button"
            data-aia-side-nav-root
            className={`block w-full rounded-sm px-2 py-2 text-left transition-colors ${
              focusedNode === rootNodeId
                ? "bg-white text-[#171717] shadow-[0_1px_0_rgba(0,0,0,0.04)]"
                : "text-[#555] hover:bg-white hover:text-[#171717]"
            }`}
            onClick={() => dispatch({ type: "SET_FOCUS_STACK", nodeIds: [rootNodeId] })}
            title={bookRootNode?.canonicalTextMd ?? "The Infinite Book"}
          >
            <span className="block truncate text-[14px] font-medium">
              {bookRootNode?.canonicalTextMd ?? "The Infinite Book"}
            </span>
            <span className="mt-0.5 block text-[12px] text-[#888]">
              {sideNavItems.length} chapter{sideNavItems.length === 1 ? "" : "s"}
            </span>
          </button>
        </div>

        <nav aria-label="AIA book navigation" className="flex-1 overflow-y-auto px-2 py-3">
          <div className="space-y-0.5">
            {sideNavItems.map((node, index) => {
              const isActive = focusedRootChildId === node.id;
              const childCount = node.childrenIds?.length ?? 0;
              return (
                <button
                  key={node.id}
                  type="button"
                  data-aia-side-nav-item={node.id}
                  data-active={isActive ? "true" : "false"}
                  className={`group flex w-full items-start gap-2 rounded-sm px-2 py-1.5 text-left transition-colors ${
                    isActive
                      ? "bg-white text-[#171717] shadow-[0_1px_0_rgba(0,0,0,0.04)]"
                      : "text-[#555] hover:bg-white hover:text-[#171717]"
                  }`}
                  onClick={() =>
                    dispatch({
                      type: "SET_FOCUS_STACK",
                      nodeIds: [rootNodeId, node.id],
                    })
                  }
                  title={node.canonicalTextMd}
                >
                  <span
                    className={`mt-[2px] flex h-5 min-w-5 items-center justify-center rounded-sm border text-[11px] ${
                      isActive
                        ? "border-[#ccc] bg-[#f5f5f5] text-[#444]"
                        : "border-[#e1e1e1] bg-white text-[#999] group-hover:border-[#ccc]"
                    }`}
                  >
                    {index + 1}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-[13px] leading-5">{node.canonicalTextMd}</span>
                    <span className="block text-[11px] leading-4 text-[#999]">
                      {childCount} section{childCount === 1 ? "" : "s"}
                    </span>
                  </span>
                </button>
              );
            })}
          </div>
        </nav>
      </aside>

      <div className="space-y-2 border-b border-[#efefef] px-4 py-2 lg:hidden">
        <label className="flex h-8 items-center gap-2 rounded-sm border border-[#ddd] bg-[#fafafa] px-2 text-[#777]">
          <Search className="h-3.5 w-3.5 shrink-0" />
          <input
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            className="min-w-0 flex-1 bg-transparent text-[13px] text-[#222] outline-none placeholder:text-[#999]"
            placeholder="Search"
          />
        </label>
        {projectionLensOptions.length > 0 ? (
          <select
            aria-label="Projection lens"
            value={selectedProjectionLensId}
            onChange={(event) =>
              dispatch({
                type: "SET_PROJECTION_LENS",
                projectionLensId: event.currentTarget.value,
              })
            }
            className="h-8 w-full rounded-sm border border-[#ddd] bg-white px-2 text-[13px] text-[#555] outline-none focus:border-[#aaa] md:hidden"
          >
            <option value="">No lens</option>
            {projectionLensOptions.map((lens) => (
              <option key={lens.id} value={lens.id}>
                {lens.label}
              </option>
            ))}
          </select>
        ) : null}
      </div>

      <div className="mx-auto max-w-[760px] px-4 pb-16 pt-8 md:px-8 lg:ml-[312px] lg:mr-auto">
        <OutlinerNode nodeId={focusedNode} isRoot searchQuery={searchQuery} />
      </div>
    </section>
  );
}

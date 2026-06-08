"use client";

import type { ChangeEvent, FormEvent, KeyboardEvent } from "react";
import { ChevronRight, ChevronDown, AlertCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useGraphStore } from "@/lib/store";

interface NodeProps {
  nodeId: string;
  isRoot?: boolean;
  searchQuery?: string;
}

export function OutlinerNode({ nodeId, isRoot = false, searchQuery = "" }: NodeProps) {
  const node = useGraphStore(state => state.nodesById[nodeId]);
  const nodesById = useGraphStore(state => state.nodesById);
  const branchesById = useGraphStore(state => state.branchesById);
  const canReviewCanon = useGraphStore(state => state.currentUser?.canReviewCanon ?? false);
  const dispatch = useGraphStore(state => state.dispatch);

  if (!node) return null;

  const aiBranches = (node.branchIds || []).map(id => branchesById[id]).filter(Boolean);
  const hasChildren = Boolean(node.childrenIds?.length);
  const isBranch = hasChildren || aiBranches.length > 0;
  const isCollapsed = isBranch && !node.isExpanded; // halo (ghost-bullet) signals hidden content
  const isParagraph = node.type === "paragraph";
  const isRootHeading = isRoot && !isParagraph;
  const query = searchQuery.trim().toLowerCase();
  const nodeMatches = (candidateId: string): boolean => {
    const candidate = nodesById[candidateId];
    if (!candidate) return false;
    if (candidate.canonicalTextMd.toLowerCase().includes(query)) return true;
    return (candidate.childrenIds ?? []).some(nodeMatches);
  };
  const matchesSearch = query.length > 0 && node.canonicalTextMd.toLowerCase().includes(query);
  const isVisibleSearchResult = query.length === 0 || nodeMatches(nodeId);
  const showChildren = (query.length > 0 || node.isExpanded) && (hasChildren || aiBranches.length > 0);
  const hasCanonConflict = (status?: string) => status === "canon_conflict";
  const needsConsistencyReview = (status?: string) => status === "unchecked";
  const blocksCanonProposal = (branch: (typeof aiBranches)[number]) => {
    const status = branch.consistencyReport?.status ?? branch.consistencyStatus;
    return hasCanonConflict(status) || needsConsistencyReview(status);
  };
  const canonProposalBlockReason = (branch: (typeof aiBranches)[number]) => {
    const status = branch.consistencyReport?.status ?? branch.consistencyStatus;
    if (hasCanonConflict(status)) return "Canon conflicts must be revised before proposal.";
    if (needsConsistencyReview(status)) return "Branch edits need a fresh consistency review before proposal.";
    return undefined;
  };

  if (!isVisibleSearchResult) return null;

  const handleExpandToggle = () => {
    if (node.isExpanded) {
      dispatch({ type: "COLLAPSE_NODE", nodeId });
    } else {
      dispatch({ type: "EXPAND_NODE", nodeId });
    }
  };

  const triggerExpandAI = () => {
    dispatch({ type: "LONG_PRESS_NODE", nodeId });
  };

  const resolveBranchContradiction = async (
    localId: string,
    contradictionId: string,
    resolutionStatus:
      | "accepted_as_antithesis"
      | "forked"
      | "revised"
      | "synthesized"
      | "dismissed"
  ) => {
    const response = await fetch(`/api/contradictions/${encodeURIComponent(contradictionId)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resolutionStatus }),
    });
    if (!response.ok) return;
    dispatch({
      type: "RESOLVE_BRANCH_CONTRADICTION",
      localId,
      contradictionId,
      resolutionStatus,
    });
  };

  const saveBranchRevision = async (localId: string, serverId: string | undefined, outputMd: string) => {
    if (!outputMd.trim()) return;

    if (serverId) {
      const response = await fetch(`/api/branches/${encodeURIComponent(serverId)}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ outputMd }),
      });
      if (!response.ok) return;
    }

    dispatch({
      type: "COMMIT_BRANCH_REVISION",
      localId,
      outputMd,
    });
  };

  const proposeBranchAsCanon = async (localId: string, serverId: string | undefined) => {
    if (!serverId) return;

    const response = await fetch(`/api/branches/${encodeURIComponent(serverId)}/proposal`, {
      method: "POST",
    });
    if (response.ok) {
      dispatch({ type: "MARK_BRANCH_CANON_PROPOSED", localId });
      return;
    }

    let error = "proposal_failed";
    try {
      const payload = await response.json();
      if (typeof payload.error === "string") error = payload.error;
    } catch {
      // Keep the generic failure code; the UI only needs a quiet badge.
    }

    dispatch({
      type: "MARK_BRANCH_CANON_PROPOSAL_FAILED",
      localId,
      error,
    });
  };

  const checkBranchConsistency = async (localId: string, serverId: string | undefined) => {
    if (!serverId) return;
    dispatch({ type: "MARK_BRANCH_CONSISTENCY_CHECKING", localId });

    const response = await fetch(`/api/branches/${encodeURIComponent(serverId)}/consistency`, {
      method: "POST",
    });
    if (!response.ok) {
      let error = "consistency_recheck_failed";
      try {
        const payload = await response.json();
        if (typeof payload.error === "string") error = payload.error;
      } catch {
        // Keep the generic failure code.
      }
      dispatch({ type: "MARK_BRANCH_CONSISTENCY_CHECK_FAILED", localId, error });
      return;
    }

    const payload = await response.json();
    if (!payload.consistencyReport) {
      dispatch({ type: "MARK_BRANCH_CONSISTENCY_CHECK_FAILED", localId, error: "consistency_report_missing" });
      return;
    }

    dispatch({
      type: "MARK_BRANCH_CONSISTENCY_CHECKED",
      localId,
      consistencyReport: payload.consistencyReport,
      contradictions: Array.isArray(payload.contradictions) ? payload.contradictions : [],
    });
  };

  const reviewCanonProposal = async (
    localId: string,
    serverId: string | undefined,
    decision: "accept" | "reject" | "revise"
  ) => {
    if (!serverId) return;

    const response = await fetch(`/api/branches/${encodeURIComponent(serverId)}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision }),
    });
    if (response.ok) {
      const payload = await response.json();
      dispatch({
        type: "MARK_BRANCH_CANON_REVIEWED",
        localId,
        decision,
        reviewFeedback: typeof payload.review?.notes === "string" ? payload.review.notes : undefined,
      });
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
      type: "MARK_BRANCH_CANON_REVIEW_FAILED",
      localId,
      error,
    });
  };

  const getCursorOffset = () => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return node.canonicalTextMd.length;
    const range = selection.getRangeAt(0);
    const preCaretRange = range.cloneRange();
    preCaretRange.selectNodeContents(range.commonAncestorContainer.parentElement ?? range.commonAncestorContainer);
    preCaretRange.setEnd(range.endContainer, range.endOffset);
    return preCaretRange.toString().length;
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.altKey && event.key === "ArrowRight") {
      event.preventDefault();
      dispatch({ type: "PUSH_FOCUS", nodeId });
      return;
    }

    if (event.altKey && event.key === "ArrowLeft") {
      event.preventDefault();
      dispatch({ type: "SWIPE_RIGHT" });
      return;
    }

    if (event.key === "Enter") {
      event.preventDefault();
      dispatch({ type: "ENTER_SPLIT", nodeId, cursorOffset: getCursorOffset() });
      return;
    }

    if (event.key === "Tab") {
      event.preventDefault();
      dispatch({ type: event.shiftKey ? "SHIFT_TAB_OUTDENT" : "TAB_INDENT", nodeId });
      return;
    }

    if (event.key === "Backspace" && getCursorOffset() === 0) {
      event.preventDefault();
      dispatch({ type: "BACKSPACE_MERGE", nodeId });
      return;
    }
  };

  const handleInput = (event: FormEvent<HTMLDivElement>) => {
    dispatch({
      type: "UPDATE_NODE_TEXT",
      nodeId,
      text: event.currentTarget.textContent ?? "",
    });
  };

  return (
    <div id={`node-${nodeId}`} className={`relative flex scroll-mt-14 flex-col ${isRoot ? "text-base" : "text-[15px]"}`}>
      <div
        className="group relative flex items-start -ml-6 py-[3px]"
      >
        <div
          className={`absolute left-0 top-[5px] flex h-5 w-5 items-center justify-center transition-opacity ${
            isBranch ? "opacity-0 group-hover:opacity-100" : "opacity-0"
          }`}
        >
          {isBranch && (
            <button
              type="button"
              className="text-neutral-400 hover:text-neutral-800"
              onClick={(event) => {
                event.stopPropagation();
                handleExpandToggle();
              }}
              aria-label={node.isExpanded ? "Collapse" : "Expand"}
            >
              {node.isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
            </button>
          )}
        </div>

        <div
          className={`ml-4 flex h-6 w-6 shrink-0 items-center justify-center ${
            isParagraph ? "" : "cursor-pointer"
          }`}
          onClick={(event) => {
            if (isParagraph) return;
            event.stopPropagation();
            dispatch({ type: "PUSH_FOCUS", nodeId });
          }}
        >
          {!isParagraph && (
            <div className="relative flex h-full w-full items-center justify-center">
              <div
                className={`absolute rounded-full transition-opacity ${
                  isCollapsed
                    ? "h-5 w-5 border border-[#d6d6d6] bg-[#f4f4f4] opacity-80 group-hover:border-[#bdbdbd] group-hover:bg-[#ededed]"
                    : "h-4 w-4 bg-neutral-200 opacity-0 group-hover:opacity-100"
                }`}
              />
              <div
                className={`z-10 rounded-full transition-colors ${
                  isBranch
                    ? "h-2 w-2 bg-[#5f5f5f] group-hover:bg-[#222]"
                    : "h-1.5 w-1.5 bg-neutral-400 group-hover:bg-neutral-600"
                }`}
              />
            </div>
          )}
        </div>

        <div className="min-w-0 flex-1 pl-1">
          <div
            contentEditable
            suppressContentEditableWarning
            spellCheck
            onInput={handleInput}
            onKeyDown={handleKeyDown}
            className={`min-h-6 w-full cursor-text whitespace-pre-wrap break-words rounded-sm px-0.5 leading-relaxed outline-none ${
              isRootHeading
                ? "mb-2 text-[22px] font-semibold text-[#111]"
                : isParagraph
                  ? "text-[17px] font-normal leading-8 text-[#2a2a2a]"
                  : "font-normal text-[#2a2a2a]"
            } ${matchesSearch ? "bg-[#fff4b8]" : ""}`}
          >
            {node.canonicalTextMd}
          </div>

          {node.syncStatus === 'conflict' && (
            <div className="mt-1 inline-flex items-center gap-2 rounded-sm border border-red-200 bg-red-50 px-2 py-1 text-xs text-red-800">
              <AlertCircle className="h-3.5 w-3.5" />
              <span>Conflict</span>
              <button 
                className="underline"
                onClick={() => dispatch({ type: "RESOLVE_CONFLICT", localId: aiBranches[0]?.localId, action: 'keep_private' })}
              >
                Keep
              </button>
              <button 
                className="underline"
                onClick={() => dispatch({ type: "RESOLVE_CONFLICT", localId: aiBranches[0]?.localId, action: 'discard' })}
              >
                Discard
              </button>
            </div>
          )}

          {!hasChildren && node.type === 'paragraph' && (
            <button
              type="button"
              aria-label="Grow branch"
              title="Grow branch"
              onClick={triggerExpandAI}
              className="mt-1 hidden h-5 rounded-sm px-1.5 text-[11px] text-[#999] hover:bg-[#f2f2f2] hover:text-[#333] group-hover:inline-flex"
            >
              +
            </button>
          )}
        </div>
      </div>

      {showChildren && (
        <div className="ml-[11px] border-l border-[#e7e7e7] pl-[21px]">
          {node.childrenIds?.map(childId => (
             <OutlinerNode key={childId} nodeId={childId} searchQuery={searchQuery} />
          ))}
          {aiBranches.map(branch => (
            <div key={branch.localId} className={`my-2 rounded-sm border px-3 py-2 text-sm ${branch.status === 'failed' ? 'border-red-200 bg-red-50' : 'border-neutral-200 bg-neutral-50'}`}>
              <div className="mb-1 flex flex-wrap items-center gap-2">
                <div className={`text-[11px] font-medium uppercase tracking-wider ${branch.status === 'failed' ? 'text-red-700' : 'text-neutral-500'}`}>
                  {branch.status === 'failed' ? 'Private divergence' : 'AI Branch'}
                </div>
                {branch.contradictions?.map((contradiction) => (
                  <span
                    key={contradiction.id}
                    title={contradiction.explanation}
                    className="inline-flex items-center gap-1 rounded-sm border border-amber-200 bg-amber-50 px-1.5 py-0.5 text-[11px] font-medium text-amber-800"
                  >
                    <AlertCircle className="h-3 w-3" />
                    {contradiction.type.replace("_", " ")}
                    {contradiction.resolutionStatus === "unresolved" ? (
                      <>
                        <button
                          type="button"
                          aria-label="Synthesize contradiction"
                          className="ml-1 underline decoration-amber-400 underline-offset-2 hover:text-amber-950"
                          onClick={() => resolveBranchContradiction(branch.localId, contradiction.id, "synthesized")}
                        >
                          Synthesize
                        </button>
                        <button
                          type="button"
                          aria-label="Fork contradiction"
                          className="underline decoration-amber-400 underline-offset-2 hover:text-amber-950"
                          onClick={() => resolveBranchContradiction(branch.localId, contradiction.id, "forked")}
                        >
                          Fork
                        </button>
                        <button
                          type="button"
                          aria-label="Revise contradiction"
                          className="underline decoration-amber-400 underline-offset-2 hover:text-amber-950"
                          onClick={() => resolveBranchContradiction(branch.localId, contradiction.id, "revised")}
                        >
                          Revise
                        </button>
                        <button
                          type="button"
                          aria-label="Keep contradiction as antithesis"
                          className="underline decoration-amber-400 underline-offset-2 hover:text-amber-950"
                          onClick={() =>
                            resolveBranchContradiction(
                              branch.localId,
                              contradiction.id,
                              "accepted_as_antithesis"
                            )
                          }
                        >
                          Antithesis
                        </button>
                        <button
                          type="button"
                          aria-label="Dismiss contradiction"
                          className="underline decoration-amber-400 underline-offset-2 hover:text-amber-950"
                          onClick={() => resolveBranchContradiction(branch.localId, contradiction.id, "dismissed")}
                        >
                          Dismiss
                        </button>
                      </>
                    ) : (
                      <span className="ml-1 text-amber-700">{contradiction.resolutionStatus.replaceAll("_", " ")}</span>
                    )}
                  </span>
                ))}
                {branch.visibility === "proposed_canon" || branch.proposalStatus === "submitted" ? (
                  <span className="rounded-sm border border-sky-200 bg-sky-50 px-1.5 py-0.5 text-[11px] font-medium text-sky-800">
                    Proposed canon
                  </span>
                ) : null}
                {branch.visibility === "accepted_canon" ? (
                  <span className="rounded-sm border border-emerald-200 bg-emerald-50 px-1.5 py-0.5 text-[11px] font-medium text-emerald-800">
                    Accepted canon
                  </span>
                ) : null}
                {branch.proposalStatus === "conflict" ? (
                  <span
                    title="Canon moved after this branch was generated."
                    className="rounded-sm border border-amber-200 bg-amber-50 px-1.5 py-0.5 text-[11px] font-medium text-amber-800"
                  >
                    Stale source
                  </span>
                ) : null}
                {branch.proposalStatus === "failed" ? (
                  <span className="rounded-sm border border-red-200 bg-red-50 px-1.5 py-0.5 text-[11px] font-medium text-red-800">
                    Proposal failed
                  </span>
                ) : null}
                {branch.reviewStatus === "rejected" ? (
                  <span className="rounded-sm border border-neutral-200 bg-white px-1.5 py-0.5 text-[11px] font-medium text-neutral-600">
                    Review rejected
                  </span>
                ) : null}
                {branch.reviewStatus === "revision_requested" ? (
                  <span className="rounded-sm border border-neutral-200 bg-white px-1.5 py-0.5 text-[11px] font-medium text-neutral-600">
                    Review revise
                  </span>
                ) : null}
                {branch.reviewStatus === "failed" ? (
                  <span
                    title={branch.reviewError}
                    className="rounded-sm border border-red-200 bg-red-50 px-1.5 py-0.5 text-[11px] font-medium text-red-800"
                  >
                    Review failed
                  </span>
                ) : null}
                {branch.consistencyStatus === "unchecked" && !branch.consistencyReport ? (
                  <span
                    title="Branch text changed after its last consistency review."
                    className="rounded-sm border border-neutral-200 bg-white px-1.5 py-0.5 text-[11px] font-medium text-neutral-600"
                  >
                    Consistency unchecked
                  </span>
                ) : null}
                {branch.consistencyCheckStatus === "failed" ? (
                  <span
                    title={branch.consistencyCheckError}
                    className="rounded-sm border border-red-200 bg-red-50 px-1.5 py-0.5 text-[11px] font-medium text-red-800"
                  >
                    Consistency check failed
                  </span>
                ) : null}
              </div>
              {branch.reviewFeedback ? (
                <div className="mb-2 rounded-sm border border-neutral-200 bg-white px-2 py-1 text-[12px] leading-5 text-neutral-600">
                  <span className="font-medium text-neutral-700">Review note:</span> {branch.reviewFeedback}
                </div>
              ) : null}
              <div className="prose prose-sm max-w-none prose-p:my-1 prose-headings:my-1">
                {branch.revisionStatus === "editing" ? (
                  <div className="not-prose">
                    <textarea
                      aria-label="Revise branch output"
                      value={branch.revisionDraftMd ?? branch.outputMd}
                      onChange={(event: ChangeEvent<HTMLTextAreaElement>) =>
                        dispatch({
                          type: "UPDATE_BRANCH_REVISION_DRAFT",
                          localId: branch.localId,
                          outputMd: event.currentTarget.value,
                        })
                      }
                      className="min-h-32 w-full resize-y rounded-sm border border-neutral-300 bg-white px-2 py-1.5 text-sm leading-6 text-neutral-900 outline-none focus:border-neutral-500"
                    />
                    <div className="mt-1 flex gap-2 text-[11px]">
                      <button
                        type="button"
                        className="rounded-sm border border-neutral-300 px-2 py-0.5 text-neutral-700 hover:bg-neutral-100"
                        onClick={() =>
                          saveBranchRevision(
                            branch.localId,
                            branch.serverId,
                            branch.revisionDraftMd ?? branch.outputMd
                          )
                        }
                      >
                        Save
                      </button>
                      <button
                        type="button"
                        className="rounded-sm px-2 py-0.5 text-neutral-500 hover:bg-neutral-100 hover:text-neutral-800"
                        onClick={() => dispatch({ type: "CANCEL_BRANCH_REVISION", localId: branch.localId })}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : branch.status === 'queued' || branch.status === 'generating' ? (
                  <span className="text-neutral-500 italic">Expanding...</span>
                ) : (
                  <ReactMarkdown>{branch.outputMd}</ReactMarkdown>
                )}
                {branch.status === "complete" &&
                branch.serverId &&
                branch.visibility !== "proposed_canon" &&
                branch.visibility !== "accepted_canon" &&
                branch.revisionStatus !== "editing" ? (
                  <div className="not-prose mt-1 flex flex-wrap gap-2">
                    {needsConsistencyReview(branch.consistencyStatus) && !branch.consistencyReport ? (
                      <button
                        type="button"
                        className="rounded-sm border border-neutral-300 px-2 py-0.5 text-[11px] text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900"
                        disabled={branch.consistencyCheckStatus === "checking"}
                        onClick={() => checkBranchConsistency(branch.localId, branch.serverId)}
                      >
                        {branch.consistencyCheckStatus === "checking" ? "Checking..." : "Check consistency"}
                      </button>
                    ) : null}
                    <button
                      type="button"
                      className="rounded-sm border border-neutral-300 px-2 py-0.5 text-[11px] text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900"
                      disabled={blocksCanonProposal(branch)}
                      title={canonProposalBlockReason(branch)}
                      onClick={() => proposeBranchAsCanon(branch.localId, branch.serverId)}
                    >
                      Propose canon
                    </button>
                  </div>
                ) : null}
                {branch.consistencyReport ? (
                  <details className="not-prose mt-2 rounded-sm border border-neutral-200 bg-white px-2 py-1 text-[11px] text-neutral-700">
                    <summary className="cursor-pointer list-none truncate text-neutral-600">
                      Consistency: {branch.consistencyReport.status.replaceAll("_", " ")}
                      <span className="ml-1 text-neutral-400">({branch.consistencyReport.reportSource})</span>
                    </summary>
                    <div className="mt-1 text-neutral-600">{branch.consistencyReport.summary}</div>
                    {branch.consistencyReport.items.length > 0 ? (
                      <div className="mt-1 space-y-1">
                        {branch.consistencyReport.items.map((item) => (
                          <div key={`${item.claimId}-${item.priorClaimId ?? "none"}`} className="border-t border-neutral-100 pt-1 first:border-t-0 first:pt-0">
                            <div className="truncate text-neutral-500">
                              {item.relation} · {item.severity}
                            </div>
                            <div>{item.explanation}</div>
                          </div>
                        ))}
                      </div>
                    ) : null}
                  </details>
                ) : null}
                {canReviewCanon && branch.status === "complete" && branch.serverId && branch.visibility === "proposed_canon" ? (
                  <div className="not-prose mt-1 flex flex-wrap gap-2">
                    <button
                      type="button"
                      className="rounded-sm border border-neutral-300 px-2 py-0.5 text-[11px] text-neutral-700 hover:bg-neutral-100 disabled:cursor-not-allowed disabled:border-neutral-200 disabled:text-neutral-300"
                      disabled={blocksCanonProposal(branch)}
                      title={
                        hasCanonConflict(branch.consistencyReport?.status)
                          ? "Canon conflicts must be revised or rejected before acceptance."
                          : needsConsistencyReview(branch.consistencyReport?.status ?? branch.consistencyStatus)
                            ? "Edited branches need a fresh consistency review before acceptance."
                          : undefined
                      }
                      onClick={() => reviewCanonProposal(branch.localId, branch.serverId, "accept")}
                    >
                      Accept
                    </button>
                    <button
                      type="button"
                      className="rounded-sm border border-neutral-300 px-2 py-0.5 text-[11px] text-neutral-700 hover:bg-neutral-100"
                      onClick={() => reviewCanonProposal(branch.localId, branch.serverId, "reject")}
                    >
                      Reject
                    </button>
                    <button
                      type="button"
                      className="rounded-sm px-2 py-0.5 text-[11px] text-neutral-500 hover:bg-neutral-100 hover:text-neutral-800"
                      onClick={() => reviewCanonProposal(branch.localId, branch.serverId, "revise")}
                    >
                      Revise
                    </button>
                  </div>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

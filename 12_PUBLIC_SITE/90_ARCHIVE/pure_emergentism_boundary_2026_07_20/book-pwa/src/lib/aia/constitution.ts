// ─────────────────────────────────────────────────────────────────────────
// AIA · Branch Constitution & context compiler — the synthesis-compression
// problem.
//
// A deep branch cannot pass twenty levels of raw ancestral text into every
// prompt. The Branch Constitution is the compact, versioned summary of what the
// reader's private branch currently *believes* — hierarchical context folding
// for a personal worldview. The context compiler assembles the LLM payload and
// guarantees the root thesis and the constitution are always present, no matter
// how deep the branch goes.
// ─────────────────────────────────────────────────────────────────────────

import type { Claim } from "./types";

export interface BranchConstitution {
  branchId: string;
  /** Bumped on every accepted commitment or recorded tension. */
  version: number;
  acceptedCommitments: Claim[];
  openTensions: string[];
  preferredStyle?: string;
}

export interface PersistedBranchConstitutionRecord {
  branchId: string;
  version: number;
  acceptedCommitmentsJson: string;
  openTensionsJson: string;
  preferredStyle: string | null;
}

export function createDefaultBranchConstitution(userId: string, branchKey = "main"): BranchConstitution {
  return {
    branchId: `user:${userId}:${branchKey}`,
    version: 1,
    acceptedCommitments: [],
    openTensions: [],
  };
}

function parseJsonArray<T>(value: string): T[] {
  try {
    const parsed = JSON.parse(value);
    return Array.isArray(parsed) ? (parsed as T[]) : [];
  } catch {
    return [];
  }
}

export function serialiseBranchConstitution(constitution: BranchConstitution): {
  acceptedCommitmentsJson: string;
  openTensionsJson: string;
} {
  return {
    acceptedCommitmentsJson: JSON.stringify(constitution.acceptedCommitments),
    openTensionsJson: JSON.stringify(constitution.openTensions),
  };
}

export function parsePersistedBranchConstitution(
  record: PersistedBranchConstitutionRecord
): BranchConstitution {
  const constitution: BranchConstitution = {
    branchId: record.branchId,
    version: record.version,
    acceptedCommitments: parseJsonArray<Claim>(record.acceptedCommitmentsJson),
    openTensions: parseJsonArray<string>(record.openTensionsJson),
  };

  if (record.preferredStyle) {
    constitution.preferredStyle = record.preferredStyle;
  }

  return constitution;
}

const generatedClaimLinePattern =
  /^\s*[-*]\s*\[(asserted|denied|qualified|questioned)\]\s*([^:]+):\s*(.+)$/i;

export function extractClaimsFromMarkdown(markdown: string, sourceBranchId: string): Claim[] {
  let sequence = 0;

  return markdown.split(/\r?\n/).flatMap((line) => {
    const match = generatedClaimLinePattern.exec(line);
    if (!match) return [];

    const [, rawStance, rawScope, rawText] = match;
    const scope = rawScope.trim();
    const text = rawText.trim();
    if (!scope || !text) return [];

    sequence += 1;
    return [
      {
        id: `claim:${sourceBranchId}:${sequence}`,
        text,
        scope,
        stance: rawStance.toLowerCase() as Claim["stance"],
        sourceBranchId,
        confidence: 0.8,
      },
    ];
  });
}

/** Fold an accepted claim into the constitution (new version, immutable). */
export function acceptIntoConstitution(c: BranchConstitution, claim: Claim): BranchConstitution {
  return {
    ...c,
    version: c.version + 1,
    acceptedCommitments: [...c.acceptedCommitments, claim],
  };
}

export function mergeClaimsIntoConstitution(
  c: BranchConstitution,
  claims: Claim[],
): BranchConstitution {
  if (claims.length === 0) return c;

  return {
    ...c,
    version: c.version + 1,
    acceptedCommitments: [...c.acceptedCommitments, ...claims],
  };
}

/** Record an unresolved tension the reader is sitting with (new version). */
export function recordOpenTension(c: BranchConstitution, tension: string): BranchConstitution {
  return {
    ...c,
    version: c.version + 1,
    openTensions: [...c.openTensions, tension],
  };
}

export interface CompileContextInput {
  /** Immutable root thesis — never folded away. */
  rootThesis: string;
  /** Already-folded summary of the deep ancestor path. */
  ancestorSummary: string;
  /** The reader's worldview anchor — never folded away. */
  constitution: BranchConstitution;
  parentSummary: string;
  targetNodeText: string;
  directive: string;
  depth: number;
}

export interface ContextPayload {
  rootThesis: string;
  ancestorSummary: string;
  branchCommitments: string[];
  parentSummary: string;
  targetNodeText: string;
  directive: string;
  depth: number;
}

export interface AncestorPathEntry {
  nodeId: string;
  title: string | null;
  summary?: string | null;
  path: string;
  depth: number;
  versionHash: string;
}

export interface TargetNodeContext {
  nodeId: string;
  title: string | null;
  text: string;
  summary?: string | null;
  path: string;
  depth: number;
  versionHash: string;
}

export interface RetrievedContextEntry {
  label: string;
  pointerHash: string;
  text: string;
}

export interface ProjectionLensContext {
  id: string;
  label: string;
  instruction: string;
}

export interface CompileBoundedExpansionInput {
  rootThesis: string;
  rootThesisHash: string;
  ancestorPath: AncestorPathEntry[];
  parentSummary: string;
  targetNode: TargetNodeContext;
  constitution: BranchConstitution;
  retrievedContext: RetrievedContextEntry[];
  projectionLens?: ProjectionLensContext;
  directive: string;
  mode: string;
  requestedDepth: number;
}

export interface BoundedExpansionPayload {
  rootThesisPointer: {
    hash: string;
    text: string;
  };
  ancestorPath: AncestorPathEntry[];
  parentSummary: string;
  targetNode: TargetNodeContext;
  branchConstitution: BranchConstitution;
  retrievedContext: RetrievedContextEntry[];
  projectionLens?: ProjectionLensContext;
  userDirective: {
    prompt: string;
    mode: string;
    requestedDepth: number;
  };
}

/**
 * Compile the expansion payload. The root thesis and the branch constitution's
 * commitments are always carried, regardless of `depth` — that is the folding
 * contract (engineering invariant #4).
 */
export function compileContext(input: CompileContextInput): ContextPayload {
  return {
    rootThesis: input.rootThesis,
    ancestorSummary: input.ancestorSummary,
    branchCommitments: input.constitution.acceptedCommitments.map((c) => c.text),
    parentSummary: input.parentSummary,
    targetNodeText: input.targetNodeText,
    directive: input.directive,
    depth: input.depth,
  };
}

export function compileBoundedExpansionPayload(input: CompileBoundedExpansionInput): BoundedExpansionPayload {
  return {
    rootThesisPointer: {
      hash: input.rootThesisHash,
      text: input.rootThesis,
    },
    ancestorPath: input.ancestorPath,
    parentSummary: input.parentSummary,
    targetNode: input.targetNode,
    branchConstitution: input.constitution,
    retrievedContext: input.retrievedContext,
    projectionLens: input.projectionLens,
    userDirective: {
      prompt: input.directive,
      mode: input.mode,
      requestedDepth: input.requestedDepth,
    },
  };
}

/** Serialise a payload in canonical order: root thesis first, directive last. */
export function compileContextString(p: ContextPayload): string {
  return [
    `[ROOT THESIS]\n${p.rootThesis}`,
    `[ANCESTOR SUMMARY]\n${p.ancestorSummary}`,
    `[BRANCH CONSTITUTION]\n${p.branchCommitments.map((c) => `- ${c}`).join("\n")}`,
    `[PARENT SUMMARY]\n${p.parentSummary}`,
    `[TARGET NODE]\n${p.targetNodeText}`,
    `[DIRECTIVE]\n${p.directive}`,
  ].join("\n\n");
}

function serialiseAncestor(ancestor: AncestorPathEntry): string {
  return [
    `- nodeId: ${ancestor.nodeId}`,
    `  path: ${ancestor.path}`,
    `  depth: ${ancestor.depth}`,
    `  version: ${ancestor.versionHash}`,
    `  title: ${ancestor.title || "Untitled"}`,
    `  summary: ${ancestor.summary || "No summary available."}`,
  ].join("\n");
}

export function serialiseBoundedExpansionPayload(payload: BoundedExpansionPayload): string {
  const commitments = payload.branchConstitution.acceptedCommitments.length
    ? payload.branchConstitution.acceptedCommitments.map((claim) => `- ${claim.text}`).join("\n")
    : "none";
  const tensions = payload.branchConstitution.openTensions.length
    ? payload.branchConstitution.openTensions.map((tension) => `- ${tension}`).join("\n")
    : "none";
  const retrievedContext = payload.retrievedContext.length
    ? payload.retrievedContext
        .map((entry) => `- ${entry.label}\n  pointer: ${entry.pointerHash}\n  text: ${entry.text}`)
        .join("\n")
    : "none";
  const projectionLens = payload.projectionLens
    ? [
        `id: ${payload.projectionLens.id}`,
        `label: ${payload.projectionLens.label}`,
        `instruction: ${payload.projectionLens.instruction}`,
      ].join("\n")
    : "none";

  return [
    `[ROOT THESIS POINTER]\nhash: ${payload.rootThesisPointer.hash}\ntext: ${payload.rootThesisPointer.text}`,
    `[ANCESTOR PATH]\n${
      payload.ancestorPath.length
        ? payload.ancestorPath.map(serialiseAncestor).join("\n")
        : "none"
    }`,
    `[PARENT SUMMARY]\n${payload.parentSummary}`,
    `[TARGET NODE]\nnodeId: ${payload.targetNode.nodeId}\npath: ${payload.targetNode.path}\ndepth: ${payload.targetNode.depth}\nversion: ${payload.targetNode.versionHash}\ntitle: ${payload.targetNode.title || "Paragraph"}\nsummary: ${
      payload.targetNode.summary || "No summary available."
    }\ntext: ${payload.targetNode.text}`,
    `[BRANCH CONSTITUTION]\nbranchId: ${payload.branchConstitution.branchId}\nversion: ${payload.branchConstitution.version}\npreferredStyle: ${
      payload.branchConstitution.preferredStyle || "default"
    }\nacceptedCommitments:\n${commitments}\nopenTensions:\n${tensions}`,
    `[PROJECTION LENS]\n${projectionLens}`,
    `[RETRIEVED CONTEXT]\n${retrievedContext}`,
    `[USER DIRECTIVE]\nprompt: ${payload.userDirective.prompt}\nmode: ${payload.userDirective.mode}\nrequestedDepth: ${payload.userDirective.requestedDepth}`,
  ].join("\n\n");
}

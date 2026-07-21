// ─────────────────────────────────────────────────────────────────────────
// AIA · Dialectical Contradiction Layer — view-model types
//
// Self-contained types for the Infinite Book's contradiction-as-branch-state
// engine. Deliberately decoupled from Prisma AND from the Zustand store
// (src/lib/store.ts) so this logic stays PURE and unit-testable, and so it can
// be wired into the store without a hard import cycle. See INTEGRATION.md for
// the field-by-field mapping onto the store's PendingAIBranch / InteractionEvent.
//
// Constitutional note: contradiction is treated as ΔΦ (a rise in integrated
// awareness), not as an error. Canon stays coherent; private branches may
// become dialectical, but never *secretly* incoherent.
// ─────────────────────────────────────────────────────────────────────────

/** How a claim positions itself relative to its scope. */
export type ClaimStance = "asserted" | "denied" | "qualified" | "questioned";

/** A single atomic proposition extracted from an expansion. */
export interface Claim {
  id: string;
  text: string;
  /** Conceptual axis the claim lives on, e.g. "definition_of_consciousness". */
  scope: string;
  stance: ClaimStance;
  /** The branch this claim was generated within. Anchors the sludge boundary. */
  sourceBranchId: string;
  /** 0..1 self-reported confidence. */
  confidence: number;
}

/** The epistemic lane a private branch occupies. */
export type BranchMode = "mainline" | "antithesis" | "synthesis" | "sandbox";

/** A branch's running coherence verdict. */
export type ConsistencyStatus =
  | "unchecked"
  | "consistent"
  | "soft_tension"
  | "hard_contradiction"
  | "canon_conflict"
  | "resolved";

/** Where a contradiction sits relative to the reader's lineage. */
export type ContradictionType =
  | "canon_conflict" // conflicts with the immutable root/canon
  | "ancestor_conflict" // conflicts with the reader's own earlier branch
  | "sibling_tension" // disagrees with a sibling branch (productive pluralism)
  | "mode_intentional"; // contradiction the reader explicitly asked for

export type Severity = "low" | "medium" | "high";

export type ResolutionStatus =
  | "unresolved"
  | "accepted_as_antithesis"
  | "forked"
  | "revised"
  | "synthesized"
  | "dismissed";

/** A detected tension between a new claim and a prior commitment. */
export interface Contradiction {
  id: string;
  type: ContradictionType;
  severity: Severity;
  newClaimId: string;
  /** The prior claim it conflicts with; null for mode_intentional with no anchor. */
  priorClaimId: string | null;
  explanation: string;
  resolutionStatus: ResolutionStatus;
}

/** The "dialectical toggle" — the kind of expansion the reader requested. */
export type ExpansionMode =
  | "expand"
  | "simplify"
  | "go_deeper"
  | "apply"
  | "challenge"
  | "synthesize"
  | "creative"
  | "technical";

/** What the UI should do when a contradiction is detected on a branch. */
export type Friction = "freeze" | "badge" | "none";

/** Result of probing two claims for conflict (semantic; injected). */
export type ConflictKind = "none" | "soft" | "hard";

/**
 * Pure semantic comparator. In production this is backed by an LLM consistency
 * report; in tests it is a deterministic stub. Keeping it injected is what lets
 * the *routing* logic be tested without a model.
 */
export type ConflictProbe = (next: Claim, prior: Claim) => ConflictKind;

/** All the lineage context classification needs — pure inputs, no I/O. */
export interface ClassificationContext {
  /** Immutable canon/root claims. */
  canonClaims: Claim[];
  /** Claims from the reader's own ancestor branches in this lineage. */
  ancestorClaims: Claim[];
  /** Claims from sibling branches off the same parent. */
  siblingClaims: Claim[];
  /** Accepted commitments from the active Branch Constitution. */
  mainlineCommitments: Claim[];
  /** The expansion mode that produced the new claims. */
  mode: ExpansionMode;
}

/** Deterministic id minter injected into pure functions (no Date/random). */
export type IdFactory = (seed: string) => string;

// ─────────────────────────────────────────────────────────────────────────
// AIA · Claim ledger & contradiction resolution.
//
// A private branch is not a flat pile of generated text — it carries a ledger
// of claims and the tensions between them. This is the dialectical resolution
// reducer: it turns an `unresolved` contradiction into one of the five lanes
// the reader can choose (revise · fork · keep-as-antithesis · synthesize ·
// dismiss). It is the full superset of the store's binary keep/discard.
// Pure and immutable, like every reducer in this layer.
// ─────────────────────────────────────────────────────────────────────────

import type { Claim, Contradiction, ResolutionStatus } from "./types";

export interface LedgerState {
  claimsById: Record<string, Claim>;
  contradictionsById: Record<string, Contradiction>;
}

export type ResolutionAction =
  | "revise"
  | "fork"
  | "keep_as_antithesis"
  | "synthesize"
  | "dismiss";

export interface ResolveInput {
  contradictionId: string;
  action: ResolutionAction;
  /** Required for `synthesize` — the reconciling claim to fold into the ledger. */
  synthesisClaim?: Claim;
}

const STATUS_FOR: Record<ResolutionAction, ResolutionStatus> = {
  revise: "revised",
  fork: "forked",
  keep_as_antithesis: "accepted_as_antithesis",
  synthesize: "synthesized",
  dismiss: "dismissed",
};

/**
 * Resolve a contradiction along one dialectical lane. Returns the input state
 * unchanged when the id is unknown; otherwise produces a new state with the
 * contradiction's `resolutionStatus` updated and (for synthesis) the new claim
 * recorded.
 */
export function resolveContradiction(state: LedgerState, input: ResolveInput): LedgerState {
  const existing = state.contradictionsById[input.contradictionId];
  if (!existing) return state;

  const contradictionsById = {
    ...state.contradictionsById,
    [input.contradictionId]: { ...existing, resolutionStatus: STATUS_FOR[input.action] },
  };

  const claimsById =
    input.action === "synthesize" && input.synthesisClaim
      ? { ...state.claimsById, [input.synthesisClaim.id]: input.synthesisClaim }
      : state.claimsById;

  return { claimsById, contradictionsById };
}

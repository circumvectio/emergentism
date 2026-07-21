// ─────────────────────────────────────────────────────────────────────────
// AIA · Canon immutability — the mutation problem (Git-for-Text).
//
// Canon text is never updated in place. A revision mints a NEW content-addressed
// version that *supersedes* the old hash; the old version is retained (K3 —
// tombstone, never silent erasure). A reader's private branch hard-binds to the
// version hash it was generated from, so an upstream canon edit has zero ripple
// into existing branches — their universe is preserved.
// ─────────────────────────────────────────────────────────────────────────

export interface CanonNodeVersion {
  nodeId: string;
  versionHash: string;
  text: string;
  /** The hash this version replaces; null for the genesis version. */
  supersedesHash: string | null;
  author: string;
}

/** A private branch's immutable pointer to the canon version it grew from. */
export interface BoundBranch {
  branchId: string;
  boundVersionHash: string;
}

/**
 * FNV-1a (32-bit) content hash. Deterministic and dependency-free — adequate as
 * a client-side content address; the server can substitute SHA-256 behind the
 * same interface without any caller change.
 */
export function hashContent(text: string): string {
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

/**
 * Copy-on-write canon revision. Returns a brand-new version object that
 * supersedes `current`; never mutates the input.
 */
export function reviseCanon(
  current: CanonNodeVersion,
  newText: string,
  author = "canon",
): CanonNodeVersion {
  return {
    nodeId: current.nodeId,
    versionHash: hashContent(newText),
    text: newText,
    supersedesHash: current.versionHash,
    author,
  };
}

/** A branch is stale once the canon it bound to is no longer the current head. */
export function isBranchStale(branch: BoundBranch, currentCanon: CanonNodeVersion): boolean {
  return branch.boundVersionHash !== currentCanon.versionHash;
}

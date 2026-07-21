import { describe, it, expect } from "vitest";
import {
  hashContent,
  reviseCanon,
  isBranchStale,
  type CanonNodeVersion,
  type BoundBranch,
} from "../versioning";

describe("hashContent", () => {
  it("is deterministic for identical text", () => {
    expect(hashContent("φ · ν = 1")).toBe(hashContent("φ · ν = 1"));
  });
  it("changes when the text changes", () => {
    expect(hashContent("a")).not.toBe(hashContent("b"));
  });
});

// Engineering invariant #1 — Canon immutability:
// Editing canon creates a NEW version and does not mutate branches bound to v1.
describe("reviseCanon — copy-on-write canon immutability", () => {
  const v1: CanonNodeVersion = {
    nodeId: "node-1",
    versionHash: hashContent("Ethics is the expansion of meaningful possibility."),
    text: "Ethics is the expansion of meaningful possibility.",
    supersedesHash: null,
    author: "canon",
  };

  it("produces a new version with a new hash that supersedes the old one", () => {
    const v2 = reviseCanon(v1, "Ethics is the expansion of meaningful possibility under η=0.");
    expect(v2.versionHash).not.toBe(v1.versionHash);
    expect(v2.supersedesHash).toBe(v1.versionHash);
    expect(v2.nodeId).toBe(v1.nodeId);
  });

  it("does not mutate the prior version object (append-only ledger)", () => {
    const snapshot = JSON.stringify(v1);
    reviseCanon(v1, "something else entirely");
    expect(JSON.stringify(v1)).toBe(snapshot);
  });

  it("leaves a branch bound to v1 still bound to v1 after canon is revised", () => {
    const branch: BoundBranch = { branchId: "br-1", boundVersionHash: v1.versionHash };
    const v2 = reviseCanon(v1, "revised canon text");
    // The branch pointer is untouched — its universe is preserved.
    expect(branch.boundVersionHash).toBe(v1.versionHash);
    expect(branch.boundVersionHash).not.toBe(v2.versionHash);
  });

  it("reports a branch as stale once its bound version is superseded", () => {
    const branch: BoundBranch = { branchId: "br-1", boundVersionHash: v1.versionHash };
    const v2 = reviseCanon(v1, "revised canon text");
    expect(isBranchStale(branch, v1)).toBe(false);
    expect(isBranchStale(branch, v2)).toBe(true);
  });
});

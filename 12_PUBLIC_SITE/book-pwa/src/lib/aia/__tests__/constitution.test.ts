import { describe, it, expect } from "vitest";
import {
  acceptIntoConstitution,
  compileBoundedExpansionPayload,
  createDefaultBranchConstitution,
  extractClaimsFromMarkdown,
  mergeClaimsIntoConstitution,
  parsePersistedBranchConstitution,
  recordOpenTension,
  compileContext,
  compileContextString,
  serialiseBranchConstitution,
  serialiseBoundedExpansionPayload,
  type BranchConstitution,
} from "../constitution";
import type { Claim } from "../types";

const commitment = (id: string, text: string): Claim => ({
  id,
  text,
  scope: "P_node_equals_phi_times_v",
  stance: "asserted",
  sourceBranchId: "br_founder",
  confidence: 1,
});

const baseConstitution = (): BranchConstitution => ({
  branchId: "br_founder",
  version: 7,
  acceptedCommitments: [commitment("c1", "P_node = Φ × V is a strategic model, not a physical law.")],
  openTensions: [],
  preferredStyle: "executive-philosophical",
});

describe("acceptIntoConstitution", () => {
  it("bumps the version and appends the commitment", () => {
    const next = acceptIntoConstitution(baseConstitution(), commitment("c2", "Ethics expands meaningful possibility."));
    expect(next.version).toBe(8);
    expect(next.acceptedCommitments).toHaveLength(2);
    expect(next.acceptedCommitments[1].id).toBe("c2");
  });

  it("does not mutate the prior constitution", () => {
    const c = baseConstitution();
    const snapshot = JSON.stringify(c);
    acceptIntoConstitution(c, commitment("c2", "new"));
    expect(JSON.stringify(c)).toBe(snapshot);
  });
});

describe("recordOpenTension", () => {
  it("appends a tension and bumps the version", () => {
    const next = recordOpenTension(baseConstitution(), "Is consciousness a force or a process?");
    expect(next.version).toBe(8);
    expect(next.openTensions).toContain("Is consciousness a force or a process?");
  });
});

describe("extractClaimsFromMarkdown", () => {
  it("extracts structured generated claims from markdown bullets", () => {
    const claims = extractClaimsFromMarkdown(
      [
        "## Extracted claims",
        "- [asserted] aia_branch_constitution: AIA branches preserve reader commitments.",
        "- [qualified] context_scope: Sibling context is allowed only in synthesize mode.",
      ].join("\n"),
      "branch-1"
    );

    expect(claims).toEqual([
      {
        id: "claim:branch-1:1",
        text: "AIA branches preserve reader commitments.",
        scope: "aia_branch_constitution",
        stance: "asserted",
        sourceBranchId: "branch-1",
        confidence: 0.8,
      },
      {
        id: "claim:branch-1:2",
        text: "Sibling context is allowed only in synthesize mode.",
        scope: "context_scope",
        stance: "qualified",
        sourceBranchId: "branch-1",
        confidence: 0.8,
      },
    ]);
  });

  it("ignores unstructured bullets", () => {
    const claims = extractClaimsFromMarkdown("- ordinary bullet\n- [maybe] scope: invalid", "branch-1");
    expect(claims).toEqual([]);
  });
});

describe("mergeClaimsIntoConstitution", () => {
  it("bumps once and appends new generated claims", () => {
    const next = mergeClaimsIntoConstitution(baseConstitution(), [
      commitment("c2", "Generated claim one."),
      commitment("c3", "Generated claim two."),
    ]);

    expect(next.version).toBe(8);
    expect(next.acceptedCommitments.map((claim) => claim.id)).toEqual(["c1", "c2", "c3"]);
  });

  it("returns the same constitution when there are no claims", () => {
    const current = baseConstitution();
    const next = mergeClaimsIntoConstitution(current, []);

    expect(next).toBe(current);
  });
});

describe("persisted Branch Constitution records", () => {
  it("creates a stable empty constitution for a user branch key", () => {
    const constitution = createDefaultBranchConstitution("user-1", "main");

    expect(constitution).toEqual({
      branchId: "user:user-1:main",
      version: 1,
      acceptedCommitments: [],
      openTensions: [],
    });
  });

  it("serialises and parses commitments, tensions, and style", () => {
    const constitution: BranchConstitution = {
      ...baseConstitution(),
      openTensions: ["Whether the metaphor should become literal remains open."],
    };
    const serialised = serialiseBranchConstitution(constitution);
    const parsed = parsePersistedBranchConstitution({
      branchId: constitution.branchId,
      version: constitution.version,
      acceptedCommitmentsJson: serialised.acceptedCommitmentsJson,
      openTensionsJson: serialised.openTensionsJson,
      preferredStyle: constitution.preferredStyle || null,
    });

    expect(parsed).toEqual(constitution);
  });

  it("falls back to empty arrays when stored JSON is malformed", () => {
    const parsed = parsePersistedBranchConstitution({
      branchId: "user:user-1:main",
      version: 2,
      acceptedCommitmentsJson: "not json",
      openTensionsJson: "{",
      preferredStyle: null,
    });

    expect(parsed.acceptedCommitments).toEqual([]);
    expect(parsed.openTensions).toEqual([]);
    expect(parsed.version).toBe(2);
  });
});

// Engineering invariant #4 — context folding:
// even at depth 20 the compiled payload still carries the root thesis and the
// reader's worldview (the Branch Constitution), never folding them away.
describe("compileContext — folding preserves the anchor at any depth", () => {
  const input = {
    rootThesis: "φ · ν = 1 on S². Coherence × viability = 1 everywhere.",
    ancestorSummary: "…twenty levels of folded summary…",
    constitution: baseConstitution(),
    parentSummary: "Consciousness as value-weighted navigation.",
    targetNodeText: "Value without awareness is blind.",
    directive: "Apply this for a founder.",
    depth: 20,
  };

  it("always includes the root thesis at depth 20", () => {
    const payload = compileContext(input);
    expect(payload.rootThesis).toBe(input.rootThesis);
    expect(payload.depth).toBe(20);
  });

  it("always includes the branch constitution's commitments", () => {
    const payload = compileContext(input);
    expect(payload.branchCommitments).toContain(
      "P_node = Φ × V is a strategic model, not a physical law.",
    );
  });

  it("carries the directive and target node through", () => {
    const payload = compileContext(input);
    expect(payload.directive).toBe("Apply this for a founder.");
    expect(payload.targetNodeText).toBe("Value without awareness is blind.");
  });

  it("serialises in canonical order — root thesis first, directive last", () => {
    const text = compileContextString(compileContext(input));
    expect(text.indexOf(input.rootThesis)).toBeGreaterThanOrEqual(0);
    expect(text.indexOf(input.rootThesis)).toBeLessThan(text.indexOf(input.directive));
    expect(text.indexOf("P_node = Φ × V is a strategic model")).toBeLessThan(text.indexOf(input.directive));
  });
});

describe("compileBoundedExpansionPayload", () => {
  it("carries root pointer, ancestor summaries, target, constitution, retrieval, and directive", () => {
    const payload = compileBoundedExpansionPayload({
      rootThesis: "Reality unfolds as possibility.",
      rootThesisHash: "root-hash",
      ancestorPath: [
        {
          nodeId: "root",
          title: "Root",
          summary: "Root summary",
          path: "root",
          depth: 1,
          versionHash: "root-v1",
        },
        {
          nodeId: "parent",
          title: "Parent",
          summary: "Parent summary",
          path: "root/parent",
          depth: 2,
          versionHash: "parent-v1",
        },
      ],
      parentSummary: "Parent summary",
      targetNode: {
        nodeId: "target",
        title: "Target",
        text: "Target node full text.",
        summary: "Target summary",
        path: "root/parent/target",
        depth: 3,
        versionHash: "target-v1",
      },
      constitution: baseConstitution(),
      retrievedContext: [
        {
          label: "Prior synthesis",
          pointerHash: "branch-v7",
          text: "A prior accepted synthesis.",
        },
      ],
      projectionLens: {
        id: "research",
        label: "Research Lens",
        instruction: "Check provenance before synthesizing.",
      },
      directive: "Make this practical.",
      mode: "apply",
      requestedDepth: 20,
    });

    expect(payload.rootThesisPointer).toEqual({
      hash: "root-hash",
      text: "Reality unfolds as possibility.",
    });
    expect(payload.ancestorPath.map((ancestor) => ancestor.nodeId)).toEqual(["root", "parent"]);
    expect(payload.parentSummary).toBe("Parent summary");
    expect(payload.targetNode.versionHash).toBe("target-v1");
    expect(payload.branchConstitution.acceptedCommitments).toHaveLength(1);
    expect(payload.retrievedContext[0].pointerHash).toBe("branch-v7");
    expect(payload.projectionLens?.instruction).toBe("Check provenance before synthesizing.");
    expect(payload.userDirective).toEqual({
      prompt: "Make this practical.",
      mode: "apply",
      requestedDepth: 20,
    });
  });

  it("serialises in bounded canonical sections without sibling context", () => {
    const payload = compileBoundedExpansionPayload({
      rootThesis: "Reality unfolds as possibility.",
      rootThesisHash: "root-hash",
      ancestorPath: [
        {
          nodeId: "root",
          title: "Root",
          summary: "Root summary",
          path: "root",
          depth: 1,
          versionHash: "root-v1",
        },
      ],
      parentSummary: "Root summary",
      targetNode: {
        nodeId: "target",
        title: "Target",
        text: "Target node full text.",
        path: "root/target",
        depth: 2,
        versionHash: "target-v1",
      },
      constitution: baseConstitution(),
      retrievedContext: [],
      directive: "Expand locally.",
      mode: "expand",
      requestedDepth: 4,
    });

    const serialised = serialiseBoundedExpansionPayload(payload);

    expect(serialised).toContain("[ROOT THESIS POINTER]");
    expect(serialised).toContain("hash: root-hash");
    expect(serialised).toContain("[ANCESTOR PATH]");
    expect(serialised).toContain("Root summary");
    expect(serialised).toContain("[TARGET NODE]");
    expect(serialised).toContain("version: target-v1");
    expect(serialised).toContain("[BRANCH CONSTITUTION]");
    expect(serialised).toContain("P_node = Φ × V is a strategic model");
    expect(serialised).toContain("[PROJECTION LENS]\nnone");
    expect(serialised).toContain("[RETRIEVED CONTEXT]\nnone");
    expect(serialised).toContain("[USER DIRECTIVE]");
    expect(serialised).not.toContain("[SIBLING CONTEXT]");
  });

  it("serialises an optional projection lens as data", () => {
    const payload = compileBoundedExpansionPayload({
      rootThesis: "Reality unfolds as possibility.",
      rootThesisHash: "root-hash",
      ancestorPath: [],
      parentSummary: "No parent.",
      targetNode: {
        nodeId: "target",
        title: "Target",
        text: "Target node full text.",
        path: "target",
        depth: 1,
        versionHash: "target-v1",
      },
      constitution: baseConstitution(),
      retrievedContext: [],
      projectionLens: {
        id: "research",
        label: "Research Lens",
        instruction: "Check provenance before synthesizing.",
      },
      directive: "Make this practical.",
      mode: "apply",
      requestedDepth: 20,
    });

    const serialised = serialiseBoundedExpansionPayload(payload);

    expect(serialised).toContain("[PROJECTION LENS]");
    expect(serialised).toContain("id: research");
    expect(serialised).toContain("Research Lens");
    expect(serialised).toContain("Check provenance before synthesizing.");
  });
});

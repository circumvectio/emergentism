import { describe, it, expect } from "vitest";
import { wouldCreateCycle, addMirrorEdge, type Edge } from "../dag";

// Engineering invariant #2 — Mirror links cannot create reachable cycles.
describe("wouldCreateCycle", () => {
  const edges: Edge[] = [
    { source: "A", target: "B" },
    { source: "B", target: "C" },
  ];

  it("rejects a self-loop", () => {
    expect(wouldCreateCycle([], "A", "A")).toBe(true);
  });

  it("detects a back-edge that would close a loop (C → A when A ⇒ C)", () => {
    expect(wouldCreateCycle(edges, "C", "A")).toBe(true);
  });

  it("detects a deeper back-edge (C → B when B ⇒ C)", () => {
    expect(wouldCreateCycle(edges, "C", "B")).toBe(true);
  });

  it("allows a forward shortcut that introduces no cycle (A → C)", () => {
    expect(wouldCreateCycle(edges, "A", "C")).toBe(false);
  });

  it("allows an edge into a fresh node", () => {
    expect(wouldCreateCycle(edges, "C", "D")).toBe(false);
  });
});

describe("addMirrorEdge", () => {
  const edges: Edge[] = [
    { source: "A", target: "B" },
    { source: "B", target: "C" },
  ];

  it("appends a safe edge immutably", () => {
    const next = addMirrorEdge(edges, "A", "C");
    expect(next).toHaveLength(3);
    expect(edges).toHaveLength(2); // input untouched
    expect(next).toContainEqual({ source: "A", target: "C" });
  });

  it("throws rather than persist a cycle", () => {
    expect(() => addMirrorEdge(edges, "C", "A")).toThrow(/cycle/i);
  });
});

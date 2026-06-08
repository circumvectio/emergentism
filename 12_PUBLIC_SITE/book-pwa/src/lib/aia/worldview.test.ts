import { describe, expect, it } from "vitest";
import { buildExpansionSystemPrompt, loadWorldviewManifest, type WorldviewManifest } from "./worldview";

const manifest: WorldviewManifest = {
  manifestVersion: "test",
  instanceId: "test-book",
  title: "Test Book",
  subtitle: "A reusable book instance",
  rootThesis: "Reality is not a pile of things; it is an unfolding tree of possibility.",
  expansionModes: {
    apply: {
      label: "Make Practical",
      tone: "Turn the idea into a decision the reader can use today.",
    },
  },
  projectionLenses: {
    research: {
      label: "Research Lens",
      instruction: "Surface provenance gaps and distinguish source text from generated interpretation.",
    },
  },
  commitmentRules: [
    "Preserve the root thesis in every expansion.",
    "Expand ONLY the selected node.",
    "End with exactly three next branches.",
  ],
  engineDefaults: {
    nextBranchesCount: 3,
    generatedMark: "[AI]",
  },
};

describe("buildExpansionSystemPrompt", () => {
  it("builds the expansion prompt from author-supplied manifest data", () => {
    const prompt = buildExpansionSystemPrompt(manifest, "apply");

    expect(prompt).toContain("Test Book");
    expect(prompt).toContain("Reality is not a pile of things");
    expect(prompt).toContain("Turn the idea into a decision");
    expect(prompt).toContain("Preserve the root thesis in every expansion.");
    expect(prompt).toContain("End with exactly three next branches.");
    expect(prompt).toContain("[AI]");
    expect(prompt).not.toContain("Brahmā expansion engine");
  });

  it("adds an author-supplied projection lens only when requested", () => {
    const prompt = buildExpansionSystemPrompt(manifest, "apply", "research");

    expect(prompt).toContain("Projection lens:");
    expect(prompt).toContain("Research Lens");
    expect(prompt).toContain("Surface provenance gaps");
  });

  it("ignores unknown projection lens ids instead of inventing engine doctrine", () => {
    const prompt = buildExpansionSystemPrompt(manifest, "apply", "unknown");

    expect(prompt).not.toContain("Projection lens:");
    expect(prompt).not.toContain("unknown");
  });

  it("falls back to expand mode when the requested mode is unknown", () => {
    const prompt = buildExpansionSystemPrompt(
      {
        ...manifest,
        expansionModes: {
          expand: {
            label: "Expand",
            tone: "Deepen the selected node.",
          },
        },
      },
      "unsupported"
    );

    expect(prompt).toContain("Deepen the selected node.");
  });
});

describe("loadWorldviewManifest", () => {
  it("loads the current Emergentism AIA manifest from the repo-level content binding", () => {
    const loaded = loadWorldviewManifest();

    expect(loaded.instanceId).toBe("emergentism");
    expect(loaded.title).toBe("Emergentism");
    expect(loaded.rootThesis).toContain("Reality is not a pile of things");
    expect(loaded.commitmentRules).toContain("Preserve the root thesis in every expansion.");
  });
});

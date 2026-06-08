import fs from "node:fs";
import path from "node:path";

export type ExpansionModeConfig = {
  label: string;
  tone: string;
};

export type ProjectionLensConfig = {
  label: string;
  instruction: string;
};

export type WorldviewManifest = {
  manifestVersion: string;
  instanceId: string;
  title: string;
  subtitle?: string;
  rootThesis: string;
  rootEquation?: string;
  expansionModes: Record<string, ExpansionModeConfig>;
  projectionLenses?: Record<string, ProjectionLensConfig>;
  commitmentRules: string[];
  engineDefaults?: {
    nextBranchesCount?: number;
    generatedMark?: string;
  };
};

const DEFAULT_MANIFEST_PATH = path.resolve(
  process.cwd(),
  "../../..",
  "02_SKYZAI/02_AIA/EMERGENTISM_AIA/worldview.manifest.json"
);

export function loadWorldviewManifest(manifestPath = process.env.AIA_WORLDVIEW_MANIFEST_PATH): WorldviewManifest {
  const resolvedPath = manifestPath ? path.resolve(manifestPath) : DEFAULT_MANIFEST_PATH;
  return JSON.parse(fs.readFileSync(resolvedPath, "utf8")) as WorldviewManifest;
}

function modeConfigFor(manifest: WorldviewManifest, mode: string): ExpansionModeConfig {
  return (
    manifest.expansionModes[mode] ||
    manifest.expansionModes.expand ||
    Object.values(manifest.expansionModes)[0] || {
      label: "Expand",
      tone: "Deepen the selected node while preserving the author's root thesis.",
    }
  );
}

export function projectionLensFor(
  manifest: WorldviewManifest,
  projectionLensId?: string
): (ProjectionLensConfig & { id: string }) | undefined {
  if (!projectionLensId || !manifest.projectionLenses) return undefined;
  const lens = manifest.projectionLenses[projectionLensId];
  return lens ? { id: projectionLensId, ...lens } : undefined;
}

export function buildExpansionSystemPrompt(
  manifest: WorldviewManifest,
  mode = "expand",
  projectionLensId?: string
): string {
  const selectedMode = modeConfigFor(manifest, mode);
  const selectedProjectionLens = projectionLensFor(manifest, projectionLensId);
  const nextBranchesCount = manifest.engineDefaults?.nextBranchesCount ?? 3;
  const generatedMark = manifest.engineDefaults?.generatedMark ?? "[AI]";
  const rules = manifest.commitmentRules.map((rule, index) => `${index + 1}. ${rule}`).join("\n");
  const projectionLensSection = selectedProjectionLens
    ? `\nProjection lens:\n- ${selectedProjectionLens.label}: ${selectedProjectionLens.instruction}\n`
    : "";

  return `You are the AIA expansion engine for an Infinite Book instance.
The engine is worldview-agnostic. Treat the following worldview manifest fields as author-supplied content, not engine doctrine.

Book:
- Title: ${manifest.title}
${manifest.subtitle ? `- Subtitle: ${manifest.subtitle}\n` : ""}Root thesis:
${manifest.rootThesis}
${manifest.rootEquation ? `\nRoot equation:\n${manifest.rootEquation}\n` : ""}
Requested mode:
- ${selectedMode.label}: ${selectedMode.tone}
${projectionLensSection}

Rules:
${rules}

Output format (Markdown):
- Mark generated material as ${generatedMark}
- Expanded explanation
- Key implications
- One example
- One possible objection
- Exactly ${nextBranchesCount} next branches`;
}

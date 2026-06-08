import type { BranchMode, Claim, ConflictKind, ConflictProbe, Contradiction, ExpansionMode, Severity } from "./types";

export type ConsistencyReportSource = "model" | "heuristic";
export type ConsistencyReportStatus =
  | "unchecked"
  | "consistent"
  | "soft_tension"
  | "hard_contradiction"
  | "canon_conflict";
export type ConsistencyReportRelation = "supports" | "tension" | "conflict" | "unknown";

export type ConsistencyReportItem = {
  claimId: string;
  relation: ConsistencyReportRelation;
  priorClaimId?: string | null;
  severity: Severity;
  explanation: string;
};

export type BranchConsistencyReport = {
  reportSource: ConsistencyReportSource;
  status: ConsistencyReportStatus;
  summary: string;
  items: ConsistencyReportItem[];
};

type PromptInput = {
  branchId: string;
  branchMode: BranchMode;
  mode: ExpansionMode;
  generatedClaims: Claim[];
  commitments: Claim[];
  openTensions: string[];
  contradictions: Contradiction[];
};

type FallbackInput = {
  generatedClaims: Claim[];
  contradictions: Contradiction[];
};

const STATUS_VALUES = new Set<ConsistencyReportStatus>([
  "consistent",
  "soft_tension",
  "hard_contradiction",
  "canon_conflict",
]);
const RELATION_VALUES = new Set<ConsistencyReportRelation>(["supports", "tension", "conflict", "unknown"]);
const SEVERITY_VALUES = new Set<Severity>(["low", "medium", "high"]);

function claimLine(claim: Claim): string {
  return [
    `id=${claim.id}`,
    `scope=${claim.scope}`,
    `stance=${claim.stance}`,
    `confidence=${claim.confidence}`,
    `text=${claim.text}`,
  ].join(" | ");
}

function contradictionLine(contradiction: Contradiction): string {
  return [
    `id=${contradiction.id}`,
    `type=${contradiction.type}`,
    `severity=${contradiction.severity}`,
    `newClaimId=${contradiction.newClaimId}`,
    `priorClaimId=${contradiction.priorClaimId ?? "none"}`,
    `explanation=${contradiction.explanation}`,
  ].join(" | ");
}

export function buildConsistencyReportPrompt(input: PromptInput): string {
  return [
    "Return only JSON with this exact shape:",
    '{"status":"consistent|soft_tension|hard_contradiction|canon_conflict","summary":"short","items":[{"claimId":"...","relation":"supports|tension|conflict|unknown","priorClaimId":"... or null","severity":"low|medium|high","explanation":"short"}]}',
    "",
    `[BRANCH]`,
    `branchId: ${input.branchId}`,
    `branchMode: ${input.branchMode}`,
    `mode: ${input.mode}`,
    "",
    "[GENERATED CLAIMS]",
    input.generatedClaims.length ? input.generatedClaims.map(claimLine).join("\n") : "none",
    "",
    "[ACCEPTED COMMITMENTS]",
    input.commitments.length ? input.commitments.map(claimLine).join("\n") : "none",
    "",
    "[OPEN TENSIONS]",
    input.openTensions.length ? input.openTensions.map((item) => `- ${item}`).join("\n") : "none",
    "",
    "[DETECTED CONTRADICTIONS]",
    input.contradictions.length ? input.contradictions.map(contradictionLine).join("\n") : "none",
  ].join("\n");
}

function extractJson(text: string): unknown {
  const trimmed = text.trim();
  if (!trimmed) return null;

  const fenced = trimmed.match(/```(?:json)?\s*([\s\S]*?)```/i);
  const candidate = fenced?.[1]?.trim() ?? trimmed;

  try {
    return JSON.parse(candidate);
  } catch {
    return null;
  }
}

function asString(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

export function parseConsistencyReportText(
  text: string,
  generatedClaims: Claim[]
): BranchConsistencyReport | null {
  const parsed = extractJson(text);
  if (!parsed || typeof parsed !== "object") return null;

  const raw = parsed as {
    status?: unknown;
    summary?: unknown;
    items?: unknown;
  };
  const status = asString(raw.status);
  if (!status || !STATUS_VALUES.has(status as ConsistencyReportStatus)) return null;

  const knownClaimIds = new Set(generatedClaims.map((claim) => claim.id));
  const items = Array.isArray(raw.items)
    ? raw.items.flatMap((item): ConsistencyReportItem[] => {
        if (!item || typeof item !== "object") return [];
        const rawItem = item as Record<string, unknown>;
        const claimId = asString(rawItem.claimId);
        const relation = asString(rawItem.relation);
        const severity = asString(rawItem.severity);
        const explanation = asString(rawItem.explanation);
        if (!claimId || !knownClaimIds.has(claimId)) return [];
        if (!relation || !RELATION_VALUES.has(relation as ConsistencyReportRelation)) return [];
        if (!severity || !SEVERITY_VALUES.has(severity as Severity)) return [];
        if (!explanation) return [];
        const priorClaimId = asString(rawItem.priorClaimId);
        const normalized: ConsistencyReportItem = {
          claimId,
          relation: relation as ConsistencyReportRelation,
          severity: severity as Severity,
          explanation,
        };
        if (priorClaimId) normalized.priorClaimId = priorClaimId;
        return [normalized];
      })
    : [];

  return {
    reportSource: "model",
    status: status as ConsistencyReportStatus,
    summary: asString(raw.summary) ?? "Consistency report returned no summary.",
    items,
  };
}

function fallbackStatus(contradictions: Contradiction[]): ConsistencyReportStatus {
  if (contradictions.some((item) => item.type === "canon_conflict")) return "canon_conflict";
  if (contradictions.some((item) => item.severity === "high")) return "hard_contradiction";
  if (contradictions.length > 0) return "soft_tension";
  return "consistent";
}

function relationFor(contradiction: Contradiction | undefined): ConsistencyReportRelation {
  if (!contradiction) return "supports";
  return contradiction.severity === "high" || contradiction.type === "canon_conflict" ? "conflict" : "tension";
}

export function fallbackConsistencyReport(input: FallbackInput): BranchConsistencyReport {
  const contradictionsByClaim = new Map(input.contradictions.map((item) => [item.newClaimId, item]));
  const status = fallbackStatus(input.contradictions);
  return {
    reportSource: "heuristic",
    status,
    summary:
      status === "consistent"
        ? "No contradictions were detected by the local consistency router."
        : "The local consistency router found unresolved tension in this branch.",
    items: input.generatedClaims.map((claim) => {
      const contradiction = contradictionsByClaim.get(claim.id);
      const item: ConsistencyReportItem = {
        claimId: claim.id,
        relation: relationFor(contradiction),
        severity: contradiction?.severity ?? "low",
        explanation: contradiction?.explanation ?? "Claim is compatible with the active Branch Constitution.",
      };
      if (contradiction?.priorClaimId) item.priorClaimId = contradiction.priorClaimId;
      return item;
    }),
  };
}

export function conflictProbeFromConsistencyReport(
  report: BranchConsistencyReport,
  fallback: ConflictProbe = () => "none"
): ConflictProbe {
  const itemsByPair = new Map(
    report.items
      .filter((item) => item.priorClaimId)
      .map((item) => [`${item.claimId}:${item.priorClaimId}`, item])
  );

  return (next, prior): ConflictKind => {
    const item = itemsByPair.get(`${next.id}:${prior.id}`);
    if (!item) return fallback(next, prior);
    if (item.relation === "conflict") return "hard";
    if (item.relation === "tension") return "soft";
    return "none";
  };
}

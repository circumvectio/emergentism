import { NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";
import {
  createDefaultBranchConstitution,
  extractClaimsFromMarkdown,
  parsePersistedBranchConstitution,
  serialiseBranchConstitution,
} from "../../../../../lib/aia/constitution";
import {
  buildConsistencyReportPrompt,
  conflictProbeFromConsistencyReport,
  fallbackConsistencyReport,
  parseConsistencyReportText,
} from "../../../../../lib/aia/consistency";
import { classifyContradiction } from "../../../../../lib/aia/contradiction";
import type { BranchMode, Claim, ConflictKind, ExpansionMode } from "../../../../../lib/aia/types";
import { hashContent } from "../../../../../lib/aia/versioning";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function currentUserId(): Promise<string | null> {
  try {
    const { userId } = await auth();
    return userId;
  } catch {
    return null;
  }
}

function branchModeFor(value: string): BranchMode {
  if (value === "antithesis" || value === "synthesis" || value === "sandbox") return value;
  return "mainline";
}

function expansionModeFor(value: string): ExpansionMode {
  if (value === "challenge" || value === "synthesize" || value === "apply") return value;
  if (value === "simplify" || value === "creative" || value === "technical") return value;
  return "go_deeper";
}

function stanceConflictProbe(next: Claim, prior: Claim): ConflictKind {
  if (next.scope !== prior.scope) return "none";

  const opposed =
    (next.stance === "asserted" && prior.stance === "denied") ||
    (next.stance === "denied" && prior.stance === "asserted");
  if (opposed) return "hard";
  if (next.stance === "qualified" || prior.stance === "qualified") return "soft";
  return "none";
}

export async function POST(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const userId = await currentUserId();
  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  let user = await prisma.user.findUnique({ where: { id: userId } });
  if (!user) {
    user = await prisma.user.create({
      data: {
        id: userId,
        email: `${userId}@placeholder.com`,
        plan: "Free",
        creditsRemaining: 3,
      },
    });
  }

  if (user.plan === "Free" && user.creditsRemaining <= 0) {
    return NextResponse.json({ error: "Out of credits. Please upgrade to Explorer." }, { status: 403 });
  }

  const { id } = await params;
  const branch = await prisma.aIPBranch.findFirst({
    where: {
      id,
      userId,
    },
    include: {
      sourceNode: {
        include: {
          currentVersion: true,
        },
      },
    },
  });

  if (!branch) {
    return NextResponse.json({ error: "Branch not found" }, { status: 404 });
  }

  if (branch.visibility !== "private") {
    return NextResponse.json({ error: "branch_not_private" }, { status: 409 });
  }

  if (!branch.sourceNode.currentVersion || branch.sourceVersionHash !== branch.sourceNode.currentVersion.hash) {
    return NextResponse.json({ error: "stale_source_version" }, { status: 409 });
  }

  const branchKey = "main";
  const defaultConstitution = createDefaultBranchConstitution(userId, branchKey);
  const serialisedDefaultConstitution = serialiseBranchConstitution(defaultConstitution);
  const persistedConstitution = await prisma.branchConstitution.upsert({
    where: {
      userId_branchKey: {
        userId,
        branchKey,
      },
    },
    create: {
      userId,
      branchKey,
      branchId: defaultConstitution.branchId,
      version: defaultConstitution.version,
      acceptedCommitmentsJson: serialisedDefaultConstitution.acceptedCommitmentsJson,
      openTensionsJson: serialisedDefaultConstitution.openTensionsJson,
    },
    update: {},
  });
  const branchConstitution = parsePersistedBranchConstitution(persistedConstitution);
  const generatedClaims = extractClaimsFromMarkdown(branch.outputMd, branch.id);
  const branchMode = branchModeFor(branch.branchMode);
  const mode = expansionModeFor(branch.mode);

  const consistencyMessage = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 700,
    temperature: 0,
    system:
      "You are the AIA consistency reviewer. Compare generated claims against the active Branch Constitution and return only the requested JSON.",
    messages: [
      {
        role: "user",
        content: buildConsistencyReportPrompt({
          branchId: branch.id,
          branchMode,
          mode,
          generatedClaims,
          commitments: branchConstitution.acceptedCommitments,
          openTensions: branchConstitution.openTensions,
          contradictions: [],
        }),
      },
    ],
  });

  const consistencyBlock = consistencyMessage.content[0];
  const consistencyText = consistencyBlock?.type === "text" ? consistencyBlock.text : "";
  const modelConsistencyReport = parseConsistencyReportText(consistencyText, generatedClaims);
  const contradictions = classifyContradiction(
    generatedClaims,
    {
      canonClaims: [],
      ancestorClaims: [],
      siblingClaims: [],
      mainlineCommitments: branchConstitution.acceptedCommitments,
      mode,
    },
    modelConsistencyReport
      ? conflictProbeFromConsistencyReport(modelConsistencyReport, stanceConflictProbe)
      : stanceConflictProbe,
    (seed) => `contradiction:${hashContent(seed).slice(0, 16)}`
  );
  const consistencyReport =
    modelConsistencyReport ?? fallbackConsistencyReport({ generatedClaims, contradictions });

  await prisma.aIAContradiction.deleteMany({
    where: {
      branchId: branch.id,
      userId,
    },
  });

  if (contradictions.length > 0) {
    await prisma.aIAContradiction.createMany({
      data: contradictions.map((contradiction) => ({
        id: contradiction.id,
        userId,
        branchId: branch.id,
        branchKey,
        type: contradiction.type,
        severity: contradiction.severity,
        newClaimId: contradiction.newClaimId,
        priorClaimId: contradiction.priorClaimId,
        explanation: contradiction.explanation,
        resolutionStatus: contradiction.resolutionStatus,
      })),
    });
  }

  await prisma.aIPBranch.update({
    where: { id: branch.id },
    data: {
      consistencyStatus: consistencyReport.status,
      consistencyReportSource: consistencyReport.reportSource,
      consistencySummary: consistencyReport.summary,
      consistencyReportJson: JSON.stringify(consistencyReport),
    },
  });

  if (user.plan === "Free") {
    await prisma.user.update({
      where: { id: userId },
      data: { creditsRemaining: user.creditsRemaining - 1 },
    });
  }

  return NextResponse.json({
    branch: {
      id: branch.id,
      consistencyStatus: consistencyReport.status,
      consistencySummary: consistencyReport.summary,
    },
    consistencyReport,
    contradictions,
  });
}

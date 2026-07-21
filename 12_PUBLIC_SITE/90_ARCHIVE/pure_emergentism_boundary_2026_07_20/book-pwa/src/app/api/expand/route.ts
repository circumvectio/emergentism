import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import Anthropic from '@anthropic-ai/sdk';
import { auth } from '@clerk/nextjs/server';
import {
  compileBoundedExpansionPayload,
  createDefaultBranchConstitution,
  extractClaimsFromMarkdown,
  mergeClaimsIntoConstitution,
  parsePersistedBranchConstitution,
  serialiseBranchConstitution,
  serialiseBoundedExpansionPayload,
} from '../../../lib/aia/constitution';
import {
  buildConsistencyReportPrompt,
  conflictProbeFromConsistencyReport,
  fallbackConsistencyReport,
  parseConsistencyReportText,
} from '../../../lib/aia/consistency';
import { classifyContradiction } from '../../../lib/aia/contradiction';
import type { Claim, ConflictKind, ExpansionMode } from '../../../lib/aia/types';
import { hashContent } from '../../../lib/aia/versioning';
import { buildExpansionSystemPrompt, loadWorldviewManifest, projectionLensFor } from '../../../lib/aia/worldview';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

function ancestorPathsFor(path: string): string[] {
  const parts = path.split('/').filter(Boolean);
  return parts.slice(0, -1).map((_, index) => parts.slice(0, index + 1).join('/'));
}

function normaliseBranchKey(branchKey: unknown): string {
  return typeof branchKey === "string" && branchKey.trim() ? branchKey.trim() : "main";
}

function normaliseRetrievalNodeIds(retrievalNodeIds: unknown): string[] {
  if (!Array.isArray(retrievalNodeIds)) return [];

  return Array.from(
    new Set(
      retrievalNodeIds
        .filter((id): id is string => typeof id === "string" && id.trim().length > 0)
        .map((id) => id.trim())
    )
  );
}

function isSiblingPath(targetPath: string, candidatePath: string): boolean {
  const targetParts = targetPath.split('/').filter(Boolean);
  const candidateParts = candidatePath.split('/').filter(Boolean);

  if (targetParts.length !== candidateParts.length) return false;
  if (targetPath === candidatePath) return false;
  return targetParts.slice(0, -1).join('/') === candidateParts.slice(0, -1).join('/');
}

function branchModeForRequestedMode(mode: string): "mainline" | "antithesis" | "synthesis" {
  if (mode === "challenge") return "antithesis";
  if (mode === "synthesize") return "synthesis";
  return "mainline";
}

function expansionModeForRequestedMode(mode: string): ExpansionMode {
  if (mode === "challenge" || mode === "synthesize" || mode === "apply") return mode;
  if (mode === "simplify" || mode === "creative" || mode === "technical") return mode;
  if (mode === "go_deeper" || mode === "deeper") return "go_deeper";
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

export async function POST(req: Request) {
  try {
    const clerkPublishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? "";
    const clerkSecretKey = process.env.CLERK_SECRET_KEY ?? "";
    const isClerkConfigured =
      /^pk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkPublishableKey) &&
      /^sk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkSecretKey);
    if (!isClerkConfigured) {
      return NextResponse.json({ error: 'Auth is not configured for AI expansion' }, { status: 503 });
    }

    const { userId } = await auth();
    if (!userId) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    // Lazy sync user & check credits
    let user = await prisma.user.findUnique({ where: { id: userId } });
    if (!user) {
      user = await prisma.user.create({
        data: {
          id: userId,
          email: `${userId}@placeholder.com`, // We don't strictly need email for this check, but schema requires it
          plan: 'Free',
          creditsRemaining: 3
        }
      });
    }

    if (user.plan === 'Free' && user.creditsRemaining <= 0) {
      return NextResponse.json({ error: 'Out of credits. Please upgrade to Explorer.' }, { status: 403 });
    }

    const { nodeId, prompt, mode, depth, branchKey, retrievalNodeIds, projectionLensId } = await req.json();
    const constitutionBranchKey = normaliseBranchKey(branchKey);
    const requestedMode = mode || 'expand';
    const branchMode = branchModeForRequestedMode(requestedMode);
    const requestedRetrievalNodeIds = normaliseRetrievalNodeIds(retrievalNodeIds);

    const node = await prisma.node.findUnique({
      where: { id: nodeId },
      include: { currentVersion: true }
    });
    if (!node || !node.currentVersion) {
      return NextResponse.json({ error: 'Node not found' }, { status: 404 });
    }

    const ancestorPaths = ancestorPathsFor(node.path);
    const ancestors = ancestorPaths.length
      ? await prisma.node.findMany({
          where: {
            bookId: node.bookId,
            path: { in: ancestorPaths },
          },
          include: { currentVersion: true },
          orderBy: { depth: "asc" },
        })
      : [];
    const retrievedNodes = requestedRetrievalNodeIds.length
      ? await prisma.node.findMany({
          where: {
            bookId: node.bookId,
            id: { in: requestedRetrievalNodeIds },
          },
          include: { currentVersion: true },
          orderBy: { depth: "asc" },
        })
      : [];

    const worldviewManifest = loadWorldviewManifest();
    const selectedProjectionLens = projectionLensFor(
      worldviewManifest,
      typeof projectionLensId === "string" ? projectionLensId.trim() : undefined
    );
    const systemPrompt = buildExpansionSystemPrompt(worldviewManifest, requestedMode, selectedProjectionLens?.id);
    const defaultConstitution = createDefaultBranchConstitution(userId, constitutionBranchKey);
    const serialisedDefaultConstitution = serialiseBranchConstitution(defaultConstitution);
    const persistedConstitution = await prisma.branchConstitution.upsert({
      where: {
        userId_branchKey: {
          userId,
          branchKey: constitutionBranchKey,
        },
      },
      create: {
        userId,
        branchKey: constitutionBranchKey,
        branchId: defaultConstitution.branchId,
        version: defaultConstitution.version,
        acceptedCommitmentsJson: serialisedDefaultConstitution.acceptedCommitmentsJson,
        openTensionsJson: serialisedDefaultConstitution.openTensionsJson,
      },
      update: {},
    });
    const branchConstitution = parsePersistedBranchConstitution(persistedConstitution);
    const parent = ancestors[ancestors.length - 1];
    const contextPayload = compileBoundedExpansionPayload({
      rootThesis: worldviewManifest.rootThesis,
      rootThesisHash: hashContent(worldviewManifest.rootThesis),
      ancestorPath: ancestors.map((ancestor) => ({
        nodeId: ancestor.id,
        title: ancestor.title,
        summary: ancestor.summary,
        path: ancestor.path,
        depth: ancestor.depth,
        versionHash: ancestor.currentVersion?.hash || "unversioned",
      })),
      parentSummary: parent?.summary || parent?.title || "No parent summary available.",
      targetNode: {
        nodeId: node.id,
        title: node.title,
        text: node.currentVersion.contentMd,
        summary: node.summary,
        path: node.path,
        depth: node.depth,
        versionHash: node.currentVersion.hash,
      },
      constitution: branchConstitution,
      retrievedContext: retrievedNodes
        .filter((retrievedNode) => requestedMode === 'synthesize' || !isSiblingPath(node.path, retrievedNode.path))
        .filter((retrievedNode) => retrievedNode.id !== node.id && retrievedNode.currentVersion)
        .map((retrievedNode) => ({
          label: retrievedNode.title || retrievedNode.path,
          pointerHash: retrievedNode.currentVersion?.hash || "unversioned",
          text: retrievedNode.currentVersion?.contentMd || "",
        })),
      projectionLens: selectedProjectionLens,
      directive: prompt || 'Expand on this concept.',
      mode: requestedMode,
      requestedDepth: depth || 1,
    });
    const userMessage = serialiseBoundedExpansionPayload(contextPayload);

    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1500,
      temperature: 0.7,
      system: systemPrompt,
      messages: [
        {
          role: "user",
          content: userMessage
        }
      ]
    });

    const firstBlock = message.content[0];
    const outputMd = firstBlock?.type === 'text' ? firstBlock.text : '';
    if (!outputMd) {
      return NextResponse.json({ error: 'Expansion returned no text' }, { status: 502 });
    }

    // Save to database
    const branch = await prisma.aIPBranch.create({
      data: {
        userId: userId,
        sourceNodeId: node.id,
        sourceVersionHash: node.currentVersion.hash,
        sourceVersionId: node.currentVersion.id,
        prompt: prompt || 'Expand',
        outputMd: outputMd,
        mode: requestedMode,
        branchMode,
        depth: depth || 1,
        model: "claude-sonnet-4-6",
        tokenCount: message.usage.output_tokens,
      }
    });

    const generatedClaims = extractClaimsFromMarkdown(outputMd, branch.id);
    const consistencyMessage = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
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
            mode: expansionModeForRequestedMode(requestedMode),
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
        mode: expansionModeForRequestedMode(requestedMode),
      },
      modelConsistencyReport
        ? conflictProbeFromConsistencyReport(modelConsistencyReport, stanceConflictProbe)
        : stanceConflictProbe,
      (seed) => `contradiction:${hashContent(seed).slice(0, 16)}`
    );
    const consistencyReport =
      modelConsistencyReport ?? fallbackConsistencyReport({ generatedClaims, contradictions });
    await prisma.aIPBranch.update({
      where: { id: branch.id },
      data: {
        consistencyStatus: consistencyReport.status,
        consistencyReportSource: consistencyReport.reportSource,
        consistencySummary: consistencyReport.summary,
        consistencyReportJson: JSON.stringify(consistencyReport),
      },
    });
    if (contradictions.length > 0) {
      await prisma.aIAContradiction.createMany({
        data: contradictions.map((contradiction) => ({
          id: contradiction.id,
          userId,
          branchId: branch.id,
          branchKey: constitutionBranchKey,
          type: contradiction.type,
          severity: contradiction.severity,
          newClaimId: contradiction.newClaimId,
          priorClaimId: contradiction.priorClaimId,
          explanation: contradiction.explanation,
          resolutionStatus: contradiction.resolutionStatus,
        })),
      });
    }
    const conflictingClaimIds = new Set(contradictions.map((contradiction) => contradiction.newClaimId));
    const compatibleClaims = branchMode === "antithesis"
      ? []
      : generatedClaims.filter((claim) => !conflictingClaimIds.has(claim.id));
    const nextConstitution = mergeClaimsIntoConstitution(branchConstitution, compatibleClaims);
    const newTensions = branchMode === "antithesis"
      ? []
      : contradictions.map((contradiction) => contradiction.explanation);

    const branchConstitutionUpdateData: {
      version?: { increment: number };
      acceptedCommitmentsJson?: string;
      openTensionsJson?: string;
      lastSynthesisBranchId?: string;
    } = {};
    if (compatibleClaims.length > 0 || newTensions.length > 0) {
      const serialisedNextConstitution = serialiseBranchConstitution({
        ...nextConstitution,
        openTensions: [...nextConstitution.openTensions, ...newTensions],
      });
      branchConstitutionUpdateData.version = { increment: 1 };
      branchConstitutionUpdateData.acceptedCommitmentsJson =
        serialisedNextConstitution.acceptedCommitmentsJson;
      branchConstitutionUpdateData.openTensionsJson = serialisedNextConstitution.openTensionsJson;
    }
    if (branchMode === "synthesis") {
      branchConstitutionUpdateData.version = branchConstitutionUpdateData.version || { increment: 1 };
      branchConstitutionUpdateData.lastSynthesisBranchId = branch.id;
    }

    if (Object.keys(branchConstitutionUpdateData).length > 0) {
      await prisma.branchConstitution.update({
        where: {
          userId_branchKey: {
            userId,
            branchKey: constitutionBranchKey,
          },
        },
        data: branchConstitutionUpdateData,
      });
    }

    if (user.plan === 'Free') {
      await prisma.user.update({
        where: { id: userId },
        data: { creditsRemaining: user.creditsRemaining - 1 }
      });
    }

    return NextResponse.json({ branch, contradictions, consistencyReport });
  } catch (error) {
    console.error("Expansion failed", error);
    return NextResponse.json({ error: 'Expansion failed' }, { status: 500 });
  }
}

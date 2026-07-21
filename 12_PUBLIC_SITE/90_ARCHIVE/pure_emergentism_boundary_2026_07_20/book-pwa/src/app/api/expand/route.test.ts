import { beforeEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const mocks = vi.hoisted(() => ({
  auth: vi.fn(),
  anthropicCreate: vi.fn(),
  branchCreate: vi.fn(),
  branchUpdate: vi.fn(),
  branchConstitutionUpdate: vi.fn(),
  branchConstitutionUpsert: vi.fn(),
  contradictionCreateMany: vi.fn(),
  nodeFindMany: vi.fn(),
  nodeFindUnique: vi.fn(),
  userCreate: vi.fn(),
  userFindUnique: vi.fn(),
  userUpdate: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  auth: mocks.auth,
}));

vi.mock("@anthropic-ai/sdk", () => ({
  default: vi.fn().mockImplementation(() => ({
    messages: {
      create: mocks.anthropicCreate,
    },
  })),
}));

vi.mock("@/lib/prisma", () => ({
  prisma: {
    aIPBranch: {
      create: mocks.branchCreate,
      update: mocks.branchUpdate,
    },
    branchConstitution: {
      update: mocks.branchConstitutionUpdate,
      upsert: mocks.branchConstitutionUpsert,
    },
    aIAContradiction: {
      createMany: mocks.contradictionCreateMany,
    },
    node: {
      findMany: mocks.nodeFindMany,
      findUnique: mocks.nodeFindUnique,
    },
    user: {
      create: mocks.userCreate,
      findUnique: mocks.userFindUnique,
      update: mocks.userUpdate,
    },
  },
}));

describe("POST /api/expand", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = "pk_test_123456789012345678901234";
    process.env.CLERK_SECRET_KEY = "sk_test_123456789012345678901234";

    mocks.auth.mockResolvedValue({ userId: "user-1" });
    mocks.userFindUnique.mockResolvedValue({
      id: "user-1",
      plan: "Free",
      creditsRemaining: 3,
    });
    mocks.nodeFindUnique.mockResolvedValue({
      id: "node-1",
      bookId: "book-1",
      title: "Canon node",
      summary: "Target summary",
      path: "root/parent/node-1",
      depth: 3,
      currentVersion: {
        id: "version-1",
        hash: "hash-1",
        contentMd: "Canonical node text.",
      },
    });
    mocks.nodeFindMany.mockResolvedValue([
      {
        id: "root",
        title: "Root",
        summary: "Root summary",
        path: "root",
        depth: 1,
        currentVersion: {
          hash: "root-v1",
        },
      },
      {
        id: "parent",
        title: "Parent",
        summary: "Parent summary",
        path: "root/parent",
        depth: 2,
        currentVersion: {
          hash: "parent-v1",
        },
      },
    ]);
    mocks.branchConstitutionUpsert.mockResolvedValue({
      branchId: "user:user-1:main",
      version: 4,
      acceptedCommitmentsJson: JSON.stringify([
        {
          id: "claim-1",
          text: "AIA branches preserve reader commitments.",
          scope: "aia_branch_constitution",
          stance: "asserted",
          sourceBranchId: "user:user-1:main",
          confidence: 1,
        },
      ]),
      openTensionsJson: JSON.stringify(["Whether to rebase stale branches is unresolved."]),
      preferredStyle: "quiet-utility",
    });
    mocks.anthropicCreate.mockResolvedValue({
      content: [{ type: "text", text: "Expanded branch." }],
      usage: { output_tokens: 12 },
    });
    mocks.branchCreate.mockResolvedValue({ id: "branch-1" });
    mocks.branchUpdate.mockResolvedValue({ id: "branch-1" });
    mocks.branchConstitutionUpdate.mockResolvedValue({ branchId: "user:user-1:main", version: 5 });
    mocks.contradictionCreateMany.mockResolvedValue({ count: 1 });
    mocks.userUpdate.mockResolvedValue({ id: "user-1", creditsRemaining: 2 });
  });

  it("persists both source version hash and source version id on the branch", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Expand this",
          mode: "standard",
          depth: 2,
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.branchCreate).toHaveBeenCalledWith({
      data: expect.objectContaining({
        sourceNodeId: "node-1",
        sourceVersionHash: "hash-1",
        sourceVersionId: "version-1",
      }),
    });
  });

  it("uses the author worldview manifest for the system prompt", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Expand this",
          mode: "apply",
          depth: 2,
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.anthropicCreate).toHaveBeenCalledWith(
      expect.objectContaining({
        system: expect.stringContaining("Reality is not a pile of things"),
      })
    );
    expect(mocks.anthropicCreate).toHaveBeenCalledWith(
      expect.objectContaining({
        system: expect.stringContaining("End with exactly three next branches."),
      })
    );
    expect(mocks.anthropicCreate).toHaveBeenCalledWith(
      expect.objectContaining({
        system: expect.not.stringContaining("Brahmā expansion engine"),
      })
    );
  });

  it("sends a bounded compiler payload with ancestor path and no sibling context", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Expand locally",
          mode: "expand",
          depth: 20,
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.nodeFindMany).toHaveBeenCalledWith({
      where: {
        bookId: "book-1",
        path: { in: ["root", "root/parent"] },
      },
      include: { currentVersion: true },
      orderBy: { depth: "asc" },
    });

    const anthropicPayload = mocks.anthropicCreate.mock.calls[0][0];
    const userContent = anthropicPayload.messages[0].content;
    expect(userContent).toContain("[ROOT THESIS POINTER]");
    expect(userContent).toContain("[ANCESTOR PATH]");
    expect(userContent).toContain("Root summary");
    expect(userContent).toContain("Parent summary");
    expect(userContent).toContain("[TARGET NODE]");
    expect(userContent).toContain("version: hash-1");
    expect(userContent).toContain("[BRANCH CONSTITUTION]");
    expect(userContent).toContain("[USER DIRECTIVE]");
    expect(userContent).toContain("requestedDepth: 20");
    expect(userContent).not.toContain("[SIBLING CONTEXT]");
  });

  it("carries a requested author-defined projection lens into prompt and payload", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Read for proof gaps",
          mode: "expand",
          projectionLensId: "research",
        }),
      })
    );

    expect(response.status).toBe(200);
    const anthropicPayload = mocks.anthropicCreate.mock.calls[0][0];
    expect(anthropicPayload.system).toContain("Projection lens:");
    expect(anthropicPayload.system).toContain("Research Lens");
    expect(anthropicPayload.messages[0].content).toContain("[PROJECTION LENS]");
    expect(anthropicPayload.messages[0].content).toContain("id: research");
  });

  it("loads the persisted Branch Constitution into the bounded payload", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Expand with my commitments",
          mode: "expand",
          depth: 3,
          branchKey: "main",
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.branchConstitutionUpsert).toHaveBeenCalledWith({
      where: {
        userId_branchKey: {
          userId: "user-1",
          branchKey: "main",
        },
      },
      create: expect.objectContaining({
        userId: "user-1",
        branchKey: "main",
        branchId: "user:user-1:main",
      }),
      update: {},
    });

    const anthropicPayload = mocks.anthropicCreate.mock.calls[0][0];
    const userContent = anthropicPayload.messages[0].content;
    expect(userContent).toContain("branchId: user:user-1:main");
    expect(userContent).toContain("version: 4");
    expect(userContent).toContain("preferredStyle: quiet-utility");
    expect(userContent).toContain("AIA branches preserve reader commitments.");
    expect(userContent).toContain("Whether to rebase stale branches is unresolved.");
  });

  it("resolves retrieved context with provenance pointers for non-sibling nodes", async () => {
    mocks.nodeFindMany
      .mockResolvedValueOnce([
        {
          id: "root",
          title: "Root",
          summary: "Root summary",
          path: "root",
          depth: 1,
          currentVersion: { hash: "root-v1" },
        },
        {
          id: "parent",
          title: "Parent",
          summary: "Parent summary",
          path: "root/parent",
          depth: 2,
          currentVersion: { hash: "parent-v1" },
        },
      ])
      .mockResolvedValueOnce([
        {
          id: "retrieved-1",
          title: "Retrieved node",
          path: "other/branch/retrieved-1",
          parentId: "other-parent",
          currentVersion: {
            hash: "retrieved-v1",
            contentMd: "Retrieved context text.",
          },
        },
      ]);

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Use relevant context",
          mode: "expand",
          retrievalNodeIds: ["retrieved-1"],
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.nodeFindMany).toHaveBeenNthCalledWith(2, {
      where: {
        bookId: "book-1",
        id: { in: ["retrieved-1"] },
      },
      include: { currentVersion: true },
      orderBy: { depth: "asc" },
    });

    const userContent = mocks.anthropicCreate.mock.calls[0][0].messages[0].content;
    expect(userContent).toContain("[RETRIEVED CONTEXT]");
    expect(userContent).toContain("Retrieved node");
    expect(userContent).toContain("pointer: retrieved-v1");
    expect(userContent).toContain("Retrieved context text.");
  });

  it("blocks sibling retrieved context outside synthesize mode", async () => {
    mocks.nodeFindMany
      .mockResolvedValueOnce([
        {
          id: "root",
          title: "Root",
          summary: "Root summary",
          path: "root",
          depth: 1,
          currentVersion: { hash: "root-v1" },
        },
        {
          id: "parent",
          title: "Parent",
          summary: "Parent summary",
          path: "root/parent",
          depth: 2,
          currentVersion: { hash: "parent-v1" },
        },
      ])
      .mockResolvedValueOnce([
        {
          id: "sibling-1",
          title: "Sibling node",
          path: "root/parent/sibling-1",
          parentId: "parent",
          currentVersion: {
            hash: "sibling-v1",
            contentMd: "Sibling context text.",
          },
        },
      ]);

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Do not bleed to sibling",
          mode: "expand",
          retrievalNodeIds: ["sibling-1"],
        }),
      })
    );

    expect(response.status).toBe(200);
    const userContent = mocks.anthropicCreate.mock.calls[0][0].messages[0].content;
    expect(userContent).toContain("[RETRIEVED CONTEXT]\nnone");
    expect(userContent).not.toContain("Sibling context text.");
  });

  it("allows sibling retrieved context only in synthesize mode", async () => {
    mocks.nodeFindMany
      .mockResolvedValueOnce([
        {
          id: "root",
          title: "Root",
          summary: "Root summary",
          path: "root",
          depth: 1,
          currentVersion: { hash: "root-v1" },
        },
        {
          id: "parent",
          title: "Parent",
          summary: "Parent summary",
          path: "root/parent",
          depth: 2,
          currentVersion: { hash: "parent-v1" },
        },
      ])
      .mockResolvedValueOnce([
        {
          id: "sibling-1",
          title: "Sibling node",
          path: "root/parent/sibling-1",
          parentId: "parent",
          currentVersion: {
            hash: "sibling-v1",
            contentMd: "Sibling context text.",
          },
        },
      ]);

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Synthesize the tension",
          mode: "synthesize",
          retrievalNodeIds: ["sibling-1"],
        }),
      })
    );

    expect(response.status).toBe(200);
    const userContent = mocks.anthropicCreate.mock.calls[0][0].messages[0].content;
    expect(userContent).toContain("Sibling node");
    expect(userContent).toContain("pointer: sibling-v1");
    expect(userContent).toContain("Sibling context text.");
  });

  it("persists challenge branches in the antithesis lane", async () => {
    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Challenge this claim",
          mode: "challenge",
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.branchCreate).toHaveBeenCalledWith({
      data: expect.objectContaining({
        mode: "challenge",
        branchMode: "antithesis",
      }),
    });
  });

  it("does not merge antithesis claims into the main Branch Constitution", async () => {
    mocks.anthropicCreate.mockResolvedValueOnce({
      content: [
        {
          type: "text",
          text: [
            "Challenge branch.",
            "",
            "## Extracted claims",
            "- [denied] aia_branch_constitution: AIA branches preserve reader commitments.",
          ].join("\n"),
        },
      ],
      usage: { output_tokens: 22 },
    });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Challenge this claim",
          mode: "challenge",
          branchKey: "main",
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.branchCreate).toHaveBeenCalledWith({
      data: expect.objectContaining({
        mode: "challenge",
        branchMode: "antithesis",
      }),
    });
    expect(mocks.contradictionCreateMany).toHaveBeenCalledWith({
      data: [
        expect.objectContaining({
          userId: "user-1",
          branchId: "branch-1",
          branchKey: "main",
          type: "mode_intentional",
          severity: "low",
          newClaimId: "claim:branch-1:1",
          priorClaimId: "claim-1",
          resolutionStatus: "unresolved",
        }),
      ],
    });
    expect(mocks.branchConstitutionUpdate).not.toHaveBeenCalled();
  });

  it("bumps the Branch Constitution after synthesis branches are created", async () => {
    mocks.branchCreate.mockResolvedValueOnce({ id: "synthesis-branch-1" });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Synthesize the open tension",
          mode: "synthesize",
          branchKey: "main",
        }),
      })
    );

    expect(response.status).toBe(200);
    expect(mocks.branchCreate).toHaveBeenCalledWith({
      data: expect.objectContaining({
        mode: "synthesize",
        branchMode: "synthesis",
      }),
    });
    expect(mocks.branchConstitutionUpdate).toHaveBeenCalledWith({
      where: {
        userId_branchKey: {
          userId: "user-1",
          branchKey: "main",
        },
      },
      data: {
        version: { increment: 1 },
        lastSynthesisBranchId: "synthesis-branch-1",
      },
    });
  });

  it("extracts compatible mainline claims into the Branch Constitution", async () => {
    mocks.anthropicCreate.mockResolvedValueOnce({
      content: [
        {
          type: "text",
          text: [
            "Expanded branch.",
            "",
            "## Extracted claims",
            "- [asserted] context_scope: Sibling context is gated by mode.",
          ].join("\n"),
        },
      ],
      usage: { output_tokens: 22 },
    });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Expand and extract claims",
          mode: "expand",
          branchKey: "main",
        }),
      })
    );

    expect(response.status).toBe(200);
    const updateCall = mocks.branchConstitutionUpdate.mock.calls[0][0];
    expect(updateCall.where).toEqual({
      userId_branchKey: {
        userId: "user-1",
        branchKey: "main",
      },
    });
    expect(updateCall.data.version).toEqual({ increment: 1 });
    const accepted = JSON.parse(updateCall.data.acceptedCommitmentsJson);
    expect(accepted.map((claim: { text: string }) => claim.text)).toContain(
      "Sibling context is gated by mode."
    );
  });

  it("classifies conflicting generated claims as open tensions instead of commitments", async () => {
    mocks.anthropicCreate.mockResolvedValueOnce({
      content: [
        {
          type: "text",
          text: [
            "Expanded branch.",
            "",
            "## Extracted claims",
            "- [denied] aia_branch_constitution: AIA branches preserve reader commitments.",
          ].join("\n"),
        },
      ],
      usage: { output_tokens: 22 },
    });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Generate a contradiction",
          mode: "expand",
          branchKey: "main",
        }),
      })
    );

    expect(response.status).toBe(200);
    const updateCall = mocks.branchConstitutionUpdate.mock.calls[0][0];
    const accepted = JSON.parse(updateCall.data.acceptedCommitmentsJson);
    const tensions = JSON.parse(updateCall.data.openTensionsJson);
    expect(accepted).toHaveLength(1);
    expect(accepted.map((claim: { id: string }) => claim.id)).not.toContain("claim:branch-1:1");
    expect(tensions.join("\n")).toContain("conflicts");
    expect(updateCall.data.version).toEqual({ increment: 1 });
    expect(mocks.contradictionCreateMany).toHaveBeenCalledWith({
      data: [
        expect.objectContaining({
          userId: "user-1",
          branchId: "branch-1",
          branchKey: "main",
          type: "ancestor_conflict",
          severity: "medium",
          newClaimId: "claim:branch-1:1",
          priorClaimId: "claim-1",
          resolutionStatus: "unresolved",
          explanation: expect.stringContaining("conflicts"),
        }),
      ],
    });
  });

  it("returns contradiction summaries with the generated branch for reader badges", async () => {
    mocks.anthropicCreate.mockResolvedValueOnce({
      content: [
        {
          type: "text",
          text: [
            "Expanded branch.",
            "",
            "## Extracted claims",
            "- [denied] aia_branch_constitution: AIA branches preserve reader commitments.",
          ].join("\n"),
        },
      ],
      usage: { output_tokens: 22 },
    });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Generate a contradiction",
          mode: "expand",
          branchKey: "main",
        }),
      })
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.contradictions).toEqual([
      expect.objectContaining({
        type: "ancestor_conflict",
        severity: "medium",
        resolutionStatus: "unresolved",
        explanation: expect.stringContaining("conflicts"),
      }),
    ]);
  });

  it("returns a model-backed consistency report with the generated branch", async () => {
    mocks.anthropicCreate
      .mockResolvedValueOnce({
        content: [
          {
            type: "text",
            text: [
              "Expanded branch.",
              "",
              "## Extracted claims",
              "- [asserted] context_scope: Sibling context is gated by mode.",
            ].join("\n"),
          },
        ],
        usage: { output_tokens: 22 },
      })
      .mockResolvedValueOnce({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              status: "consistent",
              summary: "No conflicts against current commitments.",
              items: [
                {
                  claimId: "claim:branch-1:1",
                  relation: "supports",
                  severity: "low",
                  explanation: "The generated claim reinforces the active constitution.",
                },
              ],
            }),
          },
        ],
        usage: { output_tokens: 18 },
      });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Generate a report",
          mode: "expand",
          branchKey: "main",
        }),
      })
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(mocks.anthropicCreate).toHaveBeenCalledTimes(2);
    expect(mocks.anthropicCreate).toHaveBeenNthCalledWith(
      2,
      expect.objectContaining({
        system: expect.stringContaining("AIA consistency reviewer"),
        messages: [
          expect.objectContaining({
            role: "user",
            content: expect.stringContaining("claim:branch-1:1"),
          }),
        ],
      })
    );
    expect(body.consistencyReport).toEqual({
      reportSource: "model",
      status: "consistent",
      summary: "No conflicts against current commitments.",
      items: [
        {
          claimId: "claim:branch-1:1",
          relation: "supports",
          severity: "low",
          explanation: "The generated claim reinforces the active constitution.",
        },
      ],
    });
    expect(mocks.branchUpdate).toHaveBeenCalledWith({
      where: { id: "branch-1" },
      data: {
        consistencyStatus: "consistent",
        consistencyReportSource: "model",
        consistencySummary: "No conflicts against current commitments.",
        consistencyReportJson: JSON.stringify(body.consistencyReport),
      },
    });
  });

  it("uses the model consistency report as the contradiction classification probe", async () => {
    mocks.anthropicCreate
      .mockResolvedValueOnce({
        content: [
          {
            type: "text",
            text: [
              "Expanded branch.",
              "",
              "## Extracted claims",
              "- [asserted] aia_branch_constitution: AIA branches preserve reader commitments.",
            ].join("\n"),
          },
        ],
        usage: { output_tokens: 22 },
      })
      .mockResolvedValueOnce({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              status: "hard_contradiction",
              summary: "The generated claim conflicts semantically with the active commitment.",
              items: [
                {
                  claimId: "claim:branch-1:1",
                  relation: "conflict",
                  priorClaimId: "claim-1",
                  severity: "high",
                  explanation: "The model reports that the generated claim reverses the commitment in context.",
                },
              ],
            }),
          },
        ],
        usage: { output_tokens: 18 },
      });

    const response = await POST(
      new Request("http://localhost/api/expand", {
        method: "POST",
        body: JSON.stringify({
          nodeId: "node-1",
          prompt: "Generate a model-only conflict",
          mode: "expand",
          branchKey: "main",
        }),
      })
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.contradictions).toEqual([
      expect.objectContaining({
        type: "ancestor_conflict",
        severity: "medium",
        newClaimId: "claim:branch-1:1",
        priorClaimId: "claim-1",
      }),
    ]);
    expect(mocks.contradictionCreateMany).toHaveBeenCalledWith({
      data: [
        expect.objectContaining({
          userId: "user-1",
          branchId: "branch-1",
          branchKey: "main",
          type: "ancestor_conflict",
          severity: "medium",
          newClaimId: "claim:branch-1:1",
          priorClaimId: "claim-1",
        }),
      ],
    });
    const updateCall = mocks.branchConstitutionUpdate.mock.calls[0][0];
    const accepted = JSON.parse(updateCall.data.acceptedCommitmentsJson);
    const tensions = JSON.parse(updateCall.data.openTensionsJson);
    expect(accepted.map((item: { id: string }) => item.id)).not.toContain("claim:branch-1:1");
    expect(tensions.join("\n")).toContain("conflicts");
    expect(body.consistencyReport.status).toBe("hard_contradiction");
  });
});

-- CreateTable
CREATE TABLE "GraphWriteLock" (
    "scope" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_NodeLink" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "sourceNodeId" TEXT NOT NULL,
    "sourceVersionId" TEXT,
    "targetNodeId" TEXT NOT NULL,
    "targetVersionId" TEXT,
    "relationType" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'synced',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "NodeLink_sourceNodeId_fkey" FOREIGN KEY ("sourceNodeId") REFERENCES "Node" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "NodeLink_sourceVersionId_fkey" FOREIGN KEY ("sourceVersionId") REFERENCES "NodeVersion" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "NodeLink_targetNodeId_fkey" FOREIGN KEY ("targetNodeId") REFERENCES "Node" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "NodeLink_targetVersionId_fkey" FOREIGN KEY ("targetVersionId") REFERENCES "NodeVersion" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO "new_NodeLink" ("id", "relationType", "sourceNodeId", "targetNodeId") SELECT "id", "relationType", "sourceNodeId", "targetNodeId" FROM "NodeLink";
DROP TABLE "NodeLink";
ALTER TABLE "new_NodeLink" RENAME TO "NodeLink";
CREATE TABLE "new_AIPBranch" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "sourceNodeId" TEXT NOT NULL,
    "sourceVersionHash" TEXT NOT NULL,
    "sourceVersionId" TEXT,
    "parentBranchId" TEXT,
    "prompt" TEXT NOT NULL,
    "outputMd" TEXT NOT NULL,
    "mode" TEXT NOT NULL,
    "depth" INTEGER NOT NULL,
    "model" TEXT NOT NULL,
    "tokenCount" INTEGER NOT NULL DEFAULT 0,
    "costCents" INTEGER NOT NULL DEFAULT 0,
    "visibility" TEXT NOT NULL DEFAULT 'private',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "AIPBranch_sourceNodeId_fkey" FOREIGN KEY ("sourceNodeId") REFERENCES "Node" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "AIPBranch_sourceVersionId_fkey" FOREIGN KEY ("sourceVersionId") REFERENCES "NodeVersion" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "AIPBranch_parentBranchId_fkey" FOREIGN KEY ("parentBranchId") REFERENCES "AIPBranch" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO "new_AIPBranch" ("costCents", "createdAt", "depth", "id", "mode", "model", "outputMd", "parentBranchId", "prompt", "sourceNodeId", "sourceVersionHash", "tokenCount", "userId", "visibility") SELECT "costCents", "createdAt", "depth", "id", "mode", "model", "outputMd", "parentBranchId", "prompt", "sourceNodeId", "sourceVersionHash", "tokenCount", "userId", "visibility" FROM "AIPBranch";
DROP TABLE "AIPBranch";
ALTER TABLE "new_AIPBranch" RENAME TO "AIPBranch";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;

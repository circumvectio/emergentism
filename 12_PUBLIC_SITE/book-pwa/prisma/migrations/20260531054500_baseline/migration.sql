-- CreateTable
CREATE TABLE "Book" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "canonicalVersion" INTEGER NOT NULL DEFAULT 1,
    "visibility" TEXT NOT NULL DEFAULT 'public',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Node" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "bookId" TEXT NOT NULL,
    "parentId" TEXT,
    "path" TEXT NOT NULL,
    "depth" INTEGER NOT NULL,
    "orderIndex" INTEGER NOT NULL,
    "title" TEXT,
    "currentVersionId" TEXT,
    "summary" TEXT,
    "slug" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'canon',
    "createdBy" TEXT NOT NULL DEFAULT 'system',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Node_bookId_fkey" FOREIGN KEY ("bookId") REFERENCES "Book" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Node_parentId_fkey" FOREIGN KEY ("parentId") REFERENCES "Node" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "Node_currentVersionId_fkey" FOREIGN KEY ("currentVersionId") REFERENCES "NodeVersion" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "NodeVersion" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "hash" TEXT NOT NULL,
    "nodeId" TEXT NOT NULL,
    "contentMd" TEXT NOT NULL,
    "prevVersionId" TEXT,
    "authorId" TEXT NOT NULL DEFAULT 'system',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "NodeVersion_nodeId_fkey" FOREIGN KEY ("nodeId") REFERENCES "Node" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "NodeLink" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "sourceNodeId" TEXT NOT NULL,
    "targetNodeId" TEXT NOT NULL,
    "relationType" TEXT NOT NULL,
    CONSTRAINT "NodeLink_sourceNodeId_fkey" FOREIGN KEY ("sourceNodeId") REFERENCES "Node" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "NodeLink_targetNodeId_fkey" FOREIGN KEY ("targetNodeId") REFERENCES "Node" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AIPBranch" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "sourceNodeId" TEXT NOT NULL,
    "sourceVersionHash" TEXT NOT NULL,
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
    CONSTRAINT "AIPBranch_parentBranchId_fkey" FOREIGN KEY ("parentBranchId") REFERENCES "AIPBranch" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "email" TEXT NOT NULL,
    "plan" TEXT NOT NULL DEFAULT 'Free',
    "creditsRemaining" INTEGER NOT NULL DEFAULT 3,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Payment" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "provider" TEXT NOT NULL DEFAULT 'stripe',
    "amount" INTEGER NOT NULL,
    "plan" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "CanonReview" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "branchId" TEXT NOT NULL,
    "reviewerId" TEXT NOT NULL,
    "decision" TEXT NOT NULL,
    "notes" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "CanonReview_branchId_fkey" FOREIGN KEY ("branchId") REFERENCES "AIPBranch" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Book_slug_key" ON "Book"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "Node_slug_key" ON "Node"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "NodeVersion_hash_key" ON "NodeVersion"("hash");

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

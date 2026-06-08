-- CreateTable
CREATE TABLE "AIAContradiction" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "branchId" TEXT NOT NULL,
    "branchKey" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "severity" TEXT NOT NULL,
    "newClaimId" TEXT NOT NULL,
    "priorClaimId" TEXT,
    "explanation" TEXT NOT NULL,
    "resolutionStatus" TEXT NOT NULL DEFAULT 'unresolved',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "AIAContradiction_branchId_fkey" FOREIGN KEY ("branchId") REFERENCES "AIPBranch" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE INDEX "AIAContradiction_userId_branchKey_idx" ON "AIAContradiction"("userId", "branchKey");

-- CreateIndex
CREATE INDEX "AIAContradiction_branchId_idx" ON "AIAContradiction"("branchId");

-- CreateIndex
CREATE INDEX "AIAContradiction_type_resolutionStatus_idx" ON "AIAContradiction"("type", "resolutionStatus");

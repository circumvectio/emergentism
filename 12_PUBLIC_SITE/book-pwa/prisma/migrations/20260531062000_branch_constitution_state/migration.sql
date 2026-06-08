-- CreateTable
CREATE TABLE "BranchConstitution" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "branchKey" TEXT NOT NULL,
    "branchId" TEXT NOT NULL,
    "version" INTEGER NOT NULL DEFAULT 1,
    "acceptedCommitmentsJson" TEXT NOT NULL DEFAULT '[]',
    "openTensionsJson" TEXT NOT NULL DEFAULT '[]',
    "preferredStyle" TEXT,
    "lastSynthesisBranchId" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "BranchConstitution_userId_branchKey_key" ON "BranchConstitution"("userId", "branchKey");

-- CreateIndex
CREATE UNIQUE INDEX "BranchConstitution_branchId_key" ON "BranchConstitution"("branchId");

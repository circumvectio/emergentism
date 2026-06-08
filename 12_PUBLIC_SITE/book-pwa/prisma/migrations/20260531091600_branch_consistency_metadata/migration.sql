ALTER TABLE "AIPBranch" ADD COLUMN "consistencyStatus" TEXT NOT NULL DEFAULT 'unchecked';
ALTER TABLE "AIPBranch" ADD COLUMN "consistencyReportSource" TEXT;
ALTER TABLE "AIPBranch" ADD COLUMN "consistencySummary" TEXT;
ALTER TABLE "AIPBranch" ADD COLUMN "consistencyReportJson" TEXT;

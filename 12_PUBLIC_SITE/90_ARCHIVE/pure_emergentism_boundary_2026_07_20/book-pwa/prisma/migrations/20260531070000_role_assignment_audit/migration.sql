-- Durable audit history for reviewer/admin role changes.
CREATE TABLE "RoleAssignmentAudit" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "targetUserId" TEXT NOT NULL,
    "actorUserId" TEXT NOT NULL,
    "fromRole" TEXT NOT NULL,
    "toRole" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "RoleAssignmentAudit_targetUserId_createdAt_idx" ON "RoleAssignmentAudit"("targetUserId", "createdAt");
CREATE INDEX "RoleAssignmentAudit_actorUserId_createdAt_idx" ON "RoleAssignmentAudit"("actorUserId", "createdAt");

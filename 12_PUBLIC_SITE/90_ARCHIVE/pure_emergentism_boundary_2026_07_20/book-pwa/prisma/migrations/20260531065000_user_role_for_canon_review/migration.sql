-- Add first-class account role for canon review authority.
ALTER TABLE "User" ADD COLUMN "role" TEXT NOT NULL DEFAULT 'reader';

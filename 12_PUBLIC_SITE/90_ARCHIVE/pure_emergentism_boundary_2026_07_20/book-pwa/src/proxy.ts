import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import type { NextProxy } from "next/server";
import { NextResponse } from "next/server";

// Define the routes that need protection
const isProtectedRoute = createRouteMatcher([
  '/api/expand(.*)',
]);

const clerkPublishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? "";
const clerkSecretKey = process.env.CLERK_SECRET_KEY ?? "";
const isClerkConfigured =
  /^pk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkPublishableKey) &&
  /^sk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkSecretKey);

const authMiddleware = clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const proxy: NextProxy = (req, event) => {
  if (!isClerkConfigured) {
    return NextResponse.next();
  }
  return authMiddleware(req, event);
};

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};

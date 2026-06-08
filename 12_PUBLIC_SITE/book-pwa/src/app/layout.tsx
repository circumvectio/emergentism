import type { Metadata } from "next";
import "./globals.css";

import { ClerkProvider } from "@clerk/nextjs";

export const metadata: Metadata = {
  title: "The Infinite Book of Emergence",
  description: "A Workflowy-style infinite outline for the canonical manuscript.",
  manifest: "/manifest.json",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const clerkPublishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? "";
  const clerkSecretKey = process.env.CLERK_SECRET_KEY ?? "";
  const isClerkConfigured =
    /^pk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkPublishableKey) &&
    /^sk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkSecretKey);
  const shell = (
    <html lang="en">
      <body
        className="bg-white text-neutral-950 antialiased selection:bg-neutral-200 selection:text-neutral-950"
      >
        {children}
      </body>
    </html>
  );

  if (!isClerkConfigured) {
    return shell;
  }

  return (
    <ClerkProvider publishableKey={clerkPublishableKey}>
      {shell}
    </ClerkProvider>
  );
}

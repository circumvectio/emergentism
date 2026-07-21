import { defineConfig } from "vitest/config";

// The AIA frontend state machine is pure TypeScript (reducer, selectors,
// contradiction routing). These tests need no DOM and no Prisma client —
// they exercise plain view-model logic in `src/lib/aia`.
export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
    globals: false,
  },
});

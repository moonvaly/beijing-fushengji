import { defineConfig } from "vitest/config";

export default defineConfig({
  base: "/beijing-fushengji/",
  root: ".",
  publicDir: "public",
  server: {
    port: 5173,
    fs: { allow: [".."] },
  },
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
});

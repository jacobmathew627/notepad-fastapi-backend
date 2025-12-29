import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,

    // ✅ ONLY unit / component tests
    include: ["src/**/*.{test,spec}.{js,jsx}"],

    // 🚫 ABSOLUTELY NEVER run these
    exclude: [
      "**/node_modules/**",
      "**/dist/**",
      "**/e2e/**"
    ],

    setupFiles: "./src/tests/setup.js",
  },
});

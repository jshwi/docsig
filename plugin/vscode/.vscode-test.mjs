import { defineConfig } from "@vscode/test-cli";

export default defineConfig({
  coverage: {
    reporter: ["text-summary", "html", "lcovonly", "json-summary"],
  },
  tests: [
    {
      files: "out/test/**/*.test.js",
    },
  ],
});

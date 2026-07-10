import { defineConfig } from "@vscode/test-cli";

export default defineConfig({
  coverage: {
    reporter: ["text-summary", "html", "lcovonly", "json-summary"],
  },
  tests: [
    {
      files: "out/test/**/*.test.js",
      // Avoid hanging on a locked GNOME keyring (libsecret) over SSH/headless.
      launchArgs: ["--use-inmemory-secretstorage"],
    },
  ],
});

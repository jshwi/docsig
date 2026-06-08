import * as assert from "node:assert/strict";
import * as vscode from "vscode";
import { stubDocsigConfiguration } from "./mockConfiguration";

suite("mockConfiguration", () => {
  test("passes through unrelated configuration sections", () => {
    const disposable = stubDocsigConfiguration({ checkDunders: true });

    try {
      const docsig = vscode.workspace.getConfiguration("docsig");
      const python = vscode.workspace.getConfiguration("python");

      assert.equal(docsig.get("checkDunders"), true);
      assert.notEqual(python.get("checkDunders"), true);
    } finally {
      disposable.dispose();
    }
  });
});

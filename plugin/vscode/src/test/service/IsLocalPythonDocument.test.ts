import * as assert from "node:assert/strict";
import * as vscode from "vscode";
import { isLocalPythonDocument } from "../../main/service/DocsigService";

suite("isLocalPythonDocument", () => {
  test("returns true for local python files", () => {
    const document = {
      languageId: "python",
      uri: vscode.Uri.file("/test/file.py"),
    } as vscode.TextDocument;

    assert.equal(isLocalPythonDocument(document), true);
  });

  test("returns false for non-local files", () => {
    const document = {
      languageId: "python",
      uri: vscode.Uri.parse("untitled:Untitled-1"),
    } as vscode.TextDocument;

    assert.equal(isLocalPythonDocument(document), false);
  });

  test("returns false for non-python files", () => {
    const document = {
      languageId: "plaintext",
      uri: vscode.Uri.file("/test/file.txt"),
    } as vscode.TextDocument;

    assert.equal(isLocalPythonDocument(document), false);
  });
});

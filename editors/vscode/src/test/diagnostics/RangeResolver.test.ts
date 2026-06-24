import * as assert from "node:assert/strict";
import * as sinon from "sinon";
import * as vscode from "vscode";
import {
  findFunctionRange,
  resolveRange,
} from "../../main/diagnostics/RangeResolver";

suite("RangeResolver", () => {
  teardown(() => {
    sinon.restore();
  });

  function symbol(
    name: string,
    kind: vscode.SymbolKind,
    startLine: number,
    endLine: number,
    children: vscode.DocumentSymbol[] = [],
  ): vscode.DocumentSymbol {
    const start = new vscode.Position(startLine, 0);
    const end = new vscode.Position(endLine, 10);
    return {
      name,
      detail: "",
      kind,
      range: new vscode.Range(start, end),
      selectionRange: new vscode.Range(
        start,
        new vscode.Position(startLine, name.length),
      ),
      children,
    };
  }

  test("findFunctionRange returns undefined for missing symbols", () => {
    assert.equal(findFunctionRange(undefined, 1), undefined);
  });

  test("findFunctionRange returns selection range for matching method", () => {
    const symbols = [symbol("hello", vscode.SymbolKind.Function, 0, 2)];

    const range = findFunctionRange(symbols, 1);
    assert.equal(range?.start.line, 0);
    assert.equal(range?.start.character, 0);
  });

  test("findFunctionRange searches nested symbols", () => {
    const symbols = [
      symbol("Outer", vscode.SymbolKind.Class, 0, 5, [
        symbol("inner", vscode.SymbolKind.Method, 2, 4),
      ]),
    ];

    const range = findFunctionRange(symbols, 3);
    assert.equal(range?.start.line, 2);
  });

  test("resolveRange uses file start for null line", async () => {
    const document = {
      uri: vscode.Uri.file("/test.py"),
      lineCount: 3,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;

    const range = await resolveRange(document, null);
    assert.deepEqual(range, new vscode.Range(0, 0, 0, 0));
  });

  test("resolveRange prefers function symbol range", async () => {
    const document = {
      uri: vscode.Uri.file("/test.py"),
      lineCount: 3,
      lineAt: (line: number) => ({
        text: line === 0 ? "def hello():" : "    pass",
      }),
    } as unknown as vscode.TextDocument;

    sinon
      .stub(vscode.commands, "executeCommand")
      .resolves([symbol("hello", vscode.SymbolKind.Function, 0, 2)]);

    const range = await resolveRange(document, 1);
    assert.equal(range.start.line, 0);
  });

  test("resolveRange falls back to line start when no symbol", async () => {
    const document = {
      uri: vscode.Uri.file("/test.py"),
      lineCount: 3,
      lineAt: () => ({ text: "    pass" }),
    } as unknown as vscode.TextDocument;

    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    const range = await resolveRange(document, 2);
    assert.deepEqual(
      range,
      new vscode.Range(new vscode.Position(1, 4), new vscode.Position(1, 4)),
    );
  });

  test("resolveRange falls back to file start when line is out of range", async () => {
    const document = {
      uri: vscode.Uri.file("/test.py"),
      lineCount: 2,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;

    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    const range = await resolveRange(document, 99);
    assert.deepEqual(range, new vscode.Range(0, 0, 0, 0));
  });
});

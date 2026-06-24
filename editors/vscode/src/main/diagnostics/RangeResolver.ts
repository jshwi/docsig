import * as vscode from "vscode";

const FUNCTION_KINDS = new Set([
  vscode.SymbolKind.Function,
  vscode.SymbolKind.Method,
  vscode.SymbolKind.Constructor,
]);

export function findFunctionRange(
  symbols: vscode.DocumentSymbol[] | undefined,
  line: number,
): vscode.Range | undefined {
  if (!symbols) {
    return undefined;
  }

  for (const symbol of symbols) {
    if (
      FUNCTION_KINDS.has(symbol.kind) &&
      line >= symbol.range.start.line &&
      line <= symbol.range.end.line
    ) {
      return symbol.selectionRange;
    }

    const nested = findFunctionRange(symbol.children, line);
    if (nested) {
      return nested;
    }
  }

  return undefined;
}

function lineStartRange(
  document: vscode.TextDocument,
  line: number,
): vscode.Range {
  const index = line - 1;
  if (index < 0 || index >= document.lineCount) {
    return new vscode.Range(0, 0, 0, 0);
  }

  const text = document.lineAt(index).text;
  const start = text.search(/\S/);
  const column = start >= 0 ? start : 0;
  const position = new vscode.Position(index, column);
  return new vscode.Range(position, position);
}

/** Map a docsig line number to an editor range. */
export async function resolveRange(
  document: vscode.TextDocument,
  line: number | null,
): Promise<vscode.Range> {
  if (line === null) {
    return new vscode.Range(0, 0, 0, 0);
  }

  const symbols = await vscode.commands.executeCommand<
    vscode.DocumentSymbol[] | undefined
  >("vscode.executeDocumentSymbolProvider", document.uri);

  const functionRange = findFunctionRange(symbols, line - 1);
  if (functionRange) {
    return functionRange;
  }

  return lineStartRange(document, line);
}

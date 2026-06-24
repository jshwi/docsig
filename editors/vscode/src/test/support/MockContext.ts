import * as vscode from "vscode";

export function mockExtensionContext(
  extensionPath: string,
  globalStoragePath: string,
): vscode.ExtensionContext {
  return {
    extensionPath,
    globalStorageUri: vscode.Uri.file(globalStoragePath),
    subscriptions: [],
  } as unknown as vscode.ExtensionContext;
}

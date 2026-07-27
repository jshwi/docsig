import * as vscode from "vscode";
import { Python } from "./cli/Python";
import * as Log from "./messages/Log";
import { DocsigService, isLocalPythonDocument } from "./service/DocsigService";

export function activate(context: vscode.ExtensionContext): void {
  Log.debug("activated");

  const collection = vscode.languages.createDiagnosticCollection("docsig");
  const service = new DocsigService(context, collection);
  // a file written by another program (formatter, git, another editor)
  // never reaches the document events, so its cached result would
  // survive until something reopened it
  const watcher = vscode.workspace.createFileSystemWatcher("**/*.py");

  context.subscriptions.push(
    Log.outputChannel(),
    collection,
    service,
    vscode.workspace.onDidOpenTextDocument((document) => {
      if (!isLocalPythonDocument(document)) {
        return;
      }

      const path = document.uri.fsPath;
      if (service.hasCached(path)) {
        void service.publishCached(path);
        return;
      }

      service.ensureFresh(path);
    }),
    vscode.workspace.onDidChangeTextDocument((event) => {
      if (!isLocalPythonDocument(event.document)) {
        return;
      }

      service.ensureFresh(event.document.uri.fsPath);
    }),
    vscode.workspace.onDidSaveTextDocument((document) => {
      if (!isLocalPythonDocument(document)) {
        return;
      }

      service.scheduleFromSave(document.uri.fsPath);
    }),
    watcher,
    watcher.onDidChange((uri) => service.invalidateExternalChange(uri.fsPath)),
    watcher.onDidDelete((uri) => service.invalidateExternalChange(uri.fsPath)),
    vscode.workspace.onDidChangeConfiguration((event) => {
      const docsigChanged = event.affectsConfiguration("docsig");
      const pythonChanged = event.affectsConfiguration("python");
      if (!docsigChanged && !pythonChanged) {
        return;
      }

      Python.invalidate();
      service.scheduleAfterSettingsChange();
    }),
  );

  vscode.window.visibleTextEditors.forEach((editor) => {
    const document = editor.document;
    if (!isLocalPythonDocument(document)) {
      return;
    }

    const path = document.uri.fsPath;
    if (service.hasCached(path)) {
      void service.publishCached(path);
      return;
    }

    service.ensureFresh(path);
  });
}

export function deactivate(): void {}

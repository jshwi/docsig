import * as vscode from "vscode";
import { Python } from "./cli/Python";
import * as Log from "./messages/Log";
import { DocsigService, isLocalPythonDocument } from "./service/DocsigService";

/**
 * The slice of the service the event handlers below need.
 *
 * Declaring it keeps each handler callable with a stand-in, the way the
 * intellij listeners take a project service plus the neovim autocmds
 * call plain module functions.
 */
export interface ServiceLike {
  hasCached(path: string): boolean;
  publishCached(path: string): Promise<void>;
  ensureFresh(path: string): void;
  scheduleFromSave(path: string): void;
  invalidateExternalChange(path: string): void;
  scheduleAfterSettingsChange(): void;
}

/** Publish what is known for a document, else schedule a run. */
export function attach(
  service: ServiceLike,
  document: vscode.TextDocument,
): void {
  if (!isLocalPythonDocument(document)) {
    return;
  }

  const path = document.uri.fsPath;
  if (service.hasCached(path)) {
    void service.publishCached(path);
    return;
  }

  service.ensureFresh(path);
}

/** Schedule an idle run for an edited document. */
export function onChange(
  service: ServiceLike,
  document: vscode.TextDocument,
): void {
  if (!isLocalPythonDocument(document)) {
    return;
  }

  service.ensureFresh(document.uri.fsPath);
}

/** Schedule a save run for a written document. */
export function onSave(
  service: ServiceLike,
  document: vscode.TextDocument,
): void {
  if (!isLocalPythonDocument(document)) {
    return;
  }

  service.scheduleFromSave(document.uri.fsPath);
}

/** Re-run every affected path when the settings change. */
export function onConfigurationChange(
  service: ServiceLike,
  event: vscode.ConfigurationChangeEvent,
): void {
  const docsigChanged = event.affectsConfiguration("docsig");
  const pythonChanged = event.affectsConfiguration("python");
  if (!docsigChanged && !pythonChanged) {
    return;
  }

  Python.invalidate();
  service.scheduleAfterSettingsChange();
}

export function activate(context: vscode.ExtensionContext): void {
  Log.debug("activated");

  const collection = vscode.languages.createDiagnosticCollection("docsig");
  const service = new DocsigService(context, collection);
  // a file written by another program (formatter, git, another editor)
  // never reaches the document events, so its cached result would
  // survive until something reopened it
  const watcher = vscode.workspace.createFileSystemWatcher("**/*.py");

  context.subscriptions.push(
    // not the channel itself: Log caches it, so disposing it directly
    // would leave the cached reference pointing at a closed channel
    { dispose: () => Log.disposeChannel() },
    collection,
    service,
    vscode.workspace.onDidOpenTextDocument((document) =>
      attach(service, document),
    ),
    vscode.workspace.onDidChangeTextDocument((event) =>
      onChange(service, event.document),
    ),
    vscode.workspace.onDidSaveTextDocument((document) =>
      onSave(service, document),
    ),
    watcher,
    watcher.onDidChange((uri) => service.invalidateExternalChange(uri.fsPath)),
    watcher.onDidDelete((uri) => service.invalidateExternalChange(uri.fsPath)),
    vscode.workspace.onDidChangeConfiguration((event) =>
      onConfigurationChange(service, event),
    ),
  );

  vscode.window.visibleTextEditors.forEach((editor) =>
    attach(service, editor.document),
  );
}

export function deactivate(): void {}

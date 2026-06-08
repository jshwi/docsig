import * as vscode from "vscode";
import { Cli } from "../cli/Cli";
import { resolveRange } from "../diagnostics/RangeResolver";
import * as Log from "../Log";
import { Notifications } from "../messages/Notifications";
import { Issue } from "../models/Issue";
import {
  CliLike,
  DocsigServiceDependencies,
} from "./DocsigServiceDependencies";
import { mergeIssues } from "./mergeIssues";

const DEFAULT_DEBOUNCE_MS = 600;

type AlarmMap = Map<string, NodeJS.Timeout>;

/** Project-scoped docsig orchestration and diagnostic refresh. */
export class DocsigService implements vscode.Disposable {
  private readonly cache = new Map<string, Issue[]>();
  private readonly inFlight = new Set<string>();
  private readonly saveAlarms: AlarmMap = new Map();
  private readonly idleAlarms: AlarmMap = new Map();
  private readonly idlePending = new Set<string>();
  private readonly debounceMs: number;

  constructor(
    private readonly context: vscode.ExtensionContext,
    private readonly collection: vscode.DiagnosticCollection,
    private readonly deps: DocsigServiceDependencies = {},
  ) {
    this.debounceMs = deps.debounceMs ?? DEFAULT_DEBOUNCE_MS;
  }

  dispose(): void {
    for (const timer of this.saveAlarms.values()) {
      clearTimeout(timer);
    }
    for (const timer of this.idleAlarms.values()) {
      clearTimeout(timer);
    }
    this.saveAlarms.clear();
    this.idleAlarms.clear();
    this.idlePending.clear();
  }

  hasCached(path: string): boolean {
    return this.cache.has(path);
  }

  getIssues(path: string): Issue[] {
    return this.cache.get(path) ?? [];
  }

  ensureFresh(path: string): void {
    this.schedule(path, this.idleAlarms, false, "idle");
  }

  scheduleFromSave(path: string): void {
    Log.debug(`save trigger path=${path}`);
    this.schedule(path, this.saveAlarms, true, "save");
  }

  scheduleAfterSettingsChange(): void {
    const paths = this.pathsAffectedBySettingsChange();
    if (paths.size === 0) {
      return;
    }

    Log.debug(`settings trigger paths=${paths.size}`);

    paths.forEach((path) => {
      this.cache.delete(path);
      void this.publishDiagnostics(path);
      this.schedule(path, this.saveAlarms, true, "settings");
    });
  }

  async publishCached(path: string): Promise<void> {
    if (!this.hasCached(path)) {
      return;
    }

    await this.publishDiagnostics(path);
  }

  async refreshOpenDocuments(): Promise<void> {
    const paths = [...this.cache.keys(), ...this.listVisiblePythonPaths()];

    await Promise.all(paths.map((path) => this.publishDiagnostics(path)));
  }

  /** Run docsig immediately without debounce (for tests). */
  async runNow(path: string): Promise<void> {
    await this.runDocsig(path);
  }

  private listVisiblePythonPaths(): string[] {
    if (this.deps.listVisiblePythonPaths) {
      return this.deps.listVisiblePythonPaths();
    }

    return vscode.window.visibleTextEditors
      .map((editor) => editor.document)
      .filter(isLocalPythonDocument)
      .map((document) => document.uri.fsPath);
  }

  private pathsAffectedBySettingsChange(): Set<string> {
    const paths = new Set(this.cache.keys());
    this.listVisiblePythonPaths().forEach((path) => paths.add(path));
    return paths;
  }

  private schedule(
    path: string,
    alarmMap: AlarmMap,
    resetDebounce: boolean,
    source = "unknown",
  ): void {
    Log.debug(`${source} scheduled path=${path}`);

    const isIdle = alarmMap === this.idleAlarms;
    if (isIdle && this.idlePending.has(path)) {
      return;
    }

    if (resetDebounce) {
      const existing = alarmMap.get(path);
      if (existing) {
        clearTimeout(existing);
        alarmMap.delete(path);
      }
    } else if (alarmMap.has(path)) {
      return;
    }

    if (isIdle) {
      this.idlePending.add(path);
    }

    const timer = setTimeout(() => {
      alarmMap.delete(path);
      if (isIdle) {
        this.idlePending.delete(path);
      }
      void this.runDocsig(path);
    }, this.debounceMs);

    alarmMap.set(path, timer);
  }

  private cliFor(path: string): CliLike {
    if (this.deps.cliFactory) {
      return this.deps.cliFactory(path);
    }

    return new Cli(this.context, vscode.Uri.file(path));
  }

  private async runDocsig(path: string): Promise<void> {
    const cli = this.cliFor(path);
    const folder = vscode.workspace.getWorkspaceFolder(vscode.Uri.file(path));

    if (!(await cli.isAvailable())) {
      Notifications.notifyMissingPython(folder);
      return;
    }

    if (!(await cli.isPythonSupported())) {
      Notifications.notifyUnsupportedPython(folder);
      return;
    }

    if (this.inFlight.has(path)) {
      return;
    }

    this.inFlight.add(path);

    try {
      const issues = await cli.run(path);
      this.cache.set(path, mergeIssues(this.cache.get(path), issues));
    } finally {
      this.inFlight.delete(path);
    }

    await this.publishDiagnostics(path);
  }

  private async publishDiagnostics(path: string): Promise<void> {
    const uri = vscode.Uri.file(path);
    const document = vscode.workspace.textDocuments.find(
      (open) => open.uri.fsPath === path,
    );
    if (!document) {
      return;
    }

    const issues = this.getIssues(path);
    if (issues.length === 0) {
      this.collection.delete(uri);
      return;
    }

    const diagnostics = await Promise.all(
      issues.map(async (issue) => {
        const range = await resolveRange(document, issue.line);
        return new vscode.Diagnostic(
          range,
          issue.message,
          issue.exit === 2
            ? vscode.DiagnosticSeverity.Error
            : vscode.DiagnosticSeverity.Warning,
        );
      }),
    );

    this.collection.set(uri, diagnostics);
  }
}

export function isLocalPythonDocument(document: vscode.TextDocument): boolean {
  return document.languageId === "python" && document.uri.scheme === "file";
}

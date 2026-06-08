import * as vscode from "vscode";
import { runSubprocess } from "./Subprocess";

export const MIN_MAJOR = 3;
export const MIN_MINOR = 10;

const VERSION_CHECK_SCRIPT =
  "import sys;" +
  `min_versions = (${MIN_MAJOR}, ${MIN_MINOR});` +
  "sys.exit(0 if sys.version_info >= min_versions else 1)";

interface InterpreterCache {
  path: string | undefined;
  meetsMinimum: boolean;
}

interface PythonExtensionApi {
  environments?: {
    resolveEnvironment?: (
      resource?: vscode.Uri,
    ) => Promise<{ executable?: { uri?: vscode.Uri }; path?: string }>;
  };
  settings?: {
    getExecutionDetails?: (
      resource?: vscode.Uri,
    ) => Promise<{ execCommand?: string[] }>;
  };
}

/** Resolve and validate the workspace python interpreter. */
export class Python {
  private static readonly cache = new Map<string, InterpreterCache>();

  constructor(private readonly resource?: vscode.Uri) {}

  static invalidate(): void {
    Python.cache.clear();
  }

  private cacheKey(): string {
    const folder = this.resource
      ? vscode.workspace.getWorkspaceFolder(this.resource)?.uri.fsPath
      : undefined;
    return folder ?? this.resource?.fsPath ?? "";
  }

  private async resolvePath(): Promise<string | undefined> {
    const extension = vscode.extensions.getExtension("ms-python.python");
    if (extension && !extension.isActive) {
      await extension.activate();
    }

    const api = extension?.exports as PythonExtensionApi | undefined;
    const resolved = await api?.environments?.resolveEnvironment?.(
      this.resource,
    );
    if (resolved?.executable?.uri?.fsPath) {
      return resolved.executable.uri.fsPath;
    }
    if (resolved?.path) {
      return resolved.path;
    }

    const details = await api?.settings?.getExecutionDetails?.(this.resource);
    const command = details?.execCommand?.[0];
    if (command) {
      return command;
    }

    const config = vscode.workspace.getConfiguration("python", this.resource);
    const configured = config.get<string>("defaultInterpreterPath");
    if (configured) {
      return configured;
    }

    return undefined;
  }

  private async resolveCache(): Promise<InterpreterCache> {
    const path = await this.resolvePath();
    if (!path) {
      return { path: undefined, meetsMinimum: false };
    }

    return {
      path,
      meetsMinimum: await versionSupported(path, runSubprocess),
    };
  }

  private async cacheValue(): Promise<InterpreterCache> {
    const key = this.cacheKey();
    const existing = Python.cache.get(key);
    if (existing) {
      return existing;
    }

    const value = await this.resolveCache();
    Python.cache.set(key, value);
    return value;
  }

  invalidate(): void {
    Python.invalidate();
  }

  async path(): Promise<string | undefined> {
    return (await this.cacheValue()).path;
  }

  async meetsMinimumVersion(): Promise<boolean> {
    return (await this.cacheValue()).meetsMinimum;
  }
}

export async function versionSupported(
  python: string,
  run: typeof runSubprocess = runSubprocess,
): Promise<boolean> {
  const result = await run([python, "-c", VERSION_CHECK_SCRIPT]);
  return result.exit === 0;
}

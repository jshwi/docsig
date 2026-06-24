import * as vscode from "vscode";
import { SubprocessResult } from "./Subprocess";

export type CommandRunner = (
  command: string[],
  workingDirectory?: string,
) => Promise<SubprocessResult>;

export interface PythonLike {
  path(): Promise<string | undefined>;
  meetsMinimumVersion(): Promise<boolean>;
  invalidate(): void;
}

export interface CliDependencies {
  python?: PythonLike;
  resolveExecutable?: (context: vscode.ExtensionContext) => Promise<string>;
  runCommand?: CommandRunner;
  buildOptionArgs?: (folder?: vscode.WorkspaceFolder) => string[];
}

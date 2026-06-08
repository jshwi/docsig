import * as vscode from "vscode";
import * as Log from "../Log";
import { Issue } from "../models/Issue";
import { Options } from "../settings/Options";
import { CliDependencies } from "./CliDependencies";
import { executablePath } from "./Executable";
import { Python } from "./Python";
import { runSubprocess } from "./Subprocess";

/** Run the bundled docsig checker and parse JSON diagnostics. */
export class Cli {
  private readonly python: CliDependencies["python"];

  constructor(
    private readonly context: vscode.ExtensionContext,
    private readonly resource?: vscode.Uri,
    private readonly deps: CliDependencies = {},
  ) {
    this.python = deps.python ?? new Python(resource);
  }

  private folder(): vscode.WorkspaceFolder | undefined {
    return this.resource
      ? vscode.workspace.getWorkspaceFolder(this.resource)
      : undefined;
  }

  async isAvailable(): Promise<boolean> {
    return (await this.python!.path()) !== undefined;
  }

  async isPythonSupported(): Promise<boolean> {
    return this.python!.meetsMinimumVersion();
  }

  invalidatePythonCache(): void {
    this.python!.invalidate();
  }

  async run(file: string): Promise<Issue[]> {
    const interpreter = await this.python!.path();
    if (!interpreter) {
      return [];
    }

    if (!(await this.python!.meetsMinimumVersion())) {
      return [];
    }

    const resolveExecutable = this.deps.resolveExecutable ?? executablePath;
    const runCommand = this.deps.runCommand ?? runSubprocess;
    const exe = await resolveExecutable(this.context);
    const command: string[] = [interpreter, exe, file];

    const optionArgs =
      this.deps.buildOptionArgs?.(this.folder()) ??
      buildOptionArgs(this.folder());
    command.push(...optionArgs);

    const cwd = this.folder()?.uri.fsPath;
    Log.debug(command.join(" "));
    const result = await runCommand(command, cwd);
    if (!result.out) {
      return [];
    }

    try {
      return JSON.parse(result.out) as Issue[];
    } catch (error) {
      Log.warn(`parse failed path=${file} output=${result.out}`, error);
      return [];
    }
  }
}

function buildOptionArgs(folder?: vscode.WorkspaceFolder): string[] {
  const args: string[] = [];
  new Options(folder).addArgs((arg) => args.push(arg));
  return args;
}

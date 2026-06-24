import * as vscode from "vscode";
import { ClassCheckMode, classCheckFlag } from "./ClassCheckMode";
import { toCliPath } from "./ProjectPaths";

type ArgSink = (value: string) => void;

/** Map workspace settings to docsig CLI arguments. */
export class Options {
  constructor(private readonly folder?: vscode.WorkspaceFolder) {}

  addArgs(add: ArgSink): void {
    const config = vscode.workspace.getConfiguration(
      "docsig",
      this.folder?.uri,
    );

    const classMode = config.get<ClassCheckMode>(
      "classCheckMode",
      ClassCheckMode.None,
    );
    const classFlag = classCheckFlag(classMode);
    if (classFlag) {
      add(classFlag);
    }

    this.addBool(config, "checkDunders", "--check-dunders", add);
    this.addBool(config, "checkNested", "--check-nested", add);
    this.addBool(config, "checkOverridden", "--check-overridden", add);
    this.addBool(
      config,
      "checkPropertyReturns",
      "--check-property-returns",
      add,
    );
    this.addBool(config, "checkProtected", "--check-protected", add);
    this.addBool(
      config,
      "checkProtectedClassMethods",
      "--check-protected-class-methods",
      add,
    );
    this.addBool(config, "ignoreArgs", "--ignore-args", add);
    this.addBool(config, "ignoreKwargs", "--ignore-kwargs", add);
    this.addBool(config, "ignoreNoParams", "--ignore-no-params", add);
    this.addBool(config, "includeIgnored", "--include-ignored", add);

    const exclude = config.get<string>("exclude", "")?.trim();
    if (exclude) {
      add("--exclude");
      add(exclude);
    }

    const excludes = config.get<string[]>("excludes", []).filter(Boolean);
    if (excludes.length > 0) {
      add("--excludes");
      excludes.forEach((entry) =>
        add(toCliPath(this.folder?.uri.fsPath, entry)),
      );
    }

    const disable = config.get<string[]>("disable", []).filter(Boolean);
    if (disable.length > 0) {
      add("--disable");
      add(disable.join(","));
    }

    const target = config.get<string[]>("target", []).filter(Boolean);
    if (target.length > 0) {
      add("--target");
      add(target.join(","));
    }
  }

  private addBool(
    config: vscode.WorkspaceConfiguration,
    key: string,
    flag: string,
    add: ArgSink,
  ): void {
    if (config.get<boolean>(key, false)) {
      add(flag);
    }
  }
}

import * as vscode from "vscode";
import { MIN_MAJOR, MIN_MINOR } from "../cli/Python";

const missingNotified = new Set<string>();
const unsupportedNotified = new Set<string>();

function workspaceKey(folder?: vscode.WorkspaceFolder): string {
  return folder?.uri.fsPath ?? "__global__";
}

function notifyOnce(
  key: string,
  notified: Set<string>,
  title: string,
  message: string,
): void {
  if (notified.has(key)) {
    return;
  }

  notified.add(key);
  void vscode.window.showWarningMessage(`${title}: ${message}`);
}

/** Show one-time python interpreter warnings per workspace. */
export class Notifications {
  static resetForTests(): void {
    missingNotified.clear();
    unsupportedNotified.clear();
  }

  static missingNotificationCount(): number {
    return missingNotified.size;
  }

  static unsupportedNotificationCount(): number {
    return unsupportedNotified.size;
  }

  static notifyMissingPython(folder?: vscode.WorkspaceFolder): void {
    notifyOnce(
      workspaceKey(folder),
      missingNotified,
      "Docsig requires a Python interpreter",
      `No Python ${MIN_MAJOR}.${MIN_MINOR}+ interpreter is configured for this project`,
    );
  }

  static notifyUnsupportedPython(folder?: vscode.WorkspaceFolder): void {
    notifyOnce(
      workspaceKey(folder),
      unsupportedNotified,
      "Docsig requires a newer Python interpreter",
      `The configured python version is below minimum of ${MIN_MAJOR}.${MIN_MINOR}`,
    );
  }
}

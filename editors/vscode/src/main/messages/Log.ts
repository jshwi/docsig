import * as vscode from "vscode";

const PREFIX = "docsig";

let channel: vscode.OutputChannel | undefined;

/** Return the shared docsig output channel. */
export function outputChannel(): vscode.OutputChannel {
  if (!channel) {
    channel = vscode.window.createOutputChannel("Docsig");
  }

  return channel;
}

function emit(message: string): void {
  const line = `${PREFIX} ${message}`;
  outputChannel().appendLine(line);
  console.log(line);
}

/** Write a debug line to the docsig output channel. */
export function debug(message: string): void {
  emit(message);
}

/** Write a warning line to the docsig output channel. */
export function warn(message: string, error?: unknown): void {
  emit(message);
  console.warn(`${PREFIX} ${message}`, error);
}

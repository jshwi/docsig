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

/**
 * Close the shared channel so the next caller gets a fresh one.
 *
 * The channel is cached for the life of the process, so disposing it
 * without dropping the reference leaves every later write throwing
 * "Channel has been closed". Activate registers this rather than the
 * channel itself, which is what makes a second activate work.
 */
export function disposeChannel(): void {
  channel?.dispose();
  channel = undefined;
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

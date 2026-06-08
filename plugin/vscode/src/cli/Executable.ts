import { createHash } from "node:crypto";
import {
  copyFileSync,
  createReadStream,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import * as vscode from "vscode";
import * as Log from "../Log";

const BUNDLE_NAME = "docsig.pyz";
const BUFFER_SIZE = 8192;

let openReadStream: typeof createReadStream = createReadStream;

/** Reset or override the read-stream factory in unit tests. */
export function __setOpenReadStreamForTests(
  opener?: typeof createReadStream,
): void {
  openReadStream = opener ?? createReadStream;
}

function digestBuffer(data: Buffer): Buffer {
  return createHash("sha256").update(data).digest();
}

function digestFile(path: string): Promise<Buffer | undefined> {
  return new Promise((resolve) => {
    try {
      const hash = createHash("sha256");
      const stream = openReadStream(path, { highWaterMark: BUFFER_SIZE });

      stream.on("data", (chunk) => hash.update(chunk));
      stream.on("end", () => resolve(hash.digest()));
      stream.on("error", (error) => {
        Log.warn("cached digest failed", error);
        resolve(undefined);
      });
    } catch (error) {
      Log.warn("cached digest failed", error);
      resolve(undefined);
    }
  });
}

function bundledPath(extensionPath: string): string {
  return join(extensionPath, "resources", BUNDLE_NAME);
}

function cachePath(context: vscode.ExtensionContext): string {
  return join(context.globalStorageUri.fsPath, BUNDLE_NAME);
}

async function needsExtract(
  context: vscode.ExtensionContext,
): Promise<boolean> {
  const target = cachePath(context);
  if (!existsSync(target)) {
    return true;
  }

  const bundled = readFileSync(bundledPath(context.extensionPath));
  const bundledDigest = digestBuffer(bundled);
  const cachedDigest = await digestFile(target);
  if (!cachedDigest) {
    return true;
  }

  return !cachedDigest.equals(bundledDigest);
}

function extract(context: vscode.ExtensionContext): void {
  const source = bundledPath(context.extensionPath);
  if (!existsSync(source)) {
    throw new Error("missing bundled cli");
  }

  const target = cachePath(context);
  mkdirSync(context.globalStorageUri.fsPath, { recursive: true });

  const temp = join(tmpdir(), `${BUNDLE_NAME}.${process.pid}.tmp`);
  try {
    copyFileSync(source, temp);
    renameSync(temp, target);
    if (process.platform !== "win32") {
      writeFileSync(target, readFileSync(target), { mode: 0o755 });
    }
  } catch (error) {
    if (existsSync(temp)) {
      unlinkSync(temp);
    }
    throw error;
  }
}

/** Return the filesystem path to the bundled docsig executable. */
export async function executablePath(
  context: vscode.ExtensionContext,
): Promise<string> {
  if (await needsExtract(context)) {
    extract(context);
  }

  return cachePath(context);
}

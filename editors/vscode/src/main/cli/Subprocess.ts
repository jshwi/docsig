import { spawn } from "node:child_process";

export interface SubprocessResult {
  exit: number;
  out: string;
}

/** Run a command and capture merged stdout/stderr as utf-8 text. */
export function runSubprocess(
  command: string[],
  workingDirectory?: string,
): Promise<SubprocessResult> {
  return new Promise((resolve, reject) => {
    const [executable, ...args] = command;
    const proc = spawn(executable, args, {
      cwd: workingDirectory,
      env: { ...process.env, _DOCSIG_FORMAT_JSON: "true" },
      stdio: ["ignore", "pipe", "pipe"],
    });

    const chunks: Buffer[] = [];
    const onData = (chunk: Buffer) => chunks.push(chunk);

    proc.stdout.on("data", onData);
    proc.stderr.on("data", onData);

    proc.on("error", reject);
    proc.on("close", (code) => {
      resolve({
        exit: code ?? 1,
        out: Buffer.concat(chunks).toString("utf8").trim(),
      });
    });
  });
}

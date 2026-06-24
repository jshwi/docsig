import { posix } from "node:path";

function asPosix(value: string): string {
  return value.replace(/\\/g, "/");
}

/** Normalize a stored exclude path relative to the workspace root. */
export function fromStoredPath(
  base: string | undefined,
  input: string,
): string | null {
  const trimmed = input.trim();
  if (!trimmed) {
    return null;
  }

  if (!base) {
    return asPosix(trimmed);
  }

  const absolute = posix.resolve(base, trimmed);
  if (absolute.startsWith(base)) {
    return asPosix(absolute.slice(base.length + 1));
  }

  return asPosix(trimmed);
}

/** Resolve a stored path for docsig CLI argv. */
export function toCliPath(base: string | undefined, stored: string): string {
  const trimmed = stored.trim();
  if (!trimmed) {
    return "";
  }

  if (!base) {
    return posix.resolve(trimmed);
  }

  if (posix.isAbsolute(trimmed)) {
    return posix.normalize(trimmed);
  }

  return posix.normalize(posix.join(base, trimmed));
}

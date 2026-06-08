import { Issue } from "../models/Issue";

export interface CliLike {
  isAvailable(): Promise<boolean>;
  isPythonSupported(): Promise<boolean>;
  run(file: string): Promise<Issue[]>;
}

export interface DocsigServiceDependencies {
  cliFactory?: (path: string) => CliLike;
  debounceMs?: number;
  listVisiblePythonPaths?: () => string[];
}

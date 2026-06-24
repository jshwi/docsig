import * as vscode from "vscode";

type ConfigValues = Record<string, unknown>;

export function stubDocsigConfiguration(
  values: ConfigValues,
  section = "docsig",
): vscode.Disposable {
  const original = vscode.workspace.getConfiguration;
  const getConfiguration = (
    configSection?: string,
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    _scope?: vscode.ConfigurationScope,
  ): vscode.WorkspaceConfiguration => {
    if (configSection !== section && configSection !== undefined) {
      return original.call(vscode.workspace, configSection);
    }

    return {
      get: <T>(key: string, defaultValue?: T): T => {
        if (Object.prototype.hasOwnProperty.call(values, key)) {
          return values[key] as T;
        }
        return defaultValue as T;
      },
      has: (key: string) => Object.prototype.hasOwnProperty.call(values, key),
      inspect: () => undefined,
      update: async () => undefined,
    };
  };

  (
    vscode.workspace as { getConfiguration: typeof getConfiguration }
  ).getConfiguration = getConfiguration;

  return {
    dispose: () => {
      (
        vscode.workspace as { getConfiguration: typeof original }
      ).getConfiguration = original;
    },
  };
}

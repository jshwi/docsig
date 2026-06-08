import * as assert from "node:assert/strict";
import * as vscode from "vscode";
import { ClassCheckMode } from "../../settings/ClassCheckMode";
import { Options } from "../../settings/Options";
import { stubDocsigConfiguration } from "../support/mockConfiguration";

suite("Options", () => {
  function collectArgs(values: Record<string, unknown>): string[] {
    const disposable = stubDocsigConfiguration(values);
    const args: string[] = [];
    try {
      new Options().addArgs((arg) => args.push(arg));
    } finally {
      disposable.dispose();
    }
    return args;
  }

  test("apply adds bool flag when enabled", () => {
    const args = collectArgs({ checkDunders: true });
    assert.deepEqual(args, ["--check-dunders"]);
  });

  test("apply does not add bool flag when disabled", () => {
    const args = collectArgs({ checkDunders: false });
    assert.deepEqual(args, []);
  });

  test("apply emits class check flag", () => {
    const args = collectArgs({
      classCheckMode: ClassCheckMode.CheckClass,
    });
    assert.deepEqual(args, ["--check-class"]);
  });

  test("apply skips null class check flag", () => {
    const args = collectArgs({
      classCheckMode: ClassCheckMode.None,
    });
    assert.deepEqual(args, []);
  });

  test("apply adds exclude flag and normalized value", () => {
    const args = collectArgs({ exclude: "  value  " });
    assert.deepEqual(args, ["--exclude", "value"]);
  });

  test("apply skips blank exclude", () => {
    const args = collectArgs({ exclude: "   " });
    assert.deepEqual(args, []);
  });

  test("apply adds comma list flag and values", () => {
    const args = collectArgs({ disable: ["a", "b"] });
    assert.deepEqual(args, ["--disable", "a,b"]);
  });

  test("apply skips empty comma list", () => {
    const args = collectArgs({ disable: [] });
    assert.deepEqual(args, []);
  });

  test("apply adds target flag and values", () => {
    const args = collectArgs({ target: ["SIG001", "SIG002"] });
    assert.deepEqual(args, ["--target", "SIG001,SIG002"]);
  });

  test("apply adds whitespace list flag and tokens", () => {
    const base = "/tmp/docsig-workspace";
    const folder = {
      uri: vscode.Uri.file(base),
    } as vscode.WorkspaceFolder;
    const disposable = stubDocsigConfiguration({
      excludes: ["a", "b"],
    });
    const args: string[] = [];
    try {
      new Options(folder).addArgs((arg) => args.push(arg));
    } finally {
      disposable.dispose();
    }

    assert.deepEqual(args, ["--excludes", `${base}/a`, `${base}/b`]);
  });
});

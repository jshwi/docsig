import * as assert from "node:assert/strict";
import { Cli } from "../../main/cli/Cli";
import { SubprocessResult } from "../../main/cli/Subprocess";
import { mockExtensionContext } from "../support/MockContext";
import { stubDocsigConfiguration } from "../support/MockConfiguration";

suite("Cli", () => {
  const context = mockExtensionContext(
    "/tmp/docsig-ext",
    "/tmp/docsig-storage",
  );

  function cli(
    interpreter: string | undefined,
    versionSupported = true,
    runCommand?: (command: string[]) => Promise<SubprocessResult>,
  ): Cli {
    return new Cli(context, undefined, {
      python: {
        path: async () => interpreter,
        meetsMinimumVersion: async () =>
          interpreter !== undefined && versionSupported,
        invalidate: () => undefined,
      },
      resolveExecutable: async () => "/bundled/docsig.pyz",
      runCommand: runCommand ?? (async () => ({ exit: 0, out: "" })),
      buildOptionArgs: () => [],
    });
  }

  test("run returns empty list when unavailable", async () => {
    const result = await cli(undefined).run("test.py");
    assert.deepEqual(result, []);
  });

  test("run returns empty list when output empty", async () => {
    const result = await cli("python").run("test.py");
    assert.deepEqual(result, []);
  });

  test("run parses json issues", async () => {
    const result = await cli("python", true, async () => ({
      exit: 0,
      out: '[{"message":"bad","line":1,"exit":1}]',
    })).run("test.py");

    assert.equal(result.length, 1);
    assert.equal(result[0]?.message, "bad");
    assert.equal(result[0]?.line, 1);
    assert.equal(result[0]?.exit, 1);
  });

  test("run returns empty list on invalid json", async () => {
    const result = await cli("python", true, async () => ({
      exit: 0,
      out: "not json",
    })).run("test.py");

    assert.deepEqual(result, []);
  });

  test("isAvailable returns false", async () => {
    assert.equal(await cli(undefined).isAvailable(), false);
  });

  test("isAvailable returns true", async () => {
    assert.equal(await cli("python").isAvailable(), true);
  });

  test("isPythonSupported returns false when version too old", async () => {
    assert.equal(await cli("python", false).isPythonSupported(), false);
  });

  test("isPythonSupported returns true when version ok", async () => {
    assert.equal(await cli("python", true).isPythonSupported(), true);
  });

  test("run returns empty list when python version unsupported", async () => {
    let called = false;
    const result = await cli("python", false, async () => {
      called = true;
      return { exit: 0, out: "[]" };
    }).run("test.py");

    assert.deepEqual(result, []);
    assert.equal(called, false);
  });

  test("run handles non zero exit", async () => {
    const result = await cli("python", true, async () => ({
      exit: 1,
      out: "[]",
    })).run("test.py");

    assert.deepEqual(result, []);
  });

  test("run executes full command path", async () => {
    let command: string[] = [];
    const result = await cli("python3", true, async (cmd) => {
      command = cmd;
      return { exit: 0, out: "[]" };
    }).run("test.py");

    assert.deepEqual(result, []);
    assert.equal(command[0], "python3");
    assert.equal(command[1], "/bundled/docsig.pyz");
    assert.equal(command[2], "test.py");
  });

  test("invalidatePythonCache delegates to python", () => {
    let invalidated = false;
    const subject = new Cli(context, undefined, {
      python: {
        path: async () => "python",
        meetsMinimumVersion: async () => true,
        invalidate: () => {
          invalidated = true;
        },
      },
      resolveExecutable: async () => "/bundled/docsig.pyz",
      runCommand: async () => ({ exit: 0, out: "" }),
      buildOptionArgs: () => [],
    });

    subject.invalidatePythonCache();

    assert.equal(invalidated, true);
  });

  test("run includes option args from workspace settings", async () => {
    const disposable = stubDocsigConfiguration({ checkNested: true });
    let command: string[] = [];

    try {
      const subject = new Cli(context, undefined, {
        python: {
          path: async () => "python",
          meetsMinimumVersion: async () => true,
          invalidate: () => undefined,
        },
        resolveExecutable: async () => "/bundled/docsig.pyz",
        runCommand: async (cmd) => {
          command = cmd;
          return { exit: 0, out: "[]" };
        },
      });

      await subject.run("test.py");
    } finally {
      disposable.dispose();
    }

    assert.ok(command.includes("--check-nested"));
  });

  test("run throws when bundled pyz stream is absent", async () => {
    const subject = new Cli(context, undefined, {
      python: {
        path: async () => "python3",
        meetsMinimumVersion: async () => true,
        invalidate: () => undefined,
      },
      resolveExecutable: async () => {
        throw new Error("missing bundled cli");
      },
      runCommand: async () => {
        throw new Error("subprocess must not run when bundled cli is absent");
      },
      buildOptionArgs: () => [],
    });

    await assert.rejects(
      () => subject.run("test.py"),
      (error: Error) => error.message.includes("missing bundled cli"),
    );
  });
});

import * as assert from "node:assert/strict";
import * as sinon from "sinon";
import * as vscode from "vscode";
import { Python, versionSupported } from "../../cli/Python";
import * as Subprocess from "../../cli/Subprocess";
import { stubDocsigConfiguration } from "../support/mockConfiguration";

function stubPythonExtension(
  extension: vscode.Extension<unknown> | undefined,
): void {
  const getExtension = vscode.extensions.getExtension as sinon.SinonStub;
  getExtension.returns(extension);
}

suite("Python", () => {
  setup(() => {
    sinon.stub(vscode.extensions, "getExtension").returns(undefined);
  });

  teardown(() => {
    sinon.restore();
    Python.invalidate();
  });

  test("path returns configured interpreter", async () => {
    const disposable = stubDocsigConfiguration(
      { defaultInterpreterPath: "/usr/bin/python3" },
      "python",
    );

    try {
      const path = await new Python().path();
      assert.equal(path, "/usr/bin/python3");
    } finally {
      disposable.dispose();
    }
  });

  test("path returns undefined when no interpreter", async () => {
    const disposable = stubDocsigConfiguration({}, "python");
    try {
      const path = await new Python().path();
      assert.equal(path, undefined);
    } finally {
      disposable.dispose();
    }
  });

  test("versionSupported returns true when check exits zero", async () => {
    const supported = await versionSupported("python3", async (command) => {
      assert.equal(command[0], "python3");
      assert.equal(command[1], "-c");
      return { exit: 0, out: "" };
    });

    assert.equal(supported, true);
  });

  test("versionSupported returns false when check exits non zero", async () => {
    const supported = await versionSupported("python3", async () => ({
      exit: 1,
      out: "",
    }));

    assert.equal(supported, false);
  });

  test("path resolves from python extension environment uri", async () => {
    Python.invalidate();
    sinon.stub(Subprocess, "runSubprocess").resolves({ exit: 0, out: "" });
    const activate = sinon.stub().resolves();
    stubPythonExtension({
      isActive: false,
      activate,
      exports: {
        environments: {
          resolveEnvironment: async () => ({
            executable: { uri: vscode.Uri.file("/env/python") },
          }),
        },
      },
    } as unknown as vscode.Extension<unknown>);

    const path = await new Python().path();

    assert.equal(path, "/env/python");
    assert.equal(activate.called, true);
  });

  test("path resolves from python extension environment path", async () => {
    Python.invalidate();
    sinon.stub(Subprocess, "runSubprocess").resolves({ exit: 0, out: "" });
    stubPythonExtension({
      isActive: true,
      exports: {
        environments: {
          resolveEnvironment: async () => ({ path: "/legacy/python" }),
        },
      },
    } as unknown as vscode.Extension<unknown>);

    const path = await new Python().path();

    assert.equal(path, "/legacy/python");
  });

  test("path resolves from python execution details", async () => {
    Python.invalidate();
    sinon.stub(Subprocess, "runSubprocess").resolves({ exit: 0, out: "" });
    stubPythonExtension({
      isActive: true,
      exports: {
        settings: {
          getExecutionDetails: async () => ({
            execCommand: ["/details/python"],
          }),
        },
      },
    } as unknown as vscode.Extension<unknown>);

    const path = await new Python().path();

    assert.equal(path, "/details/python");
  });

  test("path reuses cached interpreter value", async () => {
    Python.invalidate();
    const runSubprocess = sinon
      .stub(Subprocess, "runSubprocess")
      .resolves({ exit: 0, out: "" });
    const disposable = stubDocsigConfiguration(
      { defaultInterpreterPath: "/usr/bin/python3" },
      "python",
    );

    try {
      const subject = new Python();
      const first = await subject.path();
      const second = await subject.path();

      assert.equal(first, "/usr/bin/python3");
      assert.equal(second, "/usr/bin/python3");
      assert.equal(runSubprocess.callCount, 1);
    } finally {
      runSubprocess.restore();
      disposable.dispose();
    }
  });

  test("invalidate clears cached interpreter", async () => {
    Python.invalidate();
    const runSubprocess = sinon
      .stub(Subprocess, "runSubprocess")
      .resolves({ exit: 0, out: "" });
    const disposable = stubDocsigConfiguration(
      { defaultInterpreterPath: "/usr/bin/python3" },
      "python",
    );

    try {
      const subject = new Python();
      await subject.path();
      subject.invalidate();
      await subject.path();
    } finally {
      runSubprocess.restore();
      disposable.dispose();
    }

    assert.equal(runSubprocess.callCount, 2);
  });

  test("meetsMinimumVersion returns false when no interpreter", async () => {
    const disposable = stubDocsigConfiguration({}, "python");
    try {
      const supported = await new Python().meetsMinimumVersion();
      assert.equal(supported, false);
    } finally {
      disposable.dispose();
    }
  });
});

import * as assert from "node:assert/strict";
import * as sinon from "sinon";
import * as vscode from "vscode";
import { Cli } from "../../main/cli/Cli";
import { Notifications } from "../../main/messages/Notifications";
import { DocsigService } from "../../main/service/DocsigService";
import { CliLike } from "../../main/service/DocsigServiceDependencies";
import { mockExtensionContext } from "../support/MockContext";

suite("DocsigService", () => {
  let collection: vscode.DiagnosticCollection;
  let context: vscode.ExtensionContext;
  let clock: sinon.SinonFakeTimers;

  setup(() => {
    context = mockExtensionContext("/tmp/docsig-ext", "/tmp/docsig-storage");
    collection = vscode.languages.createDiagnosticCollection("docsig-test");
    clock = sinon.useFakeTimers({ shouldClearNativeTimers: true });
    Notifications.resetForTests();
  });

  teardown(() => {
    clock.restore();
    collection.dispose();
    sinon.restore();
    Notifications.resetForTests();
  });

  function mockCli(overrides: Partial<CliLike> = {}): CliLike {
    return {
      isAvailable: async () => true,
      isPythonSupported: async () => true,
      run: async () => [],
      ...overrides,
    };
  }

  function service(
    cliFactory: (path: string) => CliLike,
    listVisiblePythonPaths?: () => string[],
  ): DocsigService {
    return new DocsigService(context, collection, {
      cliFactory,
      debounceMs: 600,
      listVisiblePythonPaths,
    });
  }

  test("hasCached reflects cache contents", async () => {
    const cli = mockCli({
      run: async () => [{ line: 1, message: "m", exit: 1 }],
    });
    const subject = service(() => cli);

    assert.equal(subject.hasCached("/z.py"), false);
    await subject.runNow("/z.py");
    assert.equal(subject.hasCached("/z.py"), true);
  });

  test("getIssues returns empty when path unknown", () => {
    const subject = service(() => mockCli());
    assert.deepEqual(subject.getIssues("/no/such/path"), []);
  });

  test("scheduleFromSave notifies when python interpreter missing", async () => {
    const warn = sinon.stub(vscode.window, "showWarningMessage");
    const cli = mockCli({ isAvailable: async () => false });
    const subject = service(() => cli);

    subject.scheduleFromSave("/x.py");
    await clock.tickAsync(600);

    assert.equal(warn.callCount, 1);
    assert.match(String(warn.firstCall.args[0]), /Python interpreter/);
  });

  test("ensureFresh notifies when python interpreter missing", async () => {
    const warn = sinon.stub(vscode.window, "showWarningMessage");
    const cli = mockCli({ isAvailable: async () => false });
    const subject = service(() => cli);

    subject.ensureFresh("/x.py");
    await clock.tickAsync(600);

    assert.equal(warn.callCount, 1);
  });

  test("scheduleFromSave notifies when python version unsupported", async () => {
    const warn = sinon.stub(vscode.window, "showWarningMessage");
    const cli = mockCli({ isPythonSupported: async () => false });
    const subject = service(() => cli);

    subject.scheduleFromSave("/x.py");
    await clock.tickAsync(600);

    assert.equal(warn.callCount, 1);
    assert.match(String(warn.firstCall.args[0]), /newer Python/);
  });

  test("ensureFresh notifies when python version unsupported", async () => {
    const warn = sinon.stub(vscode.window, "showWarningMessage");
    const cli = mockCli({ isPythonSupported: async () => false });
    const subject = service(() => cli);

    subject.ensureFresh("/x.py");
    await clock.tickAsync(600);

    assert.equal(warn.callCount, 1);
  });

  test("runNow skips when path already in flight", async () => {
    let release!: () => void;
    const blocked = new Promise<void>((resolve) => {
      release = resolve;
    });
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        await blocked;
        return [];
      },
    });
    const subject = service(() => cli);

    const first = subject.runNow("/busy.py");
    const second = subject.runNow("/busy.py");
    release();
    await first;
    await second;

    assert.equal(runs, 1);
  });

  test("runNow updates cache from cli", async () => {
    const cli = mockCli({
      run: async () => [{ line: 1, message: "m", exit: 1 }],
    });
    const subject = service(() => cli);

    await subject.runNow("/c.py");

    assert.deepEqual(subject.getIssues("/c.py"), [
      { line: 1, message: "m", exit: 1 },
    ]);
  });

  test("runNow applies merge when cli returns global error", async () => {
    let call = 0;
    const cli = mockCli({
      run: async () => {
        call += 1;
        if (call === 1) {
          return [{ line: null, message: "g", exit: 2 }];
        }
        return [{ line: 1, message: "line", exit: 1 }];
      },
    });
    const subject = service(() => cli);

    await subject.runNow("/d.py");
    await subject.runNow("/d.py");

    assert.deepEqual(subject.getIssues("/d.py"), [
      { line: 1, message: "line", exit: 1 },
    ]);
  });

  test("scheduleFromSave runs cli when available", async () => {
    let ran = false;
    const cli = mockCli({
      run: async (path) => {
        assert.equal(path, "/g.py");
        ran = true;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.scheduleFromSave("/g.py");
    await clock.tickAsync(600);

    assert.equal(ran, true);
  });

  test("ensureFresh runs cli when available", async () => {
    let ran = false;
    const cli = mockCli({
      run: async () => {
        ran = true;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.ensureFresh("/h.py");
    await clock.tickAsync(600);

    assert.equal(ran, true);
  });

  test("ensureFresh coalesces when idle alarm already has pending work", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.ensureFresh("/i.py");
    subject.ensureFresh("/i.py");
    await clock.tickAsync(600);

    assert.equal(runs, 1);
  });

  test("scheduleAfterSettingsChange clears cache then runs cli", async () => {
    let ran = false;
    const cli = mockCli({
      run: async (path) => {
        if (path === "/cached.py") {
          ran = true;
        }
        return [];
      },
    });
    const subject = service(
      () => cli,
      () => [],
    );
    await subject.runNow("/cached.py");

    assert.equal(subject.hasCached("/cached.py"), true);
    subject.scheduleAfterSettingsChange();
    assert.equal(subject.hasCached("/cached.py"), false);
    await clock.tickAsync(600);

    assert.equal(ran, true);
    assert.equal(subject.hasCached("/cached.py"), true);
  });

  test("scheduleAfterSettingsChange includes open python files", async () => {
    const paths: string[] = [];
    const cli = mockCli({
      run: async (path) => {
        paths.push(path);
        return [];
      },
    });
    const subject = service(
      () => cli,
      () => ["/open.py"],
    );

    subject.scheduleAfterSettingsChange();
    await clock.tickAsync(600);

    assert.deepEqual(paths, ["/open.py"]);
  });

  test("dispose clears pending idle timers", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.ensureFresh("/idle-dispose.py");
    subject.dispose();
    await clock.tickAsync(600);

    assert.equal(runs, 0);
  });

  test("ensureFresh does not queue duplicate idle work", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.ensureFresh("/dup-idle.py");
    subject.ensureFresh("/dup-idle.py");
    await clock.tickAsync(600);

    assert.equal(runs, 1);
  });

  test("schedule skips duplicate alarm without debounce reset", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);
    type ScheduleSubject = {
      saveAlarms: Map<string, NodeJS.Timeout>;
      schedule: (
        path: string,
        alarmMap: Map<string, NodeJS.Timeout>,
        resetDebounce: boolean,
      ) => void;
    };
    const internal = subject as unknown as ScheduleSubject;

    internal.schedule("/debounce.py", internal.saveAlarms, false);
    internal.schedule("/debounce.py", internal.saveAlarms, false);
    await clock.tickAsync(600);

    assert.equal(runs, 1);
  });

  test("runNow uses default cli when factory omitted", async () => {
    sinon.stub(Cli.prototype, "isAvailable").resolves(true);
    sinon.stub(Cli.prototype, "isPythonSupported").resolves(true);
    sinon.stub(Cli.prototype, "run").resolves([]);

    const subject = new DocsigService(context, collection, {
      debounceMs: 600,
    });

    await subject.runNow("/default-cli.py");
  });

  test("dispose clears pending save timers", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.scheduleFromSave("/dispose.py");
    subject.dispose();
    await clock.tickAsync(600);

    assert.equal(runs, 0);
  });

  test("publishCached returns when path is not cached", async () => {
    const subject = service(() => mockCli());

    await subject.publishCached("/missing.py");
  });

  test("scheduleAfterSettingsChange is no-op when no paths", () => {
    const subject = service(
      () => mockCli(),
      () => [],
    );

    subject.scheduleAfterSettingsChange();
  });

  test("runNow skips publishing when document is not open", async () => {
    sinon.stub(vscode.workspace, "textDocuments").value([]);
    const cli = mockCli({
      run: async () => [{ line: 1, message: "m", exit: 1 }],
    });
    const subject = service(() => cli);

    await subject.runNow("/closed.py");

    assert.equal(collection.has(vscode.Uri.file("/closed.py")), false);
  });

  test("publishCached publishes diagnostics for open document", async () => {
    const uri = vscode.Uri.file("/pub.py");
    const document = {
      uri,
      languageId: "python",
      lineCount: 1,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;
    sinon.stub(vscode.workspace, "textDocuments").value([document]);
    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    const cli = mockCli({
      run: async () => [{ line: 1, message: "warn", exit: 1 }],
    });
    const subject = service(() => cli);
    await subject.runNow(uri.fsPath);
    collection.delete(uri);

    await subject.publishCached(uri.fsPath);

    const diagnostics = collection.get(uri);
    assert.equal(diagnostics?.length, 1);
    assert.equal(diagnostics?.[0]?.message, "warn");
  });

  test("runNow clears diagnostics when cli returns no issues", async () => {
    const uri = vscode.Uri.file("/clear.py");
    const document = {
      uri,
      languageId: "python",
      lineCount: 1,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;
    sinon.stub(vscode.workspace, "textDocuments").value([document]);
    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    let calls = 0;
    const cli = mockCli({
      run: async () => {
        calls += 1;
        if (calls === 1) {
          return [{ line: 1, message: "old", exit: 1 }];
        }
        return [];
      },
    });
    const subject = service(() => cli);

    await subject.runNow(uri.fsPath);
    assert.equal(collection.get(uri)?.length, 1);

    await subject.runNow(uri.fsPath);

    assert.equal(collection.has(uri), false);
  });

  test("runNow publishes error severity for exit code two", async () => {
    const uri = vscode.Uri.file("/err.py");
    const document = {
      uri,
      languageId: "python",
      lineCount: 1,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;
    sinon.stub(vscode.workspace, "textDocuments").value([document]);
    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    const cli = mockCli({
      run: async () => [{ line: 1, message: "fatal", exit: 2 }],
    });
    const subject = service(() => cli);

    await subject.runNow(uri.fsPath);

    assert.equal(
      collection.get(uri)?.[0]?.severity,
      vscode.DiagnosticSeverity.Error,
    );
  });

  test("refreshOpenDocuments republishes cached diagnostics", async () => {
    const uri = vscode.Uri.file("/refresh.py");
    const document = {
      uri,
      languageId: "python",
      lineCount: 1,
      lineAt: () => ({ text: "pass" }),
    } as unknown as vscode.TextDocument;
    sinon.stub(vscode.workspace, "textDocuments").value([document]);
    sinon.stub(vscode.commands, "executeCommand").resolves([]);

    const cli = mockCli({
      run: async () => [{ line: 1, message: "cached", exit: 1 }],
    });
    const subject = service(() => cli);
    await subject.runNow(uri.fsPath);
    collection.delete(uri);

    await subject.refreshOpenDocuments();

    assert.equal(collection.get(uri)?.[0]?.message, "cached");
  });

  test("scheduleFromSave resets debounce timer before queueing work", async () => {
    let runs = 0;
    const cli = mockCli({
      run: async () => {
        runs += 1;
        return [];
      },
    });
    const subject = service(() => cli);

    subject.scheduleFromSave("/save.py");
    await clock.tickAsync(300);
    subject.scheduleFromSave("/save.py");
    await clock.tickAsync(300);
    assert.equal(runs, 0);
    await clock.tickAsync(300);

    assert.equal(runs, 1);
  });
});

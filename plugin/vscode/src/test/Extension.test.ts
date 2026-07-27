import * as assert from "node:assert/strict";
import * as sinon from "sinon";
import * as vscode from "vscode";
import * as Log from "../main/messages/Log";
import {
  ServiceLike,
  activate,
  attach,
  deactivate,
  onChange,
  onConfigurationChange,
  onSave,
} from "../main/extension";
import { mockExtensionContext } from "./support/MockContext";

interface RecordingService extends ServiceLike {
  calls: string[];
  cached: Set<string>;
}

function recordingService(cached: string[] = []): RecordingService {
  const calls: string[] = [];
  return {
    calls,
    cached: new Set(cached),
    hasCached(path) {
      return this.cached.has(path);
    },
    async publishCached(path) {
      calls.push(`publishCached:${path}`);
    },
    ensureFresh(path) {
      calls.push(`ensureFresh:${path}`);
    },
    scheduleFromSave(path) {
      calls.push(`scheduleFromSave:${path}`);
    },
    invalidateExternalChange(path) {
      calls.push(`invalidate:${path}`);
    },
    scheduleAfterSettingsChange() {
      calls.push("settings");
    },
  };
}

function document(
  languageId: string,
  scheme = "file",
  path = "/a.py",
): vscode.TextDocument {
  return {
    languageId,
    uri: { scheme, fsPath: path } as vscode.Uri,
  } as vscode.TextDocument;
}

function configurationEvent(
  affected: string[],
): vscode.ConfigurationChangeEvent {
  return {
    affectsConfiguration: (section: string) => affected.includes(section),
  };
}

function disposeAll(context: vscode.ExtensionContext): void {
  context.subscriptions.forEach((subscription) => {
    subscription.dispose();
  });
  context.subscriptions.length = 0;
}

suite("extension", () => {
  teardown(() => {
    sinon.restore();
  });

  test("attach publishes what is already cached", () => {
    const service = recordingService(["/a.py"]);

    attach(service, document("python"));

    assert.deepEqual(service.calls, ["publishCached:/a.py"]);
  });

  test("attach schedules a run for an unseen file", () => {
    const service = recordingService();

    attach(service, document("python"));

    assert.deepEqual(service.calls, ["ensureFresh:/a.py"]);
  });

  test("attach ignores a non python document", () => {
    const service = recordingService();

    attach(service, document("markdown"));

    assert.deepEqual(service.calls, []);
  });

  test("attach ignores a document outside the file system", () => {
    const service = recordingService();

    attach(service, document("python", "untitled"));

    assert.deepEqual(service.calls, []);
  });

  test("onChange schedules an idle run", () => {
    const service = recordingService();

    onChange(service, document("python"));

    assert.deepEqual(service.calls, ["ensureFresh:/a.py"]);
  });

  test("onChange ignores a non python document", () => {
    const service = recordingService();

    onChange(service, document("plaintext"));

    assert.deepEqual(service.calls, []);
  });

  test("onSave schedules a save run", () => {
    const service = recordingService();

    onSave(service, document("python"));

    assert.deepEqual(service.calls, ["scheduleFromSave:/a.py"]);
  });

  test("onSave ignores a non python document", () => {
    const service = recordingService();

    onSave(service, document("plaintext"));

    assert.deepEqual(service.calls, []);
  });

  test("onConfigurationChange reruns for a docsig setting", () => {
    const service = recordingService();

    onConfigurationChange(service, configurationEvent(["docsig"]));

    assert.deepEqual(service.calls, ["settings"]);
  });

  test("onConfigurationChange reruns for a python setting", () => {
    const service = recordingService();

    onConfigurationChange(service, configurationEvent(["python"]));

    assert.deepEqual(service.calls, ["settings"]);
  });

  test("onConfigurationChange ignores an unrelated setting", () => {
    const service = recordingService();

    onConfigurationChange(service, configurationEvent(["editor"]));

    assert.deepEqual(service.calls, []);
  });

  test("activate registers its subscriptions", () => {
    const context = mockExtensionContext("/tmp/docsig-ext", "/tmp/docsig-st");
    sinon.stub(vscode.window, "visibleTextEditors").value([]);

    activate(context);

    try {
      assert.ok(context.subscriptions.length > 0);
    } finally {
      disposeAll(context);
    }
  });

  test("activate attaches to already visible python editors", () => {
    const context = mockExtensionContext("/tmp/docsig-ext", "/tmp/docsig-st");
    const opened = document("python", "file", "/visible.py");
    sinon
      .stub(vscode.window, "visibleTextEditors")
      .value([{ document: opened }]);

    activate(context);

    try {
      assert.ok(context.subscriptions.length > 0);
    } finally {
      disposeAll(context);
    }
  });

  test("activate runs a second time after a full dispose", () => {
    const context = mockExtensionContext("/tmp/docsig-ext", "/tmp/docsig-st");
    sinon.stub(vscode.window, "visibleTextEditors").value([]);

    activate(context);
    disposeAll(context);

    // the channel registered above is Log's cached one; if disposing it
    // did not drop the cache, this second run would throw "Channel has
    // been closed" from the first line of activate
    activate(context);

    try {
      Log.debug("still writable");
      assert.ok(context.subscriptions.length > 0);
    } finally {
      disposeAll(context);
    }
  });

  test("deactivate is a no-op", () => {
    assert.equal(deactivate(), undefined);
  });
});

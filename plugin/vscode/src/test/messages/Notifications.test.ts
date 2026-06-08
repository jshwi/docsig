import * as assert from "node:assert/strict";
import * as sinon from "sinon";
import * as vscode from "vscode";
import { Notifications } from "../../main/messages/Notifications";

suite("Notifications", () => {
  setup(() => {
    Notifications.resetForTests();
  });

  teardown(() => {
    sinon.restore();
    Notifications.resetForTests();
  });

  test("notifyMissingPython creates warning notification once", () => {
    const folder = {
      uri: vscode.Uri.file("/workspace-a"),
    } as vscode.WorkspaceFolder;
    const showWarning = sinon
      .stub(vscode.window, "showWarningMessage")
      .resolves(undefined);

    Notifications.notifyMissingPython(folder);
    Notifications.notifyMissingPython(folder);

    assert.equal(Notifications.missingNotificationCount(), 1);
    assert.equal(showWarning.callCount, 1);
  });

  test("notifyUnsupportedPython creates warning notification once", () => {
    const folder = {
      uri: vscode.Uri.file("/workspace-b"),
    } as vscode.WorkspaceFolder;
    const showWarning = sinon
      .stub(vscode.window, "showWarningMessage")
      .resolves(undefined);

    Notifications.notifyUnsupportedPython(folder);
    Notifications.notifyUnsupportedPython(folder);

    assert.equal(Notifications.unsupportedNotificationCount(), 1);
    assert.equal(showWarning.callCount, 1);
  });
});

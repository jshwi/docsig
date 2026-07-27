import * as assert from "node:assert/strict";
import { disposeChannel, outputChannel } from "../../main/messages/Log";

suite("Log", () => {
  test("outputChannel returns the same channel while cached", () => {
    assert.equal(outputChannel(), outputChannel());
  });

  test("disposeChannel drops the cache so the next call rebuilds", () => {
    const first = outputChannel();

    disposeChannel();

    const second = outputChannel();

    assert.notEqual(first, second);

    // the replacement is usable; the old one is closed for good
    second.appendLine("after dispose");
  });

  test("disposeChannel is safe with nothing cached", () => {
    disposeChannel();

    assert.doesNotThrow(() => {
      disposeChannel();
    });
  });
});

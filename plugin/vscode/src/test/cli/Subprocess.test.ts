import * as assert from "node:assert/strict";
import { runSubprocess } from "../../cli/Subprocess";

suite("Subprocess", () => {
  test("run trims output", async () => {
    const result = await runSubprocess(["python3", "-c", "print('  []  ')"]);

    assert.equal(result.exit, 0);
    assert.equal(result.out, "[]");
  });

  test("run starts real process for python version", async () => {
    const result = await runSubprocess(["python3", "--version"]);

    assert.equal(result.exit, 0);
    assert.notEqual(result.out, "");
  });
});

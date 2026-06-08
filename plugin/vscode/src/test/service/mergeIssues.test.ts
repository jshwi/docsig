import * as assert from "node:assert/strict";
import { Issue } from "../../models/Issue";
import { mergeIssues } from "../../service/mergeIssues";

suite("mergeIssues", () => {
  test("returns new issues when no global error", () => {
    const merged = mergeIssues(
      [{ line: 1, message: "old", exit: 1 }],
      [{ line: 2, message: "new", exit: 1 }],
    );

    assert.deepEqual(merged, [{ line: 2, message: "new", exit: 1 }]);
  });

  test("keeps prior line issues when global error", () => {
    const merged = mergeIssues(
      [
        { line: 1, message: "stale line", exit: 1 },
        { line: null, message: "old global", exit: 2 },
      ],
      [
        { line: null, message: "fresh global", exit: 2 },
        { line: 9, message: "ignored line from cli", exit: 1 },
      ],
    );

    assert.deepEqual(merged, [
      { line: 1, message: "stale line", exit: 1 },
      { line: null, message: "fresh global", exit: 2 },
    ]);
  });

  test("treats exit 2 with line as not global error", () => {
    const issues: Issue[] = [{ line: 3, message: "line error", exit: 2 }];
    assert.deepEqual(mergeIssues([], issues), issues);
  });

  test("global error drops line issues when cache empty", () => {
    const merged = mergeIssues(undefined, [
      { line: null, message: "global", exit: 2 },
      { line: 5, message: "line", exit: 1 },
    ]);

    assert.deepEqual(merged, [{ line: null, message: "global", exit: 2 }]);
  });
});

import * as assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fromStoredPath, toCliPath } from "../../main/settings/ProjectPaths";

suite("ProjectPaths", () => {
  let base: string;

  setup(() => {
    base = mkdtempSync(join(tmpdir(), "docsig-paths-"));
    mkdirSync(join(base, "foo"), { recursive: true });
  });

  teardown(() => {
    rmSync(base, { recursive: true, force: true });
  });

  test("fromStoredPath maps paths under base to relative", () => {
    const rel = fromStoredPath(base, "./this/path");
    assert.equal(rel, "this/path");
  });

  test("toCliPath resolves relative stored paths against base", () => {
    const abs = toCliPath(base, "foo/bar");
    assert.equal(abs, resolve(base, "foo/bar").replace(/\\/g, "/"));
  });

  test("fromStoredPath returns null for blank input", () => {
    assert.equal(fromStoredPath(base, "   "), null);
  });

  test("fromStoredPath normalizes backslashes when base path missing", () => {
    assert.equal(fromStoredPath(undefined, "a\\b"), "a/b");
  });

  test("fromStoredPath relativizes absolute paths under base", () => {
    const absolute = resolve(base, "foo/bar");
    assert.equal(fromStoredPath(base, absolute), "foo/bar");
  });

  test("fromStoredPath keeps input when resolved path is outside base", () => {
    assert.equal(fromStoredPath(base, "../outside"), "../outside");
  });

  test("toCliPath returns empty for blank stored path", () => {
    assert.equal(toCliPath(base, "  "), "");
  });

  test("toCliPath resolves against cwd when base path missing", () => {
    const expected = resolve("relative").replace(/\\/g, "/");
    assert.equal(toCliPath(undefined, "relative"), expected);
  });

  test("toCliPath normalizes absolute stored paths", () => {
    const stored = join(base, "sub", "dir");
    const cli = toCliPath(base, stored);
    assert.equal(cli, resolve(stored).replace(/\\/g, "/"));
  });
});

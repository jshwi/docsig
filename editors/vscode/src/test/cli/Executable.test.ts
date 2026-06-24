import * as assert from "node:assert/strict";
import {
  chmodSync,
  createReadStream,
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  __setOpenReadStreamForTests,
  executablePath,
} from "../../main/cli/Executable";
import { mockExtensionContext } from "../support/MockContext";

suite("Executable", () => {
  const root = join(tmpdir(), `docsig-exe-test-${process.pid}`);
  const extensionPath = join(root, "ext");
  const storagePath = join(root, "storage");
  const bundled = join(extensionPath, "resources", "docsig.pyz");

  suiteSetup(() => {
    mkdirSync(join(extensionPath, "resources"), { recursive: true });
    mkdirSync(storagePath, { recursive: true });
    writeFileSync(bundled, "bundled-cli");
  });

  suiteTeardown(() => {
    rmSync(root, { recursive: true, force: true });
  });

  setup(() => {
    __setOpenReadStreamForTests();
    const cached = join(storagePath, "docsig.pyz");
    if (existsSync(cached)) {
      rmSync(cached, { recursive: true, force: true });
    }
  });

  teardown(() => {
    __setOpenReadStreamForTests();
  });

  test("path extracts bundled cli when cache missing", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const path = await executablePath(context);
    const cached = join(storagePath, "docsig.pyz");

    assert.equal(path, cached);
    assert.equal(existsSync(cached), true);
    assert.ok(readFileSync(cached).length > 0);
  });

  test("path replaces stale cached bundle", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const cached = join(storagePath, "docsig.pyz");
    writeFileSync(cached, "broken");

    const path = await executablePath(context);

    assert.equal(path, cached);
    assert.ok(readFileSync(cached).length > "broken".length);
  });

  test("path throws when bundled cli is missing", async () => {
    const missingRoot = join(tmpdir(), `docsig-exe-missing-${process.pid}`);
    const missingExt = join(missingRoot, "ext");
    const missingStorage = join(missingRoot, "storage");
    mkdirSync(missingExt, { recursive: true });
    mkdirSync(missingStorage, { recursive: true });

    try {
      const context = mockExtensionContext(missingExt, missingStorage);
      await assert.rejects(
        () => executablePath(context),
        (error: Error) => error.message.includes("missing bundled cli"),
      );
    } finally {
      rmSync(missingRoot, { recursive: true, force: true });
    }
  });

  test("path re-extracts when cached digest throws synchronously", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const cached = join(storagePath, "docsig.pyz");
    writeFileSync(cached, "stale");
    __setOpenReadStreamForTests((path, options) => {
      if (path === cached) {
        throw new Error("cannot open cache");
      }
      return createReadStream(path, options);
    });

    await executablePath(context);
    assert.equal(readFileSync(cached).toString(), "bundled-cli");
  });

  test("path re-extracts when cached digest fails", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const cached = join(storagePath, "docsig.pyz");
    writeFileSync(cached, "stale");
    chmodSync(cached, 0o000);

    try {
      await executablePath(context);
      chmodSync(cached, 0o644);
      assert.equal(readFileSync(cached).toString(), "bundled-cli");
    } finally {
      if (existsSync(cached)) {
        chmodSync(cached, 0o644);
      }
    }
  });

  test("path removes temp file when extract fails", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const cached = join(storagePath, "docsig.pyz");
    mkdirSync(cached, { recursive: true });

    try {
      await assert.rejects(() => executablePath(context));
      const temp = join(tmpdir(), `docsig.pyz.${process.pid}.tmp`);
      assert.equal(existsSync(temp), false);
    } finally {
      rmSync(cached, { recursive: true, force: true });
    }
  });

  test("path reuses valid cached bundle", async () => {
    const context = mockExtensionContext(extensionPath, storagePath);
    const first = await executablePath(context);
    const cached = join(storagePath, "docsig.pyz");
    const modified = readFileSync(cached);
    const second = await executablePath(context);

    assert.equal(first, second);
    assert.deepEqual(readFileSync(cached), modified);
  });
});

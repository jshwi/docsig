import * as assert from "node:assert/strict";
import { ClassCheckMode, classCheckFlag } from "../../settings/ClassCheckMode";

suite("ClassCheckMode", () => {
  test("none emits no flag", () => {
    assert.equal(classCheckFlag(ClassCheckMode.None), null);
  });

  test("check class emits flag", () => {
    assert.equal(classCheckFlag(ClassCheckMode.CheckClass), "--check-class");
  });

  test("check class constructor emits flag", () => {
    assert.equal(
      classCheckFlag(ClassCheckMode.CheckClassConstructor),
      "--check-class-constructor",
    );
  });
});

describe("class_check_mode", function()
  local class_check_mode = require("docsig.class_check_mode")

  it("none emits no flag", function()
    assert.is_not.truthy(class_check_mode.flag("None"))
  end)

  it("check class emits flag", function()
    assert.equals(class_check_mode.flag("Check class"), "--check-class")
  end)

  it("check class constructor emits flag", function()
    assert.equals(
      class_check_mode.flag("Check class constructor"),
      "--check-class-constructor"
    )
  end)
end)

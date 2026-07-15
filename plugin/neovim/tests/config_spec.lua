describe("config", function()
  local config = require("docsig.config")

  it("resolve merges user options over defaults", function()
    local resolved = config.resolve({ check_nested = true, debounce_ms = 100 })

    assert.equals(resolved.check_nested, true)
    assert.equals(resolved.debounce_ms, 100)
    assert.equals(resolved.check_dunders, false)
  end)

  it("resolve returns defaults when opts omitted", function()
    local resolved = config.resolve()
    assert.same(resolved.check_nested, config.defaults.check_nested)
    assert.same(resolved.class_check_mode, config.defaults.class_check_mode)
  end)
end)

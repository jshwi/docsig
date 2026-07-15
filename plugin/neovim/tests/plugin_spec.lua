describe("plugin", function()
  local service_mock = {
    dispose = function() end,
    ensure_fresh = function() end,
    publish_cached = function() end,
    schedule_from_save = function() end,
    detach = function() end,
    schedule_after_settings_change = function() end,
    has_cached = function()
      return false
    end,
  }

  package.loaded["docsig.service"] = service_mock

  it("plugin loader calls setup when enabled", function()
    package.loaded["docsig"] = nil
    package.loaded["docsig.init"] = nil
    vim.g.docsig = { debounce_ms = 0 }
    dofile(vim.g.docsig_test_root .. "/plugin/docsig.lua")
    assert.truthy(require("docsig").is_setup())
  end)

  it("plugin loader skips setup when disabled", function()
    vim.g.docsig = false
    package.loaded["docsig"] = nil
    package.loaded["docsig.init"] = nil
    dofile(vim.g.docsig_test_root .. "/plugin/docsig.lua")
  end)

  it("plugin commands register DocsigRefresh", function()
    dofile(vim.g.docsig_test_root .. "/plugin/docsig-commands.lua")
    assert.equals(vim.fn.exists(":DocsigRefresh"), 2)
  end)
end)

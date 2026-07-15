describe("executable", function()
  local executable = require("docsig.executable")

  it("path returns configured executable", function()
    assert.equals(executable.path("/custom/docsig.pyz"), "/custom/docsig.pyz")
  end)

  it("path returns bundled executable", function()
    local path = executable.path(nil)
    assert.truthy(path:match("docsig%.pyz$") or path:match("docsig$"))
  end)

  local function with_mocked_discovery(mock_filereadable, mock_exepath, fn)
    local old_filereadable = vim.fn.filereadable
    local old_exepath = vim.fn.exepath
    vim.fn.filereadable = function(path)
      return mock_filereadable(path, old_filereadable)
    end

    vim.fn.exepath = function(name)
      return mock_exepath(name, old_exepath)
    end

    package.loaded["docsig.executable"] = nil
    local ok, err = pcall(fn)
    vim.fn.filereadable = old_filereadable
    vim.fn.exepath = old_exepath
    package.loaded["docsig.executable"] = nil
    if not ok then error(err, 0) end
  end

  it("path prefers bundled resources executable", function()
    with_mocked_discovery(function(path)
      if path:match("resources/docsig%.pyz$") then return 1 end
      return 0
    end, function(name, old_exepath)
      if name == "docsig" then return "" end
      return old_exepath(name)
    end, function()
      local bundled = require("docsig.executable")
      assert.truthy(bundled.path(nil):match("resources/docsig%.pyz$"))
    end)
  end)

  it("path errors when bundled executable is missing", function()
    with_mocked_discovery(function()
      return 0
    end, function(name, old_exepath)
      if name == "docsig" then return "" end
      return old_exepath(name)
    end, function()
      local missing = require("docsig.executable")
      local ok = pcall(missing.path, nil)
      assert.is_not.truthy(ok)
    end)
  end)

  it("path falls back to docsig on path", function()
    with_mocked_discovery(function()
      return 0
    end, function(name, old_exepath)
      if name == "docsig" then return "/usr/local/bin/docsig" end
      return old_exepath(name)
    end, function()
      local from_path = require("docsig.executable")
      assert.equals(from_path.path(nil), "/usr/local/bin/docsig")
    end)
  end)

  it("path errors when plugin is not on runtimepath", function()
    local old_runtime_file = vim.api.nvim_get_runtime_file
    vim.api.nvim_get_runtime_file = function(pattern, _)
      if pattern == "lua/docsig/executable.lua" then return {} end
      return old_runtime_file(pattern, _)
    end

    package.loaded["docsig.executable"] = nil

    local ok = pcall(function()
      require("docsig.executable").path(nil)
    end)
    vim.api.nvim_get_runtime_file = old_runtime_file
    package.loaded["docsig.executable"] = nil
    assert.is_not.truthy(ok)
  end)
end)

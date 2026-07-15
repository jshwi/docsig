describe("init", function()
  local config = require("docsig.config")
  local diagnostics = require("docsig.diagnostics")

  local state = { available = true, supported = true, issues = {} }

  package.loaded["docsig.python"] = {
    invalidate = function() end,
    workspace_root = function()
      return vim.g.docsig_test_root
    end,
    MIN_MAJOR = 3,
    MIN_MINOR = 10,
  }

  package.loaded["docsig.cli"] = {
    is_available = function()
      return state.available
    end,
    is_python_supported = function()
      return state.supported
    end,
    run = function(_, _, _, on_complete)
      on_complete(state.issues)
    end,
  }

  package.loaded["docsig.service"] = nil
  package.loaded["docsig"] = nil
  package.loaded["docsig.init"] = nil

  local service = require("docsig.service")
  local docsig = require("docsig")

  local function temp_buf(suffix)
    return docsig_test.temp_py_buf(suffix)
  end

  local function cfg()
    return config.resolve({ debounce_ms = 0 })
  end

  local function reset_state()
    state.available = true
    state.supported = true
    state.issues = {}
    service.dispose()
  end

  it("setup registers plugin", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    assert.truthy(docsig.is_setup())
    docsig.setup({ debounce_ms = 0 })
  end)

  it("setup publishes cached diagnostics on attach", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-cache")
    state.issues = {
      {
        line = 1,
        message = "SIG101: missing (function-doc-missing)",
        exit = 1,
      },
    }
    service.run_docsig(cfg(), path, bufnr)
    vim.wait(1000, function()
      return service.has_cached(path)
    end)
    diagnostics.clear(bufnr)
    vim.api.nvim_exec_autocmds(
      { "BufEnter", "BufReadPost" },
      { buffer = bufnr, modeline = false }
    )
    vim.wait(1000, function()
      return #vim.diagnostic.get(
        bufnr,
        { namespace = diagnostics.namespace() }
      ) > 0
    end)
    assert.equals(
      #vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() }),
      1
    )
  end)

  it("text changed autocmd schedules docsig", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-text")
    vim.api.nvim_exec_autocmds(
      "TextChanged",
      { buffer = bufnr, modeline = false }
    )
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("save autocmd schedules docsig", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-save")
    vim.api.nvim_exec_autocmds(
      "BufWritePost",
      { buffer = bufnr, modeline = false }
    )
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("buf unload autocmd detaches buffer", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-unload")
    state.issues = {
      {
        line = 1,
        message = "SIG101: missing (function-doc-missing)",
        exit = 1,
      },
    }
    service.run_docsig(cfg(), path, bufnr)
    vim.wait(1000, function()
      return service.has_cached(path)
    end)
    vim.api.nvim_exec_autocmds(
      "BufUnload",
      { buffer = bufnr, modeline = false }
    )
    assert.equals(
      #vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() }),
      0
    )
  end)

  it("refresh delegates to service", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-refresh")
    docsig.refresh(bufnr)
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("setup registers the DocsigRefresh command", function()
    reset_state()
    docsig.setup({ debounce_ms = 0 })
    local bufnr, path = temp_buf("init-command")
    vim.api.nvim_set_current_buf(bufnr)
    vim.cmd.DocsigRefresh()
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("on_settings_changed delegates to service", function()
    reset_state()
    local bufnr, path = temp_buf("init-settings")
    state.issues = {
      {
        line = 1,
        message = "SIG101: missing (function-doc-missing)",
        exit = 1,
      },
    }
    docsig.setup({ debounce_ms = 0 })
    service.run_docsig(cfg(), path, bufnr)
    vim.wait(1000, function()
      return service.has_cached(path)
    end)
    docsig.on_settings_changed()
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("setup rejects neovim versions below 0.10", function()
    reset_state()
    local old_has = vim.fn.has
    vim.fn.has = function(feature)
      if feature == "nvim-0.10" then return 0 end
      return old_has(feature)
    end

    package.loaded["docsig"] = nil
    package.loaded["docsig.init"] = nil
    local guarded = require("docsig")
    guarded.setup({ debounce_ms = 0 })
    assert.is_not.truthy(guarded.is_setup())
    vim.fn.has = old_has
  end)
end)

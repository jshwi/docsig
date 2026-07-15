describe("service", function()
  local config = require("docsig.config")
  local diagnostics = require("docsig.diagnostics")
  local notifications = require("docsig.notifications")

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
  local service = require("docsig.service")

  local function cfg()
    return config.resolve({ debounce_ms = 0 })
  end

  local function temp_buf(suffix)
    return docsig_test.temp_py_buf(suffix)
  end

  local function reset_state()
    state.available = true
    state.supported = true
    state.issues = {}
    service.dispose()
    notifications.reset_for_tests()
  end

  it("run_docsig publishes diagnostics", function()
    reset_state()
    state.issues = {
      {
        line = 1,
        message = "SIG101: missing (function-doc-missing)",
        exit = 1,
      },
    }
    local bufnr, path = temp_buf("service")
    service.run_docsig(cfg(), path, bufnr)
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

  it("run_docsig notifies when python missing", function()
    reset_state()
    state.available = false
    service.run_docsig(cfg(), "/missing.py", 0)
  end)

  it("run_docsig notifies when python unsupported", function()
    reset_state()
    state.supported = false
    service.run_docsig(cfg(), "/old.py", 0)
  end)

  it("run_docsig notifies when python missing for path-only runs", function()
    reset_state()
    local path = docsig_test.write_temp_py(
      docsig_test.temp_py_path("path-only-missing-python")
    )
    state.available = false
    service.run_docsig(cfg(), path)
  end)

  it(
    "run_docsig notifies when python unsupported for path-only runs",
    function()
      reset_state()
      local path = docsig_test.write_temp_py(
        docsig_test.temp_py_path("path-only-unsupported-python")
      )
      state.supported = false
      service.run_docsig(cfg(), path)
    end
  )

  it("run_docsig skips when path already in flight", function()
    reset_state()
    local path =
      docsig_test.write_temp_py(docsig_test.temp_py_path("in-flight"))
    service.run_docsig(cfg(), path)
    service.run_docsig(cfg(), path)
    vim.wait(1000, function()
      return false
    end)
  end)

  it("has_cached reflects cache contents", function()
    reset_state()
    local bufnr, path = temp_buf("cached")
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
    assert.truthy(service.has_cached(path))
  end)

  it("publish_cached publishes diagnostics for open buffer", function()
    reset_state()
    local bufnr, path = temp_buf("publish_cached")
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
    service.publish_cached(bufnr)
    assert.equals(
      #vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() }),
      1
    )
  end)

  it("ensure_fresh schedules docsig for python buffers", function()
    reset_state()
    local bufnr, path = temp_buf("idle")
    service.ensure_fresh(cfg(), bufnr)
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("ensure_fresh ignores non-python buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, "/tmp/docsig-idle-ignore.txt")
    vim.bo[bufnr].filetype = "text"
    service.ensure_fresh(cfg(), bufnr)
  end)

  it("schedule_from_save runs docsig", function()
    reset_state()
    local bufnr, path = temp_buf("save")
    service.schedule_from_save(cfg(), bufnr)
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("schedule_after_settings_change clears cache then reruns", function()
    local bufnr, path = temp_buf("settings")
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
    service.schedule_after_settings_change(cfg())
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("detach clears timers and diagnostics", function()
    reset_state()
    local bufnr, _ = temp_buf("detach")
    service.ensure_fresh(cfg(), bufnr)
    service.detach(bufnr)
    assert.equals(
      #vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() }),
      0
    )
  end)

  it("publish_for_path ignores missing buffer", function()
    reset_state()
    service.publish_for_path("/not-open.py")
  end)

  it("ensure_fresh ignores unnamed python buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.bo[bufnr].filetype = "python"
    service.ensure_fresh(cfg(), bufnr)
  end)

  it("ensure_fresh ignores scheme python buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, "python:///virtual/file.py")
    vim.bo[bufnr].filetype = "python"
    service.ensure_fresh(cfg(), bufnr)
  end)

  it("ensure_fresh ignores python buffers missing on disk", function()
    reset_state()
    local path = docsig_test.temp_py_path_missing("on-disk")
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, path)
    vim.bo[bufnr].filetype = "python"
    service.ensure_fresh(cfg(), bufnr)
    vim.wait(500)
    assert.is_not.truthy(service.has_cached(path))
  end)

  it("run_docsig ignores paths missing on disk", function()
    reset_state()
    local path = docsig_test.temp_py_path_missing("run-docsig")
    service.run_docsig(cfg(), path)
    assert.is_not.truthy(service.has_cached(path))
  end)

  it("ensure_fresh coalesces pending idle schedules", function()
    reset_state()
    local bufnr, path = temp_buf("idle-coalesce")
    service.ensure_fresh(cfg(), bufnr)
    service.ensure_fresh(cfg(), bufnr)
    vim.wait(2000, function()
      return service.has_cached(path)
    end)
    assert.truthy(service.has_cached(path))
  end)

  it("schedule_from_save ignores non-python buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, "/tmp/docsig-save-ignore.txt")
    vim.bo[bufnr].filetype = "text"
    service.schedule_from_save(cfg(), bufnr)
  end)

  it("publish_cached returns early without cache", function()
    reset_state()
    local bufnr, _ = temp_buf("publish-miss")
    service.publish_cached(bufnr)
  end)

  it("publish_cached ignores non-python buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.bo[bufnr].filetype = "text"
    service.publish_cached(bufnr)
  end)

  it("detach ignores unnamed buffers", function()
    reset_state()
    local bufnr = vim.api.nvim_create_buf(false, true)
    service.detach(bufnr)
  end)

  it("dispose clears active timers", function()
    reset_state()
    local cfg_long = config.resolve({ debounce_ms = 10000 })
    local bufnr, _ = temp_buf("dispose-timers")
    service.ensure_fresh(cfg_long, bufnr)
    service.schedule_from_save(cfg_long, bufnr)
    service.dispose()
  end)
end)

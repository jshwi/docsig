describe("python", function()
  local python = require("docsig.python")
  local config = require("docsig.config")

  local counter = 0

  local function temp_buf(suffix)
    counter = counter + 1
    local path = vim.g.docsig_test_root
      .. "/"
      .. suffix
      .. "-"
      .. counter
      .. ".py"
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, path)
    return bufnr, path
  end

  it("version_supported returns true for modern python", function()
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then return end

    assert.truthy(python.version_supported(interpreter))
  end)

  it("version_supported returns false for rejected exit code", function()
    assert.is_not.truthy(python.version_supported("/bin/false", function()
      return { exit = 1, out = "" }
    end))
  end)

  it("version_supported returns false when subprocess fails", function()
    assert.is_not.truthy(python.version_supported("/missing/python", function()
      error("ENOENT")
    end))
  end)

  it("path uses configured python", function()
    python.invalidate()
    local bufnr = temp_buf("configured")
    local cfg = config.resolve({ python = vim.fn.exepath("python3") })
    assert.equals(python.path(bufnr, cfg), cfg.python)
  end)

  it("path returns interpreter but marks unsupported when missing", function()
    python.invalidate()
    local bufnr = temp_buf("missing")
    local cfg = config.resolve({ python = "/missing/python" })
    assert.equals(python.path(bufnr, cfg), "/missing/python")
    assert.is_not.truthy(python.meets_minimum_version(bufnr, cfg))
  end)

  it("workspace_root finds repository root from buffer path", function()
    local bufnr = temp_buf("root")
    local repo_root = vim.fn.fnamemodify(vim.g.docsig_test_root, ":h:h")
    assert.equals(python.workspace_root(bufnr), repo_root)
  end)

  it("invalidate clears cached interpreter", function()
    python.invalidate()
    local bufnr, _ = temp_buf("cache")
    local cfg = config.resolve({ python = vim.fn.exepath("python3") })
    python.path(bufnr, cfg)
    python.invalidate()
    assert.equals(python.path(bufnr, cfg), cfg.python)
  end)

  it("meets_minimum_version uses cache", function()
    python.invalidate()
    local bufnr = temp_buf("minimum")
    local cfg = config.resolve({ python = vim.fn.exepath("python3") })
    if cfg.python == "" then return end

    assert.truthy(python.meets_minimum_version(bufnr, cfg))
    assert.truthy(python.meets_minimum_version(bufnr, cfg))
  end)

  it("path uses python3_host_prog when configured", function()
    python.invalidate()
    vim.g.python3_host_prog = vim.fn.exepath("python3")
    if vim.g.python3_host_prog == "" then return end

    local bufnr = temp_buf("host-prog")
    local cfg = config.resolve({})
    assert.equals(python.path(bufnr, cfg), vim.g.python3_host_prog)
    vim.g.python3_host_prog = nil
  end)

  it("workspace_root returns nil for unnamed buffers", function()
    local bufnr = vim.api.nvim_create_buf(false, true)
    assert.is_not.truthy(python.workspace_root(bufnr))
  end)

  it("path handles unnamed buffers", function()
    python.invalidate()
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then return end

    local bufnr = vim.api.nvim_create_buf(false, true)
    local cfg = config.resolve({ python = interpreter })
    assert.equals(python.path(bufnr, cfg), interpreter)
  end)

  it("workspace_root finds git directory", function()
    counter = counter + 1
    local root = (os.getenv("TMPDIR") or "/tmp")
      .. "/docsig-python-git-"
      .. counter
    vim.fn.mkdir(root .. "/.git", "p")
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, root .. "/module.py")
    assert.equals(
      vim.fn.resolve(python.workspace_root(bufnr)),
      vim.fn.resolve(root)
    )
    vim.fn.delete(root, "rf")
  end)

  it("workspace_root falls back to file directory", function()
    counter = counter + 1
    local base = (os.getenv("TMPDIR") or "/tmp")
      .. "/docsig-python-root-"
      .. counter
    vim.fn.mkdir(base, "p")
    local bufnr = vim.api.nvim_create_buf(false, true)
    local path = base .. "/module.py"
    vim.api.nvim_buf_set_name(bufnr, path)
    assert.equals(
      vim.fn.resolve(python.workspace_root(bufnr)),
      vim.fn.resolve(base)
    )
    vim.fn.delete(base, "rf")
  end)

  it("path returns nil when no interpreter is available", function()
    python.invalidate()
    vim.g.python3_host_prog = nil
    local old_exepath = vim.fn.exepath
    vim.fn.exepath = function()
      return ""
    end

    local bufnr = temp_buf("no-interpreter")
    local cfg = config.resolve({})
    assert.is_not.truthy(python.path(bufnr, cfg))
    vim.fn.exepath = old_exepath
  end)

  it("path uses interpreter cache", function()
    python.invalidate()
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then return end

    local bufnr = temp_buf("cache-hit")
    local cfg = config.resolve({ python = interpreter })
    assert.equals(python.path(bufnr, cfg), interpreter)
    assert.equals(python.path(bufnr, cfg), interpreter)
  end)

  it("path resolves interpreter from path when unset", function()
    python.invalidate()
    vim.g.python3_host_prog = nil
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then interpreter = vim.fn.exepath("python") end
    if interpreter == "" then return end

    local bufnr = temp_buf("path-resolve")
    local cfg = config.resolve({})
    assert.equals(python.path(bufnr, cfg), interpreter)
  end)

  it("meets_minimum_version returns false without interpreter", function()
    python.invalidate()
    vim.g.python3_host_prog = nil
    local old_exepath = vim.fn.exepath
    vim.fn.exepath = function()
      return ""
    end

    local bufnr = temp_buf("minimum-missing")
    local cfg = config.resolve({})
    assert.is_not.truthy(python.meets_minimum_version(bufnr, cfg))
    vim.fn.exepath = old_exepath
  end)
end)

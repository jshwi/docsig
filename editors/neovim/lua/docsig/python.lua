local M = {}

M.MIN_MAJOR = 3
M.MIN_MINOR = 10

local VERSION_CHECK_SCRIPT = table.concat({
  "import sys;",
  string.format("min_versions = (%d, %d);", M.MIN_MAJOR, M.MIN_MINOR),
  "sys.exit(0 if sys.version_info >= min_versions else 1)",
})

local cache = {}

local function workspace_root(bufnr)
  local name = vim.api.nvim_buf_get_name(bufnr or 0)
  if name == "" then return nil end

  local dir = vim.fs.dirname(name)
  while dir and dir ~= "" do
    if vim.fn.filereadable(vim.fs.joinpath(dir, "pyproject.toml")) == 1 then
      return dir
    end
    if vim.fn.isdirectory(vim.fs.joinpath(dir, ".git")) == 1 then
      return dir
    end
    local parent = vim.fs.dirname(dir)
    if parent == dir then break end
    dir = parent
  end

  return vim.fs.dirname(name)
end

local function cache_key(bufnr)
  local root = workspace_root(bufnr)
  if root then return root end

  return ""
end

local function configured_python()
  if vim.g.python3_host_prog and vim.g.python3_host_prog ~= "" then
    return vim.g.python3_host_prog
  end

  return nil
end

local function resolve_path(_, config)
  if config.python and config.python ~= "" then return config.python end

  local configured = configured_python()
  if configured then return configured end

  local from_path = vim.fn.exepath("python3")
  if from_path ~= "" then return from_path end

  return vim.fn.exepath("python")
end

function M.version_supported(python, subprocess)
  local run = subprocess or require("docsig.subprocess").run_sync
  local ok, result = pcall(run, { python, "-c", VERSION_CHECK_SCRIPT })
  if not ok then return false end

  return result.exit == 0
end

function M.invalidate()
  cache = {}
end

function M.workspace_root(bufnr)
  return workspace_root(bufnr)
end

function M.path(bufnr, config)
  local key = cache_key(bufnr)
  local entry = cache[key]
  if entry then return entry.path end

  local path = resolve_path(bufnr, config)
  if not path or path == "" then
    cache[key] = { path = nil, meets_minimum = false }
    return nil
  end

  local subprocess = require("docsig.subprocess")
  local meets_minimum = M.version_supported(path, subprocess.run_sync)
  cache[key] = { path = path, meets_minimum = meets_minimum }
  return path
end

function M.meets_minimum_version(bufnr, config)
  local key = cache_key(bufnr)
  local entry = cache[key]
  if entry then return entry.meets_minimum end

  M.path(bufnr, config)
  entry = cache[key]
  return entry and entry.meets_minimum or false
end

return M

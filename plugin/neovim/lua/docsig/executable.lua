local M = {}

local BUNDLE_NAME = "docsig.pyz"

local function plugin_root()
  local runtime =
    vim.api.nvim_get_runtime_file("lua/docsig/executable.lua", false)[1]
  if not runtime then error("docsig plugin is not on runtimepath") end

  return vim.fn.fnamemodify(runtime, ":p:h:h:h")
end

local function bundled_candidates()
  local root = plugin_root()
  return {
    vim.fs.joinpath(root, "resources", BUNDLE_NAME),
    vim.fs.joinpath(root, "build", BUNDLE_NAME),
    vim.fs.joinpath(root, "..", "..", "build", BUNDLE_NAME),
  }
end

local function find_bundled()
  for _, path in ipairs(bundled_candidates()) do
    if vim.fn.filereadable(path) == 1 then
      return vim.fn.fnamemodify(path, ":p")
    end
  end

  local from_path = vim.fn.exepath("docsig")
  if from_path ~= "" then return from_path end

  return nil
end

local function missing_bundle_error()
  local root = plugin_root()
  error(
    "missing docsig executable; run "
      .. string.format("make -C %s bundle", root)
      .. " or set executable in require('docsig').setup()"
  )
end

function M.path(user_executable)
  if user_executable and user_executable ~= "" then return user_executable end

  local bundled = find_bundled()
  if not bundled then missing_bundle_error() end

  return bundled
end

return M

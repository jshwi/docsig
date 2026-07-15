local config = require("docsig.config")
local executable = require("docsig.executable")
local python = require("docsig.python")

local M = {}

local function resolved_config()
  local user = vim.g.docsig
  if type(user) ~= "table" then user = {} end
  return config.resolve(user)
end

function M.check(reporter)
  local health = reporter or vim.health

  health.start("docsig")

  if vim.fn.has("nvim-0.10") == 1 then
    health.ok("Neovim 0.10+")
  else
    health.error("docsig.nvim requires Neovim 0.10 or newer")
  end

  local cfg = resolved_config()

  local python_path = python.path(0, cfg)
  if not python_path then
    health.error(
      "no Python interpreter found",
      "set g:python3_host_prog or the python option in setup()"
    )
  elseif python.version_supported(python_path) then
    health.ok("Python: " .. python_path)
  else
    health.error(
      string.format(
        "Python below minimum version %d.%d: %s",
        python.MIN_MAJOR,
        python.MIN_MINOR,
        python_path
      )
    )
  end

  local ok, path_or_err = pcall(executable.path, cfg.executable)
  if ok then
    health.ok("docsig executable: " .. path_or_err)
  else
    health.error(path_or_err, "run make bundle in the plugin directory")
  end
end

return M

local python = require("docsig.python")

local M = {}

local missing_notified = {}
local unsupported_notified = {}

local function workspace_key(bufnr)
  local root = require("docsig.python").workspace_root(bufnr)
  return root or "__global__"
end

local function notify_once(key, notified, title, message)
  if notified[key] then return end

  notified[key] = true
  vim.notify(string.format("%s: %s", title, message), vim.log.levels.WARN)
end

function M.reset_for_tests()
  missing_notified = {}
  unsupported_notified = {}
end

function M.notify_missing_python(bufnr)
  notify_once(
    workspace_key(bufnr),
    missing_notified,
    "Docsig requires a Python interpreter",
    string.format(
      "No Python %d.%d+ interpreter is configured for this project",
      python.MIN_MAJOR,
      python.MIN_MINOR
    )
  )
end

function M.notify_unsupported_python(bufnr)
  notify_once(
    workspace_key(bufnr),
    unsupported_notified,
    "Docsig requires a newer Python interpreter",
    string.format(
      "The configured python version is below minimum of %d.%d",
      python.MIN_MAJOR,
      python.MIN_MINOR
    )
  )
end

return M

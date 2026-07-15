local executable = require("docsig.executable")
local log = require("docsig.log")
local options = require("docsig.options")
local python = require("docsig.python")
local subprocess = require("docsig.subprocess")

local M = {}

function M.is_available(bufnr, config)
  return python.path(bufnr, config) ~= nil
end

function M.is_python_supported(bufnr, config)
  return python.meets_minimum_version(bufnr, config)
end

function M.run_sync(file, bufnr, config)
  local interpreter = python.path(bufnr, config)
  if not interpreter then return {} end

  if not python.meets_minimum_version(bufnr, config) then return {} end

  local exe = executable.path(config.executable)
  local root = python.workspace_root(bufnr)
  local command = { interpreter, exe, file }
  vim.list_extend(command, options.build_args(config, root))

  log.debug(table.concat(command, " "))
  local result = subprocess.run_sync(command, root)
  if result.out == "" then return {} end

  local ok, parsed = pcall(vim.json.decode, result.out)
  if not ok then
    log.warn("parse failed path=" .. file .. " output=" .. result.out)
    return {}
  end

  return parsed
end

function M.run(file, bufnr, config, on_complete)
  local interpreter = python.path(bufnr, config)
  if not interpreter then
    on_complete({})
    return
  end

  if not python.meets_minimum_version(bufnr, config) then
    on_complete({})
    return
  end

  local exe = executable.path(config.executable)
  local root = python.workspace_root(bufnr)
  local command = { interpreter, exe, file }
  vim.list_extend(command, options.build_args(config, root))

  log.debug(table.concat(command, " "))
  subprocess.run(command, root, function(result)
    if result.out == "" then
      on_complete({})
      return
    end

    local ok, parsed = pcall(vim.json.decode, result.out)
    if not ok then
      log.warn("parse failed path=" .. file .. " output=" .. result.out)
      on_complete({})
      return
    end

    on_complete(parsed)
  end)
end

return M

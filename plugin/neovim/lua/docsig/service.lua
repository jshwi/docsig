local cli = require("docsig.cli")
local diagnostics = require("docsig.diagnostics")
local log = require("docsig.log")
local merge_issues = require("docsig.merge_issues")
local notifications = require("docsig.notifications")
local python = require("docsig.python")

local M = {}

local cache = {}
local in_flight = {}
local save_timers = {}
local idle_timers = {}
local idle_pending = {}
local path_to_bufnr = {}

local function is_local_python(bufnr)
  if vim.bo[bufnr].filetype ~= "python" then return false end

  local name = vim.api.nvim_buf_get_name(bufnr)
  if name == "" then return false end

  if name:match("^%w+://") then return false end

  if vim.fn.filereadable(name) ~= 1 then return false end

  return true
end

local function path_for_bufnr(bufnr)
  return vim.api.nvim_buf_get_name(bufnr)
end

local function bufnr_for_path(path)
  return path_to_bufnr[path]
end

local function track_bufnr(bufnr)
  local path = path_for_bufnr(bufnr)
  if path ~= "" then path_to_bufnr[path] = bufnr end
end

local function clear_timer(timer_map, path)
  local timer = timer_map[path]
  if timer then
    timer:stop()
    timer:close()
    timer_map[path] = nil
  end
end

local function schedule(config, path, bufnr, timer_map, reset_debounce, source)
  log.debug(string.format("%s scheduled path=%s", source, path))

  local is_idle = timer_map == idle_timers
  if is_idle and idle_pending[path] then return end

  if reset_debounce then clear_timer(timer_map, path) end

  if is_idle then idle_pending[path] = true end

  local timer = vim.uv.new_timer()
  timer_map[path] = timer
  timer:start(config.debounce_ms, 0, function()
    vim.schedule(function()
      clear_timer(timer_map, path)
      if is_idle then idle_pending[path] = nil end
      M.run_docsig(config, path, bufnr)
    end)
  end)
end

function M.run_docsig(config, path, bufnr)
  if bufnr then
    if not is_local_python(bufnr) then return end
  elseif vim.fn.filereadable(path) ~= 1 then
    return
  end

  if bufnr then path_to_bufnr[path] = bufnr end

  if not cli.is_available(bufnr, config) then
    notifications.notify_missing_python(bufnr)
    return
  end

  if not cli.is_python_supported(bufnr, config) then
    notifications.notify_unsupported_python(bufnr)
    return
  end

  if in_flight[path] then return end

  in_flight[path] = true
  cli.run(path, bufnr, config, function(issues)
    vim.schedule(function()
      in_flight[path] = nil
      cache[path] = merge_issues.merge(cache[path], issues)
      M.publish_for_path(path)
    end)
  end)
end

function M.publish_for_path(path)
  local bufnr = bufnr_for_path(path)
  if not bufnr or not vim.api.nvim_buf_is_valid(bufnr) then return end

  diagnostics.publish(bufnr, cache[path] or {})
end

function M.has_cached(path)
  return cache[path] ~= nil
end

function M.ensure_fresh(config, bufnr)
  if not is_local_python(bufnr) then return end

  track_bufnr(bufnr)
  schedule(config, path_for_bufnr(bufnr), bufnr, idle_timers, false, "idle")
end

function M.schedule_from_save(config, bufnr)
  if not is_local_python(bufnr) then return end

  track_bufnr(bufnr)
  local path = path_for_bufnr(bufnr)
  log.debug("save trigger path=" .. path)
  schedule(config, path, bufnr, save_timers, true, "save")
end

function M.publish_cached(bufnr)
  if not is_local_python(bufnr) then return end

  local path = path_for_bufnr(bufnr)
  if not M.has_cached(path) then return end

  M.publish_for_path(path)
end

function M.schedule_after_settings_change(config)
  python.invalidate()

  local paths = {}
  for path in pairs(cache) do
    paths[path] = true
  end

  for path, bufnr in pairs(path_to_bufnr) do
    if vim.api.nvim_buf_is_valid(bufnr) then paths[path] = true end
  end

  local count = 0
  for path in pairs(paths) do
    count = count + 1
    cache[path] = nil
    M.publish_for_path(path)
    local bufnr = bufnr_for_path(path)
    if bufnr then
      schedule(config, path, bufnr, save_timers, true, "settings")
    end
  end

  if count > 0 then
    log.debug(string.format("settings trigger paths=%d", count))
  end
end

function M.detach(bufnr)
  local path = path_for_bufnr(bufnr)
  if path == "" then return end

  clear_timer(save_timers, path)
  clear_timer(idle_timers, path)
  idle_pending[path] = nil
  path_to_bufnr[path] = nil
  diagnostics.clear(bufnr)
end

function M.dispose()
  for path in pairs(save_timers) do
    clear_timer(save_timers, path)
  end
  for path in pairs(idle_timers) do
    clear_timer(idle_timers, path)
  end
  save_timers = {}
  idle_timers = {}
  idle_pending = {}
  cache = {}
  in_flight = {}
  path_to_bufnr = {}
end

return M

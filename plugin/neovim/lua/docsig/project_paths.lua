local M = {}

local function as_posix(value)
  return (value:gsub("\\", "/"))
end

function M.from_stored_path(base, input)
  local trimmed = vim.trim(input)
  if trimmed == "" then return nil end

  if not base or base == "" then return as_posix(trimmed) end

  local absolute = vim.fs.normalize(vim.fs.joinpath(base, trimmed))
  local root = vim.fs.normalize(base)
  if vim.startswith(absolute, root) then
    return as_posix(absolute:sub(#root + 2))
  end

  return as_posix(trimmed)
end

function M.to_cli_path(base, stored)
  local trimmed = vim.trim(stored)
  if trimmed == "" then return "" end

  if not base or base == "" then return vim.fn.fnamemodify(trimmed, ":p") end

  if trimmed:sub(1, 1) == "/" or trimmed:match("^%a:[/\\]") then
    return vim.fs.normalize(trimmed)
  end

  return vim.fs.normalize(vim.fs.joinpath(base, trimmed))
end

return M

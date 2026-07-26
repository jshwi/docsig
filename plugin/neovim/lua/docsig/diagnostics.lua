local M = {}

local ns = vim.api.nvim_create_namespace("docsig")

function M.namespace()
  return ns
end

local function resolve_line(bufnr, line)
  if line == nil then return 0 end

  local lnum = line - 1
  if lnum < 0 then return 0 end

  local line_count = vim.api.nvim_buf_line_count(bufnr)
  if lnum >= line_count then return 0 end

  return lnum
end

-- the intellij plugin walks the psi tree to the function name element
-- and the vscode extension asks for the symbol's selection range, so
-- underline the name here too rather than sitting at column zero
local function resolve_columns(bufnr, lnum)
  local text = vim.api.nvim_buf_get_lines(bufnr, lnum, lnum + 1, false)[1]
  if not text then return 0, 0 end

  for _, keyword in ipairs({ "def", "class" }) do
    local pos, name = text:match(keyword .. "%s+()([%w_]+)")
    if pos then return pos - 1, pos - 1 + #name end
  end

  -- no definition on the line, so sit at its first non-blank column
  local indent = text:find("%S")
  local col = indent and indent - 1 or 0
  return col, col
end

function M.publish(bufnr, issues)
  if not vim.api.nvim_buf_is_valid(bufnr) then return end

  if #issues == 0 then
    vim.diagnostic.reset(ns, bufnr)
    return
  end

  local diagnostics = {}
  for _, issue in ipairs(issues) do
    local lnum = resolve_line(bufnr, issue.line)
    local col, end_col = resolve_columns(bufnr, lnum)
    diagnostics[#diagnostics + 1] = {
      lnum = lnum,
      col = col,
      end_lnum = lnum,
      end_col = end_col,
      severity = issue.exit == 2 and vim.diagnostic.severity.ERROR
        or vim.diagnostic.severity.WARN,
      message = issue.message,
      source = "docsig",
    }
  end

  vim.diagnostic.set(ns, bufnr, diagnostics)
end

function M.clear(bufnr)
  if vim.api.nvim_buf_is_valid(bufnr) then vim.diagnostic.reset(ns, bufnr) end
end

return M

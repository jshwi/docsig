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

function M.publish(bufnr, issues)
  if not vim.api.nvim_buf_is_valid(bufnr) then return end

  if #issues == 0 then
    vim.diagnostic.reset(ns, bufnr)
    return
  end

  local diagnostics = {}
  for _, issue in ipairs(issues) do
    local lnum = resolve_line(bufnr, issue.line)
    diagnostics[#diagnostics + 1] = {
      lnum = lnum,
      col = 0,
      end_lnum = lnum,
      end_col = 0,
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

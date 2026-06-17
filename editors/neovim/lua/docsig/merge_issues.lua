local M = {}

function M.merge(previous, issues)
  local has_global_error = false
  for _, issue in ipairs(issues) do
    if issue.exit == 2 and issue.line == nil then
      has_global_error = true
      break
    end
  end

  if not has_global_error then return issues end

  local prev_line_issues = {}
  for _, issue in ipairs(previous or {}) do
    if issue.line ~= nil then
      prev_line_issues[#prev_line_issues + 1] = issue
    end
  end

  local global_issues = {}
  for _, issue in ipairs(issues) do
    if issue.line == nil then global_issues[#global_issues + 1] = issue end
  end

  return vim.list_extend(prev_line_issues, global_issues)
end

return M

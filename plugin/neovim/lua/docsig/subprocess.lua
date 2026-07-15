local M = {}

function M.run_sync(command, cwd)
  local env =
    vim.tbl_extend("force", vim.fn.environ(), { _DOCSIG_FORMAT_JSON = "true" })

  -- stdout/stderr default to capture; `stdout = true` asserts on nvim 0.10
  local result = vim.system(command, { cwd = cwd, env = env }):wait()

  local out = (result.stdout or "") .. (result.stderr or "")
  return { exit = result.code, out = vim.trim(out) }
end

function M.run(command, cwd, on_complete)
  local env =
    vim.tbl_extend("force", vim.fn.environ(), { _DOCSIG_FORMAT_JSON = "true" })

  return vim.system(command, { cwd = cwd, env = env }, function(result)
    local out = (result.stdout or "") .. (result.stderr or "")
    on_complete({ exit = result.code, out = vim.trim(out) })
  end)
end

return M

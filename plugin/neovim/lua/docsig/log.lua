local M = {}

function M.debug(message)
  if not vim.g.docsig_debug then return end

  vim.schedule(function()
    vim.print("[docsig] " .. message)
  end)
end

function M.warn(message)
  vim.schedule(function()
    vim.notify("[docsig] " .. message, vim.log.levels.WARN)
  end)
end

return M

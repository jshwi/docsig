vim.api.nvim_create_user_command("DocsigRefresh", function()
  require("docsig").refresh()
end, { desc = "Refresh docsig diagnostics for the current buffer" })

local config = require("docsig.config")
local service = require("docsig.service")

local M = {}

local user_config
local autocmd_group
local setup_done = false

local function current_config()
  return user_config or config.resolve({})
end

local function on_attach(bufnr)
  if vim.bo[bufnr].filetype ~= "python" then return end

  local path = vim.api.nvim_buf_get_name(bufnr)
  if service.has_cached(path) then
    service.publish_cached(bufnr)
    return
  end

  service.ensure_fresh(current_config(), bufnr)
end

local function create_autocmds()
  autocmd_group = vim.api.nvim_create_augroup("Docsig", { clear = true })

  vim.api.nvim_create_autocmd({ "BufEnter", "BufReadPost" }, {
    group = autocmd_group,
    pattern = "*.py",
    callback = function(args)
      on_attach(args.buf)
    end,
  })

  vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI" }, {
    group = autocmd_group,
    pattern = "*.py",
    callback = function(args)
      vim.schedule(function()
        service.ensure_fresh(current_config(), args.buf)
      end)
    end,
  })

  vim.api.nvim_create_autocmd("BufWritePost", {
    group = autocmd_group,
    pattern = "*.py",
    callback = function(args)
      service.schedule_from_save(current_config(), args.buf)
    end,
  })

  vim.api.nvim_create_autocmd("BufUnload", {
    group = autocmd_group,
    pattern = "*.py",
    callback = function(args)
      service.detach(args.buf)
    end,
  })
end

function M.setup(opts)
  if vim.fn.has("nvim-0.10") == 0 then
    vim.notify(
      "docsig.nvim requires Neovim 0.10 or newer",
      vim.log.levels.ERROR
    )
    return
  end

  if setup_done then
    service.dispose()
    if autocmd_group then
      vim.api.nvim_clear_autocmds({ group = autocmd_group })
      autocmd_group = nil
    end
  end

  user_config = config.resolve(opts)
  create_autocmds()
  vim.api.nvim_create_user_command("DocsigRefresh", function()
    M.refresh()
  end, { desc = "Refresh docsig diagnostics for the current buffer" })
  setup_done = true

  for _, bufnr in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_loaded(bufnr) then on_attach(bufnr) end
  end
end

function M.refresh(bufnr)
  bufnr = bufnr or vim.api.nvim_get_current_buf()
  service.ensure_fresh(current_config(), bufnr)
end

function M.on_settings_changed()
  service.schedule_after_settings_change(current_config())
end

function M.is_setup()
  return setup_done
end

return M

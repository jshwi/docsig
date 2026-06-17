-- busted helper; minimal_init sets up the neovim test environment

local source = debug.getinfo(1, "S").source:sub(2)
local helper_dir = vim.fn.fnamemodify(source, ":p:h")
local tmp_dir = helper_dir .. "/tmp"
local counter = 0

local M = {}

function M.reset_tmp()
  if vim.fn.isdirectory(tmp_dir) == 1 then vim.fn.delete(tmp_dir, "rf") end
  vim.fn.mkdir(tmp_dir, "p")
end

function M.temp_py_path(suffix)
  counter = counter + 1
  return tmp_dir .. "/" .. suffix .. "-" .. counter .. ".py"
end

function M.temp_py_path_missing(suffix)
  counter = counter + 1
  return tmp_dir .. "/" .. suffix .. "-missing-" .. counter .. ".py"
end

function M.write_temp_py(path, lines)
  vim.fn.mkdir(vim.fn.fnamemodify(path, ":h"), "p")
  vim.fn.writefile(lines or { "" }, path)
  return path
end

function M.temp_py_buf(suffix, lines)
  local path = M.temp_py_path(suffix)
  M.write_temp_py(path, lines)
  local bufnr = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_name(bufnr, path)
  vim.bo[bufnr].filetype = "python"
  return bufnr, path
end

_G.docsig_test = M
M.reset_tmp()

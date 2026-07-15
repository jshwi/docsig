-- luacheck config for docsig.nvim
-- see https://github.com/mpeterv/luacheck

std = "lua51+busted"

read_globals = {
  "vim",
  "describe",
  "it",
  "before_each",
  "after_each",
  "before_all",
  "after_all",
  "assert",
  "docsig_test",
}

globals = {
  "vim.g",
  "vim.fn",
  "vim.api",
  "vim.bo",
  "vim.b",
  "vim.o",
  "vim.opt",
  "vim.log",
  "vim.uv",
  "vim.fs",
  "vim.diagnostic",
}

cache = true

max_line_length = false
max_code_line_length = false

include_files = {
  "lua",
  "plugin",
  "tests",
}

exclude_files = {
  ".luarocks",
}

ignore = {
  "121",
  "122",
  "212/_.*",
  "214",
}

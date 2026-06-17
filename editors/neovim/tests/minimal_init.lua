vim.o.swapfile = false
vim.o.undofile = false

local source = debug.getinfo(1, "S").source:sub(2)
local test_dir = vim.fn.fnamemodify(vim.fn.fnamemodify(source, ":p"), ":h")
local plugin_root = vim.fn.fnamemodify(test_dir, ":h")

vim.g.docsig_test_root = plugin_root
vim.opt.runtimepath:prepend(plugin_root)
vim.opt.runtimepath:append(test_dir)
package.path = test_dir .. "/?.lua;" .. package.path

local function prepend_luarocks()
  for _, ver in ipairs({ "5.5", "5.4", "5.1" }) do
    local share = plugin_root .. "/.luarocks/share/lua/" .. ver
    local lib = plugin_root .. "/.luarocks/lib/lua/" .. ver
    if vim.fn.isdirectory(share) == 1 then
      package.path = share
        .. "/?.lua;"
        .. share
        .. "/?/init.lua;"
        .. package.path
      package.cpath = lib .. "/?.so;" .. package.cpath
    end
  end
end

prepend_luarocks()
vim.cmd.cd(plugin_root)

if os.getenv("DOCSIG_COVERAGE") == "1" then
  vim.fn.mkdir(plugin_root .. "/coverage", "p")
  require("luacov.runner").init()
end

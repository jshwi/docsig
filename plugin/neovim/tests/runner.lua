vim.cmd.cd(vim.g.docsig_test_root)

_G.arg = { [0] = "busted", "--helper=tests/helper.lua", "tests" }

local ok, err = pcall(function()
  require("busted.runner")({ standalone = false, output = "plainTerminal" })
end)

if os.getenv("DOCSIG_COVERAGE") == "1" then
  require("luacov.runner").shutdown()
  require("coverage_summary").write()
end

if _G.docsig_test then _G.docsig_test.reset_tmp() end

if not ok then
  print(tostring(err))
  vim.cmd("cquit 1")
end

vim.cmd("cquit 0")

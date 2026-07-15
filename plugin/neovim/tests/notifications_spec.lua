describe("notifications", function()
  local notifications = require("docsig.notifications")

  local counter = 0

  local function temp_buf()
    counter = counter + 1
    local path = vim.g.docsig_test_root .. "/notify-" .. counter .. ".py"
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(bufnr, path)
    vim.bo[bufnr].filetype = "python"
    return bufnr
  end

  it("notify_missing_python warns once per workspace", function()
    notifications.reset_for_tests()
    local bufnr = temp_buf()
    notifications.notify_missing_python(bufnr)
    notifications.notify_missing_python(bufnr)
  end)

  it("notify_unsupported_python warns once per workspace", function()
    notifications.reset_for_tests()
    local bufnr = temp_buf()
    notifications.notify_unsupported_python(bufnr)
    notifications.notify_unsupported_python(bufnr)
  end)
end)

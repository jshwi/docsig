describe("log", function()
  local log = require("docsig.log")

  it("debug is a no-op when disabled", function()
    vim.g.docsig_debug = false
    log.debug("quiet")
  end)

  it("debug schedules output when enabled", function()
    vim.g.docsig_debug = true
    log.debug("visible")
    vim.wait(1000, function()
      return false
    end)
    vim.g.docsig_debug = false
  end)

  it("warn schedules notification", function()
    log.warn("warning")
    vim.wait(1000, function()
      return false
    end)
  end)
end)

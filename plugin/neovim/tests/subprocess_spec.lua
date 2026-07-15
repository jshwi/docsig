describe("subprocess", function()
  package.loaded["docsig.subprocess"] = nil
  local subprocess = require("docsig.subprocess")

  it("run_sync captures stdout", function()
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then return end

    local result = subprocess.run_sync({ interpreter, "-c", "print('ok')" })
    assert.equals(result.exit, 0)
    assert.equals(result.out, "ok")
  end)

  it("run invokes callback with merged output", function()
    local interpreter = vim.fn.exepath("python3")
    if interpreter == "" then return end

    local received
    subprocess.run(
      { interpreter, "-c", "print('async')" },
      nil,
      function(result)
        received = result
      end
    )
    vim.wait(5000, function()
      return received ~= nil
    end)
    assert.equals(received.exit, 0)
    assert.equals(received.out, "async")
  end)
end)

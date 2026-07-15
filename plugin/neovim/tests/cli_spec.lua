describe("cli", function()
  package.loaded["docsig.subprocess"] = {
    run_sync = function()
      return {
        exit = 0,
        out = '[{"line":1,"message":"SIG101: function is missing a docstring (function-doc-missing)","exit":1}]',
      }
    end,
    run = function(_, _, on_complete)
      on_complete({ exit = 0, out = "[]" })
    end,
  }

  package.loaded["docsig.python"] = {
    path = function()
      return "/python"
    end,
    meets_minimum_version = function()
      return true
    end,
    workspace_root = function()
      return "/workspace"
    end,
    invalidate = function() end,
  }

  package.loaded["docsig.executable"] = {
    path = function()
      return "/docsig.pyz"
    end,
  }

  package.loaded["docsig.cli"] = nil
  local cli = require("docsig.cli")
  local config = require("docsig.config")

  local function cfg()
    return config.resolve({})
  end

  it("is_available reflects python path", function()
    assert.truthy(cli.is_available(0, cfg()))
  end)

  it("is_python_supported reflects python version", function()
    assert.truthy(cli.is_python_supported(0, cfg()))
  end)

  it("run_sync parses json issues", function()
    local issues = cli.run_sync("/file.py", 0, cfg())
    assert.equals(#issues, 1)
    assert.equals(issues[1].line, 1)
  end)

  it("run_sync returns empty list when output empty", function()
    package.loaded["docsig.subprocess"].run_sync = function()
      return { exit = 0, out = "" }
    end
    assert.same(cli.run_sync("/file.py", 0, cfg()), {})
  end)

  it("run_sync returns empty list on invalid json", function()
    package.loaded["docsig.subprocess"].run_sync = function()
      return { exit = 0, out = "not json" }
    end
    assert.same(cli.run_sync("/file.py", 0, cfg()), {})
  end)

  it("run_sync returns empty list when python missing", function()
    package.loaded["docsig.python"].path = function()
      return nil
    end

    assert.same(cli.run_sync("/file.py", 0, cfg()), {})
  end)

  it("run_sync returns empty list when python unsupported", function()
    package.loaded["docsig.python"].path = function()
      return "/python"
    end

    package.loaded["docsig.python"].meets_minimum_version = function()
      return false
    end

    assert.same(cli.run_sync("/file.py", 0, cfg()), {})
  end)

  it("run invokes callback with parsed issues", function()
    package.loaded["docsig.python"].path = function()
      return "/python"
    end

    package.loaded["docsig.python"].meets_minimum_version = function()
      return true
    end

    package.loaded["docsig.subprocess"].run = function(_, _, on_complete)
      on_complete({
        exit = 0,
        out = '[{"line":2,"message":"SIG203: params missing (params-missing)","exit":1}]',
      })
    end

    local received
    cli.run("/file.py", 0, cfg(), function(issues)
      received = issues
    end)
    vim.wait(1000, function()
      return received ~= nil
    end)
    assert.equals(#received, 1)
    assert.equals(received[1].line, 2)
  end)

  it("run returns empty list when callback gets empty output", function()
    package.loaded["docsig.subprocess"].run = function(_, _, on_complete)
      on_complete({ exit = 0, out = "" })
    end

    local received
    cli.run("/file.py", 0, cfg(), function(issues)
      received = issues
    end)
    vim.wait(1000, function()
      return received ~= nil
    end)
    assert.same(received, {})
  end)

  it("run returns empty list when callback gets invalid json", function()
    package.loaded["docsig.subprocess"].run = function(_, _, on_complete)
      on_complete({ exit = 0, out = "not json" })
    end

    local received
    cli.run("/file.py", 0, cfg(), function(issues)
      received = issues
    end)
    vim.wait(1000, function()
      return received ~= nil
    end)
    assert.same(received, {})
  end)

  it("run invokes callback with empty list when python missing", function()
    package.loaded["docsig.python"].path = function()
      return nil
    end

    package.loaded["docsig.python"].meets_minimum_version = function()
      return true
    end

    local received
    cli.run("/file.py", 0, cfg(), function(issues)
      received = issues
    end)
    vim.wait(1000, function()
      return received ~= nil
    end)
    assert.same(received, {})
  end)

  it("run invokes callback with empty list when python unsupported", function()
    package.loaded["docsig.python"].path = function()
      return "/python"
    end

    package.loaded["docsig.python"].meets_minimum_version = function()
      return false
    end

    local received
    cli.run("/file.py", 0, cfg(), function(issues)
      received = issues
    end)
    vim.wait(1000, function()
      return received ~= nil
    end)
    assert.same(received, {})
  end)
end)

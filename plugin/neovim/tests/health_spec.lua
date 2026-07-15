describe("health", function()
  local function capture_reporter()
    local calls = {}
    local function record(kind)
      return function(msg, advice)
        table.insert(calls, { kind = kind, msg = msg, advice = advice })
      end
    end

    return {
      calls = calls,
      start = record("start"),
      ok = record("ok"),
      error = record("error"),
    }
  end

  local function kinds(calls)
    local out = {}
    for _, call in ipairs(calls) do
      table.insert(out, call.kind)
    end
    return table.concat(out, " ")
  end

  local function fresh_health(mocks)
    for name, mock in pairs(mocks or {}) do
      package.loaded["docsig." .. name] = mock
    end
    package.loaded["docsig.health"] = nil
    local health = require("docsig.health")
    for name in pairs(mocks or {}) do
      package.loaded["docsig." .. name] = nil
    end
    package.loaded["docsig.health"] = nil
    return health
  end

  local old_docsig

  before_each(function()
    old_docsig = vim.g.docsig
  end)

  after_each(function()
    vim.g.docsig = old_docsig
  end)

  it("check reports all ok in a healthy environment", function()
    vim.g.docsig = {}
    local reporter = capture_reporter()
    fresh_health().check(reporter)
    assert.equals(kinds(reporter.calls), "start ok ok ok")
  end)

  it("check defaults reporter to vim.health", function()
    vim.g.docsig = false
    local old_health = vim.health
    local reporter = capture_reporter()
    vim.health = reporter

    local ok, err = pcall(function()
      fresh_health().check()
    end)
    vim.health = old_health
    assert.truthy(ok, err)
    assert.equals(reporter.calls[1].kind, "start")
  end)

  it("check reports errors when nothing is available", function()
    vim.g.docsig = {}
    local old_has = vim.fn.has
    vim.fn.has = function(feature)
      if feature == "nvim-0.10" then return 0 end
      return old_has(feature)
    end

    local reporter = capture_reporter()
    local ok, err = pcall(function()
      fresh_health({
        python = {
          path = function()
            return nil
          end,
          version_supported = function()
            return false
          end,
          MIN_MAJOR = 3,
          MIN_MINOR = 10,
        },
        executable = {
          path = function()
            error("missing docsig executable")
          end,
        },
      }).check(reporter)
    end)
    vim.fn.has = old_has
    assert.truthy(ok, err)
    assert.equals(kinds(reporter.calls), "start error error error")
  end)

  it("check reports unsupported python version", function()
    vim.g.docsig = {}
    local reporter = capture_reporter()
    fresh_health({
      python = {
        path = function()
          return "/usr/bin/python2"
        end,
        version_supported = function()
          return false
        end,
        MIN_MAJOR = 3,
        MIN_MINOR = 10,
      },
    }).check(reporter)
    assert.equals(kinds(reporter.calls), "start ok error ok")
    assert.truthy(reporter.calls[3].msg:match("below minimum"))
  end)
end)

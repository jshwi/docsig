describe("diagnostics", function()
  local diagnostics = require("docsig.diagnostics")

  local function temp_buf(lines)
    local bufnr = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, lines)
    vim.bo[bufnr].filetype = "python"
    return bufnr
  end

  it("publish maps one-based line to zero-based diagnostic", function()
    local bufnr = temp_buf({ "def foo():", "    pass" })
    diagnostics.publish(bufnr, {
      {
        line = 1,
        message = "SIG101: function is missing a docstring (function-doc-missing)",
        exit = 1,
      },
    })

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(#items, 1)
    assert.equals(items[1].lnum, 0)
    assert.equals(items[1].severity, vim.diagnostic.severity.WARN)
    assert.equals(items[1].source, "docsig")
    diagnostics.clear(bufnr)
  end)

  it("publish uses error severity for exit code two", function()
    local bufnr = temp_buf({ "def foo():", "    pass" })
    diagnostics.publish(bufnr, {
      {
        line = 2,
        message = "SIG901: invalid syntax (invalid-syntax)",
        exit = 2,
      },
    })

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(items[1].lnum, 1)
    assert.equals(items[1].severity, vim.diagnostic.severity.ERROR)
    diagnostics.clear(bufnr)
  end)

  it("publish uses file start for null line", function()
    local bufnr = temp_buf({ "import os" })
    diagnostics.publish(
      bufnr,
      { { line = nil, message = "configuration error", exit = 2 } }
    )

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(items[1].lnum, 0)
    diagnostics.clear(bufnr)
  end)

  it("publish clears diagnostics when issues empty", function()
    local bufnr = temp_buf({ "import os" })
    diagnostics.publish(bufnr, { { line = 1, message = "warn", exit = 1 } })
    diagnostics.publish(bufnr, {})

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(#items, 0)
    diagnostics.clear(bufnr)
  end)

  it("publish ignores invalid buffer", function()
    diagnostics.publish(-1, { { line = 1, message = "warn", exit = 1 } })
  end)

  it("clear ignores invalid buffer", function()
    diagnostics.clear(-1)
  end)

  it("publish falls back to file start when line out of range", function()
    local bufnr = temp_buf({ "import os" })
    diagnostics.publish(bufnr, { { line = 99, message = "warn", exit = 1 } })

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(items[1].lnum, 0)
    diagnostics.clear(bufnr)
  end)

  it("publish maps zero line to file start", function()
    local bufnr = temp_buf({ "import os" })
    diagnostics.publish(bufnr, { { line = 0, message = "warn", exit = 1 } })

    local items =
      vim.diagnostic.get(bufnr, { namespace = diagnostics.namespace() })
    assert.equals(items[1].lnum, 0)
    diagnostics.clear(bufnr)
  end)
end)

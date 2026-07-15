describe("merge_issues", function()
  local merge_issues = require("docsig.merge_issues")

  it("returns new issues when no global error", function()
    local issues = { { line = 1, message = "a", exit = 1 } }
    assert.same(merge_issues.merge(nil, issues), issues)
  end)

  it("keeps prior line issues when global error", function()
    local previous = {
      { line = 2, message = "old", exit = 1 },
      { line = nil, message = "old global", exit = 2 },
    }
    local issues = { { line = nil, message = "new global", exit = 2 } }

    assert.same(merge_issues.merge(previous, issues), {
      { line = 2, message = "old", exit = 1 },
      { line = nil, message = "new global", exit = 2 },
    })
  end)

  it("treats exit 2 with line as not global error", function()
    local issues = { { line = 3, message = "line error", exit = 2 } }
    assert.same(
      merge_issues.merge({ { line = 1, message = "old", exit = 1 } }, issues),
      issues
    )
  end)

  it("global error drops line issues when cache empty", function()
    local issues = { { line = nil, message = "global", exit = 2 } }
    assert.same(merge_issues.merge(nil, issues), issues)
  end)
end)

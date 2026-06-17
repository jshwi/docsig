describe("project_paths", function()
  local project_paths = require("docsig.project_paths")

  local base = "/workspace/project"

  it("from_stored_path returns nil for blank input", function()
    assert.is_not.truthy(project_paths.from_stored_path(base, ""))
    assert.is_not.truthy(project_paths.from_stored_path(base, "   "))
  end)

  it("from_stored_path relativizes absolute paths under base", function()
    assert.equals(
      project_paths.from_stored_path(base, "pkg/module.py"),
      "pkg/module.py"
    )
  end)

  it("from_stored_path keeps input when outside base", function()
    assert.equals(
      project_paths.from_stored_path(base, "../outside"),
      "../outside"
    )
  end)

  it("to_cli_path returns empty for blank stored path", function()
    assert.equals(project_paths.to_cli_path(base, ""), "")
  end)

  it("to_cli_path resolves relative stored paths against base", function()
    assert.equals(
      project_paths.to_cli_path(base, "pkg/module.py"),
      "/workspace/project/pkg/module.py"
    )
  end)

  it("from_stored_path normalizes backslashes when base missing", function()
    assert.equals(project_paths.from_stored_path(nil, "a\\b"), "a/b")
  end)

  it("to_cli_path resolves against cwd when base missing", function()
    local expected = vim.fn.fnamemodify("relative", ":p")
    assert.equals(project_paths.to_cli_path(nil, "relative"), expected)
  end)

  it("to_cli_path normalizes absolute stored paths", function()
    assert.equals(
      project_paths.to_cli_path(base, "/workspace/project/pkg/module.py"),
      "/workspace/project/pkg/module.py"
    )
  end)
end)

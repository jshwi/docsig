describe("options", function()
  local config = require("docsig.config")
  local options = require("docsig.options")

  local function base_cfg(overrides)
    return vim.tbl_deep_extend("force", config.resolve({}), overrides or {})
  end

  it("apply adds bool flag when enabled", function()
    assert.same(
      options.build_args(base_cfg({ check_nested = true }), "/proj"),
      { "--check-nested" }
    )
  end)

  it("apply does not add bool flag when disabled", function()
    assert.same(options.build_args(base_cfg({}), "/proj"), {})
  end)

  it("apply emits class check flag", function()
    assert.same(
      options.build_args(
        base_cfg({ class_check_mode = "Check class" }),
        "/proj"
      ),
      { "--check-class" }
    )
  end)

  it("apply adds exclude flag and normalized value", function()
    assert.same(
      options.build_args(base_cfg({ exclude = "tests/.*" }), "/proj"),
      { "--exclude", "tests/.*" }
    )
  end)

  it("apply skips blank exclude", function()
    assert.same(options.build_args(base_cfg({ exclude = "   " }), "/proj"), {})
  end)

  it("apply adds comma list flag and values", function()
    assert.same(
      options.build_args(
        base_cfg({ disable = { "SIG101", "SIG102" } }),
        "/proj"
      ),
      { "--disable", "SIG101,SIG102" }
    )
  end)

  it("apply adds target flag and values", function()
    assert.same(
      options.build_args(base_cfg({ target = { "SIG203" } }), "/proj"),
      { "--target", "SIG203" }
    )
  end)

  it("apply adds excludes paths relative to root", function()
    assert.same(
      options.build_args(base_cfg({ excludes = { "pkg/module.py" } }), "/proj"),
      { "--excludes", "/proj/pkg/module.py" }
    )
  end)

  it("apply adds remaining bool flags when enabled", function()
    assert.same(
      options.build_args(
        base_cfg({
          check_dunders = true,
          check_overridden = true,
          check_property_returns = true,
          check_protected = true,
          check_protected_class_methods = true,
          ignore_args = true,
          ignore_kwargs = true,
          ignore_no_params = true,
          include_ignored = true,
        }),
        "/proj"
      ),
      {
        "--check-dunders",
        "--check-overridden",
        "--check-property-returns",
        "--check-protected",
        "--check-protected-class-methods",
        "--ignore-args",
        "--ignore-kwargs",
        "--ignore-no-params",
        "--include-ignored",
      }
    )
  end)

  it("apply emits class constructor flag", function()
    assert.same(
      options.build_args(
        base_cfg({ class_check_mode = "Check class constructor" }),
        "/proj"
      ),
      { "--check-class-constructor" }
    )
  end)

  it("apply skips empty disable and target lists", function()
    assert.same(
      options.build_args(base_cfg({ disable = {}, target = {} }), "/proj"),
      {}
    )
  end)
end)

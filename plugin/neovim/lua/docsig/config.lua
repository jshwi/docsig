local M = {}

M.PLUGIN_VERSION = "1.0.0"

M.defaults = {
  debounce_ms = 600,
  python = nil,
  executable = nil,
  class_check_mode = "None",
  check_dunders = false,
  check_nested = false,
  check_overridden = false,
  check_property_returns = false,
  check_protected = false,
  check_protected_class_methods = false,
  ignore_args = false,
  ignore_kwargs = false,
  ignore_no_params = false,
  include_ignored = false,
  exclude = "",
  excludes = {},
  disable = {},
  target = {},
}

function M.resolve(user)
  return vim.tbl_deep_extend("force", vim.deepcopy(M.defaults), user or {})
end

return M

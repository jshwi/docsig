local class_check_mode = require("docsig.class_check_mode")
local project_paths = require("docsig.project_paths")

local M = {}

local function add_bool(cfg, key, flag, args)
  if cfg[key] then args[#args + 1] = flag end
end

function M.build_args(cfg, root)
  local args = {}

  local class_flag = class_check_mode.flag(cfg.class_check_mode)
  if class_flag then args[#args + 1] = class_flag end

  add_bool(cfg, "check_dunders", "--check-dunders", args)
  add_bool(cfg, "check_nested", "--check-nested", args)
  add_bool(cfg, "check_overridden", "--check-overridden", args)
  add_bool(cfg, "check_property_returns", "--check-property-returns", args)
  add_bool(cfg, "check_protected", "--check-protected", args)
  add_bool(
    cfg,
    "check_protected_class_methods",
    "--check-protected-class-methods",
    args
  )
  add_bool(cfg, "ignore_args", "--ignore-args", args)
  add_bool(cfg, "ignore_kwargs", "--ignore-kwargs", args)
  add_bool(cfg, "ignore_no_params", "--ignore-no-params", args)
  add_bool(cfg, "include_ignored", "--include-ignored", args)

  local exclude = vim.trim(cfg.exclude or "")
  if exclude ~= "" then
    args[#args + 1] = "--exclude"
    args[#args + 1] = exclude
  end

  local excludes = cfg.excludes or {}
  if #excludes > 0 then
    args[#args + 1] = "--excludes"
    for _, entry in ipairs(excludes) do
      if entry and entry ~= "" then
        args[#args + 1] = project_paths.to_cli_path(root, entry)
      end
    end
  end

  local disable = cfg.disable or {}
  if #disable > 0 then
    args[#args + 1] = "--disable"
    args[#args + 1] = table.concat(disable, ",")
  end

  local target = cfg.target or {}
  if #target > 0 then
    args[#args + 1] = "--target"
    args[#args + 1] = table.concat(target, ",")
  end

  return args
end

return M

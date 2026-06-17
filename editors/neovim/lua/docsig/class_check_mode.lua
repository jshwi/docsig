local M = {}

local FLAGS = { ["None"] = nil, ["Check class"] = "--check-class" }
FLAGS["Check class constructor"] = "--check-class-constructor"

function M.flag(mode)
  return FLAGS[mode]
end

return M

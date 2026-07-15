local M = {}

local function plugin_root()
  return vim.g.docsig_test_root
end

function M.write()
  local root = plugin_root()
  vim.cmd.cd(root)

  local reporter = require("luacov.reporter")
  local DefaultReporter = reporter.DefaultReporter

  local SummaryReporter = setmetatable({}, { __index = DefaultReporter })
  SummaryReporter.__index = SummaryReporter

  function SummaryReporter:on_end()
    local total_hits = 0
    local total_missed = 0
    local summary = {}

    for _, filename in ipairs(self:files()) do
      local file_summary = self._summary[filename]
      if file_summary and filename:match("/lua/docsig/") then
        local hits = file_summary.hits
        local missed = file_summary.miss
        local total = hits + missed
        total_hits = total_hits + hits
        total_missed = total_missed + missed
        summary[filename] = {
          lines = {
            total = total,
            covered = hits,
            skipped = 0,
            pct = total > 0 and (hits / total * 100) or 100,
          },
        }
      end
    end

    local grand = total_hits + total_missed
    summary.total = {
      lines = {
        total = grand,
        covered = total_hits,
        skipped = 0,
        pct = grand > 0 and (total_hits / grand * 100) or 100,
      },
    }

    vim.fn.mkdir("coverage", "p")
    vim.fn.writefile(
      { vim.json.encode(summary) },
      "coverage/coverage-summary.json"
    )
  end

  require("luacov.runner").load_config()
  reporter.report(SummaryReporter)
end

return M

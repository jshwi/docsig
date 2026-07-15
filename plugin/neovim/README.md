# docsig.nvim

<!-- Plugin description -->

Neovim plugin for [docsig](https://github.com/jshwi/docsig): report docstring
and signature mismatches for Python files using the bundled `docsig` checker.

## Requirements

- Neovim **0.10+**
- Python **3.10+** (`g:python3_host_prog` or `python3` on `PATH`)

## Installation

The plugin is published to
[jshwi/docsig.nvim](https://github.com/jshwi/docsig.nvim) with the checker
already bundled — no build step required:

```lua
-- lazy.nvim
return {
  { "jshwi/docsig.nvim", ft = "python" },
}
```

```lua
-- packer.nvim
use({ "jshwi/docsig.nvim", ft = "python" })
```

To develop against the [docsig monorepo](https://github.com/jshwi/docsig),
where the plugin lives at `plugin/neovim`, clone it, build the bundled
checker, and point at the plugin directory:

```bash
git clone https://github.com/jshwi/docsig
make -C docsig/plugin/neovim bundle
```

```lua
-- lazy.nvim
return {
  { dir = "/path/to/docsig/plugin/neovim", ft = "python" },
}
```

## Setup

The plugin loads automatically when `vim.g.docsig` is not set to `false`.

```lua
-- init.lua
vim.g.docsig = {
  check_nested = true,
  class_check_mode = "Check class",
}
```

Or call `setup` explicitly:

```lua
require("docsig").setup({
  check_nested = true,
  python = "/usr/bin/python3",
})
```

Run `:DocsigRefresh` to re-check the current buffer, and
`:checkhealth docsig` to verify the Neovim version, Python interpreter, and
bundled executable.

## Configuration

Options mirror the VS Code extension (`docsig.*` settings):

| Option | Default | CLI flag |
|--------|---------|----------|
| `debounce_ms` | `600` | — |
| `python` | auto | — |
| `executable` | bundled `docsig.pyz` | — |
| `class_check_mode` | `"None"` | `--check-class` / `--check-class-constructor` |
| `check_dunders` | `false` | `--check-dunders` |
| `check_nested` | `false` | `--check-nested` |
| `check_overridden` | `false` | `--check-overridden` |
| `check_property_returns` | `false` | `--check-property-returns` |
| `check_protected` | `false` | `--check-protected` |
| `check_protected_class_methods` | `false` | `--check-protected-class-methods` |
| `ignore_args` | `false` | `--ignore-args` |
| `ignore_kwargs` | `false` | `--ignore-kwargs` |
| `ignore_no_params` | `false` | `--ignore-no-params` |
| `include_ignored` | `false` | `--include-ignored` |
| `exclude` | `""` | `--exclude` |
| `excludes` | `{}` | `--excludes` |
| `disable` | `{}` | `--disable` |
| `target` | `{}` | `--target` |

Set `vim.g.docsig_debug = true` to log checker invocations.

## Behaviour

- Runs on buffer enter, while editing (debounced), and on save
- Maps JSON diagnostics onto source lines as warnings or errors
- Caches results per file; coalesces overlapping runs
- Uses the same bundled `docsig.pyz` workflow as the VS Code extension

## Privacy and Data Usage

Docsig runs locally on your machine. The plugin does not collect analytics,
telemetry, or usage statistics. Source code is not transmitted to external
services. The bundled checker at `resources/docsig.pyz` is invoked with your
configured Python interpreter.

## Development

```bash
make -C plugin/neovim deps bundle verify
make -C plugin/neovim format lint
make -C plugin/neovim test
```

`deps` installs luarocks packages (`luacov`, `busted`, `luacheck`) into
`.luarocks/` and [StyLua](https://github.com/JohnnyMorganz/stylua) into
`.venv/` via pip. Tests use [Busted](https://lunarmodules.github.io/busted/)
inside headless Neovim. `format` uses StyLua with `.stylua.toml`. `lint` runs
`stylua --check` and [Luacheck](https://github.com/mpeterv/luacheck) with
`.luacheckrc`.

Tests run in headless Neovim (`nvim --headless`) and require Neovim 0.10+.

## License

MIT

<!-- Plugin description end -->

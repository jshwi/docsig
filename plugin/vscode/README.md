# docsig

[![Build](https://github.com/jshwi/docsig/actions/workflows/build-vscode-extension.yaml/badge.svg)](https://github.com/jshwi/docsig/actions/workflows/build-vscode-extension.yaml)

<!-- Plugin description -->

## Docsig

Reports docstring and signature mismatches for the current Python file
using the bundled `docsig` checker.

Issues come from the same checker you run on the command line. The extension
runs it in the background after save and maps each message onto the reported
source line as a warning or error.

Configure CLI-equivalent options under **Settings | Docsig** (per
workspace). Analysis uses the workspace Python 3.10+ interpreter from the
Python extension and the bundled `docsig` executable shipped with the
extension.

## Privacy and Data Usage

Docsig runs locally on your machine.

The extension does not collect analytics, telemetry, or usage statistics.

Source code, project files, and document contents are not transmitted to
external services by the extension.

The bundled `docsig` checker is extracted locally and invoked with the
workspace Python interpreter. Results are processed entirely within the
editor.

The extension does not download or execute remote code.

<!-- Plugin description end -->

## Installation

- Using the VS Code Marketplace:

  Search for **Docsig** in the Extensions view and install.

- Manually:

  Build a `.vsix` with `make build` (output in `build/`), then install via
  **Extensions > ... > Install from VSIX...**

## Development

```bash
# from repo root
make -C plugin/vscode build
```

Press **F5** in `plugin/vscode` to launch an Extension Development Host.

## Publishing

Package with `make build` in this directory, then publish with `vsce publish`
when a Marketplace publisher token is configured.

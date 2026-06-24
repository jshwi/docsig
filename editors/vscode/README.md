# docsig

[![Build](https://github.com/jshwi/docsig/actions/workflows/build-vscode-extension.yaml/badge.svg)](https://github.com/jshwi/docsig/actions/workflows/build-vscode-extension.yaml)
[![VS Code](https://img.shields.io/badge/vscode%20extension-v1.0.0-007ACC)](https://marketplace.visualstudio.com/items?itemName=jshwi.docsig)

<!-- Plugin description -->

## Docsig

Reports docstring and signature mismatches for the current Python file
using the bundled `docsig` checker.

Issues come from the same checker you run on the command line. The extension
runs it in the background when you open a file, while you edit (debounced),
on save, or after Docsig or Python settings change. Each message is mapped
onto the reported source line as a warning or error.

Install [Docsig VS Code Extension](https://marketplace.visualstudio.com/items?itemName=jshwi.docsig),
and configure CLI-equivalent options under **Settings | Docsig** (per
workspace). Analysis uses the workspace Python 3.10+ interpreter from the
Python extension and the bundled `docsig` executable shipped with the
extension.

View extension logs under **View | Output**, then choose **Docsig** from the
channel list.

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
make -C editors/vscode build
```

Press **F5** in `editors/vscode` to launch an Extension Development Host.

## Publishing

Package with `make build` in this directory, then publish with `vsce publish`
when a Marketplace publisher token is configured.

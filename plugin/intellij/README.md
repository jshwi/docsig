# docsig

[![Build](https://github.com/jshwi/docsig/actions/workflows/build-intellij-plugin.yaml/badge.svg)](https://github.com/jshwi/docsig/actions/workflows/build-intellij-plugin.yaml)
[![Version](https://img.shields.io/jetbrains/plugin/v/32129.svg)](https://plugins.jetbrains.com/plugin/32129)

<!-- Plugin description -->

## Docsig

Reports docstring and signature mismatches for the current Python file
using the bundled `docsig` checker.

Issues come from the same checker you run on the command line. The plugin
runs it in the background after save and maps each message onto the reported
source line as a warning or error.

Configure CLI-equivalent options under **Settings | Tools | Docsig** (per
project). Analysis uses the project's configured Python 3.10+ interpreter
and the bundled `docsig` executable shipped with the plugin.

## Privacy and Data Usage

Docsig runs locally on your machine.

The plugin does not collect analytics, telemetry, or usage statistics.

Source code, project files, and document contents are not transmitted to
external services by the plugin.

The bundled `docsig` checker is extracted locally and invoked with the
project's Python interpreter. Results are processed entirely within the IDE.

The plugin does not download or execute remote code.

<!-- Plugin description end -->

## Installation

- Using the IDE built-in plugin system:

  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>Marketplace</kbd> > <kbd>Search for "docsig"</kbd> >
  <kbd>Install</kbd>

- Manually:

  Download the [latest release](https://github.com/jshwi/docsig/releases/latest) and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>

## Publishing

The first Marketplace upload is manual. Set these environment variables for
Gradle signing and automated uploads afterward:

- `CERTIFICATE_CHAIN` — Marketplace signing certificate chain
- `PRIVATE_KEY` — Marketplace signing private key
- `PRIVATE_KEY_PASSWORD` — private key password (if any)
- `PUBLISH_TOKEN` — JetBrains Marketplace token

Build a signed distribution with `make build`, then run `make publish`
when the variables above are set.

Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/docsig/compare/vscode-extension-v1.1.0...HEAD)
------------------------------------------------------------------------

[1.1.0](https://github.com/jshwi/docsig/releases/tag/vscode-extension-v1.1.0) - 2026-07-28
------------------------------------------------------------------------
### Added
- Drop stale results when a file changes outside the editor

### Fixed
- Rebuild the log channel after disposal, so logging survives a second
  activation instead of failing with 'Channel has been closed'
- update bundled docsig from v0.90.3 to v0.92.2 for several fixes, see
  the
  [docsig changelog](https://github.com/jshwi/docsig/blob/master/CHANGELOG.md)
  for details
  (docsig v0.92.2)

[1.0.1](https://github.com/jshwi/docsig/releases/tag/vscode-extension-v1.0.1) - 2026-07-10
------------------------------------------------------------------------
### Fixed
- fix(vscode-extension): avoid EXDEV when extracting CLI on Linux
  (docsig v0.89.0)

[1.0.0](https://github.com/jshwi/docsig/releases/tag/vscode-extension-v1.0.0) - 2026-06-17
------------------------------------------------------------------------
### Added
- Initial vscode extension release with bundled docsig checker
  (docsig v0.87.1)

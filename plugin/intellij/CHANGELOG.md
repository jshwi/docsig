# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- update bundled docsig from v0.87.1 to v0.90.3 for several false
  positive fixes, see the
  [docsig changelog](https://github.com/jshwi/docsig/blob/master/CHANGELOG.md)
  for details
  (docsig v0.90.3)
- invalidate stale results when a file is changed outside the ide, so
  highlights refresh without needing to edit and re-save the file

## [1.0.2] - 2026-06-13

### Changed

- vendor docstring converter in bundled pyz instead of sphinx, reducing
  bundle size by 96.5%
  (docsig v0.87.1)

## [1.0.1] - 2026-06-10

### Fixed

- pin sphinx below 8.2 so the intellij plugin bundle runs on python 3.10
  (docsig v0.86.1)

## [1.0.0] - 2026-06-06

### Added

- Initial JetBrains Marketplace release with bundled docsig checker
  (docsig v0.86.1)

[Unreleased]: https://github.com/jshwi/docsig/compare/1.0.2...HEAD
[1.0.2]: https://github.com/jshwi/docsig/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/jshwi/docsig/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/jshwi/docsig/commits/1.0.0

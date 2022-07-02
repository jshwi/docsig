Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/docsig/compare/v0.13.0...HEAD)
------------------------------------------------------------------------

[0.13.0](https://github.com/jshwi/docsig/releases/tag/v0.13.0) - 2022-07-02
------------------------------------------------------------------------
### Added
- Adds target option

[0.12.1](https://github.com/jshwi/docsig/releases/tag/v0.12.1) - 2022-06-29
------------------------------------------------------------------------
### Fixed
- Prevents duplicate error messages from occurring

[0.12.0](https://github.com/jshwi/docsig/releases/tag/v0.12.0) - 2022-06-28
------------------------------------------------------------------------
### Added
- Adds disable option
- Adds error for missing return type
- Adds error for documented property returns

### Fixed
- Allows for params with any amount of spaces before description

[0.11.0](https://github.com/jshwi/docsig/releases/tag/v0.11.0) - 2022-06-27
------------------------------------------------------------------------
### Changed
- Fails checks for missing docstring
- Ignores docstrings for overridden methods

[0.10.0](https://github.com/jshwi/docsig/releases/tag/v0.10.0) - 2022-06-26
------------------------------------------------------------------------
### Added
- Adds hint for missing returns
- Adds codes to printed messages

### Changed
- Fails checks with bad indentation

[0.9.0](https://github.com/jshwi/docsig/releases/tag/v0.9.0) - 2022-06-26
------------------------------------------------------------------------
### Added
- Adds hint for property returns
- Adds hint for missing parameters

### Fixed
- Ignores any number of underscore prefixes

[0.8.0](https://github.com/jshwi/docsig/releases/tag/v0.8.0) - 2022-06-25
------------------------------------------------------------------------
### Added
- Updates printing of subscript types and slices

### Fixed
- Fixes returning of binary operator types

[0.7.0](https://github.com/jshwi/docsig/releases/tag/v0.7.0) - 2022-06-24
------------------------------------------------------------------------
### Added
- Allows for multiple path arguments

[0.6.0](https://github.com/jshwi/docsig/releases/tag/v0.6.0) - 2022-06-21
------------------------------------------------------------------------
### Added
- Allows `key(word)` for `**kwargs`

### Changed
- Updates syntax highlighting

### Fixed
- Fixes returning of non-subscript types

[0.5.0](https://github.com/jshwi/docsig/releases/tag/v0.5.0) - 2022-06-21
------------------------------------------------------------------------
### Added
- Adds check for class methods

[0.4.0](https://github.com/jshwi/docsig/releases/tag/v0.4.0) - 2022-06-19
------------------------------------------------------------------------
### Added
- Adds support for `**kwargs`
- Adds support for `*args`

[0.3.0](https://github.com/jshwi/docsig/releases/tag/v0.3.0) - 2022-06-19
------------------------------------------------------------------------
### Added
- Adds check for incorrectly documented params

[0.2.0](https://github.com/jshwi/docsig/releases/tag/v0.2.0) - 2022-06-18
------------------------------------------------------------------------
### Added
- Adds summary for failed checks
- Adds check for returns
- Adds `docsig.messages` to public scope
- Ignores parameters named `_`

[0.1.0](https://github.com/jshwi/docsig/releases/tag/v0.1.0) - 2022-06-18
------------------------------------------------------------------------
### Added
- Initial release

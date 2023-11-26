Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/docsig/compare/v0.40.0...HEAD)
------------------------------------------------------------------------
### Added
- error handling for unknown target args
- error handling for unknown disable args
- functionality to disable checks by symbolic reference
- symbolic field to messages
- default template for error messages
- error object to `docsig.messages`
- option to check methods belonging to protected classes

### Fixed
- use system agnostic root when finding pyproject.toml

### Removed
- error constants in `docsig.messages`
- hint constants in `docsig.messages`

[0.40.0](https://github.com/jshwi/docsig/releases/tag/v0.40.0) - 2023-11-25
------------------------------------------------------------------------
### Added
- option to check `__init__` against its own docstring

[0.39.1](https://github.com/jshwi/docsig/releases/tag/v0.39.1) - 2023-11-23
------------------------------------------------------------------------
### Fixed
- catch unknown single options

[0.39.0](https://github.com/jshwi/docsig/releases/tag/v0.39.0) - 2023-11-20
------------------------------------------------------------------------
### Added
- add errors for directive options
- add errors for invalid comment directives
- add function name to summary report header

### Changed
- sort errors for report output

### Fixed
- do not treat unknown comment directive as an enabler

[0.38.0](https://github.com/jshwi/docsig/releases/tag/v0.38.0) - 2023-11-18
------------------------------------------------------------------------
### Added
- add support for enabling individual errors with comments
- add support for disabling individual errors with comments

[0.37.0](https://github.com/jshwi/docsig/releases/tag/v0.37.0) - 2023-11-17
------------------------------------------------------------------------
### Added
- raise error if file not found
- add user friendly errors for the commandline

### Fixed
- fix index error raised with alternative comment formats

[0.36.1](https://github.com/jshwi/docsig/releases/tag/v0.36.1) - 2023-11-17
------------------------------------------------------------------------
### Fixed
- fix handling of params for overloaded functions

[0.36.0](https://github.com/jshwi/docsig/releases/tag/v0.36.0) - 2023-11-14
------------------------------------------------------------------------
### Added
- add support for disable comments
- add support for overloaded functions

[0.35.0](https://github.com/jshwi/docsig/releases/tag/v0.35.0) - 2023-08-09
------------------------------------------------------------------------
### Changed
- remove default value for positional arguments

[0.34.2](https://github.com/jshwi/docsig/releases/tag/v0.34.2) - 2023-08-08
------------------------------------------------------------------------
### Fixed
- recognize positional-only arguments with methods

[0.34.1](https://github.com/jshwi/docsig/releases/tag/v0.34.1) - 2023-08-05
------------------------------------------------------------------------
### Fixed
- recognize positional-only arguments

[0.34.0](https://github.com/jshwi/docsig/releases/tag/v0.34.0) - 2023-01-23
------------------------------------------------------------------------
### Added
- Add support for Python 3.10

[0.33.2](https://github.com/jshwi/docsig/releases/tag/v0.33.2) - 2023-01-05
------------------------------------------------------------------------
### Fix
- Relax `arcon` version constraint

[0.33.1](https://github.com/jshwi/docsig/releases/tag/v0.33.1) - 2022-12-24
------------------------------------------------------------------------
### Fixed
- Fix incorrect `pre-commit` documentation

[0.33.0](https://github.com/jshwi/docsig/releases/tag/v0.33.0) - 2022-12-21
------------------------------------------------------------------------
### Added
- Add `-k/--ignore-kwargs` argument
- Add `-a/--ignore-args` argument

[0.32.0](https://github.com/jshwi/docsig/releases/tag/v0.32.0) - 2022-12-11
------------------------------------------------------------------------
### Added
- Add `-P/--check-property-returns` argument

[0.31.0](https://github.com/jshwi/docsig/releases/tag/v0.31.0) - 2022-12-11
------------------------------------------------------------------------
### Added
- Add `-i/--ignore-no-params` argument

### Changed
- `E109` raised only if docstring exists

[0.30.1](https://github.com/jshwi/docsig/releases/tag/v0.30.1) - 2022-12-10
------------------------------------------------------------------------
### Fixed
- Fix issue where str annotation for return was considered None

[0.30.0](https://github.com/jshwi/docsig/releases/tag/v0.30.0) - 2022-12-09
------------------------------------------------------------------------
### Added
- Add support for `pre-commit`

[0.29.0](https://github.com/jshwi/docsig/releases/tag/v0.29.0) - 2022-12-09
------------------------------------------------------------------------
### Added
- Add linkable path and line number

### Changed
- Update display for `-s/--summary`

[0.28.0](https://github.com/jshwi/docsig/releases/tag/v0.28.0) - 2022-12-04
------------------------------------------------------------------------
### Changed
- Generate function string representation only if function fails

[0.27.0](https://github.com/jshwi/docsig/releases/tag/v0.27.0) - 2022-12-04
------------------------------------------------------------------------
### Changed
- Update display of docstring
- Display `key` for docstring kwargs

[0.26.1](https://github.com/jshwi/docsig/releases/tag/v0.26.1) - 2022-11-30
------------------------------------------------------------------------
### Fixed
- Fix issue where dashes in config were not being parsed correctly

[0.26.0](https://github.com/jshwi/docsig/releases/tag/v0.26.0) - 2022-11-30
------------------------------------------------------------------------
### Added
- Add `E116` error for poor indentation
- Add `E115` error for syntax errors in description
- Add `E114` error for missing class docstring
- Add `messages` to `__all__`

[0.25.0](https://github.com/jshwi/docsig/releases/tag/v0.25.0) - 2022-11-28
------------------------------------------------------------------------
### Added
- Add `E113` error for missing docstring

### Fixed
- Fix error code displayed for `E112`

[0.24.1](https://github.com/jshwi/docsig/releases/tag/v0.24.1) - 2022-11-27
------------------------------------------------------------------------
### Fixed
- Allow asterisks in `Sphinx` docstrings

[0.24.0](https://github.com/jshwi/docsig/releases/tag/v0.24.0) - 2022-11-26
------------------------------------------------------------------------
### Added
- Add support for `Google` docstrings

### Fixed
- Accept `returns` keyword for return

[0.23.4](https://github.com/jshwi/docsig/releases/tag/v0.23.4) - 2022-11-25
------------------------------------------------------------------------
### Fixed
- Remove requirement for typed `numpy` docstrings

[0.23.3](https://github.com/jshwi/docsig/releases/tag/v0.23.3) - 2022-11-25
------------------------------------------------------------------------
### Fixed
- Fix `numpy` docstring syntax for handling args
- Fix `numpy` docstring syntax for kwargs in `Parameters` group
- Fix `numpy` docstring syntax for kwargs under `Parameters` section

[0.23.2](https://github.com/jshwi/docsig/releases/tag/v0.23.2) - 2022-11-23
------------------------------------------------------------------------
### Fixed
- Remove check for spaced colon in `numpy` style docstrings
- Remove indent requirement for `numpy` style docstrings

[0.23.1](https://github.com/jshwi/docsig/releases/tag/v0.23.1) - 2022-11-06
------------------------------------------------------------------------
### Fixed
- Fixes check for `numpy` style docstring

[0.23.0](https://github.com/jshwi/docsig/releases/tag/v0.23.0) - 2022-08-29
------------------------------------------------------------------------
### Added
- Adds check for `numpy` style docstrings

[0.22.0](https://github.com/jshwi/docsig/releases/tag/v0.22.0) - 2022-07-16
------------------------------------------------------------------------
### Added
- Adds `-n/--no-ansi` argument
- Adds `-S/--summary` argument

[0.21.0](https://github.com/jshwi/docsig/releases/tag/v0.21.0) - 2022-07-15
------------------------------------------------------------------------
### Added
- Adds `E112` for spelling errors

[0.20.0](https://github.com/jshwi/docsig/releases/tag/v0.20.0) - 2022-07-15
------------------------------------------------------------------------
### Added
- Adds `-D/--check-dunders` argument
- Adds `-o/--check-overridden` argument

### Changed
- Changes dunder methods to no longer be considered private
- Changes class constructor to no longer be considered a private method
- Changes class constructor to no longer be considered a dunder method

[0.19.0](https://github.com/jshwi/docsig/releases/tag/v0.19.0) - 2022-07-14
------------------------------------------------------------------------
### Added
- Adds `-p/--check-protected` argument

### Fixed
- Fixes issue where `self` and `cls` were the only first args ignored
- Fixes issue where `self` and `cls` were ignored for static methods
- Fixes issue where any func named `__init__` was not protected
- Fixes issue where any function could be a property

[0.18.0](https://github.com/jshwi/docsig/releases/tag/v0.18.0) - 2022-07-13
------------------------------------------------------------------------
### Added
- Adds `E111` check for classes that document a return

### Fixed
- Removes `E104` check for class docstrings
- Removes `E105` check for class docstrings
- Removes `E109` check for class docstrings

[0.17.0](https://github.com/jshwi/docsig/releases/tag/v0.17.0) - 2022-07-13
------------------------------------------------------------------------
### Added
- Adds `-c/--check-class` argument

[0.16.0](https://github.com/jshwi/docsig/releases/tag/v0.16.0) - 2022-07-12
------------------------------------------------------------------------
### Added
- Adds `-s/--string` argument
- Adds `docsig` function for API usage
- Adds default path argument as current working dir

### Fixed
- Fixes issue where keyword only args were not recognised

[0.15.0](https://github.com/jshwi/docsig/releases/tag/v0.15.0) - 2022-07-11
------------------------------------------------------------------------
### Added
- Adds line number to report

[0.14.0](https://github.com/jshwi/docsig/releases/tag/v0.14.0) - 2022-07-10
------------------------------------------------------------------------
### Added
- Adds `E110` catch-all for documentation not equal to its signature

### Fixed
- Fixes issue where `docsig -v` did not print version

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

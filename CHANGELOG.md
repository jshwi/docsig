# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/)
and the changes for the upcoming release can be found in
<https://github.com/jshwi/docsig/tree/main/changelog/>.

<!-- release notes start -->

## [0.72.1](https://github.com/jshwi/docsig/tree/v0.72.1) - 2025-12-24

### Fixed

- incorrect params-out-of-order ([#660](https://github.com/jshwi/docsig/issues/660))

## [0.72.0](https://github.com/jshwi/docsig/tree/v0.72.0) - 2025-12-13

### Added

- support for python3.14 ([#658](https://github.com/jshwi/docsig/issues/658))

### Changed

- drop support for python3.9 ([#656](https://github.com/jshwi/docsig/issues/656))

## [0.71.0](https://github.com/jshwi/docsig/tree/v0.71.0) - 2025-07-08

### Added

- option to enforce description capitalization ([#591](https://github.com/jshwi/docsig/issues/591))

## [0.70.0](https://github.com/jshwi/docsig/tree/v0.70.0) - 2025-07-03

### Changed

- drop support for python3.8 ([#565](https://github.com/jshwi/docsig/issues/565))

## [0.69.4](https://github.com/jshwi/docsig/tree/v0.69.4) - 2025-06-21

### Fixed

- ignore indents within directives ([#562](https://github.com/jshwi/docsig/issues/562))

## [0.69.3](https://github.com/jshwi/docsig/tree/v0.69.3) - 2025-03-08

### Fixed

- allow yield as a return doc ([#550](https://github.com/jshwi/docsig/issues/550))

## [0.69.2](https://github.com/jshwi/docsig/tree/v0.69.2) - 2025-03-08

### Fixed

- allow binary bitwise operator ([#545](https://github.com/jshwi/docsig/issues/545))

## [0.69.1](https://github.com/jshwi/docsig/tree/v0.69.1) - 2025-02-22

### Fixed

- params-out-of-order showing on single doc ([#542](https://github.com/jshwi/docsig/issues/542))

## [0.69.0](https://github.com/jshwi/docsig/tree/v0.69.0) - 2025-02-06

### Removed

- support for old-style messages ([#536](https://github.com/jshwi/docsig/issues/536))

## [0.68.0](https://github.com/jshwi/docsig/tree/v0.68.0) - 2025-02-01

### Added

- support relative paths - @niall-byrne ([#522](https://github.com/jshwi/docsig/issues/522))

### Fixed

- fix crash with broken symlinks ([#531](https://github.com/jshwi/docsig/issues/531))

## [0.67.0](https://github.com/jshwi/docsig/tree/v0.67.0) - 2025-01-27

### Added

- support for python3.13 ([#511](https://github.com/jshwi/docsig/issues/511))
- return-description-missing violation ([#525](https://github.com/jshwi/docsig/issues/525))

### Fixed

- description-missing appears in duplicate check ([#523](https://github.com/jshwi/docsig/issues/523))

## [0.66.1](https://github.com/jshwi/docsig/tree/v0.66.1) - 2024-12-30

### Fixed

- recognize all decorators when stacked ([#509](https://github.com/jshwi/docsig/issues/509))

## [0.66.0](https://github.com/jshwi/docsig/tree/v0.66.0) - 2024-12-24

### Added

- bad-closing-token violation ([#507](https://github.com/jshwi/docsig/issues/507))

## [0.65.0](https://github.com/jshwi/docsig/tree/v0.65.0) - 2024-11-27

### Removed

- summary option ([#495](https://github.com/jshwi/docsig/issues/495))

## [0.64.1](https://github.com/jshwi/docsig/tree/v0.64.1) - 2024-11-10

### Fixed

- correctly load config for windows ([#488](https://github.com/jshwi/docsig/issues/488))

## [0.64.0](https://github.com/jshwi/docsig/tree/v0.64.0) - 2024-10-04

### Added

- unicode decode error ([#472](https://github.com/jshwi/docsig/issues/472))

### Changed

- raise invalid-syntax if a string cannot be parsed ([#471](https://github.com/jshwi/docsig/issues/471))

## [0.63.0](https://github.com/jshwi/docsig/tree/v0.63.0) - 2024-09-29

### Changed

- return 123 when there is a syntax error ([#463](https://github.com/jshwi/docsig/issues/463))

## [0.62.1](https://github.com/jshwi/docsig/tree/v0.62.1) - 2024-09-28

### Fixed

- fix missing description with multiple args ([#461](https://github.com/jshwi/docsig/issues/461))

## [0.62.0](https://github.com/jshwi/docsig/tree/v0.62.0) - 2024-09-27

### Changed

- handle syntax error as a violation ([#455](https://github.com/jshwi/docsig/issues/455))

## [0.61.1](https://github.com/jshwi/docsig/tree/v0.61.1) - 2024-09-22

### Fixed

- disallow both class args with flake8 ([#452](https://github.com/jshwi/docsig/issues/452))

## [0.61.0](https://github.com/jshwi/docsig/tree/v0.61.0) - 2024-09-20

### Added

- verbose option to flake8 plugin ([#445](https://github.com/jshwi/docsig/issues/445))

### Changed

- vendor arcon ([#447](https://github.com/jshwi/docsig/issues/447))

## [0.60.1](https://github.com/jshwi/docsig/tree/v0.60.1) - 2024-08-29

### Fixed

- only check params for incorrect-indent ([#427](https://github.com/jshwi/docsig/issues/427))

## [0.60.0](https://github.com/jshwi/docsig/tree/v0.60.0) - 2024-07-31

### Added

- excludes option for path glob patterns ([#393](https://github.com/jshwi/docsig/issues/393))

## [0.59.3](https://github.com/jshwi/docsig/tree/v0.59.3) - 2024-07-28

### Fixed

- default exclude pattern for __pycache__ ([#396](https://github.com/jshwi/docsig/issues/396))

## [0.59.2](https://github.com/jshwi/docsig/tree/v0.59.2) - 2024-07-27

### Fixed

- handle directory exclude patterns ([#392](https://github.com/jshwi/docsig/issues/392))

## [0.59.1](https://github.com/jshwi/docsig/tree/v0.59.1) - 2024-07-17

### Fixed

- handle unicode decode error ([#384](https://github.com/jshwi/docsig/issues/384))

## [0.59.0](https://github.com/jshwi/docsig/tree/v0.59.0) - 2024-07-16

### Changed

- sort checked paths ([#381](https://github.com/jshwi/docsig/issues/381))

## [0.58.0](https://github.com/jshwi/docsig/tree/v0.58.0) - 2024-07-15

### Changed

- remove click from dependencies ([#376](https://github.com/jshwi/docsig/issues/376))

## [0.57.0](https://github.com/jshwi/docsig/tree/v0.57.0) - 2024-07-03

### Added

- docsig as a flake8 plugin ([#368](https://github.com/jshwi/docsig/issues/368))

## [0.56.0](https://github.com/jshwi/docsig/tree/v0.56.0) - 2024-06-23

### Changed

- error codes

### Deprecated

- old style messages

## [0.55.0](https://github.com/jshwi/docsig/tree/v0.55.0) - 2024-06-12

### Changed

- rename targets parameter to target in docsig function

## [0.54.1](https://github.com/jshwi/docsig/tree/v0.54.1) - 2024-05-23

### Fixed

- issue where spelling-error could only occur alone

## [0.54.0](https://github.com/jshwi/docsig/tree/v0.54.0) - 2024-05-21

### Added

- description-missing check

### Changed

- reword description for confirm-return-needed

### Fixed

- adjust docstring to match signature once params-missing evaluated

## [0.53.3](https://github.com/jshwi/docsig/tree/v0.53.3) - 2024-05-13

### Fixed

- param-not-equal-to-arg which should not be final catch-all

## [0.53.2](https://github.com/jshwi/docsig/tree/v0.53.2) - 2024-05-09

### Fixed

- raise E102 before E107 considered
- false positives in E105 hints
- method for detecting incorrectly indented parameter
- no longer rely on raising E102 errors to raise E106
- no longer rely on raising E101 errors to raise E106
- raise E107 without relying on other errors
- issue where E106 needed parameter name and description to match

## [0.53.1](https://github.com/jshwi/docsig/tree/v0.53.1) - 2024-05-06

### Fixed

- no longer raise E104 with optional overload ([#318](https://github.com/jshwi/docsig/issues/318))

## [0.53.0](https://github.com/jshwi/docsig/tree/v0.53.0) - 2024-05-01

### Added

- hint for confirm-return-needed
- arg for ignoring return type checker

### Changed

- output to summarised version
- remove color from help

### Deprecated

- summary option as this is now the report format

## [0.52.0](https://github.com/jshwi/docsig/tree/v0.52.0) - 2024-04-29

### Added

- message types to messages module

## [0.51.1](https://github.com/jshwi/docsig/tree/v0.51.1) - 2024-04-27

### Fixed

- import alias for imported decorators

## [0.51.0](https://github.com/jshwi/docsig/tree/v0.51.0) - 2024-04-23

### Added

- exclude files in gitignore

### Fixed

- send path in syntax error to stderr

## [0.50.0](https://github.com/jshwi/docsig/tree/v0.50.0) - 2024-04-23

### Added

- successfully parsed file to verbose output

### Changed

- improve syntax error message
- continue running all the way through on syntax error

## [0.49.2](https://github.com/jshwi/docsig/tree/v0.49.2) - 2024-04-21

### Fixed

- indent for hints

## [0.49.1](https://github.com/jshwi/docsig/tree/v0.49.1) - 2024-04-20

### Fixed

- apply no-ansi option to excepthook
- ensure colors are removed when not running in a tty
- ensure excepthook prints to stderr
- use click echo for excepthook

## [0.49.0](https://github.com/jshwi/docsig/tree/v0.49.0) - 2024-04-20

### Changed

- use click echo

## [0.48.0](https://github.com/jshwi/docsig/tree/v0.48.0) - 2024-04-19

### Changed

- replace tabs with spaces in summary
- remove typing-extensions from dependencies

## [0.47.0](https://github.com/jshwi/docsig/tree/v0.47.0) - 2024-04-14

### Added

- option for checking nested functions and classes ([#293](https://github.com/jshwi/docsig/issues/293))

### Fixed

- check indented functions and classes ([#293](https://github.com/jshwi/docsig/issues/293))

## [0.46.0](https://github.com/jshwi/docsig/tree/v0.46.0) - 2024-04-09

### Added

- verbose option

### Changed

- short form for version

## [0.45.0](https://github.com/jshwi/docsig/tree/v0.45.0) - 2024-04-09

### Added

- exclude option

### Fixed

- allow decorators to be referenced with module name
- allow checking of files not ending in .py

## [0.44.3](https://github.com/jshwi/docsig/tree/v0.44.3) - 2024-03-24

### Fixed

- treat `functools.cached_property` as a property

## [0.44.2](https://github.com/jshwi/docsig/tree/v0.44.2) - 2023-12-03

### Fixed

- wrap function with functools.wraps

## [0.44.1](https://github.com/jshwi/docsig/tree/v0.44.1) - 2023-12-01

### Fixed

- class checks can now be disabled with comments

## [0.44.0](https://github.com/jshwi/docsig/tree/v0.44.0) - 2023-11-30

### Added

- help when both class args are configured in pyproject.toml file
- check for both class args when not running the commandline
- report all errors instead of just the first

### Changed

- return string instead of raising for api
- raise system exit instead of value error

## [0.43.0](https://github.com/jshwi/docsig/tree/v0.43.0) - 2023-11-28

### Added

- option to list checks and their messages

### Fixed

- correct symbolic message for E204
- allow paths as strings when using api
- allow for passing string argument via commandline

## [0.42.1](https://github.com/jshwi/docsig/tree/v0.42.1) - 2023-11-27

### Fixed

- ensure files are read with utf-8 encoding

## [0.42.0](https://github.com/jshwi/docsig/tree/v0.42.0) - 2023-11-26

### Added

- support for python3.12

## [0.41.0](https://github.com/jshwi/docsig/tree/v0.41.0) - 2023-11-26

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

## [0.40.0](https://github.com/jshwi/docsig/tree/v0.40.0) - 2023-11-25

### Added

- option to check `__init__` against its own docstring ([#195](https://github.com/jshwi/docsig/issues/195))

## [0.39.1](https://github.com/jshwi/docsig/tree/v0.39.1) - 2023-11-23

### Fixed

- catch unknown single options

## [0.39.0](https://github.com/jshwi/docsig/tree/v0.39.0) - 2023-11-20

### Added

- add errors for directive options
- add errors for invalid comment directives
- add function name to summary report header

### Changed

- sort errors for report output

### Fixed

- do not treat unknown comment directive as an enabler

## [0.38.0](https://github.com/jshwi/docsig/tree/v0.38.0) - 2023-11-18

### Added

- add support for enabling individual errors with comments
- add support for disabling individual errors with comments

## [0.37.0](https://github.com/jshwi/docsig/tree/v0.37.0) - 2023-11-17

### Added

- raise error if file not found
- add user friendly errors for the commandline

### Fixed

- fix index error raised with alternative comment formats

## [0.36.1](https://github.com/jshwi/docsig/tree/v0.36.1) - 2023-11-17

### Fixed

- fix handling of params for overloaded functions

## [0.36.0](https://github.com/jshwi/docsig/tree/v0.36.0) - 2023-11-14

### Added

- add support for disable comments
- add support for overloaded functions ([#196](https://github.com/jshwi/docsig/issues/196))

## [0.35.0](https://github.com/jshwi/docsig/tree/v0.35.0) - 2023-08-09

### Changed

- remove default value for positional arguments

## [0.34.2](https://github.com/jshwi/docsig/tree/v0.34.2) - 2023-08-08

### Fixed

- recognize positional-only arguments with methods

## [0.34.1](https://github.com/jshwi/docsig/tree/v0.34.1) - 2023-08-05

### Fixed

- recognize positional-only arguments

## [0.34.0](https://github.com/jshwi/docsig/tree/v0.34.0) - 2023-01-23

### Added

- Add support for Python 3.10 ([#65](https://github.com/jshwi/docsig/issues/65))

## [0.33.2](https://github.com/jshwi/docsig/tree/v0.33.2) - 2023-01-05

### Fix

- Relax `arcon` version constraint

## [0.33.1](https://github.com/jshwi/docsig/tree/v0.33.1) - 2022-12-24

### Fixed

- Fix incorrect `pre-commit` documentation ([#50](https://github.com/jshwi/docsig/issues/50))

## [0.33.0](https://github.com/jshwi/docsig/tree/v0.33.0) - 2022-12-21

### Added

- Add `-k/--ignore-kwargs` argument ([#48](https://github.com/jshwi/docsig/issues/48))
- Add `-a/--ignore-args` argument ([#48](https://github.com/jshwi/docsig/issues/48))

## [0.32.0](https://github.com/jshwi/docsig/tree/v0.32.0) - 2022-12-11

### Added

- Add `-P/--check-property-returns` argument

## [0.31.0](https://github.com/jshwi/docsig/tree/v0.31.0) - 2022-12-11

### Added

- Add `-i/--ignore-no-params` argument ([#45](https://github.com/jshwi/docsig/issues/45))

### Changed

- `E109` raised only if docstring exists

## [0.30.1](https://github.com/jshwi/docsig/tree/v0.30.1) - 2022-12-10

### Fixed

- Fix issue where str annotation for return was considered None ([#44](https://github.com/jshwi/docsig/issues/44))

## [0.30.0](https://github.com/jshwi/docsig/tree/v0.30.0) - 2022-12-09

### Added

- Add support for `pre-commit` ([#39](https://github.com/jshwi/docsig/issues/39))

## [0.29.0](https://github.com/jshwi/docsig/tree/v0.29.0) - 2022-12-09

### Added

- Add linkable path and line number ([#40](https://github.com/jshwi/docsig/issues/40))

### Changed

- Update display for `-s/--summary`

## [0.28.0](https://github.com/jshwi/docsig/tree/v0.28.0) - 2022-12-04

### Changed

- Generate function string representation only if function fails

## [0.27.0](https://github.com/jshwi/docsig/tree/v0.27.0) - 2022-12-04

### Changed

- Update display of docstring
- Display `key` for docstring kwargs

## [0.26.1](https://github.com/jshwi/docsig/tree/v0.26.1) - 2022-11-30

### Fixed

- Fix issue where dashes in config were not being parsed correctly

## [0.26.0](https://github.com/jshwi/docsig/tree/v0.26.0) - 2022-11-30

### Added

- Add `E116` error for poor indentation
- Add `E115` error for syntax errors in description
- Add `E114` error for missing class docstring
- Add `messages` to `__all__`

## [0.25.0](https://github.com/jshwi/docsig/tree/v0.25.0) - 2022-11-28

### Added

- Add `E113` error for missing docstring

### Fixed

- Fix error code displayed for `E112`

## [0.24.1](https://github.com/jshwi/docsig/tree/v0.24.1) - 2022-11-27

### Fixed

- Allow asterisks in `Sphinx` docstrings

## [0.24.0](https://github.com/jshwi/docsig/tree/v0.24.0) - 2022-11-26

### Added

- Add support for `Google` docstrings

### Fixed

- Accept `returns` keyword for return

## [0.23.4](https://github.com/jshwi/docsig/tree/v0.23.4) - 2022-11-25

### Fixed

- Remove requirement for typed `numpy` docstrings

## [0.23.3](https://github.com/jshwi/docsig/tree/v0.23.3) - 2022-11-25

### Fixed

- Fix `numpy` docstring syntax for handling args
- Fix `numpy` docstring syntax for kwargs in `Parameters` group
- Fix `numpy` docstring syntax for kwargs under `Parameters` section

## [0.23.2](https://github.com/jshwi/docsig/tree/v0.23.2) - 2022-11-23

### Fixed

- Remove check for spaced colon in `numpy` style docstrings ([#36](https://github.com/jshwi/docsig/issues/36))
- Remove indent requirement for `numpy` style docstrings ([#36](https://github.com/jshwi/docsig/issues/36))

## [0.23.1](https://github.com/jshwi/docsig/tree/v0.23.1) - 2022-11-06

### Fixed

- Fixes check for `numpy` style docstring

## [0.23.0](https://github.com/jshwi/docsig/tree/v0.23.0) - 2022-08-29

### Added

- Adds check for `numpy` style docstrings ([#14](https://github.com/jshwi/docsig/issues/14))

## [0.22.0](https://github.com/jshwi/docsig/tree/v0.22.0) - 2022-07-16

### Added

- Adds `-n/--no-ansi` argument
- Adds `-S/--summary` argument

## [0.21.0](https://github.com/jshwi/docsig/tree/v0.21.0) - 2022-07-15

### Added
- Adds `E112` for spelling errors ([#7](https://github.com/jshwi/docsig/issues/7))

## [0.20.0](https://github.com/jshwi/docsig/tree/v0.20.0) - 2022-07-15

### Added

- Adds `-D/--check-dunders` argument
- Adds `-o/--check-overridden` argument

### Changed

- Changes dunder methods to no longer be considered private
- Changes class constructor to no longer be considered a private method
- Changes class constructor to no longer be considered a dunder method

## [0.19.0](https://github.com/jshwi/docsig/tree/v0.19.0) - 2022-07-14

### Added

- Adds `-p/--check-protected` argument

### Fixed

- Fixes issue where `self` and `cls` were the only first args ignored
- Fixes issue where `self` and `cls` were ignored for static methods
- Fixes issue where any func named `__init__` was not protected
- Fixes issue where any function could be a property

## [0.18.0](https://github.com/jshwi/docsig/tree/v0.18.0) - 2022-07-13

### Added

- Adds `E111` check for classes that document a return

### Fixed

- Removes `E104` check for class docstrings
- Removes `E105` check for class docstrings
- Removes `E109` check for class docstrings

## [0.17.0](https://github.com/jshwi/docsig/tree/v0.17.0) - 2022-07-13

### Added

- Adds `-c/--check-class` argument

## [0.16.0](https://github.com/jshwi/docsig/tree/v0.16.0) - 2022-07-12

### Added

- Adds `-s/--string` argument
- Adds `docsig` function for API usage
- Adds default path argument as current working dir

### Fixed

- Fixes issue where keyword only args were not recognised

## [0.15.0](https://github.com/jshwi/docsig/tree/v0.15.0) - 2022-07-11

### Added

- Adds line number to report

## [0.14.0](https://github.com/jshwi/docsig/tree/v0.14.0) - 2022-07-10

### Added

- Adds `E110` catch-all for documentation not equal to its signature

### Fixed

- Fixes issue where `docsig -v` did not print version

## [0.13.0](https://github.com/jshwi/docsig/tree/v0.13.0) - 2022-07-02

### Added

- Adds target option

## [0.12.1](https://github.com/jshwi/docsig/tree/v0.12.1) - 2022-06-29

### Fixed

- Prevents duplicate error messages from occurring

## [0.12.0](https://github.com/jshwi/docsig/tree/v0.12.0) - 2022-06-28

### Added

- Adds disable option
- Adds error for missing return type
- Adds error for documented property returns

### Fixed

- Allows for params with any amount of spaces before description

## [0.11.0](https://github.com/jshwi/docsig/tree/v0.11.0) - 2022-06-27

### Changed

- Fails checks for missing docstring
- Ignores docstrings for overridden methods

## [0.10.0](https://github.com/jshwi/docsig/tree/v0.10.0) - 2022-06-26

### Added

- Adds hint for missing returns
- Adds codes to printed messages

### Changed

- Fails checks with bad indentation

## [0.9.0](https://github.com/jshwi/docsig/tree/v0.9.0) - 2022-06-26

### Added

- Adds hint for property returns
- Adds hint for missing parameters

### Fixed

- Ignores any number of underscore prefixes

## [0.8.0](https://github.com/jshwi/docsig/tree/v0.8.0) - 2022-06-25

### Added

- Updates printing of subscript types and slices

### Fixed

- Fixes returning of binary operator types

## [0.7.0](https://github.com/jshwi/docsig/tree/v0.7.0) - 2022-06-24

### Added

- Allows for multiple path arguments

## [0.6.0](https://github.com/jshwi/docsig/tree/v0.6.0) - 2022-06-21

### Added

- Allows `key(word)` for `**kwargs`

### Changed

- Updates syntax highlighting

### Fixed

- Fixes returning of non-subscript types

## [0.5.0](https://github.com/jshwi/docsig/tree/v0.5.0) - 2022-06-21

### Added

- Adds check for class methods

## [0.4.0](https://github.com/jshwi/docsig/tree/v0.4.0) - 2022-06-19

### Added

- Adds support for `**kwargs`
- Adds support for `*args`

## [0.3.0](https://github.com/jshwi/docsig/tree/v0.3.0) - 2022-06-19

### Added

- Adds check for incorrectly documented params

## [0.2.0](https://github.com/jshwi/docsig/tree/v0.2.0) - 2022-06-18

### Added

- Adds summary for failed checks
- Adds check for returns
- Adds `docsig.messages` to public scope
- Ignores parameters named `_`

## [0.1.0](https://github.com/jshwi/docsig/tree/v0.1.0) - 2022-06-18

### Added

- Initial release

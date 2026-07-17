# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**docsig** is a Python documentation linter that checks function/method signatures match their docstring parameter documentation. It supports reStructuredText (Sphinx), NumPy, and Google docstring formats. It ships as a CLI tool, a flake8 plugin, and a pyproject.toml schema validator.

## Development Setup

This project uses **Poetry** (version pinned in `.poetry-version`) with a local virtualenv.

```bash
make install-poetry   # install Poetry to bin/poetry/
make install-venv     # create .venv and install all dependencies
```

Invoke Poetry as `bin/poetry/bin/poetry` (or use the make targets, which wire
this up) — a global `poetry` on PATH may not match `.poetry-version`.

## Commands

```bash
# Run all tests (doctest + pytest + script tests)
make tests

# Run only source tests (doctest + pytest with coverage)
make test-source

# Run pytest directly (faster, no doctest)
poetry run pytest -n=auto --cov=docsig --cov=tests

# Run a single test file
poetry run pytest tests/base_test.py -vv

# Run doctests only
poetry run pytest docs README.rst --doctest-glob='*.rst'

# Lint (pylint + docsig on itself)
make lint

# Format (black + flynt + isort)
make format

# Type check (mypy)
make types

# Run benchmarks
make benchmark   # sets RUN_BENCHMARK=true, uses pytest -m=benchmark

# Run the working tree
python -m docsig ...   # a bare `docsig` command may resolve to a stale shim
```

Coverage must remain at **100%** (`fail_under = 100` in pyproject.toml).

## Architecture

### Data Flow

```
CLI args / pyproject.toml
  │
  _config.py (Config)
  │
  _parsers.py → _module.py (Module/Class/Function AST wrappers)
  │
  _check.py (traverse functions)
  │
  _report.py (per-function validation, emits error codes)
  │
  _diagnostic.py (Collector / Diagnostic / Failures)
  │
  _report.py (text or JSON output)
```

### Key Modules

| Module                | Role                                                                                 |
| --------------------- | ------------------------------------------------------------------------------------ |
| `_core.py`            | `docsig()` entry point — wires config, file discovery, checks, and reporting         |
| `_main.py`            | CLI argument parsing and top-level exception handling                                |
| `_config.py`          | `Config`, `Check`, `Ignore` dataclasses; loads from pyproject.toml                   |
| `_module.py`          | AST-backed `Module`, `Class`, `Function` types with parsed signatures and docstrings |
| `_stub.py`            | Value-object types: `Param`, `Signature`, `Docstring`, return types                  |
| `_check.py`           | Traverses function tree, dispatches to `_report.py` per function                     |
| `_diagnostic.py`      | `Collector` aggregates results; `Diagnostic`/`FunctionResult`/`Failures`             |
| `_report.py`          | All individual check implementations; formats and prints diagnostics                 |
| `_parsers.py`         | Parses Python source files/strings into module object trees                          |
| `_files.py`           | File discovery; respects `.gitignore` and exclude patterns                           |
| `_directives.py`      | Handles inline `# noqa`-style suppression comments                                   |
| `_decorators.py`      | Decorators for `docsig()`: kwarg-to-`Message` parsing and argument validation        |
| `_hooks.py`           | `excepthook` for user-friendly errors (bypassed when `DOCSIG_DEBUG=1`)               |
| `_utils.py`           | Shared helpers: fuzzy string matching, sentence tokenizing, error printing           |
| `messages.py`         | All `Message` definitions and the `MessageMap`; error codes SIG0xx–SIG9xx            |
| `plugin/_flake8.py`   | Flake8 extension; wraps `docsig()` with `--sig-*` prefixed options                   |

### Error Code Ranges

- **SIG0xx** — configuration errors
- **SIG1xx** — missing/extra docstrings
- **SIG2xx** — signature/docstring parameter mismatches
- **SIG3xx** — parameter description issues
- **SIG4xx** — parameter checking details
- **SIG5xx** — return value checks
- **SIG9xx** — parse errors

### Configuration Precedence

pyproject.toml `[tool.docsig]` → CLI arguments override (CLI wins). The `Config` class in `_config.py` handles merging. For the flake8 plugin, all options are prefixed with `--sig-` to avoid conflicts.

### Editor Plugins

Editor integrations live under `plugin/` (`plugin/intellij`, `plugin/vscode`,
`plugin/neovim`). The neovim plugin is mirrored to the standalone
`jshwi/docsig.nvim` repo by the `publish-mirror` job in
`.github/workflows/build-neovim-plugin.yaml` on pushes to master (requires
the `DOCSIG_NVIM_DEPLOY_KEY` secret); users install `jshwi/docsig.nvim`, never
the monorepo root — the repo root must not be treated as a Neovim
runtimepath entry, since Neovim would recursively source every `.lua` file
under `plugin/`.

### Testing Patterns

Tests live in `tests/` and use fixtures to build temporary Python files on disk, run `docsig()` or the CLI against them, and assert on collected error codes. The `tests/plugins/` directory contains a custom `_gitignore` pytest plugin (added to `pythonpath` in pytest config). Script tests (`scripts/check_news.py`, `scripts/bump_version.py`) are tested separately via `make test-scripts`.

### Changelog / Release Workflow

- Changelog fragments go in `changelog/` (managed by **towncrier**)

To publish a release:

```bash
# 1. Verify all commits since last tag pass conform
git rebase v<prev> -x 'conform enforce'

# 2. Bump version on a temp branch (towncrier folds changelog fragments in)
git checkout -b bump
make bump part=patch   # or major|minor

# 3. Merge to master, push commits and tag
git checkout master && git merge bump && git push && git push --tags
git branch -d bump

# 4. Publish to PyPI
make publish

# 5. Create GitHub release using the new CHANGELOG.md section
gh release create v<N> --repo jshwi/docsig --title "v<N>" --notes "..."

# 6. Rebase dev/main onto master
git checkout dev/main && git rebase master && git push --force-with-lease
```

### wip → master promotion

Work lands on `dev/main` as `wip:` commits. When ready to ship:

1. Open a GitHub issue for the fix.
2. Check out the issue branch: `gh issue develop <N> --checkout`
3. Cherry-pick the wip commit onto the issue branch: `git cherry-pick <sha>`
4. Soft-reset to keep changes staged: `git reset --soft HEAD~1`
5. Run `make && git add . && git commit -s -m "fix: <subject> (#<N>)"` — the
  `commit-msg` hook creates the news fragment and blocks the first attempt.
6. Run `git add . && git commit -s -m "fix: <subject> (#<N>)"` again — succeeds.
7. Push, open a PR targeting `master`, wait for the pipeline.
8. Merge: `git checkout master && git merge <branch> && git push`

**wip subject → final subject:** strip `wip:`, add a colon after the type, append
the issue number.

```
wip: fix evaluate docstring when description is missing
 →  fix: evaluate docstring when description is missing (#922)
```

Do **not** open the GitHub issue or create news fragments manually — the hook
handles fragments, and the issue should only be opened once the commit is ready
to promote.

**Commit subjects must not contain `and`** — if you need `and`, split into two
commits.

**All commits need DCO sign-off** — conform enforces a `Signed-off-by` trailer,
so always commit with `git commit -s`.

**Atomic-commit exception for AI housekeeping:** changes to chore files like
`CLAUDE.md` are self-explanatory line by line, so a session's housekeeping can
be batched into a single `chore(ai): commit claude session` commit.

**Prerequisite refactors:** if the fix depends on a preparatory `refactor:`
commit, land it on master first via a temp branch before touching the issue
branch:

```bash
git checkout -b tmp
git commit -s -m "refactor: <subject>"
git checkout master && git merge tmp && git branch -d tmp && git push
```

Then rebase the issue branch onto the updated master before cherry-picking the
fix.

**`gh issue develop` only once:** running it a second time for the same issue
creates a `-1` suffixed branch. If that happens, delete both local and remote
copies of both branches before recreating.

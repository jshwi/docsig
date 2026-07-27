# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**docsig** is a Python documentation linter that checks function/method signatures match their docstring parameter documentation. It supports reStructuredText (Sphinx), NumPy, and Google docstring formats. It ships as a CLI tool, a flake8 plugin, and a pyproject.toml schema validator.

## Where Claude Works

Claude works in a clone at `~/Documents/Repos/claude/docsig`, never in the
maintainer's checkout at `~/Documents/Repos/Projects/docsig`. **That checkout
is read-only.** It may be read; it must never be written — no commits, no
`git config`, no `make`, and no running an interpreter inside the tree, since
that alone drops `__pycache__` into it. This is not a per-task choice and is
not a question to ask.

The clone carries two remotes: `origin` for GitHub and `local` for the
maintainer's `.git`. Work on `dev/main` is delivered by pushing a
`claude/<topic>-<date>` branch to `local`, which the maintainer folds in on
their side; pushing a *new branch ref* is fine, pushing onto their checked-out
branch is not. Promotions push to `origin` instead, and stop at an open pull
request.

The rule exists because a shared `.git` is genuinely unsafe here: the
`check_news.py` tests call `git init` without clearing the `GIT_DIR` git
exports to hook processes, and xdist workers once raced on the real
`.git/config` and set `core.bare = true`, breaking every checkout in the tree
mid-release. A `PreToolUse` hook now enforces the boundary rather than relying
on care.

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

Makefile file lists come from `git ls-files`, so brand-new modules are
invisible to `make lint`/`make types`/`make tests` until staged — `git add`
new files before trusting a green run, or a later stamp-cached hook pass can
mask a real failure. `rm -rf .make` forces the rest to rerun but not `types`,
whose only prerequisite is `.mypy_cache/CACHEDIR.TAG` — clear that cache too,
or mypy reports "Nothing to be done" over code it has never seen.

**A fresh worktree cannot commit until it has a `.venv`.** The pre-commit test
hook runs `make test-bump`, whose `scripts/bump_version.py` tests copy the repo
into a pytest tmpdir and run `make` there; without `.venv/bin/activate` that
copy fails and blocks the commit. The same tests also leave their fixtures —
`changelog/1.add.md` and a `toml-sort`-reformatted `pyproject.toml` — staged in
the *real* index, so clear those before retrying. Run `make install-venv` in a
new worktree first.

Coverage must remain at **100%** (`fail_under = 100` in pyproject.toml).

## Architecture

### Data Flow

```
CLI args / pyproject.toml
  │
  _config.py (Config)
  │
  _parsers.py → _scope.py (Scope/Function AST wrappers)
  │
  _traverse.py (traverse functions)
  │
  _checker.py (per-function validation, emits error codes)
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
| `_scope.py`           | AST-backed `Scope` and `Function` types with parsed signatures and docstrings        |
| `_stub.py`            | Value-object types: `Param`, `Signature`, `Docstring`, return types                  |
| `_traverse.py`        | Traverses function tree, dispatches to `_checker.py` per function                    |
| `_checker.py`         | All individual check implementations; each emits a `Message` on failure              |
| `_text.py`            | Text analysis helpers (sentence tokenizing, fuzzy match) for `_checker.py`           |
| `_diagnostic.py`      | `Collector` aggregates results; `Diagnostic`/`FunctionResult`/`Failures`             |
| `_report.py`          | Formats and prints diagnostics (plain text or `--json`)                              |
| `_parsers.py`         | Parses Python source files/strings into module object trees                          |
| `_files.py`           | File discovery; respects `.gitignore` and exclude patterns                           |
| `_directives.py`      | Handles inline `# noqa`-style suppression comments                                   |
| `_decorators.py`      | Decorators for `docsig()`: kwarg-to-`Message` parsing and argument validation        |
| `_hooks.py`           | `excepthook` for user-friendly errors (bypassed when `DOCSIG_DEBUG=1`)               |
| `messages.py`         | All `Message` definitions and the `MessageMap`; error codes SIG0xx–SIG9xx            |
| `plugin/_flake8.py`   | Flake8 extension; wraps `docsig()` with `--sig-*` prefixed options                   |

Any commit that renames, folds, or moves a module must update the Data Flow
diagram and Key Modules table above in that same commit — never deferred to a
later `chore(ai)` commit. Every file this document references must exist at
every commit, so history stays clean for `git rebase -x` checks.
`scripts/check_claude_md.py` enforces this (wired in as the `check-claude-md`
pre-commit hook); run it after any module restructuring.

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

Anything synced into that mirror must resolve inside its own tree, since the
mirror is cloned standalone and a `../..` path escapes into an unrelated
directory on a user's machine. `plugin/neovim/Makefile` is monorepo-only for
that reason and is excluded from the sync — the `Verify Mirror Is Self
Contained` step fails the publish if any synced file reaches above the root,
and the `Tag Version` step therefore reads `make version` from
`plugin/neovim`, not from the mirror.

Everything between the `<!-- Plugin description -->` markers in each
`plugin/*/README.md` is published as that integration's page on docsig.io by
`generate_integration_docs` (`docs/extensions/generate.py`), and the IntelliJ
build extracts its own marked block for the marketplace listing. Development
instructions belong *outside* the markers.

### Testing Patterns

Tests live in `tests/` and use fixtures to build temporary Python files on disk, run `docsig()` or the CLI against them, and assert on collected error codes. The `tests/plugins/` directory contains a custom `_gitignore` pytest plugin (added to `pythonpath` in pytest config). Script tests (`scripts/check_news.py`, `scripts/bump_version.py`) are tested separately via `make test-scripts`.

### Documentation

- The docs build with `-W` (warnings are errors), and every `.rst` file —
  including README.rst — is doctested. Console (`$`) code blocks are NOT
  doctested and drift silently; verify them manually when CLI output changes.
- Furo does not render `layout.html` (it ships an error page for anything
  inheriting it). Theme overrides belong in `docs/_templates/base.html`
  extending `!base.html`; SEO meta tags live in its `extrahead` block, with
  the description single-sourced from `conf.py` via `html_context`.
- Files pulled in only via `.. include::` must be added to `exclude_patterns`
  in `docs/conf.py`, or Sphinx also publishes them as standalone duplicate
  pages (and they land in the sitemap).
- Message pages (`docs/usage/messages/`) show the failing case and end with a
  doctested resolution example (exit `0`). `scripts/update_docs.py` scaffolds
  new pages but never overwrites — extend them by hand after generation.
- `make build` fails the first time README or generated docs regenerate
  (update-readme/update-docs stamp targets, same "blocks the first attempt"
  pattern as the commit-msg hook); rerun and commit the regenerated files.
- Read the Docs builds `latest` from master, so docs changes only go live on
  docsig.io once they reach master.

### Changelog / Release Workflow

- Changelog fragments go in `changelog/` (managed by **towncrier**)

A fragment's content is machine-derived from the commit subject — `check_news.py`
parses `^(\w+):\s+(.+)\s+\(#(\d+)\)$` and writes group 2 verbatim — and the
`commit-msg` hook **rewrites the file** whenever its text and the subject differ
(`commit description changed, updated <N>.fix.md`). Fragments therefore cannot be
hand-extended. Anything a fragment can't carry, such as a fix that surfaces new
violations on unchanged code, belongs in the hand-written `gh release create
--notes` body; stage that text in the PR body so it's findable at release time.

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

### Commit policy

**Commit subjects must not contain `and`** — if you need `and`, split into two
commits.

**Pick the commit type by what the change is, not by where it lands:** docs
pages are `doc:` commits and internal-only cleanups are `refactor:` commits,
even on `dev/main` — `wip:` is reserved for staged behavior changes, and
`chore(ai)` only covers AI housekeeping files like `CLAUDE.md`, never docs
content. A change that corrects expected behavior is a `fix` even when it
reads like a feature — subject it as `wip: fix ...`, not after the mechanism
(e.g. "fix commandline exclude ignored when configured in pyproject", not
"merge exclude patterns across config layers").

**`wip: fix` is reserved for `./docsig`** — only the Python package is subject
as an unscoped `wip: fix`. Everything else carries the scope of what it
touches, even when the change is a fix:

| Path                       | Scope                     |
| -------------------------- | ------------------------- |
| `docsig/`                  | none — `wip: fix ...`     |
| `plugin/intellij/src`      | `intellij-plugin`         |
| `plugin/vscode/src`        | `vscode-extension`        |
| `plugin/neovim/lua/docsig` | `neovim-plugin`           |
| `plugin/neovim/Makefile`   | `make` or `neovim-plugin` |

**Every fix commit carries a fix test:** a regression test in
`tests/fix_test.py` named `test_fix_<subject-ish>` whose docstring states the
problem it guards against, committed with the fix. Unit tests in other test
files don't satisfy this.

**All commits need DCO sign-off** — conform enforces a `Signed-off-by` trailer,
so always commit with `git commit -s`.

### Recording what Claude learns

CLAUDE.md holds three kinds of claim: **orientation** (the map — provenance is
the commit that moved the code), **preference** (the maintainer's), and **scar
tissue** (earned by something going wrong). Scar tissue is admitted only when
something actually failed *and* the repo doesn't already say it. No incident,
no rule — a lesson merely noticed goes in Claude's own memory instead.

Record it the moment it lands, never batched at session end: one `chore(ai)`
commit per rule, whose **body states the incident** — command, SHA, error —
self-contained, with no pointer to a transcript or memory file. The file gets
the rule, the commit gets the war story. A rule that supersedes another
rewrites it in place in the same commit rather than appending a qualifier
beside stale text. `.claude/skills/` follows the same policy, except a new
file's body states intent rather than an incident.

`scripts/check_ai_commit.py` (the `check-ai-commit` commit-msg hook) rejects a
bodyless `chore(ai)` commit, and batched subjects like `commit claude session`.
It cannot catch a rule never written, so before finishing a session sweep back
over it for anything learned but not committed.

### wip → master promotion

Work lands on `dev/main` as `wip:` commits. Shipping one means opening a GitHub
issue, cherry-picking onto the issue branch, letting the `commit-msg` hook build
the news fragment, and opening a PR targeting `master`.

The full procedure lives in the `promote-wip` skill
(`.claude/skills/promote-wip/SKILL.md`): every step, the hook's deliberate
first-attempt block, the conform rules the stripped subject must satisfy, the
prerequisite-refactor detour, and the `dev/main` rebase afterwards. Invoke the
skill rather than working from memory.

Two rules hold whether or not the skill is loaded:

- **Never open the GitHub issue or write news fragments by hand.** The issue is
  opened as part of the promotion, once the commit is ready; the hook owns the
  fragment.
- **The closing keyword belongs in the PR body.** `(#<N>)` in the commit subject
  is only a cross-reference and closes nothing, so open the PR **before**
  pushing master — otherwise there is no PR for the push to mark merged, and
  the issue stays open.

########################################################################
# Make Configuration
SHELL := /bin/bash
.DELETE_ON_ERROR:

# Extract version from pyproject.toml
# Use this instead of `$ uv version --short` as the version may be
# needed before uv is installed
VERSION := $(shell bash scripts/get_docsig_version.sh pyproject.toml)

# uv configuration
# CI already has a pinned uv on PATH from setup-uv, so let the
# environment point at it rather than bootstrapping a second copy
UV ?= bin/uv/uv
UV_VERSION := $(shell cat .uv-version)
# only ever bootstrap the copy under bin, never an overridden uv
ifeq ($(UV),bin/uv/uv)
	UV_BOOTSTRAP := bin/uv/uv
endif
# uv resolves the environment on every `run`; make already gates each
# target on $(VENV), so skip the redundant check
RUN := $(UV) run --no-sync

# File lists
PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py' ':!:*_vendor*')
PACKAGE_FILES := $(shell git ls-files "docsig/*.py")
TEST_FILES := $(shell git ls-files "tests/*.py")
DOCS_FILES := $(shell git ls-files \
	"docs/*.rst" "docs/*.md" "docs/_templates" "docs/static")

# Git directory, which is a file and not a directory when this is a
# worktree, so ask git where the real one is rather than assuming .git
GIT_DIR := $(shell git rev-parse --git-common-dir 2>/dev/null || echo .git)

# Virtual environment path
ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/activate
endif

# Build artifact
BUILD := dist/docsig-$(VERSION)-py3-none-any.whl

########################################################################
# Implicit Phony Targets
.PHONY: all
all: .make/pre-commit $(GIT_DIR)/blame-ignore-revs help

.PHONY: help
help: $(VENV)
	@$(RUN) python scripts/make_help.py

########################################################################
# Main Targets
$(BUILD): .make/doctest \
		.make/black \
		.make/flynt \
		.make/isort \
		.make/pylint \
		.make/docsig \
		.make/update-docs \
		.mypy_cache/CACHEDIR.TAG \
		README.rst \
		.make/doctest \
		coverage.xml \
		docs/_build/html/index.html
	@$(UV) build
	@touch $@

docs/_build/html/index.html: $(VENV) \
		$(PYTHON_FILES) \
		$(DOCS_FILES) \
		CHANGELOG.md \
		.conform.yaml \
		CONTRIBUTING.md
	@$(RUN) $(MAKE) -C docs html

$(VENV): $(UV_BOOTSTRAP) uv.lock
	@$(UV) sync --all-groups
	@touch $@

.make/pre-commit: $(VENV)
	@$(RUN) pre-commit install \
		--hook-type pre-commit \
		--hook-type pre-merge-commit \
		--hook-type pre-push \
		--hook-type prepare-commit-msg \
		--hook-type commit-msg \
		--hook-type post-commit \
		--hook-type post-checkout \
		--hook-type post-merge \
		--hook-type post-rewrite
	@mkdir -p $(@D)
	@touch $@

$(GIT_DIR)/blame-ignore-revs:
	@git config --local include.path $(@F) 2>/dev/null || true
	@mkdir -p $(@D)
	@printf '%s\n' '[blame]' 'ignoreRevsFile = .git-blame-ignore-revs' > $@

bin/uv/uv: .uv-version
	@curl -sSL https://astral.sh/uv/$(UV_VERSION)/install.sh | \
		UV_UNMANAGED_INSTALL="$$(pwd)/bin/uv" sh >/dev/null
	@touch $@

README.rst: $(VENV) $(PACKAGE_FILES)
	@$(RUN) python scripts/update_readme.py >/dev/null 2>&1 || exit 0
	@touch $@

.make/update-docs: $(VENV) $(PACKAGE_FILES)
	@$(RUN) python scripts/update_docs.py
	@mkdir -p $(@D)
	@touch $@

.make/black: $(VENV) $(PYTHON_FILES)
	@$(RUN) black $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/flynt: $(VENV) $(PYTHON_FILES)
	@$(RUN) flynt $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/isort: $(VENV) $(PYTHON_FILES)
	@$(RUN) isort $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/pylint: $(VENV) $(PYTHON_FILES)
	@$(RUN) pylint --output-format=colorized $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/docsig: $(VENV) $(PYTHON_FILES)
	@$(RUN) docsig $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.mypy_cache/CACHEDIR.TAG: $(VENV) $(PYTHON_FILES)
	@$(RUN) mypy $(PYTHON_FILES)
	@touch $@

whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(RUN) vulture > $@ || exit 0

coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(RUN) pytest -n=auto --cov=docsig --cov=tests \
		&& $(RUN) coverage xml

.make/doctest: $(VENV) README.rst $(PYTHON_FILES) $(DOCS_FILES)
	@$(RUN) pytest docs README.rst --doctest-glob='*.rst'
	@mkdir -p $(@D)
	@touch $@

docs/_build/linkcheck/output.json: $(VENV) \
		$(PYTHON_FILES) \
		$(DOCS_FILES) \
		CHANGELOG.md \
		.conform.yaml \
		CONTRIBUTING.md
	@trap "rm -f $(@); exit 1" ERR; \
		{ \
			curl -fsI --max-time 5 https://docsig.io >/dev/null 2>&1 \
			|| { echo "could not establish connection, skipping"; exit 0; }; \
			$(RUN) $(MAKE) -C docs linkcheck; \
		}

.make/check-deps: $(VENV) $(PYTHON_FILES) pyproject.toml
	@$(RUN) deptry .
	@mkdir -p $(@D)
	@touch $@

.make/test-check-ai-commit: $(VENV) scripts/check_ai_commit.py
	@$(RUN) pytest scripts/check_ai_commit.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-check-claude-md: $(VENV) scripts/check_claude_md.py
	@$(RUN) pytest scripts/check_claude_md.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-check-coverage: $(VENV) scripts/check_coverage.py
	@$(RUN) pytest scripts/check_coverage.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-commit-fix: $(VENV) scripts/commit_fix.py
	@$(RUN) pytest scripts/commit_fix.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-make-help: $(VENV) scripts/make_help.py
	@$(RUN) pytest scripts/make_help.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-update-copyright: $(VENV) scripts/update_copyright.py
	@$(RUN) pytest scripts/update_copyright.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-update-readme: $(VENV) scripts/update_readme.py
	@$(RUN) pytest scripts/update_readme.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-update-docs: $(VENV) scripts/update_docs.py
	@$(RUN) pytest scripts/update_docs.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-promote-wip: $(VENV) scripts/promote_wip.py
	@$(RUN) pytest scripts/promote_wip.py -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-check-news: $(VENV) scripts/check_news.py
	@$(RUN) pytest scripts/check_news.py --cov -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-bump: $(VENV) scripts/bump_version.py
	@$(RUN) pytest scripts/bump_version.py -n=auto
	@mkdir -p $(@D)
	@touch $@

uv.lock: $(UV_BOOTSTRAP) pyproject.toml
	@$(UV) lock
	@touch $@

# --no-hashes as pip enforces hashes for every transitive dependency once
# any are present, which --target installs cannot satisfy
build/requirements.txt: $(VENV)
	@mkdir -p $(@D)
	@$(UV) export --format requirements-txt --no-hashes \
		--no-emit-project --no-dev --output-file $@
	@touch $@

build/site-packages/$(VERSION): build/requirements.txt
	@rm -rf $(@D) >/dev/null
	@$(UV) pip install -r $< --target $(@D)
	@$(UV) pip install . --no-deps --target $(@D)
	@touch $@

build/docsig.pyz: build/site-packages/$(VERSION)
	@$(RUN) shiv \
		--site-packages $(<D) \
		--entry-point docsig.__main__:main \
		--output-file $@
	@touch $@

########################################################################
# Phony Targets
.PHONY: benchmark build bump check-ai-commit check-deps check-links clean \
	docs format install-hooks install-ignore-revs install-uv \
	install-venv lint lock-deps publish test-scripts test-source tests \
	tox types update-copyright update-deps update-docs update-readme \
	whitelist news commit-fix version neovim

#: show program's version number and exit
version:
	@echo $(VERSION)

#: run benchmarks
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(RUN) pytest -m=benchmark --benchmark-save=benchmark

#: build distribution
build: $(BUILD)

bump: part = patch
#: bump version (use: make bump part=major|minor|patch)
bump: .make/pre-commit
	@$(RUN) python scripts/bump_version.py $(part)

#: check dependencies are properly managed
check-deps: .make/check-deps

#: confirm links in documentation are valid
check-links: docs/_build/linkcheck/output.json

#: clean compiled files
clean:
	@find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.benchmarks' -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage
	@rm -rf $(GIT_DIR)/blame-ignore-revs
	@rm -rf $(GIT_DIR)/hooks/*
	@rm -rf .make
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .venv
	@rm -rf bin
	@rm -rf coverage.xml
	@rm -rf dist
	@rm -rf docs/_build
	@rm -rf docs/_generated
	@rm -rf .tox
	@rm -rf node_modules
	@rm -rf build
	@$(MAKE) -C plugin/intellij clean
	@$(MAKE) -C plugin/vscode clean

#: build documentation
docs: docs/_build/html/index.html

#: run formatters
format: .make/black .make/flynt .make/isort

#: install pre-commit hooks
install-hooks: .make/pre-commit

#: install .git-blame-ignore-revs
install-ignore-revs: $(GIT_DIR)/blame-ignore-revs

#: install uv
install-uv: $(UV_BOOTSTRAP)

#: install virtualenv
install-venv: $(VENV)

#: lint code
lint: .make/pylint .make/docsig

#: lock uv dependencies
lock-deps: uv.lock

#: publish distribution
publish: $(BUILD) check-links
	@# twine rather than `uv publish`, which is token-only and cannot read
	@# the PyPI token from the keyring
	@$(RUN) twine upload dist/docsig-$(VERSION)*

#: run tests on scripts
test-scripts: \
	.make/test-check-news \
	.make/test-bump \
	.make/test-check-ai-commit \
	.make/test-check-claude-md \
	.make/test-check-coverage \
	.make/test-commit-fix \
	.make/test-make-help \
	.make/test-update-copyright \
	.make/test-update-readme \
	.make/test-update-docs \
	.make/test-promote-wip

#: run tests on source code
test-source: .make/doctest coverage.xml

#: run all tests
tests: test-scripts test-source

#: run tox
tox: $(VENV)
	@$(RUN) tox

#: check typing
types: .mypy_cache/CACHEDIR.TAG

#: update copyright year in files containing it
update-copyright: $(VENV)
	@$(RUN) python3 scripts/update_copyright.py

#: update dependencies
update-deps: $(VENV)
	@$(UV) sync --all-groups --upgrade

#: update docs according to source
update-docs: .make/update-docs

#: update commandline documentation if needed
update-readme: README.rst

#: generate whitelist of allowed unused code
whitelist: whitelist.py

#: make news fragment
news: $(VENV)
	@$(RUN) python scripts/check_news.py $(MSG)

#: check test written for fix
commit-fix: $(VENV)
	@$(RUN) python scripts/commit_fix.py $(MSG)

#: check ai housekeeping commit explains itself
check-ai-commit: $(VENV)
	@$(RUN) python scripts/check_ai_commit.py $(MSG)

#: bundle neovim plugin
neovim:
	@$(MAKE) -C plugin/neovim bundle

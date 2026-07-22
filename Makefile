########################################################################
# Make Configuration
SHELL := /bin/bash
.DELETE_ON_ERROR:

# Extract version from pyproject.toml
# Use this instead of `$ poetry version --short` as the version may be
# needed before poetry is installed
VERSION := $(shell bash scripts/get_docsig_version.sh pyproject.toml)

# Poetry configuration
export POETRY_KEYRING_ENABLED := false
POETRY := bin/poetry/bin/poetry
POETRY_VERSION := $(shell cat .poetry-version)

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
	@$(POETRY) run python scripts/make_help.py

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
		.make/update-readme \
		coverage.xml \
		docs/_build/html/index.html
	@$(POETRY) build
	@touch $@

docs/_build/html/index.html: $(VENV) \
		$(PYTHON_FILES) \
		$(DOCS_FILES) \
		CHANGELOG.md \
		.conform.yaml \
		CONTRIBUTING.md
	@$(POETRY) run $(MAKE) -C docs html

$(VENV): poetry.lock
	@[ ! $$(basename "$$($(POETRY) env info --path)") = ".venv" ] \
		&& rm -rf "$$($(POETRY) env info --path)" \
		|| exit 0
	@POETRY_VIRTUALENVS_IN_PROJECT=1 $(POETRY) install
	@touch $@

.make/pre-commit: $(VENV)
	@$(POETRY) run pre-commit install \
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

$(POETRY): .poetry-version
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" - \
		--version $(POETRY_VERSION)
	@touch $@

.make/update-readme: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_readme.py
	@mkdir -p $(@D)
	@touch $@

.make/update-docs: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_docs.py
	@mkdir -p $(@D)
	@touch $@

.make/black: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run black $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/flynt: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run flynt $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/isort: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run isort $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/pylint: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/docsig: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run docsig $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.mypy_cache/CACHEDIR.TAG: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run mypy $(PYTHON_FILES)
	@touch $@

whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture > $@ || exit 0

coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

.make/doctest: $(VENV) .make/update-readme $(PYTHON_FILES) $(DOCS_FILES)
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'
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
			$(POETRY) run $(MAKE) -C docs linkcheck; \
		}

.make/check-deps: $(VENV) $(PYTHON_FILES) pyproject.toml
	@$(POETRY) run deptry .
	@mkdir -p $(@D)
	@touch $@

.make/test-check-news: $(VENV) scripts/check_news.py
	@$(POETRY) run pytest scripts/check_news.py --cov -n=auto
	@mkdir -p $(@D)
	@touch $@

.make/test-bump: $(VENV) scripts/bump_version.py
	@$(POETRY) run pytest scripts/bump_version.py -n=auto
	@mkdir -p $(@D)
	@touch $@

poetry.lock: $(POETRY) pyproject.toml
	@$< lock
	@touch $@

build/requirements.txt: $(VENV)
	@mkdir -p $(@D)
	@$(POETRY) export -f requirements.txt --output $@
	@touch $@

build/site-packages/$(VERSION): build/requirements.txt
	@rm -rf $(@D) >/dev/null
	@$(POETRY) run pip install -r $< --target $(@D)
	@$(POETRY) run pip install . --no-deps --target $(@D)
	@touch $@

build/docsig.pyz: build/site-packages/$(VERSION)
	@$(POETRY) run shiv \
		--site-packages $(<D) \
		--entry-point docsig.__main__:main \
		--output-file $@
	@touch $@

########################################################################
# Phony Targets
.PHONY: benchmark build bump check-deps check-links clean docs format \
	install-hooks install-ignore-revs install-poetry install-venv lint \
	lock-deps publish test-scripts test-source tests tox types \
	update-copyright update-deps update-docs update-readme whitelist \
	news commit-fix version neovim

#: show program's version number and exit
version:
	@echo $(VERSION)

#: run benchmarks
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

#: build distribution
build: $(BUILD)

bump: part = patch
#: bump version (use: make bump part=major|minor|patch)
bump: .make/pre-commit
	@$(POETRY) run python scripts/bump_version.py $(part)

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
	@rm -rf .poetry
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

#: install poetry
install-poetry: $(POETRY)

#: install virtualenv
install-venv: $(VENV)

#: lint code
lint: .make/pylint .make/docsig

#: lock poetry dependencies
lock-deps: poetry.lock

#: publish distribution
publish: $(BUILD) check-links
	@# Keyring is disabled globally to avoid hangs; publish needs it for PyPI token
	@POETRY_KEYRING_ENABLED=true $(POETRY) publish

#: run tests on scripts
test-scripts: .make/test-check-news .make/test-bump

#: run tests on source code
test-source: .make/doctest coverage.xml

#: run all tests
tests: test-scripts test-source

#: run tox
tox: $(VENV)
	@$(POETRY) run tox

#: check typing
types: .mypy_cache/CACHEDIR.TAG

#: update copyright year in files containing it
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

#: update dependencies
update-deps: $(VENV)
	@$(POETRY) update

#: update docs according to source
update-docs: .make/update-docs

#: update commandline documentation if needed
update-readme: .make/update-readme

#: generate whitelist of allowed unused code
whitelist: whitelist.py

#: make news fragment
news: $(VENV)
	@$(POETRY) run python scripts/check_news.py $(MSG)

#: check test written for fix
commit-fix: $(VENV)
	@$(POETRY) run python scripts/commit_fix.py $(MSG)

#: bundle neovim plugin
neovim:
	@$(MAKE) -C plugin/neovim bundle

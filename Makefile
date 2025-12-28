########################################################################
# Make Configuration
SHELL := /bin/bash
.DELETE_ON_ERROR:

# Extract version from pyproject.toml
VERSION := $(shell bash scripts/get_docsig_version.sh)

# Poetry configuration
POETRY := bin/poetry/bin/poetry
POETRY_VERSION := $(shell cat .poetry-version)

# File lists
PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')
PACKAGE_FILES := $(shell git ls-files "docsig/*.py")
TEST_FILES := $(shell git ls-files "tests/*.py")
DOCS_FILES := $(shell git ls-files "docs/*.rst" "docs/*.md")

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
all: .make/pre-commit .git/blame-ignore-revs help

.PHONY: help
help: $(VENV)
	@$(POETRY) run python scripts/make_help.py

########################################################################
# Main Targets
$(BUILD): .make/doctest \
	format \
	lint \
	unused \
	.make/update-docs \
	.mypy_cache/CACHEDIR.TAG \
	README.rst \
	coverage.xml \
	docs/_build/html/index.html \
	docs/_build/linkcheck/output.json
	@$(POETRY) build
	@touch $@

docs/_build/html/index.html: $(VENV) \
	$(PYTHON_FILES) \
	$(DOCS_FILES) \
	CHANGELOG.md \
	.conform.yaml \
	CONTRIBUTING.md
	@$(POETRY) run $(MAKE) -C docs html

$(VENV): $(POETRY) poetry.lock
	@[ ! $$(basename "$$($< env info --path)") = ".venv" ] \
		&& rm -rf "$$($< env info --path)" \
		|| exit 0
	@POETRY_VIRTUALENVS_IN_PROJECT=1 $< install
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

.git/blame-ignore-revs:
	@git config --local include.path $(@F) 2>/dev/null || true
	@mkdir -p $(@D)
	@printf '%s\n' '[blame]' 'ignoreRevsFile = .git-blame-ignore-revs' > $@

$(POETRY): .poetry-version
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" - \
		--version $(POETRY_VERSION)
	@touch $@

README.rst: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_readme.py >/dev/null 2>&1 || exit 0
	@touch $@

#: update docs according to source
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

.make/unused: whitelist.py
	@$(POETRY) run vulture whitelist.py docsig tests
	@mkdir -p $(@D)
	@touch $@

whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture --make-whitelist docsig tests > $@ || exit 0

coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

.make/doctest: $(VENV) README.rst $(PYTHON_FILES) $(DOCS_FILES)
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
			ping -c 1 docsig.io >/dev/null 2>&1 \
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

poetry.lock: pyproject.toml
	@$(POETRY) lock
	@touch $@

########################################################################
# Phony Targets
.PHONY: benchmark
#: run benchmarks
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

.PHONY: build
#: build distribution
build: $(BUILD)

.PHONY: bump
bump: part = patch
#: bump version (use: make bump part=major|minor|patch)
bump: .make/pre-commit
	@$(POETRY) run python scripts/bump_version.py $(part)

.PHONY: check-deps
#: check dependencies are properly managed
check-deps: .make/check-deps

.PHONY: check-links
#: confirm links in documentation are valid
check-links: docs/_build/linkcheck/output.json

.PHONY: clean
#: clean compiled files
clean:
	@find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage
	@rm -rf .git/blame-ignore-revs
	@rm -rf .git/hooks/*
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

.PHONY: docs
#: build documentation
docs: docs/_build/html/index.html

.PHONY: format
#: run formatters
format: .make/black .make/flynt .make/isort

.PHONY: install-hooks
#: install pre-commit hooks
install-hooks: .make/pre-commit

.PHONY: install-ignore-revs
#: install .git-blame-ignore-revs
install-ignore-revs: .git/blame-ignore-revs

.PHONY: install-poetry
#: install poetry
install-poetry: $(POETRY)

.PHONY: install-venv
#: install virtualenv
install-venv: $(VENV)

.PHONY: lint
#: lint code
lint: .make/pylint .make/docsig

.PHONY: lock-deps
#: lock poetry dependencies
lock-deps: poetry.lock

.PHONY: publish
#: publish distribution
publish: $(BUILD)
	@$(POETRY) publish

.PHONY: test
#: run tests
test: .make/doctest coverage.xml

.PHONY: tox
#: run tox
tox: $(VENV)
	@$(POETRY) run tox

.PHONY: types
#: check typing
types: .mypy_cache/CACHEDIR.TAG

.PHONY: unused
#: check for unused code
unused: .make/unused

.PHONY: update-copyright
#: update copyright year in files containing it
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

.PHONY: update-deps
#: update dependencies
update-deps: $(VENV)
	@$(POETRY) update

.PHONY: update-readme
#: update commandline documentation if needed
update-readme: README.rst

.PHONY: whitelist
#: generate whitelist of allowed unused code
whitelist: whitelist.py

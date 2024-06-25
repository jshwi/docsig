VERSION := 0.56.0

POETRY := bin/poetry/bin/poetry

PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')
PACKAGE_FILES := $(shell git ls-files "docsig/*.py")
TEST_FILES := $(shell git ls-files "tests/*.py")
DOCS_FILES := $(shell git ls-files "docs/*.rst" "docs/*.md")

ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/activate
endif

BUILD := dist/docsig-$(VERSION)-py3-none-any.whl

.PHONY: all
#: install development environment
all: .make/pre-commit .git/blame-ignore-revs

.PHONY: build
#: build distribution
build: $(BUILD)

#: build and check integrity of distribution
$(BUILD): .make/doctest \
	.make/format \
	.make/lint \
	.make/unused \
	.make/update-docs \
	.mypy_cache/CACHEDIR.TAG \
	README.rst \
	coverage.xml \
	docs/_build/html/index.html \
	docs/_build/linkcheck/output.json
	@$(POETRY) build
	@touch $@

.PHONY: test
#: test source
test: .make/doctest coverage.xml

.PHONY: publish
#: publish distribution
publish: $(BUILD)
	@$(POETRY) publish

#: generate documentation
docs/_build/html/index.html: $(VENV) \
	$(PYTHON_FILES) \
	$(DOCS_FILES) \
	CHANGELOG.md \
	.conform.yaml \
	CONTRIBUTING.md
	@$(POETRY) run $(MAKE) -C docs html

.PHONY: clean
#: clean compiled files
clean:
	@find . -name '__pycache__' -exec rm -rf {} +
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

#: generate virtual environment
$(VENV): $(POETRY) poetry.lock
	@[ ! $$(basename "$$($< env info --path)") = ".venv" ] \
		&& rm -rf "$$($< env info --path)" \
		|| exit 0
	@POETRY_VIRTUALENVS_IN_PROJECT=1 $< install
	@touch $@

#: install pre-commit hooks
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

#: install .git-blane-ignore-revs
.git/blame-ignore-revs:
	@git config --local include.path $(@F)
	@printf '%s\n' '[blame]' 'ignoreRevsFile = .git-blame-ignore-revs' > $@

#: install poetry
$(POETRY):
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" -
	@touch $@

#: update commandline documentation if needed
README.rst: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_readme.py >/dev/null 2>&1 || exit 0
	@touch $@

#: update docs according to source
.make/update-docs: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_docs.py
	@mkdir -p $(@D)
	@touch $@

.PHONY: update-copyright
#: update copyright year in files containing it
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

#: run checks that format code
.make/format: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run black $(PYTHON_FILES)
	@$(POETRY) run docformatter $(PYTHON_FILES)
	@$(POETRY) run flynt $(PYTHON_FILES)
	@$(POETRY) run isort $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

#: lint code
.make/lint: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)
	@$(POETRY) run docsig $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

#: check typing
.mypy_cache/CACHEDIR.TAG: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run mypy $(PYTHON_FILES)
	@touch $@

#: check for unused code
.make/unused: whitelist.py
	@$(POETRY) run vulture whitelist.py docsig tests
	@mkdir -p $(@D)
	@touch $@

#: generate whitelist of allowed unused code
whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture --make-whitelist docsig tests > $@ || exit 0

#: generate coverage report
coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

#: test code examples in documentation
.make/doctest: $(VENV) README.rst $(PYTHON_FILES) $(DOCS_FILES)
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'
	@mkdir -p $(@D)
	@touch $@

.PHONY: benchmark
#: run benchmarks
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

#: confirm links in documentation are valid
docs/_build/linkcheck/output.json: $(VENV) \
	$(PYTHON_FILES) \
	$(DOCS_FILES) \
	CHANGELOG.md \
	.conform.yaml \
	CONTRIBUTING.md
	@trap "rm -f $(@); exit 1" ERR; \
		{ \
			ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
			|| { echo "could not establish connection, skipping"; exit 0; }; \
			$(POETRY) run $(MAKE) -C docs linkcheck; \
		}

#: check dependencies are properly managed
.make/check-deps: $(VENV) $(PYTHON_FILES) pyproject.toml
	@$(POETRY) run deptry .
	@mkdir -p $(@D)
	@touch $@

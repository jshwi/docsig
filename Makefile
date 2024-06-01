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

.PHONY: all
all: .make/pre-commit .git/blame-ignore-revs

.PHONY: build
build: .make/doctest \
	.make/format \
	.make/lint \
	.mypy_cache/CACHEDIR.TAG \
	coverage.xml \
	unused

.PHONY: test
test: .make/doctest coverage.xml

docs/_build/html/index.html: $(VENV) $(PYTHON_FILES) $(DOCS_FILES)
	@$(POETRY) run $(MAKE) -C docs html

.PHONY: clean
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
	@rm -rf docs/_build
	@rm -rf docs/_generated

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
	@git config --local include.path $(@F)
	@printf '%s\n' '[blame]' 'ignoreRevsFile = .git-blame-ignore-revs' > $@

$(POETRY):
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" -
	@touch $@

README.rst: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python scripts/update_readme.py >/dev/null 2>&1 || exit 0
	@touch $@

.make/update-docs: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python3 scripts/update_docs.py
	@mkdir -p $(@D)
	@touch $@

.PHONY: update-copyright
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

.make/format: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run black $(PYTHON_FILES)
	@$(POETRY) run docformatter $(PYTHON_FILES)
	@$(POETRY) run flynt $(PYTHON_FILES)
	@$(POETRY) run isort $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/lint: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)
	@$(POETRY) run docsig $(PYTHON_FILES)
	@mkdir -p $(@D)
	@touch $@

.mypy_cache/CACHEDIR.TAG: $(VENV) $(PYTHON_FILES)
	@$(POETRY) run mypy $(PYTHON_FILES)
	@touch $@

.PHONY: unused
unused: whitelist.py
	@$(POETRY) run vulture whitelist.py docsig tests

whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture --make-whitelist docsig tests > $@ || exit 0

coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

.make/doctest: $(VENV) README.rst $(PYTHON_FILES) $(DOCS_FILES)
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'
	@mkdir -p $(@D)
	@touch $@

.PHONY: benchmark
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

docs/_build/linkcheck/output.json: $(VENV) $(PYTHON_FILES) $(DOCS_FILES)
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& $(POETRY) run $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

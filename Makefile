POETRY := bin/poetry/bin/poetry

PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')
PACKAGE_FILES := $(shell git ls-files "docsig/*.py")
TEST_FILES := $(shell git ls-files "tests/*.py")

ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/activate
endif

.PHONY: all
all: .make/pre-commit .git/blame-ignore-revs

.PHONY: build
build: format \
	format-docs \
	format-str \
	imports \
	lint \
	test \
	typecheck \
	unused

.PHONY: test
test: doctest coverage.xml

.PHONY: docs
docs: $(VENV)
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

.PHONY: update-readme
update-readme: $(VENV)
	@$(POETRY) run python3 scripts/update_readme.py

.make/update-docs: $(VENV) $(PACKAGE_FILES)
	@$(POETRY) run python3 scripts/update_docs.py
	@mkdir -p $(@D)
	@touch $@

.PHONY: update-copyright
update-copyright: $(VENV)
	@$(POETRY) run python3 scripts/update_copyright.py

.PHONY: format
format: $(VENV)
	@$(POETRY) run black $(PYTHON_FILES)

.PHONY: format-docs
format-docs: $(VENV)
	@$(POETRY) run docformatter $(PYTHON_FILES)

.PHONY: format-str
format-str: $(VENV)
	@$(POETRY) run flynt $(PYTHON_FILES)

.PHONY: imports
imports: $(VENV)
	@$(POETRY) run isort $(PYTHON_FILES)

.PHONY: lint
lint: $(VENV)
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)

.PHONY: typecheck
typecheck: $(VENV)
	@$(POETRY) run mypy .

.PHONY: unused
unused: whitelist.py
	@$(POETRY) run vulture whitelist.py docsig tests

whitelist.py: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run vulture --make-whitelist docsig tests > $@ || exit 0

coverage.xml: $(VENV) $(PACKAGE_FILES) $(TEST_FILES)
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

.PHONY: params
params: $(VENV)
	@$(POETRY) run docsig $(PYTHON_FILES)

.PHONY: doctest
doctest: $(VENV)
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'

.PHONY: benchmark
benchmark: $(VENV)
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

.PHONY: check-links
check-links: $(VENV)
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& $(POETRY) run $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

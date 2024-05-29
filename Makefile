POETRY := bin/poetry/bin/poetry

PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')

ifeq ($(OS),Windows_NT)
	VENV := .venv/Scripts/activate
else
	VENV := .venv/bin/active
endif

.PHONY: all
all: .make/pre-commit install-ignore-blame-revs

.PHONY: build
build: format \
	format-docs \
	format-str \
	imports \
	lint \
	test \
	typecheck \
	unused \
	whitelist

.PHONY: test
test: doctest coverage

.PHONY: docs
docs: $(VENV)
	@$(POETRY) run $(MAKE) -C docs html

.PHONY: clean
clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@rm -rf .git/hooks/*
	@rm -rf .make
	@rm -rf .venv
	@rm -rf bin

$(VENV): $(POETRY) pyproject.toml poetry.lock
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

.PHONY: install-ignore-blame-revs
install-ignore-blame-revs:
	@git config --local blame.ignoreRevsFile .git-blame-ignore-revs
	@echo "installed .git-blame-ignore-revs"

$(POETRY):
	@curl -sSL https://install.python-poetry.org | \
		POETRY_HOME="$$(pwd)/bin/poetry" "$$(which python)" -
	@touch $@

.PHONY: remove-ignore-blame-revs
remove-ignore-blame-revs:
	@git config --local --unset blame.ignoreRevsFile \
		&& echo "removed .git-blame-ignore-revs" \
		|| exit 0

.PHONY: update-readme
update-readme: $(VENV)
	@$(POETRY) run python3 scripts/update_readme.py

.PHONY: update-docs
update-docs: $(VENV)
	@$(POETRY) run python3 scripts/update_docs.py

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
unused:
	@$(POETRY) run vulture whitelist.py $(PYTHON_FILES)

.PHONY: whitelist
whitelist: $(VENV)
	@$(POETRY) run vulture --make-whitelist  $(PYTHON_FILES) > whitelist.py || exit 0

.PHONY: coverage
coverage: $(VENV)
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

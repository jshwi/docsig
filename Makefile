POETRY := poetry

PYTHON_FILES := $(shell git ls-files "*.py" ':!:whitelist.py')

.PHONY: all
all: install-poetry install-deps install-hooks install-ignore-blame-revs

.PHONY: remove
remove: remove-poetry remove-hooks remove-deps

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
docs: install-deps
	@$(POETRY) run $(MAKE) -C docs html

.PHONY: clean
clean:
	@find . -name '__pycache__' -exec rm -rf {} +

.PHONY: install-poetry
install-poetry:
	@command -v $(POETRY) >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install-deps
install-deps:
	@POETRY_VIRTUALENVS_IN_PROJECT=1 $(POETRY) install

.PHONY: install-pre-commit
install-pre-commit: install-deps
	@$(POETRY) run command -v pre-commit > /dev/null 2>&1 \
		|| $(POETRY) run pip --quiet install pre-commit

.PHONY: install-hooks
install-hooks: install-pre-commit
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

.PHONY: install-ignore-blame-revs
install-ignore-blame-revs:
	@git config --local blame.ignoreRevsFile .git-blame-ignore-revs
	@echo "installed .git-blame-ignore-revs"

.PHONY: remove-hooks
remove-hooks: install-pre-commit
	@$(POETRY) run pre-commit uninstall \
		--hook-type pre-commit \
		--hook-type pre-merge-commit \
		--hook-type pre-push \
		--hook-type prepare-commit-msg \
		--hook-type commit-msg \
		--hook-type post-commit \
		--hook-type post-checkout \
		--hook-type post-merge \
		--hook-type post-rewrite

.PHONY: remove-deps
remove-deps: install-deps
	rm -rf \
		$(shell dirname $(shell dirname $(shell $(POETRY) run which python)))

.PHONY: remove-poetry
remove-poetry:
	@command -v $(POETRY) >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 - --uninstall

.PHONY: remove-ignore-blame-revs
remove-ignore-blame-revs:
	@git config --local --unset blame.ignoreRevsFile \
		&& echo "removed .git-blame-ignore-revs" \
		|| exit 0

.PHONY: update-readme
update-readme: install-deps
	@$(POETRY) run python3 scripts/update_readme.py

.PHONY: update-docs
update-docs: install-deps
	@$(POETRY) run python3 scripts/update_docs.py

.PHONY: update-copyright
update-copyright: install-deps
	@$(POETRY) run python3 scripts/update_copyright.py

.PHONY: format
format: install-deps
	@$(POETRY) run black $(PYTHON_FILES)

.PHONY: format-docs
format-docs: install-deps
	@$(POETRY) run docformatter $(PYTHON_FILES)

.PHONY: format-str
format-str: install-deps
	@$(POETRY) run flynt $(PYTHON_FILES)

.PHONY: imports
imports: install-deps
	@$(POETRY) run isort $(PYTHON_FILES)

.PHONY: lint
lint: install-deps
	@$(POETRY) run pylint --output-format=colorized $(PYTHON_FILES)

.PHONY: typecheck
typecheck: install-deps
	@$(POETRY) run mypy .

.PHONY: unused
unused:
	@$(POETRY) run vulture whitelist.py $(PYTHON_FILES)

.PHONY: whitelist
whitelist: install-deps
	@$(POETRY) run vulture --make-whitelist  $(PYTHON_FILES) > whitelist.py || exit 0

.PHONY: coverage
coverage: install-deps
	@$(POETRY) run pytest -n=auto --cov=docsig --cov=tests \
		&& $(POETRY) run coverage xml

.PHONY: params
params: install-deps
	@$(POETRY) run docsig $(PYTHON_FILES)

.PHONY: doctest
doctest: install-deps
	@$(POETRY) run pytest docs README.rst --doctest-glob='*.rst'

.PHONY: benchmark
benchmark: install-deps
	@RUN_BENCHMARK=true $(POETRY) run pytest -m=benchmark --benchmark-save=benchmark

.PHONY: check-links
check-links: install-deps
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& $(POETRY) run $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

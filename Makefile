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

.PHONY: doctest
doctest: doctest-docs

.PHONY: docs
docs:
	@$(MAKE) -C docs html

.PHONY: clean
clean:
	@find . -name '__pycache__' -exec rm -rf {} +

.PHONY: install-poetry
install-poetry:
	@command -v poetry >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install-deps
install-deps:
	@POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install

.PHONY: install-pre-commit
install-pre-commit:
	@poetry run command -v pre-commit > /dev/null 2>&1 \
		|| poetry run pip --quiet install pre-commit

.PHONY: install-hooks
install-hooks: install-pre-commit
	@pre-commit install \
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
	@pre-commit uninstall \
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
remove-deps:
	rm -rf $(shell dirname $(shell dirname $(shell poetry run which python)))

.PHONY: remove-poetry
remove-poetry:
	@command -v poetry >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 - --uninstall

.PHONY: remove-ignore-blame-revs
remove-ignore-blame-revs:
	@git config --local --unset blame.ignoreRevsFile \
		&& echo "removed .git-blame-ignore-revs" \
		|| exit 0

.PHONY: update-readme
update-readme:
	@python3 scripts/update_readme.py

.PHONY: update-docs
update-docs:
	@python3 scripts/update_docs.py

.PHONY: update-copyright
update-copyright:
	@python3 scripts/update_copyright.py

.PHONY: format
format:
	@black $(PYTHON_FILES)

.PHONY: format-docs
format-docs:
	@docformatter $(PYTHON_FILES)

.PHONY: format-str
format-str:
	@flynt $(PYTHON_FILES)

.PHONY: imports
imports:
	@isort $(PYTHON_FILES)

.PHONY: lint
lint:
	@pylint --output-format=colorized $(PYTHON_FILES)

.PHONY: typecheck
typecheck:
	@mypy .

.PHONY: unused
unused:
	@vulture whitelist.py $(PYTHON_FILES)

.PHONY: whitelist
whitelist:
	@vulture --make-whitelist  $(PYTHON_FILES) > whitelist.py || exit 0

.PHONY: coverage
coverage:
	@pytest -n=auto --cov=docsig --cov=tests && coverage xml

.PHONY: params
params:
	@docsig $(PYTHON_FILES)

.PHONY: doctest-docs
doctest-docs:
	@pytest docs README.rst --doctest-glob='*.rst'

.PHONY: benchmark
benchmark:
	@RUN_BENCHMARK=true pytest -m=benchmark --benchmark-save=benchmark

.PHONY: check-links
check-links:
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

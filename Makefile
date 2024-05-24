PYTHON_FILES := $(shell git ls-files "*.py")

.PHONY: all
all: install

.PHONY: install
install: install-poetry install-deps install-hooks install-ignore-blame-revs

.PHONY: remove
remove: remove-poetry remove-hooks remove-deps

.PHONY: audit
audit: update-copyright \
	format \
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
doctest: doctest-package doctest-readme doctest-docs

.PHONY: docs
docs:
	@poetry run $(MAKE) -C docs html

.PHONY: clean
clean:
	@git clean docs -fdx

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
	@poetry run pre-commit install \
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
	@poetry run python3 scripts/update_readme.py

.PHONY: update-docs
update-docs:
	@poetry run python3 scripts/update_docs.py

.PHONY: update-copyright
update-copyright:
	@poetry run python3 scripts/update_copyright.py

.PHONY: format
format:
	@poetry run black $(PYTHON_FILES)

.PHONY: format-docs
format-docs:
	@poetry run docformatter $(PYTHON_FILES)

.PHONY: format-str
format-str:
	@poetry run flynt $(PYTHON_FILES)

.PHONY: imports
imports:
	@poetry run isort $(PYTHON_FILES)

.PHONY: lint
lint:
	@poetry run pylint --output-format=colorized $(PYTHON_FILES)

.PHONY: typecheck
typecheck:
	@poetry run mypy .

.PHONY: unused
unused:
	@poetry run vulture whitelist.py $(PYTHON_FILES)

.PHONY: whitelist
whitelist:
	@poetry run vulture --make-whitelist  $(PYTHON_FILES) > whitelist.py \
		|| exit 0

.PHONY: coverage
coverage:
	@poetry run pytest -n=auto --cov=docsig --cov=tests \
		&& poetry run coverage xml

.PHONY: doctest-package
doctest-package:
	@poetry run $(MAKE) -C docs doctest

.PHONY: doctest-package
doctest-readme:
	@poetry run python -m doctest README.rst

.PHONY: params
params:
	@poetry run docsig $(PYTHON_FILES)

.PHONY: doctest-docs
doctest-docs:
	@poetry run pytest docs --doctest-glob='*.rst'

.PHONY: benchmark
benchmark:
	@RUN_BENCHMARK=true \
		poetry run pytest \
		-m="benchmark" \
		--benchmark-save=benchmark

.PHONY: check-links
check-links:
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& poetry run $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

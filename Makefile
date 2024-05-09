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
doctest: doctest-package doctest-readme

.PHONY: docs
docs:
	@$(MAKE) -C docs html

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
	@pyaud format -fn

.PHONY: format-docs
format-docs:
	@pyaud format-docs -fn

.PHONY: format-str
format-str:
	@pyaud format-str -fn

.PHONY: imports
imports:
	@pyaud imports -fn

.PHONY: lint
lint:
	@pyaud lint -n

.PHONY: typecheck
typecheck:
	@mypy .

.PHONY: unused
unused:
	@pyaud unused -n

.PHONY: whitelist
whitelist:
	@pyaud whitelist -fn

.PHONY: coverage
coverage:
	@pyaud coverage -n

.PHONY: doctest-package
doctest-package:
	@pyaud doctest-package

.PHONY: doctest-package
doctest-readme:
	@pyaud doctest-readme

.PHONY: params
params:
	@docsig $(PYTHON_FILES)

.PHONY: doctest-docs
doctest-docs:
	@pytest docs --doctest-glob='*.rst'

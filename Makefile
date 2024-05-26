PYTHON_FILES := $(shell git ls-files "*.py")
RUN = poetry run

.PHONY: all
all: install

.PHONY: install
install: install-poetry install-deps install-hooks install-ignore-blame-revs

.PHONY: remove
remove: remove-poetry remove-deps remove-hooks remove-ignore-blame-revs

.PHONY: audit
audit: format \
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
docs:
	@$(RUN) $(MAKE) -C docs html

.PHONY: clean
clean:
	@rm -rf **/*.pyc \
		**/__pycache__ \
		.coverage \
		.mypy_cache \
		.pytest_cache \
		coverage.xml \
		dist \
		docs/_build \
		docs/_generated \
		node_modules

.PHONY: install-poetry
install-poetry:
	@command -v poetry >/dev/null 2>&1 \
		|| curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install-deps
install-deps:
	@POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install

.PHONY: install-pre-commit
install-pre-commit:
	@$(RUN) command -v pre-commit > /dev/null 2>&1 \
		|| $(RUN) pip --quiet install pre-commit

.PHONY: install-hooks
install-hooks: install-pre-commit
	@$(RUN) pre-commit install \
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
	rm -rf $(shell dirname $(shell dirname $(shell $(RUN) which python)))

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
	@$(RUN) python3 scripts/update_readme.py

.PHONY: update-docs
update-docs:
	@$(RUN) python3 scripts/update_docs.py

.PHONY: update-copyright
update-copyright:
	@$(RUN) python3 scripts/update_copyright.py

.PHONY: format
format:
	@$(RUN) black $(PYTHON_FILES)

.PHONY: format-docs
format-docs:
	@$(RUN) docformatter $(PYTHON_FILES)

.PHONY: format-str
format-str:
	@$(RUN) flynt $(PYTHON_FILES)

.PHONY: imports
imports:
	@$(RUN) isort $(PYTHON_FILES)

.PHONY: lint
lint:
	@$(RUN) pylint --output-format=colorized $(PYTHON_FILES)

.PHONY: typecheck
typecheck:
	@$(RUN) mypy .

.PHONY: unused
unused:
	@$(RUN) vulture whitelist.py $(PYTHON_FILES)

.PHONY: whitelist
whitelist:
	@$(RUN) vulture --make-whitelist  $(PYTHON_FILES) > whitelist.py \
		|| exit 0

.PHONY: coverage
coverage:
	@$(RUN) pytest -n=auto --cov=docsig --cov=tests \
		&& $(RUN) coverage xml

.PHONY: params
params:
	@$(RUN) docsig $(PYTHON_FILES)

.PHONY: doctest
doctest:
	@$(RUN) pytest docs README.rst --doctest-glob='*.rst'

.PHONY: benchmark
benchmark:
	@RUN_BENCHMARK=true \
		$(RUN) pytest \
		-m="benchmark" \
		--benchmark-save=benchmark

.PHONY: check-links
check-links:
	@ping -c 1 docsig.readthedocs.io >/dev/null 2>&1 \
		&& $(RUN) $(MAKE) -C docs linkcheck \
		|| echo "could not establish connection, skipping"

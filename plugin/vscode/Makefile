########################################################################
# Make Configuration
.DELETE_ON_ERROR:

SOURCE_FILES := $(shell git ls-files "src")
CONFIG_FILES := \
	tsconfig.json \
	eslint.config.mjs \
	.prettierrc.json \
	.vscode-test.mjs \
	Makefile
PACKAGE_FILES := \
	CHANGELOG.md \
	LICENSE \
	licenses/SPHINX_LICENSE \
	README.md \
	package.json \
	media/icon.png

VERSION := $(shell node -p "require('./package.json').version")
VSIX := build/docsig-$(VERSION).vsix

# Use a virtual display when $DISPLAY is unset (CI / remote SSH).
ifeq ($(strip $(DISPLAY)),)
VSCODE_TEST_PREFIX := xvfb-run -a
endif

########################################################################
# Implicit Phony Targets
.PHONY: all help clean

#: show this help message and exit
help:
	@python ../../scripts/make_help.py

#: clean build files
clean:
	@rm -rf .make
	@rm -rf build
	@rm -rf coverage
	@rm -rf out
	@rm -rf resources
	@rm -rf node_modules
	@rm -rf .vscode-test
	@rm -rf LICENSE
	@rm -rf licenses

########################################################################
# Main Targets
node_modules/.package-lock.json: package.json package-lock.json
	@npm install --include=dev

../../bin/poetry/bin/poetry:
	@$(MAKE) -C ../../ bin/poetry/bin/poetry

../../.venv/bin/python: venv ../../bin/poetry/bin/poetry

../../scripts/check_coverage.py: ../../.venv/bin/python

../../build/docsig.pyz:
	@$(MAKE) -C ../../ build build/docsig.pyz

resources/docsig.pyz: ../../build/docsig.pyz
	@mkdir -p $(@D)
	@cp ../../build/docsig.pyz $(@D)
	@touch $@

LICENSE: ../../LICENSE
	@cp $< $(@D)
	@touch $@

licenses/SPHINX_LICENSE: ../../licenses/SPHINX_LICENSE
	@mkdir -p $(@D)
	@cp $< $(@D)
	@touch $@

out/main/extension.js: node_modules/.package-lock.json $(SOURCE_FILES) $(CONFIG_FILES)
	@rm -rf out
	@npx tsc -p ./
	@mkdir -p $(@D)
	@touch $@

.make/format: node_modules/.package-lock.json $(SOURCE_FILES) $(CONFIG_FILES)
	@npx prettier --write src
	@mkdir -p $(@D)
	@touch $@

.make/lint: .make/format out/main/extension.js
	@npx eslint src --max-warnings 0
	@mkdir -p $(@D)
	@touch $@

coverage/coverage-summary.json: out/main/extension.js ../../scripts/check_coverage.py
	@$(VSCODE_TEST_PREFIX) npx vscode-test --coverage
	@mkdir -p $(@D)
	@touch $@

.make/test: coverage/coverage-summary.json
	@../../.venv/bin/python ../../scripts/check_coverage.py --threshold 100
	@mkdir -p $(@D)
	@touch $@

$(VSIX): \
		.make/lint \
		.make/test \
		resources/docsig.pyz \
		$(PACKAGE_FILES)
	@mkdir -p $(@D)
	@npx --yes @vscode/vsce package --no-dependencies -o $(@D)
	@touch $@

########################################################################
# Phony Targets
.PHONY: bundle compile format lint test build verify version watch ide

#: bundle the python cli
bundle: resources/docsig.pyz

#: compile typescript
compile: out/main/extension.js

#: format typescript
format: .make/format

#: lint typescript
lint: .make/lint

#: run extension tests with coverage
test: .make/test

#: build the extension package
build: $(VSIX)

#: verify packaged extension and dependencies
verify: $(VSIX)
	@npx @vscode/vsce ls --tree $(VSIX)
	@npm audit --audit-level=high --omit=dev

#: show program's version number and exit
version:
	@echo $(VERSION)

#: watch mode
watch:
	@tsc -watch -p ./

#: install node dependencies
deps: node_modules/.package-lock.json

#: install venv
venv:
	@$(MAKE) -C ../../ install-venv

bump: part = patch
#: bump version (use: make bump part=major|minor|patch)
bump: venv
	@../../.venv/bin/bump-my-version bump $(part) --verbose

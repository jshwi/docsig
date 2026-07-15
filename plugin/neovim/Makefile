########################################################################
# Make Configuration
.DELETE_ON_ERROR:

SOURCE_FILES := $(shell git ls-files "lua" "plugin")
TEST_FILES := $(shell git ls-files "tests")
SCRIPTS := $(shell git ls-files "scripts")
LUA_FILES := $(shell git ls-files "*.lua")

CONFIG_FILES := .luacov .stylua.toml .luacheckrc .busted
PACKAGE_FILES := README.md

LUA_VERSION := 5.4
STYLUA_VERSION := 2.5.2
VERSION := 1.0.0

LUA_DIR := $(shell \
	if command -v brew >/dev/null 2>&1; then \
		brew --prefix lua@$(LUA_VERSION) 2>/dev/null; \
	elif [ -x /usr/bin/lua$(LUA_VERSION) ]; then \
		echo /usr; \
	fi)
LUAJIT_DIR := $(shell \
	if command -v brew >/dev/null 2>&1; then \
		brew --prefix luajit 2>/dev/null; \
	elif [ -d /usr/include/luajit-2.1 ]; then \
		echo /usr; \
	fi)

LUA_ARGS := $(if $(LUA_DIR), --lua-version=$(LUA_VERSION) --lua-dir=$(LUA_DIR),)


########################################################################
# Implicit Phony Targets
.PHONY: all help clean

#: show this help message and exit
help:
	@python ../../scripts/make_help.py

#: clean build files
clean:
	@rm -rf .make
	@rm -rf .luarocks
	@rm -rf .venv
	@rm -rf coverage
	@rm -rf resources
	@rm -rf .git-root

########################################################################
# Main Targets
../../bin/poetry/bin/poetry:
	@$(MAKE) -C ../../ bin/poetry/bin/poetry

../../.venv/bin/python: venv ../../bin/poetry/bin/poetry

.venv/bin/activate: ../../.venv/bin/python
	@../../.venv/bin/python -m venv .venv

../../scripts/check_coverage.py: ../../.venv/bin/python

.venv/bin/stylua: .venv/bin/activate
	@.venv/bin/pip install -q git+https://github.com/johnnymorganz/stylua@v2.5.2
	@touch $@

../../build/docsig.pyz:
	@$(MAKE) -C ../../ build/docsig.pyz

resources/docsig.pyz: ../../build/docsig.pyz
	@mkdir -p $(@D)
	@cp ../../build/docsig.pyz $(@D)
	@touch $@

.luarocks/.installed:
	@luarocks install --tree .luarocks luacov
	@luarocks --lua-version=5.1 \
		--lua-dir=$(LUAJIT_DIR) \
		install \
		--tree .luarocks \
		busted 2.0.0-1
	@mkdir -p $(@D)
	@touch $@

.luarocks/bin/luacheck: .luarocks/.installed
	@luarocks $(LUA_ARGS) install --tree .luarocks luacheck
	@test -x .luarocks/bin/luacheck
	@touch $@

.make/format: .venv/bin/stylua $(CONFIG_FILES) $(LUA_FILES)
	@.venv/bin/stylua $(LUA_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/format-check: .venv/bin/stylua $(CONFIG_FILES) $(LUA_FILES)
	@.venv/bin/stylua --check $(LUA_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/luacheck: .luarocks/bin/luacheck $(CONFIG_FILES) $(LUA_FILES)
	@.luarocks/bin/luacheck $(LUA_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/lint: .make/format-check .make/luacheck
	@mkdir -p $(@D)
	@touch $@

.make/bundle: resources/docsig.pyz $(SOURCE_FILES) $(PACKAGE_FILES)
	@mkdir -p $(@D)
	@touch $@

.make/test: ../../scripts/check_coverage.py \
		.make/lint \
		.make/bundle \
		.luarocks/.installed \
		$(SOURCE_FILES) \
		$(TEST_FILES) \
		$(CONFIG_FILES)
	@DOCSIG_COVERAGE=1 nvim --headless -u tests/minimal_init.lua -l tests/runner.lua
	@../../.venv/bin/python ../../scripts/check_coverage.py --threshold 100
	@mkdir -p $(@D)
	@touch $@

########################################################################
# Phony Targets
.PHONY: bundle verify version test deps format lint luacheck

#: install luarocks dependencies
deps: .venv/bin/stylua .luarocks/bin/luacheck

#: format lua sources
format: .make/format

#: check lua formatting and static analysis
lint: .make/lint

#: run luacheck static analysis
luacheck: .make/luacheck

#: bundle the python cli
bundle: .make/bundle

#: verify bundled executable exists
verify: .make/bundle
	@test -f resources/docsig.pyz

#: run plugin tests with coverage
test: .make/test

#: show program's version number and exit
version:
	@echo $(VERSION)

#: install venv
venv:
	@$(MAKE) -C ../../ install-venv

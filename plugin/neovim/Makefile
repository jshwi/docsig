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

# uv configuration, mirroring the root makefile so an environment that
# already has a pinned uv is not made to bootstrap a second copy
UV ?= ../../bin/uv/uv
# only ever bootstrap the copy under bin, never an overridden uv
ifeq ($(UV),../../bin/uv/uv)
	UV_BOOTSTRAP := ../../bin/uv/uv
endif
# the shared python scripts declare their own dependencies inline, so
# they run without the project virtual environment
SCRIPT := $(UV) run --script

RETRIES := 3
RETRY_DELAY := 5

# rocks without a src.rock on luarocks.org are fetched from github,
# which intermittently drops the transfer mid-download
retry = n=0; until $(1); do \
		n=$$((n + 1)); \
		[ $$n -lt $(RETRIES) ] || exit 1; \
		sleep $(RETRY_DELAY); \
	done

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
help: $(UV_BOOTSTRAP)
	@$(SCRIPT) ../../scripts/make_help.py

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
../../bin/uv/uv:
	@$(MAKE) -C ../../ bin/uv/uv

../../.venv/bin/python: venv ../../bin/uv/uv

.venv/bin/activate: ../../.venv/bin/python
	@../../.venv/bin/python -m venv .venv

.venv/bin/stylua: .venv/bin/activate
	@$(call retry,.venv/bin/pip install -q \
		git+https://github.com/johnnymorganz/stylua@v$(STYLUA_VERSION))
	@touch $@

../../build/docsig.pyz:
	@$(MAKE) -C ../../ build/docsig.pyz

resources/docsig.pyz: ../../build/docsig.pyz
	@mkdir -p $(@D)
	@cp ../../build/docsig.pyz $(@D)
	@touch $@

.luarocks/.installed:
	@$(call retry,luarocks install --tree .luarocks luacov)
	@$(call retry,luarocks --lua-version=5.1 \
		--lua-dir=$(LUAJIT_DIR) \
		install \
		--tree .luarocks \
		busted 2.0.0-1)
	@mkdir -p $(@D)
	@touch $@

.luarocks/bin/luacheck: .luarocks/.installed
	@$(call retry,luarocks $(LUA_ARGS) install --tree .luarocks luacheck)
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

.make/test: $(UV_BOOTSTRAP) \
		../../scripts/check_coverage.py \
		.make/lint \
		.make/bundle \
		.luarocks/.installed \
		$(SOURCE_FILES) \
		$(TEST_FILES) \
		$(CONFIG_FILES)
	@DOCSIG_COVERAGE=1 nvim --headless -u tests/minimal_init.lua -l tests/runner.lua
	@$(SCRIPT) ../../scripts/check_coverage.py --threshold 100
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

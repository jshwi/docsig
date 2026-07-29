########################################################################
# Make Configuration
.DELETE_ON_ERROR:

# Extract version from gradle.properties
VERSION := $(shell bash ../../scripts/get_docsig_version.sh gradle.properties)

# commands
ifeq ($(shell uname -s),Darwin)
GRADLE := /bin/sh scripts/gradle.sh
else
GRADLE := ./gradlew
endif

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

# File lists
PROJECT_FILES := $(shell git ls-files "src")
SETTINGS_FILES := $(shell git ls-files "*.kts")
CONFIG_FILES := .editorconfig detekt.yaml Makefile

########################################################################
# Implicit Phony Targets
.PHONY: all help clean ide

#: show this help message and exit
help: $(UV_BOOTSTRAP)
	@$(SCRIPT) ../../scripts/make_help.py

#: clean build files
clean:
	@rm -rf .make
	@rm -rf .gradle
	@rm -rf .intellijPlatform
	@rm -rf .kotlin
	@rm -rf build

#: test the plugin in a sandboxed ide
ide:
	@$(GRADLE) runIde

#: show program's version number and exit
version:
	@echo $(VERSION)

########################################################################
# Main Targets
../../bin/uv/uv:
	@$(MAKE) -C ../../ bin/uv/uv

.make/format: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) ktlintFormat
	@mkdir -p $(@D)
	@touch $@

.make/test: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) koverVerify koverHtmlReport
	@mkdir -p $(@D)
	@touch $@

detekt-baseline.xml: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) detekt
	@mkdir -p $(@D)
	@touch $@

build/distributions/docsig-$(VERSION).zip: .make/format .make/test detekt-baseline.xml
	@$(GRADLE) buildPlugin
	@mkdir -p $(@D)
	@touch $@

########################################################################
# Phony Targets
.PHONY: format test detect docs build refresh verify venv bump

#: format source code
format: .make/format

#: test source code
test: .make/test

#: audit code quality
detect: detekt-baseline.xml

#: build the plugin
build: build/distributions/docsig-$(VERSION).zip

#: refresh build
refresh:
	@$(GRADLE) compileKotlin compileTestKotlin --rerun-tasks -q

#: verify plugin
verify:
	@$(GRADLE) verifyPlugin

#: publish plugin
publish:
	@$(GRADLE) publishPlugin

#: install venv
venv:
	@$(MAKE) -C ../../ install-venv

bump: part = patch
#: bump version (use: make bump part=major|minor|patch)
bump: venv
	@../../.venv/bin/bump-my-version bump $(part) --verbose

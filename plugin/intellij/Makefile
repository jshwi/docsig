########################################################################
# Make Configuration
.DELETE_ON_ERROR:

YELLOW := \033[33m
RESET  := \033[0m

# Extract version from pyproject.toml
VERSION := $(shell cd ../../ && bash scripts/get_docsig_version.sh)

# Poetry configuration
POETRY := ../../bin/poetry/bin/poetry

# Build artifact
BUILD := build/distributions/docsig-$(VERSION).zip

# File lists
KT_FILES := $(shell git ls-files "*.kt")
KTS_FILES := $(shell git ls-files "*.kts")
CONFIG_FILES := .editorconfig ../../.editorconfig detekt.yml

########################################################################
# Implicit Phony Targets
.PHONY: all
all: help

.PHONY: help
help: $(VENV)
	@$(POETRY) run python ../../scripts/make_help.py

########################################################################
# Main Targets
.make/format: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES) detekt-baseline.xml
	@/bin/sh gradlew ktlintFormat
	@mkdir -p $(@D)
	@touch $@

.make/test: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES) detekt-baseline.xml
	@/bin/sh gradlew test
	@mkdir -p $(@D)
	@touch $@

.make/detekt: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@output="$$(/bin/sh gradle.sh detekt 2>&1)"; \
	if echo "$$output" | \
			grep -q "Error on position 1:1 while reading the baseline xml file!"; then \
		echo "$(YELLOW)warning: detekt-baseline.xml is empty$(RESET)"; \
		echo "$(YELLOW)warning: removing target$(RESET)"; \
		rm -rf detekt-baseline.xml; \
		/bin/sh gradle.sh detekt; \
	fi
	@/bin/sh gradle.sh detekt
	@mkdir -p $(@D)
	@touch $@

detekt-baseline.xml: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES) .make/detekt
	@/bin/sh gradle.sh detektBaseline || echo "$(YELLOW)warning: command failed$(RESET)"
	@if ! [ -f detekt-baseline.xml ]; then \
		echo "$(YELLOW)warning: detekt-baseline.xml is empty$(RESET)"; \
		echo "$(YELLOW)warning: not creating target$(RESET)"; \
	fi

$(BUILD): .make/format .make/test detekt-baseline.xml
	@/bin/sh gradlew buildPlugin
	@touch $@

########################################################################
# Phony Targets
.PHONY: ide format test detect build

#: test the plugin in a sandboxed ide
ide:
	@/bin/sh gradlew runIde

#: format source code
format: .make/format

#: test source code
test: .make/test

#: audit code quality
detect: .make/detekt

#: build the plugin
build: $(BUILD)

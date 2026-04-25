########################################################################
# Make Configuration
.DELETE_ON_ERROR:

# Poetry configuration
POETRY := ../../bin/poetry/bin/poetry

# File lists
KT_FILES := $(shell git ls-files "*.kt")
KTS_FILES := $(shell git ls-files "*.kts")
CONFIG_FILES := .editorconfig ../../.editorconfig detekt.yml

########################################################################
# Implicit Phony Targets
.PHONY: all help clean ide

#: show this help message and exit
help: $(VENV)
	@$(POETRY) run python ../../scripts/make_help.py

#: clean build files
clean:
	@rm -rf .make

#: test the plugin in a sandboxed ide
ide:
	@/bin/sh gradlew runIde

########################################################################
# Main Targets
detekt-baseline.xml: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@/bin/sh scripts/gradle.sh detektBaseline
	@mkdir -p $(@D)
	@touch $@

.make/format: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@/bin/sh scripts/gradle.sh ktlintFormat
	@mkdir -p $(@D)
	@touch $@

.make/test: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@/bin/sh scripts/gradle.sh koverVerify koverHtmlReport
	@mkdir -p $(@D)
	@touch $@

.make/detekt: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@/bin/sh scripts/gradle.sh detekt
	@mkdir -p $(@D)
	@touch $@

.make/docs: $(KT_FILES) $(KTS_FILES) $(CONFIG_FILES)
	@/bin/sh scripts/gradle.sh dokkaGenerate
	@mkdir -p $(@D)
	@touch $@

.make/build: .make/format .make/test .make/detekt .make/docs
	@/bin/sh scripts/gradle.sh buildPlugin
	@mkdir -p $(@D)
	@touch $@

########################################################################
# Phony Targets
.PHONY: ide format test detect build docs clean detekt-baseline.xml

#: format source code
format: .make/format

#: test source code
test: .make/test

#: audit code quality
detect: .make/detekt

#: build the plugin
build: .make/build

#: build docs
docs: .make/docs

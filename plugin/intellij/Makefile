########################################################################
# Make Configuration
.DELETE_ON_ERROR:

# Extract version from gradle.properties
VERSION := $(shell bash ../../scripts/get_docsig_version.sh gradle.properties)

# commands
GRADLE := /bin/sh scripts/gradle.sh

# File lists
PROJECT_FILES := $(shell git ls-files "src")
SETTINGS_FILES := $(shell git ls-files "*.kts")
CONFIG_FILES := .editorconfig detekt.yaml Makefile

########################################################################
# Implicit Phony Targets
.PHONY: all help clean ide

#: show this help message and exit
help: $(REL_VENV)
	@python ../../scripts/make_help.py

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

########################################################################
# Main Targets
.make/format: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) ktlintFormat
	@mkdir -p $(@D)
	@touch $@

build/reports/kover/html/index.html: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) koverVerify koverHtmlReport
	@mkdir -p $(@D)
	@touch $@

detekt-baseline.xml: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) detekt
	@mkdir -p $(@D)
	@touch $@

build/dokka/html/index.html: $(PROJECT_FILES) $(SETTINGS_FILES) $(CONFIG_FILES)
	@$(GRADLE) dokkaGenerate
	@mkdir -p $(@D)
	@touch $@

build/distributions/docsig-$(VERSION).zip: .make/format \
		build/reports/kover/html/index.html \
		detekt-baseline.xml \
		build/dokka/html/index.html
	@$(GRADLE) buildPlugin
	@mkdir -p $(@D)
	@touch $@

########################################################################
# Phony Targets
.PHONY: format test detect docs build

#: format source code
format: .make/format

#: test source code
test: build/reports/kover/html/index.html

#: audit code quality
detect: detekt-baseline.xml

#: build docs
docs: build/dokka/html/index.html

#: build the plugin
build: build/distributions/docsig-$(VERSION).zip

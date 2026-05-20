/**
 * Option table definitions for the settings UI and CLI argv building.
 */
package com.github.jshwi.docsig.ui

/**
 * Canonical option table backing the settings UI and command builder.
 */
internal class Options {
    val entries: List<Option> =
        listOf(
            EnumOption(
                "settings.option.class-checking-mode.title",
                CHECK,
                "settings.option.class-checking-mode.summary",
                { it.state.classCheckMode },
                { s, v -> s.state.classCheckMode = v },
                ClassCheckMode.entries,
                { it.flag },
                { it.label },
            ),
            BoolOption(
                "settings.options.check-dunders.title",
                CHECK,
                "settings.options.check-dunders.summary",
                "--check-dunders",
                { it.state.checkDunders },
                { s, v -> s.state.checkDunders = v },
            ),
            BoolOption(
                "settings.options.check-nested.title",
                CHECK,
                "settings.options.check-nested.summary",
                "--check-nested",
                { it.state.checkNested },
                { s, v -> s.state.checkNested = v },
            ),
            BoolOption(
                "settings.options.check-overridden.title",
                CHECK,
                "settings.options.check-overridden.summary",
                "--check-overridden",
                { it.state.checkOverridden },
                { s, v -> s.state.checkOverridden = v },
            ),
            BoolOption(
                "settings.options.check-property-returns.title",
                CHECK,
                "settings.options.check-property-returns.summary",
                "--check-property-returns",
                { it.state.checkPropertyReturns },
                { s, v -> s.state.checkPropertyReturns = v },
            ),
            BoolOption(
                "settings.options.check-protected.title",
                CHECK,
                "settings.options.check-protected.summary",
                "--check-protected",
                { it.state.checkProtected },
                { s, v -> s.state.checkProtected = v },
            ),
            BoolOption(
                "settings.options.ignore-args.title",
                IGNORE,
                "settings.options.ignore-args.summary",
                "--ignore-args",
                { it.state.ignoreArgs },
                { s, v -> s.state.ignoreArgs = v },
            ),
            BoolOption(
                "settings.options.ignore-kwargs.title",
                IGNORE,
                "settings.options.ignore-kwargs.summary",
                "--ignore-kwargs",
                { it.state.ignoreKwargs },
                { s, v -> s.state.ignoreKwargs = v },
            ),
            BoolOption(
                "settings.options.ignore-no-params.title",
                IGNORE,
                "settings.options.ignore-no-params.summary",
                "--ignore-no-params",
                { it.state.ignoreNoParams },
                { s, v -> s.state.ignoreNoParams = v },
            ),
            BoolOption(
                "settings.options.file-discovery-include-ignored.title",
                FILE_DISCOVERY,
                "settings.options.file-discovery-include-ignored.summary",
                "--include-ignored",
                { it.state.includeIgnored },
                { s, v -> s.state.includeIgnored = v },
            ),
            StringOption(
                "settings.options.file-discovery-exclude-pattern.title",
                FILE_DISCOVERY,
                "settings.options.file-discovery-exclude-pattern.summary",
                "--exclude",
                { it.state.exclude },
                { s, v -> s.state.exclude = v },
            ),
            WhitespaceListOption(
                "settings.options.file-discovery.exclude-path.title",
                FILE_DISCOVERY,
                "settings.options.file-discovery.exclude-path.summary",
                "--excludes",
                { it.state.excludes },
                { s, v -> s.state.excludes = v },
                io = ProjectPathOptionIo(),
            ),
            CommaListOption(
                "settings.options.messages-disable.title",
                MESSAGES,
                "settings.options.messages-disable.summary",
                "--disable",
                { it.state.disable },
                { s, v -> s.state.disable = v },
                { it },
                { it },
            ),
            CommaListOption(
                "settings.options.messages-target.title",
                MESSAGES,
                "settings.options.messages-target.summary",
                "--target",
                { it.state.target },
                { s, v -> s.state.target = v },
                { it },
                { it },
            ),
        )

    companion object {
        // groups
        private const val CHECK = "settings.group.check"
        private const val IGNORE = "settings.group.ignore"
        private const val FILE_DISCOVERY = "settings.group.file-discovery"
        private const val MESSAGES = "settings.group.messages"

        internal val default = Options()
    }
}

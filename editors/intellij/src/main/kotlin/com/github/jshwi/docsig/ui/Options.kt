package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.intellij.openapi.project.Project

internal class Options(project: Project) {
    internal val entries: List<Option> =
        listOf(
            EnumOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.option.class-checking-mode.title",
                ),
                DocsigBundle.message(
                    "settings.option.class-checking-mode.summary",
                ),
                { it.state.classCheckMode },
                { s, v -> s.state.classCheckMode = v },
                ClassCheckMode.entries,
                { it.flag },
            ) { it.label },
            BoolOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.options.check-dunders.title",
                ),
                DocsigBundle.message(
                    "settings.options.check-dunders.summary",
                ),
                "--check-dunders",
                { it.state.checkDunders },
            ) { s, v -> s.state.checkDunders = v },
            BoolOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.options.check-nested.title",
                ),
                DocsigBundle.message(
                    "settings.options.check-nested.summary",
                ),
                "--check-nested",
                { it.state.checkNested },
            ) { s, v -> s.state.checkNested = v },
            BoolOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.options.check-overridden.title",
                ),
                DocsigBundle.message(
                    "settings.options.check-overridden.summary",
                ),
                "--check-overridden",
                { it.state.checkOverridden },
            ) { s, v -> s.state.checkOverridden = v },
            BoolOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.options.check-property-returns.title",
                ),
                DocsigBundle.message(
                    "settings.options.check-property-returns.summary",
                ),
                "--check-property-returns",
                { it.state.checkPropertyReturns },
            ) { s, v -> s.state.checkPropertyReturns = v },
            BoolOption(
                project,
                Group.CHECK,
                DocsigBundle.message(
                    "settings.options.check-protected.title",
                ),
                DocsigBundle.message(
                    "settings.options.check-protected.summary",
                ),
                "--check-protected",
                { it.state.checkProtected },
            ) { s, v -> s.state.checkProtected = v },
            BoolOption(
                project,
                Group.IGNORE,
                DocsigBundle.message(
                    "settings.options.ignore-args.title",
                ),
                DocsigBundle.message(
                    "settings.options.ignore-args.summary",
                ),
                "--ignore-args",
                { it.state.ignoreArgs },
            ) { s, v -> s.state.ignoreArgs = v },
            BoolOption(
                project,
                Group.IGNORE,
                DocsigBundle.message(
                    "settings.options.ignore-kwargs.title",
                ),
                DocsigBundle.message(
                    "settings.options.ignore-kwargs.summary",
                ),
                "--ignore-kwargs",
                { it.state.ignoreKwargs },
            ) { s, v -> s.state.ignoreKwargs = v },
            BoolOption(
                project,
                Group.IGNORE,
                DocsigBundle.message(
                    "settings.options.ignore-no-params.title",
                ),
                DocsigBundle.message(
                    "settings.options.ignore-no-params.summary",
                ),
                "--ignore-no-params",
                { it.state.ignoreNoParams },
            ) { s, v -> s.state.ignoreNoParams = v },
            BoolOption(
                project,
                Group.FILE_DISCOVERY,
                DocsigBundle.message(
                    "settings.options.file-discovery-include-ignored.title",
                ),
                DocsigBundle.message(
                    "settings.options.file-discovery-include-ignored.summary",
                ),
                "--include-ignored",
                { it.state.includeIgnored },
            ) { s, v -> s.state.includeIgnored = v },
            StringOption(
                project,
                Group.FILE_DISCOVERY,
                DocsigBundle.message(
                    "settings.options.file-discovery-exclude-pattern.title",
                ),
                DocsigBundle.message(
                    "settings.options.file-discovery-exclude-pattern.summary",
                ),
                "--exclude",
                { it.state.exclude },
                { s, v -> s.state.exclude = v },
            ),
            WhitespaceListOption(
                project,
                Group.FILE_DISCOVERY,
                DocsigBundle.message(
                    "settings.options.file-discovery.exclude-path.title",
                ),
                DocsigBundle.message(
                    "settings.options.file-discovery.exclude-path.summary",
                ),
                "--excludes",
                { it.state.excludes },
                { s, v -> s.state.excludes = v },
                io = ProjectPathOptionIo(),
            ),
            CommaListOption(
                project,
                Group.MESSAGES,
                DocsigBundle.message(
                    "settings.options.messages-disable.title",
                ),
                DocsigBundle.message(
                    "settings.options.messages-disable.summary",
                ),
                "--disable",
                { it.state.disable },
                { s, v -> s.state.disable = v },
                { it },
                { it },
            ),
            CommaListOption(
                project,
                Group.MESSAGES,
                DocsigBundle.message(
                    "settings.options.messages-target.title",
                ),
                DocsigBundle.message(
                    "settings.options.messages-target.summary",
                ),
                "--target",
                { it.state.target },
                { s, v -> s.state.target = v },
                { it },
                { it },
            ),
        )
}

package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

/**
 * Smoke test that every option row from [Options.default] supports the
 * option lifecycle.
 */
class OptionsTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    @Test
    fun `all options execute lifecycle methods`() {
        val settings = DocsigSettings()
        DocsigSettings.settingsProvider = { settings }

        Options.default.entries.forEach { option ->

            val args = mutableListOf<String>()

            option.apply(testProject) { args.add(it) }

            option.isModified(testProject)

            option.applyTo(testProject)

            option.resetFrom(testProject)
        }
    }

    @Test
    fun `option table lambdas are exercised`() {
        val settings = DocsigSettings()

        val classModeOpt =
            Options.default.entries.first() as EnumOption<ClassCheckMode>
        classModeOpt.set(settings, ClassCheckMode.CLASS)
        assertEquals(ClassCheckMode.CLASS, classModeOpt.get(settings))
        assertEquals(
            DocsigBundle.message(
                "settings.options.class-checking-mode-check-class",
            ),
            classModeOpt.display(ClassCheckMode.CLASS),
        )

        @Suppress("UNCHECKED_CAST")
        val disableOpt =
            Options.default.entries.first {
                it.label ==
                    DocsigBundle.message(
                        "settings.options.messages-disable.title",
                    )
            } as CommaListOption<String>
        assertEquals(
            "x",
            disableOpt.io.toInput(testProject, "x"),
        )
        assertEquals(
            "y",
            disableOpt.io.fromInput(testProject, "y"),
        )

        @Suppress("UNCHECKED_CAST")
        val targetOpt =
            Options.default.entries.first {
                it.label ==
                    DocsigBundle.message(
                        "settings.options.messages-target.title",
                    )
            } as CommaListOption<String>
        assertEquals(
            "a",
            targetOpt.io.toInput(testProject, "a"),
        )
        assertEquals(
            "b",
            targetOpt.io.fromInput(testProject, "b"),
        )

        @Suppress("UNCHECKED_CAST")
        val excludesOpt =
            Options.default.entries.first {
                it.label ==
                    DocsigBundle.message(
                        "settings.options.file-discovery.exclude-path.title",
                    )
            } as WhitespaceListOption<String>
        assertEquals(
            "exclude/me",
            excludesOpt.io.toInput(testProject, "exclude/me"),
        )
        assertEquals(
            "exclude/me",
            excludesOpt.io.fromInput(testProject, "exclude/me"),
        )
    }
}

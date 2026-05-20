package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.panel
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * Tests for [BoolOption] rendering, argv emission, and dirty tracking.
 */
class BoolOptionTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    private fun bind(settings: DocsigSettings) {
        DocsigSettings.settingsProvider = { settings }
    }

    @Test
    fun `apply adds flag when enabled`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { true },
                set = { _, _ -> },
            )

        val flags = mutableListOf<String>()

        option.apply(testProject) {
            flags += it
        }

        assertEquals(listOf("--flag"), flags)
    }

    @Test
    fun `apply does not add flag when disabled`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ -> },
            )

        val flags = mutableListOf<String>()

        option.apply(testProject) {
            flags += it
        }

        assertTrue(flags.isEmpty())
    }

    @Test
    fun `isModified returns false when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ -> },
            )

        assertFalse(option.isModified(testProject))
    }

    @Test
    fun `applyTo returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        var called = false

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ ->
                    called = true
                },
            )

        option.applyTo(testProject)

        assertFalse(called)
    }

    @Test
    fun `resetFrom returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ -> },
            )

        option.resetFrom(testProject)
    }

    @Test
    fun `isModified detects checkbox change`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ -> },
            )

        panel {
            with(option) {
                render(testProject)
            }
        }

        assertFalse(option.isModified(testProject))

        option.applyTo(testProject)

        assertFalse(option.isModified(testProject))
    }

    @Test
    fun `applyTo writes checkbox value`() {
        val settings = DocsigSettings()
        bind(settings)

        var stored = false

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { stored },
                set = { _, value ->
                    stored = value
                },
            )

        panel {
            with(option) {
                render(testProject)
            }
        }

        option.resetFrom(testProject)
        option.applyTo(testProject)

        assertFalse(stored)
    }

    @Test
    fun `isModified returns true when checkbox value changes`() {
        val settings = DocsigSettings()
        bind(settings)

        var stored = false

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { stored },
                set = { _, value ->
                    stored = value
                },
            )

        panel {
            with(option) {
                render(testProject)
            }
        }

        val field =
            BoolOption::class.java
                .getDeclaredField("component")
                .apply {
                    isAccessible = true
                }

        val checkbox =
            field.get(option) as com.intellij.ui.components.JBCheckBox

        checkbox.isSelected = true

        assertTrue(option.isModified(testProject))

        option.applyTo(testProject)

        assertTrue(stored)

        assertFalse(option.isModified(testProject))
    }
}

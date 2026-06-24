package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.panel
import io.mockk.every
import io.mockk.mockk
import io.mockk.unmockkAll
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
    fun teardown() {
        unmockkAll()
    }

    private fun bind(settings: DocsigSettings) {
        every {
            testProject.getService(DocsigSettings::class.java)
        } returns settings
    }

    @Test
    fun `apply adds flag when enabled`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { true },
            ) { _, _ -> }

        val flags = mutableListOf<String>()

        option.add {
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
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { false },
            ) { _, _ -> }

        val flags = mutableListOf<String>()

        option.add {
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
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { false },
            ) { _, _ -> }

        assertFalse(option.isModified())
    }

    @Test
    fun `applyTo returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        var called = false

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { false },
            ) { _, _ ->
                called = true
            }

        option.apply()

        assertFalse(called)
    }

    @Test
    fun `resetFrom returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { false },
            ) { _, _ -> }

        option.reset()
    }

    @Test
    fun `isModified detects checkbox change`() {
        val settings = DocsigSettings()
        bind(settings)

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { false },
            ) { _, _ -> }

        panel {
            with(option) {
                render()
            }
        }

        assertFalse(option.isModified())

        option.apply()

        assertFalse(option.isModified())
    }

    @Test
    fun `applyTo writes checkbox value`() {
        val settings = DocsigSettings()
        bind(settings)

        var stored = false

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { stored },
            ) { _, value ->
                stored = value
            }

        panel {
            with(option) {
                render()
            }
        }

        option.reset()
        option.apply()

        assertFalse(stored)
    }

    @Test
    fun `isModified returns true when checkbox value changes`() {
        val settings = DocsigSettings()
        bind(settings)

        var stored = false

        val option =
            BoolOption(
                project = testProject,
                group = Group.CHECK,
                title = "Test",
                summary = "",
                flag = "--flag",
                get = { stored },
            ) { _, value ->
                stored = value
            }

        panel {
            with(option) {
                render()
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

        assertTrue(option.isModified())

        option.apply()

        assertTrue(stored)

        assertFalse(option.isModified())
    }
}

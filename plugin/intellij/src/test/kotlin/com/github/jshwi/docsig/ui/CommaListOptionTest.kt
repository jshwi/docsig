package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * Tests for [CommaListOption] panel binding and comma-joined argv fragments.
 */
class CommaListOptionTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    private fun bind(settings: DocsigSettings) {
        DocsigSettings.settingsProvider = { settings }
    }

    private fun option(
        get: (DocsigSettings) -> List<String>,
        set: (DocsigSettings, List<String>) -> Unit = { _, _ -> },
    ): CommaListOption<String> =
        CommaListOption(
            label = "test",
            group = "group",
            summary = "",
            flag = "--flag",
            get = get,
            set = set,
            serialize = { it },
            parse = { it },
        )

    @Test
    fun apply_adds_flag_and_values() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a", "b") },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertEquals(listOf("--flag", "a,b"), out)
    }

    @Test
    fun apply_skips_empty_list() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> emptyList() },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertTrue(out.isEmpty())
    }

    @Test
    fun isModified_false_when_null_component() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a") },
            )

        assertFalse(opt.isModified(testProject))
    }

    @Test
    fun applyTo_noop_when_null_component() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a") },
            )

        opt.applyTo(testProject)
    }

    @Test
    fun resetFrom_noop_when_null_component() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a") },
            )

        opt.resetFrom(testProject)
    }

    @Test
    fun applyTo_updates_set_callback() {
        val settings = DocsigSettings()
        bind(settings)

        var captured: List<String>? = null

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("x", "y") },
                set = { _: DocsigSettings, v -> captured = v },
            )

        val panel = ListPanel(mutableListOf("x", "y"))

        val field = ListOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, panel)

        opt.applyTo(testProject)

        assertEquals(listOf("x", "y"), captured)
    }

    @Test
    fun resetFrom_updates_panel_values() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a", "b") },
            )

        val panel = ListPanel(mutableListOf("old"))

        val field = ListOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, panel)

        opt.resetFrom(testProject)

        assertEquals(listOf("a", "b"), panel.values())
    }

    @Test
    fun isModified_detects_difference() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a") },
            )

        val panel = ListPanel(listOf("b"))

        val field = ListOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, panel)

        assertTrue(opt.isModified(testProject))
    }
}

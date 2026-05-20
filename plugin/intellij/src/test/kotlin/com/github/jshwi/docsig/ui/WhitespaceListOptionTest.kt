package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

/**
 * Tests for [WhitespaceListOption] argv emission and panel binding.
 */
class WhitespaceListOptionTest {
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
    ): WhitespaceListOption<String> =
        WhitespaceListOption(
            label = "test",
            group = "group",
            summary = "",
            flag = "--excludes",
            get = get,
            set = set,
            serialize = { it },
            parse = { it },
        )

    @Test
    fun apply_adds_flag_and_one_token_per_value() {
        val settings = DocsigSettings()
        bind(settings)

        val project = mockk<Project>(relaxed = true)

        val opt =
            option(
                get = { _: DocsigSettings -> listOf("a", "b") },
            )

        val out = mutableListOf<String>()

        opt.apply(project) { out.add(it) }

        assertEquals(listOf("--excludes", "a", "b"), out)
    }

    @Test
    fun apply_skips_empty_list() {
        val settings = DocsigSettings()
        bind(settings)

        val project = mockk<Project>(relaxed = true)

        val opt =
            option(
                get = { _: DocsigSettings -> emptyList() },
            )

        val out = mutableListOf<String>()

        opt.apply(project) { out.add(it) }

        assertEquals(emptyList<String>(), out)
    }

    @Test
    fun applyTo_updates_set_callback() {
        val settings = DocsigSettings()
        bind(settings)

        val project = mockk<Project>(relaxed = true)

        var captured: List<String>? = null

        val opt =
            option(
                get = { _: DocsigSettings -> emptyList() },
                set = { _: DocsigSettings, v -> captured = v },
            )

        val panel = ListPanel(mutableListOf("./x", "y"))

        val field = ListOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, panel)

        opt.applyTo(project)

        assertEquals(listOf("./x", "y"), captured)
    }
}

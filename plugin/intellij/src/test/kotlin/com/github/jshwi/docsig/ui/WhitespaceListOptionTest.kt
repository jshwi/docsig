package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.every
import io.mockk.mockk
import io.mockk.unmockkAll
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

/**
 * Tests for [WhitespaceListOption] argv emission and panel binding.
 */
class WhitespaceListOptionTest {
    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    private fun bind(project: Project, settings: DocsigSettings) {
        every {
            project.getService(DocsigSettings::class.java)
        } returns settings
    }

    private fun option(
        project: Project,
        get: (DocsigSettings) -> List<String>,
        set: (DocsigSettings, List<String>) -> Unit = { _, _ -> },
    ): WhitespaceListOption<String> = WhitespaceListOption(
        project = project,
        label = "test",
        group = Group.CHECK,
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
        val project = mockk<Project>(relaxed = true)
        bind(project, settings)

        val opt =
            option(
                project = project,
                get = { _: DocsigSettings -> listOf("a", "b") },
            )

        val out = mutableListOf<String>()

        opt.add { out.add(it) }

        assertEquals(listOf("--excludes", "a", "b"), out)
    }

    @Test
    fun apply_skips_empty_list() {
        val settings = DocsigSettings()
        val project = mockk<Project>(relaxed = true)
        bind(project, settings)

        val opt =
            option(
                project = project,
                get = { _: DocsigSettings -> emptyList() },
            )

        val out = mutableListOf<String>()

        opt.add { out.add(it) }

        assertEquals(emptyList<String>(), out)
    }

    @Test
    fun applyTo_updates_set_callback() {
        val settings = DocsigSettings()
        val project = mockk<Project>(relaxed = true)
        bind(project, settings)

        var captured: List<String>? = null

        val opt =
            option(
                project = project,
                get = { _: DocsigSettings -> emptyList() },
                set = { _: DocsigSettings, v -> captured = v },
            )

        val panel = ListPanel(mutableListOf("./x", "y"))

        val field = ListOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, panel)

        opt.apply()

        assertEquals(listOf("./x", "y"), captured)
    }
}

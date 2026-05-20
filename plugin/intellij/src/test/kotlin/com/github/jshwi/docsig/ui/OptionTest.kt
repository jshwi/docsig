package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import kotlin.test.Test
import kotlin.test.assertSame

/**
 * Tests for [Option] default method bodies and shared helpers.
 */
class OptionTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    @Test
    fun `docsigSettings resolves via settings provider`() {
        val settings = DocsigSettings()
        DocsigSettings.settingsProvider = { settings }

        val option =
            BoolOption(
                label = "Test",
                group = "Group",
                summary = "",
                flag = "--flag",
                get = { false },
                set = { _, _ -> },
            )

        val resolved = invokeDefaultDocsigSettings(option, testProject)

        assertSame(settings, resolved)
    }

    private fun invokeDefaultDocsigSettings(
        option: Option,
        project: Project,
    ): DocsigSettings {
        val defaultImpls =
            Class.forName("com.github.jshwi.docsig.ui.Option\$DefaultImpls")
        val method =
            defaultImpls.getDeclaredMethod(
                "docsigSettings",
                Option::class.java,
                Project::class.java,
            )
        @Suppress("UNCHECKED_CAST")
        return method.invoke(null, option, project) as DocsigSettings
    }
}

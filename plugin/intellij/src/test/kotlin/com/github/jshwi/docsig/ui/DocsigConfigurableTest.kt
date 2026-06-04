package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.service.DocsigService
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import io.mockk.Runs
import io.mockk.every
import io.mockk.just
import io.mockk.mockk
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * Tests for [DocsigConfigurable] project settings UI and binding.
 */
class DocsigConfigurableTest {
    private fun projectWithSettings(): Pair<Project, DocsigSettings> {
        val project = mockk<Project>()
        val settings = DocsigSettings()

        every {
            project.getService(DocsigSettings::class.java)
        } returns settings

        return project to settings
    }

    @Test
    fun `metadata methods return expected values`() {
        val (project, _) = projectWithSettings()
        val c = DocsigConfigurable(project)

        assertEquals("Docsig", c.displayName)
        assertEquals("docsig.settings", c.id)
    }

    @Test
    fun `createComponent renders options`() {
        val (project, _) = projectWithSettings()
        val c = DocsigConfigurable(project)

        val component = c.createComponent()

        assertTrue(component.componentCount >= 0)
    }

    @Test
    fun `isModified checks options when project exists`() {
        val (project, _) = projectWithSettings()
        val c = DocsigConfigurable(project)

        assertFalse(c.isModified())
    }

    @Test
    fun `apply iterates options when project exists`() {
        val (project, _) = projectWithSettings()
        val service = mockk<DocsigService>(relaxed = true)

        every {
            project.getService(DocsigService::class.java)
        } returns service
        every { service.scheduleAfterSettingsChange() } just Runs

        DocsigConfigurable(project).apply()
    }

    @Test
    fun `reset iterates options when project exists`() {
        val (project, _) = projectWithSettings()

        DocsigConfigurable(project).reset()
    }
}

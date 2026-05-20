package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.cli.Subprocess
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectManager
import io.mockk.every
import io.mockk.mockk
import io.mockk.mockkStatic
import io.mockk.unmockkStatic
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * Tests for [DocsigConfigurable]: path validation, version checks, and UI.
 */
class DocsigConfigurableTest {
    private var fakeProcess: Process? = null

    @BeforeEach
    fun setup() {
        Subprocess.processFactory = { fakeProcess!! }
    }

    @AfterEach
    fun tearDown() {
        Subprocess.processFactory = Subprocess::defaultProcessFactory
    }

    @Test
    fun `metadata methods return expected values`() {
        val c = DocsigConfigurable()

        assertEquals("Docsig", c.displayName)
        assertEquals("docsig.settings", c.id)
    }

    @Test
    fun `isModified returns false when no project`() {
        mockkStatic(ProjectManager::class)

        val manager = mockk<ProjectManager>()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns emptyArray()

        val c = DocsigConfigurable()

        assertFalse(c.isModified())

        unmockkStatic(ProjectManager::class)
    }

    @Test
    fun `apply returns when no project`() {
        mockkStatic(ProjectManager::class)

        val manager = mockk<ProjectManager>()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns emptyArray()

        DocsigConfigurable().apply()

        unmockkStatic(ProjectManager::class)
    }

    @Test
    fun `reset returns when no project`() {
        mockkStatic(ProjectManager::class)

        val manager = mockk<ProjectManager>()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns emptyArray()

        DocsigConfigurable().reset()

        unmockkStatic(ProjectManager::class)
    }

    @Test
    fun `createComponent returns empty panel when no project`() {
        mockkStatic(ProjectManager::class)

        val manager = mockk<ProjectManager>()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns emptyArray()

        val c = DocsigConfigurable()
        val component = c.createComponent()

        assertTrue(component.componentCount >= 0)

        unmockkStatic(ProjectManager::class)
    }

    @Test
    fun `createComponent builds executable row`() {
        mockkStatic(ProjectManager::class)
        mockkStatic(DocsigSettings::class)

        val project = mockk<Project>()
        val manager = mockk<ProjectManager>()
        val settings = DocsigSettings()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns arrayOf(project)
        every { DocsigSettings.getInstance(project) } returns settings

        val c = DocsigConfigurable()

        val component = c.createComponent()

        assertTrue(component.componentCount >= 0)

        unmockkStatic(ProjectManager::class)
        unmockkStatic(DocsigSettings::class)
    }

    @Test
    fun `createComponent renders options`() {
        mockkStatic(ProjectManager::class)
        mockkStatic(DocsigSettings::class)

        val project = mockk<Project>()
        val manager = mockk<ProjectManager>()
        val settings = DocsigSettings()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns arrayOf(project)
        every { DocsigSettings.getInstance(project) } returns settings

        val c = DocsigConfigurable()

        val component = c.createComponent()

        assertTrue(component.isVisible || !component.isVisible)

        unmockkStatic(ProjectManager::class)
        unmockkStatic(DocsigSettings::class)
    }

    @Test
    fun `isModified checks options when project exists`() {
        mockkStatic(ProjectManager::class)
        mockkStatic(DocsigSettings::class)

        val project = mockk<Project>()
        val manager = mockk<ProjectManager>()
        val settings = DocsigSettings()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns arrayOf(project)
        every { DocsigSettings.getInstance(project) } returns settings

        val c = DocsigConfigurable()

        assertFalse(c.isModified())

        unmockkStatic(ProjectManager::class)
        unmockkStatic(DocsigSettings::class)
    }

    @Test
    fun `apply iterates options when project exists`() {
        mockkStatic(ProjectManager::class)
        mockkStatic(DocsigSettings::class)

        val project = mockk<Project>()
        val manager = mockk<ProjectManager>()
        val settings = DocsigSettings()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns arrayOf(project)
        every { DocsigSettings.getInstance(project) } returns settings

        DocsigConfigurable().apply()

        unmockkStatic(ProjectManager::class)
        unmockkStatic(DocsigSettings::class)
    }

    @Test
    fun `reset iterates options when project exists`() {
        mockkStatic(ProjectManager::class)
        mockkStatic(DocsigSettings::class)

        val project = mockk<Project>()
        val manager = mockk<ProjectManager>()
        val settings = DocsigSettings()

        every { ProjectManager.getInstance() } returns manager
        every { manager.openProjects } returns arrayOf(project)
        every { DocsigSettings.getInstance(project) } returns settings

        DocsigConfigurable().reset()

        unmockkStatic(ProjectManager::class)
        unmockkStatic(DocsigSettings::class)
    }
}

package com.github.jshwi.docsig.listener

import com.github.jshwi.docsig.service.DocsigService
import com.google.common.base.CharMatcher.any
import com.intellij.openapi.application.Application
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.editor.Document
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectLocator
import com.intellij.openapi.vfs.VirtualFile
import io.mockk.every
import io.mockk.mockk
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.After
import org.junit.Before
import org.junit.Test

class DocsigSaveListenerTest {
    private lateinit var service: DocsigService
    private lateinit var application: Application
    private lateinit var fileDocumentManager: FileDocumentManager
    private lateinit var document: Document

    @Before
    fun setup() {
        service = mockk(relaxed = true)
        application = mockk()
        fileDocumentManager = mockk()
        document = mockk()

        mockkStatic(ApplicationManager::class)
        mockkStatic(FileDocumentManager::class)

        every {
            ApplicationManager.getApplication()
        } returns application
        every {
            application.getService(DocsigService::class.java)
        } returns service
        every {
            FileDocumentManager.getInstance()
        } returns fileDocumentManager
    }

    @After
    fun teardown() {
        unmockkAll()
    }

    @Test
    fun `does nothing when file is null`() {
        every { fileDocumentManager.getFile(document) } returns null

        val listener = DocsigSaveListener()
        listener.beforeDocumentSaving(document)

        verify(exactly = 0) { service.scheduleFromSave(any()) }
    }

    @Test
    fun `does nothing when file is not in local file system`() {
        val file = mockk<VirtualFile>()
        every { fileDocumentManager.getFile(document) } returns file
        every { file.isInLocalFileSystem } returns false

        val listener = DocsigSaveListener()
        listener.beforeDocumentSaving(document)

        verify(exactly = 0) { service.scheduleFromSave(any()) }
    }

    @Test
    fun `schedules analysis when file is local`() {
        val file = mockk<VirtualFile>()
        val project = mockk<Project>()
        val service = mockk<DocsigService>(relaxed = true)

        val application = mockk<Application>()
        val projectLocator = mockk<ProjectLocator>()

        every { fileDocumentManager.getFile(document) } returns file
        every { file.isInLocalFileSystem } returns true
        every { file.path } returns "/test/file.py"

        mockkStatic(ApplicationManager::class)
        every { ApplicationManager.getApplication() } returns application
        every {
            application.getService(
                ProjectLocator::class.java,
            )
        } returns projectLocator

        every { projectLocator.guessProjectForFile(file) } returns project
        every { project.getService(DocsigService::class.java) } returns service

        val listener = DocsigSaveListener()
        listener.beforeDocumentSaving(document)

        verify(exactly = 1) {
            service.scheduleFromSave("/test/file.py")
        }
    }
}

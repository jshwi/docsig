package com.github.jshwi.docsig.listener

import com.github.jshwi.docsig.service.DocsigService
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.openapi.vfs.newvfs.events.VFileEvent
import io.mockk.every
import io.mockk.mockk
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.BeforeEach
import kotlin.test.Test

/**
 * Tests for [DocsigExternalChangeListener] forwarding external changes
 * to [DocsigService].
 */
class DocsigExternalChangeListenerTest {
    private lateinit var project: Project
    private lateinit var service: DocsigService

    @BeforeEach
    fun setup() {
        project = mockk()
        service = mockk(relaxed = true)

        every {
            project.getService(DocsigService::class.java)
        } returns service
    }

    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    private fun event(fromRefresh: Boolean, file: VirtualFile?): VFileEvent {
        val event = mockk<VFileEvent>()

        every { event.isFromRefresh } returns fromRefresh
        every { event.file } returns file

        return event
    }

    @Test
    fun `does nothing when event is not from refresh`() {
        val file = mockk<VirtualFile>()
        every { file.isInLocalFileSystem } returns true

        val listener = DocsigExternalChangeListener(project)
        listener.after(listOf(event(fromRefresh = false, file = file)))

        verify(exactly = 0) { service.invalidateExternalChange(any()) }
    }

    @Test
    fun `does nothing when event has no file`() {
        val listener = DocsigExternalChangeListener(project)
        listener.after(listOf(event(fromRefresh = true, file = null)))

        verify(exactly = 0) { service.invalidateExternalChange(any()) }
    }

    @Test
    fun `does nothing when file is not in local file system`() {
        val file = mockk<VirtualFile>()
        every { file.isInLocalFileSystem } returns false

        val listener = DocsigExternalChangeListener(project)
        listener.after(listOf(event(fromRefresh = true, file = file)))

        verify(exactly = 0) { service.invalidateExternalChange(any()) }
    }

    @Test
    fun `invalidates cache when local file changed externally`() {
        val file = mockk<VirtualFile>()
        every { file.isInLocalFileSystem } returns true
        every { file.path } returns "/test/file.py"

        val listener = DocsigExternalChangeListener(project)
        listener.after(listOf(event(fromRefresh = true, file = file)))

        verify(exactly = 1) {
            service.invalidateExternalChange("/test/file.py")
        }
    }
}

package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.messages.Notifications
import com.github.jshwi.docsig.models.Issue
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.openapi.Disposable
import com.intellij.openapi.application.Application
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.util.Condition
import com.intellij.openapi.vfs.LocalFileSystem
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.psi.PsiFile
import com.intellij.psi.PsiManager
import com.intellij.util.Alarm
import io.mockk.Runs
import io.mockk.every
import io.mockk.just
import io.mockk.mockk
import io.mockk.mockkObject
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import java.util.concurrent.CompletableFuture
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/**
 * Tests for [DocsigService] caching, merge rules, scheduling, and PSI refresh.
 */
class DocsigServiceTest {
    private val defaultAlarmFactory = DocsigService.alarmFactory

    private lateinit var project: Project
    private lateinit var application: Application

    @BeforeEach
    fun setup() {
        project =
            mockk(
                relaxed = true,
                moreInterfaces = arrayOf(Disposable::class),
            )
        application = mockk(relaxed = true)

        mockkStatic(ApplicationManager::class)
        every { ApplicationManager.getApplication() } returns application

        every {
            application.executeOnPooledThread(any())
        } answers {
            firstArg<Runnable>().run()
            CompletableFuture.completedFuture(null)
        }

        every {
            application.invokeLater(any<Runnable>(), any<Condition<*>>())
        } answers {
            firstArg<Runnable>().run()
        }

        DocsigService.alarmFactory = { immediateAlarm() }
    }

    @AfterEach
    fun teardown() {
        DocsigService.alarmFactory = defaultAlarmFactory
        unmockkAll()
    }

    @Test
    fun `hasCached reflects cache contents`() {
        val service = DocsigService(project)

        assertFalse(service.hasCached("/z.py"))

        putCache(service, "/z.py", emptyList())

        assertTrue(service.hasCached("/z.py"))
    }

    @Test
    fun `getIssues returns empty when path unknown`() {
        val service = DocsigService(project)

        assertTrue(service.getIssues("/no/such/path").isEmpty())
    }

    @Test
    fun `mergeIssues returns new issues when no global error`() {
        val service = DocsigService(project)
        putCache(
            service,
            "/a.py",
            listOf(Issue(1, "old", 1)),
        )

        val merged =
            invokeMergeIssues(
                service,
                "/a.py",
                listOf(Issue(2, "new", 1)),
            )

        assertEquals(
            listOf(Issue(2, "new", 1)),
            merged,
        )
    }

    @Test
    fun `mergeIssues keeps prior line issues when global error`() {
        val service = DocsigService(project)
        putCache(
            service,
            "/a.py",
            listOf(
                Issue(1, "stale line", 1),
                Issue(null, "old global", 2),
            ),
        )

        val merged =
            invokeMergeIssues(
                service,
                "/a.py",
                listOf(
                    Issue(null, "fresh global", 2),
                    Issue(9, "ignored line from cli", 1),
                ),
            )

        assertEquals(
            listOf(
                Issue(1, "stale line", 1),
                Issue(null, "fresh global", 2),
            ),
            merged,
        )
    }

    @Test
    fun `mergeIssues treats exit 2 with line as not global error`() {
        val service = DocsigService(project)

        val issues =
            listOf(
                Issue(3, "line error", 2),
            )

        assertEquals(
            issues,
            invokeMergeIssues(service, "/b.py", issues),
        )
    }

    @Test
    fun `mergeIssues global error drops line issues when cache empty`() {
        val service = DocsigService(project)

        val merged =
            invokeMergeIssues(
                service,
                "/z.py",
                listOf(
                    Issue(null, "global", 2),
                    Issue(5, "line", 1),
                ),
            )

        assertEquals(
            listOf(Issue(null, "global", 2)),
            merged,
        )
    }

    @Test
    fun `scheduleFromSave notifies when python interpreter missing`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns false
        val service = DocsigService(project)
        injectCli(service, cli)

        mockkObject(Notifications)
        every { Notifications.notifyMissingPython(project) } just Runs

        service.scheduleFromSave("/x.py")

        verify(exactly = 1) {
            Notifications.notifyMissingPython(project)
        }
        verify(exactly = 0) { cli.run(any()) }
    }

    @Test
    fun `ensureFresh notifies when python interpreter missing`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns false
        val service = DocsigService(project)
        injectCli(service, cli)

        mockkObject(Notifications)
        every { Notifications.notifyMissingPython(project) } just Runs

        service.ensureFresh("/x.py")

        verify(exactly = 1) {
            Notifications.notifyMissingPython(project)
        }
        verify(exactly = 0) { cli.run(any()) }
    }

    @Test
    fun `scheduleFromSave notifies when python version unsupported`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns false
        val service = DocsigService(project)
        injectCli(service, cli)

        mockkObject(Notifications)
        every {
            Notifications.notifyUnsupportedPython(project)
        } just Runs

        service.scheduleFromSave("/x.py")

        verify(exactly = 1) {
            Notifications.notifyUnsupportedPython(project)
        }
        verify(exactly = 0) { cli.run(any()) }
    }

    @Test
    fun `ensureFresh notifies when python version unsupported`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns false
        val service = DocsigService(project)
        injectCli(service, cli)

        mockkObject(Notifications)
        every {
            Notifications.notifyUnsupportedPython(project)
        } just Runs

        service.ensureFresh("/x.py")

        verify(exactly = 1) {
            Notifications.notifyUnsupportedPython(project)
        }
        verify(exactly = 0) { cli.run(any()) }
    }

    @Test
    fun `runDocsig skips when path already in flight`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run(any()) } returns emptyList()
        val service = DocsigService(project)
        injectCli(service, cli)

        val inFlight = inFlightSet(service)
        inFlight.add("/busy.py")

        invokeRunDocsig(service, "/busy.py")

        verify(exactly = 0) { cli.run(any()) }
    }

    @Test
    fun `runDocsig updates cache from cli`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every {
            cli.run("/c.py")
        } returns
            listOf(Issue(1, "m", 1))
        val service = DocsigService(project)
        injectCli(service, cli)

        mockPsiRefresh(project, vFile = null)

        invokeRunDocsig(service, "/c.py")

        assertEquals(
            listOf(Issue(1, "m", 1)),
            service.getIssues("/c.py"),
        )
    }

    @Test
    fun `runDocsig applies merge when cli returns global error`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every {
            cli.run("/d.py")
        } returnsMany
            listOf(
                listOf(Issue(null, "g", 2)),
                listOf(Issue(1, "line", 1)),
            )
        val service = DocsigService(project)
        injectCli(service, cli)

        mockPsiRefresh(project, vFile = null)

        invokeRunDocsig(service, "/d.py")
        invokeRunDocsig(service, "/d.py")

        assertEquals(
            listOf(Issue(1, "line", 1)),
            service.getIssues("/d.py"),
        )
    }

    @Test
    fun `notifyPsi restarts daemon when psi exists`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run("/f.py") } returns emptyList()
        val vFile = mockk<VirtualFile>()
        val psiFile = mockk<PsiFile>()
        val daemon = mockk<DaemonCodeAnalyzer>(relaxed = true)

        mockPsiRefresh(
            project,
            vFile = vFile,
            psiFile = psiFile,
            daemon = daemon,
        )

        val service = DocsigService(project)
        injectCli(service, cli)

        invokeRunDocsig(service, "/f.py")

        verify(exactly = 1) {
            daemon.restart(psiFile, "docsig")
        }
    }

    @Test
    fun `scheduleFromSave runs cli when available`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        val latch = CountDownLatch(1)
        every { cli.run("/g.py") } answers {
            latch.countDown()
            emptyList()
        }
        val service = DocsigService(project)
        injectCli(service, cli)

        mockPsiRefresh(project, vFile = null)

        service.scheduleFromSave("/g.py")

        assertTrue(latch.await(5, TimeUnit.SECONDS))
    }

    @Test
    fun `ensureFresh runs cli when available`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        val latch = CountDownLatch(1)
        every { cli.run("/h.py") } answers {
            latch.countDown()
            emptyList()
        }
        val service = DocsigService(project)
        injectCli(service, cli)

        mockPsiRefresh(project, vFile = null)

        service.ensureFresh("/h.py")

        assertTrue(latch.await(5, TimeUnit.SECONDS))
    }

    @Test
    fun `ensureFresh coalesces when idle alarm already has pending work`() {
        var cancelCalls = 0
        var requestCalls = 0
        var pending = false
        val alarm = trackingAlarm(
            onCancel = { cancelCalls += 1 },
            onAddRequest = { requestCalls += 1 },
            isPending = { pending },
            setPending = { pending = it },
        )

        DocsigService.alarmFactory = { alarm }

        val cli = mockk<Cli>(relaxed = true)
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run(any()) } returns emptyList()

        val service = DocsigService(project)
        injectCli(service, cli)

        service.ensureFresh("/i.py")
        service.ensureFresh("/i.py")

        assertEquals(0, cancelCalls)
        assertEquals(1, requestCalls)
    }

    @Test
    fun `scheduleAfterSettingsChange clears cache then runs cli`() {
        var pending = false
        val alarm = trackingAlarm(
            onCancel = {},
            onAddRequest = { pending = true },
            isPending = { pending },
            setPending = { pending = it },
        )

        DocsigService.alarmFactory = { alarm }

        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        val latch = CountDownLatch(1)
        every { cli.run("/cached.py") } answers {
            latch.countDown()
            emptyList()
        }
        val service = DocsigService(project)
        injectCli(service, cli)
        putCache(service, "/cached.py", listOf(Issue(1, "old", 1)))

        mockFileEditors(project, openPaths = emptyList())
        mockPsiRefresh(project, vFile = null)

        service.scheduleAfterSettingsChange()

        assertFalse(service.hasCached("/cached.py"))

        invokeRunDocsig(service, "/cached.py")

        assertTrue(latch.await(5, TimeUnit.SECONDS))
        assertTrue(service.hasCached("/cached.py"))
    }

    @Test
    fun `scheduleAfterSettingsChange includes open python files`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        val latch = CountDownLatch(1)
        every { cli.run("/open.py") } answers {
            latch.countDown()
            emptyList()
        }
        val service = DocsigService(project)
        injectCli(service, cli)

        mockFileEditors(project, openPaths = listOf("/open.py"))
        mockPsiRefresh(project, vFile = null)

        service.scheduleAfterSettingsChange()

        assertTrue(latch.await(5, TimeUnit.SECONDS))
    }

    @Test
    fun `scheduleAfterSettingsChange restarts daemon for cached paths`() {
        val cli = mockk<Cli>()
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run("/f.py") } returns emptyList()
        val vFile = mockk<VirtualFile>()
        val psiFile = mockk<PsiFile>()
        val daemon = mockk<DaemonCodeAnalyzer>(relaxed = true)

        mockFileEditors(project, openPaths = emptyList())
        mockPsiRefresh(
            project,
            vFile = vFile,
            psiFile = psiFile,
            daemon = daemon,
        )

        val service = DocsigService(project)
        injectCli(service, cli)
        putCache(service, "/f.py", listOf(Issue(1, "m", 1)))

        service.scheduleAfterSettingsChange()

        verify(atLeast = 1) {
            daemon.restart(psiFile, "docsig")
        }
    }

    @Test
    fun `invalidateExternalChange clears cache and restarts daemon`() {
        val vFile = mockk<VirtualFile>()
        val psiFile = mockk<PsiFile>()
        val daemon = mockk<DaemonCodeAnalyzer>(relaxed = true)

        mockPsiRefresh(
            project,
            vFile = vFile,
            psiFile = psiFile,
            daemon = daemon,
        )

        val service = DocsigService(project)
        putCache(service, "/ext.py", listOf(Issue(1, "old", 1)))

        service.invalidateExternalChange("/ext.py")

        assertFalse(service.hasCached("/ext.py"))
        verify(exactly = 1) {
            daemon.restart(psiFile, "docsig")
        }
    }

    @Test
    fun `invalidateExternalChange ignores paths without cached results`() {
        val daemon = mockk<DaemonCodeAnalyzer>(relaxed = true)

        mockPsiRefresh(
            project,
            vFile = mockk<VirtualFile>(),
            psiFile = mockk<PsiFile>(),
            daemon = daemon,
        )

        val service = DocsigService(project)

        service.invalidateExternalChange("/never/seen.py")

        verify(exactly = 0) { daemon.restart(any<PsiFile>(), any()) }
    }

    @Test
    fun `scheduleFromSave resets debounce timer before queueing work`() {
        var cancelCalls = 0
        var requestCalls = 0
        var pending = false
        val alarm = trackingAlarm(
            onCancel = { cancelCalls += 1 },
            onAddRequest = { requestCalls += 1 },
            isPending = { pending },
            setPending = { pending = it },
        )

        DocsigService.alarmFactory = { alarm }

        val cli = mockk<Cli>(relaxed = true)
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run(any()) } returns emptyList()

        val service = DocsigService(project)
        injectCli(service, cli)

        service.scheduleFromSave("/save.py")

        assertEquals(1, cancelCalls)
        assertEquals(1, requestCalls)
    }

    private fun injectCli(service: DocsigService, cli: Cli) {
        val field =
            DocsigService::class.java.getDeclaredField($$"cli$delegate")

        field.isAccessible = true
        field.set(service, lazyOf(cli))
    }

    private fun invokeMergeIssues(
        service: DocsigService,
        path: String,
        issues: List<Issue>,
    ): List<Issue> {
        val method =
            DocsigService::class.java.getDeclaredMethod(
                "mergeIssues",
                String::class.java,
                List::class.java,
            )

        method.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        return method.invoke(service, path, issues) as List<Issue>
    }

    private fun invokeRunDocsig(service: DocsigService, path: String) {
        val method =
            DocsigService::class.java.getDeclaredMethod(
                "runDocsig",
                String::class.java,
            )

        method.isAccessible = true
        method.invoke(service, path)
    }

    private fun putCache(
        service: DocsigService,
        path: String,
        issues: List<Issue>,
    ) {
        val field =
            DocsigService::class.java.getDeclaredField("cache")

        field.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        val cache =
            field.get(service) as MutableMap<String, List<Issue>>

        cache[path] = issues
    }

    private fun inFlightSet(service: DocsigService): MutableSet<String> {
        val field =
            DocsigService::class.java.getDeclaredField("inFlight")

        field.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        return field.get(service) as MutableSet<String>
    }

    private fun immediateAlarm(): Alarm {
        val alarm = mockk<Alarm>(relaxed = true)

        every { alarm.isEmpty } returns true
        every {
            alarm.addRequest(any<Runnable>(), any<Long>())
        } answers {
            firstArg<Runnable>().run()
        }

        return alarm
    }

    private fun trackingAlarm(
        onCancel: () -> Unit,
        onAddRequest: () -> Unit,
        isPending: () -> Boolean,
        setPending: (Boolean) -> Unit,
    ): Alarm {
        val alarm = mockk<Alarm>()

        every { alarm.isEmpty } answers { !isPending() }
        every { alarm.cancelAllRequests() } answers {
            onCancel()
            setPending(false)
            0
        }
        every {
            alarm.addRequest(any<Runnable>(), any<Long>())
        } answers {
            onAddRequest()
            setPending(true)
        }

        return alarm
    }

    private fun mockFileEditors(project: Project, openPaths: List<String>) {
        mockkStatic(FileEditorManager::class)
        val manager = mockk<FileEditorManager>()
        every { FileEditorManager.getInstance(project) } returns manager
        every { manager.openFiles } returns
            openPaths.map { filePath ->
                mockk<VirtualFile> {
                    every { isInLocalFileSystem } returns true
                    every { extension } returns "py"
                    every { path } returns filePath
                }
            }.toTypedArray()
    }

    private fun mockPsiRefresh(
        project: Project,
        vFile: VirtualFile?,
        psiFile: PsiFile? = null,
        daemon: DaemonCodeAnalyzer? = null,
    ) {
        mockkStatic(LocalFileSystem::class)
        val lfs = mockk<LocalFileSystem>()
        every { LocalFileSystem.getInstance() } returns lfs
        every { lfs.findFileByPath(any()) } returns vFile

        if (vFile != null && psiFile != null) {
            mockkStatic(PsiManager::class)
            val psiManager = mockk<PsiManager>()
            every { PsiManager.getInstance(project) } returns psiManager
            every { psiManager.findFile(vFile) } returns psiFile
        }

        if (daemon != null) {
            mockkStatic(DaemonCodeAnalyzer::class)
            every { DaemonCodeAnalyzer.getInstance(project) } returns daemon
        }
    }
}

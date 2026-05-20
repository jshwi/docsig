package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.notifications.Notifications
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.openapi.Disposable
import com.intellij.openapi.application.Application
import com.intellij.openapi.application.ApplicationManager
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
@Suppress("SameParameterValue")
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

        DocsigService.runScheduledWorkSynchronouslyForTests = true
    }

    @AfterEach
    fun teardown() {
        DocsigService.runScheduledWorkSynchronouslyForTests = false
        DocsigService.alarmFactory = defaultAlarmFactory
        DocsigService.cliFactory = { Cli(it) }
        AlarmAdapter.resetAlarmBuilderForTests()
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
        DocsigService.cliFactory = { cli }

        mockkObject(Notifications)
        every { Notifications.notifyMissingPython(project) } just Runs

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockkObject(Notifications)
        every { Notifications.notifyMissingPython(project) } just Runs

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockkObject(Notifications)
        every {
            Notifications.notifyUnsupportedPython(project)
        } just Runs

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockkObject(Notifications)
        every {
            Notifications.notifyUnsupportedPython(project)
        } just Runs

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockPsiRefresh(project, vFile = null)

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockPsiRefresh(project, vFile = null)

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

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
        DocsigService.cliFactory = { cli }

        mockPsiRefresh(project, vFile = null)

        val service = DocsigService(project)
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
        DocsigService.cliFactory = { cli }

        mockPsiRefresh(project, vFile = null)

        val service = DocsigService(project)
        service.ensureFresh("/h.py")

        assertTrue(latch.await(5, TimeUnit.SECONDS))
    }

    @Test
    fun `ensureFresh coalesces when idle alarm already has pending work`() {
        DocsigService.runScheduledWorkSynchronouslyForTests = false

        class FakeAlarm : AlarmLike {
            var cancelCalls = 0
            var requestCalls = 0
            private var pending = false

            override fun cancelAllRequests() {
                cancelCalls += 1
                pending = false
            }

            override fun addRequest(task: Runnable, delayMs: Long) {
                requestCalls += 1
                pending = true
            }

            override fun hasPendingRequests(): Boolean = pending
        }

        val fakeAlarm = FakeAlarm()
        DocsigService.alarmFactory = { fakeAlarm }

        val cli = mockk<Cli>(relaxed = true)
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run(any()) } returns emptyList()
        DocsigService.cliFactory = { cli }

        val service = DocsigService(project)
        service.ensureFresh("/i.py")
        service.ensureFresh("/i.py")

        assertEquals(0, fakeAlarm.cancelCalls)
        assertEquals(1, fakeAlarm.requestCalls)
    }

    @Test
    fun `scheduleFromSave resets debounce timer before queueing work`() {
        DocsigService.runScheduledWorkSynchronouslyForTests = false

        class FakeAlarm : AlarmLike {
            var cancelCalls = 0
            var requestCalls = 0
            private var pending = false

            override fun cancelAllRequests() {
                cancelCalls += 1
                pending = false
            }

            override fun addRequest(task: Runnable, delayMs: Long) {
                requestCalls += 1
                pending = true
            }

            override fun hasPendingRequests(): Boolean = pending
        }

        val fakeAlarm = FakeAlarm()
        DocsigService.alarmFactory = { fakeAlarm }

        val cli = mockk<Cli>(relaxed = true)
        every { cli.isAvailable() } returns true
        every { cli.isPythonSupported() } returns true
        every { cli.run(any()) } returns emptyList()
        DocsigService.cliFactory = { cli }

        val service = DocsigService(project)
        service.scheduleFromSave("/save.py")

        assertEquals(1, fakeAlarm.cancelCalls)
        assertEquals(1, fakeAlarm.requestCalls)
    }

    @Test
    fun `alarmFactory creates adapter that delegates to alarm`() {
        val alarm = mockk<Alarm>(relaxed = true)

        AlarmAdapter.alarmBuilder = { alarm }

        val adapter = DocsigService.alarmFactory(project)

        adapter.cancelAllRequests()
        adapter.addRequest({ }, 1L)

        verify(exactly = 1) { alarm.cancelAllRequests() }
        verify(exactly = 1) { alarm.addRequest(any<Runnable>(), 1L) }
    }

    @Test
    fun `alarm adapter constructs alarm via builder`() {
        var built = false

        AlarmAdapter.alarmBuilder = { _ ->
            built = true
            mockk(relaxed = true)
        }

        AlarmAdapter(project)

        assertTrue(built)
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

    private fun invokeRunDocsig(
        service: DocsigService,
        path: String,
    ) {
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

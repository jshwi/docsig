package com.github.jshwi.docsig.cli

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.application.PathManager
import com.intellij.openapi.module.Module
import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.projectRoots.Sdk
import com.intellij.openapi.roots.ProjectRootManager
import com.intellij.psi.util.CachedValueProvider
import com.intellij.psi.util.CachedValuesManager
import com.jetbrains.python.sdk.PythonSdkUtil
import io.mockk.every
import io.mockk.mockk
import io.mockk.mockkObject
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertThrows
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import java.nio.file.Files
import java.nio.file.Path
import java.util.UUID

class CliTest {
    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    private fun bindSettings(project: Project, settings: DocsigSettings) {
        every {
            project.getService(DocsigSettings::class.java)
        } returns settings
    }

    private fun mockCachedValuesManager(project: Project) {
        val valuesManager = mockk<CachedValuesManager>()
        val rootManager = mockk<ProjectRootManager>()

        mockkStatic(CachedValuesManager::class)
        mockkStatic(ProjectRootManager::class)

        every { CachedValuesManager.getManager(project) } returns valuesManager
        every { ProjectRootManager.getInstance(project) } returns rootManager

        every {
            valuesManager.getCachedValue(
                project,
                any<CachedValueProvider<*>>(),
            )
        } answers {
            val provider = secondArg<CachedValueProvider<*>>()
            provider.compute()!!.value
        }
    }

    private fun subprocess(
        out: String = "",
        exit: Int = 0,
    ): Subprocess.Result = Subprocess.Result(exit, out)

    private fun mockSubprocess(body: (List<String>) -> Subprocess.Result) {
        mockkObject(Subprocess)

        every { Subprocess.run(any(), any()) } answers { body(firstArg()) }
    }

    private fun mockSubprocessSkippingVersionCheck(
        runDocsig: (List<String>) -> Subprocess.Result,
    ) {
        mockkObject(Subprocess)

        every { Subprocess.run(any(), any()) } answers {
            val cmd = firstArg<List<String>>()

            if (cmd.getOrNull(1) == "-c") {
                subprocess()
            } else {
                runDocsig(cmd)
            }
        }
    }

    private fun stubBasePath(project: Project, basePath: String? = null) {
        every { project.basePath } returns basePath
    }

    private fun cli(
        project: Project,
        interpreter: String?,
        versionSupported: Boolean = true,
    ): Cli {
        stubBasePath(project)

        val python = mockk<Python>()

        every { python.path() } returns interpreter

        every { python.meetsMinimumVersion() } returns
            (interpreter != null && versionSupported)

        every { python.versionSupported(any()) } returns versionSupported

        return Cli(project, python)
    }

    @Test
    fun `run returns empty list when unavailable`() {
        val project = mockk<Project>()

        val result = cli(project, null).run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run returns empty list when output empty`() {
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess { subprocess() }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run parses json issues`() {
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess {
            subprocess(
                """[{"message":"bad","line":1,"exit":1}]""".trimIndent(),
            )
        }

        val result = cli(project, "python").run("test.py")

        assertEquals(1, result.size)

        val issue = result.first()

        assertEquals("bad", issue.message)
        assertEquals(1, issue.line)
        assertEquals(1, issue.exit)
    }

    @Test
    fun `run parses json issues carrying an unknown path field`() {
        // the docsig cli attaches a per-entry "path" key the Issue model
        // does not declare; without ignoreUnknown jackson throws and the
        // run is dropped, leaving the editor with no diagnostics
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess {
            subprocess(
                """[{"path":"/x/test.py","message":"bad","line":1,"exit":1}]"""
                    .trimIndent(),
            )
        }

        val result = cli(project, "python").run("test.py")

        assertEquals(1, result.size)

        val issue = result.first()

        assertEquals("bad", issue.message)
        assertEquals(1, issue.line)
        assertEquals(1, issue.exit)
    }

    @Test
    fun `run returns empty list on invalid json`() {
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess { subprocess("not json") }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `isAvailable returns false`() {
        val project = mockk<Project>()

        assertEquals(
            false,
            cli(project, null).isAvailable(),
        )
    }

    @Test
    fun `isAvailable returns true`() {
        val project = mockk<Project>()

        assertEquals(
            true,
            cli(project, "python").isAvailable(),
        )
    }

    @Test
    fun `isPythonSupported returns false when version too old`() {
        val project = mockk<Project>()

        assertEquals(
            false,
            cli(project, "python", versionSupported = false)
                .isPythonSupported(),
        )
    }

    @Test
    fun `isPythonSupported returns true when version ok`() {
        val project = mockk<Project>()

        assertEquals(
            true,
            cli(project, "python", versionSupported = true)
                .isPythonSupported(),
        )
    }

    @Test
    fun `run returns empty list when python version unsupported`() {
        val project = mockk<Project>()

        mockSubprocess {
            error("subprocess must not run when python is unsupported")
        }

        val result =
            cli(project, "python", versionSupported = false).run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run starts real process for python version`() {
        val result = Subprocess.run(listOf("python3", "--version"))

        assertEquals(0, result.exit)
        assertTrue(result.out.isNotEmpty())
    }

    @Test
    fun `run trims output`() {
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess {
            subprocess(
                """
                []
                """.trimIndent(),
            )
        }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run handles non zero exit`() {
        val project = mockk<Project>()

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockSubprocess { subprocess("[]", exit = 1) }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run executes full command path`() {
        val project = mockk<Project>()

        stubBasePath(project)

        mockCachedValuesManager(project)

        val settings =
            mockk<DocsigSettings>(
                relaxed = true,
            )

        val module = mockk<Module>()

        val sdk = mockk<Sdk>()

        val moduleManager =
            mockk<ModuleManager>()

        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every {
            project.locationHash
        } returns "test"

        every {
            moduleManager.modules
        } returns arrayOf(module)

        every {
            ModuleManager.getInstance(project)
        } returns moduleManager

        every {
            PythonSdkUtil.findPythonSdk(module)
        } returns sdk

        every {
            sdk.homePath
        } returns "python3"

        bindSettings(project, settings)

        mockSubprocessSkippingVersionCheck { cmd ->
            assertEquals(
                "python3",
                cmd.first(),
            )

            subprocess("[]")
        }

        val result =
            Cli(project).run(
                "test.py",
            )

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run returns empty when no python sdk`() {
        val project = mockk<Project>()

        stubBasePath(project)

        mockCachedValuesManager(project)

        bindSettings(project, mockk<DocsigSettings>(relaxed = true))

        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        val moduleManager = mockk<ModuleManager>()

        every {
            ModuleManager.getInstance(project)
        } returns moduleManager

        every {
            moduleManager.modules
        } returns emptyArray()

        mockSubprocess {
            error("subprocess must not run when command is empty")
        }

        val result = Cli(project).run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run extracts bundled cli when cache missing`(
        @TempDir tempDir: Path,
    ) {
        val project = mockk<Project>()

        stubBasePath(project)

        mockCachedValuesManager(project)

        val settings =
            mockk<DocsigSettings>(
                relaxed = true,
            )

        val module = mockk<Module>()

        val sdk = mockk<Sdk>()

        val moduleManager =
            mockk<ModuleManager>()

        mockkStatic(PathManager::class)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every {
            PathManager.getSystemPath()
        } returns tempDir.toString()

        every {
            project.locationHash
        } returns "extract-${UUID.randomUUID()}"

        every {
            moduleManager.modules
        } returns arrayOf(module)

        every {
            ModuleManager.getInstance(project)
        } returns moduleManager

        every {
            PythonSdkUtil.findPythonSdk(module)
        } returns sdk

        every {
            sdk.homePath
        } returns "python3"

        bindSettings(project, settings)

        val cached = tempDir.resolve("docsig.pyz")

        Files.createDirectories(cached.parent)
        Files.deleteIfExists(cached)

        mockSubprocessSkippingVersionCheck { cmd ->
            assertEquals(
                "python3",
                cmd.first(),
            )

            assertEquals(
                cached.toString(),
                cmd[1],
            )

            subprocess("[]")
        }

        val result =
            Cli(project).run(
                "test.py",
            )

        assertTrue(result.isEmpty())
        assertTrue(Files.exists(cached))
    }

    @Test
    fun `run throws when bundled pyz stream is absent`(
        @TempDir tempDir: Path,
    ) {
        val project = mockk<Project>()

        stubBasePath(project)

        mockCachedValuesManager(project)

        val settings =
            mockk<DocsigSettings>(
                relaxed = true,
            )

        val module = mockk<Module>()

        val sdk = mockk<Sdk>()

        val moduleManager =
            mockk<ModuleManager>()

        mockkStatic(PathManager::class)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every {
            PathManager.getSystemPath()
        } returns tempDir.toString()

        every {
            project.locationHash
        } returns "missing-stream-${UUID.randomUUID()}"

        every {
            moduleManager.modules
        } returns arrayOf(module)

        every {
            ModuleManager.getInstance(project)
        } returns moduleManager

        every {
            PythonSdkUtil.findPythonSdk(module)
        } returns sdk

        every {
            sdk.homePath
        } returns "python3"

        bindSettings(project, settings)

        val cached = tempDir.resolve("docsig.pyz")

        Files.createDirectories(cached.parent)
        Files.deleteIfExists(cached)

        mockkObject(Executable)

        every { Executable.path() } answers {
            error("missing bundled cli")
        }

        mockSubprocessSkippingVersionCheck { _ ->
            error(
                "subprocess must not run docsig when bundled cli is absent",
            )
        }

        val thrown =
            assertThrows(IllegalStateException::class.java) {
                Cli(project).run(
                    "test.py",
                )
            }

        assertTrue(
            thrown.message!!.contains("missing bundled cli"),
        )
    }

    @Test
    fun `run reads process stdout as utf-8 and trims`() {
        val result =
            Subprocess.run(
                listOf(
                    "python3",
                    "-c",
                    "print('  []  ')",
                ),
            )

        assertEquals(0, result.exit)
        assertEquals("[]", result.out)
    }
}

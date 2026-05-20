package com.github.jshwi.docsig.cli

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.application.PathManager
import com.intellij.openapi.module.Module
import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.projectRoots.Sdk
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
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import java.io.ByteArrayInputStream
import java.nio.file.Files
import java.nio.file.Path
import java.util.UUID
import kotlin.text.Charsets

class CliTest {
    @BeforeEach
    fun setup() {
        Python.cacheBypassForTests = true
    }

    @AfterEach
    fun teardown() {
        Python.cacheBypassForTests = false

        Subprocess.processFactory = Subprocess::defaultProcessFactory
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
        Executable.bundledPyzStreamProvider = null

        unmockkAll()
    }

    private fun cli(
        project: Project,
        interpreter: String?,
        versionSupported: Boolean = true,
    ): Cli {
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

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        Subprocess.processFactory = {
            process("", 0)
        }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run parses json issues`() {
        val project = mockk<Project>()

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        Subprocess.processFactory = {
            process(
                """[{"message":"bad","line":1,"exit":1}]""".trimIndent(),
                0,
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

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        Subprocess.processFactory = {
            process("not json", 0)
        }

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

        Subprocess.processFactory = {
            error("processFactory must not run when python is unsupported")
        }

        val result =
            cli(project, "python", versionSupported = false).run("test.py")

        assertTrue(result.isEmpty())
    }

    private fun process(
        output: String,
        exit: Int,
    ): Process {
        val process = mockk<Process>()

        every {
            process.inputStream
        } returns ByteArrayInputStream(output.toByteArray())

        every {
            process.waitFor()
        } returns exit

        return process
    }

    private fun processFactorySkippingVersionCheck(
        runDocsig: (List<String>) -> Process,
    ): (List<String>) -> Process = { cmd ->
        if (cmd.getOrNull(1) == "-c") {
            process("", 0)
        } else {
            runDocsig(cmd)
        }
    }

    @Test
    fun `defaultProcessFactory returns process`() {
        val process =
            Subprocess.defaultProcessFactory(
                listOf(
                    "python3",
                    "--version",
                ),
            )

        process.waitFor()

        assertEquals(0, process.exitValue())
    }

    @Test
    fun `run trims output`() {
        val project = mockk<Project>()

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        Subprocess.processFactory = {
            process(
                """
                []
                """.trimIndent(),
                0,
            )
        }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run handles non zero exit`() {
        val project = mockk<Project>()

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        Subprocess.processFactory = {
            process(
                "[]",
                1,
            )
        }

        val result = cli(project, "python").run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run executes full command path`() {
        val project = mockk<Project>()

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

        DocsigSettings.settingsProvider = {
            settings
        }

        Subprocess.processFactory =
            processFactorySkippingVersionCheck { cmd ->
                assertEquals(
                    "python3",
                    cmd.first(),
                )

                process(
                    "[]",
                    0,
                )
            }

        val result =
            Cli(project).run(
                "test.py",
            )

        assertTrue(result.isEmpty())
    }

    @Test
    fun `defaultSettingsProvider returns project DocsigSettings`() {
        val project = mockk<Project>()

        val settings = mockk<DocsigSettings>()

        every {
            project.getService(DocsigSettings::class.java)
        } returns settings

        assertEquals(
            settings,
            DocsigSettings.defaultSettingsProvider(project),
        )
    }

    @Test
    fun `run returns empty when no python sdk`() {
        val project = mockk<Project>()

        DocsigSettings.settingsProvider = {
            mockk<DocsigSettings>(relaxed = true)
        }

        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        val moduleManager = mockk<ModuleManager>()

        every {
            ModuleManager.getInstance(project)
        } returns moduleManager

        every {
            moduleManager.modules
        } returns emptyArray()

        Subprocess.processFactory = {
            error("processFactory must not run when command is empty")
        }

        val result = Cli(project).run("test.py")

        assertTrue(result.isEmpty())
    }

    @Test
    fun `run extracts bundled cli when cache missing`(
        @TempDir tempDir: Path,
    ) {
        val project = mockk<Project>()

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

        DocsigSettings.settingsProvider = {
            settings
        }

        val cached = tempDir.resolve("docsig.pyz")

        Files.createDirectories(cached.parent)
        Files.deleteIfExists(cached)

        Subprocess.processFactory =
            processFactorySkippingVersionCheck { cmd ->
                assertEquals(
                    "python3",
                    cmd.first(),
                )

                assertEquals(
                    cached.toString(),
                    cmd[1],
                )

                process(
                    "[]",
                    0,
                )
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

        DocsigSettings.settingsProvider = {
            settings
        }

        val cached = tempDir.resolve("docsig").resolve("docsig.pyz")

        Files.createDirectories(cached.parent)
        Files.deleteIfExists(cached)

        Executable.bundledPyzStreamProvider = { null }

        Subprocess.processFactory =
            processFactorySkippingVersionCheck { _ ->
                error(
                    "processFactory must not run docsig when " +
                        "bundled cli is absent",
                )
            }

        val thrown =
            assertThrows(IllegalStateException::class.java) {
                Cli(project).run(
                    "test.py",
                )
            }

        assertTrue(
            thrown.message!!.contains("missing bundled cli resource"),
        )
    }

    @Test
    fun `Subprocess run reads process stdout as utf-8 and trims`() {
        Subprocess.processFactory = { _ ->
            mockk<Process>().apply {
                every {
                    inputStream
                } returns
                    ByteArrayInputStream(
                        """
                        []
                        """.trimIndent().toByteArray(Charsets.UTF_8),
                    )

                every {
                    waitFor()
                } returns 0
            }
        }

        val result = Subprocess.run(listOf("x"))

        assertEquals("[]", result.out)
    }
}

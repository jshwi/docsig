package com.github.jshwi.docsig.cli

import com.intellij.openapi.project.Project
import io.mockk.every
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.TestInstance
import java.io.ByteArrayInputStream
import java.nio.charset.StandardCharsets
import kotlin.test.Test
import kotlin.test.assertEquals

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class CliTest {
    val project = mockk<Project>(relaxed = true)

    @BeforeEach
    fun setup() {
        Cli.settingsProvider = {
            mockk(relaxed = true) {
                every { state.cliPath } returns "docsig"
            }
        }
    }

    @AfterEach
    fun tearDown() {
        Cli.settingsProvider = {
            error("settingsProvider not mocked")
        }
    }

    private fun mockProcess(stdout: String, exitCode: Int = 0): Process {
        val process = mockk<Process>(relaxed = true)

        every { process.inputStream } returns
            ByteArrayInputStream(
                stdout.toByteArray(StandardCharsets.UTF_8),
            )

        every { process.waitFor() } returns exitCode

        return process
    }

    @Test
    fun `returns parsed issues on valid json output`() {
        val json =
            """
[
    {
        "line":103,
        "message":"SIG101: function is missing a docstring (function-doc-...)",
        "exit":1
    }
]
            """.trimIndent()

        Cli.processFactory = { _ ->
            mockProcess(json, 0)
        }

        val result = Cli.run(project, "/tmp/file.py")

        assertEquals(1, result.size)
    }

    @Test
    fun `returns empty list when CLI outputs empty string`() {
        Cli.processFactory = { _ ->
            mockProcess("", 0)
        }

        val result = Cli.run(project, "/tmp/file.py")

        assertEquals(0, result.size)
    }

    @Test
    fun `returns empty list when JSON is invalid`() {
        Cli.processFactory = { _ ->
            mockProcess("not-json", 0)
        }

        val result = Cli.run(project, "/tmp/file.py")

        assertEquals(0, result.size)
    }

    @Test
    fun `returns empty list even if CLI exits with error`() {
        Cli.processFactory = { _ ->
            mockProcess("[]", 1)
        }

        val result = Cli.run(project, "/tmp/file.py")

        assertEquals(0, result.size)
    }

    @Test
    fun `processFactory receives correct command structure`() {
        var captured: List<String>? = null

        Cli.processFactory = { cmd ->
            captured = cmd
            mockProcess("[]")
        }

        val result = Cli.run(project, "/tmp/file.py")

        Assertions.assertNotNull(captured)
        Assertions.assertTrue(captured!!.contains("/tmp/file.py"))
    }
}

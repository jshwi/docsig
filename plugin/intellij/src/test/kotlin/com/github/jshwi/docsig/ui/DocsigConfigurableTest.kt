package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.model.Version
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import java.io.ByteArrayInputStream
import java.io.InputStream
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

class DocsigConfigurableTest {
    private var fakeProcess: Process? = null

    @BeforeEach
    fun setup() {
        Cli.processFactory = { fakeProcess!! }
    }

    @AfterEach
    fun tearDown() {
        Cli.processFactory = { args ->
            ProcessBuilder(args).start()
        }
    }

    @Test
    fun `isValidExecutable returns true when marker present and exit 0`() {
        fakeProcess =
            FakeProcess(
                "Check signature params for proper documentation",
                0,
            )

        val c = DocsigConfigurable()

        val result =
            c.invokePrivate<Boolean>(
                "isValidExecutable",
                "/bin/docsig",
            )

        assertTrue(result)
    }

    @Test
    fun `isValidExecutable returns false when marker missing`() {
        fakeProcess =
            FakeProcess(
                "something else",
                0,
            )

        val c = DocsigConfigurable()

        val result =
            c.invokePrivate<Boolean>(
                "isValidExecutable",
                "/bin/docsig",
            )

        assertFalse(result)
    }

    @Test
    fun `isValidExecutable returns false when exit code non-zero`() {
        fakeProcess =
            FakeProcess(
                "Check signature params for proper documentation",
                1,
            )

        val c = DocsigConfigurable()

        val result =
            c.invokePrivate<Boolean>(
                "isValidExecutable",
                "/bin/docsig",
            )

        assertFalse(result)
    }

    @Test
    fun `getExecutableVersion parses valid version`() {
        fakeProcess =
            FakeProcess(
                "docsig version 0.84.1",
                0,
            )

        val c = DocsigConfigurable()

        val version =
            c.invokePrivate<Version?>(
                "getExecutableVersion",
                "/bin/docsig",
            )

        assertEquals("0.84.1", version.toString())
    }

    @Test
    fun `getExecutableVersion returns null when version missing`() {
        fakeProcess =
            FakeProcess(
                "no version here",
                0,
            )

        val c = DocsigConfigurable()

        val version =
            c.invokePrivate<Version?>(
                "getExecutableVersion",
                "/bin/docsig",
            )

        assertNull(version)
    }
}

/**
 * Fake process used for CLI output simulation.
 */
private class FakeProcess(
    private val output: String,
    private val exitCode: Int,
) : Process() {
    private val input =
        ByteArrayInputStream(output.toByteArray())

    override fun getInputStream(): InputStream = input

    override fun getErrorStream(): InputStream = input

    override fun getOutputStream() = throw UnsupportedOperationException()

    override fun waitFor(): Int = exitCode

    override fun exitValue(): Int = exitCode

    override fun destroy() {}
}

/**
 * Reflection helper for private methods.
 */
@Suppress("UNCHECKED_CAST")
private fun <T> Any.invokePrivate(name: String, vararg args: Any?): T {
    val method =
        this::class.java.declaredMethods.first { it.name == name }

    method.isAccessible = true
    return method.invoke(this, *args) as T
}

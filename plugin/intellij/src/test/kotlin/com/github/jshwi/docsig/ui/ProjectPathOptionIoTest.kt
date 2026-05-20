package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project
import io.mockk.every
import io.mockk.mockk
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertNull
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import java.nio.file.Path
import java.nio.file.Paths

/**
 * Tests for [ProjectPathOptionIo] storage vs argv resolution.
 */
class ProjectPathOptionIoTest {
    private val io = ProjectPathOptionIo()

    @Test
    fun `fromInput maps paths under base to relative`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        val rel = io.fromInput(project, "./this/path")

        assertEquals("this/path", rel!!.replace('\\', '/'))
    }

    @Test
    fun `toOutput resolves relative stored paths against base`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        val abs = io.toOutput(project, "this/path")

        assertEquals(
            tempDir.resolve(
                "this/path",
            ).toAbsolutePath().normalize().toString(),
            Path.of(abs).toAbsolutePath().normalize().toString(),
        )
    }

    @Test
    fun `toInput returns stored unchanged`() {
        val project = mockk<Project>(relaxed = true)

        assertEquals(
            "rel/path",
            io.toInput(project, "rel/path"),
        )
    }

    @Test
    fun `fromInput returns null for blank input`() {
        val project = mockk<Project>(relaxed = true)

        assertNull(io.fromInput(project, "   "))
    }

    @Test
    fun `fromInput normalizes backslashes when base path missing`() {
        val project = mockk<Project>()
        every { project.basePath } returns null

        assertEquals(
            "a/b",
            io.fromInput(project, "a\\b"),
        )
    }

    @Test
    fun `fromInput relativizes absolute paths under base`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        val absolute =
            tempDir.resolve("foo/bar").toAbsolutePath().normalize().toString()

        val stored = io.fromInput(project, absolute)

        assertEquals("foo/bar", stored)
    }

    @Test
    fun `fromInput keeps input when resolved path is outside base`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        val stored = io.fromInput(project, "../outside")

        assertEquals("../outside", stored)
    }

    @Test
    fun `toOutput returns empty for blank stored path`() {
        val project = mockk<Project>(relaxed = true)

        assertEquals("", io.toOutput(project, "  "))
    }

    @Test
    fun `toOutput resolves against cwd when base path missing`() {
        val project = mockk<Project>()
        every { project.basePath } returns null

        val expected =
            Paths.get("relative")
                .toAbsolutePath()
                .normalize()
                .toString()
                .replace('\\', '/')

        assertEquals(
            expected,
            io.toOutput(project, "relative"),
        )
    }

    @Test
    fun `toOutput normalizes absolute stored paths`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        val stored =
            tempDir.resolve("sub\\dir")
                .toAbsolutePath()
                .normalize()
                .toString()

        val cli = io.toOutput(project, stored)

        assertEquals(
            Path.of(stored).normalize().toString().replace('\\', '/'),
            cli,
        )
    }

    @Test
    fun `maps stored paths for argv and panel`(
        @TempDir tempDir: Path,
    ) {
        val base = tempDir.toAbsolutePath().normalize().toString()
        val project = mockk<Project>()
        every { project.basePath } returns base

        assertEquals(
            tempDir.resolve("a").toAbsolutePath().normalize().toString(),
            io.toOutput(project, "a"),
        )
        assertEquals("x", io.fromInput(project, "./x"))
    }
}

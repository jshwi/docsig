package com.github.jshwi.docsig.cli

import com.intellij.openapi.application.PathManager
import io.mockk.every
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import java.nio.file.Files
import java.nio.file.Path

class ExecutableTest {
    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    @Test
    fun `path extracts bundled cli when cache missing`(
        @TempDir tempDir: Path,
    ) {
        mockSystemPath(tempDir)

        val cached = tempDir.resolve("docsig.pyz")

        assertTrue(Files.notExists(cached))

        val path = Executable.path()

        assertEquals(cached.toString(), path)
        assertTrue(Files.isRegularFile(cached))
        assertTrue(Files.size(cached) > 0L)
    }

    @Test
    fun `path replaces stale cached bundle`(@TempDir tempDir: Path) {
        mockSystemPath(tempDir)

        val cached = tempDir.resolve("docsig.pyz")

        Files.writeString(cached, "broken")

        val path = Executable.path()

        assertEquals(cached.toString(), path)
        assertTrue(Files.size(cached) > "broken".length.toLong())
    }

    @Test
    fun `path reuses valid cached bundle`(@TempDir tempDir: Path) {
        mockSystemPath(tempDir)

        val cached = tempDir.resolve("docsig.pyz")

        val first = Executable.path()
        val modified = Files.getLastModifiedTime(cached)
        val second = Executable.path()

        assertEquals(first, second)
        assertEquals(modified, Files.getLastModifiedTime(cached))
    }

    private fun mockSystemPath(tempDir: Path) {
        mockkStatic(PathManager::class)

        every {
            PathManager.getSystemPath()
        } returns tempDir.toString()
    }
}
